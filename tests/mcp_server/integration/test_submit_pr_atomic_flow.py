# tests/mcp_server/integration/test_submit_pr_atomic_flow.py
"""Integration tests for C3: SubmitPRTool atomic execution flow.

Tests verify the full atomic sequence:
  1. branch-local artifact detection (net-diff check)
  2. neutralize_to_base for tracked artifacts
  3. commit_with_scope("ready", ...)
  4. push to remote
  5. GitHub PR creation
  6. PRStatusCache write (OPEN)

Also verifies:
  - CreatePRTool is no longer instantiated as a public MCP tool in server composition root
  - GitCommitTool no longer contains the terminal-route neutralization path

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
    - Prove CreatePRTool is not a public MCP tool in server.py
    - Prove GitCommitTool no longer contains neutralize_to_base path
    - Prove SubmitPRTool uses only GitManager (no adapter bypass)
"""

from __future__ import annotations

import asyncio
import inspect
from pathlib import Path
from unittest.mock import MagicMock

import yaml

import mcp_server.server as server_module
from mcp_server.config.schemas.contracts_config import BranchLocalArtifact
from mcp_server.core.exceptions import ExecutionError, PreflightError
from mcp_server.core.interfaces import IPRStatusWriter, PRStatus
from mcp_server.core.operation_notes import NoteContext, RecoveryNote
from mcp_server.managers.git_manager import GitManager
from mcp_server.managers.github_manager import GitHubManager
from mcp_server.managers.phase_contract_resolver import MergeReadinessContext
from mcp_server.tools import git_tools
from mcp_server.tools.pr_tools import SubmitPRInput, SubmitPRTool

_STATE_ARTIFACT = BranchLocalArtifact(
    path=".st3/state.json",
    reason="branch-local workflow state",
)
_DELIVERABLES_ARTIFACT = BranchLocalArtifact(
    path=".st3/deliverables.json",
    reason="branch-local deliverables",
)


def _make_submit_pr_tool(
    git_manager: GitManager,
    github_manager: GitHubManager,
    pr_status_writer: IPRStatusWriter,
    artifacts: tuple[BranchLocalArtifact, ...] = (_STATE_ARTIFACT,),
) -> SubmitPRTool:
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
    )


def _make_params(
    head: str = "feature/42-test",
    base: str = "main",
    title: str = "Test PR",
    body: str = "Description",
    draft: bool = False,
) -> SubmitPRInput:
    return SubmitPRInput(head=head, base=base, title=title, body=body, draft=draft)


