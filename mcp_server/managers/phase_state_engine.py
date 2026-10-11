# mcp_server/managers/phase_state_engine.py
"""
Phase state engine - ContractsConfig-driven phase transition management.

Manages branch phase state with strict sequential validation via contracts.yaml.
Supports both standard sequential transitions and forced non-sequential transitions
with audit trail.

@layer: Platform
@dependencies: [contracts_config, project_manager]
@responsibilities:
    - Initialize branch state with workflow caching
    - Validate phase transitions against workflow definitions
    - Execute standard sequential transitions
    - Execute forced non-sequential transitions with skip_reason
    - Maintain transition history with forced flag audit
    - Persist state to state.json
"""

from __future__ import annotations

# Standard library
import json
import logging
import os
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from mcp_server.core.exceptions import StateNotFoundError
from mcp_server.core.interfaces import (
    GateReport,
    IContextLoadedWriter,
    IStateRepository,
    IWorkflowGateRunner,
    IWorkflowStateMutator,
)
from mcp_server.core.interfaces.project_plan import IProjectPlanReader
from mcp_server.managers.state_repository import (
    BranchState,
    StateAlreadyExistsError,
    StateBranchMismatchError,
)
from mcp_server.managers.workflow_state_mutator import WorkflowStateMutator
from mcp_server.schemas import ContractsConfig, GitConfig
from mcp_server.schemas.deliverables import StoredPlanningModel

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TransitionRecord:
    """Phase transition record for audit trail.

    Field order: identifier â†’ data â†’ flags â†’ optional
    """

    # Core transition data
    from_phase: str
    to_phase: str
    timestamp: str

    # Metadata
    human_approval_message: str | None
    forced: bool

    # Optional fields
    skip_reason: str | None = None
    resume_cycle: str | None = None


class PhaseEntryError(ValueError):
    """Structured admission failure before a phase-state mutation."""

    def __init__(self, error_code: str) -> None:
        super().__init__(error_code)
        self.error_code = error_code


