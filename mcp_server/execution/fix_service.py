"""Admit concrete files and execute ordered fixes until the first non-success."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, StrictInt, model_validator

from mcp_server.config.schemas.adapter_manifest import FixCapability
from mcp_server.config.schemas.fixes_config import FixesConfig, FixId
from mcp_server.core.interfaces.execution import AdapterBinding, FixCatalogReader, FixScopePaths
from mcp_server.execution.check_selection import (
    ArgsSource,
    CheckSelectionError,
    FileScopePaths,
    NativeArguments,
)
from mcp_server.execution.models import (
    AdapterCallFailureReason,
    AdapterExitCode,
    AdapterRunIdentity,
    AdapterUnavailableReason,
    ApplyFixesErrorCode,
    ApplyFixesOutput,
    ConsumerNotExecutedReason,
    ExternalToolIdentity,
    FixPassed,
    FixRequest,
    FixResponse,
    FixScopeDetails,
    FixScopeIssue,
    FixSelectionDetails,
    FixSelectionIssue,
    FixTerminationDetails,
    FixUnavailable,
    InvalidCheckRequest,
    InvocationCancelled,
    InvocationCompleted,
    InvocationFailed,
    NativeEvidence,
    ProcessCapture,
    PublicFixResult,
    RejectedFixRequestDetails,
    RequestValidationIssue,
    TerminationProblem,
    WorkspaceRelativeFilePath,
)
from mcp_server.execution.process_runtime import AdapterProcessRuntime
from mcp_server.execution.protocol import AdapterResponseContract


def _sequence(value: object) -> object:
    return tuple(value) if isinstance(value, list) else value


def _arguments(value: object) -> object:
    return tuple(value.items()) if isinstance(value, dict) else value


class FixSelectionRequest(BaseModel):
    """Caller intent; native option meaning remains opaque."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    scope: Literal["targets"]
    targets: Annotated[
        tuple[WorkspaceRelativeFilePath, ...], BeforeValidator(_sequence), Field(min_length=1)
    ]
    fixes: Annotated[tuple[FixId, ...], BeforeValidator(_sequence), Field(min_length=1)]
    args: (
        Annotated[tuple[tuple[FixId, NativeArguments], ...], BeforeValidator(_arguments)] | None
    ) = None
    timeout_seconds: Annotated[StrictInt, Field(gt=0)] | None = None

    @model_validator(mode="after")
    def validate_selection(self) -> FixSelectionRequest:
        for name in ("args", "timeout_seconds"):
            if name in self.model_fields_set and getattr(self, name) is None:
                raise ValueError(f"{name}_must_be_omitted")
        if len(set(self.fixes)) != len(self.fixes):
            raise ValueError("duplicate_fix_selection")
        if self.args is not None and len(dict(self.args)) != len(self.args):
            raise ValueError("duplicate_argument_recipient")
        return self


@dataclass(frozen=True)
class _SelectedFix:
    fix_id: str
    binding: AdapterBinding[FixCapability]
    args: tuple[str, ...]
    args_source: ArgsSource
    timeout_seconds: int


class FileFixScopePaths(FileScopePaths):
    """Concrete read-only fix filesystem adapter."""

    def is_file(self, path: Path) -> bool:
        return path.is_file()


def _scope(
    paths: FixScopePaths, request: FixSelectionRequest
) -> tuple[tuple[str, ...], tuple[FixScopeIssue, ...]]:
    targets: list[Path] = []
    issues: list[FixScopeIssue] = []
    for target in request.targets or ():
        try:
            resolved = paths.resolve(target)
            is_file = paths.is_file(resolved.path) if resolved.exists else False
        except CheckSelectionError:
            # This port does not distinguish an escape from an alias to the root.
            issues.append(
                FixScopeIssue(
                    target=target,
                    reason="unresolvable",
                    message="Target cannot be admitted as a contained non-root workspace path.",
                )
            )
        except OSError:
            issues.append(
                FixScopeIssue(
                    target=target,
                    reason="unresolvable",
                    message="Target could not be resolved.",
                )
            )
        else:
            if not resolved.exists:
                issues.append(
                    FixScopeIssue(
                        target=target,
                        reason="missing",
                        message="Requested target does not exist.",
                    )
                )
            elif not is_file:
                issues.append(
                    FixScopeIssue(
                        target=target,
                        reason="not_file",
                        message="Requested target is not a regular file.",
                    )
                )
            else:
                targets.append(resolved.path)
    return tuple(str(path) for path in dict.fromkeys(targets)), tuple(issues)


def _expected_exit(response: FixResponse) -> AdapterExitCode:
    if isinstance(response.root, InvalidCheckRequest):
        return AdapterExitCode.INVALID_REQUEST
    return {
        "passed": AdapterExitCode.SUCCESS,
        "failed": AdapterExitCode.NEGATIVE_RESULT,
        "unavailable": AdapterExitCode.UNAVAILABLE,
    }[response.root.decision.status]


