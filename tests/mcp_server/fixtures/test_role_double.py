"""Narrow test-role values and a direct recording runtime for consumer proofs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field, RootModel, SerializerFunctionWrapHandler, model_serializer, model_validator

from mcp_server.core.interfaces.execution import AdapterLaunch
from mcp_server.execution.models import (
    AdapterExitCode, AdapterUnavailableReason, ExternalToolIdentity, InvalidCheckRequest,
    InvocationCompleted, NativeEvidence, NonBlankText, ProcessCapture, StreamCapture,
)
from mcp_server.execution.process_runtime import AdapterProcessRuntime
from mcp_server.execution.protocol import AdapterResponseContract


class RoleValue(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")


class NativePassed(RoleValue):
    status: Literal["passed"]
    message: NonBlankText


class NativeFailed(RoleValue):
    status: Literal["failed"]
    message: NonBlankText


class NativeUnavailable(RoleValue):
    status: Literal["unavailable"]
    reason: AdapterUnavailableReason
    message: NonBlankText


class NativeTestResult(RoleValue):
    decision: Annotated[NativePassed | NativeFailed | NativeUnavailable, Field(discriminator="status")]
    external_tools: tuple[ExternalToolIdentity, ...]
    evidence: NativeEvidence | None = None

    @model_validator(mode="after")
    def validate_evidence(self) -> NativeTestResult:
        if self.evidence is None and ("evidence" in self.model_fields_set or self.decision.status == "failed"):
            raise ValueError("evidence_missing_or_null")
        return self

    @model_serializer(mode="wrap")
    def serialize_evidence(self, handler: SerializerFunctionWrapHandler) -> dict[str, object]:
        result: dict[str, object] = handler(self)
        if self.evidence is None:
            result.pop("evidence", None)
        return result


class NativeTestResponse(RootModel[NativeTestResult | InvalidCheckRequest]):
    model_config = ConfigDict(frozen=True, strict=True)


def native_exit(response: NativeTestResponse) -> AdapterExitCode:
    if isinstance(response.root, InvalidCheckRequest):
        return AdapterExitCode.INVALID_REQUEST
    return {"passed": AdapterExitCode.SUCCESS, "failed": AdapterExitCode.NEGATIVE_RESULT,
            "unavailable": AdapterExitCode.UNAVAILABLE}[response.root.decision.status]


def role_response_contract() -> AdapterResponseContract[NativeTestResponse]:
    return AdapterResponseContract(NativeTestResponse, InvocationCompleted[NativeTestResponse], native_exit)


@dataclass(frozen=True)
class RecordedTestCall:
    launch: AdapterLaunch
    workspace_root: Path
    request: BaseModel
    timeout_seconds: float


TResponse = TypeVar("TResponse", bound=BaseModel)


class RecordingTestRuntime(AdapterProcessRuntime):
    """Return declared role bytes through the consumer's actual response contract."""

    def __init__(self, answers: tuple[tuple[bytes, int], ...]) -> None:
        self.answers = iter(answers)
        self.calls: list[RecordedTestCall] = []

    async def invoke(
        self, *, launch: AdapterLaunch, workspace_root: Path, request: BaseModel,
        response_contract: AdapterResponseContract[TResponse], timeout_seconds: float,
    ) -> InvocationCompleted[TResponse]:
        self.calls.append(RecordedTestCall(launch, workspace_root, request, timeout_seconds))
        raw, code = next(self.answers)
        empty = StreamCapture(observed_bytes=0, head="", tail="", truncated=False)
        accepted = StreamCapture(observed_bytes=len(raw), head=None, tail=None, truncated=False)
        capture = ProcessCapture(exit_code=code, stdout=accepted, stderr=empty)
        return response_contract.complete(response_contract.decode(raw, code), capture)
