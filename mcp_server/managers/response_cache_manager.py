"""ResponseCacheManager module.

Cache manager for tool responses.

@layer: managers
"""

from mcp_server.tools.base import ToolExecutionEnvelope
from mcp_server.tools.decorators import IToolResponseCache


class ResponseCacheManager(IToolResponseCache):
    """Cache manager for tool responses."""

    def __init__(self) -> None:
        self._cache: dict[str, ToolExecutionEnvelope] = {}

    def store_run(self, run_id: str, envelope: ToolExecutionEnvelope) -> None:
        self._cache[run_id] = envelope

    def get_run(self, run_id: str) -> ToolExecutionEnvelope | None:
        return self._cache.get(run_id)
