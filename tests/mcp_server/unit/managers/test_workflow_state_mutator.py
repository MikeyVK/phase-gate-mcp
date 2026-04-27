# tests/mcp_server/unit/managers/test_workflow_state_mutator.py
"""C6 (C_MUTATOR_CORE): IWorkflowStateMutator protocol and WorkflowStateMutator implementation.

Tests verify:
- IWorkflowStateMutator protocol exists in mcp_server.core.interfaces
- StateMutationConflictError exists with diagnostic and recovery fields
- WorkflowStateMutator implements IWorkflowStateMutator
- WorkflowStateMutator.apply() acquires lock, loads fresh state, calls mutate, saves
- WorkflowStateMutator.apply() raises StateMutationConflictError on branch mismatch
- server.py wires WorkflowStateMutator into PhaseStateEngine

@layer: Tests (Unit)
@dependencies: pathlib, mcp_server.core.interfaces, mcp_server.managers.workflow_state_mutator
"""
# pyright: reportPrivateUsage=false

from __future__ import annotations

import inspect
from pathlib import Path

from mcp_server.managers.state_repository import BranchState, InMemoryStateRepository


class TestIWorkflowStateMutatorProtocol:
    """C6: IWorkflowStateMutator protocol is defined in mcp_server.core.interfaces."""

    def test_iworkflow_state_mutator_importable(self) -> None:
        """IWorkflowStateMutator is importable from mcp_server.core.interfaces."""
        from mcp_server.core.interfaces import IWorkflowStateMutator  # noqa: PLC0415

        assert IWorkflowStateMutator is not None

    def test_iworkflow_state_mutator_has_apply_method(self) -> None:
        """IWorkflowStateMutator protocol declares apply(branch, mutate) -> None."""
        from mcp_server.core.interfaces import IWorkflowStateMutator  # noqa: PLC0415

        assert hasattr(IWorkflowStateMutator, "apply")

    def test_iworkflow_state_mutator_is_runtime_checkable(self) -> None:
        """IWorkflowStateMutator supports isinstance() checks."""
        from mcp_server.managers.workflow_state_mutator import WorkflowStateMutator  # noqa: PLC0415

        from mcp_server.core.interfaces import IWorkflowStateMutator  # noqa: PLC0415

        repo = InMemoryStateRepository()
        mutator = WorkflowStateMutator(state_repository=repo)
        assert isinstance(mutator, IWorkflowStateMutator)


class TestStateMutationConflictError:
    """C6: StateMutationConflictError is defined with diagnostic and recovery fields."""

    def test_state_mutation_conflict_error_importable(self) -> None:
        """StateMutationConflictError is importable from workflow_state_mutator."""
        from mcp_server.managers.workflow_state_mutator import (  # noqa: PLC0415
            StateMutationConflictError,
        )

        assert StateMutationConflictError is not None

    def test_state_mutation_conflict_error_is_exception(self) -> None:
        """StateMutationConflictError inherits from Exception."""
        from mcp_server.managers.workflow_state_mutator import (  # noqa: PLC0415
            StateMutationConflictError,
        )

        assert issubclass(StateMutationConflictError, Exception)

    def test_state_mutation_conflict_error_has_diagnostic(self) -> None:
        """StateMutationConflictError instances expose a diagnostic attribute."""
        from mcp_server.managers.workflow_state_mutator import (  # noqa: PLC0415
            StateMutationConflictError,
        )

        err = StateMutationConflictError(
            diagnostic="lock timeout on branch X",
            recovery="retry after 5s",
        )
        assert err.diagnostic == "lock timeout on branch X"

    def test_state_mutation_conflict_error_has_recovery(self) -> None:
        """StateMutationConflictError instances expose a recovery attribute."""
        from mcp_server.managers.workflow_state_mutator import (  # noqa: PLC0415
            StateMutationConflictError,
        )

        err = StateMutationConflictError(
            diagnostic="unrecoverable state",
            recovery="reinitialize branch",
        )
        assert err.recovery == "reinitialize branch"

    def test_state_mutation_conflict_error_message_is_diagnostic(self) -> None:
        """str(error) contains the diagnostic message."""
        from mcp_server.managers.workflow_state_mutator import (  # noqa: PLC0415
            StateMutationConflictError,
        )

        err = StateMutationConflictError(diagnostic="diag msg", recovery="rec msg")
        assert "diag msg" in str(err)