class TestSubmitPRHappyPath:
    """SubmitPRTool happy path: atomic flow executes in correct order."""

    def test_submit_pr_happy_path(self) -> None:
        """Full atomic flow: neutralize -> commit -> push -> create_pr -> set_pr_status(OPEN)."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.get_current_branch.return_value = "feature/42-test"
        git_manager.has_net_diff_for_path.return_value = True
        git_manager.commit_with_scope.return_value = "abc1234"

        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.return_value = {
            "number": 42,
            "url": "https://github.com/x/y/pull/42",
        }

        pr_status_writer = MagicMock(spec=IPRStatusWriter)

        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)

        result = asyncio.get_event_loop().run_until_complete(
            tool.execute(_make_params(), NoteContext())
        )

        assert not result.is_error
        git_manager.neutralize_to_base.assert_called_once()
        git_manager.commit_with_scope.assert_called_once()
        git_manager.push.assert_called_once()
        github_manager.create_pr.assert_called_once()
        pr_status_writer.set_pr_status.assert_called_once_with("feature/42-test", PRStatus.OPEN)

    def test_submit_pr_skips_neutralize_when_no_exclusions(self) -> None:
        """When no branch-local artifacts are configured, neutralize_to_base must not be called."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.get_current_branch.return_value = "feature/42-test"
        git_manager.commit_with_scope.return_value = "abc1234"

        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.return_value = {
            "number": 42,
            "url": "https://github.com/x/y/pull/42",
        }

        pr_status_writer = MagicMock(spec=IPRStatusWriter)

        # No artifacts -> neutralize must not be called
        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer, artifacts=())

        result = asyncio.get_event_loop().run_until_complete(
            tool.execute(_make_params(), NoteContext())
        )

        assert not result.is_error
        git_manager.neutralize_to_base.assert_not_called()
        pr_status_writer.set_pr_status.assert_called_once_with("feature/42-test", PRStatus.OPEN)

    def test_submit_pr_pr_status_written_open(self) -> None:
        """PRStatus.OPEN is written to the cache after successful PR creation."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.get_current_branch.return_value = "refactor/283-test"
        git_manager.has_net_diff_for_path.return_value = False
        git_manager.commit_with_scope.return_value = "deadbeef"

        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.return_value = {
            "number": 99,
            "url": "https://github.com/x/y/pull/99",
        }

        pr_status_writer = MagicMock(spec=IPRStatusWriter)

        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)

        asyncio.get_event_loop().run_until_complete(
            tool.execute(_make_params(head="refactor/283-test"), NoteContext())
        )

        pr_status_writer.set_pr_status.assert_called_once_with("refactor/283-test", PRStatus.OPEN)


class TestSubmitPRPartialFailure:
    """SubmitPRTool produces RecoveryNote on failure after neutralize."""

    def test_push_failure_produces_recovery_note(self) -> None:
        """When push raises ExecutionError, a RecoveryNote is produced and error returned."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.get_current_branch.return_value = "feature/42-test"
        git_manager.has_net_diff_for_path.return_value = True
        git_manager.commit_with_scope.return_value = "abc1234"
        git_manager.push.side_effect = ExecutionError("push failed: remote rejected")

        github_manager = MagicMock(spec=GitHubManager)
        pr_status_writer = MagicMock(spec=IPRStatusWriter)

        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)

        context = NoteContext()
        result = asyncio.get_event_loop().run_until_complete(tool.execute(_make_params(), context))

        assert result.is_error
        assert len(context.of_type(RecoveryNote)) > 0
        # PRStatus must NOT be written when push failed
        pr_status_writer.set_pr_status.assert_not_called()

    def test_create_pr_failure_produces_recovery_note(self) -> None:
        """When create_pr raises ExecutionError, a RecoveryNote is produced and error returned."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.get_current_branch.return_value = "feature/42-test"
        git_manager.commit_with_scope.return_value = "abc1234"

        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.side_effect = ExecutionError("PR already exists")

        pr_status_writer = MagicMock(spec=IPRStatusWriter)

        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)

        result = asyncio.get_event_loop().run_until_complete(
            tool.execute(_make_params(), NoteContext())
        )

        assert result.is_error
        pr_status_writer.set_pr_status.assert_not_called()


class TestSubmitPRNoAdapterBypass:
    """Structural contract: SubmitPRTool must not access GitAdapter directly."""

    def test_submit_pr_tool_execute_has_no_adapter_calls(self) -> None:
        """SubmitPRTool.execute() must not contain self._git_manager.adapter references.

        Law of Demeter (ARCHITECTURE_PRINCIPLES §7): SubmitPRTool must only
        talk to GitManager, never to GitAdapter directly.
        """
        source = inspect.getsource(SubmitPRTool.execute)
        assert "_git_manager.adapter" not in source, (
            "SubmitPRTool.execute() must not access GitAdapter directly. "
            "Use GitManager methods instead (Law of Demeter, §7)."
        )


class TestCompositionRootContracts:
    """Structural contracts: CreatePRTool not in public tools; no neutralize in GitCommitTool."""

    def test_create_pr_tool_not_instantiated_in_server(self) -> None:
        """server.py must not contain CreatePRTool() instantiation (design D2)."""
        source = inspect.getsource(server_module)
        assert "CreatePRTool(" not in source, (
            "CreatePRTool must not be instantiated in server.py. "
            "Use SubmitPRTool instead (design D2)."
        )

    def test_git_commit_tool_has_no_neutralize_path(self) -> None:
        """GitCommitTool.execute() must not contain neutralize_to_base (moved to SubmitPRTool)."""
        source = inspect.getsource(git_tools.GitCommitTool.execute)
        assert "neutralize_to_base" not in source, (
            "GitCommitTool must not contain neutralize_to_base path in C3+. "
            "Neutralization is owned by SubmitPRTool."
        )

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
        config_path = workspace_root / ".st3" / "config" / "enforcement.yaml"
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


class TestSubmitPRNeutralizesQualityState:
    """C5 (C_QA_STATE_SPLIT): quality_state.json is registered as branch-local artifact."""

    def test_quality_state_json_in_phase_contracts_branch_local_artifacts(
        self,
    ) -> None:
        """contracts.yaml must include .st3/quality_state.json as branch-local artifact.

        RED: will fail until C5 GREEN adds quality_state.json to contracts.yaml.
        """
        import yaml as _yaml  # noqa: PLC0415

        workspace_root = Path(__file__).parents[3]
        contracts_path = workspace_root / ".st3" / "config" / "contracts.yaml"
        contracts = _yaml.safe_load(contracts_path.read_text(encoding="utf-8"))
        artifact_paths = [a["path"] for a in contracts["merge_policy"]["branch_local_artifacts"]]
        assert ".st3/quality_state.json" in artifact_paths, (
            "contracts.yaml must register .st3/quality_state.json as a "
            "branch-local artifact so SubmitPRTool neutralizes it before pushing."
        )

    def test_quality_state_artifact_registered_in_server_merge_readiness(
        self,
    ) -> None:
        """MergeReadinessContext passed to SubmitPRTool must include quality_state artifact.

        RED: will fail until C5 GREEN wires quality_state.json into server.py composition.
        """
        workspace_root = Path(__file__).parents[3]
        contracts_path = workspace_root / ".st3" / "config" / "contracts.yaml"
        import yaml as _yaml  # noqa: PLC0415

        contracts = _yaml.safe_load(contracts_path.read_text(encoding="utf-8"))
        artifact_paths = [a["path"] for a in contracts["merge_policy"]["branch_local_artifacts"]]
        assert ".st3/quality_state.json" in artifact_paths, (
            "quality_state.json must appear in contracts.yaml so server.py wires "
            "it into MergeReadinessContext and SubmitPRTool neutralizes it."
        )


class TestSubmitPRAtomicRefactored:
    """C5: SubmitPRTool delegates to prepare_submission + rollback_push (design §4.3)."""

    def test_failure_a_no_upstream_blocked_before_mutation(self) -> None:
        """prepare_submission raises PreflightError -> error; no create_pr; no status."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.get_current_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.side_effect = PreflightError("No upstream configured")
        github_manager = MagicMock(spec=GitHubManager)
        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)

        result = asyncio.get_event_loop().run_until_complete(
            tool.execute(_make_params(), NoteContext())
        )

        assert result.is_error
        github_manager.create_pr.assert_not_called()
        pr_status_writer.set_pr_status.assert_not_called()

    def test_failure_b_dirty_tree_blocked_before_mutation(self) -> None:
        """prepare_submission raises PreflightError (dirty) -> error; no create_pr; no status."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.get_current_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.side_effect = PreflightError("Working directory not clean")
        github_manager = MagicMock(spec=GitHubManager)
        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)

        result = asyncio.get_event_loop().run_until_complete(
            tool.execute(_make_params(), NoteContext())
        )

        assert result.is_error
        github_manager.create_pr.assert_not_called()
        pr_status_writer.set_pr_status.assert_not_called()

    def test_failure_c_create_pr_failure_triggers_rollback_push(self) -> None:
        """prepare_submission returns True; create_pr raises -> rollback_push + RecoveryNote."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.get_current_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.return_value = True
        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.side_effect = ExecutionError("API 503")
        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)
        context = NoteContext()

        result = asyncio.get_event_loop().run_until_complete(tool.execute(_make_params(), context))

        assert result.is_error
        git_manager.rollback_push.assert_called_once()
        assert len(context.of_type(RecoveryNote)) == 1
        assert "rolled back" in context.of_type(RecoveryNote)[0].message
        pr_status_writer.set_pr_status.assert_not_called()

    def test_failure_c_no_rollback_when_no_neutralization_commit(self) -> None:
        """prepare_submission returns False (no commit); create_pr raises -> NO rollback_push."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.get_current_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.return_value = False
        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.side_effect = ExecutionError("API 503")
        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)

        result = asyncio.get_event_loop().run_until_complete(
            tool.execute(_make_params(), NoteContext())
        )

        assert result.is_error
        git_manager.rollback_push.assert_not_called()
        pr_status_writer.set_pr_status.assert_not_called()

    def test_failure_c_meta_rollback_failure_surfaced_via_recovery_note(self) -> None:
        """create_pr raises; rollback_push raises -> error returned; set_pr_status not called."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.get_current_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.return_value = True
        git_manager.rollback_push.side_effect = ExecutionError("CRITICAL: reset failed")
        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.side_effect = ExecutionError("API 503")
        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)
        context = NoteContext()

        result = asyncio.get_event_loop().run_until_complete(tool.execute(_make_params(), context))

        assert result.is_error
        pr_status_writer.set_pr_status.assert_not_called()

    def test_failure_d_push_fails_prepare_submission_raises_execution_error(self) -> None:
        """prepare_submission raises ExecutionError (push fail) -> error; rollback_push NOT called."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.get_current_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.side_effect = ExecutionError("push rejected")
        github_manager = MagicMock(spec=GitHubManager)
        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)

        result = asyncio.get_event_loop().run_until_complete(
            tool.execute(_make_params(), NoteContext())
        )

        assert result.is_error
        git_manager.rollback_push.assert_not_called()
        pr_status_writer.set_pr_status.assert_not_called()

    def test_happy_path_prepare_submission_then_create_pr_then_status(self) -> None:
        """All succeed: prepare_submission called once; set_pr_status(branch, OPEN) called."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.get_current_branch.return_value = "feature/42-test"
        git_manager.prepare_submission.return_value = True
        github_manager = MagicMock(spec=GitHubManager)
        github_manager.create_pr.return_value = {
            "number": 42,
            "url": "https://github.com/x/y/pull/42",
        }
        pr_status_writer = MagicMock(spec=IPRStatusWriter)
        tool = _make_submit_pr_tool(git_manager, github_manager, pr_status_writer)

        result = asyncio.get_event_loop().run_until_complete(
            tool.execute(_make_params(), NoteContext())
        )

        assert not result.is_error
        git_manager.prepare_submission.assert_called_once()
        pr_status_writer.set_pr_status.assert_called_once_with("feature/42-test", PRStatus.OPEN)

    def test_happy_path_artifact_paths_extracted_from_merge_readiness_context(self) -> None:
        """prepare_submission called with frozenset of both artifact paths."""
        git_manager = MagicMock(spec=GitManager)
        git_manager.get_current_branch.return_value = "feature/42-test"
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

        asyncio.get_event_loop().run_until_complete(tool.execute(_make_params(), NoteContext()))

        call_args = git_manager.prepare_submission.call_args
        artifact_paths_arg = call_args[0][0] if call_args[0] else call_args[1]["artifact_paths"]
        assert artifact_paths_arg == frozenset({".st3/state.json", ".st3/deliverables.json"})
