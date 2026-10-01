"""Strict immutable execution bindings; native settings remain adapter-owned."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StrictBool,
    StrictInt,
    StrictStr,
    field_serializer,
    model_validator,
)

from mcp_server.config.schemas.adapter_manifest import AdapterId, CapabilityId

TestId = AdapterId


def _sequence(value: object) -> object:
    return tuple(value) if isinstance(value, list) else value


def _mapping(value: object) -> object:
    if isinstance(value, Mapping):
        return tuple(value.items())
    if isinstance(value, tuple):
        return value
    raise ValueError("mapping_required")


class _TestsBase(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")


class TestBinding(_TestsBase):
    adapter_id: AdapterId
    capability: CapabilityId
    timeout_seconds: Annotated[StrictInt, Field(gt=0)]
    default_args: Annotated[tuple[StrictStr, ...], BeforeValidator(_sequence)]
    active: StrictBool


class TestsConfig(_TestsBase):
    tests: Annotated[tuple[tuple[TestId, TestBinding], ...], BeforeValidator(_mapping)]

    @field_serializer("tests")
    def serialize_tests(
        self, value: tuple[tuple[TestId, TestBinding], ...]
    ) -> dict[str, TestBinding]:
        return dict(value)

    @model_validator(mode="after")
    def validate_unique_ids(self) -> TestsConfig:
        if len(dict(self.tests)) != len(self.tests):
            raise ValueError("duplicate_test_id")
        return self
