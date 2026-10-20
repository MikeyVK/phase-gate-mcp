"""Tests for MCP Server tool registration and dispatch hooks.

@layer: Tests (Unit)
@dependencies: pytest, mcp_server.server, mcp.types
"""

import json
import logging
import os
import shutil
import subprocess
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, cast
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mcp.types import CallToolRequest, CallToolRequestParams, TextContent
from pydantic import BaseModel, ConfigDict

from mcp_server.bootstrap import ServerBootstrapper
from mcp_server.config import settings as settings_module
from mcp_server.config.settings import ServerSettings
from mcp_server.core.exceptions import ConfigError
from mcp_server.core.interfaces import ICoreTool, PRStatus
from mcp_server.core.interfaces.ipresenter import IPresenter
from mcp_server.core.interfaces.itool import ITool
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_execution import ToolExecution
from mcp_server.core.tool_factory import ToolFactory
from mcp_server.managers.state_repository import InMemoryStateRepository
from mcp_server.presenters import SchemaResourcePresenter
from mcp_server.presenters.startup_recovery_presenter import StartupRecoveryPresenter
from mcp_server.schemas.cache_publication import CachePublication
from mcp_server.schemas.presentation_output import (
    InlineOperation,
    PresentedOutput,
    PublicToolResponse,
)
from mcp_server.schemas.startup_diagnostic import StartupDiagnostic
from mcp_server.schemas.tool_outputs import HealthCheckOutput, PhaseTransitionOutput
from mcp_server.server import DegradedMCPServer, MCPServer
from mcp_server.state.response_cache import ResponseCacheManager
from mcp_server.tools.git_tools import CreateBranchTool
from mcp_server.tools.phase_tools import (
    ForcePhaseTransitionTool,
    TransitionPhaseTool,
)
from mcp_server.tools.pr_tools import SubmitPRTool
from mcp_server.tools.tool_result import ToolResult
from tests.mcp_server.test_support import (
    RealSettings,
    connected_mcp_client,
    get_default_server_root,
    make_dispatch_dependencies,
    make_dispatch_server,
    make_phase_state_engine,
    make_project_manager,
    make_response_presenter,
)

TRANSITION_ADVISORY_NOTE = (
    "🚀 REQUIRED NEXT STEP: Call get_work_context now before any other tool call "
    "to load the current phase context for this branch."
)


pytestmark = pytest.mark.usefixtures("git_workspace")


class EmptyInput(BaseModel):
    """Admit empty tool arguments through the real validation pipeline."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")


class CallLoggingInput(BaseModel):
    """Preserve the logged argument payload while admitting a concrete model."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    a: int


def _bootstrap_workspace_configs(workspace_root: Path) -> None:
    repo_root = Path(__file__).resolve().parents[3]
    source_root = repo_root / get_default_server_root()
    target_root = workspace_root / get_default_server_root()
    target_root.mkdir(parents=True, exist_ok=True)
    for directory_name in ("config", "template_suite"):
        shutil.copytree(
            source_root / directory_name,
            target_root / directory_name,
            dirs_exist_ok=True,
        )
    source_file = source_root / "deliverables.json"
    if source_file.exists():
        shutil.copy2(source_file, target_root / "deliverables.json")
    _write_phase_state(workspace_root, "research")


def _patch_server_settings(
    mock: MagicMock,
    workspace_root: str | None = None,
) -> None:
    """Configure a Settings class mock for server tests."""
    resolved_workspace_root = workspace_root or str(Path(__file__).resolve().parents[3])
    server_root_dir = get_default_server_root()

    settings = RealSettings.from_env()
    settings.server.name = "test-server"
    settings.server.workspace_root = resolved_workspace_root
    settings.server.config_root = None
    settings.server.template_root = str(
        Path(__file__).resolve().parents[3] / ".pgmcp" / "template_suite"
    )
    settings.server.server_root_dir = server_root_dir
    settings.logging.level = "INFO"
    settings.logging.audit_log = None

    mock.return_value = settings
    mock.from_env.return_value = settings


