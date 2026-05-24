# pyright: reportMissingImports=false
# tests\mcp_server\unit\tools\test_cycle_tools.py
# template=unit_test version=3d15d309 created=2026-03-13T11:30Z updated=
"""Unit tests for the renamed cycle tools module and dispatch hooks.

@layer: Tests (Unit)
@dependencies: pytest, mcp.types, mcp_server.tools.cycle_tools, tests.mcp_server.test_support
"""

from collections.abc import Awaitable, Callable
from pathlib import Path
from shutil import copytree
from unittest.mock import MagicMock, patch

import pytest
from mcp.types import CallToolRequest, CallToolRequestParams

from mcp_server.core.exceptions import ConfigError
from mcp_server.core.operation_notes import InfoNote, NoteContext
from mcp_server.server import MCPServer
from mcp_server.tools.cycle_tools import (
    ForceCycleTransitionInput,
    ForceCycleTransitionTool,
    TransitionCycleInput,
    TransitionCycleTool,
)
from mcp_server.tools.phase_tools import TRANSITION_ADVISORY_NOTE
from mcp_server.tools.tool_result import ToolResult
from tests.mcp_server.test_support import (
    make_git_manager,
    make_phase_state_engine,
    make_project_manager,
)


class FakeForceCycleStateEngine:
    """Minimal force-cycle state engine fake for wrapper tests."""

    def __init__(self, result: dict[str, object]) -> None:
        self._result = result
        self.last_call: dict[str, object] | None = None

    def force_cycle_transition(
        self,
        *,
        branch: str,
        to_cycle: int,
        skip_reason: str,
        human_approval: str,
        gate_runner: object | None = None,
    ) -> dict[str, object]:
        self.last_call = {
            "branch": branch,
            "to_cycle": to_cycle,
            "skip_reason": skip_reason,
            "human_approval": human_approval,
            "gate_runner": gate_runner,
        }
        return self._result


def _make_transition_advisory_execute(
    text: str,
) -> Callable[[object, object, NoteContext], Awaitable[ToolResult]]:
    async def execute(_self: object, _params: object, context: NoteContext) -> ToolResult:
        context.produce(InfoNote(message=TRANSITION_ADVISORY_NOTE))
        return ToolResult.text(text)

    return execute