def _project(
    selected: _SelectedFix,
    invocation: InvocationCompleted[FixResponse] | InvocationFailed | InvocationCancelled | None,
) -> PublicFixResult:
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
                response.decision.reason if isinstance(response.decision, FixUnavailable) else None
            )
            message, evidence, external_tools = (
                None if isinstance(response.decision, FixPassed) else response.decision.message,
                response.evidence,
                response.external_tools,
            )
    return PublicFixResult(
        fix_id=selected.fix_id,
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


class FixManager:
    """Own fix selection, sequential calls and concrete result projection."""

    def __init__(
        self,
        config: FixesConfig,
        catalog: FixCatalogReader,
        runtime: AdapterProcessRuntime,
        paths: FixScopePaths,
    ) -> None:
        self._config = config
        self._catalog = catalog
        self._runtime = runtime
        self._paths = paths

    async def run(self, request: FixSelectionRequest) -> ApplyFixesOutput:
        definitions = dict(self._config.fixes)
        selected_ids = request.fixes
        overrides = dict(request.args or ())
        issues = tuple(
            FixSelectionIssue(field="fixes", fix_id=fix_id, reason="unknown_fix")
            for fix_id in selected_ids
            if fix_id not in definitions
        ) + tuple(
            FixSelectionIssue(
                field="args",
                fix_id=fix_id,
                reason="unknown_fix" if fix_id not in definitions else "unselected_args",
            )
            for fix_id in overrides
            if fix_id not in selected_ids
        )
        if not definitions or issues:
            code: ApplyFixesErrorCode | None = (
                "no_configured_fixes" if not definitions else "selection_invalid"
            )
            return ApplyFixesOutput(
                success=True,
                requested_scope=request.scope,
                requested_targets=request.targets,
                selected_fixes=(),
                results=(),
                error_code=code,
                error_details=FixSelectionDetails(issues=issues) if definitions else None,
            )
        selected = tuple(
            _SelectedFix(
                fix_id,
                self._catalog.get_fix(
                    definitions[fix_id].adapter_id, definitions[fix_id].capability
                ),
                overrides.get(fix_id, definitions[fix_id].default_args),
                "caller" if fix_id in overrides else "configured",
                request.timeout_seconds or definitions[fix_id].timeout_seconds,
            )
            for fix_id in selected_ids
        )
        # Whole selection is admitted before the first possible write.
        targets, scope_issues = _scope(self._paths, request)
        rows: list[PublicFixResult] = []
        code = "scope_resolution_failed" if scope_issues else None
        details: FixScopeDetails | RejectedFixRequestDetails | FixTerminationDetails | None = (
            FixScopeDetails(issues=scope_issues) if scope_issues else None
        )
        stopped = bool(scope_issues)
        success = True
        for index, item in enumerate(selected):
            invocation = None
            if not stopped and index:
                # Re-resolve caller paths, including containment, against current disk state.
                targets, scope_issues = _scope(self._paths, request)
                if scope_issues:
                    code, stopped = "scope_resolution_failed", True
                    details = FixScopeDetails(issues=scope_issues)
            if not stopped:
                task = asyncio.current_task()
                if task is not None and task.cancelling():
                    code, stopped = "operation_interrupted", True
            if not stopped:
                invocation = await self._runtime.invoke(
                    launch=item.binding.launch,
                    workspace_root=self._paths.workspace_root,
                    request=FixRequest(
                        operation=item.binding.capability_id, targets=targets, args=item.args
                    ),
                    response_contract=AdapterResponseContract(
                        FixResponse, InvocationCompleted[FixResponse], _expected_exit
                    ),
                    timeout_seconds=item.timeout_seconds,
                )
                if isinstance(invocation, (InvocationFailed, InvocationCancelled)):
                    stopped = True
                    if invocation.termination_problem is TerminationProblem.UNCONFIRMED:
                        code = "termination_unconfirmed"
                        details = FixTerminationDetails(
                            fix_id=item.fix_id,
                            interrupted=isinstance(invocation, InvocationCancelled),
                        )
                    elif isinstance(invocation, InvocationCancelled):
                        code = "operation_interrupted"
                elif isinstance(invocation.response.root, InvalidCheckRequest):
                    code, stopped, success = "adapter_request_rejected", True, False
                    details = RejectedFixRequestDetails(fix_id=item.fix_id)
                elif invocation.response.root.decision.status != "passed":
                    stopped = True
            rows.append(_project(item, invocation))
        return ApplyFixesOutput(
            success=success,
            requested_scope=request.scope,
            requested_targets=request.targets,
            selected_fixes=selected_ids,
            results=tuple(rows),
            error_code=code,
            error_details=details,
        )
