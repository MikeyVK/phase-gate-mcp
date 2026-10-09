"""Tests for ProjectManager with workflow-based initialization.

Issue #50: Tests migrated from PHASE_TEMPLATES to workflows.yaml.
- Workflow selection from workflows.yaml
- Execution mode handling (interactive/autonomous)
- Custom phases with skip_reason
- Project plan storage in .pgmcp/deliverables.json

@layer: Tests (Unit)
@dependencies: pytest, tests.mcp_server.test_support, mcp_server.managers.project_manager
"""

import json
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from mcp_server.core.exceptions import PlanningVersionMismatchError, StateCorruptedError
from mcp_server.core.interfaces.git import CycleEvidence
from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.project_manager import ProjectInitOptions, ProjectManager
from mcp_server.managers.state_repository import StateBranchMismatchError, StateNotFoundError
from mcp_server.schemas import ContractsConfig
from mcp_server.schemas.deliverables import (
    AppendCycle,
    CycleInput,
    CyclesInput,
    DeliverableInput,
    PhaseBlockInput,
    PlanningMutationError,
    RemoveCycle,
    RemovePhase,
    ReplaceCycle,
    SavePlanningModel,
    SetPhase,
    StoredPlanningModel,
)
from mcp_server.state.workflow_status import WorkflowStatusDTO
from tests.mcp_server.test_support import (
    get_default_server_root,
    load_contracts_config,
    load_workflow_config,
    make_project_manager,
)


