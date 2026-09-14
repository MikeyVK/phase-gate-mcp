"""Apply scaffold persistence policy to factual render, check and filesystem outcomes."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Literal

from jinja2 import TemplateError
from jsonschema.exceptions import ValidationError as ContextError

from mcp_server.core.interfaces.execution import ScratchPreparationError
from mcp_server.core.interfaces.file_writer import (
    FileCreationCollisionError,
    FileCreationError,
    IArtifactFileCreator,
    WriteHousekeepingIssue,
)
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json
from mcp_server.execution.check_service import (
    CheckService,
    ContentCheckExecution,
    ContentExecution,
    ContentPreparationError,
)
from mcp_server.execution.models import (
    AdapterCallFailureReason,
    AdapterRunIdentity,
    AdapterUnavailableReason,
    CheckFailed,
    CheckUnavailable,
    ConsumerNotExecutedReason,
    InvalidCheckRequest,
    InvocationCancelled,
    InvocationCompleted,
    InvocationFailed,
    NativeEvidence,
)
from mcp_server.schemas.mutation_outputs import (
    AffectedPathDetails,
    ContextDetails,
    ContextIssue,
    HousekeepingIssue,
    InputPreparationDetails,
    InvocationEvidence,
    MutationCheck,
    MutationErrorCode,
    MutationErrorDetails,
    PersistenceDetails,
    RejectedRequestDetails,
    RenderDetails,
    ScaffoldOperationOutput,
    TargetDetails,
    TerminationDetails,
)
from mcp_server.services.artifact_identity import ArtifactIdentity
from mcp_server.services.artifact_target_resolver import ArtifactTargetResolver
from mcp_server.services.template_catalog import TemplateCatalog
from mcp_server.utils.path_resolver import ArtifactTargetError

ValidationPolicy = Literal["enforce", "report"]
ValidationStatus = Literal["passed", "failed", "unavailable", "not_executed"]


def validation_status(checks: tuple[MutationCheck, ...]) -> ValidationStatus:
    """Reduce obligations without treating collection absence as acceptance."""
    priorities: tuple[ValidationStatus, ...] = ("failed", "unavailable", "not_executed")
    for status in priorities:
        if any(check.status == status for check in checks):
            return status
    return "passed" if checks else "not_executed"


def _project_check(
    row: ContentCheckExecution,
    workspace_root: Path,
    *,
    preparation_cleanup: tuple[Path, str] | None = None,
) -> MutationCheck:
    """Retain runtime facts without reclassifying native evidence or process failures."""
    housekeeping: tuple[HousekeepingIssue, ...] = (
        (
            HousekeepingIssue(
                purpose="validation_input",
                path=row.cleanup_problem.directory.relative_to(workspace_root).as_posix(),
                message=row.cleanup_problem.message,
            ),
        )
        if row.cleanup_problem is not None
        else ()
    )
    if preparation_cleanup is not None:
        directory, cleanup_message = preparation_cleanup
        housekeeping += (
            HousekeepingIssue(
                purpose="validation_input",
                path=directory.relative_to(workspace_root).as_posix(),
                message=cleanup_message,
            ),
        )
    if row.args_source != "configured" or row.binding.contract_version != 1:
        raise ValueError("mutation_check_binding_facts_invalid")
    observation = row.invocation
    invocation = None
    termination = None
    rejection = None
    evidence: NativeEvidence | None = None
    status: ValidationStatus = "not_executed"
    reason: (
        AdapterUnavailableReason | AdapterCallFailureReason | ConsumerNotExecutedReason | None
    ) = "not_started"
    message: str | None = "Check was not started because the operation stopped."
    if observation is not None:
        response = (
            observation.response.root if isinstance(observation, InvocationCompleted) else None
        )
        invocation = InvocationEvidence(
            adapter=AdapterRunIdentity(
                adapter_id=row.binding.identity.adapter_id,
                version=row.binding.identity.version,
                fingerprint=row.binding.identity.fingerprint,
                contract_version=1,
            ),
            capture=observation.capture,
            external_tools=(
                response.external_tools
                if response is not None and not isinstance(response, InvalidCheckRequest)
                else None
            ),
        )
        if isinstance(observation, InvocationFailed):
            status = "unavailable"
            reason = observation.failure.reason
            message = observation.failure.message
            termination = observation.termination_problem
        elif isinstance(observation, InvocationCancelled):
            reason = "interrupted"
            message = "Check execution was interrupted."
            termination = observation.termination_problem
        elif isinstance(response, InvalidCheckRequest):
            reason = "invalid_request"
            message = None
            rejection = response.details
        elif response is not None:
            decision = response.decision
            status = decision.status
            reason = decision.reason if isinstance(decision, CheckUnavailable) else None
            message = (
                decision.message if isinstance(decision, (CheckFailed, CheckUnavailable)) else None
            )
            evidence = response.evidence
    return MutationCheck(
        check_id=row.check_id,
        status=status,
        reason=reason,
        message=message,
        evidence=evidence,
        request_rejection=rejection,
        invocation=invocation,
        termination_problem=termination,
        housekeeping=housekeeping,
        args_source=row.args_source,
        effective_args=row.effective_args,
    )


def _execution_blocker(
    execution: ContentExecution,
    checks: tuple[MutationCheck, ...],
) -> tuple[MutationErrorCode | None, MutationErrorDetails | None]:
    if execution.stop_reason == "adapter_request_rejected":
        rejected = next(check for check in checks if check.request_rejection is not None)
        return "adapter_request_rejected", RejectedRequestDetails(check_id=rejected.check_id)
    if execution.stop_reason == "termination_unconfirmed":
        return "termination_unconfirmed", TerminationDetails(
            check_ids=tuple(
                check.check_id for check in checks if check.termination_problem is not None
            ),
            interrupted=any(
                isinstance(row.invocation, InvocationCancelled) for row in execution.results
            ),
        )
    if execution.stop_reason == "operation_interrupted":
        return "operation_interrupted", None
    if execution.stop_reason is not None:
        raise ValueError("unexpected_content_execution_stop")
    return None, None


class ScaffoldOperation:
    """Collect scaffold facts and attempt create-only persistence under the requested policy."""

    def __init__(
        self,
        *,
        catalog: TemplateCatalog,
        identities: tuple[ArtifactIdentity, ...],
        targets: ArtifactTargetResolver,
        render: Callable[[str, object, FrozenJsonObject], str],
        checks: CheckService,
        creator: IArtifactFileCreator,
        workspace_root: Path,
    ) -> None:
        if not workspace_root.is_absolute():
            raise ValueError("absolute_workspace_required")
        self._catalog = catalog
        self._identities = {identity.id: identity for identity in identities}
        if len(self._identities) != len(identities):
            raise ValueError("duplicate_artifact_identity")
        self._targets = targets
        self._render = render
        self._checks = checks
        self._creator = creator
        self._workspace_root = workspace_root

    async def execute(
        self,
        *,
        artifact_type: str,
        file_name: str,
        context: object,
        target_path: str | None = None,
        force_target: bool = False,
        validation: ValidationPolicy = "enforce",
    ) -> ScaffoldOperationOutput:
        """Keep independent blockers distinct from output-check verdicts."""
        if validation not in ("enforce", "report"):
            raise ValueError("invalid_validation_policy")
        package = self._catalog.get(artifact_type)
        identity = self._identities[artifact_type]
        if identity.pv != package.version:
            raise ValueError("artifact_identity_version_mismatch")
        profile = package.policy.output_profile
        try:
            target = self._targets.resolve(
                template_id=artifact_type,
                persistence=package.policy.persistence,
                file_name=file_name,
                target_path=target_path,
                force_target=force_target,
            )
        except ArtifactTargetError as exc:
            return self._result(
                identity,
                profile,
                validation,
                error_code="target_invalid",
                error_details=TargetDetails(path=exc.path, reason=exc.reason, message=str(exc)),
            )
        except FileExistsError as exc:
            if not isinstance(exc.filename, str):
                raise
            return self._result(
                identity,
                profile,
                validation,
                output_path=exc.filename,
                error_code="target_exists",
                error_details=AffectedPathDetails(path=exc.filename),
            )
        provenance = freeze_json(identity.model_dump(mode="json"))
        if not isinstance(provenance, FrozenJsonObject):
            raise TypeError("artifact_provenance_object_required")
        try:
            content = self._render(artifact_type, context, provenance)
        except ContextError as exc:
            pointer = "".join(
                "/" + str(part).replace("~", "~0").replace("/", "~1") for part in exc.absolute_path
            )
            return self._result(
                identity,
                profile,
                validation,
                output_path=target.output_path,
                error_code="context_invalid",
                error_details=ContextDetails(
                    issues=(
                        ContextIssue(
                            pointer=pointer, keyword=str(exc.validator), message=exc.message
                        ),
                    ),
                ),
            )
        except TemplateError as exc:
            return self._result(
                identity,
                profile,
                validation,
                output_path=target.output_path,
                error_code="render_failed",
                error_details=RenderDetails(message=str(exc)),
            )

        try:
            execution = await self._checks.run_content(
                profile,
                target_path=str(target.path),
                content=content,
            )
        except ContentPreparationError as exc:
            cause = exc.__cause__
            if not isinstance(cause, ScratchPreparationError):
                raise
            checks = tuple(
                _project_check(
                    row,
                    self._workspace_root,
                    preparation_cleanup=cause.cleanup if row.check_id == exc.check_id else None,
                )
                for row in exc.execution.results
            )
            return self._result(
                identity,
                profile,
                validation,
                output_path=target.output_path,
                checks=checks,
                error_code="preparation_failed",
                error_details=InputPreparationDetails(
                    path=target.output_path,
                    reason=(
                        "validation_input_allocation_failed"
                        if cause.phase == "allocation"
                        else "validation_input_write_failed"
                    ),
                    message=str(cause),
                ),
            )
        checks = tuple(_project_check(row, self._workspace_root) for row in execution.results)
        if not checks:
            raise ValueError("nonempty_check_obligations_required")
        error_code, error_details = _execution_blocker(execution, checks)
        status = validation_status(checks)
        permitted = status == "passed" or (
            validation == "report" and status in ("failed", "unavailable")
        )
        if error_code is not None or not permitted:
            return self._result(
                identity,
                profile,
                validation,
                output_path=target.output_path,
                checks=checks,
                error_code=error_code or "validation_blocked",
                error_details=error_details,
            )

        try:
            housekeeping = self._creator.create_text(target.path, content)
        except FileExistsError as exc:
            collision_cleanup = (
                exc.housekeeping if isinstance(exc, FileCreationCollisionError) else ()
            )
            return self._result(
                identity,
                profile,
                validation,
                output_path=target.output_path,
                checks=checks,
                error_code="target_exists",
                error_details=AffectedPathDetails(path=target.output_path),
                housekeeping=self._housekeeping(collision_cleanup),
            )
        except FileCreationError as exc:
            return self._result(
                identity,
                profile,
                validation,
                output_path=target.output_path,
                checks=checks,
                error_code="persistence_failed",
                error_details=PersistenceDetails(
                    path=target.output_path,
                    stage=exc.stage,
                    reason=exc.reason,
                    message=str(exc),
                ),
                housekeeping=self._housekeeping(exc.housekeeping),
            )
        # Result/cache/transport failures after this point cannot undo the completed create.
        return self._result(
            identity,
            profile,
            validation,
            output_path=target.output_path,
            checks=checks,
            written=True,
            housekeeping=self._housekeeping(housekeeping),
        )

    def _housekeeping(
        self,
        issues: tuple[WriteHousekeepingIssue, ...],
    ) -> tuple[HousekeepingIssue, ...]:
        return tuple(
            HousekeepingIssue(
                purpose="write_staging",
                path=issue.path.relative_to(self._workspace_root).as_posix(),
                message=issue.message,
            )
            for issue in issues
        )

    @staticmethod
    def _result(
        identity: ArtifactIdentity,
        profile: str,
        policy: ValidationPolicy,
        *,
        output_path: str | None = None,
        checks: tuple[MutationCheck, ...] = (),
        error_code: MutationErrorCode | None = None,
        error_details: MutationErrorDetails | None = None,
        written: bool = False,
        housekeeping: tuple[HousekeepingIssue, ...] = (),
    ) -> ScaffoldOperationOutput:
        return ScaffoldOperationOutput(
            success=written,
            written=written,
            output_path=output_path,
            template_id=identity.id,
            package_version=identity.pv,
            package_fingerprint=identity.pf,
            validation_policy=policy,
            validation_status=validation_status(checks),
            profile_id=profile,
            checks=checks,
            error_code=error_code,
            error_details=error_details,
            housekeeping=housekeeping,
        )
