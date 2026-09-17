# c:\temp\pgmcp\tests\mcp_server\unit\resources\test_cache_resource.py
# template=unit_test version=3d15d309 created=2026-06-25T19:43Z updated=
"""
Unit tests for mcp_server.resources.cache.

Tests for CachedResponseResource validation and reading.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.resources.cache, unittest.mock]
"""

# Third-party
import hashlib
import json
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel

# Project modules
from mcp_server.resources.cache import CachedResponseResource
from mcp_server.state.response_cache import ResponseCacheManager


class DummyModel(BaseModel):
    value: str


@pytest.mark.anyio
class TestCachedResponseResource:
    """Test suite for cache resource."""

    def test_matches_valid_hex_uuid(self) -> None:
        """Verify matches() only returns True for valid 32-character hex UUID URIs."""
        mock_cache = MagicMock()
        resource = CachedResponseResource(mock_cache)

        # Valid hex UUID URI should match
        valid_id = "a" * 32
        assert resource.matches(f"pgmcp://cache/runs/{valid_id}")

        # Invalid formats or non-matching paths should not match
        assert not resource.matches("pgmcp://cache/runs/invalid-uuid")
        assert not resource.matches(f"pgmcp://cache/runs/{valid_id}-extra")
        assert not resource.matches("pgmcp://other/path")

    async def test_read_valid_hex_uuid(self) -> None:
        """Verify read() retrieves valid hex UUID keys and rejects invalid formats."""
        mock_cache = MagicMock()
        resource = CachedResponseResource(mock_cache)

        valid_id = "a" * 32
        model = DummyModel(value="cached-value")
        mock_cache.get.return_value = model

        # Valid URI should succeed and return compact json
        result = await resource.read(f"pgmcp://cache/runs/{valid_id}")
        assert "cached-value" in result
        mock_cache.get.assert_called_once_with(valid_id, BaseModel)

        # Invalid URI format should raise ValueError
        with pytest.raises(ValueError):
            await resource.read("pgmcp://cache/runs/invalid-uuid")

        with pytest.raises(ValueError):
            await resource.read("pgmcp://other/path")


@pytest.mark.asyncio
async def test_windows_reassemble_exact_unicode_snapshot_and_detect_mutation() -> None:
    """Window offsets count codepoints and each page identifies the full snapshot."""
    cache = ResponseCacheManager()
    model = DummyModel(value="A😀é\\n" * 20)
    publication = cache.put("example", model)
    assert publication.run_id is not None
    uri = f"pgmcp://cache/runs/{publication.run_id}"
    resource = CachedResponseResource(cache)
    complete = await resource.read(uri)
    assert publication.size_chars == len(complete)
    expected_hash = hashlib.sha256(complete.encode("utf-8")).hexdigest()
    fragments: list[str] = []
    offset = 0
    while True:
        page_uri = f"{uri}?offset={offset}&limit=7"
        assert resource.matches(page_uri)
        page = json.loads(await resource.read(page_uri))
        assert page["run_id"] == publication.run_id
        assert page["offset"] == offset
        assert page["total_chars"] == len(complete)
        assert page["sha256"] == expected_hash
        assert len(page["text"]) <= 7
        fragments.append(page["text"])
        if page["next_offset"] is None:
            break
        assert page["next_offset"] == offset + len(page["text"])
        offset = page["next_offset"]
    assert "".join(fragments) == complete

    model.value = "B" + model.value[1:]
    changed = json.loads(await resource.read(f"{uri}?offset=0&limit=7"))
    assert changed["total_chars"] == len(complete)
    assert changed["sha256"] != expected_hash


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query",
    [
        "offset=0",
        "limit=7",
        "offset=-1&limit=7",
        "offset=0&limit=0",
        "offset=0&limit=12001",
        "offset=0&offset=1",
        "offset=0&limit=7&extra=1",
        "offset=1.5&limit=7",
        "offset=&limit=7",
        "unknown=0&limit=7",
        "offset=0&limit=7#fragment",
    ],
)
async def test_invalid_window_is_rejected(query: str) -> None:
    """Reject incomplete, ambiguous and unbounded requests before reading the cache."""
    resource = CachedResponseResource(ResponseCacheManager())
    uri = f"pgmcp://cache/runs/{'a' * 32}?{query}"
    assert not resource.matches(uri)
    with pytest.raises(ValueError):
        await resource.read(uri)


@pytest.mark.asyncio
async def test_window_boundaries_and_eviction() -> None:
    """EOF is explicit; stale or out-of-range windows cannot look complete."""
    cache = ResponseCacheManager(max_size=1)
    publication = cache.put("example", DummyModel(value="x"))
    uri = f"pgmcp://cache/runs/{publication.run_id}"
    resource = CachedResponseResource(cache)
    total = len(await resource.read(uri))
    eof = json.loads(await resource.read(f"{uri}?offset={total}&limit=7"))
    assert eof["text"] == ""
    assert eof["next_offset"] is None
    with pytest.raises(ValueError, match="offset"):
        await resource.read(f"{uri}?offset={total + 1}&limit=7")
    cache.put("example", DummyModel(value="replacement"))
    with pytest.raises(ValueError, match="No cached data found"):
        await resource.read(f"{uri}?offset=0&limit=7")