class TestCycleTools:
    """Cycle tool rename, injection, and enforcement tests."""

    def test_cycle_tools_require_workspace_root_and_define_enforcement_events(
        self,
        tmp_path: Path,
    ) -> None:
        """Cycle tools should use constructor-injected workspace roots and hook metadata."""
        project_manager = make_project_manager(tmp_path)
        state_engine = make_phase_state_engine(tmp_path, project_manager=project_manager)
        git_manager = make_git_manager(tmp_path)
        transition_tool = TransitionCycleTool(
            workspace_root=tmp_path,
            project_manager=project_manager,
            state_engine=state_engine,
            git_manager=git_manager,
            server_root=tmp_path,
        )
        force_tool = ForceCycleTransitionTool(
            workspace_root=tmp_path,
            project_manager=project_manager,
            state_engine=state_engine,
            git_manager=git_manager,
            server_root=tmp_path,
        )

        assert transition_tool.workspace_root == tmp_path
        assert force_tool.workspace_root == tmp_path
        assert transition_tool.enforcement_event == "transition_cycle"
        assert force_tool.enforcement_event == "transition_cycle"

    @pytest.mark.asyncio
    async def test_call_tool_post_enforcement_runs_after_cycle_transition(
        self,
        tmp_path: Path,
    ) -> None:
        """Dispatch post-hook should still run after a successful cycle transition."""
        config_dir = tmp_path / ".phase-gate" / "config"
        copytree(Path.cwd() / ".phase-gate" / "config", config_dir, dirs_exist_ok=True)

        project_manager = make_project_manager(tmp_path)
        project_manager.initialize_project(
            issue_number=257,
            issue_title="Cycle 5.1 enforcement",
            workflow_name="feature",
        )
        project_manager.save_planning_deliverables(
            257,
            {
                "tdd_cycles": {
                    "total": 2,
                    "cycles": [
                        {
                            "cycle_number": 1,
                            "name": "One",
                            "deliverables": ["cycle-1"],
                            "exit_criteria": "pass",
                        },
                        {
                            "cycle_number": 2,
                            "name": "Two",
                            "deliverables": ["cycle-2"],
                            "exit_criteria": "pass",
                        },
                    ],
                }
            },
        )
        state_engine = make_phase_state_engine(
            tmp_path,
            project_manager=project_manager,
        )
        branch = "feature/257-reorder-workflow-phases"
        state_engine.initialize_branch(
            branch=branch,
            issue_number=257,
            initial_phase="implementation",
        )

        with (
            patch("mcp_server.server.Settings") as mock_settings_cls,
            patch(
                "mcp_server.tools.cycle_tools.TransitionCycleTool.execute",
                new=_make_transition_advisory_execute("✅ Transitioned to TDD Cycle 1/2: One"),
            ),
        ):
            mock_settings_cls.from_env.return_value.server.name = "test-server"
            mock_settings_cls.from_env.return_value.server.workspace_root = str(tmp_path)
            mock_settings_cls.from_env.return_value.server.config_root = str(
                tmp_path / ".phase-gate" / "config"
            )
            mock_settings_cls.from_env.return_value.server.server_root_dir = ".phase-gate"
            mock_settings_cls.from_env.return_value.github.token = None
            mock_settings_cls.from_env.return_value.github.owner = "test"
            mock_settings_cls.from_env.return_value.github.repo = "repo"
            mock_settings_cls.from_env.return_value.logging.level = "INFO"
            mock_settings_cls.from_env.return_value.logging.audit_log = ".logs/mcp_audit.log"

            server = MCPServer()
            server.tools = [
                TransitionCycleTool(
                    workspace_root=tmp_path,
                    project_manager=server.project_manager,
                    state_engine=server.phase_state_engine,
                    git_manager=server.git_manager,
                    gate_runner=server.workflow_gate_runner,
                    server_root=tmp_path / ".phase-gate",
                ),
            ]
            handler = server.server.request_handlers[CallToolRequest]

            with patch.object(
                server.enforcement_runner,
                "run",
                return_value=[],
            ) as mock_run:
                req = CallToolRequest(
                    params=CallToolRequestParams(
                        name="transition_cycle",
                        arguments={"to_cycle": 1, "issue_number": 257},
                    )
                )
                response = await handler(req)

        assert "✅" in response.root.content[0].text
        assert len(response.root.content) == 2
        assert response.root.content[1].text == TRANSITION_ADVISORY_NOTE
        assert any(
            call.kwargs.get("event") == "transition_cycle" and call.kwargs.get("timing") == "post"
            for call in mock_run.call_args_list
        )

    @pytest.mark.asyncio
    async def test_call_tool_post_enforcement_runs_after_force_cycle_transition(
        self,
        tmp_path: Path,
    ) -> None:
        """Successful forced cycle transitions append the advisory note after post-hook success."""
        config_dir = tmp_path / ".phase-gate" / "config"
        copytree(Path.cwd() / ".phase-gate" / "config", config_dir, dirs_exist_ok=True)

        with patch("mcp_server.server.Settings") as mock_settings_cls:
            mock_settings_cls.from_env.return_value.server.name = "test-server"
            mock_settings_cls.from_env.return_value.server.workspace_root = str(tmp_path)
            mock_settings_cls.from_env.return_value.server.config_root = str(
                tmp_path / ".phase-gate" / "config"
            )
            mock_settings_cls.from_env.return_value.server.server_root_dir = ".phase-gate"
            mock_settings_cls.from_env.return_value.github.token = None
            mock_settings_cls.from_env.return_value.github.owner = "test"
            mock_settings_cls.from_env.return_value.github.repo = "repo"
            mock_settings_cls.from_env.return_value.logging.level = "INFO"
            mock_settings_cls.from_env.return_value.logging.audit_log = ".logs/mcp_audit.log"

            server = MCPServer()
            server.tools = [
                ForceCycleTransitionTool(
                    workspace_root=tmp_path,
                    project_manager=server.project_manager,
                    state_engine=server.phase_state_engine,
                    git_manager=server.git_manager,
                    gate_runner=server.workflow_gate_runner,
                    server_root=tmp_path / ".phase-gate",
                ),
            ]
            handler = server.server.request_handlers[CallToolRequest]

            with (
                patch.object(server.enforcement_runner, "run", return_value=[]) as mock_run,
                patch.object(
                    ForceCycleTransitionTool,
                    "execute",
                    new=_make_transition_advisory_execute("✅ Forced cycle transition"),
                ),
            ):
                req = CallToolRequest(
                    params=CallToolRequestParams(
                        name="force_cycle_transition",
                        arguments={
                            "to_cycle": 2,
                            "skip_reason": "Force test",
                            "human_approval": "Approved",
                            "issue_number": 257,
                        },
                    )
                )
                response = await handler(req)

        assert response.root.content[0].text == "✅ Forced cycle transition"
        assert len(response.root.content) == 2
        assert response.root.content[1].text == TRANSITION_ADVISORY_NOTE
        assert any(
            call.kwargs.get("event") == "transition_cycle" and call.kwargs.get("timing") == "post"
            for call in mock_run.call_args_list
        )

    @pytest.mark.asyncio
    async def test_call_tool_transition_cycle_post_enforcement_error_omits_advisory_note(
        self,
        tmp_path: Path,
    ) -> None:
        """Post-hook errors must not leak the success-path advisory note for cycle transitions."""
        config_dir = tmp_path / ".phase-gate" / "config"
        copytree(Path.cwd() / ".phase-gate" / "config", config_dir, dirs_exist_ok=True)

        project_manager = make_project_manager(tmp_path)
        project_manager.initialize_project(
            issue_number=257,
            issue_title="Cycle 5.1 enforcement",
            workflow_name="feature",
        )
        project_manager.save_planning_deliverables(
            257,
            {
                "tdd_cycles": {
                    "total": 2,
                    "cycles": [
                        {
                            "cycle_number": 1,
                            "name": "One",
                            "deliverables": ["cycle-1"],
                            "exit_criteria": "pass",
                        },
                        {
                            "cycle_number": 2,
                            "name": "Two",
                            "deliverables": ["cycle-2"],
                            "exit_criteria": "pass",
                        },
                    ],
                }
            },
        )
        state_engine = make_phase_state_engine(
            tmp_path,
            project_manager=project_manager,
        )
        branch = "feature/257-reorder-workflow-phases"
        state_engine.initialize_branch(
            branch=branch,
            issue_number=257,
            initial_phase="implementation",
        )

        with patch("mcp_server.server.Settings") as mock_settings_cls:
            mock_settings_cls.from_env.return_value.server.name = "test-server"
            mock_settings_cls.from_env.return_value.server.workspace_root = str(tmp_path)
            mock_settings_cls.from_env.return_value.server.config_root = str(
                tmp_path / ".phase-gate" / "config"
            )
            mock_settings_cls.from_env.return_value.server.server_root_dir = ".phase-gate"
            mock_settings_cls.from_env.return_value.github.token = None
            mock_settings_cls.from_env.return_value.github.owner = "test"
            mock_settings_cls.from_env.return_value.github.repo = "repo"
            mock_settings_cls.from_env.return_value.logging.level = "INFO"
            mock_settings_cls.from_env.return_value.logging.audit_log = ".logs/mcp_audit.log"

            server = MCPServer()
            server.tools = [
                TransitionCycleTool(
                    workspace_root=tmp_path,
                    project_manager=project_manager,
                    state_engine=state_engine,
                    git_manager=server.git_manager,
                    gate_runner=server.workflow_gate_runner,
                    server_root=tmp_path / ".phase-gate",
                ),
            ]
            handler = server.server.request_handlers[CallToolRequest]

            with (
                patch.object(server.enforcement_runner, "run") as mock_run,
                patch.object(server.git_manager, "get_current_branch", return_value=branch),
            ):

                def side_effect(*_args: object, **kwargs: object) -> list[str]:
                    if kwargs.get("event") == "transition_cycle" and kwargs.get("timing") == "post":
                        raise ConfigError("cycle hook failed")
                    return []

                mock_run.side_effect = side_effect
                req = CallToolRequest(
                    params=CallToolRequestParams(
                        name="transition_cycle",
                        arguments={"to_cycle": 1, "issue_number": 257},
                    )
                )
                response = await handler(req)

        texts = [item.text for item in response.root.content]
        assert len(response.root.content) == 1
        assert "cycle hook failed" in texts[0]
        assert all(TRANSITION_ADVISORY_NOTE not in text for text in texts)

    @pytest.mark.asyncio
    async def test_call_tool_force_cycle_post_enforcement_returns_error(
        self,
        tmp_path: Path,
    ) -> None:
        """Force cycle transitions should fail when post-enforcement raises."""
        config_dir = tmp_path / ".phase-gate" / "config"
        copytree(Path.cwd() / ".phase-gate" / "config", config_dir, dirs_exist_ok=True)

        with patch("mcp_server.server.Settings") as mock_settings_cls:
            mock_settings_cls.from_env.return_value.server.name = "test-server"
            mock_settings_cls.from_env.return_value.server.workspace_root = str(tmp_path)
            mock_settings_cls.from_env.return_value.server.config_root = str(
                tmp_path / ".phase-gate" / "config"
            )
            mock_settings_cls.from_env.return_value.server.server_root_dir = ".phase-gate"
            mock_settings_cls.from_env.return_value.github.token = None
            mock_settings_cls.from_env.return_value.github.owner = "test"
            mock_settings_cls.from_env.return_value.github.repo = "repo"
            mock_settings_cls.from_env.return_value.logging.level = "INFO"
            mock_settings_cls.from_env.return_value.logging.audit_log = ".logs/mcp_audit.log"

            server = MCPServer()
            server.tools = [
                ForceCycleTransitionTool(
                    workspace_root=tmp_path,
                    project_manager=server.project_manager,
                    state_engine=server.phase_state_engine,
                    git_manager=server.git_manager,
                    gate_runner=server.workflow_gate_runner,
                    server_root=tmp_path / ".phase-gate",
                ),
            ]
            handler = server.server.request_handlers[CallToolRequest]

            with (
                patch.object(server.enforcement_runner, "run") as mock_run,
                patch.object(
                    ForceCycleTransitionTool,
                    "execute",
                    new=_make_transition_advisory_execute("✅ Forced cycle transition"),
                ),
            ):

                def side_effect(*_args: object, **kwargs: object) -> list[str]:
                    if kwargs.get("event") == "transition_cycle" and kwargs.get("timing") == "post":
                        raise ConfigError("cycle hook failed")
                    return []

                mock_run.side_effect = side_effect
                req = CallToolRequest(
                    params=CallToolRequestParams(
                        name="force_cycle_transition",
                        arguments={
                            "to_cycle": 2,
                            "skip_reason": "Force test",
                            "human_approval": "Approved",
                            "issue_number": 257,
                        },
                    )
                )
                response = await handler(req)

        text = response.root.content[0].text
        assert len(response.root.content) == 1
        assert "cycle hook failed" in text
        assert "⚠️" not in text
        assert "✅" not in text
        assert TRANSITION_ADVISORY_NOTE not in text


