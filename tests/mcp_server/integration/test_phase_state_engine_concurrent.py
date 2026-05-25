# tests/mcp_server/integration/test_phase_state_engine_concurrent.py
"""C4 (#292): Concurrent regression tests for PhaseStateEngine.

Proves that concurrent force_transition() and force_cycle_transition() calls
do not lose each other's mutations after the Boundary-1 stale-lambda fix.

The stale-lambda bug:
  Before C1, callers passed ``lambda _s: pre_captured_state.with_updates(...)``
  so the second writer always overwrote the first writer's changes entirely.
  After C1, callers pass ``lambda _s: _s.with_updates(...)`` so the second
  writer reads the freshest persisted state and only appends its own delta.

@layer: Tests (Integration)
@dependencies: [pytest, threading, mcp_server.managers.phase_state_engine]
"""

from __future__ import annotations

import threading
from pathlib import Path

from mcp_server.config.schemas.contracts_config import ContractsConfig
from mcp_server.core.interfaces import GateReport
from mcp_server.managers.phase_state_engine import PhaseStateEngine
from tests.mcp_server.test_support import (
    load_contracts_config,
    make_phase_state_engine,
    make_project_manager,
)

_BRANCH_D1 = "feature/292-mixed-concurrent"
_BRANCH_D2 = "feature/292-homogeneous-concurrent"
_ISSUE = 292
_PLANNING_DELIVERABLES = {
    "tdd_cycles": {
        "total": 4,
        "cycles": [
            {
                "cycle_number": 1,
                "name": "C1",
                "exit_criteria": "c1 done",
                "deliverables": [{"id": "C1-D1", "description": "C1 deliverable"}],
            },
            {
                "cycle_number": 2,
                "name": "C2",
                "exit_criteria": "c2 done",
                "deliverables": [{"id": "C2-D1", "description": "C2 deliverable"}],
            },
            {
                "cycle_number": 3,
                "name": "C3",
                "exit_criteria": "c3 done",
                "deliverables": [{"id": "C3-D1", "description": "C3 deliverable"}],
            },
            {
                "cycle_number": 4,
                "name": "C4",
                "exit_criteria": "c4 done",
                "deliverables": [{"id": "C4-D1", "description": "C4 deliverable"}],
            },
        ],
    }
}


class _ConcurrentTestGateRunner:
    """Gate runner for concurrent tests: always returns one passing gate.

    Returning a non-empty passing tuple prevents _legacy_workphases_gate_summary
    from being called inside force_transition/force_cycle_transition, avoiding
    thread-unsafe gitpython calls in WorkflowStatusResolver.resolve_current().
    is_cycle_based_phase is accurate: reads from the real ContractsConfig.
    """

    def __init__(self, contracts_config: ContractsConfig) -> None:
        self._contracts_config = contracts_config

    def is_cycle_based_phase(self, workflow_name: str, phase: str) -> bool:
        wf = self._contracts_config.workflows.get(workflow_name)
        if not wf:
            return False
        for p in wf.phases:
            if p.name == phase:
                return p.cycle_based
        return False

    def enforce(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int | None = None,
        checks: object = None,
    ) -> GateReport:
        del workflow_name, phase, cycle_number, checks
        return GateReport(passing=("nop",))

    def inspect(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int | None = None,
        checks: object = None,
    ) -> GateReport:
        del workflow_name, phase, cycle_number, checks
        return GateReport(passing=("nop",))


def _make_engine(tmp_path: Path, *, branch: str, initial_phase: str) -> PhaseStateEngine:
    """Bootstrap a PhaseStateEngine in tmp_path with a pre-initialized branch."""
    pm = make_project_manager(tmp_path)
    pm.initialize_project(
        issue_number=_ISSUE,
        issue_title="Concurrent regression test",
        workflow_name="feature",
    )
    pm.save_planning_deliverables(
        issue_number=_ISSUE,
        planning_deliverables=_PLANNING_DELIVERABLES,
    )
    engine = make_phase_state_engine(
        tmp_path,
        project_manager=pm,
        workflow_gate_runner=_ConcurrentTestGateRunner(load_contracts_config()),
    )
    engine.initialize_branch(
        branch=branch,
        issue_number=_ISSUE,
        initial_phase=initial_phase,
        parent_branch="main",
    )
    return engine


