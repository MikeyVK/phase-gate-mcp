# pyright: reportMissingImports=false
"""MCP Server Entrypoint."""

import asyncio
import json
import sys
import time
import traceback
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
from mcp_server.presenters.text_presenter import TextPresenter
from mcp_server.resources.base import BaseResource

# Resources
# Resources
# Scaffolding infrastructure (Issue #72)
from mcp_server.tools.base import ITool

# Tools
from mcp_server.tools.phase_tools import (
    TRANSITION_ADVISORY_NOTE,
)
from mcp_server.tools.tool_result import ToolResult
from mcp_server.schemas.error_outputs import (
    ValidationErrorOutput,
    EnforcementErrorOutput,
    ExecutionErrorOutput,
    CacheErrorOutput,
)
from mcp_server.utils.mcp_converters import (
    convert_tool_result_to_content,
    convert_tool_result_to_mcp_result,
)

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
        tools: list[ITool],
        resources: list[BaseResource],
        presenter: TextPresenter | None = None,
    ) -> None:
        """Initialize the MCP server with resources and tools."""
        self._settings = settings
        self._configs = configs
        self.presenter = presenter
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
        self.response_cache = getattr(managers, "response_cache", None)
        self.response_cache_manager = self.response_cache

        self.server = Server(server_name)
        self.resources = resources
        self.tools = tools

        self.setup_handlers()

    def _validate_tool_arguments(
        self, tool: ITool, arguments: dict[str, Any] | None, call_id: str, name: str
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

    async def _handle_error_dto(
        self,
        tool: ITool,
        err_dto: BaseModel,
        start_time: float,
        call_id: str,
        note_context: NoteContext | None = None,
    ) -> CallToolResult:
        run_id = uuid.uuid4().hex
        cache_error_occurred = False
        cache_err_message = ""

        # 1. Try to cache the error DTO
        if self.response_cache is not None:
            try:
                self.response_cache.put(f"pgmcp://cache/runs/{run_id}", err_dto)
            except Exception as cache_exc:
                cache_error_occurred = True
                cache_err_message = str(cache_exc)

        # 2. Present the DTO
        if cache_error_occurred:
            # Wrap as CacheErrorOutput
            cache_dto = CacheErrorOutput(
                message=cache_err_message,
                params={
                    "original_error": err_dto.message
                    if hasattr(err_dto, "message")
                    else str(err_dto)
                },
            )
            # Format using plain text directly (double fault prevention)
            text = f"CacheError: {cache_dto.message}"
            raw_result = ToolResult(content=[{"type": "text", "text": text}], is_error=True)
            return self._convert_tool_result_to_mcp_result(raw_result)

        # Present the original error DTO
        if self.presenter is not None:
            text = self.presenter.present(
                tool_name=tool.name,
                success=False,
                presentation_category="query",
                data=err_dto,
            )
        else:
            text = str(err_dto)

        uri = f"pgmcp://cache/runs/{run_id}"
        full_text = f"{text}\n\nJSON data for this run is available as an MCP Resource: {uri}"

        content: list[Any] = [{"type": "text", "text": full_text}]
        if isinstance(err_dto, ValidationErrorOutput):
            content.append(
                {
                    "type": "resource",
                    "resource": {
                        "uri": "schema://validation",
                        "mimeType": "application/json",
                        "text": json.dumps(tool.input_schema),
                    },
                }
            )

        # Append notes if any
        if note_context is not None and self.presenter is not None:
            notes = note_context.entries
            if notes:
                notes_text = self.presenter.present_notes(tool.name, notes)
                if notes_text:
                    content.append({"type": "text", "text": notes_text})

        raw_result = ToolResult(content=content, is_error=True)

        duration_ms = (time.perf_counter() - start_time) * 1000.0
        logger.debug(
            "Tool call completed with error",
            extra={
                "props": {
                    "call_id": call_id,
                    "tool_name": tool.name,
                    "duration_ms": duration_ms,
                    "error_type": type(err_dto).__name__,
                }
            },
        )
        return self._convert_tool_result_to_mcp_result(raw_result)

    def _convert_tool_result_to_content(
        self, result: ToolResult
    ) -> list[TextContent | ImageContent | EmbeddedResource]:
        """Convert ToolResult to MCP content list."""
        return convert_tool_result_to_content(result.content)

    def _convert_tool_result_to_mcp_result(self, result: ToolResult) -> CallToolResult:
        """Convert ToolResult to CallToolResult while preserving error semantics."""
        return convert_tool_result_to_mcp_result(result)

    def _run_tool_enforcement(
        self,
        tool: ITool,
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
        self.enforcement_runner.run(
            event=event or "",
            timing=timing,
            tool_category=tool_category,
            enforcement_ctx=enforcement_ctx,
            note_context=note_context,
        )

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

                        try:
                            # Validate arguments
                            validated = self._validate_tool_arguments(
                                tool, arguments, call_id, name
                            )
                        except ValidationError as val_exc:
                            err_dto = ValidationErrorOutput(
                                message=f"Invalid input for {name}",
                                validation_errors=val_exc.errors(),
                                input_schema=tool.input_schema,
                                params=arguments or {},
                            )
                            return await self._handle_error_dto(tool, err_dto, start_time, call_id)

                        try:
                            self._run_tool_enforcement(
                                tool, "pre", validated, note_context=note_context
                            )
                        except MCPError as exc:
                            logger.error(
                                "Enforcement check failed: exc=%r, code=%r, params=%r",
                                exc,
                                getattr(exc, "code", None),
                                getattr(exc, "params", None),
                            )
                            err_dto = EnforcementErrorOutput(
                                message=exc.message,
                                error_code=exc.code,
                                params=exc.params or {},
                            )
                            return await self._handle_error_dto(
                                tool, err_dto, start_time, call_id, note_context
                            )

                        # Execute tool
                        try:
                            raw_result = await tool.execute(validated, note_context)
                        except Exception as exec_exc:
                            if isinstance(exec_exc, asyncio.CancelledError):
                                raise
                            err_dto = ExecutionErrorOutput(
                                message=str(exec_exc),
                                traceback=traceback.format_exc(),
                                params=arguments or {},
                            )
                            return await self._handle_error_dto(
                                tool, err_dto, start_time, call_id, note_context
                            )

                        from mcp_server.tools.base import ToolExecutionEnvelope  # noqa: PLC0415

                        if isinstance(raw_result, ToolExecutionEnvelope):
                            data_dto = raw_result.data
                            run_id = raw_result.run_id
                        else:
                            data_dto = raw_result
                            run_id = "test-run"

                        if self.presenter is not None:
                            success = getattr(data_dto, "success", True)
                            presentation_category = (
                                getattr(tool, "presentation_category", None) or "query"
                            )
                            text = self.presenter.present(
                                tool_name=tool.name,
                                success=success,
                                presentation_category=presentation_category,
                                data=data_dto,
                            )
                        else:
                            text = str(data_dto)
                        uri = f"pgmcp://cache/runs/{run_id}"
                        full_text = (
                            f"{text}\n\n"
                            f"JSON data for this run is available as an MCP Resource: {uri}"
                        )
                        raw_result = ToolResult.text(full_text)

                        if not raw_result.is_error:
                            try:
                                self._run_tool_enforcement(
                                    tool,
                                    "post",
                                    validated,
                                    note_context=note_context,
                                    result=raw_result,
                                )
                            except MCPError as exc:
                                if tool.name in TRANSITION_ADVISORY_TOOL_NAMES:
                                    note_context.discard_info_message(TRANSITION_ADVISORY_NOTE)
                                err_dto = EnforcementErrorOutput(
                                    message=exc.message,
                                    error_code=exc.code,
                                    params=exc.params or {},
                                )
                                return await self._handle_error_dto(
                                    tool, err_dto, start_time, call_id, note_context
                                )

                        # Retrieve and format operation notes (decoupled)
                        notes = note_context.entries
                        if self.presenter is not None and notes:
                            notes_text = self.presenter.present_notes(tool.name, notes)
                            if notes_text:
                                augmented = list(raw_result.content) + [
                                    {"type": "text", "text": notes_text}
                                ]
                                raw_result = raw_result.model_copy(update={"content": augmented})

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
                    except (KeyError, AttributeError, TypeError) as e:
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
