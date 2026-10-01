"""Immutable generic adapter process invocation models."""

from __future__ import annotations

import re
from enum import IntEnum, StrEnum
from typing import Annotated, Generic, Literal, TypeVar, get_args

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    GetCoreSchemaHandler,
    GetPydanticSchema,
    JsonValue,
    RootModel,
    SerializerFunctionWrapHandler,
    StrictBool,
    StrictInt,
    StrictStr,
    StringConstraints,
    field_validator,
    model_serializer,
    model_validator,
)
from pydantic_core import CoreSchema, core_schema

from mcp_server.config.schemas.adapter_manifest import AdapterId, AdapterVersion, CapabilityId
from mcp_server.config.schemas.fixes_config import FixId
from mcp_server.config.schemas.tests_config import TestId
from mcp_server.core.interfaces.template_catalog import (
    FrozenJsonObject,
    FrozenJsonValue,
    freeze_json,
    thaw_json,
)
from mcp_server.execution.check_selection import AbsolutePath, ArgsSource, WorkspaceRelativePath


class AdapterExitCode(IntEnum):
    """Shared adapter response exit-code categories."""

    SUCCESS = 0
    NEGATIVE_RESULT = 1
    INVALID_REQUEST = 2
    UNAVAILABLE = 3


class AdapterCallFailureReason(StrEnum):
    """PGMCP-owned failures to obtain a valid adapter response."""

    LAUNCH_FAILED = "launch_failed"
    TIMEOUT = "timeout"
    PROCESS_FAILED = "process_failed"
    INVALID_RESPONSE = "invalid_response"
    RESPONSE_TOO_LARGE = "response_too_large"


class AdapterCallFailure(BaseModel):
    """A bounded adapter-call failure, distinct from native role outcomes."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    reason: AdapterCallFailureReason
    message: StrictStr

    @model_validator(mode="after")
    def validate_message(self) -> AdapterCallFailure:
        if not self.message.strip():
            raise ValueError("message_must_be_nonblank")
        return self


class TerminationProblem(StrEnum):
    """A process termination fact requiring consumer attention."""

    UNCONFIRMED = "termination_unconfirmed"


class StreamCapture(BaseModel):
    """Bounded facts observed from one child-process stream."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    observed_bytes: Annotated[StrictInt, Field(ge=0)]
    head: StrictStr | None
    tail: StrictStr | None
    truncated: StrictBool


class ProcessCapture(BaseModel):
    """Bounded stdout/stderr capture and observed process exit."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    exit_code: StrictInt | None
    stdout: StreamCapture
    stderr: StreamCapture


TResponse = TypeVar("TResponse", bound=BaseModel)


class InvocationResultBase(BaseModel):
    """Common capture carried by every attempted invocation result."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    capture: ProcessCapture
    cleanup_failure: AdapterCallFailure | None = None

    def message_with_cleanup(self, message: str | None) -> str | None:
        """Retain the primary message and any additional resource failure cause."""
        if self.cleanup_failure is None:
            return message
        return "\n".join(part for part in (message, self.cleanup_failure.message) if part)


def _capture_describes_no_started_process(capture: ProcessCapture) -> bool:
    return (
        capture.exit_code is None
        and capture.stdout.observed_bytes == 0
        and capture.stderr.observed_bytes == 0
        and capture.stdout.head == ""
        and capture.stdout.tail == ""
        and capture.stderr.head == ""
        and capture.stderr.tail == ""
        and not capture.stdout.truncated
        and not capture.stderr.truncated
    )


class InvocationCompleted(InvocationResultBase, Generic[TResponse]):
    """A complete, contract-valid adapter response."""

    outcome: Literal["completed"]
    response: TResponse

    @model_validator(mode="after")
    def validate_capture(self) -> InvocationCompleted[TResponse]:
        if self.capture.exit_code not in tuple(AdapterExitCode):
            raise ValueError("completed_exit_code_invalid")
        if (
            self.capture.stdout.head is not None
            or self.capture.stdout.tail is not None
            or self.capture.stdout.truncated
        ):
            raise ValueError("completed_stdout_raw_capture_forbidden")
        return self