class FakeTransitionCycleStateEngine:
    """Minimal transition-cycle state engine fake for wrapper tests."""

    def __init__(self, result: dict[str, object]) -> None:
        self._result = result
        self.last_call: dict[str, object] | None = None

    def transition_cycle(
        self,
        *,
        branch: str,
        to_cycle: int,
        gate_runner: object | None = None,
    ) -> dict[str, object]:
        self.last_call = {
            "branch": branch,
            "to_cycle": to_cycle,
            "gate_runner": gate_runner,
        }
        return self._result


class TestTransitionCycleToolAdvisoryNote:
    """Success-path advisory note tests for standard cycle transitions."""

    @pytest.mark.asyncio
    async def test_transition_cycle_tool_emits_advisory_info_note_after_success(
        self,
        tmp_path: Path,
    ) -> None:
        """Successful cycle transitions should emit the standard advisory note."""
        gate_runner = object()
        git_manager = MagicMock()
        git_manager.get_current_branch.return_value = "feature/257-cycle-orchestration"
        state_engine = FakeTransitionCycleStateEngine(
            {
                "success": True,
                "to_cycle": 3,
                "total_cycles": 4,
                "cycle_name": "Transition advisory note",
            }
        )
        tool = TransitionCycleTool(
            workspace_root=tmp_path,
            project_manager=MagicMock(),
            state_engine=state_engine,
            git_manager=git_manager,
            gate_runner=gate_runner,
            server_root=tmp_path,
        )
        context = NoteContext()

        result = await tool.execute(
            TransitionCycleInput(to_cycle=3, issue_number=257),
            context,
        )

        assert not result.is_error
        assert state_engine.last_call is not None
        assert state_engine.last_call["gate_runner"] is gate_runner
        notes = context.of_type(InfoNote)
        assert len(notes) == 1
        assert notes[0].message == (
            "🚀 REQUIRED NEXT STEP: Call get_work_context now before any other tool call "
            "to load the current phase context for this branch."
        )

        rendered = context.render_to_response(result)
        assert len(rendered.content) == 2
        assert rendered.content[0]["text"] == result.content[0]["text"]
        assert rendered.content[1]["text"] == notes[0].message


