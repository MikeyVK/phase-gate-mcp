# tests/mcp_server/unit/config/test_contracts_config.py
"""
Unit tests for mcp_server.config.schemas.contracts_config.

Tests for issue #271 C1: ContractsConfig, WorkflowEntry, WorkflowPhaseEntry,
PhaseContractPhase (frozen+extra='forbid'), and import path enforcement.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.config.schemas.contracts_config]
"""

from __future__ import annotations

import importlib

import pytest
from pydantic import ValidationError

from mcp_server.config.schemas.contracts_config import (
    ContractsConfig,
    MergePolicy,
    PhaseContractPhase,
    PhaseInstructionsSpec,
    WorkflowEntry,
    WorkflowPhaseEntry,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _policy(phase: str = "ready") -> MergePolicy:
    return MergePolicy(pr_allowed_phase=phase, branch_local_artifacts=[])


_STUB_INSTRUCTIONS = PhaseInstructionsSpec(
    sub_role="test-role",
    phase_instructions="Test phase instructions.",
    handover_template="Test handover template.",
)


def _wpe(name: str, **kwargs: object) -> WorkflowPhaseEntry:
    if "instructions" not in kwargs:
        kwargs["instructions"] = _STUB_INSTRUCTIONS
    return WorkflowPhaseEntry(name=name, **kwargs)  # type: ignore[arg-type]


def _minimal_config(*phase_names: str) -> ContractsConfig:
    """Build a ContractsConfig with a single 'test' workflow containing given phases."""
    phases = [_wpe(n) for n in phase_names]
    return ContractsConfig(
        merge_policy=_policy(phase_names[-1]),
        workflows={"test": WorkflowEntry(phases=phases)},
    )


# ---------------------------------------------------------------------------
# PhaseContractPhase — frozen + extra='forbid'
# ---------------------------------------------------------------------------


class TestPhaseContractPhaseFrozen:
    def test_assignment_raises(self) -> None:
        """PhaseContractPhase is frozen: attribute assignment must raise."""
        phase = PhaseContractPhase()
        with pytest.raises((ValidationError, TypeError)):
            phase.cycle_based = True  # type: ignore[misc]

    def test_extra_field_rejected(self) -> None:
        """extra='forbid': unknown field must raise ValidationError."""
        with pytest.raises(ValidationError):
            PhaseContractPhase(unknown_field="x")  # type: ignore[call-arg]

    def test_cycle_based_requires_commit_type_map(self) -> None:
        """Existing model_validator: cycle_based=True + empty commit_type_map → ValueError."""
        with pytest.raises(ValidationError, match="commit_type_map"):
            PhaseContractPhase(cycle_based=True)


# ---------------------------------------------------------------------------
# WorkflowPhaseEntry — inherits frozen + extra='forbid'
# ---------------------------------------------------------------------------


class TestWorkflowPhaseEntry:
    def test_inherits_frozen(self) -> None:
        entry = _wpe("research")
        with pytest.raises((ValidationError, TypeError)):
            entry.name = "other"  # type: ignore[misc]

    def test_name_required(self) -> None:
        """name is required; omitting it must raise ValidationError."""
        with pytest.raises(ValidationError):
            WorkflowPhaseEntry()  # type: ignore[call-arg]

    def test_generic_cycle_based_any_name(self) -> None:
        """Schema must not contain a fasename-check on 'implementation'.
        A phase named 'research' with cycle_based=True and subphases must be valid."""
        entry = _wpe(
            "research",
            cycle_based=True,
            subphases=["explore", "consolidate"],
            commit_type_map={"explore": "docs", "consolidate": "docs"},
        )
        assert entry.name == "research"
        assert entry.cycle_based is True
        assert entry.subphases == ["explore", "consolidate"]


# ---------------------------------------------------------------------------
# WorkflowEntry
# ---------------------------------------------------------------------------


class TestWorkflowEntry:
    def test_extra_field_rejected(self) -> None:
        phases = [_wpe("research"), _wpe("ready")]
        with pytest.raises(ValidationError):
            WorkflowEntry(phases=phases, unknown="x")  # type: ignore[call-arg]

    def test_frozen(self) -> None:
        phases = [_wpe("research"), _wpe("ready")]
        entry = WorkflowEntry(phases=phases)
        with pytest.raises((ValidationError, TypeError)):
            entry.phases = []  # type: ignore[misc]

    def test_phases_min_length_one(self) -> None:
        with pytest.raises(ValidationError):
            WorkflowEntry(phases=[])


# ---------------------------------------------------------------------------
# ContractsConfig — model_validator
# ---------------------------------------------------------------------------


class TestContractsConfigModelValidator:
    def test_last_phase_must_match_pr_allowed_phase(self) -> None:
        """model_validator must reject when last phase != merge_policy.pr_allowed_phase."""
        phases = [_wpe("research"), _wpe("implementation"), _wpe("ready")]
        with pytest.raises(ValidationError, match="pr_allowed_phase"):
            ContractsConfig(
                merge_policy=_policy("ready"),
                workflows={"feature": WorkflowEntry(phases=phases[:-1])},  # missing ready
            )

    def test_validator_error_message_contains_workflow_name(self) -> None:
        """Error message must contain the offending workflow name."""
        phases = [_wpe("research"), _wpe("done")]
        with pytest.raises(ValidationError) as exc_info:
            ContractsConfig(
                merge_policy=_policy("ready"),
                workflows={"my_wf": WorkflowEntry(phases=phases)},
            )
        assert "my_wf" in str(exc_info.value)


# ---------------------------------------------------------------------------
# ContractsConfig — API methods
# ---------------------------------------------------------------------------


class TestContractsConfigGetFirstPhase:
    def test_returns_first_phase_name(self) -> None:
        cfg = _minimal_config("research", "implementation", "ready")
        assert cfg.get_first_phase("test") == "research"

    def test_unknown_workflow_raises(self) -> None:
        cfg = _minimal_config("research", "ready")
        with pytest.raises(ValueError, match="Unknown workflow"):
            cfg.get_first_phase("nonexistent")


class TestContractsConfigGetPhases:
    def test_returns_ordered_list(self) -> None:
        cfg = _minimal_config("research", "design", "implementation", "ready")
        assert cfg.get_phases("test") == ["research", "design", "implementation", "ready"]

    def test_unknown_workflow_raises(self) -> None:
        cfg = _minimal_config("research", "ready")
        with pytest.raises(ValueError, match="Unknown workflow"):
            cfg.get_phases("nonexistent")


class TestContractsConfigValidateTransition:
    def test_sequential_transition_returns_true(self) -> None:
        cfg = _minimal_config("research", "design", "ready")
        assert cfg.validate_transition("test", "research", "design") is True

    def test_non_sequential_raises(self) -> None:
        cfg = _minimal_config("research", "design", "implementation", "ready")
        with pytest.raises(ValueError, match="Invalid transition"):
            cfg.validate_transition("test", "research", "implementation")

    def test_unknown_phase_raises_with_available_list(self) -> None:
        cfg = _minimal_config("research", "ready")
        with pytest.raises(ValueError):
            cfg.validate_transition("test", "research", "unknown_phase")


# ---------------------------------------------------------------------------
# Import path enforcement
# ---------------------------------------------------------------------------


class TestImportPaths:
    def test_14_old_import_path_raises_import_error(self) -> None:
        """The old mcp_server.config.schemas.phase_contracts_config module must no
        longer exist — any import attempt must raise ImportError (C1 clean-break)."""
        with pytest.raises(ImportError):
            importlib.import_module("mcp_server.config.schemas.phase_contracts_config")

    def test_new_module_path_exports_all_public_symbols(self) -> None:
        """New module path must export all symbols needed by callers."""
        mod = importlib.import_module("mcp_server.config.schemas.contracts_config")
        for symbol in [
            "BranchLocalArtifact",
            "MergePolicy",
            "CheckSpec",
            "PhaseContractPhase",
            "WorkflowPhaseEntry",
            "WorkflowEntry",
            "ContractsConfig",
        ]:
            assert hasattr(mod, symbol), f"{symbol} missing from contracts_config"


# ---------------------------------------------------------------------------
# C6 (issue #268): PhaseInstructionsSpec schema
# ---------------------------------------------------------------------------


class TestPhaseInstructionsSpec:
    """C6: PhaseInstructionsSpec — frozen model.

    Fields: sub_role, phase_instructions, handover_template.
    """

    def test_phase_instructions_spec_parses_with_all_fields(self) -> None:
        """Valid dict with all three fields parses into PhaseInstructionsSpec."""
        spec = PhaseInstructionsSpec(
            sub_role="implementer",
            phase_instructions="1. Do TDD.\n2. Commit.",
            handover_template="### Scope\n- ...",
        )
        assert spec.sub_role == "implementer"
        assert spec.phase_instructions == "1. Do TDD.\n2. Commit."
        assert spec.handover_template == "### Scope\n- ..."

    def test_phase_instructions_spec_is_frozen(self) -> None:
        """PhaseInstructionsSpec must be frozen: attribute assignment raises."""
        spec = PhaseInstructionsSpec(
            sub_role="researcher",
            phase_instructions="read files",
            handover_template="Co \u2192 Imp",
        )
        with pytest.raises((ValidationError, TypeError)):
            spec.sub_role = "other"  # type: ignore[misc]

    def test_phase_instructions_spec_requires_sub_role_and_phase_instructions(self) -> None:
        """Only sub_role and phase_instructions are required; handover_template is optional."""
        with pytest.raises(ValidationError):
            PhaseInstructionsSpec(sub_role="researcher")  # type: ignore[call-arg]


class TestWorkflowPhaseEntryInstructions:
    """C6: WorkflowPhaseEntry.instructions optional field."""

    def test_contracts_config_loads_instructions_field(self) -> None:
        """WorkflowPhaseEntry.instructions is PhaseInstructionsSpec when present."""
        entry = WorkflowPhaseEntry(
            name="implementation",
            instructions=PhaseInstructionsSpec(
                sub_role="implementer",
                phase_instructions="Do TDD.",
                handover_template="### Scope",
            ),
        )
        assert isinstance(entry.instructions, PhaseInstructionsSpec)
        assert entry.instructions.sub_role == "implementer"

    def test_contracts_config_phase_entry_without_instructions_raises(self) -> None:
        """WorkflowPhaseEntry without instructions field must raise ValidationError.

        instructions is a required field — every defined phase must have instructions.
        Fail-Fast §4: Pydantic enforces at parse time, no post-load validator needed.
        """
        with pytest.raises(ValidationError):
            WorkflowPhaseEntry(name="research")
