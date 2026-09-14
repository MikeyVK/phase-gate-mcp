"""Exercise PR body behavior through public template and native Markdown seams."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError as ContextError
from pydantic import JsonValue

from mcp_server.core.interfaces.artifact_header_reader import HeaderReadStatus
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from tests.mcp_server.fixtures.delivered_templates import DeliveredTemplate, load_delivered_template
from tests.mcp_server.integration.adapters.test_markdown_preflight import (
    MarkdownPackage,
    invoke,
    markdown_package,
    request,
)

__all__ = ["markdown_package"]


@pytest.fixture
def pull_request(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=suite,
        source_package=suite / "pr",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "explicit suite",
        template_id="pr",
    )
    selected = delivered.catalog.get("pr")
    assert selected.policy.persistence == "workspace"
    assert dict(delivered.checks.profiles)[selected.policy.output_profile].checks == (
        "markdown_body",
    )
    return delivered


def test_minimal_pr_keeps_saved_header_and_explicit_none_declaration(
    pull_request: DeliveredTemplate,
    markdown_package: MarkdownPackage,
    tmp_path: Path,
) -> None:
    context: dict[str, JsonValue] = {"changes": "", "deferred_work": []}
    before = deepcopy(context)
    output = pull_request.renderer.render("pr", context, pull_request.provenance)
    assert context == before
    assert not any(line.startswith("# ") for line in output.splitlines())
    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "pr"
    body_lines = output.splitlines()[1:]
    assert any(line.strip() and not line.startswith("#") for line in body_lines)
    assert not any(line.startswith("- [") for line in body_lines)
    code, response = invoke(
        markdown_package,
        tmp_path,
        {**request(tmp_path / "pr.md", output), "operation": "body"},
    )
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "pr.md").exists()


def test_pr_preserves_changes_deferred_groups_check_states_and_issue_identity(
    pull_request: DeliveredTemplate,
) -> None:
    context: dict[str, JsonValue] = {
        "changes": "First change paragraph.\n\nSecond change paragraph.",
        "summary": "Caller summary.",
        "testing": "Observed evidence: [run](run.log).",
        "breaking_changes": "Caller compatibility declaration.",
        "deferred_work": [
            {
                "description": "Follow up #",
                "rationale": "First rationale.",
                "references": [{"label": "Decision", "target": "design.md#Boundary"}],
            },
            {"description": "Later item", "rationale": "", "references": []},
            {"description": "Unlinked item", "rationale": ""},
        ],
        "checklist": [
            {"text": "Complete check", "checked": True},
            {"text": "Pending check", "checked": False},
        ],
        "closes": [42.0, 7],
        "related_docs": [
            {"label": "Plan [review]", "target": "plan.md#Review"},
            {"label": "Self", "target": "#Own-Context"},
        ],
    }
    before = deepcopy(context)
    output = pull_request.renderer.render("pr", context, pull_request.provenance)
    assert context == before
    for key in ("changes", "summary", "testing", "breaking_changes"):
        value = context[key]
        assert isinstance(value, str) and value in output
    assert "- [x] Complete check" in output and "- [ ] Pending check" in output
    assert "#42" in output and "#42.0" not in output
    assert output.index("#42") < output.index("#7")
    assert r"### Follow up \#" in output
    first = output.split("Follow up", 1)[1].split("Later item", 1)[0]
    second = output.split("Later item", 1)[1].split("Unlinked item", 1)[0]
    assert "First rationale." in first and "First rationale." not in second
    assert "[Decision](<design.md#Boundary>)" in first
    assert r"[Plan \[review\]][related-1]" in output
    assert "[Self][related-2]" in output
    for identity, target in (("related-1", "plan.md#Review"), ("related-2", "#Own-Context")):
        assert output.count(f"[{identity}]") == 2
        assert output.count(f"[{identity}]: <{target}>") == 1
    absent = deepcopy(context)
    items = absent["deferred_work"]
    assert isinstance(items, list)
    item = items[1]
    assert isinstance(item, dict)
    del item["references"]
    rendered = pull_request.renderer.render("pr", absent, pull_request.provenance)
    assert rendered.split() != output.split()


def test_pr_explicit_empty_optional_fields_remain_structural(
    pull_request: DeliveredTemplate,
) -> None:
    base: dict[str, JsonValue] = {"changes": "", "deferred_work": []}
    absent = pull_request.renderer.render("pr", base, pull_request.provenance)
    explicit: dict[str, JsonValue] = {
        **base,
        "summary": "",
        "testing": "",
        "breaking_changes": "",
        "checklist": [],
        "closes": [],
        "related_docs": [],
    }
    output = pull_request.renderer.render("pr", explicit, pull_request.provenance)
    assert output.count("\n## ") - absent.count("\n## ") == len(explicit) - len(base)
    assert not any(line.startswith("- [") for line in output.splitlines())


def test_pr_rejects_missing_declarations_legacy_shapes_and_publication_metadata(
    pull_request: DeliveredTemplate,
) -> None:
    base: dict[str, JsonValue] = {"changes": "", "deferred_work": []}
    invalid: list[dict[str, JsonValue]] = [
        {"changes": ""},
        {"deferred_work": []},
        {**base, "changes": None},
        {**base, "deferred_work": ["Primitive deferred item"]},
        {**base, "deferred_work": [{"description": "Missing rationale"}]},
        {**base, "deferred_work": [{"description": "Item", "rationale": "", "tracking_issue": 42}]},
        {**base, "tracking_state": "none"},
        {**base, "has_deferred": False},
        {**base, "checklist_items": []},
        {**base, "closes_issues": [42]},
        {**base, "checklist": ["Primitive checklist"]},
        {**base, "closes": ["#42"]},
        {**base, "closes": [0]},
        {**base, "title": "External title"},
    ]
    for context in invalid:
        with pytest.raises(ContextError):
            pull_request.renderer.render("pr", context, pull_request.provenance)
