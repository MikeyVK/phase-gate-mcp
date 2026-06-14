# pyright: reportPrivateUsage=false
"""Unit tests for issue_tools.py.

@layer: Tests (Unit)
@dependencies: [pytest, unittest.mock, mcp_server.tools.issue_tools]
"""

from unittest.mock import MagicMock

import pytest

from mcp_server.core.operation_notes import NoteContext
from mcp_server.schemas.tool_outputs import CloseIssueOutput, IssueOutput, ListIssuesOutput
from mcp_server.tools.issue_tools import (
    CloseIssueInput,
    CloseIssueTool,
    CreateIssueInput,
    GetIssueInput,
    GetIssueTool,
    ListIssuesInput,
    ListIssuesTool,
    UpdateIssueInput,
    UpdateIssueTool,
)
from tests.mcp_server.test_support import make_create_issue_tool


@pytest.fixture
def mock_github_manager() -> MagicMock:
    from mcp_server.schemas.github_models import IssueReadModel
    manager = MagicMock()
    mock_issue_read = IssueReadModel(
        number=123,
        url="http://github.com/issues/123",
        title="Mock Issue",
        body="## Problem\n\nSome description.",
        state="open",
        labels=["type:feature", "scope:mcp-server", "priority:medium", "phase:planning"],
        milestone=None,
        assignees=[],
        created_at="2023-01-01T00:00:00Z",
        updated_at="2023-01-01T00:00:00Z",
        closed_at=None,
        author="alice",
    )
    manager.get_issue.return_value = mock_issue_read
    return manager


@pytest.mark.asyncio
async def test_create_issue_tool(mock_github_manager: MagicMock) -> None:
    tool = make_create_issue_tool(mock_github_manager)
    issue_mock = {"number": 123, "url": "http://github.com/issues/123", "title": "New Issue"}
    mock_github_manager.create_issue.return_value = issue_mock

    params = CreateIssueInput(
        issue_type="feature",
        title="New Issue",
        priority="medium",
        scope="mcp-server",
        body="## Problem\n\nSome problem description.",
    )
    result = await tool.execute(params, NoteContext())

    mock_github_manager.validate_issue_params.assert_called_once_with(
        issue_type="feature",
        title="New Issue",
        priority="medium",
        scope="mcp-server",
        milestone=None,
        assignees=None,
    )
    mock_github_manager.create_issue.assert_called_once()
    assert isinstance(result, IssueOutput)
    assert result.success is True
    assert result.number == 123


@pytest.mark.asyncio
async def test_create_issue_tool_forwards_milestone(mock_github_manager: MagicMock) -> None:
    issue_mock = {"number": 7, "url": "http://github.com/issues/7", "title": "Milestone Issue"}
    mock_github_manager.create_issue.return_value = issue_mock

    milestone_entry = MagicMock()
    milestone_entry.title = "v2.0"
    milestone_entry.number = 2
    milestone_config = MagicMock()
    milestone_config.milestones = [milestone_entry]

    tool = make_create_issue_tool(mock_github_manager)
    tool._milestone_config = milestone_config

    params = CreateIssueInput(
        issue_type="feature",
        title="Milestone Issue",
        priority="medium",
        scope="mcp-server",
        body="## Problem\n\nNeeds milestone.",
        milestone="v2.0",
    )
    await tool.execute(params, NoteContext())

    call_kwargs = mock_github_manager.create_issue.call_args.kwargs
    assert call_kwargs["milestone"] == 2


@pytest.mark.asyncio
async def test_create_issue_tool_milestone_none_when_not_set(
    mock_github_manager: MagicMock,
) -> None:
    tool = make_create_issue_tool(mock_github_manager)
    mock_github_manager.create_issue.return_value = {"number": 8, "url": "", "title": "No ms"}

    params = CreateIssueInput(
        issue_type="feature",
        title="No milestone",
        priority="medium",
        scope="mcp-server",
        body="## Problem\n\nNo milestone set.",
    )
    await tool.execute(params, NoteContext())

    call_kwargs = mock_github_manager.create_issue.call_args.kwargs
    assert call_kwargs["milestone"] is None


