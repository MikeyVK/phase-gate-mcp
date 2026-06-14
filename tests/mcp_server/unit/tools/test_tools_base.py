"""Tests for tool result helpers.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.tools.tool_result]
"""

from mcp_server.tools.tool_result import ToolResult


def test_tool_result_helpers() -> None:
    """Test ToolResult.text and ToolResult.error helper methods."""
    # Test text helper
    result = ToolResult.text("Hello")
    assert result.content[0]["text"] == "Hello"
    assert not result.is_error

    # Test error helper
    error = ToolResult.error("Failed")
    assert error.content[0]["text"] == "Failed"
    assert error.is_error
