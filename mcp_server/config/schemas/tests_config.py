"""Strict immutable execution bindings; native settings remain adapter-owned."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, TypeGuard

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
from mcp_server.config.schemas.checks_config import ConfigurationChoice

TestId = AdapterId


def _is_object_list(value: object) -> TypeGuard[list[object]]:
    return isinstance(value, list)


def _is_object_mapping(value: object) -> TypeGuard[Mapping[object, object]]:
    return isinstance(value, Mapping)


def _is_object_tuple(value: object) -> TypeGuard[tuple[object, ...]]:
    return isinstance(value, tuple)


def _sequence(value: object) -> object:
    if _is_object_list(value):
        items: list[object] = value
        return tuple(items)
    return value


def _mapping(value: object) -> object:
    if _is_object_mapping(value):
        entries: Mapping[object, object] = value
        return tuple(entries.items())
    if _is_object_tuple(value):
        items: tuple[object, ...] = value
        return items
    raise ValueError("mapping_required")


class _TestsBase(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")


class TestBinding(_TestsBase):
    adapter_id: AdapterId
    capability: CapabilityId
    timeout_seconds: Annotated[StrictInt, Field(gt=0)]
    default_args: Annotated[tuple[StrictStr, ...], BeforeValidator(_sequence)]
    configuration_choice: ConfigurationChoice | None = None
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
