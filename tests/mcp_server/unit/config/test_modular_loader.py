# tests\mcp_server\unit\config\test_modular_loader.py
# template=unit_test version=3d15d309 created=2026-07-15T21:32Z updated=
"""
Unit tests for mcp_server.config.loader.

Verify loading and merging of modular artifact config files from the artifacts/ subdirectory.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.config.loader]
@responsibilities:
    - Test TestModularLoader functionality
    - Verify None
    - None
"""

# Standard library
from typing import Any

# Third-party
import pytest
from pathlib import Path
from pydantic import ValidationError

# Project modules
from mcp_server.config.loader import ConfigLoader, ArtifactRegistryConfig


class TestModularLoader:
    """Test suite for loader."""

    def test_loader_scans_artifacts_dir_and_merges(self, tmp_path: Path) -> None:
        """Test that loader scans artifacts/ dir and merges definitions."""
        # Arrange
        config_root = tmp_path / "config"
        index_file = config_root / "artifacts.yaml"
        index_file.parent.mkdir(parents=True, exist_ok=True)
        index_file.write_text("version: '1.0.0'\nartifact_types: []\n", encoding="utf-8")

        # Create artifacts/ directory
        artifacts_dir = config_root / "artifacts"
        artifacts_dir.mkdir(parents=True)

        # Create two modular YAML files
        (artifacts_dir / "dto.yaml").write_text("type: code\ntype_id: dto\nname: DTO\ndescription: DTO desc\nfile_extension: .py\nstate_machine:\n  states: [CREATED]\n  initial_state: CREATED\n  valid_transitions: []\n", encoding="utf-8")
        (artifacts_dir / "worker.yaml").write_text("type: code\ntype_id: worker\nname: Worker\ndescription: Worker desc\nfile_extension: .py\nstate_machine:\n  states: [CREATED]\n  initial_state: CREATED\n  valid_transitions: []\n", encoding="utf-8")

        loader = ConfigLoader(config_root)

        # Act
        config = loader.load_artifact_registry_config()

        # Assert
        assert config.version == "1.0.0"
        assert len(config.artifact_types) == 2
        type_ids = [a.type_id for a in config.artifact_types]
        assert "dto" in type_ids
        assert "worker" in type_ids

    def test_loader_fails_fast_on_invalid_yaml_in_modular_file(self, tmp_path: Path) -> None:
        """Test that loader fails fast when a modular file has invalid YAML syntax."""
        # Arrange
        config_root = tmp_path / "config"
        index_file = config_root / "artifacts.yaml"
        index_file.parent.mkdir(parents=True, exist_ok=True)
        index_file.write_text("version: '1.0.0'\nartifact_types: []\n", encoding="utf-8")

        # Create artifacts/ directory with bad YAML
        artifacts_dir = config_root / "artifacts"
        artifacts_dir.mkdir(parents=True)
        (artifacts_dir / "bad.yaml").write_text("invalid: yaml: syntax: [}", encoding="utf-8")

        loader = ConfigLoader(config_root)

        # Act & Assert
        with pytest.raises(ConfigError) as exc_info:
            loader.load_artifact_registry_config()
        assert "Invalid YAML syntax" in str(exc_info.value)

    def test_loader_clean_break_fails_without_modular_artifacts(self, tmp_path: Path) -> None:
        """Test that under Clean Break, loading fails if registry is empty."""
        # Arrange
        config_root = tmp_path / "config"
        index_file = config_root / "artifacts.yaml"
        index_file.parent.mkdir(parents=True, exist_ok=True)
        index_file.write_text("version: '1.0.0'\nartifact_types: []\n", encoding="utf-8")

        loader = ConfigLoader(config_root)

        # Act & Assert
        with pytest.raises(ConfigError) as exc_info:
            loader.load_artifact_registry_config()
        assert "Empty" in str(exc_info.value) or "no artifact types defined" in str(exc_info.value)
