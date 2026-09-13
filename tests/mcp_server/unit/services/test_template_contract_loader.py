# tests/mcp_server/unit/services/test_template_contract_loader.py
# template=unit_test version=8825c0bb created=2026-09-13T15:22Z updated=
"""Exercise real schema files and compare preparation with an independent draft validator."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError
from pydantic import JsonValue
from referencing import Registry, Resource

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.exceptions import ConfigError
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, thaw_json
from mcp_server.services.template_contract_loader import DRAFT_2020_12, TemplateContractLoader
from tests.mcp_server.fixtures.suite_roots import SuiteRoots, write_package_tree


def write_schemas(root: Path, documents: dict[str, dict[str, JsonValue]]) -> None:
    """Write only the authored documents supplied by each test."""
    write_package_tree(root, {name: json.dumps(doc).encode() for name, doc in documents.items()})


def oracle(
    root: Path, documents: dict[str, dict[str, JsonValue]], entry: str
) -> Draft202012Validator:
    """Resolve authored references through the library's separate offline registry."""
    registry: Registry[dict[str, JsonValue]] = Registry().with_resources(
        ((root / name).as_uri(), Resource.from_contents(document))
        for name, document in documents.items()
    )
    return Draft202012Validator({"$ref": (root / entry).as_uri()}, registry=registry)


