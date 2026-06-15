# mcp_server/state/response_cache.py
"""In-memory cache for storing StructuredTool outputs.

@layer: Backend (State)
@dependencies: [mcp_server.core.interfaces, collections, pydantic]
@responsibilities:
    - Cache StructuredTool output DTO instances in memory
    - Enforce a FIFO/LRU eviction policy using OrderedDict to prevent memory leaks
"""

from __future__ import annotations

from collections import OrderedDict
from typing import TYPE_CHECKING

from mcp_server.core.interfaces import IToolResponseCache

if TYPE_CHECKING:
    from pydantic import BaseModel


class ResponseCacheManager(IToolResponseCache):
    """In-memory session cache manager for tool responses.

    Uses OrderedDict to implement a simple bounded FIFO cache eviction.
    """

    def __init__(self, max_size: int = 50) -> None:
        self._max_size = max_size
        self._cache: OrderedDict[str, BaseModel] = OrderedDict()

    def put(self, uri: str, output: BaseModel) -> None:
        """Cache the *output* DTO instance under the *uri* key."""
        if uri in self._cache:
            self._cache.move_to_end(uri)
        self._cache[uri] = output

        # Enforce FIFO eviction
        if len(self._cache) > self._max_size:
            self._cache.popitem(last=False)

    def get(self, uri: str) -> BaseModel | None:
        """Retrieve the cached DTO instance for *uri*, or None."""
        if uri not in self._cache:
            return None
        self._cache.move_to_end(uri)
        return self._cache[uri]

    def exists(self, uri: str) -> bool:
        """Check if *uri* is present in the cache."""
        return uri in self._cache
