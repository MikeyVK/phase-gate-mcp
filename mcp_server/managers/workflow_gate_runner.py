# mcp_server/managers/workflow_gate_runner.py
"""Workflow gate orchestration for phase and cycle boundaries.

@layer: Platform
@dependencies: [DeliverableChecker, PhaseContractResolver]
@responsibilities:
    - Resolve workflow and cycle gate checks from config
    - Execute checks through DeliverableChecker
    - Expose phase-exit and cycle-exit boundary methods
    - Report whether a workflow phase is cycle_based
"""

from __future__ import annotations

# Project modules
from mcp_server.core.interfaces import GateReport, GateViolation
from mcp_server.managers.deliverable_checker import (
    DeliverableChecker,
    DeliverableCheckError,
)
from mcp_server.managers.phase_contract_resolver import PhaseContractResolver
from mcp_server.schemas import CheckSpec


class WorkflowGateRunner:
    """Execute resolved gate checks through DeliverableChecker."""

    def __init__(
        self,
        deliverable_checker: DeliverableChecker,
        phase_contract_resolver: PhaseContractResolver,
    ) -> None:
        self._deliverable_checker = deliverable_checker
        self._phase_contract_resolver = phase_contract_resolver

    def is_cycle_based_phase(self, workflow_name: str, phase: str) -> bool:
        """Report whether one workflow phase supports TDD cycle transitions."""
        return self._phase_contract_resolver.is_cycle_based_phase(workflow_name, phase)

    def enforce_phase_exit(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int | None = None,
    ) -> GateReport:
        """Run blocking gate evaluation for a phase exit and raise with the full report."""
        checks = self._phase_contract_resolver.resolve_phase_exit(
            workflow_name, phase, cycle_number
        )
        return self._run_resolved_checks(checks, raise_on_block=True)

    def inspect_phase_exit(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int | None = None,
    ) -> GateReport:
        """Run non-blocking gate inspection for a phase exit and return all blocked checks."""
        checks = self._phase_contract_resolver.resolve_phase_exit(
            workflow_name, phase, cycle_number
        )
        return self._run_resolved_checks(checks, raise_on_block=False)

    def enforce_cycle_exit(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int,
    ) -> GateReport:
        """Run blocking gate evaluation for a cycle exit and raise with the full report."""
        checks = self._phase_contract_resolver.resolve_cycle_exit(
            workflow_name, phase, cycle_number
        )
        return self._run_resolved_checks(checks, raise_on_block=True)

    def inspect_cycle_exit(
        self,
        workflow_name: str,
        phase: str,
        cycle_number: int,
    ) -> GateReport:
        """Run non-blocking gate inspection for a cycle exit and return all blocked checks."""
        checks = self._phase_contract_resolver.resolve_cycle_exit(
            workflow_name, phase, cycle_number
        )
        return self._run_resolved_checks(checks, raise_on_block=False)

    def _run_resolved_checks(
        self,
        resolved_checks: list[CheckSpec],
        raise_on_block: bool,
    ) -> GateReport:
        passing: list[str] = []
        blocking: list[str] = []
        details: dict[str, str] = {}

        for spec in resolved_checks:
            payload = spec.model_dump(exclude_none=True)
            try:
                self._deliverable_checker.check(spec.id, payload)
            except DeliverableCheckError as exc:
                blocking.append(spec.id)
                details[spec.id] = str(exc)
            else:
                passing.append(spec.id)

        report = GateReport(
            passing=tuple(passing),
            blocking=tuple(blocking),
            details=details,
        )
        if raise_on_block and blocking:
            first_blocking = blocking[0]
            raise GateViolation(details[first_blocking], report)
        return report
