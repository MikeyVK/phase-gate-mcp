# tests/mcp_server/unit/services/test_artifact_identity.py

# template=unit_test version=8825c0bb created=2026-09-13T17:02Z updated=

"""Independent canonical byte vectors and generation-closure identity behavior."""

from __future__ import annotations

import base64
import hashlib

import pytest
from pydantic import ValidationError

from mcp_server.config.schemas.template_suite import TemplateManifest
from mcp_server.core.exceptions import MCPError
from mcp_server.services.artifact_identity import (
    GenerationEdge,
    GenerationPackage,
    GenerationSource,
    derive_artifact_identities,
)
from tests.mcp_server.fixtures.suite_roots import SuiteRoots, write_package_tree


def package() -> GenerationPackage:

    return GenerationPackage(
        manifest=TemplateManifest(template_id="alpha", purpose="A"),
        version="1.0.0",
        directory="pkg",
    )


def source_files() -> dict[str, bytes]:

    return {
        "pkg/template.jinja2": b"hello\n",
        "pkg/policy.yaml": b"output_profile: text\npersistence: workspace\n",
        "pkg/.version": b"1.0.0\n",
        "pkg/manifest.yaml": b"template_id: alpha\npurpose: A\n",
        "pkg/context.schema.json": b'{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}\n',
    }


def sources(files: dict[str, bytes]) -> tuple[GenerationSource, ...]:

    return tuple(GenerationSource(path=name, content=value) for name, value in files.items())


def expected_fingerprint(vector: bytes) -> str:
    """Use the standard digest directly over a fixed independently authored vector."""

    return base64.urlsafe_b64encode(hashlib.sha256(vector).digest()[:12]).decode("ascii")


def test_independent_fixed_record_vectors() -> None:

    # v1: domain NUL, then kind NUL, identity NUL, decimal byte length NUL, exact value.

    package_vector = (
        b"pgmcp:resolved-package:v1\x00"
        b"file\x00package/context.schema.json\x0075\x00"
        b'{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}\n'
        b"file\x00package/manifest.yaml\x0030\x00template_id: alpha\npurpose: A\n"
        b"file\x00package/template.jinja2\x006\x00hello\n"
    )

    suite_vector = (
        b"pgmcp:source-suite:v1\x00"
        b"file\x00pkg/context.schema.json\x0075\x00"
        b'{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}\n'
        b"file\x00pkg/manifest.yaml\x0030\x00template_id: alpha\npurpose: A\n"
        b"file\x00pkg/template.jinja2\x006\x00hello\n"
    )

    (identity,) = derive_artifact_identities((package(),), sources(source_files()), ())

    assert identity.model_dump() == {
        "id": "alpha",
        "pv": "1.0.0",
        "pf": expected_fingerprint(package_vector),
        "sf": expected_fingerprint(suite_vector),
    }

    assert identity.pf != identity.sf


@pytest.mark.parametrize("newline", [b"\r\n", b"\r"], ids=["crlf", "cr"])
def test_only_bom_and_line_endings_are_normalized(newline: bytes) -> None:
    original = source_files()
    original["pkg/template.jinja2"] = "héllo\n".encode()
    altered = {
        path: content
        if path.endswith((".version", "policy.yaml"))
        else b"\xef\xbb\xbf" + content.replace(b"\n", newline)
        for path, content in reversed(original.items())
    }
    assert derive_artifact_identities((package(),), sources(original), ()) == (
        derive_artifact_identities((package(),), sources(altered), ())
    )


def test_absolute_roots_do_not_enter_the_supplied_snapshot(suite_roots: SuiteRoots) -> None:
    files = source_files()
    for root in (suite_roots.templates, suite_roots.temp):
        write_package_tree(root, files)
    first = tuple(
        GenerationSource(path=path, content=(suite_roots.templates / path).read_bytes())
        for path in files
    )
    second = tuple(
        GenerationSource(path=path, content=(suite_roots.temp / path).read_bytes())
        for path in files
    )
    assert derive_artifact_identities((package(),), first, ()) == derive_artifact_identities(
        (package(),), second, ()
    )


