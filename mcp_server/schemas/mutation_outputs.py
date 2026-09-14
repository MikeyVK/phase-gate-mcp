"""Strict immutable scaffold mutation result contracts for CY053.

@layer: Schemas
@dependencies: pydantic, execution models, template identity values
@responsibilities: Preserve complete scaffold operation, validation, invocation, and
error-detail facts without presentation or orchestration behavior.
"""

from __future__ import annotations

import re
from typing import Annotated, Literal, Self, get_args

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictStr,
    model_validator,
)

from mcp_server.config.schemas.checks_config import CheckId, ExtensionKey, ProfileId
from mcp_server.config.schemas.template_suite import TemplateId, TemplatePackageVersion
from mcp_server.execution.check_selection import WorkspaceRelativePath
from mcp_server.execution.models import (
    AdapterCallFailureReason,
    AdapterRunIdentity,
    AdapterUnavailableReason,
    ConsumerNotExecutedReason,
    ExternalToolIdentity,
    NativeEvidence,
    NonBlankText,
    ProcessCapture,
    RequestValidationIssue,
    TerminationProblem,
)
from mcp_server.services.artifact_identity import CompactFingerprint
from mcp_server.services.edit_construction import (
    EditDetails,
    EditProfileSelection,
    MetadataFallbackReason,
)


def _validate_json_pointer(value: str) -> str:
    """Validate an RFC 6901 JSON Pointer, including its valid empty root."""
    if re.fullmatch(r"(?:/(?:[^~/]|~[01])*)*", value) is None:
        raise ValueError("json_pointer_invalid")
    return value


JsonPointer = Annotated[StrictStr, AfterValidator(_validate_json_pointer)]

MutationErrorCode = Literal[
    "context_invalid",
    "target_invalid",
    "target_exists",
    "render_failed",
    "preparation_failed",
    "validation_blocked",
    "persistence_failed",
    "adapter_request_rejected",
    "termination_unconfirmed",
    "operation_interrupted",
    "original_unreadable",
    "original_changed",
    "original_missing",
    "edit_invalid",
]


