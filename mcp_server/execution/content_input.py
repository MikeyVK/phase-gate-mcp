"""Prepare proposed check content and own its temporary validation files."""

from __future__ import annotations

import re
import shutil
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Annotated, TypeAlias, TypeVar

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    StrictStr,
    StringConstraints,
    WithJsonSchema,
)

from mcp_server.config.schemas.adapter_manifest import CapabilityId, CheckCapability
from mcp_server.core.interfaces.execution import (
    AdapterBinding,
    ContentScratchFiles,
    OwnedScratchFile,
)
from mcp_server.execution.models import (
    InvocationCancelled,
    InvocationCompleted,
    InvocationFailed,
    TerminationProblem,
)

_ABSOLUTE_PATH_PATTERN = r"^(?:/|[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+)[\s\S]*$(?![\s\S])"
_FILE_EXCLUSION_PATTERN = r"(?:[\\/]|(?:^|[\\/])\.{1,2})$|^\\\\[^\\/]+[\\/][^\\/]+$(?![\s\S])"


def _absolute_file_path(value: str) -> str:
    """Validate portable path syntax without consulting the local filesystem."""
    if (
        "\x00" in value
        or re.search(_ABSOLUTE_PATH_PATTERN, value) is None
        or re.search(_FILE_EXCLUSION_PATTERN, value) is not None
    ):
        raise ValueError("absolute_file_path_required")
    return value


def _closed_alternatives(schema: dict[str, object]) -> None:
    """The closed text/file shapes are mutually exclusive on the wire."""
    schema["oneOf"] = schema.pop("anyOf")


AbsoluteFilePath = Annotated[
    str,
    StringConstraints(strict=True, min_length=1),
    AfterValidator(_absolute_file_path),
    WithJsonSchema(
        {
            "type": "string",
            "minLength": 1,
            "allOf": [
                {"not": {"pattern": "\x00"}},
                {"pattern": _ABSOLUTE_PATH_PATTERN},
                {"not": {"pattern": _FILE_EXCLUSION_PATTERN}},
            ],
        }
    ),
]


class ScaffoldTextInput(BaseModel):
    """Direct proposed text for a check adapter."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    target_path: AbsoluteFilePath
    content: StrictStr


class ScaffoldFileInput(BaseModel):
    """Proposed content materialized at an owned validation path."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    target_path: AbsoluteFilePath
    input_path: AbsoluteFilePath


ScaffoldContentInput: TypeAlias = Annotated[
    ScaffoldTextInput | ScaffoldFileInput, Field(json_schema_extra=_closed_alternatives)
]


class ScaffoldTextRequest(ScaffoldTextInput):
    """Complete direct-content check request."""

    operation: CapabilityId
    args: tuple[StrictStr, ...]


class ScaffoldFileRequest(ScaffoldFileInput):
    """Complete materialized-file check request."""

    operation: CapabilityId
    args: tuple[StrictStr, ...]


ScaffoldContentRequest: TypeAlias = Annotated[
    ScaffoldTextRequest | ScaffoldFileRequest, Field(json_schema_extra=_closed_alternatives)
]


@dataclass(frozen=True)
class PreparedContent:
    """Prepared request plus the optional invocation-owned scratch allocation."""

    request: ScaffoldContentRequest
    scratch: OwnedScratchFile | None


@dataclass(frozen=True)
class CleanupProblem:
    """Housekeeping failure kept separate from the invocation result."""

    directory: Path
    message: str