class TestProjectManagerWorkflows:
    """Test ProjectManager with workflows.yaml integration."""

    @pytest.fixture
    def workspace_root(self, legacy_suite_workspace: Path) -> Path:
        """Create temporary workspace.

        Args:
            legacy_suite_workspace: Pytest legacy_suite_workspace fixture

        Returns:
            Path to temporary workspace root
        """
        return legacy_suite_workspace

    @pytest.fixture
    def manager(self, workspace_root: Path) -> ProjectManager:
        """Create ProjectManager instance."""
        return make_project_manager(workspace_root)

    def test_workflows_loaded_from_yaml(self, legacy_suite_workspace: Path) -> None:
        """Test that workflows are loaded from workflows.yaml."""
        workflow_config = load_workflow_config(legacy_suite_workspace)
        assert "feature" in workflow_config.workflows
        assert "bug" in workflow_config.workflows
        assert "hotfix" in workflow_config.workflows
        assert "refactor" in workflow_config.workflows
        assert "docs" in workflow_config.workflows

    def test_feature_workflow_has_6_phases(self, legacy_suite_workspace: Path) -> None:
        """Test feature workflow phase count from contracts.yaml (C6+: SSOT).

        Feature workflow has 7 phases including 'ready' terminal phase.
        """
        phases = load_contracts_config(legacy_suite_workspace).get_phases("feature")
        assert len(phases) == 7
        expected = [
            "research",
            "design",
            "planning",
            "implementation",
            "validation",
            "documentation",
            "ready",
        ]
        assert phases == expected
        wf = load_workflow_config(legacy_suite_workspace).get_workflow("feature")
        assert wf.default_execution_mode == "interactive"

    def test_hotfix_workflow_has_3_phases_autonomous(self, legacy_suite_workspace: Path) -> None:
        """Test hotfix workflow from contracts.yaml (C6+: SSOT).

        Hotfix workflow has 4 phases including 'ready' terminal phase.
        """
        phases = load_contracts_config(legacy_suite_workspace).get_phases("hotfix")
        assert len(phases) == 4
        assert phases == ["implementation", "validation", "documentation", "ready"]
        assert (
            load_workflow_config(legacy_suite_workspace)
            .get_workflow("hotfix")
            .default_execution_mode
            == "autonomous"
        )

    def test_initialize_project_with_feature_workflow(
        self, manager: ProjectManager, workspace_root: Path
    ) -> None:
        """Test initialize_project with feature workflow."""
        result = manager.initialize_project(
            issue_number=42, issue_title="Add user authentication", workflow_name="feature"
        )

        assert result["success"] is True
        assert result["workflow_name"] == "feature"
        assert result["execution_mode"] == "interactive"
        assert len(result["required_phases"]) == 7

        plan = manager.get_project_plan(42)
        assert plan is not None
        assert plan["workflow_name"] == "feature"
        assert plan["execution_mode"] == "interactive"
        assert len(plan["required_phases"]) == 7

    def test_initialize_project_with_hotfix_workflow(
        self, manager: ProjectManager, workspace_root: Path
    ) -> None:
        """Test initialize_project with hotfix workflow.

        contracts.yaml SSOT — execution_mode defaults to interactive.
        """
        result = manager.initialize_project(
            issue_number=99, issue_title="Critical security fix", workflow_name="hotfix"
        )

        assert result["success"] is True
        assert result["workflow_name"] == "hotfix"
        assert result["execution_mode"] == "interactive"
        assert len(result["required_phases"]) == 4

        plan = manager.get_project_plan(99)
        assert plan is not None
        assert plan["execution_mode"] == "interactive"

    def test_initialize_project_with_execution_mode_override(
        self, manager: ProjectManager, workspace_root: Path
    ) -> None:
        """Test execution_mode override (feature normally interactive)."""
        result = manager.initialize_project(
            issue_number=77,
            issue_title="Test",
            workflow_name="feature",
            options=ProjectInitOptions(execution_mode="autonomous"),
        )

        assert result["execution_mode"] == "autonomous"

        plan = manager.get_project_plan(77)
        assert plan is not None
        assert plan["execution_mode"] == "autonomous"

    def test_initialize_project_with_custom_phases(
        self, manager: ProjectManager, workspace_root: Path
    ) -> None:
        """Test initialize_project with custom phases."""
        custom_phases = (
            "research",
            "planning",
            "design",
            "implementation",
            "validation",
            "documentation",
        )

        result = manager.initialize_project(
            issue_number=50,
            issue_title="Complex refactor",
            workflow_name="refactor",
            options=ProjectInitOptions(
                custom_phases=custom_phases, skip_reason="Adding design phase for complex refactor"
            ),
        )

        assert result["success"] is True
        assert result["workflow_name"] == "refactor"
        assert result["required_phases"] == custom_phases
        assert result["skip_reason"] == "Adding design phase for complex refactor"

        plan = manager.get_project_plan(50)
        assert plan is not None
        assert tuple(plan["required_phases"]) == custom_phases
        assert plan["skip_reason"] == "Adding design phase for complex refactor"

    def test_initialize_project_invalid_workflow(self, manager: ProjectManager) -> None:
        """Test initialize_project rejects unknown workflow."""
        with pytest.raises(ValueError) as exc_info:
            manager.initialize_project(
                issue_number=999, issue_title="Test", workflow_name="invalid_workflow"
            )

        error_msg = str(exc_info.value)
        assert "Unknown workflow: 'invalid_workflow'" in error_msg
        assert "Available:" in error_msg

    def test_initialize_project_invalid_execution_mode(self, manager: ProjectManager) -> None:
        """Test initialize_project rejects invalid execution_mode."""
        with pytest.raises(ValueError) as exc_info:
            manager.initialize_project(
                issue_number=888,
                issue_title="Test",
                workflow_name="feature",
                options=ProjectInitOptions(execution_mode="manual"),
            )

        error_msg = str(exc_info.value)
        assert "Invalid execution_mode: 'manual'" in error_msg
        assert "Valid values: 'interactive', 'autonomous'" in error_msg

    def test_initialize_project_custom_phases_without_skip_reason(
        self, manager: ProjectManager
    ) -> None:
        """Test initialize_project requires skip_reason with custom_phases."""
        with pytest.raises(ValueError) as exc_info:
            manager.initialize_project(
                issue_number=777,
                issue_title="Test",
                workflow_name="feature",
                options=ProjectInitOptions(custom_phases=("research", "implementation")),
            )

        error_msg = str(exc_info.value)
        assert "skip_reason required when custom_phases provided" in error_msg

    def test_get_project_plan_returns_stored_plan(self, manager: ProjectManager) -> None:
        """Test get_project_plan retrieves stored project plan."""
        # Initialize project
        manager.initialize_project(issue_number=42, issue_title="Test", workflow_name="feature")

        # Retrieve plan
        plan = manager.get_project_plan(issue_number=42)
        assert plan is not None
        assert plan["workflow_name"] == "feature"
        assert plan["execution_mode"] == "interactive"
        assert len(plan["required_phases"]) == 7

    def test_get_project_plan_nonexistent_returns_none(self, manager: ProjectManager) -> None:
        """Test get_project_plan returns None for nonexistent project."""
        plan = manager.get_project_plan(issue_number=999)
        assert plan is None

    def test_initialize_project_with_parent_branch(self, manager: ProjectManager) -> None:
        """Test initializing project with explicit parent_branch.

        Issue #79: parent_branch tracking for merge targets.
        """
        result = manager.initialize_project(
            issue_number=79,
            issue_title="Add parent branch tracking",
            workflow_name="feature",
            options=ProjectInitOptions(parent_branch="epic/76-quality-gates-tooling"),
        )

        # Verify parent_branch in returned result
        assert result["parent_branch"] == "epic/76-quality-gates-tooling"

        # Verify persisted to deliverables.json
        plan = manager.get_project_plan(issue_number=79)
        assert plan is not None
        assert plan["parent_branch"] == "epic/76-quality-gates-tooling"

    def test_initialize_project_without_parent_branch(self, manager: ProjectManager) -> None:
        """Test initializing project without parent_branch (backward compat).

        Issue #79: parent_branch is optional for existing workflows.
        """
        result = manager.initialize_project(
            issue_number=80, issue_title="Old style project", workflow_name="bug"
        )

        # Verify parent_branch is None
        assert result["parent_branch"] is None

        # Verify persisted as None
        plan = manager.get_project_plan(issue_number=80)
        assert plan is not None
        assert plan["parent_branch"] is None


