"""Read models for GitHub API responses.

Deprecated: Moved to mcp_server.schemas.github_models.
"""

from __future__ import annotations

from mcp_server.schemas.github_models import IssueReadModel, MilestoneReadModel, PRReadModel

__all__ = ["IssueReadModel", "MilestoneReadModel", "PRReadModel"]
