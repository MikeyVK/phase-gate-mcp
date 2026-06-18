# mcp_server/managers/enforcement_runner.py
# template=generic version=manual-cycle5 created=2026-03-13T11:20Z updated=
"""Enforcement configuration loading and dispatch.

Dispatch-level enforcement runner for tool events configured in
config/enforcement.yaml.
"""

from __future__ import annotations

import logging
import os
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
from typing import cast

from mcp_server.core.exceptions import ConfigError, ValidationError
from mcp_server.core.interfaces import IContextLoadedReader, IPRStatusReader, IStateReader, PRStatus
from mcp_server.core.operation_notes import (
    Note,
    NoteContext,
)
from mcp_server.schemas import EnforcementAction, EnforcementConfig, EnforcementRule, GitConfig
from mcp_server.tools.tool_result import ToolResult

_ENFORCEMENT_DISPLAY_PATH = "config/enforcement.yaml"
_GIT_TIMEOUT_SECONDS = 2
logger = logging.getLogger(__name__)

# Known tool_category values; config validation fails fast for any unlisted value.
KNOWN_TOOL_CATEGORIES: frozenset[str] = frozenset({"branch_mutating"})


def _git_command_env() -> dict[str, str]:
    """Build a non-interactive environment for git commands in request paths."""
    env = os.environ.copy()
    env.setdefault("GIT_TERMINAL_PROMPT", "0")
    env.setdefault("GIT_PAGER", "cat")
    env.setdefault("PAGER", "cat")
    return env


