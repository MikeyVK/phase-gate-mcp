"""Resource for coding standards."""

import json
from pathlib import Path

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.settings import Settings
from mcp_server.resources.base import BaseResource


class StandardsResource(BaseResource):
    """Provides access to coding standards."""

    uri_pattern = "pgmcp://rules/coding_standards"
    description = "Project coding standards and conventions"

    async def read(self, uri: str) -> str:  # noqa: ARG002
        """Read coding standards from the canonical quality config."""
        settings = Settings.from_env()
        server_root = Path(settings.server.workspace_root) / settings.server.server_root_dir
        config_root = server_root / "config"
        quality_config = ConfigLoader(config_root).load_quality_config()

        standards = {
            "python": {
                "version": ">=3.11",
                "style": "pep8",
                "max_line_length": 100,
            },
            "testing": {
                "framework": "pytest",
                "coverage_min": 80,
            },
            "tools": {
                "formatter": "ruff",
                "linter": "ruff",
                "type_checker": "pyright",
            },
            "quality_gates": {
                "active_gates": quality_config.active_gates,
                "gate_count": len(quality_config.active_gates),
            },
        }

        return json.dumps(standards, indent=2)
