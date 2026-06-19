# mcp_server/resources/cache.py
"""Resource for reading cached tool outputs.

@layer: MCP (Resources)
@dependencies: [mcp_server.resources.base, mcp_server.core.interfaces, re]
@responsibilities:
    - Match URIs for cached tool outputs (pgmcp://cache/runs/{run_id})
    - Read the cached output from the cache manager and return compact JSON
"""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING

from mcp_server.resources.base import BaseResource

if TYPE_CHECKING:
    from mcp_server.core.interfaces import IToolResponseCache


class CachedResponseResource(BaseResource):
    """Resource provider for cached tool responses."""

    uri_pattern = "pgmcp://cache/runs/.*"
    description = "Cached tool execution results"
    mime_type = "application/json"

    def __init__(self, cache: IToolResponseCache) -> None:
        self._cache = cache

    def matches(self, uri: str) -> bool:
        """Check if the URI matches the cached runs pattern."""
        return bool(re.match(r"^pgmcp://cache/runs/[\w-]+$", uri))

    async def read(self, uri: str) -> str:
        """Read the resource content from the cache and return compact JSON."""
        dto = self._cache.get(uri)
        if not dto:
            # Try to resolve hyphenation mismatch (hex vs hyphenated UUID)
            if "-" in uri:
                dto = self._cache.get(uri.replace("-", ""))
            else:
                match = re.match(r"^pgmcp://cache/runs/([a-f0-9]{32})$", uri)
                if match:
                    h = match.group(1)
                    hyphenated = (
                        f"pgmcp://cache/runs/{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"
                    )
                    dto = self._cache.get(hyphenated)

        if not dto:
            raise ValueError("No cached data found")

        # Returns whitespace-stripped compact JSON with None values excluded
        try:
            return dto.model_dump_json(exclude_none=True)
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
            return json.dumps(fallback)
