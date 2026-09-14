"""Exercise the delivered Research package and its explicit authored content."""

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
def research(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=suite, source_package=suite / "research",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "explicit suite", template_id="research",
    )
    selected = delivered.catalog.get("research")
    assert selected.policy.persistence == "workspace"
    assert dict(delivered.checks.profiles)[selected.policy.output_profile].checks == (
        "markdown_document",
    )
    return delivered


def test_minimal_research_is_a_valid_initial_basis_without_invented_completion(
    research: DeliveredTemplate, markdown_package: MarkdownPackage, tmp_path: Path
) -> None:
    context: dict[str, JsonValue] = {
        "title": "Investigate behavior", "problem_statement": "Observed mismatch.", "goals": [],
    }
    before = deepcopy(context)
    output = research.renderer.render("research", context, research.provenance)
    assert context == before
    assert output.count("\n# ") == 1 and "# Investigate behavior" in output
    assert "## Problem Statement" in output and "Observed mismatch." in output
    assert "## Goals" in output
    for absent in (
        "## Background", "## Findings", "## Questions", "## References", "## Approved Strategy",
        "## Expected Results", "## Evidence", "## Consumers", "## Risks", "## Assumptions",
        "## Related Documents", "**Status:**", "Version History", "Initial draft",
    ):
        assert absent not in output
    assert "\n---\n" not in output
    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "research"
    target = tmp_path / "research.md"
    code, response = invoke(markdown_package, tmp_path, request(target, output))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not target.exists()


def test_all_research_carriers_keep_authored_strategy_evidence_and_distinct_links(
    research: DeliveredTemplate, markdown_package: MarkdownPackage, tmp_path: Path
) -> None:
    context: dict[str, JsonValue] = {
        "title": "Boundary research", "problem_statement": "Caller-observed problem.",
        "goals": ["Observe the boundary", "Compare transition costs"],
        "status": "DRAFT — awaiting review", "version": "2.4", "last_updated": "2026-09-14",
        "purpose": "**Caller purpose**", "scope_in": "Included boundary", "scope_out": "Excluded work",
        "prerequisites": ["Read the contract"],
        "related_docs": [{"label": "Related design", "target": "design.md#Boundary"}],
        "background": "Authored background.\n\nSecond paragraph.", "findings": "Observed findings.",
        "questions": ["What remains unknown?", "Which consumer changes?"],
        "references": [{"label": "External source", "target": "source.md#Evidence"},
                       {"label": "Self fragment", "target": "#Caller-Anchor"}],
        "approved_strategy": "Human supplied: preserve this boundary during migration.",
        "expected_results": "Caller-defined observable result.",
        "evidence": [
            {"claim": "The consumer reaches the boundary", "observation": "Observed caller behavior",
             "sources": [{"label": "Trace source", "target": "trace.md#Recorded"}],
             "invocation": "caller-command --selected-case", "observed_result": "Recorded exit 0",
             "observed_at": "2026-09-14T10:20:30Z"},
            {"claim": "Unobtained observation", "observation": "", "sources": []},
        ],
        "consumers": [{"name": "Boundary reader", "responsibility": "Read the supplied record",
                       "impact": "Explicit migration impact"}],
        "risks": [
            {"description": "Known transition risk", "mitigation": "Caller mitigation",
             "consequence": "Caller consequence"},
            {"description": "Another bounded risk", "mitigation": ""},
        ],
        "assumptions": ["Assumed external precondition"],
    }
    before = deepcopy(context)
    output = research.renderer.render("research", context, research.provenance)
    assert context == before
    for supplied in (
        "Caller-observed problem.", "Observe the boundary", "Compare transition costs",
        "DRAFT — awaiting review", "2.4", "2026-09-14", "**Caller purpose**",
        "Included boundary", "Excluded work", "Read the contract",
        "Authored background.\n\nSecond paragraph.", "Observed findings.",
        "What remains unknown?", "Which consumer changes?",
        "Human supplied: preserve this boundary during migration.",
        "Caller-defined observable result.", "The consumer reaches the boundary",
        "Observed caller behavior", "caller-command --selected-case", "Recorded exit 0",
        "2026-09-14T10:20:30Z", "Unobtained observation", "Boundary reader",
        "Read the supplied record", "Explicit migration impact", "Known transition risk",
        "Caller mitigation", "Caller consequence", "Another bounded risk",
        "Assumed external precondition",
    ):
        assert supplied in output, supplied
    assert output.index("Observe the boundary") < output.index("Compare transition costs")
    assert output.index("What remains unknown?") < output.index("Which consumer changes?")
    assert "## References" in output and "## Related Documents" in output
    assert "[External source](<source.md#Evidence>)" in output
    assert "[Related design](<design.md#Boundary>)" in output
    assert "[Self fragment](<#Caller-Anchor>)" in output
    assert "[Trace source](<trace.md#Recorded>)" in output
    assert output.count("\n# ") == 1
    code, response = invoke(markdown_package, tmp_path, request(tmp_path / "populated.md", output))
    assert code == 0 and response["decision"] == {"status": "passed"}


