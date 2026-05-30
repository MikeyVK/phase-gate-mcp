"""Tests for Validation tools.

@layer: Tests (Unit)
@dependencies: [pytest, unittest.mock, mcp_server.tools.validation_tools]
"""

from unittest.mock import patch

import pytest

import mcp_server.tools.validation_tools as validation_module
from mcp_server.core.operation_notes import NoteContext
from mcp_server.tools.validation_tools import (
    ValidateDTOInput,
    ValidateDTOTool,
)


def test_validation_tool_class_removed() -> None:
    """Invariant: ValidationTool stub must be absent.

    The stub unconditionally returned success without performing any validation.
    """
    assert not hasattr(validation_module, "ValidationTool"), "ValidationTool stub must be removed"


@pytest.mark.asyncio
async def test_dto_validation_tool() -> None:
    """Test ValidateDTOTool returns pass status for DTO validation."""
    tool = ValidateDTOTool()

    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("pathlib.Path.read_text", return_value="@dataclass\nclass TestDTO: ..."),
    ):
        result = await tool.execute(
            ValidateDTOInput(file_path="backend/dtos/test.py"), NoteContext()
        )

    assert result.is_error is False
    assert "DTO validation passed" in result.content[0]["text"]


@pytest.mark.asyncio
async def test_dto_validation_tool_missing_file() -> None:
    """Test ValidateDTOTool returns ToolResult.error for missing files."""
    tool = ValidateDTOTool()

    with patch("pathlib.Path.exists", return_value=False):
        result = await tool.execute(
            ValidateDTOInput(file_path="this/file/does/not/exist.py"), NoteContext()
        )

    assert result.is_error is True
    assert "DTO file not found" in result.content[0]["text"]
