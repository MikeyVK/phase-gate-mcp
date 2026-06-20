# c:\temp\pgmcp\mcp_server\core\interfaces\icore_tool.py
# template=interface version=3fb28c28 created=2026-06-19T21:33Z updated=
"""ICoreTool module.

New ICoreTool generic interface.

@layer: Backend (Contracts)
"""

# Standard library
from typing import Generic, Protocol, TypeVar, runtime_checkable

# Third-party
from pydantic import BaseModel

# Project modules
from mcp_server.core.operation_notes import NoteContext

TInput = TypeVar("TInput", bound=BaseModel, contravariant=True)
TOutput = TypeVar("TOutput", bound=BaseModel, covariant=True)


@runtime_checkable
class ICoreTool(Protocol, Generic[TInput, TOutput]):
    """Generic interface for typed core tool execution."""

    @property
    def name(self) -> str:
        """Name of the tool."""
        ...

    @property
    def description(self) -> str:
        """Description of the tool."""
        ...

    @property
    def args_model(self) -> type[BaseModel] | None: ...

    async def execute(self, params: TInput, context: NoteContext) -> TOutput:
        """Execute the contract operation."""
        ...
