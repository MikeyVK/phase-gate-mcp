# mcp_server/schemas/render_contexts/resource.py
"""ResourceRenderContext schema.

System-enriched context with lifecycle fields for resource template rendering.

@layer: MCP Server (Schema Infrastructure)
"""

# Third-party
from pydantic import ConfigDict

# Project modules
from mcp_server.schemas.base import BaseRenderContext
from mcp_server.schemas.contexts.resource import ResourceContext


class ResourceRenderContext(BaseRenderContext, ResourceContext):
    """System-enriched resource render context."""

    model_config = ConfigDict(
        frozen=False,
        extra="forbid",
    )
