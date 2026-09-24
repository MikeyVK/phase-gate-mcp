"""Command line interface for the MCP server."""

import argparse
import asyncio
import shutil
import sys
from pathlib import Path

from mcp_server.bootstrap import ServerBootstrapper
from mcp_server.config.settings import Settings


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

            from mcp_server.cli_renewal import build_default_operation  # noqa: PLC0415

            operation = build_default_operation(_settings)
            operation.execute()
            outcome = operation.last_result
            if outcome is None or outcome.exit_code != 0:
                raise RuntimeError("target_initialization_failed")

            print(  # noqa: T201
                f"Successfully initialized server root at '{resolved_server_root}'",
                file=sys.stdout,
            )
            sys.exit(0)
        except Exception as e:
            print(f"Error initializing server root: {e}", file=sys.stderr)  # noqa: T201
            sys.exit(1)

    resolved_server_root = Path(_settings.server.resolved_server_root)
    if not resolved_server_root.exists():
        print(  # noqa: T201
            f"Error: Server root directory '{resolved_server_root}' does not exist.\n"
            "Please run with --init to initialize it.",
            file=sys.stderr,
        )
        sys.exit(1)

    from mcp_server.core.exceptions import ConfigError  # noqa: PLC0415
    from mcp_server.server import DegradedMCPServer  # noqa: PLC0415

    bootstrapper = ServerBootstrapper(_settings)
    try:
        server = bootstrapper.bootstrap_target()
    except (ConfigError, FileNotFoundError) as e:
        server = DegradedMCPServer(_settings, str(e))
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
