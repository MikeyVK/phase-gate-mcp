# mcp_server/schemas/tool_outputs.py
# template=schema version=74378193 created=2026-06-12T20:49Z updated=2026-06-12T21:00Z
"""Base tool output schemas.

@layer: Schemas
"""

from pydantic import BaseModel, ConfigDict


class BaseToolOutput(BaseModel):
    """Base class for all structured tool outputs."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    success: bool = True
    error_message: str | None = None
    post_tool_instruction: str | None = None
