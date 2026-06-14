"""Unit tests for pr_tools.py.

@layer: Tests (Unit)
@dependencies: [pytest, unittest.mock, mcp_server.tools.pr_tools]
"""

from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from mcp_server.core.operation_notes import NoteContext
from mcp_server.schemas.github_models import PRReadModel
from mcp_server.schemas.tool_outputs import ListPRsOutput, MergePROutput, PROutput
from mcp_server.tools.pr_tools import (
    GetPRInput,
    GetPRTool,
    ListPRsInput,
    ListPRsTool,
    MergePRInput,
    MergePRTool,
)


@pytest.fixture
def mock_git_config() -> MagicMock:
    git_config = MagicMock()
    git_config.default_base_branch = "main"
    return git_config


@pytest.fixture
def mock_github_manager() -> MagicMock:
    return MagicMock()


@pytest.mark.asyncio
async def test_list_prs_tool(mock_github_manager: MagicMock, mock_git_config: MagicMock) -> None:
    tool = ListPRsTool(manager=mock_github_manager, git_config=mock_git_config)
    # Mock PR objects with minimal attributes
    pr1 = MagicMock(number=10, title="PR 10", state="open")
    pr1.base.ref = "main"
    pr1.head.ref = "feature/10"
    pr1.html_url = "https://github.com/pulls/10"

    mock_github_manager.list_prs.return_value = [pr1]

    params = ListPRsInput(state="open")
    result = await tool.execute(params, NoteContext())

    mock_github_manager.list_prs.assert_called_with(state="open", base=None, head=None)
    assert isinstance(result, ListPRsOutput)
    assert result.success is True
    assert result.prs_count == 1
    assert result.pull_requests[0].number == 10
    assert result.pull_requests[0].title == "PR 10"


@pytest.mark.asyncio
async def test_merge_pr_tool(mock_github_manager: MagicMock, mock_git_config: MagicMock) -> None:
    pr_status_writer = MagicMock()
    tool = MergePRTool(
        manager=mock_github_manager,
        git_config=mock_git_config,
        pr_status_writer=pr_status_writer,
    )
    mock_pr_model = PRReadModel(
        pr_number=20,
        title="Test PR",
        state="open",
        base_branch="main",
        head_branch="feature/20-test",
        merged_at=None,
        merge_sha=None,
        body="",
    )
    mock_github_manager.get_pr.return_value = mock_pr_model
    mock_github_manager.merge_pr.return_value = {"sha": "commitsHA123"}

    params = MergePRInput(pr_number=20, merge_method="merge")
    result = await tool.execute(params, NoteContext())

    mock_github_manager.merge_pr.assert_called_with(
        pr_number=20, commit_message=None, merge_method="merge"
    )
    assert isinstance(result, MergePROutput)
    assert result.success is True
    assert result.pr_number == 20
    assert result.merge_sha == "commitsHA123"
    assert result.merge_method == "merge"


def test_merge_pr_input_rejects_squash() -> None:
    """squash is no longer a valid merge_method."""
    with pytest.raises(ValidationError):
        MergePRInput(pr_number=1, merge_method="squash")


def test_merge_pr_input_rejects_rebase() -> None:
    """rebase is no longer a valid merge_method."""
    with pytest.raises(ValidationError):
        MergePRInput(pr_number=1, merge_method="rebase")


@pytest.mark.asyncio
async def test_get_pr_tool(mock_github_manager: MagicMock) -> None:
    mock_pr_model = PRReadModel(
        pr_number=42,
        title="Test PR",
        state="open",
        base_branch="main",
        head_branch="feature/42-test",
        merged_at=None,
        merge_sha=None,
        body="Some body",
    )
    mock_github_manager.get_pr.return_value = mock_pr_model

    tool = GetPRTool(manager=mock_github_manager)
    params = GetPRInput(pr_number=42)
    result = await tool.execute(params, NoteContext())

    assert isinstance(result, PROutput)
    assert result.success is True
    assert result.number == 42
    assert result.title == "Test PR"
    assert result.head_ref == "feature/42-test"
    assert result.base_ref == "main"