def test_storage_directory_changes_suite_identity_only() -> None:
    (before,) = derive_artifact_identities((package(),), sources(source_files()), ())
    relocated = GenerationPackage(
        manifest=package().manifest, version="1.0.0", directory="other-location"
    )
    files = {
        path.replace("pkg/", "other-location/", 1): value for path, value in source_files().items()
    }
    (after,) = derive_artifact_identities((relocated,), sources(files), ())
    assert (after.id, after.pv, after.pf) == (before.id, before.pv, before.pf)
    assert after.sf != before.sf


@pytest.mark.parametrize(
    ("version", "change_source"),
    [("1.0.0", False), ("2.0.0", False), ("1.0.0", True), ("2.0.0", True)],
)
def test_all_version_and_fingerprint_relations_are_facts(version: str, change_source: bool) -> None:
    (before,) = derive_artifact_identities((package(),), sources(source_files()), ())
    updated = GenerationPackage(manifest=package().manifest, version=version, directory="pkg")
    files = source_files()
    files["pkg/.version"] = f"{version}\n".encode()
    files["pkg/policy.yaml"] = b"output_profile: text\npersistence: temporary\n"
    if change_source:
        files["pkg/template.jinja2"] += b"{# authored change #}"
    (after,) = derive_artifact_identities((updated,), sources(files), ())
    assert after.pv == version
    assert (before.pv == after.pv) == (version == "1.0.0")
    assert (before.pf != after.pf) == change_source
    assert (before.sf != after.sf) == change_source


@pytest.mark.parametrize("member", ["manifest.yaml", "context.schema.json", "template.jinja2"])
def test_complete_generation_source_bytes_contribute(member: str) -> None:
    (before,) = derive_artifact_identities((package(),), sources(source_files()), ())
    files = source_files()
    files[f"pkg/{member}"] += b"\n"
    (after,) = derive_artifact_identities((package(),), sources(files), ())
    assert before.pf != after.pf
    assert before.sf != after.sf


def shared_snapshot() -> tuple[
    tuple[GenerationPackage, ...], dict[str, bytes], tuple[GenerationEdge, ...]
]:
    """Explicit admitted source/edge facts for independent transitive-closure evidence."""
    packages: list[GenerationPackage] = []
    files: dict[str, bytes] = {}
    edges: list[GenerationEdge] = []
    for identity in ("alpha", "beta", "gamma"):
        packages.append(
            GenerationPackage(
                manifest=TemplateManifest(template_id=identity, purpose="A"),
                version="1.0.0",
                directory=identity,
            )
        )
        files.update(
            {
                path.replace("pkg/", f"{identity}/", 1): value
                for path, value in source_files().items()
            }
        )
        files[f"{identity}/manifest.yaml"] = f"template_id: {identity}\npurpose: A\n".encode()
    for identity in ("alpha", "beta"):
        files[f"{identity}/template.jinja2"] = b'{% extends "shared/templates/base.jinja2" %}'
        edges.append(
            GenerationEdge(
                source=f"{identity}/template.jinja2",
                target="shared/templates/base.jinja2",
                kind="extends",
                position="1",
            )
        )
    files["shared/templates/base.jinja2"] = b'{% include "shared/templates/pattern.jinja2" %}'
    files["shared/templates/pattern.jinja2"] = b"shared text"
    files["shared/templates/unused.jinja2"] = b"unused text"
    files["shared/definitions/record.schema.json"] = (
        b'{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}'
    )
    files["alpha/context.schema.json"] = (
        b'{"$schema":"https://json-schema.org/draft/2020-12/schema",'
        b'"$ref":"../shared/definitions/record.schema.json"}'
    )
    edges.extend(
        (
            GenerationEdge(
                source="shared/templates/base.jinja2",
                target="shared/templates/pattern.jinja2",
                kind="include",
                position="1",
            ),
            GenerationEdge(
                source="alpha/context.schema.json",
                target="shared/definitions/record.schema.json",
                kind="schema_ref",
                position="/$ref",
            ),
        )
    )
    return tuple(packages), files, tuple(edges)


