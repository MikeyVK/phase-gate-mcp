"""Exercise delivered architecture records through public rendering and native links."""

from __future__ import annotations

from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError
from pydantic import JsonValue

from mcp_server.core.interfaces.template_catalog import thaw_json
from mcp_server.schemas.template_identity import ArtifactIdentity
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from tests.mcp_server.fixtures.delivered_templates import DeliveredTemplate, load_delivered_template
from tests.mcp_server.integration.adapters.test_lychee import (
    DEFAULT_ARGS,
    LycheeRuntime,
    invoke,
    package_for,
)

pytest_plugins = ("tests.mcp_server.integration.adapters.test_lychee",)


CHAPTERS = (
    ("introduction_and_goals", "1. Introduction and Goals"),
    ("architecture_constraints", "2. Architecture Constraints"),
    ("context_and_scope", "3. Context and Scope"),
    ("solution_strategy", "4. Solution Strategy"),
    ("building_block_view", "5. Building Block View"),
    ("runtime_view", "6. Runtime View"),
    ("deployment_view", "7. Deployment View"),
    ("crosscutting_concepts", "8. Cross-cutting Concepts"),
    ("architecture_decisions", "9. Architecture Decisions"),
    ("quality_requirements", "10. Quality Requirements"),
    ("risks_and_technical_debt", "11. Risks and Technical Debts"),
    ("glossary", "12. Glossary"),
)


def delivered(tmp_path: Path, repo: Path, name: str) -> DeliveredTemplate:
    return load_delivered_template(
        source_suite=repo / ".pgmcp/template_suite",
        source_package=repo / ".pgmcp/template_suite" / name,
        config_root=repo / ".pgmcp/config",
        destination=tmp_path / name,
        template_id=name,
    )


def metadata(status: str = "draft") -> dict[str, JsonValue]:
    return {
        "status": status,
        "revisions": [
            {"version": "0.1", "date": "2026-10-11", "author": "Record author", "change": "Draft"}
        ],
    }


def common_fields() -> dict[str, JsonValue]:
    return {
        "purpose": "Authored record purpose",
        "scope_in": "Storage boundary",
        "scope_out": "Transport boundary",
        "prerequisites": ["Read workload"],
        "related_docs": [{"label": "Related view", "target": "sad.md#5-building-block-view"}],
    }


def assert_common_consumption(text: str) -> None:
    for fact in (
        "Authored record purpose",
        "Storage boundary",
        "Transport boundary",
        "Read workload",
        "[Related view](<sad.md#5-building-block-view>)",
    ):
        assert fact in text


def adr_context() -> dict[str, JsonValue]:
    return {
        "title": "Storage decision",
        "adr_id": "ADR-42",
        "document_metadata": metadata(),
        "context": "",
        "decision_drivers": [],
        "options": [],
        "decision": "",
        "rationale": "",
        "consequences": "",
    }


def sad_context() -> dict[str, JsonValue]:
    context: dict[str, JsonValue] = {
        "title": "System architecture",
        "document_metadata": metadata(),
        "architecture_scope": "proposed",
        **{field: "" for field, _ in CHAPTERS},
    }
    context["architecture_decisions"] = {"overview": "", "adrs": []}
    context["quality_requirements"] = {"overview": "", "scenarios": []}
    return context


