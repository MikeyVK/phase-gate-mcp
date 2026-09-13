# tests/mcp_server/unit/services/test_artifact_identity.py
# template=unit_test version=8825c0bb created=2026-09-13T17:02Z updated=
"""Independent canonical byte vectors and generation-closure identity behavior."""

from __future__ import annotations

import base64
import hashlib

from mcp_server.config.schemas.template_suite import TemplateManifest
from mcp_server.services.artifact_identity import (
    GenerationPackage,
    GenerationSource,
    derive_artifact_identities,
)


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
        "pkg/context.schema.json":
            b'{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}\n',
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

