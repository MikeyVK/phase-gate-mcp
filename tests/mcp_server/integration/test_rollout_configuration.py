# tests\mcp_server\integration\test_rollout_configuration.py
# template=integration_test version=c2e61372 created=2026-09-17T15:06Z updated=2026-09-17
"""
Integration tests for rollout_configuration_compatibility.

Verifies prospective V3 rollout configuration compatibility, schema admission
against the real 19-package template catalog reconciled with project_structure.yaml,
obsolete configuration rejection, atomic compare-before-write replacement via
CheckedFileWriter with race-condition drift refusal, clean-break presentation alignment,
and native Pyright setting preservation without mutating live configurations.

@layer: Tests (Integration)
@dependencies: [pytest, tomllib, ConfigLoader, ConfigValidator, ArtifactLocationsConfig]
@responsibilities:
    - Test end-to-end rollout_configuration_compatibility
    - Verify public target loaders accept prospective configs with real 19 template_ids
    - Reconcile placement roots against owner's project_structure.yaml and design contracts
    - Verify CheckedFileWriter.replace_if_unchanged atomic replacement and drift refusal
    - Verify presentation.yaml clean break: no legacy quality gates/autofix, full V3 surface
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
from mcp_server.bootstrap import SupportedToolContract
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.artifact_locations import ArtifactLocationsConfig
from mcp_server.config.schemas.presentation_config import PresentationConfig
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.exceptions import ConfigError
from mcp_server.execution.models import ApplyFixesOutput, RunTestsOutput
from mcp_server.presenters.text_presenter import TextPresenter, validate_presentation_alignment
from mcp_server.schemas.execution_outputs import RunChecksOutput
from mcp_server.utils.atomic_file_writer import CheckedFileWriter, OriginalChangedError

# Authoritative prospective V3 artifacts.yaml reconciled with project_structure.yaml
PROSPECTIVE_V3_ARTIFACTS_YAML = """version: "2.0.0"
artifacts:
  architecture:
    default_root: "docs/architecture"
    additional_roots:
      - "docs/reference"
      - "docs/manuals"
  commit:
    default_root: ".pgmcp/temp/artifacts"
  design:
    default_root: "docs/development"
    additional_roots:
      - "docs"
  generic_doc:
    default_root: "docs"
    additional_roots:
      - "docs/development"
      - "docs/reference"
      - "docs/manuals"
  issue:
    default_root: ".github/ISSUE_TEMPLATE"
  planning:
    default_root: "docs/development"
    additional_roots:
      - "docs"
  pr:
    default_root: ".github/PULL_REQUEST_TEMPLATE"
  pytest_integration_test:
    default_root: "tests/mcp_server/integration"
    additional_roots:
      - "tests/integration"
  pytest_unit_test:
    default_root: "tests/mcp_server/unit"
    additional_roots:
      - "tests/backend"
      - "tests/unit"
  python_adapter:
    default_root: "mcp_server/adapters"
    additional_roots:
      - "backend/adapters"
  python_class:
    default_root: "mcp_server"
    additional_roots:
      - "backend"
  python_protocol:
    default_root: "mcp_server/core/interfaces"
    additional_roots:
      - "backend/interfaces"
  python_pydantic_config:
    default_root: "mcp_server/config/schemas"
    additional_roots:
      - "mcp_server/schemas"
  python_pydantic_dto:
    default_root: "mcp_server/dtos"
    additional_roots:
      - "backend/dtos"
      - "mcp_server/schemas"
  python_worker:
    default_root: "mcp_server/workers"
    additional_roots:
      - "backend/workers"
      - "mcp_server/execution"
  reference:
    default_root: "docs/reference"
    additional_roots:
      - "docs/architecture"
      - "docs/manuals"
      - "docs/coding_standards"
  research:
    default_root: "docs/development"
    additional_roots:
      - "docs"
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

