"""Git tools."""

import json
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any, ClassVar, Literal

import anyio
from pydantic import BaseModel, ConfigDict, Field, field_validator

from mcp_server.core.exceptions import MCPError
from mcp_server.core.interfaces import IContextLoadedWriter
from mcp_server.core.logging import get_logger
from mcp_server.core.operation_notes import CommitNote, NoteContext
from mcp_server.managers import phase_state_engine
from mcp_server.managers.git_manager import BranchDeleteResult, GitManager
from mcp_server.managers.phase_contract_resolver import PhaseContractResolver
from mcp_server.managers.state_repository import StateBranchMismatchError
from mcp_server.schemas import GitConfig
from mcp_server.tools.base import BaseTool, BranchMutatingTool
from mcp_server.tools.tool_result import ToolResult

logger = get_logger("tools.git")


class CommitPhaseMismatchError(MCPError):
    """Raised when the provided workflow_phase/cycle_number doesn't match state.json."""


def build_commit_type_resolver(
    state_engine: phase_state_engine.PhaseStateEngine,
    resolver: PhaseContractResolver,
) -> Callable[[str, str, str | None], str | None]:
    """Build a resolver that derives commit types from injected phase contracts."""

    def resolve_commit_type(branch: str, workflow_phase: str, sub_phase: str | None) -> str | None:
        try:
            state = state_engine.get_state(branch)
        except StateBranchMismatchError:
            return None
        return resolver.resolve_commit_type(state.workflow_name, workflow_phase, sub_phase)

    return resolve_commit_type


def build_phase_guard(server_root: Path) -> Callable[[str, str, int | None], None]:
    """Build a guard callable that blocks commits when phase/cycle mismatches state.json."""
    state_file = server_root / "state.json"

    def phase_mismatch(branch: str, workflow_phase: str, cycle_number: int | None) -> None:
        if not state_file.exists():
            return
        data: dict[str, Any] = json.loads(state_file.read_text(encoding="utf-8"))
        if data.get("branch") != branch:
            return  # state.json belongs to a different branch — skip

        current_phase = data.get("current_phase", "unknown")
        if workflow_phase != current_phase:
            msg = (
                f"Phase mismatch: committing as '{workflow_phase}' "
                f"but state.json shows current_phase='{current_phase}'.\n"
                f"Run first: transition_phase(branch='{branch}', to_phase='{workflow_phase}')"
            )
            raise CommitPhaseMismatchError(msg)

        if workflow_phase == "implementation" and cycle_number is not None:
            current_cycle = data.get("current_cycle")
            if current_cycle is not None and cycle_number != current_cycle:
                msg = (
                    f"Cycle mismatch: committing as cycle {cycle_number} "
                    f"but state.json shows current_cycle={current_cycle}.\n"
                    f"Run first: transition_cycle(to_cycle={cycle_number})"
                )
                raise CommitPhaseMismatchError(msg)

    return phase_mismatch


def _input_schema(args_model: type[BaseModel] | None) -> dict[str, Any]:
    if args_model is None:
        return {}
    return args_model.model_json_schema()


