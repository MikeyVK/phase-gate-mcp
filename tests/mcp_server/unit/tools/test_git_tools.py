"""Unit tests for git_tools.py.

@layer: Tests (Unit)
@dependencies: [pytest, pathlib, mcp_server.tools.git_tools]
"""

from pathlib import Path
from unittest.mock import ANY, MagicMock

import pytest
from pydantic import ValidationError

from mcp_server.adapters.git_adapter import GitAdapter
from mcp_server.config.loader import ConfigLoader
from mcp_server.core.exceptions import ExecutionError
from mcp_server.core.interfaces import IContextLoadedWriter
from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.git_manager import BranchDeleteResult, GitManager
from mcp_server.managers.state_repository import StateBranchMismatchError
from mcp_server.tools.git_tools import (
    CheckMergeInput,
    CheckMergeTool,
    CommitPhaseMismatchError,
    CreateBranchInput,
    CreateBranchTool,
    GetParentBranchInput,
    GetParentBranchTool,
    GitCheckoutInput,
    GitCheckoutTool,
    GitCommitInput,
    GitCommitTool,
    GitDeleteBranchInput,
    GitDeleteBranchTool,
    GitMergeInput,
    GitMergeTool,
    GitPushInput,
    GitPushTool,
    GitRestoreInput,
    GitRestoreTool,
    GitStashInput,
    GitStashTool,
    GitStatusInput,
    GitStatusTool,
)
from mcp_server.tools.tool_result import ToolResult


@pytest.fixture
def mock_git_manager() -> MagicMock:
    """Fixture for mocked GitManager."""
    manager = MagicMock()
    git_config = MagicMock()
    git_config.branch_types = ["feature", "bug", "fix", "docs", "refactor", "epic"]
    git_config.commit_types = ["feat", "fix", "docs", "chore", "test", "refactor"]
    git_config.has_branch_type.side_effect = lambda value: value in git_config.branch_types
    git_config.has_commit_type.side_effect = lambda value: value.lower() in git_config.commit_types
    git_config.extract_issue_number.side_effect = lambda branch: 79 if "79" in branch else 999
    manager.git_config = git_config
    manager.adapter.get_current_branch.return_value = "feature/257-reorder-workflow-phases"
    return manager


@pytest.mark.asyncio
async def test_create_branch_tool_requires_base_branch() -> None:
    """Test that base_branch parameter is required."""
    with pytest.raises(Exception):  # noqa: B017 — Pydantic validation error; exact type varies by version
        CreateBranchInput(name="test-branch", branch_type="feature")


@pytest.mark.asyncio
async def test_create_branch_tool_calls_manager_with_explicit_base(
    mock_git_manager: MagicMock,
) -> None:
    """Test that tool passes all parameters including base_branch to manager."""
    tool = CreateBranchTool(manager=mock_git_manager)
    mock_git_manager.create_branch.return_value = "feature/test-branch"

    params = CreateBranchInput(name="test-branch", branch_type="feature", base_branch="HEAD")
    result = await tool.execute(params, NoteContext())

    mock_git_manager.create_branch.assert_called_once_with("test-branch", "feature", "HEAD", ANY)
    assert isinstance(result, ToolResult)
    assert result.content[0]["text"].startswith("✅ ")
    assert "Created branch: feature/test-branch" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_create_branch_tool_with_branch_name_as_base(mock_git_manager: MagicMock) -> None:
    """Test creating branch from another branch name."""
    tool = CreateBranchTool(manager=mock_git_manager)
    mock_git_manager.create_branch.return_value = "fix/new-fix"

    params = CreateBranchInput(
        name="new-fix", branch_type="fix", base_branch="refactor/51-labels-yaml"
    )
    result = await tool.execute(params, NoteContext())

    mock_git_manager.create_branch.assert_called_once_with(
        "new-fix", "fix", "refactor/51-labels-yaml", ANY
    )
    assert "fix/new-fix" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_create_branch_tool_name_changed(mock_git_manager: MagicMock) -> None:
    """Test that tool name is 'create_branch' (not 'create_feature_branch')."""
    tool = CreateBranchTool(manager=mock_git_manager)
    assert tool.name == "create_branch", "Tool should be renamed to create_branch"


@pytest.mark.asyncio
async def test_git_status_tool(mock_git_manager: MagicMock) -> None:
    """Test git status tool."""
    tool = GitStatusTool(manager=mock_git_manager)
    mock_git_manager.get_status.return_value = {
        "branch": "main",
        "is_clean": False,
        "untracked_files": ["foo.py"],
        "modified_files": ["bar.py"],
    }

    result = await tool.execute(GitStatusInput(), NoteContext())

    assert isinstance(result, ToolResult)
    assert "Branch: main" in result.content[0]["text"]
    assert "Untracked: foo.py" in result.content[0]["text"]
    assert "Modified: bar.py" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_git_commit_tool_rejects_legacy_phase_kwarg() -> None:
    """Legacy phase= must be removed from GitCommitInput in cycle 4."""
    with pytest.raises(ValidationError):
        GitCommitInput(phase="red", message="failing test", cycle_number=1)


