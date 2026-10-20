"""Public behavior of protected presentation and optional UTF-8 detail budgets."""

import pytest

from mcp_server.config.schemas.presentation_config import FormattingConfig
from mcp_server.core.exceptions import ConfigError
from mcp_server.presenters.text_budget_limiter import TextBudgetLimiter
from mcp_server.schemas.presentation_output import RenderedPresentation


def _formatting() -> FormattingConfig:
    return FormattingConfig(
        inline_sequence_omission_template="… {omitted_count} more",
        collection_omission_template="- … {omitted_count} more {field}",
        truncation_notice="[TRUNCATED: COMPLETE CACHE]",
        cache_unavailable_truncation_notice="[TRUNCATED: CACHE UNAVAILABLE]",
    )


def _limiter(max_bytes: int) -> TextBudgetLimiter:
    return TextBudgetLimiter(max_text_response_bytes=max_bytes, formatting=_formatting())


class TestTextBudgetLimiter:
    """Required guidance is never part of a destructive prefix cut."""

    @pytest.mark.parametrize("details", ["", "small details"])
    def test_preserves_complete_under_budget_presentation(self, details: str) -> None:
        core = "Required instruction"
        expected = core + ("\n\n" + details if details else "")
        result = _limiter(len(expected.encode("utf-8"))).limit(
            RenderedPresentation(core=core, details=details), cache_available=True
        )
        assert result.text == expected
        assert not result.details_truncated

    @pytest.mark.parametrize("cache_available", [False, True])
    def test_limits_only_optional_details_and_protects_notices(self, cache_available: bool) -> None:
        core = "Required instruction\n\ncache:" + "a" * 32
        result = _limiter(160).limit(
            RenderedPresentation(core=core, details="First block\n\n" + "🚀" * 200),
            cache_available=cache_available,
        )
        assert result.text.startswith(core)
        assert result.details_truncated
        notice = (
            _formatting().truncation_notice
            if cache_available
            else _formatting().cache_unavailable_truncation_notice
        )
        assert notice in result.text
        assert len(result.text.encode("utf-8")) <= 160
        assert "�" not in result.text

    def test_final_bound_includes_large_main_text(self) -> None:
        core = "Required phase guidance " * 500
        result = _limiter(8_000).limit(
            RenderedPresentation(core=core, details="optional"),
            cache_available=False,
        )
        assert len(result.text.encode("utf-8")) <= 8_000
        assert _formatting().cache_unavailable_truncation_notice in result.text
        assert result.details_truncated

    def test_closes_optional_fence_without_cutting_required_guidance(self) -> None:
        result = _limiter(130).limit(
            RenderedPresentation(core="Required", details="Before\n```text\n" + "inside\n" * 40),
            cache_available=True,
        )
        assert result.text.startswith("Required")
        assert result.text.count("```") % 2 == 0
        assert result.details_truncated
        assert len(result.text.encode("utf-8")) <= 130

    def test_rejects_nonpositive_budget(self) -> None:
        with pytest.raises(ConfigError):
            _limiter(0)
