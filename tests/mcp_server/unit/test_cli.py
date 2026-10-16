# tests/mcp_server/unit/test_cli.py
"""
Tests for CLI.

@layer: Tests (Unit)
@dependencies: [contextlib, pytest, unittest.mock, mcp_server.cli]
"""

# Standard library
import contextlib
import json
from pathlib import Path
from unittest.mock import ANY, MagicMock, patch

# Third-party
import pytest

from mcp_server.cli import main
from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject
from mcp_server.schemas.startup_diagnostic import StartupDiagnostic
from mcp_server.services.template_renewal import RenewalOutcome, RenewalResult


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


@pytest.mark.parametrize("outcome", ["fresh_installed", "candidate_invalid", "upgrade_busy"])
def test_cli_init_result(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], outcome: RenewalOutcome
) -> None:
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
    binding = {
        "adapter_id": "fixture",
        "capability": "check",
        "timeout_seconds": 9,
        "default_args": ["--literal", "two words"],
        "configuration_choice": "configured_arguments",
    }
    copied_config = {
        "checks": {
            "configured_targets": {},
            "checks": {"chosen": binding},
            "profiles": {"preflight": {"checks": ["chosen"]}},
            "profiles_by_extension": {".py": "preflight"},
            "run_checks": {},
        },
        "tests": {"tests": {"chosen": {**binding, "active": True}}},
        "fixes": {"fixes": {"chosen": binding}},
    }
    for section, data in copied_config.items():
        (mock_assets / "config" / f"{section}.yaml").write_text(json.dumps(data), encoding="utf-8")
    import shutil  # noqa: PLC0415

    original_copytree = shutil.copytree

    def mock_copytree(src, dst, *args, **kwargs):
        shutil.copytree = original_copytree
        try:
            return shutil.copytree(mock_assets, dst, *args, **kwargs)
        finally:
            shutil.copytree = mock_copytree

    operation = MagicMock()
    operation.last_result = RenewalResult(outcome=outcome, failure_code="fixture_result")
    with (
        patch("sys.argv", ["mcp-server", "--init"]),
        patch("sys.exit", side_effect=SystemExit(operation.last_result.exit_code)) as exit_process,
        patch("shutil.copytree", side_effect=mock_copytree),
        patch("mcp_server.cli_renewal.build_default_operation", return_value=operation),
        contextlib.suppress(SystemExit),
    ):
        main(settings)

    server_root = workspace / ".pgmcp"
    assert (server_root / "config/workflows.yaml").is_file()
    assert (server_root / "template_suite").is_dir()
    assert not (server_root / ".version").exists()
    for section, expected in copied_config.items():
        installed = json.loads(
            (server_root / "config" / f"{section}.yaml").read_text(encoding="utf-8")
        )
        assert installed == expected
        assert (
            json.loads((mock_assets / "config" / f"{section}.yaml").read_text(encoding="utf-8"))
            == expected
        )
    operation.execute.assert_called_once_with()
    exit_process.assert_called_once_with(operation.last_result.exit_code)
    captured = capsys.readouterr()
    if outcome == "fresh_installed":
        assert "Successfully initialized" in captured.out
        assert not captured.err
    else:
        assert "fixture_result" in captured.err
        assert not captured.out


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
    owner_config = server_root / "checks.yaml"
    owner_config.write_bytes(b"owner choices")

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
    assert owner_config.read_bytes() == b"owner choices"


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
        degraded.assert_called_once_with(
            settings,
            StartupDiagnostic(
                exception_type="mcp_server.core.exceptions.ConfigError",
                message="Corrupt artifacts.yaml config",
                code="ERR_CONFIG",
                params=FrozenJsonObject(()),
            ),
            ANY,
        )
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
        degraded.assert_called_once_with(
            settings,
            StartupDiagnostic(
                exception_type="mcp_server.core.exceptions.ConfigError",
                message="Workspace version mismatch",
                code="ERR_CONFIG",
                params=FrozenJsonObject(()),
            ),
            ANY,
        )


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


def test_cli_init_exception_preserves_diagnostic(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Initialization failures expose the original chained exception and facts."""
    from mcp_server.core.exceptions import ConfigError  # noqa: PLC0415

    settings = Settings(server=ServerSettings(workspace_root=str(tmp_path)))
    assets = tmp_path / "assets"
    assets.mkdir()
    cause = OSError("fixture source unreadable")

    def fail_copy(*_args: object, **_kwargs: object) -> None:
        try:
            raise cause
        except OSError as error:
            raise ConfigError(
                "fixture invalid assets",
                file_path=str(assets),
            ) from error

    with (
        patch("sys.argv", ["pgmcp", "--init"]),
        patch("shutil.copytree", side_effect=fail_copy),
        pytest.raises(SystemExit) as exited,
    ):
        main(settings)

    assert exited.value.code == 1
    err = capsys.readouterr().err
    assert "fixture source unreadable" in err
    assert "fixture invalid assets" in err
    assert "ERR_CONFIG" in err
    assert str(assets) in err
    assert "Traceback" in err
    assert "fail_copy" in err
