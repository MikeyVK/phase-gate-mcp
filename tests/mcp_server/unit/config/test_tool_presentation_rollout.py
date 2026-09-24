# tests/mcp_server/unit/config/test_tool_presentation_rollout.py
# template=unit_test version=8825c0bb created=2026-08-21T22:59Z updated=2026-08-22
"""Approved tool-presentation rollout contract tests.

@layer: Tests (Unit)
@dependencies: [pyyaml, presentation_config, text_presenter, tool_outputs]
@responsibilities:
    - Verify current declarative presentation mechanics
    - Verify representative nested and inline output
"""

from __future__ import annotations

import string
from pathlib import Path
from typing import TypeAlias

import yaml

from mcp_server.config.schemas.presentation_config import (
    CollectionPresentationConfig,
    PresentationConfig,
)
from mcp_server.presenters.text_presenter import TextPresenter
from mcp_server.schemas.tool_outputs import (
    HealthCheckOutput,
    HealthStatus,
    IssueOutput,
    IssueSummaryDTO,
    ListIssuesOutput,
    PhaseDTO,
    PhaseTaskDTO,
    ProjectPlanOutput,
    PROutput,
)

_REPO_ROOT = Path(__file__).parents[4]
_PRESENTATION_PATH = _REPO_ROOT / ".pgmcp" / "config" / "presentation.yaml"

PlaceholderSet: TypeAlias = frozenset[str]
CollectionExpectation: TypeAlias = tuple[str, PlaceholderSet, tuple[str, PlaceholderSet] | None]


def _placeholders(template: str) -> PlaceholderSet:
    return frozenset(
        field_name.split(".")[0].split("[")[0]
        for _, field_name, _, _ in string.Formatter().parse(template)
        if field_name is not None
    )


def _load_config() -> PresentationConfig:
    raw = yaml.safe_load(_PRESENTATION_PATH.read_text(encoding="utf-8"))
    return PresentationConfig.model_validate(raw)


def _collection_shape(
    declaration: CollectionPresentationConfig,
) -> CollectionExpectation:
    child = None
    if declaration.children:
        nested = declaration.children[0]
        child = (nested.field, _placeholders(nested.item_template))
    return declaration.field, _placeholders(declaration.item_template), child


_MECHANICS: dict[str, tuple[int, tuple[CollectionExpectation, ...]]] = {
    "transition_cycle": (20, (("skipped_gates", frozenset({"item"}), None),)),
    "force_cycle_transition": (20, (("skipped_gates", frozenset({"item"}), None),)),
    "get_work_context": (20, ()),
    "initialize_project": (
        20,
        (
            ("required_phases", frozenset({"item"}), None),
            ("files_created", frozenset({"item"}), None),
        ),
    ),
    "get_project_plan": (
        10,
        (
            (
                "phases",
                frozenset({"name", "status"}),
                ("tasks", frozenset({"id", "title", "status"})),
            ),
        ),
    ),
    "save_planning_deliverables": (
        10,
        (("cycles", frozenset({"cycle_number", "deliverables_count"}), None),),
    ),
    "update_planning_deliverables": (
        10,
        (("cycles", frozenset({"cycle_number", "deliverables_count"}), None),),
    ),
    "transition_phase": (20, (("skipped_gates", frozenset({"item"}), None),)),
    "force_phase_transition": (20, (("skipped_gates", frozenset({"item"}), None),)),
    "git_list_branches": (
        20,
        (("branches", frozenset({"name", "is_current", "upstream"}), None),),
    ),
    "git_status": (
        20,
        (
            ("modified_files", frozenset({"item"}), None),
            ("untracked_files", frozenset({"item"}), None),
        ),
    ),
    "git_add_or_commit": (20, (("files", frozenset({"item"}), None),)),
    "git_restore": (20, (("files", frozenset({"item"}), None),)),
    "git_stash": (10, (("stashes", frozenset({"item"}), None),)),
    "create_issue": (10, ()),
    "update_issue": (10, ()),
    "get_issue": (10, ()),
    "list_issues": (
        10,
        (
            (
                "issues",
                frozenset(
                    {
                        "number",
                        "title",
                        "state",
                        "html_url",
                        "labels",
                        "assignees_summary",
                        "created_at",
                    }
                ),
                None,
            ),
        ),
    ),
    "list_prs": (
        10,
        (
            (
                "pull_requests",
                frozenset({"number", "title", "state", "html_url", "base_ref", "head_ref"}),
                None,
            ),
        ),
    ),
    "list_labels": (
        10,
        (("labels", frozenset({"name", "color", "description"}), None),),
    ),
    "add_labels": (10, ()),
    "remove_labels": (10, ()),
    "list_milestones": (
        10,
        (("milestones", frozenset({"number", "title", "state"}), None),),
    ),
}