class TestProjectManagerPhaseDetection:
    """Test ProjectManager phase detection (Issue #139).

    Cycle 3.2: get_project_plan should return current_phase via ScopeDecoder.
    """

    @pytest.fixture
    def workspace_root(self, legacy_suite_workspace: Path) -> Path:
        """Create temporary workspace with .pgmcp directory."""
        phase_gate_dir = legacy_suite_workspace / get_default_server_root()
        phase_gate_dir.mkdir(exist_ok=True)

        # Create workphases.yaml
        workphases_path = phase_gate_dir / "workphases.yaml"
        workphases_path.write_text(
            """
version: "1.0.0"
phases:
  research:
    display_name: "Research"
    commit_type_hint: "docs"
    subphases: []
  implementation:
    display_name: "Implementation"
    commit_type_hint: null
    subphases: ["red", "green", "refactor"]
  documentation:
    display_name: "Documentation"
    commit_type_hint: "docs"
    subphases: ["reference", "guides"]
"""
        )

        return legacy_suite_workspace

    @pytest.fixture
    def manager(self, workspace_root: Path) -> ProjectManager:
        """Create ProjectManager instance."""
        return make_project_manager(workspace_root)

    def test_get_project_plan_includes_current_phase_from_state_json(
        self, legacy_suite_workspace: Path
    ) -> None:
        """After #298: current_phase comes from state.json via resolver when state present.

        Issue #139: Phase detection is now state.json-authoritative (not commit-scope).
        """
        resolver = MagicMock()
        resolver.resolve_current.return_value = WorkflowStatusDTO(
            current_phase="implementation",
            sub_phase=None,
            current_cycle=None,
            phase_source="state.json",
            phase_confidence="high",
            phase_detection_error=None,
        )
        manager = make_project_manager(legacy_suite_workspace, workflow_status_resolver=resolver)
        manager.initialize_project(
            issue_number=139,
            issue_title="Add current_phase to get_project_plan",
            workflow_name="feature",
        )

        plan = manager.get_project_plan(issue_number=139)

        assert plan is not None
        assert "current_phase" in plan
        assert plan["phase_source"] == "state.json"
        assert "phase_detection_error" in plan

    def test_get_project_plan_has_no_phase_fields_when_state_absent(
        self, legacy_suite_workspace: Path
    ) -> None:
        """After #298: when resolver raises StateNotFoundError, plan has no phase fields.

        Issue #140: No state.json → plan returned without phase metadata.
        """
        resolver = MagicMock()
        resolver.resolve_current.side_effect = StateNotFoundError("no-state-branch")
        manager = make_project_manager(legacy_suite_workspace, workflow_status_resolver=resolver)

        manager.initialize_project(
            issue_number=140,
            issue_title="Test unknown phase",
            workflow_name="bug",
        )

        plan = manager.get_project_plan(issue_number=140)

        assert plan is not None
        assert "current_phase" not in plan
        assert "phase_source" not in plan


class EvidenceReader:
    """Explicit controllable read-only evidence; each invocation is recorded."""

    def __init__(self, evidence: CycleEvidence) -> None:
        self.evidence = evidence
        self.calls: list[tuple[int, str | None]] = []
        self.action: Callable[[], None] | None = None

    def read_cycle_evidence(self, issue_number: int, execution_phase: str | None) -> CycleEvidence:
        self.calls.append((issue_number, execution_phase))
        if self.action is not None:
            self.action()
        return replace(self.evidence, execution_phase=execution_phase)


def author_cycle(name: str) -> CycleInput:
    return CycleInput(
        cycle_name=name,
        deliverables=[
            DeliverableInput(deliverable_name="Result", description=f"Result for {name}")
        ],
        exit_criteria="Behavior demonstrated",
    )


def phase_block(name: str) -> PhaseBlockInput:
    return PhaseBlockInput(
        deliverables=[DeliverableInput(deliverable_name=name, description=f"Evidence for {name}")]
    )


def stored_plan(manager: ProjectManager) -> StoredPlanningModel:
    plan = manager.get_project_plan(491)
    assert plan is not None
    return StoredPlanningModel.model_validate(plan["planning_deliverables"])


@pytest.fixture
def evidence_reader() -> EvidenceReader:
    return EvidenceReader(CycleEvidence("complete", "refactor/491-planning", "head", None, ()))


