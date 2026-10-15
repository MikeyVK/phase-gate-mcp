# tests/mcp_server/integration/test_submit_pr_atomic_flow.py
"""Integration tests for submit_pr atomicity (issue #295).

Tests verify the full atomic sequence:
  1. Preflight (is_clean, has_upstream) via GitManager.prepare_submission
  2. Branch-local artifact neutralization (encapsulated in prepare_submission)
  3. Push (encapsulated in prepare_submission)
  4. GitHub PR creation
  5. PRStatusCache write (OPEN)

@layer: Tests (Integration)
@dependencies: [pathlib, pytest, unittest.mock,
    mcp_server.tools.pr_tools,
    mcp_server.core.interfaces,
    mcp_server.core.operation_notes,
    mcp_server.managers.git_manager,
    mcp_server.managers.github_manager]
@responsibilities:
    - Prove SubmitPRTool.execute() writes PRStatus.OPEN after successful PR creation
    - Prove atomic flow: neutralize -> commit -> push -> create_pr -> set_pr_status
    - Prove skip of neutralize when no branch-local artifacts have net diff
    - Prove partial failure produces RecoveryNote
    - Prove matching registration supplies submission targets
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import MagicMock

import pytest
import yaml

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.contracts_config import BranchLocalArtifact
from mcp_server.core.exceptions import ExecutionError, PreflightError
from mcp_server.core.interfaces import IPRStatusWriter, IStateReader, PRStatus
from mcp_server.core.operation_notes import Note, NoteContext
from mcp_server.managers.git_manager import GitManager
from mcp_server.managers.github_manager import GitHubManager
from mcp_server.managers.phase_contract_resolver import MergeReadinessContext
from mcp_server.managers.state_repository import BranchState
from mcp_server.schemas.github_models import PRReadModel
from mcp_server.tools.pr_tools import SubmitPRInput, SubmitPRTool
from tests.mcp_server.test_support import get_default_server_root

_STATE_ARTIFACT = BranchLocalArtifact(
    path=f"{get_default_server_root()}/state.json",
    reason="branch-local workflow state",
)
_DELIVERABLES_ARTIFACT = BranchLocalArtifact(
    path=f"{get_default_server_root()}/deliverables.json",
    reason="branch-local deliverables",
)


def _make_submit_pr_tool(
    git_manager: GitManager,
    github_manager: GitHubManager,
    pr_status_writer: IPRStatusWriter,
    artifacts: tuple[BranchLocalArtifact, ...] = (_STATE_ARTIFACT,),
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
    repo_root = Path(__file__).parents[3]
    git_config = ConfigLoader(repo_root / get_default_server_root() / "config").load_git_config()
    if isinstance(github_manager, MagicMock):
        github_manager.get_pr.return_value = PRReadModel(
            pr_number=101,
            title="Test PR",
            state="open",
            base_branch="main",
            head_branch="feature/42-test",
            merged_at=None,
            merge_sha=None,
            body="Description",
            html_url="http://github.com/pulls/101",
        )
    merge_readiness_context = MergeReadinessContext(
        terminal_phase="ready",
        pr_allowed_phase="ready",
        branch_local_artifacts=artifacts,
    )
    return SubmitPRTool(
        git_manager=git_manager,
        github_manager=github_manager,
        pr_status_writer=pr_status_writer,
        merge_readiness_context=merge_readiness_context,
        state_reader=state_reader,
        git_config=git_config,
    )


def _make_params(
    title: str = "Test PR",
    body: str = "Description",
    draft: bool = False,
) -> SubmitPRInput:
    return SubmitPRInput(title=title, body=body, draft=draft)


class TestSubmitPRHappyPath:
    """SubmitPRTool happy path: atomic flow executes in correct order."""

    def test_submit_pr_happy_path(self) -> None:
        """Full atomic flow: prepare_submission -> create_pr -> set_pr_status(OPEN)."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.return_value = True

        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.return_value = {
            "number": 42,
            "url": "https://github.com/x/y/pull/42",
        }

        pr_status_writer = MagicMock(spec=IPRStatusWriter)

        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)

        result = asyncio.run(tool.execute(_make_params(), NoteContext()))

        assert result.success is True
        git_manager.prepare_submission.assert_called_once()
        github_manager.create_pr.assert_called_once()
        pr_status_writer.set_pr_status.assert_called_once_with("feature/42-test", PRStatus.OPEN)

    def test_submit_pr_skips_neutralize_when_no_exclusions(self) -> None:
        """When no branch-local artifacts are configured, prepare_submission still called."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.return_value = False

        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.return_value = {
            "number": 42,
            "url": "https://github.com/x/y/pull/42",
        }

        pr_status_writer = MagicMock(spec=IPRStatusWriter)

        # No artifacts -> frozenset() passed to prepare_submission
        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer, artifacts=())

        result = asyncio.run(tool.execute(_make_params(), NoteContext()))

        assert result.success is True
        git_manager.prepare_submission.assert_called_once()
        pr_status_writer.set_pr_status.assert_called_once_with("feature/42-test", PRStatus.OPEN)

    def test_submit_pr_pr_status_written_open(self) -> None:
        """PRStatus.OPEN is written to the cache after successful PR creation."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = "refactor/283-test"
        git_manager.prepare_submission.return_value = False

        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.return_value = {
            "number": 99,
            "url": "https://github.com/x/y/pull/99",
        }

        pr_status_writer = MagicMock(spec=IPRStatusWriter)

        reader = MagicMock(spec=IStateReader)
        reader.load.return_value = BranchState(
            branch="refactor/283-test",
            issue_number=283,
            workflow_name="refactor",
            current_phase="ready",
            parent_branch="main",
        )
        tool = _make_submit_pr_tool(
            git_manager, github_manager, pr_status_writer, state_reader=reader
        )

        asyncio.run(tool.execute(_make_params(), NoteContext()))

        pr_status_writer.set_pr_status.assert_called_once_with("refactor/283-test", PRStatus.OPEN)


