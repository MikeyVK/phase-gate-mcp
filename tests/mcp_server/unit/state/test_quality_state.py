# tests/mcp_server/unit/state/test_quality_state.py
"""C5 (C_QA_STATE_SPLIT): QualityState DTO for isolated quality-gate baseline persistence.

Tests verify:
- QualityState is importable from mcp_server.state.quality_state
- baseline_sha field: str | None = None
- failed_files field: list[str] = []
- Model is frozen (immutable)
- extra="forbid" enforced

@layer: Tests (Unit)
@dependencies: pytest, pydantic, mcp_server.state.quality_state
"""
# pyright: reportPrivateUsage=false

from __future__ import annotations

import pytest
from pydantic import ValidationError

# RED: will fail with ModuleNotFoundError until C5 GREEN creates quality_state.py
from mcp_server.state.quality_state import QualityState


class TestQualityStateModel:
    """C5: QualityState is an immutable Pydantic model for quality gate baseline state."""

    def test_quality_state_importable(self) -> None:
        """QualityState is importable from mcp_server.state.quality_state."""
        assert QualityState is not None

    def test_default_baseline_sha_is_none(self) -> None:
        """Default baseline_sha is None (no baseline recorded)."""
        state = QualityState()
        assert state.baseline_sha is None

    def test_default_failed_files_is_empty_list(self) -> None:
        """Default failed_files is an empty list."""
        state = QualityState()
        assert state.failed_files == []

    def test_can_set_baseline_sha(self) -> None:
        """baseline_sha can be set to a SHA string."""
        state = QualityState(baseline_sha="abc123def")
        assert state.baseline_sha == "abc123def"

    def test_can_set_failed_files(self) -> None:
        """failed_files can be set to a list of file paths."""
        state = QualityState(failed_files=["a.py", "b.py"])
        assert state.failed_files == ["a.py", "b.py"]

    def test_model_is_frozen(self) -> None:
        """QualityState is immutable — assignments after construction raise."""
        state = QualityState(baseline_sha="sha1")
        with pytest.raises(ValidationError):
            state.baseline_sha = "sha2"  # type: ignore[misc]

    def test_extra_fields_are_forbidden(self) -> None:
        """extra='forbid' enforced — unknown fields raise ValidationError."""
        with pytest.raises(ValidationError):
            QualityState(unknown_field="oops")  # type: ignore[call-arg]

    def test_instances_with_same_values_are_equal(self) -> None:
        """Two QualityState instances with the same field values compare equal."""
        a = QualityState(baseline_sha="abc", failed_files=["x.py"])
        b = QualityState(baseline_sha="abc", failed_files=["x.py"])
        assert a == b

    def test_baseline_sha_none_accepted(self) -> None:
        """baseline_sha=None is explicitly accepted."""
        state = QualityState(baseline_sha=None)
        assert state.baseline_sha is None