@pytest.mark.asyncio
async def test_git_commit_tool_docs(mock_git_manager: MagicMock) -> None:
    """Test git commit tool with documentation workflow_phase."""
    tool = GitCommitTool(manager=mock_git_manager)
    mock_git_manager.commit_with_scope.return_value = "doc1234"

    params = GitCommitInput(workflow_phase="documentation", message="update readme")
    result = await tool.execute(params, NoteContext())

    mock_git_manager.commit_with_scope.assert_called_once_with(
        workflow_phase="documentation",
        message="update readme",
        note_context=ANY,
        sub_phase=None,
        cycle_number=None,
        commit_type=None,
        files=None,
        skip_paths=frozenset(),
        issue_number=999,
    )
    assert "Committed: doc1234" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_git_commit_tool_resolves_commit_type_from_phase_contracts(
    mock_git_manager: MagicMock,
) -> None:
    """Implementation commits should pass a resolved commit_type into GitManager."""
    resolver = MagicMock(return_value="refactor")
    tool = GitCommitTool(manager=mock_git_manager, commit_type_resolver=resolver)
    mock_git_manager.commit_with_scope.return_value = "abc1234"
    mock_git_manager.adapter.get_current_branch.return_value = "feature/257-reorder-workflow-phases"

    params = GitCommitInput(
        message="refactor code",
        workflow_phase="implementation",
        sub_phase="refactor",
        cycle_number=4,
    )
    result = await tool.execute(params, NoteContext())

    resolver.assert_called_once_with(
        "feature/257-reorder-workflow-phases",
        "implementation",
        "refactor",
    )
    mock_git_manager.commit_with_scope.assert_called_once_with(
        workflow_phase="implementation",
        message="refactor code",
        note_context=ANY,
        sub_phase="refactor",
        cycle_number=4,
        commit_type="refactor",
        files=None,
        skip_paths=frozenset(),
        issue_number=999,
    )
    assert "Committed: abc1234" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_git_commit_tool_with_workflow_phase(mock_git_manager: MagicMock) -> None:
    """Test git commit tool with workflow_phase parameter (NEW)."""
    tool = GitCommitTool(manager=mock_git_manager)
    mock_git_manager.commit_with_scope.return_value = "wf1234"

    params = GitCommitInput(
        message="complete research",
        workflow_phase="research",
    )
    result = await tool.execute(params, NoteContext())

    mock_git_manager.commit_with_scope.assert_called_once_with(
        workflow_phase="research",
        message="complete research",
        note_context=ANY,
        sub_phase=None,
        cycle_number=None,
        commit_type=None,
        files=None,
        skip_paths=frozenset(),
        issue_number=999,
    )
    assert "Committed: wf1234" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_git_commit_tool_with_workflow_phase_and_subphase(
    mock_git_manager: MagicMock,
) -> None:
    """Test git commit tool with workflow_phase and sub_phase."""
    tool = GitCommitTool(manager=mock_git_manager)
    mock_git_manager.commit_with_scope.return_value = "wf5678"

    params = GitCommitInput(
        message="add failing test",
        workflow_phase="implementation",
        sub_phase="red",
        cycle_number=1,
    )
    result = await tool.execute(params, NoteContext())

    mock_git_manager.commit_with_scope.assert_called_once_with(
        workflow_phase="implementation",
        message="add failing test",
        note_context=ANY,
        sub_phase="red",
        cycle_number=1,
        commit_type=None,
        files=None,
        skip_paths=frozenset(),
        issue_number=999,
    )
    assert "Committed: wf5678" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_git_commit_tool_with_cycle_number(mock_git_manager: MagicMock) -> None:
    """Test git commit tool with cycle_number."""
    tool = GitCommitTool(manager=mock_git_manager)
    mock_git_manager.commit_with_scope.return_value = "wf9012"

    params = GitCommitInput(
        message="implement feature",
        workflow_phase="implementation",
        sub_phase="green",
        cycle_number=1,
    )
    result = await tool.execute(params, NoteContext())

    mock_git_manager.commit_with_scope.assert_called_once_with(
        workflow_phase="implementation",
        message="implement feature",
        note_context=ANY,
        sub_phase="green",
        cycle_number=1,
        commit_type=None,
        files=None,
        skip_paths=frozenset(),
        issue_number=999,
    )
    assert "Committed: wf9012" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_git_commit_tool_with_workflow_phase_and_files(mock_git_manager: MagicMock) -> None:
    """Test git commit tool with workflow_phase and files."""
    tool = GitCommitTool(manager=mock_git_manager)
    mock_git_manager.commit_with_scope.return_value = "wf3456"

    params = GitCommitInput(
        message="refactor code",
        workflow_phase="implementation",
        sub_phase="refactor",
        cycle_number=1,
        files=["src/app.py", "tests/test_app.py"],
    )
    result = await tool.execute(params, NoteContext())

    mock_git_manager.commit_with_scope.assert_called_once_with(
        workflow_phase="implementation",
        message="refactor code",
        note_context=ANY,
        sub_phase="refactor",
        cycle_number=1,
        commit_type=None,
        files=["src/app.py", "tests/test_app.py"],
        skip_paths=frozenset(),
        issue_number=999,
    )
    assert "Committed: wf3456" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_git_commit_tool_backward_compat_with_old_phase(mock_git_manager: MagicMock) -> None:
    """Legacy phase input is rejected instead of being mapped implicitly."""
    del mock_git_manager
    with pytest.raises(ValidationError):
        GitCommitInput(phase="red", message="old style commit", cycle_number=2)


