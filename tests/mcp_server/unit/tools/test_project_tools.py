"""Public project tools and complete planning command/readback behavior.

@layer: Tests (Unit)
"""

from pathlib import Path
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from mcp_server.core.interfaces.git import CycleEvidence
from mcp_server.core.operation_notes import Note, NoteContext
from mcp_server.managers.project_manager import ProjectManager
from mcp_server.schemas.deliverables import (
    AppendCycle,
    CycleInput,
    CyclesInput,
    DeliverableInput,
    PhaseBlockInput,
    RemoveCycle,
    RemovePhase,
    ReplaceCycle,
    SavePlanningModel,
    SetPhase,
)
from mcp_server.tools.project_tools import (
    GetProjectPlanInput,
    GetProjectPlanTool,
    InitializeProjectInput,
    InitializeProjectTool,
    SavePlanningDeliverablesInput,
    SavePlanningDeliverablesTool,
    UpdatePlanningDeliverablesInput,
    UpdatePlanningDeliverablesTool,
)
from tests.mcp_server.test_support import (
    make_git_manager,
    make_phase_state_engine,
    make_project_manager,
)


class TestInitializeProjectToolParentBranch:
    """Test parent_branch functionality in InitializeProjectTool."""

    @pytest.fixture
    def workspace_root(self, legacy_suite_workspace: Path) -> Path:
        """Create temporary workspace.

        Args:
            legacy_suite_workspace: Pytest legacy_suite_workspace fixture

        Returns:
            Path to temporary workspace root
        """
        return legacy_suite_workspace

    @pytest.fixture
    def tool(self, workspace_root: Path) -> InitializeProjectTool:
        """Create InitializeProjectTool instance.

        Args:
            workspace_root: Path to workspace root

        Returns:
            InitializeProjectTool instance
        """
        manager = make_project_manager(workspace_root)
        return InitializeProjectTool(
            workspace_root=workspace_root,
            manager=manager,
            git_manager=make_git_manager(workspace_root),
            state_engine=make_phase_state_engine(workspace_root, project_manager=manager),
            contracts_config=None,
        )

    @pytest.mark.asyncio
    async def test_reinitialization_rejects_before_project_and_state_writes(
        self, tool: InitializeProjectTool, workspace_root: Path
    ) -> None:
        """An initialized branch retains both files when initialization is rejected."""
        branch = "feature/491-guard"
        with patch.object(tool.git_manager, "get_current_branch", return_value=branch):
            first = await tool.execute(
                InitializeProjectInput(
                    issue_number=491,
                    issue_title="Original",
                    workflow_name="feature",
                    parent_branch="main",
                ),
                NoteContext(),
            )
            assert first.success
            plan_path = workspace_root / ".pgmcp" / "deliverables.json"
            before_plan = plan_path.read_bytes()
            before_state = tool.state_engine.get_state(branch)
            rejected = await tool.execute(
                InitializeProjectInput(
                    issue_number=491,
                    issue_title="Changed",
                    workflow_name="bug",
                    parent_branch="main",
                ),
                NoteContext(),
            )
        assert not rejected.success
        assert plan_path.read_bytes() == before_plan
        assert tool.state_engine.get_state(branch) == before_state

    @pytest.mark.asyncio
    async def test_initialize_with_explicit_parent_branch(
        self, tool: InitializeProjectTool
    ) -> None:
        """Test initializing project with explicit parent_branch."""
        from mcp_server.schemas.tool_outputs import InitializeProjectOutput  # noqa: PLC0415

        # Mock git to return current branch
        with patch.object(tool.git_manager, "get_current_branch") as mock_branch:
            mock_branch.return_value = "feature/79-test"

            # Execute
            result = await tool.execute(
                InitializeProjectInput(
                    issue_number=79,
                    issue_title="Test",
                    workflow_name="feature",
                    parent_branch="epic/76-quality-gates",
                ),
                NoteContext(),
            )

        # Verify
        assert isinstance(result, InitializeProjectOutput)
        assert result.success
        assert result.parent_branch == "epic/76-quality-gates"

    @pytest.mark.asyncio
    async def test_initialize_auto_detects_parent_branch(self, tool: InitializeProjectTool) -> None:
        """Test auto-detection of parent_branch via git reflog."""
        from mcp_server.schemas.tool_outputs import InitializeProjectOutput  # noqa: PLC0415

        # Mock git operations
        with (
            patch.object(tool.git_manager, "get_current_branch") as mock_branch,
            patch.object(tool, "_detect_parent_branch_from_reflog") as mock_detect,
        ):
            mock_branch.return_value = "feature/80-test"
            mock_detect.return_value = "main"  # Auto-detected

            # Execute - no parent_branch parameter
            result = await tool.execute(
                InitializeProjectInput(
                    issue_number=80, issue_title="Test Auto-detect", workflow_name="bug"
                ),
                NoteContext(),
            )

        # Verify
        assert isinstance(result, InitializeProjectOutput)
        assert result.success
        assert result.parent_branch == "main"
        mock_detect.assert_called_once_with("feature/80-test")

    @pytest.mark.asyncio
    async def test_initialize_auto_detect_fails_gracefully(
        self, tool: InitializeProjectTool
    ) -> None:
        """Test auto-detection failure results in None."""
        from mcp_server.schemas.tool_outputs import InitializeProjectOutput  # noqa: PLC0415

        # Mock git operations
        with (
            patch.object(tool.git_manager, "get_current_branch") as mock_branch,
            patch.object(tool, "_detect_parent_branch_from_reflog") as mock_detect,
        ):
            mock_branch.return_value = "feature/81-test"
            mock_detect.return_value = None  # Detection failed

            # Execute
            result = await tool.execute(
                InitializeProjectInput(
                    issue_number=81, issue_title="Test Failed Detect", workflow_name="docs"
                ),
                NoteContext(),
            )

        # Verify - no error, parent_branch is null
        assert isinstance(result, InitializeProjectOutput)
        assert result.success
        assert result.parent_branch is None
        mock_detect.assert_called_once_with("feature/81-test")

    @pytest.mark.asyncio
    async def test_explicit_parent_branch_overrides_auto_detect(
        self, tool: InitializeProjectTool
    ) -> None:
        """Test explicit parent_branch skips auto-detection."""
        from mcp_server.schemas.tool_outputs import InitializeProjectOutput  # noqa: PLC0415

        # Mock git operations
        with (
            patch.object(tool.git_manager, "get_current_branch") as mock_branch,
            patch.object(tool, "_detect_parent_branch_from_reflog") as mock_detect,
        ):
            mock_branch.return_value = "feature/82-test"

            # Execute with explicit parent_branch
            result = await tool.execute(
                InitializeProjectInput(
                    issue_number=82,
                    issue_title="Test Override",
                    workflow_name="feature",
                    parent_branch="epic/special",
                ),
                NoteContext(),
            )

        # Verify - auto-detect NOT called
        assert isinstance(result, InitializeProjectOutput)
        assert result.success
        assert result.parent_branch == "epic/special"
        mock_detect.assert_not_called()


