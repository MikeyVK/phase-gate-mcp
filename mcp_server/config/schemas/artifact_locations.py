"""Immutable artifact-location configuration values."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, Literal

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    StrictStr,
    field_serializer,
    model_validator,
)

from mcp_server.config.schemas.template_suite import TemplateId
from mcp_server.utils.path_resolver import normalize_workspace_relative_path


def _sequence(value: object) -> object:
    if isinstance(value, list):
        return tuple(value)
    return value


def _mapping_items(value: object) -> object:
    if isinstance(value, Mapping):
        return tuple(value.items())
    if isinstance(value, tuple):
        for item in value:
            if not isinstance(item, (tuple, list)) or len(item) != 2:
                raise ValueError("mapping_items_required")
        return tuple((item[0], item[1]) for item in value)
    raise ValueError("mapping_required")


WorkspaceRelativeRoot = Annotated[StrictStr, AfterValidator(normalize_workspace_relative_path)]
WorkspaceRelativeRoots = Annotated[tuple[WorkspaceRelativeRoot, ...], BeforeValidator(_sequence)]


class _ArtifactLocationsBase(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")


class ArtifactLocation(_ArtifactLocationsBase):
    """One package's normalized workspace-relative allowed roots."""

    default_root: WorkspaceRelativeRoot
    additional_roots: WorkspaceRelativeRoots = ()

    @model_validator(mode="after")
    def validate_distinct_roots(self) -> ArtifactLocation:
        roots = (self.default_root, *self.additional_roots)
        if len(set(roots)) != len(roots):
            raise ValueError("duplicate_artifact_location_root")
        return self


class ArtifactLocationsConfig(_ArtifactLocationsBase):
    """Workspace authority for package artifact locations."""

    version: Literal["2.0.0"]
    artifacts: Annotated[
        tuple[tuple[TemplateId, ArtifactLocation], ...], BeforeValidator(_mapping_items)
    ]

    @field_serializer("artifacts")
    def serialize_artifacts(
        self, value: tuple[tuple[TemplateId, ArtifactLocation], ...]
    ) -> dict[str, ArtifactLocation]:
        return dict(value)

    @model_validator(mode="after")
    def validate_unique_artifacts(self) -> ArtifactLocationsConfig:
        if len(dict(self.artifacts)) != len(self.artifacts):
            raise ValueError("duplicate_artifact_location_id")
        return self
