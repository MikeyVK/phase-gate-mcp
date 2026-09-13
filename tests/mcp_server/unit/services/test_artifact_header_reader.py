# tests/mcp_server/unit/services/test_artifact_header_reader.py
# template=unit_test version=8825c0bb created=2026-09-13T17:18Z updated=
"""Independent first-line vectors and rendering through the retained shared Jinja root."""

from __future__ import annotations

from pathlib import Path

import pytest
from jinja2 import DictLoader, Environment, StrictUndefined
from pydantic import ValidationError

from mcp_server.core.interfaces.artifact_header_reader import (
    HeaderReadResult,
    HeaderReadStatus,
    IArtifactHeaderReader,
)
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from mcp_server.services.artifact_identity import ArtifactIdentity
from mcp_server.services.template_graph import TemplateGraphResolver
from tests.mcp_server.fixtures.suite_roots import SuiteRoots, write_package_tree

RECORD = "pgmcp:v1 id=example pv=1.2.3 pf=AbCdEfGhIjKlMn_- sf=0123456789abcdef"
ROOT_NAME = "shared/templates/bases/tier0_root.jinja2"


def provenance() -> ArtifactIdentity:
    """Use independently authored values, unrelated to any catalog or filename."""
    return ArtifactIdentity(
        id="example", pv="1.2.3", pf="AbCdEfGhIjKlMn_-", sf="0123456789abcdef"
    )


@pytest.mark.parametrize("line", [f"# {RECORD}", f"// {RECORD}", f"<!-- {RECORD} -->"])
@pytest.mark.parametrize("ending", ["", "\n", "\r\n"])
@pytest.mark.parametrize("bom", ["", "\ufeff"])
def test_complete_native_frames(line: str, ending: str, bom: str) -> None:
    original = bom + line + ending + ("body\n" if ending else "")
    unchanged = original
    reader: IArtifactHeaderReader = ArtifactHeaderReader()
    result = reader.read(original)
    assert result.status is HeaderReadStatus.RECOGNIZED
    assert result.provenance == provenance()
    assert original == unchanged


@pytest.mark.parametrize(
    "text",
    ["", "ordinary text", f"\n# {RECORD}", f"#!/bin/sh\n# {RECORD}",
     f"body\r\n<!-- {RECORD} -->", f"x" * 100_000 + f"\n# {RECORD}"],
)
def test_absence_never_searches_later_lines(text: str) -> None:
    assert ArtifactHeaderReader().read(text) == HeaderReadResult(
        status=HeaderReadStatus.ABSENT, provenance=None
    )


@pytest.mark.parametrize(
    "line",
    [
        RECORD,
        f"/* {RECORD} */",
        f"#  {RECORD}",
        f" # {RECORD}",
        f"# {RECORD} ",
        f"<!-- {RECORD}",
        f"<!-- {RECORD} --> tail",
        f"// {RECORD} -->",
        f"\ufeff\ufeff# {RECORD}",
        f"# {RECORD}\r",
        f"# {RECORD}".replace("pgmcp:v1", "pgmcp:v2"),
        f"# {RECORD}".replace(" id=example", ""),
        f"# {RECORD}".replace(" id=example pv=1.2.3", " pv=1.2.3 id=example"),
        f"# {RECORD}".replace(" pv=1.2.3", " id=second pv=1.2.3"),
        f"# {RECORD} extra=value",
        f"# {RECORD}".replace("id=example", "id=bad=id"),
        f"# {RECORD}".replace("pv=1.2.3", "pv=01.2.3"),
        f"# {RECORD}".replace("pf=AbCdEfGhIjKlMn_-", "pf=AbCdEfGhIjKlMn_="),
        f"# {RECORD}".replace("sf=0123456789abcdef", "sf=0123456789abcde"),
        f"# {RECORD}".replace("sf=0123456789abcdef", "sf=0123456789abcdefg"),
        f"# {RECORD}".replace("id=example", "id=" + "a" * 25),
        f"# {RECORD}".replace("pv=1.2.3", "pv=1.2.3-alpha1"),
        f"# {RECORD}".replace("id=example", "id=example\t"),
        f"# {RECORD}".replace("id=example", "id=bad\x00id"),
        f"# {RECORD}" + "x" * 100_000,
    ],
)
def test_rejected_headers_never_expose_partial_provenance(line: str) -> None:
    result = ArtifactHeaderReader().read(line)
    assert result.status is HeaderReadStatus.INVALID
    assert result.provenance is None