@pytest.mark.asyncio
async def test_git_commit_tool_with_commit_type_override(mock_git_manager: MagicMock) -> None:
    """Test commit_type override parameter."""
    tool = GitCommitTool(manager=mock_git_manager)
    mock_git_manager.commit_with_scope.return_value = "override123"

    params = GitCommitInput(
        workflow_phase="implementation",
        sub_phase="red",
        commit_type="fix",  # Override default 'test'
        message="fix failing test",
        cycle_number=1,
    )
    result = await tool.execute(params, NoteContext())

    # Should pass commit_type to commit_with_scope
    mock_git_manager.commit_with_scope.assert_called_once_with(
        workflow_phase="implementation",
        message="fix failing test",
        note_context=ANY,
        sub_phase="red",
        cycle_number=1,
        commit_type="fix",
        files=None,
        skip_paths=frozenset(),
        issue_number=999,
    )
    assert "Committed: override123" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_git_commit_tool_schema_excludes_invalid_commit_type(
    mock_git_manager: MagicMock,
) -> None:
    """A4 schema: commit_type.enum from git_config does not include unknown types."""
    tool = GitCommitTool(manager=mock_git_manager)
    schema = tool.input_schema
    enum_values = schema["properties"]["commit_type"]["enum"]
    assert "invalid_type" not in enum_values
    assert "feat" in enum_values  # from mock_git_manager fixture


@pytest.mark.asyncio
async def test_git_commit_tool_execute_with_valid_commit_type(mock_git_manager: MagicMock) -> None:
    """Tool executes correctly when commit_type is a valid enum value."""
    tool = GitCommitTool(manager=mock_git_manager)
    mock_git_manager.commit_with_scope.return_value = "case123"

    params = GitCommitInput(
        workflow_phase="implementation",
        sub_phase="red",
        commit_type="feat",
        message="add feature",
        cycle_number=1,
    )

    result = await tool.execute(params, NoteContext())

    mock_git_manager.commit_with_scope.assert_called_once_with(
        workflow_phase="implementation",
        message="add feature",
        note_context=ANY,
        sub_phase="red",
        cycle_number=1,
        commit_type="feat",
        files=None,
        skip_paths=frozenset(),
        issue_number=999,
    )
    assert "Committed: case123" in result.content[0]["text"]


def test_git_commit_input_rejects_missing_cycle_number_for_implementation() -> None:
    """GitCommitInput model_validator rejects workflow_phase=implementation without cycle_number."""
    with pytest.raises(ValidationError, match="cycle_number"):
        GitCommitInput(workflow_phase="implementation", message="test commit")


@pytest.mark.asyncio
async def test_git_commit_integration_workflow_phases() -> None:
    """Integration test: Full commit workflow with real workphases.yaml."""
    # Create a real GitManager with mocked adapter but real workphases config
    mock_adapter = MagicMock()
    mock_adapter.commit.return_value = "integration123"

    loader = ConfigLoader(config_root=Path(".phase-gate/config"))
    git_config = loader.load_git_config()
    workphases_config = loader.load_workphases_config()
    manager = GitManager(
        git_config=git_config,
        adapter=mock_adapter,
        workphases_config=workphases_config,
    )
    resolver = MagicMock(
        side_effect=lambda _branch, workflow_phase, sub_phase: {
            ("implementation", "red"): "test",
            ("implementation", "green"): "feat",
            ("implementation", "refactor"): "refactor",
        }.get((workflow_phase, sub_phase))
    )
    tool = GitCommitTool(manager=manager, commit_type_resolver=resolver)
    manager.adapter.get_current_branch.return_value = "feature/999-e2e-test"

    # Test 1: Research phase (no subphase)
    params1 = GitCommitInput(message="investigate alternatives", workflow_phase="research")
    result1 = await tool.execute(params1, NoteContext())

    assert "Committed: integration123" in result1.content[0]["text"]
    mock_adapter.commit.assert_called_with(
        "docs(P_RESEARCH): investigate alternatives (#999)", files=None, skip_paths=frozenset()
    )

    # Test 2: TDD with subphase
    params2 = GitCommitInput(
        message="add failing test",
        workflow_phase="implementation",
        sub_phase="red",
        cycle_number=1,
    )
    result2 = await tool.execute(params2, NoteContext())

    assert "Committed: integration123" in result2.content[0]["text"]
    mock_adapter.commit.assert_called_with(
        "test(P_IMPLEMENTATION_SP_C1_RED): add failing test (#999)",
        files=None,
        skip_paths=frozenset(),
    )

    # Test 3: Coordination phase (NEW)
    params3 = GitCommitInput(
        message="delegate to child issues",
        workflow_phase="coordination",
        sub_phase="delegation",
    )
    result3 = await tool.execute(params3, NoteContext())

    assert "Committed: integration123" in result3.content[0]["text"]
    mock_adapter.commit.assert_called_with(
        "chore(P_COORDINATION_SP_DELEGATION): delegate to child issues (#999)",
        files=None,
        skip_paths=frozenset(),
    )


