"""Exercise delivered Planning content and its explicit operational projection."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError as ContextError
from pydantic import JsonValue

from mcp_server.core.interfaces.artifact_header_reader import HeaderReadStatus
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from tests.mcp_server.fixtures.delivered_templates import DeliveredTemplate, load_delivered_template
from tests.mcp_server.fixtures.suite_roots import SuiteRoots
from tests.mcp_server.integration.adapters.test_markdown_preflight import (
    MarkdownPackage,
    invoke,
    markdown_package,
    request,
)
from tests.mcp_server.test_support import load_contracts_config, make_project_manager

__all__ = ["markdown_package"]


@pytest.fixture
def planning(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=suite,
        source_package=suite / "planning",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "explicit suite",
        template_id="planning",
    )
    selected = delivered.catalog.get("planning")
    assert selected.policy.persistence == "workspace"
    assert dict(delivered.checks.profiles)[selected.policy.output_profile].checks == (
        "markdown_document",
    )
    return delivered


def test_initial_planning_does_not_invent_work_or_completion(
    planning: DeliveredTemplate,
    markdown_package: MarkdownPackage,
    tmp_path: Path,
) -> None:
    context: dict[str, JsonValue] = {
        "title": "Plan the boundary",
        "summary": "Authored planning basis.",
        "work_units": [],
    }
    before = deepcopy(context)
    output = planning.renderer.render("planning", context, planning.provenance)
    assert context == before
    assert output.count("\n# ") == 1 and f"# {context['title']}" in output
    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "planning"
    target = tmp_path / "planning.md"
    code, response = invoke(markdown_package, tmp_path, request(target, output))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not target.exists()


def test_refined_plan_retains_authored_ownership_scope_and_evidence_requirements(
    planning: DeliveredTemplate,
    markdown_package: MarkdownPackage,
    tmp_path: Path,
) -> None:
    context: dict[str, JsonValue] = {
        "title": "Bounded plan",
        "summary": "Implement the approved boundary.",
        "status": "DRAFT — awaiting review",
        "version": "3.2",
        "last_updated": "2026-09-14",
        "purpose": "**Caller purpose**",
        "scope_in": "Included surface",
        "scope_out": "Excluded surface",
        "prerequisites": ["Approved strategy"],
        "related_docs": [{"label": "Design", "target": "design.md#Boundary"}],
        "dependencies": ["External owner response"],
        "risks": [
            {
                "description": "Overall risk #",
                "mitigation": "Explicit mitigation",
                "consequence": "Potential delay",
            }
        ],
        "milestones": ["Consumer cutover", "Bridge retirement"],
        "work_units": [
            {
                "id": "WU-B",
                "name": "Migrate consumer #",
                "goal": "Keep accepted caller behavior",
                "deliverables": [
                    {
                        "id": "B.D1",
                        "description": "Caller adapter",
                        "owner": "Adapter owner",
                        "validates": None,
                    }
                ],
                "exit_criteria": "Caller evidence recorded.\nIndependent review complete.",
                "scope_in": "Named consumer",
                "scope_out": "Other consumers",
                "owner": "Migration owner",
                "dependencies": ["WU-A"],
                "obligations": ["Preserve accepted calls"],
                "verification": [
                    {
                        "obligation": "Caller proof #",
                        "method": "Run the selected comparison",
                        "expected_result": "Preserved output",
                        "references": [{"label": "Proof design", "target": "#Caller-Proof"}],
                    },
                    {
                        "obligation": "Review exclusions",
                        "method": "Inspect changes",
                        "expected_result": "Excluded code retained",
                        "references": [],
                    },
                    {
                        "obligation": "Review ordering",
                        "method": "Read dependencies",
                        "expected_result": "Explicit order retained",
                    },
                ],
                "risks": [
                    {"description": "Local transition risk #", "mitigation": "", "consequence": ""}
                ],
                "stop_conditions": ["Stop on an unexplained mismatch"],
            },
            {
                "id": "WU-A",
                "name": "Prepare reader",
                "goal": "Expose narrow reader",
                "deliverables": [{"id": "A.D1", "description": "Reader implementation"}],
                "exit_criteria": "Reader reviewed",
            },
        ],
        "phase_deliverables": {
            "design": [{"id": "D.DESIGN", "description": "Reviewed contract"}],
            "validation": [
                {"id": "D.VALIDATE", "description": "Observed final evidence", "validates": None}
            ],
            "documentation": [
                {"id": "D.DOC", "description": "Final usage guide", "owner": "Documentation owner"}
            ],
        },
    }
    before = deepcopy(context)
    output = planning.renderer.render("planning", context, planning.provenance)
    assert context == before
    for key in ("summary", "scope_in", "scope_out"):
        value = context[key]
        assert isinstance(value, str) and value in output
    assert output.index("Migrate consumer") < output.index("Prepare reader")
    assert output.index("Consumer cutover") < output.index("Bridge retirement")
    for escaped in (
        r"Migrate consumer \#",
        r"Caller proof \#",
        r"Local transition risk \#",
        r"Overall risk \#",
    ):
        assert escaped in output
    assert "[Design](<design.md#Boundary>)" in output
    assert "[Proof design](<#Caller-Proof>)" in output
    absent = deepcopy(context)
    units = absent["work_units"]
    assert isinstance(units, list) and isinstance(units[0], dict)
    verification = units[0]["verification"]
    assert isinstance(verification, list) and isinstance(verification[1], dict)
    del verification[1]["references"]
    assert (
        planning.renderer.render("planning", absent, planning.provenance).split() != output.split()
    )
    code, response = invoke(markdown_package, tmp_path, request(tmp_path / "refined.md", output))
    assert code == 0 and response["decision"] == {"status": "passed"}


def test_empty_planning_sections_and_work_unit_capacities_are_visible(
    planning: DeliveredTemplate,
) -> None:
    context: dict[str, JsonValue] = {
        "title": "Empty capacities",
        "summary": "Authored basis.",
        "purpose": "",
        "scope_in": "",
        "scope_out": "",
        "prerequisites": [],
        "related_docs": [],
        "dependencies": [],
        "risks": [],
        "milestones": [],
        "work_units": [
            {
                "id": "WU-EMPTY",
                "name": "Empty unit",
                "goal": "Defined goal",
                "deliverables": [{"id": "D1", "description": "Defined deliverable"}],
                "exit_criteria": "Explicit exit",
                "scope_in": "",
                "scope_out": "",
                "dependencies": [],
                "obligations": [],
                "verification": [],
                "risks": [],
                "stop_conditions": [],
            }
        ],
        "phase_deliverables": {"design": [], "validation": [], "documentation": []},
    }
    output = planning.renderer.render("planning", context, planning.provenance)
    units = context["work_units"]
    assert isinstance(units, list) and isinstance(units[0], dict)
    required = ("id", "name", "goal", "deliverables", "exit_criteria")
    base: dict[str, JsonValue] = {
        "title": context["title"],
        "summary": context["summary"],
        "work_units": [{key: units[0][key] for key in required}],
    }
    absent = planning.renderer.render("planning", base, planning.provenance)
    assert output.split() != absent.split()
    headings = [line for line in output.splitlines() if line.startswith("## ")]
    absent_headings = [line for line in absent.splitlines() if line.startswith("## ")]
    assert len(headings) - len(absent_headings) == len(context) - len(base)
    assert len(headings) == len(set(headings))
    unit_section = output.split("### WU-EMPTY", 1)[1].split("\n## ", 1)[0]
    exit_criteria = units[0]["exit_criteria"]
    assert isinstance(exit_criteria, str) and exit_criteria in unit_section
    assert "##### D1\n" in unit_section


def test_explicit_projection_survives_actual_planning_save_and_readback(
    planning: DeliveredTemplate,
    legacy_suite_roots: SuiteRoots,
) -> None:
    specifications: list[JsonValue] = [
        {"type": "file_exists", "file": "src/reader.py", "text": None, "path": None},
        {"type": "file_glob", "file": "src/*.py"},
        {"type": "contains_text", "file": "proof.md", "text": "Retained behavior", "path": None},
        {"type": "absent_text", "file": "proof.md", "text": "", "path": None},
        {"type": "key_path", "file": "contract.json", "path": "version", "text": None},
    ]
    deliverables: list[JsonValue] = [
        {"id": f"D{index}", "description": f"Deliverable {index}", "validates": spec}
        for index, spec in enumerate(specifications, 1)
    ]
    first_cycle: dict[str, JsonValue] = {
        "cycle_number": 1,
        "name": "Prepare reader",
        "deliverables": deliverables[:3],
        "exit_criteria": "Reader public behavior verified.\nReady for consumer.",
    }
    second_cycle: dict[str, JsonValue] = {
        "cycle_number": 2,
        "name": "Migrate consumer",
        "deliverables": deliverables[3:],
        "exit_criteria": "Consumer preserved and bridge retired.",
    }
    cycles: list[JsonValue] = [first_cycle, second_cycle]
    work_units: list[JsonValue] = [
        {"id": "WU-A", "goal": "Expose reader", "owner": "Reader owner", **first_cycle},
        {"id": "WU-B", "goal": "Preserve consumer", "dependencies": ["WU-A"], **second_cycle},
    ]
    phase_design: list[JsonValue] = [{"id": "DESIGN.1", "description": "Boundary contract"}]
    phase_validation: list[JsonValue] = [
        {"id": "VALIDATE.1", "description": "Independent evidence", "validates": None},
    ]
    phase_docs: list[JsonValue] = [{"id": "DOC.1", "description": "Published usage"}]
    context: dict[str, JsonValue] = {
        "title": "Operational mapping",
        "summary": "Map only explicit cycles.",
        "work_units": work_units,
        "phase_deliverables": {
            "design": phase_design,
            "validation": phase_validation,
            "documentation": phase_docs,
        },
    }
    before = deepcopy(context)
    output = planning.renderer.render("planning", context, planning.provenance)
    assert context == before
    assert output.index("Prepare reader") < output.index("Migrate consumer")
    for deliverable in deliverables:
        assert isinstance(deliverable, dict)
        identifier = deliverable["id"]
        assert isinstance(identifier, str) and identifier in output
        spec = deliverable["validates"]
        assert isinstance(spec, dict)
        kind = spec["type"]
        assert isinstance(kind, str) and kind in output
    for cycle in (first_cycle, second_cycle):
        for key in ("name", "exit_criteria"):
            value = cycle[key]
            assert isinstance(value, str) and value in output
    payload: dict[str, JsonValue] = {
        "cycles": {"total": 2, "cycles": cycles},
        "design": {"deliverables": phase_design},
        "validation": {"deliverables": phase_validation},
        "documentation": {"deliverables": phase_docs},
    }
    contracts = load_contracts_config(legacy_suite_roots.workspace)
    workflow = next(
        name
        for name, definition in contracts.workflows.items()
        if any(phase.cycle_based for phase in definition.phases)
    )
    manager = make_project_manager(legacy_suite_roots.workspace, contracts_config=contracts)
    manager.initialize_project(71, "Explicit planning projection", workflow)
    manager.save_planning_deliverables(71, payload)
    reader = make_project_manager(legacy_suite_roots.workspace, contracts_config=contracts)
    restored = reader.get_project_plan(71)
    assert restored is not None and restored["planning_deliverables"] == payload
    assert context == before


def test_planning_rejects_legacy_and_invalid_operational_shapes(
    planning: DeliveredTemplate,
) -> None:
    unit: dict[str, JsonValue] = {
        "id": "WU1",
        "name": "Work",
        "goal": "Goal",
        "exit_criteria": "Exit",
        "deliverables": [{"id": "D1", "description": "Deliverable"}],
    }
    base: dict[str, JsonValue] = {"title": "Plan", "summary": "Summary", "work_units": []}
    invalid: list[dict[str, JsonValue]] = [
        {"title": "Plan", "work_units": []},
        {**base, "summary": ""},
        {**base, "cycles": []},
        {**base, "success_criteria": []},
        {**base, "work_units": [{**unit, "success_criteria": "Old exit"}]},
        {**base, "work_units": [{**unit, "deliverables": []}]},
        {**base, "work_units": [{**unit, "cycle_number": 0}]},
        {**base, "work_units": [{**unit, "cycle_number": True}]},
        {
            **base,
            "work_units": [{**unit, "verification": [{"obligation": "Proof", "method": "Read"}]}],
        },
        {**base, "work_units": [{**unit, "scope_in": None}]},
        {**base, "phase_deliverables": {"implementation": []}},
        {**base, "phase_deliverables": {"design": None}},
        {**base, "risks": ["Risk"]},
    ]
    bad_specs: list[JsonValue] = [
        {"type": "file_exists"},
        {"type": "file_glob", "file": None},
        {"type": "contains_text", "file": "proof.md"},
        {"type": "absent_text", "file": "proof.md", "text": None},
        {"type": "key_path", "file": "contract.json"},
        {"type": "expression", "file": "contract.json"},
        {"type": "file_exists", "file": "source.py", "command": "inferred"},
    ]
    invalid.extend(
        {
            **base,
            "work_units": [
                {
                    **unit,
                    "deliverables": [
                        {"id": "D1", "description": "Deliverable", "validates": spec},
                    ],
                }
            ],
        }
        for spec in bad_specs
    )
    for context in invalid:
        with pytest.raises(ContextError):
            planning.renderer.render("planning", context, planning.provenance)
