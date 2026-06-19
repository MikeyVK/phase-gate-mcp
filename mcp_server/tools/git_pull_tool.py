"""Git pull tool.

Pull updates from a remote into the current branch.

Responsibilities:
- Execute potentially blocking GitPython network operations via `anyio.to_thread.run_sync`.
- Enforce safe-by-default behavior via GitManager preflight.
- Re-sync PhaseStateEngine state after a successful pull.

Usage example:
- Call `git_pull` with {"remote": "origin", "rebase": false}

@layer: Tools
@dependencies: [GitManager, PhaseStateEngine, anyio]
"""

from __future__ import annotations

from typing import Any

import anyio
from pydantic import BaseModel, ConfigDict, Field

from mcp_server.core.exceptions import MCPError
from mcp_server.core.interfaces import IContextLoadedWriter
from mcp_server.core.logging import get_logger
from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers import phase_state_engine
from mcp_server.managers.git_manager import GitManager
from mcp_server.managers.state_repository import StateBranchMismatchError
from mcp_server.schemas.tool_outputs import GitPullOutput
from mcp_server.tools.base import ILegacyTool

logger = get_logger("tools.git_pull")


class GitPullInput(BaseModel):
    """Input for GitPullTool."""

    model_config = ConfigDict(extra="forbid")

    remote: str = Field(
        default="origin",
        description="Remote name to pull from (default: origin)",
    )
    rebase: bool = Field(
        default=False,
        description="Use --rebase instead of merge",
    )


class GitPullTool(ILegacyTool):
    """Pull updates from a remote into the current branch.

    Responsibilities:
    - Offload git pull to a worker thread (Issue #85 stdio hang prevention).
    - Re-sync PhaseStateEngine after pull to reduce state drift.

    Usage example:
    - Call with {"remote": "origin", "rebase": false}
    """

    tool_category = "branch_mutating"

    @property
    def name(self) -> str:
        return "git_pull"

    @property
    def description(self) -> str:
        return "Pull updates from a remote"

    @property
    def args_model(self) -> type[BaseModel] | None:
        return GitPullInput

    def __init__(
        self,
        manager: GitManager,
        state_engine: phase_state_engine.PhaseStateEngine | None = None,
        context_loaded_writer: IContextLoadedWriter | None = None,
    ) -> None:
        self.manager = manager
        self._state_engine = state_engine
        self._context_loaded_writer = context_loaded_writer

    def _get_state_engine(self) -> phase_state_engine.PhaseStateEngine:
        if self._state_engine is None:
            raise ValueError("PhaseStateEngine must be injected for git_pull")
        return self._state_engine

    @property
    def input_schema(self) -> dict[str, Any]:
        return _input_schema(self.args_model)

    async def execute(self, params: GitPullInput, context: NoteContext) -> GitPullOutput:
        pull_result = ""
        try:
            pull_result = await anyio.to_thread.run_sync(
                lambda: self.manager.pull(
                    note_context=context, remote=params.remote, rebase=params.rebase
                )
            )
        except MCPError as exc:
            logger.error(
                "git_pull failed",
                extra={"props": {"remote": params.remote, "error": str(exc)}},
            )
            return GitPullOutput(
                success=False,
                error_message=str(exc),
                remote=params.remote,
                raw_output="",
                rebase=params.rebase,
            )
        except (OSError, ValueError, RuntimeError) as exc:
            logger.error(
                "git_pull failed (runtime)",
                extra={"props": {"remote": params.remote, "error": str(exc)}},
            )
            return GitPullOutput(
                success=False,
                error_message=f"Pull failed: {exc}",
                remote=params.remote,
                raw_output="",
                rebase=params.rebase,
            )

        # Sync phase state after pull (commits may have changed).
        try:
            current_branch = self.manager.get_current_branch()
            if self._context_loaded_writer is not None and not pull_result.lower().startswith(
                "already up to date"
            ):
                self._context_loaded_writer.set_context_loaded(current_branch, value=False)
            await anyio.to_thread.run_sync(self._get_state_engine().get_state, current_branch)
        except (MCPError, ValueError, OSError, StateBranchMismatchError) as exc:
            logger.warning(
                "Phase state sync failed after pull",
                extra={"props": {"error": str(exc)}},
            )

        return GitPullOutput(
            success=True,
            remote=params.remote,
            raw_output=pull_result,
            rebase=params.rebase,
        )


def _input_schema(model: type[BaseModel] | None) -> dict[str, Any]:
    if model is None:
        return {}
    return model.model_json_schema()
