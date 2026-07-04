# tests/mcp_server/unit/test_cli.py
"""
Tests for CLI.

@layer: Tests (Unit)
@dependencies: [contextlib, pytest, unittest.mock, mcp_server.cli]
"""

# Standard library
import contextlib
from unittest.mock import MagicMock, patch

# Third-party
import pytest

# Project modules
from mcp_server.cli import main


def test_cli_version(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that --version flag prints version and exits without running server."""
    with (
        patch("mcp_server.config.settings.metadata.version", return_value="3.0.0"),
        patch("sys.exit") as mock_exit,
        patch("mcp_server.cli.ServerBootstrapper") as mock_bootstrapper,
        patch("sys.argv", ["mcp-server", "--version"]),
    ):
        mock_exit.side_effect = SystemExit(0)
        with contextlib.suppress(SystemExit):
            main()

        mock_exit.assert_called_with(0)
        mock_bootstrapper.assert_not_called()

    captured = capsys.readouterr()
    assert "Phase-Gate MCP Server v3.0.0" in captured.out


def test_cli_run() -> None:
    """Test that main() bootstraps and runs the server when no arguments provided."""
    mock_server = MagicMock()
    mock_bootstrapper_instance = MagicMock()
    mock_bootstrapper_instance.bootstrap.return_value = mock_server

    with (
        patch("mcp_server.config.settings.metadata.version", return_value="3.0.0"),
        patch("mcp_server.cli.ServerBootstrapper", return_value=mock_bootstrapper_instance),
        patch("asyncio.run") as mock_asyncio_run,
        patch("sys.argv", ["mcp-server"]),
    ):
        main()
        mock_bootstrapper_instance.bootstrap.assert_called_once()
        mock_asyncio_run.assert_called_once_with(mock_server.run())


def test_cli_init_success(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Test that --init copies assets to resolved_server_root."""
    from pathlib import Path
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    
    from mcp_server.config.settings import Settings
    settings = Settings(
        workspace_root=str(workspace),
        server_root_dir=".pgmcp",
    )
    
    with (
        patch("sys.argv", ["mcp-server", "--init"]),
        patch("sys.exit") as mock_exit,
    ):
        mock_exit.side_effect = SystemExit(0)
        with contextlib.suppress(SystemExit):
            main(settings)
            
        mock_exit.assert_called_with(0)
        
    server_root = workspace / ".pgmcp"
    assert (server_root / "config").exists()
    assert (server_root / "templates").exists()
    assert (server_root / "config" / "workflows.yaml").exists()


def test_cli_fails_fast_when_state_dir_missing(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Test that CLI exits with error if .pgmcp directory is missing."""
    from pathlib import Path
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    
    from mcp_server.config.settings import Settings
    settings = Settings(
        workspace_root=str(workspace),
        server_root_dir=".pgmcp",
    )
    
    with (
        patch("sys.argv", ["mcp-server"]),
        patch("sys.exit") as mock_exit,
    ):
        mock_exit.side_effect = SystemExit(1)
        with contextlib.suppress(SystemExit):
            main(settings)
            
        mock_exit.assert_called_with(1)
        
    captured = capsys.readouterr()
    assert "Please run with --init to initialize" in captured.err or "Please run with --init to initialize" in captured.out


def test_cli_init_already_exists(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Test that --init gracefully aborts if .pgmcp already exists."""
    from pathlib import Path
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    server_root = workspace / ".pgmcp"
    server_root.mkdir()
    
    from mcp_server.config.settings import Settings
    settings = Settings(
        workspace_root=str(workspace),
        server_root_dir=".pgmcp",
    )
    
    with (
        patch("sys.argv", ["mcp-server", "--init"]),
        patch("sys.exit") as mock_exit,
    ):
        mock_exit.side_effect = SystemExit(1)
        with contextlib.suppress(SystemExit):
            main(settings)
            
        mock_exit.assert_called_with(1)
        
    captured = capsys.readouterr()
    assert "already exists" in captured.err or "already exists" in captured.out
