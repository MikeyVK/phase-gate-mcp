"""
@module: tests.integration.test_config_error_e2e
@layer: Test Infrastructure
@dependencies: pytest, mcp_server.core.exceptions, mcp_server.config
@responsibilities:
  - E2E test for ConfigError scenarios
  - Test loading invalid artifacts.yaml
  - Verify error messages include file path
"""

from pathlib import Path

import pytest

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas import ArtifactRegistryConfig
from mcp_server.core.exceptions import ConfigError


def _load_artifact_registry(config_path: Path) -> ArtifactRegistryConfig:
    # Place config files inside a 'config' subdir so normalize_config_root recognises it
    config_dir = config_path.parent
    return ConfigLoader(config_dir).load_artifact_registry_config(config_path=config_path)


def _make_config_path(tmp_path: Path, filename: str) -> Path:
    """Return a path inside a 'config' subdir so ConfigLoader can resolve it."""
    config_dir = tmp_path / "config"
    config_dir.mkdir(exist_ok=True)
    return config_dir / filename


def test_config_error_for_invalid_yaml(tmp_path: Path) -> None:
    """ConfigError raised for invalid YAML syntax."""
    bad_yaml = _make_config_path(tmp_path, "bad_artifacts.yaml")
    bad_yaml.write_text("version: '1.0.0'\nartifacts: {invalid", encoding="utf-8")

    with pytest.raises(ConfigError) as exc_info:
        _load_artifact_registry(bad_yaml)

    error = exc_info.value
    assert error.code == "ERR_CONFIG"
    assert str(bad_yaml) in error.message or "bad_artifacts.yaml" in error.message
    assert "YAML" in error.message


def test_config_error_for_missing_required_field(tmp_path: Path) -> None:
    """ConfigError raised when artifacts.yaml missing required fields."""
    incomplete_yaml = _make_config_path(tmp_path, "incomplete_artifacts.yaml")
    incomplete_yaml.write_text(
        """version: "1.0.0"
artifact_types:
  - type: doc
    type_id: test
    name: Test
    description: Test artifact
    template_path: null
    fallback_template: null
    name_suffix: null
    file_extension: ".md"
    generate_test: false
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigError) as exc_info:
        _load_artifact_registry(incomplete_yaml)

    error = exc_info.value
    assert error.code == "ERR_CONFIG"
    assert "state_machine" in error.message.lower() or "required" in error.message.lower()


def test_config_error_includes_file_path(tmp_path: Path) -> None:
    """ConfigError message includes file path for debugging."""
    bad_yaml = _make_config_path(tmp_path, "debug_test.yaml")
    bad_yaml.write_text("invalid yaml: [", encoding="utf-8")

    with pytest.raises(ConfigError) as exc_info:
        _load_artifact_registry(bad_yaml)

    error = exc_info.value
    assert error.file_path is not None or "debug_test.yaml" in error.message
