# tests/mcp_server/core/test_phase_detection.py
# template=unit_test version=6b0f1f7e created=2026-02-15T06:35Z updated=
"""
Unit tests for mcp_server.core.phase_detection.

Test PhaseDetectionResult TypedDict schema validation and field types

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.core.phase_detection, unittest.mock]
@responsibilities:
    - Test PhaseDetectionResult TypedDict schema
    - Verify ScopeDecoder.detect_phase() deterministic precedence
    - Cover error handling scenarios (graceful degradation)
    - Validate phase names against workphases.yaml
"""

# Third-party
# Project modules
from mcp_server.config.schemas.workphases import PhaseDefinition, WorkphasesConfig
from mcp_server.core.phase_detection import PhaseDetectionResult, ScopeDecoder

# Minimal WorkphasesConfig for unit tests — covers all phases referenced by test assertions.
_TEST_WORKPHASES = WorkphasesConfig(
    phases={
        "research": PhaseDefinition(commit_type_hint="docs"),
        "planning": PhaseDefinition(commit_type_hint="docs"),
        "design": PhaseDefinition(commit_type_hint="docs"),
        "implementation": PhaseDefinition(
            commit_type_hint=None, subphases=["red", "green", "refactor"]
        ),
        "validation": PhaseDefinition(commit_type_hint="test"),
        "documentation": PhaseDefinition(commit_type_hint="docs"),
        "coordination": PhaseDefinition(commit_type_hint="chore"),
        "ready": PhaseDefinition(commit_type_hint="chore", terminal=True),
    }
)


class TestPhaseDetectionResult:
    """Test suite for PhaseDetectionResult TypedDict schema."""

    def test_phase_detection_result_schema(self) -> None:
        """Verify PhaseDetectionResult has all 6 required fields with correct types."""
        # Arrange - Create instance using TypedDict syntax
        result: PhaseDetectionResult = {
            "workflow_phase": "implementation",
            "sub_phase": "red",
            "source": "commit-scope",
            "confidence": "high",
            "raw_scope": "P_IMPLEMENTATION_SP_RED",
            "error_message": None,
        }

        # Assert - Verify all required fields present and correct
        assert result["workflow_phase"] == "implementation"
        assert result["sub_phase"] == "red"
        assert result["source"] == "commit-scope"
        assert result["confidence"] == "high"
        assert result["raw_scope"] == "P_IMPLEMENTATION_SP_RED"
        assert result["error_message"] is None


class TestScopeDecoder:
    """Test suite for ScopeDecoder deterministic phase detection."""

    def test_parse_commit_scope_phase_only(self) -> None:
        """Parse commit scope with P_PHASE format (no subphase)."""
        # Arrange
        decoder = ScopeDecoder(_TEST_WORKPHASES)
        commit_message = "docs(P_RESEARCH): complete problem analysis"

        # Act
        result = decoder.detect_phase(commit_message)

        # Assert
        assert result["workflow_phase"] == "research"
        assert result["sub_phase"] is None
        assert result["source"] == "commit-scope"
        assert result["confidence"] == "high"
        assert result["raw_scope"] == "P_RESEARCH"
        assert result["error_message"] is None

    def test_parse_commit_scope_phase_and_subphase(self) -> None:
        """Parse commit scope with P_PHASE_SP_SUBPHASE format."""
        # Arrange
        decoder = ScopeDecoder(_TEST_WORKPHASES)
        commit_message = "test(P_IMPLEMENTATION_SP_RED): add user validation tests"

        # Act
        result = decoder.detect_phase(commit_message)

        # Assert
        assert result["workflow_phase"] == "implementation"
        assert result["sub_phase"] == "red"
        assert result["source"] == "commit-scope"
        assert result["confidence"] == "high"
        assert result["raw_scope"] == "P_IMPLEMENTATION_SP_RED"
        assert result["error_message"] is None

    def test_unknown_error_message_contains_recovery_steps(self) -> None:
        """Verify unknown fallback includes actionable recovery instructions."""
        # Arrange
        decoder = ScopeDecoder(_TEST_WORKPHASES)
        commit_message = None  # No commit message

        # Act
        result = decoder.detect_phase(commit_message)

        # Assert - error message has recovery steps
        assert result["error_message"] is not None
        assert "Phase detection failed" in result["error_message"]
        assert "transition_phase" in result["error_message"]
        assert "type(P_PHASE): message" in result["error_message"]
        assert "research, planning, design, implementation" in result["error_message"]

    def test_validate_commit_scope_accepts_valid_phases(self) -> None:
        """Valid phase in commit-scope should be accepted."""
        # Arrange - valid phases from workphases.yaml
        valid_commits = [
            ("docs(P_RESEARCH): research", "research"),
            ("chore(P_PLANNING): planning", "planning"),
            ("docs(P_DESIGN): design", "design"),
            ("test(P_IMPLEMENTATION_SP_RED): implementation test", "implementation"),
            ("test(P_VALIDATION): validation", "validation"),
            ("docs(P_DOCUMENTATION): docs", "documentation"),
            ("chore(P_COORDINATION): coordination", "coordination"),
        ]

        decoder = ScopeDecoder(_TEST_WORKPHASES)

        for commit, expected_phase in valid_commits:
            # Act
            result = decoder.detect_phase(commit)

            # Assert - valid phase accepted with high confidence
            assert result["workflow_phase"] == expected_phase
            assert result["source"] == "commit-scope"
            assert result["confidence"] == "high"