@pytest.mark.asyncio
async def test_git_checkout_tool(mock_git_manager: MagicMock) -> None:
    """Test git checkout tool with PhaseStateEngine state sync."""
    # Mock PhaseStateEngine to return state with phase info
    mock_engine = MagicMock()
    mock_state = MagicMock()
    mock_state.current_phase = "implementation"
    mock_state.parent_branch = None
    mock_engine.get_state.return_value = mock_state

    tool = GitCheckoutTool(manager=mock_git_manager, state_engine=mock_engine)
    params = GitCheckoutInput(branch="main")
    result = await tool.execute(params, NoteContext())

    mock_git_manager.checkout.assert_called_once_with("main")
    mock_engine.get_state.assert_called_once_with("main")
    assert "Switched to branch: main" in result.content[0]["text"]
    assert "implementation" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_git_checkout_tool_displays_parent_branch(mock_git_manager: MagicMock) -> None:
    """Test git checkout displays parent_branch when present.

    Issue #79: Show parent_branch in checkout output for context.
    """
    tool = GitCheckoutTool(manager=mock_git_manager)

    # Mock PhaseStateEngine to return state with parent_branch
    mock_engine = MagicMock()
    mock_state = MagicMock()
    mock_state.current_phase = "design"
    mock_state.parent_branch = "epic/76-quality-gates"
    mock_engine.get_state.return_value = mock_state

    tool = GitCheckoutTool(manager=mock_git_manager, state_engine=mock_engine)
    params = GitCheckoutInput(branch="feature/79-test")
    result = await tool.execute(params, NoteContext())

    mock_git_manager.checkout.assert_called_once_with("feature/79-test")
    assert "Switched to branch: feature/79-test" in result.content[0]["text"]
    assert "Current phase: design" in result.content[0]["text"]
    assert "Parent branch: epic/76-quality-gates" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_git_checkout_tool_no_parent_branch(mock_git_manager: MagicMock) -> None:
    """Test git checkout without parent_branch doesn't show it.

    Issue #79: Backward compatibility - don't show parent if None.
    """
    tool = GitCheckoutTool(manager=mock_git_manager)

    # Mock PhaseStateEngine to return state WITHOUT parent_branch
    mock_engine = MagicMock()
    mock_state = MagicMock()
    mock_state.current_phase = "implementation"
    mock_state.parent_branch = None
    mock_engine.get_state.return_value = mock_state

    tool = GitCheckoutTool(manager=mock_git_manager, state_engine=mock_engine)
    params = GitCheckoutInput(branch="main")
    result = await tool.execute(params, NoteContext())

    mock_git_manager.checkout.assert_called_once_with("main")
    output = result.content[0]["text"]
    assert "Switched to branch: main" in output
    assert "Current phase: implementation" in output
    assert "Parent branch:" not in output  # Should NOT appear


@pytest.mark.asyncio
async def test_git_push_tool(mock_git_manager: MagicMock) -> None:
    """Test git push tool."""
    tool = GitPushTool(manager=mock_git_manager)
    mock_git_manager.get_status.return_value = {"branch": "feature/foo"}

    params = GitPushInput(set_upstream=True)
    result = await tool.execute(params, NoteContext())

    mock_git_manager.push.assert_called_once_with(set_upstream=True)
    assert "Pushed branch: feature/foo" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_git_merge_tool(mock_git_manager: MagicMock) -> None:
    """Test git merge tool."""
    tool = GitMergeTool(manager=mock_git_manager)
    mock_git_manager.get_status.return_value = {"branch": "main"}

    params = GitMergeInput(branch="feature/foo")
    result = await tool.execute(params, NoteContext())

    mock_git_manager.merge.assert_called_once_with("feature/foo", ANY)
    assert "Merged feature/foo into main" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_git_delete_branch_tool(mock_git_manager: MagicMock) -> None:
    """Test git delete branch tool."""
    tool = GitDeleteBranchTool(manager=mock_git_manager)
    mock_git_manager.delete_branch.return_value = BranchDeleteResult(
        local_status="deleted", remote_status="deleted"
    )

    params = GitDeleteBranchInput(branch="feature/old", force=True)
    result = await tool.execute(params, NoteContext())
    mock_git_manager.delete_branch.assert_called_once_with(
        "feature/old", ANY, force=True, mode="both"
    )
    expected = "Deleted branch: feature/old (local: deleted, remote: deleted)"
    assert result.content[0]["text"] == expected


@pytest.mark.asyncio
async def test_git_delete_branch_mode_local(mock_git_manager: MagicMock) -> None:
    """Test delete branch tool passes mode=local to manager."""
    tool = GitDeleteBranchTool(manager=mock_git_manager)
    mock_git_manager.delete_branch.return_value = BranchDeleteResult(
        local_status="deleted", remote_status="skipped"
    )

    params = GitDeleteBranchInput(branch="feature/old", mode="local")
    result = await tool.execute(params, NoteContext())

    mock_git_manager.delete_branch.assert_called_once_with(
        "feature/old", ANY, force=False, mode="local"
    )
    assert result.content[0]["text"] == "Deleted branch: feature/old (local: deleted)"


@pytest.mark.asyncio
async def test_git_delete_branch_mode_remote(mock_git_manager: MagicMock) -> None:
    """Test delete branch tool passes mode=remote to manager."""
    tool = GitDeleteBranchTool(manager=mock_git_manager)
    mock_git_manager.delete_branch.return_value = BranchDeleteResult(
        local_status="skipped", remote_status="deleted"
    )

    params = GitDeleteBranchInput(branch="feature/old", mode="remote")
    result = await tool.execute(params, NoteContext())

    mock_git_manager.delete_branch.assert_called_once_with(
        "feature/old", ANY, force=False, mode="remote"
    )
    assert result.content[0]["text"] == "Deleted branch: feature/old (remote: deleted)"


