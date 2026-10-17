# c:\temp\pgmcp\mcp_server\core\decorators\tool_error_handler_decorator.py
# template=generic version=f35abd82 created=2026-06-19T22:03Z updated=
"""ToolErrorHandlerDecorator module.

Outermost decorator that traps unhandled exceptions and converts them to error DTOs.

@layer: Backend (Decorators)
@dependencies: [mcp_server.core.interfaces.itool, pydantic]
@responsibilities:
    - Trap unhandled exceptions and return ExecutionErrorOutput DTO
    - Trap ConfigError and return ConfigErrorOutput DTO
"""

# Standard library
import logging
from typing import Any, Generic, TypeVar

# Third-party
from pydantic import BaseModel

# Project modules
from mcp_server.core.error_handling import capture_exception
from mcp_server.core.interfaces.itool import ITool
from mcp_server.core.interfaces.tool_input_contract import JsonObject
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_execution import ToolExecution
from mcp_server.schemas.error_outputs import ConfigErrorOutput, ExecutionErrorOutput

logger = logging.getLogger(__name__)


TOutput = TypeVar("TOutput", bound=BaseModel)


class ToolErrorHandlerDecorator(
    ITool[TOutput | ConfigErrorOutput | ExecutionErrorOutput],
    Generic[TOutput],  # noqa: UP046 -- Preserve invariant wrapper contract; reassess in #513.
):
    """Outermost decorator that traps unhandled exceptions and converts them to error DTOs."""

    def __init__(self, inner_tool: ITool[TOutput]) -> None:
        self._inner_tool = inner_tool

    @property
    def name(self) -> str:
        return self._inner_tool.name

    @property
    def description(self) -> str:
        return self._inner_tool.description

    @property
    def args_model(self) -> type[BaseModel] | None:
        return self._inner_tool.args_model

    @property
    def tool_category(self) -> str | None:
        return getattr(self._inner_tool, "tool_category", None)

    @property
    def enforcement_event(self) -> str:
        return getattr(self._inner_tool, "enforcement_event", self.name)

    @property
    def input_schema(self) -> dict[str, Any]:
        return self._inner_tool.input_schema

    async def execute(
        self, params: JsonObject, context: NoteContext
    ) -> ToolExecution[TOutput | ConfigErrorOutput | ExecutionErrorOutput]:
        try:
            return await self._inner_tool.execute(params, context)
        except Exception as exc:
            logger.error(
                "Unhandled exception during tool execution for %s: %s",
                self.name,
                str(exc),
                exc_info=True,
            )
            return ToolExecution(
                operation=capture_exception(exc, params=params),
                attachments=(),
            )
