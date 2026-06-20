# mcp_server/core/interfaces/ipresenter.py
# template=interface version=3fb28c28 created=2026-06-19T22:33Z updated=
"""IPresenter module.

Interface for translating execution results and notes into markdown.

@layer: Backend (Contracts)
"""

# Standard library
from typing import Protocol, runtime_checkable

# Third-party
from pydantic import BaseModel

# Project modules
from mcp_server.core.operation_notes import Note


@runtime_checkable
class IPresenter(Protocol):
    """Interface for translating execution results and notes into markdown."""

    def present(
        self,
        tool_name: str,
        data: BaseModel,
        notes: list[Note],
        run_id: str | None = None,
    ) -> str:
        """Format the output DTO and operation notes into a single user-facing markdown string."""
        ...
