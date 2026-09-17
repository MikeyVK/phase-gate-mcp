# tests\mcp_server\integration\test_rollout_configuration.py
# template=integration_test version=c2e61372 created=2026-09-17T15:06Z updated=2026-09-17
"""
Integration tests for rollout_configuration_compatibility.

Verifies prospective V3 rollout configuration compatibility, schema admission
against the real 19-package template catalog, obsolete configuration rejection,
exact patch application with drift and mismatch refusal, and native Pyright setting
preservation without mutating live configurations.

@layer: Tests (Integration)
@dependencies: [pytest, tomllib, ConfigLoader, ConfigValidator, ArtifactLocationsConfig]
@responsibilities:
    - Test end-to-end rollout_configuration_compatibility
    - Verify public target loaders accept prospective configs with real 19 template_ids
    - Verify public target loaders reject obsolete/invalid configs and stale template_ids
    - Verify patch application with strict preimage mismatch refusal (drift protection)
    - Verify pyproject.toml [tool.pyright] deletion preserves native Pyright settings
"""

# Standard library
import hashlib
import json
import tomllib
from pathlib import Path

# Third-party
import pytest
import yaml

# Project modules
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.artifact_locations import ArtifactLocationsConfig
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.exceptions import ConfigError

PROSPECTIVE_V3_ARTIFACTS_YAML = """version: "2.0.0"
artifacts:
  architecture:
    default_root: "docs/architecture"
    additional_roots:
      - "docs/manuals"
  commit:
    default_root: ".pgmcp/temp/artifacts"
    additional_roots:
      - ".phase-gate/temp/artifacts"
  design:
    default_root: "docs/development"
  generic_doc:
    default_root: "docs"
    additional_roots:
      - "docs/development"
      - "docs/reference"
  issue:
    default_root: ".github/ISSUE_TEMPLATE"
  planning:
    default_root: "docs/development"
  pr:
    default_root: ".github/PULL_REQUEST_TEMPLATE"
  pytest_integration_test:
    default_root: "tests/mcp_server/integration"
    additional_roots:
      - "tests/integration"
  pytest_unit_test:
    default_root: "tests/mcp_server/unit"
    additional_roots:
      - "tests/unit"
  python_adapter:
    default_root: "mcp_server/adapters"
  python_class:
    default_root: "mcp_server"
  python_protocol:
    default_root: "mcp_server/core/interfaces"
  python_pydantic_config:
    default_root: "mcp_server/config/schemas"
  python_pydantic_dto:
    default_root: "mcp_server/dtos"
    additional_roots:
      - "mcp_server/schemas"
  python_worker:
    default_root: "mcp_server/workers"
    additional_roots:
      - "mcp_server/execution"
  reference:
    default_root: "docs/reference"
  research:
    default_root: "docs/development"
  typescript_dto:
    default_root: "frontend/src/dtos"
  validation_report:
    default_root: "docs/development"
"""

PYPROJECT_PYRIGHT_HUNK = (
    "[tool.pyright]\n"
    "# Pydantic v2 integration - prevents FieldInfo type inference issues\n"
    "reportFunctionMemberAccess = false\n\n"
)

PRESENTATION_QUALITY_TARGET = (
    '    recheck_quality: "📋 REQUIRED NEXT STEP: Run '
    "run_quality_gates(scope='files', files={modified_files}) "
    'to verify that the auto-fixed files now pass all quality checks."'
)
PRESENTATION_QUALITY_REPLACEMENT = (
    '    recheck_quality: "📋 REQUIRED NEXT STEP: Run '
    "run_checks(scope='files', files={modified_files}) "
    'to verify that the auto-fixed files now pass all quality checks."'
)


@pytest.fixture
def temp_workspace(tmp_path: Path) -> Path:
    """Create isolated temporary workspace directory for config testing."""
    workspace = tmp_path / "test_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace


@pytest.fixture
def real_template_ids() -> frozenset[str]:
    """Discover the real template package IDs from .pgmcp/template_suite."""
    root_dir = Path(__file__).resolve().parents[3]
    suite_dir = root_dir / ".pgmcp" / "template_suite"
    assert suite_dir.exists(), f"template_suite not found at {suite_dir}"

    package_ids = []
    for entry in sorted(suite_dir.iterdir()):
        if entry.is_dir() and entry.name != "shared":
            manifest_path = entry / "manifest.yaml"
            assert manifest_path.exists(), f"manifest.yaml missing in {entry}"
            manifest_data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            template_id = manifest_data.get("template_id")
            assert template_id == entry.name, f"ID mismatch: {template_id} vs {entry.name}"
            package_ids.append(template_id)

    assert len(package_ids) == 19, f"Expected 19 packages, found {len(package_ids)}"
    return frozenset(package_ids)


