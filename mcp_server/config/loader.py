"""Central config loader for migrated YAML-backed schemas."""

from __future__ import annotations

from collections.abc import Callable, Hashable
from pathlib import Path
from typing import Any, TypeVar

import yaml
from pydantic import BaseModel, TypeAdapter, ValidationError

from mcp_server.config.composition import compose_configuration, validate_complete_configuration
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
    PresentationConfig,
    ScopeConfig,
    TestsConfig,
    WorkflowConfig,
    WorkphasesConfig,
)
from mcp_server.config.schemas.adapter_manifest import AdapterManifest, AdapterTrustConfig
from mcp_server.config.schemas.artifact_locations import ArtifactLocationsConfig
from mcp_server.config.schemas.server_config import ServerConfig
from mcp_server.config.schemas.template_suite import (
    TemplateManifest,
    TemplatePackageVersion,
    TemplatePolicy,
)
from mcp_server.config.settings import GitHubSettings
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


class _ConfigYamlLoader(yaml.SafeLoader):
    """Preserve typed keys while rejecting duplicates before mapping construction."""

    def construct_mapping(self, node: yaml.Node, deep: bool = False) -> dict[Hashable, object]:
        if not isinstance(node, yaml.MappingNode):
            raise yaml.YAMLError("configuration_mapping_required")
        self.flatten_mapping(node)
        construct: Callable[[yaml.Node, bool], object] = self.construct_object
        result: dict[Hashable, object] = {}
        for key_node, value_node in node.value:
            key = construct(key_node, deep)
            if not isinstance(key, (str, int)) or isinstance(key, bool) or key in result:
                raise yaml.YAMLError("duplicate_or_invalid_configuration_key")
            result[key] = construct(value_node, deep)
        return result


def normalize_config_root(config_root: Path | str) -> Path:
    """Return the resolved config directory path.

    After C3: callers always pass ``server_root / "config"`` (derived from
    ``workspace_root / settings.server.server_root_dir / "config"``).  No heuristic or
    disk-based probe is performed — the path is resolved and returned as-is.
    """
    return Path(config_root).resolve()


