# c:\temp\pgmcp\tests\mcp_server\unit\tools\test_autofix_tool.py
# template=unit_test version=3d15d309 created=2026-06-13T19:23Z updated=
"""
Unit tests for mcp_server.tools.quality_tools.

None

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.tools.quality_tools, unittest.mock]
@responsibilities:
    - Test TestAutoFixTool functionality
    - Verify None
    - None
"""

# Standard library
import asyncio
from typing import Awaitable, AsyncIterator, Optional, Any
from unittest.mock import Mock, MagicMock, AsyncMock, patch

# Third-party
import pytest
from pathlib import Path

# Project modules
from mcp_server.tools.quality_tools import AutoFixTool, AutoFixInput, AutoFixOutput


class TestAutoFixTool:
    """Test suite for quality_tools, response cache, and resources."""

    def test_response_cache_manager_fifo_eviction(self) -> None:
        """Verify that ResponseCacheManager caches DTOs and applies FIFO eviction."""
        from mcp_server.state.response_cache import ResponseCacheManager
        from pydantic import BaseModel

        class DummyDTO(BaseModel):
            success: bool
            value: str

        cache = ResponseCacheManager(max_size=3)
        dto1 = DummyDTO(success=True, value="one")
        dto2 = DummyDTO(success=True, value="two")
        dto3 = DummyDTO(success=True, value="three")
        dto4 = DummyDTO(success=True, value="four")

        # Add 3 items
        cache.put("pgmcp://cache/runs/1", dto1)
        cache.put("pgmcp://cache/runs/2", dto2)
        cache.put("pgmcp://cache/runs/3", dto3)

        assert cache.get("pgmcp://cache/runs/1") == dto1
        assert cache.get("pgmcp://cache/runs/2") == dto2
        assert cache.get("pgmcp://cache/runs/3") == dto3

        # Add 4th item -> dto1 should be evicted (oldest)
        cache.put("pgmcp://cache/runs/4", dto4)

        assert cache.get("pgmcp://cache/runs/1") is None
        assert cache.get("pgmcp://cache/runs/2") == dto2
        assert cache.get("pgmcp://cache/runs/3") == dto3
        assert cache.get("pgmcp://cache/runs/4") == dto4

    @pytest.mark.asyncio
    async def test_cached_response_resource_matching_and_reading(self) -> None:
        """Verify that CachedResponseResource matches URIs and reads compact JSON."""
        from mcp_server.state.response_cache import ResponseCacheManager
        from mcp_server.resources.cache import CachedResponseResource
        from pydantic import BaseModel

        class DummyDTO(BaseModel):
            success: bool
            message: str | None = None

        cache = ResponseCacheManager(max_size=5)
        resource = CachedResponseResource(cache=cache)

        uri_ok = "pgmcp://cache/runs/abc-123"
        uri_bad = "pgmcp://cache/runs"
        uri_wrong = "pgmcp://other/runs/abc-123"

        assert resource.matches(uri_ok) is True
        assert resource.matches(uri_bad) is False
        assert resource.matches(uri_wrong) is False

        # Put DTO with None field
        dto = DummyDTO(success=True, message=None)
        cache.put(uri_ok, dto)

        # Read -> should return compact whitespace-stripped JSON with None field excluded
        json_data = await resource.read(uri_ok)
        assert json_data == '{"success":true}'

        # Read missing URI -> raises ValueError
        with pytest.raises(ValueError, match="No cached data found"):
            await resource.read("pgmcp://cache/runs/missing")

    def test_quality_config_validation_rules(self) -> None:
        """Verify that quality_config validation raises error for misconfigured autofix gates."""
        from mcp_server.config.schemas.quality_config import QualityGate
        from pydantic import ValidationError

        # Gate with supports_autofix=True but missing fix_command should fail validation
        with pytest.raises(ValidationError):
            QualityGate.model_validate({
                "name": "Test Gate",
                "description": "desc",
                "execution": {
                    "command": ["ruff", "format"],
                    "timeout_seconds": 60
                },
                "success": {
                    "exit_codes_ok": [0]
                },
                "capabilities": {
                    "file_types": [".py"],
                    "supports_autofix": True
                }
            })

        # Correct config should pass validation
        gate = QualityGate.model_validate({
            "name": "Test Gate",
            "description": "desc",
            "execution": {
                "command": ["ruff", "format", "--check"],
                "fix_command": ["ruff", "format"],
                "timeout_seconds": 60
            },
            "success": {
                "exit_codes_ok": [0]
            },
            "capabilities": {
                "file_types": [".py"],
                "supports_autofix": True
            }
        })
        assert gate.execution.fix_command == ["ruff", "format"]

    @pytest.mark.asyncio
    async def test_autofix_tool_execution_and_caching(self) -> None:
        """Verify that AutoFixTool executes via QAManager and caches the result."""
        from mcp_server.core.operation_notes import NoteContext
        from mcp_server.state.response_cache import ResponseCacheManager
        from mcp_server.tools.quality_tools import AutoFixTool, AutoFixInput, AutoFixOutput

        qa_manager = MagicMock()
        cache = ResponseCacheManager()
        tool = AutoFixTool(qa_manager=qa_manager, cache=cache)

        # Mock QAManager to return a valid AutoFixOutput DTO
        expected_output = AutoFixOutput(
            success=True,
            modified_files=["foo.py"],
            modified_files_count=1,
            formatted_modified_files="- foo.py",
            gates_executed=["ruff"],
            gates_executed_count=1
        )
        qa_manager.run_auto_fix.return_value = expected_output

        params = AutoFixInput(scope="auto")
        note_ctx = NoteContext()

        with patch("uuid.uuid4") as mock_uuid:
            mock_uuid.return_value = MagicMock(hex="test-run-id")
            result = await tool.execute_structured(params, note_ctx)

        # Check result
        assert isinstance(result, AutoFixOutput)
        assert result.success is True

        # Check QAManager delegation
        qa_manager.run_auto_fix.assert_called_once_with(scope="auto", files=None)

        # Check cache storage
        cached_dto = cache.get("pgmcp://cache/runs/test-run-id")
        assert cached_dto == expected_output