class TestForceCycleToolAdvisoryNote:
    """Success-path advisory note tests for forced cycle transitions."""

    @pytest.mark.asyncio
    async def test_force_cycle_tool_emits_advisory_info_note_after_success(
        self,
        tmp_path: Path,
    ) -> None:
        """Forced cycle transitions should emit the standard advisory note."""
        git_manager = MagicMock()
        git_manager.get_current_branch.return_value = "feature/257-cycle-orchestration"
        state_engine = FakeForceCycleStateEngine(
            {
                "success": True,
                "from_cycle": 2,
                "to_cycle": 3,
                "total_cycles": 4,
                "cycle_name": "Transition advisory note",
                "skipped_gates": [],
                "passing_gates": [],
            }
        )
        tool = ForceCycleTransitionTool(
            workspace_root=tmp_path,
            project_manager=MagicMock(),
            state_engine=state_engine,
            git_manager=git_manager,
            gate_runner=object(),
            server_root=tmp_path,
        )
        context = NoteContext()

        result = await tool.execute(
            ForceCycleTransitionInput(
                to_cycle=3,
                skip_reason="audited skip",
                human_approval="Verifier approved",
                issue_number=257,
            ),
            context,
        )

        assert not result.is_error
        notes = context.of_type(InfoNote)
        assert len(notes) == 1
        assert notes[0].message == (
            "🚀 REQUIRED NEXT STEP: Call get_work_context now before any other tool call "
            "to load the current phase context for this branch."
        )


