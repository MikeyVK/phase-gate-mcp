"""Protect required presentation while bounding optional UTF-8 detail text."""

from __future__ import annotations

from mcp_server.config.schemas.presentation_config import FormattingConfig
from mcp_server.core.exceptions import ConfigError
from mcp_server.schemas.presentation_output import BoundedPresentation, RenderedPresentation


class TextBudgetLimiter:
    """Apply a presentation allowance without ever cutting the mandatory core."""

    _BLOCK_SEPARATOR = "\n\n"
    _FENCE_CLOSURE = "\n```"

    def __init__(self, *, max_text_response_bytes: int, formatting: FormattingConfig) -> None:
        if max_text_response_bytes <= 0:
            raise ConfigError("Text response byte budget must be greater than zero")
        self._max_bytes = max_text_response_bytes
        self._formatting = formatting

    def limit(
        self, presentation: RenderedPresentation, *, cache_available: bool
    ) -> BoundedPresentation:
        """Reserve core/notices and shorten only optional rendered details."""
        core, details = presentation.core, presentation.details
        complete = self._join(core, details)
        if not details or self._byte_length(complete) <= self._max_bytes:
            return BoundedPresentation(text=complete, details_truncated=False)
        notice = (
            self._formatting.truncation_notice
            if cache_available
            else self._formatting.cache_unavailable_truncation_notice
        )
        protected = self._join(core, notice)
        available = max(self._max_bytes - self._byte_length(protected) - 2, 0)
        excerpt = self.excerpt(details, max_bytes=available)
        return BoundedPresentation(
            text=self._join(core, excerpt.text, notice), details_truncated=True
        )

    @classmethod
    def excerpt(cls, details: str, *, max_bytes: int) -> BoundedPresentation:
        """Return valid Unicode and closed formatting inside a detail allowance."""
        if cls._byte_length(details) <= max_bytes:
            return BoundedPresentation(text=details, details_truncated=False)
        prefix = cls._select_readable_prefix(details, max(max_bytes, 0))
        if cls._has_open_fence(prefix):
            prefix = cls._select_readable_prefix(
                details, max(max_bytes - cls._byte_length(cls._FENCE_CLOSURE), 0)
            )
            if cls._has_open_fence(prefix):
                prefix += cls._FENCE_CLOSURE
        return BoundedPresentation(text=prefix, details_truncated=True)

    @staticmethod
    def _join(*parts: str) -> str:
        return "\n\n".join(part for part in parts if part)

    @classmethod
    def _select_readable_prefix(cls, body: str, max_bytes: int) -> str:
        candidate = cls._utf8_prefix(body, max_bytes)
        if len(candidate) == len(body):
            return candidate
        block_boundary = candidate.rfind(cls._BLOCK_SEPARATOR)
        if block_boundary > 0:
            return candidate[:block_boundary].rstrip()
        line_boundary = candidate.rfind("\n")
        if line_boundary > 0:
            return candidate[:line_boundary].rstrip()
        return candidate.rstrip()

    @staticmethod
    def _utf8_prefix(text: str, max_bytes: int) -> str:
        if max_bytes <= 0:
            return ""
        encoded = text.encode("utf-8")
        return encoded[:max_bytes].decode("utf-8", errors="ignore")

    @staticmethod
    def _has_open_fence(text: str) -> bool:
        return sum(1 for line in text.splitlines() if line.lstrip().startswith("```")) % 2 == 1

    @staticmethod
    def _byte_length(text: str) -> int:
        return len(text.encode("utf-8"))
