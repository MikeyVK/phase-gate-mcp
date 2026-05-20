# mcp_server/state/context_loaded_cache.py
"""Session-scope in-memory cache for get_work_context load status per branch.

@layer: Backend (State)
@dependencies: [mcp_server.core.interfaces]
@responsibilities:
    - Track whether get_work_context has been called for a branch in this session
    - Default to False on cold start (no file reads, no import-time side effects)
    - Implement IContextLoadedReader and IContextLoadedWriter (ISP split)
"""

from __future__ import annotations

from mcp_server.core.interfaces import IContextLoadedReader, IContextLoadedWriter


class ContextLoadedCache(IContextLoadedReader, IContextLoadedWriter):
    """Session-scope in-memory flag store for per-branch context-loaded status.

    Defaults to False on cold start. No file I/O, no ClassVar singleton.
    """

    def __init__(self) -> None:
        self._cache: dict[str, bool] = {}

    def is_context_loaded(self, branch: str) -> bool:
        """Return True if get_work_context has been called for *branch* this session."""
        return self._cache.get(branch, False)

    def set_context_loaded(self, branch: str, *, value: bool) -> None:
        """Record context-loaded status for *branch*."""
        self._cache[branch] = value
