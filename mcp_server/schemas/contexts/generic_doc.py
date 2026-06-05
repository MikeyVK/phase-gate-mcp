# mcp_server/schemas/contexts/generic_doc.py
"""GenericDocContext schema.

Context schema for generic_doc document artifact scaffolding.

@layer: MCP Server (Schema Infrastructure)
"""

# Third-party
from pydantic import Field

# Project modules
from mcp_server.schemas.contexts.doc_base import DocArtifactContext


class GenericDocContext(DocArtifactContext):
    """Context schema for structured generic document scaffolding.

    Inherits:
        - title (from TitledArtifactContext, with non-empty validation)
        - status (DocumentStatus enum)
        - version (validated x.y or x.y.z)
        - last_updated (validated YYYY-MM-DD)
    """

    purpose: str = Field(description="Purpose statement for the document")
    summary: str = Field(description="High-level summary for the document")
    scope_in: str | None = Field(default=None, description="In-scope summary")
    scope_out: str | None = Field(default=None, description="Out-of-scope summary")
    prerequisites: list[str] = Field(default_factory=list, description="Prerequisite items")
    related_docs: list[str] = Field(default_factory=list, description="Related document paths")
    key_changes: list[str] = Field(default_factory=list, description="Key change bullets")
    migration_steps: list[str] = Field(default_factory=list, description="Migration step list")
    validation_checklist: list[str] = Field(
        default_factory=list,
        description="Validation checklist items",
    )
    faq: list[dict[str, str]] = Field(default_factory=list, description="FAQ entries")
    custom_sections: list[dict[str, object]] = Field(
        default_factory=list,
        description="Additional structured document sections",
    )
