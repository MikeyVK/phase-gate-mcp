"""Canonical JSON representation shared by cache publication and resource reads."""

from __future__ import annotations

import json
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
    """Serialize once using the existing optional-null and error fallback contract."""
    # Required null and explicitly supplied null are operation facts.
    try:
        content = dto.model_dump_json(exclude=_absent_optional_nulls(dto))
    except Exception as e:
        fallback = {
            "success": False,
            "error_type": "SerializationError",
            "message": f"Unable to serialize DTO: {e}",
            "dto_type": type(dto).__name__,
        }
        if hasattr(dto, "error_message") and dto.error_message:
            fallback["error_message"] = str(dto.error_message)
        if hasattr(dto, "traceback") and dto.traceback:
            fallback["traceback"] = str(dto.traceback)
        content = json.dumps(fallback)

    return content
