"""Tests for PhaseStateEngine with parent_branch tracking.

Issue #79: Tests for parent_branch in state management.
- initialize_branch with parent_branch
- Auto-recovery includes parent_branch from deliverables.json

@layer: Tests (Unit)
@dependencies: pytest, tests.mcp_server.test_support, mcp_server.managers.phase_state_engine
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from mcp_server.managers.project_manager import ProjectInitOptions
from mcp_server.managers.state_repository import InMemoryStateRepository
from mcp_server.schemas.deliverables import SavePlanningModel
from tests.mcp_server.test_support import (
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
        self, engine: PhaseStateEngine, project_manager: ProjectManager
    ) -> None:
        """Test initializing branch with explicit parent_branch.

        Issue #79: parent_branch can be passed explicitly to override project's value.
        """
        # Setup - create project with one parent
        project_manager.initialize_project(
            issue_number=79,
            issue_title="Test",
            workflow_name="feature",
            options=ProjectInitOptions(parent_branch="main"),
        )

        # Execute - initialize branch with different parent (override)
        result = engine.initialize_branch(
            branch="feature/79-test",
            issue_number=79,
            initial_phase="research",
            parent_branch="epic/76-qa",  # Override project's "main"
        )

        # Verify
        assert result["success"] is True
        assert result["parent_branch"] == "epic/76-qa"

        # Verify persisted to state.json
        state = engine.get_state("feature/79-test")
        assert state.parent_branch == "epic/76-qa"

    def test_initialize_branch_inherits_parent_from_project(
        self, engine: PhaseStateEngine, project_manager: ProjectManager
    ) -> None:
        """Test initializing branch inherits parent_branch from project.

        Issue #79: If parent_branch not provided, inherit from deliverables.json.
        """
        # Setup - create project with parent
        project_manager.initialize_project(
            issue_number=80,
            issue_title="Test",
            workflow_name="bug",
            options=ProjectInitOptions(parent_branch="epic/76-qa"),
        )

        # Execute - initialize branch WITHOUT parent_branch parameter
        result = engine.initialize_branch(
            branch="bug/80-test",
            issue_number=80,
            initial_phase="implementation",
            # No parent_branch - should inherit from project
        )

        # Verify
        assert result["success"] is True
        assert result["parent_branch"] == "epic/76-qa"

        # Verify persisted to state.json
        state = engine.get_state("bug/80-test")
        assert state.parent_branch == "epic/76-qa"

    def test_initialize_branch_with_none_parent_branch(
        self, engine: PhaseStateEngine, project_manager: ProjectManager
    ) -> None:
        """Test initializing branch when project has no parent_branch.

        Issue #79: Backward compatibility - parent_branch can be None.
        """
        # Setup - create project WITHOUT parent_branch
        project_manager.initialize_project(
            issue_number=81, issue_title="Old Project", workflow_name="docs"
        )

        # Execute - initialize branch
        result = engine.initialize_branch(
            branch="docs/81-test", issue_number=81, initial_phase="documentation"
        )

        # Verify
        assert result["success"] is True
        assert result["parent_branch"] is None

        # Verify persisted to state.json
        state = engine.get_state("docs/81-test")
        assert state.parent_branch is None

    def test_initialize_branch_returns_warning_for_uncommitted_state_changes(
        self,
        engine: PhaseStateEngine,
        project_manager: ProjectManager,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """initialize_branch warns explicitly when tracked state.json has local changes."""
        project_manager.initialize_project(
            issue_number=84,
            issue_title="Warn on dirty state",
            workflow_name="feature",
        )
        monkeypatch.setattr(engine, "_has_uncommitted_state_changes", lambda: True)

        result = engine.initialize_branch(
            branch="feature/84-dirty-state",
            issue_number=84,
            initial_phase="research",
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
            issue_number=146, issue_title="TDD Cycle Tracking", workflow_name="feature"
        )

        # Execute - initialize branch
        result = engine.initialize_branch(
            branch="feature/146-tdd-cycle-tracking", issue_number=146, initial_phase="research"
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
        manager.initialize_project(146, "Cycle validation", "feature")
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
        engine.initialize_branch(branch, 146, "implementation")
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
        manager.initialize_project(147, "No planning yet", "bug")
        engine = make_phase_state_engine(
            tmp_path, project_manager=manager, state_repository=InMemoryStateRepository()
        )
        branch = "bug/147-no-plan"
        engine.initialize_branch(branch, 147, "implementation")
        state = engine.get_state(branch)
        with pytest.raises(ValueError, match="planning_deliverables_missing"):
            engine.transition_cycle(branch, 1)
        assert engine.get_state(branch) == state
