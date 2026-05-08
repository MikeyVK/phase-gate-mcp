"""
Integration test: End-to-end validation failure response via handle_call_tool.
Scope: Cycle 2, Change A — ensures early-return guard works correctly.
"""
import json
from typing import Any

import pytest

from mcp_server.tools.tool_result import ToolResult
from mcp_server.server import MCPServer
from mcp_server.tools.base import BaseTool
from pydantic import BaseModel


class IntegrationInput(BaseModel):
    action: str


class MockIntegrationTool(BaseTool):
    """Mock tool for integration testing."""

    name = "MockIntegrationTool"
    args_model = IntegrationInput

    async def execute(self, params: IntegrationInput, context):
        return ToolResult(content=[{"type": "text", "text": f"Action: {params.action}"}])

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "The action to perform."},
            },
            "required": ["action"],
        }


class TestStrictInputValidationResponse:
    """Integration test: validation failure flows through MCP response pipeline."""

    @pytest.fixture
    async def server(self) -> MCPServer:
        """MCPServer with MockIntegrationTool."""
        return MCPServer(tools=[MockIntegrationTool()])

    @pytest.mark.asyncio
    async def test_extra_field_returns_call_tool_result_error(self, server: MCPServer):
        """
        RED condition: End-to-end test. When an extra unknown field is supplied,
        handle_call_tool returns CallToolResult with isError=True and schema resource.

        Before fix: would return raw list[TextContent] that was not a CallToolResult.
        After fix: proper CallToolResult(isError=True) + structured content.
        """
        # Call with an extra field that will fail strict validation (Cycle 1 adds extra="forbid")
        extra_field_args = {"action": "test", "unknown_field": "typo"}

        result = await server.handle_call_tool("MockIntegrationTool", extra_field_args)

        # Result is a CallToolResult from MCP (converted from ToolResult)
        assert hasattr(result, "isError"), "Result must have isError attribute (MCP CallToolResult shape)"
        assert result.isError is True, "isError must be True on validation failure"

    @pytest.mark.asyncio
    async def test_schema_resource_in_error_response(self, server: MCPServer):
        """
        RED condition: The error response includes a schema://validation resource
        so the agent can learn the valid input structure.
        """
        extra_field_args = {"action": "test", "unknown_field": "typo"}
        result = await server.handle_call_tool("MockIntegrationTool", extra_field_args)

        assert result.isError is True

        # Check content includes schema resource
        content = result.content
        assert isinstance(content, list), "content must be a list"

        # Look for resource item
        resource_items = [c for c in content if isinstance(c, dict) and c.get("type") == "resource"]
        assert len(resource_items) > 0, "Expected schema://validation resource in error response"

        resource = resource_items[0]["resource"]
        assert resource["uri"] == "schema://validation"
        assert resource["mimeType"] == "application/json"

        # Validate schema JSON
        schema = json.loads(resource["text"])
        assert "properties" in schema
        assert "action" in schema["properties"]
