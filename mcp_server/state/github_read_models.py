"""Read models for GitHub API responses."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class PRReadModel(BaseModel):
    """Immutable read model for a GitHub pull request."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    pr_number: int
    title: str
    state: str
    base_branch: str
    head_branch: str
    merged_at: str | None
    merge_sha: str | None
    body: str
