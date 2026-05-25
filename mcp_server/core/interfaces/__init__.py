# mcp_server\core\interfaces\__init__.py
# template=generic version=f35abd82 created=2026-03-12T15:02Z updated=
"""Protocol interfaces for workflow state, gate orchestration, PR status, and test execution."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from mcp_server.managers.pytest_runner import PytestResult
    from mcp_server.managers.state_repository import BranchState
    from mcp_server.state.quality_state import QualityState


class PRStatus(Enum):
    """Lifecycle status of the PR on the current branch."""

    OPEN = "open"
    ABSENT = "absent"


@runtime_checkable
class IPRStatusReader(Protocol):
    """Read the cached PR status for a branch."""

    def get_pr_status(self, branch: str) -> PRStatus:
        raise NotImplementedError


@runtime_checkable
class IPRStatusWriter(Protocol):
    """Write the PR status for a branch into the cache."""

    def set_pr_status(self, branch: str, status: PRStatus) -> None:
        raise NotImplementedError


@runtime_checkable
class IPytestRunner(Protocol):
    """Run a pytest invocation and return a structured PytestResult."""

    def run(self, cmd: list[str], cwd: str, timeout: int) -> PytestResult:
        raise NotImplementedError


@dataclass(frozen=True)
class GateReport:
    """Result of one gate evaluation pass."""

    passing: tuple[str, ...] = ()
    blocking: tuple[str, ...] = ()
    details: dict[str, str] = field(default_factory=dict)


class GateViolation(ValueError):  # noqa: N818 - domain event name, not a technical error type
    """Raised when enforce mode encounters a blocking gate."""

    def __init__(self, message: str, report: GateReport) -> None:
        super().__init__(message)
        self.report = report


class IStateReader(Protocol):
    """Read-only access to persisted branch state."""

    def load(self, branch: str) -> BranchState:
        raise NotImplementedError


class IStateRepository(IStateReader, Protocol):
    """Read-write access to persisted branch state."""

    def save(self, state: BranchState) -> None:
        raise NotImplementedError


class IStateReconstructor(Protocol):
    """Reconstruct missing or invalid branch state for one branch."""

    def reconstruct(self, branch: str) -> BranchState:
        raise NotImplementedError


class IWorkflowGateRunner(Protocol):
    """Evaluate resolved workflow gate checks via phase or cycle boundary methods."""

    def enforce_phase_exit(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int | None = None,
    ) -> GateReport:
        raise NotImplementedError

    def inspect_phase_exit(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int | None = None,
    ) -> GateReport:
        raise NotImplementedError

    def enforce_cycle_exit(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int,
    ) -> GateReport:
        raise NotImplementedError

    def inspect_cycle_exit(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int,
    ) -> GateReport:
        raise NotImplementedError

    def is_cycle_based_phase(self, workflow_name: str, phase: str) -> bool:
        raise NotImplementedError


@runtime_checkable
class IGitContextReader(Protocol):
    """Read-only git context for the current branch."""

    def get_current_branch(self) -> str:
        raise NotImplementedError

    def get_recent_commits(self, limit: int = 5) -> list[str]:
        raise NotImplementedError


@runtime_checkable
class IQualityStateRepository(Protocol):
    """Read/apply access to persisted quality-gate baseline state."""

    def load(self) -> QualityState:
        """Return current QualityState; default-construct when absent."""
        raise NotImplementedError

    def apply(self, mutate: Callable[[QualityState], QualityState]) -> None:
        """Read current state, apply mutate, and persist atomically."""
        raise NotImplementedError


@runtime_checkable
class IWorkflowStateMutator(Protocol):
    """Command-side seam for coordinated workflow state writes.

    All workflow state mutations must route through this interface so that
    concurrent write paths share one coordinated lock boundary.
    """

    def apply(
        self,
        branch: str,
        mutate: Callable[[BranchState], BranchState],
    ) -> None:
        """Apply *mutate* to the current BranchState for *branch* atomically.

        Raises:
            StateMutationConflictError: on lock timeout, branch mismatch, or
                unrecoverable state.
        """
        raise NotImplementedError


@runtime_checkable
class IContextLoadedReader(Protocol):
    """Read whether get_work_context has been called for a branch this session."""

    def is_context_loaded(self, branch: str) -> bool:
        raise NotImplementedError


@runtime_checkable
class IContextLoadedWriter(Protocol):
    """Record that get_work_context has been called for a branch this session."""

    def set_context_loaded(self, branch: str, *, value: bool) -> None:
        raise NotImplementedError
