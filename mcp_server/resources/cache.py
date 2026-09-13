# mcp_server/resources/cache.py
"""Resource for reading cached tool outputs.

@layer: MCP (Resources)
@dependencies: [mcp_server.resources.base, mcp_server.core.interfaces, re]
@responsibilities:
    - Match URIs for cached tool outputs (pgmcp://cache/runs/{run_id})
    - Read the cached output from the cache manager and return compact JSON
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import TYPE_CHECKING
from urllib.parse import parse_qsl

from pydantic import BaseModel

from mcp_server.resources.base import BaseResource
from mcp_server.schemas.cache_chunk import CachedResponseChunk, CacheReadWindow

if TYPE_CHECKING:
    from mcp_server.core.interfaces import IToolResponseReader


def _parse_read_uri(uri: str) -> tuple[str, CacheReadWindow | None]:
    """Validate a run URI and optional explicit window without accessing the cache."""
    base, separator, query = uri.partition("?")
    match = re.fullmatch(r"pgmcp://cache/runs/([a-f0-9]{32})", base)
    if match is None or "#" in uri:
        raise ValueError(f"Invalid resource URI: {uri}")
    if not separator:
        return match.group(1), None
    pairs = parse_qsl(query, keep_blank_values=True, strict_parsing=True, max_num_fields=2)
    if len(pairs) != 2 or {key for key, _ in pairs} != {"offset", "limit"}:
        raise ValueError("A cache window requires exactly one offset and one limit")
    if any(re.fullmatch(r"[0-9]+", value) is None for _, value in pairs):
        raise ValueError("Cache offset and limit must be nonnegative decimal integers")
    return match.group(1), CacheReadWindow.model_validate(
        {key: int(value) for key, value in pairs}, strict=True
    )


class CachedResponseResource(BaseResource):
    """Resource provider for cached tool responses."""

    uri_pattern = "pgmcp://cache/runs/.*"
    description = "Cached tool execution results"
    mime_type = "application/json"

    def __init__(self, cache: IToolResponseReader) -> None:
        self._cache = cache

    def matches(self, uri: str) -> bool:
        """Match complete reads and valid bounded windows of cached run resources."""
        try:
            _parse_read_uri(uri)
        except ValueError:
            return False
        return True

    async def read(self, uri: str) -> str:
        """Return complete JSON or a verifiable Unicode-codepoint window of it."""
        run_id, window = _parse_read_uri(uri)

        dto = self._cache.get(run_id, BaseModel)
        if not dto:
            raise ValueError("No cached data found")

        # Returns whitespace-stripped compact JSON with None values excluded
        try:
            content = dto.model_dump_json(exclude_none=True)
        except Exception as e:
            fallback = {
                "success": False,
                "error_type": "SerializationError",
                "message": f"Unable to serialize DTO: {e}",
                "dto_type": type(dto).__name__,
            }
            if hasattr(dto, "error_message") and dto.error_message:
                fallback["error_message"] = str(dto.error_message)
            if hasattr(dto, "traceback") and dto.traceback:
                fallback["traceback"] = str(dto.traceback)
            content = json.dumps(fallback)

        if window is None:
            return content
        if window.offset > len(content):
            raise ValueError("Cache window offset exceeds the response length")
        end = min(window.offset + window.limit, len(content))
        return CachedResponseChunk(
            run_id=run_id,
            offset=window.offset,
            total_chars=len(content),
            sha256=hashlib.sha256(content.encode("utf-8")).hexdigest(),
            text=content[window.offset : end],
            next_offset=end if end < len(content) else None,
        ).model_dump_json()
