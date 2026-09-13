# mcp_server/services/artifact_identity.py
# template=service version=5d5b489a created=2026-09-13T17:02Z updated=
"""Pure generation identity over admitted source snapshots; no filesystem or history access."""

from __future__ import annotations

import re
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator

from mcp_server.config.schemas.template_suite import (
    TemplateId,
    TemplateManifest,
    TemplatePackageVersion,
)
from mcp_server.services.template_graph import EdgeKind

CompactFingerprint = Annotated[
    str,
    StringConstraints(
        strict=True,
        min_length=16,
        max_length=16,
        pattern=re.compile(r"^[A-Za-z0-9_-]{16}$(?![\s\S])"),
    ),
]


class GenerationSource(BaseModel):
    """One exact admitted source at a normalized suite-relative path."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    path: str
    content: bytes

    @field_validator("path")
    @classmethod
    def relative_path(cls, value: str) -> str:
        """Reject host paths and noncanonical logical spelling."""
        return _relative_path(value)


class GenerationPackage(BaseModel):
    """Admitted package facts; the storage directory is not semantic identity."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    manifest: TemplateManifest
    version: TemplatePackageVersion
    directory: str

    @field_validator("directory")
    @classmethod
    def direct_directory(cls, value: str) -> str:
        """Require one non-reserved direct package locator."""
        _relative_path(value)
        if "/" in value or value == "shared":
            raise ValueError("generation_package_directory_invalid")
        return value


class GenerationEdge(BaseModel):
    """A resolver-derived typed file dependency, with its stable source position."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    source: str
    target: str
    kind: EdgeKind | Literal["schema_ref"]
    position: str = ""

    @field_validator("source", "target")
    @classmethod
    def relative_endpoint(cls, value: str) -> str:
        """Use logical file endpoints, never host paths."""
        return _relative_path(value)


class ArtifactIdentity(BaseModel):
    """The four canonical generation facts consumed by artifact provenance."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    id: TemplateId
    pv: TemplatePackageVersion
    pf: CompactFingerprint
    sf: CompactFingerprint


def _relative_path(value: str) -> str:
    if (
        not value
        or "\\" in value
        or ":" in value
        or "\x00" in value
        or any(part in {"", ".", ".."} for part in value.split("/"))
    ):
        raise ValueError("generation_source_path_invalid")
    return value


def derive_artifact_identities(
    packages: tuple[GenerationPackage, ...],
    sources: tuple[GenerationSource, ...],
    edges: tuple[GenerationEdge, ...],
) -> tuple[ArtifactIdentity, ...]:
    """Derive package/suite equality facts from one admitted immutable input."""
    raise NotImplementedError