@pytest.fixture
def planning_manager(
    legacy_suite_workspace: Path, evidence_reader: EvidenceReader
) -> ProjectManager:
    manager = make_project_manager(legacy_suite_workspace, cycle_evidence_reader=evidence_reader)
    manager.initialize_project(491, "Planning contracts", "refactor")
    manager.save_planning_deliverables(
        491,
        SavePlanningModel(
            cycles=CyclesInput(
                cycles=[author_cycle(name) for name in ("First", "Second", "Third")]
            ),
            phases={"validation": phase_block("Report"), "documentation": phase_block("Guide")},
        ),
    )
    return manager


class TestPlanningDeliverablesSchema:
    """Complete block mutations and durable readback through the public manager."""

    def test_save_derives_names_and_references_and_is_write_once(
        self, planning_manager: ProjectManager
    ) -> None:
        saved = stored_plan(planning_manager)
        assert saved.cycles is not None
        assert saved.cycles.total == 3
        assert [cycle.cycle_id for cycle in saved.cycles.cycles] == ["C_1", "C_2", "C_3"]
        assert [cycle.cycle_name for cycle in saved.cycles.cycles] == ["First", "Second", "Third"]
        assert saved.cycles.cycles[1].deliverables[0].deliverable_id == "D_2.1"
        assert saved.phases["validation"].deliverables[0].deliverable_id == "D_1"
        raw = json.loads(planning_manager.deliverables_file.read_text(encoding="utf-8"))
        assert raw["projects"]["491"]["planning_deliverables"] == saved.model_dump(
            exclude_none=True
        )
        before = planning_manager.deliverables_file.read_bytes()
        with pytest.raises(PlanningMutationError, match="planning_already_saved"):
            planning_manager.save_planning_deliverables(
                491, SavePlanningModel(cycles=CyclesInput(cycles=[author_cycle("Replacement")]))
            )
        assert planning_manager.deliverables_file.read_bytes() == before

    def test_operations_target_original_snapshot_and_replace_whole_blocks(
        self, planning_manager: ProjectManager, evidence_reader: EvidenceReader
    ) -> None:
        untouched = stored_plan(planning_manager).phases["documentation"]
        planning_manager.update_planning_deliverables(
            491,
            [
                RemoveCycle(op="remove_cycle", cycle_id="C_2"),
                ReplaceCycle(
                    op="replace_cycle", cycle_id="C_3", cycle=author_cycle("Changed third")
                ),
                AppendCycle(op="append_cycle", cycle=author_cycle("Append one")),
                AppendCycle(op="append_cycle", cycle=author_cycle("Append two")),
                SetPhase(op="set_phase", phase="validation", block=phase_block("New report")),
            ],
            context=NoteContext(),
        )
        result = stored_plan(planning_manager)
        assert result.cycles is not None
        assert result.cycles.total == 4
        assert [cycle.cycle_name for cycle in result.cycles.cycles] == [
            "First",
            "Changed third",
            "Append one",
            "Append two",
        ]
        assert result.cycles.cycles[1].deliverables[0].deliverable_id == "D_2.1"
        assert result.phases["documentation"] == untouched
        assert [d.deliverable_name for d in result.phases["validation"].deliverables] == [
            "New report"
        ]
        planning_manager.update_planning_deliverables(
            491, [RemovePhase(op="remove_phase", phase="documentation")], context=NoteContext()
        )
        assert "documentation" not in stored_plan(planning_manager).phases
        assert evidence_reader.calls == [(491, "implementation"), (491, "implementation")]

    @pytest.mark.parametrize("target", ["cycle", "phase"])
    @pytest.mark.parametrize("failure", ["missing", "duplicate"])
    def test_ambiguous_or_missing_targets_leave_bytes_unchanged(
        self, planning_manager: ProjectManager, target: str, failure: str
    ) -> None:
        before = planning_manager.deliverables_file.read_bytes()
        if target == "cycle":
            operation = RemoveCycle(
                op="remove_cycle", cycle_id="C_9" if failure == "missing" else "C_2"
            )
        else:
            operation = RemovePhase(
                op="remove_phase", phase="design" if failure == "missing" else "validation"
            )
        operations = [operation] if failure == "missing" else [operation, operation]
        with pytest.raises(
            PlanningMutationError,
            match="planning_duplicate_target"
            if failure == "duplicate"
            else "planning_target_missing",
        ):
            planning_manager.update_planning_deliverables(491, operations, context=NoteContext())
        assert planning_manager.deliverables_file.read_bytes() == before

    @pytest.mark.parametrize("removed", ["C_1", "C_2"])
    def test_evidenced_cycles_cannot_be_deleted_or_renumbered_even_with_force(
        self, planning_manager: ProjectManager, evidence_reader: EvidenceReader, removed: str
    ) -> None:
        evidence_reader.evidence = replace(
            evidence_reader.evidence,
            status="unavailable",
            protected_cycle_numbers=(1, 3),
            reason_code="git_history_shallow",
        )
        before = planning_manager.deliverables_file.read_bytes()
        with pytest.raises(PlanningMutationError, match="planning_cycle_protected"):
            planning_manager.update_planning_deliverables(
                491,
                [RemoveCycle(op="remove_cycle", cycle_id=removed)],
                context=NoteContext(),
                force=True,
            )
        assert planning_manager.deliverables_file.read_bytes() == before
        assert len(evidence_reader.calls) == 1

    def test_protected_content_can_be_replaced_without_changing_identity(
        self, planning_manager: ProjectManager, evidence_reader: EvidenceReader
    ) -> None:
        evidence_reader.evidence = replace(evidence_reader.evidence, protected_cycle_numbers=(2,))
        planning_manager.update_planning_deliverables(
            491,
            [ReplaceCycle(op="replace_cycle", cycle_id="C_2", cycle=author_cycle("Revised"))],
            context=NoteContext(),
        )
        result = stored_plan(planning_manager)
        assert result.cycles is not None
        assert result.cycles.cycles[1].cycle_id == "C_2"
        assert result.cycles.cycles[1].cycle_name == "Revised"

    @pytest.mark.parametrize("retry_complete", [False, True])
    def test_force_retries_evidence_and_reports_only_a_successful_override(
        self,
        planning_manager: ProjectManager,
        evidence_reader: EvidenceReader,
        retry_complete: bool,
    ) -> None:
        evidence_reader.evidence = replace(
            evidence_reader.evidence, status="unavailable", reason_code="git_history_unavailable"
        )
        operations = [SetPhase(op="set_phase", phase="validation", block=phase_block("Revised"))]
        before = planning_manager.deliverables_file.read_bytes()
        rejected_context = NoteContext()
        with pytest.raises(PlanningMutationError, match="planning_evidence_unavailable"):
            planning_manager.update_planning_deliverables(491, operations, context=rejected_context)
        assert planning_manager.deliverables_file.read_bytes() == before
        assert rejected_context.entries[0].params["evidence_overridden"] is False
        if retry_complete:
            evidence_reader.evidence = replace(
                evidence_reader.evidence, status="complete", reason_code=None
            )
        context = NoteContext()
        planning_manager.update_planning_deliverables(491, operations, context=context, force=True)
        assert len(evidence_reader.calls) == 2
        assert context.entries[0].params["evidence_overridden"] is (not retry_complete)
        assert context.entries[0].params["head_sha"] == "head"

    @pytest.mark.parametrize("reason", ["branch_issue_mismatch", "git_snapshot_changed"])
    def test_force_does_not_override_identity_conflicts(
        self, planning_manager: ProjectManager, evidence_reader: EvidenceReader, reason: str
    ) -> None:
        evidence_reader.evidence = replace(
            evidence_reader.evidence, status="unavailable", reason_code=reason
        )
        before = planning_manager.deliverables_file.read_bytes()
        with pytest.raises(PlanningMutationError, match="planning_identity_conflict"):
            planning_manager.update_planning_deliverables(
                491,
                [SetPhase(op="set_phase", phase="validation", block=phase_block("Changed"))],
                context=NoteContext(),
                force=True,
            )
        assert planning_manager.deliverables_file.read_bytes() == before

    def test_concurrent_plan_changes_are_not_overwritten(
        self, planning_manager: ProjectManager, evidence_reader: EvidenceReader
    ) -> None:
        original = stored_plan(planning_manager)

        def replace_snapshot() -> None:
            envelope = json.loads(planning_manager.deliverables_file.read_text(encoding="utf-8"))
            envelope["projects"]["491"]["issue_title"] = "Concurrent change"
            planning_manager.deliverables_file.write_text(json.dumps(envelope), encoding="utf-8")

        evidence_reader.action = replace_snapshot
        with pytest.raises(PlanningMutationError, match="planning_snapshot_conflict"):
            planning_manager.update_planning_deliverables(
                491,
                [RemoveCycle(op="remove_cycle", cycle_id="C_2")],
                context=NoteContext(),
                force=True,
            )
        assert stored_plan(planning_manager) == original
        plan = planning_manager.get_project_plan(491)
        assert plan is not None
        assert plan["issue_title"] == "Concurrent change"

    def test_failed_persistence_does_not_publish_an_accepted_override(
        self, planning_manager: ProjectManager, evidence_reader: EvidenceReader
    ) -> None:
        evidence_reader.evidence = replace(
            evidence_reader.evidence, status="unavailable", reason_code="git_history_unavailable"
        )
        context = NoteContext()
        before = planning_manager.deliverables_file.read_bytes()
        with (
            patch(
                "mcp_server.utils.atomic_json_writer.AtomicJsonWriter.write_json",
                side_effect=OSError("disk"),
            ),
            pytest.raises(OSError, match="disk"),
        ):
            planning_manager.update_planning_deliverables(
                491,
                [RemoveCycle(op="remove_cycle", cycle_id="C_2")],
                context=context,
                force=True,
            )
        assert not any(note.params["evidence_overridden"] for note in context.entries)
        assert planning_manager.deliverables_file.read_bytes() == before

    @pytest.mark.parametrize("phase", ["implementation", "unconfigured"])
    def test_invalid_phase_membership_rejects_save_and_update(
        self, planning_manager: ProjectManager, phase: str
    ) -> None:
        planning_manager.initialize_project(492, "Invalid membership", "refactor")
        before = planning_manager.deliverables_file.read_bytes()
        with pytest.raises(PlanningMutationError, match="planning_phase_invalid"):
            planning_manager.save_planning_deliverables(
                492,
                SavePlanningModel(
                    cycles=CyclesInput(cycles=[author_cycle("First")]),
                    phases={phase: phase_block("Wrong")},
                ),
            )
        assert planning_manager.deliverables_file.read_bytes() == before
        with pytest.raises(PlanningMutationError, match="planning_phase_invalid"):
            planning_manager.update_planning_deliverables(
                491,
                [SetPhase(op="set_phase", phase=phase, block=phase_block("Wrong"))],
                context=NoteContext(),
                force=True,
            )
        assert planning_manager.deliverables_file.read_bytes() == before

    def test_required_cycle_cannot_be_removed(
        self, legacy_suite_workspace: Path, evidence_reader: EvidenceReader
    ) -> None:
        manager = make_project_manager(
            legacy_suite_workspace, cycle_evidence_reader=evidence_reader
        )
        manager.initialize_project(491, "One cycle", "refactor")
        manager.save_planning_deliverables(
            491,
            SavePlanningModel(
                cycles=CyclesInput(cycles=[author_cycle("Only")]),
                phases={"validation": phase_block("Report")},
            ),
        )
        before = manager.deliverables_file.read_bytes()
        with pytest.raises(PlanningMutationError, match="planning_cycles_required"):
            manager.update_planning_deliverables(
                491, [RemoveCycle(op="remove_cycle", cycle_id="C_1")], context=NoteContext()
            )
        assert manager.deliverables_file.read_bytes() == before

    @pytest.mark.parametrize(
        ("workflow", "authoring", "error"),
        [
            (
                "refactor",
                SavePlanningModel(phases={"validation": phase_block("Report")}),
                "planning_cycles_required",
            ),
            (
                "docs",
                SavePlanningModel(cycles=CyclesInput(cycles=[author_cycle("Not admitted")])),
                "planning_cycles_forbidden",
            ),
        ],
    )
    def test_initial_cycle_requirement_is_configured(
        self, legacy_suite_workspace: Path, workflow: str, authoring: SavePlanningModel, error: str
    ) -> None:
        manager = make_project_manager(legacy_suite_workspace)
        manager.initialize_project(491, "Configured behavior", workflow)
        before = manager.deliverables_file.read_bytes()
        with pytest.raises(PlanningMutationError, match=error):
            manager.save_planning_deliverables(491, authoring)
        assert manager.deliverables_file.read_bytes() == before

    def test_alternative_configured_execution_phase_is_passed_to_evidence(
        self, legacy_suite_workspace: Path, evidence_reader: EvidenceReader
    ) -> None:
        raw = load_contracts_config(legacy_suite_workspace).model_dump()
        phases = raw["workflows"]["refactor"]["phases"]
        next(phase for phase in phases if phase["cycle_based"])["name"] = "build"
        manager = make_project_manager(
            legacy_suite_workspace,
            contracts_config=ContractsConfig.model_validate(raw),
            cycle_evidence_reader=evidence_reader,
        )
        manager.initialize_project(491, "Alternate phase", "refactor")
        manager.save_planning_deliverables(
            491, SavePlanningModel(cycles=CyclesInput(cycles=[author_cycle("Only")]))
        )
        manager.update_planning_deliverables(
            491, [AppendCycle(op="append_cycle", cycle=author_cycle("Next"))], context=NoteContext()
        )
        assert evidence_reader.calls == [(491, "build")]

    def test_invalid_stored_references_are_never_repaired_by_query_or_update(
        self, planning_manager: ProjectManager, evidence_reader: EvidenceReader
    ) -> None:
        envelope = json.loads(planning_manager.deliverables_file.read_text(encoding="utf-8"))
        envelope["projects"]["491"]["planning_deliverables"]["cycles"]["cycles"][0]["cycle_id"] = (
            "C_9"
        )
        planning_manager.deliverables_file.write_text(json.dumps(envelope), encoding="utf-8")
        before = planning_manager.deliverables_file.read_bytes()
        backup = planning_manager.deliverables_file.with_suffix(".json.bak")
        backup.write_bytes(b"Recovery point")
        with pytest.raises(PlanningMutationError, match="planning_stored_invalid"):
            planning_manager.get_project_plan(491)
        with pytest.raises(PlanningMutationError, match="planning_stored_invalid"):
            planning_manager.update_planning_deliverables(
                491,
                [RemoveCycle(op="remove_cycle", cycle_id="C_2")],
                context=NoteContext(),
                force=True,
            )
        assert planning_manager.deliverables_file.read_bytes() == before
        assert backup.read_bytes() == b"Recovery point"
        assert evidence_reader.calls == []

    @pytest.mark.parametrize(
        "field", ["cycle_name", "exit_criteria", "deliverable_name", "description"]
    )
    def test_complete_authoring_blocks_require_meaningful_text(self, field: str) -> None:
        raw = author_cycle("Complete").model_dump()
        if field in {"cycle_name", "exit_criteria"}:
            raw[field] = "   "
        else:
            raw["deliverables"][0][field] = "   "
        with pytest.raises(ValidationError):
            CycleInput.model_validate(raw)

    def test_null_cycles_and_empty_plan_have_no_authoring_meaning(self) -> None:
        with pytest.raises(ValidationError):
            SavePlanningModel.model_validate(
                {"cycles": None, "phases": {"validation": phase_block("Report")}}
            )
        with pytest.raises(ValidationError):
            SavePlanningModel.model_validate({})


