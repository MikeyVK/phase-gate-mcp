# c:\temp\pgmcp\tests\mcp_server\unit\state\test_response_cache.py
# template=unit_test version=3d15d309 created=2026-06-25T19:42Z updated=
"""
Unit tests for mcp_server.state.response_cache.

Tests for ResponseCacheManager key validation and normalization.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.state.response_cache, unittest.mock]
"""

# Third-party
import pytest
from pydantic import BaseModel, ValidationError

# Project modules
from mcp_server.schemas.cache_publication import CachePublication
from mcp_server.state.response_cache import ResponseCacheManager


class TestResponseCache:
    """Test suite for response_cache."""

    def test_cache_publication_validation(self) -> None:
        """Verify that CachePublication run_id enforces 32-character hex UUID format."""
        # Valid hex UUID should pass
        pub = CachePublication(run_id="a" * 32)
        assert pub.run_id == "a" * 32

        # Invalid strings should raise ValidationError
        with pytest.raises(ValidationError):
            CachePublication(run_id="invalid-uuid")

        with pytest.raises(ValidationError):
            CachePublication(run_id="g" * 32)  # Non-hex characters

    @pytest.mark.parametrize("publication_fails", [False, True])
    def test_response_cache_manager_put_get_exists(
        self,
        publication_fails: bool,
        monkeypatch: pytest.MonkeyPatch,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Verify cache publication or its non-destructive failure with diagnosis."""
        cache = ResponseCacheManager()

        class DummyModel(BaseModel):
            value: str

        model = DummyModel(value="test")
        cause = OSError("cache storage unavailable")
        failure = RuntimeError("cache publication failed")

        if publication_fails:

            def fail_publication() -> None:
                raise failure from cause

            monkeypatch.setattr("mcp_server.state.response_cache.uuid.uuid4", fail_publication)

        pub = cache.put("test_tool", model)

        if publication_fails:
            assert not pub.success
            assert pub.run_id is None
            assert pub.error_code == "write_failed"
            assert model.value == "test"
            record = caplog.records[-1]
            assert record.exc_info is not None
            assert record.exc_info[1] is failure
            assert failure.__cause__ is cause
            assert "OSError: cache storage unavailable" in caplog.text
            assert "RuntimeError: cache publication failed" in caplog.text
            return

        assert pub.success
        assert pub.run_id is not None
        assert len(pub.run_id) == 32

        # exists and get should work with the raw run_id
        assert cache.exists(pub.run_id)
        assert cache.get(pub.run_id, DummyModel) == model

        # exists and get should reject invalid formats or URIs
        assert not cache.exists("invalid-uuid")
        assert cache.get("invalid-uuid") is None
        assert not cache.exists(f"pgmcp://cache/runs/{pub.run_id}")
        assert cache.get(f"pgmcp://cache/runs/{pub.run_id}") is None
