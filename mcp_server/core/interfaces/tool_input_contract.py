# mcp_server/core/interfaces/tool_input_contract.py
# template=interface version=3fb28c28 created=2026-09-13T17:48Z updated=
"""Immutable prepared tool-input authority shared by exposure and admission."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, Protocol, TypeAlias, TypeVar

from jsonschema import Draft202012Validator
from pydantic import BaseModel, JsonValue, ValidationError
from pydantic_core import InitErrorDetails

from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, freeze_json, thaw_json
from mcp_server.utils.schema_utils import resolve_schema_refs

JsonObject: TypeAlias = dict[str, JsonValue]
TInput_co = TypeVar("TInput_co", bound=BaseModel | None, covariant=True)
TModel = TypeVar("TModel", bound=BaseModel)


class IToolInputContract(Protocol[TInput_co]):
    """Expose a schema snapshot and its matching typed admission operation."""

    @property
    def schema(self) -> FrozenJsonObject:
        """Return the immutable prepared schema."""
        ...

    def validate(self, raw: JsonObject) -> TInput_co:
        """Admit input or raise the existing Pydantic ValidationError."""
        ...


@dataclass(frozen=True)
class PreparedToolInputContract(Generic[TInput_co]):
    """Hold the composition root's schema and admission without reload capability."""

    schema: FrozenJsonObject
    admit: Callable[[JsonObject], TInput_co]

    def validate(self, raw: JsonObject) -> TInput_co:
        """Delegate to the same admission authority paired with the schema."""
        return self.admit(raw)


def prepare_model_input(model: type[TModel]) -> PreparedToolInputContract[TModel]:
    """Prepare exposure and admission from one typed tool definition or projection."""
    schema = freeze_json(resolve_schema_refs(model.model_json_schema()))
    if not isinstance(schema, FrozenJsonObject):
        raise TypeError("tool_input_schema_must_be_object")
    validator = Draft202012Validator(thaw_json(schema))

    def admit(raw: JsonObject) -> TModel:
        errors: list[InitErrorDetails] = [
            {
                "type": "value_error",
                "loc": tuple(error.absolute_path),
                "input": error.instance,
                "ctx": {"error": ValueError(error.message)},
            }
            for error in validator.iter_errors(raw)
        ]
        if errors:
            raise ValidationError.from_exception_data(model.__name__, errors)
        return model.model_validate(raw)

    return PreparedToolInputContract(schema=schema, admit=admit)
