# tests\mcp_server\unit\config\test_template_path_resolution.py
# template=unit_test version=3d15d309 created=2026-07-07T22:05Z updated=
"""
Unit tests for mcp_server.config.settings.

Unit tests for dynamic template path resolution.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.config.settings, unittest.mock]
"""

# Standard library
import os
from pathlib import Path

# Project modules
from tests.mcp_server.test_support import get_template_root


class TestTemplatePathResolution:
    """Test suite for settings."""

    def test_get_template_root_respects_env_override(self) -> None:
        """get_template_root() dynamically respects PGMCP_TEMPLATE_ROOT env var."""
        old_val = os.environ.get("PGMCP_TEMPLATE_ROOT")
        mock_path = "/tmp/mock_template_path_override"
        os.environ["PGMCP_TEMPLATE_ROOT"] = mock_path
        try:
            resolved = get_template_root()
            assert resolved == Path(mock_path)
        finally:
            if old_val is not None:
                os.environ["PGMCP_TEMPLATE_ROOT"] = old_val
            else:
                os.environ.pop("PGMCP_TEMPLATE_ROOT", None)

    def test_scaffolding_templates_directory_deleted(self) -> None:
        """Verify duplicate scaffolding templates directory has been deleted."""
        project_root = Path(__file__).resolve().parents[4]
        dup_dir = project_root / "mcp_server" / "scaffolding" / "templates"
        assert not dup_dir.exists(), "Duplicate scaffolding templates folder must be deleted."
