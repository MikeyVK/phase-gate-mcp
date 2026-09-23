"""Integration test configuration for MCP server tests.

@layer: Tests (Support)
@dependencies: pytest, unittest.mock, mcp_server.bootstrap
"""

from collections.abc import Generator
from pathlib import Path
from shutil import copytree
from unittest.mock import MagicMock, patch

import pytest

from mcp_server.bootstrap import ServerBootstrapper
from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.server import MCPServer


@pytest.fixture
def server(tmp_path: Path, pytestconfig: pytest.Config) -> Generator[MCPServer, None, None]:
    """Compose the public V3 server in an isolated workspace with mocked GitHub calls."""
    source = pytestconfig.rootpath / ".pgmcp"
    target = tmp_path / ".pgmcp"
    config_root = target / "config"
    template_root = target / "template_suite"
    copytree(source / "config", config_root)
    copytree(source / "template_suite", template_root)

    settings = Settings(
        server=ServerSettings(
            workspace_root=str(tmp_path),
            config_root=str(config_root),
            template_root=str(template_root),
            bypass_version_check=True,
        )
    )
    with patch("mcp_server.managers.github_manager.GitHubAdapter") as mock_adapter_class:
        mock_adapter = MagicMock()
        mock_adapter.list_issues.return_value = []
        mock_adapter_class.return_value = mock_adapter
        yield ServerBootstrapper(settings).bootstrap_target()
