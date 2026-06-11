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
from typing import Any

# Third-party
import pytest
from pathlib import Path

# Project modules
from mcp_server.utils.mcp_converters import convert_tool_result_to_mcp_result
from mcp_server.tools.tool_result import ToolResult
from mcp.types import CallToolResult, TextContent


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

    def test_convert_tool_result_json_populates_structured_content(self) -> None:
        """Should extract type='json' block and populate structuredContent."""
        test_data = {"key": "value", "list": [1, 2, 3]}
        result = ToolResult.json_data(test_data, text="Summary text")
        mcp_result = convert_tool_result_to_mcp_result(result)
        
        assert isinstance(mcp_result, CallToolResult)
        assert not mcp_result.isError
        # The JSON content block must be popped, leaving only the TextContent block
        assert len(mcp_result.content) == 1
        assert isinstance(mcp_result.content[0], TextContent)
        assert mcp_result.content[0].text == "Summary text"
        
        # The structuredContent field must contain the original dict data
        assert getattr(mcp_result, "structuredContent", None) == test_data

    def test_convert_tool_result_multiple_json_blocks_fails(self) -> None:
        """Should raise ValueError if multiple JSON blocks are present."""
        result = ToolResult(
            content=[
                {"type": "json", "json": {"a": 1}},
                {"type": "json", "json": {"b": 2}},
            ],
            is_error=False
        )
        with pytest.raises(ValueError, match="Multiple JSON content blocks"):
            convert_tool_result_to_mcp_result(result)