class _GetProjectPlanManagerStub:
    """Minimal manager stub for GetProjectPlanTool tests."""

    def __init__(
        self,
        plan: dict[str, object] | None,
        error: Exception | None = None,
    ) -> None:
        self._plan = plan
        self._error = error
        self.issue_numbers: list[int] = []

    def get_project_plan(self, issue_number: int) -> dict[str, object] | None:
        self.issue_numbers.append(issue_number)
        if self._error is not None:
            raise self._error
        return self._plan


class TestGetProjectPlanTool:
    """Issue #253 C5: operator guidance on missing project plan."""

    @pytest.mark.asyncio
    async def test_get_plan_exists_returns_text_json(self) -> None:
        from mcp_server.schemas.tool_outputs import ProjectPlanOutput  # noqa: PLC0415

        plan = {"issue_number": 253, "workflow_name": "bug", "current_phase": "implementation"}
        # Stub the manager to return plan (the tool will parse and map this dict)
        # We will mock the mapper or stub dict output
        # Let's ensure the tool maps it properly
        tool = GetProjectPlanTool(manager=_GetProjectPlanManagerStub(plan=plan))
        context = NoteContext()

        result = await tool.execute(GetProjectPlanInput(issue_number=253), context)

        assert isinstance(result, ProjectPlanOutput)
        assert result.success
        assert result.issue_number == 253
        assert result.workflow_name == "bug"
        assert len(context.entries) == 0

    @pytest.mark.asyncio
    async def test_get_plan_not_found_returns_error(self) -> None:
        from mcp_server.schemas.tool_outputs import ProjectPlanOutput  # noqa: PLC0415

        tool = GetProjectPlanTool(manager=_GetProjectPlanManagerStub(plan=None))
        context = NoteContext()

        result = await tool.execute(GetProjectPlanInput(issue_number=253), context)

        assert isinstance(result, ProjectPlanOutput)
        assert not result.success
        assert result.error_message == "No project plan found for issue #253"

    @pytest.mark.asyncio
    async def test_get_plan_not_found_adds_suggestion_note(self) -> None:
        tool = GetProjectPlanTool(manager=_GetProjectPlanManagerStub(plan=None))
        context = NoteContext()

        await tool.execute(GetProjectPlanInput(issue_number=253), context)

        notes = context.entries
        assert len(notes) == 1
        assert isinstance(notes[0], Note)
        assert notes[0].key == "initialize_project_suggestion"
        assert notes[0].params == {"issue_number": 253}

    # Obsolete test removed
    @pytest.mark.asyncio
    async def test_get_plan_value_error_returns_error(self) -> None:
        from mcp_server.schemas.tool_outputs import ProjectPlanOutput  # noqa: PLC0415

        tool = GetProjectPlanTool(
            manager=_GetProjectPlanManagerStub(plan=None, error=ValueError("bad plan state"))
        )
        context = NoteContext()

        result = await tool.execute(GetProjectPlanInput(issue_number=253), context)

        assert isinstance(result, ProjectPlanOutput)
        assert not result.success
        assert result.error_message == "bad plan state"
        assert len(context.entries) == 0

    @pytest.mark.asyncio
    async def test_get_plan_returns_complete_stored_planning(self) -> None:
        """The read-only dependency preserves D1/D2, order and exit criteria."""
        payload = _stored_deliverables()
        manager = _GetProjectPlanManagerStub(
            plan={"workflow_name": "feature", "planning_deliverables": payload}
        )
        result = await GetProjectPlanTool(manager=manager).execute(
            GetProjectPlanInput(issue_number=253), NoteContext()
        )

        assert result.success
        assert result.planning_deliverables is not None
        assert result.planning_deliverables.model_dump(exclude_none=True) == payload
        assert manager.issue_numbers == [253]

    @pytest.mark.asyncio
    async def test_get_plan_without_planning_remains_supported(self) -> None:
        """An initialized project need not have planning deliverables yet."""
        manager = _GetProjectPlanManagerStub(plan={"workflow_name": "feature"})
        result = await GetProjectPlanTool(manager=manager).execute(
            GetProjectPlanInput(issue_number=253), NoteContext()
        )
        assert result.success
        assert result.planning_deliverables is None

    @pytest.mark.asyncio
    async def test_get_plan_rejects_invalid_stored_planning(self) -> None:
        """A corrupt payload must not become a successful partial plan."""
        manager = _GetProjectPlanManagerStub(
            plan={"workflow_name": "feature", "planning_deliverables": {"unexpected": []}}
        )
        result = await GetProjectPlanTool(manager=manager).execute(
            GetProjectPlanInput(issue_number=253), NoteContext()
        )
        assert not result.success
        assert result.error_message is not None
        assert "unexpected" in result.error_message
        assert result.planning_deliverables is None


