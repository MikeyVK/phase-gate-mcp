"""Deterministic commit-scope decoding through the shared configured grammar."""

import re
from dataclasses import dataclass
from typing import Literal

from mcp_server.core.scope_contract import ScopeContract


@dataclass(frozen=True)
class PhaseDetectionResult:
    """Immutable configured scope interpretation or structured uncertainty."""

    workflow_phase: str | None
    cycle_number: int | None
    sub_phase: str | None
    source: Literal["commit-scope", "unknown"]
    confidence: Literal["high", "unknown"]
    raw_scope: str | None
    error_code: str | None


class ScopeDecoder:
    """Decode commit subjects without inferring phase from title or commit type."""

    COMMIT_SCOPE_PATTERN = re.compile(r"^[a-z]+\(([^)]+)\)!?:", re.IGNORECASE)

    def __init__(self, contract: ScopeContract) -> None:
        self._contract = contract

    def detect_phase(self, commit_message: str | None) -> PhaseDetectionResult:
        """Return decoded fields or an unknown result with a diagnostic code."""
        if not commit_message:
            return self._unknown("scope_input_missing")
        match = self.COMMIT_SCOPE_PATTERN.match(commit_message)
        if match is None:
            return self._unknown("commit_scope_missing")
        scope = match.group(1)
        fields = self._contract.decode(scope)
        if fields is None:
            return self._unknown("commit_scope_invalid", scope)
        return PhaseDetectionResult(
            workflow_phase=fields.workflow_phase,
            cycle_number=fields.cycle_number,
            sub_phase=fields.sub_phase,
            source="commit-scope",
            confidence="high",
            raw_scope=scope,
            error_code=None,
        )

    @staticmethod
    def _unknown(code: str, scope: str | None = None) -> PhaseDetectionResult:
        return PhaseDetectionResult(None, None, None, "unknown", "unknown", scope, code)