class InvocationFailed(InvocationResultBase):
    """A PGMCP-owned invocation failure."""

    outcome: Literal["failed"]
    failure: AdapterCallFailure
    termination_problem: TerminationProblem | None
    preceding_response: JsonEvidence | None = None

    @model_validator(mode="after")
    def validate_failure(self) -> InvocationFailed:
        if self.preceding_response is not None and (
            self.failure.reason is not AdapterCallFailureReason.PROCESS_FAILED
            or not preserves_completed_response(self.preceding_response, self.capture)
        ):
            raise ValueError("preceding_response_requires_completed_process_capture")
        if self.failure.reason is AdapterCallFailureReason.LAUNCH_FAILED:
            if self.termination_problem is TerminationProblem.UNCONFIRMED:
                raise ValueError("launch_failed_cannot_be_termination_unconfirmed")
            if not _capture_describes_no_started_process(self.capture):
                raise ValueError("launch_failed_capture_claims_started_process")
        return self


class InvocationCancelled(InvocationResultBase):
    """An invocation cancelled before a completed adapter result."""

    outcome: Literal["cancelled"]
    termination_problem: TerminationProblem | None


# Check role contracts deliberately retain native data without finding normalization.
NonBlankText = Annotated[str, StringConstraints(strict=True, pattern=r"\S")]
AdapterUnavailableReason = Literal[
    "dependency_unavailable",
    "unsupported_input",
    "invalid_configuration",
    "execution_error",
    "invalid_result",
]