def _minimal_deliverables() -> SavePlanningModel:
    """One complete authored cycle; references are server-owned."""
    return SavePlanningModel(
        cycles=CyclesInput(cycles=[_cycle("First", "Initial public boundary")]),
    )


def _cycle(name: str, description: str) -> CycleInput:
    return CycleInput(
        cycle_name=name,
        deliverables=[DeliverableInput(deliverable_name=name, description=description)],
        exit_criteria=f"{name} verified",
    )


def _stored_deliverables() -> dict[str, object]:
    """A complete stored value for the read-only dependency."""
    return {
        "cycles": {
            "total": 1,
            "cycles": [
                {
                    "cycle_id": "C_1",
                    "cycle_number": 1,
                    "cycle_name": "First",
                    "deliverables": [
                        {
                            "deliverable_id": "D_1.1",
                            "deliverable_name": "First",
                            "description": "Initial public boundary",
                        }
                    ],
                    "exit_criteria": "First verified",
                }
            ],
        },
        "phases": {},
    }


class _CompleteEvidence:
    """Supply explicit complete execution evidence to planning update tests."""

    def read_cycle_evidence(self, issue_number: int, execution_phase: str | None) -> CycleEvidence:
        return CycleEvidence(
            status="complete",
            branch=f"feature/{issue_number}-test",
            head_sha="test-head",
            execution_phase=execution_phase,
            protected_cycle_numbers=(),
        )


