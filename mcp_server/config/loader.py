"""Central config loader for migrated YAML-backed schemas."""

from __future__ import annotations

from collections.abc import Callable, Hashable, Iterable
from pathlib import Path
from typing import Any, TypeVar

import yaml
from pydantic import BaseModel, TypeAdapter, ValidationError

from mcp_server.config.schemas import (
    ChecksConfig,
    ContractsConfig,
    ContributorConfig,
    EnforcementConfig,
    FixesConfig,
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
    TestsConfig,
    WorkflowConfig,
    WorkphasesConfig,
)
from mcp_server.config.schemas.adapter_manifest import AdapterManifest, AdapterTrustConfig
from mcp_server.config.schemas.artifact_locations import ArtifactLocationsConfig
from mcp_server.config.schemas.template_suite import (
    TemplateManifest,
    TemplatePackageVersion,
    TemplatePolicy,
)
from mcp_server.core.exceptions import ConfigError
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject

SchemaT = TypeVar("SchemaT", bound=BaseModel)


class _AdapterYamlLoader(yaml.SafeLoader):
    """Reject duplicate or non-string keys before immutable declaration admission."""

    def construct_mapping(self, node: yaml.Node, deep: bool = False) -> dict[Hashable, object]:
        if not isinstance(node, yaml.MappingNode):
            raise yaml.YAMLError("adapter_mapping_required")
        construct: Callable[[yaml.Node, bool], object] = self.construct_object
        result: dict[Hashable, object] = {}
        for key_node, value_node in node.value:
            key = construct(key_node, deep)
            if not isinstance(key, str) or key in result:
                raise yaml.YAMLError("duplicate_or_invalid_adapter_key")
            result[key] = construct(value_node, deep)
        return result


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

    def __init__(
        self,
        config_root: Path,
        template_root: Path | None = None,
        *,
        context_schema_reader: Callable[[Path], FrozenJsonObject] | None = None,
    ) -> None:
        self._context_schema_reader = context_schema_reader
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

    def load_adapter_manifest(self, path: Path) -> AdapterManifest:
        """Read one package declaration without legacy configuration-version rules."""
        return self._load_declaration(AdapterManifest, path)

    def load_adapter_trust(self) -> AdapterTrustConfig:
        """Read the required owner policy from the explicitly selected config root."""
        return self._load_declaration(AdapterTrustConfig, self.config_root / "adapters.yaml")

    def load_checks_config(self) -> ChecksConfig:
        """Read required checks.yaml without activating or reading legacy quality config."""
        return self._load_declaration(
            ChecksConfig, self.config_root / "checks.yaml", description="checks configuration"
        )

    def load_tests_config(self) -> TestsConfig:
        """Read required test bindings without native dependency probing."""
        return self._load_declaration(
            TestsConfig, self.config_root / "tests.yaml", description="tests configuration"
        )

    def load_artifact_locations_config(self) -> ArtifactLocationsConfig:
        """Read the required workspace artifact-location declaration."""
        return self._load_declaration(
            ArtifactLocationsConfig,
            self.config_root / "artifacts.yaml",
            description="artifact locations configuration",
        )

    def load_fixes_config(self) -> FixesConfig:
        """Read required fix bindings without native dependency probing."""
        return self._load_declaration(
            FixesConfig, self.config_root / "fixes.yaml", description="fixes configuration"
        )

    def _load_declaration(
        self, schema: type[SchemaT], path: Path, *, description: str = "adapter declaration"
    ) -> SchemaT:
        try:
            with path.open(encoding="utf-8") as stream:
                data = yaml.load(stream, Loader=_AdapterYamlLoader)
            return schema.model_validate(data)
        except (OSError, yaml.YAMLError, ValidationError) as exc:
            raise ConfigError(f"Invalid {description}: {exc}", str(path)) from exc

    def load_template_context_schema(self, schema_path: Path) -> FrozenJsonObject:
        """Read an explicit prepared contract through the composition-supplied reader."""
        if self._context_schema_reader is None:
            raise ConfigError("template_context_reader_required")
        return self._context_schema_reader(schema_path)

    def load_template_manifest(self, path: Path) -> TemplateManifest:
        """Read the closed package manifest without legacy registry/version fields."""
        data, _ = self._load_yaml("manifest.yaml", config_path=path)
        return TemplateManifest.model_validate(data)

    def load_template_policy(self, path: Path) -> TemplatePolicy:
        """Read package-owned evidence selection and persistence policy."""
        data, _ = self._load_yaml("policy.yaml", config_path=path)
        return TemplatePolicy.model_validate(data)

    def load_template_version(self, path: Path) -> str:
        """Read one canonical SemVer label, permitting one ordinary final newline."""
        value = path.read_text(encoding="utf-8").removesuffix("\r\n").removesuffix("\n")
        return TypeAdapter(TemplatePackageVersion).validate_python(value)

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
