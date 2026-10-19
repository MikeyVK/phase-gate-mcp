"""Workflow catalogs load from an explicit product basis."""

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from mcp_server.config.loader import ConfigLoader
from mcp_server.core.exceptions import ConfigError
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject


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


def _server_basis(root: Path, **changes: object) -> Path:
    """Write raw owner input for the public configuration boundary."""
    data: dict[str, object] = {
        "version": "1.0.0",
        "startup_lock": {"max_wait_seconds": 30, "retry_interval_seconds": 0.25},
        "proxy": {"initialization_timeout_seconds": 60},
    }
    data.update(changes)
    basis = root / "defaults" / "server.yaml"
    basis.parent.mkdir(parents=True, exist_ok=True)
    basis.write_text(yaml.safe_dump(data), encoding="utf-8")
    return basis


def test_server_policy_composes_without_template_reads(tmp_path: Path) -> None:
    _server_basis(tmp_path)
    (tmp_path / "server.yaml").write_text(
        "startup_lock:\n  max_wait_seconds: 40\n", encoding="utf-8"
    )

    def unrelated_reader(_path: Path) -> FrozenJsonObject:
        pytest.fail("Server policy must not read templates")

    result = ConfigLoader(tmp_path, context_schema_reader=unrelated_reader).load_server_config()
    assert result.startup_lock.max_wait_seconds == 40
    assert result.startup_lock.retry_interval_seconds == 0.25
    assert result.proxy.initialization_timeout_seconds == 60
    with pytest.raises(ValidationError):
        result.startup_lock.max_wait_seconds = 50


@pytest.mark.parametrize(
    "changes",
    [
        {"startup_lock": {"max_wait_seconds": 0, "retry_interval_seconds": 0.25}},
        {"startup_lock": {"max_wait_seconds": True, "retry_interval_seconds": 0.25}},
        {"startup_lock": {"max_wait_seconds": "30", "retry_interval_seconds": 0.25}},
        {"proxy": {"initialization_timeout_seconds": float("inf")}},
        {"startup_lock": {"max_wait_seconds": 1, "retry_interval_seconds": 2}},
        {"proxy": {"initialization_timeout_seconds": 30}},
    ],
)
def test_server_policy_rejects_invalid_budgets(tmp_path: Path, changes: dict[str, object]) -> None:
    _server_basis(tmp_path, **changes)
    with pytest.raises(ConfigError):
        ConfigLoader(tmp_path).load_server_config()


def test_server_policy_requires_product_basis(tmp_path: Path) -> None:
    basis = _server_basis(tmp_path)
    basis.replace(tmp_path / "server.yaml")
    with pytest.raises(ConfigError) as caught:
        ConfigLoader(tmp_path).load_server_config()
    assert caught.value.file_path == str(basis.resolve())
