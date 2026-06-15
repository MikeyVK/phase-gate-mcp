"""Base interfaces and envelopes for MCP tools.

@layer: Backend (Tools)
"""

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel

from mcp_server.core.operation_notes import NoteContext


@dataclass(frozen=True)
class ToolExecutionEnvelope:
    """Envelope containing the pure domain DTO and orchestration metadata."""

    run_id: str
    data: BaseModel
    presentation_context: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class ITool(Protocol):
    """Protocol for the new MVP tool architecture."""

    @property
    def name(self) -> str: ...

    @property
    def description(self) -> str: ...

    @property
    def args_model(self) -> type[BaseModel] | None: ...

    async def execute(self, params: Any, context: NoteContext) -> ToolExecutionEnvelope | BaseModel:  # noqa: ANN401
        """Execute the tool and return either a ToolExecutionEnvelope or a pure BaseModel."""
        ...
