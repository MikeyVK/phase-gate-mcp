# c:\temp\pgmcp\mcp_server\schemas\cache_publication.py
# template=dto version=0d83ee77 created=2026-06-20T18:39Z updated=
"""CachePublication DTO module.

Data Transfer Object for CachePublication.

@layer: DTOs
@dependencies: pydantic.BaseModel
@responsibilities: Data validation, type safety
"""

from __future__ import annotations

# Third-party
from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

from mcp_server.schemas.error_outputs import ConfigErrorOutput, ExecutionErrorOutput

HexUUID = Annotated[str, StringConstraints(pattern=r"^[a-f0-9]{32}$")]


class CachePublication(BaseModel):
    """CachePublication DTO."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    run_id: HexUUID | None = None
    success: bool = True
    error_code: str | None = None
    size_chars: int | None = Field(default=None, ge=0)
    diagnostic: ConfigErrorOutput | ExecutionErrorOutput | None = None

    @model_validator(mode="after")
    def validate_publication_facts(self) -> Self:
        """Keep successful publication distinct from unavailable delivery."""
        if self.success:
            if self.run_id is None or self.error_code is not None or self.diagnostic is not None:
                raise ValueError("Successful publication requires a run_id and no error diagnosis")
        elif self.run_id is not None or not self.error_code or self.size_chars is not None:
            raise ValueError("Failed publication requires an error_code and no run_id or size")
        return self
