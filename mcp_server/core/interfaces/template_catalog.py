# mcp_server/core/interfaces/template_catalog.py
# template=interface version=3fb28c28 created=2026-09-13T15:00Z updated=
"""Deeply immutable JSON values shared by read-only catalog consumers.

@layer: Core (Contracts)
@dependencies: pydantic
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias, Union

from pydantic import ConfigDict, JsonValue, RootModel

FrozenJsonValue: TypeAlias = Union[
    str, bool, int, float, None, tuple["FrozenJsonValue", ...], "FrozenJsonObject"
]


@dataclass(frozen=True)
class FrozenJsonObject(Mapping[str, FrozenJsonValue]):
    """An immutable object whose recursively frozen entries retain caller key presence."""

    entries: tuple[tuple[str, FrozenJsonValue], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.entries, tuple):
            raise TypeError("mutable_json_object_entries")
        seen: set[str] = set()
        for entry in self.entries:
            if not isinstance(entry, tuple) or len(entry) != 2:
                raise TypeError("invalid_json_object_entry")
            key, value = entry
            if not isinstance(key, str) or key in seen:
                raise ValueError("invalid_json_object_key")
            seen.add(key)
            _validate_frozen(value)

    def __getitem__(self, key: str) -> FrozenJsonValue:
        for entry_key, value in self.entries:
            if entry_key == key:
                return value
        raise KeyError(key)

    def __iter__(self) -> Iterator[str]:
        return (key for key, _ in self.entries)

    def __len__(self) -> int:
        return len(self.entries)


class _FiniteJsonInput(RootModel[JsonValue]):
    """Validate generic JSON shape without defining any template-specific field rules."""

    model_config = ConfigDict(frozen=True, strict=True, allow_inf_nan=False)


def freeze_json(value: object) -> FrozenJsonValue:
    """Admit finite JSON without coercion, defaults or filtering, then detach its containers."""
    return _freeze_validated(_FiniteJsonInput.model_validate(value).root)


def _freeze_validated(value: JsonValue) -> FrozenJsonValue:
    if isinstance(value, dict):
        return FrozenJsonObject(
            tuple((key, _freeze_validated(item)) for key, item in value.items())
        )
    if isinstance(value, list):
        return tuple(_freeze_validated(item) for item in value)
    return value


def thaw_json(value: FrozenJsonValue) -> JsonValue:
    """Produce ordinary detached JSON arrays/objects at a serialization or renderer boundary."""
    if isinstance(value, FrozenJsonObject):
        return {key: thaw_json(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [thaw_json(item) for item in value]
    return value


def _validate_frozen(value: FrozenJsonValue) -> None:
    if isinstance(value, tuple):
        for item in value:
            _validate_frozen(item)
    elif isinstance(value, float):
        if not isfinite(value):
            raise ValueError("non_finite_json_number")
    elif value is not None and not isinstance(value, (str, bool, int, FrozenJsonObject)):
        raise TypeError("non_json_or_mutable_value")