class _CheckModel(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")


class ExternalToolIdentity(_CheckModel):
    tool_id: NonBlankText
    version: NonBlankText | None


class TextEvidence(_CheckModel):
    format: Literal["text"]
    data: StrictStr


def _frozen_json_schema(_source: object, handler: GetCoreSchemaHandler) -> CoreSchema:
    return core_schema.no_info_plain_validator_function(
        freeze_json,
        json_schema_input_schema=handler.generate_schema(JsonValue),
        serialization=core_schema.plain_serializer_function_ser_schema(thaw_json),
    )


class JsonEvidence(_CheckModel):
    format: Literal["json"]
    data: Annotated[
        str | bool | int | float | None | tuple[FrozenJsonValue, ...] | FrozenJsonObject,
        GetPydanticSchema(_frozen_json_schema),
    ]


NativeEvidence = Annotated[TextEvidence | JsonEvidence, Field(discriminator="format")]


def preserves_completed_response(
    evidence: NativeEvidence | None, capture: ProcessCapture | None
) -> bool:
    """Identify a retained accepted response beside a later invocation failure."""
    return (
        isinstance(evidence, JsonEvidence)
        and isinstance(evidence.data, FrozenJsonObject)
        and capture is not None
        and capture.exit_code
        in (AdapterExitCode.SUCCESS, AdapterExitCode.NEGATIVE_RESULT, AdapterExitCode.UNAVAILABLE)
        and capture.stdout.observed_bytes > 0
        and capture.stdout.head is None
        and capture.stdout.tail is None
        and not capture.stdout.truncated
    )


class CheckPassed(_CheckModel):
    status: Literal["passed"]


class CheckFailed(_CheckModel):
    status: Literal["failed"]
    message: NonBlankText


class CheckUnavailable(_CheckModel):
    status: Literal["unavailable"]
    reason: AdapterUnavailableReason
    message: NonBlankText


class CheckNotExecuted(_CheckModel):
    status: Literal["not_executed"]
    reason: Literal["scope_restricted", "not_applicable"]
    message: NonBlankText


ContentDecision = Annotated[
    CheckPassed | CheckFailed | CheckUnavailable, Field(discriminator="status")
]
SelectionDecision = Annotated[
    CheckPassed | CheckFailed | CheckUnavailable | CheckNotExecuted, Field(discriminator="status")
]


class RequestValidationIssue(_CheckModel):
    location: tuple[StrictStr | Annotated[StrictInt, Field(ge=0)], ...]
    code: Literal["missing_field", "unknown_field", "wrong_type", "invalid_value"]


class InvalidCheckRequest(_CheckModel):
    reason: Literal["invalid_request"]
    details: Annotated[tuple[RequestValidationIssue, ...], Field(min_length=1)]


class _CheckEvidence(_CheckModel):
    external_tools: tuple[ExternalToolIdentity, ...]
    evidence: NativeEvidence | None = None

    @field_validator("evidence", mode="before")
    @classmethod
    def reject_null_evidence(cls, value: object) -> object:
        if value is None:
            raise ValueError("evidence_must_be_omitted")
        return value

    @model_serializer(mode="wrap")
    def serialize_evidence(self, handler: SerializerFunctionWrapHandler) -> dict[str, object]:
        result: dict[str, object] = handler(self)
        if self.evidence is None:
            result.pop("evidence", None)
        return result


class ContentRoleResponse(_CheckEvidence):
    decision: ContentDecision

    @model_validator(mode="after")
    def require_failed_evidence(self) -> ContentRoleResponse:
        if isinstance(self.decision, CheckFailed) and self.evidence is None:
            raise ValueError("failed_evidence_required")
        return self


class CheckedCoverage(_CheckModel):
    targets: tuple[WorkspaceRelativePath, ...]
    expanded: StrictBool


class SelectionRoleResponse(_CheckEvidence):
    decision: SelectionDecision
    coverage: CheckedCoverage | None
    required_targets: tuple[WorkspaceRelativePath, ...]

    @model_validator(mode="after")
    def validate_selection_facts(self) -> SelectionRoleResponse:
        if isinstance(self.decision, CheckFailed) and self.evidence is None:
            raise ValueError("failed_evidence_required")
        if isinstance(self.decision, CheckNotExecuted):
            if self.coverage is not None:
                raise ValueError("not_executed_coverage_forbidden")
            if bool(self.required_targets) != (self.decision.reason == "scope_restricted"):
                raise ValueError("required_targets_reason_mismatch")
        elif self.required_targets:
            raise ValueError("required_targets_without_scope_refusal")
        return self


class ContentCheckResponse(RootModel[ContentRoleResponse | InvalidCheckRequest]):
    model_config = ConfigDict(frozen=True, strict=True)


class SelectionCheckResponse(RootModel[SelectionRoleResponse | InvalidCheckRequest]):
    model_config = ConfigDict(frozen=True, strict=True)


# Test contracts retain their own native decisions and concrete public projection.
class _TestModel(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")


class TestRequest(_TestModel):
    operation: CapabilityId
    targets: tuple[AbsolutePath, ...]
    args: tuple[StrictStr, ...]


class TestPassed(_TestModel):
    status: Literal["passed"]
    message: NonBlankText


class TestFailed(_TestModel):
    status: Literal["failed"]
    message: NonBlankText


class TestUnavailable(_TestModel):
    status: Literal["unavailable"]
    reason: AdapterUnavailableReason
    message: NonBlankText


TestDecision = Annotated[TestPassed | TestFailed | TestUnavailable, Field(discriminator="status")]


def _require_test_evidence(evidence: NativeEvidence | None) -> None:
    if (
        evidence is None
        or (isinstance(evidence, TextEvidence) and not evidence.data.strip())
        or (isinstance(evidence, JsonEvidence) and evidence.data is None)
    ):
        raise ValueError("substantive_failed_evidence_required")


class TestRoleResponse(_TestModel):
    decision: TestDecision
    external_tools: tuple[ExternalToolIdentity, ...]
    evidence: NativeEvidence | None = None

    @model_validator(mode="after")
    def validate_evidence(self) -> TestRoleResponse:
        if self.evidence is None and "evidence" in self.model_fields_set:
            raise ValueError("evidence_must_be_omitted")
        if self.decision.status == "failed":
            _require_test_evidence(self.evidence)
        return self

    @model_serializer(mode="wrap")
    def serialize_evidence(self, handler: SerializerFunctionWrapHandler) -> dict[str, object]:
        result: dict[str, object] = handler(self)
        if self.evidence is None:
            result.pop("evidence", None)
        return result


class TestResponse(RootModel[TestRoleResponse | InvalidCheckRequest]):
    model_config = ConfigDict(frozen=True, strict=True)


AdapterFingerprint = Annotated[
    str, StringConstraints(strict=True, min_length=16, max_length=16, pattern=r"^[A-Za-z0-9_-]+$")
]


class AdapterRunIdentity(_TestModel):
    adapter_id: AdapterId
    version: AdapterVersion
    fingerprint: AdapterFingerprint
    contract_version: Literal[1]


ConsumerNotExecutedReason = Literal["not_started", "interrupted", "invalid_request"]
TestScope = Literal["configured", "workspace", "targets"]


class PublicTestResult(_TestModel):
    test_id: TestId
    status: Literal["passed", "failed", "unavailable", "not_executed"]
    reason: AdapterUnavailableReason | AdapterCallFailureReason | ConsumerNotExecutedReason | None
    message: NonBlankText | None
    evidence: NativeEvidence | None
    external_tools: tuple[ExternalToolIdentity, ...] | None
    adapter: AdapterRunIdentity | None
    capture: ProcessCapture | None
    termination_problem: TerminationProblem | None
    request_rejection: Annotated[tuple[RequestValidationIssue, ...], Field(min_length=1)] | None
    args_source: ArgsSource | None
    effective_args: tuple[StrictStr, ...] | None

    @model_validator(mode="after")
    def validate_observation(self) -> PublicTestResult:
        if (self.args_source is None) != (self.effective_args is None):
            raise ValueError("argument_facts_must_agree")
        not_started = self.status == "not_executed" and self.reason == "not_started"
        if not_started:
            if self.adapter is not None or self.capture is not None:
                raise ValueError("not_started_attempt_forbidden")
        elif self.adapter is None or self.capture is None:
            raise ValueError("attempt_identity_and_capture_required")
        if self.status == "not_executed":
            if self.reason not in {"not_started", "interrupted", "invalid_request"}:
                raise ValueError("invalid_not_executed_reason")
            if (
                (self.reason == "not_started" and self.message is not None)
                or self.evidence is not None
                or self.external_tools is not None
            ):
                raise ValueError("not_executed_native_facts_forbidden")
            if (self.request_rejection is not None) != (self.reason == "invalid_request"):
                raise ValueError("request_rejection_reason_mismatch")
            if self.termination_problem is not None:
                raise ValueError("interruption_termination_owned_by_operation")
        else:
            if self.request_rejection is not None or self.message is None:
                raise ValueError("ordinary_result_facts_invalid")
            if self.status in {"passed", "failed"}:
                if self.reason is not None or self.external_tools is None:
                    raise ValueError("accepted_result_requires_native_facts")
            elif isinstance(self.reason, AdapterCallFailureReason):
                if self.external_tools is not None or (
                    self.evidence is not None
                    and (
                        self.reason is not AdapterCallFailureReason.PROCESS_FAILED
                        or not preserves_completed_response(self.evidence, self.capture)
                    )
                ):
                    raise ValueError("invocation_failure_native_facts_forbidden")
            elif (
                self.reason not in get_args(AdapterUnavailableReason) or self.external_tools is None
            ):
                raise ValueError("adapter_unavailable_facts_invalid")
            if self.termination_problem is not None and not isinstance(
                self.reason, AdapterCallFailureReason
            ):
                raise ValueError("termination_problem_requires_invocation_failure")
            if self.status == "failed":
                _require_test_evidence(self.evidence)
        return self


class TestSelectionIssue(_TestModel):
    field: Literal["tests", "args"]
    test_id: TestId
    reason: Literal["unknown_test", "unselected_args"]

    @model_validator(mode="after")
    def validate_field(self) -> TestSelectionIssue:
        if self.reason == "unselected_args" and self.field != "args":
            raise ValueError("unselected_args_requires_args_field")
        return self


class TestSelectionDetails(_TestModel):
    issues: Annotated[tuple[TestSelectionIssue, ...], Field(min_length=1)]


class ScopeIssue(_TestModel):
    target: WorkspaceRelativePath
    reason: Literal["missing", "outside_workspace", "unresolvable"]
    message: NonBlankText


class ScopeDetails(_TestModel):
    issues: Annotated[tuple[ScopeIssue, ...], Field(min_length=1)]


class RejectedTestRequestDetails(_TestModel):
    test_id: TestId


class TestTerminationDetails(_TestModel):
    test_ids: Annotated[tuple[TestId, ...], Field(min_length=1)]
    interrupted: StrictBool

    @model_validator(mode="after")
    def unique_tests(self) -> TestTerminationDetails:
        if len(set(self.test_ids)) != len(self.test_ids):
            raise ValueError("duplicate_termination_test")
        return self


RunTestsErrorCode = Literal[
    "no_configured_tests",
    "no_active_tests",
    "selection_invalid",
    "scope_resolution_failed",
    "adapter_request_rejected",
    "operation_interrupted",
    "termination_unconfirmed",
]


class RunTestsOutput(_TestModel):
    success: StrictBool
    requested_scope: TestScope
    requested_targets: tuple[WorkspaceRelativePath, ...]
    selected_tests: tuple[TestId, ...]
    results: tuple[PublicTestResult, ...]
    error_code: RunTestsErrorCode | None
    error_details: (
        TestSelectionDetails
        | ScopeDetails
        | RejectedTestRequestDetails
        | TestTerminationDetails
        | None
    )

    @model_validator(mode="after")
    def validate_output(self) -> RunTestsOutput:
        if self.requested_scope != "targets" and self.requested_targets:
            raise ValueError("requested_targets_only_for_targets_scope")
        if len(set(self.selected_tests)) != len(self.selected_tests):
            raise ValueError("duplicate_selected_test")
        if tuple(row.test_id for row in self.results) != self.selected_tests:
            raise ValueError("result_obligations_must_match_selection")
        detail_types = {
            "selection_invalid": TestSelectionDetails,
            "scope_resolution_failed": ScopeDetails,
            "adapter_request_rejected": RejectedTestRequestDetails,
            "termination_unconfirmed": TestTerminationDetails,
        }
        expected = detail_types.get(self.error_code) if self.error_code is not None else None
        if expected is None:
            if self.error_details is not None:
                raise ValueError("unexpected_error_details")
        elif not isinstance(self.error_details, expected):
            raise ValueError("error_details_type_mismatch")
        rejected = tuple(row.test_id for row in self.results if row.reason == "invalid_request")
        if isinstance(self.error_details, RejectedTestRequestDetails):
            if self.success or rejected != (self.error_details.test_id,):
                raise ValueError("rejected_request_requires_failed_operation_and_row")
        elif rejected:
            raise ValueError("rejected_request_requires_operation_error")
        interrupted = tuple(row.test_id for row in self.results if row.reason == "interrupted")
        unconfirmed = tuple(
            row.test_id
            for row in self.results
            if row.termination_problem is TerminationProblem.UNCONFIRMED
        )
        if isinstance(self.error_details, TestTerminationDetails):
            expected_tests = tuple(
                row.test_id
                for row in self.results
                if row.test_id in unconfirmed or row.test_id in interrupted
            )
            if (
                self.error_details.test_ids != expected_tests
                or self.error_details.interrupted != bool(interrupted)
            ):
                raise ValueError("termination_details_must_match_observed_rows")
        elif unconfirmed:
            raise ValueError("unconfirmed_termination_requires_operation_error")
        if (self.error_code == "operation_interrupted" and not interrupted) or (
            interrupted
            and self.error_code not in {"operation_interrupted", "termination_unconfirmed"}
        ):
            raise ValueError("interrupted_row_requires_operation_error")
        return self


def _file_path(value: str) -> str:
    if re.search(r"(?:[\\/]|(?:^|[\\/])\.{1,2})$", value) is not None:
        raise ValueError("file_path_required")
    return value


def _relative_file_path(value: str) -> str:
    if any(character in value for character in "*?[]"):
        raise ValueError("literal_file_path_required")
    return _file_path(value)


AbsoluteFilePath = Annotated[AbsolutePath, AfterValidator(_file_path)]
WorkspaceRelativeFilePath = Annotated[WorkspaceRelativePath, AfterValidator(_relative_file_path)]


# Fix contracts own stop-first mutation facts separately from test outcomes.
class _FixModel(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")


class FixRequest(_FixModel):
    operation: CapabilityId
    targets: Annotated[tuple[AbsoluteFilePath, ...], Field(min_length=1)]
    args: tuple[StrictStr, ...]


class FixPassed(_FixModel):
    status: Literal["passed"]


class FixFailed(_FixModel):
    status: Literal["failed"]
    message: NonBlankText


class FixUnavailable(_FixModel):
    status: Literal["unavailable"]
    reason: AdapterUnavailableReason
    message: NonBlankText


FixDecision = Annotated[FixPassed | FixFailed | FixUnavailable, Field(discriminator="status")]


def _require_fix_evidence(evidence: NativeEvidence | None) -> None:
    if (
        evidence is None
        or (isinstance(evidence, TextEvidence) and not evidence.data.strip())
        or (isinstance(evidence, JsonEvidence) and evidence.data is None)
    ):
        raise ValueError("substantive_failed_evidence_required")


class FixRoleResponse(_FixModel):
    decision: FixDecision
    external_tools: tuple[ExternalToolIdentity, ...]
    evidence: NativeEvidence | None = None

    @model_validator(mode="after")
    def validate_evidence(self) -> FixRoleResponse:
        if self.evidence is None and "evidence" in self.model_fields_set:
            raise ValueError("evidence_must_be_omitted")
        if self.decision.status == "failed":
            _require_fix_evidence(self.evidence)
        return self

    @model_serializer(mode="wrap")
    def serialize_evidence(self, handler: SerializerFunctionWrapHandler) -> dict[str, object]:
        result: dict[str, object] = handler(self)
        if self.evidence is None:
            result.pop("evidence", None)
        return result


class FixResponse(RootModel[FixRoleResponse | InvalidCheckRequest]):
    model_config = ConfigDict(frozen=True, strict=True)


class PublicFixResult(_FixModel):
    fix_id: FixId
    status: Literal["passed", "failed", "unavailable", "not_executed"]
    reason: AdapterUnavailableReason | AdapterCallFailureReason | ConsumerNotExecutedReason | None
    message: NonBlankText | None
    evidence: NativeEvidence | None
    external_tools: tuple[ExternalToolIdentity, ...] | None
    adapter: AdapterRunIdentity | None
    capture: ProcessCapture | None
    termination_problem: TerminationProblem | None
    request_rejection: Annotated[tuple[RequestValidationIssue, ...], Field(min_length=1)] | None
    args_source: ArgsSource | None
    effective_args: tuple[StrictStr, ...] | None

    @model_validator(mode="after")
    def validate_observation(self) -> PublicFixResult:
        if (self.args_source is None) != (self.effective_args is None):
            raise ValueError("argument_facts_must_agree")
        not_started = self.status == "not_executed" and self.reason == "not_started"
        if not_started:
            if self.adapter is not None or self.capture is not None:
                raise ValueError("not_started_attempt_forbidden")
        elif self.adapter is None or self.capture is None:
            raise ValueError("attempt_identity_and_capture_required")
        if self.status == "not_executed":
            if self.reason not in {"not_started", "interrupted", "invalid_request"}:
                raise ValueError("invalid_not_executed_reason")
            if (
                (self.reason == "not_started" and self.message is not None)
                or self.evidence is not None
                or self.external_tools is not None
            ):
                raise ValueError("not_executed_native_facts_forbidden")
            if (self.request_rejection is not None) != (self.reason == "invalid_request"):
                raise ValueError("request_rejection_reason_mismatch")
            if self.termination_problem is not None:
                raise ValueError("interruption_termination_owned_by_operation")
        else:
            if self.request_rejection is not None:
                raise ValueError("ordinary_result_rejection_forbidden")
            if (self.status == "passed") != (self.message is None):
                raise ValueError("message_must_match_fix_decision")
            if self.status in {"passed", "failed"}:
                if self.reason is not None or self.external_tools is None:
                    raise ValueError("accepted_result_requires_native_facts")
            elif isinstance(self.reason, AdapterCallFailureReason):
                if self.external_tools is not None or (
                    self.evidence is not None
                    and (
                        self.reason is not AdapterCallFailureReason.PROCESS_FAILED
                        or not preserves_completed_response(self.evidence, self.capture)
                    )
                ):
                    raise ValueError("invocation_failure_native_facts_forbidden")
            elif (
                self.reason not in get_args(AdapterUnavailableReason) or self.external_tools is None
            ):
                raise ValueError("adapter_unavailable_facts_invalid")
            if self.termination_problem is not None and not isinstance(
                self.reason, AdapterCallFailureReason
            ):
                raise ValueError("termination_problem_requires_invocation_failure")
            if self.status == "failed":
                _require_fix_evidence(self.evidence)
        return self


class FixSelectionIssue(_FixModel):
    field: Literal["fixes", "args"]
    fix_id: FixId
    reason: Literal["unknown_fix", "unselected_args"]

    @model_validator(mode="after")
    def validate_field(self) -> FixSelectionIssue:
        if self.reason == "unselected_args" and self.field != "args":
            raise ValueError("unselected_args_requires_args_field")
        return self


class FixSelectionDetails(_FixModel):
    issues: Annotated[tuple[FixSelectionIssue, ...], Field(min_length=1)]


class FixScopeIssue(_FixModel):
    target: WorkspaceRelativePath
    reason: Literal["missing", "not_file", "outside_workspace", "unresolvable"]
    message: NonBlankText


class FixScopeDetails(_FixModel):
    issues: Annotated[tuple[FixScopeIssue, ...], Field(min_length=1)]


class RejectedFixRequestDetails(_FixModel):
    fix_id: FixId


class FixTerminationDetails(_FixModel):
    fix_id: FixId
    interrupted: StrictBool


ApplyFixesErrorCode = Literal[
    "no_configured_fixes",
    "selection_invalid",
    "scope_resolution_failed",
    "adapter_request_rejected",
    "operation_interrupted",
    "termination_unconfirmed",
]


class ApplyFixesOutput(_FixModel):
    success: StrictBool
    requested_scope: Literal["targets"]
    requested_targets: Annotated[tuple[WorkspaceRelativePath, ...], Field(min_length=1)]
    selected_fixes: tuple[FixId, ...]
    results: tuple[PublicFixResult, ...]
    error_code: ApplyFixesErrorCode | None
    error_details: (
        FixSelectionDetails
        | FixScopeDetails
        | RejectedFixRequestDetails
        | FixTerminationDetails
        | None
    )

    @model_validator(mode="after")
    def validate_output(self) -> ApplyFixesOutput:
        if len(set(self.selected_fixes)) != len(self.selected_fixes):
            raise ValueError("duplicate_selected_fix")
        if tuple(row.fix_id for row in self.results) != self.selected_fixes:
            raise ValueError("result_obligations_must_match_selection")
        unresolved = self.error_code in {"no_configured_fixes", "selection_invalid"}
        if unresolved != (not self.selected_fixes):
            raise ValueError("selection_must_resolve_before_results")
        detail_types = {
            "selection_invalid": FixSelectionDetails,
            "scope_resolution_failed": FixScopeDetails,
            "adapter_request_rejected": RejectedFixRequestDetails,
            "termination_unconfirmed": FixTerminationDetails,
        }
        expected = detail_types.get(self.error_code) if self.error_code is not None else None
        if expected is None:
            if self.error_details is not None:
                raise ValueError("unexpected_error_details")
        elif not isinstance(self.error_details, expected):
            raise ValueError("error_details_type_mismatch")
        rejected = tuple(row.fix_id for row in self.results if row.reason == "invalid_request")
        if self.success == bool(rejected):
            raise ValueError("internal_rejection_determines_operational_failure")
        if isinstance(self.error_details, RejectedFixRequestDetails):
            if rejected != (self.error_details.fix_id,):
                raise ValueError("rejection_details_must_match_row")
        elif rejected and self.error_code != "termination_unconfirmed":
            raise ValueError("rejected_request_requires_operation_error")
        interrupted = tuple(row.fix_id for row in self.results if row.reason == "interrupted")
        unconfirmed = tuple(
            row.fix_id
            for row in self.results
            if row.termination_problem is TerminationProblem.UNCONFIRMED
        )
        if isinstance(self.error_details, FixTerminationDetails):
            affected = interrupted if self.error_details.interrupted else unconfirmed + rejected
            if affected != (self.error_details.fix_id,):
                raise ValueError("termination_details_must_match_observed_row")
        elif unconfirmed:
            raise ValueError("unconfirmed_termination_requires_operation_error")
        if interrupted and self.error_code not in {
            "operation_interrupted",
            "termination_unconfirmed",
        }:
            raise ValueError("interruption_requires_operation_error")
        # Cancellation may precede every attempt, leaving all rows not_started.
        if self.error_code == "operation_interrupted" and not any(
            row.reason in {"not_started", "interrupted"} for row in self.results
        ):
            raise ValueError("interruption_requires_unfinished_work")
        return self