@pytest.mark.asyncio
async def test_update_issue_tool(mock_github_manager: MagicMock) -> None:
    tool = UpdateIssueTool(manager=mock_github_manager)
    mock_github_manager.update_issue.return_value = MagicMock(number=123)

    params = UpdateIssueInput(issue_number=123, title="Updated Title")
    result = await tool.execute(params, NoteContext())

    mock_github_manager.update_issue.assert_called_with(
        issue_number=123,
        title="Updated Title",
        body=None,
        state=None,
        labels=None,
        assignees=None,
        milestone=None,
    )
    assert isinstance(result, IssueOutput)
    assert result.success is True
    assert result.number == 123


@pytest.mark.asyncio
async def test_list_issues_tool(mock_github_manager: MagicMock) -> None:
    tool = ListIssuesTool(manager=mock_github_manager)
    
    issue1 = MagicMock()
    issue1.number = 1
    issue1.title = "Issue 1"
    issue1.state = "open"
    issue1.html_url = "https://github.com/issues/1"
    issue1.labels = [MagicMock(name="bug")]
    issue1.assignees = []
    issue1.created_at = "2023-01-01T00:00:00Z"

    issue2 = MagicMock()
    issue2.number = 2
    issue2.title = "Issue 2"
    issue2.state = "closed"
    issue2.html_url = "https://github.com/issues/2"
    issue2.labels = []
    issue2.assignees = []
    issue2.created_at = "2023-01-01T00:00:00Z"

    mock_github_manager.list_issues.return_value = [issue1, issue2]

    params = ListIssuesInput(state="open", labels=["bug"])
    result = await tool.execute(params, NoteContext())

    mock_github_manager.list_issues.assert_called_with(state="open", labels=["bug"])
    assert isinstance(result, ListIssuesOutput)
    assert result.success is True
    assert result.issues_count == 2
    assert result.issues[0].number == 1
    assert result.issues[0].title == "Issue 1"


@pytest.mark.asyncio
async def test_get_issue_tool(mock_github_manager: MagicMock) -> None:
    tool = GetIssueTool(manager=mock_github_manager)

    mock_model = MagicMock()
    issue_data = {
        "number": 1,
        "url": "https://github.com/owner/repo/issues/1",
        "title": "Bug",
        "body": "Fix it",
        "state": "open",
        "labels": [],
        "milestone": None,
        "assignees": [],
        "created_at": "2023-01-01T00:00:00+00:00",
        "updated_at": "2023-01-01T00:00:00+00:00",
        "closed_at": None,
        "author": "alice",
    }
    mock_model.model_dump.return_value = issue_data
    mock_github_manager.get_issue.return_value = mock_model

    result = await tool.execute(GetIssueInput(issue_number=1), NoteContext())

    mock_github_manager.get_issue.assert_called_with(1)
    assert isinstance(result, IssueOutput)
    assert result.success is True
    assert result.number == 1
    assert result.title == "Bug"


@pytest.mark.asyncio
async def test_close_issue_tool(mock_github_manager: MagicMock) -> None:
    tool = CloseIssueTool(manager=mock_github_manager)
    mock_github_manager.close_issue.return_value = MagicMock(number=5)

    result = await tool.execute(CloseIssueInput(issue_number=5, comment="Done"), NoteContext())

    mock_github_manager.close_issue.assert_called_with(5, comment="Done")
    assert isinstance(result, CloseIssueOutput)
    assert result.success is True
    assert result.issue_number == 5


def test_create_issue_input_body_is_str() -> None:
    """C1 RED: CreateIssueInput.body must accept a plain string, not IssueBody."""
    params = CreateIssueInput(
        issue_type="feature",
        title="Test issue",
        priority="medium",
        scope="mcp-server",
        body="## Problem\n\nSomething is broken.",
    )
    assert params.body == "## Problem\n\nSomething is broken."


def test_create_issue_input_body_rejects_dict() -> None:
    """C1 RED: CreateIssueInput.body must reject structured dicts (no IssueBody coercion)."""
    with pytest.raises(Exception):  # noqa: B017
        CreateIssueInput(
            issue_type="feature",
            title="Test issue",
            priority="medium",
            scope="mcp-server",
            body={"problem": "something"},  # type: ignore[arg-type]
        )
