# mcp_server/schemas/render_contexts/adapter.py
"""AdapterRenderContext schema.

System-enriched context with lifecycle fields for adapter template rendering.

@layer: MCP Server (Schema Infrastructure)
"""

# Third-party
from pydantic import ConfigDict

# Project modules
from mcp_server.schemas.base import BaseRenderContext
from mcp_server.schemas.contexts.adapter import AdapterContext


class AdapterRenderContext(BaseRenderContext, AdapterContext):
    """System-enriched adapter render context."""

    model_config = ConfigDict(
        frozen=False,
        extra="forbid",
    )
