# tests\mcp_server\unit\managers\test_phase_contract_resolver_c3.py
# template=unit_test version=3d15d309 created=2026-05-02T18:35Z updated=
"""
Unit tests for mcp_server.managers.phase_contract_resolver.

Unit tests for PhaseConfigContext contracts field rename (issue #271 C3)

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.managers.phase_contract_resolver]
@responsibilities:
    - PhaseConfigContext accepts contracts: ContractsConfig (field renamed)
    - PhaseConfigContext.phase_contracts field no longer exists
    - PhaseContractResolver resolves via contracts field
    - _PHASE_CONTRACTS_DISPLAY_PATH constant equals '.st3/config/contracts.yaml'
"""

# Standard library
import importlib

# Project modules
from mcp_server.config.schemas.contracts_config import (
    BranchLocalArtifact,
    ContractsConfig,
    MergePolicy,
    WorkflowEntry,
    WorkflowPhaseEntry,
)
from mcp_server.config.schemas.workphases import PhaseDefinition, WorkphasesConfig
from mcp_server.managers.phase_contract_resolver import PhaseConfigContext, PhaseContractResolver


def _minimal_contracts() -> ContractsConfig:
    return ContractsConfig(
        merge_policy=MergePolicy(
            pr_allowed_phase="ready",
            branch_local_artifacts=[
                BranchLocalArtifact(path=".st3/state.json", reason="branch-local")
            ],
        ),
        workflows={
            "feature": WorkflowEntry(
                phases=[
                    WorkflowPhaseEntry(name="research"),
                    WorkflowPhaseEntry(name="ready"),
                ]
            )
        },
    )


def _minimal_workphases() -> WorkphasesConfig:
    return WorkphasesConfig(
        version="1.0",
        phases={
            "research": PhaseDefinition(display_name="Research"),
            "ready": PhaseDefinition(display_name="Ready", terminal=True),
        },
    )


class TestPhaseConfigContextContractsField:
    def test_contracts_field_accepts_contracts_config(self) -> None:
        """PhaseConfigContext must accept contracts: ContractsConfig."""
        ctx = PhaseConfigContext(
            workphases=_minimal_workphases(),
            contracts=_minimal_contracts(),
        )
        assert ctx.contracts == _minimal_contracts()

    def test_phase_contracts_field_does_not_exist(self) -> None:
        """PhaseConfigContext must NOT have a phase_contracts field."""
        ctx = PhaseConfigContext(
            workphases=_minimal_workphases(),
            contracts=_minimal_contracts(),
        )
        assert not hasattr(ctx, "phase_contracts")


class TestPhaseContractResolverUsesContracts:
    def test_resolver_resolves_via_contracts_field(self) -> None:
        """PhaseContractResolver must resolve phase checks via the contracts field."""
        ctx = PhaseConfigContext(
            workphases=_minimal_workphases(),
            contracts=_minimal_contracts(),
        )
        resolver = PhaseContractResolver(ctx)
        result = resolver.resolve(workflow_name="feature", phase="research", cycle_number=None)
        assert isinstance(result, list)


class TestPhaseContractsDisplayPath:
    def test_display_path_equals_contracts_yaml(self) -> None:
        """_PHASE_CONTRACTS_DISPLAY_PATH must equal '.st3/config/contracts.yaml'."""
        module = importlib.import_module("mcp_server.managers.phase_contract_resolver")
        assert module._PHASE_CONTRACTS_DISPLAY_PATH == ".st3/config/contracts.yaml"  # noqa: SLF001
