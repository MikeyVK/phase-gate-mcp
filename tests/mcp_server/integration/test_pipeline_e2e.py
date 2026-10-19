# tests\mcp_server\integration\test_pipeline_e2e.py
# template=integration_test version=85ea75d4 created=2026-06-20T05:50Z updated=2026-08-19T19:05Z
"""Integration tests for pipeline_e2e.

E2E pipeline integration tests verifying decorator wrapping, caching and presenting

@layer: Tests (Integration)
@dependencies: [pytest, pytest-asyncio, tempfile, ResponseCacheManager, EnforcementRunner]
@responsibilities:
    - Test end-to-end pipeline_e2e
    - Verify full-stack integration
    - Validate file system interactions
"""

# Standard library
import json
import re
import shutil
from collections.abc import Generator
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

# Third-party
import pytest
from mcp.types import CallToolRequest, CallToolRequestParams
from pydantic import BaseModel

from mcp_server.config.schemas.presentation_config import PresentationConfig
from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.core.exceptions import (
    ValidationError as CoreValidationError,
)
from mcp_server.core.interfaces.icore_tool import ICoreTool
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_factory import ToolFactory
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.schemas.cache_publication import CachePublication
from mcp_server.schemas.error_outputs import EnforcementErrorOutput
from mcp_server.schemas.presentation_output import InlineOperation, PublicToolResponse
from mcp_server.server import MCPServer
from mcp_server.state.response_cache import ResponseCacheManager
from tests.mcp_server.test_support import (
    assert_itool_result,
    connected_mcp_client,
    make_config_loader,
    make_response_presenter,
    make_test_server,
)


# Dummy Core Tool for E2E validation
class DummyInput(BaseModel):
    val: int


class DummyOutput(BaseModel):
    success: bool = True
    result: str


def _presentation_config() -> dict[str, Any]:
    config = make_config_loader().load_presentation_config().model_dump(by_alias=True)
    config["tools"] = {"dummy_core_tool": {"template_success": "Success: {result}"}}
    return config


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
def temp_workspace(tmp_path: Path) -> Generator[Path]:
    """Create temporary workspace for integration testing."""
    workspace = tmp_path / "test_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    yield workspace
    if workspace.exists():
        shutil.rmtree(workspace)


@pytest.fixture
def isolated_server(temp_workspace: Path) -> MCPServer:
    """Compose the real server with a private writable root per test."""
    repo_root = Path(__file__).resolve().parents[3]
    settings = Settings(
        server=ServerSettings(
            workspace_root=str(temp_workspace),
            config_root=str(repo_root / ".pgmcp" / "config"),
            template_root=str(repo_root / ".pgmcp" / "template_suite"),
            bypass_version_check=True,
        )
    )
    return make_test_server(settings=settings)