@pytest.mark.parametrize("ending", ["", "\n", "\r\n"])
def test_exact_maximum_character_budget_with_bom(ending: str) -> None:
    # SemVer at the full eleven-character boundary.
    record = ArtifactIdentity(id="a" * 24, pv="10.2.3-beta1", pf="A" * 16, sf="B" * 16)
    line = "<!-- pgmcp:v1 id=" + "a" * 24 + " pv=10.2.3-beta1 pf=" + "A" * 16
    line += " sf=" + "B" * 16 + " -->"
    assert len(line) == 100
    assert ArtifactHeaderReader().read("\ufeff" + line + ending).provenance == record
    result = ArtifactHeaderReader().read("\ufeff" + line + " " + ending)
    assert result.status is HeaderReadStatus.INVALID
    assert result.provenance is None


@pytest.mark.parametrize(
    ("status", "has_provenance", "valid"),
    [
        (HeaderReadStatus.RECOGNIZED, True, True),
        (HeaderReadStatus.RECOGNIZED, False, False),
        (HeaderReadStatus.ABSENT, False, True),
        (HeaderReadStatus.ABSENT, True, False),
        (HeaderReadStatus.INVALID, False, True),
        (HeaderReadStatus.INVALID, True, False),
    ],
)
def test_closed_result_combinations(
    status: HeaderReadStatus, has_provenance: bool, valid: bool
) -> None:
    values = {"status": status, "provenance": provenance() if has_provenance else None}
    if valid:
        result = HeaderReadResult.model_validate(values)
        with pytest.raises(ValidationError):
            result.status = HeaderReadStatus.INVALID
        if result.provenance is not None:
            with pytest.raises(ValidationError):
                result.provenance.id = "changed"
    else:
        with pytest.raises(ValidationError, match="header_result_inconsistent"):
            HeaderReadResult.model_validate(values)


@pytest.mark.parametrize(
    "values",
    [
        {"status": HeaderReadStatus.ABSENT},
        {"status": "absent", "provenance": None},
        {"status": HeaderReadStatus.ABSENT, "provenance": None, "reason": "extra"},
        {"status": HeaderReadStatus.RECOGNIZED, "provenance": {"id": "partial"}},
    ],
)
def test_result_rejects_defaults_coercion_extras_and_partial_records(
    values: dict[str, object],
) -> None:
    with pytest.raises(ValidationError):
        HeaderReadResult.model_validate(values)


@pytest.mark.parametrize(
    ("frame_start", "frame_end"),
    [("#", ""), ("//", ""), ("<!--", " -->")],
)
def test_selected_graph_renders_retained_root_and_round_trips(
    suite_roots: SuiteRoots, frame_start: str, frame_end: str
) -> None:
    root_path = Path(__file__).resolve().parents[4] / ".pgmcp/template_suite" / ROOT_NAME
    native_base = (
        '{% extends "' + ROOT_NAME + '" %}'
        "{% block comment_start %}" + frame_start + "{% endblock %}"
        "{% block comment_end %}" + frame_end + "{% endblock %}"
    )
    write_package_tree(
        suite_roots.templates,
        {
            ROOT_NAME: root_path.read_bytes(),
            "shared/templates/bases/native.jinja2": native_base.encode(),
            "opaque/template.jinja2": (
                b'{% extends "shared/templates/bases/native.jinja2" %}'
                b"{% block content %}{{ content.body }}{% endblock %}"
            ),
        },
    )
    graph = TemplateGraphResolver(suite_roots.templates, Environment().parse).resolve(
        [("example", "opaque/template.jinja2")]
    )
    assert set(graph.roots[0].closure) == {
        ROOT_NAME, "shared/templates/bases/native.jinja2", "opaque/template.jinja2"
    }
    renderer = Environment(
        loader=DictLoader(
            {source.name: source.content.decode("utf-8") for source in graph.sources}
        ),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    rendered = renderer.get_template(graph.roots[0].template_name).render(
        provenance=provenance(), content={"body": "original body\n"}
    )
    assert rendered == frame_start + " " + RECORD + frame_end + "\noriginal body\n"
    assert ArtifactHeaderReader().read(rendered).provenance == provenance()
