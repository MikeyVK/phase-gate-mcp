# tests\mcp_server\integration\test_rollout_configuration.py
# template=integration_test version=c2e61372 created=2026-09-17T15:06Z updated=2026-09-17
"""
Integration tests for rollout_configuration_compatibility.

Verifies prospective V3 rollout configuration compatibility, schema admission,
obsolete configuration rejection, and Pyright setting preservation between
pyproject.toml and pyrightconfig.json without mutating live configurations.

@layer: Tests (Integration)
@dependencies: [pytest, tomllib, ConfigLoader, ConfigValidator, ArtifactLocationsConfig]
@responsibilities:
    - Test end-to-end rollout_configuration_compatibility
    - Verify public target loaders accept prospective configs
    - Verify public target loaders reject obsolete/invalid configs
    - Verify pyproject.toml [tool.pyright] deletion preserves native Pyright settings
"""

# Standard library
import json
import tomllib
from pathlib import Path

# Third-party
import pytest

# Project modules
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.artifact_locations import (
    ArtifactLocationsConfig,
)
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.exceptions import ConfigError


@pytest.fixture
def temp_workspace(tmp_path: Path) -> Path:
    """Create isolated temporary workspace directory for config testing."""
    workspace = tmp_path / "test_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace


class TestRolloutConfiguration:
    """Integration test suite for rollout_configuration_compatibility."""

    def test_artifacts_location_config_validates_prospective_v3(self, temp_workspace: Path) -> None:
        """Verify that ConfigLoader accepts valid prospective V3 artifacts.yaml."""
        config_dir = temp_workspace / ".pgmcp" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        artifacts_file = config_dir / "artifacts.yaml"

        prospective_yaml = (
            'version: "2.0.0"\n'
            "artifacts:\n"
            "  dto:\n"
            '    default_root: "mcp_server/dtos"\n'
            "    additional_roots:\n"
            '      - "mcp_server/models"\n'
            "  worker:\n"
            '    default_root: "mcp_server/workers"\n'
            "  generic_doc:\n"
            '    default_root: "docs/development"\n'
        )
        artifacts_file.write_text(prospective_yaml, encoding="utf-8")

        loader = ConfigLoader(config_dir)
        config = loader.load_artifact_locations_config()

        assert isinstance(config, ArtifactLocationsConfig)
        assert config.version == "2.0.0"
        locations_dict = dict(config.artifacts)
        assert "dto" in locations_dict
        assert locations_dict["dto"].default_root == "mcp_server/dtos"
        assert locations_dict["dto"].additional_roots == ("mcp_server/models",)
        assert locations_dict["worker"].default_root == "mcp_server/workers"
        assert locations_dict["worker"].additional_roots == ()
        assert locations_dict["generic_doc"].default_root == "docs/development"

        # Verify cross-validation against loaded package IDs
        validator = ConfigValidator()
        known_templates = frozenset(["dto", "worker", "generic_doc", "extra_pkg"])
        # Should succeed because all configured keys are in known_templates
        validator.validate_artifact_locations(config, known_templates)

    def test_artifacts_location_config_rejects_obsolete_and_invalid(
        self, temp_workspace: Path
    ) -> None:
        """Verify that ConfigLoader rejects obsolete V1 and invalid configurations."""
        config_dir = temp_workspace / ".pgmcp" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        artifacts_file = config_dir / "artifacts.yaml"

        # 1. Legacy/obsolete V1 schema rejection
        legacy_v1_yaml = "version: 1.0.0\nartifact_types: []\n"
        artifacts_file.write_text(legacy_v1_yaml, encoding="utf-8")

        loader = ConfigLoader(config_dir)
        with pytest.raises(ConfigError) as exc_info:
            loader.load_artifact_locations_config()
        assert "invalid artifact locations configuration" in str(exc_info.value).lower()

        # 2. Duplicate root in single artifact location
        duplicate_root_yaml = (
            'version: "2.0.0"\n'
            "artifacts:\n"
            "  dto:\n"
            '    default_root: "mcp_server/dtos"\n'
            "    additional_roots:\n"
            '      - "mcp_server/dtos"\n'
        )
        artifacts_file.write_text(duplicate_root_yaml, encoding="utf-8")
        with pytest.raises(ConfigError):
            loader.load_artifact_locations_config()

        # 3. Unknown template key during validator coherence check
        valid_yaml = (
            'version: "2.0.0"\nartifacts:\n  stale_template:\n    default_root: "docs/stale"\n'
        )
        artifacts_file.write_text(valid_yaml, encoding="utf-8")
        config = loader.load_artifact_locations_config()
        validator = ConfigValidator()
        with pytest.raises(ConfigError) as exc_info:
            validator.validate_artifact_locations(config, frozenset(["dto", "worker"]))
        assert "artifact_location_template_unknown" in str(exc_info.value)
        assert "stale_template" in str(exc_info.value)

    def test_pyproject_pyright_removal_preserves_pyrightconfig_values(
        self,
    ) -> None:
        """Verify that deleting [tool.pyright] from pyproject.toml preserves native settings."""
        root_dir = Path(__file__).resolve().parents[3]
        pyproject_path = root_dir / "pyproject.toml"
        pyrightconfig_path = root_dir / "pyrightconfig.json"

        assert pyproject_path.exists(), f"pyproject.toml not found at {pyproject_path}"
        assert pyrightconfig_path.exists(), f"pyrightconfig.json not found at {pyrightconfig_path}"

        # 1. Verify pyrightconfig.json contains canonical settings (CY022 authority)
        pyright_config = json.loads(pyrightconfig_path.read_text(encoding="utf-8"))
        assert pyright_config.get("reportFunctionMemberAccess") is False
        assert pyright_config.get("pythonVersion") == "3.11"
        assert pyright_config.get("pythonPlatform") == "Windows"
        assert pyright_config.get("typeCheckingMode") == "strict"
        assert "mcp_server" in pyright_config.get("include", [])

        # 2. Parse live pyproject.toml and extract [tool.pyright]
        pyproject_raw = pyproject_path.read_text(encoding="utf-8")
        parsed_before = tomllib.loads(pyproject_raw)
        assert "tool" in parsed_before
        assert "pyright" in parsed_before["tool"]
        assert parsed_before["tool"]["pyright"].get("reportFunctionMemberAccess") is False

        # 3. Simulate prospective deletion hunk
        pyright_hunk = (
            "[tool.pyright]\n"
            "# Pydantic v2 integration - prevents FieldInfo type inference issues\n"
            "reportFunctionMemberAccess = false\n"
        )
        assert pyright_hunk in pyproject_raw or pyright_hunk.replace("\n", "\r\n") in pyproject_raw

        # Normalize CRLF/LF for replacement
        hunk_to_remove = (
            pyright_hunk if pyright_hunk in pyproject_raw else pyright_hunk.replace("\n", "\r\n")
        )
        prospective_pyproject = pyproject_raw.replace(hunk_to_remove, "")
        parsed_after = tomllib.loads(prospective_pyproject)

        # 4. Assert [tool.pyright] is gone, but all other configurations remain intact
        assert "pyright" not in parsed_after.get("tool", {})
        assert "project" in parsed_after
        assert parsed_after["project"]["name"] == parsed_before["project"]["name"]
        assert parsed_after["tool"]["ruff"] == parsed_before["tool"]["ruff"]
        assert parsed_after["tool"]["coverage"] == parsed_before["tool"]["coverage"]
        assert parsed_after["tool"]["mypy"] == parsed_before["tool"]["mypy"]
        assert parsed_after["tool"]["pytest"] == parsed_before["tool"]["pytest"]

    def test_live_configuration_remains_unmutated_in_cy070(self) -> None:
        """Verify that live repository configuration files remain intact during CY070."""
        root_dir = Path(__file__).resolve().parents[3]
        live_artifacts = root_dir / ".pgmcp" / "config" / "artifacts.yaml"
        live_pyproject = root_dir / "pyproject.toml"

        # Live artifacts.yaml must retain legacy format until CY072 cutover
        artifacts_content = live_artifacts.read_text(encoding="utf-8")
        assert "artifact_types" in artifacts_content

        # Live pyproject.toml must retain [tool.pyright] until CY072 cutover
        pyproject_content = live_pyproject.read_text(encoding="utf-8")
        assert "[tool.pyright]" in pyproject_content