@pytest.mark.asyncio
async def test_git_stash_tool(mock_git_manager: MagicMock) -> None:
    """Test git stash tool with different actions."""
    tool = GitStashTool(manager=mock_git_manager)

    # Push
    result = await tool.execute(GitStashInput(action="push", message="wip"), NoteContext())
    mock_git_manager.stash.assert_called_with(message="wip", include_untracked=False)
    assert "Stashed changes: wip" in result.content[0]["text"]

    # Pop
    result = await tool.execute(GitStashInput(action="pop"), NoteContext())
    mock_git_manager.stash_pop.assert_called_once()
    assert "Applied and removed latest stash" in result.content[0]["text"]

    # List
    mock_git_manager.stash_list.return_value = ["stash@{0}: wip"]
    result = await tool.execute(GitStashInput(action="list"), NoteContext())
    assert "stash@{0}: wip" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_git_restore_tool(mock_git_manager: MagicMock) -> None:
    """Test git restore tool."""
    tool = GitRestoreTool(manager=mock_git_manager)

    params = GitRestoreInput(files=["foo.py", "bar.py"], source="HEAD")
    result = await tool.execute(params, NoteContext())

    mock_git_manager.restore.assert_called_once_with(
        files=["foo.py", "bar.py"], note_context=ANY, source="HEAD"
    )
    assert "Restored 2 file(s)" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_get_parent_branch_current_branch() -> None:
    """Test get parent branch for current branch.

    Issue #79: Query parent_branch from PhaseStateEngine state.
    """
    mock_git_manager = MagicMock()
    mock_git_manager.get_current_branch.return_value = "feature/79-parent-branch-tracking"

    mock_engine = MagicMock()
    mock_state = MagicMock()
    mock_state.current_phase = "implementation"
    mock_state.parent_branch = "epic/76-quality-gates"
    mock_engine.get_state.return_value = mock_state

    tool = GetParentBranchTool(manager=mock_git_manager, state_engine=mock_engine)
    params = GetParentBranchInput()
    result = await tool.execute(params, NoteContext())

    mock_engine.get_state.assert_called_once_with("feature/79-parent-branch-tracking")
    assert "Parent branch: epic/76-quality-gates" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_get_parent_branch_specified_branch() -> None:
    """Test get parent branch for specified branch.

    Issue #79: Query parent_branch for any branch, not just current.
    """
    mock_engine = MagicMock()
    mock_state = MagicMock()
    mock_state.current_phase = "design"
    mock_state.parent_branch = "epic/76-quality-gates"
    mock_engine.get_state.return_value = mock_state

    tool = GetParentBranchTool(manager=MagicMock(), state_engine=mock_engine)
    params = GetParentBranchInput(branch="feature/77-error-handling")
    result = await tool.execute(params, NoteContext())

    mock_engine.get_state.assert_called_once_with("feature/77-error-handling")
    assert "Parent branch: epic/76-quality-gates" in result.content[0]["text"]
    assert "feature/77-error-handling" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_get_parent_branch_not_set() -> None:
    """Test get parent branch when not set.

    Issue #79: Graceful handling when parent_branch is None.
    """
    mock_engine = MagicMock()
    mock_state = MagicMock()
    mock_state.current_phase = "implementation"
    mock_state.parent_branch = None
    mock_engine.get_state.return_value = mock_state

    tool = GetParentBranchTool(manager=MagicMock(), state_engine=mock_engine)
    params = GetParentBranchInput(branch="main")
    result = await tool.execute(params, NoteContext())

    mock_engine.get_state.assert_called_once_with("main")
    output = result.content[0]["text"]
    assert "Parent branch: (not set)" in output
    assert "main" in output


# ===== Cycle Number Enforcement Tests (Issue #146 Cycle 5) =====


def test_git_commit_tdd_requires_cycle_number() -> None:
    """Test that TDD phase commits REQUIRE cycle_number (Issue #146).

    Enforcement moved from execute() to GitCommitInput model_validator (Issue #358 C1).
    """
    with pytest.raises(ValidationError, match="cycle_number"):
        GitCommitInput(
            message="update documentation",
            workflow_phase="implementation",
            # cycle_number is MISSING - should raise ValidationError at model level
        )


def test_git_commit_tdd_subphase_requires_cycle_number() -> None:
    """Test that TDD sub-phase commits REQUIRE cycle_number (Issue #146).

    Enforcement moved from execute() to GitCommitInput model_validator (Issue #358 C1).
    """
    with pytest.raises(ValidationError, match="cycle_number"):
        GitCommitInput(
            message="implement feature",
            workflow_phase="implementation",
            sub_phase="green",
            # cycle_number is MISSING - should raise ValidationError at model level
        )


@pytest.mark.asyncio
async def test_git_commit_non_tdd_allows_no_cycle_number(mock_git_manager: MagicMock) -> None:
    """Test that non-TDD phases do NOT require cycle_number (Issue #146)."""
    tool = GitCommitTool(manager=mock_git_manager)
    mock_git_manager.commit_with_scope.return_value = "abc1234"

    # Commit in research phase without cycle_number - should succeed
    params = GitCommitInput(
        message="research alternatives",
        workflow_phase="research",
        # cycle_number is OMITTED - should be allowed
    )

    result = await tool.execute(params, NoteContext())

    # Should succeed
    assert "Committed: abc1234" in result.content[0]["text"]
    mock_git_manager.commit_with_scope.assert_called_once_with(
        workflow_phase="research",
        message="research alternatives",
        note_context=ANY,
        sub_phase=None,
        cycle_number=None,
        commit_type=None,
        files=None,
        skip_paths=frozenset(),
        issue_number=999,
    )


