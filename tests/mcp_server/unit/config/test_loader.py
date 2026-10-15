"""Workflow catalogs load from an explicit product basis."""

from pathlib import Path

from mcp_server.config.loader import ConfigLoader


def test_load_workflow_config_catalog_only(tmp_path: Path) -> None:
    basis = tmp_path / "defaults"
    basis.mkdir()
    (basis / "workflows.yaml").write_text(
        "version: '1.0.0'\nworkflows:\n  feature:\n    description: Feature workflow\n",
        encoding="utf-8",
    )
    result = ConfigLoader(tmp_path).load_workflow_config()
    assert result.workflows["feature"].description == "Feature workflow"
    assert result.get_workflow("feature").default_execution_mode == "interactive"
