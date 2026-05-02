# mcp_server/schemas/contexts/planning.py
# template=schema version=74378193 created=2026-02-18T00:00Z updated=
"""PlanningContext schema.

Context schema for Planning document artifact scaffolding (user-facing, no lifecycle fields)

@layer: MCP Server (Schema Infrastructure)
"""

# Third-party
from pydantic import Field

# Project modules
from mcp_server.schemas.contexts.doc_base import DocArtifactContext


class PlanningContext(DocArtifactContext):
    """Context schema for Planning document artifact scaffolding (user-facing).

    Covers required fields per concrete/planning.md.jinja2 TEMPLATE_METADATA.
    Lifecycle fields (output_path, version_hash, etc.) added by PlanningRenderContext.

    Inherits:
        - title (from DocArtifactContext, with non-empty validation)
    """

    summary: str = Field(description="High-level summary of what is being planned")
    tdd_cycles: list[dict] = Field(
        description=(
            "TDD cycle breakdown. Each entry is a dict with keys: "
            "name (str), goal (str), tests (list[str]), "
            "success_criteria (list[str] | str), dependencies (list[str], optional)."
        )
    )
    purpose: str | None = Field(default=None, description="Purpose of this planning document")
    scope_in: str | None = Field(default=None, description="What is in scope")
    scope_out: str | None = Field(default=None, description="What is out of scope")
    prerequisites: list[str] = Field(
        default_factory=list, description="Prerequisites before work can begin"
    )
    dependencies: list[str] = Field(
        default_factory=list, description="Dependencies between cycles or on external work"
    )
    risks: list[dict] = Field(
        default_factory=list,
        description=(
            "Identified risks. Each entry is a dict with keys: "
            "description (str), mitigation (str)."
        ),
    )
    milestones: list[str] = Field(
        default_factory=list, description="Key milestones and checkpoints"
    )
    related_docs: list[str] = Field(
        default_factory=list, description="Related documents in the project"
    )
