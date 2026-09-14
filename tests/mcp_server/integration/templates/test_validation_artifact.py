"""Exercise the delivered validation-report package and authored outcome carriers."""

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
def validation_report(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=suite,
        source_package=suite / "validation_report",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "explicit suite",
        template_id="validation_report",
    )
    selected = delivered.catalog.get("validation_report")
    assert selected.policy.persistence == "workspace"
    assert dict(delivered.checks.profiles)[selected.policy.output_profile].checks == (
        "markdown_document",
    )
    return delivered


def test_minimal_validation_report_is_authored_without_invented_outcome(
    validation_report: DeliveredTemplate, markdown_package: MarkdownPackage, tmp_path: Path,
) -> None:
    context: dict[str, JsonValue] = {"title": "Validation basis"}
    before = deepcopy(context)
    output = validation_report.renderer.render(
        "validation_report", context, validation_report.provenance,
    )
    assert context == before
    assert output.count("\n# ") == 1 and "# Validation basis" in output
    for absent in (
        "## Issue Number", "## Cycle", "## Validation Status", "## Scope",
        "## Obligations", "## Evidence", "## Demonstration", "## Preservation",
        "## Containment", "## Failures", "## Caveats", "## Risks", "## Deferred Work",
        "**Status:**", "PASS", "FAIL", "PARTIAL", "Initial draft",
    ):
        assert absent not in output
    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "validation_report"
    code, response = invoke(markdown_package, tmp_path, request(tmp_path / "validation.md", output))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "validation.md").exists()


def test_validation_report_preserves_all_authored_carriers_and_workflow_meanings(
    validation_report: DeliveredTemplate, markdown_package: MarkdownPackage, tmp_path: Path,
) -> None:
    context: dict[str, JsonValue] = {
        "title": "Boundary validation",
        "issue_number": 42.0,
        "cycle": "CY045",
        "validation_status": "PARTIAL",
        "scope": "Validate the delivered boundary.",
        "status": "DRAFT — awaiting review",
        "version": "1.2",
        "last_updated": "2026-09-14",
        "purpose": "Caller-authored validation purpose.",
        "scope_in": "Included surface",
        "scope_out": "Excluded surface",
        "prerequisites": ["Read the approved contract"],
        "related_docs": [{"label": "Design", "target": "design.md#Boundary"}],
        "obligations": [
            {
                "obligation": "Preserve accepted calls #",
                "evidence": [{"label": "Call trace", "target": "trace.md#Calls"}],
                "outcome": "Observed caller evidence.",
            },
            {"obligation": "Review containment", "evidence": []},
            {"obligation": "Review ordering", "evidence": [], "outcome": ""},
        ],
        "evidence": [
            {
                "claim": "The adapter retained the contract #",
                "observation": "Observed native result.",
                "sources": [{"label": "Native log", "target": "run.log#Result"}],
                "invocation": "caller-command --case",
                "observed_result": "Exit 0",
                "observed_at": "2026-09-14T10:20:30.125+02:00",
            },
            {
                "claim": "A second authored observation",
                "observation": "",
                "sources": [{"label": "Self fragment", "target": "#Own-Evidence"}],
            },
            {"claim": "Unobtained evidence", "observation": "", "sources": []},
        ],
        "demonstration": "Caller-visible demonstration.",
        "preservation": "Accepted behavior remains unchanged.",
        "containment": "Unrelated paths were untouched.",
        "failures": ["One expected limitation"],
        "caveats": ["Native duration varies"],
        "risks": [
            {
                "description": "Migration risk #",
                "mitigation": "Retain the bridge until consumers move",
                "consequence": "Temporary duplication",
            },
            {"description": "Unresolved risk", "mitigation": ""},
        ],
        "deferred_work": [
            {
                "description": "Remove the compatibility bridge #",
                "rationale": "A later owner controls cleanup",
                "references": [{"label": "Plan", "target": "planning.md#Cleanup"}],
            },
            {"description": "Deferred detail", "rationale": "", "references": []},
            {"description": "Another follow-up", "rationale": "Explicit later responsibility"},
        ],
    }
    before = deepcopy(context)
    output = validation_report.renderer.render(
        "validation_report", context, validation_report.provenance,
    )
    assert context == before
    for supplied in (
        "#42", "CY045", "PARTIAL", "Validate the delivered boundary.",
        "DRAFT — awaiting review", "1.2", "2026-09-14", "Caller-authored validation purpose.",
        "Included surface", "Excluded surface", "Read the approved contract",
        "Observed native result.", "Review ordering", "Unobtained evidence",
        "Another follow-up", "Explicit later responsibility",
        "Preserve accepted calls", "Call trace", "Observed caller evidence.",
        "The adapter retained the contract", "A second authored observation", "caller-command --case", "Exit 0",
        "2026-09-14T10:20:30.125+02:00", "Caller-visible demonstration.",
        "Accepted behavior remains unchanged.", "Unrelated paths were untouched.",
        "One expected limitation", "Native duration varies", "Migration risk", "Unresolved risk",
        "Retain the bridge until consumers move", "Temporary duplication",
        "Remove the compatibility bridge", "Deferred detail", "A later owner controls cleanup", "Plan",
    ):
        assert supplied in output, supplied
    for heading in (
        "## Issue Number", "## Cycle", "## Validation Status", "## Scope",
        "## Obligations", "## Evidence", "## Demonstration", "## Preservation",
        "## Containment", "## Failures", "## Caveats", "## Risks", "## Deferred Work",
    ):
        assert heading in output
    for heading in (
        r"### Preserve accepted calls \#",
        r"### The adapter retained the contract \#",
        r"### Migration risk \#",
        r"### Remove the compatibility bridge \#",
    ):
        assert heading in output
    assert "[Design](<design.md#Boundary>)" in output
    assert "[Native log](<run.log#Result>)" in output
    assert "[Self fragment](<#Own-Evidence>)" in output
    assert "[Call trace](<trace.md#Calls>)" in output
    assert "[Plan](<planning.md#Cleanup>)" in output
    assert output.count("**References:**") == 2
    assert output.count("**Outcome:**") == 2
    assert "#42.0" not in output
    assert output.index("Preserve accepted calls") < output.index("Review containment")
    assert output.count("\n# ") == 1
    code, response = invoke(markdown_package, tmp_path, request(tmp_path / "populated.md", output))
    assert code == 0 and response["decision"] == {"status": "passed"}


