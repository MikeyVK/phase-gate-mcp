# mcp_server/utils/atomic_file_writer.py
# template=generic version=f35abd82 created=2026-07-21T11:59Z updated=2026-07-21T11:59Z
"""Atomic file writer utilities supporting text and JSON payloads."""

from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any

from mcp_server.core.interfaces.file_writer import IAtomicFileWriter

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