class TestWorkflowStateMutatorApply:
    """C6: WorkflowStateMutator.apply() coordinates state reads and writes atomically."""

    def test_apply_saves_mutated_state(self) -> None:
        """apply() persists the return value of the mutate callback."""
        from mcp_server.managers.workflow_state_mutator import WorkflowStateMutator  # noqa: PLC0415

        repo = InMemoryStateRepository()
        state = BranchState(
            branch="feature/x",
            workflow_name="feature",
            current_phase="research",
        )
        repo.save(state)

        mutator = WorkflowStateMutator(state_repository=repo)
        mutator.apply("feature/x", lambda s: s.with_updates(current_phase="design"))

        saved = repo.load("feature/x")
        assert saved.current_phase == "design"

    def test_apply_passes_current_state_to_callback(self) -> None:
        """apply() passes the currently persisted state to the mutate callback."""
        from mcp_server.managers.workflow_state_mutator import WorkflowStateMutator  # noqa: PLC0415

        repo = InMemoryStateRepository()
        state = BranchState(
            branch="feature/x",
            workflow_name="feature",
            current_phase="planning",
        )
        repo.save(state)

        seen: list[BranchState] = []

        def capture(s: BranchState) -> BranchState:
            seen.append(s)
            return s

        mutator = WorkflowStateMutator(state_repository=repo)
        mutator.apply("feature/x", capture)

        assert len(seen) == 1
        assert seen[0].current_phase == "planning"

    def test_apply_raises_on_branch_mismatch(self) -> None:
        """apply() raises StateMutationConflictError when mutate returns wrong branch."""
        import pytest  # noqa: PLC0415
        from mcp_server.managers.workflow_state_mutator import (  # noqa: PLC0415
            StateMutationConflictError,
            WorkflowStateMutator,
        )

        repo = InMemoryStateRepository()
        state = BranchState(
            branch="feature/x",
            workflow_name="feature",
            current_phase="research",
        )
        repo.save(state)

        # Callback returns state with wrong branch identity
        def bad_mutate(s: BranchState) -> BranchState:
            return s.with_updates(branch="feature/y")

        mutator = WorkflowStateMutator(state_repository=repo)
        with pytest.raises(StateMutationConflictError):
            mutator.apply("feature/x", bad_mutate)

    def test_apply_supports_bootstrap_when_no_prior_state(self, tmp_path: Path) -> None:
        """apply() succeeds on fresh branch (no prior state) for initialize_branch use case."""
        from mcp_server.managers.workflow_state_mutator import WorkflowStateMutator  # noqa: PLC0415

        repo = InMemoryStateRepository()
        fresh_state = BranchState(
            branch="feature/new",
            workflow_name="feature",
            current_phase="research",
            issue_number=42,
        )

        mutator = WorkflowStateMutator(state_repository=repo)
        # Callback ignores existing state (there is none) and creates a fresh one
        mutator.apply("feature/new", lambda _s: fresh_state)

        saved = repo.load("feature/new")
        assert saved.current_phase == "research"
        assert saved.issue_number == 42

    def test_apply_uses_atomic_lock_source_check(self) -> None:
        """WorkflowStateMutator uses a threading lock for coordinated mutation (source check)."""
        import mcp_server.managers.workflow_state_mutator as _mod  # noqa: PLC0415

        source = inspect.getsource(_mod)
        assert "Lock" in source or "lock" in source.lower(), (
            "WorkflowStateMutator must use a threading lock for coordination"
        )


class TestServerMutatorWiringC6:
    """C6: mcp_server/server.py wires WorkflowStateMutator."""

    def test_server_imports_workflow_state_mutator(self) -> None:
        """server.py imports or references WorkflowStateMutator (source check)."""
        import mcp_server.server as _srv  # noqa: PLC0415

        source = inspect.getsource(_srv)
        assert "WorkflowStateMutator" in source, (
            "mcp_server/server.py must wire WorkflowStateMutator into PhaseStateEngine"
        )