def _run_git_command(
    workspace_root: Path,
    args: list[str],
    failure_context: str,
) -> subprocess.CompletedProcess[str]:
    """Run a git subcommand non-interactively and return the CompletedProcess."""
    try:
        return subprocess.run(
            ["git", *args],
            cwd=workspace_root,
            env=_git_command_env(),
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            check=False,
            timeout=_GIT_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        logger.warning("git command failed (%s): %s", failure_context, exc)
        return subprocess.CompletedProcess(
            args=["git", *args], returncode=1, stdout="", stderr=str(exc)
        )


def _get_current_git_branch(workspace_root: Path) -> str | None:
    """Return the active git branch name, or None on detached HEAD / error."""
    result = _run_git_command(
        workspace_root,
        ["rev-parse", "--abbrev-ref", "HEAD"],
        failure_context="git rev-parse --abbrev-ref HEAD",
    )
    if result.returncode != 0:
        return None
    name = result.stdout.strip()
    return name if name and name != "HEAD" else None


__all__ = [
    "EnforcementAction",
    "EnforcementConfig",
    "EnforcementContext",
    "EnforcementConfig",
    "EnforcementRule",
    "EnforcementRunner",
]


@dataclass(frozen=True)
class EnforcementContext:
    """Runtime context passed to action handlers."""

    workspace_root: Path
    tool_name: str
    params: object
    tool_result: ToolResult | None = None

    def get_param(self, name: str) -> object | None:
        """Read one parameter from Pydantic models, namespaces, or dicts."""
        if hasattr(self.params, name):
            return cast(object, getattr(self.params, name))
        if isinstance(self.params, dict):
            return self.params.get(name)
        return None


ActionHandler = Callable[
    [EnforcementAction, EnforcementContext, Path, NoteContext],
    None,
]


class EnforcementRegistry:
    """Registry for named enforcement action handlers."""

    def __init__(self, handlers: dict[str, ActionHandler] | None = None) -> None:
        self._handlers = handlers or {}

    def register(self, action_type: str, handler: ActionHandler) -> None:
        """Register one action handler."""
        self._handlers[action_type] = handler

    def has(self, action_type: str) -> bool:
        """Check whether one action type is registered."""
        return action_type in self._handlers

    def get(self, action_type: str) -> ActionHandler:
        """Get one registered action handler."""
        return self._handlers[action_type]


class EnforcementRunner:
    """Load and execute enforcement rules for tool events."""

    def __init__(
        self,
        workspace_root: Path,
        config: EnforcementConfig,
        git_config: GitConfig,
        state_reader: IStateReader,
        registry: EnforcementRegistry | dict[str, ActionHandler] | None = None,
        pr_status_reader: IPRStatusReader | None = None,
        server_root: Path | None = None,
        context_loaded_reader: IContextLoadedReader | None = None,
    ) -> None:
        self.workspace_root = Path(workspace_root)
        if server_root is None:
            raise ValueError(
                "EnforcementRunner requires server_root. "
                "Pass server_root=workspace_root / settings.server.server_root_dir from server.py."
            )
        self.server_root = server_root
        self._config = config
        self._git_config = git_config
        self._state_reader = state_reader
        self._pr_status_reader = pr_status_reader
        self._context_loaded_reader = context_loaded_reader
        if registry is None:
            self._registry = self._build_default_registry()
        elif isinstance(registry, EnforcementRegistry):
            self._registry = registry
        else:
            self._registry = EnforcementRegistry(registry)
        self._validate_registered_actions()

    def run(
        self,
        event: str,
        timing: str,
        enforcement_ctx: EnforcementContext,
        note_context: NoteContext,
        tool_category: str | None = None,
    ) -> None:
        """Execute matching actions for one event and timing pair.

        C3: returns None; all results conveyed via note_context.produce().
        Dispatch matches on rule.tool (tool name) OR rule.tool_category (category).
        """
        for rule in self._config.enforcement:
            if rule.event_source != "tool":
                continue
            if rule.timing != timing:
                continue
            # Match by tool name or tool_category (mutually exclusive per schema validator)
            if rule.tool is not None and rule.tool != event:
                continue
            if rule.tool_category is not None and rule.tool_category != tool_category:
                continue
            if rule.tool is None and rule.tool_category is None:
                continue
            for action in rule.actions:
                self._registry.get(action.type)(
                    action, enforcement_ctx, self.workspace_root, note_context
                )

    def _validate_registered_actions(self) -> None:
        """Fail fast when config references unknown action types or tool categories."""
        unknown_actions = sorted(
            {
                action.type
                for rule in self._config.enforcement
                for action in rule.actions
                if not self._registry.has(action.type)
            }
        )
        if unknown_actions:
            raise ConfigError(
                f"Unknown enforcement action type(s): {', '.join(unknown_actions)}",
                file_path=_ENFORCEMENT_DISPLAY_PATH,
            )

        unknown_categories = sorted(
            {
                rule.tool_category
                for rule in self._config.enforcement
                if rule.tool_category is not None
                and rule.tool_category not in KNOWN_TOOL_CATEGORIES
            }
        )
        if unknown_categories:
            raise ConfigError(
                f"Unknown tool_category value(s): {', '.join(unknown_categories)}",
                file_path=_ENFORCEMENT_DISPLAY_PATH,
            )

    def _build_default_registry(self) -> EnforcementRegistry:
        """Build the default action registry."""
        registry = EnforcementRegistry()
        registry.register(
            "check_branch_policy",
            self._handle_check_branch_policy,
        )
        registry.register(
            "check_pr_status",
            self._handle_check_pr_status,
        )
        registry.register(
            "check_phase_readiness",
            self._handle_check_phase_readiness,
        )
        registry.register(
            "check_context_loaded",
            self._handle_check_context_loaded,
        )
        return registry

    def _handle_check_branch_policy(
        self,
        action: EnforcementAction,
        context: EnforcementContext,
        workspace_root: Path,
        note_context: NoteContext,
    ) -> None:
        """Block invalid branch creation bases based on branch-type rules."""
        del self, workspace_root
        branch_type = context.get_param("branch_type")
        base_branch = context.get_param("base_branch")
        if not branch_type or not base_branch:
            return

        allowed_patterns = action.rules.get(str(branch_type), [])
        if not allowed_patterns:
            return

        if any(fnmatch(str(base_branch), pattern) for pattern in allowed_patterns):
            return

        note_context.produce(
            Note(
                key="allowed_bases_suggestion",
                params={"bases": ", ".join(allowed_patterns)},
            )
        )
        raise ValidationError(
            f"Branch type '{branch_type}' cannot be created from base '{base_branch}'",
            error_code="invalid_base_branch",
            params={"branch_type": branch_type, "base_branch": base_branch},
        )

    def _handle_check_pr_status(
        self,
        action: EnforcementAction,
        context: EnforcementContext,
        workspace_root: Path,
        note_context: NoteContext,
    ) -> None:
        """Block branch-mutating tool calls when an open PR exists for this branch.

        Reads IPRStatusReader (session-leading cache, cold-start API fallback).
        Raises ConfigError when no reader is configured (misconfigured startup).
        Raises ValidationError when PRStatus.OPEN is found.
        """
        del action
        if self._pr_status_reader is None:
            raise ConfigError(
                "check_pr_status action requires pr_status_reader; "
                "wire PRStatusCache in EnforcementRunner.__init__",
                file_path=_ENFORCEMENT_DISPLAY_PATH,
            )
        # Prefer an explicit 'head' param; fall back to the current git branch.
        # Tool names must never be used as branch identifiers.
        branch = str(
            context.get_param("head")
            or _get_current_git_branch(workspace_root)
            or context.tool_name  # last-resort: should not happen in practice
        )
        status = self._pr_status_reader.get_pr_status(branch)
        if status == PRStatus.OPEN:
            note_context.produce(
                Note(
                    key="close_open_pr_suggestion",
                    params={},
                )
            )
            raise ValidationError(
                f"Branch '{branch}' has an open PR. "
                "Branch-mutating tools are blocked until the PR is merged.",
                error_code="open_pr_blocker",
                params={"branch": branch},
            )

    def _handle_check_phase_readiness(
        self,
        action: EnforcementAction,
        context: EnforcementContext,
        workspace_root: Path,
        note_context: NoteContext,
    ) -> None:
        """Block tool execution when the current workflow phase does not match policy.

        Reads action.policy as the required phase name; compares against
        live state.json via IStateReader. Raises ValidationError on mismatch or absent state.
        """
        required_phase = action.policy
        branch = str(
            context.get_param("current_branch") or _get_current_git_branch(workspace_root) or ""
        )
        try:
            current_phase: str | None = self._state_reader.load(branch).current_phase
        except Exception:
            current_phase = None
        if current_phase != required_phase:
            note_context.produce(
                Note(
                    key="transition_phase_suggestion",
                    params={"required_phase": required_phase},
                )
            )
            raise ValidationError(
                f"Tool requires phase '{required_phase}'. Current phase: '{current_phase}'.",
                error_code="phase_readiness_mismatch",
                params={"required_phase": required_phase, "current_phase": current_phase},
            )

    def _handle_check_context_loaded(
        self,
        action: EnforcementAction,
        context: EnforcementContext,
        workspace_root: Path,
        note_context: NoteContext,
    ) -> None:
        """Block tool execution until get_work_context has been called for this branch.

        Gate is explicitly disabled when action.enabled=False (explicit over implicit:
        disabling requires a deliberate YAML config decision, never an absent dependency).
        Raises ConfigError when action.enabled=True but reader is not injected — this is a
        composition-root wiring error (server.py forgot to inject ContextLoadedCache).

        Checks action.exempt_tools next — if context.tool_name is listed, the check
        is skipped entirely (no reader access required). This allows get_work_context
        itself to be exempted via YAML config without any tool names in Python code.

        Bootstrap predicate: if state.json does not exist, the phase engine has not
        been initialised yet. The gate is semantically inactive in that state so that
        initialize_project (and any other bootstrapping tool) is never blocked.

        Raises ConfigError when reader is not configured (wiring error).
        Raises ValidationError when context has not been loaded for the current branch.
        """
        if not action.enabled:
            return  # gate explicitly disabled via YAML config

        if context.tool_name in action.exempt_tools:
            return

        branch = str(
            context.get_param("current_branch") or _get_current_git_branch(workspace_root) or ""
        )

        # Bootstrap predicate + mismatch bypass via IStateReader.
        # FileNotFoundError means no active workflow — gate is inactive.
        try:
            loaded_state = self._state_reader.load(branch)
            branch_issue = self._git_config.extract_issue_number(branch)
            if loaded_state.issue_number != branch_issue:
                return
        except FileNotFoundError:
            return  # Bootstrap: no state.json means gate is inactive
        except Exception:
            pass

        if self._context_loaded_reader is None:
            raise ConfigError(
                "check_context_loaded action requires context_loaded_reader; "
                "wire ContextLoadedCache in EnforcementRunner.__init__",
                file_path=_ENFORCEMENT_DISPLAY_PATH,
            )

        if not self._context_loaded_reader.is_context_loaded(branch):
            note_context.produce(
                Note(
                    key="load_context_suggestion",
                    params={},
                )
            )
            raise ValidationError(
                f"get_work_context has not been called for branch '{branch}'. "
                "Call get_work_context before using this tool.",
                error_code="context_not_loaded",
                params={"branch": branch},
            )
