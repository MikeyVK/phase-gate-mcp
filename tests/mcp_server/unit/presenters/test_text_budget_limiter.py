"""Public final UTF-8 bounds, footer retention and readable truncation."""

import pytest

from mcp_server.core.exceptions import ConfigError
from mcp_server.presenters.text_budget_limiter import TextBudgetLimiter


class TestTextBudgetLimiter:
    """The final allowance includes text, notices, footer and fence closure."""

    @pytest.mark.parametrize("body", ["", "small details"])
    def test_preserves_complete_under_budget_presentation(self, body: str) -> None:
        footer = "result-location"
        expected = "\n\n".join(part for part in (body, footer) if part)
        result = TextBudgetLimiter(max_text_response_bytes=100).limit(
            body, footer=footer, truncation_notice="SHORTENED"
        )
        assert result.text == expected
        assert not result.details_truncated

    def test_final_bound_includes_large_main_text(self) -> None:
        result = TextBudgetLimiter(max_text_response_bytes=8000).limit(
            "Required phase guidance " * 500,
            footer="RESULT-LOCATION",
            truncation_notice="SHORTENED",
        )
        assert len(result.text.encode("utf-8")) <= 8000
        assert result.text.endswith("RESULT-LOCATION")
        assert "SHORTENED" in result.text
        assert result.details_truncated

    def test_bounds_unicode_and_closes_intersected_fence(self) -> None:
        result = TextBudgetLimiter(max_text_response_bytes=130).limit(
            "Before\n```text\n" + "🙂漢\n" * 40,
            footer="READ-FULL-RESULT",
            truncation_notice="SHORTENED",
        )
        assert result.text.count("```") % 2 == 0
        assert result.text.endswith("READ-FULL-RESULT")
        assert "�" not in result.text
        assert result.details_truncated
        assert len(result.text.encode("utf-8")) <= 130

    def test_rejects_impossible_footer_budget(self) -> None:
        with pytest.raises(ConfigError):
            TextBudgetLimiter(max_text_response_bytes=10).limit(
                "large body", footer="footer beyond budget", truncation_notice="SHORTENED"
            )

    def test_rejects_nonpositive_budget(self) -> None:
        with pytest.raises(ConfigError):
            TextBudgetLimiter(max_text_response_bytes=0)