class TestPrimaryMixedConcurrentWritesC4:
    """C4-D1: force_transition() + force_cycle_transition() concurrent.

    Mixed writers modify different state fields (transitions vs cycle_history).
    Without the fresh-lambda fix, the second writer would overwrite the first
    writer's entire BranchState, discarding both mutations.
    """

    def test_force_transition_and_force_cycle_transition_concurrent(self, tmp_path: Path) -> None:
        """C4-D1: Mixed writers do not lose each other's mutations under concurrent access.

        Thread A calls force_transition() — appends to state.transitions.
        Thread B calls force_cycle_transition() — appends to state.cycle_history.
        Both use threading.Barrier for synchronized start.
        Final state must contain both mutations (C4-D1).
        """
        engine = _make_engine(tmp_path, branch=_BRANCH_D1, initial_phase="implementation")

        barrier: threading.Barrier = threading.Barrier(2)
        errors: list[BaseException] = []

        def run_force_transition() -> None:
            try:
                barrier.wait()
                engine.force_transition(
                    _BRANCH_D1,
                    "validation",
                    skip_reason="C4-D1-thread-A",
                    human_approval="C4 regression test approved",
                )
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        def run_force_cycle_transition() -> None:
            try:
                barrier.wait()
                engine.force_cycle_transition(
                    branch=_BRANCH_D1,
                    to_cycle=2,
                    skip_reason="C4-D1-thread-B",
                    human_approval="C4 regression test approved",
                )
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        t_a = threading.Thread(target=run_force_transition)
        t_b = threading.Thread(target=run_force_cycle_transition)
        t_a.start()
        t_b.start()
        t_a.join()
        t_b.join()

        if errors:
            raise AssertionError(
                f"Concurrent thread raised an unexpected exception: {errors[0]}"
            ) from errors[0]

        final_state = engine.get_state(_BRANCH_D1)
        assert len(final_state.transitions) >= 1, (
            "force_transition() mutation lost: state.transitions is empty after concurrent run"
        )
        assert len(final_state.cycle_history) >= 1, (
            "force_cycle_transition() mutation lost: "
            "state.cycle_history is empty after concurrent run"
        )


class TestSecondaryHomogeneousConcurrentWritesC4:
    """C4-D2: Two concurrent force_transition() calls — both records present.

    Homogeneous writers both modify state.transitions.
    Without the fresh-lambda fix, the second writer would start from pre-captured
    state so cycle_history=[first_entry] written by writer-1 would be overwritten
    by writer-2's lambda that captured the original empty state.
    """

    def test_two_concurrent_force_transitions_both_records_present(self, tmp_path: Path) -> None:
        """C4-D2: Two concurrent force_transition() calls — both transition records survive.

        Thread A calls force_transition(to_phase='design').
        Thread B calls force_transition(to_phase='planning').
        Both start from 'research' phase via threading.Barrier.
        Final state.transitions must contain records from both calls (C4-D2).
        """
        engine = _make_engine(tmp_path, branch=_BRANCH_D2, initial_phase="research")

        barrier: threading.Barrier = threading.Barrier(2)
        errors: list[BaseException] = []

        def run_force_transition_a() -> None:
            try:
                barrier.wait()
                engine.force_transition(
                    _BRANCH_D2,
                    "design",
                    skip_reason="C4-D2-thread-A",
                    human_approval="C4 regression test approved",
                )
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        def run_force_transition_b() -> None:
            try:
                barrier.wait()
                engine.force_transition(
                    _BRANCH_D2,
                    "planning",
                    skip_reason="C4-D2-thread-B",
                    human_approval="C4 regression test approved",
                )
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        t_a = threading.Thread(target=run_force_transition_a)
        t_b = threading.Thread(target=run_force_transition_b)
        t_a.start()
        t_b.start()
        t_a.join()
        t_b.join()

        if errors:
            raise AssertionError(
                f"Concurrent thread raised an unexpected exception: {errors[0]}"
            ) from errors[0]

        final_state = engine.get_state(_BRANCH_D2)
        assert len(final_state.transitions) == 2, (
            f"Expected 2 transition records after two concurrent force_transition() calls, "
            f"got {len(final_state.transitions)}: {final_state.transitions}"
        )
