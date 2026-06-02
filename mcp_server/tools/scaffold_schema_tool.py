# mcp_server/tools/scaffold_schema_tool.py
"""
Scaffold Schema Tool - Expose artifact context JSON Schema.

Returns the JSON Schema for the context parameter of a V2 artifact type,
enabling agents to discover required/optional fields before scaffolding.

@layer: Backend (Tools)
@dependencies: [ArtifactManager, BaseTool, ToolResult]
@responsibilities:
    - Accept artifact_type from MCP client
    - Delegate to ArtifactManager.get_context_schema()
    - Return JSON Schema dict as ToolResult
    - Let tool_error_handler handle ConfigError for V1-only types
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.artifact_manager import ArtifactManager
from mcp_server.tools.base import BaseTool
from mcp_server.tools.tool_result import ToolResult


class ScaffoldSchemaInput(BaseModel):
    """Input for scaffold_schema tool."""

    model_config = ConfigDict(extra="forbid")

    artifact_type: str = Field(
        ...,
        description="Artifact type ID from registry (e.g., 'dto', 'design', 'research')",
    )


class ScaffoldSchemaTool(BaseTool):
    """Read-only tool that returns the JSON Schema for an artifact context.

    Enables agents to discover required and optional context fields
    before calling scaffold_artifact.
    """

    name = "scaffold_schema"
    description = "Return the JSON Schema for the context parameter of an artifact type."
    args_model = ScaffoldSchemaInput

    def __init__(self, manager: ArtifactManager | None = None) -> None:
        """Initialize tool with an explicitly injected artifact manager."""
        super().__init__()
        if manager is None:
            raise ValueError("ArtifactManager must be injected for scaffold_schema")
        self.manager = manager

    @property
    def input_schema(self) -> dict[str, Any]:
        schema = super().input_schema
        schema["properties"]["artifact_type"]["enum"] = self.manager.registry.list_type_ids()
        return schema

    async def execute(self, params: ScaffoldSchemaInput, context: NoteContext) -> ToolResult:
        """Return JSON Schema for the artifact type's context model.

        All exceptions are handled by tool_error_handler decorator.

        Args:
            params: Input containing artifact_type
            context: NoteContext (unused, required by protocol)

        Returns:
            ToolResult with JSON Schema dict
        """
        schema_dict = self.manager.get_context_schema(params.artifact_type)
        return ToolResult.json_data(schema_dict)
