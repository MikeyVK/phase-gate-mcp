# tests/mcp_server/unit/managers/test_phase_state_engine_c4_issue257.py
"""Tests for C_CYCLE_ORCHESTRATION behavior (Issue #257 Cycle 4).

@layer: Tests (Unit)
@dependencies: [pytest, tests.mcp_server.test_support, mcp_server.managers.phase_state_engine]
"""

from __future__ import annotations

from pathlib import Path

import pytest

from mcp_server.core.interfaces import GateReport, GateViolation
from mcp_server.managers.phase_contract_resolver import PhaseContractResolver
from mcp_server.managers.project_manager import ProjectManager
from mcp_server.managers.state_repository import InMemoryStateRepository
from mcp_server.schemas.deliverables import SavePlanningModel
from tests.mcp_server.test_support import (
    get_default_server_root,
    make_phase_contract_resolver,
    make_phase_state_engine,
    make_project_manager,
)


class BlockingCycleGateRunner:
    """Gate runner fake that blocks normal cycle transitions."""

    def __init__(self) -> None:
        self.enforce_calls: list[tuple[str, str, int | None, int]] = []

    def is_cycle_based_phase(self, workflow_name: str, phase: str) -> bool:
        del workflow_name
        return phase == "implementation"

    def enforce_cycle_exit(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int,
        *,
        issue_number: int,
    ) -> GateReport:
        self.enforce_calls.append((workflow_name, phase, cycle_number, issue_number))
        report = GateReport(
            passing=(),
            blocking=("cycle-docs",),
            details={"cycle-docs": "missing cycle transition evidence"},
        )
        raise GateViolation("missing cycle transition evidence", report)

    def inspect_cycle_exit(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int,
        *,
        issue_number: int,
    ) -> GateReport:
        del workflow_name, phase, cycle_number, issue_number
        return GateReport()


class ReportingCycleGateRunner:
    """Gate runner fake that reports force-transition inspection results."""

    def __init__(self) -> None:
        self.inspect_calls: list[tuple[str, str, int | None, int]] = []

    def is_cycle_based_phase(self, workflow_name: str, phase: str) -> bool:
        del workflow_name
        return phase == "implementation"

    def enforce_cycle_exit(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int,
        *,
        issue_number: int,
    ) -> GateReport:
        del workflow_name, phase, cycle_number, issue_number
        return GateReport()

    def inspect_cycle_exit(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int,
        *,
        issue_number: int,
    ) -> GateReport:
        self.inspect_calls.append((workflow_name, phase, cycle_number, issue_number))
        return GateReport(
            passing=("cycle-docs",),
            blocking=("cycle-checklist",),
            details={"cycle-checklist": "missing force-transition checklist"},
        )


class ConfigAwareCycleGateRunner:
    """Gate runner fake that delegates cycle-based phase lookup to config."""

    def __init__(self, resolver: PhaseContractResolver) -> None:
        self._resolver = resolver
        self.enforce_calls: list[tuple[str, str, int | None, int]] = []
        self.inspect_calls: list[tuple[str, str, int | None, int]] = []

    def enforce_cycle_exit(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int,
        *,
        issue_number: int,
    ) -> GateReport:
        self.enforce_calls.append((workflow_name, phase, cycle_number, issue_number))
        return GateReport()

    def inspect_cycle_exit(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int,
        *,
        issue_number: int,
    ) -> GateReport:
        self.inspect_calls.append((workflow_name, phase, cycle_number, issue_number))
        return GateReport()

    def is_cycle_based_phase(self, workflow_name: str, phase: str) -> bool:
        return self._resolver.is_cycle_based_phase(workflow_name, phase)


@pytest.fixture
def workspace_root(tmp_path: Path) -> Path:
    """Temporary workspace root for cycle-orchestration tests."""
    return tmp_path


@pytest.fixture
def project_manager(workspace_root: Path) -> ProjectManager:
    """ProjectManager bound to the temp workspace."""
    return make_project_manager(workspace_root)