class TestForceCycleToolFormatting:
    """Formatting tests for the shared force-cycle gate report path."""

    @pytest.mark.asyncio
    async def test_force_cycle_tool_formats_blocking_gates_before_success(
        self,
        tmp_path: Path,
    ) -> None:
        """Blocking gate warnings must appear before the success line."""
        gate_runner = object()
        git_manager = MagicMock()
        git_manager.get_current_branch.return_value = "feature/257-cycle-orchestration"
        state_engine = FakeForceCycleStateEngine(
            {
                "success": True,
                "from_cycle": 2,
                "to_cycle": 4,
                "total_cycles": 4,
                "cycle_name": "Cycle orchestration",
                "skipped_gates": ["cycle-checklist"],
                "passing_gates": ["cycle-docs"],
            }
        )
        tool = ForceCycleTransitionTool(
            workspace_root=tmp_path,
            project_manager=MagicMock(),
            state_engine=state_engine,
            git_manager=git_manager,
            gate_runner=gate_runner,
            server_root=tmp_path,
        )

        result = await tool.execute(
            ForceCycleTransitionInput(
                to_cycle=4,
                skip_reason="audited skip",
                human_approval="Verifier approved",
                issue_number=257,
            ),
            NoteContext(),
        )

        assert not result.is_error
        assert state_engine.last_call is not None
        assert state_engine.last_call["gate_runner"] is gate_runner
        text = result.content[0]["text"]
        assert "ACTION REQUIRED" in text
        assert "cycle-checklist" in text
        assert text.index("ACTION REQUIRED") < text.index("✅")

    @pytest.mark.asyncio
    async def test_force_cycle_tool_formats_passing_gates_after_success(
        self,
        tmp_path: Path,
    ) -> None:
        """Passing gate information must remain informational after the success line."""
        git_manager = MagicMock()
        git_manager.get_current_branch.return_value = "feature/257-cycle-orchestration"
        state_engine = FakeForceCycleStateEngine(
            {
                "success": True,
                "from_cycle": 2,
                "to_cycle": 3,
                "total_cycles": 4,
                "cycle_name": "State recovery",
                "skipped_gates": [],
                "passing_gates": ["cycle-docs"],
            }
        )
        tool = ForceCycleTransitionTool(
            workspace_root=tmp_path,
            project_manager=MagicMock(),
            state_engine=state_engine,
            git_manager=git_manager,
            gate_runner=object(),
            server_root=tmp_path,
        )

        result = await tool.execute(
            ForceCycleTransitionInput(
                to_cycle=3,
                skip_reason="audited skip",
                human_approval="Verifier approved",
                issue_number=257,
            ),
            NoteContext(),
        )

        assert not result.is_error
        text = result.content[0]["text"]
        assert "✅" in text
        assert "cycle-docs" in text
        assert text.index("✅") < text.index("cycle-docs")
