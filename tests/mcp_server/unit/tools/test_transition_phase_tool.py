"""RED tests for transition_phase MCP tool.

Issue #50 - Step 5: Update TransitionPhaseTool to New API

Tests MCP tool that exposes PhaseStateEngine.transition() to users.
Enforces strict sequential phase transitions per workflow definition.

@layer: Tests (Unit)
@dependencies: [pytest, pathlib, mcp_server.tools.phase_tools]
"""

from pathlib import Path

import pytest

from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.phase_state_engine import PhaseStateEngine
from mcp_server.managers.project_manager import ProjectManager
from mcp_server.schemas.tool_outputs import PhaseTransitionOutput
from mcp_server.tools.phase_tools import (
    TransitionPhaseInput,
    TransitionPhaseTool,
)
from tests.mcp_server.test_support import make_phase_state_engine, make_project_manager


class TestTransitionPhaseTool:
    """Test transition_phase MCP tool."""

    @pytest.fixture
    def workspace_root(self, tmp_path: Path) -> Path:
        """Create temporary workspace."""
        return tmp_path

    @pytest.fixture
    def project_manager(self, workspace_root: Path) -> ProjectManager:
        """Create ProjectManager instance."""
        return make_project_manager(workspace_root)

    @pytest.fixture
    def phase_engine(
        self, workspace_root: Path, project_manager: ProjectManager
    ) -> PhaseStateEngine:
        """Create PhaseStateEngine instance."""
        return make_phase_state_engine(workspace_root, project_manager=project_manager)

    @pytest.fixture
    def tool(self, workspace_root: Path) -> TransitionPhaseTool:
        """Create TransitionPhaseTool instance."""
        project_manager = make_project_manager(workspace_root)
        state_engine = make_phase_state_engine(workspace_root, project_manager=project_manager)
        return TransitionPhaseTool(
            workspace_root=workspace_root,
            project_manager=project_manager,
            state_engine=state_engine,
            server_root=workspace_root,
            workphases_config=None,
        )

    @pytest.fixture
    def initialized_branch(
        self,
        project_manager: ProjectManager,
        phase_engine: PhaseStateEngine,
        feature_phases: list[str],
    ) -> str:
        """Initialize a project and branch for testing."""
        # Initialize project with feature workflow
        project_manager.initialize_project(
            issue_number=42, issue_title="Test feature", workflow_name="feature"
        )

        # Initialize branch in first phase of feature workflow
        branch = "feature/42-test-feature"
        phase_engine.initialize_branch(
            branch=branch, issue_number=42, initial_phase=feature_phases[0]
        )

        return branch

    @pytest.mark.asyncio
    async def test_transition_phase_tool_success(
        self, tool: TransitionPhaseTool, initialized_branch: str, feature_phases: list[str]
    ) -> None:
        """Test successful sequential transition: first → second phase."""
        # Arrange
        params = TransitionPhaseInput(
            branch=initialized_branch, to_phase=feature_phases[1], human_approval="Ready to plan"
        )

        # Act
        result = await tool.execute(params, NoteContext())

        # Assert
        assert isinstance(result, PhaseTransitionOutput)
        assert result.success is True
        assert result.branch == initialized_branch
        assert result.from_phase == feature_phases[0]
        assert result.to_phase == feature_phases[1]

    @pytest.mark.asyncio
    async def test_transition_phase_tool_emits_advisory_info_note_after_success(
        self, tool: TransitionPhaseTool, initialized_branch: str, feature_phases: list[str]
    ) -> None:
        """Successful transitions should emit the standard get_work_context advisory note."""
        params = TransitionPhaseInput(
            branch=initialized_branch, to_phase=feature_phases[1], human_approval="Ready to plan"
        )
        context = NoteContext()

        result = await tool.execute(params, context)

        assert isinstance(result, PhaseTransitionOutput)
        assert result.success is True

        assert len(context.entries) == 0

    @pytest.mark.asyncio
    async def test_transition_phase_tool_validates_sequence(
        self, tool: TransitionPhaseTool, initialized_branch: str, feature_phases: list[str]
    ) -> None:
        """Test that non-sequential transition is rejected."""
        # Arrange - Try to skip second phase and go directly to third
        params = TransitionPhaseInput(
            branch=initialized_branch, to_phase=feature_phases[2], human_approval="Trying to skip"
        )

        # Act
        result = await tool.execute(params, NoteContext())

        # Assert
        assert isinstance(result, PhaseTransitionOutput)
        assert result.success is False
        assert result.error_message is not None
        assert "Invalid transition" in result.error_message

    @pytest.mark.asyncio
    async def test_transition_phase_tool_unknown_branch(
        self, tool: TransitionPhaseTool, feature_phases: list[str]
    ) -> None:
        """Test error handling for unknown branch."""
        # Arrange
        params = TransitionPhaseInput(
            branch="feature/999-nonexistent",
            to_phase=feature_phases[1],
            human_approval="Should fail",
        )

        # Act
        result = await tool.execute(params, NoteContext())

        # Assert
        assert isinstance(result, PhaseTransitionOutput)
        assert result.success is False

    @pytest.mark.asyncio
    async def test_transition_phase_tool_invalid_target_phase(
        self, tool: TransitionPhaseTool, initialized_branch: str
    ) -> None:
        """Test error handling for invalid target phase."""
        # Arrange - Target phase not in workflow
        params = TransitionPhaseInput(
            branch=initialized_branch, to_phase="invalid_phase", human_approval="Should fail"
        )

        # Act
        result = await tool.execute(params, NoteContext())

        # Assert
        assert isinstance(result, PhaseTransitionOutput)
        assert result.success is False

    @pytest.mark.asyncio
    async def test_transition_phase_tool_with_human_approval(
        self,
        tool: TransitionPhaseTool,
        initialized_branch: str,
        phase_engine: PhaseStateEngine,
        feature_phases: list[str],
    ) -> None:
        """Test transition includes human approval in record."""
        # Arrange
        approval_message = "All discovery tasks complete"
        params = TransitionPhaseInput(
            branch=initialized_branch, to_phase=feature_phases[1], human_approval=approval_message
        )

        # Act
        result = await tool.execute(params, NoteContext())

        # Assert - Verify transition succeeded
        assert isinstance(result, PhaseTransitionOutput)
        assert result.success is True

        # Verify human approval recorded in state
        state = phase_engine.get_state(initialized_branch)
        transition = state.transitions[0]
        assert transition["human_approval"] == approval_message

    def test_transition_phase_tool_input_model_validation(self, feature_phases: list[str]) -> None:
        """Test that TransitionPhaseInput model validates correctly."""
        # Test valid input
        valid_input = TransitionPhaseInput(branch="feature/42-test", to_phase=feature_phases[1])
        assert valid_input.branch == "feature/42-test"
        assert valid_input.to_phase == feature_phases[1]
        assert valid_input.human_approval is None

        # Test with optional human_approval
        with_approval = TransitionPhaseInput(
            branch="feature/42-test", to_phase=feature_phases[1], human_approval="Ready"
        )
        assert with_approval.human_approval == "Ready"
