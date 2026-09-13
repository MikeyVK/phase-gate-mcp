"""Resolve static JSON Schema references without changing their assertion scope."""

from __future__ import annotations

import copy
import re
from collections.abc import Callable
from typing import Any, TypeAlias
from urllib.parse import unquote, urldefrag

from pydantic import JsonValue

JsonSchema: TypeAlias = dict[str, JsonValue] | bool
SchemaDocumentReader: TypeAlias = Callable[[str, str], tuple[str, JsonSchema]]
SchemaLocation: TypeAlias = tuple[str, tuple[str, ...]]
ExpansionGuard: TypeAlias = Callable[[SchemaLocation, tuple[SchemaLocation, ...]], bool]

_SCHEMA_MAPS = frozenset(
    {"$defs", "definitions", "properties", "patternProperties", "dependentSchemas"}
)
_SCHEMA_LISTS = frozenset({"allOf", "anyOf", "oneOf", "prefixItems"})
_SCHEMA_VALUES = frozenset(
    {
        "items",
        "contains",
        "additionalProperties",
        "propertyNames",
        "unevaluatedProperties",
        "unevaluatedItems",
        "not",
        "if",
        "then",
        "else",
        "contentSchema",
    }
)
_FORBIDDEN = frozenset({"$id", "$anchor", "$dynamicRef", "$dynamicAnchor", "$vocabulary"})


def schema_object(value: JsonValue) -> JsonSchema:
    """Narrow a schema position without interpreting its assertions."""
    if isinstance(value, (dict, bool)):
        return value
    raise ValueError("invalid_schema_position")


def resolve_json_schema(
    schema: JsonSchema,
    *,
    document_id: str = "",
    read_document: SchemaDocumentReader | None = None,
    expansion_guard: ExpansionGuard | None = None,
) -> JsonSchema:
    """Prepare finite static references; the injected reader owns document admission.

    Traverse only standard schema positions. Literal annotations and unknown extension
    values remain data. Referenced assertions occupy their own allOf branch so siblings
    cannot overwrite them or change the scope of unevaluated-member constraints.
    """
    resolver = _SchemaResolver(document_id, copy.deepcopy(schema), read_document, expansion_guard)
    return resolver.resolve(document_id)


def resolve_schema_refs(schema: dict[str, Any]) -> dict[str, Any]:
    """Normalize generated MCP object schemas without requiring an authored dialect."""
    resolved = resolve_json_schema(schema)
    if isinstance(resolved, bool):
        return {"allOf": [resolved]}
    return resolved


class _SchemaResolver:
    """One preparation's document cache and active expansion stack."""

    def __init__(
        self,
        document_id: str,
        schema: JsonSchema,
        reader: SchemaDocumentReader | None,
        expansion_guard: ExpansionGuard | None,
    ) -> None:
        self._documents = {document_id: schema}
        self._reader = reader
        self._expansion_guard = expansion_guard
        self._active: set[SchemaLocation] = set()
        self._stack: list[SchemaLocation] = []

    def resolve(self, document_id: str) -> JsonSchema:
        result = self._walk(self._documents[document_id], document_id)
        checked = {document_id}
        while pending := self._documents.keys() - checked:
            for pending_id in pending:
                self._walk(self._documents[pending_id], pending_id)
                checked.add(pending_id)
        return result

    def _walk(
        self, node: JsonSchema, document_id: str, pointer: tuple[str, ...] = ()
    ) -> JsonSchema:
        if isinstance(node, bool):
            return node
        location = (document_id, pointer)
        if location in self._active or (
            self._expansion_guard is not None
            and self._expansion_guard(location, tuple(self._stack))
        ):
            raise ValueError("cyclic_schema_reference")
        if _FORBIDDEN.intersection(node):
            raise ValueError("unsupported_schema_keyword")
        if "$schema" in node and pointer:
            raise ValueError("subschema_dialect")
        self._active.add(location)
        self._stack.append(location)
        try:
            result = self._children(node, document_id, pointer)
            if "$ref" not in node:
                return result
            reference = node["$ref"]
            if not isinstance(reference, str):
                raise ValueError("invalid_schema_reference")
            target = self._reference(reference, document_id)
            if not result:
                return target
            existing = result.get("allOf", [])
            if not isinstance(existing, list):
                raise ValueError("invalid_schema_position")
            result["allOf"] = [*existing, target]
            return result
        finally:
            self._active.remove(location)
            self._stack.pop()

    def _children(
        self, node: dict[str, JsonValue], document_id: str, pointer: tuple[str, ...]
    ) -> dict[str, JsonValue]:
        result: dict[str, JsonValue] = {}
        for key, value in node.items():
            if key == "$ref":
                continue
            if key in _SCHEMA_MAPS:
                if not isinstance(value, dict):
                    raise ValueError("invalid_schema_position")
                prepared: JsonValue = {
                    name: self._walk(schema_object(child), document_id, (*pointer, key, name))
                    for name, child in value.items()
                }
                if key in {"$defs", "definitions"}:
                    continue
            elif key in _SCHEMA_LISTS:
                if not isinstance(value, list):
                    raise ValueError("invalid_schema_position")
                prepared = [
                    self._walk(schema_object(child), document_id, (*pointer, key, str(index)))
                    for index, child in enumerate(value)
                ]
            elif key in _SCHEMA_VALUES:
                prepared = self._walk(schema_object(value), document_id, (*pointer, key))
            else:
                prepared = copy.deepcopy(value)
            result[key] = prepared
        return result

    def _reference(self, reference: str, document_id: str) -> JsonSchema:
        relative, fragment = urldefrag(reference)
        if relative:
            if self._reader is None:
                raise ValueError("external_schema_reference")
            document_id, document = self._reader(document_id, relative)
            if document_id not in self._documents:
                self._documents[document_id] = copy.deepcopy(document)
        document = self._documents[document_id]
        target, pointer = _pointer(document, fragment)
        resolved = self._walk(target, document_id, pointer)
        if isinstance(resolved, dict):
            resolved.pop("$schema", None)
        return resolved


def _pointer(document: JsonSchema, fragment: str) -> tuple[JsonSchema, tuple[str, ...]]:
    """Interpret a URI-fragment JSON Pointer, including escaped and array tokens."""
    fragment = unquote(fragment, errors="strict")
    if not fragment:
        return document, ()
    if not fragment.startswith("/"):
        raise ValueError("unsupported_schema_fragment")
    value: JsonValue = document
    tokens: list[str] = []
    for token in fragment[1:].split("/"):
        if re.search(r"~(?![01])", token):
            raise ValueError("invalid_schema_pointer")
        token = token.replace("~1", "/").replace("~0", "~")
        tokens.append(token)
        if isinstance(value, dict) and token in value:
            value = value[token]
        elif isinstance(value, list) and re.fullmatch(r"0|[1-9][0-9]*", token):
            index = int(token)
            if index >= len(value):
                raise ValueError("unresolved_schema_pointer")
            value = value[index]
        else:
            raise ValueError("unresolved_schema_pointer")
    return schema_object(value), tuple(tokens)
