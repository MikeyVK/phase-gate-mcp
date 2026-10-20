"""Compose one configured presentation/data projection without changing operation facts."""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, JsonValue

from mcp_server.config.schemas.presentation_config import (
    GlobalPresentationConfig,
    ResolvedResponseProfile,
)
from mcp_server.core.error_handling import capture_exception
from mcp_server.core.interfaces.ipresenter import IPresenter, IResourcePresenter, ITextPresenter
from mcp_server.core.operation_notes import NoteEntry
from mcp_server.core.tool_execution import SchemaAttachment
from mcp_server.presenters.text_budget_limiter import TextBudgetLimiter
from mcp_server.schemas.cache_publication import CachePublication
from mcp_server.schemas.error_outputs import ConfigErrorOutput, ExecutionErrorOutput
from mcp_server.schemas.presentation_output import (
    DeliveryFailure,
    InlineOperation,
    OperationDelivery,
    PresentedOutput,
    PublicToolResponse,
    RenderedPresentation,
    ResourceOperation,
)

logger = logging.getLogger(__name__)


def processing_diagnostic(
    error_message: str, traceback: str | None, *, max_bytes: int
) -> ExecutionErrorOutput:
    """Project only bounded native strings, never arbitrary exception context."""
    message_prefix = error_message[:max_bytes]
    message = TextBudgetLimiter.excerpt(message_prefix, max_bytes=max_bytes)
    remaining = max(max_bytes - len(message.text.encode("utf-8")), 0)
    trace_text = None
    truncated = len(message_prefix) < len(error_message) or message.details_truncated
    if traceback is not None:
        trace_prefix = traceback[:remaining]
        trace = TextBudgetLimiter.excerpt(trace_prefix, max_bytes=remaining)
        trace_text = trace.text
        truncated = truncated or len(trace_prefix) < len(traceback) or trace.details_truncated
    return ExecutionErrorOutput(
        error_message=message.text,
        traceback=trace_text,
        params={"diagnostic_details_truncated": truncated},
    )


