"""Central config loader for migrated YAML-backed schemas."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any, TypeVar

import yaml
from pydantic import BaseModel, ValidationError

from mcp_server.config.schemas import (
    ArtifactRegistryConfig,
    ContractsConfig,
    ContributorConfig,
    EnforcementConfig,
    GitConfig,
    IssueConfig,
    LabelConfig,
    MilestoneConfig,
    OperationPoliciesConfig,
    PresentationConfig,
    ProjectStructureConfig,
    QualityConfig,
    ScaffoldMetadataConfig,
    ScopeConfig,
    WorkflowConfig,
    WorkphasesConfig,
)
from mcp_server.core.exceptions import ConfigError

SchemaT = TypeVar("SchemaT", bound=BaseModel)


def normalize_config_root(config_root: Path | str) -> Path:
    """Return the resolved config directory path.

    After C3: callers always pass ``server_root / "config"`` (derived from
    ``workspace_root / settings.server.server_root_dir / "config"``).  No heuristic or
    disk-based probe is performed — the path is resolved and returned as-is.
    """
    return Path(config_root).resolve()


def resolve_config_root(
    preferred_root: Path | str | None = None,
    explicit_root: Path | str | None = None,
    required_files: Iterable[str] = (),
) -> Path:
    """Resolve one canonical phase-gate config root without legacy compatibility fallbacks."""
    required = tuple(required_files)

    def _has_required_files(candidate: Path) -> bool:
        return all((candidate / file_name).exists() for file_name in required)

    if explicit_root is not None:
        explicit_candidate = normalize_config_root(explicit_root)
        if explicit_candidate.exists() and _has_required_files(explicit_candidate):
            return explicit_candidate
        missing = [
            file_name for file_name in required if not (explicit_candidate / file_name).exists()
        ]
        if missing:
            missing_text = ", ".join(str(file_name) for file_name in missing)
            raise FileNotFoundError(
                "Explicit config_root is missing required files: "
                f"{missing_text} ({explicit_candidate})"
            )
        raise FileNotFoundError(f"Explicit config_root does not exist: {explicit_candidate}")

    candidates: list[Path] = []

    if preferred_root is not None:
        candidates.append(Path(preferred_root).resolve())
    candidates.append(Path.cwd().resolve())
    candidates.append(Path(__file__).resolve().parents[2])

    unique_candidates: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        unique_candidates.append(candidate)

    for candidate in unique_candidates:
        if candidate.exists() and _has_required_files(candidate):
            return candidate

    raise FileNotFoundError("Could not locate canonical phase-gate config directory")


class ConfigLoader:
    """Single YAML reader for migrated config schemas."""

    def __init__(self, config_root: Path, template_root: Path | None = None) -> None:
        self.config_root = normalize_config_root(config_root)
        if template_root is not None:
            self.template_root = Path(template_root).resolve()
        else:
            try:
                from mcp_server.config.settings import Settings  # noqa: PLC0415

                settings = Settings.from_env()
                self.template_root = Path(settings.server.resolved_template_root)
            except Exception:  # noqa: BLE001
                self.template_root = (self.config_root.parent / "templates").resolve()

    def load_git_config(self, config_path: Path | None = None) -> GitConfig:
        data, resolved_path = self._load_yaml("git.yaml", config_path=config_path)
        return self._validate_schema(GitConfig, data, resolved_path)

    def load_label_config(self, config_path: Path | None = None) -> LabelConfig:
        data, resolved_path = self._load_yaml("labels.yaml", config_path=config_path)
        return self._validate_schema(LabelConfig, data, resolved_path)

    def load_presentation_config(self, config_path: Path | None = None) -> PresentationConfig:
        data, resolved_path = self._load_yaml("presentation.yaml", config_path=config_path)
        return self._validate_schema(PresentationConfig, data, resolved_path)

    def load_scope_config(self, config_path: Path | None = None) -> ScopeConfig:
        data, resolved_path = self._load_yaml("scopes.yaml", config_path=config_path)
        return self._validate_schema(ScopeConfig, data, resolved_path)

    def load_workflow_config(self, config_path: Path | None = None) -> WorkflowConfig:
        data, resolved_path = self._load_yaml("workflows.yaml", config_path=config_path)
        return self._validate_schema(WorkflowConfig, data, resolved_path)

    def load_workphases_config(self, config_path: Path | None = None) -> WorkphasesConfig:
        data, resolved_path = self._load_yaml("workphases.yaml", config_path=config_path)
        return self._validate_schema(WorkphasesConfig, data, resolved_path)

    def load_artifact_registry_config(
        self,
        config_path: Path | None = None,
    ) -> ArtifactRegistryConfig:
        legacy_dir = self.config_root / "artifacts"
        if legacy_dir.is_dir():
            raise ConfigError(
                "Legacy config/artifacts/ directory is no longer supported under the "
                "Template Packages contract. Fix: Move all artifact modular configuration "
                "files to templates/config/ and delete this directory.",
                file_path=str(legacy_dir),
            )

        if config_path is None:
            resolved_path = Path(self.config_root) / "artifacts.yaml"
        else:
            resolved_path = Path(config_path).resolve()

        if not resolved_path.exists():
            raise ConfigError(
                "Artifact registry not found: "
                f"{resolved_path}. Expected: config/artifacts.yaml. "
                "Fix: Create config/artifacts.yaml manually or restore from backup.",
                file_path=str(resolved_path),
            )

        try:
            with resolved_path.open(encoding="utf-8") as file_handle:
                raw_loaded = yaml.safe_load(file_handle)
        except yaml.YAMLError as exc:
            raise ConfigError(
                "Invalid YAML syntax: "
                f"{exc}. Fix: Check YAML syntax; common issues are incorrect "
                "indentation, missing colons, and unquoted special characters. "
                "Use a YAML validator.",
                file_path=str(resolved_path),
            ) from exc

        if raw_loaded is None:
            raw_loaded = {}
        elif not isinstance(raw_loaded, dict):
            raise ConfigError(
                f"Invalid YAML root in {resolved_path.name}: expected mapping",
                file_path=str(resolved_path),
            )

        index_version = raw_loaded.get("version", "1.0.0")
        merged_artifact_types = list(raw_loaded.get("artifact_types", []))

        if config_path is not None:
            config_dir = resolved_path.parent
        else:
            config_dir = (
                Path(self.template_root) / "config" if self.template_root else resolved_path.parent
            )
        if not config_dir.is_dir():
            if not merged_artifact_types:
                raise ConfigError(
                    "Empty artifact registry: no artifact types defined",
                    file_path=str(resolved_path),
                )
        else:
            yaml_files = sorted(
                [
                    f
                    for f in config_dir.iterdir()
                    if (
                        f.is_file()
                        and f.suffix in (".yaml", ".yml")
                        and f.name not in ("artifacts.yaml", resolved_path.name)
                    )
                ]
            )
            for filepath in yaml_files:
                try:
                    with filepath.open(encoding="utf-8") as fh:
                        file_data = yaml.safe_load(fh)
                except yaml.YAMLError as exc:
                    raise ConfigError(
                        f"Invalid YAML syntax: {exc}.",
                        file_path=str(filepath),
                    ) from exc
                if file_data is None:
                    continue
                if isinstance(file_data, dict) and (
                    "version" in file_data or "artifact_types" in file_data
                ):
                    continue
                if isinstance(file_data, list):
                    merged_artifact_types.extend(file_data)
                elif isinstance(file_data, dict):
                    merged_artifact_types.append(file_data)
                else:
                    raise ConfigError(
                        "Invalid YAML structure in modular file: "
                        f"expected mapping or list, got {type(file_data).__name__}",
                        file_path=str(filepath),
                    )

        if not merged_artifact_types:
            raise ConfigError(
                "Empty artifact registry: no artifact types defined",
                file_path=str(resolved_path),
            )

        full_config = {
            "version": index_version,
            "artifact_types": merged_artifact_types,
        }

        return self._validate_schema(ArtifactRegistryConfig, full_config, resolved_path)

    def load_contributor_config(self, config_path: Path | None = None) -> ContributorConfig:
        data, resolved_path = self._load_yaml("contributors.yaml", config_path=config_path)
        return self._validate_schema(ContributorConfig, data, resolved_path)

    def load_issue_config(self, config_path: Path | None = None) -> IssueConfig:
        data, resolved_path = self._load_yaml("issues.yaml", config_path=config_path)
        return self._validate_schema(IssueConfig, data, resolved_path)

    def load_milestone_config(self, config_path: Path | None = None) -> MilestoneConfig:
        data, resolved_path = self._load_yaml("milestones.yaml", config_path=config_path)
        return self._validate_schema(MilestoneConfig, data, resolved_path)

    def load_operation_policies_config(
        self,
        config_path: Path | None = None,
    ) -> OperationPoliciesConfig:
        data, resolved_path = self._load_yaml("policies.yaml", config_path=config_path)
        operations = data.get("operations")
        if not isinstance(operations, dict):
            raise ConfigError(
                f"Missing 'operations' key in {resolved_path.name}",
                file_path=str(resolved_path),
            )

        payload = {
            **data,
            "operations": {
                operation_id: {"operation_id": operation_id, **operation_data}
                for operation_id, operation_data in operations.items()
            },
        }
        return self._validate_schema(OperationPoliciesConfig, payload, resolved_path)

    def load_project_structure_config(
        self,
        config_path: Path | None = None,
        artifact_registry: ArtifactRegistryConfig | None = None,
    ) -> ProjectStructureConfig:
        data, resolved_path = self._load_yaml(
            "project_structure.yaml",
            config_path=config_path,
        )
        directories = data.get("directories")
        if not isinstance(directories, dict):
            raise ConfigError(
                f"Missing 'directories' key in {resolved_path.name}",
                file_path=str(resolved_path),
            )

        payload = {
            **data,
            "directories": {
                directory_path: {"path": directory_path, **directory_data}
                for directory_path, directory_data in directories.items()
            },
        }
        config = self._validate_schema(ProjectStructureConfig, payload, resolved_path)
        effective_artifact_registry = artifact_registry or self.load_artifact_registry_config()
        self._validate_project_structure_artifact_types(
            config,
            effective_artifact_registry,
            resolved_path,
        )
        self._validate_project_structure_parent_references(config, resolved_path)
        return config

    def load_quality_config(self, config_path: Path | None = None) -> QualityConfig:
        data, resolved_path = self._load_yaml("quality.yaml", config_path=config_path)
        return self._validate_schema(QualityConfig, data, resolved_path)

    def load_scaffold_metadata_config(
        self,
        config_path: Path | None = None,
    ) -> ScaffoldMetadataConfig:
        data, resolved_path = self._load_yaml(
            "scaffold_metadata.yaml",
            config_path=config_path,
        )
        return self._validate_schema(ScaffoldMetadataConfig, data, resolved_path)

    def load_enforcement_config(self, config_path: Path | None = None) -> EnforcementConfig:
        data, resolved_path = self._load_yaml(
            "enforcement.yaml",
            config_path=config_path,
            allow_missing=True,
        )
        if not resolved_path.exists():
            return EnforcementConfig(version="1.0.0")
        return self._validate_schema(EnforcementConfig, data, resolved_path)

    def load_contracts_config(
        self,
        config_path: Path | None = None,
    ) -> ContractsConfig:
        data, resolved_path = self._load_yaml(
            "contracts.yaml",
            config_path=config_path,
        )
        return self._validate_schema(ContractsConfig, data, resolved_path)

    def _validate_project_structure_artifact_types(
        self,
        config: ProjectStructureConfig,
        artifact_registry: ArtifactRegistryConfig,
        resolved_path: Path,
    ) -> None:
        valid_types = set(artifact_registry.list_type_ids())
        for directory_path, policy in config.directories.items():
            invalid_types = set(policy.allowed_artifact_types) - valid_types
            if invalid_types:
                raise ConfigError(
                    f"Directory '{directory_path}' references unknown artifact types: "
                    f"{sorted(invalid_types)}. Valid types from artifact registry: "
                    f"{sorted(valid_types)}",
                    file_path=str(resolved_path),
                )

    def _validate_project_structure_parent_references(
        self,
        config: ProjectStructureConfig,
        resolved_path: Path,
    ) -> None:
        for directory_path, policy in config.directories.items():
            if policy.parent is not None and policy.parent not in config.directories:
                raise ConfigError(
                    f"Directory '{directory_path}' references unknown parent: '{policy.parent}'",
                    file_path=str(resolved_path),
                )

    def _resolve_yaml_path(self, file_name: str | Path, config_path: Path | None = None) -> Path:
        if config_path is None:
            return self.config_root / file_name
        return Path(config_path).resolve()

    def _load_yaml(
        self,
        file_name: str | Path,
        config_path: Path | None = None,
        allow_missing: bool = False,
    ) -> tuple[dict[str, Any], Path]:
        resolved_path = self._resolve_yaml_path(file_name, config_path=config_path)

        if not resolved_path.exists():
            if allow_missing:
                return {}, resolved_path
            raise ConfigError(
                f"Config file not found: {resolved_path.name}",
                file_path=str(resolved_path),
            )

        try:
            with resolved_path.open(encoding="utf-8") as file_handle:
                loaded = yaml.safe_load(file_handle) or {}
        except yaml.YAMLError as exc:
            raise ConfigError(
                f"Invalid YAML in {resolved_path.name}: {exc}",
                file_path=str(resolved_path),
            ) from exc

        if not isinstance(loaded, dict):
            raise ConfigError(
                f"Invalid YAML root in {resolved_path.name}: expected mapping",
                file_path=str(resolved_path),
            )

        return loaded, resolved_path

    def _validate_schema(
        self,
        schema_cls: type[SchemaT],
        data: dict[str, Any],
        resolved_path: Path,
    ) -> SchemaT:
        # Resolve expected version dynamically from schema type annotation
        version_field = schema_cls.model_fields.get("version")
        annotation = version_field.annotation if version_field else None
        args = getattr(annotation, "__args__", None)
        if args and isinstance(args, tuple) and len(args) > 0:
            expected_val = str(args[0])
        else:
            expected_val = "1.0.0"

        # Explicit check for version field existence before validation
        if "version" not in data:
            raise ConfigError(
                f"Configuration version is missing in {resolved_path.name}. "
                f"(expected version '{expected_val}')",
                file_path=str(resolved_path),
            )

        try:
            return schema_cls.model_validate(data)
        except ValidationError as exc:
            errors = exc.errors()
            for err in errors:
                if "version" in err.get("loc", ()):
                    input_val = err.get("input")
                    raise ConfigError(
                        f"Config version mismatch in {resolved_path.name}: "
                        f"expected version '{expected_val}', found '{input_val}'. "
                        f"Please update your configuration.",
                        file_path=str(resolved_path),
                    ) from exc
            raise ConfigError(
                f"Config validation failed for {resolved_path.name}: {exc}",
                file_path=str(resolved_path),
            ) from exc
