# c:\temp\pgmcp\mcp_server\core\interfaces\context.py
# template=interface version=3fb28c28 created=2026-06-20T18:33:58Z updated=
"""IContextLoadedReader module.

Read whether get_work_context has been called for a branch this session.

@layer: Backend (Contracts)
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class IContextLoadedReader(Protocol):
    """Read whether get_work_context has been called for a branch this session."""

    def is_context_loaded(self, branch: str) -> bool:
        raise NotImplementedError


@runtime_checkable
class IContextLoadedWriter(Protocol):
    """Record that get_work_context has been called for a branch this session."""

    def set_context_loaded(self, branch: str, *, value: bool) -> None:
        raise NotImplementedError
