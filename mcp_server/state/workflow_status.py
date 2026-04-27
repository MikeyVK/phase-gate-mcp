# mcp_server/state/workflow_status.py
# template=generic version=f35abd82 created=2026-03-23T00:00Z updated=
"""WorkflowStatusDTO — immutable read-side workflow status model."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class WorkflowStatusDTO(BaseModel):
    """Immutable read-side workflow status for the current branch."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    current_phase: str
    sub_phase: str | None = None
    current_cycle: int | None = None
    phase_source: Literal["commit-scope", "state.json", "unknown"]
    phase_confidence: Literal["high", "medium", "unknown"]
    phase_detection_error: str | None = None
