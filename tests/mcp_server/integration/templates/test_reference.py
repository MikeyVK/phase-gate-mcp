"""Exercise Reference package behavior without coupling tests to editorial headings."""

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
def reference(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=suite,
        source_package=suite / "reference",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "explicit suite",
        template_id="reference",
    )
    selected = delivered.catalog.get("reference")
    assert selected.policy.persistence == "workspace"
    assert dict(delivered.checks.profiles)[selected.policy.output_profile].checks == (
        "markdown_document",
    )
    return delivered


def test_minimal_reference_accepts_required_source_and_empty_api(
    reference: DeliveredTemplate,
    markdown_package: MarkdownPackage,
    tmp_path: Path,
) -> None:
    context: dict[str, JsonValue] = {
        "title": "Reference basis",
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
        "sources": [{"label": "Primary source", "target": "source.md#Overview"}],
        "api_reference": [],
    }
    before = deepcopy(context)
    output = reference.renderer.render("reference", context, reference.provenance)
    assert context == before
    assert f"# {context['title']}" in output
    assert "[Primary source][src-1]" in output
    assert "[src-1]: <source.md#Overview>" in output
    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "reference"
    code, response = invoke(markdown_package, tmp_path, request(tmp_path / "reference.md", output))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "reference.md").exists()


def test_reference_preserves_grouping_links_and_safe_native_code_rendering(
    reference: DeliveredTemplate,
    markdown_package: MarkdownPackage,
    tmp_path: Path,
) -> None:
    signature = chr(96) + "read(value: str)" + chr(96)
    example_code = "const value = reader.read(input);\n" + chr(96) * 3 + "\ninside"
    context: dict[str, JsonValue] = {
        "title": "Boundary reference",
        "document_metadata": {
            "status": "DRAFT — awaiting review",
            "revisions": [
                {
                    "version": "4.1",
                    "date": "2026-09-14",
                    "author": "Template fixture",
                    "change": "Authored fixture revision.",
                }
            ],
        },
        "purpose": "Purpose marker.",
        "scope_in": "Included marker.",
        "scope_out": "Excluded marker.",
        "prerequisites": ["Prerequisite marker"],
        "related_docs": [{"label": "Self", "target": "#Own-Reference"}],
        "sources": [
            {"label": "Primary source", "target": "source.md#Overview"},
            {"label": "Duplicate target", "target": "source.md#Overview"},
        ],
        "test_evidence": [
            {"label": "Test evidence", "target": "source.md#Overview"},
            {"label": "Second test", "target": "test.md#Run"},
        ],
        "api_reference": [
            {
                "name": "Reader API #",
                "description": "Reader component marker.",
                "methods": [
                    {
                        "signature": signature,
                        "parameters": "",
                        "returns": "str",
                        "description": "Method description marker.",
                        "errors": "Method error marker.",
                        "sources": [{"label": "API source", "target": "api.md#Reader"}],
                    },
                    {
                        "signature": "close()",
                        "parameters": "none",
                        "returns": "",
                        "sources": [{"label": "Method source", "target": "api.md#Reader"}],
                    },
                ],
                "sources": [{"label": "Component source", "target": "api.md#Reader"}],
            },
            {
                "name": "Writer API",
                "description": "",
                "methods": [
                    {
                        "signature": "write(value: str)",
                        "parameters": "",
                        "returns": "",
                        "sources": [],
                    },
                    {
                        "signature": "flush()",
                        "parameters": "",
                        "returns": "",
                        "sources": [{"label": "Writer method source", "target": "writer.md#Flush"}],
                    },
                ],
                "sources": [],
            },
            {"name": "Unexpanded API", "description": ""},
            {"name": "Reserved API", "description": "", "methods": []},
        ],
        "usage_examples": [
            {
                "description": "TypeScript usage",
                "language": "TypeScript",
                "code": example_code,
            },
            {"description": "Shell usage", "language": "Shell", "code": ""},
        ],
    }
    before = deepcopy(context)
    output = reference.renderer.render("reference", context, reference.provenance)
    assert context == before
    for key in ("purpose", "scope_in", "scope_out"):
        value = context[key]
        assert isinstance(value, str) and value in output
    assert output.index("Reader API") < output.index("Writer API")
    assert output.index("read(value: str)") < output.index("close()")
    fence = chr(96) * 4
    assert fence + "TypeScript\n" + example_code + "\n" + fence in output
    inline = chr(96) * 2
    assert inline + " " + signature + " " + inline in output
    reader_group = output.split("Reader API", 1)[1].split("Writer API", 1)[0]
    writer_group = output.split("Writer API", 1)[1].split("\n### ", 1)[0]
    assert "read(value: str)" in reader_group and "close()" in reader_group
    assert "write(value: str)" not in reader_group
    assert "write(value: str)" in writer_group and "flush()" in writer_group
    assert "read(value: str)" not in writer_group
    assert "[Self](<#Own-Reference>)" in output
    expected_definitions = {
        "src-1": "source.md#Overview",
        "src-2": "source.md#Overview",
        "test-1": "source.md#Overview",
        "test-2": "test.md#Run",
        "api-1-src-1": "api.md#Reader",
        "api-1-method-1-src-1": "api.md#Reader",
        "api-1-method-2-src-1": "api.md#Reader",
        "api-2-method-2-src-1": "writer.md#Flush",
    }
    for reference_id, target in expected_definitions.items():
        assert output.count(f"[{reference_id}]") == 2
        assert output.count(f"[{reference_id}]: <{target}>") == 1
    code, response = invoke(markdown_package, tmp_path, request(tmp_path / "populated.md", output))
    assert code == 0 and response["decision"] == {"status": "passed"}


