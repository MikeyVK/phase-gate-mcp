"""Verify the delivered Design package through authored content and native Markdown checks."""

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
def design(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=suite,
        source_package=suite / "design",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "explicit suite",
        template_id="design",
    )
    selected = delivered.catalog.get("design")
    assert selected.policy.persistence == "workspace"
    assert dict(delivered.checks.profiles)[selected.policy.output_profile].checks == (
        "markdown_document",
    )
    return delivered


def test_initial_design_does_not_require_or_invent_a_decision(
    design: DeliveredTemplate, markdown_package: MarkdownPackage, tmp_path: Path
) -> None:
    context: dict[str, JsonValue] = {
        "title": "Design the boundary",
        "problem_statement": "Preserve the caller contract.",
        "requirements_functional": [],
        "requirements_nonfunctional": [],
    }
    before = deepcopy(context)
    output = design.renderer.render("design", context, design.provenance)
    assert context == before
    assert output.count("\n# ") == 1 and "# Design the boundary" in output
    for heading in ("Problem Statement", "Functional Requirements", "Nonfunctional Requirements"):
        assert f"## {heading}" in output
    for absent in (
        "## Options",
        "## Decision",
        "## Rationale",
        "## Key Decisions",
        "## Validation",
        "## Risks",
        "## Related Documents",
        "**Status:**",
        "Version History",
        "Initial draft",
    ):
        assert absent not in output
    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "design"
    target = tmp_path / "design.md"
    code, response = invoke(markdown_package, tmp_path, request(target, output))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not target.exists()


