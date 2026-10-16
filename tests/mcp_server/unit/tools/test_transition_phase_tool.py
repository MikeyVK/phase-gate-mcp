"""RED tests for transition_phase MCP tool.

Issue #50 - Step 5: Update TransitionPhaseTool to New API

Tests MCP tool that exposes PhaseStateEngine.transition() to users.
Enforces strict sequential phase transitions per workflow definition.

@layer: Tests (Unit)
@dependencies: [pytest, pathlib, mcp_server.tools.phase_tools]
"""

from pathlib import Path
from typing import cast
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel, ValidationError

from mcp_server.core.decorators.input_validation_decorator import InputValidationDecorator
from mcp_server.core.decorators.tool_error_handler_decorator import ToolErrorHandlerDecorator
from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.interfaces.tool_input_contract import JsonObject
from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.phase_state_engine import PhaseStateEngine
from mcp_server.managers.project_manager import ProjectManager
from mcp_server.schemas.deliverables import PlanningMutationError, SavePlanningModel
from mcp_server.schemas.error_outputs import ExecutionErrorOutput
from mcp_server.schemas.tool_outputs import PhaseTransitionOutput
from mcp_server.tools.phase_tools import (
    ForcePhaseTransitionInput,
    ForcePhaseTransitionTool,
    TransitionPhaseInput,
    TransitionPhaseTool,
)
from tests.mcp_server.test_support import make_phase_state_engine, make_project_manager


@pytest.mark.asyncio
@pytest.mark.parametrize("forced", [False, True], ids=["normal", "forced"])
async def test_wrapped_transition_preserves_planning_domain_diagnosis(
    tmp_path: Path, forced: bool
) -> None:
    """Both public transition routes retain the original planning failure facts."""
    engine = MagicMock(spec=PhaseStateEngine)
    failure = PlanningMutationError("planning_stored_invalid", params={"issue_number": 503})
    transition = engine.force_transition if forced else engine.transition
    transition.side_effect = failure
    tool_type = ForcePhaseTransitionTool if forced else TransitionPhaseTool
    core = tool_type(
        workspace_root=tmp_path,
        project_manager=MagicMock(spec=ProjectManager),
        state_engine=engine,
        server_root=tmp_path,
    )
    params: JsonObject = {"branch": "refactor/503-example", "to_phase": "planning"}
    if forced:
        params.update(skip_reason="Repair planning", human_approval_message="Approved repair")

    # Input validation bridges the typed core to the public dictionary boundary.
    validated = InputValidationDecorator(cast(ICoreTool[BaseModel, BaseModel], core))
    wrapped = ToolErrorHandlerDecorator(validated)
    result = await wrapped.execute(params, NoteContext())

    diagnostic = result.operation
    assert isinstance(diagnostic, ExecutionErrorOutput)
    assert diagnostic.error_code == failure.code
    assert diagnostic.error_params == failure.params
    assert diagnostic.traceback is not None
    assert type(failure).__name__ in diagnostic.traceback
    transition.assert_called_once()


