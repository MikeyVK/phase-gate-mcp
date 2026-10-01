"""Resolve test bindings and preserve native facts through the shared runtime."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, StrictInt, model_validator

from mcp_server.config.schemas.adapter_manifest import TestCapability
from mcp_server.config.schemas.tests_config import TestId, TestsConfig
from mcp_server.core.interfaces.execution import AdapterBinding, ScopePaths, TestCatalogReader
from mcp_server.execution.check_selection import (
    ArgsSource,
    CheckSelectionError,
    NativeArguments,
    WorkspaceRelativePath,
)
from mcp_server.execution.models import (
    AdapterCallFailureReason,
    AdapterExitCode,
    AdapterRunIdentity,
    AdapterUnavailableReason,
    ConsumerNotExecutedReason,
    ExternalToolIdentity,
    InvalidCheckRequest,
    InvocationCancelled,
    InvocationCompleted,
    InvocationFailed,
    NativeEvidence,
    ProcessCapture,
    PublicTestResult,
    RejectedTestRequestDetails,
    RequestValidationIssue,
    RunTestsErrorCode,
    RunTestsOutput,
    ScopeDetails,
    ScopeIssue,
    TerminationProblem,
    TestRequest,
    TestResponse,
    TestScope,
    TestSelectionDetails,
    TestSelectionIssue,
    TestTerminationDetails,
    TestUnavailable,
)
from mcp_server.execution.process_runtime import AdapterProcessRuntime
from mcp_server.execution.protocol import (
    AdapterRequestContract,
    AdapterResponseContract,
    TestWireRequest,
)


def _sequence(value: object) -> object:
    return tuple(value) if isinstance(value, list) else value


def _arguments(value: object) -> object:
    return tuple(value.items()) if isinstance(value, dict) else value


class TestSelectionRequest(BaseModel):
    """Caller intent; native option meaning remains opaque."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    scope: TestScope
    targets: (
        Annotated[
            tuple[WorkspaceRelativePath, ...], BeforeValidator(_sequence), Field(min_length=1)
        ]
        | None
    ) = None
    tests: Annotated[tuple[TestId, ...], BeforeValidator(_sequence), Field(min_length=1)] | None = (
        None
    )
    args: (
        Annotated[tuple[tuple[TestId, NativeArguments], ...], BeforeValidator(_arguments)] | None
    ) = None
    timeout_seconds: Annotated[StrictInt, Field(gt=0)] | None = None

    @model_validator(mode="after")
    def validate_selection(self) -> TestSelectionRequest:
        for name in ("targets", "tests", "args", "timeout_seconds"):
            if name in self.model_fields_set and getattr(self, name) is None:
                raise ValueError(f"{name}_must_be_omitted")
        if (self.scope == "targets") != (self.targets is not None):
            raise ValueError("targets_required_only_for_targets_scope")
        if any(not PurePosixPath(path.replace("\\", "/")).parts for path in self.targets or ()):
            raise ValueError("workspace_root_requires_workspace_scope")
        if self.tests is not None and len(set(self.tests)) != len(self.tests):
            raise ValueError("duplicate_test_selection")
        if self.args is not None and len(dict(self.args)) != len(self.args):
            raise ValueError("duplicate_argument_recipient")
        return self


@dataclass(frozen=True)
class _SelectedTest:
    test_id: str
    binding: AdapterBinding[TestCapability]
    args: tuple[str, ...]
    args_source: ArgsSource
    timeout_seconds: int


def _scope(
    paths: ScopePaths, request: TestSelectionRequest
) -> tuple[tuple[str, ...], tuple[ScopeIssue, ...]]:
    if request.scope == "configured":
        return (), ()
    if request.scope == "workspace":
        return (str(paths.workspace_root),), ()
    targets: list[str] = []
    issues: list[ScopeIssue] = []
    for target in request.targets or ():
        try:
            resolved = paths.resolve(target)
        except CheckSelectionError:
            # This port does not distinguish an escape from an alias to the root.
            issues.append(
                ScopeIssue(
                    target=target,
                    reason="unresolvable",
                    message="Target cannot be admitted as a contained non-root workspace path.",
                )
            )
        except OSError:
            issues.append(
                ScopeIssue(
                    target=target,
                    reason="unresolvable",
                    message="Target could not be resolved.",
                )
            )
        else:
            if not resolved.exists:
                issues.append(
                    ScopeIssue(
                        target=target,
                        reason="missing",
                        message="Requested target does not exist.",
                    )
                )
            else:
                targets.append(str(resolved.path))
    return tuple(dict.fromkeys(targets)), tuple(issues)


def _expected_exit(response: TestResponse) -> AdapterExitCode:
    if isinstance(response.root, InvalidCheckRequest):
        return AdapterExitCode.INVALID_REQUEST
    return {
        "passed": AdapterExitCode.SUCCESS,
        "failed": AdapterExitCode.NEGATIVE_RESULT,
        "unavailable": AdapterExitCode.UNAVAILABLE,
    }[response.root.decision.status]


