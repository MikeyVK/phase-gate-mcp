"""Commit-scope detector delegating to its injected decoder."""

from mcp_server.core.phase_detection import PhaseDetectionResult, ScopeDecoder


class CommitPhaseDetector:
    """Expose the shared decoder without configuration loading or reconstruction."""

    def __init__(self, decoder: ScopeDecoder) -> None:
        self._decoder = decoder

    def detect_from_commit(self, commit_message: str | None) -> PhaseDetectionResult:
        """Return the injected decoder's immutable interpretation unchanged."""
        return self._decoder.detect_phase(commit_message)