class _MutationModel(BaseModel):
    """Frozen strict base for inward-owned mutation facts."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")


class ContextIssue(_MutationModel):
    """One schema-validation issue at an RFC 6901 instance pointer."""

    pointer: JsonPointer
    keyword: NonBlankText
    message: NonBlankText


class ContextDetails(_MutationModel):
    """Nonempty artifact-context validation issue collection."""

    issues: Annotated[tuple[ContextIssue, ...], Field(min_length=1)]


class TargetDetails(_MutationModel):
    """Why a requested target cannot be used."""

    path: WorkspaceRelativePath
    reason: Literal["outside_workspace", "force_required", "not_file", "unresolvable"]
    message: NonBlankText


class AffectedPathDetails(_MutationModel):
    """A target path affected by a create-only collision or lifecycle fact."""

    path: WorkspaceRelativePath


class RenderDetails(_MutationModel):
    """Factual output rendering failure."""

    message: NonBlankText


class LockWaitDetails(_MutationModel):
    """A preparation failure caused by lock waiting."""

    path: WorkspaceRelativePath
    reason: Literal["lock_wait_timeout"]


class InputPreparationDetails(_MutationModel):
    """A validation-input allocation or write failure."""

    path: WorkspaceRelativePath
    reason: Literal["validation_input_allocation_failed", "validation_input_write_failed"]
    message: NonBlankText


PreparationDetails = LockWaitDetails | InputPreparationDetails


class PersistenceDetails(_MutationModel):
    """Factual create/write-stage persistence failure."""

    path: WorkspaceRelativePath
    stage: Literal["write_staging", "create", "replace"]
    reason: Literal["permission_denied", "io_error"]
    message: NonBlankText


class RejectedRequestDetails(_MutationModel):
    """The check row that owns an internally rejected adapter request."""

    check_id: CheckId


class TerminationDetails(_MutationModel):
    """Checks affected by interruption or unconfirmed process termination."""

    check_ids: Annotated[tuple[CheckId, ...], Field(min_length=1)]
    interrupted: StrictBool

    @model_validator(mode="after")
    def validate_unique_check_ids(self) -> TerminationDetails:
        if len(set(self.check_ids)) != len(self.check_ids):
            raise ValueError("duplicate_termination_check")
        return self


class OriginalReadDetails(_MutationModel):
    """Observed original-file read failure, independent of content checking."""

    path: WorkspaceRelativePath
    reason: Literal["permission_denied", "invalid_encoding", "io_error"]
    message: NonBlankText


MutationErrorDetails = (
    OriginalReadDetails
    | EditDetails
    | ContextDetails
    | TargetDetails
    | AffectedPathDetails
    | RenderDetails
    | PreparationDetails
    | PersistenceDetails
    | RejectedRequestDetails
    | TerminationDetails
)


class HousekeepingIssue(_MutationModel):
    """A non-blocking cleanup problem owned by the mutation attempt."""

    purpose: Literal["validation_input", "write_staging"]
    path: WorkspaceRelativePath
    message: NonBlankText


class InvocationEvidence(_MutationModel):
    """Provenance and bounded capture for one attempted adapter invocation."""

    adapter: AdapterRunIdentity
    capture: ProcessCapture
    external_tools: tuple[ExternalToolIdentity, ...] | None


class MutationCheck(_MutationModel):
    """One concrete scaffold output-validation check record."""

    check_id: CheckId
    status: Literal["passed", "failed", "unavailable", "not_executed"]
    reason: AdapterUnavailableReason | AdapterCallFailureReason | ConsumerNotExecutedReason | None
    message: NonBlankText | None
    evidence: NativeEvidence | None
    request_rejection: Annotated[tuple[RequestValidationIssue, ...], Field(min_length=1)] | None
    invocation: InvocationEvidence | None
    termination_problem: TerminationProblem | None
    housekeeping: tuple[HousekeepingIssue, ...]
    args_source: Literal["configured"] | None
    effective_args: tuple[StrictStr, ...] | None

    @model_validator(mode="after")
    def validate_observation(self) -> MutationCheck:
        if (self.args_source is None) != (self.effective_args is None):
            raise ValueError("argument_facts_must_agree")
        if self.invocation is not None and self.args_source is None:
            raise ValueError("attempt_argument_facts_required")

        if self.status == "not_executed":
            if self.reason not in get_args(ConsumerNotExecutedReason):
                raise ValueError("invalid_not_executed_reason")
            if self.evidence is not None:
                raise ValueError("not_executed_native_facts_forbidden")
            if (self.request_rejection is not None) != (self.reason == "invalid_request"):
                raise ValueError("request_rejection_reason_mismatch")
            if self.reason == "invalid_request":
                if self.message is not None or self.termination_problem is not None:
                    raise ValueError("invalid_request_facts_invalid")
                if self.invocation is None:
                    raise ValueError("attempt_identity_and_capture_required")
            elif self.reason == "not_started":
                if self.message is None:
                    raise ValueError("not_started_message_required")
                if self.invocation is not None or self.termination_problem is not None:
                    raise ValueError("not_started_attempt_forbidden")
            else:
                if self.message is None:
                    raise ValueError("interrupted_message_required")
                if self.invocation is None:
                    raise ValueError("attempt_identity_and_capture_required")
            if self.invocation is not None and self.invocation.external_tools is not None:
                raise ValueError("not_executed_external_tools_forbidden")
            return self

        if self.invocation is None:
            raise ValueError("attempt_identity_and_capture_required")
        if self.request_rejection is not None:
            raise ValueError("ordinary_result_rejection_forbidden")

        if self.status == "passed":
            if (
                self.reason is not None
                or self.message is not None
                or self.termination_problem is not None
            ):
                raise ValueError("passed_result_facts_invalid")
            if self.invocation.external_tools is None:
                raise ValueError("passed_result_requires_external_tools")
            return self

        if self.message is None:
            raise ValueError("ordinary_result_message_required")

        if self.status == "failed":
            if self.reason is not None:
                raise ValueError("failed_reason_forbidden")
            if self.evidence is None:
                raise ValueError("failed_result_requires_evidence")
            if self.termination_problem is not None:
                raise ValueError("failed_termination_forbidden")
            if self.invocation.external_tools is None:
                raise ValueError("failed_result_requires_external_tools")
            return self

        if not (
            self.reason in get_args(AdapterUnavailableReason)
            or isinstance(self.reason, AdapterCallFailureReason)
        ):
            raise ValueError("unavailable_reason_invalid")
        if isinstance(self.reason, AdapterCallFailureReason):
            if self.evidence is not None or self.invocation.external_tools is not None:
                raise ValueError("invocation_failure_native_facts_forbidden")
        else:
            if self.invocation.external_tools is None:
                raise ValueError("adapter_unavailable_requires_external_tools")
        if self.termination_problem is not None and not isinstance(
            self.reason, AdapterCallFailureReason
        ):
            raise ValueError("termination_problem_requires_invocation_failure")
        return self


class _MutationOperationOutput(_MutationModel):
    """Shared immutable validation and lifecycle facts for completed mutation attempts."""

    success: StrictBool
    written: StrictBool
    validation_policy: Literal["enforce", "report"]
    validation_status: Literal["passed", "failed", "unavailable", "not_executed"]
    profile_id: ProfileId | None
    checks: tuple[MutationCheck, ...]
    error_code: MutationErrorCode | None
    error_details: MutationErrorDetails | None
    housekeeping: tuple[HousekeepingIssue, ...]

    @model_validator(mode="after")
    def validate_operation(self) -> Self:
        if self.success != self.written:
            raise ValueError("success_written_must_agree")
        if not self.success and self.error_code is None:
            raise ValueError("unsuccessful_operation_requires_error")
        if self.success and self.error_code is not None:
            raise ValueError("successful_operation_cannot_have_error")

        statuses = tuple(row.status for row in self.checks)
        if self.written:
            if "not_executed" in statuses:
                raise ValueError("written_operation_requires_complete_validation")
            if self.validation_policy == "enforce" and self.validation_status != "passed":
                raise ValueError("enforce_write_requires_passed_validation")
        if self.error_code == "validation_blocked" and (
            self.validation_policy != "enforce" or self.validation_status == "passed"
        ):
            raise ValueError("validation_blocked_requires_enforce_failure")

        if self.validation_status == "passed":
            if not statuses or any(status != "passed" for status in statuses):
                raise ValueError("passed_status_requires_all_passed_checks")
        elif self.validation_status == "failed":
            if "failed" not in statuses:
                raise ValueError("failed_status_requires_failed_check")
        elif self.validation_status == "unavailable":
            if "failed" in statuses or "unavailable" not in statuses:
                raise ValueError("unavailable_status_invalid")
        elif any(status in {"failed", "unavailable"} for status in statuses) or (
            statuses and all(status == "passed" for status in statuses)
        ):
            raise ValueError("not_executed_status_invalid")

        expected_details: dict[str, type[BaseModel] | tuple[type[BaseModel], ...] | None] = {
            "context_invalid": ContextDetails,
            "original_unreadable": OriginalReadDetails,
            "original_changed": AffectedPathDetails,
            "original_missing": AffectedPathDetails,
            "edit_invalid": EditDetails,
            "target_invalid": TargetDetails,
            "target_exists": AffectedPathDetails,
            "render_failed": RenderDetails,
            "preparation_failed": (LockWaitDetails, InputPreparationDetails),
            "validation_blocked": None,
            "persistence_failed": PersistenceDetails,
            "adapter_request_rejected": RejectedRequestDetails,
            "termination_unconfirmed": TerminationDetails,
            "operation_interrupted": None,
        }
        if self.error_code is None:
            if self.error_details is not None:
                raise ValueError("unexpected_error_details")
        else:
            expected = expected_details[self.error_code]
            if expected is None:
                if self.error_details is not None:
                    raise ValueError("unexpected_error_details")
            elif not isinstance(self.error_details, expected):
                raise ValueError("error_details_type_mismatch")

        rejected = tuple(row.check_id for row in self.checks if row.reason == "invalid_request")
        if isinstance(self.error_details, RejectedRequestDetails):
            if self.success or rejected != (self.error_details.check_id,):
                raise ValueError("rejected_request_requires_failed_operation_and_row")
        elif rejected and self.error_code != "adapter_request_rejected":
            raise ValueError("rejected_request_requires_operation_error")

        interrupted = tuple(row.check_id for row in self.checks if row.reason == "interrupted")
        unconfirmed = tuple(
            row.check_id
            for row in self.checks
            if row.termination_problem is TerminationProblem.UNCONFIRMED
        )
        if isinstance(self.error_details, TerminationDetails) and (
            self.error_details.check_ids != unconfirmed
            or self.error_details.interrupted != bool(interrupted)
        ):
            raise ValueError("termination_details_must_match_observed_rows")
        if unconfirmed and not isinstance(self.error_details, TerminationDetails):
            raise ValueError("unconfirmed_termination_requires_operation_error")

        if self.error_code == "operation_interrupted" and not interrupted:
            raise ValueError("interruption_error_requires_interrupted_rows")
        if interrupted and self.error_code not in {
            "operation_interrupted",
            "termination_unconfirmed",
        }:
            raise ValueError("interruption_requires_operation_error")
        return self


class ScaffoldOperationOutput(_MutationOperationOutput):
    """Complete immutable scaffold operation result."""

    output_path: WorkspaceRelativePath | None
    template_id: TemplateId
    package_version: TemplatePackageVersion
    package_fingerprint: CompactFingerprint

    @model_validator(mode="after")
    def validate_scaffold(self) -> Self:
        if self.written and self.output_path is None:
            raise ValueError("written_output_path_required")
        if self.written and self.validation_status == "not_executed":
            raise ValueError("written_operation_requires_complete_validation")
        if self.error_code in {
            "original_unreadable",
            "original_changed",
            "original_missing",
            "edit_invalid",
        }:
            raise ValueError("edit_error_for_scaffold_forbidden")
        return self


class EditOperationOutput(_MutationOperationOutput):
    """Complete edit result with factual source selection and completed text effect."""

    path: WorkspaceRelativePath
    content_changed: StrictBool | None
    selected_source: Literal["input", "metadata", "extension", "none"] | None
    template_id: TemplateId | None
    extension: ExtensionKey | None
    selection_reason: MetadataFallbackReason | None

    @model_validator(mode="after")
    def validate_edit(self) -> Self:
        if self.written != (self.content_changed is not None):
            raise ValueError("completed_write_required_for_text_effect")
        if self.selected_source is None:
            if any(
                value is not None
                for value in (
                    self.profile_id,
                    self.template_id,
                    self.extension,
                    self.selection_reason,
                )
            ):
                raise ValueError("unreached_selection_facts_forbidden")
        else:
            EditProfileSelection(
                selected_source=self.selected_source,
                profile_id=self.profile_id,
                template_id=self.template_id,
                extension=self.extension,
                selection_reason=self.selection_reason,
            )
        if self.checks and self.profile_id is None:
            raise ValueError("check_facts_require_selected_profile")
        if self.written and self.selected_source is None:
            raise ValueError("written_edit_requires_selection")
        if self.written and self.profile_id is not None and not self.checks:
            raise ValueError("selected_profile_requires_check_obligations")
        return self
