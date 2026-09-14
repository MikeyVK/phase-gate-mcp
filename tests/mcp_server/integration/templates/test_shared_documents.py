"""Observe actual shared document sources through independent concrete consumers."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from shutil import copytree

import pytest
from jsonschema.exceptions import ValidationError as ContextError
from pydantic import JsonValue

from mcp_server.config.validator import ConfigValidator
from mcp_server.core.interfaces.artifact_header_reader import HeaderReadStatus
from mcp_server.core.interfaces.template_catalog import thaw_json
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from mcp_server.services.template_contract_loader import DRAFT_2020_12, TemplateContractLoader
from tests.mcp_server.integration.adapters.test_markdown_preflight import (
    MarkdownPackage,
    invoke,
    markdown_package,
    request,
)
from tests.mcp_server.integration.templates.test_shared_python import render

__all__ = ["markdown_package"]


DOCUMENT = (
    '{% extends "shared/templates/bases/tier2_markdown_document.jinja2" %}\n'
    "{% block document_body %}## Specific content\n\nCaller section.{% endblock %}"
)
TRACKING = (
    '{% extends "shared/templates/bases/tier2_markdown_tracking.jinja2" %}\n'
    "{% block tracking_body %}{{ content.prose }}{% endblock %}"
)


def render_records(tmp_path: Path, repo: Path, template: str, content: dict[str, JsonValue]) -> str:
    """Pair delivered schema references with unchanged content and the actual shared graph."""
    suite = tmp_path / "schema suite"
    if not suite.exists():
        copytree(repo / ".pgmcp/template_suite/shared", suite / "shared")
    package = suite / "consumer"
    package.mkdir(exist_ok=True)
    schema_path = package / "context.schema.json"
    schema_path.write_text(
        json.dumps(
            {
                "$schema": DRAFT_2020_12,
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "links": {
                        "type": "array",
                        "items": {"$ref": "../shared/definitions/link.schema.json"},
                    },
                    "issues": {
                        "type": "array",
                        "items": {"$ref": "../shared/definitions/issue-reference.schema.json"},
                    },
                    "checklist": {
                        "type": "array",
                        "items": {"$ref": "../shared/definitions/checklist-item.schema.json"},
                    },
                },
            }
        ),
        encoding="utf-8",
    )
    loaded = TemplateContractLoader(suite).load_context_schema(schema_path)
    before = deepcopy(content)
    validated = thaw_json(ConfigValidator().validate_template_context(loaded, content))
    assert validated == content == before
    return render(tmp_path, repo, template, content)


def test_common_document_fields_preserve_absent_empty_and_populated_content(
    tmp_path: Path, pytestconfig: pytest.Config, markdown_package: MarkdownPackage
) -> None:
    repo = pytestconfig.rootpath
    minimal = render(tmp_path, repo, DOCUMENT, {"title": "Explicit title"})
    assert minimal.count("\n# ") == 1
    headings = ("Purpose", "Scope In", "Scope Out", "Prerequisites", "Related Documents")
    for absent in headings:
        assert f"## {absent}" not in minimal
    for absent in ("Status:", "Version:", "Last Updated:", "Version History", "Initial draft"):
        assert absent not in minimal
    empty = render(
        tmp_path,
        repo,
        DOCUMENT,
        {
            "title": "Explicit title",
            "purpose": "",
            "scope_in": "",
            "scope_out": "",
            "prerequisites": [],
            "related_docs": [],
        },
    )
    for heading in headings:
        assert f"## {heading}" in empty
    assert not any(line.startswith("- ") for line in empty.splitlines())
    assert "None" not in empty
    context: dict[str, JsonValue] = {
        "title": "Authored [title]\n# not another heading #",
        "status": "DRAFT — awaiting review",
        "version": "2.3",
        "last_updated": "2026-09-14",
        "purpose": "**Authored** purpose",
        "scope_in": "Include this",
        "scope_out": "Exclude that",
        "prerequisites": ["First\ncontinued", "Second"],
        "related_docs": [{"label": "Own section", "target": "#Exact-Section"}],
    }
    before = deepcopy(context)
    populated = render(tmp_path, repo, DOCUMENT, context)
    assert context == before and populated.count("\n# ") == 1
    assert r"Authored \[title\]&#10;# not another heading \#" in populated
    assert "**Status:** DRAFT — awaiting review" in populated
    assert "**Version:** 2.3" in populated and "**Last Updated:** 2026-09-14" in populated
    assert "**Authored** purpose" in populated
    assert "- First\n  continued\n- Second" in populated
    assert "[Own section](<#Exact-Section>)" in populated
    header = ArtifactHeaderReader().read(populated)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "custom.consumer"
    code, result = invoke(markdown_package, tmp_path, request(tmp_path / "document.md", populated))
    assert code == 0 and result["decision"] == {"status": "passed"}


def test_markdown_and_text_tracking_keep_body_only_structure(
    tmp_path: Path, pytestconfig: pytest.Config, markdown_package: MarkdownPackage
) -> None:
    repo = pytestconfig.rootpath
    output = render(
        tmp_path,
        repo,
        TRACKING,
        {
            "prose": "## Authored body\n\nActual content.",
            "related_docs": [{"label": "Reference", "target": "own-file.md#Exact-Section"}],
        },
    )
    assert "\n# " not in output and "Version History" not in output
    assert "[Reference][related-1]" in output
    assert output.count("[related-1]: <own-file.md#Exact-Section>") == 1
    code, result = invoke(
        markdown_package,
        tmp_path,
        {
            **request(tmp_path / "body.md", output),
            "operation": "body",
        },
    )
    assert code == 0 and result["decision"] == {"status": "passed"}
    text = render(
        tmp_path,
        repo,
        '{% extends "shared/templates/bases/tier2_text_tracking.jinja2" %}\n'
        "{% block tracking_body %}{{ content.message }}{% endblock %}",
        {"message": "feat(api)!: Explicit subject\n\nCaller body\nRefs: #7"},
    )
    assert text.splitlines()[0].startswith("# pgmcp:v1 id=custom.consumer ")
    assert "feat(api)!: Explicit subject\n\nCaller body\nRefs: #7" in text
    assert "<!--" not in text and "## " not in text
    assert ArtifactHeaderReader().read(text).status is HeaderReadStatus.RECOGNIZED


def test_shared_records_validate_before_render_and_preserve_explicit_check_state(
    tmp_path: Path, pytestconfig: pytest.Config
) -> None:
    template = (
        '{% extends "shared/templates/bases/tier2_markdown_tracking.jinja2" %}\n'
        '{% import "shared/templates/patterns/markdown/sections.jinja2" as sections %}\n'
        "{% block tracking_body %}{{ sections.checklist(content.checklist) }}\n"
        "{{ sections.issue_refs(content.issues) }}{% endblock %}"
    )
    context: dict[str, JsonValue] = {
        "links": [{"label": "Source", "target": "#section"}],
        "issues": [1, 42.0],
        "checklist": [
            {"text": "Observed\ncontinued", "checked": True},
            {"text": "Not observed", "checked": False},
        ],
    }
    output = render_records(tmp_path, pytestconfig.rootpath, template, context)
    assert "- [x] Observed\n      continued\n- [ ] Not observed" in output
    assert "#1, #42" in output and "#42.0" not in output
    invalid: list[dict[str, JsonValue]] = [
        {"links": ["[Source](source.md)"]},
        {"links": [{"label": "Source"}]},
        {"links": [{"label": "", "target": "source.md"}]},
        {"links": [{"label": "Source", "target": None}]},
        {"links": [{"label": "Source", "target": "source.md", "title": "Hidden"}]},
        {"issues": [0]},
        {"issues": [-1]},
        {"issues": [True]},
        {"issues": ["#42"]},
        {"checklist": [{"text": "Implicit"}]},
        {"checklist": [{"text": "Wrong", "checked": "false"}]},
        {"checklist": [{"text": "", "checked": False}]},
        {"checklist": [{"text": "Extra", "checked": False, "done": True}]},
    ]
    for rejected in invalid:
        with pytest.raises(ContextError):
            render_records(tmp_path, pytestconfig.rootpath, template, rejected)
    assert (
        render_records(tmp_path, pytestconfig.rootpath, template, {"issues": [], "checklist": []})
        .strip()
        .endswith("-->")
    )


def test_link_forms_escape_positions_and_keep_occurrence_namespaces(
    tmp_path: Path, pytestconfig: pytest.Config
) -> None:
    template = (
        '{% extends "shared/templates/bases/tier2_markdown_tracking.jinja2" %}\n'
        '{% import "shared/templates/patterns/markdown/links.jinja2" as links %}\n'
        "{% block tracking_body %}{{ links.inline_list(content.links) }}\n"
        "{{ links.reference_list(content.links, 'src') }}\n"
        "{{ links.reference_list(content.links, 'api-2-method-1-src') }}{% endblock %}"
    )
    context: dict[str, JsonValue] = {
        "links": [
            {
                "label": "A [B] \\ C | &copy;",
                "target": "folder with spaces/a[1]\\b.md#Exact-Section",
            },
            {"label": "Duplicate target", "target": "folder with spaces/a[1]\\b.md#Exact-Section"},
            {"label": "Self", "target": "#Exact-Section"},
            {"label": "Pipes", "target": "a|b.md?x=1&copy;"},
        ]
    }
    output = render_records(tmp_path, pytestconfig.rootpath, template, context)
    label = r"A \[B\] \\ C &#124; &amp;copy;"
    target = r"folder with spaces/a[1]\\b.md#Exact-Section"
    assert f"[{label}](<{target}>)" in output
    assert "[Self](<#Exact-Section>)" in output
    assert "[Pipes](<a&#124;b.md?x=1&amp;copy;>)" in output
    for namespace in ("src", "api-2-method-1-src"):
        assert f"[{label}][{namespace}-1]" in output
        assert f"[Duplicate target][{namespace}-2]" in output
        for index, expected in (
            (1, target),
            (2, target),
            (3, "#Exact-Section"),
            (4, "a&#124;b.md?x=1&amp;copy;"),
        ):
            assert output.count(f"[{namespace}-{index}]: <{expected}>") == 1


def test_sections_keep_markdown_rows_lists_and_conflicting_code_delimiters_safe(
    tmp_path: Path, pytestconfig: pytest.Config
) -> None:
    template = (
        '{% extends "shared/templates/bases/tier2_markdown_tracking.jinja2" %}\n'
        '{% import "shared/templates/patterns/markdown/sections.jinja2" as sections %}\n'
        "{% block tracking_body %}{{ sections.heading(content.heading) }}\n"
        "| Value |\n| --- |\n| {{ sections.table_cell(content.cell) }} |\n"
        "{{ sections.bullets(content.bullets) }}\n"
        "{{ sections.code_fence(content.code, 'typescript') }}\n"
        "{{ sections.code_fence(content.tilde_code, content.language) }}\n"
        "{{ sections.inline_code(content.signature) }}\n"
        "{{ sections.inline_code(content.padded) }}{% endblock %}"
    )
    output = render(
        tmp_path,
        pytestconfig.rootpath,
        template,
        {
            "heading": "Section [name]\n# own text #",
            "cell": "**bold** | value\nnext row",
            "bullets": ["First\ncontinued", "Second"],
            "code": "const value = `text`;\n``````\n<kept>",
            "tilde_code": "caller text\n~~~~~~\nkept",
            "language": "lang`info",
            "signature": "`edge`",
            "padded": " surrounded ",
        },
    )
    assert r"## Section \[name\]&#10;# own text \#" in output
    assert "| **bold** \\| value<br>next row |" in output
    assert "- First\n  continued\n- Second" in output
    assert "```````typescript\nconst value = `text`;\n``````\n<kept>\n```````" in output
    assert "~~~~~~~lang`info\ncaller text\n~~~~~~\nkept\n~~~~~~~" in output
    assert "`` `edge` ``" in output
    assert "`  surrounded  `" in output