class TestProjectManagerResolverAdoption:
    """C4: WorkflowStatusResolver adoption in ProjectManager.get_project_plan().

    Issue #231: These tests FAIL (RED) until WorkflowStatusResolver is injected
    into ProjectManager and used in get_project_plan().
    """

    def test_get_project_plan_uses_resolver_phase(self, legacy_suite_workspace: Path) -> None:
        """get_project_plan uses WorkflowStatusResolver.resolve_current() when injected."""
        resolver = MagicMock()
        resolver.resolve_current.return_value = WorkflowStatusDTO(
            current_phase="research",
            sub_phase=None,
            current_cycle=None,
            phase_source="state.json",
            phase_confidence="high",
            phase_detection_error=None,
        )
        manager = make_project_manager(legacy_suite_workspace, workflow_status_resolver=resolver)
        manager.initialize_project(99, "Test resolver adoption", "feature")

        plan = manager.get_project_plan(99)

        assert plan is not None
        assert plan["current_phase"] == "research"
        assert plan["phase_source"] == "state.json"
        resolver.resolve_current.assert_called_once()

    def test_get_project_plan_formats_phase_colon_sub_phase(
        self, legacy_suite_workspace: Path
    ) -> None:
        """get_project_plan formats 'phase:sub_phase' when resolver returns sub_phase."""
        resolver = MagicMock()
        resolver.resolve_current.return_value = WorkflowStatusDTO(
            current_phase="implementation",
            sub_phase="red",
            current_cycle=1,
            phase_source="state.json",
            phase_confidence="high",
            phase_detection_error=None,
        )
        manager = make_project_manager(legacy_suite_workspace, workflow_status_resolver=resolver)
        manager.initialize_project(100, "Test sub-phase format", "feature")

        plan = manager.get_project_plan(100)

        assert plan is not None
        assert plan["current_phase"] == "implementation:red"

    def test_get_project_plan_passes_resolver_error_to_plan(
        self, legacy_suite_workspace: Path
    ) -> None:
        """get_project_plan propagates phase_detection_error from resolver."""
        resolver = MagicMock()
        resolver.resolve_current.return_value = WorkflowStatusDTO(
            current_phase="implementation",
            sub_phase=None,
            current_cycle=None,
            phase_source="state.json",
            phase_confidence="high",
            phase_detection_error="Phase detection failed: no state file",
        )
        manager = make_project_manager(legacy_suite_workspace, workflow_status_resolver=resolver)
        manager.initialize_project(101, "Test error propagation", "feature")

        plan = manager.get_project_plan(101)

        assert plan is not None
        assert plan["phase_detection_error"] == "Phase detection failed: no state file"


