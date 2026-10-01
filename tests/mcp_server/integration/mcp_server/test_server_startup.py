"""Integration tests for the MCP server.

@layer: Tests (Integration)
@dependencies: [pytest, mcp_server.server]
"""

import json

import pytest
from mcp.types import (
    ReadResourceRequest,
    ReadResourceRequestParams,
    ReadResourceResult,
    TextResourceContents,
)
from pydantic import AnyUrl

from mcp_server.server import MCPServer


@pytest.mark.asyncio
async def test_server_initialization(server: MCPServer) -> None:
    """Test that the MCP server initializes correctly."""
    assert server.server.name == "phase-gate-mcp"
    assert len(server.resources) > 0


@pytest.mark.asyncio
async def test_list_resources(server: MCPServer) -> None:
    """Test that resources are correctly registered."""
    resource_uris = [r.uri_pattern for r in server.resources]
    assert "pgmcp://rules/coding_standards" in resource_uris


@pytest.mark.asyncio
async def test_read_resource(server: MCPServer) -> None:
    """Test that resources can be read."""
    response = await server.server.request_handlers[ReadResourceRequest](
        ReadResourceRequest(
            params=ReadResourceRequestParams(uri=AnyUrl("pgmcp://rules/coding_standards"))
        )
    )
    assert isinstance(response.root, ReadResourceResult)
    assert len(response.root.contents) == 1
    content = response.root.contents[0]
    assert isinstance(content, TextResourceContents)
    policy = json.loads(content.text)
    assert policy["schema_version"] == 1
    assert policy["run_checks"]["bindings"]
