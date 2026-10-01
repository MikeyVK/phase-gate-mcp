# mcp_server/services/template_contract_loader.py
# template=service version=5d5b489a created=2026-09-13T15:22Z updated=
"""Prepare explicit, contained template context schemas without activating startup readers."""

from __future__ import annotations

import json
import os
import re
from itertools import pairwise
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

from jsonschema import Draft202012Validator
from pydantic import JsonValue

from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json, thaw_json
from mcp_server.utils.schema_utils import JsonSchema, SchemaLocation, resolve_json_schema

DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"


class TemplateContractLoader:
    """Read one suite's admitted schema graph into a detached immutable exposure."""

    def __init__(self, suite_root: Path) -> None:
        if not suite_root.is_absolute():
            raise ValueError("absolute_suite_root_required")
        self._suite_root = suite_root.resolve()
        self._reference_edges: set[tuple[str, str, str]] = set()

    @property
    def reference_edges(self) -> tuple[tuple[str, str, str], ...]:
        """Return admitted cross-file schema references for generation provenance."""
        return tuple(sorted(self._reference_edges))

    def load_context_schema(self, schema_path: Path) -> FrozenJsonObject:
        """Prepare a fresh snapshot; subsequent validation never reopens schema files."""
        path, owner = self._admit_path(schema_path)
        if owner == "shared":
            raise ValueError("package_context_required")
        documents = {path: _read_document(path)}
        reference_floors: dict[tuple[str, str], Path] = {}

        def read_reference(referrer: str, reference: str) -> tuple[str, JsonSchema]:
            target, floor = self._reference_path(Path(referrer), reference)
            self._reference_edges.add(
                (
                    Path(referrer).relative_to(self._suite_root).as_posix(),
                    target.relative_to(self._suite_root).as_posix(),
                    reference,
                )
            )
            previous = reference_floors.get((referrer, str(target)), floor)
            while not previous.is_relative_to(floor):
                floor = floor.parent
            reference_floors[(referrer, str(target))] = floor
            if target not in documents:
                documents[target] = _read_document(target)
            return str(target), documents[target]

        resolved = resolve_json_schema(
            documents[path],
            document_id=str(path),
            read_document=read_reference,
            expansion_guard=lambda location, ancestors: _expanding_alias_cycle(
                location, ancestors, reference_floors
            ),
        )
        Draft202012Validator.check_schema(resolved)
        frozen = freeze_json(resolved)
        if not isinstance(frozen, FrozenJsonObject):
            raise ValueError("context_schema_object_required")
        return frozen

    def _admit_path(self, path: Path) -> tuple[Path, str]:
        candidate = path if path.is_absolute() else self._suite_root / path
        lexical = Path(os.path.abspath(candidate))
        resolved = lexical.resolve(strict=True)
        lexical_owner = self._owner(lexical)
        if self._owner(resolved) != lexical_owner:
            raise ValueError("schema_symlink_boundary")
        if not resolved.is_file():
            raise ValueError("schema_file_required")
        # URI bases retain lexical location; only containment and cycle identity use real paths.
        return lexical, lexical_owner

    def _owner(self, path: Path) -> str:
        if not path.is_relative_to(self._suite_root):
            raise ValueError("schema_outside_suite")
        parts = path.relative_to(self._suite_root).parts
        if len(parts) < 2:
            raise ValueError("schema_package_required")
        if parts[0] == "shared" and (len(parts) < 3 or parts[1] != "definitions"):
            raise ValueError("schema_shared_definitions_required")
        return parts[0]

    def _reference_path(self, referrer: Path, reference: str) -> tuple[Path, Path]:
        uri = urlsplit(reference)
        if uri.scheme or uri.netloc or uri.query or uri.fragment:
            raise ValueError("external_schema_reference")
        if re.search(r"%(?![0-9a-fA-F]{2})", uri.path):
            raise ValueError("invalid_schema_reference")
        decoded = unquote(uri.path, errors="strict")
        if not decoded or decoded.startswith("/") or "\\" in decoded or ":" in decoded:
            raise ValueError("absolute_schema_reference")
        target, owner = self._admit_path(referrer.parent / decoded)
        source_owner = self._owner(referrer)
        if owner != source_owner and owner != "shared":
            raise ValueError("schema_dependency_direction")
        # Track the lowest lexical directory visited before dot-segment normalization.
        cursor = referrer.parent
        floor = cursor
        for part in PurePosixPath(decoded).parts:
            cursor = cursor.parent if part == ".." else cursor / part
            if len(cursor.parts) < len(floor.parts):
                floor = cursor
        return target, floor


def _read_document(path: Path) -> dict[str, JsonValue]:
    """Read finite JSON, check the declared dialect and delegate schema shape validation."""
    raw = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    document = thaw_json(freeze_json(raw))
    if not isinstance(document, dict) or document.get("$schema") != DRAFT_2020_12:
        raise ValueError("authored_schema_dialect_required")
    Draft202012Validator.check_schema(document)
    return document


def _unique_object(pairs: list[tuple[str, JsonValue]]) -> dict[str, JsonValue]:
    result: dict[str, JsonValue] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate_schema_key")
        result[key] = value
    return result


def _expanding_alias_cycle(
    location: SchemaLocation,
    ancestors: tuple[SchemaLocation, ...],
    reference_floors: dict[tuple[str, str], Path],
) -> bool:
    """Reject repeatable directory-alias growth, not terminating physical revisits.

    A repeated physical schema and pointer with the same physical base can repeat
    indefinitely when its logical base grew below the previous base and the intervening
    walk never climbed outside that base. A walk that consumes ancestor segments can
    instead terminate and must remain governed by ordinary logical URI cycle detection.
    """
    current = Path(location[0])
    physical = current.resolve(strict=True)
    physical_base = current.parent.resolve(strict=True)
    for index, (document_id, pointer) in enumerate(ancestors):
        previous = Path(document_id)
        base = previous.parent
        walk = (*ancestors[index:], location)
        if (
            pointer == location[1]
            and current.parent != base
            and current.parent.is_relative_to(base)
            and previous.resolve(strict=True) == physical
            and base.resolve(strict=True) == physical_base
            and all(
                reference_floors[(source[0], target[0])].is_relative_to(base)
                for source, target in pairwise(walk)
                if source[0] != target[0]
            )
        ):
            return True
    return False
