"""
@module: tests.conftest
@layer: Test Infrastructure
@dependencies: pytest
@responsibilities:
  - Register root-level pytest plugins for the full test tree
  - Host only top-level cross-suite pytest configuration
"""

pytest_plugins = [
    "tests.mcp_server.fixtures.artifact_test_harness",
    "tests.mcp_server.fixtures.workflow_fixtures",
]

import os
from pathlib import Path

# Configure default templates root for settings path resolution in tests
_project_root = Path(__file__).resolve().parent.parent
os.environ["MCP_TEMPLATE_ROOT"] = str(
    (_project_root / "mcp_server" / "assets" / "templates").resolve()
)
