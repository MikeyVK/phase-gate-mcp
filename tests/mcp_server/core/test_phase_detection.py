"""Public behavior coverage for lossless configured commit-scope decoding."""

from dataclasses import FrozenInstanceError

import pytest

from mcp_server.config.schemas.workphases import WorkphasesConfig
from mcp_server.core.phase_detection import ScopeDecoder
from mcp_server.core.scope_contract import ScopeContract
from mcp_server.core.scope_encoder import ScopeEncoder


@pytest.fixture
def contract() -> ScopeContract:
    """Use nonstandard canonical names to prove configured vocabulary is authoritative."""
    config = WorkphasesConfig.model_validate(
        {
            "phases": {
                "Build_Code": {"subphases": ["Check_Types", "Ship"]},
                "Review": {},
                "Done": {"terminal": True},
            }
        }
    )
    return ScopeContract(config)


@pytest.mark.parametrize(
    ("cycle", "subphase"), [(None, None), (None, "Ship"), (3, None), (3, "Check_Types")]
)
def test_round_trip_preserves_configured_names_and_optional_fields(
    contract: ScopeContract, cycle: int | None, subphase: str | None
) -> None:
    """Decoding reproduces canonical configured names and the distinct cycle."""
    scope = ScopeEncoder(contract).generate_scope("build_code", subphase, cycle)
    result = ScopeDecoder(contract).detect_phase(f"feat({scope}): apply change")
    assert result.workflow_phase == "Build_Code"
    assert result.cycle_number == cycle
    assert result.sub_phase == subphase
    assert result.source == "commit-scope"
    assert result.confidence == "high"
    assert result.raw_scope == scope
    assert result.error_code is None


@pytest.mark.parametrize(
    ("message", "code"),
    [
        (None, "scope_input_missing"),
        ("", "scope_input_missing"),
        ("feat: apply change", "commit_scope_missing"),
        ("feat(P_BUILD_CODE_C0): apply change", "commit_scope_invalid"),
        ("feat(P_UNKNOWN): apply change", "commit_scope_invalid"),
        ("feat(P_BUILD_CODE_SP_ABSENT): apply change", "commit_scope_invalid"),
    ],
)
def test_unknown_has_no_guessed_fields(
    contract: ScopeContract, message: str | None, code: str
) -> None:
    """Missing or invalid scope produces machine-readable uncertainty."""
    result = ScopeDecoder(contract).detect_phase(message)
    assert result.workflow_phase is None
    assert result.cycle_number is None
    assert result.sub_phase is None
    assert result.source == "unknown"
    assert result.confidence == "unknown"
    assert result.error_code == code


def test_detection_result_is_immutable(contract: ScopeContract) -> None:
    """A consumer cannot mutate interpreted Git evidence."""
    result = ScopeDecoder(contract).detect_phase("docs(P_REVIEW): review")
    with pytest.raises(FrozenInstanceError):
        result.workflow_phase = "Build_Code"
    assert result.workflow_phase == "Review"
