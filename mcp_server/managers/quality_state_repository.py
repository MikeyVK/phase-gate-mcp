# mcp_server/managers/quality_state_repository.py
# template=generic version=f35abd82 created=2026-03-18T00:00Z updated=
"""FileQualityStateRepository — atomic persistence of quality-gate baseline state."""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from pathlib import Path

from mcp_server.state.quality_state import QualityState
from mcp_server.utils.atomic_json_writer import AtomicJsonWriter

logger = logging.getLogger(__name__)


class FileQualityStateRepository:
    """Persist QualityState to a dedicated JSON file using AtomicJsonWriter.

    Backing file: ``.st3/quality_state.json`` (separate from ``state.json``).
    """

    def __init__(
        self,
        backing_file: Path,
        writer: AtomicJsonWriter | None = None,
    ) -> None:
        self._backing_file = backing_file
        self._writer = writer or AtomicJsonWriter()

    def load(self) -> QualityState:
        """Return current QualityState; return default QualityState() when absent or malformed."""
        if not self._backing_file.exists():
            return QualityState()
        try:
            raw = json.loads(self._backing_file.read_text(encoding="utf-8"))
            return QualityState(**raw)
        except (json.JSONDecodeError, OSError, Exception):
            logger.warning("quality_state.json malformed; returning default state")
            return QualityState()

    def apply(self, mutate: Callable[[QualityState], QualityState]) -> None:
        """Read current state, apply mutate callback, and persist atomically."""
        current = self.load()
        updated = mutate(current)
        payload = {
            "baseline_sha": updated.baseline_sha,
            "failed_files": list(updated.failed_files),
        }
        self._writer.write_json(self._backing_file, payload)
