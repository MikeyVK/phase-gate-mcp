# artifact: type=unit_test, version=1.0, created=2026-06-02T00:00:00Z
"""Unit tests for ScaffoldSchemaTool (C2).

@layer: Tests (Unit)
@dependencies: [pytest, unittest.mock, mcp_server.tools.scaffold_schema_tool]
"""

from unittest.mock import MagicMock

import pytest

from mcp_server.core.operation_notes import NoteContext
from mcp_server.tools.scaffold_schema_tool import (
    ScaffoldSchemaInput,
    ScaffoldSchemaTool,
)
from tests.mcp_server.test_support import assert_structured_result


class TestScaffoldSchemaTool:
    """Tests for ScaffoldSchemaTool — C2.D1 + C2.D3."""

    @pytest.fixture
    def mock_manager(self) -> MagicMock:
        """Mock ArtifactManager with get_context_schema and registry."""
        manager = MagicMock()
        manager.get_context_schema.return_value = {
            "type": "object",
            "properties": {"title": {"type": "string"}, "problem": {"type": "string"}},
            "required": ["title"],
        }
        manager.registry.list_type_ids.return_value = [
            "architecture",
            "commit",
            "design",
            "dto",
            "generic",
            "generic_doc",
            "integration_test",
            "issue",
            "planning",
            "pr",
            "reference",
            "research",
            "schema",
            "service",
            "tool",
            "unit_test",
            "worker",
        ]
        return manager

    @pytest.fixture
    def tool(self, mock_manager: MagicMock) -> ScaffoldSchemaTool:
        """Create tool with mocked manager."""
        return ScaffoldSchemaTool(manager=mock_manager)

    def test_tool_has_correct_metadata(self, tool: ScaffoldSchemaTool) -> None:
        """Tool should have name='scaffold_schema' and description mentioning schema."""
        assert tool.name == "scaffold_schema"
        assert "schema" in tool.description.lower()

    def test_input_schema_has_artifact_type_enum(
        self, tool: ScaffoldSchemaTool, mock_manager: MagicMock
    ) -> None:
        """input_schema property must populate artifact_type.enum from registry."""
        schema = tool.input_schema
        assert "properties" in schema
        assert "artifact_type" in schema["properties"]
        artifact_type_schema = schema["properties"]["artifact_type"]
        assert "enum" in artifact_type_schema, "artifact_type must have enum populated"
        enum_values = artifact_type_schema["enum"]
        assert isinstance(enum_values, list)
        assert "research" in enum_values
        assert "dto" in enum_values
        mock_manager.registry.list_type_ids.assert_called()

    @pytest.mark.asyncio
    async def test_returns_schema_for_v2_type(
        self, tool: ScaffoldSchemaTool, mock_manager: MagicMock
    ) -> None:
        """execute() delegates to manager.get_context_schema and returns JSON result."""
        params = ScaffoldSchemaInput(artifact_type="research")
        result = await tool.execute(params, NoteContext())

        mock_manager.get_context_schema.assert_called_once_with("research")

        assert_structured_result(
            result,
            {
                "type": "object",
                "properties": {"title": {"type": "string"}, "problem": {"type": "string"}},
                "required": ["title"],
            },
        )

    @pytest.mark.asyncio
    async def test_returns_schema_for_generic_doc(
        self, tool: ScaffoldSchemaTool, mock_manager: MagicMock
    ) -> None:
        """execute() returns a schema ToolResult for generic_doc once V2 support exists."""
        expected_schema = {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "purpose": {"type": "string"},
                "summary": {"type": "string"},
            },
            "required": ["title", "purpose", "summary"],
        }
        mock_manager.get_context_schema.return_value = expected_schema
        params = ScaffoldSchemaInput(artifact_type="generic_doc")
        result = await tool.execute(params, NoteContext())

        assert_structured_result(result, expected_schema)