# Presentation prospective patch targets and replacements
PRESENTATION_RECHECK_TARGET = (
    '    recheck_quality: "📋 REQUIRED NEXT STEP: Run '
    "run_quality_gates(scope='files', files={modified_files}) "
    'to verify that the auto-fixed files now pass all quality checks."'
)
PRESENTATION_RECHECK_REPLACEMENT = (
    '    recheck_quality: "📋 REQUIRED NEXT STEP: Run '
    "run_checks(scope='targets', targets={modified_files}) "
    'to verify that the applied fixes now pass all checks."'
)

PRESENTATION_SUGGESTION_TARGET = (
    '        quality_gates_failed_verbose_suggestion: "Some quality gates failed. '
    "Rerun the tool with verbose=True to retrieve complete linter/checker tracebacks. "
    'Suggested command: run_quality_gates({scope_part}, verbose=True)"'
)
PRESENTATION_SUGGESTION_REPLACEMENT = (
    '        checks_failed_verbose_suggestion: "Some checks failed. '
    "Rerun the tool with verbose=True to retrieve complete tracebacks. "
    'Suggested command: run_checks(scope={scope_part}, verbose=True)"'
)

PRESENTATION_AUTOFIX_TARGET = """  auto_fix:
    category: mutation
    max_items: 20
    template_success: |
      **Auto-Fix Run Completed Successfully**
      - Gates executed: {gates_executed_count}
      - Files modified: {modified_files_count}
    template_failure: |
      **Auto-Fix Run Failed**
      - Error: {error_message}
      - Gates executed: {gates_executed_count}
      - Files modified: {modified_files_count}
    collections:
      - field: gates_executed
        heading: "Gates executed:"
        item_template: "- {item}"
      - field: modified_files
        heading: "Files modified:"
        item_template: "- {item}"
"""

PRESENTATION_APPLYFIXES_REPLACEMENT = """  apply_fixes:
    category: mutation
    max_items: 5
    template_success: "{requested_scope}"
    template_failure: "{requested_scope}: {error_code}"
    collections:
      - field: results
        heading: "Fixes"
        item_template: "{fix_id}: {status}; args_source={args_source}"
    enum_cases:
      - field: error_code
        cases:
          no_configured_fixes: "No fix bindings configured."
          selection_invalid: "Fix selection invalid."
          scope_resolution_failed: "Fix scope could not be resolved."
          adapter_request_rejected: "Internal fix request rejected."
          operation_interrupted: "Fix operation interrupted."
          termination_unconfirmed: "Fix termination unconfirmed."
"""

PRESENTATION_QUALITY_AND_TESTS_TARGET = (
    "  run_quality_gates:\n"
    "    category: quality\n"
    "    max_items: 10\n"
    "    template_success: |\n"
    "      Quality gate execution completed.\n"
    "      - Scope: {scope}\n"
    "      - File count: {file_count}\n"
    "      - Overall pass: {overall_pass}\n"
    "    template_failure: |\n"
    "      Quality gate execution completed.\n"
    "      - Scope: {scope}\n"
    "      - File count: {file_count}\n"
    "      - Overall pass: {overall_pass}\n"
    "    collections:\n"
    "      - field: gates\n"
    '        heading: "Gate results:"\n'
    '        item_template: "- {name}: status={status}, passed={passed}, score={score}"\n'
    "        children:\n"
    "          - field: findings\n"
    '            heading: "  Findings:"\n'
    '            item_template: "  - {file}:{line}:{column} [{code}] {message} '
    '(severity={severity}, fixable={fixable})"\n'
    "  run_tests:\n"
    "    category: testing\n"
    "    max_items: 5\n"
    "    template_success: |\n"
    "      Tests completed (exit {exit_code}).\n"
    "      - Passed: {passed_count}\n"
    "      - Failed: {failed_count}\n"
    "      - Skipped: {skipped_count}\n"
    "      - Errors: {errors_count}\n"
    "      - Duration: {duration_seconds}s\n"
    "      - Coverage: {coverage_pct}%\n"
    "    template_failure: |\n"
    "      Tests completed (exit {exit_code}): {error_message}\n"
    "      - Passed: {passed_count}\n"
    "      - Failed: {failed_count}\n"
    "      - Skipped: {skipped_count}\n"
    "      - Errors: {errors_count}\n"
    "      - Duration: {duration_seconds}s\n"
    "      - Coverage: {coverage_pct}%\n"
    "    collections:\n"
    "      - field: failures\n"
    '        heading: "Failures:"\n'
    '        item_template: "- {test_id} ({location}): {short_reason} '
    '[collection error: {is_collection_error}]"\n'
)

