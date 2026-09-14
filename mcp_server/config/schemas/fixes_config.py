"""Strict immutable execution bindings; native settings remain adapter-owned."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StrictInt,
    StrictStr,
    field_serializer,
    model_validator,
)

from mcp_server.config.schemas.adapter_manifest import AdapterId, CapabilityId

FixId = AdapterId


def _sequence(value: object) -> object:
    return tuple(value) if isinstance(value, list) else value


def _mapping(value: object) -> object:
    if isinstance(value, Mapping):
        return tuple(value.items())
    if isinstance(value, tuple):
        return value
    raise ValueError("mapping_required")


class _FixesBase(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")


class FixBinding(_FixesBase):
    adapter_id: AdapterId
    capability: CapabilityId
    timeout_seconds: Annotated[StrictInt, Field(gt=0)]
    default_args: Annotated[tuple[StrictStr, ...], BeforeValidator(_sequence)]


class FixesConfig(_FixesBase):
    fixes: Annotated[tuple[tuple[FixId, FixBinding], ...], BeforeValidator(_mapping)]

    @field_serializer("fixes")
    def serialize_fixes(self, value: tuple[tuple[FixId, FixBinding], ...]) -> dict[str, FixBinding]:
        return dict(value)

    @model_validator(mode="after")
    def validate_unique_ids(self) -> FixesConfig:
        if len(dict(self.fixes)) != len(self.fixes):
            raise ValueError("duplicate_fix_id")
        return self
