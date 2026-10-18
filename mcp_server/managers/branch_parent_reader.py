from __future__ import annotations

from mcp_server.core.exceptions import StateNotFoundError
from mcp_server.core.interfaces import IStateReader
from mcp_server.managers.state_repository import StateBranchMismatchError
from mcp_server.schemas import GitConfig


class BranchStateParentReader:
    """Read parent branch for a branch from persisted state with identity validation."""

    def __init__(
        self,
        state_reader: IStateReader,
        git_config: GitConfig,
    ) -> None:
        self._state_reader = state_reader
        self._git_config = git_config

    def get_parent_branch(self, branch: str) -> str | None:
        """Return the registered parent for an exact branch and positive issue match.

        Missing or mismatched registration returns None; invalid state propagates.
        """
        try:
            state = self._state_reader.load(branch)
        except StateNotFoundError, StateBranchMismatchError:
            return None

        if state.branch != branch:
            return None
        extracted_issue = self._git_config.extract_issue_number(branch)
        if extracted_issue is None or extracted_issue < 1 or state.issue_number != extracted_issue:
            return None

        return state.parent_branch
