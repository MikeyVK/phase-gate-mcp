from tests.mcp_server.test_support import get_default_server_root

# tests/mcp_server/unit/config/test_loader.py
# template=unit_test version= created=2026-04-09T00:00Z updated=
"""
Unit tests for ConfigLoader (issue #271 C2 cleanup).

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.config.loader, mcp_server.config.schemas]
"""

# Standard library
from pathlib import Path

# Project modules
from mcp_server.config.loader import ConfigLoader


def _workflow_yaml_without_phases() -> str:
    """Minimal valid workflows.yaml fixture (C6+: no phases field)."""
    return (
        "version: '1.0'\n"
        "workflows:\n"
        "  feature:\n"
        "    name: feature\n"
        "    default_execution_mode: interactive\n"
        "    description: Feature workflow\n"
    )


class TestLoadWorkflowConfig:
    def test_load_workflow_config_catalog_only(self, tmp_path: Path) -> None:
        """load_workflow_config() returns catalog metadata without phase ordering (C6+)."""
        config_dir = tmp_path / get_default_server_root() / "config"
        config_dir.mkdir(parents=True)
        (config_dir / "workflows.yaml").write_text(
            _workflow_yaml_without_phases(),
            encoding="utf-8",
        )
        loader = ConfigLoader(config_root=config_dir)

        result = loader.load_workflow_config()

        wt = result.workflows["feature"]
        assert wt.name == "feature"
        assert wt.description == "Feature workflow"
        assert wt.default_execution_mode == "interactive"
        assert not hasattr(wt, "phases")
