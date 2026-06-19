# mcp_server/state/response_cache.py
"""In-memory cache for storing StructuredTool outputs.

@layer: Backend (State)
@dependencies: [mcp_server.core.interfaces, collections, pydantic]
@responsibilities:
    - Cache StructuredTool output DTO instances in memory
    - Enforce a FIFO/LRU eviction policy using OrderedDict to prevent memory leaks
"""

from __future__ import annotations

import uuid
from collections import OrderedDict
from typing import TYPE_CHECKING, Type, TypeVar, cast

from mcp_server.core.interfaces import IToolResponsePublisher, IToolResponseReader

if TYPE_CHECKING:
    from pydantic import BaseModel

T = TypeVar("T", bound="BaseModel")


class ResponseCacheManager(IToolResponsePublisher, IToolResponseReader):
    """In-memory session cache manager for tool responses.

    Uses OrderedDict to implement a simple bounded FIFO cache eviction.
    """

    def __init__(self, max_size: int = 50) -> None:
        self._max_size = max_size
        self._cache: OrderedDict[str, BaseModel] = OrderedDict()

    def put(self, tool_name: str, output: BaseModel) -> str | None:
        """Publish the output DTO to the cache and return a unique run_id."""
        try:
            # Generate a new unique run_id (or extract it if tool_name is a URI)
            run_id = tool_name
            if "pgmcp://cache/runs/" in tool_name:
                run_id = tool_name.split("/")[-1]
            else:
                run_id = uuid.uuid4().hex

            if run_id in self._cache:
                self._cache.move_to_end(run_id)
            self._cache[run_id] = output

            # Enforce FIFO eviction
            if len(self._cache) > self._max_size:
                self._cache.popitem(last=False)
            return run_id
        except Exception:
            return None

    def get(self, run_id: str, response_model: Type[T] | None = None) -> T | None:
        """Retrieve and deserialize a cached DTO using the expected type-safe model."""
        actual_id = run_id
        if "pgmcp://cache/runs/" in run_id:
            actual_id = run_id.split("/")[-1]

        if actual_id not in self._cache:
            return None

        self._cache.move_to_end(actual_id)
        dto = self._cache[actual_id]

        # If response_model is provided, check or cast
        if response_model is not None:
            if isinstance(dto, response_model):
                return dto
            return None

        return cast(T, dto)

    def exists(self, run_id: str) -> bool:
        """Check if a cached result exists for the run_id."""
        actual_id = run_id
        if "pgmcp://cache/runs/" in run_id:
            actual_id = run_id.split("/")[-1]
        return actual_id in self._cache