def _project(
    selected: _SelectedTest,
    invocation: InvocationCompleted[TestResponse] | InvocationFailed | InvocationCancelled | None,
) -> PublicTestResult:
    status: Literal["passed", "failed", "unavailable", "not_executed"] = "not_executed"
    reason: (
        AdapterUnavailableReason | AdapterCallFailureReason | ConsumerNotExecutedReason | None
    ) = "not_started"
    message: str | None = None
    evidence: NativeEvidence | None = None
    external_tools: tuple[ExternalToolIdentity, ...] | None = None
    adapter: AdapterRunIdentity | None = None
    capture: ProcessCapture | None = None
    termination: TerminationProblem | None = None
    rejection: tuple[RequestValidationIssue, ...] | None = None
    if invocation is not None:
        binding = selected.binding
        adapter = AdapterRunIdentity.model_validate(
            {
                "adapter_id": binding.identity.adapter_id,
                "version": binding.identity.version,
                "fingerprint": binding.identity.fingerprint,
                "contract_version": binding.contract_version,
            }
        )
        capture = invocation.capture
        if isinstance(invocation, InvocationCancelled):
            reason = "interrupted"
        elif isinstance(invocation, InvocationFailed):
            status, reason, message = (
                "unavailable",
                invocation.failure.reason,
                invocation.failure.message,
            )
            termination = invocation.termination_problem
        elif isinstance(invocation.response.root, InvalidCheckRequest):
            reason = "invalid_request"
            rejection = invocation.response.root.details
        else:
            response = invocation.response.root
            status = response.decision.status
            reason = (
                response.decision.reason if isinstance(response.decision, TestUnavailable) else None
            )
            message, evidence, external_tools = (
                response.decision.message,
                response.evidence,
                response.external_tools,
            )
    return PublicTestResult(
        test_id=selected.test_id,
        status=status,
        reason=reason,
        message=message,
        evidence=evidence,
        external_tools=external_tools,
        adapter=adapter,
        capture=capture,
        termination_problem=termination,
        request_rejection=rejection,
        args_source=selected.args_source,
        effective_args=selected.args,
    )


class TestRunManager:
    """Own test selection, sequential calls and concrete result projection."""

    def __init__(
        self,
        config: TestsConfig,
        catalog: TestCatalogReader,
        runtime: AdapterProcessRuntime,
        paths: ScopePaths,
    ) -> None:
        self._config = config
        self._catalog = catalog
        self._runtime = runtime
        self._paths = paths

    async def run(self, request: TestSelectionRequest) -> RunTestsOutput:
        definitions = dict(self._config.tests)
        selected_ids = (
            request.tests
            if request.tests is not None
            else tuple(test_id for test_id, binding in self._config.tests if binding.active)
        )
        overrides = dict(request.args or ())
        issues = tuple(
            TestSelectionIssue(field="tests", test_id=test_id, reason="unknown_test")
            for test_id in selected_ids
            if test_id not in definitions
        ) + tuple(
            TestSelectionIssue(
                field="args",
                test_id=test_id,
                reason="unknown_test" if test_id not in definitions else "unselected_args",
            )
            for test_id in overrides
            if test_id not in selected_ids
        )
        if issues or not selected_ids:
            code: RunTestsErrorCode = (
                "selection_invalid"
                if issues
                else "no_configured_tests"
                if not definitions
                else "no_active_tests"
            )
            return RunTestsOutput(
                success=True,
                requested_scope=request.scope,
                requested_targets=request.targets or (),
                selected_tests=(),
                results=(),
                error_code=code,
                error_details=TestSelectionDetails(issues=issues) if issues else None,
            )
        selected = tuple(
            _SelectedTest(
                test_id,
                self._catalog.get_test(
                    definitions[test_id].adapter_id, definitions[test_id].capability
                ),
                overrides.get(test_id, definitions[test_id].default_args),
                "caller" if test_id in overrides else "configured",
                request.timeout_seconds or definitions[test_id].timeout_seconds,
            )
            for test_id in selected_ids
        )
        targets, scope_issues = _scope(self._paths, request)
        if scope_issues:
            return RunTestsOutput(
                success=True,
                requested_scope=request.scope,
                requested_targets=request.targets or (),
                selected_tests=selected_ids,
                results=tuple(_project(item, None) for item in selected),
                error_code="scope_resolution_failed",
                error_details=ScopeDetails(issues=scope_issues),
            )
        rows: list[PublicTestResult] = []
        stop: RunTestsErrorCode | None = None
        details: RejectedTestRequestDetails | TestTerminationDetails | None = None
        success = True
        for item in selected:
            invocation = None
            if stop is None:
                invocation = await self._runtime.invoke(
                    launch=item.binding.launch,
                    workspace_root=self._paths.workspace_root,
                    request=TestRequest(
                        operation=item.binding.capability_id,
                        targets=targets,
                        args=item.args,
                    ),
                    request_contract=AdapterRequestContract(TestWireRequest),
                    response_contract=AdapterResponseContract(
                        TestResponse,
                        InvocationCompleted[TestResponse],
                        _expected_exit,
                    ),
                    timeout_seconds=item.timeout_seconds,
                )
                if isinstance(invocation, (InvocationFailed, InvocationCancelled)):
                    if invocation.termination_problem is TerminationProblem.UNCONFIRMED:
                        stop = "termination_unconfirmed"
                        details = TestTerminationDetails(
                            test_ids=(item.test_id,),
                            interrupted=isinstance(invocation, InvocationCancelled),
                        )
                    elif isinstance(invocation, InvocationCancelled):
                        stop = "operation_interrupted"
                elif isinstance(invocation.response.root, InvalidCheckRequest):
                    stop = "adapter_request_rejected"
                    details = RejectedTestRequestDetails(test_id=item.test_id)
                    success = False
            rows.append(_project(item, invocation))
        return RunTestsOutput(
            success=success,
            requested_scope=request.scope,
            requested_targets=request.targets or (),
            selected_tests=selected_ids,
            results=tuple(rows),
            error_code=stop,
            error_details=details,
        )