# ---------------------------------------------------------------------------
# C6 RED — project_manager get_project_plan graceful degradation (issue #298)
# ---------------------------------------------------------------------------


class TestGetProjectPlanGracefulDegradation:
    """C6 (issue #298): get_project_plan() skips phase-enrichment on resolver errors."""

    def _make_manager_with_resolver(
        self, legacy_suite_workspace: Path, resolver_side_effect: Exception
    ) -> ProjectManager:
        """Return a ProjectManager whose resolver raises the given exception."""
        mock_resolver = MagicMock()
        mock_resolver.resolve_current.side_effect = resolver_side_effect

        manager = make_project_manager(legacy_suite_workspace)
        manager._workflow_status_resolver = mock_resolver  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001 — inject test double: no public setter

        # Seed the project plan
        manager.initialize_project(
            issue_number=298,
            issue_title="Graceful degradation test",
            workflow_name="feature",
        )
        return manager

    def test_get_project_plan_returns_plan_without_phase_fields_when_state_absent(
        self, legacy_suite_workspace: Path
    ) -> None:
        """StateNotFoundError from resolver must not propagate; plan returned without phase keys."""
        manager = self._make_manager_with_resolver(
            legacy_suite_workspace,
            resolver_side_effect=StateNotFoundError("feature/298-test"),
        )
        plan = manager.get_project_plan(298)

        assert plan is not None
        assert "current_phase" not in plan
        assert "phase_source" not in plan

    def test_get_project_plan_returns_plan_without_phase_fields_on_mismatch(
        self, legacy_suite_workspace: Path
    ) -> None:
        """StateBranchMismatchError from resolver must not propagate; plan without phase keys."""
        manager = self._make_manager_with_resolver(
            legacy_suite_workspace,
            resolver_side_effect=StateBranchMismatchError("branch mismatch"),
        )
        plan = manager.get_project_plan(298)

        assert plan is not None
        assert plan is not None
        assert "current_phase" not in plan
        assert "parent_branch" not in plan or "parent" not in plan  # type: ignore[operator]


