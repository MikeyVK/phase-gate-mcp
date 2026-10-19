"""Canonical JSON representation shared by cache publication and resource reads."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from pydantic.main import IncEx


def _absent_optional_nulls(value: object) -> IncEx:
    """Derive omissions from the actual DTO fields, including the selected variant."""
    if isinstance(value, BaseModel):
        fields: dict[str, IncEx | bool] = {}
        for name, field in type(value).model_fields.items():
            item = getattr(value, name)
            if item is None and not field.is_required() and name not in value.model_fields_set:
                fields[name] = True
            else:
                nested = _absent_optional_nulls(item)
                if nested:
                    fields[name] = nested
        return fields
    if isinstance(value, (list, tuple)):
        elements: dict[int, IncEx | bool] = {}
        for index, item in enumerate(value):
            nested = _absent_optional_nulls(item)
            if nested:
                elements[index] = nested
        return elements
    if isinstance(value, dict):
        members: dict[str, IncEx | bool] = {}
        for key, item in value.items():
            nested = _absent_optional_nulls(item)
            if nested:
                members[key] = nested
        return members
    return {}


def serialize_cached_response(dto: BaseModel) -> str:
    """Return canonical operation JSON or propagate the original serialization error."""
    # Required null and explicitly supplied null are operation facts.
    return dto.model_dump_json(exclude=_absent_optional_nulls(dto))
