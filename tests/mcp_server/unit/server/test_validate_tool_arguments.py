"""
Unit tests for _validate_tool_arguments failure path and schema://validation resource.
Scope: Cycle 2, Change A — argument validation returns ToolResult on failure.
"""

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from mcp_server.core.operation_notes import NoteContext
from mcp_server.server import MCPServer
from mcp_server.tools.base import BaseTool
from mcp_server.tools.tool_result import ToolResult

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _patch_server_settings(mock: MagicMock, workspace_root: str | None = None) -> None:
    resolved = workspace_root or str(Path(__file__).resolve().parents[4])
    resolved_cfg = str(Path(resolved) / ".phase-gate")
    mock.from_env.return_value.server.name = "test-server"
    mock.from_env.return_value.server.workspace_root = resolved
    mock.from_env.return_value.server.config_root = resolved_cfg
    mock.from_env.return_value.server.state_dir = ".phase-gate"
    mock.from_env.return_value.github.token = None
    mock.from_env.return_value.github.owner = "test"
    mock.from_env.return_value.github.repo = "test-repo"
    mock.from_env.return_value.logging.level = "WARNING"
    mock.from_env.return_value.logging.audit_log = False


# ---------------------------------------------------------------------------
# Mock tool
# ---------------------------------------------------------------------------


class SimpleInput(BaseModel):
    required_field: str
    optional_field: int = 42


class MockSimpleTool(BaseTool):
    """Minimal mock tool for argument validation tests."""

    name = "mock_simple"
    args_model = SimpleInput

    async def execute(self, params: Any, context: NoteContext) -> ToolResult:  # noqa: ANN401, ARG002
        return ToolResult(content=[{"type": "text", "text": "OK"}])

    @property
    def input_schema(self) -> dict[str, Any]:
        """Return normalized schema (from Cycle 1, no $defs/$ref)."""
        return {
            "type": "object",
            "properties": {
                "required_field": {"type": "string", "description": "A required string field."},
                "optional_field": {"type": "integer", "description": "An optional integer."},
            },
            "required": ["required_field"],
        }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestValidateToolArgumentsFailurePath:
    """Test suite for _validate_tool_arguments return type and schema resource."""

    @pytest.fixture
    def server(self) -> MCPServer:
        """Minimal MCPServer instance for testing _validate_tool_arguments."""
        with patch("mcp_server.server.Settings") as mock_settings_cls:
            _patch_server_settings(mock_settings_cls)
            return MCPServer()

    def test_returns_tool_result_on_validation_error(self, server: MCPServer) -> None:
        """
        RED condition: When Pydantic validation fails (missing required field),
        _validate_tool_arguments returns a ToolResult with is_error=True.

        Before fix: would return list[TextContent], bypassing MCP pipeline.
        After fix: returns ToolResult with proper error shape.
        """
        tool = MockSimpleTool()
        invalid_args = {"optional_field": 99}

        result = server._validate_tool_arguments(  # pyright: ignore[reportPrivateUsage]
            tool, invalid_args, call_id="test-call", name="mock_simple"
        )

        assert isinstance(result, ToolResult), (
            f"Expected ToolResult on validation error, got {type(result).__name__}"
        )
        assert result.is_error is True, "is_error must be True for validation failure"

    def test_failure_includes_schema_resource(self, server: MCPServer) -> None:
        """
        RED condition: The failure response must include a schema://validation
        EmbeddedResource with the valid input schema in JSON.
        """
        tool = MockSimpleTool()
        invalid_args = {"unknown_field": "typo"}

        result = server._validate_tool_arguments(  # pyright: ignore[reportPrivateUsage]
            tool, invalid_args, call_id="test-call", name="mock_simple"
        )

        assert isinstance(result, ToolResult)

        resource_items = [
            c for c in result.content if isinstance(c, dict) and c.get("type") == "resource"
        ]
        assert len(resource_items) > 0, "Expected schema://validation resource in failure response"

        resource = resource_items[0]["resource"]
        assert resource["uri"] == "schema://validation", (
            f"Expected uri=schema://validation, got {resource['uri']}"
        )
        assert resource["mimeType"] == "application/json", (
            f"Expected application/json, got {resource['mimeType']}"
        )

        schema = json.loads(resource["text"])
        assert isinstance(schema, dict), "schema must be a dict"
        assert "properties" in schema, "schema must have properties"
        assert "required_field" in schema["properties"], "required_field must be in properties"
        assert "description" in schema["properties"]["required_field"], (
            "Field description must be preserved in schema"
        )

    def test_failure_includes_diagnostic_text(self, server: MCPServer) -> None:
        """
        RED condition: The response includes human-readable diagnostic text
        explaining what validation failed.
        """
        tool = MockSimpleTool()
        invalid_args = {"optional_field": "not-an-integer"}

        result = server._validate_tool_arguments(  # pyright: ignore[reportPrivateUsage]
            tool, invalid_args, call_id="test-call", name="mock_simple"
        )

        assert isinstance(result, ToolResult)

        text_items = [c for c in result.content if isinstance(c, dict) and c.get("type") == "text"]
        assert len(text_items) > 0, "Expected diagnostic text in failure response"

        text_content = text_items[0]["text"]
        assert "Invalid input" in text_content, (
            f"Diagnostic text must mention 'Invalid input', got: {text_content}"
        )
        assert "mock_simple" in text_content, (
            f"Diagnostic text must mention tool name, got: {text_content}"
        )

    def test_success_returns_model_instance(self, server: MCPServer) -> None:
        """
        Happy path: When validation succeeds, _validate_tool_arguments
        returns a BaseModel instance, not a ToolResult.
        """
        tool = MockSimpleTool()
        valid_args = {"required_field": "hello"}

        result = server._validate_tool_arguments(  # pyright: ignore[reportPrivateUsage]
            tool, valid_args, call_id="test-call", name="mock_simple"
        )

        assert isinstance(result, SimpleInput), (
            f"Expected SimpleInput model instance on success, got {type(result).__name__}"
        )
        assert result.required_field == "hello"
        assert result.optional_field == 42

    def test_schema_is_normalized_no_defs_no_ref(self, server: MCPServer) -> None:
        """
        RED condition: The schema://validation resource must not contain
        $defs or $ref (Cycle 1 guarantee: all schemas are normalized).
        """
        tool = MockSimpleTool()
        invalid_args = {}

        result = server._validate_tool_arguments(  # pyright: ignore[reportPrivateUsage]
            tool, invalid_args, call_id="test-call", name="mock_simple"
        )

        assert isinstance(result, ToolResult)
        resource_items = [
            c for c in result.content if isinstance(c, dict) and c.get("type") == "resource"
        ]
        schema = json.loads(resource_items[0]["resource"]["text"])

        assert "$defs" not in schema, "Schema must not contain $defs (Cycle 1 guarantee)"
        assert "$ref" not in json.dumps(schema), "Schema must not contain $ref anywhere"
