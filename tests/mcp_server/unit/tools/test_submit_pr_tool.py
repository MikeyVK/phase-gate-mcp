# tests/mcp_server/unit/tools/test_submit_pr_tool.py
"""Unit tests for SubmitPRTool and SubmitPRInput scaffold.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.tools.pr_tools, mcp_server.tools.base]
"""

from __future__ import annotations

import asyncio
import inspect
from unittest.mock import MagicMock

from mcp_server.core.interfaces import IPRStatusWriter
from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.git_manager import GitManager
from mcp_server.managers.github_manager import GitHubManager
from mcp_server.managers.phase_contract_resolver import MergeReadinessContext
from mcp_server.tools.base import BranchMutatingTool
from mcp_server.tools.pr_tools import SubmitPRInput, SubmitPRTool


class TestSubmitPRInput:
    """SubmitPRInput Pydantic model has the required fields per design 3.2."""

    def test_head_field_required(self) -> None:
        assert "head" in SubmitPRInput.model_fields

    def test_title_field_required(self) -> None:
        assert "title" in SubmitPRInput.model_fields

    def test_base_field_optional(self) -> None:
        field = SubmitPRInput.model_fields.get("base")
        assert field is not None
        assert not field.is_required()

    def test_draft_field_optional(self) -> None:
        field = SubmitPRInput.model_fields.get("draft")
        assert field is not None
        assert not field.is_required()


class TestSubmitPRTool:
    """SubmitPRTool is a BranchMutatingTool named 'submit_pr'."""

    def test_class_exists(self) -> None:
        assert SubmitPRTool is not None

    def test_inherits_branch_mutating_tool(self) -> None:
        assert issubclass(SubmitPRTool, BranchMutatingTool)

    def test_name_is_submit_pr(self) -> None:
        assert SubmitPRTool.name == "submit_pr"

    def test_args_model_is_submit_pr_input(self) -> None:
        assert SubmitPRTool.args_model is SubmitPRInput


def _make_tool_for_lod(
    git_manager: GitManager,
    github_manager: GitHubManager,
    pr_status_writer: IPRStatusWriter,
) -> SubmitPRTool:
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
    )


class TestSubmitPRToolLoD:
    """C5 LoD structural tests: execute() must not call git internals directly."""

    def test_submit_pr_execute_does_not_call_git_internals_directly(
        self,
    ) -> None:
        """execute() must only call GitManager.prepare_submission, not lower-level methods."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.get_current_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.return_value = False
        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.return_value = {
            "number": 1,
            "url": "https://github.com/x/y/pull/1",
        }
        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_tool_for_lod(git_manager, github_manager, pr_status_writer)
        params = SubmitPRInput(head="feature/42-test", base="main", title="Test PR")

        asyncio.get_event_loop().run_until_complete(tool.execute(params, NoteContext()))

        # These methods must NOT be called directly by execute() (LoD violation)
        git_manager.neutralize_to_base.assert_not_called()
        git_manager.commit_with_scope.assert_not_called()
        git_manager.push.assert_not_called()
        git_manager.has_net_diff_for_path.assert_not_called()

    def test_submit_pr_execute_does_not_access_adapter(
        self,
    ) -> None:
        """execute() must not call self._git_manager.adapter directly."""
        source = inspect.getsource(SubmitPRTool.execute)
        assert "_git_manager.adapter" not in source, (
            "SubmitPRTool.execute() must not access GitAdapter directly. "
            "Use GitManager methods instead (Law of Demeter)."
        )
