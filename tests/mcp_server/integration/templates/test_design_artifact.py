"""Verify the delivered Design package through authored content."""

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
    return delivered


def test_initial_design_does_not_require_or_invent_a_decision(design: DeliveredTemplate) -> None:
    context: dict[str, JsonValue] = {
        "title": "Design the boundary",
        "document_metadata": {
            "status": "DRAFT — fixture input",
            "revisions": [
                {
                    "version": "0.1",
                    "date": "2026-10-03",
                    "author": "Template fixture",
                    "change": "Authored fixture revision.",
                }
            ],
        },
        "problem_statement": "Preserve the caller contract.",
        "requirements_functional": [],
        "requirements_nonfunctional": [],
    }
    before = deepcopy(context)
    output = design.renderer.render("design", context, design.provenance)
    assert context == before
    assert output.count("\n# ") == 1 and f"# {context['title']}" in output
    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "design"


def test_design_preserves_ordered_options_contracts_and_planned_evidence(
    design: DeliveredTemplate,
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
        "document_metadata": {
            "status": "DRAFT — awaiting review",
            "revisions": [
                {
                    "version": "2.1",
                    "date": "2026-09-14",
                    "author": "Template fixture",
                    "change": "Authored fixture revision.",
                }
            ],
        },
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
    for key in ("problem_statement", "production_design", "preservation", "transition_and_cleanup"):
        value = context[key]
        assert isinstance(value, str) and value in output
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
    groups = output.split("\n## ")
    functional = next(group for group in groups if "Preserve accepted calls" in group)
    nonfunctional = next(group for group in groups if "Keep bounded runtime" in group)
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
    for collection, field in (("key_decisions", "alternatives"), ("validation", "references")):
        absent = deepcopy(context)
        records = absent[collection]
        assert isinstance(records, list) and isinstance(records[1], dict)
        del records[1][field]
        rendered = design.renderer.render("design", absent, design.provenance)
        assert rendered.split() != output.split()
    assert output.count("\n# ") == 1


def test_design_explicit_empty_sections_remain_visible(design: DeliveredTemplate) -> None:
    context: dict[str, JsonValue] = {
        "title": "Initial design",
        "document_metadata": {
            "status": "DRAFT — fixture input",
            "revisions": [
                {
                    "version": "0.1",
                    "date": "2026-10-03",
                    "author": "Template fixture",
                    "change": "Authored fixture revision.",
                }
            ],
        },
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
    base = {
        key: context[key]
        for key in (
            "title",
            "document_metadata",
            "problem_statement",
            "requirements_functional",
            "requirements_nonfunctional",
        )
    }
    absent = design.renderer.render("design", base, design.provenance)
    headings = [line for line in output.splitlines() if line.startswith("## ")]
    absent_headings = [line for line in absent.splitlines() if line.startswith("## ")]
    assert len(headings) - len(absent_headings) == len(context) - len(base)
    assert len(headings) == len(set(headings))
    assert not any(line.startswith("- ") for line in output.splitlines())


def test_design_rejects_legacy_shapes_and_invalid_record_contracts(
    design: DeliveredTemplate,
) -> None:
    base: dict[str, JsonValue] = {
        "title": "Design",
        "document_metadata": {
            "status": "DRAFT — fixture input",
            "revisions": [
                {
                    "version": "0.1",
                    "date": "2026-10-03",
                    "author": "Template fixture",
                    "change": "Authored fixture revision.",
                }
            ],
        },
        "problem_statement": "Problem",
        "requirements_functional": [],
        "requirements_nonfunctional": [],
    }
    invalid: list[dict[str, JsonValue]] = [
        {
            "title": "Design",
            "document_metadata": {
                "status": "DRAFT — fixture input",
                "revisions": [
                    {
                        "version": "0.1",
                        "date": "2026-10-03",
                        "author": "Template fixture",
                        "change": "Authored fixture revision.",
                    }
                ],
            },
            "problem_statement": "Problem",
            "requirements_functional": [],
        },
        {**base, "title": ""},
        {**base, "problem_statement": ""},
        {**base, "requirements_functional": [""]},
        {**base, "requirements_nonfunctional": "Fast"},
        {**base, "requirements": []},
        {**base, "questions_list": []},
        {**base, "decision": None},
        {**base, "workflow": "feature"},
        {
            **base,
            "document_metadata": {
                "status": "",
                "revisions": [
                    {
                        "version": "0.1",
                        "date": "2026-10-03",
                        "author": "Template fixture",
                        "change": "Authored fixture revision.",
                    }
                ],
            },
        },
        {
            **base,
            "document_metadata": {
                "status": "DRAFT — fixture input",
                "revisions": [
                    {
                        "version": "0.1",
                        "date": "2026-09-14\n",
                        "author": "Template fixture",
                        "change": "Authored fixture revision.",
                    }
                ],
            },
        },
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
