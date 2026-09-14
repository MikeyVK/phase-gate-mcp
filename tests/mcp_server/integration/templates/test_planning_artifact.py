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
    assert output.count("\n# ") == 1 and "# Plan the boundary" in output
    assert "## Summary" in output and "Authored planning basis." in output
    assert "## Work Units" in output
    for absent in (
        "## Dependencies",
        "## Risks",
        "## Milestones",
        "## Phase Deliverables",
        "## Related Documents",
        "**Status:**",
        "Version History",
        "Initial draft",
        "TDD",
    ):
        assert absent not in output
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
    for supplied in (
        "Implement the approved boundary.",
        "DRAFT — awaiting review",
        "3.2",
        "2026-09-14",
        "**Caller purpose**",
        "Included surface",
        "Excluded surface",
        "Approved strategy",
        "External owner response",
        "Explicit mitigation",
        "Potential delay",
        "Consumer cutover",
        "Bridge retirement",
        "WU-B",
        "Keep accepted caller behavior",
        "B.D1",
        "Caller adapter",
        "Adapter owner",
        "Caller evidence recorded.\nIndependent review complete.",
        "Named consumer",
        "Other consumers",
        "Migration owner",
        "WU-A",
        "Preserve accepted calls",
        "Run the selected comparison",
        "Preserved output",
        "Review exclusions",
        "Inspect changes",
        "Excluded code retained",
        "Review ordering",
        "Read dependencies",
        "Explicit order retained",
        "Stop on an unexplained mismatch",
        "Prepare reader",
        "Expose narrow reader",
        "A.D1",
        "Reader implementation",
        "Reader reviewed",
        "D.DESIGN",
        "Reviewed contract",
        "D.VALIDATE",
        "Observed final evidence",
        "D.DOC",
        "Final usage guide",
        "Documentation owner",
    ):
        assert supplied in output, supplied
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
    assert output.count("**References:**") == 2
    assert output.count("**Validates:** null") == 2
    assert "**Cycle Number:**" not in output
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
    for label in (
        "Purpose",
        "Scope In",
        "Scope Out",
        "Prerequisites",
        "Related Documents",
        "Dependencies",
        "Risks",
        "Milestones",
        "Phase Deliverables",
    ):
        assert f"## {label}" in output
    for label in (
        "Scope In",
        "Scope Out",
        "Dependencies",
        "Obligations",
        "Verification",
        "Risks",
        "Stop Conditions",
        "Design",
        "Validation",
        "Documentation",
    ):
        assert label in output
    unit_section = output.split("### WU-EMPTY", 1)[1].split("## Phase Deliverables", 1)[0]
    assert not any(line.startswith("## ") for line in unit_section.splitlines())
    for heading in (
        "Scope In",
        "Scope Out",
        "Deliverables",
        "Exit Criteria",
        "Dependencies",
        "Obligations",
        "Verification",
        "Risks",
        "Stop Conditions",
    ):
        assert f"#### {heading}\n" in unit_section
    assert "##### D1\n" in unit_section
    for invented in ("None", "To be defined", "Initial draft", "**Status:**", "TDD"):
        assert invented not in output


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
    assert "**Cycle Number:** 1" in output and "**Cycle Number:** 2" in output
    for supplied in (
        "WU-A",
        "WU-B",
        "Reader owner",
        "D1",
        "D2",
        "D3",
        "D4",
        "D5",
        "file_exists",
        "file_glob",
        "contains_text",
        "absent_text",
        "key_path",
        "src/reader.py",
        "src/*.py",
        "proof.md",
        "Retained behavior",
        "contract.json",
        "version",
        "Reader public behavior verified.\nReady for consumer.",
        "Consumer preserved and bridge retired.",
        "DESIGN.1",
        "VALIDATE.1",
        "DOC.1",
    ):
        assert supplied in output, supplied
    assert "**Text:** null" in output and "**Path:** null" in output
    absent_text_section = output.split("**Type:** absent_text", 1)[1].split(
        "**Type:** key_path", 1
    )[0]
    assert any(line.rstrip() == "**Text:**" for line in absent_text_section.splitlines())
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