def test_design_preserves_ordered_options_contracts_and_planned_evidence(
    design: DeliveredTemplate, markdown_package: MarkdownPackage, tmp_path: Path
) -> None:
    options: list[JsonValue] = [
        {"name": f"Candidate {index}", "description": f"Authored option {index}."}
        for index in range(1, 12)
    ]
    options[0] = {
        "name": "Candidate 1 #",
        "description": "First option.",
        "pros": ["Keeps the public seam"],
        "cons": ["Requires transition work"],
    }
    options[1] = {"name": "Candidate 2", "description": "", "pros": [], "cons": []}
    context: dict[str, JsonValue] = {
        "title": "Boundary design",
        "problem_statement": "Caller-defined mismatch.",
        "requirements_functional": ["Preserve accepted calls", "Return explicit outcomes"],
        "requirements_nonfunctional": ["Keep bounded runtime"],
        "status": "DRAFT — awaiting review",
        "version": "2.1",
        "last_updated": "2026-09-14",
        "purpose": "**Authored purpose**",
        "scope_in": "Included seam",
        "scope_out": "Excluded behavior",
        "prerequisites": ["Read the approved strategy"],
        "related_docs": [{"label": "Research", "target": "research.md#Findings"}],
        "constraints": ["Keep the approved strategy"],
        "options": options,
        "decision": "Caller selected the second option.",
        "rationale": "Caller trade-off.\n\nAdditional rationale.",
        "key_decisions": [
            {
                "decision": "Keep the boundary #",
                "rationale": "Preserves consumer calls",
                "alternatives": ["Rejected global rewrite"],
            },
            {"decision": "Deferred detail", "rationale": "", "alternatives": []},
            {"decision": "Authored detail", "rationale": "No alternatives supplied"},
        ],
        "questions": ["Which owner supplies the dependency?"],
        "production_design": "Inject the narrow reader.",
        "test_design": "Observe calls through the public seam.",
        "contracts": [
            {
                "heading": "Input contract #",
                "content": "Authored **contract**.\n\nNext paragraph.",
                "bullets": ["Accepted input", "Explicit output"],
                "checklist": [
                    {"text": "Caller verified", "checked": True},
                    {"text": "Awaiting evidence", "checked": False},
                ],
            },
            {"heading": "Empty prose contract", "content": ""},
            {"heading": "Empty bullets contract", "bullets": []},
            {"heading": "Empty checklist contract", "checklist": []},
        ],
        "flow": "Caller → reader → result",
        "state_and_failures": "A failed read leaves state unchanged.",
        "preservation": "Retain accepted input semantics.",
        "transition_and_cleanup": "Cut over the named consumer, then retire its bridge.",
        "validation": [
            {
                "obligation": "Preserve the seam #",
                "method": "Compare public results",
                "expected_result": "Same accepted outcomes",
                "references": [{"label": "Planned check", "target": "#Caller-Check"}],
            },
            {
                "obligation": "Prove the exclusion",
                "method": "Inspect the diff",
                "expected_result": "Excluded path unchanged",
                "references": [],
            },
            {
                "obligation": "Review ownership",
                "method": "Read the consumer",
                "expected_result": "Narrow dependency retained",
            },
        ],
        "risks": [
            {
                "description": "Consumer transition risk #",
                "mitigation": "Named migration",
                "consequence": "Consumer interruption",
            },
            {"description": "Unresolved risk", "mitigation": ""},
        ],
        "planning_consequences": "Implement the reader before migrating its consumer.",
        "sources": [{"label": "Contract", "target": "contract.md#Boundary"}],
    }
    before = deepcopy(context)
    output = design.renderer.render("design", context, design.provenance)
    assert context == before
    for supplied in (
        "Caller-defined mismatch.",
        "**Authored purpose**",
        "Included seam",
        "Excluded behavior",
        "DRAFT — awaiting review",
        "2.1",
        "2026-09-14",
        "Read the approved strategy",
        "Keep the approved strategy",
        "First option.",
        "Keeps the public seam",
        "Requires transition work",
        "Caller selected the second option.",
        "Caller trade-off.\n\nAdditional rationale.",
        "Preserves consumer calls",
        "Rejected global rewrite",
        "Deferred detail",
        "Authored detail",
        "No alternatives supplied",
        "Which owner supplies the dependency?",
        "Inject the narrow reader.",
        "Observe calls through the public seam.",
        "Authored **contract**.\n\nNext paragraph.",
        "Accepted input",
        "Explicit output",
        "Empty prose contract",
        "Empty bullets contract",
        "Empty checklist contract",
        "Caller → reader → result",
        "A failed read leaves state unchanged.",
        "Retain accepted input semantics.",
        "Cut over the named consumer, then retire its bridge.",
        "Compare public results",
        "Same accepted outcomes",
        "Prove the exclusion",
        "Inspect the diff",
        "Excluded path unchanged",
        "Review ownership",
        "Read the consumer",
        "Narrow dependency retained",
        "Named migration",
        "Consumer interruption",
        "Unresolved risk",
        "Implement the reader before migrating its consumer.",
    ):
        assert supplied in output, supplied
    positions = [output.index(f"### {index}. Candidate {index}") for index in range(1, 12)]
    assert positions == sorted(positions)
    assert "Authored option 11." in output
    for heading in (
        r"### 1. Candidate 1 \#",
        r"### Keep the boundary \#",
        r"### Input contract \#",
        r"### Preserve the seam \#",
        r"### Consumer transition risk \#",
    ):
        assert heading in output
    functional = output.split("## Functional Requirements\n", 1)[1].split("\n## ", 1)[0]
    nonfunctional = output.split("## Nonfunctional Requirements\n", 1)[1].split("\n## ", 1)[0]
    assert functional.index("Preserve accepted calls") < functional.index(
        "Return explicit outcomes"
    )
    assert "Keep bounded runtime" not in functional
    assert (
        "Keep bounded runtime" in nonfunctional and "Preserve accepted calls" not in nonfunctional
    )
    assert "- [x] Caller verified" in output and "- [ ] Awaiting evidence" in output
    assert "[Research](<research.md#Findings>)" in output
    assert "[Contract](<contract.md#Boundary>)" in output
    assert "[Planned check](<#Caller-Check>)" in output
    assert output.count("**Alternatives:**") == 2
    assert output.count("**References:**") == 2
    assert "Observed Result" not in output
    assert output.count("\n# ") == 1
    code, response = invoke(markdown_package, tmp_path, request(tmp_path / "populated.md", output))
    assert code == 0 and response["decision"] == {"status": "passed"}


