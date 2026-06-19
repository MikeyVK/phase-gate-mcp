# c:\temp\pgmcp\mcp_server\core\interfaces\itool.py
# template=interface version=3fb28c28 created=2026-06-19T21:33Z updated=
"""ITool module.

Interface for outer untyped dictionary tool execution.

@layer: Backend (Contracts)
"""

# Standard library
from typing import Any, Protocol, runtime_checkable

# Third-party
from pydantic import BaseModel

# Project modules
from mcp_server.core.operation_notes import NoteContext


@runtime_checkable
class ITool(Protocol):
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

    async def execute(self, params: dict[str, Any], context: NoteContext) -> BaseModel:
        """Execute the contract operation."""
        ...
