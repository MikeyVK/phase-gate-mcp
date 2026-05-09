import json
import pytest
from mcp_server.utils.schema_utils import resolve_schema_refs


class TestResolveSchemaRefs:
    """Test schema normalization: $defs + $ref inlining."""

    def test_resolve_schema_refs_inlines_defs(self):
        """Schema with $defs + $ref → all refs inlined."""
        # Nested model generates:
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "items": {
                    "$ref": "#/$defs/Item"
                }
            },
            "$defs": {
                "Item": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "value": {"type": "string"}
                    }
                }
            }
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

    def test_resolve_schema_refs_preserves_descriptions(self):
        """Field descriptions survive inlining."""
        schema = {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The user's full name"
                },
                "items": {
                    "$ref": "#/$defs/Item"
                }
            },
            "$defs": {
                "Item": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "description": "Unique item identifier"
                        }
                    }
                }
            }
        }

        result = resolve_schema_refs(schema)

        # Descriptions must survive
        assert result["properties"]["name"]["description"] == "The user's full name"
        assert result["properties"]["items"]["properties"]["id"]["description"] == "Unique item identifier"

    def test_resolve_schema_refs_noop_on_flat_schema(self):
        """Flat schema unchanged."""
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"}
            }
        }

        result = resolve_schema_refs(schema)

        # Should be identical (or at least equivalent)
        assert result == schema
        assert "$defs" not in result
        assert "$ref" not in json.dumps(result)
