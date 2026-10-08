"""Exercise Issue body behavior through public template."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError as ContextError
from pydantic import JsonValue

from mcp_server.core.interfaces.artifact_header_reader import HeaderReadStatus
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from tests.mcp_server.fixtures.delivered_templates import DeliveredTemplate, load_delivered_template


@pytest.fixture
def issue(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=suite,
        source_package=suite / "issue",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "explicit suite",
        template_id="issue",
    )
    selected = delivered.catalog.get("issue")
    assert selected.policy.persistence == "workspace"
    return delivered


def test_minimal_issue_body_has_no_h1_and_keeps_saved_header(
    issue: DeliveredTemplate,
) -> None:
    context: dict[str, JsonValue] = {"problem": "Observed problem marker."}
    before = deepcopy(context)
    output = issue.renderer.render("issue", context, issue.provenance)
    assert context == before
    assert not any(line.startswith("# ") for line in output.splitlines())
    problem = context["problem"]
    assert isinstance(problem, str) and problem in output

    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "issue"


def test_issue_preserves_optional_values_order_and_related_reference_namespace(
    issue: DeliveredTemplate,
) -> None:
    context: dict[str, JsonValue] = {
        "problem": "Observed problem marker.",
        "summary": "Summary marker.",
        "expected": "Expected marker.",
        "actual": "Actual marker.",
        "context": "Context marker.\nSecond line.",
        "reproduction_steps": ["first step\ncontinued", "second step"],
        "related_docs": [
            {"label": "Spec | marker", "target": "docs/[spec].md#Part A"},
            {"label": "Self marker", "target": "#Caller-Anchor"},
        ],
    }
    before = deepcopy(context)
    output = issue.renderer.render("issue", context, issue.provenance)
    assert context == before

    for key in ("summary", "expected", "actual", "context"):
        value = context[key]
        assert isinstance(value, str) and value in output
    assert "1. first step\n   continued" in output and "2. second step" in output
    assert output.index("first step") < output.index("second step")
    assert "[Spec &#124; marker][related-1]" in output
    assert "[Self marker][related-2]" in output
    assert "[related-1]: <docs/[spec].md#Part A>" in output
    assert "[related-2]: <#Caller-Anchor>" in output
    assert output.count("[related-1]") == 2
    assert output.count("[related-2]") == 2


def test_issue_absent_and_explicit_empty_optional_fields_remain_distinct(
    issue: DeliveredTemplate,
) -> None:
    base: dict[str, JsonValue] = {"problem": "Observed problem marker."}
    absent = issue.renderer.render("issue", base, issue.provenance)
    explicit: dict[str, JsonValue] = {
        **base,
        "summary": "",
        "expected": "",
        "actual": "",
        "context": "",
        "reproduction_steps": [],
        "related_docs": [],
    }
    before = deepcopy(explicit)
    populated = issue.renderer.render("issue", explicit, issue.provenance)
    assert explicit == before
    assert populated.count("\n## ") - absent.count("\n## ") == len(explicit) - len(base)


def test_issue_rejects_invalid_body_context(issue: DeliveredTemplate) -> None:
    base: dict[str, JsonValue] = {"problem": "Problem"}
    invalid: list[dict[str, JsonValue]] = [
        {},
        {"problem": ""},
        {"problem": None},
        {**base, "summary": None},
        {**base, "steps_to_reproduce": ["legacy"]},
        {**base, "related_docs": ["Primitive link"]},
        {**base, "related_docs": [{"label": "Missing target"}]},
        {**base, "reproduction_steps": "Scalar steps"},
        {**base, "title": "External title"},
        {**base, "labels": ["External metadata"]},
        {**base, "issue_number": 42},
    ]
    for context in invalid:
        with pytest.raises(ContextError):
            issue.renderer.render("issue", context, issue.provenance)
