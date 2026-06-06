# pyright: reportCallIssue=false, reportAttributeAccessIssue=false
"""
Cycle 4 — CreateIssueInput schema refactor.

Tests:
- All required fields (issue_type, title, priority, scope, body)
- Structural validation only; semantic validation moved to GitHubManager
- Optional fields: is_epic, parent_issue, milestone, assignees
- body is a pre-rendered markdown string

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.tools.issue_tools]
"""

import pytest
from pydantic import ValidationError

from mcp_server.tools.issue_tools import CreateIssueInput

VALID_BODY = "## Problem\n\nThe tool crashes on startup."

VALID_MINIMAL: dict[str, object] = {
    "issue_type": "feature",
    "title": "Add structured issue creation",
    "priority": "medium",
    "scope": "mcp-server",
    "body": VALID_BODY,
}


class TestCreateIssueInputRequired:
    def test_all_required_fields_accepted(self) -> None:
        inp = CreateIssueInput(**VALID_MINIMAL)
        assert inp.issue_type == "feature"
        assert inp.title == "Add structured issue creation"
        assert inp.priority == "medium"
        assert inp.scope == "mcp-server"
        assert inp.body == VALID_BODY

    def test_missing_issue_type_raises(self) -> None:
        data = {key: value for key, value in VALID_MINIMAL.items() if key != "issue_type"}
        with pytest.raises(ValidationError):
            CreateIssueInput(**data)

    def test_missing_title_raises(self) -> None:
        data = {key: value for key, value in VALID_MINIMAL.items() if key != "title"}
        with pytest.raises(ValidationError):
            CreateIssueInput(**data)

    def test_missing_priority_raises(self) -> None:
        data = {key: value for key, value in VALID_MINIMAL.items() if key != "priority"}
        with pytest.raises(ValidationError):
            CreateIssueInput(**data)

    def test_missing_scope_raises(self) -> None:
        data = {key: value for key, value in VALID_MINIMAL.items() if key != "scope"}
        with pytest.raises(ValidationError):
            CreateIssueInput(**data)

    def test_missing_body_raises(self) -> None:
        data = {key: value for key, value in VALID_MINIMAL.items() if key != "body"}
        with pytest.raises(ValidationError):
            CreateIssueInput(**data)


class TestPrimitiveFieldAcceptance:
    def test_unknown_issue_type_is_accepted_structurally(self) -> None:
        inp = CreateIssueInput(**{**VALID_MINIMAL, "issue_type": "nonsense"})
        assert inp.issue_type == "nonsense"

    def test_long_title_is_accepted_structurally(self) -> None:
        title = "A" * 200
        inp = CreateIssueInput(**{**VALID_MINIMAL, "title": title})
        assert inp.title == title

    def test_unknown_priority_is_accepted_structurally(self) -> None:
        inp = CreateIssueInput(**{**VALID_MINIMAL, "priority": "urgent"})
        assert inp.priority == "urgent"

    def test_unknown_scope_is_accepted_structurally(self) -> None:
        inp = CreateIssueInput(**{**VALID_MINIMAL, "scope": "backend"})
        assert inp.scope == "backend"


class TestBodyTypeValidation:
    def test_body_plain_string_accepted(self) -> None:
        inp = CreateIssueInput(**{**VALID_MINIMAL, "body": "## Problem\n\nSomething is broken."})
        assert inp.body == "## Problem\n\nSomething is broken."

    def test_body_dict_rejected(self) -> None:
        with pytest.raises(ValidationError):
            CreateIssueInput(**{**VALID_MINIMAL, "body": {"problem": "Dict input"}})  # type: ignore[arg-type]

    def test_body_none_rejected(self) -> None:
        with pytest.raises(ValidationError):
            CreateIssueInput(**{**VALID_MINIMAL, "body": None})  # type: ignore[arg-type]


class TestOptionalFields:
    def test_is_epic_defaults_to_false(self) -> None:
        inp = CreateIssueInput(**VALID_MINIMAL)
        assert inp.is_epic is False

    def test_is_epic_true_accepted(self) -> None:
        inp = CreateIssueInput(**{**VALID_MINIMAL, "is_epic": True})
        assert inp.is_epic is True

    def test_parent_issue_defaults_to_none(self) -> None:
        inp = CreateIssueInput(**VALID_MINIMAL)
        assert inp.parent_issue is None

    def test_parent_issue_positive_int_accepted(self) -> None:
        inp = CreateIssueInput(**{**VALID_MINIMAL, "parent_issue": 91})
        assert inp.parent_issue == 91

    def test_parent_issue_zero_raises(self) -> None:
        with pytest.raises(ValidationError):
            CreateIssueInput(**{**VALID_MINIMAL, "parent_issue": 0})

    def test_parent_issue_negative_raises(self) -> None:
        with pytest.raises(ValidationError):
            CreateIssueInput(**{**VALID_MINIMAL, "parent_issue": -1})

    def test_milestone_defaults_to_none(self) -> None:
        inp = CreateIssueInput(**VALID_MINIMAL)
        assert inp.milestone is None

    def test_milestone_string_title_accepted(self) -> None:
        inp = CreateIssueInput(**{**VALID_MINIMAL, "milestone": "v2.0"})
        assert inp.milestone == "v2.0"

    def test_assignees_defaults_to_none(self) -> None:
        inp = CreateIssueInput(**VALID_MINIMAL)
        assert inp.assignees is None

    def test_assignees_list_accepted(self) -> None:
        inp = CreateIssueInput(**{**VALID_MINIMAL, "assignees": ["alice", "bob"]})
        assert inp.assignees == ["alice", "bob"]