class CreateBranchInput(BaseModel):
    """Input for CreateBranchTool."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., description="Branch name (kebab-case)")
    branch_type: str = Field(default="feature", description="Branch type")
    _git_config: ClassVar[GitConfig | None] = None

    @classmethod
    def configure(cls, git_config: GitConfig) -> None:
        cls._git_config = git_config

    @classmethod
    def _require_git_config(cls) -> GitConfig:
        if cls._git_config is None:
            raise ValueError("GitConfig must be injected before branch input validation")
        return cls._git_config

    base_branch: str = Field(
        ...,
        description="Base branch to create from (e.g., 'HEAD', 'main', 'refactor/51-labels-yaml')",
    )

    @field_validator("branch_type")
    @classmethod
    def validate_branch_type(cls, value: str) -> str:
        """Validate branch_type against GitConfig (Convention #7)."""
        git_config = cls._require_git_config()
        if not git_config.has_branch_type(value):
            valid_types = ", ".join(git_config.branch_types)
            raise ValueError(
                f"Invalid branch_type '{value}'. Valid types from git.yaml: {valid_types}"
            )
        return value


class CreateBranchTool(BranchMutatingTool):
    """Tool to create a git branch from specified base."""

    name = "create_branch"
    description = "Create a new branch from specified base branch"
    args_model = CreateBranchInput
    enforcement_event = "create_branch"

    def __init__(
        self,
        manager: GitManager | None = None,
        state_engine: phase_state_engine.PhaseStateEngine | None = None,
    ) -> None:
        if manager is None:
            raise ValueError("GitManager must be injected")
        self.manager = manager
        self._state_engine = state_engine
        CreateBranchInput.configure(self.manager.git_config)

    def _get_state_engine(self) -> phase_state_engine.PhaseStateEngine:
        if self._state_engine is None:
            raise ValueError("PhaseStateEngine must be injected for git tools that sync state")
        return self._state_engine

    @property
    def input_schema(self) -> dict[str, Any]:
        return _input_schema(self.args_model)

    async def execute(self, params: CreateBranchInput, context: NoteContext) -> ToolResult:
        logger.info(
            "Branch creation requested",
            extra={
                "props": {
                    "name": params.name,
                    "branch_type": params.branch_type,
                    "base_branch": params.base_branch,
                }
            },
        )

        try:
            branch_name = self.manager.create_branch(
                params.name, params.branch_type, params.base_branch, context
            )
            return ToolResult.text(f"\u2705 Created and switched to branch: {branch_name}")
        except Exception as e:
            logger.error(
                "Branch creation failed", extra={"props": {"name": params.name, "error": str(e)}}
            )
            raise


class GitStatusInput(BaseModel):
    """Input for GitStatusTool (empty)."""

    model_config = ConfigDict(extra="forbid")


class GitStatusTool(BaseTool):
    """Tool to check git status."""

    name = "git_status"
    description = "Check current git status"
    args_model = GitStatusInput

    def __init__(
        self,
        manager: GitManager | None = None,
        state_engine: phase_state_engine.PhaseStateEngine | None = None,
    ) -> None:
        if manager is None:
            raise ValueError("GitManager must be injected")
        self.manager = manager
        self._state_engine = state_engine

    def _get_state_engine(self) -> phase_state_engine.PhaseStateEngine:
        if self._state_engine is None:
            raise ValueError("PhaseStateEngine must be injected for git tools that sync state")
        return self._state_engine

    @property
    def input_schema(self) -> dict[str, Any]:
        return _input_schema(self.args_model)

    async def execute(
        self,
        params: GitStatusInput,
        context: NoteContext,
    ) -> ToolResult:
        del params
        del context

        status = self.manager.get_status()

        text = f"Branch: {status['branch']}\n"
        text += f"Clean: {status['is_clean']}\n"
        if status["untracked_files"]:
            text += f"Untracked: {', '.join(status['untracked_files'])}\n"
        if status["modified_files"]:
            text += f"Modified: {', '.join(status['modified_files'])}\n"

        return ToolResult.text(text)


class GitCommitInput(BaseModel):
    """Input for GitCommitTool."""

    _git_config: ClassVar[GitConfig | None] = None

    @classmethod
    def configure(cls, git_config: GitConfig) -> None:
        cls._git_config = git_config

    model_config = ConfigDict(extra="forbid")

    message: str = Field(..., description="Commit message (without type/scope prefix)")
    files: list[str] | None = Field(
        default=None,
        description=(
            "Optional list of file paths to stage and commit. When omitted, commits all changes."
        ),
    )

    # NEW: Workflow-first fields
    workflow_phase: str | None = Field(
        default=None,
        description=(
            "Workflow phase (research|planning|design|tdd|integration|documentation|coordination). "
            "Required when using new workflow-first format."
        ),
    )
    sub_phase: str | None = Field(
        default=None,
        description=(
            "Sub-phase (MUST be in workphases.yaml[phase].subphases). "
            "Examples: 'red', 'green', 'c1'. Optional."
        ),
    )
    cycle_number: int | None = Field(
        default=None,
        description="Cycle number (e.g., 1, 2, 3). Optional, used in multi-cycle TDD.",
    )
    commit_type: str | None = Field(
        default=None,
        description=(
            "Commit type override (test|feat|refactor|docs|chore|fix). "
            "Auto-determined from workphases.yaml if omitted."
        ),
    )

    @field_validator("commit_type")
    @classmethod
    def validate_commit_type(cls, value: str | None) -> str | None:
        """Validate commit_type against GitConfig (Convention #6). Only if provided."""
        if value is None:
            return None

        git_config = cls._git_config
        if git_config is None:
            raise ValueError("GitConfig must be injected before validation")
        if not git_config.has_commit_type(value):
            valid_types = ", ".join(git_config.commit_types)
            raise ValueError(
                f"Invalid commit_type '{value}'. "
                f"Valid types from git.yaml: {valid_types}. "
                f"See: https://www.conventionalcommits.org/"
            )

        return value.lower()  # Normalize to lowercase


class GitCommitTool(BranchMutatingTool):
    """Tool to commit changes with workflow-scoped commit messages."""

    name = "git_add_or_commit"
    description = "Commit changes with workflow phase scope (e.g., test(P_TDD_SP_RED): message)"
    args_model = GitCommitInput
    enforcement_event: str | None = "git_add_or_commit"

    def __init__(
        self,
        manager: GitManager | None = None,
        phase_guard: Callable[[str, str, int | None], None] | None = None,
        commit_type_resolver: Callable[[str, str, str | None], str | None] | None = None,
        state_engine: phase_state_engine.PhaseStateEngine | None = None,
    ) -> None:
        if manager is None:
            raise ValueError("GitManager must be injected")
        self.manager = manager
        GitCommitInput.configure(self.manager.git_config)
        self._phase_guard = phase_guard
        self._commit_type_resolver = commit_type_resolver
        self._state_engine = state_engine

    @property
    def input_schema(self) -> dict[str, Any]:
        return _input_schema(self.args_model)

    async def execute(self, params: GitCommitInput, context: NoteContext) -> ToolResult:
        workflow_phase = params.workflow_phase
        current_branch = self.manager.adapter.get_current_branch()
        issue_number: int | None = None

        if workflow_phase is None:
            if self._state_engine is None:
                raise ValueError("PhaseStateEngine must be injected for auto-detection")
            try:
                state = self._state_engine.get_state(current_branch)
                workflow_phase = state.current_phase
                issue_number = state.issue_number
            except (FileNotFoundError, StateBranchMismatchError):
                return ToolResult.error(
                    f"No state.json found for branch '{current_branch}'. "
                    "Provide workflow_phase explicitly: "
                    "git_add_or_commit(workflow_phase='<phase>', message='...')"
                )

            logger.info(
                "Auto-detected workflow_phase from state.json",
                extra={"props": {"branch": current_branch, "workflow_phase": workflow_phase}},
            )
        else:
            issue_number = self.manager.git_config.extract_issue_number(current_branch)

        if workflow_phase == "implementation" and params.cycle_number is None:
            raise ValueError(
                "cycle_number is required for TDD phase commits. "
                "All TDD work belongs to a specific cycle. "
                "Use: git_add_or_commit(workflow_phase='implementation', cycle_number=N, ...)"
            )

        if self._phase_guard is not None:
            self._phase_guard(current_branch, workflow_phase, params.cycle_number)

        commit_type = params.commit_type
        if commit_type is None and self._commit_type_resolver is not None:
            commit_type = self._commit_type_resolver(
                current_branch,
                workflow_phase,
                params.sub_phase,
            )

        ctx = context
        commit_hash = self.manager.commit_with_scope(
            workflow_phase=workflow_phase,
            message=params.message,
            note_context=ctx,
            sub_phase=params.sub_phase,
            cycle_number=params.cycle_number,
            commit_type=commit_type,
            files=params.files,
            skip_paths=frozenset(),
            issue_number=issue_number,
        )
        ctx.produce(CommitNote(commit_hash=commit_hash))
        if self._state_engine is not None:
            self._state_engine.record_sub_phase(current_branch, params.sub_phase)
        return ToolResult.text(f"Committed: {commit_hash}")


class GitRestoreInput(BaseModel):
    """Input for GitRestoreTool."""

    model_config = ConfigDict(extra="forbid")

    files: list[str] = Field(
        ..., min_length=1, description="File paths to restore (discard local changes)"
    )
    source: str = Field(default="HEAD", description="Git ref to restore from (default: HEAD)")


class GitRestoreTool(BranchMutatingTool):
    """Tool to restore files to a ref (discard local changes)."""

    name = "git_restore"
    description = "Restore files to a git ref (discard local changes)"
    args_model = GitRestoreInput

    def __init__(
        self,
        manager: GitManager | None = None,
        state_engine: phase_state_engine.PhaseStateEngine | None = None,
    ) -> None:
        if manager is None:
            raise ValueError("GitManager must be injected")
        self.manager = manager
        self._state_engine = state_engine

    def _get_state_engine(self) -> phase_state_engine.PhaseStateEngine:
        if self._state_engine is None:
            raise ValueError("PhaseStateEngine must be injected for git tools that sync state")
        return self._state_engine

    @property
    def input_schema(self) -> dict[str, Any]:
        return _input_schema(self.args_model)

    async def execute(self, params: GitRestoreInput, context: NoteContext) -> ToolResult:
        self.manager.restore(files=params.files, note_context=context, source=params.source)
        return ToolResult.text(f"Restored {len(params.files)} file(s) from {params.source}")


class GitCheckoutInput(BaseModel):
    """Input for GitCheckoutTool."""

    model_config = ConfigDict(extra="forbid")

    branch: str = Field(..., description="Branch name to checkout")


class GitCheckoutTool(BaseTool):
    """Tool to checkout to a branch.

    Automatically synchronizes PhaseStateEngine state after branch switch
    to ensure correct TDD phase tracking.
    """

    name = "git_checkout"
    description = "Switch to an existing branch"
    args_model = GitCheckoutInput

    def __init__(
        self,
        manager: GitManager | None = None,
        state_engine: phase_state_engine.PhaseStateEngine | None = None,
        context_loaded_writer: IContextLoadedWriter | None = None,
    ) -> None:
        if manager is None:
            raise ValueError("GitManager must be injected")
        self.manager = manager
        self._state_engine = state_engine
        self._context_loaded_writer = context_loaded_writer

    def _get_state_engine(self) -> phase_state_engine.PhaseStateEngine:
        if self._state_engine is None:
            raise ValueError("PhaseStateEngine must be injected for git tools that sync state")
        return self._state_engine

    @property
    def input_schema(self) -> dict[str, Any]:
        return _input_schema(self.args_model)

    async def execute(self, params: GitCheckoutInput, context: NoteContext) -> ToolResult:
        del context

        try:
            # GitPython operations can block; run them in a worker thread.
            await anyio.to_thread.run_sync(self.manager.checkout, params.branch)
        except MCPError as exc:
            logger.error(
                "Branch checkout failed",
                extra={"props": {"branch": params.branch, "error": str(exc)}},
            )
            return ToolResult.error(str(exc))

        current_phase = "unknown"
        parent_branch: str | None = None
        try:
            state_engine = self._get_state_engine()
            state = await anyio.to_thread.run_sync(state_engine.get_state, params.branch)
            current_phase = state.current_phase or "unknown"
            parent_branch = state.parent_branch
        except (MCPError, ValueError, OSError, StateBranchMismatchError) as exc:
            logger.warning(
                "Phase state sync failed after checkout",
                extra={"props": {"branch": params.branch, "error": str(exc)}},
            )

        output = f"Switched to branch: {params.branch}\nCurrent phase: {current_phase}"
        if parent_branch:
            output += f"\nParent branch: {parent_branch}"

        if self._context_loaded_writer is not None:
            self._context_loaded_writer.set_context_loaded(params.branch, value=False)
        return ToolResult.text(output)


class GitPushInput(BaseModel):
    """Input for GitPushTool."""

    model_config = ConfigDict(extra="forbid")

    set_upstream: bool = Field(
        default=False, description="Set upstream tracking (for new branches)"
    )


class GitPushTool(BranchMutatingTool):
    """Tool to push current branch to origin."""

    name = "git_push"
    description = "Push current branch to origin remote"
    args_model = GitPushInput

    def __init__(
        self,
        manager: GitManager | None = None,
        state_engine: phase_state_engine.PhaseStateEngine | None = None,
    ) -> None:
        if manager is None:
            raise ValueError("GitManager must be injected")
        self.manager = manager
        self._state_engine = state_engine

    def _get_state_engine(self) -> phase_state_engine.PhaseStateEngine:
        if self._state_engine is None:
            raise ValueError("PhaseStateEngine must be injected for git tools that sync state")
        return self._state_engine

    @property
    def input_schema(self) -> dict[str, Any]:
        return _input_schema(self.args_model)

    async def execute(self, params: GitPushInput, context: NoteContext) -> ToolResult:
        del context

        status = self.manager.get_status()
        self.manager.push(set_upstream=params.set_upstream)
        return ToolResult.text(f"Pushed branch: {status['branch']}")


class GitMergeInput(BaseModel):
    """Input for GitMergeTool."""

    model_config = ConfigDict(extra="forbid")

    branch: str = Field(..., description="Branch name to merge")


class GitMergeTool(BranchMutatingTool):
    """Tool to merge a branch into current branch."""

    name = "git_merge"
    description = "Merge a branch into the current branch"
    args_model = GitMergeInput

    def __init__(
        self,
        manager: GitManager | None = None,
        state_engine: phase_state_engine.PhaseStateEngine | None = None,
    ) -> None:
        if manager is None:
            raise ValueError("GitManager must be injected")
        self.manager = manager
        self._state_engine = state_engine

    def _get_state_engine(self) -> phase_state_engine.PhaseStateEngine:
        if self._state_engine is None:
            raise ValueError("PhaseStateEngine must be injected for git tools that sync state")
        return self._state_engine

    @property
    def input_schema(self) -> dict[str, Any]:
        return _input_schema(self.args_model)

    async def execute(self, params: GitMergeInput, context: NoteContext) -> ToolResult:
        status = self.manager.get_status()
        self.manager.merge(params.branch, context)
        return ToolResult.text(f"Merged {params.branch} into {status['branch']}")


class GitDeleteBranchInput(BaseModel):
    """Input for GitDeleteBranchTool."""

    model_config = ConfigDict(extra="forbid")

    branch: str = Field(..., description="Branch name to delete")
    force: bool = Field(default=False, description="Force delete unmerged branch")
    mode: Literal["local", "remote", "both"] = Field(
        default="both",
        description="Deletion scope: local-only, remote-only, or both (default)",
    )


class GitDeleteBranchTool(BranchMutatingTool):
    """Tool to delete a branch."""

    name = "git_delete_branch"
    description = "Delete a git branch (cannot delete protected branches)"
    args_model = GitDeleteBranchInput

    def __init__(
        self,
        manager: GitManager | None = None,
        state_engine: phase_state_engine.PhaseStateEngine | None = None,
    ) -> None:
        if manager is None:
            raise ValueError("GitManager must be injected")
        self.manager = manager
        self._state_engine = state_engine

    def _get_state_engine(self) -> phase_state_engine.PhaseStateEngine:
        if self._state_engine is None:
            raise ValueError("PhaseStateEngine must be injected for git tools that sync state")
        return self._state_engine

    @property
    def input_schema(self) -> dict[str, Any]:
        return _input_schema(self.args_model)

    async def execute(self, params: GitDeleteBranchInput, context: NoteContext) -> ToolResult:
        result: BranchDeleteResult = self.manager.delete_branch(
            params.branch, context, force=params.force, mode=params.mode
        )
        parts: list[str] = []
        if result.local_status != "skipped":
            parts.append(f"local: {result.local_status}")
        if result.remote_status != "skipped":
            parts.append(f"remote: {result.remote_status}")
        suffix = f" ({', '.join(parts)})" if parts else ""
        return ToolResult.text(f"Deleted branch: {params.branch}{suffix}")


class GitStashInput(BaseModel):
    """Input for GitStashTool."""

    model_config = ConfigDict(extra="forbid")

    action: str = Field(
        ...,
        description="Stash action: push (save), pop (restore), list",
        pattern="^(push|pop|list)$",
    )
    message: str | None = Field(
        default=None, description="Optional name for the stash (only for push)"
    )
    include_untracked: bool = Field(
        default=False, description="Include untracked files when stashing (git stash push -u)"
    )


class GitStashTool(BaseTool):
    """Tool to stash changes in a dirty working directory."""

    name = "git_stash"
    description = "Stash the changes in a dirty working directory (git stash)"
    args_model = GitStashInput

    def __init__(
        self,
        manager: GitManager | None = None,
        state_engine: phase_state_engine.PhaseStateEngine | None = None,
    ) -> None:
        if manager is None:
            raise ValueError("GitManager must be injected")
        self.manager = manager
        self._state_engine = state_engine

    def _get_state_engine(self) -> phase_state_engine.PhaseStateEngine:
        if self._state_engine is None:
            raise ValueError("PhaseStateEngine must be injected for git tools that sync state")
        return self._state_engine

    @property
    def input_schema(self) -> dict[str, Any]:
        return _input_schema(self.args_model)

    async def execute(self, params: GitStashInput, context: NoteContext) -> ToolResult:
        del context

        if params.action == "push":
            self.manager.stash(message=params.message, include_untracked=params.include_untracked)
            if params.message:
                return ToolResult.text(f"Stashed changes: {params.message}")
            return ToolResult.text("Stashed current changes")
        if params.action == "pop":
            self.manager.stash_pop()
            return ToolResult.text("Applied and removed latest stash")
        if params.action == "list":
            stashes = self.manager.stash_list()
            if not stashes:
                return ToolResult.text("No stashes found")
            return ToolResult.text("\n".join(stashes))
        return ToolResult.text(f"Unknown action: {params.action}")


class GetParentBranchInput(BaseModel):
    """Input for GetParentBranchTool."""

    model_config = ConfigDict(extra="forbid")

    branch: str | None = Field(
        default=None, description="Branch name to inspect (default: current branch)"
    )


class GetParentBranchTool(BaseTool):
    """Tool to show a branch's configured parent branch.

    Issue #79: Parent branch is tracked in PhaseStateEngine state.
    """

    name = "get_parent_branch"
    description = "Detect parent branch for a branch (via PhaseStateEngine state)"
    args_model = GetParentBranchInput

    def __init__(
        self,
        manager: GitManager | None = None,
        state_engine: phase_state_engine.PhaseStateEngine | None = None,
    ) -> None:
        if manager is None:
            raise ValueError("GitManager must be injected")
        self.manager = manager
        self._state_engine = state_engine

    def _get_state_engine(self) -> phase_state_engine.PhaseStateEngine:
        if self._state_engine is None:
            raise ValueError("PhaseStateEngine must be injected for git tools that inspect state")
        return self._state_engine

    @property
    def input_schema(self) -> dict[str, Any]:
        return _input_schema(self.args_model)

    async def execute(self, params: GetParentBranchInput, context: NoteContext) -> ToolResult:
        del context

        if self._state_engine is None:
            return ToolResult.error("PhaseStateEngine must be injected")

        try:
            branch = params.branch or self.manager.get_current_branch()
            state = await anyio.to_thread.run_sync(self._state_engine.get_state, branch)
            parent = state.parent_branch

            if parent:
                return ToolResult.text(f"Branch: {branch}\nParent branch: {parent}")
            return ToolResult.text(f"Branch: {branch}\nParent branch: (not set)")
        except (
            subprocess.CalledProcessError,
            subprocess.TimeoutExpired,
            OSError,
            StateBranchMismatchError,
        ) as exc:
            return ToolResult.error(f"Failed to get parent branch: {exc}")
