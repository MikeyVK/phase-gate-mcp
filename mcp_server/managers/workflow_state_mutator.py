# mcp_server/managers/workflow_state_mutator.py
"""Coordinate initialization and ordinary updates through one in-process state lock."""

from __future__ import annotations

import threading
from collections.abc import Callable
from typing import TYPE_CHECKING

from mcp_server.core.exceptions import StateNotFoundError
from mcp_server.managers.state_repository import (
    BranchState,
    StateAlreadyExistsError,
    StateBranchMismatchError,
)

if TYPE_CHECKING:
    from mcp_server.core.interfaces import IStateRepository

_LOCK_TIMEOUT_SECONDS: float = 5.0


class StateMutationConflictError(Exception):
    """A coordinated state mutation cannot safely complete."""

    def __init__(self, diagnostic: str, recovery: str) -> None:
        super().__init__(diagnostic)
        self.diagnostic = diagnostic
        self.recovery = recovery


class WorkflowStateMutator:
    """Own locked complete initialization and fresh read-mutate-validate-save."""

    def __init__(self, state_repository: IStateRepository) -> None:
        self._state_repository = state_repository
        self._lock = threading.Lock()

    def initialize(self, state: BranchState) -> None:
        """Admit absence or valid other-branch handover and save complete new state."""
        candidate = BranchState.model_validate(state.model_dump())
        self._acquire_lock(candidate.branch)
        try:
            try:
                current = self._state_repository.load(candidate.branch)
            except StateNotFoundError:
                current = None
            if current is not None and current.branch == candidate.branch:
                raise StateAlreadyExistsError(
                    f"Branch '{candidate.branch}' already has an initialized state "
                    f"(phase: {current.current_phase}). "
                    "Call initialize_project only once per branch."
                )
            self._state_repository.save(candidate)
        finally:
            self._lock.release()

    def apply(
        self,
        branch: str,
        mutate: Callable[[BranchState], BranchState],
    ) -> None:
        """Mutate existing matching state without changing its registration identity."""
        self._acquire_lock(branch)
        try:
            state = self._state_repository.load(branch)
            if state.branch != branch:
                raise StateBranchMismatchError(
                    f"Loaded state branch '{state.branch}' "
                    f"does not match requested branch '{branch}'"
                )
            updated = mutate(state)
            candidate = BranchState.model_validate(updated.model_dump())
            if (
                candidate.branch != state.branch
                or candidate.issue_number != state.issue_number
                or candidate.parent_branch != state.parent_branch
            ):
                raise StateMutationConflictError(
                    f"Mutation changed registration identity for branch '{branch}'.",
                    "Preserve the registered branch, issue_number and parent_branch.",
                )
            self._state_repository.save(candidate)
        finally:
            self._lock.release()

    def _acquire_lock(self, branch: str) -> None:
        """Apply the existing bounded wait to both command paths."""
        if not self._lock.acquire(timeout=_LOCK_TIMEOUT_SECONDS):
            raise StateMutationConflictError(
                f"Lock timeout acquiring mutation lock for branch '{branch}'.",
                (
                    "Another operation is holding the workflow state lock. "
                    "Retry after the current operation completes."
                ),
            )
