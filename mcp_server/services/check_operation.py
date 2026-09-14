"""Compose check selection and execution without changing native result meaning."""

from __future__ import annotations

from typing import Literal

from mcp_server.core.interfaces.git import BranchBasisUnavailableError
from mcp_server.execution.check_selection import (
    CheckScopeError,
    CheckSelectionError,
    CheckSelectionFailureReason,
    CheckSelectionRequest,
    CheckSelector,
)
from mcp_server.execution.check_service import CheckExecution, CheckService
from mcp_server.execution.models import (
    AdapterCallFailureReason,
    AdapterRunIdentity,
    AdapterUnavailableReason,
    CheckedCoverage,
    CheckFailed,
    CheckNotExecuted,
    CheckUnavailable,
    ConsumerNotExecutedReason,
    ExternalToolIdentity,
    InvalidCheckRequest,
    InvocationCancelled,
    InvocationFailed,
    NativeEvidence,
    RequestValidationIssue,
    ScopeDetails,
    ScopeIssue,
    SelectionCheckResponse,
)
from mcp_server.schemas.execution_outputs import (
    BranchBasisDetails,
    CheckSelectionDetails,
    RunChecksErrorCode,
    RunChecksOutput,
    SelectionCheckResult,
    UnknownCheckIssue,
    UnknownProfileIssue,
    UnselectedCheckArgsIssue,
    UnsupportedSelectionIssue,
)
from mcp_server.schemas.mutation_outputs import RejectedRequestDetails, TerminationDetails


def project_selection_check(row: CheckExecution[SelectionCheckResponse]) -> SelectionCheckResult:
    """Transfer attempted and unstarted facts without inventing native outcomes."""
    status: Literal["passed", "failed", "unavailable", "not_executed"] = "not_executed"
    reason: (
        AdapterUnavailableReason
        | AdapterCallFailureReason
        | ConsumerNotExecutedReason
        | Literal["scope_restricted", "not_applicable"]
        | None
    ) = "not_started"
    message: str | None = "Check was not started because the operation stopped."
    evidence: NativeEvidence | None = None
    external: tuple[ExternalToolIdentity, ...] | None = None
    coverage: CheckedCoverage | None = None
    required: tuple[str, ...] = ()
    rejection: tuple[RequestValidationIssue, ...] | None = None
    adapter = None
    capture = None
    termination = None
    observed = row.invocation
    if observed is not None:
        if row.binding.contract_version != 1:
            raise ValueError("selection_check_contract_version_invalid")
        adapter = AdapterRunIdentity(
            adapter_id=row.binding.identity.adapter_id,
            version=row.binding.identity.version,
            fingerprint=row.binding.identity.fingerprint,
            contract_version=1,
        )
        capture = observed.capture
        if isinstance(observed, InvocationFailed):
            status, reason, message = (
                "unavailable",
                observed.failure.reason,
                observed.failure.message,
            )
            termination = observed.termination_problem
        elif isinstance(observed, InvocationCancelled):
            reason, message = "interrupted", "Check execution was interrupted."
            termination = observed.termination_problem
        else:
            response = observed.response.root
            if isinstance(response, InvalidCheckRequest):
                reason, message, rejection = "invalid_request", None, response.details
            else:
                decision = response.decision
                status = decision.status
                reason = (
                    decision.reason
                    if isinstance(decision, (CheckUnavailable, CheckNotExecuted))
                    else None
                )
                message = (
                    decision.message
                    if isinstance(decision, (CheckFailed, CheckUnavailable, CheckNotExecuted))
                    else None
                )
                evidence, external = response.evidence, response.external_tools
                coverage, required = response.coverage, response.required_targets
    return SelectionCheckResult(
        check_id=row.check_id,
        status=status,
        reason=reason,
        message=message,
        evidence=evidence,
        external_tools=external,
        adapter=adapter,
        capture=capture,
        termination_problem=termination,
        request_rejection=rejection,
        args_source=row.args_source,
        effective_args=row.effective_args,
        coverage=coverage,
        required_targets=required,
    )


