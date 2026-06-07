# mcp_server/schemas/contexts/doc_base.py
# template=schema version=74378193 created=2026-02-18T00:00Z updated=
"""DocArtifactContext base schema for document artifact types.

Common base for all document artifact context schemas: research, planning,
design, architecture, reference. Inherits title field + validator from
TitledArtifactContext, eliminating duplication.

@layer: MCP Server (Schema Infrastructure)
"""

# Standard library
import enum
import re

# Third-party
from pydantic import ConfigDict, Field, field_validator

# Project modules
from mcp_server.schemas.contexts.titled_base import TitledArtifactContext


class DocumentStatus(enum.StrEnum):
    """Valid lifecycle statuses for governed document artifacts."""

    DRAFT = "DRAFT"
    PRELIMINARY = "PRELIMINARY"
    APPROVED = "APPROVED"
    DEFINITIVE = "DEFINITIVE"
    DEPRECATED = "DEPRECATED"
    PENDING = "PENDING"


class DocArtifactContext(TitledArtifactContext):
    """Base context class for all document artifact types.

    Inherits `title` field and `validate_title_not_empty` from
    TitledArtifactContext. Document subclasses (research, planning, design,
    architecture, reference) extend this class.

    Structural fields `status`, `version`, and `last_updated` are required on
    every governed document artifact. They are always rendered unconditionally
    by every concrete doc template. A document without these fields is
    incomplete, not optional.
    """

    model_config = ConfigDict(frozen=False, extra="forbid")

    status: DocumentStatus = Field(
        description=(
            "Document lifecycle status (DRAFT|PRELIMINARY|APPROVED|DEFINITIVE|DEPRECATED|PENDING)"
        )
    )
    version: str = Field(description="Document version in x.y or x.y.z format (e.g. 1.0, 2.3.1)")
    last_updated: str = Field(description="Last updated date in ISO format YYYY-MM-DD")

    @field_validator("version")
    @classmethod
    def validate_version_format(cls, v: str) -> str:
        if not re.match(r"^\d+\.\d+(\.\d+)?$", v):
            raise ValueError(f"version must be in x.y or x.y.z format, got: {v!r}")
        return v

    @field_validator("last_updated")
    @classmethod
    def validate_last_updated_format(cls, v: str) -> str:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            raise ValueError(f"last_updated must be in YYYY-MM-DD format, got: {v!r}")
        return v
