"""Tests for ITool base components and decorators.

@layer: Tests (Unit)
"""

from typing import Any
import pytest
from pydantic import BaseModel, ConfigDict

from mcp_server.core.operation_notes import NoteContext
# This will cause an ImportError intentionally for the RED phase
from mcp_server.tools.base import ITool, ToolExecutionEnvelope
from mcp_server.tools.decorators import ResourcePublishingDecorator
from mcp_server.managers.response_cache_manager import ResponseCacheManager


class DummyDTO(BaseModel):
    model_config = ConfigDict(frozen=True)
    message: str


class DummyITool(ITool):
    name = "dummy_itool"
    description = "Dummy ITool"
    args_model = None

    async def execute(self, params: Any, context: NoteContext) -> ToolExecutionEnvelope:
        dto = DummyDTO(message="success")
        return ToolExecutionEnvelope(
            run_id="test-run-123",
            data=dto,
            presentation_context={"extra": "info"}
        )


@pytest.mark.asyncio
async def test_tool_execution_envelope() -> None:
    """Test the ToolExecutionEnvelope structure."""
    dto = DummyDTO(message="hello")
    envelope = ToolExecutionEnvelope(run_id="run-1", data=dto)
    
    assert envelope.run_id == "run-1"
    assert envelope.data == dto
    assert envelope.presentation_context == {}


@pytest.mark.asyncio
async def test_resource_publishing_decorator() -> None:
    """Test that ResourcePublishingDecorator caches the DTO."""
    tool = DummyITool()
    # Assuming ResponseCacheManager has an interface like this, we'll implement it in GREEN
    cache_manager = ResponseCacheManager()
    decorated_tool = ResourcePublishingDecorator(tool, cache_manager)
    
    context = NoteContext()
    envelope = await decorated_tool.execute(None, context)
    
    assert envelope.run_id == "test-run-123"
    assert isinstance(envelope.data, DummyDTO)
    assert envelope.data.message == "success"
    
    # Verify cache
    cached = cache_manager.get_run("test-run-123")
    assert cached is not None
    assert cached.data == envelope.data
