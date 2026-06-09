# tests\mcp_server\unit\server\test_bootstrap.py
# template=unit_test version=3d15d309 created=2026-06-09T09:48Z updated=
"""Unit tests for mcp_server.bootstrap.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.bootstrap, unittest.mock]
@responsibilities:
    - Test TestBootstrap functionality
    - Verify immutability of ConfigLayer and ManagerGraph
    - Test ServerBootstrapper config loading and manager creation
"""

import dataclasses
from unittest.mock import MagicMock, patch

import pytest

from mcp_server.bootstrap import ConfigLayer, ManagerGraph, ServerBootstrapper
from mcp_server.server import MCPServer
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


class TestServerBootstrapperConfigsAndManagers:
    """Test suite for ServerBootstrapper config loading and manager creation."""

    def test_bootstrapper_initialization(self) -> None:
        """Verify ServerBootstrapper can be initialized with Settings."""
        mock_settings = MagicMock()
        bootstrapper = ServerBootstrapper(mock_settings)
        assert bootstrapper._settings is mock_settings  # pyright: ignore[reportPrivateUsage]

    def test_bootstrapper_bootstrap_returns_mcpserver(self) -> None:
        """Verify bootstrap() returns an MCPServer with all managers wired."""
        mock_settings = MagicMock()
        mock_settings.github.token = None
        mock_settings.server.name = "test-server"
        mock_settings.server.workspace_root = "/fake/root"
        mock_settings.server.server_root_dir = ".phase-gate"
        mock_settings.server.logs_dir = "logs"
        mock_settings.logging.level = "WARNING"
        mock_settings.logging.audit_log = "/fake/root/.phase-gate/logs/mcp_audit.log"
        mock_config_layer = MagicMock()
        mock_manager_graph = MagicMock()
        with (
            patch("mcp_server.bootstrap.setup_logging") as mock_setup_logging,
            patch("mcp_server.bootstrap.TemplateRegistry") as mock_template_registry_cls,
            patch("mcp_server.bootstrap.ConfigLoader"),
            patch("mcp_server.bootstrap.ConfigValidator"),
            patch("mcp_server.server.MCPServer") as mock_mcp_server_cls,
        ):
            bootstrapper = ServerBootstrapper(mock_settings)

            # Mock the building methods
            bootstrapper._build_config_layer = MagicMock(return_value=mock_config_layer)  # pyright: ignore[reportPrivateUsage]
            bootstrapper._build_manager_graph = MagicMock(return_value=mock_manager_graph)  # pyright: ignore[reportPrivateUsage]

            server = bootstrapper.bootstrap()

            # Verify side-effects
            mock_setup_logging.assert_called_once()
            mock_template_registry_cls.assert_called_once()

            # Verify building methods were called
            bootstrapper._build_config_layer.assert_called_once()  # pyright: ignore[reportPrivateUsage]
            bootstrapper._build_manager_graph.assert_called_once()  # pyright: ignore[reportPrivateUsage]
            # Verify MCPServer was created with injected dependencies
            assert mock_mcp_server_cls.called
            call_kwargs = mock_mcp_server_cls.call_args[1]
            assert call_kwargs["settings"] is mock_settings
            assert call_kwargs["configs"] is mock_config_layer
            assert call_kwargs["managers"] is mock_manager_graph
            assert server is mock_mcp_server_cls.return_value

    def test_build_config_layer(self) -> None:
        """Verify _build_config_layer builds a valid ConfigLayer."""
        mock_settings = MagicMock()
        mock_settings.server.workspace_root = "/fake/root"
        mock_settings.server.server_root_dir = ".phase-gate"

        bootstrapper = ServerBootstrapper(mock_settings)

        with (
            patch("mcp_server.bootstrap.ConfigLoader") as mock_config_loader_cls,
            patch("mcp_server.bootstrap.ConfigValidator") as mock_config_validator_cls,
        ):
            mock_loader = mock_config_loader_cls.return_value
            mock_loader.load_git_config.return_value = MagicMock(spec=GitConfig)
            mock_loader.load_workflow_config.return_value = MagicMock(spec=WorkflowConfig)
            mock_loader.load_workphases_config.return_value = MagicMock(spec=WorkphasesConfig)
            mock_loader.load_quality_config.return_value = MagicMock(spec=QualityConfig)
            mock_loader.load_label_config.return_value = MagicMock(spec=LabelConfig)
            mock_loader.load_issue_config.return_value = MagicMock(spec=IssueConfig)
            mock_loader.load_scope_config.return_value = MagicMock(spec=ScopeConfig)
            mock_loader.load_milestone_config.return_value = MagicMock(spec=MilestoneConfig)
            mock_loader.load_artifact_registry_config.return_value = MagicMock(
                spec=ArtifactRegistryConfig
            )
            mock_loader.load_project_structure_config.return_value = MagicMock(
                spec=ProjectStructureConfig
            )
            mock_loader.load_operation_policies_config.return_value = MagicMock(
                spec=OperationPoliciesConfig
            )
            mock_loader.load_enforcement_config.return_value = MagicMock(spec=EnforcementConfig)
            mock_loader.load_contracts_config.return_value = MagicMock(spec=ContractsConfig)

            layer = bootstrapper._build_config_layer()  # pyright: ignore[reportPrivateUsage]

            assert isinstance(layer, ConfigLayer)
            mock_config_validator_cls.return_value.validate_startup.assert_called_once()


