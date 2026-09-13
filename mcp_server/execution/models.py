"""Immutable generic adapter process invocation models."""

from __future__ import annotations

from enum import IntEnum, StrEnum
from typing import Annotated, Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr, model_validator


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
        if self.capture.exit_code not in {0, 1, 2, 3}:
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
