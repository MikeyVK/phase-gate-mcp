# mcp_server/services/artifact_identity.py
# template=service version=5d5b489a created=2026-09-13T17:02Z updated=
"""Pure generation identity over admitted source snapshots; no filesystem or history access."""

from __future__ import annotations

import base64
import hashlib
import json
import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator

from mcp_server.config.schemas.template_suite import (
    TemplateId,
    TemplateManifest,
    TemplatePackageVersion,
)
from mcp_server.core.exceptions import MCPError
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
    """Derive equality facts from a complete resolver-produced source snapshot.

    Parsing, schema semantics and graph admission belong to the suite resolvers.
    These inputs are internal facts, never an authored contributor inventory.
    """
    directories = {package.directory: package for package in packages}
    identities = {package.manifest.template_id for package in packages}
    if not packages or len(directories) != len(packages) or len(identities) != len(packages):
        raise MCPError("generation_package_inventory_invalid", code="ERR_CONFIG")
    files = {source.path: source.content for source in sources}
    if len(files) != len(sources):
        raise MCPError("generation_source_duplicate", code="ERR_CONFIG")
    for directory in directories:
        missing = {
            f"{directory}/{member}"
            for member in (
                "manifest.yaml",
                "context.schema.json",
                "template.jinja2",
                ".version",
                "policy.yaml",
            )
        } - files.keys()
        if missing:
            raise _source_error("generation_source_missing", min(missing))

    generation = {
        path: normalize_source_bytes(content)
        for path, content in files.items()
        if _generation_source(path, directories.keys())
    }
    adjacency: dict[str, set[str]] = {}
    for edge in edges:
        if edge.source not in generation or edge.target not in generation:
            raise _source_error("generation_dependency_missing", edge.target)
        source_owner = edge.source.split("/", 1)[0]
        target_owner = edge.target.split("/", 1)[0]
        if target_owner not in {source_owner, "shared"}:
            raise _source_error("generation_dependency_lateral", edge.target)
        suffix = ".json" if edge.kind == "schema_ref" else ".jinja2"
        if not edge.source.endswith(suffix) or not edge.target.endswith(suffix):
            raise _source_error("generation_dependency_kind_invalid", edge.target)
        adjacency.setdefault(edge.source, set()).add(edge.target)

    closures: dict[str, frozenset[str]] = {}
    for package in packages:
        pending = [
            f"{package.directory}/{member}"
            for member in ("manifest.yaml", "context.schema.json", "template.jinja2")
        ]
        visited: set[str] = set()
        while pending:
            path = pending.pop()
            if path not in visited:
                visited.add(path)
                pending.extend(adjacency.get(path, ()))
        closures[package.directory] = frozenset(visited)
    reached = set().union(*closures.values())
    for path in generation:
        if not path.startswith("shared/") and path not in reached:
            raise _source_error("generation_private_source_unreachable", path)

    suite_fingerprint = fingerprint_records(
        "pgmcp:source-suite:v1",
        (FingerprintRecord("file", path, content) for path, content in generation.items()),
    )
    result: list[ArtifactIdentity] = []
    for package in sorted(packages, key=lambda item: item.manifest.template_id):
        closure = closures[package.directory]
        records = [
            FingerprintRecord("file", _package_path(path, package.directory), generation[path])
            for path in closure
        ]
        records.extend(
            FingerprintRecord(
                f"edge:{edge.kind}",
                json.dumps(
                    [
                        _package_path(edge.source, package.directory),
                        _package_path(edge.target, package.directory),
                        edge.position,
                    ],
                    ensure_ascii=False,
                    separators=(",", ":"),
                ),
                b"",
            )
            for edge in edges
            if edge.source in closure
        )
        result.append(
            ArtifactIdentity(
                id=package.manifest.template_id,
                pv=package.version,
                pf=fingerprint_records("pgmcp:resolved-package:v1", records),
                sf=suite_fingerprint,
            )
        )
    return tuple(result)


@dataclass(frozen=True)
class FingerprintRecord:
    kind: str
    identity: str
    value: bytes


def fingerprint_records(domain: str, records: Iterable[FingerprintRecord]) -> str:
    """v1 fields are NUL-delimited; values are framed by decimal UTF-8 byte length."""
    digest = hashlib.sha256()
    digest.update(domain.encode("ascii") + b"\x00")
    for record in sorted(set(records), key=lambda item: (item.kind, item.identity)):
        digest.update(record.kind.encode("utf-8") + b"\x00")
        digest.update(record.identity.encode("utf-8") + b"\x00")
        digest.update(str(len(record.value)).encode("ascii") + b"\x00")
        digest.update(record.value)
    return base64.urlsafe_b64encode(digest.digest()[:12]).decode("ascii")


def normalize_source_bytes(content: bytes) -> bytes:
    return content.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def _package_path(path: str, directory: str) -> str:
    prefix = f"{directory}/"
    return f"package/{path.removeprefix(prefix)}" if path.startswith(prefix) else path


def _generation_source(path: str, directories: Iterable[str]) -> bool:
    owner, _, relative = path.partition("/")
    if owner == "shared":
        if relative.startswith("templates/") and relative.endswith(".jinja2"):
            return True
        if relative.startswith("definitions/") and relative.endswith(".schema.json"):
            return True
        raise _source_error("generation_source_unknown", path)
    if owner not in directories:
        raise _source_error("generation_source_unknown", path)
    if relative in {".version", "policy.yaml"}:
        return False
    if relative in {"manifest.yaml", "context.schema.json", "template.jinja2"}:
        return True
    if relative.endswith((".json", ".jinja2")):
        return True
    raise _source_error("generation_source_unknown", path)


def _source_error(key: str, path: str) -> MCPError:
    return MCPError(key, code="ERR_CONFIG", params={"source": path})
