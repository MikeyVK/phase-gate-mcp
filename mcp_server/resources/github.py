"""GitHub resources."""

import json

from mcp_server.managers.github_manager import GitHubManager
from mcp_server.resources.base import BaseResource


class GitHubIssuesResource(BaseResource):
    """Resource for accessing GitHub issues."""

    uri_pattern = "pgmcp://github/issues"
    description = "Active GitHub issues"

    def __init__(self, manager: GitHubManager | None = None) -> None:
        self.manager = manager or GitHubManager()

    async def read(self, uri: str) -> str:  # noqa: ARG002
        """Read the resource content."""
        data = self.manager.get_issues_resource_data()
        return json.dumps(data, indent=2)
