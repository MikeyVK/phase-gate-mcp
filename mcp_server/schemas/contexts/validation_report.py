# mcp_server/schemas/contexts/validation_report.py
"""ValidationReportContext schema.

Context schema for validation_report document artifact scaffolding.

@layer: MCP Server (Schema Infrastructure)
"""

# Third-party
from pydantic import Field

# Project modules
from mcp_server.schemas.contexts.doc_base import DocArtifactContext


class ValidationReportContext(DocArtifactContext):
    """Context schema for validation report document scaffolding."""

    issue_number: int | None = Field(default=None, description="Issue reference number")
    cycle: str | None = Field(default=None, description="Cycle label being validated")
    validation_status: str | None = Field(
        default=None,
        description="Validation outcome (PASS/FAIL/PARTIAL)",
    )
    scope: str | None = Field(default=None, description="Validation scope summary")
