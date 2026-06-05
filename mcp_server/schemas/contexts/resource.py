# mcp_server/schemas/contexts/resource.py
"""ResourceContext schema.

Context schema for resource artifact scaffolding (user-facing, no lifecycle fields)

@layer: MCP Server (Schema Infrastructure)
"""

# Third-party
from pydantic import ConfigDict, Field, field_validator

# Project modules
from mcp_server.schemas.base import BaseContext
from mcp_server.schemas.contexts.method_spec import MethodSpec


class ResourceContext(BaseContext):
    """Context schema for resource artifact scaffolding (user-facing)."""

    model_config = ConfigDict(
        frozen=False,
        extra="forbid",
    )

    name: str = Field(description="Name of the resource class (PascalCase required)")
    description: str | None = Field(
        default=None,
        description="Description of the resource's purpose",
    )
    resource_type: str | None = Field(
        default=None,
        description="Resource category or protocol surface",
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