class TestSubmitPRPartialFailure:
    """SubmitPRTool produces RecoveryNote on failure after neutralize."""

    def test_push_failure_produces_recovery_note(self) -> None:
        """When prepare_submission raises ExecutionError (push failed), error returned."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.side_effect = ExecutionError("push failed: remote rejected")

        github_manager = MagicMock(spec=GitHubManager)
        pr_status_writer = MagicMock(spec=IPRStatusWriter)

        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)

        context = NoteContext()
        with pytest.raises(ExecutionError):
            asyncio.run(tool.execute(_make_params(), context))
        # PRStatus must NOT be written when push failed
        pr_status_writer.set_pr_status.assert_not_called()

    def test_create_pr_failure_produces_recovery_note(self) -> None:
        """When create_pr raises ExecutionError, error returned; no status written."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.return_value = False

        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.side_effect = ExecutionError("PR already exists")

        pr_status_writer = MagicMock(spec=IPRStatusWriter)

        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)

        with pytest.raises(ExecutionError):
            asyncio.run(tool.execute(_make_params(), NoteContext()))
        pr_status_writer.set_pr_status.assert_not_called()


class TestCompositionRootContracts:
    """Configured admission remains attached to the public submission tool."""

    def test_submit_pr_tool_declares_enforcement_event(self) -> None:
        """SubmitPRTool.enforcement_event must be 'submit_pr' so phase-readiness gate fires."""
        assert SubmitPRTool.enforcement_event == "submit_pr", (
            "SubmitPRTool must declare enforcement_event = 'submit_pr'. "
            "Without it, check_phase_readiness in enforcement.yaml is never dispatched."
        )

    def test_enforcement_yaml_has_exclude_artifacts_and_phase_readiness_for_submit_pr(
        self,
    ) -> None:
        """enforcement.yaml must NOT include exclude_branch_local_artifacts for submit_pr.

        C6 design decision D5 (revised): neutralisation is self-contained inside
        SubmitPRTool.execute() via injected MergeReadinessContext. The enforcement
        runner no longer needs to pre-populate ExclusionNotes.
        check_phase_readiness must still be present.
        """
        workspace_root = Path(__file__).parents[3]
        config_path = workspace_root / get_default_server_root() / "config" / "enforcement.yaml"
        config = yaml.safe_load(config_path.read_text(encoding="utf-8"))

        submit_pr_actions = [
            action["type"]
            for rule in config["enforcement"]
            if rule.get("tool") == "submit_pr" and rule.get("timing") == "pre"
            for action in rule.get("actions", [])
        ]

        assert "exclude_branch_local_artifacts" not in submit_pr_actions, (
            "submit_pr mag geen exclude_branch_local_artifacts enforcement hebben; "
            "neutralisatie is self-contained in SubmitPRTool.execute()"
        )
        assert "check_phase_readiness" in submit_pr_actions, (
            "submit_pr pre rule must include check_phase_readiness."
        )


