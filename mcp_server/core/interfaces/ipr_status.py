# c:\temp\pgmcp\mcp_server\core\interfaces\ipr_status.py
# template=interface version=3fb28c28 created=2026-06-20T18:29:20Z updated=
"""IPRStatusReader module.

Read the cached PR status for a branch.

@layer: Backend (Contracts)
"""

from __future__ import annotations

from enum import Enum
from typing import Protocol, runtime_checkable


class PRStatus(Enum):
    """Lifecycle status of the PR on the current branch."""

    OPEN = "open"
    ABSENT = "absent"


@runtime_checkable
class IPRStatusReader(Protocol):
    """Read the cached PR status for a branch."""

    def get_pr_status(self, branch: str) -> PRStatus:
        raise NotImplementedError


@runtime_checkable
class IPRStatusWriter(Protocol):
    """Write the PR status for a branch into the cache."""

    def set_pr_status(self, branch: str, status: PRStatus) -> None:
        raise NotImplementedError