@pytest.mark.asyncio
async def test_git_commit_tdd_with_cycle_number_succeeds(mock_git_manager: MagicMock) -> None:
    """Test that TDD commits WITH cycle_number succeed (Issue #146)."""
    tool = GitCommitTool(manager=mock_git_manager)
    mock_git_manager.commit_with_scope.return_value = "def5678"

    # Commit in TDD phase WITH cycle_number - should succeed
    params = GitCommitInput(
        message="add schema validation",
        workflow_phase="implementation",
        sub_phase="green",
        cycle_number=3,
    )

    result = await tool.execute(params, NoteContext())

    # Should succeed
    assert "Committed: def5678" in result.content[0]["text"]
    mock_git_manager.commit_with_scope.assert_called_once_with(
        workflow_phase="implementation",
        message="add schema validation",
        note_context=ANY,
        sub_phase="green",
        cycle_number=3,
        commit_type=None,
        files=None,
        skip_paths=frozenset(),
        issue_number=999,
    )


# --- C2 re-run: commit phase mismatch guard (GAP-07) ---


@pytest.mark.asyncio
async def test_git_add_or_commit_raises_on_phase_mismatch(mock_git_manager: MagicMock) -> None:
    """CommitPhaseMismatchError when workflow_phase doesn't match state.json (GAP-07)."""

    def phase_guard(_branch: str, workflow_phase: str, _cycle_number: int | None) -> None:
        raise CommitPhaseMismatchError(
            f"phase_mismatch: commit says '{workflow_phase}' but state.json says 'design'"
        )

    tool = GitCommitTool(manager=mock_git_manager, phase_guard=phase_guard)
    mock_git_manager.adapter.get_current_branch.return_value = (
        "feature/229-phase-deliverables-enforcement"
    )

    params = GitCommitInput(
        workflow_phase="implementation",
        cycle_number=2,
        message="add red test",
    )
    result = await tool.execute(params, NoteContext())

    assert result.is_error
    assert "phase_mismatch" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_git_add_or_commit_raises_on_cycle_mismatch(mock_git_manager: MagicMock) -> None:
    """CommitPhaseMismatchError when cycle_number mismatches state.json (GAP-07)."""

    def phase_guard(_branch: str, _workflow_phase: str, cycle_number: int | None) -> None:
        raise CommitPhaseMismatchError(
            f"phase_mismatch: commit says cycle {cycle_number} but state.json says cycle 3"
        )

    tool = GitCommitTool(manager=mock_git_manager, phase_guard=phase_guard)
    mock_git_manager.adapter.get_current_branch.return_value = (
        "feature/229-phase-deliverables-enforcement"
    )

    params = GitCommitInput(
        workflow_phase="implementation",
        cycle_number=2,
        message="add green impl",
    )
    result = await tool.execute(params, NoteContext())

    assert result.is_error
    assert "phase_mismatch" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_git_add_or_commit_passes_when_phase_and_cycle_match(
    mock_git_manager: MagicMock,
) -> None:
    """No error when workflow_phase and cycle_number match state.json (GAP-07)."""

    def phase_guard(_branch: str, _workflow_phase: str, _cycle_number: int | None) -> None:
        pass  # phase=tdd, cycle=2 matches state.json

    tool = GitCommitTool(manager=mock_git_manager, phase_guard=phase_guard)
    mock_git_manager.adapter.get_current_branch.return_value = (
        "feature/229-phase-deliverables-enforcement"
    )
    mock_git_manager.commit_with_scope.return_value = "abc1234"

    params = GitCommitInput(
        workflow_phase="implementation",
        cycle_number=2,
        message="implement guard",
    )
    result = await tool.execute(params, NoteContext())

    assert "Committed: abc1234" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_git_commit_no_state_json_returns_error(mock_git_manager: MagicMock) -> None:
    """GitCommitTool returns ToolResult.error when state.json is missing (e.g. main)."""
    mock_state_engine = MagicMock()
    mock_state_engine.get_state.side_effect = FileNotFoundError("Branch state for 'main' not found")
    mock_git_manager.adapter.get_current_branch.return_value = "main"

    tool = GitCommitTool(manager=mock_git_manager, state_engine=mock_state_engine)

    # No workflow_phase — triggers auto-detect from state.json
    params = GitCommitInput(message="chore: cleanup")

    result = await tool.execute(params, NoteContext())

    assert result.is_error
    error_text = result.content[0]["text"]
    assert "workflow_phase" in error_text
    assert "main" in error_text