class FileContentScratch:
    """Allocate and remove one exclusive validation directory per invocation."""

    def __init__(
        self,
        validation_root: Path,
        *,
        fresh_id: Callable[[], str],
        write_bytes: Callable[[Path, bytes], int] = Path.write_bytes,
        remove_tree: Callable[[Path], None] = shutil.rmtree,
    ) -> None:
        if not validation_root.is_absolute():
            raise ValueError("validation_root_must_be_absolute")
        self._validation_root = validation_root
        self._fresh_id = fresh_id
        self._write_bytes = write_bytes
        self._remove_tree = remove_tree

    def create(self, basename: str, content: bytes) -> OwnedScratchFile:
        """Create one exclusive owned directory and write exact UTF-8 bytes."""
        _validate_component(basename, "scratch_basename")
        allocation_id = self._fresh_id()
        _validate_component(allocation_id, "scratch_id")
        directory = self._validation_root / allocation_id
        input_path = directory / basename
        directory.mkdir(parents=True, exist_ok=False)
        try:
            written = self._write_bytes(input_path, content)
            if written != len(content):
                raise OSError("scratch_write_incomplete")
        except BaseException as exc:
            try:
                self._remove_tree(directory)
            except BaseException as rollback_error:
                exc.add_note(f"scratch_rollback_failed: {rollback_error}")
            raise
        return OwnedScratchFile(directory=directory, input_path=input_path)

    def remove(self, allocation: OwnedScratchFile) -> None:
        """Remove only the exact directory and file shape this provider owns."""
        if (
            allocation.directory.parent != self._validation_root
            or allocation.input_path.parent != allocation.directory
            or allocation.directory == self._validation_root
        ):
            raise ValueError("scratch_allocation_not_owned")
        self._remove_tree(allocation.directory)


TResponse = TypeVar("TResponse", bound=BaseModel)


class ContentInputPreparer:
    """Select and prepare the manifest-declared proposed-content route."""

    def __init__(self, scratch: ContentScratchFiles) -> None:
        self._scratch = scratch

    def prepare(
        self,
        binding: AdapterBinding[CheckCapability],
        *,
        target_path: str,
        content: str,
        args: tuple[str, ...],
    ) -> PreparedContent:
        """Validate the request before allocating any temporary file."""
        if "content" not in binding.capability.inputs:
            raise ValueError("content_input_not_supported")
        if binding.capability.requires_file is None:
            raise ValueError("content_file_requirement_missing")

        direct = ScaffoldTextRequest(
            operation=binding.capability_id,
            target_path=target_path,
            content=content,
            args=args,
        )
        if not binding.capability.requires_file:
            return PreparedContent(request=direct, scratch=None)

        encoded = content.encode("utf-8")
        allocation = self._scratch.create(_portable_basename(target_path), encoded)
        try:
            request = ScaffoldFileRequest(
                operation=direct.operation,
                target_path=direct.target_path,
                input_path=str(allocation.input_path),
                args=direct.args,
            )
        except BaseException as exc:
            try:
                self._scratch.remove(allocation)
            except BaseException as rollback_error:
                exc.add_note(f"scratch_rollback_failed: {rollback_error}")
            raise
        return PreparedContent(request=request, scratch=allocation)

    def cleanup(
        self,
        prepared: PreparedContent,
        outcome: InvocationCompleted[TResponse] | InvocationFailed | InvocationCancelled,
    ) -> CleanupProblem | None:
        """Attempt safe cleanup without replacing the primary invocation outcome."""
        allocation = prepared.scratch
        if allocation is None:
            return None
        if (
            isinstance(outcome, (InvocationFailed, InvocationCancelled))
            and outcome.termination_problem is TerminationProblem.UNCONFIRMED
        ):
            return None
        try:
            self._scratch.remove(allocation)
        except OSError as exc:
            return CleanupProblem(directory=allocation.directory, message=str(exc))
        return None


def _validate_component(value: str, name: str) -> None:
    if (
        not value
        or value in {".", ".."}
        or "\x00" in value
        or ":" in value
        or PurePosixPath(value).name != value
        or PureWindowsPath(value).name != value
    ):
        raise ValueError(f"{name}_must_be_single_path_component")


def _portable_basename(path: str) -> str:
    basename = PureWindowsPath(path).name if "\\" in path else PurePosixPath(path).name
    _validate_component(basename, "scratch_basename")
    return basename
