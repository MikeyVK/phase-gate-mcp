# tests\mcp_server\integration\test_pipeline_e2e.py
# template=integration_test version=85ea75d4 created=2026-06-20T05:50Z updated=
"""
Integration tests for pipeline_e2e.

E2E pipeline integration tests verifying Russian doll decorator wrapping, caching and presenting

@layer: Tests (Integration)
@dependencies: [pytest, pytest-asyncio, tempfile, ResponseCacheManager, EnforcementRunner]
@responsibilities:
    - Test end-to-end pipeline_e2e
    - Verify full-stack integration
    - Validate file system interactions
"""

# Standard library
import re
import shutil
from unittest.mock import MagicMock

# Third-party
import pytest
from pydantic import BaseModel

from mcp_server.state.response_cache import ResponseCacheManager
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_factory import ToolFactory
from mcp_server.presenters.text_presenter import TextPresenter
from mcp.types import CallToolRequest, CallToolRequestParams
from tests.mcp_server.test_support import make_test_server, assert_itool_result


# Dummy Core Tool for E2E validation
class DummyInput(BaseModel):
    val: int


class DummyOutput(BaseModel):
    success: bool = True
    result: str


class DummyCoreTool(ICoreTool[DummyInput, DummyOutput]):
    @property
    def name(self) -> str:
        return "dummy_core_tool"

    @property
    def description(self) -> str:
        return "Dummy core tool for E2E testing"

    @property
    def args_model(self) -> type[BaseModel] | None:
        return DummyInput

    async def execute(self, params: DummyInput, context: NoteContext) -> DummyOutput:
        del context  # Unused
        return DummyOutput(success=True, result=f"Value: {params.val}")


@pytest.fixture
def temp_workspace(tmp_path):
    """Create temporary workspace for integration testing."""
    workspace = tmp_path / "test_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    yield workspace
    if workspace.exists():
        shutil.rmtree(workspace)


class TestPipelineE2E:
    """Integration test suite for pipeline_e2e."""

    @pytest.mark.asyncio
    async def test_pipeline_e2e_flow(self, temp_workspace):
        """Test the end-to-end flow of the new pipeline structure."""
        # Initialize dependencies

        cache_manager = ResponseCacheManager()
        enforcement_runner = MagicMock(spec=EnforcementRunner)

        # Build tool using new factory
        factory = ToolFactory(enforcement_runner=enforcement_runner, workspace_root=temp_workspace)
        decorated_tool = factory.create_tool(DummyCoreTool())

        # Set up test server
        server = make_test_server()
        server.response_cache_manager = cache_manager
        config_data = {
            "global": {
                "next_instruction_texts": {
                    "uri_reference": (
                        "*(Full details available in the structured JSON payload. "
                        "View resource: pgmcp://cache/runs/{run_id})*"
                    )
                }
            },
            "tools": {
                "dummy_core_tool": {
                    "template_success": "Success: {result}",
                    "next_instructions": ["uri_reference"],
                }
            },
        }
        server.presenter = TextPresenter(config_data=config_data)
        server.tools = [decorated_tool]

        # Act - Trigger tool call request
        handler = server.server.request_handlers[CallToolRequest]
        req = CallToolRequest(
            params=CallToolRequestParams(
                name="dummy_core_tool",
                arguments={"val": 42},
            )
        )
        response = await handler(req)

        # Assert - Verify presented output and cache
        text_content = assert_itool_result(response.root)
        assert "Value: 42" in text_content

        # Verify run_id cache resolution

        match = re.search(r"pgmcp://cache/runs/([a-f0-9\-]+)", text_content)
        assert match is not None
        run_id = match.group(1)

        cached_dto = cache_manager.get(run_id, DummyOutput)
        assert cached_dto is not None
        assert cached_dto.result == "Value: 42"