def _create_cycle_engine(
    workspace_root: Path,
    project_manager: ProjectManager,
    gate_runner: object,
) -> tuple[object, str]:
    """Create one implementation-phase branch ready for cycle transitions."""
    issue_number = 257
    branch = "feature/257-cycle-orchestration"
    repository = InMemoryStateRepository()

    project_manager.initialize_project(
        issue_number=issue_number,
        issue_title="Cycle orchestration",
        workflow_name="feature",
    )
    project_manager.save_planning_deliverables(
        issue_number,
        SavePlanningModel.model_validate(
            {
                "cycles": {
                    "cycles": [
                        {
                            "cycle_name": "Gate API",
                            "deliverables": [{"deliverable_name": "D1", "description": "c1"}],
                            "exit_criteria": "gate runner ready",
                        },
                        {
                            "cycle_name": "Gate wiring",
                            "deliverables": [{"deliverable_name": "D2", "description": "c2"}],
                            "exit_criteria": "phase transitions delegated",
                        },
                        {
                            "cycle_name": "State recovery",
                            "deliverables": [{"deliverable_name": "D3", "description": "c3"}],
                            "exit_criteria": "get_state is pure",
                        },
                        {
                            "cycle_name": "Cycle orchestration",
                            "deliverables": [{"deliverable_name": "D4", "description": "c4"}],
                            "exit_criteria": "cycle tools are thin",
                        },
                    ],
                }
            }
        ),
    )
    engine = make_phase_state_engine(
        workspace_root,
        project_manager=project_manager,
        state_repository=repository,
        workflow_gate_runner=gate_runner,
    )
    engine.initialize_branch(
        branch=branch,
        issue_number=issue_number,
        initial_phase="implementation",
    )
    repository.save(engine.get_state(branch).with_updates(current_cycle=1, last_cycle=None))
    return engine, branch


def _write_cycle_based_tdd_configs(workspace_root: Path) -> None:
    """Write a minimal workflow where implementation is cycle-based (config-driven)."""
    config_dir = workspace_root / get_default_server_root() / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "workflows.yaml").write_text(
        (
            "version: '1.0.0'\n"
            "workflows:\n"
            "  feature:\n"
            "    name: feature\n"
            "    phases: [planning, implementation, documentation]\n"
        ),
        encoding="utf-8",
    )
    (config_dir / "workphases.yaml").write_text(
        (
            "version: '1.0.0'\n"
            "phases:\n"
            "  planning:\n"
            "    display_name: Planning\n"
            "  implementation:\n"
            "    display_name: Implementation\n"
            "    subphases: [red, green, refactor]\n"
            "  documentation:\n"
            "    display_name: Documentation\n"
            "  ready:\n"
            "    display_name: Ready\n"
            "    terminal: true\n"
        ),
        encoding="utf-8",
    )
    (config_dir / "contracts.yaml").write_text(
        (
            "version: '1.0.0'\n"
            "merge_policy:\n"
            "  pr_allowed_phase: ready\n"
            "  branch_local_artifacts: []\n"
            "workflows:\n"
            "  feature:\n"
            "    phases:\n"
            "      - name: planning\n"
            "        instructions:\n"
            "          sub_role: test-role\n"
            "          phase_instructions: Test instructions.\n"
            "          handover_template: Test handover.\n"
            "      - name: implementation\n"
            "        cycle_based: true\n"
            "        subphases: [red, green, refactor]\n"
            "        commit_type_map:\n"
            "          red: test\n"
            "          green: feat\n"
            "          refactor: refactor\n"
            "        instructions:\n"
            "          sub_role: test-role\n"
            "          phase_instructions: Test instructions.\n"
            "          handover_template: Test handover.\n"
            "      - name: documentation\n"
            "        instructions:\n"
            "          sub_role: test-role\n"
            "          phase_instructions: Test instructions.\n"
            "          handover_template: Test handover.\n"
            "      - name: ready\n"
            "        instructions:\n"
            "          sub_role: test-role\n"
            "          phase_instructions: Test instructions.\n"
            "          handover_template: Test handover.\n"
        ),
        encoding="utf-8",
    )


