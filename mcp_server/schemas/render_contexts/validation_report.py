# mcp_server/schemas/render_contexts/validation_report.py
"""ValidationReportRenderContext schema.

System-enriched context with lifecycle fields for validation report rendering.

@layer: MCP Server (Schema Infrastructure)
"""

# Third-party
from pydantic import ConfigDict

# Project modules
from mcp_server.schemas.base import BaseRenderContext
from mcp_server.schemas.contexts.validation_report import ValidationReportContext


class ValidationReportRenderContext(BaseRenderContext, ValidationReportContext):
    """System-enriched validation report render context."""

    model_config = ConfigDict(
        frozen=False,
        extra="forbid",
    )