class ConfigLoader:
    """Single YAML reader for migrated config schemas."""

    def __init__(
        self,
        config_root: Path,
        *,
        context_schema_reader: Callable[[Path], FrozenJsonObject] | None = None,
    ) -> None:
        self._context_schema_reader = context_schema_reader
        self.config_root = normalize_config_root(config_root)

    def load_adapter_manifest(self, path: Path) -> AdapterManifest:
        """Read one package declaration without legacy configuration-version rules."""
        return self._load_declaration(AdapterManifest, path)

    def load_adapter_trust(self) -> AdapterTrustConfig:
        """Read the required owner policy from the explicitly selected config root."""
        return self._load_workspace(AdapterTrustConfig, "adapters.yaml")

    def load_checks_config(self) -> ChecksConfig:
        """Read required checks.yaml without activating or reading legacy quality config."""
        return self._load_workspace(ChecksConfig, "checks.yaml")

    def load_tests_config(self) -> TestsConfig:
        """Read required test bindings without native dependency probing."""
        return self._load_workspace(TestsConfig, "tests.yaml")

    def load_artifact_locations_config(self) -> ArtifactLocationsConfig:
        """Read the required workspace artifact-location declaration."""
        return self._load_workspace(ArtifactLocationsConfig, "artifacts.yaml")

    def load_fixes_config(self) -> FixesConfig:
        """Read required fix bindings without native dependency probing."""
        return self._load_workspace(FixesConfig, "fixes.yaml")

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
        return self._load_workspace(GitConfig, "git.yaml", config_path=config_path)

    def load_label_config(self, config_path: Path | None = None) -> LabelConfig:
        return self._load_workspace(LabelConfig, "labels.yaml", config_path=config_path)

    def load_presentation_config(self, config_path: Path | None = None) -> PresentationConfig:
        return self._load_workspace(
            PresentationConfig, "presentation.yaml", config_path=config_path
        )

    def load_scope_config(self, config_path: Path | None = None) -> ScopeConfig:
        return self._load_workspace(ScopeConfig, "scopes.yaml", config_path=config_path)

    def load_workflow_config(self, config_path: Path | None = None) -> WorkflowConfig:
        return self._load_workspace(WorkflowConfig, "workflows.yaml", config_path=config_path)

    def load_workphases_config(self, config_path: Path | None = None) -> WorkphasesConfig:
        return self._load_workspace(WorkphasesConfig, "workphases.yaml", config_path=config_path)

    def load_contributor_config(self, config_path: Path | None = None) -> ContributorConfig:
        return self._load_workspace(ContributorConfig, "contributors.yaml", config_path=config_path)

    def load_issue_config(self, config_path: Path | None = None) -> IssueConfig:
        return self._load_workspace(IssueConfig, "issues.yaml", config_path=config_path)

    def load_milestone_config(self, config_path: Path | None = None) -> MilestoneConfig:
        return self._load_workspace(MilestoneConfig, "milestones.yaml", config_path=config_path)

    def load_enforcement_config(self, config_path: Path | None = None) -> EnforcementConfig:
        return self._load_workspace(
            EnforcementConfig, "enforcement.yaml", config_path=config_path, optional=True
        )

    def load_contracts_config(
        self,
        config_path: Path | None = None,
    ) -> ContractsConfig:
        return self._load_workspace(ContractsConfig, "contracts.yaml", config_path=config_path)

    def load_server_config(self) -> ServerConfig:
        """Read required startup policy through ordinary workspace composition."""
        return self._load_workspace(ServerConfig, "server.yaml")

    def load_github_config(self, config_path: Path | None = None) -> GitHubSettings:
        """Load workspace GitHub identity and optional explicit token alternative."""
        return self._load_workspace(GitHubSettings, "github.yaml", config_path=config_path)

    def _load_workspace(
        self,
        schema: type[SchemaT],
        file_name: str,
        *,
        config_path: Path | None = None,
        optional: bool = False,
    ) -> SchemaT:
        """Admit one complete basis and an optional workspace difference document."""
        if config_path is not None:
            path = Path(config_path).resolve()
            data, _ = self._load_yaml(file_name, config_path=path)
            try:
                validate_complete_configuration(data)
            except ValueError as exc:
                raise ConfigError(str(exc), str(path)) from exc
            return self._admit(schema, data, path)

        basis_path = self.config_root / "defaults" / file_name
        override_path = self.config_root / file_name
        if optional and not basis_path.exists():
            if not override_path.exists():
                return schema.model_validate({})
            return self._load_workspace(schema, file_name, config_path=override_path)
        basis, _ = self._load_yaml(file_name, config_path=basis_path)
        try:
            validate_complete_configuration(basis)
            self._admit(schema, basis, basis_path)
            changes = (
                self._load_yaml(file_name, config_path=override_path)[0]
                if override_path.exists()
                else None
            )
            merged = compose_configuration(basis, changes)
        except ValueError as exc:
            raise ConfigError(str(exc), str(override_path)) from exc
        return self._admit(schema, merged, override_path if changes is not None else basis_path)

    def _admit(self, schema: type[SchemaT], data: dict[str, Any], path: Path) -> SchemaT:
        if "version" in schema.model_fields:
            return self._validate_schema(schema, data, path)
        try:
            return schema.model_validate(data)
        except ValidationError as exc:
            errors = [
                (error["loc"], error["type"], error["msg"])
                for error in exc.errors(include_input=False, include_context=False)
            ]
            raise ConfigError(f"Config validation failed: {errors}", str(path)) from exc

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
                loaded = yaml.load(file_handle, Loader=_ConfigYamlLoader)
        except (OSError, yaml.YAMLError) as exc:
            raise ConfigError(
                f"Invalid YAML in {resolved_path.name}: {exc}",
                file_path=str(resolved_path),
            ) from exc

        if not isinstance(loaded, dict) or any(not isinstance(key, str) for key in loaded):
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
                f"Config validation failed for {resolved_path.name}: "
                f"{[(err['loc'], err['type'], err['msg']) for err in errors]}",
                file_path=str(resolved_path),
            ) from exc
