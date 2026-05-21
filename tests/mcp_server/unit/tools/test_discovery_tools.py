# tests/mcp_server/unit/tools/test_discovery_tools.py
# pyright: reportPrivateUsage=false
"""
Tests for Discovery Tools (search_documentation, get_work_context).

@layer: Tests (Unit)
@dependencies: [pytest, tempfile, unittest.mock, mcp_server.tools.discovery_tools]
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

import mcp_server.tools.discovery_tools as discovery_module
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
from mcp_server.core.interfaces import IContextLoadedWriter
from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.state_repository import StateBranchMismatchError, StateNotFoundError
from mcp_server.state.workflow_status import WorkflowStatusDTO
from mcp_server.tools.discovery_tools import (
    GetWorkContextInput,
    GetWorkContextTool,
    SearchDocumentationInput,
    SearchDocumentationTool,
)
from tests.mcp_server.test_support import make_phase_state_engine, make_project_manager


def make_settings(workspace_root: Path | str = ".", github_token: str | None = None) -> Settings:
    """Create explicit settings for discovery tool tests."""
    return Settings(
        server={"workspace_root": str(workspace_root)},
        github={"token": github_token},
    )


def make_work_context_tool(
    workspace_root: Path | str = ".",
    github_token: str | None = None,
    contracts_config: ContractsConfig | None = None,
    context_loaded_writer: IContextLoadedWriter | None = None,
) -> GetWorkContextTool:
    settings = make_settings(workspace_root=workspace_root, github_token=github_token)
    return GetWorkContextTool(
        settings=settings,
        git_manager=MagicMock(),
        project_manager=MagicMock(),
        state_engine=MagicMock(),
        github_manager=MagicMock(),
        workphases_config=load_workphases_config(),
        workflow_status_resolver=MagicMock(),
        contracts_config=contracts_config,
        context_loaded_writer=context_loaded_writer,
    )


def load_workflow_config() -> WorkflowConfig:
    return ConfigLoader(Path(".phase-gate/config")).load_workflow_config()


def load_git_config() -> GitConfig:
    return ConfigLoader(Path(".phase-gate/config")).load_git_config()


def load_workphases_config() -> WorkphasesConfig:
    return ConfigLoader(Path(".phase-gate/config")).load_workphases_config()


def load_contracts_config() -> ContractsConfig:
    return ConfigLoader(Path(".phase-gate/config")).load_contracts_config()


class TestSearchDocumentationTool:
    """Tests for SearchDocumentationTool."""

    @pytest.fixture()
    def tool(self) -> SearchDocumentationTool:
        """Fixture to instantiate SearchDocumentationTool."""
        return SearchDocumentationTool(settings=make_settings())

    def test_tool_name(self, tool: SearchDocumentationTool) -> None:
        """Should have correct tool name."""
        assert tool.name == "search_documentation"

    def test_tool_description(self, tool: SearchDocumentationTool) -> None:
        """Should have a non-empty description."""
        assert tool.description
        assert len(tool.description) > 0

    def test_tool_schema_has_query(self, tool: SearchDocumentationTool) -> None:  # noqa: ARG002
        """Should require query parameter."""
        with pytest.raises(ValidationError):
            SearchDocumentationInput()  # Missing required query

    def test_tool_schema_has_scope(self, tool: SearchDocumentationTool) -> None:  # noqa: ARG002
        """Should have scope with default value."""
        result = SearchDocumentationInput(query="test")
        assert result.scope == "all"

    @pytest.mark.asyncio
    async def test_search_returns_results(self, tool: SearchDocumentationTool) -> None:
        """Should return search results with snippets."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create mock docs directory
            docs_dir = Path(tmpdir) / "docs"
            docs_dir.mkdir()

            test_file = docs_dir / "test.md"
            test_file.write_text("# Test Document\nContains worker implementation info.")

            tool._settings.server.workspace_root = tmpdir
            result = await tool.execute(SearchDocumentationInput(query="worker"), NoteContext())

            assert not result.is_error
            assert "test.md" in result.content[0]["text"]

    @pytest.mark.asyncio
    async def test_search_with_scope(self, tool: SearchDocumentationTool) -> None:
        """Should filter by scope."""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_dir = Path(tmpdir) / "docs"
            (docs_dir / "architecture").mkdir(parents=True)

            test_file = docs_dir / "architecture" / "design.md"
            test_file.write_text("# Architecture Design")

            tool._settings.server.workspace_root = tmpdir
            result = await tool.execute(
                SearchDocumentationInput(query="design", scope="architecture"), NoteContext()
            )

            assert not result.is_error

    @pytest.mark.asyncio
    async def test_search_empty_results(self, tool: SearchDocumentationTool) -> None:
        """Should handle no results gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_dir = Path(tmpdir) / "docs"
            docs_dir.mkdir()

            test_file = docs_dir / "test.md"
            test_file.write_text("# Test")

            tool._settings.server.workspace_root = tmpdir
            result = await tool.execute(
                SearchDocumentationInput(query="nonexistent123"), NoteContext()
            )

            assert not result.is_error
            assert "No results" in result.content[0]["text"]


class TestGetWorkContextTool:
    """Tests for GetWorkContextTool."""

    @pytest.fixture()
    def tool(self) -> GetWorkContextTool:
        """Fixture to instantiate GetWorkContextTool."""
        return make_work_context_tool()

    def test_tool_name(self, tool: GetWorkContextTool) -> None:
        """Should have correct tool name."""
        assert tool.name == "get_work_context"

    def test_tool_description(self, tool: GetWorkContextTool) -> None:
        """Should have a non-empty description containing 'workflow phase'."""
        assert tool.description
        assert "workflow phase" in tool.description.lower()

    def test_tool_schema_has_include_closed(self, tool: GetWorkContextTool) -> None:  # noqa: ARG002
        """include_closed_recent removed in C1 (issue #268); model still constructs OK."""
        result = GetWorkContextInput()
        assert not hasattr(result, "include_closed_recent")

    @pytest.mark.asyncio
    async def test_get_context_returns_branch_info(self, tool: GetWorkContextTool) -> None:
        """Should return branch information."""
        with patch("mcp_server.tools.discovery_tools.GitManager") as mock_git_class:
            mock_git = MagicMock()
            mock_git.get_current_branch.return_value = "main"
            mock_git.get_recent_commits.return_value = []
            mock_git_class.return_value = mock_git
            tool._git_manager = mock_git

            tool._settings.github.token = None
            result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        assert "main" in result.content[0]["text"]

    @pytest.mark.asyncio
    async def test_get_context_extracts_issue_number(self, tool: GetWorkContextTool) -> None:
        """Issue number comes from BranchState after C1 (issue #268)."""
        tool._state_engine.get_state.return_value.issue_number = 42  # pyright: ignore[reportPrivateUsage]
        mock_git = MagicMock()
        mock_git.get_current_branch.return_value = "feature/42-implement-dto"
        tool._git_manager = mock_git  # pyright: ignore[reportPrivateUsage]
        tool._settings.github.token = None  # pyright: ignore[reportPrivateUsage]

        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        assert "#42" in result.content[0]["text"]

    @pytest.mark.asyncio
    async def test_get_context_extracts_issue_number_alternate_format(
        self, tool: GetWorkContextTool
    ) -> None:
        """Issue number from BranchState for fix/ branches after C1 (issue #268)."""
        tool._state_engine.get_state.return_value.issue_number = 99  # pyright: ignore[reportPrivateUsage]
        mock_git = MagicMock()
        mock_git.get_current_branch.return_value = "fix/99-bug"
        tool._git_manager = mock_git  # pyright: ignore[reportPrivateUsage]
        tool._settings.github.token = None  # pyright: ignore[reportPrivateUsage]

        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        assert "#99" in result.content[0]["text"]

    @pytest.mark.asyncio
    async def test_get_context_detects_workflow_phase_from_commit_scope(
        self, tool: GetWorkContextTool
    ) -> None:
        """Phase and sub-phase come from BranchState after C1 (issue #268)."""
        tool._state_engine.get_state.return_value.current_phase = "implementation"  # pyright: ignore[reportPrivateUsage]
        tool._state_engine.get_state.return_value.current_sub_phase = "red"  # pyright: ignore[reportPrivateUsage]
        tool._state_engine.get_state.return_value.workflow_name = "feature"  # pyright: ignore[reportPrivateUsage]
        mock_git = MagicMock()
        mock_git.get_current_branch.return_value = "feature/42-dto"
        tool._git_manager = mock_git  # pyright: ignore[reportPrivateUsage]
        tool._settings.github.token = None  # pyright: ignore[reportPrivateUsage]

        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        text = result.content[0]["text"].lower()
        assert "implementation" in text
        assert "red" in text or "🔴" in result.content[0]["text"]

    @pytest.mark.asyncio
    async def test_detect_workflow_phase_variations(self, tool: GetWorkContextTool) -> None:
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

        mock_git = MagicMock()
        mock_git.get_current_branch.return_value = "main"
        tool._git_manager = mock_git  # pyright: ignore[reportPrivateUsage]
        tool._settings.github.token = None  # pyright: ignore[reportPrivateUsage]

        for expected_phase, expected_emoji in test_cases:
            tool._state_engine.get_state.return_value.current_phase = expected_phase  # pyright: ignore[reportPrivateUsage]
            tool._state_engine.get_state.return_value.workflow_name = "feature"  # pyright: ignore[reportPrivateUsage]
            result = await tool.execute(GetWorkContextInput(), NoteContext())
            text = result.content[0]["text"].lower()
            assert expected_phase in text or expected_emoji in result.content[0]["text"]

    @pytest.mark.asyncio
    async def test_get_context_with_github_integration(self, tool: GetWorkContextTool) -> None:
        """Should handle GitHub integration gracefully (error case)."""
        mock_git = MagicMock()
        mock_git.get_current_branch.return_value = "feature/42-implement-dto"
        mock_git.get_recent_commits.return_value = []
        tool._git_manager = mock_git
        mock_github_manager = tool._github_manager
        assert mock_github_manager is not None
        mock_github_manager.get_issue.side_effect = RuntimeError("GitHub unavailable")

        tool._settings.github.token = "test-token"

        # Execute - GitHub code path will fail gracefully
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        # Should not error even if GitHub fetch fails
        assert not result.is_error

    @pytest.mark.asyncio
    async def test_get_context_github_success(self, tool: GetWorkContextTool) -> None:
        """GitHub block removed in C1 (issue #268); tool completes successfully."""
        mock_git = MagicMock()
        mock_git.get_current_branch.return_value = "feature/42-test"
        tool._git_manager = mock_git  # pyright: ignore[reportPrivateUsage]
        tool._settings.github.token = "test-token"  # pyright: ignore[reportPrivateUsage]

        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        # GitHub issue title no longer included in output after C1
        assert "Test Issue" not in result.content[0]["text"]

    @pytest.mark.asyncio
    async def test_get_context_shows_error_message_when_phase_unknown(
        self, tool: GetWorkContextTool
    ) -> None:
        """When state engine fails, output shows unknown confidence (no error raised)."""
        tool._state_engine.get_state.side_effect = OSError("state.json missing")  # pyright: ignore[reportPrivateUsage]
        mock_git = MagicMock()
        mock_git.get_current_branch.return_value = "main"
        tool._git_manager = mock_git  # pyright: ignore[reportPrivateUsage]
        tool._settings.github.token = None  # pyright: ignore[reportPrivateUsage]

        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        text = result.content[0]["text"]
        # Graceful fallback: phase_confidence=unknown → ⚠️ message or ❓ emoji
        assert "unknown" in text.lower() or "❓" in text


class TestGetWorkContextTddCycleInfo:
    """Tests for TDD cycle info in get_work_context.

    Issue #146 Cycle 3: Conditional visibility of tdd_cycle_info.
    """

    @pytest.fixture()
    def tool(self) -> GetWorkContextTool:
        """Fixture to instantiate GetWorkContextTool."""
        return make_work_context_tool()

    @pytest.mark.asyncio
    async def test_tdd_cycle_info_shown_during_tdd_phase(
        self, tool: GetWorkContextTool, tmp_path: Path
    ) -> None:
        """Test that tdd_cycle_info appears when in TDD phase.

        Issue #146 Cycle 3: Conditional visibility based on workflow_phase.
        """
        workspace_root = tmp_path

        # Create minimal project structure
        project_manager = make_project_manager(workspace_root)
        state_engine = make_phase_state_engine(workspace_root, project_manager=project_manager)

        # Initialize project
        project_manager.initialize_project(
            issue_number=146, issue_title="TDD Cycle Tracking", workflow_name="feature"
        )

        # Save planning deliverables with total=2 (matching 2 cycles)
        planning_deliverables = {
            "tdd_cycles": {
                "total": 2,
                "cycles": [
                    {
                        "cycle_number": 1,
                        "name": " & Storage",
                        "deliverables": ["ProjectManager schema"],
                        "exit_criteria": "Schema validated",
                    },
                    {
                        "cycle_number": 2,
                        "name": "Validation Logic",
                        "deliverables": ["Cycle validation"],
                        "exit_criteria": "All validation covered",
                    },
                ],
            }
        }
        project_manager.save_planning_deliverables(146, planning_deliverables)

        # Set implementation phase with current cycle = 2
        state_engine.initialize_branch(
            branch="feature/146-tdd-cycle-tracking",
            issue_number=146,
            initial_phase="implementation",
        )
        state = state_engine.get_state("feature/146-tdd-cycle-tracking")
        state = state.with_updates(current_cycle=2)
        state_engine._save_state("feature/146-tdd-cycle-tracking", state)

        # Mock Git and settings
        with (
            patch("mcp_server.tools.discovery_tools.GitManager") as mock_git_class,
        ):
            mock_git = MagicMock()
            mock_git.get_current_branch.return_value = "feature/146-tdd-cycle-tracking"
            # Provide implementation-scoped commit so ScopeDecoder has context
            mock_git.get_recent_commits.return_value = [
                "test(P_IMPLEMENTATION_SP_C2_GREEN): add cycle info display"
            ]
            mock_git_class.return_value = mock_git
            tool._git_manager = mock_git

            tool._settings.github.token = None
            tool._project_manager = project_manager
            tool._state_engine = state_engine
            tool._settings.server.workspace_root = str(workspace_root)

            # Configure resolver to match expected phase/cycle for TDD info visibility
            tool._workflow_status_resolver.resolve_current.return_value = WorkflowStatusDTO(  # pyright: ignore[reportPrivateUsage]
                current_phase="implementation",
                sub_phase="green",
                current_cycle=2,
                phase_source="state.json",
                phase_confidence="high",
                phase_detection_error=None,
            )

            result = await tool.execute(GetWorkContextInput(), NoteContext())

        # Assert - after C1 (issue #268) TDD cycle info removed from output
        assert not result.is_error, f"Expected success, got error: {result.content}"
        text = result.content[0]["text"]
        # TDD cycle noise block removed in C1 (issue #268)
        assert "TDD Cycle" not in text, f"Unexpected cycle info in output after C1: {text}"

    @pytest.mark.asyncio
    async def test_tdd_cycle_info_hidden_outside_tdd_phase(
        self, tool: GetWorkContextTool, tmp_path: Path
    ) -> None:
        """Test that tdd_cycle_info is hidden when NOT in TDD phase.

        Issue #146 Cycle 3: Conditional visibility - no noise outside TDD.
        """
        workspace_root = tmp_path

        # Create minimal project structure
        project_manager = make_project_manager(workspace_root)
        state_engine = make_phase_state_engine(workspace_root, project_manager=project_manager)

        # Initialize project
        project_manager.initialize_project(
            issue_number=146, issue_title="TDD Cycle Tracking", workflow_name="feature"
        )

        # Save planning deliverables
        planning_deliverables = {
            "tdd_cycles": {
                "total": 1,
                "cycles": [
                    {
                        "cycle_number": 1,
                        "name": "Schema & Storage",
                        "deliverables": ["ProjectManager schema"],
                        "exit_criteria": "Tests pass",
                    }
                ],
            }
        }
        project_manager.save_planning_deliverables(146, planning_deliverables)

        # Set DESIGN phase (not TDD)
        state_engine.initialize_branch(
            branch="feature/146-tdd-cycle-tracking", issue_number=146, initial_phase="design"
        )

        # Mock Git
        with (
            patch("mcp_server.tools.discovery_tools.GitManager") as mock_git_class,
        ):
            mock_git = MagicMock()
            mock_git.get_current_branch.return_value = "feature/146-tdd-cycle-tracking"
            mock_git.get_recent_commits.return_value = [
                "test(P_IMPLEMENTATION_SP_C1_RED): graceful degradation path"
            ]
            mock_git_class.return_value = mock_git
            tool._git_manager = mock_git

            tool._settings.github.token = None
            tool._project_manager = project_manager
            tool._state_engine = state_engine
            tool._settings.server.workspace_root = str(workspace_root)

            result = await tool.execute(GetWorkContextInput(), NoteContext())

        # Assert - NO tdd_cycle_info in design phase
        assert not result.is_error
        text = result.content[0]["text"]
        # Should NOT mention TDD cycle info or cycle names
        assert "TDD Cycle" not in text, f"Expected NO cycle info in design phase: {text}"
        assert "Validation Logic" not in text, f"Expected NO cycle name in design phase: {text}"

    @pytest.mark.asyncio
    async def test_tdd_cycle_info_graceful_degradation(
        self, tool: GetWorkContextTool, tmp_path: Path
    ) -> None:
        """Test graceful degradation when planning deliverables missing.

        Issue #146 Cycle 3: Avoid crashes if planning_deliverables not saved.
        """
        workspace_root = tmp_path

        # Create minimal project structure WITHOUT planning deliverables
        project_manager = make_project_manager(workspace_root)
        state_engine = make_phase_state_engine(workspace_root, project_manager=project_manager)

        # Initialize project WITHOUT planning deliverables
        project_manager.initialize_project(
            issue_number=146, issue_title="TDD Cycle Tracking", workflow_name="feature"
        )
        # NOTE: Deliberately NOT calling save_planning_deliverables

        # Set implementation phase
        state_engine.initialize_branch(
            branch="feature/146-tdd-cycle-tracking",
            issue_number=146,
            initial_phase="implementation",
        )

        # Mock Git
        with (
            patch("mcp_server.tools.discovery_tools.GitManager") as mock_git_class,
        ):
            mock_git = MagicMock()
            mock_git.get_current_branch.return_value = "feature/146-tdd-cycle-tracking"
            mock_git.get_recent_commits.return_value = [
                "test(P_IMPLEMENTATION_SP_C1_RED): graceful degradation path"
            ]
            mock_git_class.return_value = mock_git
            tool._git_manager = mock_git

            tool._settings.github.token = None
            tool._project_manager = project_manager
            tool._state_engine = state_engine
            tool._settings.server.workspace_root = str(workspace_root)

            result = await tool.execute(GetWorkContextInput(), NoteContext())

        # Assert - tool should NOT crash
        assert not result.is_error, f"Tool crashed: {result.content}"
        text = result.content[0]["text"]
        # Should show implementation phase
        assert "implementation" in text.lower() or "🔴" in text or "🟢" in text


class TestTddCycleInfoStatusField:
    """Tests for the status field in tdd_cycle_info (Issue #146 Cycle 7 D2).

    design.md:365-376 specifies tdd_cycle_info must include status='in_progress'.
    discovery_tools.py:168-175 did not include this field.
    """

    @pytest.fixture()
    def tool(self) -> GetWorkContextTool:
        """Fixture to instantiate GetWorkContextTool."""
        return make_work_context_tool()

    @pytest.mark.asyncio
    async def test_tdd_cycle_info_includes_status_field(
        self, tool: GetWorkContextTool, tmp_path: Path
    ) -> None:
        """tdd_cycle_info must include status='in_progress' per design.md:375.

        Issue #146 Cycle 7 D2: Align implementation with design spec.
        The status field is always 'in_progress' when the cycle is active.
        """
        workspace_root = tmp_path
        project_manager = make_project_manager(workspace_root)
        state_engine = make_phase_state_engine(workspace_root, project_manager=project_manager)

        project_manager.initialize_project(
            issue_number=146, issue_title="TDD Cycle Tracking", workflow_name="feature"
        )

        planning_deliverables = {
            "tdd_cycles": {
                "total": 1,
                "cycles": [
                    {
                        "cycle_number": 1,
                        "name": "Status Field Test",
                        "deliverables": ["Add status field"],
                        "exit_criteria": "Status field present in output",
                    }
                ],
            }
        }
        project_manager.save_planning_deliverables(146, planning_deliverables)

        state_engine.initialize_branch(
            branch="feature/146-tdd-cycle-tracking",
            issue_number=146,
            initial_phase="implementation",
        )
        # Set current cycle so tdd_cycle_info is populated
        state = state_engine.get_state("feature/146-tdd-cycle-tracking")
        state = state.with_updates(current_cycle=1)
        state_engine._save_state("feature/146-tdd-cycle-tracking", state)

        with (
            patch("mcp_server.tools.discovery_tools.GitManager") as mock_git_class,
        ):
            mock_git = MagicMock()
            mock_git.get_current_branch.return_value = "feature/146-tdd-cycle-tracking"
            # Provide a non-empty commits list so ScopeDecoder is invoked (not short-circuited)
            mock_git.get_recent_commits.return_value = [
                "test(P_IMPLEMENTATION_SP_C1_RED): add status field test"
            ]
            mock_git_class.return_value = mock_git
            tool._git_manager = mock_git

            tool._settings.github.token = None
            tool._project_manager = project_manager
            tool._state_engine = state_engine
            tool._settings.server.workspace_root = str(workspace_root)

            # Configure resolver to provide implementation phase with cycle 1
            tool._workflow_status_resolver.resolve_current.return_value = WorkflowStatusDTO(
                current_phase="implementation",
                sub_phase="red",
                current_cycle=1,
                phase_source="state.json",
                phase_confidence="high",
                phase_detection_error=None,
            )

            result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error, f"Tool failed: {result.content}"
        # TDD cycle status removed from output in C1 (issue #268)
        text = result.content[0]["text"]
        assert "in_progress" not in text, f"Unexpected tdd_cycle_info in output after C1: {text}"


class TestGetWorkContextResolverAdoption:
    """C4: WorkflowStatusResolver adoption in GetWorkContextTool.execute().

    Issue #231: These tests FAIL (RED) until WorkflowStatusResolver is added as
    a constructor parameter and used in execute() instead of local phase detection.
    """

    @pytest.mark.asyncio
    async def test_execute_calls_resolver_when_injected(self) -> None:
        """GetWorkContextTool calls resolver.resolve_current() when resolver is injected."""
        resolver = MagicMock()
        resolver.resolve_current.return_value = WorkflowStatusDTO(
            current_phase="design",
            sub_phase=None,
            current_cycle=None,
            phase_source="state.json",
            phase_confidence="high",
            phase_detection_error=None,
        )
        settings = make_settings()
        settings.github.token = None
        mock_git = MagicMock()
        mock_git.get_current_branch.return_value = "feature/99-test"

        tool = GetWorkContextTool(
            settings=settings,
            git_manager=mock_git,
            project_manager=MagicMock(),
            state_engine=MagicMock(),
            workflow_status_resolver=resolver,
        )
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        # C1: resolver no longer called; execute() reads BranchState directly
        assert "Branch:" in result.content[0]["text"]

    @pytest.mark.asyncio
    async def test_execute_gates_cycle_enrichment_on_current_cycle_not_none(self) -> None:
        """Cycle enrichment gated on current_cycle is not None, not phase string equality."""
        resolver = MagicMock()
        resolver.resolve_current.return_value = WorkflowStatusDTO(
            current_phase="implementation",
            sub_phase="red",
            current_cycle=None,  # Gate: no cycle → no enrichment
            phase_source="state.json",
            phase_confidence="high",
            phase_detection_error=None,
        )
        settings = make_settings()
        settings.github.token = None
        mock_git = MagicMock()
        mock_git.get_current_branch.return_value = "feature/99-test"

        tool = GetWorkContextTool(
            settings=settings,
            git_manager=mock_git,
            project_manager=MagicMock(),
            state_engine=MagicMock(),
            workflow_status_resolver=resolver,
        )
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        assert "TDD Cycle" not in result.content[0]["text"]

    @pytest.mark.asyncio
    async def test_execute_shows_phase_from_resolver(self) -> None:
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

        assert not result.is_error
        assert "research" in result.content[0]["text"].lower()


# ---------------------------------------------------------------------------
# C6 RED — GetWorkContextTool StateNotFoundError / StateBranchMismatchError (issue #298)
# ---------------------------------------------------------------------------


def _make_work_context_tool(
    tmp_path: Path,
    resolver_side_effect: Exception,
) -> GetWorkContextTool:
    """Return a GetWorkContextTool whose resolver raises the given exception."""
    mock_git = MagicMock()
    mock_git.get_current_branch.return_value = "feature/298-test"

    mock_resolver = MagicMock()
    mock_resolver.resolve_current.side_effect = resolver_side_effect

    settings = make_settings(tmp_path)

    return GetWorkContextTool(
        settings=settings,
        git_manager=mock_git,
        project_manager=MagicMock(),
        state_engine=MagicMock(),
        workflow_status_resolver=mock_resolver,
    )


class TestGetWorkContextStateErrors:
    """C6 (issue #298): StateNotFoundError / StateBranchMismatchError → error + RecoveryNote."""

    @pytest.mark.asyncio
    async def test_get_work_context_returns_error_with_recovery_note_when_state_absent(
        self, tmp_path: Path
    ) -> None:
        """StateNotFoundError from state_engine → graceful degradation (not error) after C1."""
        tool = _make_work_context_tool(
            tmp_path, resolver_side_effect=StateNotFoundError("feature/298-test")
        )
        ctx = NoteContext()
        result = await tool.execute(GetWorkContextInput(), ctx)

        # C1 (issue #268): graceful degradation path; state errors no longer hard-fail
        assert not result.is_error

    @pytest.mark.asyncio
    async def test_get_work_context_returns_error_with_recovery_note_on_mismatch(
        self, tmp_path: Path
    ) -> None:
        """StateBranchMismatchError from state_engine → graceful degradation after C1."""
        tool = _make_work_context_tool(
            tmp_path, resolver_side_effect=StateBranchMismatchError("branch mismatch")
        )
        ctx = NoteContext()
        result = await tool.execute(GetWorkContextInput(), ctx)

        # C1 (issue #268): graceful degradation path; state errors no longer hard-fail
        assert not result.is_error

    @pytest.mark.asyncio
    async def test_get_work_context_graceful_io_error_path_unchanged(self, tmp_path: Path) -> None:
        """OSError in resolver still uses existing graceful fallback (not error result)."""
        tool = _make_work_context_tool(tmp_path, resolver_side_effect=OSError("disk error"))
        ctx = NoteContext()
        result = await tool.execute(GetWorkContextInput(), ctx)

        assert not result.is_error  # OSError → graceful degradation, not hard error


# ---------------------------------------------------------------------------
# C1 RED — GetWorkContextTool sub_role_hint + phase_instructions (issue #268)
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
        tool = self._make_tool(phase="implementation")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        text = result.content[0]["text"]
        # C1: "Role: implementer" in compact orientation header
        assert "Role: implementer" in text

    @pytest.mark.asyncio
    async def test_get_work_context_returns_phase_instructions_for_feature_implementation(
        self,
    ) -> None:
        """phase_instructions must be non-empty for (feature, implementation)."""
        tool = self._make_tool(phase="implementation")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        text = result.content[0]["text"]
        # C1: phase instructions appear in "### 🎯 Phase Instructions" block
        assert "Phase Instructions" in text
        # Instructions must mention the core TDD tools agents should call
        assert "get_project_plan" in text
        assert "run_tests" in text

    @pytest.mark.asyncio
    async def test_get_work_context_returns_empty_string_for_unknown_workflow_phase(
        self,
    ) -> None:
        """Unknown (workflow, phase) combo must return empty string, never KeyError."""
        tool = self._make_tool(phase="nonexistent_phase_xyz")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        # No crash; output shows "No instructions defined" for unknown combo
        text = result.content[0]["text"]
        assert "No instructions defined" in text or "❓" in text

    @pytest.mark.asyncio
    async def test_get_work_context_returns_empty_string_when_workflow_unavailable(
        self,
    ) -> None:
        """Graceful fallback when workflow resolution raises (OSError path)."""
        mock_git = MagicMock()
        mock_git.get_current_branch.return_value = "feature/268-test"
        resolver = MagicMock()
        resolver.resolve_current.side_effect = OSError("state.json missing")
        settings = make_settings()
        settings.github.token = None
        tool = GetWorkContextTool(
            settings=settings,
            git_manager=mock_git,
            project_manager=MagicMock(),
            state_engine=MagicMock(),
            workflow_status_resolver=resolver,
        )

        # OSError path uses graceful fallback — not an error result
        result = await tool.execute(GetWorkContextInput(), NoteContext())
        assert not result.is_error

    # --- C1 correction: bug workflow entries ---

    @pytest.mark.asyncio
    async def test_get_work_context_returns_phase_instructions_for_bug_research(
        self,
    ) -> None:
        """phase_instructions for (bug, research) must contain key research actions."""
        tool = self._make_tool(phase="research", workflow_name="bug")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        text = result.content[0]["text"]
        # C1: phase instructions appear in "### 🎯 Phase Instructions" block
        assert "Phase Instructions" in text
        assert "get_issue" in text  # bug research always starts with reading the issue
        assert "root cause" in text.lower()  # must identify root cause

    @pytest.mark.asyncio
    async def test_get_work_context_returns_phase_instructions_for_bug_implementation(
        self,
    ) -> None:
        """phase_instructions for (bug, implementation) must contain TDD hard rules."""
        tool = self._make_tool(phase="implementation", workflow_name="bug")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        text = result.content[0]["text"]
        # C1: phase instructions appear in "### 🎯 Phase Instructions" block
        assert "Phase Instructions" in text
        assert "RED" in text  # TDD RED phase required
        assert "get_project_plan" in text  # always read deliverables first


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

    def test_get_work_context_input_has_no_include_closed_recent(self) -> None:
        """GetWorkContextInput must reject include_closed_recent (field removed in C1)."""
        with pytest.raises(ValidationError):
            GetWorkContextInput(include_closed_recent=True)  # type: ignore[call-arg]

    @pytest.mark.asyncio
    async def test_get_work_context_returns_sub_role_hint_for_known_phase(self) -> None:
        """New format: orientation header shows 'Role: implementer' for implementation phase."""
        tool = self._make_tool(current_phase="implementation")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        assert "Role: implementer" in result.content[0]["text"]

    @pytest.mark.asyncio
    async def test_get_work_context_returns_phase_instructions_for_feature_implementation(
        self,
    ) -> None:
        """New format: phase_instructions rendered under '### \U0001f3af Phase Instructions'."""
        tool = self._make_tool(workflow_name="feature", current_phase="implementation")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        text = result.content[0]["text"]
        assert "### \U0001f3af Phase Instructions" in text
        assert "get_project_plan" in text

    @pytest.mark.asyncio
    async def test_get_work_context_returns_empty_string_for_unknown_workflow_phase(
        self,
    ) -> None:
        """Unknown (workflow, phase): no crash; fallback message shown under instruction header."""
        tool = self._make_tool(workflow_name="unknownwf", current_phase="unknownphase")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        text = result.content[0]["text"]
        assert "### \U0001f3af Phase Instructions" in text
        assert "No instructions defined" in text

    @pytest.mark.asyncio
    async def test_get_work_context_returns_workflow_name_from_branch_state(self) -> None:
        """Orientation header must contain 'Workflow: feature' sourced from BranchState."""
        tool = self._make_tool(workflow_name="feature")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        assert "Workflow: feature" in result.content[0]["text"]

    @pytest.mark.asyncio
    async def test_get_work_context_returns_issue_number_from_branch_state(self) -> None:
        """Orientation header shows issue #268 from BranchState, not branch-name regex."""
        # Branch name has no number → old regex gives None; BranchState.issue_number=268
        tool = self._make_tool(branch="feature/no-number-in-name", issue_number=268)
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        assert "Issue: #268" in result.content[0]["text"]

    @pytest.mark.asyncio
    async def test_get_work_context_returns_parent_branch_from_branch_state(self) -> None:
        """Orientation header must show 'Parent: main' from BranchState.parent_branch."""
        tool = self._make_tool(parent_branch="main")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        assert "Parent: main" in result.content[0]["text"]

    @pytest.mark.asyncio
    async def test_get_work_context_omits_noise_fields(self) -> None:
        """Active issue, recent commits, and TDD cycle info must not appear in C1 output."""
        mock_issue = MagicMock()
        mock_issue.number = 268
        mock_issue.title = "Test Issue"
        mock_issue.body = ""
        mock_issue.labels = []

        tool = self._make_tool(github_token="test-token", github_issue=mock_issue)
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        text = result.content[0]["text"]
        assert "### Active Issue:" not in text
        assert "Recent Commits:" not in text
        assert "TDD Cycle" not in text

    @pytest.mark.asyncio
    async def test_get_work_context_phase_instructions_is_dominant_first_block(self) -> None:
        """'### \U0001f3af Phase Instructions' must be the first ### header in the output."""
        tool = self._make_tool(workflow_name="feature", current_phase="implementation")
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        text = result.content[0]["text"]
        assert "### \U0001f3af Phase Instructions" in text, f"Header not found in output:\n{text}"
        first_h3 = text.find("###")
        phase_instructions_pos = text.find("### \U0001f3af Phase Instructions")
        assert first_h3 == phase_instructions_pos, (
            f"'### \U0001f3af Phase Instructions' is not the first ### header.\nText:\n{text}"
        )

    @pytest.mark.asyncio
    async def test_get_work_context_graceful_degradation_when_state_unavailable(self) -> None:
        """No error result when state is unavailable (bootstrap degradation)."""
        # state_engine.get_state raises → new code: graceful; old code path: via resolver
        tool = self._make_tool(state_raises=StateNotFoundError("feature/268-test"))
        # Also make resolver raise → triggers old-code ToolResult.error (the RED proof)
        tool._workflow_status_resolver.resolve_current.side_effect = StateNotFoundError(
            "feature/268-test"
        )

        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error, (
            f"Expected graceful degradation, got error.\nContent: {result.content}"
        )
        assert "feature/268-test" in result.content[0]["text"]


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
                phases=[
                    WorkflowPhaseEntry(
                        name=phase,
                        instructions=PhaseInstructionsSpec(
                            sub_role=sub_role,
                            phase_instructions=phase_instructions,
                            handover_template=handover_template,
                        ),
                    ),
                    WorkflowPhaseEntry(
                        name="ready",
                        instructions=PhaseInstructionsSpec(
                            sub_role="documenter",
                            phase_instructions="Create PR.",
                            handover_template=None,
                        ),
                    ),
                ]
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

    def test_sub_role_map_removed_from_module(self) -> None:
        assert not hasattr(discovery_module, "_SUB_ROLE_MAP")

    def test_phase_instructions_map_removed_from_module(self) -> None:
        assert not hasattr(discovery_module, "_PHASE_INSTRUCTIONS_MAP")

    @pytest.mark.asyncio
    async def test_sub_role_comes_from_contracts(self) -> None:
        """sub_role_hint must come from ContractsConfig, not hardcoded maps."""
        contracts = _make_c7_contracts(sub_role="implementer-c7")
        tool = self._make_c7_tool(contracts_config=contracts)
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        text = result.content[0]["text"]
        assert "implementer-c7" in text

    @pytest.mark.asyncio
    async def test_phase_instructions_come_from_contracts(self) -> None:
        """phase_instructions must come from ContractsConfig, not hardcoded maps."""
        contracts = _make_c7_contracts(
            phase_instructions="Do TDD. Call get_project_plan.",
        )
        tool = self._make_c7_tool(contracts_config=contracts)
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        text = result.content[0]["text"]
        assert "Do TDD. Call get_project_plan." in text

    @pytest.mark.asyncio
    async def test_handover_template_in_response(self) -> None:
        """Hand-over template must appear in response when contracts provide one."""
        contracts = _make_c7_contracts(handover_template="## Hand-over\nScope: ...")
        tool = self._make_c7_tool(contracts_config=contracts)
        result = await tool.execute(GetWorkContextInput(), NoteContext())

        assert not result.is_error
        text = result.content[0]["text"]
        assert "### Hand-over Template" in text
        assert "## Hand-over" in text

    @pytest.mark.asyncio
    async def test_context_loaded_writer_called_on_success(self) -> None:
        """IContextLoadedWriter.set_context_loaded must be called after successful execute."""
        writer = MagicMock(spec=IContextLoadedWriter)
        tool = self._make_c7_tool(context_loaded_writer=writer)
        await tool.execute(GetWorkContextInput(), NoteContext())

        writer.set_context_loaded.assert_called_once_with("feature/42-test", value=True)
