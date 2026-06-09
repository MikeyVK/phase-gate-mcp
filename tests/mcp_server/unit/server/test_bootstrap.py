# tests\mcp_server\unit\server\test_bootstrap.py
# template=unit_test version=3d15d309 created=2026-06-09T09:48Z updated=
"""Unit tests for mcp_server.bootstrap.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.bootstrap, unittest.mock]
@responsibilities:
    - Test TestBootstrap functionality
    - Verify immutability of ConfigLayer and ManagerGraph
"""

import dataclasses
from unittest.mock import MagicMock

import pytest

from mcp_server.bootstrap import ConfigLayer, ManagerGraph
from mcp_server.config.schemas import (
    ArtifactRegistryConfig,
    ContractsConfig,
    ContributorConfig,
    EnforcementConfig,
    GitConfig,
    IssueConfig,
    LabelConfig,
    MilestoneConfig,
    OperationPoliciesConfig,
    ProjectStructureConfig,
    QualityConfig,
    ScopeConfig,
    WorkflowConfig,
    WorkphasesConfig,
)
from mcp_server.managers.artifact_manager import ArtifactManager
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.managers.git_manager import GitManager
from mcp_server.managers.github_manager import GitHubManager
from mcp_server.managers.phase_contract_resolver import PhaseContractResolver
from mcp_server.managers.phase_state_engine import PhaseStateEngine
from mcp_server.managers.project_manager import ProjectManager
from mcp_server.managers.qa_manager import QAManager
from mcp_server.managers.quality_state_repository import FileQualityStateRepository
from mcp_server.managers.state_reconstructor import StateReconstructor
from mcp_server.managers.state_repository import FileStateRepository
from mcp_server.managers.workflow_gate_runner import WorkflowGateRunner
from mcp_server.managers.workflow_state_mutator import WorkflowStateMutator
from mcp_server.managers.workflow_status_resolver import WorkflowStatusResolver
from mcp_server.scaffolding.template_registry import TemplateRegistry
from mcp_server.state.context_loaded_cache import ContextLoadedCache
from mcp_server.state.pr_status_cache import PRStatusCache


class TestBootstrap:
    """Test suite for bootstrap containers."""

    def test_config_layer_immutability(self) -> None:
        """Verify ConfigLayer is frozen and raises FrozenInstanceError on modification."""
        mock_configs = {
            "git_config": MagicMock(spec=GitConfig),
            "workflow_config": MagicMock(spec=WorkflowConfig),
            "workphases_config": MagicMock(spec=WorkphasesConfig),
            "quality_config": MagicMock(spec=QualityConfig),
            "label_config": MagicMock(spec=LabelConfig),
            "issue_config": MagicMock(spec=IssueConfig),
            "scope_config": MagicMock(spec=ScopeConfig),
            "milestone_config": MagicMock(spec=MilestoneConfig),
            "contributor_config": MagicMock(spec=ContributorConfig),
            "artifact_registry": MagicMock(spec=ArtifactRegistryConfig),
            "project_structure_config": MagicMock(spec=ProjectStructureConfig),
            "operation_policies_config": MagicMock(spec=OperationPoliciesConfig),
            "enforcement_config": MagicMock(spec=EnforcementConfig),
            "contracts_config": MagicMock(spec=ContractsConfig),
        }
        layer = ConfigLayer(**mock_configs)

        # Assert all fields are set
        for k, v in mock_configs.items():
            assert getattr(layer, k) is v

        # Assert mutation raises FrozenInstanceError
        with pytest.raises(dataclasses.FrozenInstanceError):
            layer.git_config = MagicMock(spec=GitConfig)

    def test_manager_graph_immutability(self) -> None:
        """Verify ManagerGraph is frozen and raises FrozenInstanceError on modification."""
        mock_managers = {
            "template_registry": MagicMock(spec=TemplateRegistry),
            "git_manager": MagicMock(spec=GitManager),
            "state_repository": MagicMock(spec=FileStateRepository),
            "workflow_status_resolver": MagicMock(spec=WorkflowStatusResolver),
            "project_manager": MagicMock(spec=ProjectManager),
            "phase_contract_resolver": MagicMock(spec=PhaseContractResolver),
            "workflow_gate_runner": MagicMock(spec=WorkflowGateRunner),
            "state_reconstructor": MagicMock(spec=StateReconstructor),
            "workflow_state_mutator": MagicMock(spec=WorkflowStateMutator),
            "context_loaded_cache": MagicMock(spec=ContextLoadedCache),
            "phase_state_engine": MagicMock(spec=PhaseStateEngine),
            "quality_state_repository": MagicMock(spec=FileQualityStateRepository),
            "qa_manager": MagicMock(spec=QAManager),
            "github_manager": MagicMock(spec=GitHubManager),
            "artifact_manager": MagicMock(spec=ArtifactManager),
            "pr_status_cache": MagicMock(spec=PRStatusCache),
            "enforcement_runner": MagicMock(spec=EnforcementRunner),
        }
        graph = ManagerGraph(**mock_managers)

        # Assert all fields are set
        for k, v in mock_managers.items():
            assert getattr(graph, k) is v

        # Assert mutation raises FrozenInstanceError
        with pytest.raises(dataclasses.FrozenInstanceError):
            graph.git_manager = MagicMock(spec=GitManager)
