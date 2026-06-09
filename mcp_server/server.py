# pyright: reportMissingImports=false
"""MCP Server Entrypoint."""

import asyncio
import json
import sys
import time
import uuid
from io import TextIOWrapper
from pathlib import Path
from typing import Any, cast

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
from pydantic import AnyUrl, BaseModel, ValidationError

# Config
from mcp_server.bootstrap import ConfigLayer, ManagerGraph
from mcp_server.config.settings import Settings
from mcp_server.core.exceptions import MCPError
from mcp_server.core.logging import get_logger
from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.enforcement_runner import EnforcementContext
from mcp_server.resources.base import BaseResource

# Resources
# Scaffolding infrastructure (Issue #72)
from mcp_server.tools.base import BaseTool

# Tools
from mcp_server.tools.phase_tools import (
    TRANSITION_ADVISORY_NOTE,
)
from mcp_server.tools.tool_result import ToolResult

logger = get_logger("server")
lifecycle_logger = get_logger("server_lifecycle")

TRANSITION_ADVISORY_TOOL_NAMES = {
    "transition_phase",
    "force_phase_transition",
    "transition_cycle",
    "force_cycle_transition",
}


class MCPServer:
    """Main MCP server class that handles resources and tools."""

    def __init__(
        self,
        settings: Settings,
        configs: ConfigLayer,
        managers: ManagerGraph,
        tools: list[BaseTool],
        resources: list[BaseResource],
    ) -> None:
        """Initialize the MCP server with resources and tools."""
        self._settings = settings
        self._configs = configs
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

        self.server = Server(server_name)
        self.resources = resources
        self.tools = tools

        self.setup_handlers()

    def _validate_tool_arguments(
        self, tool: BaseTool, arguments: dict[str, Any] | None, call_id: str, name: str
    ) -> BaseModel | dict[str, Any] | ToolResult:
        """Validate tool arguments against args_model.

        Returns:
            - Validated BaseModel instance if validation succeeds
            - Raw arguments dict if no args_model
            - ToolResult with is_error=True if validation fails
        """
        if not getattr(tool, "args_model", None):
            return arguments or {}

        model_cls = cast(type[BaseModel], tool.args_model)
        logger.debug(
            "Validating tool arguments",
            extra={
                "props": {
                    "call_id": call_id,
                    "tool_name": name,
                    "model": model_cls.__name__,
                }
            },
        )
        try:
            model_validated = model_cls(**(arguments or {}))
            logger.debug(
                "Arguments validated successfully",
                extra={
                    "props": {
                        "call_id": call_id,
                        "tool_name": name,
                    }
                },
            )
            return model_validated
        except ValidationError as validation_error:
            logger.warning(
                "Argument validation failed: %s",
                validation_error,
                extra={
                    "props": {
                        "call_id": call_id,
                        "tool_name": name,
                        "model": model_cls.__name__,
                        "arguments": arguments,
                    }
                },
            )
            error_details = str(validation_error)
            return ToolResult(
                content=[
                    {"type": "text", "text": f"Invalid input for {name}: {error_details}"},
                    {
                        "type": "resource",
                        "resource": {
                            "uri": "schema://validation",
                            "mimeType": "application/json",
                            "text": json.dumps(tool.input_schema),
                        },
                    },
                ],
                is_error=True,
            )

    def _convert_tool_result_to_content(
        self, result: ToolResult
    ) -> list[TextContent | ImageContent | EmbeddedResource]:
        """Convert ToolResult to MCP content list."""
        response_content: list[TextContent | ImageContent | EmbeddedResource] = []

        for content in result.content:
            if content.get("type") == "text":
                text = content["text"]
                response_content.append(TextContent(type="text", text=text))
            elif content.get("type") == "json":
                response_content.append(
                    TextContent(
                        type="text",
                        text=json.dumps(content["json"], indent=2, default=str),
                    )
                )
            elif content.get("type") == "image":
                response_content.append(
                    ImageContent(type="image", data=content["data"], mimeType=content["mimeType"])
                )
            elif content.get("type") == "resource":
                response_content.append(
                    EmbeddedResource(type="resource", resource=content["resource"])
                )

        return response_content

    def _convert_tool_result_to_mcp_result(self, result: ToolResult) -> CallToolResult:
        """Convert ToolResult to CallToolResult while preserving error semantics."""
        return CallToolResult(
            content=self._convert_tool_result_to_content(result),
            isError=result.is_error,
        )

    def _run_tool_enforcement(
        self,
        tool: BaseTool,
        timing: str,
        params: BaseModel | dict[str, Any],
        note_context: NoteContext,
        result: ToolResult | None = None,
    ) -> ToolResult | None:
        """Execute pre/post enforcement for one tool when configured."""
        event = getattr(tool, "enforcement_event", None)
        tool_category = getattr(tool, "tool_category", None)
        if event is None and tool_category is None:
            return None

        enforcement_ctx = EnforcementContext(
            workspace_root=self._workspace_root,
            tool_name=tool.name,
            params=params,
            tool_result=result,
        )
        try:
            self.enforcement_runner.run(
                event=event or "",
                timing=timing,
                tool_category=tool_category,
                enforcement_ctx=enforcement_ctx,
                note_context=note_context,
            )
        except MCPError as exc:
            if timing == "post" and tool.name in TRANSITION_ADVISORY_TOOL_NAMES:
                note_context.discard_info_message(TRANSITION_ADVISORY_NOTE)
            base = ToolResult.error(message=exc.message, error_code=exc.code)
            return note_context.render_to_response(base)
        return None

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
            for resource in self.resources:
                if resource.matches(uri):
                    return await resource.read(uri)
            raise ValueError(f"Resource not found: {uri}")

        @self.server.list_tools()  # type: ignore[no-untyped-call, untyped-decorator]
        async def handle_list_tools() -> list[Tool]:
            return [
                Tool(name=t.name, description=t.description, inputSchema=t.input_schema)
                for t in self.tools
            ]

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
                        # Validate arguments
                        validated = self._validate_tool_arguments(tool, arguments, call_id, name)
                        # Early return if validation failed
                        if isinstance(validated, ToolResult):
                            return self._convert_tool_result_to_mcp_result(validated)

                        note_context = NoteContext()

                        pre_result = self._run_tool_enforcement(
                            tool, "pre", validated, note_context=note_context
                        )
                        if pre_result is not None:
                            return self._convert_tool_result_to_mcp_result(pre_result)

                        # Execute tool
                        raw_result = await tool.execute(validated, note_context)

                        if not raw_result.is_error:
                            post_result = self._run_tool_enforcement(
                                tool,
                                "post",
                                validated,
                                note_context=note_context,
                                result=raw_result,
                            )
                            if post_result is not None:
                                return self._convert_tool_result_to_mcp_result(post_result)

                        # Render notes and convert result to MCP content
                        result = note_context.render_to_response(raw_result)
                        response_content = self._convert_tool_result_to_mcp_result(result)

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
                    except (KeyError, AttributeError, TypeError) as e:
                        # Response processing error (dict access, attribute access, type issues)
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
    settings = settings or Settings.from_env()
    server = MCPServer(settings=settings)
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
