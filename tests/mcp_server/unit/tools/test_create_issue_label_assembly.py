"""
Cycle 5 — Label assembly in CreateIssueTool.

Tests public issue creation and the labels forwarded to GitHubManager.

@layer: Tests (Unit)
@dependencies: [pytest, unittest.mock, mcp_server.tools.issue_tools]
"""

from typing import cast
from unittest.mock import MagicMock

import pytest

from mcp_server.core.operation_notes import NoteContext
from mcp_server.schemas.github_models import IssueReadModel
from mcp_server.tools.issue_tools import CreateIssueInput, CreateIssueTool
from tests.mcp_server.test_support import make_create_issue_tool

pytestmark = pytest.mark.asyncio

BODY = "## Problem\n\nTest problem."


def make_params(**overrides: object) -> CreateIssueInput:
    base = {
        "issue_type": "feature",
        "title": "Test issue",
        "priority": "medium",
        "scope": "mcp-server",
        "body": BODY,
    }
    base.update(overrides)
    return CreateIssueInput(**base)


def make_tool(manager: MagicMock | None = None) -> CreateIssueTool:
    mgr = manager or MagicMock()
    mgr.create_issue.return_value = {"number": 1, "title": "T", "url": ""}
    mock_issue_read = IssueReadModel(
        number=1,
        url="http://github.com/issues/1",
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
    mgr.get_issue.return_value = mock_issue_read
    return make_create_issue_tool(mgr)


async def assembled_labels(params: CreateIssueInput) -> list[str]:
    """Observe labels submitted by the public issue-creation operation."""
    manager = MagicMock()
    tool = make_tool(manager)
    result = await tool.execute(params, NoteContext())
    assert result.success is True
    manager.create_issue.assert_called_once()
    return cast(list[str], manager.create_issue.call_args.kwargs["labels"])


class TestTypeLabelAssembly:
    async def test_feature_produces_type_feature(self) -> None:
        labels = await assembled_labels(make_params(issue_type="feature"))
        assert "type:feature" in labels

    async def test_bug_produces_type_bug(self) -> None:
        labels = await assembled_labels(make_params(issue_type="bug"))
        assert "type:bug" in labels

    async def test_hotfix_produces_type_bug_not_type_hotfix(self) -> None:
        labels = await assembled_labels(make_params(issue_type="hotfix"))
        assert "type:bug" in labels
        assert "type:hotfix" not in labels

    async def test_chore_produces_type_chore(self) -> None:
        labels = await assembled_labels(make_params(issue_type="chore"))
        assert "type:chore" in labels

    async def test_is_epic_overrides_type_to_type_epic(self) -> None:
        labels = await assembled_labels(make_params(issue_type="feature", is_epic=True))
        assert "type:epic" in labels
        assert "type:feature" not in labels

    async def test_is_epic_overrides_any_issue_type(self) -> None:
        labels = await assembled_labels(make_params(issue_type="bug", is_epic=True))
        assert "type:epic" in labels
        assert "type:bug" not in labels

    async def test_no_duplicate_type_labels(self) -> None:
        labels = await assembled_labels(make_params(issue_type="feature"))
        type_labels = [label for label in labels if label.startswith("type:")]
        assert len(type_labels) == 1


class TestScopeLabelAssembly:
    async def test_scope_mcp_server_produces_scope_mcp_server(self) -> None:
        labels = await assembled_labels(make_params(scope="mcp-server"))
        assert "scope:mcp-server" in labels

    async def test_scope_tooling_produces_scope_tooling(self) -> None:
        labels = await assembled_labels(make_params(scope="tooling"))
        assert "scope:tooling" in labels

    async def test_scope_platform_produces_scope_platform(self) -> None:
        labels = await assembled_labels(make_params(scope="platform"))
        assert "scope:platform" in labels


class TestPriorityLabelAssembly:
    async def test_priority_medium_produces_priority_medium(self) -> None:
        labels = await assembled_labels(make_params(priority="medium"))
        assert "priority:medium" in labels

    async def test_priority_high_produces_priority_high(self) -> None:
        labels = await assembled_labels(make_params(priority="high"))
        assert "priority:high" in labels

    async def test_priority_critical_produces_priority_critical(self) -> None:
        labels = await assembled_labels(make_params(priority="critical"))
        assert "priority:critical" in labels


class TestPhaseLabelAssembly:
    async def test_feature_workflow_first_phase_is_research(self) -> None:
        labels = await assembled_labels(make_params(issue_type="feature"))
        assert "phase:research" in labels

    async def test_hotfix_workflow_first_phase_is_implementation(self) -> None:
        labels = await assembled_labels(make_params(issue_type="hotfix"))
        assert "phase:implementation" in labels

    async def test_docs_workflow_first_phase_is_planning(self) -> None:
        labels = await assembled_labels(make_params(issue_type="docs"))
        assert "phase:planning" in labels

    async def test_bug_workflow_first_phase_is_research(self) -> None:
        labels = await assembled_labels(make_params(issue_type="bug"))
        assert "phase:research" in labels

    async def test_chore_workflow_first_phase_is_research(self) -> None:
        labels = await assembled_labels(make_params(issue_type="chore"))
        assert "phase:research" in labels

    async def test_no_duplicate_phase_labels(self) -> None:
        labels = await assembled_labels(make_params(issue_type="feature"))
        phase_labels = [label for label in labels if label.startswith("phase:")]
        assert len(phase_labels) == 1


class TestParentLabelAssembly:
    async def test_parent_issue_produces_parent_n_label(self) -> None:
        labels = await assembled_labels(make_params(parent_issue=91))
        assert "parent:91" in labels

    async def test_parent_issue_none_produces_no_parent_label(self) -> None:
        labels = await assembled_labels(make_params(parent_issue=None))
        assert not any(label.startswith("parent:") for label in labels)

    async def test_parent_issue_different_value(self) -> None:
        labels = await assembled_labels(make_params(parent_issue=149))
        assert "parent:149" in labels


class TestFullLabelSet:
    async def test_minimal_input_produces_four_labels(self) -> None:
        labels = await assembled_labels(make_params())
        assert len(labels) == 4

    async def test_with_parent_issue_produces_five_labels(self) -> None:
        labels = await assembled_labels(make_params(parent_issue=10))
        assert len(labels) == 5

    async def test_full_label_set_no_duplicates(self) -> None:
        labels = await assembled_labels(
            make_params(issue_type="bug", priority="high", scope="platform", parent_issue=55)
        )
        assert len(labels) == len(set(labels))
