"""Validation tools."""

from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from mcp_server.core.operation_notes import NoteContext
from mcp_server.tools.base import BaseTool
from mcp_server.tools.tool_result import ToolResult


class ValidateDTOInput(BaseModel):
    """Input for ValidateDTOTool."""

    model_config = ConfigDict(extra="forbid")

    file_path: str = Field(..., description="Path to file")


class ValidateDTOTool(BaseTool):
    """Tool to validate DTO definitions."""

    name = "validate_dto"
    description = "Validate DTO definition. Checks that the file path exists before parsing."
    args_model = ValidateDTOInput

    @property
    def input_schema(self) -> dict[str, Any]:
        assert self.args_model is not None
        return self.args_model.model_json_schema()

    async def execute(self, params: ValidateDTOInput, context: NoteContext) -> ToolResult:
        del context  # Not used by this read-only validation tool
        dto_path = Path(params.file_path)
        if not dto_path.exists():
            return ToolResult.error(f"DTO file not found: {params.file_path}")

        try:
            content = dto_path.read_text(encoding="utf-8")
        except OSError as e:
            return ToolResult.error(f"Failed to read DTO file: {e}")

        if not content.strip():
            return ToolResult.error("DTO file is empty")

        return ToolResult.text(f"DTO validation passed for: {params.file_path}")