class TestGitCommitBranchMismatch:
    """C_ENGINE_BREAK: GitCommitTool handles StateBranchMismatchError (issue #231, cycle 2)."""

    @pytest.mark.asyncio
    async def test_commit_auto_detect_handles_branch_mismatch(
        self, mock_git_manager: MagicMock
    ) -> None:
        """Auto-detect path must catch StateBranchMismatchError and return ToolResult.error."""
        mock_state_engine = MagicMock()
        mock_state_engine.get_state.side_effect = StateBranchMismatchError(
            "Loaded state branch 'main' does not match requested branch 'feature/231-test'"
        )
        mock_git_manager.adapter.get_current_branch.return_value = "feature/231-test"

        tool = GitCommitTool(manager=mock_git_manager, state_engine=mock_state_engine)
        params = GitCommitInput(message="chore: cleanup")

        result = await tool.execute(params, NoteContext())

        assert result.is_error

    @pytest.mark.asyncio
    async def test_commit_type_resolver_returns_none_on_branch_mismatch(
        self, mock_git_manager: MagicMock
    ) -> None:
        """build_commit_type_resolver returns None (no type) on StateBranchMismatchError."""
        mock_state_engine = MagicMock()
        mock_state_engine.get_state.side_effect = StateBranchMismatchError(
            "Loaded state branch 'main' does not match requested branch 'feature/231-test'"
        )
        mock_git_manager.adapter.get_current_branch.return_value = "feature/231-test"
        mock_git_manager.commit_with_scope.return_value = "abc1234"

        resolver_fn = MagicMock(return_value=None)
        tool = GitCommitTool(manager=mock_git_manager, commit_type_resolver=resolver_fn)
        params = GitCommitInput(
            message="refactor cleanup",
            workflow_phase="implementation",
            sub_phase="refactor",
            cycle_number=2,
        )

        result = await tool.execute(params, NoteContext())

        assert not result.is_error
        assert "Committed: abc1234" in result.content[0]["text"]

    @pytest.mark.asyncio
    async def test_get_parent_branch_handles_branch_mismatch(
        self, mock_git_manager: MagicMock
    ) -> None:
        """GetParentBranchTool.execute() returns error on StateBranchMismatchError."""
        mock_state_engine = MagicMock()
        mock_state_engine.get_state.side_effect = StateBranchMismatchError(
            "Loaded state branch 'main' does not match requested branch 'feature/231-test'"
        )
        mock_git_manager.get_current_branch.return_value = "feature/231-test"

        tool = GetParentBranchTool(manager=mock_git_manager, state_engine=mock_state_engine)
        params = GetParentBranchInput()

        result = await tool.execute(params, NoteContext())

        assert result.is_error


# ---------------------------------------------------------------------------
# C5 RED — GitCommitTool triggers record_sub_phase (issue #298)
# ---------------------------------------------------------------------------


class TestGitCommitToolRecordSubPhase:
    """C5 (issue #298): GitCommitTool.execute() calls record_sub_phase after every commit."""

    @pytest.mark.asyncio
    async def test_git_commit_tool_calls_record_sub_phase_with_sub_phase(
        self, mock_git_manager: MagicMock
    ) -> None:
        """After a successful commit with sub_phase='red', record_sub_phase is called with 'red'."""
        mock_state_engine = MagicMock()
        mock_git_manager.commit_with_scope.return_value = "aabbccdd"
        mock_git_manager.adapter.get_current_branch.return_value = "feature/298-test"

        tool = GitCommitTool(manager=mock_git_manager, state_engine=mock_state_engine)
        params = GitCommitInput(
            workflow_phase="implementation",
            cycle_number=1,
            sub_phase="red",
            message="add failing test",
        )
        result = await tool.execute(params, NoteContext())

        assert not result.is_error
        mock_state_engine.record_sub_phase.assert_called_once_with("feature/298-test", "red")

    @pytest.mark.asyncio
    async def test_git_commit_tool_calls_record_sub_phase_with_none(
        self, mock_git_manager: MagicMock
    ) -> None:
        """After a successful commit with sub_phase=None, record_sub_phase is called with None."""
        mock_state_engine = MagicMock()
        mock_git_manager.commit_with_scope.return_value = "11223344"
        mock_git_manager.adapter.get_current_branch.return_value = "feature/298-test"

        tool = GitCommitTool(manager=mock_git_manager, state_engine=mock_state_engine)
        params = GitCommitInput(
            workflow_phase="research",
            message="initial research notes",
        )
        result = await tool.execute(params, NoteContext())

        assert not result.is_error
        mock_state_engine.record_sub_phase.assert_called_once_with("feature/298-test", None)

    @pytest.mark.asyncio
    async def test_git_commit_tool_does_not_call_record_sub_phase_when_engine_none(
        self, mock_git_manager: MagicMock
    ) -> None:
        """When state_engine is None, record_sub_phase must NOT be called (no AttributeError)."""
        mock_git_manager.commit_with_scope.return_value = "deadbeef"
        mock_git_manager.adapter.get_current_branch.return_value = "feature/298-test"

        tool = GitCommitTool(manager=mock_git_manager)  # no state_engine
        params = GitCommitInput(
            workflow_phase="documentation",
            message="update readme",
        )
        result = await tool.execute(params, NoteContext())

        assert not result.is_error  # must succeed without engine


# C_228.2 RED — issue_number wiring in GitCommitTool (issue #228)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_commit_tool_auto_detect_includes_suffix(mock_git_manager: MagicMock) -> None:
    """Auto-detect path: get_state() returns issue_number=42.

    commit_with_scope must be called with issue_number=42.
    """
    mock_state_engine = MagicMock()
    branch_state_stub = MagicMock()
    branch_state_stub.current_phase = "research"
    branch_state_stub.issue_number = 42
    mock_state_engine.get_state.return_value = branch_state_stub

    mock_git_manager.adapter.get_current_branch.return_value = "feature/42-my-feature"
    mock_git_manager.commit_with_scope.return_value = "abc1234"

    tool = GitCommitTool(manager=mock_git_manager, state_engine=mock_state_engine)
    params = GitCommitInput(message="implement suffix")
    # workflow_phase is None → triggers auto-detect

    result = await tool.execute(params, NoteContext())

    mock_state_engine.get_state.assert_called_once_with("feature/42-my-feature")
    mock_git_manager.commit_with_scope.assert_called_once_with(
        workflow_phase="research",
        message="implement suffix",
        note_context=ANY,
        sub_phase=None,
        cycle_number=None,
        commit_type=ANY,
        files=None,
        skip_paths=frozenset(),
        issue_number=42,
    )
    assert not result.is_error