_INLINE_SEQUENCE_FIELDS = {
    "get_work_context": "valid_phases",
    "create_issue": "labels",
    "update_issue": "labels",
    "get_issue": "labels",
    "add_labels": "labels",
    "remove_labels": "labels",
}


class TestToolPresentationRollout:
    """Verify approved presentation mechanics without wording snapshots."""

    def test_matches_approved_mechanics_matrix(self) -> None:
        config = _load_config()

        for tool_name, (max_items, collections) in _MECHANICS.items():
            tool = config.tools[tool_name]
            assert tool.max_items == max_items, tool_name
            assert tuple(_collection_shape(item) for item in tool.collections) == collections, (
                tool_name
            )

        for tool_name, field in _INLINE_SEQUENCE_FIELDS.items():
            tool = config.tools[tool_name]
            templates = [tool.template_success or ""]
            templates.extend(
                case_template
                for enum_case in tool.enum_cases
                for case_template in enum_case.cases.values()
            )
            assert any(field in _placeholders(template) for template in templates), tool_name

    def test_renders_nested_project_plan_in_source_order(self) -> None:
        presenter = TextPresenter(config=_load_config())
        output = ProjectPlanOutput(
            issue_number=456,
            workflow_name="feature",
            phases=[
                PhaseDTO(
                    name="research",
                    status="complete",
                    tasks=[
                        PhaseTaskDTO(id="R1", title="Map boundaries", status="complete"),
                        PhaseTaskDTO(id="R2", title="Approve strategy", status="complete"),
                    ],
                ),
                PhaseDTO(
                    name="design",
                    status="active",
                    tasks=[PhaseTaskDTO(id="D1", title="Define model", status="active")],
                ),
            ],
        )

        text = presenter.present_text("get_project_plan", output)

        markers = ["research", "R1", "R2", "design", "D1"]
        positions = [text.index(marker) for marker in markers]
        assert positions == sorted(positions)

    def test_renders_nested_issue_labels_without_python_repr(self) -> None:
        presenter = TextPresenter(config=_load_config())
        output = ListIssuesOutput(
            issues_count=1,
            issues=[
                IssueSummaryDTO(
                    number=456,
                    title="Compact output",
                    state="open",
                    html_url="https://example.invalid/issues/456",
                    labels=["feature", "priority:high", "presentation"],
                    assignees_summary="agent",
                    created_at="2026-08-22",
                )
            ],
        )

        text = presenter.present_text("list_issues", output)

        assert "feature, priority:high, presentation" in text
        assert "['feature'" not in text

    def test_expands_issue_and_pr_details(self) -> None:
        presenter = TextPresenter(config=_load_config())
        issue = IssueOutput(
            number=456,
            title="Compact output",
            state="open",
            milestone_title="M1",
            assignees_summary="agent",
            html_url="https://example.invalid/issues/456",
            body="Issue body",
            labels=["feature"],
            created_at="2026-08-22",
            updated_at="2026-08-22",
            author="owner",
        )
        pull_request = PROutput(
            number=99,
            title="Compact output",
            html_url="https://example.invalid/pull/99",
            state="open",
            base_ref="main",
            head_ref="feature/456",
            body="PR body",
        )

        issue_text = presenter.present_text("get_issue", issue)
        pr_text = presenter.present_text("get_pr", pull_request)

        for value in ("Issue body", "feature", issue.html_url, issue.created_at):
            assert value in issue_text
        for value in ("PR body", "open", pull_request.html_url):
            assert value in pr_text

    def test_retains_health_check_identity_below_budget(self) -> None:
        presenter = TextPresenter(config=_load_config())
        output = HealthCheckOutput(
            status=HealthStatus.HEALTHY,
            version="1.2.3",
            pid=42,
            platform="test",
            uptime_seconds=3.5,
        )

        text = presenter.present_text("health_check", output)

        assert text == (
            "📋 **Server Health Status**\n"
            "- Status: healthy\n"
            "- Version: 1.2.3\n"
            "- Process ID: 42\n"
            "- Platform: test\n"
            "- Uptime: 3.5 seconds\n"
        )
