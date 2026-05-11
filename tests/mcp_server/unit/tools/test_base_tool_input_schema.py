import json
from typing import Any

from pydantic import BaseModel, Field

from mcp_server.core.operation_notes import NoteContext
from mcp_server.tools.base import BaseTool
from mcp_server.tools.tool_result import ToolResult


class SimpleNestedModel(BaseModel):
    """A simple nested model to test BaseTool schema normalization."""

    nested_id: int = Field(description="Nested identifier")
    nested_value: str = Field(description="Nested value")


class SimpleInputWithNested(BaseModel):
    """Input with nested model that exercises schema normalization."""

    name: str
    nested: SimpleNestedModel


class SimpleToolForTesting(BaseTool):
    """Minimal tool for schema testing."""

    def __init__(self) -> None:
        self.args_model = SimpleInputWithNested
        self.name = "test_tool"
        self.description = "Test tool"

    async def execute(self, params: Any, context: NoteContext) -> ToolResult:  # noqa: ANN401, ARG002
        return ToolResult.text("ok")


class TestBaseToolInputSchemaNormalization:
    """Test that BaseTool.input_schema always normalizes (no $defs/$ref)."""

    def test_base_tool_input_schema_no_defs(self) -> None:
        """Any BaseTool subclass with nested model must not expose $defs in input_schema."""
        tool = SimpleToolForTesting()
        schema = tool.input_schema

        # No $defs allowed
        assert "$defs" not in schema, "Schema must not contain $defs after BaseTool.input_schema"

        # No $ref allowed
        schema_str = json.dumps(schema)
        assert "$ref" not in schema_str, "Schema must not contain $ref after BaseTool.input_schema"

        # The nested structure must be inlined instead
        assert "nested" in schema["properties"]
        assert "nested_id" in schema["properties"]["nested"]["properties"], (
            "Nested properties must be inlined, not referenced"
        )

    def test_base_tool_input_schema_preserves_descriptions(self) -> None:
        """Descriptions preserved in normalized schema."""
        tool = SimpleToolForTesting()
        schema = tool.input_schema

        # Field descriptions must survive
        assert (
            schema["properties"]["nested"]["properties"]["nested_id"]["description"]
            == "Nested identifier"
        )
        assert (
            schema["properties"]["nested"]["properties"]["nested_value"]["description"]
            == "Nested value"
        )
