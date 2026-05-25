# mcp_server/managers/quality_state_repository.py
# template=generic version=f35abd82 created=2026-03-18T00:00Z updated=
"""FileQualityStateRepository — atomic persistence of quality-gate baseline state."""

from __future__ import annotations

import json
import logging
import threading
from collections.abc import Callable
from pathlib import Path

from mcp_server.state.quality_state import QualityState
from mcp_server.utils.atomic_json_writer import AtomicJsonWriter

logger = logging.getLogger(__name__)


class QualityStateMutationConflictError(Exception):
    """Raised when a quality-state mutation cannot complete safely due to lock timeout.

    Carries both a diagnostic message (suitable for ToolResult.error) and a
    recovery hint (suitable for RecoveryNote).
    """

    def __init__(self, diagnostic: str, recovery: str) -> None:
        super().__init__(diagnostic)
        self.diagnostic = diagnostic
        self.recovery = recovery


class FileQualityStateRepository:
    """Persist QualityState to a dedicated JSON file using AtomicJsonWriter.

    Backing file: ``quality_state.json`` under the state root.
    """

    def __init__(
        self,
        backing_file: Path,
        writer: AtomicJsonWriter | None = None,
    ) -> None:
        self._backing_file = backing_file
        self._writer = writer or AtomicJsonWriter()
        self._lock = threading.Lock()

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
        """Read current state, apply mutate callback, and persist atomically.

        Acquires an in-process lock (timeout = 5 s) to serialize concurrent callers.
        Raises QualityStateMutationConflictError if the lock cannot be acquired.
        """
        acquired = self._lock.acquire(timeout=5.0)
        if not acquired:
            raise QualityStateMutationConflictError(
                diagnostic="Quality state write failed — lock timeout (5s): another caller is still writing.",
                recovery="Retry the quality-gates run once the current run completes.",
            )
        try:
            current = self.load()
            updated = mutate(current)
            payload = {
                "baseline_sha": updated.baseline_sha,
                "failed_files": list(updated.failed_files),
            }
            self._writer.write_json(self._backing_file, payload)
        finally:
            self._lock.release()
