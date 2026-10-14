"""Status resource."""

import json
import time

from mcp_server.core.exceptions import MCPSystemError
from mcp_server.core.interfaces import IGitContextReader, IStateReader
from mcp_server.resources.base import BaseResource


class StatusResource(BaseResource):
    """Resource for project status."""

    uri_pattern = "pgmcp://status/phase"
    description = "Current development phase and git status"

    def __init__(self, git_context_reader: IGitContextReader, state_reader: IStateReader) -> None:
        self._git = git_context_reader
        self._state_reader = state_reader

    async def read(self, uri: str) -> str:  # noqa: ARG002
        """Read status."""
        try:
            git_status = self._git.get_status()
            branch = git_status["branch"]
            phase = self._state_reader.load(branch).current_phase

            data = {
                "current_phase": phase,
                "active_branch": branch,
                "is_clean": git_status["is_clean"],
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return json.dumps(data, indent=2)

        except MCPSystemError as e:
            return json.dumps({"error": str(e)})