@pytest.fixture
def planning_manager(legacy_suite_workspace: Path) -> ProjectManager:
    manager = make_project_manager(
        legacy_suite_workspace, cycle_evidence_reader=_CompleteEvidence()
    )
    manager.initialize_project(229, "Planning commands", "feature")
    return manager


class TestPlanningCommands:
    """Public command results expose the complete, actually persisted plan."""

    @pytest.mark.asyncio
    async def test_save_numbers_names_and_returns_complete_plan(
        self, planning_manager: ProjectManager
    ) -> None:
        result = await SavePlanningDeliverablesTool(manager=planning_manager).execute(
            SavePlanningDeliverablesInput(
                issue_number=229, planning_deliverables=_minimal_deliverables()
            ),
            NoteContext(),
        )
        assert result.success
        assert result.total_cycles == 1 and result.total_deliverables == 1
        assert result.planning_deliverables is not None
        cycle = result.planning_deliverables.cycles
        assert cycle is not None
        assert cycle.cycles[0].cycle_id == "C_1"
        assert cycle.cycles[0].deliverables[0].deliverable_id == "D_1.1"
        assert cycle.cycles[0].cycle_name == "First"
        assert result.cycles[0].cycle_id == "C_1"
        assert result.cycles[0].cycle_name == "First"
        plan = planning_manager.get_project_plan(229)
        assert plan is not None
        assert (
            result.planning_deliverables.model_dump(exclude_none=True)
            == plan["planning_deliverables"]
        )

    @pytest.mark.asyncio
    async def test_duplicate_save_returns_failure_without_a_successful_plan(
        self, planning_manager: ProjectManager
    ) -> None:
        tool = SavePlanningDeliverablesTool(manager=planning_manager)
        params = SavePlanningDeliverablesInput(
            issue_number=229, planning_deliverables=_minimal_deliverables()
        )
        assert (await tool.execute(params, NoteContext())).success
        before = planning_manager.get_project_plan(229)
        result = await tool.execute(params, NoteContext())
        assert not result.success and result.error_code is not None
        assert result.planning_deliverables is None
        assert result.total_cycles == 0 and result.total_deliverables == 0
        assert planning_manager.get_project_plan(229) == before

    @pytest.mark.asyncio
    async def test_append_and_replace_return_preserved_and_replaced_blocks(
        self, planning_manager: ProjectManager
    ) -> None:
        planning_manager.save_planning_deliverables(229, _minimal_deliverables())
        tool = UpdatePlanningDeliverablesTool(manager=planning_manager)
        result = await tool.execute(
            UpdatePlanningDeliverablesInput(
                issue_number=229,
                operations=[
                    ReplaceCycle(
                        op="replace_cycle", cycle_id="C_1", cycle=_cycle("Revised", "Replacement")
                    ),
                    AppendCycle(op="append_cycle", cycle=_cycle("Second", "New boundary")),
                ],
            ),
            NoteContext(),
        )
        assert result.success and result.total_cycles == 2 and result.total_deliverables == 2
        assert result.planning_deliverables is not None
        cycles = result.planning_deliverables.cycles
        assert cycles is not None
        assert [cycle.cycle_name for cycle in cycles.cycles] == ["Revised", "Second"]
        assert [cycle.cycle_id for cycle in cycles.cycles] == ["C_1", "C_2"]
        assert [cycle.deliverables[0].deliverable_id for cycle in cycles.cycles] == [
            "D_1.1",
            "D_2.1",
        ]
        assert cycles.cycles[0].exit_criteria == "Revised verified"

    @pytest.mark.asyncio
    @pytest.mark.parametrize("phase", ["design", "validation", "documentation"])
    async def test_set_phase_replaces_complete_block_and_retains_cycles(
        self, planning_manager: ProjectManager, phase: str
    ) -> None:
        original = PhaseBlockInput(
            deliverables=[
                DeliverableInput(deliverable_name="Original", description="Original block")
            ]
        )
        planning_manager.save_planning_deliverables(
            229, SavePlanningModel(cycles=_minimal_deliverables().cycles, phases={phase: original})
        )
        replacement = PhaseBlockInput(
            deliverables=[
                DeliverableInput(deliverable_name="Replacement", description="Replacement block")
            ]
        )
        result = await UpdatePlanningDeliverablesTool(manager=planning_manager).execute(
            UpdatePlanningDeliverablesInput(
                issue_number=229,
                operations=[SetPhase(op="set_phase", phase=phase, block=replacement)],
            ),
            NoteContext(),
        )
        assert result.success and result.total_deliverables == 2
        assert result.planning_deliverables is not None
        block = result.planning_deliverables.phases[phase]
        assert len(block.deliverables) == 1
        assert block.deliverables[0].deliverable_name == "Replacement"
        assert block.deliverables[0].deliverable_id == "D_1"
        cycles = result.planning_deliverables.cycles
        assert cycles is not None and cycles.cycles[0].cycle_name == "First"

    @pytest.mark.asyncio
    async def test_remove_phase_and_cycle_are_explicit_and_compact_references(
        self, planning_manager: ProjectManager
    ) -> None:
        planning_manager.save_planning_deliverables(
            229,
            SavePlanningModel(
                cycles=CyclesInput(
                    cycles=[_cycle("First", "First block"), _cycle("Second", "Second block")]
                ),
                phases={
                    "design": PhaseBlockInput(
                        deliverables=[
                            DeliverableInput(deliverable_name="Design", description="Design block")
                        ]
                    )
                },
            ),
        )
        result = await UpdatePlanningDeliverablesTool(manager=planning_manager).execute(
            UpdatePlanningDeliverablesInput(
                issue_number=229,
                operations=[
                    RemoveCycle(op="remove_cycle", cycle_id="C_1"),
                    RemovePhase(op="remove_phase", phase="design"),
                ],
            ),
            NoteContext(),
        )
        assert result.success and result.total_cycles == 1 and result.total_deliverables == 1
        assert result.planning_deliverables is not None
        assert result.planning_deliverables.phases == {}
        cycles = result.planning_deliverables.cycles
        assert cycles is not None
        assert cycles.cycles[0].cycle_id == "C_1"
        assert cycles.cycles[0].cycle_name == "Second"
        assert cycles.cycles[0].deliverables[0].deliverable_id == "D_1.1"

    @pytest.mark.asyncio
    async def test_update_before_save_returns_failure_and_no_plan(
        self, planning_manager: ProjectManager
    ) -> None:
        result = await UpdatePlanningDeliverablesTool(manager=planning_manager).execute(
            UpdatePlanningDeliverablesInput(
                issue_number=229,
                operations=[AppendCycle(op="append_cycle", cycle=_cycle("First", "First block"))],
            ),
            NoteContext(),
        )
        assert not result.success and result.error_code is not None
        assert result.planning_deliverables is None and result.total_cycles == 0

    @pytest.mark.asyncio
    async def test_unknown_configured_phase_rejects_without_changing_plan(
        self, planning_manager: ProjectManager
    ) -> None:
        planning_manager.save_planning_deliverables(229, _minimal_deliverables())
        before = planning_manager.get_project_plan(229)
        result = await UpdatePlanningDeliverablesTool(manager=planning_manager).execute(
            UpdatePlanningDeliverablesInput(
                issue_number=229,
                operations=[
                    SetPhase(
                        op="set_phase",
                        phase="unknown_phase",
                        block=PhaseBlockInput(
                            deliverables=[
                                DeliverableInput(
                                    deliverable_name="Invalid", description="Unknown phase"
                                )
                            ]
                        ),
                    )
                ],
            ),
            NoteContext(),
        )
        assert not result.success and result.error_code is not None
        assert planning_manager.get_project_plan(229) == before

    @pytest.mark.parametrize(
        "validates",
        [
            {"type": "does_not_exist", "file": "x.py"},
            {"type": "contains_text", "file": "x.py"},
            {"type": "file_glob", "dir": "src", "pattern": ""},
        ],
    )
    def test_invalid_rule_is_rejected_at_request_admission(self, validates: dict[str, str]) -> None:
        with pytest.raises(ValidationError):
            SavePlanningDeliverablesInput.model_validate(
                {
                    "issue_number": 229,
                    "planning_deliverables": {
                        "cycles": {
                            "cycles": [
                                {
                                    "cycle_name": "Invalid rule",
                                    "exit_criteria": "Not persisted",
                                    "deliverables": [
                                        {
                                            "deliverable_name": "Rule",
                                            "description": "Rule admission",
                                            "validates": validates,
                                        }
                                    ],
                                }
                            ]
                        }
                    },
                }
            )


