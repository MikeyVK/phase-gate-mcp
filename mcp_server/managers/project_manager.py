# mcp_server/managers/project_manager.py
"""
Project manager - ContractsConfig-driven project initialization.

Manages project initialization with workflow selection from contracts.yaml.
Replaces hardcoded PHASE_TEMPLATES with dynamic ContractsConfig phase sequences.

@layer: Platform
@dependencies: [contracts_config]
@responsibilities:
    - Initialize projects with workflow selection
    - Validate workflow existence and execution mode
    - Support custom phase overrides with skip_reason
    - Persist project plans to deliverables.json
    - Retrieve stored project plans
"""

from __future__ import annotations

# Standard library
import json
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pydantic import ValidationError

from mcp_server.core.exceptions import (
    PlanningVersionMismatchError,
    StateCorruptedError,
    StateNotFoundError,
)

# Project modules
from mcp_server.core.interfaces.git import CycleEvidence, ICycleEvidenceReader
from mcp_server.core.operation_notes import Note, NoteContext
from mcp_server.managers.git_manager import GitManager
from mcp_server.managers.state_repository import StateBranchMismatchError
from mcp_server.managers.state_version_validator import StateVersionValidator
from mcp_server.schemas import ContractsConfig, WorkphasesConfig
from mcp_server.schemas.deliverables import (
    AppendCycle,
    CycleInput,
    DeliverableInput,
    PhaseBlockInput,
    PlanningMutationError,
    PlanningOperation,
    RemoveCycle,
    RemovePhase,
    ReplaceCycle,
    SavePlanningModel,
    SetPhase,
    StoredCycle,
    StoredCycles,
    StoredDeliverable,
    StoredPhaseBlock,
    StoredPlanningModel,
)
from mcp_server.utils.atomic_json_writer import AtomicJsonWriter

if TYPE_CHECKING:
    from mcp_server.managers.workflow_status_resolver import WorkflowStatusResolver

# Per-phase keys recognised in planning_deliverables (C8/GAP-15)
# _known_phase_keys is removed (obsolete)


@dataclass
class ProjectInitOptions:
    """Optional parameters for project initialization.

    Reduces initialize_project() from 7 to 4 parameters.
    Field order: overrides → customizations → metadata
    """

    # Overrides
    execution_mode: str | None = None

    # Customizations
    custom_phases: tuple[str, ...] | None = None
    skip_reason: str | None = None

    # Branch metadata
    parent_branch: str | None = None


@dataclass
class ProjectPlan:
    """Project phase plan data structure.

    Field order: identifier → core data → optional → metadata

    Note: Has 8 fields which exceeds pylint's default of 7,
    but all fields are necessary for complete project metadata.
    """

    # Identifiers
    issue_number: int
    issue_title: str

    # Core workflow data
    workflow_name: str
    execution_mode: str
    required_phases: tuple[str, ...]

    # Optional fields
    skip_reason: str | None = None
    parent_branch: str | None = None
    created_at: str | None = None


