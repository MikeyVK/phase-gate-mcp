"""Behavior contracts for complete registration and coordinated state mutation."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from mcp_server.core.exceptions import StateNotFoundError
from mcp_server.core.interfaces import IWorkflowStateMutator
from mcp_server.managers.state_repository import (
    BranchState,
    InMemoryStateRepository,
    StateAlreadyExistsError,
)
from mcp_server.managers.workflow_state_mutator import (
    StateMutationConflictError,
    WorkflowStateMutator,
)


def registration() -> BranchState:
    """Explicit registration shared only within mutator behavior tests."""
    return BranchState(
        branch="feature/42-work",
        issue_number=42,
        parent_branch="main",
        workflow_name="feature",
        current_phase="research",
    )


def test_initialize_persists_complete_fresh_registration() -> None:
    repository = InMemoryStateRepository()
    mutator = WorkflowStateMutator(repository)
    state = registration()
    mutator.initialize(state)
    assert repository.load(state.branch) == state
    assert isinstance(mutator, IWorkflowStateMutator)


def test_initialize_rejects_same_branch_and_admits_other_branch() -> None:
    repository = InMemoryStateRepository()
    mutator = WorkflowStateMutator(repository)
    previous = registration().with_updates(current_sub_phase="red", skip_reason="Old reason")
    mutator.initialize(previous)
    with pytest.raises(StateAlreadyExistsError):
        mutator.initialize(registration())
    assert repository.load(previous.branch) == previous

    candidate = registration().with_updates(branch="bug/43-next", issue_number=43)
    mutator.initialize(candidate)
    assert repository.load(previous.branch) == candidate
    assert repository.load(candidate.branch) == candidate
    assert candidate.skip_reason is None
    assert candidate.current_sub_phase is None


def test_apply_passes_fresh_state_and_saves_callback_result() -> None:
    repository = InMemoryStateRepository()
    state = registration()
    repository.save(state)
    mutator = WorkflowStateMutator(repository)
    seen: list[BranchState] = []

    def mutate(current: BranchState) -> BranchState:
        seen.append(current)
        return current.with_updates(current_phase="design")

    mutator.apply(state.branch, mutate)
    assert seen == [state]
    assert repository.load(state.branch).current_phase == "design"


@pytest.mark.parametrize(
    "updates",
    [
        {"branch": "feature/43-other"},
        {"issue_number": 43},
        {"parent_branch": "release/next"},
    ],
)
def test_apply_preserves_registration_identity(updates: dict[str, object]) -> None:
    repository = InMemoryStateRepository()
    state = registration()
    repository.save(state)
    mutator = WorkflowStateMutator(repository)
    with pytest.raises(StateMutationConflictError):
        mutator.apply(state.branch, lambda current: current.with_updates(**updates))
    assert repository.load(state.branch) == state
    mutator.apply(state.branch, lambda current: current.with_updates(current_phase="design"))
    assert repository.load(state.branch).current_phase == "design"


def test_apply_requires_existing_registration_without_calling_callback() -> None:
    repository = InMemoryStateRepository()
    mutator = WorkflowStateMutator(repository)
    called: list[BranchState] = []

    def mutate(current: BranchState) -> BranchState:
        called.append(current)
        return current

    with pytest.raises(StateNotFoundError):
        mutator.apply("feature/42-work", mutate)
    assert called == []
    with pytest.raises(StateNotFoundError):
        repository.load("feature/42-work")


def test_failed_callback_preserves_state_and_releases_lock() -> None:
    repository = InMemoryStateRepository()
    state = registration()
    repository.save(state)
    mutator = WorkflowStateMutator(repository)
    failure = OSError("callback failed")

    def mutate(_current: BranchState) -> BranchState:
        raise failure

    with pytest.raises(OSError) as rejected:
        mutator.apply(state.branch, mutate)
    assert rejected.value is failure
    assert repository.load(state.branch) == state
    mutator.apply(state.branch, lambda current: current.with_updates(current_phase="design"))
    assert repository.load(state.branch).current_phase == "design"


def test_invalid_complete_candidate_is_not_saved() -> None:
    repository = InMemoryStateRepository()
    state = registration()
    repository.save(state)
    mutator = WorkflowStateMutator(repository)
    invalid = BranchState.model_construct(**{**state.model_dump(), "parent_branch": " "})
    with pytest.raises(ValidationError):
        mutator.apply(state.branch, lambda _current: invalid)
    assert repository.load(state.branch) == state
    with pytest.raises(ValidationError):
        repository.save(invalid)
    assert repository.load(state.branch) == state


def test_conflict_retains_diagnostic_and_recovery_facts() -> None:
    error = StateMutationConflictError("lock conflict", "retry operation")
    assert str(error) == error.diagnostic == "lock conflict"
    assert error.recovery == "retry operation"
