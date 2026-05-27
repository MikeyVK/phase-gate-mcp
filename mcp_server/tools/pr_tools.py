"""GitHub PR tools."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict, Field

from mcp_server.core.exceptions import ExecutionError, PreflightError
from mcp_server.core.interfaces import IPRStatusWriter, PRStatus
from mcp_server.core.operation_notes import NoteContext, RecoveryNote
from mcp_server.managers.github_manager import GitHubManager
from mcp_server.managers.phase_contract_resolver import MergeReadinessContext
from mcp_server.schemas import GitConfig
from mcp_server.tools.base import BaseTool, BranchMutatingTool
from mcp_server.tools.tool_result import ToolResult

if TYPE_CHECKING:
    from mcp_server.managers.git_manager import GitManager


class ListPRsInput(BaseModel):
    """Input for ListPRsTool."""

    model_config = ConfigDict(extra="forbid")

    state: str = Field(
        default="open", description="Filter by PR state", pattern="^(open|closed|all)$"
    )
    base: str | None = Field(default=None, description="Filter by base branch")
    head: str | None = Field(default=None, description="Filter by head branch")


class ListPRsTool(BaseTool):
    """Tool to list pull requests."""

    name = "list_prs"
    description = "List pull requests with optional state/base/head filters"
    args_model = ListPRsInput

    def __init__(self, manager: GitHubManager, git_config: GitConfig) -> None:
        self.manager = manager
        self._git_config = git_config

    @property
    def input_schema(self) -> dict[str, Any]:
        return super().input_schema

    async def execute(self, params: ListPRsInput, context: NoteContext) -> ToolResult:
        del context  # Not used
        try:
            prs = self.manager.list_prs(state=params.state, base=params.base, head=params.head)
        except ExecutionError as e:
            return ToolResult.error(str(e))

        if not prs:
            return ToolResult.text("No pull requests found matching the criteria.")

        lines = [f"Found {len(prs)} pull request(s):\n"]
        for pr in prs:
            lines.append(
                f"- #{pr.number}: {pr.title}\n"
                f"  State: {pr.state} | Base: {pr.base.ref} | Head: {pr.head.ref}\n"
            )

        return ToolResult.text("\n".join(lines))


class MergePRInput(BaseModel):
    """Input for MergePRTool."""

    model_config = ConfigDict(extra="forbid")

    pr_number: int = Field(..., description="Pull request number to merge")
    commit_message: str | None = Field(
        default=None, description="Optional commit message for the merge"
    )
    merge_method: str = Field(
        default="merge", description="Merge strategy (only 'merge' is supported)", pattern="^merge$"
    )


class MergePRTool(BaseTool):
    """Tool to merge a pull request."""

    name = "merge_pr"
    description = "Merge a pull request with optional commit message and method"
    args_model = MergePRInput

    def __init__(
        self,
        manager: GitHubManager,
        git_config: GitConfig,
        pr_status_writer: IPRStatusWriter,
    ) -> None:
        self.manager = manager
        self._git_config = git_config
        self._pr_status_writer = pr_status_writer

    @property
    def input_schema(self) -> dict[str, Any]:
        return super().input_schema

    async def execute(self, params: MergePRInput, context: NoteContext) -> ToolResult:
        del context  # Not used
        try:
            model = self.manager.get_pr(params.pr_number)
            head_branch = model.head_branch
            result = self.manager.merge_pr(
                pr_number=params.pr_number,
                commit_message=params.commit_message,
                merge_method=params.merge_method,
            )
        except ExecutionError as e:
            return ToolResult.error(str(e))

        self._pr_status_writer.set_pr_status(head_branch, PRStatus.ABSENT)
        return ToolResult.text(
            f"Merged PR #{params.pr_number} using {params.merge_method} (SHA {result['sha']})"
        )


class GetPRInput(BaseModel):
    """Input for GetPRTool."""

    model_config = ConfigDict(extra="forbid")

    pr_number: int = Field(..., description="Pull request number")


class GetPRTool(BaseTool):
    """Tool to get a single pull request."""

    name = "get_pr"
    description = "Get detailed information about a specific pull request"
    args_model = GetPRInput

    def __init__(self, manager: GitHubManager) -> None:
        self.manager = manager

    @property
    def input_schema(self) -> dict[str, Any]:
        return super().input_schema

    async def execute(self, params: GetPRInput, context: NoteContext) -> ToolResult:
        del context  # Not used
        try:
            model = self.manager.get_pr(params.pr_number)
        except ExecutionError as e:
            return ToolResult.error(str(e))
        return ToolResult.text(json.dumps(model.model_dump(), indent=2))


class SubmitPRInput(BaseModel):
    """Input for SubmitPRTool — atomic branch submission."""

    model_config = ConfigDict(extra="forbid")

    head: str = Field(..., description="Source branch name (e.g. feature/42-name)")
    title: str = Field(..., description="PR title")
    base: str | None = Field(default=None, description="Target branch (defaults to main)")
    body: str | None = Field(default=None, description="PR description (markdown)")
    draft: bool = Field(default=False, description="Create as draft PR")


class SubmitPRTool(BranchMutatingTool):
    """Atomic branch-submission tool.

    Performs: neutralize branch-local artifacts → commit → push → create PR
    → write PRStatus.OPEN to PRStatusCache in one tool call.

    Readiness gate (phase == ready) is enforced via enforcement.yaml, not here.
    Blocked when PRStatus.OPEN already exists on this branch (check_pr_status rule).
    """

    name = "submit_pr"
    description = "Atomically neutralize, commit, push, and create a PR for the current branch"
    args_model = SubmitPRInput
    enforcement_event: str | None = "submit_pr"

    def __init__(
        self,
        git_manager: GitManager,
        github_manager: GitHubManager,
        pr_status_writer: IPRStatusWriter,
        merge_readiness_context: MergeReadinessContext,
    ) -> None:
        self._git_manager = git_manager
        self._github_manager = github_manager
        self._pr_status_writer = pr_status_writer
        self._merge_readiness_context = merge_readiness_context

    @property
    def input_schema(self) -> dict[str, Any]:
        return super().input_schema

    async def execute(self, params: SubmitPRInput, context: NoteContext) -> ToolResult:
        branch = self._git_manager.get_current_branch()
        base = params.base or self._git_manager.git_config.default_base_branch
        artifact_paths = frozenset(
            a.path for a in self._merge_readiness_context.branch_local_artifacts
        )
        # [GIT] Full git transaction
        try:
            commit_made = self._git_manager.prepare_submission(artifact_paths, base, context)
        except (PreflightError, ExecutionError) as exc:
            return ToolResult.error(str(exc))
        # [GITHUB] Create PR — rollback push on failure
        try:
            result = self._github_manager.create_pr(
                title=params.title,
                body=params.body or "",
                head=params.head,
                base=base,
                draft=params.draft,
            )
        except ExecutionError as exc:
            if commit_made:
                try:
                    self._git_manager.rollback_push(context)
                    context.produce(
                        RecoveryNote(
                            f"GitHub PR creation failed: {exc}. "
                            "Remote branch has been rolled back to pre-submit state. "
                            "Working tree is clean. Retry submit_pr once the API issue is resolved."
                        )
                    )
                except ExecutionError:
                    pass  # RecoveryNote already produced by rollback_push
            return ToolResult.error(str(exc))
        # [STATUS] Record PR as open
        self._pr_status_writer.set_pr_status(branch, PRStatus.OPEN)
        return ToolResult.text(f"Created PR #{result['number']}: {result['url']}")