class ProjectManager:
    """Project initialization manager with ContractsConfig support.

    Uses contracts.yaml for workflow phase definitions.
    """

    def __init__(
        self,
        workspace_root: Path | str,
        contracts_config: ContractsConfig,
        git_manager: GitManager | None = None,
        workphases_config: WorkphasesConfig | None = None,
        *,
        cycle_evidence_reader: ICycleEvidenceReader,
        workflow_status_resolver: WorkflowStatusResolver,
        server_root: Path,
        state_version_validator: StateVersionValidator | None = None,
    ) -> None:
        """Initialize ProjectManager."""
        self.workspace_root = Path(workspace_root)
        self._contracts_config = contracts_config
        self._cycle_evidence_reader = cycle_evidence_reader
        self._git_manager = git_manager
        self._workphases_config = workphases_config
        self._workflow_status_resolver = workflow_status_resolver
        self.deliverables_file = server_root / "deliverables.json"
        self.atomic_json_writer = AtomicJsonWriter()
        self._state_version_validator = state_version_validator or StateVersionValidator()

    @property
    def workphases_config(self) -> WorkphasesConfig | None:
        """Return the workphases configuration."""
        return self._workphases_config

    def initialize_project(
        self,
        issue_number: int,
        issue_title: str,
        workflow_name: str,
        options: ProjectInitOptions | None = None,
    ) -> dict[str, Any]:
        """Initialize project with workflow selection.

        Args:
            issue_number: GitHub issue number
            issue_title: Issue title
            workflow_name: Workflow from contracts.yaml (feature, bug, hotfix, etc.)
            options: Optional parameters (execution_mode, custom_phases, skip_reason,
                    parent_branch)

        Returns:
            dict with success, workflow_name, execution_mode, required_phases,
            skip_reason, parent_branch

        Raises:
            ValueError: If workflow invalid or custom_phases without skip_reason
        """
        opts = options or ProjectInitOptions()

        # Extract parent_branch from options
        parent_branch = opts.parent_branch

        # Validate workflow exists
        if workflow_name not in self._contracts_config.workflows:
            available = list(self._contracts_config.workflows.keys())
            msg = f"Unknown workflow: '{workflow_name}'. Available: {available}"
            raise ValueError(msg)

        # Determine execution mode (default: interactive; no longer from workflow config)
        exec_mode = opts.execution_mode or "interactive"

        # Validate execution mode
        if exec_mode not in ("interactive", "autonomous"):
            msg = (
                f"Invalid execution_mode: '{exec_mode}'. Valid values: 'interactive', 'autonomous'"
            )
            raise ValueError(msg)

        # Determine phases (custom override or contracts default)
        if opts.custom_phases:
            if not opts.skip_reason:
                msg = "skip_reason required when custom_phases provided"
                raise ValueError(msg)
            required_phases = opts.custom_phases
        else:
            required_phases = tuple(self._contracts_config.get_phases(workflow_name))

        # Create project plan
        plan = ProjectPlan(
            issue_number=issue_number,
            issue_title=issue_title,
            workflow_name=workflow_name,
            execution_mode=exec_mode,
            required_phases=required_phases,
            skip_reason=opts.skip_reason,
            parent_branch=parent_branch,
            created_at=datetime.now(UTC).isoformat(),
        )

        # Save to deliverables.json
        self._save_project_plan(plan)

        # Return result
        return {
            "success": True,
            "workflow_name": plan.workflow_name,
            "execution_mode": plan.execution_mode,
            "required_phases": plan.required_phases,
            "skip_reason": plan.skip_reason,
            "parent_branch": plan.parent_branch,
        }

    def get_first_phase(self, workflow_name: str) -> str:
        """Return the first phase name for the given workflow."""
        return self._contracts_config.get_first_phase(workflow_name)

    def get_phases(self, workflow_name: str) -> list[str]:
        """Return all phase names for the given workflow in order."""
        return self._contracts_config.get_phases(workflow_name)

    def save_planning_deliverables(
        self, issue_number: int, planning_deliverables: SavePlanningModel
    ) -> None:
        """Validate and persist one complete initial plan, once."""
        projects, project, snapshot = self._planning_project(issue_number)
        if "planning_deliverables" in project:
            raise PlanningMutationError("planning_already_saved")
        try:
            authoring = SavePlanningModel.model_validate(planning_deliverables)
            cycles = authoring.cycles.cycles if authoring.cycles is not None else []
            candidate = self._number_plan(cycles, authoring.phases)
        except ValidationError as exc:
            raise PlanningMutationError("planning_input_invalid") from exc
        self._validate_planning(project, candidate)
        self._persist_planning(projects, project, candidate, snapshot)

    def update_planning_deliverables(
        self,
        issue_number: int,
        operations: Sequence[PlanningOperation],
        *,
        context: NoteContext,
        force: bool = False,
    ) -> None:
        """Resolve complete operations against one snapshot and protect execution identities."""
        projects, project, snapshot = self._planning_project(issue_number)
        if "planning_deliverables" not in project:
            raise PlanningMutationError("planning_missing")
        current = self._stored_plan(project)
        if not operations or type(force) is not bool:
            raise PlanningMutationError("planning_input_invalid")
        candidate, survivor_positions = self._compose_plan(current, operations)
        execution_phase = self._validate_planning(project, candidate)
        evidence = self._cycle_evidence_reader.read_cycle_evidence(issue_number, execution_phase)
        try:
            if evidence.reason_code in {"branch_issue_mismatch", "git_snapshot_changed"}:
                raise PlanningMutationError("planning_identity_conflict")
            replacement_targets = {
                operation.cycle_id
                for operation in operations
                if isinstance(operation, ReplaceCycle)
            }
            for protected in evidence.protected_cycle_numbers:
                if (
                    survivor_positions.get(protected) != protected
                    or f"C_{protected}" in replacement_targets
                ):
                    raise PlanningMutationError("planning_cycle_protected")
            if evidence.status == "unavailable" and not force:
                raise PlanningMutationError("planning_evidence_unavailable")
            self._persist_planning(projects, project, candidate, snapshot)
        except PlanningMutationError:
            context.produce(self._evidence_note(evidence, overridden=False))
            raise
        context.produce(
            self._evidence_note(evidence, overridden=force and evidence.status == "unavailable")
        )

    def _planning_project(self, issue_number: int) -> tuple[dict[str, Any], dict[str, Any], bytes]:
        if not self.deliverables_file.exists():
            raise PlanningMutationError("planning_project_missing")
        snapshot = self.deliverables_file.read_bytes()
        try:
            projects = self._read_projects()
        except (PlanningVersionMismatchError, StateCorruptedError):
            self._state_version_validator.backup_file(self.deliverables_file)
            raise
        if self.deliverables_file.read_bytes() != snapshot:
            raise PlanningMutationError("planning_snapshot_conflict")
        project = projects.get(str(issue_number))
        if project is None:
            raise PlanningMutationError("planning_project_missing")
        if not isinstance(project, dict):
            raise PlanningMutationError("planning_stored_invalid")
        return projects, project, snapshot

    def _stored_plan(self, project: dict[str, Any]) -> StoredPlanningModel:
        try:
            model = StoredPlanningModel.model_validate(project["planning_deliverables"])
        except (KeyError, ValidationError) as exc:
            raise PlanningMutationError("planning_stored_invalid") from exc
        self._validate_planning(project, model)
        return model

    def _validate_planning(self, project: dict[str, Any], model: StoredPlanningModel) -> str | None:
        workflow_name = project.get("workflow_name")
        if not isinstance(workflow_name, str):
            raise PlanningMutationError("planning_workflow_invalid")
        workflow = self._contracts_config.workflows.get(workflow_name)
        if workflow is None:
            raise PlanningMutationError("planning_workflow_invalid")
        execution_phases = [phase.name for phase in workflow.phases if phase.cycle_based]
        if len(execution_phases) > 1:
            raise PlanningMutationError("planning_workflow_invalid")
        execution_phase = execution_phases[0] if execution_phases else None
        phases = project.get("required_phases")
        if not isinstance(phases, list) or any(not isinstance(phase, str) for phase in phases):
            raise PlanningMutationError("planning_stored_invalid")
        if any(phase not in phases or phase == execution_phase for phase in model.phases):
            raise PlanningMutationError("planning_phase_invalid")
        if execution_phase is not None and model.cycles is None:
            raise PlanningMutationError("planning_cycles_required")
        if execution_phase is None and model.cycles is not None:
            raise PlanningMutationError("planning_cycles_forbidden")
        return execution_phase

    @staticmethod
    def _number_plan(
        cycles: Sequence[CycleInput], phases: dict[str, PhaseBlockInput]
    ) -> StoredPlanningModel:
        numbered = [
            StoredCycle(
                cycle_id=f"C_{number}",
                cycle_number=number,
                cycle_name=cycle.cycle_name,
                deliverables=ProjectManager._number_deliverables(
                    cycle.deliverables, f"D_{number}."
                ),
                exit_criteria=cycle.exit_criteria,
            )
            for number, cycle in enumerate(cycles, 1)
        ]
        return StoredPlanningModel(
            cycles=StoredCycles(total=len(numbered), cycles=numbered) if numbered else None,
            phases={
                phase: StoredPhaseBlock(
                    deliverables=ProjectManager._number_deliverables(block.deliverables, "D_")
                )
                for phase, block in phases.items()
            },
        )

    @staticmethod
    def _number_deliverables(
        deliverables: Sequence[DeliverableInput], prefix: str
    ) -> list[StoredDeliverable]:
        return [
            StoredDeliverable(
                deliverable_id=f"{prefix}{index}",
                deliverable_name=deliverable.deliverable_name,
                description=deliverable.description,
                validates=deliverable.validates,
            )
            for index, deliverable in enumerate(deliverables, 1)
        ]

    @staticmethod
    def _author_cycle(cycle: StoredCycle) -> CycleInput:
        return CycleInput(
            cycle_name=cycle.cycle_name,
            deliverables=[
                DeliverableInput(
                    deliverable_name=deliverable.deliverable_name,
                    description=deliverable.description,
                    validates=deliverable.validates,
                )
                for deliverable in cycle.deliverables
            ],
            exit_criteria=cycle.exit_criteria,
        )

    @staticmethod
    def _compose_plan(
        current: StoredPlanningModel, operations: Sequence[PlanningOperation]
    ) -> tuple[StoredPlanningModel, dict[int, int]]:
        original = current.cycles.cycles if current.cycles is not None else []
        cycle_ids = {cycle.cycle_id for cycle in original}
        replacements: dict[str, CycleInput] = {}
        removals: set[str] = set()
        appends: list[CycleInput] = []
        targets: set[tuple[str, str]] = set()
        phases = {
            phase: PhaseBlockInput(
                deliverables=[
                    DeliverableInput(
                        deliverable_name=deliverable.deliverable_name,
                        description=deliverable.description,
                        validates=deliverable.validates,
                    )
                    for deliverable in block.deliverables
                ]
            )
            for phase, block in current.phases.items()
        }
        for operation in operations:
            if isinstance(operation, AppendCycle):
                appends.append(operation.cycle)
                continue
            if isinstance(operation, (ReplaceCycle, RemoveCycle)):
                target = ("cycle", operation.cycle_id)
                if operation.cycle_id not in cycle_ids:
                    raise PlanningMutationError("planning_target_missing")
                if target in targets:
                    raise PlanningMutationError("planning_duplicate_target")
                targets.add(target)
                if isinstance(operation, ReplaceCycle):
                    replacements[operation.cycle_id] = operation.cycle
                else:
                    removals.add(operation.cycle_id)
            elif isinstance(operation, (SetPhase, RemovePhase)):
                target = ("phase", operation.phase)
                if target in targets:
                    raise PlanningMutationError("planning_duplicate_target")
                targets.add(target)
                if isinstance(operation, SetPhase):
                    phases[operation.phase] = operation.block
                elif operation.phase not in current.phases:
                    raise PlanningMutationError("planning_target_missing")
                else:
                    del phases[operation.phase]
            else:
                raise PlanningMutationError("planning_input_invalid")
        survivors = [cycle for cycle in original if cycle.cycle_id not in removals]
        survivor_positions = {
            cycle.cycle_number: position for position, cycle in enumerate(survivors, 1)
        }
        cycles = [
            replacements.get(cycle.cycle_id) or ProjectManager._author_cycle(cycle)
            for cycle in survivors
        ]
        cycles.extend(appends)
        try:
            candidate = ProjectManager._number_plan(cycles, phases)
        except ValidationError as exc:
            raise PlanningMutationError("planning_result_empty") from exc
        return candidate, survivor_positions

    def _persist_planning(
        self,
        projects: dict[str, Any],
        project: dict[str, Any],
        candidate: StoredPlanningModel,
        snapshot: bytes,
    ) -> None:
        if self.deliverables_file.read_bytes() != snapshot:
            raise PlanningMutationError("planning_snapshot_conflict")
        project["planning_deliverables"] = candidate.model_dump(exclude_none=True)
        self._write_deliverables(projects)

    @staticmethod
    def _evidence_note(evidence: CycleEvidence, *, overridden: bool) -> Note:
        return Note(
            key="planning_cycle_evidence",
            params={
                "status": evidence.status,
                "branch": evidence.branch,
                "head_sha": evidence.head_sha,
                "execution_phase": evidence.execution_phase,
                "protected_cycle_numbers": list(evidence.protected_cycle_numbers),
                "reason_code": evidence.reason_code,
                "diagnostic_commit_sha": evidence.diagnostic_commit_sha,
                "evidence_overridden": overridden,
            },
        )

    def get_project_plan(self, issue_number: int) -> dict[str, Any] | None:
        """Get stored project plan with current phase detection.

        Issue #298: state.json is the authoritative source. WorkflowStatusResolver
        reads current_phase from state.json directly. Returns plan without phase
        fields when state is absent or mismatched (graceful degradation).

        Args:
            issue_number: GitHub issue number

        Returns:
            Project plan dict with phase detection fields, or None if not found
        """
        if not self.deliverables_file.exists():
            return None

        projects = self._read_projects()
        plan: dict[str, Any] | None = projects.get(str(issue_number))

        if plan is None:
            return None

        if "planning_deliverables" in plan:
            self._stored_plan(plan)

        # Use WorkflowStatusResolver to detect current phase (Issue #231 C4)
        try:
            status = self._workflow_status_resolver.resolve_current()
        except (StateNotFoundError, StateBranchMismatchError, OSError):
            return plan
        if status.sub_phase:
            plan["current_phase"] = f"{status.current_phase}:{status.sub_phase}"
        else:
            plan["current_phase"] = status.current_phase
        plan["phase_source"] = status.phase_source
        plan["phase_detection_error"] = status.phase_detection_error
        return plan

    def _read_projects(self) -> dict[str, Any]:
        """Read and validate deliverables envelope (Query).

        Returns:
            Dict of projects nested under "projects" key.
        """
        if not self.deliverables_file.exists():
            return {}

        self._state_version_validator.validate_file(
            self.deliverables_file, expected_version="1.0.0", is_planning=True
        )

        content = self.deliverables_file.read_text(encoding="utf-8-sig")
        data = json.loads(content)
        if not isinstance(data, dict):
            return {}
        projects = data.get("projects")
        if projects is None:
            projects = {k: v for k, v in data.items() if k != "schema_version"}
        if not isinstance(projects, dict):
            return {}
        return projects

    def _write_deliverables(self, projects: dict[str, Any]) -> None:
        """Persist deliverables.json via atomic replacement (Command)."""
        payload = {
            "schema_version": "1.0.0",
            "projects": projects,
        }
        self.atomic_json_writer.write_json(self.deliverables_file, payload)

    def _save_project_plan(self, plan: ProjectPlan) -> None:
        """Save project plan to deliverables.json.

        Args:
            plan: ProjectPlan to save
        """
        # Ensure state directory exists
        self.deliverables_file.parent.mkdir(parents=True, exist_ok=True)

        # Load existing projects
        try:
            projects = self._read_projects()
        except (PlanningVersionMismatchError, StateCorruptedError):
            self._state_version_validator.backup_file(self.deliverables_file)
            raise

        # Store plan (convert tuple to list for JSON)
        projects[str(plan.issue_number)] = {
            "issue_title": plan.issue_title,
            "workflow_name": plan.workflow_name,
            "execution_mode": plan.execution_mode,
            "required_phases": list(plan.required_phases),
            "skip_reason": plan.skip_reason,
            "parent_branch": plan.parent_branch,
            "created_at": plan.created_at,
        }

        # Write to file
        self._write_deliverables(projects)
