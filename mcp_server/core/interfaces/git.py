# c:\temp\pgmcp\mcp_server\core\interfaces\git.py
# template=interface version=3fb28c28 created=2026-06-20T18:31:11Z updated=
"""IGitContextReader module.

Read-only git context for the current branch.

@layer: Backend (Contracts)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class BranchChanges:
    """Tracked and untracked paths introduced relative to a branch parent."""

    current_paths: tuple[str, ...]
    removed_paths: tuple[str, ...]


@runtime_checkable
class IBranchChangeReader(Protocol):
    """Read branch changes without exposing broader Git context operations."""

    def get_current_branch(self) -> str:
        raise NotImplementedError

    def get_branch_changes(self, parent: str) -> BranchChanges:
        raise NotImplementedError


@runtime_checkable
class IGitContextReader(Protocol):
    """Read-only git context for the current branch."""

    def get_current_branch(self) -> str:
        raise NotImplementedError

    def get_recent_commits(self, limit: int = 5) -> list[str]:
        raise NotImplementedError

    def get_status(self) -> dict[str, Any]:
        raise NotImplementedError


@runtime_checkable
class IBranchParentReader(Protocol):
    """Read the parent branch for a given branch from persisted state."""

    def get_parent_branch(self, branch: str) -> str | None:
        raise NotImplementedError