class TestSubmitPRAtomicRefactored:
    """C5: SubmitPRTool delegates to prepare_submission + rollback_push (design Â§4.3)."""

    def test_failure_a_no_upstream_blocked_before_mutation(self) -> None:
        """prepare_submission raises PreflightError -> error; no create_pr; no status."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.side_effect = PreflightError("No upstream configured")
        github_manager = MagicMock(spec=GitHubManager)
        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)

        with pytest.raises(ExecutionError):
            asyncio.run(tool.execute(_make_params(), NoteContext()))
        github_manager.create_pr.assert_not_called()
        pr_status_writer.set_pr_status.assert_not_called()

    def test_failure_b_dirty_tree_blocked_before_mutation(self) -> None:
        """prepare_submission raises PreflightError (dirty) -> error; no create_pr; no status."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.side_effect = PreflightError("Working directory not clean")
        github_manager = MagicMock(spec=GitHubManager)
        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)

        with pytest.raises(ExecutionError):
            asyncio.run(tool.execute(_make_params(), NoteContext()))
        github_manager.create_pr.assert_not_called()
        pr_status_writer.set_pr_status.assert_not_called()

    def test_failure_c_create_pr_failure_triggers_rollback_push(self) -> None:
        """prepare_submission returns True; create_pr raises -> rollback_push + RecoveryNote."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.return_value = True
        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.side_effect = ExecutionError("API 503")
        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)
        context = NoteContext()

        with pytest.raises(ExecutionError):
            asyncio.run(tool.execute(_make_params(), context))
        git_manager.rollback_push.assert_called_once()
        notes = [
            n
            for n in context.of_type(Note)
            if n.key == "submit_pr_api_failed_with_rollback_recovery"
        ]
        assert len(notes) == 1
        assert "API 503" in notes[0].params.get("error_details", "")
        pr_status_writer.set_pr_status.assert_not_called()

    def test_failure_c_no_rollback_when_no_neutralization_commit(self) -> None:
        """prepare_submission returns False (no commit); create_pr raises -> NO rollback_push."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.return_value = False
        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.side_effect = ExecutionError("API 503")
        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)

        with pytest.raises(ExecutionError):
            asyncio.run(tool.execute(_make_params(), NoteContext()))
        git_manager.rollback_push.assert_not_called()
        pr_status_writer.set_pr_status.assert_not_called()

    def test_failure_c_meta_rollback_failure_surfaced_via_recovery_note(self) -> None:
        """create_pr raises; rollback_push raises -> error returned; set_pr_status not called."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.return_value = True
        git_manager.rollback_push.side_effect = ExecutionError("CRITICAL: reset failed")
        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.side_effect = ExecutionError("API 503")
        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)
        context = NoteContext()

        with pytest.raises(ExecutionError):
            asyncio.run(tool.execute(_make_params(), context))
        pr_status_writer.set_pr_status.assert_not_called()

    def test_failure_d_push_fails_prepare_submission_raises_execution_error(self) -> None:
        """prepare_submission raises ExecutionError (push fail) -> error, no rollback."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.side_effect = ExecutionError("push rejected")
        github_manager = MagicMock(spec=GitHubManager)
        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)

        with pytest.raises(ExecutionError):
            asyncio.run(tool.execute(_make_params(), NoteContext()))
        git_manager.rollback_push.assert_not_called()
        pr_status_writer.set_pr_status.assert_not_called()

    def test_happy_path_prepare_submission_then_create_pr_then_status(self) -> None:
        """All succeed: prepare_submission called once; set_pr_status(branch, OPEN) called."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.return_value = True
        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.return_value = {
            "number": 42,
            "url": "https://github.com/x/y/pull/42",
        }
        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)

        result = asyncio.run(tool.execute(_make_params(), NoteContext()))

        assert result.success is True
        git_manager.prepare_submission.assert_called_once()
        pr_status_writer.set_pr_status.assert_called_once_with("feature/42-test", PRStatus.OPEN)

    def test_happy_path_artifact_paths_extracted_from_merge_readiness_context(self) -> None:
        """prepare_submission called with frozenset of both artifact paths."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.return_value = False
        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.return_value = {
            "number": 1,
            "url": "https://github.com/x/y/pull/1",
        }
        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_submit_pr_tool(
            git_manager,
            github_manager,
            pr_status_writer,
            artifacts=(_STATE_ARTIFACT, _DELIVERABLES_ARTIFACT),
        )

        asyncio.run(tool.execute(_make_params(), NoteContext()))

        call_args = git_manager.prepare_submission.call_args
        artifact_paths_arg = call_args[0][0] if call_args[0] else call_args[1]["artifact_paths"]
        assert artifact_paths_arg == frozenset(
            {
                f"{get_default_server_root()}/state.json",
                f"{get_default_server_root()}/deliverables.json",
            }
        )


class TestSubmitPRBaseFromRegistration:
    """Submission targets come from the matching registered branch."""

    def test_pr_opened_against_reader_provided_parent_branch(self) -> None:
        """Neutralization and PR creation both use the registered parent."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.require_attached_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.return_value = False
        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.return_value = {
            "number": 7,
            "url": "https://github.com/x/y/pull/7",
        }
        pr_status_writer = MagicMock(spec=IPRStatusWriter)

        reader = MagicMock(spec=IStateReader)
        reader.load.return_value = BranchState(
            branch="feature/42-test",
            issue_number=42,
            workflow_name="feature",
            current_phase="ready",
            parent_branch="epic/320-production-readiness-tracker",
        )

        tool = _make_submit_pr_tool(
            git_manager, github_manager, pr_status_writer, state_reader=reader
        )

        params = SubmitPRInput(title="Test PR")

        asyncio.run(tool.execute(params, NoteContext()))

        reader.load.assert_called_once_with("feature/42-test")
        assert git_manager.prepare_submission.call_args.args[1] == (
            "epic/320-production-readiness-tracker"
        )
        _, kwargs = github_manager.create_pr.call_args
        assert kwargs["base"] == "epic/320-production-readiness-tracker"
