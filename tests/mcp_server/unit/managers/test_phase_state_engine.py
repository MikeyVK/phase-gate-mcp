"""Tests for PhaseStateEngine implementation-phase lifecycle hooks.

Issue #146 Cycle 4: implementation phase lifecycle hooks.

@layer: Tests (Unit)
@dependencies: pytest, tests.mcp_server.test_support, mcp_server.managers.phase_state_engine
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from mcp_server.core.interfaces import IContextLoadedWriter
from mcp_server.managers.phase_state_engine import PhaseStateEngine
from mcp_server.managers.state_repository import (
    BranchState,
    InMemoryStateRepository,
    StateBranchMismatchError,
)
from tests.mcp_server.test_support import make_phase_state_engine, make_project_manager


class TestTDDPhaseHooks:
    """Tests for implementation phase entry/exit hooks.

    Issue #146 Cycle 4: on_enter_implementation_phase and on_exit_implementation_phase.
    """

    @pytest.fixture()
    def setup_project(self, tmp_path: Path) -> tuple[Path, int]:
        """Create project with planning deliverables."""
        workspace_root = tmp_path
        issue_number = 146

        project_manager = make_project_manager(workspace_root)

        # Initialize project
        project_manager.initialize_project(
            issue_number=issue_number,
            issue_title="TDD Cycle Tracking",
            workflow_name="feature",
        )

        # Save planning deliverables (4 cycles)
        planning_deliverables = {
            "tdd_cycles": {
                "total": 4,
                "cycles": [
                    {
                        "cycle_number": 1,
                        "name": "Schema & Storage",
                        "deliverables": ["Schema"],
                        "exit_criteria": "Tests pass",
                    },
                    {
                        "cycle_number": 2,
                        "name": "Validation Logic",
                        "deliverables": ["Validators"],
                        "exit_criteria": "All scenarios covered",
                    },
                    {
                        "cycle_number": 3,
                        "name": "Discovery Tools",
                        "deliverables": ["get_work_context"],
                        "exit_criteria": "Tools return cycle info",
                    },
                    {
                        "cycle_number": 4,
                        "name": "Transition Tools",
                        "deliverables": ["transition_cycle", "force_cycle_transition"],
                        "exit_criteria": "All transitions working",
                    },
                ],
            }
        }
        project_manager.save_planning_deliverables(
            issue_number=issue_number, planning_deliverables=planning_deliverables
        )

        return workspace_root, issue_number

    def test_on_enter_implementation_phase_initializes_cycle_1(
        self, setup_project: tuple[Path, int]
    ) -> None:
        """Test that entering implementation phase auto-initializes cycle 1."""
        # Arrange
        workspace_root, issue_number = setup_project
        branch = "feature/146-tdd-cycle-tracking"

        project_manager = make_project_manager(workspace_root)
        state_engine = make_phase_state_engine(
            workspace_root,
            project_manager=project_manager,
            state_repository=InMemoryStateRepository(),
        )

        # Initialize branch in design phase (one step before implementation)
        state_engine.initialize_branch(
            branch=branch, issue_number=issue_number, initial_phase="design"
        )

        # Verify no TDD cycle yet
        state = state_engine.get_state(branch)
        assert state.current_cycle is None

        # Act
        state_engine.on_enter_cycle_based_phase(branch, issue_number)

        # Assert
        state = state_engine.get_state(branch)
        assert state.current_cycle == 1
        assert state.last_cycle == 0

    def test_on_enter_implementation_phase_does_not_block_without_planning_deliverables(
        self, tmp_path: Path
    ) -> None:
        """Test that entering implementation phase does NOT block on missing planning deliverables.

        GAP-02 fix (Issue #229 C2): the planning-deliverables check was moved to
        on_exit_planning_phase. TDD entry must no longer enforce this contract.
        """
        # Arrange
        workspace_root = tmp_path
        issue_number = 146
        branch = "feature/146-tdd-cycle-tracking"

        project_manager = make_project_manager(workspace_root)
        state_engine = make_phase_state_engine(
            workspace_root,
            project_manager=project_manager,
            state_repository=InMemoryStateRepository(),
        )

        # Initialize project WITHOUT planning deliverables
        project_manager.initialize_project(
            issue_number=issue_number,
            issue_title="TDD Cycle Tracking",
            workflow_name="feature",
        )

        state_engine.initialize_branch(
            branch=branch, issue_number=issue_number, initial_phase="design"
        )

        # Act & Assert â€” must NOT raise; gate lives at planning exit now
        state_engine.on_enter_cycle_based_phase(branch, issue_number)
        state = state_engine.get_state(branch)
        assert state.current_cycle == 1

    def test_on_exit_implementation_phase_preserves_last_cycle(
        self, setup_project: tuple[Path, int]
    ) -> None:
        """Test that exiting implementation phase preserves last_cycle."""
        # Arrange
        workspace_root, issue_number = setup_project
        branch = "feature/146-tdd-cycle-tracking"

        project_manager = make_project_manager(workspace_root)
        state_repository = InMemoryStateRepository()
        state_engine = make_phase_state_engine(
            workspace_root,
            project_manager=project_manager,
            state_repository=state_repository,
        )

        # Initialize in implementation phase at cycle 3
        state_engine.initialize_branch(
            branch=branch, issue_number=issue_number, initial_phase="implementation"
        )
        state = state_engine.get_state(branch)
        state_repository.save(state.with_updates(current_cycle=3))

        # Act
        state_engine.on_exit_cycle_based_phase(branch)

        # Assert
        state = state_engine.get_state(branch)
        assert state.last_cycle == 3
        assert state.current_cycle == 3

    def test_on_exit_implementation_phase_validates_completion(
        self, setup_project: tuple[Path, int]
    ) -> None:
        """Test that exiting implementation phase validates all cycles completed."""
        # Arrange
        workspace_root, issue_number = setup_project
        branch = "feature/146-tdd-cycle-tracking"

        project_manager = make_project_manager(workspace_root)
        state_repository = InMemoryStateRepository()
        state_engine = make_phase_state_engine(
            workspace_root,
            project_manager=project_manager,
            state_repository=state_repository,
        )

        # Initialize in implementation phase at cycle 2 (not completed)
        state_engine.initialize_branch(
            branch=branch, issue_number=issue_number, initial_phase="implementation"
        )
        state = state_engine.get_state(branch)
        state_repository.save(state.with_updates(current_cycle=2))

        # Act
        # Design decision: Allow exit with warning (logs but doesn't block)
        state_engine.on_exit_cycle_based_phase(branch)

        # Assert
        state = state_engine.get_state(branch)
        assert state.last_cycle == 2
        assert state.current_cycle == 2


class TestPhaseStateEngineCleanBreak:
    """C_ENGINE_BREAK: get_state() propagates StateBranchMismatchError (issue #231)."""

    class _FixedReader:
        """Returns the configured state regardless of the requested branch."""

        def __init__(self, state: BranchState) -> None:
            self._state = state

        def load(self, _branch: str) -> BranchState:
            return self._state

    def test_get_state_raises_mismatch_error_not_file_not_found(self, tmp_path: Path) -> None:
        """get_state() must raise StateBranchMismatchError on mismatch, not FileNotFoundError."""
        fixed_state = BranchState(
            branch="main",
            issue_number=None,
            workflow_name="feature",
            current_phase="implementation",
            current_cycle=None,
            required_phases=["implementation"],
            transitions=[],
        )
        engine = make_phase_state_engine(
            workspace_root=tmp_path,
            state_repository=self._FixedReader(fixed_state),
        )
        with pytest.raises(StateBranchMismatchError):
            engine.get_state("feature/231-state-snapshot-cqrs")


class TestTransitionHooksWiring:
    """Tests that transition() automatically calls entry/exit hooks (Issue #146 Cycle 5 D3)."""

    @pytest.fixture()
    def setup_project(self, tmp_path: Path) -> tuple[Path, int]:
        """Create project with planning deliverables."""
        workspace_root = tmp_path
        issue_number = 999
        config_dir = workspace_root / ".phase-gate" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        (config_dir / "contracts.yaml").write_text(
            (
                "merge_policy:\n"
                "  pr_allowed_phase: ready\n"
                "  branch_local_artifacts: []\n"
                "workflows:\n"
                "  feature:\n"
                "    phases:\n"
                "      - name: design\n"
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
                "      - name: validation\n"
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

        project_manager = make_project_manager(workspace_root)
        project_manager.initialize_project(
            issue_number=issue_number,
            issue_title="Hook Wiring Test",
            workflow_name="feature",
        )
        project_manager.save_planning_deliverables(
            issue_number=issue_number,
            planning_deliverables={
                "tdd_cycles": {
                    "total": 1,
                    "cycles": [
                        {
                            "cycle_number": 1,
                            "name": "Basic",
                            "deliverables": ["A"],
                            "exit_criteria": "pass",
                        }
                    ],
                }
            },
        )
        return workspace_root, issue_number

    def test_transition_to_tdd_calls_enter_hook(self, setup_project: tuple[Path, int]) -> None:
        """Test that transition() to 'implementation' auto-calls on_enter_implementation_phase (Issue #146)."""
        workspace_root, issue_number = setup_project
        branch = "feature/999-hook-wiring"

        project_manager = make_project_manager(workspace_root)
        state_engine = make_phase_state_engine(
            workspace_root,
            project_manager=project_manager,
            state_repository=InMemoryStateRepository(),
        )

        # Initialize branch in design phase (one step before implementation)
        state_engine.initialize_branch(
            branch=branch, issue_number=issue_number, initial_phase="design"
        )

        # Verify no active cycle before transition
        state = state_engine.get_state(branch)
        assert state.current_cycle is None

        # Transition to implementation - should auto-call on_enter_implementation_phase
        state_engine.transition(branch=branch, to_phase="implementation")

        # Assert: hook was triggered and cycle 1 was initialized
        state = state_engine.get_state(branch)
        assert state.current_cycle == 1, (
            "on_enter_implementation_phase was not called by transition() - "
            "current_cycle should be 1 after entering implementation phase"
        )

    def test_transition_from_tdd_calls_exit_hook(self, setup_project: tuple[Path, int]) -> None:
        """Test that transition() from 'implementation' auto-calls on_exit_implementation_phase."""
        workspace_root, issue_number = setup_project
        branch = "feature/999-hook-wiring"

        project_manager = make_project_manager(workspace_root)
        state_repository = InMemoryStateRepository()
        state_engine = make_phase_state_engine(
            workspace_root,
            project_manager=project_manager,
            state_repository=state_repository,
        )

        # Initialize branch in implementation phase at cycle 2
        state_engine.initialize_branch(
            branch=branch, issue_number=issue_number, initial_phase="implementation"
        )
        state = state_engine.get_state(branch)
        state_repository.save(state.with_updates(current_cycle=2))

        # Transition away from TDD - should auto-call on_exit_implementation_phase
        state_engine.transition(branch=branch, to_phase="validation")

        # Assert: hook was triggered and last_cycle was preserved
        state = state_engine.get_state(branch)
        assert state.last_cycle == 2, (
            "on_exit_implementation_phase was not called by transition() - "
            "last_cycle should be 2 after exiting implementation phase"
        )
        assert state.current_cycle == 2, "current_cycle should be preserved after exiting implementation phase"

    def test_force_reentry_to_implementation_preserves_active_cycle(
        self, setup_project: tuple[Path, int]
    ) -> None:
        """Implementation detour re-entry preserves the active cycle.

        Re-entry after a planning detour must not reset the cycle to 1.
        """
        workspace_root, issue_number = setup_project
        branch = "feature/999-detour-reentry"

        project_manager = make_project_manager(workspace_root)
        state_repository = InMemoryStateRepository()
        state_engine = make_phase_state_engine(
            workspace_root,
            project_manager=project_manager,
            state_repository=state_repository,
        )

        state_engine.initialize_branch(
            branch=branch, issue_number=issue_number, initial_phase="implementation"
        )
        state = state_engine.get_state(branch)
        state_repository.save(state.with_updates(current_cycle=2))

        state_engine.force_transition(
            branch=branch,
            to_phase="planning",
            skip_reason="Test detour to planning",
            human_approval="Test approved on 2026-06-04",
        )
        state_engine.force_transition(
            branch=branch,
            to_phase="implementation",
            skip_reason="Test re-entry to implementation",
            human_approval="Test approved on 2026-06-04",
        )

        state = state_engine.get_state(branch)
        assert state.current_phase == "implementation"
        assert state.current_cycle == 2, "current_cycle should remain on the active detour cycle"
        assert state.last_cycle == 2


class TestPhaseStateEngineMutatorRoutingC6:
    """C6 (C_MUTATOR_CORE): PhaseStateEngine routes writes through IWorkflowStateMutator."""

    class _TrackingMutator:
        """Spy mutator that records apply() calls and delegates to real repository."""

        def __init__(self, repo: InMemoryStateRepository) -> None:
            self._repo = repo
            self.apply_calls: list[str] = []

        def apply(self, branch: str, mutate: object) -> None:
            self.apply_calls.append(branch)
            try:
                state = self._repo.load(branch)
            except KeyError:
                state = BranchState(
                    branch=branch,
                    workflow_name="",
                    current_phase="",
                )
            new_state = mutate(state)  # type: ignore[operator]
            self._repo.save(new_state)

    def test_phase_state_engine_accepts_workflow_state_mutator_kwarg(self, tmp_path: Path) -> None:
        """PhaseStateEngine accepts workflow_state_mutator kwarg.

        RED: make_phase_state_engine does not have this param -> TypeError.
        """
        repo = InMemoryStateRepository()
        mutator = self._TrackingMutator(repo)
        engine = make_phase_state_engine(
            tmp_path,
            state_repository=repo,
            workflow_state_mutator=mutator,
        )
        assert engine is not None

    def test_initialize_branch_routes_through_mutator(self, tmp_path: Path) -> None:
        """initialize_branch() calls workflow_state_mutator.apply().

        RED: fails until GREEN routes initialize_branch through mutator.
        """
        project_manager = make_project_manager(tmp_path)
        project_manager.initialize_project(
            issue_number=231,
            issue_title="State Split",
            workflow_name="feature",
        )
        repo = InMemoryStateRepository()
        mutator = self._TrackingMutator(repo)
        engine = make_phase_state_engine(
            tmp_path,
            project_manager=project_manager,
            state_repository=repo,
            workflow_state_mutator=mutator,
        )
        engine.initialize_branch(
            branch="feature/231-test",
            issue_number=231,
            initial_phase="research",
        )
        assert mutator.apply_calls == ["feature/231-test"]

    def test_transition_routes_through_mutator(self, tmp_path: Path) -> None:
        """transition() calls workflow_state_mutator.apply().

        RED: fails until GREEN routes transition() through mutator.
        """
        project_manager = make_project_manager(tmp_path)
        project_manager.initialize_project(
            issue_number=231,
            issue_title="State Split",
            workflow_name="feature",
        )
        repo = InMemoryStateRepository()
        mutator = self._TrackingMutator(repo)
        engine = make_phase_state_engine(
            tmp_path,
            project_manager=project_manager,
            state_repository=repo,
            workflow_state_mutator=mutator,
        )
        seed = BranchState(
            branch="feature/231-test",
            issue_number=231,
            workflow_name="feature",
            current_phase="research",
        )
        repo.save(seed)
        mutator.apply_calls.clear()

        engine.transition(branch="feature/231-test", to_phase="design")

        assert "feature/231-test" in mutator.apply_calls

    def test_on_enter_implementation_phase_routes_through_mutator(self, tmp_path: Path) -> None:
        """on_enter_implementation_phase() calls mutator.apply().

        RED: fails until GREEN routes implementation hooks through mutator.
        """
        project_manager = make_project_manager(tmp_path)
        project_manager.initialize_project(
            issue_number=231,
            issue_title="State Split",
            workflow_name="feature",
        )
        repo = InMemoryStateRepository()
        mutator = self._TrackingMutator(repo)
        engine = make_phase_state_engine(
            tmp_path,
            project_manager=project_manager,
            state_repository=repo,
            workflow_state_mutator=mutator,
        )
        seed = BranchState(
            branch="feature/231-test",
            issue_number=231,
            workflow_name="feature",
            current_phase="implementation",
        )
        repo.save(seed)
        mutator.apply_calls.clear()

        engine.on_enter_cycle_based_phase("feature/231-test", 231)

        assert "feature/231-test" in mutator.apply_calls

    def test_on_exit_implementation_phase_routes_through_mutator(self, tmp_path: Path) -> None:
        """on_exit_implementation_phase() calls mutator.apply().

        RED: fails until GREEN routes implementation hooks through mutator.
        """
        project_manager = make_project_manager(tmp_path)
        project_manager.initialize_project(
            issue_number=231,
            issue_title="State Split",
            workflow_name="feature",
        )
        repo = InMemoryStateRepository()
        mutator = self._TrackingMutator(repo)
        engine = make_phase_state_engine(
            tmp_path,
            project_manager=project_manager,
            state_repository=repo,
            workflow_state_mutator=mutator,
        )
        seed = BranchState(
            branch="feature/231-test",
            issue_number=231,
            workflow_name="feature",
            current_phase="implementation",
            current_cycle=1,
        )
        repo.save(seed)
        mutator.apply_calls.clear()

        engine.on_exit_cycle_based_phase("feature/231-test")

        assert "feature/231-test" in mutator.apply_calls


# ---------------------------------------------------------------------------
# C4 RED — PhaseStateEngine.record_sub_phase() + clearing (issue #298)
# ---------------------------------------------------------------------------


class TestPhaseStateEngineRecordSubPhase:
    """C4 (issue #298): record_sub_phase() persists sub_phase; transitions clear it."""

    def _make_engine_and_state(
        self, tmp_path: Path, *, sub_phase: str | None = None
    ) -> tuple[object, InMemoryStateRepository, str]:
        """Return (engine, repo, branch) with seeded state."""
        branch = "feature/298-test"
        project_manager = make_project_manager(tmp_path)
        project_manager.initialize_project(
            issue_number=298,
            issue_title="Sub-phase persistence",
            workflow_name="feature",
        )
        repo = InMemoryStateRepository()
        engine = make_phase_state_engine(
            tmp_path,
            project_manager=project_manager,
            state_repository=repo,
        )
        seed = BranchState(
            branch=branch,
            issue_number=298,
            workflow_name="feature",
            current_phase="implementation",
            current_cycle=1,
            current_sub_phase=sub_phase,
        )
        repo.save(seed)
        return engine, repo, branch

    def test_record_sub_phase_writes_to_state(self, tmp_path: Path) -> None:
        """record_sub_phase(branch, 'red') must persist current_sub_phase='red'."""
        engine, repo, branch = self._make_engine_and_state(tmp_path)
        engine.record_sub_phase(branch, "red")
        assert repo.load(branch).current_sub_phase == "red"

    def test_record_sub_phase_none_clears_state(self, tmp_path: Path) -> None:
        """record_sub_phase(branch, None) must set current_sub_phase=None."""
        engine, repo, branch = self._make_engine_and_state(tmp_path, sub_phase="red")
        engine.record_sub_phase(branch, None)
        assert repo.load(branch).current_sub_phase is None

    def test_transition_clears_sub_phase(self, tmp_path: Path) -> None:
        """transition() must clear current_sub_phase (set to None) on state write."""
        _, repo, branch = self._make_engine_and_state(tmp_path, sub_phase="green")
        # transition from research so no gate enforcement needed; seed directly
        repo.save(repo.load(branch).with_updates(current_phase="research", current_cycle=None))
        project_manager = make_project_manager(tmp_path)
        engine2 = make_phase_state_engine(
            tmp_path, project_manager=project_manager, state_repository=repo
        )
        engine2.transition(branch=branch, to_phase="design")
        assert repo.load(branch).current_sub_phase is None

    def test_force_transition_clears_sub_phase(self, tmp_path: Path) -> None:
        """force_transition() must clear current_sub_phase on state write."""
        engine, repo, branch = self._make_engine_and_state(tmp_path, sub_phase="red")
        repo.save(repo.load(branch).with_updates(current_phase="research", current_cycle=None))
        engine.force_transition(
            branch=branch,
            to_phase="design",
            skip_reason="QA approved skip",
            human_approval="MVerkaik approved on 2026-05-05",
        )
        assert repo.load(branch).current_sub_phase is None

    def test_transition_cycle_clears_sub_phase(self, tmp_path: Path) -> None:
        """transition_cycle() must clear current_sub_phase on state write."""
        project_manager = make_project_manager(tmp_path)
        project_manager.initialize_project(
            issue_number=298,
            issue_title="Sub-phase persistence",
            workflow_name="feature",
        )
        project_manager.save_planning_deliverables(
            issue_number=298,
            planning_deliverables={
                "tdd_cycles": {
                    "total": 2,
                    "cycles": [
                        {
                            "cycle_number": 1,
                            "name": "C1",
                            "deliverables": ["deliverable-a"],
                            "exit_criteria": "pass",
                        },
                        {
                            "cycle_number": 2,
                            "name": "C2",
                            "deliverables": ["deliverable-b"],
                            "exit_criteria": "pass",
                        },
                    ],
                }
            },
        )
        repo = InMemoryStateRepository()
        engine = make_phase_state_engine(
            tmp_path, project_manager=project_manager, state_repository=repo
        )
        branch = "feature/298-test"
        repo.save(
            BranchState(
                branch=branch,
                issue_number=298,
                workflow_name="feature",
                current_phase="implementation",
                current_cycle=1,
                current_sub_phase="refactor",
            )
        )
        engine.transition_cycle(branch=branch, to_cycle=2)
        assert repo.load(branch).current_sub_phase is None

    def test_on_exit_cycle_based_phase_does_not_touch_sub_phase(self, tmp_path: Path) -> None:
        """on_exit_cycle_based_phase() must not modify current_sub_phase."""
        engine, repo, branch = self._make_engine_and_state(tmp_path, sub_phase="green")
        engine.on_exit_cycle_based_phase(branch)
        # sub_phase must remain unchanged (hook owns only cycle tracking)
        assert repo.load(branch).current_sub_phase == "green"


class TestContextLoadedWriterReset:
    """C5: IContextLoadedWriter injected into PhaseStateEngine clears flag on state changes."""

    _CONTRACTS_YAML = (
        "merge_policy:\n"
        "  pr_allowed_phase: ready\n"
        "  branch_local_artifacts: []\n"
        "workflows:\n"
        "  feature:\n"
        "    phases:\n"
        "      - name: design\n"
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
        "      - name: validation\n"
        "        instructions:\n"
        "          sub_role: test-role\n"
        "          phase_instructions: Test instructions.\n"
        "          handover_template: Test handover.\n"
        "      - name: ready\n"
        "        instructions:\n"
        "          sub_role: test-role\n"
        "          phase_instructions: Test instructions.\n"
        "          handover_template: Test handover.\n"
    )

    @pytest.fixture()
    def project(self, tmp_path: Path) -> tuple[Path, int]:
        """Set up project with two TDD cycles for reset-writer tests."""
        config_dir = tmp_path / ".phase-gate" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        (config_dir / "contracts.yaml").write_text(self._CONTRACTS_YAML, encoding="utf-8")

        issue_number = 268
        pm = make_project_manager(tmp_path)
        pm.initialize_project(
            issue_number=issue_number,
            issue_title="Context loaded writer test",
            workflow_name="feature",
        )
        pm.save_planning_deliverables(
            issue_number=issue_number,
            planning_deliverables={
                "tdd_cycles": {
                    "total": 2,
                    "cycles": [
                        {
                            "cycle_number": 1,
                            "name": "A",
                            "deliverables": ["x"],
                            "exit_criteria": "pass",
                        },
                        {
                            "cycle_number": 2,
                            "name": "B",
                            "deliverables": ["y"],
                            "exit_criteria": "pass",
                        },
                    ],
                }
            },
        )
        return tmp_path, issue_number

    def test_phase_state_engine_resets_flag_on_transition(self, project: tuple[Path, int]) -> None:
        """writer.set_context_loaded(branch, False) called after successful transition()."""
        workspace_root, issue_number = project
        branch = f"feature/{issue_number}-test"
        writer = MagicMock(spec=IContextLoadedWriter)

        engine = make_phase_state_engine(
            workspace_root,
            project_manager=make_project_manager(workspace_root),
            state_repository=InMemoryStateRepository(),
            context_loaded_writer=writer,
        )
        engine.initialize_branch(branch=branch, issue_number=issue_number, initial_phase="design")
        engine.transition(branch=branch, to_phase="implementation")

        writer.set_context_loaded.assert_called_with(branch, value=False)

    def test_phase_state_engine_resets_flag_on_force_transition(
        self, project: tuple[Path, int]
    ) -> None:
        """writer.set_context_loaded(branch, False) called after successful force_transition()."""
        workspace_root, issue_number = project
        branch = f"feature/{issue_number}-test"
        writer = MagicMock(spec=IContextLoadedWriter)

        engine = make_phase_state_engine(
            workspace_root,
            project_manager=make_project_manager(workspace_root),
            state_repository=InMemoryStateRepository(),
            context_loaded_writer=writer,
        )
        engine.initialize_branch(branch=branch, issue_number=issue_number, initial_phase="design")
        engine.force_transition(
            branch=branch,
            to_phase="validation",
            skip_reason="skipping for test",
            human_approval="test approved on 2026-01-01",
        )

        writer.set_context_loaded.assert_called_with(branch, value=False)

    def test_phase_state_engine_resets_flag_on_enter_cycle(self, project: tuple[Path, int]) -> None:
        """writer.set_context_loaded(branch, False) called after successful transition_cycle()."""
        workspace_root, issue_number = project
        branch = f"feature/{issue_number}-test"
        writer = MagicMock(spec=IContextLoadedWriter)
        repo = InMemoryStateRepository()

        engine = make_phase_state_engine(
            workspace_root,
            project_manager=make_project_manager(workspace_root),
            state_repository=repo,
            context_loaded_writer=writer,
        )
        repo.save(
            BranchState(
                branch=branch,
                issue_number=issue_number,
                workflow_name="feature",
                current_phase="implementation",
                current_cycle=1,
            )
        )
        writer.reset_mock()
        engine.transition_cycle(branch=branch, to_cycle=2)

        writer.set_context_loaded.assert_called_with(branch, value=False)

    def test_phase_state_engine_no_reset_when_writer_none(self, project: tuple[Path, int]) -> None:
        """No AttributeError when context_loaded_writer=None and transition() is called."""
        workspace_root, issue_number = project
        branch = f"feature/{issue_number}-test"

        engine = make_phase_state_engine(
            workspace_root,
            project_manager=make_project_manager(workspace_root),
            state_repository=InMemoryStateRepository(),
            context_loaded_writer=None,
        )
        engine.initialize_branch(branch=branch, issue_number=issue_number, initial_phase="design")
        # Must not raise AttributeError when writer is None
        engine.transition(branch=branch, to_phase="implementation")

    def test_phase_state_engine_resets_flag_on_force_cycle_transition(
        self, project: tuple[Path, int]
    ) -> None:
        """writer.set_context_loaded(branch, False) called after force_cycle_transition().

        Retroactive RED for C5.D2 — force_cycle_transition reset was implemented in C5
        but lacked a dedicated test (QA finding F1, SESSIE_OVERDRACHT_20260520_C5_QA.md).
        """
        workspace_root, issue_number = project
        branch = f"feature/{issue_number}-test"
        writer = MagicMock(spec=IContextLoadedWriter)
        repo = InMemoryStateRepository()

        engine = make_phase_state_engine(
            workspace_root,
            project_manager=make_project_manager(workspace_root),
            state_repository=repo,
            context_loaded_writer=writer,
        )
        repo.save(
            BranchState(
                branch=branch,
                issue_number=issue_number,
                workflow_name="feature",
                current_phase="implementation",
                current_cycle=1,
            )
        )
        writer.reset_mock()
        engine.force_cycle_transition(
            branch=branch,
            to_cycle=2,
            skip_reason="skipping for test",
            human_approval="test approved on 2026-01-01",
        )

        writer.set_context_loaded.assert_called_with(branch, value=False)


class TestPhaseStateFreshSLambdaC1:
    """C1 (#292): PSE write lambdas must derive result from _s, not pre-captured state.

    Each of the 8 _apply_state() callers currently passes ``lambda _s: pre_captured_state``,
    discarding the fresh state loaded under lock. These tests prove the stale-lambda bug by
    giving the mutator a *different* _s than what was loaded before the call and asserting the
    saved result is derived from that fresh _s.

    RED: all four tests fail because the lambda ignores _s.
    GREEN: all four tests pass after migrating callers to ``_s.with_updates()``.
    """

    class _FreshSMutator:
        """Mutator that calls the lambda with a caller-supplied _s.

        Simulates a concurrent write that modified state between the outer
        ``_load_state_or_reconstruct()`` and the lock acquisition inside ``apply()``.
        The lambda receives this fresh _s, which differs from the stale pre-loaded state.
        """

        def __init__(self, repo: InMemoryStateRepository, fresh_s: BranchState) -> None:
            self._repo = repo
            self._fresh_s = fresh_s
            self.results: list[BranchState] = []

        def apply(self, _branch: str, mutate: object) -> None:
            result = mutate(self._fresh_s)  # type: ignore[operator]
            self._repo.save(result)
            self.results.append(result)

    @pytest.fixture()
    def cycle_project(self, tmp_path: Path) -> tuple[Path, int]:
        """Workspace with a cycle-based implementation phase and 2 planned cycles."""
        config_dir = tmp_path / ".phase-gate" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        (config_dir / "contracts.yaml").write_text(
            (
                "merge_policy:\n"
                "  pr_allowed_phase: ready\n"
                "  branch_local_artifacts: []\n"
                "workflows:\n"
                "  bug:\n"
                "    phases:\n"
                "      - name: research\n"
                "        instructions:\n"
                "          sub_role: researcher\n"
                "          phase_instructions: Research.\n"
                "          handover_template: Handover.\n"
                "      - name: implementation\n"
                "        cycle_based: true\n"
                "        subphases: [red, green, refactor]\n"
                "        commit_type_map:\n"
                "          red: test\n"
                "          green: feat\n"
                "          refactor: refactor\n"
                "        instructions:\n"
                "          sub_role: implementer\n"
                "          phase_instructions: Implement.\n"
                "          handover_template: Handover.\n"
                "      - name: ready\n"
                "        instructions:\n"
                "          sub_role: releaser\n"
                "          phase_instructions: Ready.\n"
                "          handover_template: Handover.\n"
            ),
            encoding="utf-8",
        )
        pm = make_project_manager(tmp_path)
        pm.initialize_project(
            issue_number=292, issue_title="Concurrent mutations", workflow_name="bug"
        )
        pm.save_planning_deliverables(
            issue_number=292,
            planning_deliverables={
                "tdd_cycles": {
                    "total": 2,
                    "cycles": [
                        {
                            "cycle_number": 1,
                            "name": "C1",
                            "deliverables": ["D1"],
                            "exit_criteria": "pass",
                        },
                        {
                            "cycle_number": 2,
                            "name": "C2",
                            "deliverables": ["D2"],
                            "exit_criteria": "pass",
                        },
                    ],
                }
            },
        )
        return tmp_path, 292

    # -----------------------------------------------------------------------
    # transition()
    # -----------------------------------------------------------------------

    def test_transition_lambda_uses_s_transitions(self, tmp_path: Path) -> None:
        """transition() lambda appends to _s.transitions, not to pre-captured state.transitions.

        Before fix: ``lambda _s: state.with_updates(transitions=[*state.transitions, new])``
        captures stale list (empty) -> 1 transition saved.
        After fix:  ``lambda _s: _s.with_updates(transitions=[*_s.transitions, new])``
        uses fresh _s (1 concurrent entry) -> 2 transitions saved.
        """
        pm = make_project_manager(tmp_path)
        pm.initialize_project(issue_number=292, issue_title="Test", workflow_name="feature")
        repo = InMemoryStateRepository()
        concurrent_entry = {
            "from_phase": "concurrent",
            "to_phase": "write",
            "timestamp": "2026-01-01T00:00:00+00:00",
            "human_approval": None,
            "forced": False,
            "skip_reason": None,
        }
        seed = BranchState(
            branch="feature/292-test",
            issue_number=292,
            workflow_name="feature",
            current_phase="research",
            transitions=[],
        )
        repo.save(seed)
        # fresh_s has 1 extra transition simulating a concurrent write under lock
        fresh_s = seed.with_updates(transitions=[concurrent_entry])
        mutator = self._FreshSMutator(repo, fresh_s)
        engine = make_phase_state_engine(
            tmp_path,
            project_manager=pm,
            state_repository=repo,
            workflow_state_mutator=mutator,
        )

        engine.transition(branch="feature/292-test", to_phase="design")

        # After fix: 2 transitions (1 from fresh_s + 1 new).
        # Before fix: 1 transition (lambda captures stale transitions=[]).
        assert len(mutator.results) >= 1
        last = mutator.results[-1]
        assert len(last.transitions) == 2, (
            f"Expected 2 transitions (1 concurrent + 1 new), got {len(last.transitions)}. "
            "Lambda must use _s.transitions (fresh under lock), not pre-captured state.transitions."
        )

    # -----------------------------------------------------------------------
    # force_transition()
    # -----------------------------------------------------------------------

    def test_force_transition_lambda_uses_s_transitions(self, tmp_path: Path) -> None:
        """force_transition() lambda appends to _s.transitions, not pre-captured state.transitions.

        Same stale-lambda pattern as transition(); verified independently.
        """
        pm = make_project_manager(tmp_path)
        pm.initialize_project(issue_number=292, issue_title="Test", workflow_name="feature")
        repo = InMemoryStateRepository()
        concurrent_entry = {
            "from_phase": "concurrent",
            "to_phase": "write",
            "timestamp": "2026-01-01T00:00:00+00:00",
            "human_approval": None,
            "forced": False,
            "skip_reason": None,
        }
        seed = BranchState(
            branch="feature/292-test",
            issue_number=292,
            workflow_name="feature",
            current_phase="research",
            transitions=[],
        )
        repo.save(seed)
        fresh_s = seed.with_updates(transitions=[concurrent_entry])
        mutator = self._FreshSMutator(repo, fresh_s)
        engine = make_phase_state_engine(
            tmp_path,
            project_manager=pm,
            state_repository=repo,
            workflow_state_mutator=mutator,
        )

        engine.force_transition(
            branch="feature/292-test",
            to_phase="design",
            skip_reason="force-test",
            human_approval="tester approved on 2026-05-25",
        )

        assert len(mutator.results) >= 1
        last = mutator.results[-1]
        assert len(last.transitions) == 2, (
            f"Expected 2 transitions (1 concurrent + 1 new), got {len(last.transitions)}. "
            "Lambda must use _s.transitions (fresh under lock), not pre-captured state.transitions."
        )

    # -----------------------------------------------------------------------
    # transition_cycle()
    # -----------------------------------------------------------------------

    def test_transition_cycle_lambda_uses_s_cycle_history(
        self, cycle_project: tuple[Path, int]
    ) -> None:
        """transition_cycle() lambda appends to _s.cycle_history, not pre-captured cycle_history.

        Before fix: ``[*state.cycle_history, entry]`` with stale empty list -> 1 history entry.
        After fix:  ``[*_s.cycle_history, entry]`` with fresh list (1 concurrent) -> 2 entries.
        """
        tmp_path, issue_number = cycle_project
        branch = "bug/292-concurrent-state-mutations-lost-updates"
        pm = make_project_manager(tmp_path)
        repo = InMemoryStateRepository()
        concurrent_history = {
            "cycle_number": 0,
            "name": "concurrent",
            "forced": False,
            "entered": "2026-01-01T00:00:00+00:00",
        }
        seed = BranchState(
            branch=branch,
            issue_number=issue_number,
            workflow_name="bug",
            current_phase="implementation",
            current_cycle=None,
            last_cycle=0,
            cycle_history=[],
        )
        repo.save(seed)
        # fresh_s has 1 pre-existing history entry from a concurrent cycle write
        fresh_s = seed.with_updates(cycle_history=[concurrent_history])
        mutator = self._FreshSMutator(repo, fresh_s)
        engine = make_phase_state_engine(
            tmp_path,
            project_manager=pm,
            state_repository=repo,
            workflow_state_mutator=mutator,
        )

        engine.transition_cycle(branch=branch, to_cycle=1)

        # After fix: 2 entries (1 concurrent from fresh_s + 1 new).
        # Before fix: 1 entry (lambda captures stale cycle_history=[]).
        assert len(mutator.results) >= 1
        last = mutator.results[-1]
        assert len(last.cycle_history) == 2, (
            f"Expected 2 cycle_history entries (1 concurrent + 1 new), "
            f"got {len(last.cycle_history)}. "
            "Lambda must use _s.cycle_history (fresh under lock), "
            "not pre-captured state.cycle_history."
        )

    # -----------------------------------------------------------------------
    # force_cycle_transition()
    # -----------------------------------------------------------------------

    def test_force_cycle_transition_lambda_uses_s_cycle_history(
        self, cycle_project: tuple[Path, int]
    ) -> None:
        """force_cycle_transition() lambda appends to _s.cycle_history, not pre-captured.

        Seed has 1 cycle_history entry; fresh_s adds a concurrent extra entry (2 total).
        After fix: appends to fresh_s's 2-entry list -> 3 entries saved.
        Before fix: appends to stale 1-entry list -> only 2 entries saved.
        """
        tmp_path, issue_number = cycle_project
        branch = "bug/292-concurrent-state-mutations-lost-updates"
        pm = make_project_manager(tmp_path)
        repo = InMemoryStateRepository()
        c1_history = {
            "cycle_number": 1,
            "name": "C1",
            "forced": False,
            "entered": "2026-01-01T00:00:00+00:00",
        }
        concurrent_history = {
            "cycle_number": 0,
            "name": "concurrent",
            "forced": False,
            "entered": "2026-01-01T00:01:00+00:00",
        }
        seed = BranchState(
            branch=branch,
            issue_number=issue_number,
            workflow_name="bug",
            current_phase="implementation",
            current_cycle=1,
            last_cycle=0,
            cycle_history=[c1_history],
        )
        repo.save(seed)
        # fresh_s has 2 entries: the concurrent write added one between load and lock
        fresh_s = seed.with_updates(cycle_history=[c1_history, concurrent_history])
        mutator = self._FreshSMutator(repo, fresh_s)
        engine = make_phase_state_engine(
            tmp_path,
            project_manager=pm,
            state_repository=repo,
            workflow_state_mutator=mutator,
        )

        engine.force_cycle_transition(
            branch=branch,
            to_cycle=2,
            skip_reason="force-test",
            human_approval="tester approved on 2026-05-25",
        )

        # After fix: 3 entries (2 from fresh_s + 1 new force-cycle entry).
        # Before fix: 2 entries (1 from stale seed + 1 new force-cycle entry).
        assert len(mutator.results) >= 1
        last = mutator.results[-1]
        assert len(last.cycle_history) == 3, (
            f"Expected 3 cycle_history entries (2 from fresh_s + 1 new), "
            f"got {len(last.cycle_history)}. "
            "Lambda must use _s.cycle_history (fresh under lock), "
            "not pre-captured state.cycle_history."
        )


# C2 RED — _save_state() dead method removal (issue #292)


class TestSaveStateMethodRemoved:
    """C2 (#292): _save_state() must be deleted from PhaseStateEngine.

    C2 removes this dead method. All state writes now go through
    WorkflowStateMutator.apply() or IStateRepository.save() directly.

    RED: test fails because _save_state() still exists.
    GREEN: test passes after _save_state() is deleted from PhaseStateEngine.
    """

    def test_save_state_method_deleted(self) -> None:
        """_save_state() must not exist on PhaseStateEngine (C2-D1)."""
        assert not hasattr(PhaseStateEngine, "_save_state"), (
            "_save_state() still exists on PhaseStateEngine. "
            "C2 removes this dead method — all state writes go through "
            "WorkflowStateMutator.apply() or IStateRepository.save() directly."
        )
