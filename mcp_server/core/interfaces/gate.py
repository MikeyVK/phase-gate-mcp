# c:\temp\pgmcp\mcp_server\core\interfaces\gate.py
# template=interface version=3fb28c28 created=2026-06-20T18:27Z updated=
"""IWorkflowGateRunner module.

Evaluate resolved workflow gate checks via phase or cycle boundary methods.

@layer: Backend (Contracts)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


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