def _write_phase_state(workspace_root: Path, current_phase: str) -> None:
    state_file = workspace_root / get_default_server_root() / "state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(
        json.dumps(
            {
                "schema_version": "2.0.0",
                "branch": "refactor/283-ready-phase-enforcement",
                "parent_branch": "main",
                "workflow_name": "refactor",
                "current_phase": current_phase,
                "issue_number": 283,
            }
        ),
        encoding="utf-8",
    )


def _git_test_env() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("GIT_TERMINAL_PROMPT", "0")
    env.setdefault("GIT_PAGER", "cat")
    env.setdefault("PAGER", "cat")
    return env


def _run_git(workspace_root: Path, *args: str) -> None:
    subprocess.run(
        ["git", *args],
        cwd=workspace_root,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        check=True,
        timeout=5,
        env=_git_test_env(),
    )


def _make_submit_pr_request() -> CallToolRequest:
    return CallToolRequest(
        params=CallToolRequestParams(
            name="submit_pr",
            arguments={
                "title": "Test PR",
                "body": "Test body",
            },
        )
    )


def _text_content(item: object) -> str:
    """Assert the SDK text block expected by these dispatch tests."""
    assert isinstance(item, TextContent)
    return item.text


def _make_transition_advisory_execute(
    _text: str,
) -> Callable[[object, object, NoteContext], Awaitable[PhaseTransitionOutput]]:
    async def execute(
        _self: object, _params: object, context: NoteContext
    ) -> PhaseTransitionOutput:
        del context
        # No legacy InfoNote produced
        return PhaseTransitionOutput(
            success=True,
            branch=getattr(_params, "branch", "feature/257-reorder-workflow-phases"),
            from_phase="research",
            to_phase=getattr(_params, "to_phase", "planning"),
            passing_gates=[],
            skipped_gates=[],
            passing_gates_count=0,
            skipped_gates_count=0,
        )

    return execute


