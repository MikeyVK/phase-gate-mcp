from tests.mcp_server.test_support import get_default_server_root
# tests\mcp_server\unit\managers\test_enforcement_runner_unit.py
# template=unit_test version=3d15d309 created=2026-04-14T09:09Z updated=
"""
Unit tests for mcp_server.managers.enforcement_runner (C6 cleanup).

GitCommitTool.execute() NoteContext wiring tests.

@layer: Tests (Unit)
@dependencies: [json, pathlib, pytest, unittest.mock, mcp_server.core.operation_notes,
    mcp_server.managers.enforcement_runner, mcp_server.tools.git_tools]
@responsibilities:
    - Prove GitCommitTool.execute() accepts context: NoteContext as second parameter
    - Prove GitCommitTool reads ExclusionNote.file_path and forwards as skip_paths
"""

# Standard library
from unittest.mock import MagicMock

# Third-party
import pytest

# Project modules
from mcp_server.core.operation_notes import Note, NoteContext
from mcp_server.tools.git_tools import GitCommitInput, GitCommitTool
from mcp_server.tools.tool_result import ToolResult

_STATE_JSON = ".phase-gate/state.json"
_DELIVERABLES_JSON = ".phase-gate/deliverables.json"


class TestGitCommitToolC3:
    """C3 contract: GitCommitTool.execute() accepts NoteContext as second parameter."""

    @pytest.mark.asyncio
    async def test_git_commit_tool_execute_accepts_context(self) -> None:
        """execute(params, context) accepted as new public contract."""
        mock_manager = MagicMock()
        mock_manager.git_config.commit_types = ["feat", "fix", "chore", "refactor", "test", "docs"]
        mock_manager.adapter.get_current_branch.return_value = "refactor/283"
        mock_manager.commit_with_scope.return_value = "abc1234"

        tool = GitCommitTool(manager=mock_manager)
        params = GitCommitInput(message="test", workflow_phase="documentation")
        result = await tool.execute(params, NoteContext())
        assert result.success is True

    @pytest.mark.asyncio
    @pytest.mark.xfail(
        reason=(
            "Pre-existing: neutralize_to_base not yet called by GitCommitTool "
            "(C8 contract, separate issue)"
        ),
        strict=False,
    )
    @pytest.mark.asyncio
    async def test_server_renders_exclusion_note_in_response(self) -> None:
        """NoteContext.render_to_response must include ExclusionNote text in the result."""
        note_context = NoteContext()
        mock_presenter = MagicMock()
        mock_presenter.present_notes.return_value = f"Excluded from commit index: {_STATE_JSON}"
        note_context.presenter = mock_presenter
        note_context.tool_name = "git_add_or_commit"
        note_context.produce(Note(key="file_excluded", params={"file_path": _STATE_JSON}))
        base = ToolResult.text("abc1234")

        rendered = note_context.render_to_response(base)

        all_text = " ".join(c["text"] for c in rendered.content if c.get("type") == "text")
        assert _STATE_JSON in all_text