def test_design_explicit_empty_sections_remain_visible(design: DeliveredTemplate) -> None:
    context: dict[str, JsonValue] = {
        "title": "Initial design",
        "problem_statement": "Known problem.",
        "requirements_functional": [],
        "requirements_nonfunctional": [],
        "purpose": "",
        "scope_in": "",
        "scope_out": "",
        "prerequisites": [],
        "related_docs": [],
        "constraints": [],
        "options": [],
        "decision": "",
        "rationale": "",
        "key_decisions": [],
        "questions": [],
        "production_design": "",
        "test_design": "",
        "contracts": [],
        "flow": "",
        "state_and_failures": "",
        "preservation": "",
        "transition_and_cleanup": "",
        "validation": [],
        "risks": [],
        "planning_consequences": "",
        "sources": [],
    }
    output = design.renderer.render("design", context, design.provenance)
    headings = [line for line in output.splitlines() if line.startswith("## ")]
    for heading in (
        "Purpose",
        "Scope In",
        "Scope Out",
        "Prerequisites",
        "Related Documents",
        "Functional Requirements",
        "Nonfunctional Requirements",
        "Constraints",
        "Options",
        "Decision",
        "Rationale",
        "Key Decisions",
        "Questions",
        "Production Design",
        "Test Design",
        "Contracts",
        "Flow",
        "State and Failures",
        "Preservation",
        "Transition and Cleanup",
        "Validation",
        "Risks",
        "Planning Consequences",
        "Sources",
    ):
        assert headings.count(f"## {heading}") == 1
    assert not any(line.startswith("- ") for line in output.splitlines())
    for invented in ("None", "To be defined", "Initial draft", "**Status:**", "Agent"):
        assert invented not in output


def test_design_rejects_legacy_shapes_and_invalid_record_contracts(
    design: DeliveredTemplate,
) -> None:
    base: dict[str, JsonValue] = {
        "title": "Design",
        "problem_statement": "Problem",
        "requirements_functional": [],
        "requirements_nonfunctional": [],
    }
    invalid: list[dict[str, JsonValue]] = [
        {"title": "Design", "problem_statement": "Problem", "requirements_functional": []},
        {**base, "title": ""},
        {**base, "problem_statement": ""},
        {**base, "requirements_functional": [""]},
        {**base, "requirements_nonfunctional": "Fast"},
        {**base, "requirements": []},
        {**base, "questions_list": []},
        {**base, "decision": None},
        {**base, "workflow": "feature"},
        {**base, "status": ""},
        {**base, "last_updated": "2026-09-14\n"},
        {**base, "options": ["Option"]},
        {**base, "options": [{"name": "Option", "description": "", "selected": True}]},
        {**base, "key_decisions": [{"decision": "Decision"}]},
        {**base, "contracts": [{"heading": "Missing content"}]},
        {**base, "contracts": [{"heading": "Contract", "content": "", "children": []}]},
        {**base, "contracts": [{"heading": "Contract", "checklist": [{"text": "Check"}]}]},
        {
            **base,
            "contracts": [
                {"heading": "Contract", "checklist": [{"text": "Check", "checked": None}]}
            ],
        },
        {**base, "validation": [{"obligation": "Proof", "method": "Inspect"}]},
        {
            **base,
            "validation": [
                {
                    "obligation": "Proof",
                    "method": "Inspect",
                    "expected_result": "Preserved",
                    "observation": "Invented",
                }
            ],
        },
        {**base, "risks": [{"description": "Risk"}]},
        {**base, "risks": [{"description": "Risk", "mitigation": "", "probability": 0}]},
        {**base, "sources": [{"target": "contract.md"}]},
    ]
    for context in invalid:
        with pytest.raises(ContextError):
            design.renderer.render("design", context, design.provenance)
