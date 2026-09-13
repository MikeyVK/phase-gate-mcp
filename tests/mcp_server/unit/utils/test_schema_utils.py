import json

import pytest
from jsonschema import Draft202012Validator

from mcp_server.utils.schema_utils import resolve_schema_refs


class TestResolveSchemaRefs:
    """Test schema normalization: $defs + $ref inlining."""

    def test_resolve_schema_refs_inlines_defs(self) -> None:
        """Schema with $defs + $ref → all refs inlined."""
        # Nested model generates:
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "items": {"$ref": "#/$defs/Item"}},
            "$defs": {
                "Item": {
                    "type": "object",
                    "properties": {"id": {"type": "integer"}, "value": {"type": "string"}},
                }
            },
        }

        result = resolve_schema_refs(schema)

        # Assert $defs is gone
        assert "$defs" not in result
        assert "$ref" not in json.dumps(result)  # no $ref anywhere

        # Assert Item structure is inlined
        assert "items" in result["properties"]
        # Should be the actual structure, not a $ref
        assert result["properties"]["items"]["type"] == "object"
        assert "id" in result["properties"]["items"]["properties"]

    def test_resolve_schema_refs_preserves_descriptions(self) -> None:
        """Field descriptions survive inlining."""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The user's full name"},
                "items": {"$ref": "#/$defs/Item"},
            },
            "$defs": {
                "Item": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "description": "Unique item identifier"}
                    },
                }
            },
        }

        result = resolve_schema_refs(schema)

        # Descriptions must survive
        assert result["properties"]["name"]["description"] == "The user's full name"
        assert (
            result["properties"]["items"]["properties"]["id"]["description"]
            == "Unique item identifier"
        )

    def test_resolve_schema_refs_noop_on_flat_schema(self) -> None:
        """Flat schema unchanged."""
        schema = {
            "type": "object",
            "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
        }

        result = resolve_schema_refs(schema)

        # Should be identical (or at least equivalent)
        assert result == schema
        assert "$defs" not in result
        assert "$ref" not in json.dumps(result)


    def test_referenced_and_adjacent_constraints_both_apply(self) -> None:
        """A sibling cannot weaken an assertion from the referenced schema."""
        schema = {
            "$defs": {"Name": {"type": "string", "minLength": 5}},
            "$ref": "#/$defs/Name",
            "minLength": 2,
            "description": "Caller-facing description",
        }
        resolved = resolve_schema_refs(schema)
        assert Draft202012Validator(schema).is_valid("ab") is False
        assert Draft202012Validator(resolved).is_valid("ab") is False
        assert Draft202012Validator(resolved).is_valid("abcde") is True
        assert resolved["description"] == "Caller-facing description"

    def test_literal_schema_looking_data_is_not_rewritten(self) -> None:
        """Only schema positions participate in reference resolution."""
        literal = {"$ref": "#/missing", "$dynamicRef": "#data"}
        schema = {"const": literal, "default": literal, "examples": [literal]}
        assert resolve_schema_refs(schema) == schema

    @pytest.mark.parametrize("reference", ["#/$defs/Missing", "#named"])
    def test_unresolvable_references_fail_closed(self, reference: str) -> None:
        """Missing and unsupported references never become unconstrained objects."""
        with pytest.raises(ValueError):
            resolve_schema_refs({"$ref": reference})

    def test_cyclic_reference_reports_admission_error(self) -> None:
        """Cycles cannot produce a finite, reference-free exposure."""
        schema = {"$defs": {"Loop": {"$ref": "#/$defs/Loop"}}, "$ref": "#/$defs/Loop"}
        with pytest.raises(ValueError):
            resolve_schema_refs(schema)

    def test_json_pointer_resolves_nested_escaped_definition_names(self) -> None:
        """JSON Pointer paths are not reduced to the final token."""
        schema = {
            "$defs": {"a/b": {"$defs": {"~Name": {"type": "string"}}}},
            "$ref": "#/$defs/a~1b/$defs/~0Name",
        }
        assert resolve_schema_refs(schema) == {"type": "string"}

    def test_false_reference_is_not_missing(self) -> None:
        """Boolean false subschemas retain rejection semantics."""
        schema = {"type": "object", "properties": {"forbidden": {"$ref": "#/$defs/Never"}},
                  "$defs": {"Never": False}}
        resolved = resolve_schema_refs(schema)
        assert Draft202012Validator(resolved).is_valid({})
        assert not Draft202012Validator(resolved).is_valid({"forbidden": None})
