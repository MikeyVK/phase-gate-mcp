"""Command line interface for the MCP server."""

import argparse
import asyncio
import shutil
import sys
from pathlib import Path

import yaml

from mcp_server.bootstrap import ServerBootstrapper
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.settings import Settings
from mcp_server.core.error_handling import capture_exception
from mcp_server.core.exceptions import ConfigError, MCPError
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json
from mcp_server.presenters.renewal_presenter import RenewalPresenter
from mcp_server.presenters.schema_resource_presenter import SchemaResourcePresenter
from mcp_server.presenters.startup_recovery_presenter import StartupRecoveryPresenter
from mcp_server.schemas.startup_diagnostic import StartupDiagnostic


def _capture_startup_diagnostic(
    error: BaseException, seen: frozenset[int] = frozenset()
) -> StartupDiagnostic:
    """Detach original exception facts without discarding parameters or cause."""
    seen = seen | {id(error)}
    cause = error.__cause__
    if cause is None and not error.__suppress_context__:
        cause = error.__context__
    params = freeze_json(error.params if isinstance(error, MCPError) else {})
    assert isinstance(params, FrozenJsonObject)
    file_path = None
    if isinstance(error, ConfigError):
        file_path = error.file_path
    elif isinstance(error, FileNotFoundError) and error.filename is not None:
        file_path = str(error.filename)
    return StartupDiagnostic(
        exception_type=f"{type(error).__module__}.{type(error).__qualname__}",
        message=error.message if isinstance(error, MCPError) else str(error),
        code=error.code if isinstance(error, MCPError) else None,
        params=params,
        file_path=file_path,
        cause=(
            _capture_startup_diagnostic(cause, seen)
            if cause is not None and id(cause) not in seen
            else None
        ),
    )


def _reset_binding_choices(server_root: Path) -> None:
    """Clear inherited acknowledgements only in fresh-init configuration."""
    loader = ConfigLoader(server_root / "config")
    declarations = (
        ("checks", loader.load_checks_config()),
        ("tests", loader.load_tests_config()),
        ("fixes", loader.load_fixes_config()),
    )
    for section, declaration in declarations:
        data = declaration.model_dump(mode="json", exclude_unset=True)
        for binding in data[section].values():
            binding["configuration_choice"] = None
        (loader.config_root / f"{section}.yaml").write_text(
            yaml.safe_dump(data, sort_keys=False), encoding="utf-8", newline="\n"
        )


def main(settings: Settings | None = None) -> None:
    """CLI entry point."""
    _settings = settings or Settings.from_env()

    parser = argparse.ArgumentParser(description="Phase-Gate MCP Server")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument(
        "--init",
        action="store_true",
        help="Initialize workspace configuration and templates",
    )
    parser.add_argument(
        "--upgrade",
        action="store_true",
        help="Upgrade workspace configuration and templates",
    )

    args, unknown = parser.parse_known_args()
    if args.upgrade:
        from mcp_server.cli_renewal import main as renewal_main  # noqa: PLC0415

        sys.exit(renewal_main(sys.argv[1:], settings=_settings))
    if unknown:
        parser.error(f"unrecognized arguments: {' '.join(unknown)}")
    if args.version:
        # pylint: disable=no-member
        print(f"Phase-Gate MCP Server v{_settings.server.version}")  # noqa: T201
        sys.exit(0)

    if args.init:
        resolved_server_root = Path(_settings.server.resolved_server_root)
        if resolved_server_root.exists():
            print(  # noqa: T201
                f"Error: Server root directory '{resolved_server_root}' already exists.",
                file=sys.stderr,
            )
            sys.exit(1)

        try:
            package_root = Path(__file__).resolve().parent
            assets_dir = package_root / "assets"

            resolved_server_root.mkdir(parents=True, exist_ok=True)
            shutil.copytree(
                assets_dir,
                resolved_server_root,
                dirs_exist_ok=True,
            )

            _reset_binding_choices(resolved_server_root)

            from mcp_server.cli_renewal import build_default_operation  # noqa: PLC0415

            operation = build_default_operation(_settings)
            operation.execute()
            outcome = operation.last_result
            if outcome is None:
                raise RuntimeError("target_initialization_result_missing")
            if outcome.exit_code != 0:
                sys.stderr.write(RenewalPresenter().present(outcome))
                sys.stderr.flush()
                sys.exit(outcome.exit_code)

            print(  # noqa: T201
                f"Successfully initialized server root at '{resolved_server_root}'",
                file=sys.stdout,
            )
            sys.exit(0)
        except Exception as error:  # noqa: BLE001 -- Terminal CLI boundary preserves exception diagnostics.
            sys.stderr.write(RenewalPresenter().present_error(capture_exception(error)))
            sys.stderr.flush()
            sys.exit(1)

    resolved_server_root = Path(_settings.server.resolved_server_root)
    if not resolved_server_root.exists():
        print(  # noqa: T201
            f"Error: Server root directory '{resolved_server_root}' does not exist.\n"
            "Please run with --init to initialize it.",
            file=sys.stderr,
        )
        sys.exit(1)

    from mcp_server.server import DegradedMCPServer  # noqa: PLC0415

    bootstrapper = ServerBootstrapper(_settings)
    try:
        server = bootstrapper.bootstrap_target()
    except (MCPError, FileNotFoundError) as error:
        if isinstance(error, MCPError) and error.code != "ERR_CONFIG":
            raise
        server = DegradedMCPServer(
            _settings,
            _capture_startup_diagnostic(error),
            StartupRecoveryPresenter(SchemaResourcePresenter()),
        )
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
