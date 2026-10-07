# mcp_server\core\tool_execution.py
# template=generic version=f35abd82 created=2026-09-13T18:22Z updated=
"""Typed in-process operation and schema attachment transport.

@layer: Core (Contracts)
@dependencies: pydantic, template_catalog, template_suite
"""

from typing import Annotated, Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field, GetPydanticSchema
from pydantic_core import core_schema

from mcp_server.core.interfaces.template_catalog import FrozenJsonObject
from mcp_server.schemas.template_identity import TemplateId

TOutput_co = TypeVar("TOutput_co", bound=BaseModel, covariant=True)


class WholeToolSchemaIdentity(BaseModel):
    """Identify the input schema for the invoked tool."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    kind: Literal["whole_tool"]


class TemplateContextSchemaIdentity(BaseModel):
    """Identify a selected template's context schema."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    kind: Literal["template_context"]
    template_id: TemplateId


SchemaIdentity = Annotated[
    WholeToolSchemaIdentity | TemplateContextSchemaIdentity, Field(discriminator="kind")
]


class SchemaAttachment(BaseModel):
    """Carry immutable schema facts, without presentation or cache policy."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    identity: SchemaIdentity
    # The approved field intentionally replaces BaseModel's deprecated schema() method.
    schema: Annotated[  # type: ignore[assignment]  # pyright: ignore[reportIncompatibleMethodOverride]
        FrozenJsonObject,
        GetPydanticSchema(
            lambda _source, _handler: core_schema.is_instance_schema(FrozenJsonObject)
        ),
    ]


class ToolExecution(BaseModel, Generic[TOutput_co]):
    """Keep the operation separate from resources attached to this execution."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")
    operation: TOutput_co
    attachments: tuple[SchemaAttachment, ...]


def operation_output_model(model: type[BaseModel]) -> type[BaseModel]:
    """Unwrap the one known transport type when deriving operation metadata."""
    if not issubclass(model, ToolExecution):
        return model
    operation = model.model_fields["operation"].annotation
    if not isinstance(operation, type) or not issubclass(operation, BaseModel):
        raise TypeError("ToolExecution output metadata requires a concrete operation model")
    return operation
