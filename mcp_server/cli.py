"""Command line interface for the MCP server."""

import argparse
import asyncio
import sys

from mcp_server.bootstrap import ServerBootstrapper
from mcp_server.config.settings import Settings


def main(settings: Settings | None = None) -> None:
    """CLI entry point."""
    _settings = settings or Settings.from_env()

    parser = argparse.ArgumentParser(description="Phase-Gate MCP Server")
    parser.add_argument("--version", action="store_true", help="Show version")

    args = parser.parse_args()

    if args.version:
        # pylint: disable=no-member
        print(f"Phase-Gate MCP Server v{_settings.server.version}")
        sys.exit(0)

    bootstrapper = ServerBootstrapper(_settings)
    server = bootstrapper.bootstrap()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
