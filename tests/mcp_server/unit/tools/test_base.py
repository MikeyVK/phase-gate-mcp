"""Tests for ILegacyTool base components and decorators.

@layer: Tests (Unit)
"""

from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict

import mcp_server.tools.base as base_mod
from mcp_server.core.operation_notes import NoteContext
from mcp_server.state.response_cache import ResponseCacheManager
from mcp_server.tools.base import ILegacyTool, ToolExecutionEnvelope
from mcp_server.tools.decorators import ResourcePublishingDecorator


class DummyDTO(BaseModel):
    model_config = ConfigDict(frozen=True)
    message: str


class DummyITool(ILegacyTool):
    @property
    def name(self) -> str:
        return "dummy_itool"

    @property
    def description(self) -> str:
        return "Dummy ILegacyTool"

    @property
    def args_model(self) -> type[BaseModel] | None:
        return None

    async def execute(self, params: Any, context: NoteContext) -> DummyDTO:  # noqa: ARG002, ANN401
        return DummyDTO(message="success")


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
    cache_manager = ResponseCacheManager()
    decorated_tool = ResourcePublishingDecorator(tool, cache_manager)

    context = NoteContext()
    envelope = await decorated_tool.execute(None, context)

    assert envelope.run_id is not None
    assert isinstance(envelope.data, DummyDTO)
    assert envelope.data.message == "success"

    # Verify cache using the generated run_id
    cached = cache_manager.get(f"pgmcp://cache/runs/{envelope.run_id}")
    assert cached is not None
    assert cached == envelope.data


def test_legacy_classes_deleted() -> None:
    """Verify legacy classes are deleted from base.py."""
    assert not hasattr(base_mod, "BaseTool")
    assert not hasattr(base_mod, "StructuredTool")
    assert not hasattr(base_mod, "BranchMutatingTool")