@pytest.mark.asyncio
async def test_commit_tool_explicit_phase_uses_git_config(mock_git_manager: MagicMock) -> None:
    """Explicit workflow_phase: git_config.extract_issue_number called; no get_state call."""
    mock_git_manager.adapter.get_current_branch.return_value = "feature/42-my-feature"
    mock_git_manager.git_config.extract_issue_number.side_effect = None
    mock_git_manager.git_config.extract_issue_number.return_value = 42
    mock_git_manager.commit_with_scope.return_value = "abc1234"

    tool = GitCommitTool(manager=mock_git_manager)
    params = GitCommitInput(
        message="complete research",
        workflow_phase="research",
    )

    result = await tool.execute(params, NoteContext())

    mock_git_manager.git_config.extract_issue_number.assert_called_once_with(
        "feature/42-my-feature"
    )
    mock_git_manager.commit_with_scope.assert_called_once_with(
        workflow_phase="research",
        message="complete research",
        note_context=ANY,
        sub_phase=None,
        cycle_number=None,
        commit_type=ANY,
        files=None,
        skip_paths=frozenset(),
        issue_number=42,
    )
    assert not result.is_error


@pytest.mark.asyncio
async def test_commit_tool_auto_detect_mismatch_returns_error(mock_git_manager: MagicMock) -> None:
    """StateBranchMismatchError on auto-detect path returns ToolResult.error.

    Must not silently degrade to issue_number=None.
    """
    mock_state_engine = MagicMock()
    mock_state_engine.get_state.side_effect = StateBranchMismatchError(
        "Loaded state branch 'main' does not match requested branch 'feature/42-test'"
    )
    mock_git_manager.adapter.get_current_branch.return_value = "feature/42-test"

    tool = GitCommitTool(manager=mock_git_manager, state_engine=mock_state_engine)
    params = GitCommitInput(message="chore: cleanup")

    result = await tool.execute(params, NoteContext())

    assert result.is_error
    mock_git_manager.commit_with_scope.assert_not_called()


@pytest.mark.asyncio
async def test_git_checkout_resets_context_loaded_on_success(
    mock_git_manager: MagicMock,
) -> None:
    """writer.set_context_loaded(branch, False) called on successful checkout."""
    writer = MagicMock(spec=IContextLoadedWriter)
    tool = GitCheckoutTool(manager=mock_git_manager, context_loaded_writer=writer)

    params = GitCheckoutInput(branch="feature/268-test")
    result = await tool.execute(params, NoteContext())

    assert not result.is_error
    writer.set_context_loaded.assert_called_once_with("feature/268-test", value=False)


@pytest.mark.asyncio
async def test_git_checkout_no_reset_when_writer_none(
    mock_git_manager: MagicMock,
) -> None:
    """No error when context_loaded_writer=None and checkout succeeds."""
    tool = GitCheckoutTool(manager=mock_git_manager, context_loaded_writer=None)

    params = GitCheckoutInput(branch="feature/268-test")
    result = await tool.execute(params, NoteContext())

    assert not result.is_error


# ---------------------------------------------------------------------------
# CheckMergeTool tests (C6 RED)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_check_merge_sha_is_ancestor(mock_git_manager: MagicMock) -> None:
    """SHA is an ancestor of HEAD -> ToolResult.text returned."""
    mock_git_manager.is_ancestor.return_value = True
    tool = CheckMergeTool(manager=mock_git_manager)

    params = CheckMergeInput(merge_sha="abc1234")
    result = await tool.execute(params, NoteContext())

    assert not result.is_error
    mock_git_manager.is_ancestor.assert_called_once_with("abc1234")


@pytest.mark.asyncio
async def test_check_merge_sha_not_ancestor(mock_git_manager: MagicMock) -> None:
    """SHA is not an ancestor (status 1) -> ToolResult.error returned."""
    mock_git_manager.is_ancestor.return_value = False
    tool = CheckMergeTool(manager=mock_git_manager)

    params = CheckMergeInput(merge_sha="abc1234")
    result = await tool.execute(params, NoteContext())

    assert result.is_error
    mock_git_manager.is_ancestor.assert_called_once_with("abc1234")


@pytest.mark.asyncio
async def test_check_merge_git_error_raises(mock_git_manager: MagicMock) -> None:
    """Git command fails (status >=2) -> execute returns ToolResult.error via error_handling."""
    mock_git_manager.is_ancestor.side_effect = ExecutionError("git error status 2")
    tool = CheckMergeTool(manager=mock_git_manager)

    params = CheckMergeInput(merge_sha="abc1234")
    result = await tool.execute(params, NoteContext())

    assert result.is_error


@pytest.mark.asyncio
async def test_check_merge_manager_delegates_to_adapter() -> None:
    """GitManager.is_ancestor delegates to GitAdapter.is_ancestor and propagates value."""
    mock_adapter = MagicMock(spec=GitAdapter)
    mock_adapter.is_ancestor.return_value = True
    mock_adapter.get_current_branch.return_value = "bug/357-fix-agent-lifecycle"

    mock_git_config = MagicMock()
    mock_git_config.default_base_branch = "main"

    real_manager = GitManager(git_config=mock_git_config, adapter=mock_adapter)
    result = real_manager.is_ancestor("abc1234")

    assert result is True
    mock_adapter.is_ancestor.assert_called_once_with("abc1234")