class TestServerBootstrapperToolsAndResources:
    """Test suite for ServerBootstrapper tool and resource extraction."""

    def test_build_tools_without_github_token(self) -> None:
        """Verify _build_tools returns only non-GitHub tools when token is None."""
        mock_settings = MagicMock()
        mock_settings.github.token = None
        mock_settings.server.workspace_root = "/fake/root"
        mock_settings.server.server_root_dir = ".phase-gate"

        bootstrapper = ServerBootstrapper(mock_settings)
        mock_configs = MagicMock()
        mock_managers = MagicMock()

        tools = bootstrapper._build_tools(mock_configs, mock_managers)  # pyright: ignore[reportPrivateUsage]
        assert isinstance(tools, list)
        tool_names = {t.name for t in tools}
        assert "create_issue" not in tool_names
        assert "git_status" in tool_names

    def test_build_tools_with_github_token(self) -> None:
        """Verify _build_tools returns GitHub tools when token is present."""
        mock_settings = MagicMock()
        mock_settings.github.token = "token"
        mock_settings.server.workspace_root = "/fake/root"
        mock_settings.server.server_root_dir = ".phase-gate"

        bootstrapper = ServerBootstrapper(mock_settings)
        mock_configs = MagicMock()
        mock_configs.contracts_config.merge_policy.branch_local_artifacts = []
        mock_managers = MagicMock()
        tools = bootstrapper._build_tools(mock_configs, mock_managers)  # pyright: ignore[reportPrivateUsage]
        assert isinstance(tools, list)
        tool_names = {t.name for t in tools}
        assert "create_issue" in tool_names

    def test_build_resources_without_github_token(self) -> None:
        """Verify _build_resources returns only core resources when token is None."""
        mock_settings = MagicMock()
        mock_settings.github.token = None
        mock_settings.server.workspace_root = "/fake/root"
        mock_settings.server.server_root_dir = ".phase-gate"

        bootstrapper = ServerBootstrapper(mock_settings)
        mock_configs = MagicMock()
        mock_managers = MagicMock()
        resources = bootstrapper._build_resources(mock_configs, mock_managers)  # pyright: ignore[reportPrivateUsage]
        assert isinstance(resources, list)
        resource_uris = {r.uri_pattern for r in resources}
        assert "pgmcp://rules/coding_standards" in resource_uris
        assert "pgmcp://github/issues" not in resource_uris

    def test_build_resources_with_github_token(self) -> None:
        """Verify _build_resources returns GitHub issues resource when token is present."""
        mock_settings = MagicMock()
        mock_settings.github.token = "token"
        mock_settings.server.workspace_root = "/fake/root"
        mock_settings.server.server_root_dir = ".phase-gate"

        bootstrapper = ServerBootstrapper(mock_settings)
        mock_configs = MagicMock()
        mock_managers = MagicMock()
        resources = bootstrapper._build_resources(mock_configs, mock_managers)  # pyright: ignore[reportPrivateUsage]
        assert isinstance(resources, list)
        resource_uris = {r.uri_pattern for r in resources}
        assert "pgmcp://rules/coding_standards" in resource_uris
        assert "pgmcp://github/issues" in resource_uris

    def test_bootstrap_wires_tools_and_resources(self) -> None:
        """Verify bootstrap() calls _build_tools and _build_resources and injects them."""
        mock_settings = MagicMock()
        mock_settings.server.name = "test-server"
        mock_settings.server.workspace_root = "/fake/root"
        mock_settings.server.server_root_dir = ".phase-gate"
        mock_settings.server.logs_dir = "logs"
        mock_settings.logging.level = "WARNING"
        mock_settings.logging.audit_log = "/fake/root/.phase-gate/logs/mcp_audit.log"

        mock_config_layer = MagicMock()
        mock_manager_graph = MagicMock()
        mock_tools = [MagicMock()]
        mock_resources = [MagicMock()]

        with (
            patch("mcp_server.bootstrap.setup_logging"),
            patch("mcp_server.bootstrap.TemplateRegistry"),
            patch("mcp_server.bootstrap.ConfigLoader"),
            patch("mcp_server.bootstrap.ConfigValidator"),
            patch("mcp_server.server.MCPServer") as mock_mcp_server_cls,
        ):
            bootstrapper = ServerBootstrapper(mock_settings)
            bootstrapper._build_config_layer = MagicMock(return_value=mock_config_layer)  # pyright: ignore[reportPrivateUsage]
            bootstrapper._build_manager_graph = MagicMock(return_value=mock_manager_graph)  # pyright: ignore[reportPrivateUsage]
            bootstrapper._build_tools = MagicMock(return_value=mock_tools)  # pyright: ignore[reportPrivateUsage]
            bootstrapper._build_resources = MagicMock(return_value=mock_resources)  # pyright: ignore[reportPrivateUsage]

            server = bootstrapper.bootstrap()

            bootstrapper._build_tools.assert_called_once_with(mock_config_layer, mock_manager_graph)  # pyright: ignore[reportPrivateUsage]
            bootstrapper._build_resources.assert_called_once_with(  # pyright: ignore[reportPrivateUsage]
                mock_config_layer, mock_manager_graph
            )

            mock_mcp_server_cls.assert_called_once_with(
                settings=mock_settings,
                configs=mock_config_layer,
                managers=mock_manager_graph,
                tools=mock_tools,
                resources=mock_resources,
            )
            assert server is mock_mcp_server_cls.return_value


