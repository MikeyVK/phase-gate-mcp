"""Tests for GitCheckoutTool async execution.

@layer: Tests (Unit)
@dependencies: [pytest, unittest.mock, mcp_server.tools.git_tools]
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from mcp_server.core.operation_notes import NoteContext
from mcp_server.tools.git_tools import GitCheckoutTool


class TestGitCheckoutAsync:
    """Test suite for git_checkout tool async execution."""

    @pytest.mark.asyncio
    async def test_checkout_uses_anyio_to_thread(self) -> None:
        """Verify git_checkout calls anyio.to_thread.run_sync()."""
        mock_manager = Mock()
        mock_manager.get_current_branch.return_value = "main"
        tool = GitCheckoutTool(manager=mock_manager)

        params = Mock()
        params.branch = "feature/123-test"

        mock_run_sync = AsyncMock(side_effect=RuntimeError("stop"))
        with (
            patch("anyio.to_thread.run_sync", mock_run_sync),
            pytest.raises(RuntimeError, match="stop") as caught,
        ):
            await tool.execute(params, NoteContext())

        assert caught.value is mock_run_sync.side_effect