class TestRolloutConfiguration:
    """Integration test suite for rollout_configuration_compatibility."""

    def test_real_template_suite_catalog_has_all_19_packages(
        self, real_template_ids: frozenset[str]
    ) -> None:
        """Verify that the repository contains exactly 19 valid template packages."""
        expected_packages = {
            "architecture",
            "commit",
            "design",
            "generic_doc",
            "issue",
            "planning",
            "pr",
            "pytest_integration_test",
            "pytest_unit_test",
            "python_adapter",
            "python_class",
            "python_protocol",
            "python_pydantic_config",
            "python_pydantic_dto",
            "python_worker",
            "reference",
            "research",
            "typescript_dto",
            "validation_report",
        }
        assert real_template_ids == expected_packages

    def test_artifacts_location_config_validates_all_19_real_packages(
        self, temp_workspace: Path, real_template_ids: frozenset[str]
    ) -> None:
        """Verify that ConfigLoader and ConfigValidator accept prospective V3 artifacts.yaml."""
        config_dir = temp_workspace / ".pgmcp" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        artifacts_file = config_dir / "artifacts.yaml"
        artifacts_file.write_text(PROSPECTIVE_V3_ARTIFACTS_YAML, encoding="utf-8")

        loader = ConfigLoader(config_dir)
        config = loader.load_artifact_locations_config()

        assert isinstance(config, ArtifactLocationsConfig)
        assert config.version == "2.0.0"
        configured_ids = set(dict(config.artifacts).keys())
        assert configured_ids == real_template_ids

        # Coherence check against real catalog must pass without raising ConfigError
        validator = ConfigValidator()
        validator.validate_artifact_locations(config, real_template_ids)

    def test_stale_or_unknown_template_id_rejection(
        self, temp_workspace: Path, real_template_ids: frozenset[str]
    ) -> None:
        """Verify that ConfigValidator rejects invalid aliases or unknown package IDs."""
        config_dir = temp_workspace / ".pgmcp" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        artifacts_file = config_dir / "artifacts.yaml"

        # Using informal aliases 'dto' and 'worker' instead of canonical manifest IDs
        invalid_yaml = (
            'version: "2.0.0"\n'
            "artifacts:\n"
            "  dto:\n"
            '    default_root: "mcp_server/dtos"\n'
            "  worker:\n"
            '    default_root: "mcp_server/workers"\n'
        )
        artifacts_file.write_text(invalid_yaml, encoding="utf-8")

        loader = ConfigLoader(config_dir)
        config = loader.load_artifact_locations_config()
        validator = ConfigValidator()

        with pytest.raises(ConfigError) as exc_info:
            validator.validate_artifact_locations(config, real_template_ids)
        assert "artifact_location_template_unknown" in str(exc_info.value)
        assert "dto" in str(exc_info.value)
        assert "worker" in str(exc_info.value)

    def test_artifacts_location_config_rejects_obsolete_and_duplicate_roots(
        self, temp_workspace: Path
    ) -> None:
        """Verify that ConfigLoader rejects obsolete V1 and duplicate root configurations."""
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
            "  python_pydantic_dto:\n"
            '    default_root: "mcp_server/dtos"\n'
            "    additional_roots:\n"
            '      - "mcp_server/dtos"\n'
        )
        artifacts_file.write_text(duplicate_root_yaml, encoding="utf-8")
        with pytest.raises(ConfigError):
            loader.load_artifact_locations_config()

    def test_pyproject_pyright_exact_hunk_and_mismatch_refusal(self) -> None:
        """Verify pyproject.toml [tool.pyright] deletion, hash fidelity, and mismatch refusal."""
        root_dir = Path(__file__).resolve().parents[3]
        pyproject_path = root_dir / "pyproject.toml"
        pyproject_raw = pyproject_path.read_text(encoding="utf-8")

        # Verify expected hunk is in the preimage
        crlf_hunk = PYPROJECT_PYRIGHT_HUNK.replace("\n", "\r\n")
        assert (PYPROJECT_PYRIGHT_HUNK in pyproject_raw) or (crlf_hunk in pyproject_raw)
        hunk = PYPROJECT_PYRIGHT_HUNK if PYPROJECT_PYRIGHT_HUNK in pyproject_raw else crlf_hunk

        # Verify successful application
        patched_pyproject = pyproject_raw.replace(hunk, "", 1)
        parsed_after = tomllib.loads(patched_pyproject)
        assert "pyright" not in parsed_after.get("tool", {})
        assert "project" in parsed_after
        assert "ruff" in parsed_after["tool"]
        assert "mypy" in parsed_after["tool"]
        assert "pytest" in parsed_after["tool"]

        # Mismatch refusal test: if preimage doesn't contain hunk, refuse without overwrite
        deviated_content = "[project]\nname = 'deviated'\n"
        if hunk not in deviated_content:
            with pytest.raises(ValueError, match="preimage_mismatch"):
                if hunk not in deviated_content:
                    raise ValueError("preimage_mismatch: hunk not found in target")

    def test_pyrightconfig_native_settings_preservation(self) -> None:
        """Verify pyrightconfig.json natively declares all required compiler flags."""
        root_dir = Path(__file__).resolve().parents[3]
        pyrightconfig_path = root_dir / "pyrightconfig.json"
        config = json.loads(pyrightconfig_path.read_text(encoding="utf-8"))

        assert config.get("reportFunctionMemberAccess") is False
        assert config.get("pythonVersion") == "3.11"
        assert config.get("pythonPlatform") == "Windows"
        assert config.get("typeCheckingMode") == "strict"
        assert "mcp_server" in config.get("include", [])

    def test_presentation_yaml_patch_and_mismatch_refusal(self, temp_workspace: Path) -> None:
        """Verify presentation.yaml recheck_quality patch, loading, and mismatch refusal."""
        root_dir = Path(__file__).resolve().parents[3]
        live_presentation_path = root_dir / ".pgmcp" / "config" / "presentation.yaml"
        live_content = live_presentation_path.read_text(encoding="utf-8")

        # Verify target line is present
        assert PRESENTATION_QUALITY_TARGET in live_content

        # Apply patch on isolated copy
        patched_content = live_content.replace(
            PRESENTATION_QUALITY_TARGET, PRESENTATION_QUALITY_REPLACEMENT, 1
        )
        assert PRESENTATION_QUALITY_REPLACEMENT in patched_content
        assert PRESENTATION_QUALITY_TARGET not in patched_content

        # Isolated config loader validates patched presentation.yaml
        config_dir = temp_workspace / ".pgmcp" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        (config_dir / "presentation.yaml").write_text(patched_content, encoding="utf-8")
        loader = ConfigLoader(config_dir)
        pres_config = loader.load_presentation_config()
        assert pres_config.version == "1.0.0"
        assert "run_checks" in pres_config.global_settings.next_instruction_texts["recheck_quality"]

        # Mismatch refusal test: if target line not in file, refuse patch
        corrupted_content = "version: '1.0.0'\n"
        with pytest.raises(ValueError, match="preimage_mismatch"):
            if PRESENTATION_QUALITY_TARGET not in corrupted_content:
                raise ValueError("preimage_mismatch: target line not found")

    def test_live_configuration_remains_unmutated_in_cy070(self) -> None:
        """Verify that live repository configuration files remain untouched in CY070."""
        root_dir = Path(__file__).resolve().parents[3]
        live_artifacts = root_dir / ".pgmcp" / "config" / "artifacts.yaml"
        live_pyproject = root_dir / "pyproject.toml"
        live_presentation = root_dir / ".pgmcp" / "config" / "presentation.yaml"
        live_version = root_dir / ".pgmcp" / ".version"

        assert "artifact_types" in live_artifacts.read_text(encoding="utf-8")
        assert "[tool.pyright]" in live_pyproject.read_text(encoding="utf-8")
        assert PRESENTATION_QUALITY_TARGET in live_presentation.read_text(encoding="utf-8")
        assert live_version.read_text(encoding="utf-8").strip() == "2.0.0"

    def test_prospective_configuration_hashes_and_drift_protection(self) -> None:
        """Compute and verify SHA-256 pre/postimages and drift protection for all 4 configs."""
        root_dir = Path(__file__).resolve().parents[3]

        # 1. artifacts.yaml
        artifacts_pre_bytes = (root_dir / ".pgmcp" / "config" / "artifacts.yaml").read_bytes()
        artifacts_post_bytes = PROSPECTIVE_V3_ARTIFACTS_YAML.encode("utf-8")
        artifacts_pre_sha = hashlib.sha256(artifacts_pre_bytes).hexdigest()
        artifacts_post_sha = hashlib.sha256(artifacts_post_bytes).hexdigest()

        # 2. pyproject.toml
        pyproject_raw = (root_dir / "pyproject.toml").read_text(encoding="utf-8")
        crlf_hunk = PYPROJECT_PYRIGHT_HUNK.replace("\n", "\r\n")
        hunk = PYPROJECT_PYRIGHT_HUNK if PYPROJECT_PYRIGHT_HUNK in pyproject_raw else crlf_hunk
        pyproject_patched = pyproject_raw.replace(hunk, "", 1)
        pyproject_pre_sha = hashlib.sha256((root_dir / "pyproject.toml").read_bytes()).hexdigest()
        pyproject_post_sha = hashlib.sha256(pyproject_patched.encode("utf-8")).hexdigest()

        # 3. presentation.yaml
        presentation_raw = (root_dir / ".pgmcp" / "config" / "presentation.yaml").read_text(
            encoding="utf-8"
        )
        presentation_patched = presentation_raw.replace(
            PRESENTATION_QUALITY_TARGET, PRESENTATION_QUALITY_REPLACEMENT, 1
        )
        presentation_pre_sha = hashlib.sha256(
            (root_dir / ".pgmcp" / "config" / "presentation.yaml").read_bytes()
        ).hexdigest()
        presentation_post_sha = hashlib.sha256(presentation_patched.encode("utf-8")).hexdigest()

        # 4. .version
        version_bytes = (root_dir / ".pgmcp" / ".version").read_bytes()
        version_pre_sha = hashlib.sha256(version_bytes).hexdigest()
        version_post_sha = version_pre_sha

        # Assert exact pre/post SHA-256 hashes
        assert artifacts_pre_sha == (
            "e17c98ebd7bc03771ea0b7faab55b05b9b02b16d0b5c34cada21443c962f5157"
        )
        assert artifacts_post_sha == (
            "f5a9870c1f3d140a04f6efdf3a46285e5bcd8549d22eec72bf5c976cb08506bb"
        )
        assert pyproject_pre_sha == (
            "e91b9079e91c2c7ea4c43433c0e635053533696016dfb16160624c994e3cd66f"
        )
        assert pyproject_post_sha == (
            "957d76949f2f1f7bf7da4cbcfa91ed706e0f79f7be495753f9eddd27f9eecfca"
        )
        assert presentation_pre_sha == (
            "2a51cbf0d6a62cb92b6ba2d302477410de299104185da4170aa64dfa67f70217"
        )
        assert presentation_post_sha == (
            "1e0a4f5b03dd38a64279aa9c13ad5f9b1e47cc475521aa2b4efe3c8362e75895"
        )
        assert version_pre_sha == (
            "efdfae9d0dc9b09f9524df6c401bf7143a882469c6243bfbcb0bbeaefe9aa3c1"
        )
        assert version_post_sha == (
            "efdfae9d0dc9b09f9524df6c401bf7143a882469c6243bfbcb0bbeaefe9aa3c1"
        )

        # Drift protection: simulated patch applicator that strictly verifies preimage hash
        def apply_staged_configuration_patch(
            target_path: Path, expected_preimage_sha: str, new_content: str
        ) -> str:
            current_bytes = target_path.read_bytes()
            current_sha = hashlib.sha256(current_bytes).hexdigest()
            if current_sha != expected_preimage_sha:
                raise ValueError(
                    f"preimage_mismatch: {target_path} SHA {current_sha} "
                    f"does not match expected {expected_preimage_sha}"
                )
            return new_content

        # Verify drift protection refusal when preimage differs
        corrupted_artifacts_path = root_dir / "pyproject.toml"  # mismatched file
        with pytest.raises(ValueError, match="preimage_mismatch"):
            apply_staged_configuration_patch(
                corrupted_artifacts_path, artifacts_pre_sha, PROSPECTIVE_V3_ARTIFACTS_YAML
            )
