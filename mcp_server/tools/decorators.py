"""ResourcePublishingDecorator module.

Decorators for MCP tools, including ResourcePublishingDecorator.

@layer: tools
"""

from typing import Any

from pydantic import BaseModel

from mcp_server.core.interfaces import IToolResponseCache
from mcp_server.core.operation_notes import NoteContext
from mcp_server.tools.base import ITool, ToolExecutionEnvelope
from mcp_server.utils.schema_utils import resolve_schema_refs


class ResourcePublishingDecorator(ITool):
    """Decorator that caches ITool execution envelopes for resource retrieval."""

    def __init__(self, tool: ITool, cache: IToolResponseCache) -> None:
        self._tool = tool
        self._cache = cache

    @property
    def name(self) -> str:
        return self._tool.name

    @property
    def description(self) -> str:
        return self._tool.description

    @property
    def args_model(self) -> type[BaseModel] | None:
        return self._tool.args_model

    @property
    def input_schema(self) -> dict[str, Any]:
        if self.args_model:
            return resolve_schema_refs(self.args_model.model_json_schema())
        return {
            "type": "object",
            "properties": {},
        }

    async def execute(self, params: Any, context: NoteContext) -> ToolExecutionEnvelope:  # noqa: ANN401
        import uuid  # noqa: PLC0415

        result = await self._tool.execute(params, context)
        if isinstance(result, ToolExecutionEnvelope):
            return result
        run_id = str(uuid.uuid4())
        self._cache.put(f"pgmcp://cache/runs/{run_id}", result)
        return ToolExecutionEnvelope(run_id=run_id, data=result)

    def __getattr__(self, name: str) -> Any:  # noqa: ANN401
        return getattr(self._tool, name)