def test_reference_distinguishes_absent_and_explicit_empty_optional_values(
    reference: DeliveredTemplate,
) -> None:
    base: dict[str, JsonValue] = {
        "title": "Optional reference",
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
        "sources": [{"label": "Required source", "target": "#Source"}],
        "api_reference": [
            {
                "name": "Stable API",
                "description": "Stable API marker.",
                "methods": [
                    {
                        "signature": "stable()",
                        "parameters": "",
                        "returns": "str",
                    }
                ],
            }
        ],
    }
    absent = reference.renderer.render("reference", base, reference.provenance)
    explicit = {
        **base,
        "purpose": "",
        "scope_in": "",
        "scope_out": "",
        "prerequisites": [],
        "related_docs": [],
        "test_evidence": [],
        "usage_examples": [],
        "api_reference": [
            {
                "name": "Stable API",
                "description": "Stable API marker.",
                "methods": [
                    {
                        "signature": "stable()",
                        "parameters": "",
                        "returns": "str",
                        "description": "",
                        "errors": "",
                        "sources": [],
                    }
                ],
                "sources": [],
            }
        ],
    }
    before = deepcopy(explicit)
    populated = reference.renderer.render("reference", explicit, reference.provenance)
    assert explicit == before
    assert populated.split() != absent.split()
    assert "Stable API" in absent and "stable()" in absent
    assert "Stable API" in populated and "stable()" in populated
    assert "Required source" in populated
    assert "Optional reference" in populated


def test_reference_rejects_invalid_and_legacy_shapes(
    reference: DeliveredTemplate,
) -> None:
    base: dict[str, JsonValue] = {
        "title": "Reference",
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
        "sources": [{"label": "Source", "target": "source.md"}],
        "api_reference": [],
    }
    invalid: list[dict[str, JsonValue]] = [
        {
            "title": "Reference",
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
            "api_reference": [],
        },
        {**base, "sources": []},
        {**base, "sources": [{"label": "Source"}]},
        {**base, "sources": [{"target": "source.md"}]},
        {**base, "source_file": "source.md"},
        {**base, "test_file": "test.md"},
        {**base, "test_count": 1},
        {
            **base,
            "usage_examples": [
                {"description": "Example", "language": "Type\nScript", "code": "run"}
            ],
        },
        {**base, "usage_examples": [{"description": None, "language": "Shell", "code": "run"}]},
        {**base, "usage_examples": [{"description": "Example", "code": "run"}]},
        {**base, "usage_examples": ["Example"]},
        {
            **base,
            "api_reference": [
                {
                    "name": "API",
                    "description": "",
                    "methods": [
                        {"parameters": "", "returns": ""},
                    ],
                }
            ],
        },
        {
            **base,
            "api_reference": [
                {
                    "name": "API",
                    "description": "",
                    "methods": [
                        {
                            "signature": "run()",
                            "parameters": "",
                            "returns": "",
                            "sources": [{"target": "api.md"}],
                        },
                    ],
                }
            ],
        },
        {
            **base,
            "api_reference": [
                {
                    "name": "API",
                    "description": "",
                    "methods": [
                        {"signature": "run()", "parameters": None, "returns": ""},
                    ],
                }
            ],
        },
        {**base, "api_reference": [{"name": "API", "description": None, "methods": []}]},
        {
            **base,
            "api_reference": [
                {
                    "name": "API",
                    "description": "",
                    "methods": [
                        {"signature": "run()", "parameters": "", "returns": "", "methods": []},
                    ],
                }
            ],
        },
        {**base, "workflow": "reference"},
    ]
    for context in invalid:
        with pytest.raises(ContextError):
            reference.renderer.render("reference", context, reference.provenance)
