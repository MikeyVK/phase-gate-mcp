# tests/mcp_server/unit/config/test_workflow_config_c6.py
# template=unit_test version=manual created=2026-05-03T00:00Z updated=
"""
Unit tests for C6 (issue #271): WorkflowTemplate cleanup + validator inversion.

Verifies:
- WorkflowTemplate.phases field is removed (contracts.yaml is SSOT for phase ordering)
- WorkflowConfig.get_first_phase / validate_transition methods are removed
- WorkflowConfig.has_workflow + get_workflow still work (catalog role unchanged)
- Validator raises ConfigError when contracts.yaml phase is absent from workphases.yaml
- server.py integration: ContractsConfig wired through full stack

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.config.schemas, mcp_server.config.validator]
"""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from mcp_server.config.schemas.contracts_config import (
    ContractsConfig,
    MergePolicy,
    WorkflowEntry,
    WorkflowPhaseEntry,
)
from mcp_server.config.schemas.workflows import WorkflowTemplate
from mcp_server.config.schemas.workphases import PhaseDefinition
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.exceptions import ConfigError
from mcp_server.schemas import (
    ArtifactRegistryConfig,
    OperationPoliciesConfig,
    ProjectStructureConfig,
    WorkflowConfig,
    WorkphasesConfig,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _workphases(phases: list[str]) -> WorkphasesConfig:
    phase_dict: dict[str, PhaseDefinition] = {}
    for p in phases:
        is_terminal = p == "ready"
        phase_dict[p] = PhaseDefinition(
            display_name=p.capitalize(),
            terminal=is_terminal,
        )
    return WorkphasesConfig(version="1.0", phases=phase_dict)


def _contracts(workflow_phases: list[str], pr_allowed_phase: str = "ready") -> ContractsConfig:
    phases = [WorkflowPhaseEntry(name=p) for p in workflow_phases]
    return ContractsConfig(
        merge_policy=MergePolicy(pr_allowed_phase=pr_allowed_phase),
        workflows={"feature": WorkflowEntry(phases=phases)},
    )


def _minimal_workflow_config() -> WorkflowConfig:
    """WorkflowConfig without phases (post-C6 format)."""
    return WorkflowConfig(
        version="1.0",
        workflows={
            "feature": WorkflowTemplate(
                name="feature",
                description="Feature workflow",
                default_execution_mode="interactive",
            )
        },
    )


def _stub_validate_startup_args(
    contracts: ContractsConfig,
    workphases: WorkphasesConfig,
) -> dict[str, Any]:
    return {
        "policies": OperationPoliciesConfig(version="1.0", operations={}),  # type: ignore[call-arg]
        "workflow": _minimal_workflow_config(),
        "structure": ProjectStructureConfig(version="1.0", directories={}),  # type: ignore[call-arg]
        "artifact": ArtifactRegistryConfig(version="1.0", artifact_types=[]),
        "contracts": contracts,
        "workphases": workphases,
    }


# ---------------------------------------------------------------------------
# WorkflowTemplate cleanup
# ---------------------------------------------------------------------------


class TestWorkflowTemplateCleanup:
    """C6: WorkflowTemplate.phases must be removed (contracts.yaml is the SSOT)."""

    def test_phases_field_does_not_exist(self) -> None:
        """WorkflowTemplate must not have a 'phases' field after C6 cleanup."""
        assert "phases" not in WorkflowTemplate.model_fields, (
            "WorkflowTemplate.phases must be removed in C6 — "
            "phase ordering lives in contracts.yaml, not workflows.yaml"
        )

    def test_workflow_template_valid_without_phases(self) -> None:
        """WorkflowTemplate can be constructed without phases after C6."""
        wt = WorkflowTemplate(
            name="feature",
            description="Feature workflow",
            default_execution_mode="interactive",
        )
        assert wt.name == "feature"

    def test_workflow_template_rejects_phases_as_extra_field(self) -> None:
        """WorkflowTemplate rejects 'phases' as an extra field (extra='forbid' enforcement)."""
        with pytest.raises(ValidationError):
            WorkflowTemplate(  # type: ignore[call-arg]
                name="feature",
                description="Feature workflow",
                default_execution_mode="interactive",
                phases=["research"],
            )


# ---------------------------------------------------------------------------
# WorkflowConfig cleanup
# ---------------------------------------------------------------------------


class TestWorkflowConfigCleanup:
    """C6: WorkflowConfig.get_first_phase and validate_transition must be removed."""

    def test_get_first_phase_does_not_exist(self) -> None:
        """WorkflowConfig.get_first_phase must not exist after C6 cleanup."""
        assert not hasattr(WorkflowConfig, "get_first_phase"), (
            "WorkflowConfig.get_first_phase must be removed in C6 — "
            "use ContractsConfig.get_first_phase instead"
        )

    def test_validate_transition_does_not_exist(self) -> None:
        """WorkflowConfig.validate_transition must not exist after C6 cleanup."""
        assert not hasattr(WorkflowConfig, "validate_transition"), (
            "WorkflowConfig.validate_transition must be removed in C6 — "
            "use ContractsConfig.validate_transition instead"
        )

    def test_has_workflow_still_exists(self) -> None:
        """WorkflowConfig.has_workflow catalog method must remain after C6."""
        config = _minimal_workflow_config()
        assert config.has_workflow("feature") is True
        assert config.has_workflow("nonexistent") is False

    def test_get_workflow_still_exists_and_returns_metadata(self) -> None:
        """WorkflowConfig.get_workflow catalog method must remain and return WorkflowTemplate."""
        config = _minimal_workflow_config()
        wt = config.get_workflow("feature")
        assert isinstance(wt, WorkflowTemplate)
        assert wt.name == "feature"
        assert wt.description == "Feature workflow"


# ---------------------------------------------------------------------------
# Validator inversion (D7)
# ---------------------------------------------------------------------------


class TestValidatorInversion:
    """C6 D7: startup validator checks contracts.yaml phases against workphases catalog."""

    def test_phase_in_contracts_missing_from_workphases_raises_config_error(self) -> None:
        """ConfigError when contracts.yaml references a phase absent from workphases.yaml."""
        contracts = _contracts(["research", "implementation", "ready"])
        # workphases only knows 'ready' — misses 'research' and 'implementation'
        workphases = _workphases(["ready"])

        args = _stub_validate_startup_args(contracts, workphases)
        with pytest.raises(ConfigError, match="research|implementation"):
            ConfigValidator().validate_startup(**args)  # type: ignore[arg-type]

    def test_all_phases_present_in_workphases_passes(self) -> None:
        """No error when all contracts.yaml phases exist in workphases.yaml."""
        phases = ["research", "implementation", "ready"]
        contracts = _contracts(phases)
        workphases = _workphases(phases)

        args = _stub_validate_startup_args(contracts, workphases)
        ConfigValidator().validate_startup(**args)  # type: ignore[arg-type]
