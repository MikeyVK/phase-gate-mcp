"""Immutable closed models for .pgmcp/installation.json."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType

from pydantic import (
    BaseModel,
    ConfigDict,
    field_serializer,
    field_validator,
    model_validator,
)

from mcp_server.schemas.template_identity import CompactFingerprint, TemplateId


class TemplateCheckpoint(BaseModel):
    """One complete adopted operational component map."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    shared: CompactFingerprint
    packages: Mapping[TemplateId, CompactFingerprint]

    @field_validator("packages", mode="after")
    @classmethod
    def freeze_packages(
        cls,
        value: Mapping[TemplateId, CompactFingerprint],
    ) -> Mapping[TemplateId, CompactFingerprint]:
        """Keep package entries immutable and deterministic."""

        return MappingProxyType(dict(sorted(value.items())))

    @field_serializer("packages")
    def serialize_packages(self, value: Mapping[TemplateId, CompactFingerprint]) -> dict[str, str]:
        return dict(value)


class InstallationState(BaseModel):
    """The exact closed installation.json contract."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    pgmcp_version: str
    template_checkpoint: TemplateCheckpoint | None = None

    @field_validator("pgmcp_version")
    @classmethod
    def nonempty_version(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("pgmcp_version_required")
        return value

    @model_validator(mode="after")
    def reject_explicit_null_checkpoint(self) -> InstallationState:
        if "template_checkpoint" in self.model_fields_set and self.template_checkpoint is None:
            raise ValueError("template_checkpoint_null_forbidden")
        return self
