# mcp_server/core/commit_phase_detector.py
# template=generic version=f35abd82 created=2026-03-23T00:00Z updated=
"""CommitPhaseDetector — commit-scope-only phase detector.

Wraps ScopeDecoder with fallback_to_state=False so the resolver path never
performs an implicit second state read.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from mcp_server.config.loader import ConfigLoader
from mcp_server.core.phase_detection import PhaseDetectionResult, ScopeDecoder

if TYPE_CHECKING:
    from mcp_server.config.schemas.workphases import WorkphasesConfig


class CommitPhaseDetector:
    """Detect workflow phase from a commit message without reading state.json."""

    def __init__(
        self,
        workphases_config: WorkphasesConfig | None = None,
        config_root: Path | None = None,
    ) -> None:
        if workphases_config is None:
            if config_root is None:
                raise ValueError(
                    "CommitPhaseDetector requires either workphases_config or config_root. "
                    "No default state directory is used."
                )
            config_loader = ConfigLoader(config_root)
            try:
                workphases_config = config_loader.load_workphases_config()
            except Exception:  # noqa: BLE001
                workphases_config = None

        self._workphases_config = workphases_config

    def detect_from_commit(self, commit_message: str | None) -> PhaseDetectionResult:
        """Detect phase from commit-scope only (no state.json fallback)."""
        if self._workphases_config is None or not commit_message:
            return {
                "workflow_phase": "unknown",
                "sub_phase": None,
                "source": "unknown",
                "confidence": "unknown",
                "raw_scope": None,
                "error_message": "No workphases config or commit message available",
            }

        decoder = ScopeDecoder(self._workphases_config)
        return decoder.detect_phase(commit_message=commit_message, fallback_to_state=False)
