# tests/mcp_server/unit/state/test_context_loaded_cache.py
"""Unit tests for ContextLoadedCache — C2 of issue #268.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.state.context_loaded_cache, mcp_server.core.interfaces]
"""

from __future__ import annotations

from mcp_server.core.interfaces import IContextLoadedReader, IContextLoadedWriter
from mcp_server.state.context_loaded_cache import ContextLoadedCache


class TestContextLoadedCacheContract:
    """ContextLoadedCache satisfies both IContextLoadedReader and IContextLoadedWriter."""

    def test_icontextloaded_reader_protocol_conformance(self) -> None:
        cache = ContextLoadedCache()
        assert isinstance(cache, IContextLoadedReader)

    def test_icontextloaded_writer_protocol_conformance(self) -> None:
        cache = ContextLoadedCache()
        assert isinstance(cache, IContextLoadedWriter)


class TestContextLoadedCacheBehavior:
    """ContextLoadedCache is a session-scope in-memory flag store."""

    def test_context_loaded_cache_defaults_false(self) -> None:
        cache = ContextLoadedCache()
        assert cache.is_context_loaded("feature/some-branch") is False

    def test_context_loaded_cache_set_true(self) -> None:
        cache = ContextLoadedCache()
        cache.set_context_loaded("feature/some-branch", value=True)
        assert cache.is_context_loaded("feature/some-branch") is True

    def test_context_loaded_cache_reset(self) -> None:
        cache = ContextLoadedCache()
        cache.set_context_loaded("feature/some-branch", value=True)
        cache.set_context_loaded("feature/some-branch", value=False)
        assert cache.is_context_loaded("feature/some-branch") is False

    def test_context_loaded_cache_per_branch_isolation(self) -> None:
        cache = ContextLoadedCache()
        cache.set_context_loaded("feature/branch-a", value=True)
        assert cache.is_context_loaded("feature/branch-b") is False
