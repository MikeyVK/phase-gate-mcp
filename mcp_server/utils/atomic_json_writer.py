# mcp_server\utils\atomic_json_writer.py
# template=generic version=f35abd82 created=2026-03-12T15:02Z updated=
"""Atomic JSON file writer utilities."""

from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any

_MAX_REPLACE_RETRIES = 10
_REPLACE_RETRY_SLEEP_S = 0.002


class AtomicJsonWriter:
    """Write JSON payloads via temp file replacement."""

    def write_json(
        self,
        path: Path,
        payload: dict[str, Any],
        *,
        temp_name: str = ".tmp",
    ) -> None:
        """Write JSON data to a unique temp file and replace the target atomically.

        Uses a per-call unique temp filename to avoid temp-file collisions under
        concurrent writes.  On Windows, os.replace() can raise PermissionError if
        the destination is held open by a concurrent reader; retry up to
        _MAX_REPLACE_RETRIES times with a short sleep before re-raising.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        unique_suffix = uuid.uuid4().hex
        temp_path = path.parent / f"{temp_name}_{unique_suffix}"
        content = json.dumps(payload, indent=2)
        temp_path.write_text(content, encoding="utf-8")
        last_exc: Exception | None = None
        for _ in range(_MAX_REPLACE_RETRIES):
            try:
                os.replace(temp_path, path)
                return
            except PermissionError as exc:
                last_exc = exc
                time.sleep(_REPLACE_RETRY_SLEEP_S)
        if last_exc is not None:
            raise last_exc
