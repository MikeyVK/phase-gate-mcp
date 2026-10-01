# c:\temp\pgmcp\tests\mcp_server\unit\tools\test_autofix_tool.py
# template=unit_test version=3d15d309 created=2026-06-13T19:23Z updated=
"""Response-cache eviction and resource read behavior.

@layer: Tests (Unit)
"""

import pytest
from pydantic import BaseModel

from mcp_server.resources.cache import CachedResponseResource
from mcp_server.state.response_cache import ResponseCacheManager


class TestResponseCacheAndResource:
    """Keep cache eviction and resource reads independently observable."""

    def test_response_cache_manager_fifo_eviction(self) -> None:
        """Verify that ResponseCacheManager caches DTOs and applies FIFO eviction."""

        class DummyDTO(BaseModel):
            success: bool
            value: str

        cache = ResponseCacheManager(max_size=3)
        dto1 = DummyDTO(success=True, value="one")
        dto2 = DummyDTO(success=True, value="two")
        dto3 = DummyDTO(success=True, value="three")
        dto4 = DummyDTO(success=True, value="four")

        # Add 3 items
        run1 = cache.put("test_tool", dto1)
        run2 = cache.put("test_tool", dto2)
        run3 = cache.put("test_tool", dto3)

        assert run1 is not None
        assert run2 is not None
        assert run3 is not None
        assert run1.run_id is not None
        assert run2.run_id is not None
        assert run3.run_id is not None

        assert cache.get(run1.run_id, DummyDTO) == dto1
        assert cache.get(run2.run_id, DummyDTO) == dto2
        assert cache.get(run3.run_id, DummyDTO) == dto3

        # Add 4th item -> run1 should be evicted (oldest)
        run4 = cache.put("test_tool", dto4)
        assert run4 is not None
        assert run4.run_id is not None

        assert cache.get(run1.run_id, DummyDTO) is None
        assert cache.get(run2.run_id, DummyDTO) == dto2
        assert cache.get(run3.run_id, DummyDTO) == dto3
        assert cache.get(run4.run_id, DummyDTO) == dto4

    @pytest.mark.asyncio
    async def test_cached_response_resource_matching_and_reading(self) -> None:
        """Verify that CachedResponseResource matches URIs and reads compact JSON."""

        class DummyDTO(BaseModel):
            success: bool
            message: str | None = None

        cache = ResponseCacheManager(max_size=5)
        resource = CachedResponseResource(cache=cache)

        # Put DTO with an absent optional null field
        dto = DummyDTO(success=True)
        pub = cache.put("test_tool", dto)
        assert pub is not None
        assert pub.run_id is not None

        uri_ok = f"pgmcp://cache/runs/{pub.run_id}"
        uri_bad = "pgmcp://cache/runs"
        uri_wrong = "pgmcp://other/runs/abc-123"
        assert resource.matches(uri_ok) is True
        assert resource.matches(uri_bad) is False
        assert resource.matches(uri_wrong) is False

        # Read -> omit the absent optional null while preserving compact JSON
        json_data = await resource.read(uri_ok)
        assert json_data == '{"success":true}'

        # Read missing URI -> raises ValueError
        with pytest.raises(ValueError, match="No cached data found"):
            await resource.read("pgmcp://cache/runs/" + "f" * 32)
