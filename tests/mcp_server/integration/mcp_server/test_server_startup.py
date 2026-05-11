"""Integration tests for the MCP server.

@layer: Tests (Integration)
@dependencies: [pytest, mcp_server.server]
"""

import pytest

from mcp_server.server import MCPServer


@pytest.mark.asyncio
async def test_server_initialization(server: MCPServer) -> None:
    """Test that the MCP server initializes correctly."""
    assert server.server.name == "mcp-workflow"
    assert len(server.resources) > 0


@pytest.mark.asyncio
async def test_list_resources(server: MCPServer) -> None:
    """Test that resources are correctly registered."""
    resource_uris = [r.uri_pattern for r in server.resources]
    assert "pgmcp://rules/coding_standards" in resource_uris


@pytest.mark.asyncio
async def test_read_resource(server: MCPServer) -> None:
    """Test that resources can be read."""
    resource = next(
        r for r in server.resources if r.uri_pattern == "pgmcp://rules/coding_standards"
    )
    content = await resource.read("pgmcp://rules/coding_standards")
    assert "python" in content
