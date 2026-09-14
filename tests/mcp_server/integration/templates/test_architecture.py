"""Exercise the delivered Architecture package and explicit authored concepts."""

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
def architecture(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=suite,
        source_package=suite / "architecture",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "explicit suite",
        template_id="architecture",
    )
    selected = delivered.catalog.get("architecture")
    assert selected.policy.persistence == "workspace"
    assert dict(delivered.checks.profiles)[selected.policy.output_profile].checks == (
        "markdown_document",
    )
    return delivered


def test_minimal_architecture_is_a_valid_initial_basis_without_sources(
    architecture: DeliveredTemplate,
    markdown_package: MarkdownPackage,
    tmp_path: Path,
) -> None:
    context: dict[str, JsonValue] = {"title": "Architecture basis", "concepts": []}
    before = deepcopy(context)
    output = architecture.renderer.render("architecture", context, architecture.provenance)
    assert context == before
    assert output.count("\n# ") == 1 and f"# {context['title']}" in output
    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "architecture"
    code, response = invoke(
        markdown_package, tmp_path, request(tmp_path / "architecture.md", output)
    )
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "architecture.md").exists()


def test_architecture_preserves_ordered_concepts_diagrams_decisions_and_links(
    architecture: DeliveredTemplate,
    markdown_package: MarkdownPackage,
    tmp_path: Path,
) -> None:
    context: dict[str, JsonValue] = {
        "title": "Boundary architecture",
        "status": "DRAFT — awaiting review",
        "version": "2.0",
        "last_updated": "2026-09-14",
        "purpose": "Caller-authored purpose.",
        "scope_in": "Included boundary",
        "scope_out": "Excluded systems",
        "prerequisites": ["Read the contract"],
        "related_docs": [{"label": "Self", "target": "#Own-Architecture"}],
        "constraints": ["Keep the public seam"],
        "concepts": [
            {
                "name": "Ingress boundary #",
                "description": "First concept.",
                "diagram": "graph TD\nA --> B\n" + chr(96) * 3 + "\nembedded",
                "subsections": [
                    {"name": "Inputs #", "description": "Accepted inputs."},
                    {"name": "Outputs", "description": "Returned outputs."},
                ],
            },
            {
                "name": "Persistence boundary",
                "description": "Second concept.",
                "diagram": "",
                "subsections": [],
            },
            {"name": "Owner boundary", "description": "Third concept without optional sections."},
        ],
        "decisions": [
            {
                "decision": "Keep the reader #",
                "rationale": "Preserves callers.",
                "alternatives": ["Rewrite all consumers"],
            },
            {"decision": "Defer cleanup", "rationale": "", "alternatives": []},
            {"decision": "Document ownership", "rationale": "No alternatives supplied"},
        ],
        "sources": [
            {"label": "Contract", "target": "contract.md#Boundary"},
            {"label": "Self source", "target": "#Own-Source"},
        ],
    }
    before = deepcopy(context)
    output = architecture.renderer.render("architecture", context, architecture.provenance)
    assert context == before
    for key in ("purpose", "scope_in", "scope_out"):
        value = context[key]
        assert isinstance(value, str) and value in output
    for heading in (
        r"### 1. Ingress boundary \#",
        "### 2. Persistence boundary",
        r"#### Inputs \#",
        "#### Outputs",
    ):
        assert heading in output
    assert r"### Keep the reader \#" in output
    assert "### Defer cleanup" in output
    assert "### Document ownership" in output
    absent = deepcopy(context)
    decisions = absent["decisions"]
    assert isinstance(decisions, list) and isinstance(decisions[1], dict)
    del decisions[1]["alternatives"]
    assert (
        architecture.renderer.render("architecture", absent, architecture.provenance).split()
        != output.split()
    )
    first_concept = output.split("### 1. Ingress boundary", 1)[1].split("### 2.", 1)[0]
    fence = chr(96) * 4
    diagram = "graph TD\nA --> B\n" + chr(96) * 3 + "\nembedded"
    assert fence + "mermaid\n" + diagram + "\n" + fence in first_concept
    assert first_concept.index("#### Inputs") < first_concept.index("#### Outputs")
    third_concept = output.split("### 3. Owner boundary", 1)[1].split("\n## ", 1)[0]
    assert not any(line.startswith("#### ") for line in third_concept.splitlines())
    assert "[Contract](<contract.md#Boundary>)" in output
    assert "[Self source](<#Own-Source>)" in output
    assert "[Self](<#Own-Architecture>)" in output
    assert output.index("Ingress boundary") < output.index("Persistence boundary")
    assert output.index("Keep the reader") < output.index("Defer cleanup")
    assert output.count("\n# ") == 1
    without_decisions = {key: value for key, value in context.items() if key != "decisions"}
    undecided = architecture.renderer.render(
        "architecture", without_decisions, architecture.provenance
    )
    assert "Keep the public seam" in undecided and undecided.split() != output.split()
    code, response = invoke(markdown_package, tmp_path, request(tmp_path / "populated.md", output))
    assert code == 0 and response["decision"] == {"status": "passed"}


def test_architecture_explicit_empty_common_and_concept_capacities_remain_visible(
    architecture: DeliveredTemplate,
) -> None:
    context: dict[str, JsonValue] = {
        "title": "Empty architecture",
        "purpose": "",
        "scope_in": "",
        "scope_out": "",
        "prerequisites": [],
        "related_docs": [],
        "constraints": [],
        "concepts": [
            {"name": "Empty concept", "description": "", "diagram": "", "subsections": []}
        ],
        "decisions": [],
        "sources": [],
    }
    output = architecture.renderer.render("architecture", context, architecture.provenance)
    absent_context: dict[str, JsonValue] = {
        "title": context["title"],
        "concepts": [{"name": "Empty concept", "description": ""}],
    }
    absent = architecture.renderer.render("architecture", absent_context, architecture.provenance)
    assert output.split() != absent.split()
    headings = [line for line in output.splitlines() if line.startswith("## ")]
    absent_headings = [line for line in absent.splitlines() if line.startswith("## ")]
    assert len(headings) - len(absent_headings) == len(context) - len(absent_context)
    assert len(headings) == len(set(headings))
    assert "Empty concept" in output
    fence = chr(96) * 3
    assert fence + "mermaid\n\n" + fence in output


def test_architecture_rejects_closed_and_invalid_concept_records(
    architecture: DeliveredTemplate,
) -> None:
    base: dict[str, JsonValue] = {"title": "Architecture", "concepts": []}
    invalid: list[dict[str, JsonValue]] = [
        {"title": "Architecture"},
        {"title": "", "concepts": []},
        {**base, "constraints": [""]},
        {**base, "concepts": ["Concept"]},
        {**base, "concepts": [{"description": "Missing name"}]},
        {**base, "concepts": [{"name": "Concept", "description": None}]},
        {
            **base,
            "concepts": [
                {
                    "name": "Concept",
                    "description": "",
                    "subsections": [
                        {"name": "Nested", "description": "", "subsections": []},
                    ],
                }
            ],
        },
        {**base, "sources": [{"target": "architecture.md"}]},
        {**base, "decisions": [{"decision": "Decision"}]},
        {**base, "decisions": [{"decision": "Decision", "rationale": "", "unknown": True}]},
        {**base, "workflow": "architecture"},
    ]
    for context in invalid:
        with pytest.raises(ContextError):
            architecture.renderer.render("architecture", context, architecture.provenance)
