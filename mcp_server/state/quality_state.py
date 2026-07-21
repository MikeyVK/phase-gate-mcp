# mcp_server/state/quality_state.py
# template=generic version=f35abd82 created=2026-03-18T00:00Z updated=2026-07-20T23:32Z
"""Immutable quality-gate baseline state DTO."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class QualityState(BaseModel):
    """Immutable snapshot of quality-gate baseline tracking state.

    Stored in ``quality_state.json`` under the state root.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: str = "1.0.0"
    baseline_sha: str | None = None
    failed_files: list[str] = Field(default_factory=list)
