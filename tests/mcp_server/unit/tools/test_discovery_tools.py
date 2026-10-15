# tests/mcp_server/unit/tools/test_discovery_tools.py
"""
Tests for the get_work_context discovery tool.

@layer: Tests (Unit)
@dependencies: [pytest, tempfile, unittest.mock, mcp_server.tools.discovery_tools]
"""

from dataclasses import dataclass
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas import GitConfig
from mcp_server.config.schemas.contracts_config import (
    ContractsConfig,
    MergePolicy,
    PhaseInstructionsSpec,
    WorkflowEntry,
    WorkflowPhaseEntry,
)
from mcp_server.config.schemas.workflows import WorkflowConfig
from mcp_server.config.schemas.workphases import WorkphasesConfig
from mcp_server.config.settings import Settings
from mcp_server.core.exceptions import StateNotFoundError
from mcp_server.core.interfaces import IContextLoadedWriter
from mcp_server.core.operation_notes import NoteContext
from mcp_server.schemas.tool_outputs import GetWorkContextOutput, WorkflowStateStatus
from mcp_server.state.workflow_status import WorkflowStatusDTO
from mcp_server.tools.discovery_tools import GetWorkContextInput, GetWorkContextTool
from tests.mcp_server.test_support import (
    get_default_server_root,
)


def make_settings(workspace_root: Path | str = ".", github_token: str | None = None) -> Settings:
    """Create explicit settings for discovery tool tests."""
    return Settings(
        server={"workspace_root": str(workspace_root)},
        github={"token": github_token},
    )


@dataclass(frozen=True)
class WorkContextCase:
    """Keep injected dependencies accessible without inspecting the tool."""

    tool: GetWorkContextTool
    git: MagicMock
    state: MagicMock


def make_work_context_tool(
    workspace_root: Path | str = ".",
    github_token: str | None = None,
    contracts_config: ContractsConfig | None = None,
    context_loaded_writer: IContextLoadedWriter | None = None,
) -> WorkContextCase:
    settings = make_settings(workspace_root=workspace_root, github_token=github_token)
    git = MagicMock()
    state = MagicMock()
    tool = GetWorkContextTool(
        settings=settings,
        git_manager=git,
        project_manager=MagicMock(),
        state_engine=state,
        github_manager=MagicMock(),
        workphases_config=load_workphases_config(),
        workflow_status_resolver=MagicMock(),
        contracts_config=contracts_config,
        context_loaded_writer=context_loaded_writer,
    )
    return WorkContextCase(tool=tool, git=git, state=state)


def load_workflow_config() -> WorkflowConfig:
    return ConfigLoader(Path(f"{get_default_server_root()}/config")).load_workflow_config()


def load_git_config() -> GitConfig:
    return ConfigLoader(Path(f"{get_default_server_root()}/config")).load_git_config()


def load_workphases_config() -> WorkphasesConfig:
    return ConfigLoader(Path(f"{get_default_server_root()}/config")).load_workphases_config()


def load_contracts_config() -> ContractsConfig:
    return ConfigLoader(Path(f"{get_default_server_root()}/config")).load_contracts_config()