def test_validation_report_explicit_empty_sections_remain_visible(
    validation_report: DeliveredTemplate,
) -> None:
    context: dict[str, JsonValue] = {
        "title": "Empty validation",
        "purpose": "",
        "scope_in": "",
        "scope_out": "",
        "prerequisites": [],
        "related_docs": [],
        "scope": "",
        "obligations": [],
        "evidence": [],
        "demonstration": "",
        "preservation": "",
        "containment": "",
        "failures": [],
        "caveats": [],
        "risks": [],
        "deferred_work": [],
    }
    output = validation_report.renderer.render(
        "validation_report", context, validation_report.provenance,
    )
    headings = [line for line in output.splitlines() if line.startswith("## ")]
    for heading in (
        "Purpose", "Scope In", "Scope Out", "Prerequisites", "Related Documents",
        "Scope", "Obligations", "Evidence", "Demonstration", "Preservation",
        "Containment", "Failures", "Caveats", "Risks", "Deferred Work",
    ):
        assert headings.count(f"## {heading}") == 1
    assert not any(line.startswith("- ") for line in output.splitlines())
    for invented in ("None", "To be defined", "Initial draft", "PASS", "Agent"):
        assert invented not in output


def test_validation_report_rejects_legacy_shapes_and_invalid_carriers(
    validation_report: DeliveredTemplate,
) -> None:
    base: dict[str, JsonValue] = {"title": "Validation"}
    invalid: list[dict[str, JsonValue]] = [
        {},
        {"title": ""},
        {**base, "issue_number": 0},
        {**base, "issue_number": True},
        {**base, "cycle": None},
        {**base, "scope": None},
        {**base, "deferred_work": [{"description": "Work", "rationale": "", "tracking_state": "new"}]},
        {**base, "issue_number": "42"},
        {**base, "issue_number": None},
        {**base, "validation_status": "PASSING"},
        {**base, "last_updated": "2026-09-14\n"},
        {**base, "evidence": [{"claim": "Claim", "observation": "", "sources": [],
                               "observed_at": "yesterday"}]},
        {**base, "evidence": [{"claim": "Claim", "observation": "", "sources": [
            {"target": "run.log"}]}]},
        {**base, "obligations": [{"obligation": "Proof", "evidence": [
            {"label": "Trace", "target": "trace.md"}], "unexpected": True}]},
        {**base, "deferred_work": [{"description": "Cleanup"}]},
        {**base, "workflow": "validation"},
        {**base, "status": ""},
    ]
    for context in invalid:
        with pytest.raises(ContextError):
            validation_report.renderer.render(
                "validation_report", context, validation_report.provenance,
            )
