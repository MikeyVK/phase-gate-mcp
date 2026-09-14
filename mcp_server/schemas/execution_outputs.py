"""Strict public run-check result contracts and selection projections."""

from __future__ import annotations

from typing import Annotated, Literal, Self, get_args

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr, model_validator

from mcp_server.config.schemas.checks_config import CheckId, ProfileId
from mcp_server.execution.check_selection import (
    ArgsSource,
    CheckScope,
    WorkspaceRelativePath,
)
from mcp_server.execution.models import (
    AdapterCallFailureReason,
    AdapterRunIdentity,
    AdapterUnavailableReason,
    CheckedCoverage,
    ConsumerNotExecutedReason,
    ExternalToolIdentity,
    JsonEvidence,
    NativeEvidence,
    NonBlankText,
    ProcessCapture,
    RequestValidationIssue,
    ScopeDetails,
    TerminationProblem,
    TextEvidence,
)
from mcp_server.schemas.mutation_outputs import RejectedRequestDetails, TerminationDetails


class _ExecutionOutputModel(BaseModel):
    """Frozen strict base for role-owned execution output facts."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")


class UnknownProfileIssue(_ExecutionOutputModel):
    reason: Literal["unknown_profile"]
    profile_id: ProfileId


class UnknownCheckIssue(_ExecutionOutputModel):
    reason: Literal["unknown_check"]
    check_id: CheckId


class UnselectedCheckArgsIssue(_ExecutionOutputModel):
    reason: Literal["unselected_args"]
    check_id: CheckId


class UnsupportedSelectionIssue(_ExecutionOutputModel):
    reason: Literal["selection_unsupported"]
    check_id: CheckId


CheckSelectionIssue = Annotated[
    UnknownProfileIssue | UnknownCheckIssue | UnselectedCheckArgsIssue | UnsupportedSelectionIssue,
    Field(discriminator="reason"),
]


class CheckSelectionDetails(_ExecutionOutputModel):
    issues: Annotated[tuple[CheckSelectionIssue, ...], Field(min_length=1)]


class BranchBasisDetails(_ExecutionOutputModel):
    reason: Literal["parent_unavailable", "merge_base_unavailable"]
    message: NonBlankText


RunChecksErrorCode = Literal[
    "no_configured_checks",
    "selection_invalid",
    "default_profile_missing",
    "branch_basis_unavailable",
    "scope_resolution_failed",
    "adapter_request_rejected",
    "operation_interrupted",
    "termination_unconfirmed",
]

SelectionResultReason = (
    AdapterUnavailableReason
    | AdapterCallFailureReason
    | ConsumerNotExecutedReason
    | Literal["scope_restricted", "not_applicable"]
    | None
)


class SelectionCheckResult(_ExecutionOutputModel):
    """One selected check's factual native or lifecycle result."""

    check_id: CheckId
    status: Literal["passed", "failed", "unavailable", "not_executed"]
    reason: SelectionResultReason
    message: NonBlankText | None
    evidence: NativeEvidence | None
    external_tools: tuple[ExternalToolIdentity, ...] | None
    adapter: AdapterRunIdentity | None
    capture: ProcessCapture | None
    termination_problem: TerminationProblem | None
    request_rejection: Annotated[tuple[RequestValidationIssue, ...], Field(min_length=1)] | None
    args_source: ArgsSource
    effective_args: tuple[StrictStr, ...]
    coverage: CheckedCoverage | None
    required_targets: tuple[WorkspaceRelativePath, ...]

    @model_validator(mode="after")
    def validate_observation(self) -> Self:
        attempted = self.adapter is not None or self.capture is not None
        if (self.adapter is None) != (self.capture is None):
            raise ValueError("attempt_identity_and_capture_must_agree")

        if self.status == "not_executed":
            if self.reason not in {
                "not_started",
                "interrupted",
                "invalid_request",
                "scope_restricted",
                "not_applicable",
            }:
                raise ValueError("invalid_selection_not_executed_reason")
            if self.reason == "invalid_request":
                if (
                    not attempted
                    or self.message is not None
                    or self.evidence is not None
                    or self.external_tools is not None
                    or self.request_rejection is None
                    or self.coverage is not None
                    or self.required_targets
                    or self.termination_problem is not None
                ):
                    raise ValueError("invalid_request_selection_facts_invalid")
            elif self.reason in {"scope_restricted", "not_applicable"}:
                if (
                    not attempted
                    or self.message is None
                    or self.request_rejection is not None
                    or self.coverage is not None
                    or bool(self.required_targets) != (self.reason == "scope_restricted")
                    or self.external_tools is None
                    or self.termination_problem is not None
                ):
                    raise ValueError("scope_refusal_selection_facts_invalid")
            elif self.reason == "not_started":
                if (
                    attempted
                    or self.message is None
                    or self.evidence is not None
                    or self.external_tools is not None
                    or self.request_rejection is not None
                    or self.coverage is not None
                    or self.required_targets
                    or self.termination_problem is not None
                ):
                    raise ValueError("not_started_selection_facts_invalid")
            else:
                if (
                    not attempted
                    or self.message is None
                    or self.evidence is not None
                    or self.external_tools is not None
                    or self.request_rejection is not None
                    or self.coverage is not None
                    or self.required_targets
                ):
                    raise ValueError("interrupted_selection_facts_invalid")
            return self

        if not attempted:
            raise ValueError("ordinary_selection_attempt_required")
        if self.request_rejection is not None:
            raise ValueError("ordinary_selection_rejection_forbidden")
        if self.required_targets:
            raise ValueError("ordinary_selection_required_targets_forbidden")
        if self.status == "passed":
            if (
                self.reason is not None
                or self.message is not None
                or self.termination_problem is not None
                or self.external_tools is None
            ):
                raise ValueError("passed_selection_facts_invalid")
        elif self.status == "failed":
            if (
                self.reason is not None
                or self.message is None
                or self.evidence is None
                or (isinstance(self.evidence, TextEvidence) and not self.evidence.data.strip())
                or (isinstance(self.evidence, JsonEvidence) and self.evidence.data is None)
                or self.external_tools is None
                or self.termination_problem is not None
            ):
                raise ValueError("failed_selection_facts_invalid")
        else:
            if self.message is None:
                raise ValueError("unavailable_selection_message_required")
            if isinstance(self.reason, AdapterCallFailureReason):
                if (
                    self.evidence is not None
                    or self.external_tools is not None
                    or self.coverage is not None
                ):
                    raise ValueError("runtime_unavailable_selection_facts_invalid")
            elif (
                self.reason not in get_args(AdapterUnavailableReason)
                or self.external_tools is None
                or self.termination_problem is not None
            ):
                raise ValueError("adapter_unavailable_selection_facts_invalid")
        return self


