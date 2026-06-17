# pyright: reportMissingImports=false
"""Tests for MCP Server tool registration and dispatch hooks.

@layer: Tests (Unit)
@dependencies: pytest, mcp_server.server, mcp.types
"""

import json
import logging
import os
import shutil
import subprocess
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, cast
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mcp.types import CallToolRequest, CallToolRequestParams

from mcp_server.core.exceptions import ConfigError
from mcp_server.core.operation_notes import InfoNote, NoteContext
from mcp_server.managers.state_repository import InMemoryStateRepository
from mcp_server.schemas.tool_outputs import PhaseTransitionOutput
from mcp_server.tools.base import ITool
from mcp_server.tools.git_tools import CreateBranchTool
from mcp_server.tools.phase_tools import (
    TRANSITION_ADVISORY_NOTE,
    ForcePhaseTransitionTool,
    TransitionPhaseTool,
)
from mcp_server.tools.tool_result import ToolResult
from tests.mcp_server.test_support import (
    make_phase_state_engine,
    make_project_manager,
    make_test_server,
)


def _bootstrap_workspace_configs(workspace_root: Path) -> None:
    repo_root = Path(__file__).resolve().parents[3]
    shutil.copytree(repo_root / ".phase-gate", workspace_root / ".phase-gate", dirs_exist_ok=True)


def _patch_server_settings(
    mock: MagicMock,
    workspace_root: str | None = None,
    token: str | None = None,
) -> None:
    """Configure a Settings class mock for server tests."""
    resolved_workspace_root = workspace_root or str(Path(__file__).resolve().parents[3])
    resolved_config_root = str(Path(resolved_workspace_root) / ".phase-gate")
    mock.from_env.return_value.server.name = "test-server"
    mock.from_env.return_value.server.workspace_root = resolved_workspace_root
    mock.from_env.return_value.server.config_root = resolved_config_root
    mock.from_env.return_value.server.server_root_dir = ".phase-gate"
    mock.from_env.return_value.github.token = token
    mock.from_env.return_value.github.owner = "test"
    mock.from_env.return_value.github.repo = "repo"
    mock.from_env.return_value.logging.level = "INFO"
    mock.from_env.return_value.logging.audit_log = ".logs/mcp_audit.log"


