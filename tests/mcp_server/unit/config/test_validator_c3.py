# tests/mcp_server/unit/config/test_validator_c3.py
# template=unit_test version=3d15d309 created=2026-04-09T19:17Z updated=
"""
Unit tests for mcp_server.config.validator.

Tests public startup cross-validation of the merge-policy phase.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.config.validator, mcp_server.schemas]
@responsibilities:
    - Test TestConfigValidatorC3 functionality
    - Verify merge policy phase validation
    - Verify merge policy cross-validation raises ConfigError for unknown phases
"""

# Standard library
from typing import Any

# Third-party
import pytest

from mcp_server.config.schemas.contracts_config import ContractsConfig, MergePolicy
from mcp_server.config.schemas.workphases import PhaseDefinition

# Project modules
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.exceptions import ConfigError
from mcp_server.schemas import (
    OperationPoliciesConfig,
    WorkflowConfig,
    WorkphasesConfig,
)


def _workphases(phases: list[str] | None = None, terminal: str = "ready") -> WorkphasesConfig:
    phase_dict: dict[str, PhaseDefinition] = {}
    for p in phases or ["planning", "implementation"]:
        phase_dict[p] = PhaseDefinition(display_name=p.capitalize())
    phase_dict[terminal] = PhaseDefinition(display_name=terminal.capitalize(), terminal=True)
    return WorkphasesConfig(version="1.0.0", phases=phase_dict)


def _contracts(pr_allowed_phase: str = "ready") -> ContractsConfig:
    return ContractsConfig(
        merge_policy=MergePolicy(pr_allowed_phase=pr_allowed_phase),
        workflows={},
    )


def _stub_validate_startup_args(
    pr_allowed_phase: str = "ready",
    workphases: WorkphasesConfig | None = None,
) -> dict[str, Any]:
    return {
        "policies": OperationPoliciesConfig(version="1.0.0", operations={}),  # type: ignore[call-arg]
        "workflow": WorkflowConfig(version="1.0.0", workflows={}),
        "contracts": _contracts(pr_allowed_phase),
        "workphases": workphases or _workphases(),
    }


class TestConfigValidatorC3:
    """Test public startup validation of merge-policy phase references."""

    def test_validate_startup_accepts_known_merge_policy_phase(self) -> None:
        """A known merge-policy phase passes startup cross-validation."""
        ConfigValidator().validate_startup(**_stub_validate_startup_args())

    def test_validate_startup_raises_for_invalid_merge_policy_phase(
        self,
    ) -> None:
        """validate_startup raises ConfigError for invalid pr_allowed_phase."""
        # Arrange
        kwargs = _stub_validate_startup_args(pr_allowed_phase="unknown_phase")

        # Act / Assert
        with pytest.raises(ConfigError, match="unknown_phase"):
            ConfigValidator().validate_startup(**kwargs)
