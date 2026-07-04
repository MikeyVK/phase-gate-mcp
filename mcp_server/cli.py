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

    args = parser.parse_args()

    if args.version:
        # pylint: disable=no-member
        print(f"Phase-Gate MCP Server v{_settings.server.version}")
        sys.exit(0)

    if args.init:
        resolved_server_root = Path(_settings.server.resolved_server_root)
        if resolved_server_root.exists():
            print(
                f"Error: Server root directory '{resolved_server_root}' already exists.",
                file=sys.stderr,
            )
            sys.exit(1)

        try:
            package_root = Path(__file__).resolve().parent
            assets_dir = package_root / "assets"

            resolved_server_root.mkdir(parents=True, exist_ok=True)
            shutil.copytree(
                assets_dir / "config", resolved_server_root / "config", dirs_exist_ok=True
            )
            shutil.copytree(
                assets_dir / "templates", resolved_server_root / "templates", dirs_exist_ok=True
            )

            print(
                f"Successfully initialized server root at '{resolved_server_root}'",
                file=sys.stdout,
            )
            sys.exit(0)
        except Exception as e:
            print(f"Error initializing server root: {e}", file=sys.stderr)
            sys.exit(1)

    resolved_server_root = Path(_settings.server.resolved_server_root)
    if not resolved_server_root.exists():
        print(
            f"Error: Server root directory '{resolved_server_root}' does not exist.\n"
            "Please run with --init to initialize it.",
            file=sys.stderr,
        )
        sys.exit(1)

    bootstrapper = ServerBootstrapper(_settings)
    server = bootstrapper.bootstrap()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