def _write_phase_state(workspace_root: Path, current_phase: str) -> None:
    state_file = workspace_root / ".phase-gate" / "state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(
        json.dumps(
            {
                "branch": "refactor/283-ready-phase-enforcement",
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


def _track_branch_local_artifacts(workspace_root: Path) -> None:
    deliverables_file = workspace_root / ".phase-gate" / "deliverables.json"
    if not deliverables_file.exists():
        deliverables_file.write_text("{}\n", encoding="utf-8")

    _run_git(workspace_root, "init")
    _run_git(workspace_root, "add", ".phase-gate/state.json", ".phase-gate/deliverables.json")


def _make_submit_pr_request() -> CallToolRequest:
    return CallToolRequest(
        params=CallToolRequestParams(
            name="submit_pr",
            arguments={
                "title": "Test PR",
                "body": "Test body",
                "head": "refactor/283-ready-phase-enforcement",
                "base": "main",
            },
        )
    )


def _make_transition_advisory_execute(
    _text: str,
) -> Callable[[object, object, NoteContext], Awaitable[PhaseTransitionOutput]]:
    async def execute(
        _self: object, _params: object, context: NoteContext
    ) -> PhaseTransitionOutput:
        context.produce(InfoNote(message=TRANSITION_ADVISORY_NOTE))
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

    def test_github_tools_always_registered(self) -> None:
        """GitHub tools should always be registered, even without token."""
        with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
            _patch_server_settings(mock_settings_cls)

            server = make_test_server()
            tool_names = [t.name for t in server.tools]

            assert "create_issue" in tool_names
            assert "list_issues" in tool_names
            assert "get_issue" in tool_names
            assert "close_issue" in tool_names
            assert "get_pr" not in tool_names

    def test_github_tools_registered_with_token(self) -> None:
        """GitHub tools should be registered when token is configured."""
        with (
            patch("mcp_server.config.settings.Settings") as mock_settings_cls,
            patch("mcp_server.resources.github.GitHubManager") as mock_res_manager,
            patch("mcp_server.tools.pr_tools.GitHubManager") as mock_pr_manager,
            patch("mcp_server.tools.label_tools.GitHubManager") as mock_label_manager,
        ):
            _patch_server_settings(mock_settings_cls, token="test-token")

            mock_res_manager.return_value = MagicMock()
            mock_pr_manager.return_value = MagicMock()
            mock_label_manager.return_value = MagicMock()

            server = make_test_server()
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

        class DummyTool(ITool):
            """Dummy tool for testing server call_tool logging."""

            @property
            def name(self) -> str:
                return "dummy_tool"

            @property
            def description(self) -> str:
                return "Dummy tool"

            @property
            def args_model(self) -> None:
                return None

            @property
            def input_schema(self) -> dict[str, Any]:
                return {"type": "object", "properties": {}}

            async def execute(self, params: Any, context: NoteContext) -> ToolResult:  # noqa: ANN401
                del params, context
                return ToolResult.text("ok")

        with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
            _patch_server_settings(mock_settings_cls)

            server = make_test_server()
            server.tools = [DummyTool()]

            handler = server.server.request_handlers[CallToolRequest]
            caplog.set_level(logging.DEBUG, logger="mcp_server.server")

            req = CallToolRequest(
                params=CallToolRequestParams(
                    name="dummy_tool",
                    arguments={"a": 1},
                )
            )
            await handler(req)

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
        config_dir = tmp_path / ".phase-gate" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        (config_dir / "enforcement.yaml").write_text(
            """
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

            server = make_test_server()
            manager = MagicMock()
            manager.git_config = server.git_manager.git_config
            server.tools = [CreateBranchTool(manager=manager)]
            handler = server.server.request_handlers[CallToolRequest]

            req = CallToolRequest(
                params=CallToolRequestParams(
                    name="create_branch",
                    arguments={
                        "name": "new-thing",
                        "branch_type": "feature",
                        "base_branch": "release/1.0",
                    },
                )
            )
            response = await handler(req)

        assert "cannot be created from base" in response.root.content[0].text
        manager.create_branch.assert_not_called()

    @pytest.mark.asyncio
    async def test_call_tool_pre_enforcement_blocks_submit_pr_outside_ready_phase(
        self,
        tmp_path: Path,
    ) -> None:
        """Dispatch pre-hook should return a phase error and never reach GitHub PR creation."""
        _bootstrap_workspace_configs(tmp_path)
        _write_phase_state(tmp_path, "documentation")

        with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
            _patch_server_settings(
                mock_settings_cls,
                workspace_root=str(tmp_path),
                token="test-token",
            )

            server = make_test_server()
            handler = server.server.request_handlers[CallToolRequest]

            with patch.object(
                server.github_manager,
                "create_pr",
                side_effect=AssertionError("create_pr should not be called"),
            ) as mock_create_pr:
                response = await handler(_make_submit_pr_request())

        text = "\n".join(c.text for c in response.root.content if hasattr(c, "text"))
        assert response.root.isError is True
        assert "requires phase 'ready'" in text
        assert "Current phase: 'documentation'" in text
        assert 'transition_phase(to_phase="ready")' in text
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
        )

        research_doc = tmp_path / "docs" / "development" / "issue257" / "cycle5-research.md"
        research_doc.parent.mkdir(parents=True, exist_ok=True)
        research_doc.write_text("# Research\n", encoding="utf-8")

        with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
            _patch_server_settings(mock_settings_cls, workspace_root=str(tmp_path))

            server = make_test_server()
            server.tools = [
                TransitionPhaseTool(
                    workspace_root=tmp_path,
                    project_manager=project_manager,
                    state_engine=state_engine,
                    server_root=tmp_path / ".phase-gate",
                    workphases_config=None,
                )
            ]
            handler = server.server.request_handlers[CallToolRequest]

            with (
                patch.object(server.enforcement_runner, "run", return_value=[]) as mock_run,
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
                            "human_approval": "Move into planning",
                        },
                    )
                )
                response = await handler(req)

        assert "Transitioned phase to" in response.root.content[0].text
        assert len(response.root.content) == 2
        assert TRANSITION_ADVISORY_NOTE in response.root.content[1].text
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

            server = make_test_server()
            server.tools = [
                ForcePhaseTransitionTool(
                    workspace_root=tmp_path,
                    project_manager=server.project_manager,
                    state_engine=server.phase_state_engine,
                    server_root=tmp_path / ".phase-gate",
                    workphases_config=None,
                )
            ]
            handler = server.server.request_handlers[CallToolRequest]

            with (
                patch.object(server.enforcement_runner, "run", return_value=[]) as mock_run,
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
                            "human_approval": "Approved",
                        },
                    )
                )
                response = await handler(req)

        assert "Transitioned phase to" in response.root.content[0].text
        assert len(response.root.content) == 2
        assert TRANSITION_ADVISORY_NOTE in response.root.content[1].text
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
        )

        with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
            _patch_server_settings(mock_settings_cls, workspace_root=str(tmp_path))

            server = make_test_server()
            server.tools = [
                TransitionPhaseTool(
                    workspace_root=tmp_path,
                    project_manager=project_manager,
                    state_engine=state_engine,
                    server_root=tmp_path / ".phase-gate",
                    workphases_config=None,
                )
            ]
            handler = server.server.request_handlers[CallToolRequest]

            with patch.object(server.enforcement_runner, "run") as mock_run:

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
                            "human_approval": "Move into design",
                        },
                    )
                )
                response = await handler(req)

        texts = [item.text for item in response.root.content]
        assert len(response.root.content) == 1
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

            server = make_test_server()
            server.tools = [
                ForcePhaseTransitionTool(
                    workspace_root=tmp_path,
                    project_manager=server.project_manager,
                    state_engine=server.phase_state_engine,
                    server_root=tmp_path / ".phase-gate",
                    workphases_config=None,
                )
            ]
            handler = server.server.request_handlers[CallToolRequest]

            with (
                patch.object(server.enforcement_runner, "run") as mock_run,
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
                            "human_approval": "Approved",
                        },
                    )
                )
                response = await handler(req)

        text = response.root.content[0].text
        assert len(response.root.content) == 1
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
        ) -> AsyncIterator[tuple[MagicMock, MagicMock]]:
            yield MagicMock(), MagicMock()

        with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
            _patch_server_settings(mock_settings_cls)
            injected_settings = mock_settings_cls.from_env.return_value
            server = make_test_server(settings=injected_settings)
            mock_settings_cls.from_env.reset_mock()

            with (
                patch("mcp_server.server.TextIOWrapper", return_value=MagicMock()),
                patch("mcp_server.server.stdio_server", side_effect=fake_stdio_server),
                patch("mcp_server.server.anyio.wrap_file", return_value=MagicMock()),
                patch.object(server.server, "run", new=AsyncMock()) as mock_run,
            ):
                await server.run()

        mock_settings_cls.from_env.assert_not_called()
        mock_run.assert_awaited_once()


@pytest.mark.asyncio
async def test_call_tool_handles_itool_bridge() -> None:
    """MCPServer should format ITool responses as pure TextContent and cache the DTO."""
    from pydantic import BaseModel, ConfigDict  # noqa: PLC0415

    # We expect this to fail in RED phase because these don't exist yet
    from mcp_server.state.response_cache import ResponseCacheManager  # noqa: PLC0415
    from mcp_server.tools.base import ITool  # noqa: PLC0415
    from mcp_server.tools.decorators import ResourcePublishingDecorator  # noqa: PLC0415
    from tests.mcp_server.test_support import assert_itool_result  # noqa: PLC0415

    class DummyDTO(BaseModel):
        model_config = ConfigDict(frozen=True)
        val: int

    class DummyITool(ITool):
        @property
        def name(self) -> str:
            return "dummy_itool"

        @property
        def description(self) -> str:
            return "Dummy"

        @property
        def args_model(self) -> type[BaseModel] | None:
            return None

        async def execute(
            self,
            params: Any,  # noqa: ARG002, ANN401
            context: NoteContext,  # noqa: ARG002
        ) -> DummyDTO:
            return DummyDTO(val=42)

    with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
        _patch_server_settings(mock_settings_cls)

        server = make_test_server()
        tool = DummyITool()
        cache_manager = ResponseCacheManager()
        server.response_cache_manager = cache_manager
        server.tools = [ResourcePublishingDecorator(tool, cache_manager)]

        handler = server.server.request_handlers[CallToolRequest]

        req = CallToolRequest(
            params=CallToolRequestParams(
                name="dummy_itool",
                arguments={},
            )
        )
        response = await handler(req)

        text_content = assert_itool_result(response.root)
        assert text_content != ""

        import re  # noqa: PLC0415

        match = re.search(r"pgmcp://cache/runs/([a-f0-9\-]+)", text_content)
        assert match is not None
        run_id = match.group(1)

        cached = cache_manager.get(f"pgmcp://cache/runs/{run_id}")
        assert cached is not None
        assert cached.val == 42


@pytest.mark.asyncio
async def test_handle_call_tool_validation_error_intercept() -> None:
    """ValidationError in handle_call_tool should map to ValidationErrorOutput DTO,
    cache it, and format it.
    """
    from pydantic import BaseModel, Field  # noqa: PLC0415
    from mcp_server.schemas.error_outputs import ValidationErrorOutput  # noqa: PLC0415
    from mcp_server.state.response_cache import ResponseCacheManager  # noqa: PLC0415
    from mcp_server.presenters.text_presenter import TextPresenter  # noqa: PLC0415

    class DummyArgs(BaseModel):
        val: int = Field(..., description="Integer field")

    class DummyTool(ITool):
        @property
        def name(self) -> str:
            return "dummy_tool"

        @property
        def description(self) -> str:
            return "Dummy Tool"

        @property
        def args_model(self) -> type[BaseModel] | None:
            return DummyArgs

        @property
        def input_schema(self) -> dict[str, Any]:
            return {"type": "object", "properties": {"val": {"type": "integer"}}}

        async def execute(self, params: Any, context: NoteContext) -> Any:  # noqa: ARG002, ANN401
            return ToolResult.text("success")

    with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
        _patch_server_settings(mock_settings_cls)

        config_data = {
            "global": {
                "default_failure_template": "Failure: {error_message}",
                "emojis": {"failure": "❌"},
            },
            "tools": {},
        }
        presenter = TextPresenter(config_data=config_data)

        server = make_test_server()
        server.presenter = presenter
        tool = DummyTool()
        cache_manager = ResponseCacheManager()
        server.response_cache = cache_manager
        server.response_cache_manager = cache_manager
        server.tools = [tool]

        handler = server.server.request_handlers[CallToolRequest]

        # Call with invalid arguments (missing 'val')
        req = CallToolRequest(
            params=CallToolRequestParams(
                name="dummy_tool",
                arguments={},
            )
        )
        response = await handler(req)

        # Check response content contains the cache message
        content = response.root.content
        assert len(content) == 2  # The formatted text + the schema resource
        text = getattr(content[0], "text", "")
        assert "❌ Failure: Validation failed" in text
        assert "pgmcp://cache/runs/" in text

        import re  # noqa: PLC0415

        match = re.search(r"pgmcp://cache/runs/([a-f0-9\-]+)", text)
        assert match is not None
        run_id = match.group(1)

        cached = cache_manager.get(f"pgmcp://cache/runs/{run_id}")
        assert isinstance(cached, ValidationErrorOutput)
        assert cached.success is False
        assert cached.error_type == "ValidationError"
        assert len(cached.validation_errors) > 0


@pytest.mark.asyncio
async def test_handle_call_tool_enforcement_error_intercept() -> None:
    """MCPError in enforcement runner should map to EnforcementErrorOutput DTO,
    cache it, and format it.
    """
    from pydantic import BaseModel  # noqa: PLC0415
    from mcp_server.schemas.error_outputs import EnforcementErrorOutput  # noqa: PLC0415
    from mcp_server.state.response_cache import ResponseCacheManager  # noqa: PLC0415
    from mcp_server.presenters.text_presenter import TextPresenter  # noqa: PLC0415
    from mcp_server.core.exceptions import MCPError  # noqa: PLC0415

    class DummyTool(ITool):
        @property
        def name(self) -> str:
            return "dummy_tool"

        @property
        def description(self) -> str:
            return "Dummy Tool"

        @property
        def args_model(self) -> type[BaseModel] | None:
            return None

        @property
        def input_schema(self) -> dict[str, Any]:
            return {"type": "object", "properties": {}}

        @property
        def enforcement_event(self) -> str:
            return "test_event"

        async def execute(self, params: Any, context: NoteContext) -> Any:  # noqa: ARG002, ANN401
            return ToolResult.text("success")

    with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
        _patch_server_settings(mock_settings_cls)

        config_data = {
            "global": {
                "default_failure_template": "Failure: {error_message}",
                "emojis": {"failure": "❌"},
                "failures": {"dirty_workdir": "Dirty: {branch}"},
            },
            "tools": {},
        }
        presenter = TextPresenter(config_data=config_data)

        server = make_test_server()
        server.presenter = presenter
        tool = DummyTool()
        cache_manager = ResponseCacheManager()
        server.response_cache = cache_manager
        server.response_cache_manager = cache_manager
        server.tools = [tool]

        # Force enforcement runner to raise MCPError
        with patch.object(server.enforcement_runner, "run") as mock_run:
            mock_run.side_effect = MCPError(
                code="dirty_workdir", message="Workdir is dirty", params={"branch": "main"}
            )

            handler = server.server.request_handlers[CallToolRequest]

            req = CallToolRequest(
                params=CallToolRequestParams(
                    name="dummy_tool",
                    arguments={},
                )
            )
            response = await handler(req)

        content = response.root.content
        assert len(content) == 1
        text = getattr(content[0], "text", "")
        assert "❌ Dirty: main" in text
        assert "pgmcp://cache/runs/" in text

        import re  # noqa: PLC0415

        match = re.search(r"pgmcp://cache/runs/([a-f0-9\-]+)", text)
        assert match is not None
        run_id = match.group(1)

        cached = cache_manager.get(f"pgmcp://cache/runs/{run_id}")
        assert isinstance(cached, EnforcementErrorOutput)
        assert cached.success is False
        assert cached.error_type == "EnforcementError"
        assert cached.error_code == "dirty_workdir"
        assert cached.params == {"branch": "main"}


@pytest.mark.asyncio
async def test_handle_call_tool_execution_error_intercept() -> None:
    """Execution exceptions in tool should map to ExecutionErrorOutput DTO,
    cache it, and format it.
    """
    from pydantic import BaseModel  # noqa: PLC0415
    from mcp_server.schemas.error_outputs import ExecutionErrorOutput  # noqa: PLC0415
    from mcp_server.state.response_cache import ResponseCacheManager  # noqa: PLC0415
    from mcp_server.presenters.text_presenter import TextPresenter  # noqa: PLC0415

    class DummyTool(ITool):
        @property
        def name(self) -> str:
            return "dummy_tool"

        @property
        def description(self) -> str:
            return "Dummy Tool"

        @property
        def args_model(self) -> type[BaseModel] | None:
            return None

        @property
        def input_schema(self) -> dict[str, Any]:
            return {"type": "object", "properties": {}}

        async def execute(self, params: Any, context: NoteContext) -> Any:  # noqa: ARG002, ANN401
            raise ValueError("Execution failed completely")

    with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
        _patch_server_settings(mock_settings_cls)

        config_data = {
            "global": {
                "default_failure_template": "Failure: {error_message}",
                "emojis": {"failure": "❌"},
            },
            "tools": {},
        }
        presenter = TextPresenter(config_data=config_data)

        server = make_test_server()
        server.presenter = presenter
        tool = DummyTool()
        cache_manager = ResponseCacheManager()
        server.response_cache = cache_manager
        server.response_cache_manager = cache_manager
        server.tools = [tool]

        handler = server.server.request_handlers[CallToolRequest]

        req = CallToolRequest(
            params=CallToolRequestParams(
                name="dummy_tool",
                arguments={},
            )
        )
        response = await handler(req)

        content = response.root.content
        assert len(content) == 1
        text = getattr(content[0], "text", "")
        assert "❌ Failure: Execution failed completely" in text
        assert "pgmcp://cache/runs/" in text

        import re  # noqa: PLC0415

        match = re.search(r"pgmcp://cache/runs/([a-f0-9\-]+)", text)
        assert match is not None
        run_id = match.group(1)

        cached = cache_manager.get(f"pgmcp://cache/runs/{run_id}")
        assert isinstance(cached, ExecutionErrorOutput)
        assert cached.success is False
        assert cached.error_type == "ExecutionError"
        assert "Execution failed completely" in cached.message
        assert cached.traceback is not None


@pytest.mark.asyncio
async def test_handle_call_tool_cache_error_intercept() -> None:
    """Caching exceptions should map to CacheErrorOutput DTO,
    and be returned as plain text without crashing.
    """
    from pydantic import BaseModel  # noqa: PLC0415
    from mcp_server.state.response_cache import ResponseCacheManager  # noqa: PLC0415
    from mcp_server.presenters.text_presenter import TextPresenter  # noqa: PLC0415

    class DummyTool(ITool):
        @property
        def name(self) -> str:
            return "dummy_tool"

        @property
        def description(self) -> str:
            return "Dummy Tool"

        @property
        def args_model(self) -> type[BaseModel] | None:
            return None

        @property
        def input_schema(self) -> dict[str, Any]:
            return {"type": "object", "properties": {}}

        async def execute(self, params: Any, context: NoteContext) -> Any:  # noqa: ARG002, ANN401
            raise ValueError("Execution failed completely")

    with patch("mcp_server.config.settings.Settings") as mock_settings_cls:
        _patch_server_settings(mock_settings_cls)

        config_data = {
            "global": {
                "default_failure_template": "Failure: {error_message}",
                "emojis": {"failure": "❌"},
            },
            "tools": {},
        }
        presenter = TextPresenter(config_data=config_data)

        server = make_test_server()
        server.presenter = presenter
        tool = DummyTool()
        cache_manager = ResponseCacheManager()
        server.response_cache = cache_manager
        server.response_cache_manager = cache_manager
        server.tools = [tool]

        # Force cache_manager.put to raise an exception
        with patch.object(cache_manager, "put", side_effect=RuntimeError("Cache disk failure")):
            handler = server.server.request_handlers[CallToolRequest]

            req = CallToolRequest(
                params=CallToolRequestParams(
                    name="dummy_tool",
                    arguments={},
                )
            )
            response = await handler(req)

        content = response.root.content
        assert len(content) == 1
        text = getattr(content[0], "text", "")
        # Should return direct text block with cache error details, no resource cached
        assert "CacheError" in text
        assert "Cache disk failure" in text
        assert "pgmcp://cache/runs/" not in text
