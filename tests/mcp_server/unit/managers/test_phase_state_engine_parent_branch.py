"""Tests for PhaseStateEngine with parent_branch tracking.

Explicit parent admission and configured cycle behavior through public state operations.

@layer: Tests (Unit)
@dependencies: pytest, tests.mcp_server.test_support, mcp_server.managers.phase_state_engine
"""

from __future__ import annotations

from pathlib import Path
from subprocess import CompletedProcess
from typing import TYPE_CHECKING

import pytest

from mcp_server.core.exceptions import PreflightError, StateNotFoundError
from mcp_server.managers.state_repository import BranchState, InMemoryStateRepository
from mcp_server.schemas.deliverables import SavePlanningModel
from tests.mcp_server.test_support import (
    get_default_server_root,
    make_phase_state_engine,
    make_project_manager,
)

if TYPE_CHECKING:
    from mcp_server.managers.phase_state_engine import PhaseStateEngine
    from mcp_server.managers.project_manager import ProjectManager


class TestPhaseStateEngineParentBranch:
    """Test parent_branch functionality in PhaseStateEngine."""

    @pytest.fixture
    def workspace_root(self, tmp_path: Path) -> Path:
        """Create temporary workspace.

        Args:
            tmp_path: Pytest tmp_path fixture

        Returns:
            Path to temporary workspace root
        """
        return tmp_path

    @pytest.fixture
    def project_manager(self, workspace_root: Path) -> ProjectManager:
        """Create ProjectManager instance.

        Args:
            workspace_root: Path to workspace root

        Returns:
            ProjectManager instance
        """
        return make_project_manager(workspace_root)

    @pytest.fixture
    def engine(self, workspace_root: Path, project_manager: ProjectManager) -> PhaseStateEngine:
        """Create PhaseStateEngine instance.

        Args:
            workspace_root: Path to workspace root
            project_manager: ProjectManager instance

        Returns:
            PhaseStateEngine instance
        """
        return make_phase_state_engine(
            workspace_root,
            project_manager=project_manager,
            state_repository=InMemoryStateRepository(),
        )

    def test_initialize_branch_with_explicit_parent_branch(
        self, workspace_root: Path, project_manager: ProjectManager
    ) -> None:
        """Handover registers explicit identity without carrying prior branch progress."""
        repository = InMemoryStateRepository()
        repository.save(
            BranchState(
                branch="feature/78-previous",
                parent_branch="main",
                issue_number=78,
                workflow_name="feature",
                current_phase="implementation",
                current_cycle=2,
                last_cycle=1,
                cycle_history=[{"cycle_number": 1}],
                transitions=[{"from_phase": "research", "to_phase": "implementation"}],
                skip_reason="Previous branch decision",
                current_sub_phase="red",
            )
        )
        engine = make_phase_state_engine(
            workspace_root, project_manager=project_manager, state_repository=repository
        )
        project_manager.initialize_project(
            issue_number=79,
            issue_title="Explicit parent",
            workflow_name="feature",
            parent_branch="epic/76-qa",
        )

        result = engine.initialize_branch(
            branch="feature/79-test",
            issue_number=79,
            initial_phase="research",
            parent_branch="epic/76-qa",
        )

        assert result["success"] is True
        assert result["parent_branch"] == "epic/76-qa"
        state = engine.get_state("feature/79-test")
        assert state.parent_branch == "epic/76-qa"
        assert state.issue_number == 79
        assert state.current_cycle is None
        assert state.last_cycle is None
        assert state.cycle_history == []
        assert state.transitions == []
        assert state.skip_reason is None
        assert state.current_sub_phase is None
        plan = project_manager.get_project_plan(79)
        assert plan is not None
        assert plan["parent_branch"] == "epic/76-qa"

    def test_parent_mismatch_preserves_registration_absence(
        self, engine: PhaseStateEngine, project_manager: ProjectManager
    ) -> None:
        """A different supplied parent cannot register inconsistent branch state."""
        project_manager.initialize_project(
            issue_number=80,
            issue_title="Parent admission",
            workflow_name="bug",
            parent_branch="epic/76-qa",
        )
        before = project_manager.get_project_plan(80)

        with pytest.raises(PreflightError):
            engine.initialize_branch(
                branch="bug/80-test",
                issue_number=80,
                initial_phase="implementation",
                parent_branch="main",
            )

        with pytest.raises(StateNotFoundError):
            engine.get_state("bug/80-test")
        assert project_manager.get_project_plan(80) == before

    def test_initialize_branch_returns_warning_for_uncommitted_state_changes(
        self,
        engine: PhaseStateEngine,
        project_manager: ProjectManager,
        workspace_root: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """initialize_branch warns explicitly when tracked state.json has local changes."""
        project_manager.initialize_project(
            issue_number=84,
            issue_title="Warn on dirty state",
            workflow_name="feature",
            parent_branch="main",
        )
        state_file = workspace_root / get_default_server_root() / "state.json"
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(
            BranchState(
                branch="feature/83-previous",
                issue_number=83,
                workflow_name="feature",
                current_phase="ready",
                parent_branch="main",
            ).model_dump_json(),
            encoding="utf-8",
        )
        monkeypatch.setattr(
            "mcp_server.managers.phase_state_engine.subprocess.run",
            lambda *args, **kwargs: CompletedProcess(
                args=[], returncode=0, stdout=" M state.json\n"
            ),
        )

        result = engine.initialize_branch(
            branch="feature/84-dirty-state",
            issue_number=84,
            initial_phase="research",
            parent_branch="main",
        )

        assert result["warnings"] == ["state.json has uncommitted local changes"]


class TestTddCycleTrackingFields:
    """Test TDD cycle tracking fields in state management.

    Issue #146: State management correctly initializes/clears cycle fields.
    """

    @pytest.fixture
    def workspace_root(self, tmp_path: Path) -> Path:
        """Create temporary workspace.

        Args:
            tmp_path: Pytest tmp_path fixture

        Returns:
            Path to temporary workspace root
        """
        return tmp_path

    @pytest.fixture
    def project_manager(self, workspace_root: Path) -> ProjectManager:
        """Create ProjectManager instance.

        Args:
            workspace_root: Path to workspace root

        Returns:
            ProjectManager instance
        """
        return make_project_manager(workspace_root)

    @pytest.fixture
    def engine(self, workspace_root: Path, project_manager: ProjectManager) -> PhaseStateEngine:
        """Create PhaseStateEngine instance.

        Args:
            workspace_root: Path to workspace root
            project_manager: ProjectManager instance

        Returns:
            PhaseStateEngine instance
        """
        return make_phase_state_engine(
            workspace_root,
            project_manager=project_manager,
            state_repository=InMemoryStateRepository(),
        )

    def test_initialize_branch_creates_tdd_cycle_fields(
        self, engine: PhaseStateEngine, project_manager: ProjectManager
    ) -> None:
        """Test initialize_branch creates tdd_cycle_* fields.

        Issue #146: current_cycle, last_cycle, cycle_history must be initialized.
        """
        # Setup - create project
        project_manager.initialize_project(
            issue_number=146,
            issue_title="TDD Cycle Tracking",
            workflow_name="feature",
            parent_branch="main",
        )

        # Execute - initialize branch
        result = engine.initialize_branch(
            branch="feature/146-tdd-cycle-tracking",
            issue_number=146,
            initial_phase="research",
            parent_branch="main",
        )

        # Verify - result contains success
        assert result["success"] is True

        # Verify - state.json contains tdd_cycle_* fields
        state = engine.get_state("feature/146-tdd-cycle-tracking")
        assert hasattr(state, "current_cycle")
        assert hasattr(state, "last_cycle")
        assert hasattr(state, "cycle_history")

        # Verify - initial values
        assert state.current_cycle is None
        assert state.last_cycle is None
        assert state.cycle_history == []

        # Verify - initial values (None/[])
        assert state.current_cycle is None
        assert state.last_cycle is None
        assert state.cycle_history == []


class TestCycleValidationLogic:
    """Cycle admission is observed through complete public transitions."""

    @pytest.fixture
    def planned_engine(self, tmp_path: Path) -> tuple[PhaseStateEngine, str]:
        manager = make_project_manager(tmp_path)
        manager.initialize_project(146, "Cycle validation", "feature", parent_branch="main")
        manager.save_planning_deliverables(
            146,
            SavePlanningModel.model_validate(
                {
                    "cycles": {
                        "cycles": [
                            {
                                "cycle_name": f"Cycle {number}",
                                "deliverables": [
                                    {
                                        "deliverable_name": "Result",
                                        "description": f"Result {number}",
                                    }
                                ],
                                "exit_criteria": "Behavior demonstrated",
                            }
                            for number in range(1, 5)
                        ]
                    }
                }
            ),
        )
        engine = make_phase_state_engine(
            tmp_path, project_manager=manager, state_repository=InMemoryStateRepository()
        )
        branch = "feature/146-cycle-validation"
        engine.initialize_branch(branch, 146, "implementation", parent_branch="main")
        return engine, branch

    @pytest.mark.parametrize("cycle_number", [0, -1, 5])
    def test_invalid_cycle_range_preserves_state(
        self, planned_engine: tuple[PhaseStateEngine, str], cycle_number: int
    ) -> None:
        engine, branch = planned_engine
        state = engine.get_state(branch)
        with pytest.raises(ValueError, match="cycle_number must be in range"):
            engine.force_cycle_transition(
                branch, cycle_number, "Investigated selection", "Owner approved"
            )
        assert engine.get_state(branch) == state

    def test_valid_cycle_range_is_available_through_public_progression(
        self, planned_engine: tuple[PhaseStateEngine, str]
    ) -> None:
        engine, branch = planned_engine
        for number in range(1, 5):
            result = engine.transition_cycle(branch, number)
            assert result["to_cycle"] == number
            assert result["total_cycles"] == 4
            assert engine.get_state(branch).current_cycle == number

    def test_missing_plan_rejects_cycle_transition_without_mutation(self, tmp_path: Path) -> None:
        manager = make_project_manager(tmp_path)
        manager.initialize_project(147, "No planning yet", "bug", parent_branch="main")
        engine = make_phase_state_engine(
            tmp_path, project_manager=manager, state_repository=InMemoryStateRepository()
        )
        branch = "bug/147-no-plan"
        engine.initialize_branch(branch, 147, "implementation", parent_branch="main")
        state = engine.get_state(branch)
        with pytest.raises(ValueError, match="planning_deliverables_missing"):
            engine.transition_cycle(branch, 1)
        assert engine.get_state(branch) == state
