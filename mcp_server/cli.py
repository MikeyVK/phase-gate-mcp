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
                assets_dir,
                resolved_server_root,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("template_registry.json"),
            )

            # Write package version file
            version_file = resolved_server_root / ".version"
            version_file.write_text(_settings.server.version + "\n", encoding="utf-8")

            print(
                f"Successfully initialized server root at '{resolved_server_root}'",
                file=sys.stdout,
            )
            sys.exit(0)
        except Exception as e:
            print(f"Error initializing server root: {e}", file=sys.stderr)
            sys.exit(1)

    if args.upgrade:
        resolved_server_root = Path(_settings.server.resolved_server_root)
        if not resolved_server_root.exists():
            print(
                f"Error: Server root directory '{resolved_server_root}' does not exist.\n"
                "Please run with --init to initialize it.",
                file=sys.stderr,
            )
            sys.exit(1)

        try:
            from mcp_server.services.workspace_upgrader import WorkspaceUpgrader  # noqa: PLC0415

            upgrader = WorkspaceUpgrader(_settings)
            log_dto = upgrader.execute_upgrade()
            print(
                f"Successfully upgraded server workspace at '{resolved_server_root}' "
                f"from v{log_dto.from_version} to v{log_dto.to_version}.",
                file=sys.stdout,
            )
            sys.exit(0)
        except Exception as e:
            print(f"Error upgrading server root: {e}", file=sys.stderr)
            sys.exit(1)

    resolved_server_root = Path(_settings.server.resolved_server_root)
    if not resolved_server_root.exists():
        print(
            f"Error: Server root directory '{resolved_server_root}' does not exist.\n"
            "Please run with --init to initialize it.",
            file=sys.stderr,
        )
        sys.exit(1)

    from mcp_server.core.exceptions import ConfigError  # noqa: PLC0415
    from mcp_server.server import DegradedMCPServer  # noqa: PLC0415

    bootstrapper = ServerBootstrapper(_settings)
    try:
        server = bootstrapper.bootstrap()
    except (ConfigError, FileNotFoundError) as e:
        server = DegradedMCPServer(_settings, str(e))
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
