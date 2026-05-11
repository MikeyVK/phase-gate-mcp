"""Integration test configuration for MCP server tests.

@layer: Tests (Support)
@dependencies: pytest, unittest.mock, mcp_server.server
"""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.server import MCPServer


@pytest.fixture
def server() -> Generator[MCPServer, None, None]:
    """
    Create an MCPServer instance with mocked GitHub dependencies.

    This patches the GitHubAdapter at the manager level so all GitHub
    operations return mock data instead of hitting the real API.
    Uses explicit Settings to avoid inheriting MCP_SERVER_NAME from the
    host process (e.g. the running MCP server that launches the tests).
    """
    # Patch the GitHubAdapter at the point where it's instantiated
    with patch("mcp_server.managers.github_manager.GitHubAdapter") as mock_adapter_class:
        # Configure the mock adapter
        mock_adapter = MagicMock()
        mock_adapter.list_issues.return_value = []
        mock_adapter_class.return_value = mock_adapter

        settings = Settings(server=ServerSettings())
        yield MCPServer(settings=settings)