def test_adr_drafts_and_populated_alternatives(tmp_path: Path, pytestconfig: pytest.Config) -> None:
    package = delivered(tmp_path, pytestconfig.rootpath, "adr")
    context = adr_context()
    minimal = package.renderer.render("adr", context, package.provenance)
    assert "**ADR:** ADR-42" in minimal and "**Status:** draft" in minimal
    for heading in (
        "Context",
        "Decision Drivers",
        "Options",
        "Decision",
        "Rationale",
        "Consequences",
    ):
        assert f"## {heading}\n" in minimal
    for heading in (
        "Participants",
        "Tags",
        "Verification",
        "SAD Sections",
        "Supersedes",
        "Superseded By",
    ):
        assert f"## {heading}" not in minimal
    assert minimal.count("\n# ") == 1
    context.update(
        {
            "document_metadata": metadata("accepted"),
            "context": "Existing storage pressure",
            "decision_drivers": ["Latency first", "Operational simplicity"],
            "options": [
                {
                    "name": "Embedded",
                    "description": "Local writes",
                    "pros": ["Low latency"],
                    "cons": [],
                },
                {"name": "Remote", "description": "Shared writes", "cons": ["Network cost"]},
            ],
            "decision": "Use embedded storage",
            "rationale": "Bounded operational cost",
            "consequences": "Backups become explicit",
            "participants": ["Alice", "Bob"],
            "tags": ["storage"],
            "verification": "",
            "sad_sections": [],
            "supersedes": [],
            "superseded_by": [],
        }
    )
    context.update(common_fields())
    context["verification"] = "Measure bounded write latency"
    populated = package.renderer.render("adr", context, package.provenance)
    assert_common_consumption(populated)
    assert "Measure bounded write latency" in populated
    assert populated.index("Embedded") < populated.index("Remote")
    for fact in (
        "Local writes",
        "Shared writes",
        "Low latency",
        "Network cost",
        "Latency first",
        "Operational simplicity",
        "Alice",
        "Bob",
        "storage",
        "Use embedded storage",
        "Bounded operational cost",
        "Backups become explicit",
    ):
        assert fact in populated
    assert "**Status:** accepted" in populated
    assert "**Cons:**" in populated and "## Verification" in populated
    for heading in ("SAD Sections", "Supersedes", "Superseded By"):
        assert f"## {heading}" in populated
    assert populated.rstrip().endswith("| 0.1 | 2026-10-11 | Record author | Draft |")


def test_sad_drafts_and_effective_nested_fields(
    tmp_path: Path, pytestconfig: pytest.Config
) -> None:
    package = delivered(tmp_path, pytestconfig.rootpath, "sad")
    context = sad_context()
    expected_provenance = ArtifactIdentity.model_validate(thaw_json(package.provenance))
    minimal = package.renderer.render("sad", context, package.provenance)
    assert ArtifactHeaderReader().read(minimal).provenance == expected_provenance
    headings = [line for line in minimal.splitlines() if line.startswith("## ")]
    assert [line for line in headings if line[3:4].isdigit()] == [
        f"## {heading}" for _, heading in CHAPTERS
    ]
    for heading in ("10.1 Quality Requirements Overview", "10.2 Quality Scenarios"):
        assert f"### {heading}" in minimal
    assert minimal.count("**Architecture Scope:** proposed") == 1
    context.update({field: f"Authored {field}" for field, _ in CHAPTERS})
    context["architecture_scope"] = "mixed"
    context["architecture_decisions"] = {
        "overview": "Decision catalogue",
        "adrs": [
            {
                "adr_id": "ADR-42",
                "status": "accepted",
                "link": {"label": "Storage decision", "target": "adr.md#decision"},
            }
        ],
    }
    context["quality_requirements"] = {
        "overview": "Measured behavior",
        "scenarios": [
            {
                "name": "Peak load",
                "scenario": "Concurrent reads",
                "response_measure": "P95 below ten milliseconds",
            }
        ],
    }
    context.update(common_fields())
    populated = package.renderer.render("sad", context, package.provenance)
    assert ArtifactHeaderReader().read(populated).provenance == expected_provenance
    assert_common_consumption(populated)
    for field, _ in CHAPTERS:
        if field not in ("architecture_decisions", "quality_requirements"):
            assert f"Authored {field}" in populated
    for fact in (
        "Decision catalogue",
        "ADR-42",
        "accepted",
        "[Storage decision](<adr.md#decision>)",
        "Measured behavior",
        "Peak load",
        "Concurrent reads",
        "P95 below ten milliseconds",
    ):
        assert fact in populated
    assert populated.count("**Architecture Scope:** mixed") == 1
    assert populated.index("Gernot Starke") < populated.index("## Version History")
    assert populated.index("Peter Hruschka") < populated.index("## Version History")
    assert "CC BY-SA 4.0" in populated


