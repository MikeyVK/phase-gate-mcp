# mcp_server/managers/workspace_version_validator.py
"""WorkspaceVersionValidator manager — validates workspace version compatibility.

@layer: Managers
@dependencies: [pathlib, mcp_server.core.exceptions.ConfigError]
@responsibilities:
    - Verify .version file existence in server root
    - Validate workspace version matches running server version
    - Raise descriptive ConfigError with remediation advice (--init or --upgrade)
"""

from __future__ import annotations

from pathlib import Path

from mcp_server.core.exceptions import ConfigError


class WorkspaceVersionValidator:
    """Validates workspace version against expected server version."""

    def validate(
        self,
        server_root: Path,
        expected_version: str,
        bypass_version_check: bool = False,
    ) -> None:
        """Validate workspace version string against expected server version.

        Raises:
            ConfigError: If version file is missing, unreadable, or version mismatches.
        """
        if bypass_version_check:
            return

        version_file = server_root / ".version"
        if not version_file.exists():
            raise ConfigError(
                f"Workspace version tracking file is missing: '{version_file.as_posix()}'. "
                "Please run with '--init' to initialize the workspace.",
                file_path=version_file.as_posix(),
            )

        try:
            version_str = version_file.read_text(encoding="utf-8").strip()
        except Exception as e:
            raise ConfigError(
                f"Failed to read workspace version file: {e}",
                file_path=version_file.as_posix(),
            ) from e

        if version_str != expected_version:
            raise ConfigError(
                f"Workspace version mismatch. Workspace version: {version_str}, "
                f"Server version: {expected_version}. Please run 'pgmcp --upgrade' to upgrade your workspace.",
                file_path=version_file.as_posix(),
            )

    def read_version(self, server_root: Path) -> str | None:
        """Read version string from workspace if file exists, else return None."""
        version_file = server_root / ".version"
        if version_file.exists():
            return version_file.read_text(encoding="utf-8").strip()
        return None
