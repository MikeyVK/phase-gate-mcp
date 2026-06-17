# mcp_server/schemas/error_outputs.py
# template=schema version=74378193 created=2026-06-17T20:16Z updated=
"""ToolErrorOutput and subclass schemas for structured error outputs.

@layer: Schemas
"""

# Standard library
from typing import Any

# Third-party
from pydantic import BaseModel, ConfigDict, Field


class ToolErrorOutput(BaseModel):
    """Base class for all structured tool error outputs."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    success: bool = False
    error_type: str
    message: str
    traceback: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)


class ValidationErrorOutput(ToolErrorOutput):
    """Error output for Pydantic input validation failures."""

    error_type: str = "ValidationError"
    validation_errors: list[dict[str, Any]] | str
    input_schema: dict[str, Any] = Field(default_factory=dict)


class ExecutionErrorOutput(ToolErrorOutput):
    """Error output for unhandled tool execution exceptions."""

    error_type: str = "ExecutionError"


class CacheErrorOutput(ToolErrorOutput):
    """Error output for cache publishing failures."""

    error_type: str = "CacheError"


class EnforcementErrorOutput(ToolErrorOutput):
    """Error output for phase enforcement gate check failures."""

    error_type: str = "EnforcementError"
    error_code: str
