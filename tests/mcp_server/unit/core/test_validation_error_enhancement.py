# artifact: type=unit_test, version=1.0, created=2026-01-21T22:04:10Z
"""
Unit tests for ValidationError schema handling — C1.D4.

Tests ValidationError.to_resource_dict() for structured JSON responses.
Schema is now a JSON Schema dict (from get_context_schema / model_json_schema).
@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.core.exceptions]
@responsibilities:
    - Test to_resource_dict() returns proper structure with JSON Schema dict
    - Test validation info (missing/provided) included
    - Test resource dict format matches ToolResult contract
    - Test None schema handled gracefully
"""

# Standard library
from typing import Any

# Third-party
import pytest

# Project modules
from mcp_server.core.exceptions import ValidationError


@pytest.fixture(name="sample_schema")
def fixture_sample_schema() -> dict[str, Any]:
    """Provides sample JSON Schema dict for testing (replaces TemplateSchema)."""
    return {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Name field"},
            "description": {"type": "string", "description": "Description field"},
            "frozen": {"type": "boolean", "description": "Optional frozen flag"},
        },
        "required": ["name", "description"],
    }


class TestValidationErrorEnhancement:
    """Tests for ValidationError to_resource_dict() with JSON Schema dict."""

    def test_to_resource_dict_includes_schema(self, sample_schema: dict[str, Any]) -> None:
        """to_resource_dict() returns dict with artifact_type and JSON Schema dict."""
        # Arrange
        error = ValidationError(message="Missing required fields", schema=sample_schema)

        # Act
        result = error.to_resource_dict("dto")

        # Assert
        assert result["artifact_type"] == "dto"
        assert "schema" in result
        schema = result["schema"]
        assert isinstance(schema, dict)
        assert schema.get("type") == "object"
        assert "properties" in schema
        assert "required" in schema
        assert "name" in schema["required"]
        assert "description" in schema["required"]

    def test_to_resource_dict_includes_validation(self, sample_schema: dict[str, Any]) -> None:
        """to_resource_dict() includes validation details (missing/provided)."""
        # Arrange
        error = ValidationError(message="Missing required fields", schema=sample_schema)
        error.missing = ["description"]
        error.provided = ["name"]

        # Act
        result = error.to_resource_dict("dto")

        # Assert
        assert "validation" in result
        assert result["validation"]["missing"] == ["description"]
        assert result["validation"]["provided"] == ["name"]

    def test_to_resource_dict_handles_none_schema(self) -> None:
        """to_resource_dict() handles None schema gracefully."""
        # Arrange
        error = ValidationError(message="Validation failed", schema=None)

        # Act
        result = error.to_resource_dict("dto")

        # Assert
        assert result["artifact_type"] == "dto"
        assert "schema" not in result