class PhaseStateEngine:
    """Phase state and transition manager with workflow validation.

    Validates transitions against contracts.yaml definitions.
    Supports standard sequential and forced non-sequential transitions.
    """

    def __init__(
        self,
        workspace_root: Path | str,
        project_manager: IProjectPlanReader,
        git_config: GitConfig,
        contracts_config: ContractsConfig,
        state_repository: IStateRepository,
        workflow_gate_runner: IWorkflowGateRunner,
        server_root: Path,
        workflow_state_mutator: IWorkflowStateMutator | None = None,
        state_reconstructor: object | None = None,
        context_loaded_writer: IContextLoadedWriter | None = None,
    ) -> None:
        """Initialize PhaseStateEngine."""
        del state_reconstructor  # Retained for the public constructor contract.
        self._workspace_root = Path(workspace_root)
        self.state_path = server_root / "state.json"
        resolved_server_root = server_root or (self._workspace_root / ".pgmcp")
        self.state_path = resolved_server_root / "state.json"
        self.project_manager = project_manager

        self._contracts_config = contracts_config
        self._git_config = git_config
        self._state_repository = state_repository
        self._workflow_gate_runner = workflow_gate_runner
        if workflow_state_mutator is None:
            workflow_state_mutator = WorkflowStateMutator(state_repository=state_repository)
        self._workflow_state_mutator = workflow_state_mutator

        self._context_loaded_writer = context_loaded_writer

    def _reset_context_loaded(self, branch: str) -> None:
        """Reset context-loaded flag after a state-changing transition."""
        if self._context_loaded_writer is not None:
            self._context_loaded_writer.set_context_loaded(branch, value=False)

    def validate_branch_initialization(self, branch: str) -> None:
        """Reject existing same-branch state without project or workflow mutations."""
        # Guard: refuse to overwrite an existing BranchState for this branch
        try:
            loaded = self._state_repository.load(branch)
            if loaded.branch == branch:
                raise StateAlreadyExistsError(
                    f"Branch '{branch}' already has an initialized state "
                    f"(phase: {loaded.current_phase}). "
                    "Call initialize_project only once per branch."
                )
        except (
            FileNotFoundError,
            KeyError,
            OSError,
            json.JSONDecodeError,
            ValidationError,
            StateNotFoundError,
        ):
            pass

    def initialize_branch(
        self, branch: str, issue_number: int, initial_phase: str, parent_branch: str | None = None
    ) -> dict[str, Any]:
        """Initialize branch state with workflow caching.

        Caches workflow_name in state.json for performance optimization.

        Args:
            branch: Branch name (e.g., 'feature/42-test')
            issue_number: GitHub issue number
            initial_phase: Starting phase
            parent_branch: Optional parent branch - if None, inherits from project

        Returns:
            dict with success, branch, current_phase, parent_branch

        Raises:
            ValueError: If project not initialized
        """
        self.validate_branch_initialization(branch)

        project = self.project_manager.get_project_plan(issue_number)
        if not project:
            msg = f"Project {issue_number} not found. Initialize project first."
            raise ValueError(msg)

        # Determine parent_branch: explicit param or inherit from project
        if parent_branch is None:
            parent_branch = project.get("parent_branch")

        warnings: list[str] = []
        if self._has_uncommitted_state_changes():
            warnings.append("state.json has uncommitted local changes")

        self._workflow_state_mutator.apply(
            branch,
            lambda _s: _s.with_updates(
                branch=branch,
                issue_number=issue_number,
                workflow_name=project["workflow_name"],
                current_phase=initial_phase,
                current_cycle=None,
                last_cycle=None,
                cycle_history=[],
                required_phases=project.get("required_phases", []),
                execution_mode=project.get("execution_mode", "normal"),
                issue_title=project.get("issue_title"),
                parent_branch=parent_branch,
                created_at=datetime.now(UTC).isoformat(),
                transitions=[],
                reconstructed=False,
            ),
        )

        return {
            "success": True,
            "branch": branch,
            "current_phase": initial_phase,
            "parent_branch": parent_branch,
            "warnings": warnings,
        }

    def transition(
        self,
        branch: str,
        to_phase: str,
        human_approval_message: str | None = None,
        *,
        resume_cycle: str | None = None,
    ) -> dict[str, Any]:
        """Validate a sequential phase entry before one composed state mutation."""
        state = self.get_state(branch)
        self._validate_transition_entry(state, to_phase, resume_cycle, forced=False)
        resolved_approval = self._resolve_approval(human_approval_message, required=False)
        self._workflow_gate_runner.enforce_phase_exit(
            issue_number=self._require_issue_number(branch, state),
            workflow_name=state.workflow_name,
            phase=state.current_phase,
            cycle_number=state.current_cycle,
        )
        transition = TransitionRecord(
            from_phase=state.current_phase,
            to_phase=to_phase,
            timestamp=datetime.now(UTC).isoformat(),
            human_approval_message=resolved_approval,
            forced=False,
            resume_cycle=resume_cycle,
        )
        self._apply_phase_transition(branch, state, transition)
        return {"success": True, "from_phase": state.current_phase, "to_phase": to_phase}

    def force_transition(
        self,
        branch: str,
        to_phase: str,
        skip_reason: str,
        human_approval_message: str | None = None,
        *,
        resume_cycle: str | None = None,
    ) -> dict[str, Any]:
        """Skip exit gates, while retaining phase, plan and cycle-entry validity."""
        if not skip_reason or not skip_reason.strip():
            raise PhaseEntryError("phase_skip_reason_required")
        resolved_approval = self._resolve_approval(human_approval_message, required=True)
        state = self.get_state(branch)
        self._validate_transition_entry(state, to_phase, resume_cycle, forced=True)
        report = self._workflow_gate_runner.inspect_phase_exit(
            issue_number=self._require_issue_number(branch, state),
            workflow_name=state.workflow_name,
            phase=state.current_phase,
            cycle_number=state.current_cycle,
        )
        skipped_gates = list(report.blocking)
        if skipped_gates:
            logger.warning(
                "force_transition skipped_gates=%s (from=%s, to=%s, skip_reason=%r)",
                skipped_gates,
                state.current_phase,
                to_phase,
                skip_reason,
            )
        transition = TransitionRecord(
            from_phase=state.current_phase,
            to_phase=to_phase,
            timestamp=datetime.now(UTC).isoformat(),
            human_approval_message=resolved_approval,
            forced=True,
            skip_reason=skip_reason,
            resume_cycle=resume_cycle,
        )
        self._apply_phase_transition(branch, state, transition)
        return {
            "success": True,
            "from_phase": state.current_phase,
            "to_phase": to_phase,
            "forced": True,
            "skip_reason": skip_reason,
            "skipped_gates": skipped_gates,
            "passing_gates": list(report.passing),
            "gate_report": self._gate_report_to_payload(report),
        }

    def _validate_transition_entry(
        self, state: BranchState, to_phase: str, resume_cycle: str | None, *, forced: bool
    ) -> int | None:
        self._require_issue_number(state.branch, state)
        workflow = self._contracts_config.workflows.get(state.workflow_name)
        if workflow is None:
            raise PhaseEntryError("phase_workflow_invalid")
        workflow.get_phase(state.current_phase)
        try:
            target = workflow.get_phase(to_phase)
        except ValueError as exc:
            raise PhaseEntryError("phase_target_invalid") from exc
        if not forced:
            self._contracts_config.validate_transition(
                state.workflow_name, state.current_phase, to_phase
            )
        if not target.cycle_based:
            if resume_cycle is not None:
                raise PhaseEntryError("cycle_resume_not_allowed")
            return None
        issue_number = self._require_issue_number(state.branch, state)
        planning = self._get_planning(issue_number)
        if planning.cycles is None:
            raise PhaseEntryError("planning_cycles_required")
        prior_work = state.current_cycle is not None or bool(state.cycle_history)
        if prior_work and resume_cycle is None:
            raise PhaseEntryError("cycle_resume_required")
        selected_ref = resume_cycle if resume_cycle is not None else "C_1"
        selected = next(
            (cycle for cycle in planning.cycles.cycles if cycle.cycle_id == selected_ref), None
        )
        if selected is None or (not prior_work and selected.cycle_number != 1):
            raise PhaseEntryError("cycle_resume_invalid")
        return selected.cycle_number

    def _apply_phase_transition(
        self, branch: str, initial: BranchState, transition: TransitionRecord
    ) -> None:
        def compose(fresh: BranchState) -> BranchState:
            if (
                fresh.branch != branch
                or fresh.issue_number != initial.issue_number
                or fresh.workflow_name != initial.workflow_name
                or fresh.current_phase != initial.current_phase
                or fresh.current_cycle != initial.current_cycle
            ):
                raise PhaseEntryError("phase_transition_state_changed")
            selected_cycle = self._validate_transition_entry(
                fresh, transition.to_phase, transition.resume_cycle, forced=transition.forced
            )
            last_cycle = fresh.last_cycle
            if (
                self._contracts_config.workflows[fresh.workflow_name]
                .get_phase(fresh.current_phase)
                .cycle_based
                and fresh.current_cycle is not None
            ):
                last_cycle = fresh.current_cycle
            current_cycle = fresh.current_cycle
            if selected_cycle is not None:
                current_cycle = selected_cycle
                last_cycle = None
            updates: dict[str, Any] = {
                "current_phase": transition.to_phase,
                "current_cycle": current_cycle,
                "last_cycle": last_cycle,
                "current_sub_phase": None,
                "transitions": [*fresh.transitions, self._transition_to_dict(transition)],
            }
            if transition.forced:
                updates["skip_reason"] = transition.skip_reason
            return fresh.with_updates(**updates)

        self._workflow_state_mutator.apply(branch, compose)
        self._reset_context_loaded(branch)

    def transition_cycle(
        self,
        branch: str,
        to_cycle: int,
        gate_runner: IWorkflowGateRunner | None = None,
    ) -> dict[str, Any]:
        """Execute one strict sequential cycle transition inside the active cycle-based phase."""
        state = self.get_state(branch)
        issue_number = self._require_issue_number(branch, state)
        cycles, total_cycles = self._get_cycles(issue_number)
        runner = gate_runner or self._workflow_gate_runner
        self._validate_cycle_phase(
            workflow_name=state.workflow_name,
            current_phase=state.current_phase,
            gate_runner=runner,
        )
        self._validate_cycle_number_range(to_cycle, issue_number)
        self._validate_strict_cycle_progression(state.current_cycle, to_cycle)
        self._validate_current_cycle_exit_criteria(state.current_cycle, cycles)

        if state.current_cycle is not None:
            runner.enforce_cycle_exit(
                issue_number=issue_number,
                workflow_name=state.workflow_name,
                phase=state.current_phase,
                cycle_number=state.current_cycle,
            )

        from_cycle = state.current_cycle or 0
        cycle_name = self._get_cycle_name(cycles, to_cycle)
        history_entry = {
            "cycle_number": to_cycle,
            "name": cycle_name,
            "forced": False,
            "entered": datetime.now(UTC).isoformat(),
        }
        self._workflow_state_mutator.apply(
            branch,
            lambda _s: _s.with_updates(
                last_cycle=from_cycle,
                current_cycle=to_cycle,
                cycle_history=[*_s.cycle_history, history_entry],
                current_sub_phase=None,
            ),
        )
        self._reset_context_loaded(branch)

        return {
            "success": True,
            "from_cycle": from_cycle,
            "to_cycle": to_cycle,
            "total_cycles": total_cycles,
            "cycle_name": cycle_name,
        }

    def force_cycle_transition(
        self,
        branch: str,
        to_cycle: int,
        skip_reason: str,
        human_approval_message: str | None = None,
        gate_runner: IWorkflowGateRunner | None = None,
    ) -> dict[str, Any]:
        """Execute one forced cycle transition inside the active cycle-based phase."""
        if not skip_reason or not skip_reason.strip():
            raise ValueError(
                "skip_reason is required for forced transitions. "
                "Provide justification for backward/skip transition."
            )

        resolved_approval = self._resolve_approval(human_approval_message, required=True)
        state = self.get_state(branch)
        issue_number = self._require_issue_number(branch, state)
        cycles, total_cycles = self._get_cycles(issue_number)
        runner = gate_runner or self._workflow_gate_runner
        self._validate_cycle_phase(
            workflow_name=state.workflow_name,
            current_phase=state.current_phase,
            gate_runner=runner,
        )
        self._validate_cycle_number_range(to_cycle, issue_number)

        report: GateReport
        if state.current_cycle is not None:
            report = runner.inspect_cycle_exit(
                issue_number=issue_number,
                workflow_name=state.workflow_name,
                phase=state.current_phase,
                cycle_number=state.current_cycle,
            )
        else:
            report = GateReport()

        from_cycle = state.current_cycle or 0
        cycle_name = self._get_cycle_name(cycles, to_cycle)
        skipped_cycles = list(range(min(from_cycle, to_cycle) + 1, max(from_cycle, to_cycle)))
        history_entry = {
            "cycle_number": to_cycle,
            "name": cycle_name,
            "entered": datetime.now(UTC).isoformat(),
            "forced": True,
            "skip_reason": skip_reason,
            "human_approval_message": resolved_approval,
            "skipped_cycles": skipped_cycles,
        }
        self._workflow_state_mutator.apply(
            branch,
            lambda _s: _s.with_updates(
                last_cycle=from_cycle,
                current_cycle=to_cycle,
                cycle_history=[*_s.cycle_history, history_entry],
                current_sub_phase=None,
            ),
        )
        self._reset_context_loaded(branch)

        return {
            "success": True,
            "from_cycle": from_cycle,
            "to_cycle": to_cycle,
            "total_cycles": total_cycles,
            "cycle_name": cycle_name,
            "forced": True,
            "skip_reason": skip_reason,
            "skipped_gates": list(report.blocking),
            "passing_gates": list(report.passing),
            "gate_report": self._gate_report_to_payload(report),
        }

    def get_current_phase(self, branch: str) -> str:
        """Get current phase for branch."""
        return self.get_state(branch).current_phase

    def _gate_report_to_payload(self, report: GateReport) -> dict[str, Any]:
        """Serialize one gate report into plain Python collections."""
        return {
            "passing": list(report.passing),
            "blocking": list(report.blocking),
            "details": dict(report.details),
        }

    def _has_uncommitted_state_changes(self) -> bool:
        """Check whether tracked state.json has local git changes."""
        if not self.state_path.exists():
            return False

        try:
            env = os.environ.copy()
            env.setdefault("GIT_TERMINAL_PROMPT", "0")
            env.setdefault("GIT_PAGER", "cat")
            env.setdefault("PAGER", "cat")

            result = subprocess.run(
                [
                    "git",
                    "status",
                    "--porcelain",
                    "--",
                    str(self.state_path.relative_to(self._workspace_root_path())),
                ],
                cwd=self._workspace_root_path(),
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                check=True,
                timeout=2,
                env=env,
            )
            return bool(result.stdout.strip())
        except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            logger.warning(
                "Unable to check state.json git status during initialize_branch: %s",
                exc,
            )
            return False

    def get_state(self, branch: str) -> BranchState:
        """Get persisted state for one branch without reconstruction side effects."""
        loaded_state = self._state_repository.load(branch)
        if loaded_state.branch != branch:
            msg = f"Branch state for '{branch}' not found"
            raise StateBranchMismatchError(msg)
        return loaded_state

    def _require_issue_number(self, branch: str, state: BranchState) -> int:
        """Return the persisted issue number or raise a descriptive error."""
        issue_number = state.issue_number
        if issue_number is None:
            raise ValueError(f"Branch '{branch}' has no issue_number in state")
        return issue_number

    def _get_planning(self, issue_number: int) -> StoredPlanningModel:
        plan = self.project_manager.get_project_plan(issue_number)
        if plan is None or "planning_deliverables" not in plan:
            raise PhaseEntryError("planning_deliverables_missing")
        try:
            return StoredPlanningModel.model_validate(plan["planning_deliverables"])
        except ValidationError as exc:
            raise PhaseEntryError("planning_deliverables_invalid") from exc

    def _get_cycles(self, issue_number: int) -> tuple[list[dict[str, Any]], int]:
        """Return validated current cycles and their stored derived total."""
        planning = self._get_planning(issue_number)
        if planning.cycles is None:
            raise PhaseEntryError("planning_cycles_required")
        return [
            cycle.model_dump(exclude_none=True) for cycle in planning.cycles.cycles
        ], planning.cycles.total

    def _is_cycle_based_phase(
        self,
        workflow_name: str,
        phase: str,
        gate_runner: IWorkflowGateRunner | None = None,
    ) -> bool:
        """Return whether one workflow phase is configured for cycle transitions."""
        runner = gate_runner or self._workflow_gate_runner
        return runner.is_cycle_based_phase(workflow_name, phase)

    def _validate_cycle_phase(
        self,
        workflow_name: str,
        current_phase: str,
        gate_runner: IWorkflowGateRunner | None = None,
    ) -> None:
        """Ensure cycle transitions only run inside phases marked cycle_based."""
        if not self._is_cycle_based_phase(workflow_name, current_phase, gate_runner):
            raise ValueError(
                "Cycle transitions only allowed during cycle-based phases "
                f"(current: {current_phase})."
            )

    def _validate_strict_cycle_progression(
        self,
        current_cycle: int | None,
        to_cycle: int,
    ) -> None:
        """Validate forward-only, sequential strict cycle movement."""
        if current_cycle is not None and to_cycle <= current_cycle:
            raise ValueError(
                f"Backwards transition not allowed (current: {current_cycle}, "
                f"target: {to_cycle}). Use force_cycle_transition for backwards transitions."
            )
        if current_cycle is not None and to_cycle != current_cycle + 1:
            raise ValueError(
                f"Non-sequential transition not allowed (current: {current_cycle}, "
                f"target: {to_cycle}). Use force_cycle_transition to skip cycles."
            )

    def _validate_current_cycle_exit_criteria(
        self,
        current_cycle: int | None,
        cycles: list[dict[str, Any]],
    ) -> None:
        """Ensure the current cycle defines exit criteria before a strict move."""
        if current_cycle is None:
            return

        current_cycle_data = next(
            (
                cycle
                for cycle in cycles
                if isinstance(cycle, dict) and cycle.get("cycle_number") == current_cycle
            ),
            None,
        )
        if current_cycle_data is None:
            return

        exit_criteria = current_cycle_data.get("exit_criteria", "")
        if not isinstance(exit_criteria, str) or not exit_criteria.strip():
            raise ValueError(
                f"Cycle {current_cycle} exit criteria not defined. "
                "Define exit_criteria in planning deliverables before transitioning."
            )

    def _get_cycle_name(self, cycles: list[dict[str, Any]], to_cycle: int) -> str:
        """Resolve the display name for one target cycle."""
        cycle_details = next(
            (
                cycle
                for cycle in cycles
                if isinstance(cycle, dict) and cycle.get("cycle_number") == to_cycle
            ),
            None,
        )
        if cycle_details is None:
            return "Unknown"
        name = cycle_details.get("cycle_name")
        return name if isinstance(name, str) and name else "Unknown"

    def _validate_cycle_number_range(self, cycle_number: int, issue_number: int) -> None:
        """Validate cycle_number is within valid range [1..total].

        Args:
            cycle_number: Cycle number to validate
            issue_number: GitHub issue number for context

        Raises:
            ValueError: If cycle_number is out of range or planning deliverables not found

        Issue #146 Cycle 2: Range validation for TDD cycle transitions.
        """
        _cycles, total_cycles = self._get_cycles(issue_number)

        if cycle_number < 1 or cycle_number > total_cycles:
            msg = f"cycle_number must be in range [1..{total_cycles}], got {cycle_number}"
            raise ValueError(msg)

    def record_sub_phase(self, branch: str, sub_phase: str | None) -> None:
        """Persist the current TDD sub_phase (red/green/refactor/None) to state.

        Registered by GitCommitTool before a commit and rolled back if it fails.
        Even None is written explicitly to clear a previously stored value.
        """
        self._workflow_state_mutator.apply(
            branch, lambda s: s.with_updates(current_sub_phase=sub_phase)
        )

    def _transition_to_dict(self, transition: TransitionRecord) -> dict[str, Any]:
        """Convert TransitionRecord to dict for JSON serialization.

        Args:
            transition: TransitionRecord instance

        Returns:
            dict representation
        """
        payload = {
            "from_phase": transition.from_phase,
            "to_phase": transition.to_phase,
            "timestamp": transition.timestamp,
            "human_approval_message": transition.human_approval_message,
            "forced": transition.forced,
            "skip_reason": transition.skip_reason,
        }
        if transition.resume_cycle is not None:
            payload["resume_cycle"] = transition.resume_cycle
        return payload

    def _workspace_root_path(self) -> Path:
        """Return the workspace root derived from the tracked state file location."""
        return self._workspace_root

    def _resolve_approval(
        self,
        human_approval_message: str | None,
        required: bool = False,
    ) -> str | None:
        """Resolve human_approval_message parameter."""
        actual_approval = human_approval_message
        if required and (not actual_approval or not actual_approval.strip()):
            raise ValueError(
                "human_approval_message is required for forced transitions. "
                "Provide approval (e.g., 'John approved on 2026-02-17')."
            )
        return actual_approval
