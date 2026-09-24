# tests/mcp_server/unit/test_cli.py
"""
Tests for CLI.

@layer: Tests (Unit)
@dependencies: [contextlib, pytest, unittest.mock, mcp_server.cli]
"""

# Standard library
import contextlib
from pathlib import Path
from unittest.mock import MagicMock, patch

# Third-party
import pytest

from mcp_server.cli import main
from mcp_server.config.settings import ServerSettings, Settings


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
    """Normal dispatch selects the V3 bootstrap."""
    mock_server = MagicMock()
    bootstrapper = MagicMock()
    bootstrapper.bootstrap_target.return_value = mock_server

    with (
        patch("mcp_server.config.settings.metadata.version", return_value="3.0.0"),
        patch("mcp_server.cli.ServerBootstrapper", return_value=bootstrapper),
        patch("asyncio.run") as mock_asyncio_run,
        patch("sys.argv", ["mcp-server"]),
    ):
        main()
        bootstrapper.bootstrap_target.assert_called_once()
        mock_asyncio_run.assert_called_once_with(mock_server.run())


def test_cli_init_success(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Initialization copies assets and delegates checkpoint creation to renewal."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    settings = Settings(
        server=ServerSettings(workspace_root=str(workspace), server_root_dir=".pgmcp")
    )
    mock_assets = tmp_path / "mock_assets"
    (mock_assets / "config").mkdir(parents=True)
    (mock_assets / "template_suite").mkdir(parents=True)
    (mock_assets / "config" / "workflows.yaml").touch()
    import shutil  # noqa: PLC0415

    original_copytree = shutil.copytree

    def mock_copytree(src, dst, *args, **kwargs):
        shutil.copytree = original_copytree
        try:
            return shutil.copytree(mock_assets, dst, *args, **kwargs)
        finally:
            shutil.copytree = mock_copytree

    operation = MagicMock()
    operation.last_result.exit_code = 0
    with (
        patch("sys.argv", ["mcp-server", "--init"]),
        patch("sys.exit", side_effect=SystemExit(0)),
        patch("shutil.copytree", side_effect=mock_copytree),
        patch("mcp_server.cli_renewal.build_default_operation", return_value=operation),
        contextlib.suppress(SystemExit),
    ):
        main(settings)

    server_root = workspace / ".pgmcp"
    assert (server_root / "config/workflows.yaml").is_file()
    assert (server_root / "template_suite").is_dir()
    assert not (server_root / ".version").exists()
    operation.execute.assert_called_once_with()
    assert "Successfully initialized" in capsys.readouterr().out


def test_cli_fails_fast_when_state_dir_missing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test that CLI exits with error if .pgmcp directory is missing."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    settings = Settings(
        server=ServerSettings(
            workspace_root=str(workspace),
            server_root_dir=".pgmcp",
        )
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
    assert (
        "Please run with --init to initialize" in captured.err
        or "Please run with --init to initialize" in captured.out
    )


