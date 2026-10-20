"""Compose one configured presentation/data projection without changing operation facts."""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, JsonValue

from mcp_server.config.schemas.presentation_config import (
    GlobalPresentationConfig,
)
from mcp_server.config.settings import ResponseMode
from mcp_server.core.error_handling import capture_exception
from mcp_server.core.interfaces.ipresenter import IPresenter, IResourcePresenter, ITextPresenter
from mcp_server.core.operation_notes import NoteEntry
from mcp_server.core.tool_execution import SchemaAttachment
from mcp_server.presenters.text_budget_limiter import TextBudgetLimiter
from mcp_server.schemas.cache_publication import CachePublication
from mcp_server.schemas.error_outputs import ConfigErrorOutput, ExecutionErrorOutput
from mcp_server.schemas.presentation_output import (
    AttachmentReference,
    DeliveryFailure,
    InlineOperation,
    OperationDelivery,
    PresentationResource,
    PresentedOutput,
    PublicToolResponse,
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
    """Deliver bounded text and one supplementary route with separate resources."""

    def __init__(
        self,
        text_presenter: ITextPresenter,
        resource_presenter: IResourcePresenter,
        mode: ResponseMode,
        global_config: GlobalPresentationConfig,
    ) -> None:
        self._text_presenter = text_presenter
        self._resource_presenter = resource_presenter
        self._mode = mode
        self._global = global_config
        self._limiter = TextBudgetLimiter(
            max_text_response_bytes=global_config.max_text_response_bytes,
        )

    def output_schema(self) -> dict[str, JsonValue] | None:
        """Describe full structured delivery and its truthful failure variants."""
        if self._mode == "resource":
            return None
        schema = PublicToolResponse.model_json_schema()
        schema["properties"]["presentation"] = {"type": "string"}
        schema["anyOf"] = [
            {
                "properties": {
                    "data": {"$ref": "#/$defs/InlineOperation"},
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
                },
            },
        ]
        return schema

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
        """Project one execution without replaying a failed operation serializer."""
        resolved_success = (
            success
            if success is not None
            else bool(data.get("success", True))
            if isinstance(data, dict)
            else getattr(data, "success", True)
        )
        resources = self._resource_presenter.present_resources(attachments)
        diagnostic = cache_pub.diagnostic if cache_pub is not None else None
        if cache_pub is not None and cache_pub.error_code == "serialization_failed":
            return self._delivery_failure(
                resolved_success, resources, diagnostic, "operation_serialization_failed"
            )

        rendered = self._text_presenter.present_text(
            tool_name=tool_name,
            data=data,
            notes=notes,
            cache_pub=cache_pub,
            success=resolved_success,
        )
        body = self._join(rendered.core, rendered.details)
        delivery: OperationDelivery | None = None
        failure: DeliveryFailure | None = None
        if self._mode == "structured":
            try:
                operation = (
                    data.model_dump(mode="json", by_alias=True)
                    if isinstance(data, BaseModel)
                    else data
                )
                delivery = InlineOperation(delivery="inline", operation=operation)
            except Exception as exc:  # Presentation boundary retains the native cause.
                logger.exception("Inline operation serialization failed")
                diagnostic = capture_exception(exc)
                failure = DeliveryFailure(
                    code="operation_serialization_failed", details_truncated=False
                )
        elif cache_pub is None or not cache_pub.success:
            failure = DeliveryFailure(code="cache_publication_failed", details_truncated=False)

        if failure is not None:
            excerpt, truncated = self._diagnostic_excerpt(diagnostic)
            body = self._join(
                body,
                self._word("delivery_failure_outcome").format(success=resolved_success),
                self._word(failure.code),
                excerpt,
            )
            failure = failure.model_copy(update={"details_truncated": truncated})
        elif cache_pub is not None and not cache_pub.success:
            body = self._join(body, self._word("cache_publication_failed"))

        footer = self._footer(resources, cache_pub, structured_complete=delivery is not None)
        full_presentation = self._join(body, footer)
        structured = None
        if self._mode == "structured":
            structured = PublicToolResponse(
                success=resolved_success,
                presentation=full_presentation,
                data=delivery,
                attachments=self._references(resources),
                delivery_error=failure,
            ).model_dump(mode="json")
        text = self._bound(
            body,
            footer,
            available=delivery is not None or (cache_pub is not None and cache_pub.success),
        )
        return PresentedOutput(text=text, structured_content=structured, resources=resources)

    def _delivery_failure(
        self,
        success: bool,
        resources: tuple[PresentationResource, ...],
        diagnostic: ConfigErrorOutput | ExecutionErrorOutput | None,
        code: str,
    ) -> PresentedOutput:
        """Use known facts only after an earlier full serializer failed."""
        excerpt, truncated = self._diagnostic_excerpt(diagnostic)
        body = self._join(
            self._word("delivery_failure_outcome").format(success=success),
            self._word(code),
            excerpt,
        )
        footer = self._footer(resources, None, structured_complete=False)
        failure = DeliveryFailure(
            code="operation_serialization_failed", details_truncated=truncated
        )
        structured = None
        if self._mode == "structured":
            structured = PublicToolResponse(
                success=success,
                presentation=self._join(body, footer),
                data=None,
                attachments=self._references(resources),
                delivery_error=failure,
            ).model_dump(mode="json")
        return PresentedOutput(
            text=self._bound(body, footer, available=False),
            structured_content=structured,
            resources=resources,
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
        """Deliver known outcome and bounded diagnosis without normal rendering."""
        diagnostic = processing_diagnostic(
            error_message,
            traceback,
            max_bytes=self._global.max_cache_failure_detail_bytes,
        )
        notice = self._word("response_processing_failed").format(success=operation_success)
        publication = (
            CachePublication(run_id=cache_run_id, size_chars=cache_size_chars)
            if cache_run_id is not None
            else None
        )
        footer = self._footer((), publication, structured_complete=False)
        if diagnostic.params["diagnostic_details_truncated"]:
            footer = self._join(footer, self._word("processing_diagnostic_truncated"))
        body = self._join(
            notice,
            self._word("diagnostic_excerpt_label"),
            diagnostic.error_message or "",
            diagnostic.traceback or "",
        )
        structured = None
        if self._mode == "structured":
            reference = (
                ResourceOperation(
                    delivery="resource",
                    uri=f"pgmcp://cache/runs/{cache_run_id}",
                    size_chars=cache_size_chars,
                )
                if cache_run_id is not None
                else None
            )
            structured = PublicToolResponse(
                success=operation_success,
                presentation=self._join(notice, footer),
                data=reference,
                attachments=(),
                delivery_error=None,
                processing_error=diagnostic,
            ).model_dump(mode="json")
        return PresentedOutput(
            text=self._bound(body, footer, available=publication is not None),
            structured_content=structured,
        )

    def _footer(
        self,
        resources: tuple[PresentationResource, ...],
        publication: CachePublication | None,
        *,
        structured_complete: bool,
    ) -> str:
        attachment_notice = self._word("attachment_reference") if resources else ""
        if structured_complete:
            reference = self._word("structured_reference")
        elif publication is not None and publication.success:
            reference = self._word("uri_reference").format(run_id=publication.run_id)
            if (
                publication.size_chars is not None
                and publication.size_chars > self._global.cache_read_budget_chars
            ):
                reference = self._join(
                    reference, self._global.next_instruction_texts.get("pagination_reference", "")
                )
        else:
            reference = self._word("recovery_cache_unavailable")
        return self._join(attachment_notice, reference)

    def _bound(self, body: str, footer: str, *, available: bool) -> str:
        notice = (
            self._global.formatting.truncation_notice
            if available
            else self._global.formatting.cache_unavailable_truncation_notice
        )
        return self._limiter.limit(body, footer=footer, truncation_notice=notice).text

    def _diagnostic_excerpt(
        self,
        diagnostic: ConfigErrorOutput | ExecutionErrorOutput | None,
    ) -> tuple[str, bool]:
        if diagnostic is None:
            return self._word("diagnostic_unavailable"), False
        label = self._word("diagnostic_excerpt_label")
        allowance = max(
            self._global.max_cache_failure_detail_bytes - len(label.encode("utf-8")) - 4, 0
        )
        bounded = processing_diagnostic(
            diagnostic.error_message or "",
            diagnostic.traceback,
            max_bytes=allowance,
        )
        truncated = bool(bounded.params["diagnostic_details_truncated"])
        text = self._join(label, bounded.error_message or "", bounded.traceback or "")
        if truncated:
            text = self._join(text, self._word("processing_diagnostic_truncated"))
        return text, truncated

    @staticmethod
    def _references(
        resources: tuple[PresentationResource, ...],
    ) -> tuple[AttachmentReference, ...]:
        return tuple(
            AttachmentReference(uri=resource.uri, mime_type=resource.mime_type)
            for resource in resources
        )

    def _word(self, key: str) -> str:
        return self._global.next_instruction_texts[key]

    @staticmethod
    def _join(*parts: str) -> str:
        return "\n\n".join(part for part in parts if part)
