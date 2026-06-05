# mcp_server/schemas/contexts/adapter.py
"""AdapterContext schema.

Context schema for adapter artifact scaffolding (user-facing, no lifecycle fields)

@layer: MCP Server (Schema Infrastructure)
"""

# Third-party
from pydantic import ConfigDict, Field, field_validator

# Project modules
from mcp_server.schemas.base import BaseContext
from mcp_server.schemas.contexts.method_spec import MethodSpec


class AdapterContext(BaseContext):
    """Context schema for adapter artifact scaffolding (user-facing)."""

    model_config = ConfigDict(
        frozen=False,
        extra="forbid",
    )

    name: str = Field(description="Name of the adapter class (PascalCase required)")
    description: str | None = Field(
        default=None,
        description="Description of the adapter's purpose",
    )
    target_interface: str | None = Field(
        default=None,
        description="Target interface or protocol implemented by the adapter",
    )
    methods: list[MethodSpec] = Field(
        default_factory=list,
        description="Optional structured method definitions",
    )

    @field_validator("name")
    @classmethod
    def validate_name_not_empty(cls, value: str) -> str:
        """Validate name is not empty."""
        if not value or not value.strip():
            raise ValueError("name must be non-empty string")
        return value