class TestMCPServerBootstrap:
    """Test suite for MCPServer dependency injection requirements."""

    def test_mcp_server_requires_injected_dependencies(self) -> None:
        """Verify that MCPServer raises TypeError when initialized without dependencies."""
        mock_settings = MagicMock()
        # Once the fallback code is deleted, this must raise a TypeError (missing required arguments)
        with pytest.raises(TypeError):
            MCPServer(settings=mock_settings)  # type: ignore[call-arg]

    def test_mcp_server_accepts_injected_dependencies(self) -> None:
        """Verify MCPServer successfully initializes with all dependencies injected."""
        mock_settings = MagicMock()
        mock_configs = MagicMock()
        mock_managers = MagicMock()
        mock_tools = []
        mock_resources = []

        server = MCPServer(
            settings=mock_settings,
            configs=mock_configs,
            managers=mock_managers,
            tools=mock_tools,
            resources=mock_resources,
        )
        assert server._settings is mock_settings
        assert server.tools is mock_tools
        assert server.resources is mock_resources

    def test_make_test_server_creates_valid_server(self) -> None:
        """Verify make_test_server helper creates a valid MCPServer instance."""
        from tests.mcp_server.test_support import make_test_server

        server = make_test_server()
        assert isinstance(server, MCPServer)
        assert server.tools is not None
        assert server.resources is not None
