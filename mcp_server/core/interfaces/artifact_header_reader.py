# mcp_server/core/interfaces/artifact_header_reader.py
# template=interface version=3fb28c28 created=2026-09-13T17:18Z updated=
"""Closed provenance recognition result and narrow text-only reader contract."""

from __future__ import annotations

from enum import StrEnum
from typing import Protocol, Self

from pydantic import BaseModel, ConfigDict, model_validator

from mcp_server.schemas.template_identity import ArtifactIdentity


class HeaderReadStatus(StrEnum):
    """Distinguish complete recognition, ordinary absence and rejected metadata."""

    RECOGNIZED = "recognized"
    ABSENT = "absent"
    INVALID = "invalid"


class HeaderReadResult(BaseModel):
    """Expose provenance exactly when the entire record was recognized."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    status: HeaderReadStatus
    provenance: ArtifactIdentity | None

    @model_validator(mode="after")
    def complete_recognition(self) -> Self:
        """Reject incomplete successes and provenance attached to rejection."""
        if (self.status is HeaderReadStatus.RECOGNIZED) != (self.provenance is not None):
            raise ValueError("header_result_inconsistent")
        return self


class IArtifactHeaderReader(Protocol):
    """Read original artifact text without filesystem, catalog or mutation access."""

    def read(self, content: str) -> HeaderReadResult:
        """Inspect only the first physical line and return a closed result."""
        ...