class TestTemplateContractLoader:
    """Contained preparation, immutable validation and legacy constructor preservation."""

    @pytest.mark.parametrize(
        ("context", "accepted"),
        [
            ({}, True),
            ({"label": ""}, True),
            ({"label": None}, True),
            ({"enabled": False, "count": 0}, True),
            ({"count": 2.0}, True),
            ({"count": 2.5}, False),
            ({"enabled": 0}, False),
            ({"link": {"target": "here"}}, True),
            ({"link": {}}, False),
            ({"link": {"target": ""}}, False),
            ({"link": {"target": "here", "unknown": 1}}, False),
            ({"unknown": "value"}, False),
            ({"forbidden": None}, False),
            ({"date": "tomorrow"}, True),
        ],
    )
    def test_shared_nested_schema_parity_and_presence(
        self, suite_roots: SuiteRoots, context: dict[str, JsonValue], accepted: bool
    ) -> None:
        """Nested shared definitions and caller values retain draft-2020-12 meaning."""
        root = suite_roots.templates
        documents: dict[str, dict[str, JsonValue]] = {
            "pkg/context.schema.json": {
                "$schema": DRAFT_2020_12,
                "type": "object",
                "properties": {
                    "label": {"type": ["string", "null"], "default": "not inserted"},
                    "enabled": {"type": "boolean", "default": True},
                    "count": {"type": "integer"},
                    "link": {"$ref": "../shared/definitions/links.json#/$defs/Link"},
                    "forbidden": {"$ref": "#/$defs/Never"},
                    "date": {"type": "string", "format": "date"},
                },
                "$defs": {"Never": False},
                "additionalProperties": False,
            },
            "shared/definitions/links.json": {
                "$schema": DRAFT_2020_12,
                "$defs": {
                    "Link": {
                        "type": "object",
                        "required": ["target"],
                        "additionalProperties": False,
                        "properties": {"target": {"$ref": "text.json#/$defs/Nonempty"}},
                    }
                },
            },
            "shared/definitions/text.json": {
                "$schema": DRAFT_2020_12,
                "$defs": {"Nonempty": {"type": "string", "minLength": 1}},
            },
        }
        write_schemas(root, documents)
        snapshot = TemplateContractLoader(root).load_context_schema(Path("pkg/context.schema.json"))
        exposed = thaw_json(snapshot)
        assert oracle(root, documents, "pkg/context.schema.json").is_valid(context) is accepted
        assert Draft202012Validator(exposed).is_valid(context) is accepted
        validator = ConfigValidator()
        original = json.dumps(context)
        if accepted:
            assert thaw_json(validator.validate_template_context(snapshot, context)) == context
            assert json.dumps(context) == original
        else:
            with pytest.raises(ValidationError):
                validator.validate_template_context(snapshot, context)

    @pytest.mark.parametrize(
        ("assertions", "instances"),
        [
            (
                {
                    "$defs": {"Name": {"type": "string", "minLength": 5, "description": "Base"}},
                    "$ref": "#/$defs/Name",
                    "minLength": 2,
                    "description": "Sibling",
                },
                [("ab", False), ("abcde", True)],
            ),
            (
                {
                    "$defs": {"Base": {"properties": {"a": {"type": "integer"}}}},
                    "$ref": "#/$defs/Base",
                    "type": "object",
                    "allOf": [{"properties": {"b": {"type": "string"}}}],
                    "unevaluatedProperties": False,
                },
                [({"a": 1, "b": "x"}, True), ({"a": 1, "c": 2}, False)],
            ),
            (
                {
                    "$defs": {"Base": {"properties": {"a": True}, "unevaluatedProperties": False}},
                    "$ref": "#/$defs/Base",
                    "properties": {"b": True},
                },
                [({"a": 1}, True), ({"a": 1, "b": 2}, False)],
            ),
            (
                {
                    "$defs": {"First": {"prefixItems": [{"type": "integer"}]}},
                    "$ref": "#/$defs/First",
                    "type": "array",
                    "allOf": [{"contains": {"const": "tail"}}],
                    "unevaluatedItems": False,
                },
                [([1, "tail"], True), ([1, "extra", "tail"], False)],
            ),
            (
                {
                    "type": "object",
                    "if": {"required": ["a"]},
                    "then": {"required": ["b"]},
                    "else": {"not": {"required": ["b"]}},
                    "dependentSchemas": {"b": {"properties": {"b": {"type": "integer"}}}},
                },
                [({}, True), ({"a": 0, "b": 2}, True), ({"a": 0}, False), ({"b": 2}, False)],
            ),
        ],
    )
    def test_combinations_and_unevaluated_member_parity(
        self,
        suite_roots: SuiteRoots,
        assertions: dict[str, JsonValue],
        instances: list[tuple[JsonValue, bool]],
    ) -> None:
        """Reference removal preserves both adjacent and referenced evaluation scopes."""
        root = suite_roots.templates
        documents = {"pkg/context.schema.json": {"$schema": DRAFT_2020_12, **assertions}}
        write_schemas(root, documents)
        snapshot = TemplateContractLoader(root).load_context_schema(Path("pkg/context.schema.json"))
        authored = oracle(root, documents, "pkg/context.schema.json")
        exposed = Draft202012Validator(thaw_json(snapshot))
        for instance, accepted in instances:
            assert authored.is_valid(instance) is accepted
            assert exposed.is_valid(instance) is accepted

    def test_local_documents_and_literal_data_use_schema_positions(
        self, suite_roots: SuiteRoots
    ) -> None:
        """Relative document bases, escaped pointers and schema-looking data stay distinct."""
        root = suite_roots.templates
        literal: JsonValue = {"$ref": "#not-a-reference", "$id": "literal", "$schema": "data"}
        documents: dict[str, dict[str, JsonValue]] = {
            "pkg/context.schema.json": {
                "$schema": DRAFT_2020_12,
                "$ref": "nested/object.json",
                "examples": [literal],
                "default": literal,
                "x-extension": literal,
            },
            "pkg/nested/object.json": {
                "$schema": DRAFT_2020_12,
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "$ref": {"const": literal},
                    "name": {"$ref": "../names.json#/$defs/a~1b/$defs/~0Name"},
                },
            },
            "pkg/names.json": {
                "$schema": DRAFT_2020_12,
                "$defs": {"a/b": {"$defs": {"~Name": {"type": "string", "minLength": 1}}}},
            },
        }
        write_schemas(root, documents)
        snapshot = TemplateContractLoader(root).load_context_schema(Path("pkg/context.schema.json"))
        exposed = thaw_json(snapshot)
        assert isinstance(exposed, dict)
        assert exposed["default"] == literal
        assert exposed["examples"] == [literal]
        for context in [{"$ref": literal, "name": "yes"}, {"name": ""}, {"unknown": 1}]:
            assert oracle(root, documents, "pkg/context.schema.json").is_valid(context) == (
                Draft202012Validator(exposed).is_valid(context)
            )

    @pytest.mark.parametrize(
        "reference",
        [
            "#/$defs/Missing",
            "#named",
            "#/$defs/bad~2key",
            "missing.json",
            "https://example.invalid/schema.json",
            "file:///schema.json",
            "//host/schema",
            "/absolute.json",
            "C:/absolute.json",
            r"C:\absolute.json",
            "../../outside.json",
            "../other/context.schema.json",
            "../shared/templates/schema.json",
            "../shared/definitions/escape.json",
            "../other/../other/context.schema.json",
            "%2Fabsolute.json",
            "..%2F..%2Foutside.json",
            "context.schema.json?query=1",
        ],
    )
    def test_missing_external_and_wrong_direction_references_fail(
        self, suite_roots: SuiteRoots, reference: str
    ) -> None:
        root = suite_roots.templates
        documents: dict[str, dict[str, JsonValue]] = {
            "pkg/context.schema.json": {"$schema": DRAFT_2020_12, "$ref": reference},
            "other/context.schema.json": {"$schema": DRAFT_2020_12},
            "shared/templates/schema.json": {"$schema": DRAFT_2020_12},
            "shared/definitions/escape.json": {
                "$schema": DRAFT_2020_12,
                "$ref": "../../pkg/context.schema.json",
            },
        }
        write_schemas(root, documents)
        with pytest.raises((ValueError, OSError)):
            TemplateContractLoader(root).load_context_schema(Path("pkg/context.schema.json"))

    @pytest.mark.parametrize(
        "unsupported",
        [
            {"$id": "identity"},
            {"$anchor": "name"},
            {"$dynamicRef": "#name"},
            {"$dynamicAnchor": "name"},
            {"$vocabulary": {}},
            {"properties": {"x": {"$schema": DRAFT_2020_12}}},
            {"$defs": {"Loop": {"$ref": "#/$defs/Loop"}}},
            {"$ref": "#"},
            {"$ref": "other.json"},
        ],
    )
    def test_unsupported_features_and_cycles_are_rejected(
        self, suite_roots: SuiteRoots, unsupported: dict[str, JsonValue]
    ) -> None:
        root = suite_roots.templates
        write_schemas(
            root,
            {
                "pkg/context.schema.json": {"$schema": DRAFT_2020_12, **unsupported},
                "pkg/other.json": {"$schema": DRAFT_2020_12, "$ref": "context.schema.json"},
            },
        )
        with pytest.raises(ValueError):
            TemplateContractLoader(root).load_context_schema(Path("pkg/context.schema.json"))

    @pytest.mark.parametrize(
        "document",
        [
            {},
            {"$schema": "http://json-schema.org/draft-07/schema#"},
            {"$schema": DRAFT_2020_12, "type": 1},
            {"$schema": DRAFT_2020_12, "allOf": []},
        ],
    )
    def test_dialect_and_standard_schema_shape_are_checked(
        self, suite_roots: SuiteRoots, document: dict[str, JsonValue]
    ) -> None:
        write_schemas(suite_roots.templates, {"pkg/context.schema.json": document})
        with pytest.raises((ValueError, SchemaError)):
            TemplateContractLoader(suite_roots.templates).load_context_schema(
                Path("pkg/context.schema.json")
            )

    def test_symlink_escape_rejected_before_read(self, suite_roots: SuiteRoots) -> None:
        """An existing target outside the suite cannot be admitted through a directory link."""
        root = suite_roots.templates
        write_schemas(
            root,
            {
                "pkg/context.schema.json": {
                    "$schema": DRAFT_2020_12,
                    "$ref": "linked/hidden.json",
                }
            },
        )
        write_package_tree(suite_roots.temp, {"hidden.json": b"not JSON"})
        link = root / "pkg" / "linked"
        if os.name == "nt":
            subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(link), str(suite_roots.temp)],
                check=True,
                capture_output=True,
            )
        else:
            link.symlink_to(suite_roots.temp, target_is_directory=True)
        with pytest.raises(ValueError, match="schema_outside_suite"):
            TemplateContractLoader(root).load_context_schema(Path("pkg/context.schema.json"))

    def test_explicit_config_entry_returns_snapshot_under_hostile_cwd(
        self, suite_roots: SuiteRoots, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        root = suite_roots.templates
        path = root / "pkg" / "context.schema.json"
        document: dict[str, JsonValue] = {
            "$schema": DRAFT_2020_12,
            "type": "object",
            "additionalProperties": False,
            "properties": {"value": {"type": "integer"}},
        }
        write_schemas(root, {"pkg/context.schema.json": document})
        reader = TemplateContractLoader(root)
        loader = ConfigLoader(
            suite_roots.config, root, context_schema_reader=reader.load_context_schema
        )
        monkeypatch.chdir(suite_roots.temp)
        monkeypatch.setenv("PGMCP_WORKSPACE_ROOT", str(suite_roots.temp))
        snapshot = loader.load_template_context_schema(path)
        assert isinstance(snapshot, FrozenJsonObject)
        write_schemas(root, {"pkg/context.schema.json": {"$schema": DRAFT_2020_12, "not": {}}})
        exposed = thaw_json(snapshot)
        assert isinstance(exposed, dict)
        exposed.clear()
        assert thaw_json(ConfigValidator().validate_template_context(snapshot, {"value": 0})) == {
            "value": 0
        }
        with pytest.raises(ValidationError):
            ConfigValidator().validate_template_context(snapshot, {"unknown": 0})
        with pytest.raises(ConfigError, match="template_context_reader_required"):
            ConfigLoader(suite_roots.config, root).load_template_context_schema(path)

    @pytest.mark.parametrize("payload", [b'{"$schema": 1, "$schema": 2}', b'{"n": NaN}', b"[]"])
    def test_noncanonical_json_documents_fail(
        self, suite_roots: SuiteRoots, payload: bytes
    ) -> None:
        write_package_tree(suite_roots.templates, {"pkg/context.schema.json": payload})
        with pytest.raises(ValueError):
            TemplateContractLoader(suite_roots.templates).load_context_schema(
                Path("pkg/context.schema.json")
            )

    def test_contained_symlink_preserves_referring_document_uri(
        self, suite_roots: SuiteRoots
    ) -> None:
        """Containment canonicalization must not rebase a document's relative references."""
        root = suite_roots.templates
        documents: dict[str, dict[str, JsonValue]] = {
            "pkg/context.schema.json": {"$schema": DRAFT_2020_12, "$ref": "alias/object.json"},
            "pkg/deep/real/object.json": {"$schema": DRAFT_2020_12, "$ref": "../value.json"},
            "pkg/value.json": {"$schema": DRAFT_2020_12, "type": "string"},
            "pkg/deep/value.json": {"$schema": DRAFT_2020_12, "type": "integer"},
        }
        write_schemas(root, documents)
        link_directory(root / "pkg/alias", root / "pkg/deep/real")
        documents["pkg/alias/object.json"] = documents["pkg/deep/real/object.json"]
        snapshot = TemplateContractLoader(root).load_context_schema(Path("pkg/context.schema.json"))
        expected = oracle(root, documents, "pkg/context.schema.json")
        actual = Draft202012Validator(thaw_json(snapshot))
        assert expected.is_valid("text")
        assert actual.is_valid("text")
        assert not actual.is_valid(1)

    def test_alias_expanding_cycle_fails_before_path_growth(self, suite_roots: SuiteRoots) -> None:
        """Physical cycle identity stays bounded even when logical URIs keep changing."""
        root = suite_roots.templates
        write_schemas(
            root,
            {
                "pkg/context.schema.json": {
                    "$schema": DRAFT_2020_12,
                    "$ref": "alias/context.schema.json",
                }
            },
        )
        link_directory(root / "pkg/alias", root / "pkg")
        with pytest.raises(ValueError, match="cyclic_schema_reference"):
            TemplateContractLoader(root).load_context_schema(Path("pkg/context.schema.json"))


def link_directory(link: Path, target: Path) -> None:
    """Exercise real directory aliases on both Windows and POSIX."""
    if os.name == "nt":
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            check=True,
            capture_output=True,
        )
    else:
        link.symlink_to(target, target_is_directory=True)
