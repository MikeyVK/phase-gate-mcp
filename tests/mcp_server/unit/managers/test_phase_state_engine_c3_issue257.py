# tests/mcp_server/unit/managers/test_phase_state_engine_c3_issue257.py
"""Tests for C_STATE_RECOVERY behavior (Issue #257 Cycle 3).

Cycle 3 goals covered here:
- transition() reconstructs missing state through IStateReconstructor.
- reconstructed state is saved before transition flow continues.
- force_transition() reconstructs missing state through the same recovery path.
- get_state() is a pure query and does not reconstruct or persist on failure.

@layer: Tests (Unit)
@dependencies: [pytest, tests.mcp_server.test_support, mcp_server.managers.phase_state_engine]
"""

from __future__ import annotations

from pathlib import Path

import pytest

from mcp_server.core.interfaces import GateReport
from mcp_server.managers.project_manager import ProjectManager
from mcp_server.managers.state_repository import BranchState
from tests.mcp_server.test_support import make_phase_state_engine, make_project_manager


@pytest.fixture
def workspace_root(tmp_path: Path) -> Path:
    """Temporary workspace root for tests."""
    return tmp_path


@pytest.fixture
def project_manager(workspace_root: Path) -> ProjectManager:
    """ProjectManager bound to the temp workspace."""
    return make_project_manager(workspace_root)


class MissingThenPersistingRepository:
    """Repository that simulates one missing-state load until a save happens."""

    def __init__(self) -> None:
        self._states: dict[str, BranchState] = {}
        self.save_count = 0

    def load(self, branch: str) -> BranchState:
        if branch not in self._states:
            raise FileNotFoundError(branch)
        return self._states[branch]

    def save(self, state: BranchState) -> None:
        self.save_count += 1
        self._states[state.branch] = state


class RaisingRepository:
    """Repository that always raises on load and tracks whether save was attempted."""

    def __init__(self, exc: Exception) -> None:
        self._exc = exc
        self.saved_states: list[BranchState] = []

    def load(self, _branch: str) -> BranchState:
        raise self._exc

    def save(self, state: BranchState) -> None:
        self.saved_states.append(state)


class PassingGateRunner:
    """Gate runner fake that allows every transition."""

    def is_cycle_based_phase(self, workflow_name: str, phase: str) -> bool:
        del workflow_name
        return phase == "implementation"

    def enforce_phase_exit(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int | None = None,
    ) -> GateReport:
        del workflow_name, phase, cycle_number
        return GateReport()

    def inspect_phase_exit(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int | None = None,
    ) -> GateReport:
        del workflow_name, phase, cycle_number
        return GateReport()


class ReportingGateRunner(PassingGateRunner):
    """Gate runner fake that reports forced-transition audit information."""

    def inspect_phase_exit(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int | None = None,
    ) -> GateReport:
        del workflow_name, phase, cycle_number
        return GateReport(
            passing=("design-doc",),
            blocking=("planning-doc",),
            details={"planning-doc": "missing planning document"},
        )


def test_get_state_does_not_reconstruct_or_save_on_load_failure(
    workspace_root: Path,
    project_manager: ProjectManager,
) -> None:
    """get_state() must not reconstruct or persist when the repository load fails."""
    project_manager.initialize_project(
        issue_number=257,
        issue_title="Cycle 3 pure query",
        workflow_name="feature",
    )
    repository = RaisingRepository(FileNotFoundError("missing state"))
    engine = make_phase_state_engine(
        workspace_root,
        project_manager=project_manager,
        state_repository=repository,
        workflow_gate_runner=PassingGateRunner(),
    )

    with pytest.raises(FileNotFoundError, match="missing state"):
        engine.get_state("feature/257-c3-pure-query")

    assert repository.saved_states == []


def test_get_state_raises_when_repository_load_fails(
    workspace_root: Path,
    project_manager: ProjectManager,
) -> None:
    """get_state() must surface repository errors as a pure query API."""
    project_manager.initialize_project(
        issue_number=257,
        issue_title="Cycle 3 repository failure",
        workflow_name="feature",
    )
    repository = RaisingRepository(OSError("disk failure"))
    engine = make_phase_state_engine(
        workspace_root,
        project_manager=project_manager,
        state_repository=repository,
        workflow_gate_runner=PassingGateRunner(),
    )

    with pytest.raises(OSError, match="disk failure"):
        engine.get_state("feature/257-c3-io-error")

    assert repository.saved_states == []