@pytest.mark.parametrize(
    "family,change",
    [
        ("adr", {"unexpected": True}),
        ("adr", {"document_metadata": metadata("unknown")}),
        ("adr", {"options": [{"name": "Missing description"}]}),
        ("sad", {"architecture_scope": "future"}),
        (
            "sad",
            {
                "architecture_decisions": {
                    "overview": "",
                    "adrs": [{"adr_id": "x", "status": "draft"}],
                }
            },
        ),
        (
            "sad",
            {
                "quality_requirements": {
                    "overview": "",
                    "scenarios": [{"name": "x", "scenario": ""}],
                }
            },
        ),
    ],
)
def test_context_rejects_undeclared_and_incomplete_records(
    tmp_path: Path, pytestconfig: pytest.Config, family: str, change: dict[str, JsonValue]
) -> None:
    package = delivered(tmp_path, pytestconfig.rootpath, family)
    context = adr_context() if family == "adr" else sad_context()
    context.update(change)
    with pytest.raises(ValidationError):
        package.renderer.render(family, context, package.provenance)


@pytest.mark.parametrize("family,field", [("adr", "decision"), ("sad", "glossary")])
def test_core_carriers_remain_required(
    tmp_path: Path, pytestconfig: pytest.Config, family: str, field: str
) -> None:
    package = delivered(tmp_path, pytestconfig.rootpath, family)
    context = adr_context() if family == "adr" else sad_context()
    del context[field]
    with pytest.raises(ValidationError):
        package.renderer.render(family, context, package.provenance)


@pytest.mark.parametrize("broken", [False, True])
def test_real_adr_sad_relative_fragments(
    tmp_path: Path, pytestconfig: pytest.Config, lychee_runtime: LycheeRuntime, broken: bool
) -> None:
    adr = delivered(tmp_path / "adr graph", pytestconfig.rootpath, "adr")
    sad = delivered(tmp_path / "sad graph", pytestconfig.rootpath, "sad")
    a = adr_context()
    a["sad_sections"] = [
        {
            "label": "Storage view",
            "target": "sad.md#absent" if broken else "sad.md#5-building-block-view",
        }
    ]
    a["supersedes"] = [{"label": "Context", "target": "sad.md#3-context-and-scope"}]
    a["superseded_by"] = [{"label": "Quality", "target": "sad.md#10-quality-requirements"}]
    s = sad_context()
    s["architecture_decisions"] = {
        "overview": "Related record",
        "adrs": [
            {
                "adr_id": "ADR-42",
                "status": "draft",
                "link": {"label": "Storage decision", "target": "adr.md#decision"},
            }
        ],
    }
    adr_file = lychee_runtime.workspace / "adr.md"
    sad_file = lychee_runtime.workspace / "sad.md"
    adr_text = adr.renderer.render("adr", a, adr.provenance)
    sad_text = sad.renderer.render("sad", s, sad.provenance)
    assert "[Storage view](<sad.md#" in adr_text
    assert "[Context](<sad.md#3-context-and-scope>)" in adr_text
    assert "[Quality](<sad.md#10-quality-requirements>)" in adr_text
    adr_file.write_text(adr_text, encoding="utf-8")
    sad_file.write_text(sad_text, encoding="utf-8")
    native_package = package_for(lychee_runtime, tmp_path, pytestconfig.rootpath)
    code, response = invoke(
        native_package,
        {
            "operation": "links",
            "targets": [str(adr_file), str(sad_file)],
            "args": [*DEFAULT_ARGS, "--format", "json"],
        },
    )
    assert code == (1 if broken else 0)
    decision = response["decision"]
    assert isinstance(decision, dict) and decision["status"] == ("failed" if broken else "passed")
    assert response["external_tools"] == [{"tool_id": "lychee", "version": "0.24.2"}]
    assert adr_file.read_text(encoding="utf-8") == adr_text
    assert sad_file.read_text(encoding="utf-8") == sad_text
