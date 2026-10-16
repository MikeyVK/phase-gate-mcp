"""Workspace layering preserves source admission and explicit configuration intent."""

from pathlib import Path

import pytest

from mcp_server.config.loader import ConfigLoader, normalize_config_root
from mcp_server.core.exceptions import ConfigError
from tests.mcp_server.test_support import get_default_server_root


def _write_yaml(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _basis(root: Path) -> Path:
    return _write_yaml(
        root / "defaults" / "workflows.yaml",
        "version: '1.0.0'\nworkflows:\n  first:\n    description: original\n  second: {}\n",
    )


def test_normalize_config_root_is_explicit(tmp_path: Path) -> None:
    assert normalize_config_root(tmp_path / "config") == (tmp_path / "config").resolve()


def test_layers_add_update_delete_without_rewriting_sources(tmp_path: Path) -> None:
    basis = _basis(tmp_path)
    override = _write_yaml(
        tmp_path / "workflows.yaml",
        "workflows:\n  first:\n    description: changed\n"
        "  second:\n    $delete: true\n  third: {}\n",
    )
    before = (basis.read_bytes(), override.read_bytes())
    config = ConfigLoader(tmp_path).load_workflow_config()
    assert set(config.workflows) == {"first", "third"}
    assert config.workflows["first"].description == "changed"
    assert (basis.read_bytes(), override.read_bytes()) == before


@pytest.mark.parametrize("invalid", ["", "[]", "workflows: {}\nworkflows: {}\n"])
def test_rejects_invalid_present_override(tmp_path: Path, invalid: str) -> None:
    _basis(tmp_path)
    _write_yaml(tmp_path / "workflows.yaml", invalid)
    with pytest.raises(ConfigError):
        ConfigLoader(tmp_path).load_workflow_config()


def test_required_basis_cannot_be_replaced_by_root_file(tmp_path: Path) -> None:
    _write_yaml(tmp_path / "workflows.yaml", "version: '1.0.0'\nworkflows: {}\n")
    with pytest.raises(ConfigError, match="workflows.yaml"):
        ConfigLoader(tmp_path).load_workflow_config()


def test_explicit_complete_file_has_no_companion_lookup(tmp_path: Path) -> None:
    complete = _basis(tmp_path / "separate")
    config = ConfigLoader(tmp_path / "missing").load_workflow_config(config_path=complete)
    assert set(config.workflows) == {"first", "second"}


def test_workspace_override_cannot_repair_invalid_product_basis(tmp_path: Path) -> None:
    basis = _basis(tmp_path)
    basis.write_text("version: '9.0.0'\nworkflows: {}\n", encoding="utf-8")
    _write_yaml(tmp_path / "workflows.yaml", "version: '1.0.0'\n")
    with pytest.raises(ConfigError, match="version"):
        ConfigLoader(tmp_path).load_workflow_config()


def test_optional_enforcement_without_either_source_is_empty(tmp_path: Path) -> None:
    assert ConfigLoader(tmp_path).load_enforcement_config().enforcement == {}


def test_inherits_enforcement_guards_from_complete_product_basis(tmp_path: Path) -> None:
    """Empty workspace differences preserve the complete validated product guards."""
    product_path = (
        Path(__file__).resolve().parents[4]
        / get_default_server_root()
        / "config"
        / "defaults"
        / "enforcement.yaml"
    )
    basis = _write_yaml(
        tmp_path / "defaults" / "enforcement.yaml", product_path.read_text(encoding="utf-8")
    )
    _write_yaml(tmp_path / "enforcement.yaml", "{}\n")
    complete = ConfigLoader(tmp_path).load_enforcement_config(config_path=basis)
    inherited = ConfigLoader(tmp_path).load_enforcement_config()
    assert inherited == complete
    assert any(
        action.type == "check_pr_status"
        for rule in inherited.enforcement.values()
        for action in rule.actions.values()
    )
    basis.write_text("enforcement: [invalid]\n", encoding="utf-8")
    with pytest.raises(ConfigError):
        ConfigLoader(tmp_path).load_enforcement_config()
