"""Integration-style tests for CreateIssueTool.

@layer: Tests (Integration)
@dependencies: [pytest, unittest.mock, mcp_server.tools.issue_tools]
"""

from __future__ import annotations

import datetime
from unittest.mock import MagicMock

import pytest

from mcp_server.core.exceptions import ExecutionError
from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.github_manager import GitHubManager
from mcp_server.schemas import MilestoneConfig
from mcp_server.schemas.github_models import IssueReadModel
from mcp_server.tools.issue_tools import CreateIssueInput, CreateIssueTool
from tests.mcp_server.test_support import load_issue_tool_dependencies, make_create_issue_tool

pytestmark = pytest.mark.asyncio

MINIMAL_BODY = "## Problem\n\n[e2e smoke] Integration test - safe to close automatically."


def make_input(**overrides: object) -> CreateIssueInput:
    defaults: dict[str, object] = {
        "issue_type": "feature",
        "title": "[e2e smoke] create_issue integration test",
        "priority": "low",
        "scope": "tooling",
        "body": MINIMAL_BODY,
    }
    defaults.update(overrides)
    return CreateIssueInput(**defaults)


def make_validating_tool(
    *, milestone_config: MilestoneConfig | None = None
) -> tuple[CreateIssueTool, MagicMock]:
    dependencies = load_issue_tool_dependencies()
    adapter = MagicMock()
    manager = GitHubManager(
        adapter=adapter,
        issue_config=dependencies["issue_config"],
        label_config=dependencies["label_config"],
        scope_config=dependencies["scope_config"],
        milestone_config=milestone_config or dependencies["milestone_config"],
        contributor_config=dependencies["contributor_config"],
        git_config=dependencies["git_config"],
    )
    tool = CreateIssueTool(
        manager=manager,
        issue_config=dependencies["issue_config"],
        milestone_config=milestone_config or dependencies["milestone_config"],
        contracts_config=dependencies["contracts_config"],
        label_config=dependencies["label_config"],
        scope_config=dependencies["scope_config"],
        git_config=dependencies["git_config"],
    )
    return tool, adapter


async def test_minimal_input_creates_issue_with_correct_labels() -> None:
    mock_manager = MagicMock()
    mock_manager.create_issue.return_value = {
        "number": 42,
        "title": "[e2e smoke] create_issue integration test",
    }
    mock_manager.get_issue.return_value = IssueReadModel(
        number=42,
        url="http://github.com/issues/42",
        title="[e2e smoke] create_issue integration test",
        body=MINIMAL_BODY,
        state="open",
        labels=["type:feature", "scope:tooling", "priority:low", "phase:research"],
        milestone=None,
        assignees=[],
        created_at="2026-06-14T22:50:00Z",
        updated_at="2026-06-14T22:50:00Z",
        closed_at=None,
        author="user",
    )

    tool = make_create_issue_tool(mock_manager)
    params = make_input()

    result = await tool.execute(params, NoteContext())

    assert result.success is True
    assert result.number == 42
    assert result.title == "[e2e smoke] create_issue integration test"

    _, call_kwargs = mock_manager.create_issue.call_args
    label_names = set(call_kwargs["labels"])

    assert "type:feature" in label_names
    assert "scope:tooling" in label_names
    assert "priority:low" in label_names
    assert "phase:research" in label_names


async def test_all_options_creates_issue_with_full_label_set() -> None:
    mock_manager = MagicMock()
    mock_manager.create_issue.return_value = {
        "number": 99,
        "title": "[e2e smoke] create_issue full-options test",
    }
    mock_manager.get_issue.return_value = IssueReadModel(
        number=99,
        url="http://github.com/issues/99",
        title="[e2e smoke] create_issue full-options test",
        body="## Problem\n\n[e2e smoke] Full-options test.",
        state="open",
        labels=["type:epic", "parent:149", "scope:mcp-server", "priority:medium", "phase:research"],
        milestone=None,
        assignees=[],
        created_at="2026-06-14T22:50:00Z",
        updated_at="2026-06-14T22:50:00Z",
        closed_at=None,
        author="user",
    )

    tool = make_create_issue_tool(mock_manager)
    params = make_input(
        title="[e2e smoke] create_issue full-options test",
        issue_type="feature",
        is_epic=True,
        parent_issue=149,
        priority="medium",
        scope="mcp-server",
        body="## Problem\n\n[e2e smoke] Full-options test.",
    )

    result = await tool.execute(params, NoteContext())

    assert result.success is True
    assert result.number == 99

    _, call_kwargs = mock_manager.create_issue.call_args
    label_names = set(call_kwargs["labels"])

    assert "type:epic" in label_names
    assert "parent:149" in label_names
    assert "scope:mcp-server" in label_names
    assert "priority:medium" in label_names
    assert "phase:research" in label_names


async def test_invalid_issue_type_is_refused_before_api_call() -> None:
    tool, adapter = make_validating_tool()

    with pytest.raises(ExecutionError, match="Unknown issue type"):
        await tool.execute(make_input(issue_type="invalid_type"), NoteContext())

    adapter.create_issue.assert_not_called()


async def test_invalid_scope_is_refused_before_api_call() -> None:
    tool, adapter = make_validating_tool()

    with pytest.raises(ExecutionError, match="Unknown scope"):
        await tool.execute(make_input(scope="nonexistent-scope"), NoteContext())

    adapter.create_issue.assert_not_called()


async def test_invalid_priority_is_refused_before_api_call() -> None:
    tool, adapter = make_validating_tool()

    with pytest.raises(ExecutionError, match="Unknown priority"):
        await tool.execute(make_input(priority="ultra-critical"), NoteContext())

    adapter.create_issue.assert_not_called()


async def test_title_too_long_is_refused_before_api_call() -> None:
    tool, adapter = make_validating_tool()

    with pytest.raises(ExecutionError, match="Title too long"):
        await tool.execute(make_input(title="X" * 200), NoteContext())

    adapter.create_issue.assert_not_called()


async def test_milestone_accepted_when_milestones_yaml_is_empty() -> None:
    dependencies = load_issue_tool_dependencies()
    empty_milestones = MilestoneConfig(version="1.0.0", milestones=[])
    adapter = MagicMock()
    manager = GitHubManager(
        adapter=adapter,
        issue_config=dependencies["issue_config"],
        label_config=dependencies["label_config"],
        scope_config=dependencies["scope_config"],
        milestone_config=empty_milestones,
        contributor_config=dependencies["contributor_config"],
        git_config=dependencies["git_config"],
    )
    tool = CreateIssueTool(
        manager=manager,
        issue_config=dependencies["issue_config"],
        milestone_config=empty_milestones,
        contracts_config=dependencies["contracts_config"],
        label_config=dependencies["label_config"],
        scope_config=dependencies["scope_config"],
        git_config=dependencies["git_config"],
    )
    issue_mock = MagicMock()
    issue_mock.number = 11
    issue_mock.html_url = "http://x"
    issue_mock.title = "Milestone ok"
    issue_mock.body = "body"
    issue_mock.state = "open"
    issue_mock.labels = []
    issue_mock.milestone = None
    issue_mock.assignees = []
    issue_mock.created_at = datetime.datetime.now(datetime.UTC)
    issue_mock.updated_at = datetime.datetime.now(datetime.UTC)
    issue_mock.closed_at = None
    issue_mock.user.login = "user"

    adapter.create_issue.return_value = issue_mock
    adapter.get_issue.return_value = issue_mock

    result = await tool.execute(make_input(milestone="any-future-milestone"), NoteContext())

    assert result.success is True
    assert result.number == 11
