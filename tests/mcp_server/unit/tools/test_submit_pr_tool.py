# tests/mcp_server/unit/tools/test_submit_pr_tool.py
"""Unit tests for SubmitPRTool and SubmitPRInput scaffold.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.tools.pr_tools]
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from mcp_server.config.loader import ConfigLoader
from mcp_server.core.exceptions import PreflightError, StateNotFoundError
from mcp_server.core.interfaces import IPRStatusWriter, IStateReader
from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.git_manager import GitManager
from mcp_server.managers.github_manager import GitHubManager
from mcp_server.managers.phase_contract_resolver import MergeReadinessContext
from mcp_server.managers.state_repository import BranchState, StateBranchMismatchError
from mcp_server.schemas.github_models import PRReadModel
from mcp_server.schemas.tool_outputs import PROutput
from mcp_server.tools.pr_tools import SubmitPRInput, SubmitPRTool
from tests.mcp_server.test_support import get_default_server_root


class TestSubmitPRInput:
    """SubmitPRInput Pydantic model has the required fields per design 3.2."""

    def test_title_field_required(self) -> None:
        assert "title" in SubmitPRInput.model_fields

    def test_draft_field_optional(self) -> None:
        field = SubmitPRInput.model_fields.get("draft")
        assert field is not None
        assert not field.is_required()


class TestSubmitPRTool:
    """SubmitPRTool is a BranchMutatingTool named 'submit_pr'."""

    def test_class_exists(self) -> None:
        assert SubmitPRTool is not None

    def test_is_branch_mutating_in_config(self) -> None:
        repo_root = Path(__file__).parent.parent.parent.parent.parent
        loader = ConfigLoader(config_root=repo_root / get_default_server_root() / "config")
        config = loader.load_enforcement_config()
        assert "submit_pr" in config.categories.get("branch_mutating", [])

    def test_name_is_submit_pr(self) -> None:
        tool = SubmitPRTool(
            MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()
        )
        assert tool.name == "submit_pr"

    def test_args_model_is_submit_pr_input(self) -> None:
        tool = SubmitPRTool(
            MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()
        )
        assert tool.args_model is SubmitPRInput


def _make_tool(
    git_manager: GitManager,
    github_manager: GitHubManager,
    pr_status_writer: IPRStatusWriter,
    state_reader: IStateReader | None = None,
) -> SubmitPRTool:
    if state_reader is None:
        reader = MagicMock(spec=IStateReader)
        reader.load.return_value = BranchState(
            branch="feature/42-test",
            issue_number=42,
            workflow_name="feature",
            current_phase="ready",
            parent_branch="main",
        )
        state_reader = reader
    repo_root = Path(__file__).parents[4]
    git_config = ConfigLoader(repo_root / get_default_server_root() / "config").load_git_config()
    mock_pr = PRReadModel(
        pr_number=1,
        title="Test PR",
        state="open",
        base_branch="main",
        head_branch="feature/42-test",
        merged_at=None,
        merge_sha=None,
        body="",
        html_url="https://github.com/x/y/pull/1",
    )
    github_manager.get_pr.return_value = mock_pr
    merge_readiness_context = MergeReadinessContext(
        terminal_phase="ready",
        pr_allowed_phase="ready",
        branch_local_artifacts=[],
    )
    return SubmitPRTool(
        git_manager=git_manager,
        github_manager=github_manager,
        pr_status_writer=pr_status_writer,
        merge_readiness_context=merge_readiness_context,
        state_reader=state_reader,
        git_config=git_config,
    )


class TestSubmitPRToolLoD:
    """C5 LoD structural tests: execute() must not call git internals directly."""

    def test_submit_pr_execute_does_not_call_git_internals_directly(
        self,
    ) -> None:
        """execute() must only call GitManager.prepare_submission, not lower-level methods."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.return_value = False
        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.return_value = {
            "number": 1,
            "url": "https://github.com/x/y/pull/1",
        }
        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_tool(git_manager, github_manager, pr_status_writer)
        params = SubmitPRInput(title="Test PR")

        asyncio.run(tool.execute(params, NoteContext()))

        # These methods must NOT be called directly by execute() (LoD violation)
        git_manager.neutralize_to_base.assert_not_called()
        git_manager.commit_with_scope.assert_not_called()
        git_manager.push.assert_not_called()
        git_manager.has_net_diff_for_path.assert_not_called()