class TestPipelineE2E:
    """Integration test suite for pipeline_e2e."""

    @pytest.mark.asyncio
    async def test_pipeline_e2e_flow(
        self, temp_workspace: Path, isolated_server: MCPServer
    ) -> None:
        """Test the end-to-end flow of the new pipeline structure."""
        cache_manager = ResponseCacheManager()
        enforcement_runner = MagicMock(spec=EnforcementRunner)

        # Build tool using new factory
        factory = ToolFactory(enforcement_runner=enforcement_runner, workspace_root=temp_workspace)
        decorated_tool = factory.create_tool(DummyCoreTool())

        # Set up test server
        server = isolated_server
        server.response_cache_manager = cache_manager
        config_data = _presentation_config()
        server.presenter = make_response_presenter(PresentationConfig.model_validate(config_data))
        server.tools = [decorated_tool]

        # Act - Trigger tool call request
        req = CallToolRequest(
            params=CallToolRequestParams(
                name="dummy_core_tool",
                arguments={"val": 42},
            )
        )
        async with connected_mcp_client(server) as client:
            response = await client.call_tool(req.params.name, req.params.arguments)

        # Assert - Verify presented output and cache
        text_content = assert_itool_result(response)
        assert "Value: 42" in text_content

        # Verify run_id cache resolution
        match = re.search(r"pgmcp://cache/runs/([a-f0-9\-]+)", text_content)
        assert match is not None
        run_id = match.group(1)

        cached_dto = cache_manager.get(run_id, DummyOutput)
        assert cached_dto is not None
        assert cached_dto.result == "Value: 42"
        assert response.structured_content is not None
        envelope = PublicToolResponse.model_validate_json(json.dumps(response.structured_content))
        assert isinstance(envelope.data, InlineOperation)
        assert envelope.data.operation == cached_dto.model_dump(mode="json", by_alias=True)

    @pytest.mark.asyncio
    async def test_pipeline_cache_fallback(
        self, temp_workspace: Path, isolated_server: MCPServer
    ) -> None:
        """Preserve the operation and configured cache-failure evidence without a cache URI."""
        cache_manager = MagicMock(spec=ResponseCacheManager)
        cache_pub_fail = CachePublication(run_id=None, success=False, error_code="write_failed")
        cache_manager.put.return_value = cache_pub_fail
        enforcement_runner = MagicMock(spec=EnforcementRunner)

        factory = ToolFactory(enforcement_runner=enforcement_runner, workspace_root=temp_workspace)
        decorated_tool = factory.create_tool(DummyCoreTool())

        server = isolated_server
        server.response_cache_manager = cache_manager
        config_data = _presentation_config()
        config_data["global"]["next_instruction_texts"]["cache_publication_failed"] = (
            "CACHE FAILURE MARKER"
        )
        server.presenter = make_response_presenter(PresentationConfig.model_validate(config_data))
        server.tools = [decorated_tool]

        req = CallToolRequest(
            params=CallToolRequestParams(
                name="dummy_core_tool",
                arguments={"val": 100},
            )
        )
        async with connected_mcp_client(server) as client:
            response = await client.call_tool(req.params.name, req.params.arguments)

        text_content = assert_itool_result(response)
        assert "Value: 100" in text_content
        warning = config_data["global"]["next_instruction_texts"]["cache_publication_failed"]
        assert warning in text_content
        assert "pgmcp://cache/runs/" not in text_content
        expected = DummyOutput(success=True, result="Value: 100")
        assert not response.is_error
        assert response.structured_content is not None
        envelope = PublicToolResponse.model_validate_json(json.dumps(response.structured_content))
        assert envelope.success
        assert isinstance(envelope.data, InlineOperation)
        assert envelope.data.operation == expected.model_dump(mode="json", by_alias=True)
        assert envelope.presentation == text_content
        assert envelope.delivery_error is None
        cache_manager.put.assert_called_once_with("dummy_core_tool", expected)

    @pytest.mark.asyncio
    async def test_pipeline_enforcement_blocker(
        self, temp_workspace: Path, isolated_server: MCPServer
    ) -> None:
        """Verify that when the enforcement runner raises a ValidationError,
        the pipeline maps it to EnforcementErrorOutput DTO and returns it formatted.
        """
        cache_manager = ResponseCacheManager()
        enforcement_runner = MagicMock(spec=EnforcementRunner)
        enforcement_runner.run.side_effect = CoreValidationError(
            message="Dirty workdir detected",
            error_code="dirty_workdir",
            params={"branch": "feature-branch"},
        )

        factory = ToolFactory(enforcement_runner=enforcement_runner, workspace_root=temp_workspace)
        decorated_tool = factory.create_tool(DummyCoreTool())

        server = isolated_server
        server.response_cache_manager = cache_manager
        config_data = _presentation_config()
        config_data["global"]["failures"] = {"dirty_workdir": "Branch {branch} is dirty!"}
        server.presenter = make_response_presenter(PresentationConfig.model_validate(config_data))
        server.tools = [decorated_tool]

        req = CallToolRequest(
            params=CallToolRequestParams(
                name="dummy_core_tool",
                arguments={"val": 42},
            )
        )
        async with connected_mcp_client(server) as client:
            response = await client.call_tool(req.params.name, req.params.arguments)

        assert response.is_error
        assert len(response.content) == 1
        text_content = response.content[0].text
        assert "❌ Branch feature-branch is dirty!" in text_content

        match = re.search(r"pgmcp://cache/runs/([a-f0-9\-]+)", text_content)
        assert match is not None
        run_id = match.group(1)

        cached_dto = cache_manager.get(run_id, EnforcementErrorOutput)
        assert cached_dto is not None
        assert cached_dto.success is False
        assert cached_dto.error_type == "EnforcementError"
        assert cached_dto.error_code == "dirty_workdir"
        assert cached_dto.params == {"branch": "feature-branch"}
