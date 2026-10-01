# c:\temp\pgmcp\mcp_server\core\interfaces\itool.py
# template=interface version=3fb28c28 created=2026-06-19T21:33Z updated=
"""ITool module.

Interface for outer untyped dictionary tool execution.

@layer: Backend (Contracts)
"""

# Standard library
from typing import Any, Generic, Protocol, runtime_checkable

# Third-party
from pydantic import BaseModel
from typing_extensions import TypeVar

from mcp_server.core.interfaces.tool_input_contract import JsonObject

# Project modules
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_execution import ToolExecution

TOutput_co = TypeVar("TOutput_co", bound=BaseModel, covariant=True, default=BaseModel)


@runtime_checkable
class ITool(Protocol, Generic[TOutput_co]):
    """Interface for outer untyped dictionary tool execution."""

    @property
    def name(self) -> str:
        """Name of the tool."""
        ...

    @property
    def description(self) -> str:
        """Description of the tool."""
        ...

    @property
    def args_model(self) -> type[BaseModel] | None:
        """Args model of the tool."""
        ...

    @property
    def input_schema(self) -> dict[str, Any]:
        """Input schema of the tool."""
        ...

    async def execute(self, params: JsonObject, context: NoteContext) -> ToolExecution[TOutput_co]:
        """Execute the contract operation."""
        ...