class TestSubmitPRRegistration:
    """Registration authorizes targets before the existing submission effects."""

    def test_registered_parent_supplies_submission_base(self) -> None:
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.return_value = False
        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.return_value = {"number": 1}
        reader = MagicMock(spec=IStateReader)
        reader.load.return_value = BranchState(
            branch="feature/42-test",
            issue_number=42,
            workflow_name="feature",
            current_phase="ready",
            parent_branch="epic/320-production-readiness",
        )
        writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_tool(git_manager, github_manager, writer, reader)

        asyncio.run(tool.execute(SubmitPRInput(title="Test PR"), NoteContext()))

        reader.load.assert_called_once_with("feature/42-test")
        assert git_manager.prepare_submission.call_args.args[1] == "epic/320-production-readiness"
        assert github_manager.create_pr.call_args.kwargs["head"] == "feature/42-test"
        assert github_manager.create_pr.call_args.kwargs["base"] == "epic/320-production-readiness"
        writer.set_pr_status.assert_called_once()

    @pytest.mark.parametrize(
        "failure", ["missing", "branch", "issue", "unreadable", "unidentified"]
    )
    def test_invalid_registration_prevents_submission_effects(self, failure: str) -> None:
        branch = "feature/no-issue" if failure == "unidentified" else "feature/42-test"
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = branch
        github_manager = MagicMock(spec=GitHubManager)
        writer = MagicMock(spec=IPRStatusWriter)
        reader = MagicMock(spec=IStateReader)
        expected: type[Exception] = PreflightError
        original: Exception | None = None
        if failure == "missing":
            original = StateNotFoundError("Registration absent")
            reader.load.side_effect = original
            expected = StateNotFoundError
        elif failure == "unreadable":
            original = PermissionError("Registration unreadable")
            reader.load.side_effect = original
            expected = PermissionError
        else:
            reader.load.return_value = BranchState(
                branch="feature/42-other" if failure == "branch" else branch,
                issue_number=99 if failure == "issue" else 42,
                workflow_name="feature",
                current_phase="ready",
                parent_branch="main",
            )
            if failure == "branch":
                expected = StateBranchMismatchError
        tool = _make_tool(git_manager, github_manager, writer, reader)

        with pytest.raises(expected) as captured:
            asyncio.run(tool.execute(SubmitPRInput(title="Test PR"), NoteContext()))

        if original is not None:
            assert captured.value is original
        git_manager.prepare_submission.assert_not_called()
        git_manager.rollback_push.assert_not_called()
        github_manager.create_pr.assert_not_called()
        writer.set_pr_status.assert_not_called()


class TestSubmitPRToolExecute:
    """Tests verify that SubmitPRTool execution returns the new DTO."""

    @pytest.mark.asyncio
    async def test_submit_pr_returns_dto(self) -> None:
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.return_value = False
        github_manager = MagicMock(spec=GitHubManager)

        mock_pr = PRReadModel(
            pr_number=1,
            title="Test PR",
            state="open",
            base_branch="main",
            head_branch="feature/42-test",
            merged_at=None,
            merge_sha=None,
            body="",
            html_url="https://github.com/x/y/pull/1",
        )
        github_manager.create_pr.return_value = {
            "number": 1,
            "url": "https://github.com/x/y/pull/1",
        }
        github_manager.get_pr.return_value = mock_pr

        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_tool(git_manager, github_manager, pr_status_writer)
        params = SubmitPRInput(title="Test PR")

        result = await tool.execute(params, NoteContext())
        assert isinstance(result, PROutput)
        assert result.success is True
        assert result.number == 1
        assert result.title == "Test PR"
        assert result.html_url == "https://github.com/x/y/pull/1"
