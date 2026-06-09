"""
Integration test: End-to-end validation failure response via handle_call_tool.
Scope: Cycle 2, Change A — ensures early-return guard works correctly.
"""

import json
from typing import Any

import pytest
import pytest_asyncio
from mcp.types import EmbeddedResource
from pydantic import BaseModel, ConfigDict

from mcp_server.server import MCPServer
from tests.mcp_server.test_support import make_test_server
from mcp_server.tools.base import BaseTool
from mcp_server.tools.tool_result import ToolResult


class IntegrationInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: str


class MockIntegrationTool(BaseTool):
    """Mock tool for integration testing."""

    name = "MockIntegrationTool"
    args_model = IntegrationInput

    async def execute(  # noqa: ANN201
        self,
        params: IntegrationInput,
        context: Any,  # noqa: ANN401, ARG002
    ):
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

    @pytest_asyncio.fixture
    async def server(self) -> MCPServer:
        """MCPServer with MockIntegrationTool registered."""
        s = make_test_server()
        s.tools.append(MockIntegrationTool())
        return s

    @pytest.mark.asyncio
    async def test_extra_field_returns_call_tool_result_error(  # noqa: ANN201
        self, server: MCPServer
    ):
        """
        Integration test: end-to-end validation failure path.
        When an extra unknown field is supplied, _validate_tool_arguments returns a
        ToolResult and _convert_tool_result_to_mcp_result wraps it in a
        CallToolResult with isError=True.

        Before fix: validation errors bypassed the ToolResult path.
        After fix: proper CallToolResult(isError=True) returned.
        """
        tool = next(t for t in server.tools if t.name == "MockIntegrationTool")
        extra_field_args = {"action": "test", "unknown_field": "typo"}

        validated = server._validate_tool_arguments(  # pyright: ignore[reportPrivateUsage]
            tool, extra_field_args, "test-call-id", "MockIntegrationTool"
        )

        assert isinstance(validated, ToolResult), "Validation failure must return ToolResult"
        assert validated.is_error is True

        result = server._convert_tool_result_to_mcp_result(validated)  # pyright: ignore[reportPrivateUsage]
        assert hasattr(result, "isError"), "Converted result must have isError"
        assert result.isError is True

    @pytest.mark.asyncio
    async def test_schema_resource_in_error_response(  # noqa: ANN201
        self, server: MCPServer
    ):
        """
        Integration test: error response includes schema://validation resource
        so the agent can learn the valid input structure.
        """
        tool = next(t for t in server.tools if t.name == "MockIntegrationTool")
        extra_field_args = {"action": "test", "unknown_field": "typo"}

        validated = server._validate_tool_arguments(  # pyright: ignore[reportPrivateUsage]
            tool, extra_field_args, "test-call-id", "MockIntegrationTool"
        )
        assert isinstance(validated, ToolResult)

        result = server._convert_tool_result_to_mcp_result(validated)  # pyright: ignore[reportPrivateUsage]
        assert result.isError is True

        # content on CallToolResult contains MCP TextContent / EmbeddedResource objects
        content = result.content
        assert isinstance(content, list), "content must be a list"

        # Look for embedded resource item (schema://validation)
        resource_items = [c for c in content if isinstance(c, EmbeddedResource)]
        assert len(resource_items) > 0, "Expected schema://validation EmbeddedResource"

        resource = resource_items[0].resource
        assert str(resource.uri) == "schema://validation"
        assert resource.mimeType == "application/json"

        schema = json.loads(resource.text)
        assert "properties" in schema
        assert "action" in schema["properties"]