class TestProjectManagerVersioning:
    """Tests for deliverables.json envelope versioning and validation."""

    @pytest.mark.parametrize(
        ("source", "error_type"),
        [
            ('{"schema_version": "0.9.0", "projects": {}}', PlanningVersionMismatchError),
            ("{invalid-json", StateCorruptedError),
        ],
    )
    def test_query_preserves_invalid_planning_and_existing_backup(
        self, legacy_suite_workspace: Path, source: str, error_type: type[Exception]
    ) -> None:
        """Reading invalid planning must retain both source and prior recovery bytes."""
        manager = make_project_manager(legacy_suite_workspace)
        deliverables_file = manager.deliverables_file
        deliverables_file.parent.mkdir(parents=True, exist_ok=True)
        deliverables_file.write_text(source, encoding="utf-8")
        backup_file = deliverables_file.with_suffix(".json.bak")
        backup_file.write_bytes(b"prior recovery point")

        with pytest.raises(error_type):
            manager.get_project_plan(42)

        assert deliverables_file.read_bytes() == source.encode("utf-8")
        assert backup_file.read_bytes() == b"prior recovery point"

    @pytest.mark.parametrize("command", ["initialize", "save", "update"])
    @pytest.mark.parametrize(
        ("source", "error_type"),
        [
            ('{"schema_version": "0.9.0", "projects": {}}', PlanningVersionMismatchError),
            ("{invalid-json", StateCorruptedError),
        ],
    )
    def test_commands_preserve_invalid_planning_backup_behavior(
        self, legacy_suite_workspace: Path, command: str, source: str, error_type: type[Exception]
    ) -> None:
        """All existing write entry points still back up an invalid envelope."""
        manager = make_project_manager(legacy_suite_workspace)
        deliverables_file = manager.deliverables_file
        deliverables_file.parent.mkdir(parents=True, exist_ok=True)
        deliverables_file.write_text(source, encoding="utf-8")
        backup_file = deliverables_file.with_suffix(".json.bak")
        backup_file.write_bytes(b"prior recovery point")

        with pytest.raises(error_type):
            if command == "initialize":
                manager.initialize_project(42, "Readback recovery", "feature")
            elif command == "save":
                manager.save_planning_deliverables(
                    42, SavePlanningModel(phases={"validation": phase_block("Report")})
                )
            else:
                manager.update_planning_deliverables(
                    42,
                    [SetPhase(op="set_phase", phase="validation", block=phase_block("Report"))],
                    context=NoteContext(),
                )

        assert not deliverables_file.exists()
        assert backup_file.read_bytes() == source.encode("utf-8")

    def test_project_manager_write_deliverables_saves_envelope(
        self, legacy_suite_workspace: Path
    ) -> None:
        """Verify that ProjectManager saves deliverables nested in a version envelope."""
        manager = make_project_manager(legacy_suite_workspace)

        manager.initialize_project(
            issue_number=42,
            issue_title="Versioning test",
            workflow_name="feature",
        )

        deliverables_file = legacy_suite_workspace / get_default_server_root() / "deliverables.json"
        assert deliverables_file.exists()

        content = deliverables_file.read_text(encoding="utf-8")
        data = json.loads(content)

        assert data.get("schema_version") == "1.0.0"
        assert "projects" in data
        assert "42" in data["projects"]
