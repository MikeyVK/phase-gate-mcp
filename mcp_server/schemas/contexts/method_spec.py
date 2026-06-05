# mcp_server/schemas/contexts/method_spec.py
"""MethodSpec value object.

Structured method definition for code artifact scaffolding.

@layer: MCP Server (Schema Infrastructure)
"""

# Third-party
from pydantic import BaseModel, ConfigDict, Field, field_validator


class MethodSpec(BaseModel):
    """Immutable method definition used by code artifact context schemas."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str = Field(
        description="Method name",
    )
    params: str = Field(
        default="",
        description="Comma-separated method parameters excluding self",
    )
    return_type: str = Field(
        default="",
        description="Return type annotation",
    )
    docstring: str = Field(
        default="",
        description="Method docstring content",
    )
    body: str = Field(
        default="pass",
        description="Method body source code",
    )

    @field_validator("name")
    @classmethod
    def validate_name_not_empty(cls, value: str) -> str:
        """Validate name is not empty."""
        if not value or not value.strip():
            raise ValueError("name must be non-empty string")
        return value
