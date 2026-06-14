# tests\mcp_server\unit\server\test_tool_result_conversion.py
# template=unit_test version=3d15d309 created=2026-06-11T06:54Z updated=
"""
Unit tests for mcp_server.utils.mcp_converters.

Unit tests for ToolResult to MCP result conversion.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.utils.mcp_converters]
@responsibilities:
    - Test TestToolResultConversion functionality
    - Verify None
    - None
"""

# Standard library

# Third-party
from mcp.types import CallToolResult, TextContent

from mcp_server.tools.tool_result import ToolResult

# Project modules
from mcp_server.utils.mcp_converters import convert_tool_result_to_mcp_result


class TestToolResultConversion:
    """Test suite for mcp_converters."""

    def test_convert_tool_result_text_only(self) -> None:
        """Should convert text-only ToolResult to CallToolResult normally."""
        result = ToolResult.text("Hello World")
        mcp_result = convert_tool_result_to_mcp_result(result)

        assert isinstance(mcp_result, CallToolResult)
        assert not mcp_result.isError
        assert len(mcp_result.content) == 1
        assert isinstance(mcp_result.content[0], TextContent)
        assert mcp_result.content[0].text == "Hello World"
        assert getattr(mcp_result, "structuredContent", None) is None
