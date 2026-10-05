# pgmcp:v1 id=python_pydantic_dto pv=1.0.0 pf=QqfSP7PZ6WteOp8N sf=5--KpGf2wHUv2qAj

"""Immutable original startup failure facts, independent of admitted configuration."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    GetPydanticSchema,
    JsonValue,
    WithJsonSchema,
    field_serializer,
)
from pydantic_core import core_schema

from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, thaw_json

DiagnosticParameters = Annotated[
    FrozenJsonObject,
    GetPydanticSchema(lambda _source, _handler: core_schema.is_instance_schema(FrozenJsonObject)),
    WithJsonSchema({"type": "object", "additionalProperties": True}),
]


class StartupDiagnostic(BaseModel):
    """Preserve deeply immutable startup diagnostics with their original cause."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    exception_type: str
    message: str
    code: str | None
    params: DiagnosticParameters
    file_path: str | None = None
    cause: StartupDiagnostic | None = None

    @field_serializer("params", when_used="json")
    def serialize_params(self, value: FrozenJsonObject) -> Mapping[str, JsonValue]:
        """Expose an ordinary JSON object without changing the frozen source."""
        serialized = thaw_json(value)
        if not isinstance(serialized, dict):
            raise TypeError("startup_diagnostic_params_object_required")
        return serialized