PRESENTATION_CHECKS_AND_TESTS_REPLACEMENT = """  run_checks:
    category: quality
    max_items: 5
    template_success: "{requested_scope}: {run_status}; profile={selected_profile}"
    template_failure: "{requested_scope}: {run_status}; error={error_code}"
    collections:
      - field: results
        heading: "Checks"
        item_template: "{check_id}: {status}; args_source={args_source}"
    enum_cases:
      - field: error_code
        cases:
          no_configured_checks: "No checks are configured."
          default_profile_missing: "No default check profile is configured."
          selection_invalid: "The check selection is invalid."
          branch_basis_unavailable: "The branch comparison basis is unavailable."
          scope_resolution_failed: "The requested scope could not be resolved."
          adapter_request_rejected: "An adapter rejected the check request."
          operation_interrupted: "The operation was interrupted."
          termination_unconfirmed: "Process termination was not confirmed."
  run_tests:
    category: testing
    max_items: 5
    template_success: "{requested_scope}"
    template_failure: "{requested_scope}: {error_code}"
    collections:
      - field: results
        heading: "Tests"
        item_template: "{test_id}: {status}; args_source={args_source}"
    enum_cases:
      - field: error_code
        cases:
          no_configured_tests: "No test bindings configured."
          no_active_tests: "No active test bindings."
          selection_invalid: "Test selection invalid."
          scope_resolution_failed: "Test scope could not be resolved."
          adapter_request_rejected: "Internal test request rejected."
          operation_interrupted: "Test operation interrupted."
          termination_unconfirmed: "Test termination unconfirmed."
"""


def apply_checked_replacement(
    target_path: Path,
    expected_preimage_sha: str,
    new_content: str,
    expected_postimage_sha: str,
) -> None:
    """Atomic compare-before-write replacement via the production CheckedFileWriter boundary.

    1. Reads original snapshot bytes from target_path.
    2. Validates original bytes against expected_preimage_sha.
    3. Validates new_content bytes against expected_postimage_sha.
    4. Delegates atomic replace to CheckedFileWriter().replace_if_unchanged().
       The CheckedFileWriter boundary re-verifies target file content immediately prior
       to os.replace, raising OriginalChangedError if concurrent modification occurred.
    """
    if not target_path.exists():
        raise FileNotFoundError(f"target file not found: {target_path}")
    snapshot_bytes = target_path.read_bytes()
    snapshot_sha = hashlib.sha256(snapshot_bytes).hexdigest()
    if snapshot_sha != expected_preimage_sha:
        raise ValueError(
            f"preimage_mismatch: {target_path} SHA {snapshot_sha} "
            f"does not match expected {expected_preimage_sha}"
        )

    new_bytes = new_content.encode("utf-8")
    new_sha = hashlib.sha256(new_bytes).hexdigest()
    if new_sha != expected_postimage_sha:
        raise ValueError(
            f"postimage_mismatch: generated SHA {new_sha} "
            f"does not match expected {expected_postimage_sha}"
        )

    replacer = CheckedFileWriter()
    replacer.replace_if_unchanged(target_path, snapshot_bytes, new_content)


