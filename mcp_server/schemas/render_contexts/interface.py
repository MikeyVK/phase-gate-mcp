# mcp_server/schemas/render_contexts/interface.py
"""InterfaceRenderContext schema.

System-enriched context with lifecycle fields for interface template rendering.

@layer: MCP Server (Schema Infrastructure)
"""

# Third-party
from pydantic import ConfigDict

# Project modules
from mcp_server.schemas.base import BaseRenderContext
from mcp_server.schemas.contexts.interface import InterfaceContext


class InterfaceRenderContext(BaseRenderContext, InterfaceContext):
    """System-enriched interface render context."""

    model_config = ConfigDict(
        frozen=False,
        extra="forbid",
    )