class TestProjectManagerWorkflowStatusResolverC4:
    """C4 coverage: ProjectManager.workflow_status_resolver parameter (Issue #231 C4)."""

    def test_project_manager_accepts_workflow_status_resolver_kwarg(
        self, legacy_suite_workspace: Path
    ) -> None:
        """ProjectManager constructed with workflow_status_resolver calls it on get_project_plan."""
        from unittest.mock import MagicMock  # noqa: PLC0415

        from mcp_server.state.workflow_status import WorkflowStatusDTO  # noqa: PLC0415

        mock_resolver = MagicMock()
        mock_resolver.resolve_current.return_value = WorkflowStatusDTO(
            current_phase="research",
            sub_phase=None,
            current_cycle=None,
            phase_source="state.json",
            phase_confidence="high",
            phase_detection_error=None,
        )
        manager = make_project_manager(
            legacy_suite_workspace, workflow_status_resolver=mock_resolver
        )
        manager.initialize_project(
            issue_number=231,
            issue_title="State Snapshot CQRS",
            workflow_name="feature",
        )
        plan = manager.get_project_plan(231)
        assert plan is not None
        mock_resolver.resolve_current.assert_called_once()

    def test_get_project_plan_uses_resolver_resolve_current(
        self, legacy_suite_workspace: Path
    ) -> None:
        """get_project_plan delegates phase detection to resolver.resolve_current()."""
        from unittest.mock import MagicMock  # noqa: PLC0415

        from mcp_server.state.workflow_status import WorkflowStatusDTO  # noqa: PLC0415

        mock_resolver = MagicMock()
        mock_resolver.resolve_current.return_value = WorkflowStatusDTO(
            current_phase="implementation",
            sub_phase="red",
            current_cycle=3,
            phase_source="state.json",
            phase_confidence="high",
            phase_detection_error=None,
        )
        manager = make_project_manager(
            legacy_suite_workspace, workflow_status_resolver=mock_resolver
        )
        manager.initialize_project(
            issue_number=231,
            issue_title="State Snapshot CQRS",
            workflow_name="feature",
        )

        plan = manager.get_project_plan(231)

        assert plan is not None
        mock_resolver.resolve_current.assert_called_once()
        assert plan["current_phase"] == "implementation:red"

    def test_get_project_plan_includes_phase_source(self, legacy_suite_workspace: Path) -> None:
        """get_project_plan includes phase_source from resolver in returned plan."""
        from unittest.mock import MagicMock  # noqa: PLC0415

        from mcp_server.state.workflow_status import WorkflowStatusDTO  # noqa: PLC0415

        mock_resolver = MagicMock()
        mock_resolver.resolve_current.return_value = WorkflowStatusDTO(
            current_phase="validation",
            sub_phase=None,
            current_cycle=None,
            phase_source="state.json",
            phase_confidence="high",
            phase_detection_error=None,
        )
        manager = make_project_manager(
            legacy_suite_workspace, workflow_status_resolver=mock_resolver
        )
        manager.initialize_project(
            issue_number=231,
            issue_title="State Snapshot CQRS",
            workflow_name="feature",
        )

        plan = manager.get_project_plan(231)

        assert plan is not None
        assert plan["phase_source"] == "state.json"
        assert plan["current_phase"] == "validation"

    def test_get_project_plan_includes_phase_detection_error(
        self, legacy_suite_workspace: Path
    ) -> None:
        """get_project_plan includes phase_detection_error from resolver."""
        from unittest.mock import MagicMock  # noqa: PLC0415

        from mcp_server.state.workflow_status import WorkflowStatusDTO  # noqa: PLC0415

        mock_resolver = MagicMock()
        mock_resolver.resolve_current.return_value = WorkflowStatusDTO(
            current_phase="validation",
            sub_phase=None,
            current_cycle=None,
            phase_source="state.json",
            phase_confidence="high",
            phase_detection_error="No commits found",
        )
        manager = make_project_manager(
            legacy_suite_workspace, workflow_status_resolver=mock_resolver
        )
        manager.initialize_project(
            issue_number=231,
            issue_title="State Snapshot CQRS",
            workflow_name="feature",
        )

        plan = manager.get_project_plan(231)

        assert plan is not None
        assert plan["phase_detection_error"] == "No commits found"