def test_explicit_empty_sections_remain_visible_without_placeholders(
    research: DeliveredTemplate,
) -> None:
    context: dict[str, JsonValue] = {
        "title": "Initial skeleton", "problem_statement": "Known problem.", "goals": [],
        "purpose": "", "scope_in": "", "scope_out": "", "prerequisites": [], "related_docs": [],
        "background": "", "findings": "", "questions": [], "references": [],
        "approved_strategy": "", "expected_results": "", "evidence": [],
        "consumers": [], "risks": [], "assumptions": [],
    }
    output = research.renderer.render("research", context, research.provenance)
    for heading in (
        "Purpose", "Scope In", "Scope Out", "Prerequisites", "Related Documents", "Background",
        "Findings", "Questions", "References", "Approved Strategy", "Expected Results",
        "Evidence", "Consumers", "Risks", "Assumptions", "Goals",
    ):
        assert f"## {heading}" in output
    assert not any(line.startswith("- ") for line in output.splitlines())
    for invented in ("None", "To be defined", "Initial draft", "**Status:**", "Agent"):
        assert invented not in output


def test_schema_rejects_legacy_aliases_primitive_records_and_invalid_presence(
    research: DeliveredTemplate,
) -> None:
    base: dict[str, JsonValue] = {"title": "Research", "problem_statement": "Problem", "goals": []}
    evidence: dict[str, JsonValue] = {"claim": "Claim", "observation": "", "sources": []}
    invalid: list[dict[str, JsonValue]] = [
        {"title": "Research", "problem_statement": "Problem"}, {**base, "title": ""},
        {**base, "problem_statement": ""}, {**base, "goals": "Goal"},
        {**base, "goals": [""]}, {**base, "status": ""}, {**base, "background": None},
        {**base, "questions_list": []}, {**base, "open_questions": []},
        {**base, "workflow": "inferred"}, {**base, "approved_strategy": True},
        {**base, "references": ["[Source](source.md)"]},
        {**base, "last_updated": "tomorrow"},
        {**base, "evidence": [{**evidence, "observed_at": "yesterday"}]},
        {**base, "evidence": [{"claim": "Claim", "observation": ""}]},
        {**base, "evidence": [{**evidence, "approval": True}]},
        {**base, "evidence": [{**evidence, "sources": [{"target": "source.md"}]}]},
        {**base, "consumers": [{"name": "Reader", "responsibility": ""}]},
        {**base, "risks": [{"description": "Risk"}]},
        {**base, "risks": [{"description": "Risk", "mitigation": "", "probability": 0}]},
    ]
    for context in invalid:
        with pytest.raises(ContextError):
            research.renderer.render("research", context, research.provenance)
