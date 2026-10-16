"""Behavior tests for identified, ranked workflow contracts."""

import pytest
from pydantic import ValidationError

from mcp_server.config.schemas.contracts_config import (
    ContractsConfig,
    MergePolicy,
    PhaseInstructionsSpec,
    WorkflowEntry,
    WorkflowPhaseEntry,
)

_INSTRUCTIONS = PhaseInstructionsSpec(sub_role="test-role", phase_instructions="Execute phase.")


def _phase(order: int, **kwargs: object) -> WorkflowPhaseEntry:
    return WorkflowPhaseEntry(order=order, instructions=_INSTRUCTIONS, **kwargs)  # type: ignore[arg-type]


def _contracts(phases: dict[str, WorkflowPhaseEntry], terminal: str = "ready") -> ContractsConfig:
    return ContractsConfig(
        merge_policy=MergePolicy(pr_allowed_phase=terminal),
        workflows={"sample": WorkflowEntry(phases=phases)},
    )


def test_explicit_order_drives_first_phase_and_transition() -> None:
    contracts = _contracts({"ready": _phase(30), "build": _phase(20), "draft": _phase(10)})
    assert contracts.get_first_phase("sample") == "draft"
    assert contracts.get_phases("sample") == ["draft", "build", "ready"]
    assert contracts.validate_transition("sample", "draft", "build")
    assert contracts.workflows["sample"].get_phase("build").order == 20
    with pytest.raises(ValueError, match="Invalid transition"):
        contracts.validate_transition("sample", "draft", "ready")


@pytest.mark.parametrize("unknown", ["workflow", "phase"])
def test_unknown_identifiers_report_lookup_failure(unknown: str) -> None:
    contracts = _contracts({"ready": _phase(10)})
    with pytest.raises(ValueError):
        if unknown == "workflow":
            contracts.get_phases("missing")
        else:
            contracts.workflows["sample"].get_phase("missing")


def test_terminal_validation_uses_rank_not_mapping_insertion() -> None:
    with pytest.raises(ValidationError, match="pr_allowed_phase"):
        _contracts({"ready": _phase(10), "draft": _phase(20)})


def test_cycle_owner_uses_phase_keys_and_rejects_multiple_owners() -> None:
    with pytest.raises(ValidationError, match="compose.*inspect"):
        WorkflowEntry(
            phases={
                "compose": _phase(10, cycle_based=True, commit_type_map={"build": "feat"}),
                "inspect": _phase(20, cycle_based=True, commit_type_map={"check": "test"}),
            }
        )


def test_cycle_phase_requires_commit_mapping() -> None:
    with pytest.raises(ValidationError, match="commit_type_map"):
        _phase(10, cycle_based=True)


@pytest.mark.parametrize("phases", [{}, {"": {"order": 10, "instructions": _INSTRUCTIONS}}])
def test_workflow_requires_nonempty_phase_identifiers(phases: object) -> None:
    with pytest.raises(ValidationError):
        WorkflowEntry.model_validate({"phases": phases})


@pytest.mark.parametrize("order", [None, True, "10"])
def test_phase_requires_explicit_integer_order(order: object) -> None:
    with pytest.raises(ValidationError):
        WorkflowPhaseEntry.model_validate({"order": order, "instructions": _INSTRUCTIONS})


def test_sibling_phase_order_must_be_unique() -> None:
    with pytest.raises(ValidationError, match="Duplicate"):
        WorkflowEntry(phases={"first": _phase(10), "second": _phase(10)})


def test_contract_value_objects_are_frozen() -> None:
    phase = _phase(10)
    with pytest.raises(ValidationError):
        phase.cycle_based = True  # type: ignore[misc]


def test_instructions_are_required_and_retain_handover() -> None:
    with pytest.raises(ValidationError):
        WorkflowPhaseEntry.model_validate({"order": 10})
    spec = PhaseInstructionsSpec(
        sub_role="implementer", phase_instructions="Execute.", handover_template="Review."
    )
    assert spec.handover_template == "Review."
