# mcp_server/core/interfaces/tool_input_contract.py
# template=interface version=3fb28c28 created=2026-09-13T17:48Z updated=
"""Immutable prepared tool-input authority shared by exposure and admission."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, Protocol, TypeAlias, TypeVar

from pydantic import BaseModel, JsonValue

from mcp_server.core.interfaces.template_catalog import FrozenJsonObject

JsonObject: TypeAlias = dict[str, JsonValue]
TInput = TypeVar("TInput", bound=BaseModel | None, covariant=True)
TModel = TypeVar("TModel", bound=BaseModel)


class IToolInputContract(Protocol[TInput]):
    """Expose a schema snapshot and its matching typed admission operation."""

    @property
    def schema(self) -> FrozenJsonObject:
        """Return the immutable prepared schema."""
        ...

    def validate(self, raw: JsonObject) -> TInput:
        """Admit input or raise the existing Pydantic ValidationError."""
        ...


@dataclass(frozen=True)
class PreparedToolInputContract(Generic[TInput]):
    """Hold the composition root's schema and admission without reload capability."""

    schema: FrozenJsonObject
    admit: Callable[[JsonObject], TInput]

    def validate(self, raw: JsonObject) -> TInput:
        """Delegate to the same admission authority paired with the schema."""
        return self.admit(raw)


def prepare_model_input(model: type[TModel]) -> PreparedToolInputContract[TModel]:
    """Prepare exposure and admission from one typed tool definition or projection."""
    raise NotImplementedError
