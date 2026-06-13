# mcp_server/resources/cache.py
"""Resource for reading cached tool outputs.

@layer: MCP (Resources)
@dependencies: [mcp_server.resources.base, mcp_server.core.interfaces, re]
@responsibilities:
    - Match URIs for cached tool outputs (pgmcp://cache/runs/{run_id})
    - Read the cached output from the cache manager and return compact JSON
"""

from __future__ import annotations

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
            raise ValueError(f"No cached data found for URI: {uri}")

        # Returns whitespace-stripped compact JSON with None values excluded
        return dto.model_dump_json(exclude_none=True)