class RunChecksOutput(_ExecutionOutputModel):
    """Operational run-check result with ordered selection evidence."""

    success: StrictBool
    run_status: Literal["passed", "failed", "incomplete", "empty_selection"] | None
    requested_scope: CheckScope
    requested_targets: tuple[WorkspaceRelativePath, ...]
    selected_profile: ProfileId | None
    removed_targets: tuple[WorkspaceRelativePath, ...]
    results: tuple[SelectionCheckResult, ...]
    error_code: RunChecksErrorCode | None
    error_details: (
        CheckSelectionDetails
        | BranchBasisDetails
        | ScopeDetails
        | RejectedRequestDetails
        | TerminationDetails
        | None
    )

    @model_validator(mode="after")
    def validate_output(self) -> Self:
        if self.requested_scope == "targets" and not self.requested_targets:
            raise ValueError("targets_scope_requires_requested_targets")
        if self.requested_scope != "targets" and self.requested_targets:
            raise ValueError("requested_targets_only_for_targets_scope")
        if self.requested_scope != "branch" and self.removed_targets:
            raise ValueError("removed_targets_only_for_branch_scope")
        ids = tuple(row.check_id for row in self.results)
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate_selection_result")
        if self.error_code in {
            "no_configured_checks",
            "selection_invalid",
            "default_profile_missing",
            "branch_basis_unavailable",
            "scope_resolution_failed",
        } and (self.results or self.run_status is not None):
            raise ValueError("early_refusal_cannot_have_results")

        rejected = tuple(row.check_id for row in self.results if row.reason == "invalid_request")
        if rejected and self.error_code != "adapter_request_rejected":
            raise ValueError("invalid_request_requires_operation_error")
        if self.error_code == "adapter_request_rejected":
            if (
                self.success
                or not isinstance(self.error_details, RejectedRequestDetails)
                or rejected != (self.error_details.check_id,)
            ):
                raise ValueError("adapter_rejection_facts_invalid")
        elif not self.success:
            raise ValueError("unexpected_operational_failure")

        expected_details: dict[str, type[BaseModel] | tuple[type[BaseModel], ...] | None] = {
            "no_configured_checks": None,
            "selection_invalid": CheckSelectionDetails,
            "default_profile_missing": None,
            "branch_basis_unavailable": BranchBasisDetails,
            "scope_resolution_failed": ScopeDetails,
            "adapter_request_rejected": RejectedRequestDetails,
            "operation_interrupted": None,
            "termination_unconfirmed": TerminationDetails,
        }
        expected = expected_details.get(self.error_code) if self.error_code is not None else None
        if expected is None:
            if self.error_details is not None:
                raise ValueError("unexpected_error_details")
        elif not isinstance(self.error_details, expected):
            raise ValueError("error_details_type_mismatch")

        unconfirmed = tuple(
            row.check_id
            for row in self.results
            if row.termination_problem is TerminationProblem.UNCONFIRMED
        )
        interrupted = tuple(row.check_id for row in self.results if row.reason == "interrupted")
        if isinstance(self.error_details, TerminationDetails):
            if (
                self.error_details.check_ids != unconfirmed
                or self.error_details.interrupted != bool(interrupted)
            ):
                raise ValueError("termination_details_must_match_rows")
        elif unconfirmed:
            raise ValueError("unconfirmed_termination_requires_details")
        if self.error_code == "operation_interrupted" and not interrupted:
            raise ValueError("operation_interrupted_requires_interrupted_row")
        if interrupted and self.error_code not in {
            "operation_interrupted",
            "termination_unconfirmed",
        }:
            raise ValueError("interrupted_rows_require_operation_error")

        if self.results:
            statuses = tuple(row.status for row in self.results)
            expected_status = (
                "incomplete"
                if any(status in {"unavailable", "not_executed"} for status in statuses)
                else "failed"
                if "failed" in statuses
                else "passed"
            )
            if self.run_status != expected_status:
                raise ValueError("run_status_does_not_match_results")
        elif self.run_status == "empty_selection":
            if self.requested_scope != "branch" or self.error_code is not None:
                raise ValueError("empty_selection_requires_branch_scope")
        elif self.run_status is not None or self.error_code is None:
            raise ValueError("empty_results_require_empty_selection_or_early_error")
        return self


__all__ = [
    "BranchBasisDetails",
    "CheckSelectionDetails",
    "CheckSelectionIssue",
    "RunChecksErrorCode",
    "RunChecksOutput",
    "SelectionCheckResult",
    "UnknownCheckIssue",
    "UnknownProfileIssue",
    "UnselectedCheckArgsIssue",
    "UnsupportedSelectionIssue",
]
