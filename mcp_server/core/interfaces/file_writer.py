# mcp_server/core/interfaces/file_writer.py
# template=interface version=f35abd82 created=2026-07-21T11:59Z updated=2026-07-21T11:59Z
"""Protocol interface for atomic file writing."""

import errno
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class WriteHousekeepingIssue:
    """A cleanup problem observed after or alongside artifact creation."""

    path: Path
    message: str


class FileCreationError(OSError):
    """A create-only staging or final-create failure."""

    def __init__(
        self,
        stage: Literal["write_staging", "create"],
        reason: Literal["permission_denied", "io_error"],
        message: str,
        *,
        housekeeping: tuple[WriteHousekeepingIssue, ...] = (),
    ) -> None:
        super().__init__(message)
        self.stage = stage
        self.reason = reason
        self.housekeeping = housekeeping


class FileCreationCollisionError(FileExistsError):
    """A final create-if-absent collision with staging cleanup facts."""

    def __init__(
        self,
        path: Path,
        *,
        housekeeping: tuple[WriteHousekeepingIssue, ...] = (),
    ) -> None:
        super().__init__(errno.EEXIST, "Artifact target already exists", str(path))
        self.path = path
        self.housekeeping = housekeeping


@dataclass(frozen=True, slots=True)
class OriginalFileSnapshot:
    """One native-read original with logical and source-preserving text views."""

    original_bytes: bytes
    original_text: str
    original_source_text: str


class OriginalTargetMissingError(FileNotFoundError):
    """The expected target was absent during an original or guard read."""

    def __init__(
        self,
        path: Path,
        *,
        housekeeping: tuple[WriteHousekeepingIssue, ...] = (),
    ) -> None:
        super().__init__(str(path))
        self.path = path
        self.housekeeping = housekeeping


class OriginalTargetNotFileError(OSError):
    """The observed target leaf is a directory, symlink, or other non-file."""

    def __init__(
        self,
        path: Path,
        *,
        housekeeping: tuple[WriteHousekeepingIssue, ...] = (),
    ) -> None:
        super().__init__(str(path))
        self.path = path
        self.housekeeping = housekeeping


class OriginalReadError(OSError):
    """A typed failure while reading or decoding the original target."""

    def __init__(
        self,
        path: Path,
        reason: Literal["permission_denied", "invalid_encoding", "io_error"],
        message: str,
        *,
        housekeeping: tuple[WriteHousekeepingIssue, ...] = (),
    ) -> None:
        super().__init__(message)
        self.path = path
        self.reason = reason
        self.housekeeping = housekeeping


class OriginalChangedError(OSError):
    """The target bytes no longer match the invocation's original basis."""

    def __init__(
        self,
        path: Path,
        *,
        housekeeping: tuple[WriteHousekeepingIssue, ...] = (),
    ) -> None:
        super().__init__(str(path))
        self.path = path
        self.housekeeping = housekeeping


class FileReplacementError(OSError):
    """A checked replacement failed before a committed target replacement."""

    def __init__(
        self,
        stage: Literal["write_staging", "replace"],
        reason: Literal["permission_denied", "io_error"],
        message: str,
        *,
        housekeeping: tuple[WriteHousekeepingIssue, ...] = (),
    ) -> None:
        super().__init__(message)
        self.stage = stage
        self.reason = reason
        self.housekeeping = housekeeping


@runtime_checkable
class IOriginalFileReader(Protocol):
    """Narrow original-file snapshot reader for edit operations."""

    def read_snapshot(self, path: Path) -> OriginalFileSnapshot: ...


@runtime_checkable
class ICheckedFileReplacer(Protocol):
    """Narrow existing-target replacer guarded by original bytes."""

    def replace_if_unchanged(
        self,
        path: Path,
        expected_original: bytes,
        content: str,
    ) -> tuple[WriteHousekeepingIssue, ...]: ...


@runtime_checkable
class IArtifactFileCreator(Protocol):
    """Narrow protocol for create-only artifact persistence."""

    def create_text(self, path: Path, content: str) -> tuple[WriteHousekeepingIssue, ...]:
        """Create one previously absent UTF-8 text file."""
        ...


@runtime_checkable
class IAtomicFileWriter(Protocol):
    """Protocol interface for atomic file operations across all file types."""

    def write_text(self, path: Path, content: str, *, temp_name: str = ".tmp") -> None:
        """Atomically write text content to path via temp file replacement."""
        ...

    def write_json(self, path: Path, payload: dict[str, Any], *, temp_name: str = ".tmp") -> None:
        """Atomically write JSON payload to path via temp file replacement."""
        ...