def build_prospective_presentation_yaml(live_content: str) -> str:
    """Apply the full clean-break V3 prospective patch to presentation.yaml."""
    content = live_content

    # 1. Update recheck_quality instruction
    assert PRESENTATION_RECHECK_TARGET in content
    content = content.replace(PRESENTATION_RECHECK_TARGET, PRESENTATION_RECHECK_REPLACEMENT, 1)

    # 2. Update suggestion instruction
    assert PRESENTATION_SUGGESTION_TARGET in content
    content = content.replace(
        PRESENTATION_SUGGESTION_TARGET, PRESENTATION_SUGGESTION_REPLACEMENT, 1
    )

    # 3. Replace auto_fix with apply_fixes
    auto_fix_target = PRESENTATION_AUTOFIX_TARGET
    if auto_fix_target not in content:
        auto_fix_target = auto_fix_target.replace("\n", "\r\n")
    assert auto_fix_target in content
    content = content.replace(auto_fix_target, PRESENTATION_APPLYFIXES_REPLACEMENT, 1)

    # 4. Replace run_quality_gates + V2 run_tests with run_checks + V3 run_tests
    quality_tests_target = PRESENTATION_QUALITY_AND_TESTS_TARGET
    if quality_tests_target not in content:
        quality_tests_target = quality_tests_target.replace("\n", "\r\n")
    assert quality_tests_target in content
    return content.replace(quality_tests_target, PRESENTATION_CHECKS_AND_TESTS_REPLACEMENT, 1)


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

    def test_artifacts_location_config_validates_prospective_v3(
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

    def test_artifacts_checked_replacement_and_drift_protection(self, temp_workspace: Path) -> None:
        """Test CheckedFileWriter replacement, hash assertion, and race drift refusal."""
        root_dir = Path(__file__).resolve().parents[3]
        live_file = root_dir / ".pgmcp" / "config" / "artifacts.yaml"
        isolated_target = temp_workspace / ".pgmcp" / "config" / "artifacts.yaml"
        isolated_target.parent.mkdir(parents=True, exist_ok=True)
        isolated_target.write_bytes(live_file.read_bytes())

        pre_sha = hashlib.sha256(live_file.read_bytes()).hexdigest()
        post_sha = hashlib.sha256(PROSPECTIVE_V3_ARTIFACTS_YAML.encode("utf-8")).hexdigest()

        # Success path on isolated copy using CheckedFileWriter boundary
        apply_checked_replacement(isolated_target, pre_sha, PROSPECTIVE_V3_ARTIFACTS_YAML, post_sha)
        assert isolated_target.read_bytes() == PROSPECTIVE_V3_ARTIFACTS_YAML.encode("utf-8")
        assert hashlib.sha256(isolated_target.read_bytes()).hexdigest() == post_sha

        # Drift protection: simulate concurrent race between snapshot and commit
        race_target = temp_workspace / "race_artifacts.yaml"
        race_target.write_bytes(live_file.read_bytes())
        snapshot_bytes = race_target.read_bytes()

        # Concurrent modification happens before replacer commits
        race_target.write_text("version: 1.0.0\n# concurrent race edit\n", encoding="utf-8")
        drift_bytes = race_target.read_bytes()

        replacer = CheckedFileWriter()
        with pytest.raises(OriginalChangedError):
            replacer.replace_if_unchanged(
                race_target, snapshot_bytes, PROSPECTIVE_V3_ARTIFACTS_YAML
            )

        # Target file is demonstrably unaltered after refusal
        assert race_target.read_bytes() == drift_bytes
        # Staging file is cleaned up
        assert not list(temp_workspace.glob("*.staging"))

    def test_pyproject_pyright_exact_hunk_and_mismatch_refusal(self, temp_workspace: Path) -> None:
        """Verify pyproject.toml [tool.pyright] CheckedFileWriter replacement and drift refusal."""
        root_dir = Path(__file__).resolve().parents[3]
        pyproject_path = root_dir / "pyproject.toml"
        pyproject_raw = pyproject_path.read_text(encoding="utf-8")

        # Verify expected hunk is in the preimage
        crlf_hunk = PYPROJECT_PYRIGHT_HUNK.replace("\n", "\r\n")
        assert (PYPROJECT_PYRIGHT_HUNK in pyproject_raw) or (crlf_hunk in pyproject_raw)
        hunk = PYPROJECT_PYRIGHT_HUNK if PYPROJECT_PYRIGHT_HUNK in pyproject_raw else crlf_hunk

        # Build patched content
        patched_pyproject = pyproject_raw.replace(hunk, "", 1)
        parsed_after = tomllib.loads(patched_pyproject)
        assert "pyright" not in parsed_after.get("tool", {})
        assert "project" in parsed_after
        assert "ruff" in parsed_after["tool"]
        assert "mypy" in parsed_after["tool"]
        assert "pytest" in parsed_after["tool"]

        pre_sha = hashlib.sha256(pyproject_path.read_bytes()).hexdigest()
        post_sha = hashlib.sha256(patched_pyproject.encode("utf-8")).hexdigest()

        # Success path on isolated copy
        isolated_target = temp_workspace / "pyproject.toml"
        isolated_target.write_bytes(pyproject_path.read_bytes())
        apply_checked_replacement(isolated_target, pre_sha, patched_pyproject, post_sha)
        assert isolated_target.read_bytes() == patched_pyproject.encode("utf-8")

        # Drift protection: concurrent race edit refusal
        race_target = temp_workspace / "race_pyproject.toml"
        race_target.write_bytes(pyproject_path.read_bytes())
        snapshot_bytes = race_target.read_bytes()

        race_target.write_text("[project]\nname = 'concurrent_drift'\n", encoding="utf-8")
        drift_bytes = race_target.read_bytes()

        replacer = CheckedFileWriter()
        with pytest.raises(OriginalChangedError):
            replacer.replace_if_unchanged(race_target, snapshot_bytes, patched_pyproject)
        assert race_target.read_bytes() == drift_bytes

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

    def test_presentation_yaml_clean_break_patch_and_drift_refusal(
        self, temp_workspace: Path
    ) -> None:
        """Verify full V3 clean break presentation patch, loading, and drift refusal."""
        root_dir = Path(__file__).resolve().parents[3]
        live_presentation_path = root_dir / ".pgmcp" / "config" / "presentation.yaml"
        live_content = live_presentation_path.read_text(encoding="utf-8")

        # Build patched content
        patched_content = build_prospective_presentation_yaml(live_content)

        # Clean-break invariants: legacy tools must be completely gone
        assert "run_quality_gates" not in patched_content
        assert "auto_fix" not in patched_content

        # New V3 surfaces must be present
        assert "apply_fixes" in patched_content
        assert "run_checks" in patched_content
        assert "run_tests" in patched_content

        # Write to isolated copy and validate loader acceptance
        config_dir = temp_workspace / ".pgmcp" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        isolated_presentation = config_dir / "presentation.yaml"
        isolated_presentation.write_text(patched_content, encoding="utf-8")

        loader = ConfigLoader(config_dir)
        pres_config = loader.load_presentation_config()
        assert pres_config.version == "1.0.0"
        assert "run_checks" in pres_config.global_settings.next_instruction_texts["recheck_quality"]
        assert "apply_fixes" in pres_config.tools
        assert "run_checks" in pres_config.tools
        assert "run_tests" in pres_config.tools
        assert "run_quality_gates" not in pres_config.tools
        assert "auto_fix" not in pres_config.tools

        # Validate presentation alignment of the new V3 tools against their output models
        v3_tools_subset = {
            "run_checks": pres_config.tools["run_checks"],
            "run_tests": pres_config.tools["run_tests"],
            "apply_fixes": pres_config.tools["apply_fixes"],
        }
        v3_presenter = TextPresenter(
            config=PresentationConfig.model_validate(
                {
                    "version": "1.0.0",
                    "global": pres_config.global_settings,
                    "tools": v3_tools_subset,
                }
            )
        )
        v3_contracts = (
            SupportedToolContract(name="run_checks", output_model=RunChecksOutput),
            SupportedToolContract(name="run_tests", output_model=RunTestsOutput),
            SupportedToolContract(name="apply_fixes", output_model=ApplyFixesOutput),
        )
        validate_presentation_alignment(v3_presenter, v3_contracts)

        # Checked replacement test via CheckedFileWriter
        pre_sha = hashlib.sha256(live_presentation_path.read_bytes()).hexdigest()
        post_sha = hashlib.sha256(patched_content.encode("utf-8")).hexdigest()

        isolated_target = temp_workspace / "presentation_target.yaml"
        isolated_target.write_bytes(live_presentation_path.read_bytes())
        apply_checked_replacement(isolated_target, pre_sha, patched_content, post_sha)
        assert isolated_target.read_bytes() == patched_content.encode("utf-8")

        # Drift protection: concurrent race refusal
        race_target = temp_workspace / "race_presentation.yaml"
        race_target.write_bytes(live_presentation_path.read_bytes())
        snapshot_bytes = race_target.read_bytes()

        race_target.write_text("version: '1.0.0'\n# concurrent edit\n", encoding="utf-8")
        drift_bytes = race_target.read_bytes()

        replacer = CheckedFileWriter()
        with pytest.raises(OriginalChangedError):
            replacer.replace_if_unchanged(race_target, snapshot_bytes, patched_content)
        assert race_target.read_bytes() == drift_bytes

    def test_version_checked_replacement_and_preservation(self, temp_workspace: Path) -> None:
        """Verify .version CheckedFileWriter replacement, byte preservation, and drift refusal."""
        root_dir = Path(__file__).resolve().parents[3]
        live_version_path = root_dir / ".pgmcp" / ".version"
        live_bytes = live_version_path.read_bytes()
        live_text = live_bytes.decode("utf-8")

        pre_sha = hashlib.sha256(live_bytes).hexdigest()
        post_sha = pre_sha  # byte-identical preservation

        isolated_target = temp_workspace / ".version"
        isolated_target.write_bytes(live_bytes)
        apply_checked_replacement(isolated_target, pre_sha, live_text, post_sha)
        assert isolated_target.read_bytes() == live_bytes
        assert isolated_target.read_text(encoding="utf-8").strip() == "2.0.0"

        # Drift protection: concurrent race refusal
        race_target = temp_workspace / "race_version"
        race_target.write_bytes(live_bytes)
        snapshot_bytes = race_target.read_bytes()

        race_target.write_bytes(b"2.0.1\n")
        drift_bytes = race_target.read_bytes()

        replacer = CheckedFileWriter()
        with pytest.raises(OriginalChangedError):
            replacer.replace_if_unchanged(race_target, snapshot_bytes, live_text)
        assert race_target.read_bytes() == drift_bytes

    def test_live_configuration_remains_unmutated_in_cy070(self) -> None:
        """Verify that live repository configuration files remain untouched in CY070."""
        root_dir = Path(__file__).resolve().parents[3]
        live_artifacts = root_dir / ".pgmcp" / "config" / "artifacts.yaml"
        live_pyproject = root_dir / "pyproject.toml"
        live_presentation = root_dir / ".pgmcp" / "config" / "presentation.yaml"
        live_version = root_dir / ".pgmcp" / ".version"

        assert "artifact_types" in live_artifacts.read_text(encoding="utf-8")
        assert "[tool.pyright]" in live_pyproject.read_text(encoding="utf-8")
        assert "run_quality_gates" in live_presentation.read_text(encoding="utf-8")
        assert "auto_fix" in live_presentation.read_text(encoding="utf-8")
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
        presentation_patched = build_prospective_presentation_yaml(presentation_raw)
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
            "2206dc35df61476b9d89b2887b902dc6a4e58fc3076af5ee1106140e4dd4b9d2"
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
            "96e94c62d64e43e0c50389a17c7edf012fa1785ec072d2d4b80b07eb811a9888"
        )
        assert version_pre_sha == (
            "efdfae9d0dc9b09f9524df6c401bf7143a882469c6243bfbcb0bbeaefe9aa3c1"
        )
        assert version_post_sha == (
            "efdfae9d0dc9b09f9524df6c401bf7143a882469c6243bfbcb0bbeaefe9aa3c1"
        )
