"""Integration tests for the MCP server.

@layer: Tests (Integration)
@dependencies: [pytest, mcp_server.server]
"""

import json

import pytest
from mcp.shared.exceptions import MCPError
from mcp.types import (
    ReadResourceResult,
    TextResourceContents,
)

from mcp_server.server import MCPServer
from tests.mcp_server.test_support import connected_mcp_client


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
    async with connected_mcp_client(server) as client:
        response = await client.read_resource("pgmcp://rules/coding_standards")
    assert isinstance(response, ReadResourceResult)
    assert len(response.contents) == 1
    content = response.contents[0]
    assert isinstance(content, TextResourceContents)
    assert str(content.uri) == "pgmcp://rules/coding_standards"
    assert content.mime_type == "text/plain"
    policy = json.loads(content.text)
    assert policy["schema_version"] == 1
    assert policy["run_checks"]["bindings"]

    async with connected_mcp_client(server) as client:
        with pytest.raises(MCPError, match="Resource not found: pgmcp://missing") as caught:
            await client.read_resource("pgmcp://missing")
        assert caught.value.code == 0