class TestServerToolRegistration:
    """Tests for server tool registration."""

    def test_github_tools_always_registered(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """GitHub tools should always be registered, even without token."""
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
            _patch_server_settings(mock_settings_cls, workspace_root=str(tmp_path))
            settings = mock_settings_cls.from_env.return_value
            settings.server.config_root = str(
                Path(__file__).resolve().parents[3] / ".pgmcp" / "config"
            )

            server = ServerBootstrapper(settings).bootstrap_target()
            tool_names = [t.name for t in server.tools]

            assert "create_issue" in tool_names
            assert "list_issues" in tool_names
            assert "get_issue" in tool_names
            assert "close_issue" in tool_names
            assert "get_pr" not in tool_names

    def test_github_tools_registered_with_token(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """GitHub tools should be registered when token is configured."""
        monkeypatch.setenv("GITHUB_TOKEN", "test-token")
        with (
            patch("mcp_server.config.settings.Settings") as mock_settings_cls,
            patch("mcp_server.resources.github.GitHubManager") as mock_res_manager,
            patch("mcp_server.tools.pr_tools.GitHubManager") as mock_pr_manager,
            patch("mcp_server.tools.label_tools.GitHubManager") as mock_label_manager,
        ):
            _patch_server_settings(mock_settings_cls, workspace_root=str(tmp_path))
            settings = mock_settings_cls.from_env.return_value
            settings.server.config_root = str(
                Path(__file__).resolve().parents[3] / ".pgmcp" / "config"
            )

            mock_res_manager.return_value = MagicMock()
            mock_pr_manager.return_value = MagicMock()
            mock_label_manager.return_value = MagicMock()

            server = ServerBootstrapper(settings).bootstrap_target()
            tool_names = [t.name for t in server.tools]

            assert "create_issue" in tool_names
            assert "list_issues" in tool_names
            assert "get_issue" in tool_names
            assert "close_issue" in tool_names
            assert "add_labels" in tool_names
            assert "get_pr" in tool_names

    @pytest.mark.asyncio
    async def test_call_tool_logging_has_call_id_and_duration(
        self,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """call_tool handler should log correlation id and duration."""

        class DummyTool(ICoreTool[CallLoggingInput, ToolResult]):
            """Dummy tool for testing server call_tool logging."""

            @property
            def name(self) -> str:
                return "dummy_tool"

            @property
            def description(self) -> str:
                return "Dummy tool"

            @property
            def args_model(self) -> type[CallLoggingInput]:
                return CallLoggingInput

            async def execute(self, params: CallLoggingInput, context: NoteContext) -> ToolResult:
                del params, context
                return ToolResult.text("ok")

        with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
            _patch_server_settings(mock_settings_cls)
            managers = make_dispatch_dependencies(mock_settings_cls.from_env.return_value)
            workspace_root = Path(mock_settings_cls.from_env.return_value.server.workspace_root)

            server = make_dispatch_server(mock_settings_cls.from_env.return_value)
            factory = ToolFactory(managers.enforcement_runner, workspace_root)
            server.tools = [factory.create_tool(DummyTool())]

            caplog.set_level(logging.DEBUG, logger="mcp_server.server")

            req = CallToolRequest(
                params=CallToolRequestParams(
                    name="dummy_tool",
                    arguments={"a": 1},
                )
            )
            async with connected_mcp_client(server) as client:
                await client.call_tool(req.params.name, req.params.arguments)

        start_logs = [
            r
            for r in caplog.records
            if r.name == "mcp_server.server" and r.getMessage() == "Tool call received"
        ]
        assert start_logs
        start_props = cast(dict[str, Any], getattr(start_logs[0], "props", {}))
        assert start_props["tool_name"] == "dummy_tool"
        assert "call_id" in start_props

        done_logs = [
            r
            for r in caplog.records
            if r.name == "mcp_server.server" and r.getMessage() == "Tool call completed"
        ]
        assert done_logs
        done_props = cast(dict[str, Any], getattr(done_logs[0], "props", {}))
        assert done_props["tool_name"] == "dummy_tool"
        assert done_props["call_id"] == start_props["call_id"]
        assert "duration_ms" in done_props

    @pytest.mark.asyncio
    async def test_call_tool_pre_enforcement_blocks_invalid_create_branch_base(
        self,
        tmp_path: Path,
    ) -> None:
        """Dispatch pre-hook should block invalid branch creation before tool execution."""
        config_dir = tmp_path / get_default_server_root() / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        (config_dir / "enforcement.yaml").write_text(
            """
            version: "1.0.0"
            enforcement:
              - event_source: tool
                tool: create_branch
                timing: pre
                actions:
                  - type: check_branch_policy
                    rules:
                      feature: [main, \"epic/*\"]
            """,
            encoding="utf-8",
        )

        _bootstrap_workspace_configs(tmp_path)

        with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
            _patch_server_settings(mock_settings_cls, workspace_root=str(tmp_path))
            managers = make_dispatch_dependencies(mock_settings_cls.from_env.return_value)
            workspace_root = Path(mock_settings_cls.from_env.return_value.server.workspace_root)

            server = make_dispatch_server(mock_settings_cls.from_env.return_value)
            manager = MagicMock()
            manager.git_config = managers.git_manager.git_config
            factory = ToolFactory(managers.enforcement_runner, workspace_root)
            server.tools = [factory.create_tool(CreateBranchTool(manager=manager))]

            req = CallToolRequest(
                params=CallToolRequestParams(
                    name="create_branch",
                    arguments={
                        "issue_number": 123,
                        "name": "new-thing",
                        "branch_type": "feature",
                        "base_branch": "release/1.0",
                    },
                )
            )
            async with connected_mcp_client(server) as client:
                response = await client.call_tool(req.params.name, req.params.arguments)

        assert "cannot be created from base" in _text_content(response.content[0])
        manager.create_branch.assert_not_called()

    @pytest.mark.asyncio
    async def test_call_tool_pre_enforcement_blocks_submit_pr_outside_ready_phase(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Dispatch pre-hook should return a phase error and never reach GitHub PR creation."""
        monkeypatch.setattr(
            "mcp_server.managers.github_manager.GitHubManager.get_pr_status",
            MagicMock(return_value=PRStatus.ABSENT),
        )
        monkeypatch.delenv("PGMCP_SERVER_PROJECT_DIR", raising=False)
        _bootstrap_workspace_configs(tmp_path)
        _write_phase_state(tmp_path, "documentation")

        with (
            patch("mcp_server.config.settings.Settings") as mock_settings_cls,
            patch(
                "mcp_server.managers.enforcement_runner._get_current_git_branch",
                return_value="refactor/283-ready-phase-enforcement",
            ),
        ):
            _patch_server_settings(
                mock_settings_cls,
                workspace_root=str(tmp_path),
            )

            managers = make_dispatch_dependencies(mock_settings_cls.from_env.return_value)
            workspace_root = Path(mock_settings_cls.from_env.return_value.server.workspace_root)
            server = make_dispatch_server(mock_settings_cls.from_env.return_value)
            server.tools = [
                ToolFactory(managers.enforcement_runner, workspace_root).create_tool(
                    SubmitPRTool(
                        git_manager=managers.git_manager,
                        github_manager=managers.github_manager,
                        pr_status_writer=managers.pr_status_cache,
                        merge_readiness_context=MagicMock(),
                        state_reader=MagicMock(),
                        git_config=managers.git_manager.git_config,
                    )
                )
            ]

            with patch(
                "mcp_server.managers.github_manager.GitHubManager.create_pr",
                side_effect=AssertionError("create_pr should not be called"),
            ) as mock_create_pr:
                async with connected_mcp_client(server) as client:
                    response = await client.call_tool(
                        _make_submit_pr_request().params.name,
                        _make_submit_pr_request().params.arguments,
                    )

        text = "\n".join(c.text for c in response.content if isinstance(c, TextContent))
        assert response.is_error is True
        assert "requires phase 'ready'" in text
        assert "Current phase: 'documentation'" in text
        assert "Request a transition to the ready phase." in text
        mock_create_pr.assert_not_called()

    @pytest.mark.asyncio
    async def test_call_tool_post_enforcement_runs_after_transition(
        self,
        tmp_path: Path,
    ) -> None:
        """Dispatch post-hook should still run after a successful phase transition."""
        _bootstrap_workspace_configs(tmp_path)

        project_manager = make_project_manager(tmp_path)
        project_manager.initialize_project(
            issue_number=257,
            issue_title="Cycle 5 enforcement",
            workflow_name="feature",
            parent_branch="main",
        )
        state_engine = make_phase_state_engine(
            tmp_path,
            project_manager=project_manager,
            state_repository=InMemoryStateRepository(),
        )
        state_engine.initialize_branch(
            branch="feature/257-reorder-workflow-phases",
            issue_number=257,
            initial_phase="research",
            parent_branch="main",
        )

        research_doc = tmp_path / "docs" / "development" / "issue257" / "cycle5-research.md"
        research_doc.parent.mkdir(parents=True, exist_ok=True)
        research_doc.write_text("# Research\n", encoding="utf-8")

        with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
            _patch_server_settings(mock_settings_cls, workspace_root=str(tmp_path))
            managers = make_dispatch_dependencies(mock_settings_cls.from_env.return_value)
            workspace_root = Path(mock_settings_cls.from_env.return_value.server.workspace_root)

            server = make_dispatch_server(mock_settings_cls.from_env.return_value)
            factory = ToolFactory(managers.enforcement_runner, workspace_root)
            server.tools = [
                factory.create_tool(
                    TransitionPhaseTool(
                        workspace_root=tmp_path,
                        project_manager=project_manager,
                        state_engine=state_engine,
                        server_root=tmp_path / get_default_server_root(),
                        workphases_config=None,
                    )
                )
            ]

            with (
                patch.object(managers.enforcement_runner, "run", return_value=[]) as mock_run,
                patch.object(
                    TransitionPhaseTool,
                    "execute",
                    new=_make_transition_advisory_execute("Successfully transitioned"),
                ),
            ):
                req = CallToolRequest(
                    params=CallToolRequestParams(
                        name="transition_phase",
                        arguments={
                            "branch": "feature/257-reorder-workflow-phases",
                            "to_phase": "planning",
                            "human_approval_message": "Move into planning",
                        },
                    )
                )
                async with connected_mcp_client(server) as client:
                    response = await client.call_tool(req.params.name, req.params.arguments)

        assert "Transitioned 'research' → 'planning'" in _text_content(response.content[0])
        assert len(response.content) == 1
        assert TRANSITION_ADVISORY_NOTE in _text_content(response.content[0])
        assert any(
            call.kwargs.get("event") == "transition_phase" and call.kwargs.get("timing") == "post"
            for call in mock_run.call_args_list
        )

    @pytest.mark.asyncio
    async def test_call_tool_post_enforcement_runs_after_force_phase_transition(
        self,
        tmp_path: Path,
    ) -> None:
        """Successful forced phase transitions append the advisory note after post-hook success."""
        _bootstrap_workspace_configs(tmp_path)

        with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
            _patch_server_settings(mock_settings_cls, workspace_root=str(tmp_path))
            managers = make_dispatch_dependencies(mock_settings_cls.from_env.return_value)
            workspace_root = Path(mock_settings_cls.from_env.return_value.server.workspace_root)

            server = make_dispatch_server(mock_settings_cls.from_env.return_value)
            factory = ToolFactory(managers.enforcement_runner, workspace_root)
            server.tools = [
                factory.create_tool(
                    ForcePhaseTransitionTool(
                        workspace_root=tmp_path,
                        project_manager=managers.project_manager,
                        state_engine=managers.phase_state_engine,
                        server_root=tmp_path / get_default_server_root(),
                        workphases_config=None,
                    )
                )
            ]

            with (
                patch.object(managers.enforcement_runner, "run", return_value=[]) as mock_run,
                patch.object(
                    ForcePhaseTransitionTool,
                    "execute",
                    new=_make_transition_advisory_execute("✅ Forced phase transition"),
                ),
            ):
                req = CallToolRequest(
                    params=CallToolRequestParams(
                        name="force_phase_transition",
                        arguments={
                            "branch": "feature/257-reorder-workflow-phases",
                            "to_phase": "planning",
                            "skip_reason": "Force test",
                            "human_approval_message": "Approved",
                        },
                    )
                )
                async with connected_mcp_client(server) as client:
                    response = await client.call_tool(req.params.name, req.params.arguments)

        assert "Force-transitioned 'research' → 'planning'" in _text_content(response.content[0])
        assert len(response.content) == 1
        assert TRANSITION_ADVISORY_NOTE in _text_content(response.content[0])
        assert any(
            call.kwargs.get("event") == "transition_phase" and call.kwargs.get("timing") == "post"
            for call in mock_run.call_args_list
        )

    @pytest.mark.asyncio
    async def test_call_tool_transition_post_enforcement_error_omits_advisory_note(
        self,
        tmp_path: Path,
    ) -> None:
        """Post-hook errors must not leak the success-path advisory note."""
        _bootstrap_workspace_configs(tmp_path)

        project_manager = make_project_manager(tmp_path)
        project_manager.initialize_project(
            issue_number=257,
            issue_title="Cycle 5 enforcement",
            workflow_name="feature",
            parent_branch="main",
        )
        state_engine = make_phase_state_engine(
            tmp_path,
            project_manager=project_manager,
            state_repository=InMemoryStateRepository(),
        )
        branch = "feature/257-reorder-workflow-phases"
        state_engine.initialize_branch(
            branch=branch,
            issue_number=257,
            initial_phase="research",
            parent_branch="main",
        )

        with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
            _patch_server_settings(mock_settings_cls, workspace_root=str(tmp_path))
            managers = make_dispatch_dependencies(mock_settings_cls.from_env.return_value)
            workspace_root = Path(mock_settings_cls.from_env.return_value.server.workspace_root)

            server = make_dispatch_server(mock_settings_cls.from_env.return_value)
            factory = ToolFactory(managers.enforcement_runner, workspace_root)
            server.tools = [
                factory.create_tool(
                    TransitionPhaseTool(
                        workspace_root=tmp_path,
                        project_manager=project_manager,
                        state_engine=state_engine,
                        server_root=tmp_path / get_default_server_root(),
                        workphases_config=None,
                    )
                )
            ]

            with patch.object(managers.enforcement_runner, "run") as mock_run:

                def side_effect(*_args: object, **kwargs: object) -> list[str]:
                    if kwargs.get("event") == "transition_phase" and kwargs.get("timing") == "post":
                        raise ConfigError("post hook failed")
                    return []

                mock_run.side_effect = side_effect
                req = CallToolRequest(
                    params=CallToolRequestParams(
                        name="transition_phase",
                        arguments={
                            "branch": branch,
                            "to_phase": "design",
                            "human_approval_message": "Move into design",
                        },
                    )
                )
                async with connected_mcp_client(server) as client:
                    response = await client.call_tool(req.params.name, req.params.arguments)

        texts = [_text_content(item) for item in response.content]
        assert len(response.content) == 1
        assert "post hook failed" in texts[0]
        assert all(TRANSITION_ADVISORY_NOTE not in text for text in texts)

    @pytest.mark.asyncio
    async def test_call_tool_force_phase_post_enforcement_returns_error(
        self,
        tmp_path: Path,
    ) -> None:
        """Force phase transitions should fail when post-enforcement raises."""
        _bootstrap_workspace_configs(tmp_path)

        with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
            _patch_server_settings(mock_settings_cls, workspace_root=str(tmp_path))
            managers = make_dispatch_dependencies(mock_settings_cls.from_env.return_value)
            workspace_root = Path(mock_settings_cls.from_env.return_value.server.workspace_root)

            server = make_dispatch_server(mock_settings_cls.from_env.return_value)
            factory = ToolFactory(managers.enforcement_runner, workspace_root)
            server.tools = [
                factory.create_tool(
                    ForcePhaseTransitionTool(
                        workspace_root=tmp_path,
                        project_manager=managers.project_manager,
                        state_engine=managers.phase_state_engine,
                        server_root=tmp_path / get_default_server_root(),
                        workphases_config=None,
                    )
                )
            ]

            with (
                patch.object(managers.enforcement_runner, "run") as mock_run,
                patch.object(
                    ForcePhaseTransitionTool,
                    "execute",
                    new=_make_transition_advisory_execute("✅ Forced phase transition"),
                ),
            ):

                def side_effect(*_args: object, **kwargs: object) -> list[str]:
                    if kwargs.get("event") == "transition_phase" and kwargs.get("timing") == "post":
                        raise ConfigError("post hook failed")
                    return []

                mock_run.side_effect = side_effect
                req = CallToolRequest(
                    params=CallToolRequestParams(
                        name="force_phase_transition",
                        arguments={
                            "branch": "feature/257-reorder-workflow-phases",
                            "to_phase": "planning",
                            "skip_reason": "Force test",
                            "human_approval_message": "Approved",
                        },
                    )
                )
                async with connected_mcp_client(server) as client:
                    response = await client.call_tool(req.params.name, req.params.arguments)

        text = _text_content(response.content[0])
        assert len(response.content) == 1
        assert "post hook failed" in text
        assert "⚠️" not in text
        assert "✅" not in text
        assert TRANSITION_ADVISORY_NOTE not in text

    @pytest.mark.asyncio
    async def test_run_uses_injected_settings_without_extra_from_env(self) -> None:
        """run() should reuse the injected settings object from the composition root."""

        @asynccontextmanager
        async def fake_stdio_server(
            *_args: object, **_kwargs: object
        ) -> AsyncGenerator[tuple[MagicMock, MagicMock]]:
            yield MagicMock(), MagicMock()

        with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
            _patch_server_settings(mock_settings_cls)
            injected_settings = mock_settings_cls.from_env.return_value
            server = make_dispatch_server(injected_settings)
            mock_settings_cls.from_env.reset_mock()

            with (
                patch("mcp_server.server.stdio_server", side_effect=fake_stdio_server),
                patch.object(server.server, "run", new=AsyncMock()) as mock_run,
            ):
                await server.run()

        mock_settings_cls.from_env.assert_not_called()
        mock_run.assert_awaited_once()


@pytest.mark.asyncio
async def test_handle_call_tool_cache_error_intercept() -> None:
    """Retain complete inline operation data when cache publication fails."""

    class DummyTool(ICoreTool[EmptyInput, ToolResult]):
        @property
        def name(self) -> str:
            return "dummy_tool"

        @property
        def description(self) -> str:
            return "Dummy Tool"

        @property
        def args_model(self) -> type[EmptyInput]:
            return EmptyInput

        async def execute(self, params: EmptyInput, context: NoteContext) -> ToolResult:
            del params, context
            return ToolResult.text("success")

    with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
        _patch_server_settings(mock_settings_cls)

        presenter = make_response_presenter()

        managers = make_dispatch_dependencies(mock_settings_cls.from_env.return_value)
        workspace_root = Path(mock_settings_cls.from_env.return_value.server.workspace_root)
        tool = DummyTool()
        cache_manager = ResponseCacheManager()
        server = MCPServer(
            settings=mock_settings_cls.from_env.return_value,
            tools=[],
            resources=[],
            presenter=presenter,
            publisher=cache_manager,
        )
        factory = ToolFactory(managers.enforcement_runner, workspace_root)
        server.tools = [factory.create_tool(tool)]

        with patch.object(
            cache_manager,
            "put",
            return_value=CachePublication(success=False, error_code="write_failed"),
        ) as mock_put:
            req = CallToolRequest(
                params=CallToolRequestParams(
                    name="dummy_tool",
                    arguments={},
                )
            )

            with patch.object(presenter, "present", wraps=presenter.present) as mock_present:
                async with connected_mcp_client(server) as client:
                    response = await client.call_tool(req.params.name, req.params.arguments)

        content = response.content
        assert len(content) == 1
        text = getattr(content[0], "text", "")
        assert response.is_error is False
        assert response.structured_content is not None
        envelope = PublicToolResponse.model_validate_json(json.dumps(response.structured_content))
        assert envelope.success
        assert isinstance(envelope.data, InlineOperation)
        assert "success" in json.dumps(envelope.data.operation)
        # Since cache_pub.run_id is None, there should be NO cache URI in output
        assert "pgmcp://cache/runs/" not in text

        # Verify presenter was called with cache_pub
        mock_present.assert_called_once()
        _, kwargs = mock_present.call_args
        assert kwargs.get("cache_pub") is not None
        assert kwargs.get("cache_pub").success is False
        mock_put.assert_called_once()


def test_server_constructor_clean() -> None:
    """Verify that MCPServer can be constructed without configs or managers."""

    with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
        _patch_server_settings(mock_settings_cls)
        settings = mock_settings_cls.from_env.return_value
        presenter = MagicMock(spec=IPresenter)
        server = MCPServer(
            settings=settings,
            tools=[],
            resources=[],
            presenter=presenter,
            publisher=None,
        )
        assert server.presenter is presenter


@pytest.mark.asyncio
async def test_degraded_health_tool_uses_normalized_pipeline(tmp_path: Path) -> None:
    """The config-error fallback remains callable through the outer tool contract."""
    server = DegradedMCPServer(
        settings_module.Settings(server=ServerSettings(workspace_root=str(tmp_path))),
        StartupDiagnostic(
            exception_type="mcp_server.core.exceptions.ConfigError",
            message="Invalid configuration",
            code="ERR_CONFIG",
            params=FrozenJsonObject(()),
        ),
        StartupRecoveryPresenter(SchemaResourcePresenter()),
    )
    assert [tool.name for tool in server.tools] == ["health_check", "restart_server"]
    execution = await server.tools[0].execute({}, NoteContext())
    assert isinstance(execution.operation, HealthCheckOutput)
    assert execution.attachments == ()
    assert "Invalid configuration" in str(execution.operation)

    async with connected_mcp_client(server) as client:
        catalog = await client.list_tools()
        response = await client.call_tool("health_check", {})

    assert response.structured_content is not None
    envelope = PublicToolResponse.model_validate_json(json.dumps(response.structured_content))
    assert isinstance(envelope.data, InlineOperation)
    assert execution.operation.startup_diagnostic is not None
    assert envelope.data.operation["startup_diagnostic"] == (
        execution.operation.startup_diagnostic.model_dump(mode="json")
    )
    assert envelope.data.operation["status"] == "unhealthy"
    assert envelope.success is execution.operation.success
    assert response.is_error is not execution.operation.success
    assert envelope.delivery_error is None
    assert envelope.attachments == ()
    assert len(response.content) == 1
    text = response.content[0]
    assert isinstance(text, TextContent)
    assert envelope.presentation == text.text
    assert execution.operation.startup_diagnostic.message in text.text
    assert catalog.tools[0].output_schema == PublicToolResponse.model_json_schema()


@pytest.mark.asyncio
@pytest.mark.parametrize("operation_success", [True, False])
async def test_server_transfers_selected_structured_projection(
    tmp_path: Path, operation_success: bool
) -> None:
    """Forward the presenter schema and projection without requiring tool output metadata."""

    class Operation(BaseModel):
        success: bool
        marker: str

    operation = Operation(success=operation_success, marker="structured operation marker")
    envelope = PublicToolResponse(
        success=operation_success,
        presentation="complete structured guidance",
        data=InlineOperation(delivery="inline", operation=operation.model_dump(mode="json")),
        attachments=(),
        delivery_error=None,
    )
    projected = PresentedOutput(text=None, structured_content=envelope.model_dump(mode="json"))
    presenter = MagicMock(spec=IPresenter)
    presenter.present.return_value = projected
    presenter.output_schema.return_value = PublicToolResponse.model_json_schema()
    tool = MagicMock(spec=ITool)
    tool.name = "structured_operation"
    tool.description = "Return a supplied operation"
    tool.input_schema = {"type": "object", "properties": {}}
    tool.execute = AsyncMock(return_value=ToolExecution(operation=operation, attachments=()))
    server = MCPServer(
        settings=settings_module.Settings(server=ServerSettings(workspace_root=str(tmp_path))),
        tools=[tool],
        resources=[],
        presenter=presenter,
    )

    async with connected_mcp_client(server) as client:
        catalog = await client.list_tools()
        response = await client.call_tool(tool.name, {})

    assert catalog.tools[0].output_schema == presenter.output_schema.return_value
    assert response.content == []
    assert response.structured_content == projected.structured_content
    assert response.is_error is not operation_success
    presenter.present.assert_called_once()
    assert presenter.present.call_args.kwargs["data"] is operation
