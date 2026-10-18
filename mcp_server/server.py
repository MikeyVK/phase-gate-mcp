# pyright: reportMissingImports=false
"""MCP Server Entrypoint."""

import asyncio
import time
import uuid
from pathlib import Path
from typing import Any, cast

from mcp.server import Server, ServerRequestContext
from mcp.server.stdio import stdio_server
from mcp.shared.exceptions import MCPError
from mcp.types import (
    CallToolRequestParams,
    CallToolResult,
    ListResourcesResult,
    ListToolsResult,
    PaginatedRequestParams,
    ReadResourceRequestParams,
    ReadResourceResult,
    Resource,
    TextContent,
    TextResourceContents,
    Tool,
)
from pydantic import BaseModel

# Config
from mcp_server.config.settings import Settings

# Resources
# Resources
# Scaffolding infrastructure (Issue #72)
from mcp_server.core.decorators import InputValidationDecorator, ToolErrorHandlerDecorator
from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.interfaces.ipresenter import IPresenter
from mcp_server.core.interfaces.itool import ITool
from mcp_server.core.interfaces.itool_response_cache import IToolResponsePublisher
from mcp_server.core.logging import get_logger
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_execution import operation_output_model
from mcp_server.resources.base import BaseResource
from mcp_server.schemas.presentation_output import PresentedOutput
from mcp_server.schemas.startup_diagnostic import StartupDiagnostic

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
        tools: list[ITool],
        resources: list[BaseResource],
        presenter: IPresenter | None = None,
        publisher: IToolResponsePublisher | None = None,
    ) -> None:
        """Initialize the MCP server with resources and tools."""
        self._settings = settings
        self.presenter = presenter
        self.response_cache_manager = publisher
        self.resources = resources
        self.tools = tools

        self.setup_handlers()

    def _convert_tool_result_to_mcp_result(self, result: ToolResult) -> CallToolResult:
        """Convert ToolResult to CallToolResult while preserving error semantics."""
        return convert_tool_result_to_mcp_result(result)

    def setup_handlers(self) -> None:
        """Set up the MCP protocol handlers."""

        async def handle_list_resources(
            _ctx: ServerRequestContext[None], _params: PaginatedRequestParams | None
        ) -> ListResourcesResult:
            return ListResourcesResult(
                resources=[
                    Resource(
                        uri=r.uri_pattern,
                        name=r.uri_pattern.rsplit("/", maxsplit=1)[-1],
                        description=r.description,
                        mime_type=r.mime_type,
                    )
                    for r in self.resources
                ]
            )

        async def handle_read_resource(
            _ctx: ServerRequestContext[None], params: ReadResourceRequestParams
        ) -> ReadResourceResult:
            uri = params.uri
            try:
                for resource in self.resources:
                    if resource.matches(uri):
                        return ReadResourceResult(
                            contents=[
                                TextResourceContents(
                                    uri=uri, mime_type="text/plain", text=await resource.read(uri)
                                )
                            ]
                        )
                raise ValueError(f"Resource not found: {uri}")
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # noqa: BLE001 — terminal SDK boundary preserves the cause
                raise MCPError(code=0, message=str(exc)) from exc

        async def handle_list_tools(
            _ctx: ServerRequestContext[None], _params: PaginatedRequestParams | None
        ) -> ListToolsResult:
            tools_list = []
            for t in self.tools:
                output_schema = None
                if hasattr(t, "output_model") and getattr(t, "output_model", None) is not None:
                    output_schema = operation_output_model(t.output_model).model_json_schema()
                tools_list.append(
                    Tool(
                        name=t.name,
                        description=t.description,
                        input_schema=t.input_schema,
                        output_schema=output_schema,
                    )
                )
            return ListToolsResult(tools=tools_list)

        async def handle_call_tool(
            _ctx: ServerRequestContext[None], params: CallToolRequestParams
        ) -> CallToolResult:
            name, arguments = params.name, params.arguments
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

                        # 1. Execute the normalized pipeline; cache only the operation.
                        execution = await tool.execute(arguments or {}, note_context)
                        result_dto = execution.operation

                        # 2. Publish result to cache (resilient; returns None on failure)
                        cache_pub = None
                        if self.response_cache_manager is not None:
                            cache_pub = self.response_cache_manager.put(tool.name, result_dto)

                        # 3. Generate presentation output (formats DTO, notes, resources)
                        if self.presenter is not None:
                            presented = self.presenter.present(
                                tool_name=tool.name,
                                data=result_dto,
                                notes=note_context.entries,
                                cache_pub=cache_pub,
                                attachments=execution.attachments,
                            )
                        else:
                            presented = PresentedOutput(text=str(result_dto), resources=[])

                        # 4. Construct and return normalized ToolResult
                        content: list[dict[str, Any]] = [{"type": "text", "text": presented.text}]
                        for res in presented.resources:
                            content.append(
                                {
                                    "type": "resource",
                                    "resource": {
                                        "uri": res.uri,
                                        "mimeType": res.mime_type,
                                        "text": res.content,
                                    },
                                }
                            )

                        success = getattr(result_dto, "success", True)
                        raw_result = ToolResult(content=content, is_error=not success)
                        response_content = self._convert_tool_result_to_mcp_result(raw_result)

                        response_content.structured_content = result_dto.model_dump(
                            mode="json", by_alias=True
                        )

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
                        return CallToolResult(
                            content=[
                                TextContent(
                                    type="text", text=f"Error processing tool response: {e!s}"
                                )
                            ],
                            is_error=True,
                        )
            return CallToolResult(
                content=[TextContent(type="text", text=f"Tool not found: {name}")],
                is_error=True,
            )

        self.server = Server[None](
            self._settings.server.name,
            on_list_resources=handle_list_resources,
            on_read_resource=handle_read_resource,
            on_list_tools=handle_list_tools,
            on_call_tool=handle_call_tool,
        )

    async def run(self) -> None:
        """Run the MCP server."""
        server_name = self._settings.server.name

        logger.info("Starting MCP server: %s", server_name)
        lifecycle_logger.info("MCP server running")

        try:
            async with stdio_server() as (read_stream, write_stream):
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


class DegradedMCPServer(MCPServer):
    """Compose only diagnostic and retry tools after recognized startup rejection."""

    def __init__(
        self, settings: Settings, diagnostic: StartupDiagnostic, presenter: IPresenter
    ) -> None:
        """Keep recovery independent of rejected configuration and template admission."""
        from mcp_server.schemas.tool_outputs import (  # noqa: PLC0415
            HealthCheckOutput,
            RestartServerOutput,
        )
        from mcp_server.tools.admin_tools import RestartServerTool  # noqa: PLC0415
        from mcp_server.tools.health_tools import HealthCheckTool  # noqa: PLC0415

        health_tool = HealthCheckTool(settings, diagnostic)
        restart_tool = RestartServerTool(server_root=Path(settings.server.resolved_server_root))
        super().__init__(
            settings=settings,
            tools=[
                ToolErrorHandlerDecorator(
                    InputValidationDecorator[HealthCheckOutput](
                        cast(ICoreTool[BaseModel, HealthCheckOutput], health_tool)
                    )
                ),
                ToolErrorHandlerDecorator(
                    InputValidationDecorator[RestartServerOutput](
                        cast(ICoreTool[BaseModel, RestartServerOutput], restart_tool)
                    )
                ),
            ],
            resources=[],
            presenter=presenter,
            publisher=None,
        )
