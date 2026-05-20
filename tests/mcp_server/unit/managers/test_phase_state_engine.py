"""Tests for PhaseStateEngine implementation-phase lifecycle hooks.

Issue #146 Cycle 4: TDD phase lifecycle hooks.

@layer: Tests (Unit)
@dependencies: pytest, tests.mcp_server.test_support, mcp_server.managers.phase_state_engine
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from mcp_server.core.interfaces import IContextLoadedWriter
from mcp_server.managers.state_repository import (
    BranchState,
    InMemoryStateRepository,
    StateBranchMismatchError,
)
from tests.mcp_server.test_support import make_phase_state_engine, make_project_manager


class TestTDDPhaseHooks:
    """Tests for TDD phase entry/exit hooks.

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
        """Test that entering TDD phase auto-initializes cycle 1."""
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
        """Test that entering TDD phase does NOT block on missing planning deliverables.

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
        """Test that exiting TDD phase preserves last_cycle."""
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

        # Initialize in TDD phase at cycle 3
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
        assert state.current_cycle is None

    def test_on_exit_implementation_phase_validates_completion(
        self, setup_project: tuple[Path, int]
    ) -> None:
        """Test that exiting TDD phase validates all cycles completed."""
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

        # Initialize in TDD phase at cycle 2 (not completed)
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
        assert state.current_cycle is None


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
                "      - name: implementation\n"
                "        cycle_based: true\n"
                "        subphases: [red, green, refactor]\n"
                "        commit_type_map:\n"
                "          red: test\n"
                "          green: feat\n"
                "          refactor: refactor\n"
                "      - name: validation\n"
                "      - name: ready\n"
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
        """Test that transition() to 'tdd' auto-calls on_enter_implementation_phase (Issue #146)."""
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

        # Verify no TDD cycle before transition
        state = state_engine.get_state(branch)
        assert state.current_cycle is None

        # Transition to TDD - should auto-call on_enter_implementation_phase
        state_engine.transition(branch=branch, to_phase="implementation")

        # Assert: hook was triggered and cycle 1 was initialized
        state = state_engine.get_state(branch)
        assert state.current_cycle == 1, (
            "on_enter_implementation_phase was not called by transition() - "
            "current_cycle should be 1 after entering TDD phase"
        )

    def test_transition_from_tdd_calls_exit_hook(self, setup_project: tuple[Path, int]) -> None:
        """Test that transition() from 'tdd' auto-calls on_exit_implementation_phase."""
        workspace_root, issue_number = setup_project
        branch = "feature/999-hook-wiring"

        project_manager = make_project_manager(workspace_root)
        state_repository = InMemoryStateRepository()
        state_engine = make_phase_state_engine(
            workspace_root,
            project_manager=project_manager,
            state_repository=state_repository,
        )

        # Initialize branch in TDD phase at cycle 2
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
            "last_cycle should be 2 after exiting TDD phase"
        )
        assert state.current_cycle is None, "current_cycle should be None after exiting TDD phase"


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
        "      - name: implementation\n"
        "        cycle_based: true\n"
        "        subphases: [red, green, refactor]\n"
        "        commit_type_map:\n"
        "          red: test\n"
        "          green: feat\n"
        "          refactor: refactor\n"
        "      - name: validation\n"
        "      - name: ready\n"
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
