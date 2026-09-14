"""Exercise Generic Document behavior through public template and native Markdown seams."""

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
def generic_document(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=suite,
        source_package=suite / "generic_doc",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "explicit suite",
        template_id="generic_doc",
    )
    selected = delivered.catalog.get("generic_doc")
    assert selected.policy.persistence == "workspace"
    assert dict(delivered.checks.profiles)[selected.policy.output_profile].checks == (
        "markdown_document",
    )
    return delivered


def test_minimal_generic_document_is_renderable_and_native_markdown_valid(
    generic_document: DeliveredTemplate,
    markdown_package: MarkdownPackage,
    tmp_path: Path,
) -> None:
    context: dict[str, JsonValue] = {
        "title": "Document basis",
        "purpose": "Purpose marker.",
        "summary": "Summary marker.",
    }
    before = deepcopy(context)
    output = generic_document.renderer.render("generic_doc", context, generic_document.provenance)
    assert context == before
    assert f"# {context['title']}" in output
    for key in ("purpose", "summary"):
        value = context[key]
        assert isinstance(value, str) and value in output

    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "generic_doc"

    code, response = invoke(markdown_package, tmp_path, request(tmp_path / "generic.md", output))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "generic.md").exists()


def test_generic_document_preserves_authored_order_and_record_state(
    generic_document: DeliveredTemplate,
) -> None:
    context: dict[str, JsonValue] = {
        "title": "Migration basis",
        "purpose": "Purpose marker.",
        "summary": "Summary marker.",
        "key_changes": ["change-one", "change-two"],
        "migration_steps": ["line one\nline two", "final step"],
        "validation_checklist": [
            {"text": "checked item", "checked": True},
            {"text": "unchecked item", "checked": False},
        ],
        "faq": [
            {"question": "First question", "answer": "First answer."},
            {"question": "Second question", "answer": ""},
        ],
        "sections": [
            {
                "heading": "Custom one #",
                "content": "custom content",
                "bullets": ["bullet one", "bullet two"],
            },
            {
                "heading": "Custom two",
                "checklist": [{"text": "section check", "checked": False}],
            },
        ],
        "related_docs": [{"label": "Related marker", "target": "docs/ref.md#part"}],
    }
    before = deepcopy(context)
    output = generic_document.renderer.render("generic_doc", context, generic_document.provenance)
    assert context == before

    assert "- [x] checked item" in output and "- [ ] unchecked item" in output
    assert "1. line one\n   line two" in output and "2. final step" in output
    assert output.index("change-one") < output.index("change-two")
    assert output.index("line one") < output.index("final step")
    assert r"### Custom one \#" in output
    first_section = output.split("Custom one", 1)[1].split("Custom two", 1)[0]
    second_section = output.split("Custom two", 1)[1].split("\n## ", 1)[0]
    assert "custom content" in first_section and "- bullet one" in first_section
    assert first_section.index("bullet one") < first_section.index("bullet two")
    assert "- [ ] section check" in second_section and "custom content" not in second_section
    first_faq = output.split("First question", 1)[1].split("Second question", 1)[0]
    assert "First answer." in first_faq
    assert "[Related marker](<docs/ref.md#part>)" in output


def test_generic_document_distinguishes_absent_and_explicit_empty_structures(
    generic_document: DeliveredTemplate,
) -> None:
    base: dict[str, JsonValue] = {
        "title": "Presence basis",
        "purpose": "Purpose marker.",
        "summary": "Summary marker.",
    }
    absent = generic_document.renderer.render("generic_doc", base, generic_document.provenance)
    explicit: dict[str, JsonValue] = {
        **base,
        "key_changes": [],
        "migration_steps": [],
        "validation_checklist": [],
        "faq": [],
        "sections": [],
        "scope_in": "",
        "scope_out": "",
        "prerequisites": [],
        "related_docs": [],
    }
    before = deepcopy(explicit)
    populated = generic_document.renderer.render(
        "generic_doc", explicit, generic_document.provenance
    )
    assert explicit == before
    assert populated.count("\n## ") - absent.count("\n## ") == len(explicit) - len(base)
    for carrier, empty in (("content", ""), ("bullets", []), ("checklist", [])):
        nested: dict[str, JsonValue] = {
            **base,
            "sections": [{"heading": "Empty section", carrier: empty}],
        }
        rendered = generic_document.renderer.render(
            "generic_doc", nested, generic_document.provenance
        )
        assert "### Empty section" in rendered
        assert not any(line.startswith("- ") for line in rendered.splitlines())


def test_generic_document_rejects_out_of_contract_records(
    generic_document: DeliveredTemplate,
) -> None:
    base: dict[str, JsonValue] = {"title": "Basis", "purpose": "Purpose", "summary": "Summary"}
    invalid: list[dict[str, JsonValue]] = [
        {"title": "Missing purpose", "summary": "Summary"},
        {**base, "purpose": ""},
        {**base, "summary": None},
        {**base, "custom_sections": []},
        {**base, "content": "Legacy free-form document"},
        {**base, "prerequisites": "Scalar list"},
        {**base, "related_docs": "guide.md"},
        {**base, "validation_checklist": [{"text": "bad", "checked": None}]},
        {**base, "faq": [{"question": "Missing answer"}]},
        {**base, "faq": ["Primitive record"]},
        {**base, "sections": [{"heading": "No carrier"}]},
        {**base, "sections": [{"heading": "Nested", "content": "", "sections": []}]},
    ]
    for context in invalid:
        with pytest.raises(ContextError):
            generic_document.renderer.render("generic_doc", context, generic_document.provenance)