class ResponsePresenter(IPresenter):
    """Route shared rendered guidance and complete data using one immutable profile."""

    def __init__(
        self,
        text_presenter: ITextPresenter,
        resource_presenter: IResourcePresenter,
        profile: ResolvedResponseProfile,
        global_config: GlobalPresentationConfig,
    ) -> None:
        self._text_presenter = text_presenter
        self._resource_presenter = resource_presenter
        self._profile = profile
        self._global = global_config
        self._limiter = TextBudgetLimiter(
            max_text_response_bytes=profile.max_text_response_bytes,
            formatting=global_config.formatting,
        )

    def output_schema(self) -> dict[str, JsonValue] | None:
        """Describe the selected common envelope and its admitted emergency variant."""
        if not self._has_structured:
            return None
        schema = PublicToolResponse.model_json_schema()
        properties = schema["properties"]
        properties["presentation"] = (
            {"type": "string"} if self._structured_presentation else {"type": "null"}
        )
        if self._profile.data_channel == "structured":
            selected = (
                "InlineOperation"
                if self._profile.data_delivery == "inline"
                else "ResourceOperation"
            )
            normal_data: dict[str, JsonValue] = {"$ref": f"#/$defs/{selected}"}
        else:
            normal_data = {"type": "null"}
            properties["attachments"]["maxItems"] = 0
        if self._profile.data_channel == "text":
            properties["processing_error"] = {"type": "null"}
        schema["anyOf"] = [
            {
                "properties": {
                    "data": normal_data,
                    "delivery_error": {"type": "null"},
                    "processing_error": {"type": "null"},
                }
            },
            {
                "properties": {
                    "data": {"type": "null"},
                    "delivery_error": {"$ref": "#/$defs/DeliveryFailure"},
                    "processing_error": {"type": "null"},
                }
            },
        ]
        if self._profile.data_channel == "structured":
            schema["anyOf"].append(
                {
                    "required": ["processing_error"],
                    "properties": {
                        "data": {
                            "anyOf": [
                                {"$ref": "#/$defs/ResourceOperation"},
                                {"type": "null"},
                            ]
                        },
                        "attachments": {"maxItems": 0},
                        "delivery_error": {"type": "null"},
                        "processing_error": {"$ref": "#/$defs/ExecutionErrorOutput"},
                    }
                }
            )
        return schema

    @property
    def _has_structured(self) -> bool:
        return self._structured_presentation or self._profile.data_channel == "structured"

    @property
    def _structured_presentation(self) -> bool:
        return self._profile.presentation_channel in {"structured", "both"}

    @property
    def _text_presentation(self) -> bool:
        return self._profile.presentation_channel in {"text", "both"}

    def present(
        self,
        tool_name: str,
        data: BaseModel | dict[str, Any],
        notes: list[NoteEntry] | None = None,
        cache_pub: CachePublication | None = None,
        success: bool | None = None,
        *,
        attachments: tuple[SchemaAttachment, ...] = (),
    ) -> PresentedOutput:
        """Render once, preserve the outcome, then select transport projections."""
        resolved_success = (
            success
            if success is not None
            else bool(data.get("success", True))
            if isinstance(data, dict)
            else getattr(data, "success", True)
        )
        rendered = self._text_presenter.present_text(
            tool_name=tool_name,
            data=data,
            notes=notes,
            cache_pub=cache_pub,
            success=resolved_success,
        )
        resources = self._resource_presenter.present_resources(attachments)
        cache_available = cache_pub is not None and cache_pub.success
        core = rendered.core
        if cache_available:
            assert cache_pub is not None
            core = self._join(core, self._cache_guidance(cache_pub))
        elif cache_pub is not None:
            core = self._join(core, self._word("cache_publication_failed"))
        bounded = self._limiter.limit(
            RenderedPresentation(core=core, details=rendered.details),
            cache_available=cache_available,
        )
        presentation = bounded.text
        delivery: OperationDelivery | None = None
        failure: DeliveryFailure | None = None
        diagnostic = cache_pub.diagnostic if cache_pub is not None else None
        if self._profile.data_delivery == "inline":
            try:
                operation = (
                    data.model_dump(mode="json", by_alias=True)
                    if isinstance(data, BaseModel)
                    else data
                )
                delivery = InlineOperation(delivery="inline", operation=operation)
            except Exception as exc:  # noqa: BLE001 -- Presentation boundary preserves original cause.
                logger.exception("Inline operation serialization failed")
                diagnostic = capture_exception(exc)
                failure = DeliveryFailure(
                    code="operation_serialization_failed", details_truncated=False
                )
        elif cache_available:
            assert cache_pub is not None
            delivery = ResourceOperation(
                delivery="resource",
                uri=f"pgmcp://cache/runs/{cache_pub.run_id}",
                size_chars=cache_pub.size_chars,
            )
        else:
            failure = DeliveryFailure(
                code=(
                    "operation_serialization_failed"
                    if cache_pub is not None and cache_pub.error_code == "serialization_failed"
                    else "cache_publication_failed"
                ),
                details_truncated=False,
            )
        if failure is not None:
            presentation, truncated = self._emergency(
                presentation, data, diagnostic, failure.code, cache_available
            )
            failure = failure.model_copy(update={"details_truncated": truncated})
        structured = None
        if self._has_structured:
            envelope = PublicToolResponse(
                success=resolved_success,
                presentation=presentation if self._structured_presentation else None,
                data=delivery if self._profile.data_channel == "structured" else None,
                attachments=resources if self._profile.data_channel == "structured" else (),
                delivery_error=failure,
            )
            structured = envelope.model_dump(mode="json")
        text_parts = []
        if self._text_presentation or failure is not None:
            text_parts.append(presentation)
        if self._profile.data_channel == "text":
            text_payload = PublicToolResponse(
                success=resolved_success,
                presentation=None,
                data=delivery,
                attachments=resources,
                delivery_error=failure,
            ).model_dump_json()
            text_parts.append(f"```json\n{text_payload}\n```")
        return PresentedOutput(
            text=self._join(*text_parts) if text_parts else None,
            structured_content=structured,
        )

    def recover(
        self,
        *,
        operation_success: bool,
        error_message: str,
        traceback: str | None,
        cache_run_id: str | None,
        cache_size_chars: int | None,
    ) -> PresentedOutput:
        """Deliver small known facts without the original payload or rendering."""
        diagnostic = processing_diagnostic(
            error_message, traceback, max_bytes=self._profile.max_cache_failure_detail_bytes
        )
        notice = self._word("response_processing_failed").format(success=operation_success)
        reference = None
        if cache_run_id is not None:
            receipt = CachePublication(run_id=cache_run_id, size_chars=cache_size_chars)
            reference = ResourceOperation(
                delivery="resource",
                uri=f"pgmcp://cache/runs/{cache_run_id}",
                size_chars=cache_size_chars,
            )
            notice = self._join(notice, self._cache_guidance(receipt))
        else:
            notice = self._join(notice, self._word("recovery_cache_unavailable"))
        if diagnostic.params["diagnostic_details_truncated"]:
            notice = self._join(notice, self._word("processing_diagnostic_truncated"))
        structured = None
        if self._has_structured:
            structured = PublicToolResponse(
                success=operation_success,
                presentation=notice if self._structured_presentation else None,
                data=reference if self._profile.data_channel == "structured" else None,
                attachments=(),
                delivery_error=None,
                processing_error=(
                    diagnostic if self._profile.data_channel == "structured" else None
                ),
            ).model_dump(mode="json")
        text_parts = [notice] if self._text_presentation else []
        if self._profile.data_channel == "text":
            envelope = PublicToolResponse(
                success=operation_success,
                presentation=None,
                data=reference,
                attachments=(),
                delivery_error=None,
                processing_error=diagnostic,
            )
            text_parts.append(f"```json\n{envelope.model_dump_json()}\n```")
        return PresentedOutput(
            text=self._join(*text_parts) if text_parts else None,
            structured_content=structured,
        )

    def _cache_guidance(self, publication: CachePublication) -> str:
        instructions = self._global.next_instruction_texts
        reference = instructions.get("uri_reference", "").format(run_id=publication.run_id)
        if (
            publication.size_chars is not None
            and publication.size_chars > self._profile.cache_read_budget_chars
        ):
            reference = self._join(reference, instructions.get("pagination_reference", ""))
        return reference

    def _emergency(
        self,
        presentation: str,
        data: BaseModel | dict[str, Any],
        diagnostic: ConfigErrorOutput | ExecutionErrorOutput | None,
        code: str,
        cache_available: bool,
    ) -> tuple[str, bool]:
        """Retain protected guidance and add only bounded, labelled native detail."""
        warning = self._word(code)
        core = self._join(presentation, warning) if warning not in presentation else presentation
        if diagnostic is not None:
            details = diagnostic.traceback or diagnostic.error_message or ""
        else:
            values = (
                {name: getattr(data, name) for name in type(data).model_fields}
                if isinstance(data, BaseModel)
                else data
            )
            details = "\n".join(
                f"{key}: {value}" for key, value in values.items() if isinstance(value, str)
            )
        if not details:
            return self._join(core, self._word("diagnostic_unavailable")), False
        label = self._word("diagnostic_excerpt_label")
        allowance = self._profile.max_cache_failure_detail_bytes
        label_bytes = len(label.encode("utf-8")) + 2
        excerpt = self._limiter.excerpt(details, max_bytes=max(allowance - label_bytes, 0))
        diagnostic_text = self._join(label, excerpt.text) if excerpt.text else ""
        if excerpt.details_truncated:
            notice = (
                self._global.formatting.truncation_notice
                if cache_available
                else self._global.formatting.cache_unavailable_truncation_notice
            )
            core = self._join(core, notice)
        return self._join(core, diagnostic_text), excerpt.details_truncated

    def _word(self, key: str) -> str:
        return self._global.next_instruction_texts[key]

    @staticmethod
    def _join(*parts: str) -> str:
        return "\n\n".join(part for part in parts if part)
