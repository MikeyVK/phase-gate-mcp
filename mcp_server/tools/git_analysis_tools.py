"""Git analysis tools for inspecting repository state."""

import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.git_manager import GitManager
from mcp_server.schemas.tool_outputs import (
    BranchDetailDTO,
    GitDiffOutput,
    GitListBranchesOutput,
)
from mcp_server.tools.base import ILegacyTool


class GitListBranchesInput(BaseModel):
    """Input for GitListBranchesTool."""

    model_config = ConfigDict(extra="forbid")

    verbose: bool = Field(default=False, description="Include upstream/hash info (-vv)")
    remote: bool = Field(default=False, description="Include remote branches (-r)")


class GitListBranchesTool(ILegacyTool):
    """Tool to list git branches with optional details."""

    @property
    def name(self) -> str:
        return "git_list_branches"

    @property
    def description(self) -> str:
        return "List git branches with optional verbose info and remotes"

    @property
    def args_model(self) -> type[BaseModel] | None:
        return GitListBranchesInput

    def __init__(self, manager: GitManager) -> None:
        self.manager = manager

    @property
    def input_schema(self) -> dict[str, Any]:
        assert self.args_model is not None
        return self.args_model.model_json_schema()

    async def execute(
        self, params: GitListBranchesInput, context: NoteContext
    ) -> GitListBranchesOutput:
        del context  # Not used
        try:
            current_branch = self.manager.get_current_branch()
            raw_branches = self.manager.list_branches(verbose=params.verbose, remote=params.remote)

            branches = []
            for line in raw_branches:
                line_str = line.strip()
                if not line_str:
                    continue
                is_current = line_str.startswith("*")
                # Remove current branch prefix *
                cleaned = line_str.removeprefix("*").strip()

                # The first word is the branch name
                parts = cleaned.split()
                if not parts:
                    continue
                name = parts[0]

                # If verbose, we might have hash and upstream info
                commit_hash = None
                upstream = None
                if params.verbose and len(parts) > 1:
                    commit_hash = parts[1]
                    for part in parts[2:]:
                        if part.startswith("[") and part.endswith("]"):
                            upstream = part[1:-1]
                            break

                if name == current_branch:
                    is_current = True

                branches.append(
                    BranchDetailDTO(
                        name=name,
                        is_current=is_current,
                        commit_hash=commit_hash,
                        upstream=upstream,
                    )
                )

            return GitListBranchesOutput(
                success=True,
                current_branch=current_branch,
                branches=branches,
                branches_count=len(branches),
            )
        except Exception as e:
            return GitListBranchesOutput(
                success=False,
                error_message=str(e),
                current_branch="",
                branches=[],
                branches_count=0,
            )


class GitDiffInput(BaseModel):
    """Input for GitDiffTool."""

    model_config = ConfigDict(extra="forbid")

    target_branch: str = Field(..., description="Target branch to compare against (e.g. main)")
    source_branch: str = Field(default="HEAD", description="Source branch (default: HEAD)")


class GitDiffTool(ILegacyTool):
    """Tool to get diff statistics between branches."""

    @property
    def name(self) -> str:
        return "git_diff_stat"

    @property
    def description(self) -> str:
        return "Get diff statistics between two branches"

    @property
    def args_model(self) -> type[BaseModel] | None:
        return GitDiffInput

    def __init__(self, manager: GitManager) -> None:
        self.manager = manager

    @property
    def input_schema(self) -> dict[str, Any]:
        assert self.args_model is not None
        return self.args_model.model_json_schema()

    async def execute(self, params: GitDiffInput, context: NoteContext) -> GitDiffOutput:
        del context  # Not used
        try:
            stats = self.manager.compare_branches(params.target_branch, params.source_branch)

            files_match = re.search(r"(\d+)\s+file[s]?\s+changed", stats)
            insertions_match = re.search(r"(\d+)\s+insertion[s]?\(\+\)", stats)
            deletions_match = re.search(r"(\d+)\s+deletion[s]?\(-\)", stats)

            files_changed = int(files_match.group(1)) if files_match else None
            insertions = int(insertions_match.group(1)) if insertions_match else None
            deletions = int(deletions_match.group(1)) if deletions_match else None

            return GitDiffOutput(
                success=True,
                source_branch=params.source_branch,
                target_branch=params.target_branch,
                stats=stats,
                files_changed=files_changed,
                insertions=insertions,
                deletions=deletions,
            )
        except Exception as e:
            return GitDiffOutput(
                success=False,
                error_message=str(e),
                source_branch=params.source_branch,
                target_branch=params.target_branch,
                stats="",
                files_changed=None,
                insertions=None,
                deletions=None,
            )
