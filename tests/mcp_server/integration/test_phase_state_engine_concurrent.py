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

import pytest

from tests.mcp_server.test_support import make_phase_state_engine, make_project_manager

_BRANCH_D1 = "feature/292-mixed-concurrent"
_BRANCH_D2 = "feature/292-homogeneous-concurrent"
_ISSUE = 292
_PLANNING_DELIVERABLES = {
    "tdd_cycles": {
        "total": 4,
        "cycles": [
            {"cycle_number": 1, "name": "C1", "exit_criteria": "c1 done"},
            {"cycle_number": 2, "name": "C2", "exit_criteria": "c2 done"},
            {"cycle_number": 3, "name": "C3", "exit_criteria": "c3 done"},
            {"cycle_number": 4, "name": "C4", "exit_criteria": "c4 done"},
        ],
    }
}


def _make_engine(tmp_path: Path, *, branch: str, initial_phase: str):
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
    engine = make_phase_state_engine(tmp_path, project_manager=pm)
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

    def test_force_transition_and_force_cycle_transition_concurrent(
        self, tmp_path: Path
    ) -> None:
        """C4-D1: Mixed writers do not lose each other's mutations under concurrent access.

        Thread A calls force_transition() — appends to state.transitions.
        Thread B calls force_cycle_transition() — appends to state.cycle_history.
        Both use threading.Barrier for synchronized start.
        Final state must contain both mutations (C4-D1).
        """
        pytest.fail("C4-RED: stub — C4-D1 mixed concurrent writer test not yet implemented")


class TestSecondaryHomogeneousConcurrentWritesC4:
    """C4-D2: Two concurrent force_transition() calls — both records present.

    Homogeneous writers both modify state.transitions.
    Without the fresh-lambda fix, the second writer would start from pre-captured
    state so cycle_history=[first_entry] written by writer-1 would be overwritten
    by writer-2's lambda that captured the original empty state.
    """

    def test_two_concurrent_force_transitions_both_records_present(
        self, tmp_path: Path
    ) -> None:
        """C4-D2: Two concurrent force_transition() calls — both transition records survive.

        Thread A calls force_transition(to_phase='design').
        Thread B calls force_transition(to_phase='planning').
        Both start from 'research' phase via threading.Barrier.
        Final state.transitions must contain records from both calls (C4-D2).
        """
        pytest.fail(
            "C4-RED: stub — C4-D2 homogeneous concurrent writer test not yet implemented"
        )