class CheckOperation:
    """Own selection-result projection while the shared executor retains execution facts."""

    def __init__(self, *, selector: CheckSelector, executor: CheckService) -> None:
        self._selector = selector
        self._executor = executor

    async def execute(self, request: CheckSelectionRequest) -> RunChecksOutput:
        """Resolve once, execute once, and preserve expected operation refusals."""
        error_code: RunChecksErrorCode | None = None
        error_details: (
            CheckSelectionDetails
            | BranchBasisDetails
            | ScopeDetails
            | RejectedRequestDetails
            | TerminationDetails
            | None
        ) = None
        try:
            plan = self._selector.select(request)
        except CheckScopeError as exc:
            error_code = "scope_resolution_failed"
            error_details = ScopeDetails(
                issues=(
                    ScopeIssue(
                        target=exc.target,
                        reason=exc.scope_reason,
                        message=exc.message,
                    ),
                )
            )
        except BranchBasisUnavailableError as exc:
            error_code = "branch_basis_unavailable"
            error_details = BranchBasisDetails(reason=exc.reason, message=exc.message)
        except CheckSelectionError as exc:
            if exc.reason is CheckSelectionFailureReason.NO_CONFIGURED_CHECKS:
                error_code = "no_configured_checks"
            elif exc.reason is CheckSelectionFailureReason.DEFAULT_PROFILE_MISSING:
                error_code = "default_profile_missing"
            else:
                if exc.selection_id is None:
                    raise
                issue: (
                    UnknownProfileIssue
                    | UnknownCheckIssue
                    | UnselectedCheckArgsIssue
                    | UnsupportedSelectionIssue
                )
                if exc.reason is CheckSelectionFailureReason.UNKNOWN_PROFILE:
                    issue = UnknownProfileIssue(
                        reason="unknown_profile", profile_id=exc.selection_id
                    )
                elif exc.reason is CheckSelectionFailureReason.UNKNOWN_CHECK:
                    issue = UnknownCheckIssue(reason="unknown_check", check_id=exc.selection_id)
                elif exc.reason is CheckSelectionFailureReason.UNSELECTED_ARGS:
                    issue = UnselectedCheckArgsIssue(
                        reason="unselected_args", check_id=exc.selection_id
                    )
                elif exc.reason is CheckSelectionFailureReason.SELECTION_UNSUPPORTED:
                    issue = UnsupportedSelectionIssue(
                        reason="selection_unsupported",
                        check_id=exc.selection_id,
                    )
                else:
                    raise
                error_code = "selection_invalid"
                error_details = CheckSelectionDetails(issues=(issue,))
        else:
            execution = await self._executor.run_selection(plan)
            results = tuple(project_selection_check(row) for row in execution.results)
            error_code = execution.stop_reason
            if error_code == "adapter_request_rejected":
                rejected = next(row for row in results if row.request_rejection is not None)
                error_details = RejectedRequestDetails(check_id=rejected.check_id)
            elif error_code == "termination_unconfirmed":
                error_details = TerminationDetails(
                    check_ids=tuple(row.check_id for row in results if row.termination_problem),
                    interrupted=any(row.reason == "interrupted" for row in results),
                )
            return RunChecksOutput(
                success=error_code != "adapter_request_rejected",
                run_status=execution.run_status,
                requested_scope=request.scope,
                requested_targets=request.targets or (),
                selected_profile=plan.selected_profile,
                removed_targets=execution.scope.removed_targets,
                results=results,
                error_code=error_code,
                error_details=error_details,
            )
        return RunChecksOutput(
            success=True,
            run_status=None,
            requested_scope=request.scope,
            requested_targets=request.targets or (),
            selected_profile=None,
            removed_targets=(),
            results=(),
            error_code=error_code,
            error_details=error_details,
        )
