# tests\mcp_server\unit\tools\test_health_tools.py
# template=unit_test version=3d15d309 created=2026-06-14T16:27Z updated=
"""
Unit tests for mcp_server.tools.health_tools.

None

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.tools.health_tools, unittest.mock]
@responsibilities:
    - Test TestHealthAndAdminTools functionality
    - Verify None
    - None
"""

# Standard library
from pathlib import Path
from unittest.mock import patch

# Third-party
import pytest

# Project modules
from mcp_server.tools.health_tools import HealthCheckTool


class TestHealthAndAdminTools:
    """Test suite for health and admin tools."""

    @pytest.mark.asyncio
    async def test_health_check_tool_returns_dto(self) -> None:
        """HealthCheckTool should execute and return HealthCheckOutput."""
        from mcp_server.core.operation_notes import NoteContext  # noqa: PLC0415
        from mcp_server.schemas.tool_outputs import HealthCheckOutput  # noqa: PLC0415
        from mcp_server.tools.health_tools import HealthCheckInput  # noqa: PLC0415

        tool = HealthCheckTool()
        context = NoteContext()
        params = HealthCheckInput()

        result = await tool.execute(params, context)

        assert isinstance(result, HealthCheckOutput)
        assert result.success
        assert result.status == "healthy"

    @pytest.mark.asyncio
    async def test_restart_server_tool_returns_dto(self, tmp_path: Path) -> None:
        """RestartServerTool should execute and return RestartServerOutput."""
        from mcp_server.core.operation_notes import NoteContext  # noqa: PLC0415
        from mcp_server.schemas.tool_outputs import RestartServerOutput  # noqa: PLC0415
        from mcp_server.tools.admin_tools import (  # noqa: PLC0415
            RestartServerInput,
            RestartServerTool,
        )

        tool = RestartServerTool(server_root=tmp_path)
        context = NoteContext()
        params = RestartServerInput(reason="testing")
        with patch("asyncio.create_task") as mock_create_task:
            result = await tool.execute(params, context)

            assert isinstance(result, RestartServerOutput)
            assert result.success
            assert result.reason == "testing"
            assert result.pid > 0
            assert result.iso_time != ""

            mock_create_task.assert_called_once()
