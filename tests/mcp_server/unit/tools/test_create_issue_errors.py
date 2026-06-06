"""
Cycle 6 — Error handling in CreateIssueTool.execute().

Tests that expected failure modes produce ToolResult.error() with actionable
messages instead of leaking raw exceptions to the caller.

@layer: Tests (Unit)
@dependencies: [pytest, unittest.mock, mcp_server.tools.issue_tools]
"""

from unittest.mock import MagicMock

import pytest

from mcp_server.core.exceptions import ExecutionError
from mcp_server.core.operation_notes import NoteContext
from mcp_server.tools.issue_tools import CreateIssueInput, CreateIssueTool
from tests.mcp_server.test_support import make_create_issue_tool

BODY = "## Problem\n\nTest error scenarios."


def make_valid_params() -> CreateIssueInput:
    return CreateIssueInput(
        issue_type="feature",
        title="Error test issue",
        priority="medium",
        scope="mcp-server",
        body=BODY,
    )


def make_tool(manager: MagicMock | None = None) -> CreateIssueTool:
    mgr = manager or MagicMock()
    mgr.create_issue.return_value = {"number": 1, "title": "T", "url": ""}
    return make_create_issue_tool(mgr)


class TestExecutionErrorHandling:
    @pytest.mark.asyncio
    async def test_validation_error_returns_tool_result_error(self) -> None:
        mock_manager = MagicMock()
        mock_manager.validate_issue_params.side_effect = ValueError("Unknown issue type")
        tool = make_create_issue_tool(mock_manager)

        result = await tool.execute(make_valid_params(), NoteContext())

        assert result.is_error is True
        assert "Issue validation failed" in result.content[0]["text"]

    @pytest.mark.asyncio
    async def test_execution_error_returns_tool_result_error(self) -> None:
        mock_manager = MagicMock()
        mock_manager.create_issue.side_effect = ExecutionError("GitHub API rate limit exceeded")
        tool = make_create_issue_tool(mock_manager)

        result = await tool.execute(make_valid_params(), NoteContext())

        assert result.is_error is True

    @pytest.mark.asyncio
    async def test_execution_error_message_is_included(self) -> None:
        mock_manager = MagicMock()
        mock_manager.create_issue.side_effect = ExecutionError("GitHub API rate limit exceeded")
        tool = make_create_issue_tool(mock_manager)

        result = await tool.execute(make_valid_params(), NoteContext())

        result_text = result.content[0]["text"]
        assert "rate limit" in result_text or "GitHub" in result_text

    @pytest.mark.asyncio
    async def test_execution_error_does_not_raise(self) -> None:
        mock_manager = MagicMock()
        mock_manager.create_issue.side_effect = ExecutionError("Network error")
        tool = make_create_issue_tool(mock_manager)

        result = await tool.execute(make_valid_params(), NoteContext())
        assert result is not None
