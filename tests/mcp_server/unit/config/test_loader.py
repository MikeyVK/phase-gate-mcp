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


def _workflow_yaml(phases: list[str]) -> str:
    phases_str = ", ".join(phases)
    return (
        "version: '1.0'\n"
        "workflows:\n"
        "  feature:\n"
        "    name: feature\n"
        f"    phases: [{phases_str}]\n"
        "    default_execution_mode: interactive\n"
        "    description: Feature workflow\n"
    )


class TestLoadWorkflowConfig:
    def test_load_workflow_config_does_not_inject(self, tmp_path: Path) -> None:
        """load_workflow_config() result must NOT contain terminal phase injection."""
        config_dir = tmp_path / ".st3" / "config"
        config_dir.mkdir(parents=True)
        (config_dir / "workflows.yaml").write_text(
            _workflow_yaml(["planning", "implementation"]),
            encoding="utf-8",
        )
        loader = ConfigLoader(config_root=tmp_path)

        result = loader.load_workflow_config()

        assert "ready" not in result.workflows["feature"].phases
