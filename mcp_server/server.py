# pyright: reportMissingImports=false
"""MCP Server Entrypoint."""

import asyncio
import json
import sys
import time
import uuid
from io import TextIOWrapper
from pathlib import Path
from typing import Any

import anyio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolResult,
    EmbeddedResource,
    ImageContent,
    Resource,
    TextContent,
    Tool,
)
from pydantic import AnyUrl

# Config
from mcp_server.bootstrap import ConfigLayer, ManagerGraph
from mcp_server.config.settings import Settings
from mcp_server.core.logging import get_logger
from mcp_server.core.operation_notes import NoteContext
from mcp_server.presenters.text_presenter import TextPresenter, SafeNoneFormatter
from mcp_server.resources.base import BaseResource

# Resources
# Resources
# Scaffolding infrastructure (Issue #72)
from mcp_server.core.interfaces.itool import ITool
from mcp_server.core.interfaces.itool_response_cache import IToolResponsePublisher

# Tools
from mcp_server.tools.tool_result import ToolResult
from mcp_server.utils.mcp_converters import (
    convert_tool_result_to_mcp_result,
)

logger = get_logger("server")
lifecycle_logger = get_logger("server_lifecycle")


class MCPServer:
    """Main MCP server class that handles resources and tools."""

    def __init__(
        self,
        settings: Settings,
        configs: ConfigLayer,
        managers: ManagerGraph,
        tools: list[ITool],
        resources: list[BaseResource],
        presenter: TextPresenter | None = None,
        publisher: IToolResponsePublisher | None = None,
    ) -> None:
        """Initialize the MCP server with resources and tools."""
        self._settings = settings
        self._configs = configs
        self.presenter = presenter
        server_name = settings.server.name
        workspace_root = Path(settings.server.workspace_root)

        self._workspace_root = workspace_root
        self.template_registry = managers.template_registry
        self.git_manager = managers.git_manager
        self._state_repository = managers.state_repository
        self.workflow_status_resolver = managers.workflow_status_resolver
        self.project_manager = managers.project_manager
        self.phase_contract_resolver = managers.phase_contract_resolver
        self.workflow_gate_runner = managers.workflow_gate_runner
        self.state_reconstructor = managers.state_reconstructor
        self._workflow_state_mutator = managers.workflow_state_mutator
        self._context_loaded_cache = managers.context_loaded_cache
        self.phase_state_engine = managers.phase_state_engine
        self.qa_manager = managers.qa_manager
        self.github_manager = managers.github_manager
        self.artifact_manager = managers.artifact_manager
        self.pr_status_cache = managers.pr_status_cache
        self.enforcement_runner = managers.enforcement_runner
        self.response_cache_manager = publisher

        self.server = Server(server_name)
        self.resources = resources
        self.tools = tools

        self.setup_handlers()

    def _convert_tool_result_to_mcp_result(self, result: ToolResult) -> CallToolResult:
        """Convert ToolResult to CallToolResult while preserving error semantics."""
        return convert_tool_result_to_mcp_result(result)

    def setup_handlers(self) -> None:
        """Set up the MCP protocol handlers."""

        @self.server.list_resources()  # type: ignore[no-untyped-call, untyped-decorator]
        async def handle_list_resources() -> list[Resource]:
            return [
                Resource(
                    uri=AnyUrl(r.uri_pattern),
                    name=r.uri_pattern.rsplit("/", maxsplit=1)[-1],
                    description=r.description,
                    mimeType=r.mime_type,
                )
                for r in self.resources
            ]

        @self.server.read_resource()  # type: ignore[no-untyped-call, untyped-decorator]
        async def handle_read_resource(uri: str) -> str:
            uri_str = str(uri)
            for resource in self.resources:
                if resource.matches(uri_str):
                    return await resource.read(uri_str)
            raise ValueError(f"Resource not found: {uri_str}")

        @self.server.list_tools()  # type: ignore[no-untyped-call, untyped-decorator]
        async def handle_list_tools() -> list[Tool]:
            tools_list = []
            for t in self.tools:
                output_schema = None
                if hasattr(t, "output_model") and getattr(t, "output_model", None) is not None:
                    output_schema = t.output_model.model_json_schema()
                tools_list.append(
                    Tool(
                        name=t.name,
                        description=t.description,
                        inputSchema=t.input_schema,
                        outputSchema=output_schema,
                    )
                )
            return tools_list

        @self.server.call_tool()  # type: ignore[untyped-decorator]
        async def handle_call_tool(
            name: str, arguments: dict[str, Any] | None
        ) -> CallToolResult | list[TextContent | ImageContent | EmbeddedResource]:
            call_id = uuid.uuid4().hex
            start_time = time.perf_counter()
            argument_keys = sorted((arguments or {}).keys())

            logger.debug(
                "Tool call received",
                extra={
                    "props": {
                        "call_id": call_id,
                        "tool_name": name,
                        "argument_keys": argument_keys,
                    }
                },
            )

            for tool in self.tools:
                if tool.name == name:
                    try:
                        note_context = NoteContext()

                        # 1. Execute target tool (guaranteed to return a BaseModel DTO)
                        result_dto = await tool.execute(arguments or {}, note_context)

                        # 2. Publish result to cache (resilient; returns None on failure)
                        run_id = None
                        if self.response_cache_manager is not None:
                            run_id = self.response_cache_manager.put(tool.name, result_dto)

                        # 3. Generate markdown output (resilient; formats DTO and notes)
                        if self.presenter is not None:
                            markdown = self.presenter.present(
                                tool_name=tool.name,
                                data=result_dto,
                                notes=note_context.entries,
                                run_id=run_id,
                            )
                        else:
                            markdown = str(result_dto)

                        # Check if cache URI needs to be appended
                        if run_id and "pgmcp://cache/runs/" not in markdown:
                            uri_ref_tmpl = None
                            if self.presenter is not None:
                                uri_ref_tmpl = self.presenter.get_next_instruction_texts().get(
                                    "uri_reference"
                                )
                            if uri_ref_tmpl and self.presenter is not None:
                                try:
                                    none_val = self.presenter.get_none_value()
                                    formatter = SafeNoneFormatter(none_val)
                                    uri_text = formatter.format(uri_ref_tmpl, run_id=run_id)
                                except Exception:
                                    uri_text = uri_ref_tmpl.format(run_id=run_id)
                            else:
                                uri_text = (
                                    "*(Full details available in the structured JSON payload. "
                                    f"View resource: pgmcp://cache/runs/{run_id})*"
                                )
                            markdown = f"{markdown}\n\n{uri_text}"

                        # 4. Construct and return normalized ToolResult
                        raw_result = ToolResult.text(markdown)

                        # In case result DTO indicates an error, flag the ToolResult as an error
                        success = getattr(result_dto, "success", True)
                        if not success:
                            raw_result = raw_result.model_copy(update={"is_error": True})
                            if getattr(result_dto, "error_type", None) == "ValidationError":
                                raw_result.content.append(
                                    {
                                        "type": "resource",
                                        "resource": {
                                            "uri": "schema://validation",
                                            "mimeType": "application/json",
                                            "text": json.dumps(tool.input_schema),
                                        },
                                    }
                                )
                        response_content = self._convert_tool_result_to_mcp_result(raw_result)

                        duration_ms = (time.perf_counter() - start_time) * 1000.0
                        logger.debug(
                            "Tool call completed",
                            extra={
                                "props": {
                                    "call_id": call_id,
                                    "tool_name": name,
                                    "duration_ms": duration_ms,
                                }
                            },
                        )
                        return response_content
                    except asyncio.CancelledError:
                        duration_ms = (time.perf_counter() - start_time) * 1000.0
                        logger.info(
                            "Tool call cancelled",
                            extra={
                                "props": {
                                    "call_id": call_id,
                                    "tool_name": name,
                                    "duration_ms": duration_ms,
                                }
                            },
                        )
                        raise
                    except Exception as e:
                        duration_ms = (time.perf_counter() - start_time) * 1000.0
                        logger.error(
                            "Response processing failed: %s",
                            e,
                            exc_info=True,
                            extra={
                                "props": {
                                    "call_id": call_id,
                                    "tool_name": name,
                                    "duration_ms": duration_ms,
                                    "error_type": type(e).__name__,
                                }
                            },
                        )
                        return [
                            TextContent(type="text", text=f"Error processing tool response: {e!s}")
                        ]
            raise ValueError(f"Tool not found: {name}")

    async def run(self) -> None:
        """Run the MCP server."""
        server_name = self._settings.server.name

        logger.info("Starting MCP server: %s", server_name)
        lifecycle_logger.info("MCP server running")

        # Force LF only on Windows to prevent "invalid trailing data"
        # and other CRLF issues in the JSON-RPC stream
        stdout = anyio.wrap_file(TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="\n"))

        try:
            async with stdio_server(stdout=stdout) as (read_stream, write_stream):
                await self.server.run(
                    read_stream, write_stream, self.server.create_initialization_options()
                )
        except KeyboardInterrupt:
            lifecycle_logger.info("MCP server interrupted by user")
        finally:
            lifecycle_logger.info("MCP server shutting down")

    async def shutdown(self) -> None:
        """Shutdown the MCP server gracefully."""
        lifecycle_logger.info("MCP server shutting down")


def main(settings: Settings | None = None) -> None:
    """Entry point for the MCP server."""
    from mcp_server.bootstrap import ServerBootstrapper  # noqa: PLC0415

    settings = settings or Settings.from_env()
    bootstrapper = ServerBootstrapper(settings)
    server = bootstrapper.bootstrap()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
