"""Immutable generic adapter process invocation models."""

from __future__ import annotations

from enum import IntEnum, StrEnum
from typing import Annotated, Generic, Literal, TypeVar

from pydantic import (
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

from mcp_server.core.interfaces.template_catalog import (
    FrozenJsonObject,
    FrozenJsonValue,
    freeze_json,
    thaw_json,
)
from mcp_server.execution.check_selection import WorkspaceRelativePath


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

    @model_validator(mode="after")
    def validate_failure(self) -> InvocationFailed:
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