def test_cli_init_already_exists(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Test that --init gracefully aborts if .pgmcp already exists."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    server_root = workspace / ".pgmcp"
    server_root.mkdir()

    settings = Settings(
        server=ServerSettings(
            workspace_root=str(workspace),
            server_root_dir=".pgmcp",
        )
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


def test_cli_degraded_server_on_config_error(tmp_path: Path) -> None:
    """A target-bootstrap configuration error selects the degraded server."""
    from unittest.mock import AsyncMock  # noqa: PLC0415

    from mcp_server.core.exceptions import ConfigError  # noqa: PLC0415

    workspace = tmp_path / "workspace"
    (workspace / ".pgmcp").mkdir(parents=True)
    settings = Settings(
        server=ServerSettings(workspace_root=str(workspace), server_root_dir=".pgmcp")
    )
    with (
        patch("sys.argv", ["mcp-server"]),
        patch(
            "mcp_server.bootstrap.ServerBootstrapper.bootstrap_target",
            side_effect=ConfigError("Corrupt artifacts.yaml config"),
        ),
        patch("mcp_server.server.DegradedMCPServer") as degraded,
    ):
        degraded.return_value.run = AsyncMock()
        main(settings)
        degraded.assert_called_once_with(settings, "Corrupt artifacts.yaml config")
        degraded.return_value.run.assert_called_once()


def test_cli_degraded_server_on_version_mismatch(tmp_path: Path) -> None:
    """A target-bootstrap version error selects the degraded server."""
    from unittest.mock import AsyncMock  # noqa: PLC0415

    from mcp_server.core.exceptions import ConfigError  # noqa: PLC0415

    workspace = tmp_path / "workspace"
    (workspace / ".pgmcp").mkdir(parents=True)
    settings = Settings(
        server=ServerSettings(workspace_root=str(workspace), server_root_dir=".pgmcp")
    )
    with (
        patch("sys.argv", ["mcp-server"]),
        patch(
            "mcp_server.bootstrap.ServerBootstrapper.bootstrap_target",
            side_effect=ConfigError("Workspace version mismatch"),
        ),
        patch("mcp_server.server.DegradedMCPServer") as degraded,
    ):
        degraded.return_value.run = AsyncMock()
        main(settings)
        degraded.assert_called_once_with(settings, "Workspace version mismatch")


def test_cli_upgrade_missing_server_root_exits_1(tmp_path: Path) -> None:
    """Upgrade dispatch forwards the renewal result without a legacy precheck."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    settings = Settings(
        server=ServerSettings(workspace_root=str(workspace), server_root_dir=".pgmcp")
    )
    with (
        patch("sys.argv", ["mcp-server", "--upgrade"]),
        patch("mcp_server.cli_renewal.main", return_value=1) as renewal,
        patch("sys.exit", side_effect=SystemExit(1)) as exit_process,
        contextlib.suppress(SystemExit),
    ):
        main(settings)
        renewal.assert_called_once_with(["--upgrade"], settings=settings)
        exit_process.assert_called_once_with(1)


def test_cli_upgrade_success_exits_0(tmp_path: Path) -> None:
    """Upgrade dispatch returns a successful renewal status."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    settings = Settings(
        server=ServerSettings(workspace_root=str(workspace), server_root_dir=".pgmcp")
    )
    with (
        patch("sys.argv", ["mcp-server", "--upgrade"]),
        patch("mcp_server.cli_renewal.main", return_value=0) as renewal,
        patch("sys.exit", side_effect=SystemExit(0)) as exit_process,
        contextlib.suppress(SystemExit),
    ):
        main(settings)
        renewal.assert_called_once_with(["--upgrade"], settings=settings)
        exit_process.assert_called_once_with(0)


def test_cli_upgrade_failure_exits_1(tmp_path: Path) -> None:
    """Upgrade dispatch returns a failed renewal status."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    settings = Settings(
        server=ServerSettings(workspace_root=str(workspace), server_root_dir=".pgmcp")
    )
    with (
        patch("sys.argv", ["mcp-server", "--upgrade"]),
        patch("mcp_server.cli_renewal.main", return_value=1) as renewal,
        patch("sys.exit", side_effect=SystemExit(1)) as exit_process,
        contextlib.suppress(SystemExit),
    ):
        main(settings)
        renewal.assert_called_once_with(["--upgrade"], settings=settings)
        exit_process.assert_called_once_with(1)


def test_version_consistency() -> None:
    """Verify version parity across SSOT files (pyproject.toml, manifest, settings.py)."""
    import yaml  # noqa: PLC0415

    from mcp_server.config.settings import Settings  # noqa: PLC0415

    repo_root = Path(__file__).resolve().parent.parent.parent.parent

    # 1. pyproject.toml
    pyproject_path = repo_root / "pyproject.toml"
    assert pyproject_path.exists()
    pyproject_text = pyproject_path.read_text(encoding="utf-8")
    assert 'version = "2.0.0"' in pyproject_text

    # 2. release_manifest.yaml
    manifest_path = repo_root / ".pgmcp" / "config" / "release_manifest.yaml"
    assert manifest_path.exists()
    manifest_data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    assert manifest_data.get("version") == "2.0.0"

    # 3. Settings default version
    settings = Settings()
    assert settings.server.version == "2.0.0"
