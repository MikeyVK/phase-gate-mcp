"""Immutable presentation values and the public response envelope.

Operation models remain internal and are serialized only at the presentation boundary.
"""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from mcp_server.schemas.error_outputs import ExecutionErrorOutput


class PresentationResource(BaseModel):
    """An attachment's complete identity, media type and textual contents."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    uri: str
    mime_type: str = "application/json"
    content: str


class RenderedPresentation(BaseModel):
    """Required guidance separated from optional rendered details."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    core: str
    details: str


class InlineOperation(BaseModel):
    """Complete JSON-mode operation facts supplied directly."""

    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    delivery: Literal["inline"]
    operation: dict[str, JsonValue]


class ResourceOperation(BaseModel):
    """A reference to a successfully serialized and published operation."""

    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    delivery: Literal["resource"]
    uri: str
    size_chars: int | None = Field(ge=0)


class DeliveryFailure(BaseModel):
    """Delivery status independent of the actual operation outcome."""

    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    code: Literal["cache_publication_failed", "operation_serialization_failed"]
    details_truncated: bool


type OperationDelivery = Annotated[
    InlineOperation | ResourceOperation, Field(discriminator="delivery")
]


class PublicToolResponse(BaseModel):
    """The selected public presentation, data and direct attachments."""

    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    success: bool
    presentation: str | None
    data: OperationDelivery | None
    attachments: tuple[PresentationResource, ...]
    delivery_error: DeliveryFailure | None
    processing_error: ExecutionErrorOutput | None = None


class PresentedOutput(BaseModel):
    """The selected transport projection, independent of MCP SDK classes."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    text: str | None
    structured_content: dict[str, JsonValue] | None


class BoundedPresentation(BaseModel):
    """A readable projection with explicit optional-detail omission."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    text: str
    details_truncated: bool
