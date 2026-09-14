"""Coordinate original-file validation and guarded replacement within one cooperating lock."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from pathlib import Path
from typing import Literal

from mcp_server.core.interfaces.execution import ScopePaths, ScratchPreparationError
from mcp_server.core.interfaces.file_writer import (
    FileReplacementError,
    ICheckedFileReplacer,
    IOriginalFileReader,
    OriginalChangedError,
    OriginalReadError,
    OriginalTargetMissingError,
    OriginalTargetNotFileError,
    WriteHousekeepingIssue,
)
from mcp_server.execution.check_service import CheckService, ContentPreparationError
from mcp_server.schemas.mutation_outputs import (
    AffectedPathDetails,
    EditOperationOutput,
    HousekeepingIssue,
    InputPreparationDetails,
    LockWaitDetails,
    MutationCheck,
    MutationErrorCode,
    MutationErrorDetails,
    OriginalReadDetails,
    PersistenceDetails,
    TargetDetails,
)
from mcp_server.services.edit_construction import (
    EditConstructionError,
    EditProfileSelection,
)
from mcp_server.services.edit_construction import (
    EditOperation as EditCommand,
)
from mcp_server.services.scaffold_operation import (
    ValidationPolicy,
    mutation_execution_blocker,
    project_mutation_check,
    validation_status,
)
from mcp_server.utils.path_resolver import ArtifactTargetError, normalize_workspace_relative_path

_FILE_ERRORS = (
    OriginalTargetMissingError,
    OriginalTargetNotFileError,
    OriginalReadError,
    OriginalChangedError,
    FileReplacementError,
)


def _file_details(
    path: str,
    error: OSError | UnicodeDecodeError,
) -> tuple[MutationErrorCode, MutationErrorDetails]:
    """Translate only observed filesystem failures into mutation-owned facts."""
    if isinstance(error, (OriginalTargetMissingError, FileNotFoundError)):
        return "original_missing", AffectedPathDetails(path=path)
    if isinstance(error, OriginalChangedError):
        return "original_changed", AffectedPathDetails(path=path)
    if isinstance(error, (OriginalTargetNotFileError, IsADirectoryError)):
        return "target_invalid", TargetDetails(path=path, reason="not_file", message=str(error))
    if isinstance(error, FileReplacementError):
        return "persistence_failed", PersistenceDetails(
            path=path,
            stage=error.stage,
            reason=error.reason,
            message=str(error),
        )
    if isinstance(error, OriginalReadError):
        return "original_unreadable", OriginalReadDetails(
            path=path,
            reason=error.reason,
            message=str(error),
        )
    reason: Literal["invalid_encoding", "permission_denied", "io_error"] = (
        "invalid_encoding"
        if isinstance(error, UnicodeDecodeError)
        else "permission_denied"
        if isinstance(error, PermissionError)
        else "io_error"
    )
    return "original_unreadable", OriginalReadDetails(path=path, reason=reason, message=str(error))


class EditOperation:
    """Own the logical edit while injected boundaries supply source and persistence facts."""

    def __init__(
        self,
        *,
        paths: ScopePaths,
        reader: IOriginalFileReader,
        writer: ICheckedFileReplacer,
        select: Callable[[str, str, str | None], EditProfileSelection],
        construct: Callable[[str, EditCommand], str],
        checks: CheckService,
    ) -> None:
        self._paths = paths
        self._reader = reader
        self._writer = writer
        self._select = select
        self._construct = construct
        self._checks = checks
        self._locks: dict[Path, asyncio.Lock] = {}

    async def execute(
        self,
        *,
        path: str,
        operation: EditCommand,
        template_id: str | None = None,
        validation: ValidationPolicy = "enforce",
    ) -> EditOperationOutput:
        """Acquire cooperating-call exclusion without timing the validation body."""
        if validation not in ("enforce", "report"):
            raise ValueError("invalid_validation_policy")
        logical = normalize_workspace_relative_path(path)
        if logical == ".":
            return self._result(
                logical,
                validation,
                error_code="target_invalid",
                error_details=TargetDetails(
                    path=logical,
                    reason="not_file",
                    message="workspace_root_is_directory",
                ),
            )
        try:
            target = self._paths.resolve(logical).path
        except ArtifactTargetError as exc:
            return self._result(
                logical,
                validation,
                error_code="target_invalid",
                error_details=TargetDetails(path=exc.path, reason=exc.reason, message=str(exc)),
            )
        lock = self._locks.setdefault(target, asyncio.Lock())
        try:
            await asyncio.wait_for(lock.acquire(), timeout=0.01)
        except TimeoutError:
            return self._result(
                logical,
                validation,
                error_code="preparation_failed",
                error_details=LockWaitDetails(path=logical, reason="lock_wait_timeout"),
            )
        try:
            return await self._execute_locked(logical, target, operation, template_id, validation)
        finally:
            lock.release()

    async def _execute_locked(
        self,
        logical: str,
        target: Path,
        operation: EditCommand,
        template_id: str | None,
        policy: ValidationPolicy,
    ) -> EditOperationOutput:
        try:
            original = self._reader.read_snapshot(target)
        except (OSError, UnicodeDecodeError) as exc:
            code, details = _file_details(logical, exc)
            return self._result(logical, policy, error_code=code, error_details=details)

        selection = self._select(original.original_text, target.name, template_id)
        try:
            proposed = self._construct(original.original_text, operation)
        except EditConstructionError as exc:
            return self._result(
                logical,
                policy,
                selection=selection,
                error_code="edit_invalid",
                error_details=exc.details,
            )

        checks: tuple[MutationCheck, ...] = ()
        if selection.profile_id is not None:
            try:
                execution = await self._checks.run_content(
                    selection.profile_id,
                    target_path=str(target),
                    content=proposed,
                )
            except ContentPreparationError as exc:
                cause = exc.__cause__
                if not isinstance(cause, ScratchPreparationError):
                    raise
                checks = tuple(
                    project_mutation_check(
                        row,
                        self._paths.workspace_root,
                        preparation_cleanup=cause.cleanup if row.check_id == exc.check_id else None,
                    )
                    for row in exc.execution.results
                )
                return self._result(
                    logical,
                    policy,
                    selection=selection,
                    checks=checks,
                    error_code="preparation_failed",
                    error_details=InputPreparationDetails(
                        path=logical,
                        reason=(
                            "validation_input_allocation_failed"
                            if cause.phase == "allocation"
                            else "validation_input_write_failed"
                        ),
                        message=str(cause),
                    ),
                )
            checks = tuple(
                project_mutation_check(row, self._paths.workspace_root) for row in execution.results
            )
            if not checks:
                raise ValueError("selected_profile_requires_check_obligations")
            blocker_code, blocker_details = mutation_execution_blocker(execution, checks)
            if blocker_code is not None:
                return self._result(
                    logical,
                    policy,
                    selection=selection,
                    checks=checks,
                    error_code=blocker_code,
                    error_details=blocker_details,
                )

        if policy == "enforce" and validation_status(checks) != "passed":
            return self._result(
                logical,
                policy,
                selection=selection,
                checks=checks,
                error_code="validation_blocked",
            )
        if any(check.status == "not_executed" for check in checks):
            raise ValueError("incomplete_checks_without_execution_blocker")
        try:
            housekeeping = self._writer.replace_if_unchanged(
                target,
                original.original_bytes,
                proposed,
            )
        except _FILE_ERRORS as exc:
            code, details = _file_details(logical, exc)
            return self._result(
                logical,
                policy,
                selection=selection,
                checks=checks,
                error_code=code,
                error_details=details,
                housekeeping=self._housekeeping(exc.housekeeping),
            )
        # Later construction/publication errors cannot undo this completed replacement.
        return self._result(
            logical,
            policy,
            selection=selection,
            checks=checks,
            written=True,
            content_changed=proposed != original.original_text,
            housekeeping=self._housekeeping(housekeeping),
        )

    def _housekeeping(
        self,
        issues: tuple[WriteHousekeepingIssue, ...],
    ) -> tuple[HousekeepingIssue, ...]:
        return tuple(
            HousekeepingIssue(
                purpose="write_staging",
                path=issue.path.relative_to(self._paths.workspace_root).as_posix(),
                message=issue.message,
            )
            for issue in issues
        )

    @staticmethod
    def _result(
        path: str,
        policy: ValidationPolicy,
        *,
        selection: EditProfileSelection | None = None,
        checks: tuple[MutationCheck, ...] = (),
        error_code: MutationErrorCode | None = None,
        error_details: MutationErrorDetails | None = None,
        written: bool = False,
        content_changed: bool | None = None,
        housekeeping: tuple[HousekeepingIssue, ...] = (),
    ) -> EditOperationOutput:
        return EditOperationOutput(
            success=written,
            written=written,
            path=path,
            content_changed=content_changed,
            validation_policy=policy,
            validation_status=validation_status(checks),
            selected_source=selection.selected_source if selection is not None else None,
            profile_id=selection.profile_id if selection is not None else None,
            template_id=selection.template_id if selection is not None else None,
            extension=selection.extension if selection is not None else None,
            selection_reason=selection.selection_reason if selection is not None else None,
            checks=checks,
            error_code=error_code,
            error_details=error_details,
            housekeeping=housekeeping,
        )