def _create_config_driven_cycle_engine(
    workspace_root: Path,
    initial_phase: str,
) -> tuple[object, str, ConfigAwareCycleGateRunner]:
    """Create one branch using local phase_contracts cycle_based config."""
    issue_number = 257
    branch = f"feature/257-{initial_phase}-cycle-based"
    repository = InMemoryStateRepository()

    _write_cycle_based_tdd_configs(workspace_root)
    project_manager = make_project_manager(workspace_root)
    project_manager.initialize_project(
        issue_number=issue_number,
        issue_title="Config-driven cycle phase",
        workflow_name="feature",
    )
    project_manager.save_planning_deliverables(
        issue_number,
        SavePlanningModel.model_validate(
            {
                "cycles": {
                    "cycles": [
                        {
                            "cycle_name": "Cycle 1",
                            "deliverables": [{"deliverable_name": "D1", "description": "c1"}],
                            "exit_criteria": "first cycle ready",
                        },
                        {
                            "cycle_name": "Cycle 2",
                            "deliverables": [{"deliverable_name": "D2", "description": "c2"}],
                            "exit_criteria": "second cycle ready",
                        },
                    ],
                }
            }
        ),
    )
    gate_runner = ConfigAwareCycleGateRunner(
        make_phase_contract_resolver(workspace_root, project_plan_reader=project_manager)
    )
    engine = make_phase_state_engine(
        workspace_root,
        project_manager=project_manager,
        state_repository=repository,
        workflow_gate_runner=gate_runner,
    )
    engine.initialize_branch(
        branch=branch,
        issue_number=issue_number,
        initial_phase=initial_phase,
    )
    state = engine.get_state(branch)
    repository.save(state.with_updates(current_cycle=1, last_cycle=0))
    return engine, branch, gate_runner


def test_transition_cycle_raises_when_gate_blocks(
    workspace_root: Path,
    project_manager: ProjectManager,
) -> None:
    """transition_cycle() must use shared gate enforcement before persisting state."""
    gate_runner = BlockingCycleGateRunner()
    engine, branch = _create_cycle_engine(
        workspace_root,
        project_manager,
        gate_runner=gate_runner,
    )

    with pytest.raises(GateViolation, match="missing cycle transition evidence"):
        engine.transition_cycle(branch=branch, to_cycle=2)

    state = engine.get_state(branch)
    assert state.current_cycle == 1
    assert gate_runner.enforce_calls == [("feature", "implementation", 1, 257)]


def test_force_cycle_transition_returns_gate_inspection_report(
    workspace_root: Path,
    project_manager: ProjectManager,
) -> None:
    """force_cycle_transition() must return shared gate inspection details."""
    gate_runner = ReportingCycleGateRunner()
    engine, branch = _create_cycle_engine(
        workspace_root,
        project_manager,
        gate_runner=gate_runner,
    )

    result = engine.force_cycle_transition(
        branch=branch,
        to_cycle=3,
        skip_reason="audited forward skip",
        human_approval_message="Verifier approved on 2026-04-04",
    )

    state = engine.get_state(branch)
    history_entry = state.cycle_history[-1]

    assert result["success"] is True
    assert result["from_cycle"] == 1
    assert result["to_cycle"] == 3
    assert result["skipped_gates"] == ["cycle-checklist"]
    assert result["passing_gates"] == ["cycle-docs"]
    assert result["gate_report"] == {
        "passing": ["cycle-docs"],
        "blocking": ["cycle-checklist"],
        "details": {"cycle-checklist": "missing force-transition checklist"},
    }
    assert gate_runner.inspect_calls == [("feature", "implementation", 1, 257)]
    assert state.current_cycle == 3
    assert state.last_cycle == 1
    assert history_entry["forced"] is True
    assert history_entry["skipped_cycles"] == [2]


def test_cycle_transition_is_allowed_in_any_cycle_based_phase(workspace_root: Path) -> None:
    """Cycle transitions should follow cycle_based config instead of phase name."""
    engine, branch, gate_runner = _create_config_driven_cycle_engine(
        workspace_root,
        initial_phase="implementation",
    )

    result = engine.transition_cycle(branch=branch, to_cycle=2)

    state = engine.get_state(branch)
    assert result["success"] is True
    assert result["from_cycle"] == 1
    assert result["to_cycle"] == 2
    assert gate_runner.enforce_calls == [("feature", "implementation", 1, 257)]
    assert state.current_cycle == 2


def test_cycle_transition_is_blocked_in_non_cycle_based_phase(workspace_root: Path) -> None:
    """Cycle transitions should fail generically outside cycle_based phases."""
    engine, branch, gate_runner = _create_config_driven_cycle_engine(
        workspace_root,
        initial_phase="planning",
    )

    with pytest.raises(ValueError, match="cycle-based") as exc_info:
        engine.transition_cycle(branch=branch, to_cycle=2)

    assert "implementation" not in str(exc_info.value)
    assert gate_runner.enforce_calls == []
