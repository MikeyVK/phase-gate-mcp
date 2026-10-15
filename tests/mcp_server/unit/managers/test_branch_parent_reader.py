from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from mcp_server.config.schemas.git_config import GitConfig
from mcp_server.core.interfaces import IStateReader
from mcp_server.managers.branch_parent_reader import BranchStateParentReader
from mcp_server.managers.state_repository import BranchState, StateNotFoundError


class TestBranchStateParentReader:
    """Unit tests for BranchStateParentReader."""

    @pytest.fixture
    def git_config(self) -> GitConfig:
        return GitConfig(
            branch_types=["feature", "bug", "refactor", "docs", "hotfix", "epic"],
            protected_branches=["main", "master", "develop"],
            branch_name_pattern=r"^[a-z0-9-]+$",
            commit_types=["feat", "fix", "docs", "style", "refactor", "test", "chore"],
            issue_title_max_length=72,
        )

    def test_get_parent_branch_returns_parent_when_issue_matches(
        self, git_config: GitConfig
    ) -> None:
        """Happy path: state.issue_number == branch issue -> return parent_branch."""
        mock_reader = MagicMock(spec=IStateReader)
        mock_reader.load.return_value = BranchState(
            branch="bug/357-fix-test",
            issue_number=357,
            workflow_name="bug",
            current_phase="implementation",
            parent_branch="epic/320-production-readiness",
        )
        reader = BranchStateParentReader(
            state_reader=mock_reader,
            git_config=git_config,
        )
        result = reader.get_parent_branch("bug/357-fix-test")
        assert result == "epic/320-production-readiness"
        mock_reader.load.assert_called_once_with("bug/357-fix-test")

    def test_get_parent_branch_returns_none_on_issue_mismatch(self, git_config: GitConfig) -> None:
        """Mismatch guard: state.issue_number != extracted issue -> return None."""
        mock_reader = MagicMock(spec=IStateReader)
        mock_reader.load.return_value = BranchState(
            branch="bug/357-fix-test",
            issue_number=999,
            workflow_name="bug",
            current_phase="implementation",
            parent_branch="epic/320-production-readiness",
        )
        reader = BranchStateParentReader(
            state_reader=mock_reader,
            git_config=git_config,
        )
        result = reader.get_parent_branch("bug/357-fix-test")
        assert result is None

    def test_get_parent_branch_returns_none_on_exact_branch_mismatch(
        self, git_config: GitConfig
    ) -> None:
        """Another registration for the same issue is not the requested branch basis."""
        mock_reader = MagicMock(spec=IStateReader)
        mock_reader.load.return_value = BranchState(
            branch="bug/357-other-work",
            issue_number=357,
            workflow_name="bug",
            current_phase="implementation",
            parent_branch="main",
        )
        reader = BranchStateParentReader(
            state_reader=mock_reader,
            git_config=git_config,
        )
        result = reader.get_parent_branch("bug/357-fix-test")
        assert result is None

    def test_get_parent_branch_returns_none_on_state_not_found(self, git_config: GitConfig) -> None:
        """Resilience: state.json absent (StateNotFoundError) -> return None."""
        mock_reader = MagicMock(spec=IStateReader)
        mock_reader.load.side_effect = StateNotFoundError("state.json absent")
        reader = BranchStateParentReader(
            state_reader=mock_reader,
            git_config=git_config,
        )
        result = reader.get_parent_branch("bug/357-fix-test")
        assert result is None
        mock_reader.load.assert_called_once_with("bug/357-fix-test")
