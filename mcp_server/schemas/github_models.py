# mcp_server/schemas/github_models.py
# template=schema version=74378193 created=2026-06-14T19:21Z updated=
"""PRReadModel schema.

GitHub API read models for Issue and PR tools

@layer: Schemas
"""

# Third-party
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
    html_url: str


class MilestoneReadModel(BaseModel):
    """Immutable read model for a GitHub milestone."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    number: int
    title: str
    state: str


class IssueReadModel(BaseModel):
    """Immutable read model for a GitHub issue."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    number: int
    url: str
    title: str
    body: str
    state: str
    labels: list[str]
    milestone: MilestoneReadModel | None
    assignees: list[str]
    created_at: str
    updated_at: str
    closed_at: str | None
    author: str
