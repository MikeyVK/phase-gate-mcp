# mcp_server/utils/atomic_file_writer.py
# template=generic version=f35abd82 created=2026-07-21T11:59Z updated=2026-07-21T11:59Z
"""Atomic file writer utilities supporting text and JSON payloads."""

from __future__ import annotations

import contextlib
import json
import os
import time
import uuid
from pathlib import Path
from typing import Any, Literal

from mcp_server.core.interfaces.file_writer import (
    FileCreationCollisionError,
    FileCreationError,
    IArtifactFileCreator,
    IAtomicFileWriter,
    WriteHousekeepingIssue,
)

_MAX_REPLACE_RETRIES = 10
_REPLACE_RETRY_SLEEP_S = 0.002


class AtomicFileWriter(IAtomicFileWriter):
    """Concrete implementation of IAtomicFileWriter with Windows permission retry logic."""

    def write_text(self, path: Path, content: str, *, temp_name: str = ".tmp") -> None:
        """Write text content to a unique temp file and replace target atomically."""
        path.parent.mkdir(parents=True, exist_ok=True)
        unique_suffix = uuid.uuid4().hex
        temp_path = path.parent / f"{temp_name}_{unique_suffix}"
        temp_path.write_text(content, encoding="utf-8")
        self._replace_with_retry(temp_path, path)

    def write_json(self, path: Path, payload: dict[str, Any], *, temp_name: str = ".tmp") -> None:
        """Write JSON data to a unique temp file and replace target atomically."""
        path.parent.mkdir(parents=True, exist_ok=True)
        unique_suffix = uuid.uuid4().hex
        temp_path = path.parent / f"{temp_name}_{unique_suffix}"
        content = json.dumps(payload, indent=2)
        temp_path.write_text(content, encoding="utf-8")
        self._replace_with_retry(temp_path, path)

    def _replace_with_retry(self, src: Path, dst: Path) -> None:
        """Replace src with dst, retrying up to _MAX_REPLACE_RETRIES on PermissionError."""
        last_exc: Exception | None = None
        for _ in range(_MAX_REPLACE_RETRIES):
            try:
                os.replace(src, dst)
                return
            except PermissionError as exc:
                last_exc = exc
                time.sleep(_REPLACE_RETRY_SLEEP_S)
        if last_exc is not None:
            raise last_exc


class CreateOnlyFileWriter(IArtifactFileCreator):
    """Create one UTF-8 artifact without replacing an existing target."""

    def create_text(self, path: Path, content: str) -> tuple[WriteHousekeepingIssue, ...]:
        """Stage content, atomically create the target, then clean up staging."""
        target = Path(path)
        staging = target.parent / f".{uuid.uuid4().hex}.staging"
        payload = content.encode("utf-8")

        owned_staging = False
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            descriptor = os.open(
                staging,
                os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0),
                0o666,
            )
            owned_staging = True
            try:
                written = os.write(descriptor, payload)
                if written != len(payload):
                    raise OSError(
                        f"short staging write: expected {len(payload)} bytes, wrote {written}"
                    )
            except OSError:
                with contextlib.suppress(OSError):
                    os.close(descriptor)
                raise
            os.close(descriptor)
        except OSError as exc:
            housekeeping = self._cleanup(staging, owned=owned_staging)
            raise FileCreationError(
                "write_staging",
                self._reason(exc),
                str(exc),
                housekeeping=housekeeping,
            ) from exc

        try:
            os.link(staging, target)
        except FileExistsError as exc:
            housekeeping = self._cleanup(staging, owned=True)
            raise FileCreationCollisionError(target, housekeeping=housekeeping) from exc
        except OSError as exc:
            housekeeping = self._cleanup(staging, owned=True)
            raise FileCreationError(
                "create",
                self._reason(exc),
                str(exc),
                housekeeping=housekeeping,
            ) from exc

        return self._cleanup(staging, owned=True)

    @staticmethod
    def _reason(exc: OSError) -> Literal["permission_denied", "io_error"]:
        return "permission_denied" if isinstance(exc, PermissionError) else "io_error"

    @staticmethod
    def _cleanup(
        path: Path,
        *,
        owned: bool,
    ) -> tuple[WriteHousekeepingIssue, ...]:
        if not owned:
            return ()
        try:
            path.unlink(missing_ok=True)
        except OSError as exc:
            return (WriteHousekeepingIssue(path=path, message=str(exc)),)
        return ()
