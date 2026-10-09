"""Behavior coverage for configured scope encoding and vocabulary admission."""

import pytest

from mcp_server.config.schemas.workphases import WorkphasesConfig
from mcp_server.core.scope_contract import ScopeContract
from mcp_server.core.scope_encoder import ScopeEncoder


@pytest.fixture
def encoder() -> ScopeEncoder:
    """Use an in-memory vocabulary with optional configured subphases."""
    config = WorkphasesConfig.model_validate(
        {
            "phases": {
                "research": {},
                "implementation": {"subphases": ["red", "green", "refactor"]},
                "ready": {"terminal": True},
            }
        }
    )
    return ScopeEncoder(ScopeContract(config))


@pytest.mark.parametrize(
    ("phase", "subphase", "cycle", "expected"),
    [
        ("research", None, None, "P_RESEARCH"),
        ("implementation", "red", None, "P_IMPLEMENTATION_SP_RED"),
        ("implementation", None, 2, "P_IMPLEMENTATION_C2"),
        ("implementation", "green", 2, "P_IMPLEMENTATION_C2_SP_GREEN"),
        ("Implementation", "GREEN", 2, "P_IMPLEMENTATION_C2_SP_GREEN"),
    ],
)
def test_encode_optional_fields(
    encoder: ScopeEncoder,
    phase: str,
    subphase: str | None,
    cycle: int | None,
    expected: str,
) -> None:
    """Each independent optional field contributes to the emitted scope."""
    assert encoder.generate_scope(phase, subphase, cycle) == expected


@pytest.mark.parametrize(
    ("phase", "subphase"),
    [("absent", None), ("implementation", "absent"), ("research", "red")],
)
def test_reject_values_outside_config(
    encoder: ScopeEncoder, phase: str, subphase: str | None
) -> None:
    """Unconfigured semantic values cannot produce a scope."""
    with pytest.raises(ValueError):
        encoder.generate_scope(phase, subphase)


@pytest.mark.parametrize("cycle", [0, -1, True])
def test_cycle_must_be_positive_integer(encoder: ScopeEncoder, cycle: int) -> None:
    """A cycle cannot be zero, negative or a boolean."""
    with pytest.raises(ValueError):
        encoder.generate_scope("implementation", cycle_number=cycle)


@pytest.mark.parametrize(
    "phases",
    [
        {"build": {}, "BUILD": {}, "done": {"terminal": True}},
        {"build": {"subphases": ["green", "GREEN"]}, "done": {"terminal": True}},
        {"build_C2": {}, "done": {"terminal": True}},
        {"build_SP_green": {}, "done": {"terminal": True}},
        {"build": {"subphases": ["green_SP_extra"]}, "done": {"terminal": True}},
    ],
)
def test_config_rejects_ambiguous_scope_vocabulary(phases: dict[str, object]) -> None:
    """Ambiguous normalized names and reserved delimiters fail at config admission."""
    with pytest.raises(ValueError):
        WorkphasesConfig.model_validate({"phases": phases})
