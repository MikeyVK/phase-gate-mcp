# mcp_server/managers/workflow_status_resolver.py
# template=generic version=f35abd82 created=2026-03-23T00:00Z updated=
"""WorkflowStatusResolver — read-only resolver for current branch workflow status."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from mcp_server.managers.state_repository import StateBranchMismatchError
from mcp_server.state.workflow_status import WorkflowStatusDTO

if TYPE_CHECKING:
    from mcp_server.core.commit_phase_detector import CommitPhaseDetector
    from mcp_server.core.interfaces import IGitContextReader, IStateReader

logger = logging.getLogger(__name__)

_HIGH_CONFIDENCE: frozenset[str] = frozenset({"high"})


class WorkflowStatusResolver:
    """Resolve current-branch workflow status from git context and persisted state."""

    def __init__(
        self,
        git_context_reader: IGitContextReader,
        state_reader: IStateReader,
        commit_phase_detector: CommitPhaseDetector,
    ) -> None:
        self._git = git_context_reader
        self._state = state_reader
        self._detector = commit_phase_detector

    def resolve_current(self) -> WorkflowStatusDTO:
        """Resolve workflow status for the current branch."""
        branch = self._git.get_current_branch()

        # Load persisted state (may fail gracefully)
        persisted_cycle: int | None = None
        persisted_phase: str | None = None
        try:
            branch_state = self._state.load(branch)
            persisted_cycle = branch_state.current_cycle
            persisted_phase = branch_state.current_phase
        except (KeyError, StateBranchMismatchError, FileNotFoundError, OSError) as exc:
            logger.debug("Could not load branch state for '%s': %s", branch, exc)

        # Detect phase from latest commit
        commits = self._git.get_recent_commits(limit=1)
        commit_message = commits[0] if commits else None
        detection = self._detector.detect_from_commit(commit_message)

        if detection["confidence"] in _HIGH_CONFIDENCE:
            return WorkflowStatusDTO(
                current_phase=detection["workflow_phase"],
                sub_phase=detection["sub_phase"],
                current_cycle=persisted_cycle,
                phase_source="commit-scope",
                phase_confidence="high",
                phase_detection_error=detection.get("error_message"),
            )

        # Fall back to persisted state
        if persisted_phase is not None:
            return WorkflowStatusDTO(
                current_phase=persisted_phase,
                current_cycle=persisted_cycle,
                phase_source="state.json",
                phase_confidence="medium",
                phase_detection_error=detection.get("error_message"),
            )

        return WorkflowStatusDTO(
            current_phase="unknown",
            current_cycle=persisted_cycle,
            phase_source="unknown",
            phase_confidence="unknown",
            phase_detection_error=detection.get("error_message"),
        )