class TestTransitionPhaseTool:
    """Test transition_phase MCP tool."""

    @pytest.fixture
    def workspace_root(self, configured_workspace: Path) -> Path:
        """Create temporary workspace."""
        return configured_workspace

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
            issue_number=42,
            issue_title="Test feature",
            workflow_name="feature",
            parent_branch="main",
        )

        # Initialize branch in first phase of feature workflow
        branch = "feature/42-test-feature"
        phase_engine.initialize_branch(
            branch=branch,
            issue_number=42,
            initial_phase=feature_phases[0],
            parent_branch="main",
        )

        return branch

    @pytest.mark.asyncio
    async def test_transition_phase_tool_success(
        self, tool: TransitionPhaseTool, initialized_branch: str, feature_phases: list[str]
    ) -> None:
        """Test successful sequential transition: first → second phase."""
        # Arrange
        params = TransitionPhaseInput(
            branch=initialized_branch,
            to_phase=feature_phases[1],
            human_approval_message="Ready to plan",
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
    @pytest.mark.parametrize(
        ("workflow", "initial", "next_phase", "skipped_phase"),
        [
            ("chore", "research", "implementation", "documentation"),
            ("hotfix", "implementation", "validation", "ready"),
        ],
    )
    async def test_compact_workflow_enforces_its_configured_sequence(
        self,
        tool: TransitionPhaseTool,
        project_manager: ProjectManager,
        phase_engine: PhaseStateEngine,
        workflow: str,
        initial: str,
        next_phase: str,
        skipped_phase: str,
    ) -> None:
        """Compact workflows permit the next phase and rejects skipping a configured phase."""
        project_manager.initialize_project(
            issue_number=446,
            issue_title="Compact workflow",
            workflow_name=workflow,
            parent_branch="main",
        )
        branch = f"{workflow}/446-compact-workflow"
        phase_engine.initialize_branch(
            branch=branch,
            issue_number=446,
            initial_phase=initial,
            parent_branch="main",
        )

        next_result = await tool.execute(
            TransitionPhaseInput(branch=branch, to_phase=next_phase),
            NoteContext(),
        )
        skipped_result = await tool.execute(
            TransitionPhaseInput(branch=branch, to_phase=skipped_phase),
            NoteContext(),
        )

        assert next_result.success is True
        assert next_result.from_phase == initial
        assert next_result.to_phase == next_phase
        assert phase_engine.get_state(branch).current_cycle is None
        assert skipped_result.success is False
        assert skipped_result.error_message is not None
        assert "Invalid transition" in skipped_result.error_message

    @pytest.mark.asyncio
    async def test_transition_phase_tool_emits_advisory_info_note_after_success(
        self, tool: TransitionPhaseTool, initialized_branch: str, feature_phases: list[str]
    ) -> None:
        """Successful transitions should emit the standard get_work_context advisory note."""
        params = TransitionPhaseInput(
            branch=initialized_branch,
            to_phase=feature_phases[1],
            human_approval_message="Ready to plan",
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
            branch=initialized_branch,
            to_phase=feature_phases[2],
            human_approval_message="Trying to skip",
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
            human_approval_message="Should fail",
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
            branch=initialized_branch,
            to_phase="invalid_phase",
            human_approval_message="Should fail",
        )

        # Act
        result = await tool.execute(params, NoteContext())

        # Assert
        assert isinstance(result, PhaseTransitionOutput)
        assert result.success is False

    @pytest.mark.asyncio
    async def test_transition_phase_tool_with_human_approval_message(
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
            branch=initialized_branch,
            to_phase=feature_phases[1],
            human_approval_message=approval_message,
        )

        # Act
        result = await tool.execute(params, NoteContext())

        # Assert - Verify transition succeeded
        assert isinstance(result, PhaseTransitionOutput)
        assert result.success is True

        # Verify human approval recorded in state
        state = phase_engine.get_state(initialized_branch)
        transition = state.transitions[0]
        assert transition["human_approval_message"] == approval_message

    def test_transition_phase_tool_input_model_validation(self, feature_phases: list[str]) -> None:
        """Test that TransitionPhaseInput model validates correctly."""
        # Test valid input
        valid_input = TransitionPhaseInput(branch="feature/42-test", to_phase=feature_phases[1])
        assert valid_input.branch == "feature/42-test"
        assert valid_input.to_phase == feature_phases[1]
        assert valid_input.human_approval_message is None

        # Test with optional human_approval_message
        with_approval = TransitionPhaseInput(
            branch="feature/42-test", to_phase=feature_phases[1], human_approval_message="Ready"
        )
        assert with_approval.human_approval_message == "Ready"

    def test_transition_phase_input_rejects_boolean_approval(self) -> None:
        """Reject boolean input for human_approval_message (C_PHASE_TOOLS.2)."""
        for approval in (True, False):
            with pytest.raises(ValidationError, match="human_approval_message"):
                TransitionPhaseInput.model_validate(
                    {
                        "branch": "feature/42-test",
                        "to_phase": "design",
                        "human_approval_message": approval,
                    }
                )


@pytest.mark.asyncio
@pytest.mark.parametrize("forced", [False, True])
async def test_public_phase_tools_resolve_current_plan_cycle(
    configured_workspace: Path, forced: bool
) -> None:
    """Both public tools carry selection and structured rejection without writes."""
    manager = make_project_manager(configured_workspace)
    manager.initialize_project(491, "Cycle selection", "feature", parent_branch="main")
    manager.save_planning_deliverables(
        491,
        SavePlanningModel.model_validate(
            {
                "cycles": {
                    "cycles": [
                        {
                            "cycle_name": name,
                            "deliverables": [
                                {
                                    "deliverable_name": "Behavior",
                                    "description": "Prove the selected behavior",
                                }
                            ],
                            "exit_criteria": "Focused behavior is proven",
                        }
                        for name in ("First", "Second")
                    ]
                }
            }
        ),
    )
    engine = make_phase_state_engine(configured_workspace, project_manager=manager)
    branch = "feature/491-selection"
    engine.initialize_branch(branch, 491, "planning", parent_branch="main")
    engine.transition(branch, "implementation")
    engine.transition_cycle(branch, 2)
    engine.force_transition(branch, "planning", "Revise the plan", "Owner approval")
    before = engine.get_state(branch)
    tool_kwargs = {
        "workspace_root": configured_workspace,
        "project_manager": manager,
        "state_engine": engine,
        "server_root": configured_workspace,
    }
    tool = ForcePhaseTransitionTool(**tool_kwargs) if forced else TransitionPhaseTool(**tool_kwargs)
    for selection, expected in (
        (None, "cycle_resume_required"),
        ("C_3", "cycle_resume_invalid"),
        ("C_2", None),
    ):
        if forced:
            params = ForcePhaseTransitionInput(
                branch=branch,
                to_phase="implementation",
                resume_cycle=selection,
                skip_reason="Resume selected work",
                human_approval_message="Owner approval",
            )
        else:
            params = TransitionPhaseInput(
                branch=branch, to_phase="implementation", resume_cycle=selection
            )
        result = await tool.execute(params, NoteContext())
        assert result.error_code == expected
        assert result.success is (expected is None)
        state = engine.get_state(branch)
        if expected is not None:
            assert state == before
        else:
            assert state.current_cycle == 2
            assert state.last_cycle is None
            assert state.current_sub_phase is None
            assert state.cycle_history == before.cycle_history
            assert state.transitions[-1]["resume_cycle"] == "C_2"
