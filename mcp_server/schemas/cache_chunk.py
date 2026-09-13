# mcp_server/schemas/cache_chunk.py
# template=dto version=0d83ee77 created=2026-09-13T12:37Z updated=
"""Bounded cache resource reads.

Offsets and lengths count Unicode codepoints in the complete JSON text.
@layer: DTOs
"""

from pydantic import BaseModel, ConfigDict, Field


class CacheReadWindow(BaseModel):
    """Explicit bounded window requested on an existing resource URI."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    offset: int = Field(ge=0)
    limit: int = Field(gt=0, le=12000)


class CachedResponseChunk(BaseModel):
    """A verifiable fragment of one cached JSON response."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    run_id: str
    offset: int
    total_chars: int
    sha256: str
    text: str
    next_offset: int | None