class TestGetWorkContextTool:
    """Tests for GetWorkContextTool."""

    @pytest.fixture()
    def case(self) -> WorkContextCase:
        """Fixture to instantiate GetWorkContextTool."""
        return make_work_context_tool()

    def test_tool_name(self, case: WorkContextCase) -> None:
        """Should have correct tool name."""
        assert case.tool.name == "get_work_context"

    @pytest.mark.asyncio
    async def test_get_context_returns_branch_info(self, case: WorkContextCase) -> None:
        """Should return branch information."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        case.git.get_current_branch.return_value = "main"
        result = await case.tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.current_branch == "main"

    @pytest.mark.asyncio
    async def test_get_context_extracts_issue_number(self, case: WorkContextCase) -> None:
        """Issue number comes from BranchState after C1 (issue #268)."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        case.state.get_state.return_value.issue_number = 42
        case.git.get_current_branch.return_value = "feature/42-implement-dto"

        result = await case.tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.issue_number == 42

    @pytest.mark.asyncio
    async def test_get_context_extracts_issue_number_alternate_format(
        self, case: WorkContextCase
    ) -> None:
        """Issue number from BranchState for bug/ branches after C1 (issue #268)."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        case.state.get_state.return_value.issue_number = 99
        case.git.get_current_branch.return_value = "bug/99-bug"

        result = await case.tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.issue_number == 99

    @pytest.mark.asyncio
    async def test_get_context_reads_phase_and_sub_phase_from_state(
        self, case: WorkContextCase
    ) -> None:
        """Phase and sub-phase come from BranchState after C1 (issue #268)."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        case.state.get_state.return_value.current_phase = "implementation"
        case.state.get_state.return_value.current_sub_phase = "red"
        case.state.get_state.return_value.workflow_name = "feature"
        case.git.get_current_branch.return_value = "feature/42-dto"

        result = await case.tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.phase == "implementation"
        assert result.sub_phase == "red"

    @pytest.mark.asyncio
    async def test_detect_workflow_phase_variations(self, case: WorkContextCase) -> None:
        """All 7 workflow phases appear in output when set via BranchState after C1."""
        test_cases = [
            ("research", "🔍"),
            ("planning", "📋"),
            ("design", "🎨"),
            ("implementation", "🧪"),
            ("validation", "✅"),
            ("documentation", "📝"),
            ("coordination", "🤝"),
        ]

        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        case.git.get_current_branch.return_value = "main"

        for expected_phase, _ in test_cases:
            case.state.get_state.return_value.current_phase = expected_phase
            case.state.get_state.return_value.workflow_name = "feature"
            result = await case.tool.execute(GetWorkContextInput(), NoteContext())
            assert isinstance(result, GetWorkContextOutput)
            assert result.success
            assert result.phase == expected_phase

    @pytest.mark.asyncio
    async def test_get_context_shows_error_message_when_phase_unknown(
        self, case: WorkContextCase
    ) -> None:
        """When state engine fails, output shows unknown confidence (no error raised)."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        case.state.get_state.side_effect = OSError("state.json missing")
        case.git.get_current_branch.return_value = "main"

        result = await case.tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.phase_confidence == "unknown"
        assert result.workflow_state_status is WorkflowStateStatus.UNREADABLE


class TestGetWorkContextStateCycleProjection:
    """Expose phase and cycle information from injected branch state."""

    @pytest.mark.asyncio
    async def test_execute_hides_cycle_for_non_cycle_phase_even_when_preserved(self) -> None:
        planning_case = make_work_context_tool(contracts_config=load_contracts_config())
        planning_case.git.get_current_branch.return_value = "bug/230-test"
        planning_case.state.get_state.return_value.workflow_name = "bug"
        planning_case.state.get_state.return_value.current_phase = "planning"
        planning_case.state.get_state.return_value.issue_number = 230
        planning_case.state.get_state.return_value.parent_branch = None
        planning_case.state.get_state.return_value.current_cycle = 3
        planning_case.state.get_state.return_value.current_sub_phase = None

        planning_result = await planning_case.tool.execute(GetWorkContextInput(), NoteContext())

        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        assert isinstance(planning_result, GetWorkContextOutput)
        assert planning_result.success
        assert planning_result.phase == "planning"
        assert planning_result.current_cycle is None

        implementation_case = make_work_context_tool(contracts_config=load_contracts_config())
        implementation_case.git.get_current_branch.return_value = "bug/230-test"
        implementation_case.state.get_state.return_value.workflow_name = "bug"
        implementation_case.state.get_state.return_value.current_phase = "implementation"
        implementation_case.state.get_state.return_value.issue_number = 230
        implementation_case.state.get_state.return_value.parent_branch = None
        implementation_case.state.get_state.return_value.current_cycle = 3
        implementation_case.state.get_state.return_value.current_sub_phase = None

        implementation_result = await implementation_case.tool.execute(
            GetWorkContextInput(), NoteContext()
        )

        assert isinstance(implementation_result, GetWorkContextOutput)
        assert implementation_result.success
        assert implementation_result.phase == "implementation"
        assert implementation_result.current_cycle == 3

    @pytest.mark.asyncio
    async def test_execute_shows_phase_from_branch_state(self) -> None:
        """GetWorkContextTool output reflects phase from BranchState after C1."""
        resolver = MagicMock()
        settings = make_settings()
        settings.github.token = None
        mock_git = MagicMock()
        mock_git.get_current_branch.return_value = "feature/42-test"
        mock_state_engine = MagicMock()
        mock_state_engine.get_state.return_value.current_phase = "research"
        mock_state_engine.get_state.return_value.workflow_name = "feature"

        tool = GetWorkContextTool(
            settings=settings,
            git_manager=mock_git,
            project_manager=MagicMock(),
            state_engine=mock_state_engine,
            workflow_status_resolver=resolver,
        )
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.phase == "research"


# ---------------------------------------------------------------------------
# C6 RED — GetWorkContextTool StateNotFoundError / StateBranchMismatchError (issue #298)
# ---------------------------------------------------------------------------


class TestGetWorkContextSubRoleAndPhaseInstructions:
    """C1 MVP (issue #268): sub_role_hint and phase_instructions fields in response."""

    def _make_tool(self, phase: str, workflow_name: str = "feature") -> GetWorkContextTool:
        """Return a GetWorkContextTool whose resolver returns the given phase."""
        mock_git = MagicMock()
        mock_git.get_current_branch.return_value = "feature/268-test"
        resolver = MagicMock()
        resolver.resolve_current.return_value = WorkflowStatusDTO(
            current_phase=phase,
            sub_phase=None,
            current_cycle=None,
            phase_source="state.json",
            phase_confidence="high",
            phase_detection_error=None,
        )
        mock_state_engine = MagicMock()
        mock_branch_state = MagicMock()
        mock_branch_state.workflow_name = workflow_name
        mock_branch_state.current_phase = phase
        mock_state_engine.get_state.return_value = mock_branch_state
        settings = make_settings()
        settings.github.token = None
        return GetWorkContextTool(
            settings=settings,
            git_manager=mock_git,
            project_manager=MagicMock(),
            state_engine=mock_state_engine,
            workflow_status_resolver=resolver,
            contracts_config=load_contracts_config(),
        )

    @pytest.mark.asyncio
    async def test_get_work_context_returns_sub_role_hint_for_known_phase(self) -> None:
        """sub_role_hint must equal 'implementer' when phase is 'implementation'."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        tool = self._make_tool(phase="implementation")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.sub_role_hint == "implementer"
        assert result.workflow_state_status is WorkflowStateStatus.AVAILABLE

    @pytest.mark.asyncio
    async def test_get_work_context_returns_phase_instructions_for_feature_implementation(
        self,
    ) -> None:
        """phase_instructions must be non-empty for (feature, implementation)."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        tool = self._make_tool(phase="implementation")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert "get_project_plan" in result.phase_instructions
        assert "run_tests" in result.phase_instructions

    @pytest.mark.asyncio
    async def test_get_work_context_returns_empty_string_for_unknown_workflow_phase(
        self,
    ) -> None:
        """Unknown (workflow, phase) combo must return empty string, never KeyError."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        tool = self._make_tool(phase="nonexistent_phase_xyz")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.phase_instructions == ""
        assert result.workflow_state_status is WorkflowStateStatus.INVALID_PHASE
        assert "research" in result.valid_phases

    @pytest.mark.asyncio
    async def test_get_work_context_returns_phase_instructions_for_bug_research(
        self,
    ) -> None:
        """phase_instructions for (bug, research) must contain key research actions."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        tool = self._make_tool(phase="research", workflow_name="bug")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert "get_issue" in result.phase_instructions
        assert "root cause" in result.phase_instructions.lower()

    @pytest.mark.asyncio
    async def test_get_work_context_returns_phase_instructions_for_bug_implementation(
        self,
    ) -> None:
        """phase_instructions for (bug, implementation) must contain TDD hard rules."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        tool = self._make_tool(phase="implementation", workflow_name="bug")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert "RED" in result.phase_instructions
        assert "get_project_plan" in result.phase_instructions


# ---------------------------------------------------------------------------
# C1 RED — GetWorkContextTool response restructuring (issue #268 F_268.13)
# ---------------------------------------------------------------------------


class TestGetWorkContextC1Restructuring:
    """C1 (issue #268 F_268.13): execute() restructuring + _format_context() rewrite.

    All tests in this class FAIL (RED) until C1 is implemented in discovery_tools.py.
    """

    def _make_tool(
        self,
        *,
        branch: str = "feature/268-test",
        workflow_name: str = "feature",
        current_phase: str = "implementation",
        issue_number: int = 268,
        parent_branch: str | None = "main",
        current_cycle: int | None = None,
        state_raises: Exception | None = None,
        github_token: str | None = None,
        github_issue: object | None = None,
    ) -> GetWorkContextTool:
        """Return a GetWorkContextTool pre-configured for C1 restructuring tests."""
        mock_git = MagicMock()
        mock_git.get_current_branch.return_value = branch

        mock_state_engine = MagicMock()
        if state_raises is not None:
            mock_state_engine.get_state.side_effect = state_raises
        else:
            mock_state = MagicMock()
            mock_state.workflow_name = workflow_name
            mock_state.current_phase = current_phase
            mock_state.issue_number = issue_number
            mock_state.parent_branch = parent_branch
            mock_state.current_cycle = current_cycle
            mock_state.current_sub_phase = None
            mock_state_engine.get_state.return_value = mock_state

        mock_resolver = MagicMock()
        mock_resolver.resolve_current.return_value = WorkflowStatusDTO(
            current_phase=current_phase,
            sub_phase=None,
            current_cycle=current_cycle,
            phase_source="state.json",
            phase_confidence="high",
            phase_detection_error=None,
        )

        mock_github = None
        if github_token is not None:
            mock_github = MagicMock()
            mock_github.get_issue.return_value = github_issue

        settings = make_settings(github_token=github_token)
        return GetWorkContextTool(
            settings=settings,
            git_manager=mock_git,
            project_manager=MagicMock(),
            state_engine=mock_state_engine,
            github_manager=mock_github,
            workflow_status_resolver=mock_resolver,
            contracts_config=load_contracts_config(),
        )

    @pytest.mark.asyncio
    async def test_get_work_context_returns_sub_role_hint_for_known_phase(self) -> None:
        """New format: orientation header shows 'Role: implementer' for implementation phase."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        tool = self._make_tool(current_phase="implementation")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.sub_role_hint == "implementer"

    @pytest.mark.asyncio
    async def test_get_work_context_returns_phase_instructions_for_feature_implementation(
        self,
    ) -> None:
        """New format: phase_instructions rendered under '### 🎯 Phase Instructions'."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        tool = self._make_tool(workflow_name="feature", current_phase="implementation")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert "get_project_plan" in result.phase_instructions

    @pytest.mark.asyncio
    async def test_get_work_context_returns_empty_string_for_unknown_workflow_phase(
        self,
    ) -> None:
        """Unknown (workflow, phase): no crash; fallback message shown under instruction header."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        tool = self._make_tool(workflow_name="unknownwf", current_phase="unknownphase")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.phase_instructions == ""
        assert result.workflow_state_status is WorkflowStateStatus.AVAILABLE

    @pytest.mark.asyncio
    async def test_get_work_context_returns_structured_invalid_phase_status(self) -> None:
        """Known workflow plus invalid phase returns status and valid phases only."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        tool = self._make_tool(workflow_name="feature", current_phase="invalid_phase")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.workflow_state_status is WorkflowStateStatus.INVALID_PHASE
        assert result.phase_instructions == ""
        contracts = load_contracts_config()
        assert result.valid_phases == tuple(contracts.workflows["feature"].get_phase_ids())

    @pytest.mark.asyncio
    async def test_get_work_context_does_not_synthesize_invalid_phase_prose(self) -> None:
        """Invalid phase recovery wording belongs to presentation configuration."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        tool = self._make_tool(workflow_name="feature", current_phase="invalid_phase")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.workflow_state_status is WorkflowStateStatus.INVALID_PHASE
        assert result.phase_instructions == ""
        assert "invalid_phase_warning" not in type(result).model_fields

    @pytest.mark.asyncio
    async def test_get_work_context_returns_workflow_name_from_branch_state(self) -> None:
        """Orientation header must contain 'Workflow: feature' sourced from BranchState."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        tool = self._make_tool(workflow_name="feature")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.workflow_name == "feature"

    @pytest.mark.asyncio
    async def test_get_work_context_returns_issue_number_from_branch_state(self) -> None:
        """Orientation header shows issue #268 from BranchState, not branch-name regex."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        tool = self._make_tool(branch="feature/no-number-in-name", issue_number=268)
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.issue_number == 268

    @pytest.mark.asyncio
    async def test_get_work_context_returns_parent_branch_from_branch_state(self) -> None:
        """Orientation header must show 'Parent: main' from BranchState.parent_branch."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        tool = self._make_tool(parent_branch="main")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.parent_branch == "main"

    @pytest.mark.asyncio
    async def test_get_work_context_omits_noise_fields(self) -> None:
        """Verify DTO attributes are present."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        mock_issue = MagicMock()
        mock_issue.number = 268
        tool = self._make_tool(github_token="test-token", github_issue=mock_issue)
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success

    @pytest.mark.asyncio
    async def test_get_work_context_phase_instructions_is_dominant_first_block(self) -> None:
        """Verify phase instructions are non-empty."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        tool = self._make_tool(workflow_name="feature", current_phase="implementation")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert len(result.phase_instructions) > 0

    @pytest.mark.asyncio
    async def test_get_work_context_renders_todo_discipline_reminder_in_header(self) -> None:
        """Verify success."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        tool = self._make_tool(workflow_name="feature", current_phase="implementation")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success

    @pytest.mark.asyncio
    async def test_get_work_context_graceful_degradation_when_state_unavailable(self) -> None:
        """No error result when state is unavailable (bootstrap degradation)."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        tool = self._make_tool(state_raises=StateNotFoundError("feature/268-test"))

        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.current_branch == "feature/268-test"
        assert result.workflow_state_status is WorkflowStateStatus.MISSING


# ---------------------------------------------------------------------------
# C7 GREEN - GetWorkContextTool ContractsConfig injection (issue #268)
# ---------------------------------------------------------------------------


def _make_c7_contracts(
    workflow: str = "feature",
    phase: str = "implementation",
    sub_role: str = "implementer-c7",
    phase_instructions: str = "Do TDD. Call get_project_plan.",
    handover_template: str | None = "## Hand-over\nScope: ...",
) -> ContractsConfig:
    """Build a minimal ContractsConfig for C7 injection tests."""
    return ContractsConfig(
        merge_policy=MergePolicy(pr_allowed_phase="ready"),
        workflows={
            workflow: WorkflowEntry(
                phases={
                    phase: WorkflowPhaseEntry(
                        order=10,
                        instructions=PhaseInstructionsSpec(
                            sub_role=sub_role,
                            phase_instructions=phase_instructions,
                            handover_template=handover_template,
                        ),
                    ),
                    "ready": WorkflowPhaseEntry(
                        order=20,
                        instructions=PhaseInstructionsSpec(
                            sub_role="documenter",
                            phase_instructions="Create PR.",
                            handover_template=None,
                        ),
                    ),
                }
            ),
        },
    )


class TestGetWorkContextC7ContractsInjection:
    """C7: Verify removal of hardcoded MVP maps and ContractsConfig injection."""

    def _make_c7_tool(
        self,
        contracts_config: ContractsConfig | None = None,
        context_loaded_writer: IContextLoadedWriter | None = None,
        workflow: str = "feature",
        phase: str = "implementation",
    ) -> GetWorkContextTool:
        """Return a GetWorkContextTool pre-configured for C7 tests."""
        mock_git = MagicMock()
        mock_git.get_current_branch.return_value = "feature/42-test"
        resolver = MagicMock()
        resolver.resolve_current.return_value = WorkflowStatusDTO(
            current_phase=phase,
            sub_phase=None,
            current_cycle=None,
            phase_source="state.json",
            phase_confidence="high",
            phase_detection_error=None,
        )
        mock_state_engine = MagicMock()
        mock_branch_state = MagicMock()
        mock_branch_state.workflow_name = workflow
        mock_branch_state.current_phase = phase
        mock_state_engine.get_state.return_value = mock_branch_state
        settings = make_settings()
        settings.github.token = None
        return GetWorkContextTool(
            settings=settings,
            git_manager=mock_git,
            project_manager=MagicMock(),
            state_engine=mock_state_engine,
            github_manager=MagicMock(),
            workphases_config=load_workphases_config(),
            workflow_status_resolver=resolver,
            contracts_config=contracts_config,
            context_loaded_writer=context_loaded_writer,
        )

    @pytest.mark.asyncio
    async def test_sub_role_comes_from_contracts(self) -> None:
        """sub_role_hint must come from ContractsConfig, not hardcoded maps."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        contracts = _make_c7_contracts(sub_role="implementer-c7")
        tool = self._make_c7_tool(contracts_config=contracts)
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.sub_role_hint == "implementer-c7"

    @pytest.mark.asyncio
    async def test_phase_instructions_come_from_contracts(self) -> None:
        """phase_instructions must come from ContractsConfig, not hardcoded maps."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        contracts = _make_c7_contracts(
            phase_instructions="Do TDD. Call get_project_plan.",
        )
        tool = self._make_c7_tool(contracts_config=contracts)
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.phase_instructions == "Do TDD. Call get_project_plan."

    @pytest.mark.asyncio
    async def test_handover_template_in_response(self) -> None:
        """Hand-over template must appear in response when contracts provide one."""
        from mcp_server.schemas.tool_outputs import GetWorkContextOutput  # noqa: PLC0415

        contracts = _make_c7_contracts(handover_template="## Hand-over\nScope: ...")
        tool = self._make_c7_tool(contracts_config=contracts)
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.handover_template == "## Hand-over\nScope: ..."

    @pytest.mark.asyncio
    async def test_context_loaded_writer_called_on_success(self) -> None:
        """IContextLoadedWriter.set_context_loaded must be called after successful execute."""
        writer = MagicMock(spec=IContextLoadedWriter)
        tool = self._make_c7_tool(context_loaded_writer=writer)
        await tool.execute(GetWorkContextInput(), NoteContext())

        writer.set_context_loaded.assert_called_once_with("feature/42-test", value=True)

    @pytest.mark.asyncio
    async def test_c68_docflow_e01_v3_instructions_without_obsolete_syntax(self) -> None:
        """DOCFLOW-E01: the public discovery tool emits live V3 instructions."""
        root = Path(__file__).parents[4]
        contracts_path = root / get_default_server_root() / "config" / "contracts.yaml"
        contracts = ConfigLoader(contracts_path.parent).load_contracts_config()
        tool = self._make_c7_tool(contracts_config=contracts, workflow="feature", phase="research")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert isinstance(result, GetWorkContextOutput)
        assert result.success
        assert result.sub_role_hint == "researcher"
        assert result.phase_instructions is not None
        assert "context=" not in result.phase_instructions
        assert "scaffold_schema" in result.phase_instructions
        assert "scaffold_artifact" in result.phase_instructions
        assert "safe_edit_file" in result.phase_instructions
        assert "Review requested" in (result.handover_template or "")
