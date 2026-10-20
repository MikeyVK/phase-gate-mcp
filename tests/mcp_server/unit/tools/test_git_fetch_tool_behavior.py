# pyright: reportPrivateUsage=false
"""Behavior tests for GitFetchTool.

Also verifies the public input schema and argument defaults.

@layer: Tests (Unit)
@dependencies: [pytest, unittest.mock, mcp_server.tools.git_fetch_tool]
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from mcp_server.core.exceptions import PreflightError
from mcp_server.core.operation_notes import NoteContext
from mcp_server.tools.git_fetch_tool import GitFetchInput, GitFetchTool


def test_git_fetch_tool_input_schema_property() -> None:
    """Expose the concrete argument model and its remote-operation defaults."""

    tool = GitFetchTool(manager=Mock())
    schema = tool.input_schema
    assert isinstance(schema, dict)
    assert tool.args_model is GitFetchInput
    assert schema["properties"]["remote"]["default"] == "origin"
    assert schema["properties"]["prune"]["default"] is False
    assert schema["additionalProperties"] is False


@pytest.mark.asyncio
async def test_git_fetch_success_returns_text() -> None:
    """Returns ToolResult.text when manager fetch succeeds."""

    manager = Mock()
    manager.fetch.return_value = "Fetched from origin: 1 ref(s)"
    tool = GitFetchTool(manager=manager)

    run_sync = AsyncMock(return_value=manager.fetch.return_value)
    with patch("mcp_server.tools.git_fetch_tool.anyio.to_thread.run_sync", new=run_sync):
        result = await tool.execute(GitFetchInput(), NoteContext())

    from mcp_server.schemas.tool_outputs import GitFetchOutput  # noqa: PLC0415

    assert isinstance(result, GitFetchOutput)
    assert result.success is True
    assert result.remote == "origin"
    assert "Fetched from origin" in result.raw_output


@pytest.mark.asyncio
async def test_git_fetch_mcperror_returns_tool_error() -> None:
    """Converts MCPError from manager into ToolResult.error."""

    manager = Mock()
    tool = GitFetchTool(manager=manager)

    run_sync = AsyncMock(side_effect=PreflightError("No remote"))
    with patch("mcp_server.tools.git_fetch_tool.anyio.to_thread.run_sync", new=run_sync):
        result = await tool.execute(GitFetchInput(remote="origin"), NoteContext())

    from mcp_server.schemas.tool_outputs import GitFetchOutput  # noqa: PLC0415

    assert isinstance(result, GitFetchOutput)
    assert result.success is False
    assert result.error_message is not None
    assert "No remote" in result.error_message
    assert "No remote" in result.error_message


@pytest.mark.asyncio
async def test_git_fetch_runtime_error_returns_tool_error() -> None:
    """Converts runtime exception into ToolResult.error with prefix."""

    manager = Mock()
    tool = GitFetchTool(manager=manager)

    run_sync = AsyncMock(side_effect=RuntimeError("boom"))
    with patch("mcp_server.tools.git_fetch_tool.anyio.to_thread.run_sync", new=run_sync):
        result = await tool.execute(GitFetchInput(remote="origin"), NoteContext())

    from mcp_server.schemas.tool_outputs import GitFetchOutput  # noqa: PLC0415

    assert isinstance(result, GitFetchOutput)
    assert result.success is False
    assert result.error_message is not None
    assert "Fetch failed: boom" in result.error_message
    assert "Fetch failed: boom" in result.error_message