@pytest.mark.parametrize(
    ("changed", "affected"),
    [
        ("shared/templates/pattern.jinja2", {"alpha", "beta"}),
        ("shared/definitions/record.schema.json", {"alpha"}),
        ("shared/templates/unused.jinja2", set()),
        ("beta/template.jinja2", {"beta"}),
    ],
)
def test_package_closures_are_isolated_and_transitive(changed: str, affected: set[str]) -> None:
    packages, files, edges = shared_snapshot()
    before = {item.id: item for item in derive_artifact_identities(packages, sources(files), edges)}
    files[changed] += b"\n"
    after = {item.id: item for item in derive_artifact_identities(packages, sources(files), edges)}
    assert {key for key in before if before[key].pf != after[key].pf} == affected
    assert all(before[key].sf != after[key].sf for key in before)


def test_graph_relationships_contribute_to_package_but_not_source_suite_identity() -> None:
    packages, files, edges = shared_snapshot()
    before = derive_artifact_identities(packages, sources(files), edges)
    # Isolate canonical graph material from source-byte identity, without executing it.
    changed_edges = tuple(
        GenerationEdge(
            source=edge.source, target=edge.target, kind="import", position=edge.position
        )
        if edge.kind == "extends"
        else edge
        for edge in edges
    )
    after = derive_artifact_identities(packages, sources(files), changed_edges)
    assert [item.sf for item in before] == [item.sf for item in after]
    assert {old.id for old, new in zip(before, after, strict=True) if old.pf != new.pf} == {
        "alpha",
        "beta",
    }
    assert before == derive_artifact_identities(
        tuple(reversed(packages)), tuple(reversed(sources(files))), tuple(reversed(edges))
    )


@pytest.mark.parametrize(
    ("extra_path", "error"),
    [
        ("pkg/unexpected.txt", "generation_source_unknown"),
        ("shared/policy.yaml", "generation_source_unknown"),
        ("unknown/template.jinja2", "generation_source_unknown"),
        ("pkg/private.jinja2", "generation_private_source_unreachable"),
    ],
)
def test_unknown_or_unjustified_sources_fail(extra_path: str, error: str) -> None:
    files = {**source_files(), extra_path: b"extra"}
    with pytest.raises(MCPError, match=error):
        derive_artifact_identities((package(),), sources(files), ())


def test_missing_duplicate_and_lateral_inputs_fail() -> None:
    files = source_files()
    files.pop("pkg/manifest.yaml")
    with pytest.raises(MCPError, match="generation_source_missing"):
        derive_artifact_identities((package(),), sources(files), ())
    complete = sources(source_files())
    with pytest.raises(MCPError, match="generation_source_duplicate"):
        derive_artifact_identities((package(),), (*complete, complete[0]), ())
    packages, shared, edges = shared_snapshot()
    for source, target in [
        ("alpha/template.jinja2", "beta/template.jinja2"),
        ("shared/templates/base.jinja2", "alpha/template.jinja2"),
    ]:
        extra = GenerationEdge(source=source, target=target, kind="include")
        with pytest.raises(MCPError, match="generation_dependency_lateral"):
            derive_artifact_identities(packages, sources(shared), (*edges, extra))


@pytest.mark.parametrize("path", ["/absolute/file", "C:/host/file", "../escape", "a//b", "a/./b"])
def test_host_and_noncanonical_source_paths_fail(path: str) -> None:
    with pytest.raises(ValidationError):
        GenerationSource(path=path, content=b"")


def test_results_and_source_snapshots_are_immutable() -> None:
    supplied = sources(source_files())
    (identity,) = derive_artifact_identities((package(),), supplied, ())
    with pytest.raises(ValidationError, match="frozen_instance"):
        identity.pv = "2.0.0"
    with pytest.raises(ValidationError, match="frozen_instance"):
        supplied[0].content = b"changed"
