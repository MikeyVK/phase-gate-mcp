# pyright: reportPrivateUsage=false
"""Tests for GitCheckoutTool state synchronization with PhaseStateEngine.

@layer: Tests (Unit)
@dependencies: [pytest, unittest.mock, mcp_server.tools.git_tools]
"""

from unittest.mock import Mock

import pytest

from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.state_repository import BranchState, StateBranchMismatchError
from mcp_server.tools.git_tools import GitCheckoutTool
from mcp_server.tools.tool_result import ToolResult


class TestGitCheckoutStateSync:
    """Test suite for git_checkout tool PhaseStateEngine state synchronization."""

    @pytest.mark.asyncio
    async def test_checkout_syncs_state_and_returns_phase(self) -> None:
        """Test that git_checkout syncs state and returns current phase info."""
        mock_manager = Mock()
        tool = GitCheckoutTool(manager=mock_manager)

        params = Mock()
        params.branch = "feature/123-test"

        mock_engine = Mock()
        mock_engine.get_state.return_value = BranchState(
            branch="feature/123-test",
            issue_number=123,
            workflow_name="feature",
            current_phase="implementation",
            current_cycle=1,
            required_phases=["research", "planning", "design", "implementation"],
            transitions=[],
        )
        tool._state_engine = mock_engine

        result = await tool.execute(params, NoteContext())

        mock_manager.checkout.assert_called_once_with("feature/123-test")
        mock_engine.get_state.assert_called_once_with("feature/123-test")

        from mcp_server.schemas.tool_outputs import GitCheckoutOutput
        assert isinstance(result, GitCheckoutOutput)
        assert result.success is True
        assert result.branch == "feature/123-test"
        assert result.current_phase == "implementation"

    @pytest.mark.asyncio
    async def test_checkout_handles_state_sync_failure_gracefully(self) -> None:
        """Test that git_checkout handles state sync failures gracefully."""
        mock_manager = Mock()
        tool = GitCheckoutTool(manager=mock_manager)

        params = Mock()
        params.branch = "feature/456-test"

        mock_engine = Mock()
        mock_engine.get_state.side_effect = ValueError("State sync failed")
        tool._state_engine = mock_engine

        result = await tool.execute(params, NoteContext())

        mock_manager.checkout.assert_called_once_with("feature/456-test")
        from mcp_server.schemas.tool_outputs import GitCheckoutOutput
        assert isinstance(result, GitCheckoutOutput)
        assert result.success is True
        assert result.branch == "feature/456-test"

    @pytest.mark.asyncio
    async def test_checkout_handles_unknown_phase(self) -> None:
        """Test that git_checkout handles unknown/missing phase gracefully."""
        mock_manager = Mock()
        tool = GitCheckoutTool(manager=mock_manager)

        params = Mock()
        params.branch = "main"

        mock_engine = Mock()
        mock_engine.get_state.return_value = BranchState(
            branch="main",
            issue_number=None,
            workflow_name="feature",
            current_phase="unknown",
            transitions=[],
        )
        tool._state_engine = mock_engine

        result = await tool.execute(params, NoteContext())

        mock_manager.checkout.assert_called_once_with("main")
        mock_engine.get_state.assert_called_once_with("main")

        from mcp_server.schemas.tool_outputs import GitCheckoutOutput
        assert isinstance(result, GitCheckoutOutput)
        assert result.success is True
        assert result.branch == "main"
        assert result.current_phase == "unknown"

    @pytest.mark.asyncio
    async def test_checkout_handles_state_branch_mismatch_gracefully(self) -> None:
        """Checkout handles StateBranchMismatchError gracefully (C_ENGINE_BREAK)."""
        mock_manager = Mock()
        tool = GitCheckoutTool(manager=mock_manager)

        params = Mock()
        params.branch = "feature/231-state-snapshot-cqrs"

        mock_engine = Mock()
        mock_engine.get_state.side_effect = StateBranchMismatchError(
            "Loaded state branch 'main' does not match "
            "requested branch 'feature/231-state-snapshot-cqrs'"
        )
        tool._state_engine = mock_engine

        result = await tool.execute(params, NoteContext())

        mock_manager.checkout.assert_called_once_with("feature/231-state-snapshot-cqrs")
        from mcp_server.schemas.tool_outputs import GitCheckoutOutput
        assert isinstance(result, GitCheckoutOutput)
        assert result.success is True
        assert result.branch == "feature/231-state-snapshot-cqrs"
