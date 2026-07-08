"""
@module: tests.conftest
@layer: Test Infrastructure
@dependencies: pytest
@responsibilities:
  - Register root-level pytest plugins for the full test tree
  - Host only top-level cross-suite pytest configuration
"""

import pytest

pytest_plugins = [
    "tests.mcp_server.fixtures.artifact_test_harness",
    "tests.mcp_server.fixtures.workflow_fixtures",
]


def pytest_sessionstart(session: pytest.Session) -> None:
    """Set MCP_TEMPLATE_ROOT dynamically before running tests."""
    import os  # noqa: PLC0415
    from pathlib import Path  # noqa: PLC0415
    from mcp_server.config.settings import Settings  # noqa: PLC0415

    _project_root = Path(session.config.rootdir)
    default_settings = Settings()
    dev_server_root = default_settings.server.server_root_dir

    # Fail-fast check for compiled package assets in development repository
    assets_dir = _project_root / "mcp_server" / "assets"
    if not assets_dir.exists() or not any(assets_dir.iterdir()):
        pytest.exit(
            "CRITICAL: The mcp_server/assets/ directory is empty or missing. "
            "Please run 'python scripts/build_package.py' first.",
            returncode=1,
        )

    # Configure default templates root for settings path resolution in tests
    os.environ["MCP_TEMPLATE_ROOT"] = str((_project_root / dev_server_root / "templates").resolve())
