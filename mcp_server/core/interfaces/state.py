# c:\temp\pgmcp\mcp_server\core\interfaces\state.py
# template=interface version=3fb28c28 created=2026-06-20T18:28:18Z updated=
"""IStateReader module.

Read-only access to persisted branch state.

@layer: Backend (Contracts)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from mcp_server.managers.state_repository import BranchState


class IStateReader(Protocol):
    """Read-only access to the single current branch registration."""

    def load(self, branch: str) -> BranchState:
        """Return current valid state, even when it names another branch.

        Raise StateNotFoundError only for genuine absence. Invalid or unreadable
        source propagates its diagnosis without source or backup mutation.
        Branch-specific authorization uses a separate exact-branch reader.
        """
        raise NotImplementedError


class IStateRepository(IStateReader, Protocol):
    """Read-write access to the single current branch registration."""

    def save(self, state: BranchState) -> None:
        """Validate complete field data and replace the current registration."""
        raise NotImplementedError
