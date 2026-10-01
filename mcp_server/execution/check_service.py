"""Execute configured checks while retaining role and invocation facts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel

from mcp_server.config.schemas.adapter_manifest import CheckCapability
from mcp_server.config.schemas.checks_config import ChecksConfig
from mcp_server.core.interfaces.execution import AdapterBinding, CheckCatalogReader
from mcp_server.execution.check_selection import ArgsSource, CheckSelectionPlan, ResolvedCheckScope
from mcp_server.execution.content_input import (
    CleanupProblem,
    ContentInputPreparer,
    ScaffoldTextRequest,
)
from mcp_server.execution.models import (
    AdapterExitCode,
    ContentCheckResponse,
    InvalidCheckRequest,
    InvocationCancelled,
    InvocationCompleted,
    InvocationFailed,
    SelectionCheckResponse,
    TerminationProblem,
)
from mcp_server.execution.process_runtime import AdapterProcessRuntime
from mcp_server.execution.protocol import (
    AdapterRequestContract,
    AdapterResponseContract,
    ContentFileCheckWireRequest,
    ContentTextCheckWireRequest,
    SelectionCheckWireRequest,
)

TRequest = TypeVar("TRequest", bound=BaseModel)
TCheck = TypeVar("TCheck", ContentCheckResponse, SelectionCheckResponse)
StopReason = Literal["adapter_request_rejected", "operation_interrupted", "termination_unconfirmed"]
SelectionStatus = Literal["passed", "failed", "incomplete", "empty_selection"]


@dataclass(frozen=True)
class CheckExecution(Generic[TCheck]):
    """A known obligation and its optional factual invocation; no fabricated response."""

    check_id: str
    binding: AdapterBinding[CheckCapability]
    effective_args: tuple[str, ...]
    args_source: ArgsSource
    timeout_seconds: int
    invocation: InvocationCompleted[TCheck] | InvocationFailed | InvocationCancelled | None
    not_executed: Literal["not_started"] | None


@dataclass(frozen=True)
class ContentCheckExecution(CheckExecution[ContentCheckResponse]):
    cleanup_problem: CleanupProblem | None


@dataclass(frozen=True)
class SelectionExecution:
    scope: ResolvedCheckScope
    results: tuple[CheckExecution[SelectionCheckResponse], ...]
    run_status: SelectionStatus
    stop_reason: StopReason | None


@dataclass(frozen=True)
class ContentExecution:
    results: tuple[ContentCheckExecution, ...]
    stop_reason: StopReason | Literal["content_preparation_failed"] | None


class ContentPreparationError(RuntimeError):
    """Operation failure carrying completed facts and all known unstarted obligations."""

    def __init__(self, check_id: str, execution: ContentExecution) -> None:
        super().__init__(f"Content preparation failed for {check_id}")
        self.check_id = check_id
        self.execution = execution


def _expected_exit(response: ContentCheckResponse | SelectionCheckResponse) -> AdapterExitCode:
    if isinstance(response.root, InvalidCheckRequest):
        return AdapterExitCode.INVALID_REQUEST
    return {
        "passed": AdapterExitCode.SUCCESS,
        "failed": AdapterExitCode.NEGATIVE_RESULT,
        "unavailable": AdapterExitCode.UNAVAILABLE,
        "not_executed": AdapterExitCode.UNAVAILABLE,
    }[response.root.decision.status]


def _stop_reason(
    invocation: InvocationCompleted[TCheck] | InvocationFailed | InvocationCancelled,
) -> StopReason | None:
    if isinstance(invocation, (InvocationFailed, InvocationCancelled)):
        if invocation.termination_problem is TerminationProblem.UNCONFIRMED:
            return "termination_unconfirmed"
        if isinstance(invocation, InvocationCancelled):
            return "operation_interrupted"
    elif isinstance(invocation.response.root, InvalidCheckRequest):
        return "adapter_request_rejected"
    return None


def _selection_status(
    results: tuple[CheckExecution[SelectionCheckResponse], ...],
) -> SelectionStatus:
    negative = False
    incomplete = False
    for row in results:
        invocation = row.invocation
        if not isinstance(invocation, InvocationCompleted):
            incomplete = True
            continue
        response = invocation.response.root
        if isinstance(response, InvalidCheckRequest) or response.decision.status in {
            "unavailable",
            "not_executed",
        }:
            incomplete = True
        elif response.decision.status == "failed":
            negative = True
    if incomplete:
        return "incomplete"
    return "failed" if negative else "passed"


class CheckService:
    """Shared factual executor for explicit selection and configured content profiles."""

    def __init__(
        self,
        config: ChecksConfig,
        catalog: CheckCatalogReader,
        runtime: AdapterProcessRuntime,
        content: ContentInputPreparer,
        workspace_root: Path,
    ) -> None:
        if not workspace_root.is_absolute():
            raise ValueError("absolute_workspace_required")
        self._config = config
        self._catalog = catalog
        self._runtime = runtime
        self._content = content
        self._workspace_root = workspace_root

    async def _invoke(
        self,
        binding: AdapterBinding[CheckCapability],
        request: TRequest,
        request_contract: AdapterRequestContract[TRequest],
        contract: AdapterResponseContract[TCheck],
        timeout_seconds: int,
    ) -> InvocationCompleted[TCheck] | InvocationFailed | InvocationCancelled:
        return await self._runtime.invoke(
            launch=binding.launch,
            workspace_root=self._workspace_root,
            request=request,
            request_contract=request_contract,
            response_contract=contract,
            timeout_seconds=timeout_seconds,
        )

    async def run_selection(self, plan: CheckSelectionPlan) -> SelectionExecution:
        """Execute already-resolved obligations; an empty branch never launches discovery."""
        if plan.empty_selection:
            return SelectionExecution(plan.scope, (), "empty_selection", None)
        if not plan.calls:
            raise ValueError("nonempty_check_obligations_required")
        rows: list[CheckExecution[SelectionCheckResponse]] = []
        stop: StopReason | None = None
        for call in plan.calls:
            invocation = None
            if stop is None:
                invocation = await self._invoke(
                    call.binding,
                    call.request,
                    AdapterRequestContract(SelectionCheckWireRequest),
                    AdapterResponseContract(
                        SelectionCheckResponse,
                        InvocationCompleted[SelectionCheckResponse],
                        _expected_exit,
                    ),
                    call.timeout_seconds,
                )
                stop = _stop_reason(invocation)
            rows.append(
                CheckExecution(
                    check_id=call.check_id,
                    binding=call.binding,
                    effective_args=call.request.args,
                    args_source=call.args_source,
                    timeout_seconds=call.timeout_seconds,
                    invocation=invocation,
                    not_executed="not_started" if invocation is None else None,
                )
            )
        results = tuple(rows)
        return SelectionExecution(plan.scope, results, _selection_status(results), stop)

    async def run_content(
        self,
        profile_id: str,
        *,
        target_path: str,
        content: str,
    ) -> ContentExecution:
        """Use only configured bindings; mutation policy and summary stay with the consumer."""
        profiles = dict(self._config.profiles)
        if profile_id not in profiles:
            raise ValueError("unknown_content_profile")
        declarations = dict(self._config.checks)
        calls = tuple(
            (
                check_id,
                declarations[check_id],
                self._catalog.get_check(
                    declarations[check_id].adapter_id,
                    declarations[check_id].capability,
                ),
            )
            for check_id in profiles[profile_id].checks
        )
        # Admit the complete obligation set before preparing content or invoking an adapter.
        if any("content" not in binding.capability.inputs for _, _, binding in calls):
            raise ValueError("content_input_not_supported")
        rows: list[ContentCheckExecution] = []
        stop: StopReason | Literal["content_preparation_failed"] | None = None
        preparation_failure: tuple[str, Exception] | None = None
        for check_id, declaration, binding in calls:
            invocation = None
            cleanup = None
            if stop is None:
                try:
                    prepared = self._content.prepare(
                        binding,
                        target_path=target_path,
                        content=content,
                        args=declaration.default_args,
                    )
                except (OSError, ValueError) as exc:
                    preparation_failure = (check_id, exc)
                    stop = "content_preparation_failed"
                else:
                    invocation = await self._invoke(
                        binding,
                        prepared.request,
                        AdapterRequestContract(
                            ContentTextCheckWireRequest
                            if isinstance(prepared.request, ScaffoldTextRequest)
                            else ContentFileCheckWireRequest
                        ),
                        AdapterResponseContract(
                            ContentCheckResponse,
                            InvocationCompleted[ContentCheckResponse],
                            _expected_exit,
                        ),
                        declaration.timeout_seconds,
                    )
                    cleanup = self._content.cleanup(prepared, invocation)
                    stop = _stop_reason(invocation)
            rows.append(
                ContentCheckExecution(
                    check_id=check_id,
                    binding=binding,
                    effective_args=declaration.default_args,
                    args_source="configured",
                    timeout_seconds=declaration.timeout_seconds,
                    invocation=invocation,
                    not_executed="not_started" if invocation is None else None,
                    cleanup_problem=cleanup,
                )
            )
        result = ContentExecution(tuple(rows), stop)
        if preparation_failure is not None:
            failed_check, cause = preparation_failure
            raise ContentPreparationError(failed_check, result) from cause
        return result
