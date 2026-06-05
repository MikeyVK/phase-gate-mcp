# mcp_server/schemas/render_contexts/generic_doc.py
"""GenericDocRenderContext schema.

System-enriched context with lifecycle fields for generic_doc rendering.

@layer: MCP Server (Schema Infrastructure)
"""

# Third-party
from pydantic import ConfigDict

# Project modules
from mcp_server.schemas.base import BaseRenderContext
from mcp_server.schemas.contexts.generic_doc import GenericDocContext


class GenericDocRenderContext(BaseRenderContext, GenericDocContext):
    """System-enriched generic_doc render context."""

    model_config = ConfigDict(
        frozen=False,
        extra="forbid",
    )
