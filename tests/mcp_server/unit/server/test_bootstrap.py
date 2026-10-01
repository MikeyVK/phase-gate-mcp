# tests\mcp_server\unit\server\test_bootstrap.py
# template=unit_test version=3d15d309 created=2026-06-09T09:48Z updated=2026-08-19T19:50Z
"""Unit tests for mcp_server.bootstrap.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.bootstrap, unittest.mock]
@responsibilities:
    - Test TestBootstrap functionality
    - Verify immutability of ConfigLayer and ManagerGraph
    - Test target startup and tool registration
"""

import dataclasses
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel

from mcp_server.bootstrap import (
    ConfigLayer,
    ManagerGraph,
    ServerBootstrapper,
    SupportedToolContract,
    ToolAssembly,
)
from mcp_server.config.schemas import (
    ContractsConfig,
    ContributorConfig,
    EnforcementConfig,
    GitConfig,
    IssueConfig,
    LabelConfig,
    MilestoneConfig,
    OperationPoliciesConfig,
    PresentationConfig,
    ScopeConfig,
    WorkflowConfig,
    WorkphasesConfig,
)
from mcp_server.config.settings import GitHubSettings, ServerSettings, Settings
from mcp_server.core.exceptions import ConfigError
from mcp_server.core.interfaces import ICoreTool, IToolResponsePublisher
from mcp_server.core.operation_notes import NoteContext
from mcp_server.core.tool_execution import ToolExecution
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.managers.git_manager import GitManager
from mcp_server.managers.github_manager import GitHubManager
from mcp_server.managers.phase_contract_resolver import PhaseContractResolver
from mcp_server.managers.phase_state_engine import PhaseStateEngine
from mcp_server.managers.project_manager import ProjectManager
from mcp_server.managers.state_repository import FileStateRepository
from mcp_server.managers.workflow_gate_runner import WorkflowGateRunner
from mcp_server.managers.workflow_state_mutator import WorkflowStateMutator
from mcp_server.managers.workflow_status_resolver import WorkflowStatusResolver
from mcp_server.server import MCPServer
from mcp_server.state.context_loaded_cache import ContextLoadedCache
from mcp_server.state.pr_status_cache import PRStatusCache


class _AssemblyInput(BaseModel):
    """Synthetic core-tool input for assembly contract tests."""


class _AssemblyOutput(BaseModel):
    """Synthetic core-tool output for assembly contract tests."""


class _AlternativeAssemblyOutput(BaseModel):
    """Conflicting synthetic output model."""


class _GenericAssemblyTool(ICoreTool[_AssemblyInput, _AssemblyOutput]):
    """Concrete generic specialization without explicit output_model metadata."""

    def __init__(self, name: str = "generic_tool") -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return "Synthetic assembly tool"

    @property
    def args_model(self) -> type[BaseModel]:
        return _AssemblyInput

    async def execute(self, params: _AssemblyInput, context: NoteContext) -> _AssemblyOutput:
        del params, context
        return _AssemblyOutput()


class _ConflictingAssemblyTool(_GenericAssemblyTool):
    """Tool whose explicit output metadata conflicts with its generic contract."""

    output_model = _AlternativeAssemblyOutput


class _UnresolvedAssemblyTool:
    """Tool-shaped object without output-model metadata."""

    name = "unresolved_tool"


class TestToolAssembly:
    """Durable public-contract tests for supported and active tool assembly."""

    @pytest.mark.parametrize("attached_metadata", [False, True])
    def test_derives_frozen_supported_contracts_from_generic_specialization(
        self, attached_metadata: bool
    ) -> None:
        tool = _GenericAssemblyTool()
        if attached_metadata:
            tool.output_model = ToolExecution[_AssemblyOutput]

        assembly = ToolAssembly.create(
            supported_tools=(tool,),
            active_tools=(tool,),
        )

        assert assembly.supported_contracts == (
            SupportedToolContract(name="generic_tool", output_model=_AssemblyOutput),
        )
        assert assembly.supported_tools == (tool,)
        assert assembly.active_tools == (tool,)
        with pytest.raises(dataclasses.FrozenInstanceError):
            assembly.active_tools = ()  # type: ignore[misc]

    @pytest.mark.parametrize(
        ("supported_tools", "expected_message"),
        [
            ((_GenericAssemblyTool(""),), "non-empty"),
            (
                (
                    _GenericAssemblyTool("duplicate"),
                    _GenericAssemblyTool("duplicate"),
                ),
                "duplicate",
            ),
            ((_UnresolvedAssemblyTool(),), "output model"),
            ((_ConflictingAssemblyTool(),), "Conflicting"),
        ],
    )
    def test_rejects_invalid_supported_contracts(
        self,
        supported_tools: tuple[object, ...],
        expected_message: str,
    ) -> None:
        with pytest.raises(ConfigError, match=expected_message):
            ToolAssembly.create(
                supported_tools=supported_tools,
                active_tools=(),
            )

    def test_rejects_active_tool_outside_supported_object_set(self) -> None:
        supported = _GenericAssemblyTool("supported")
        unrelated = _GenericAssemblyTool("unrelated")

        with pytest.raises(ConfigError, match="active"):
            ToolAssembly.create(
                supported_tools=(supported,),
                active_tools=(unrelated,),
            )


class TestBootstrap:
    """Test suite for bootstrap containers."""

    def test_config_layer_immutability(self) -> None:
        """Verify ConfigLayer is frozen and raises FrozenInstanceError on modification."""
        mock_configs = {
            "git_config": MagicMock(spec=GitConfig),
            "workflow_config": MagicMock(spec=WorkflowConfig),
            "workphases_config": MagicMock(spec=WorkphasesConfig),
            "label_config": MagicMock(spec=LabelConfig),
            "issue_config": MagicMock(spec=IssueConfig),
            "scope_config": MagicMock(spec=ScopeConfig),
            "milestone_config": MagicMock(spec=MilestoneConfig),
            "contributor_config": MagicMock(spec=ContributorConfig),
            "operation_policies_config": MagicMock(spec=OperationPoliciesConfig),
            "enforcement_config": MagicMock(spec=EnforcementConfig),
            "contracts_config": MagicMock(spec=ContractsConfig),
            "presentation_config": MagicMock(spec=PresentationConfig),
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
            "git_manager": MagicMock(spec=GitManager),
            "state_repository": MagicMock(spec=FileStateRepository),
            "workflow_status_resolver": MagicMock(spec=WorkflowStatusResolver),
            "project_manager": MagicMock(spec=ProjectManager),
            "phase_contract_resolver": MagicMock(spec=PhaseContractResolver),
            "workflow_gate_runner": MagicMock(spec=WorkflowGateRunner),
            "workflow_state_mutator": MagicMock(spec=WorkflowStateMutator),
            "context_loaded_cache": MagicMock(spec=ContextLoadedCache),
            "phase_state_engine": MagicMock(spec=PhaseStateEngine),
            "github_manager": MagicMock(spec=GitHubManager),
            "pr_status_cache": MagicMock(spec=PRStatusCache),
            "enforcement_runner": MagicMock(spec=EnforcementRunner),
            "response_cache": MagicMock(spec=IToolResponsePublisher),
        }
        graph = ManagerGraph(**mock_managers)

        # Assert all fields are set
        for k, v in mock_managers.items():
            assert getattr(graph, k) is v

        # Assert mutation raises FrozenInstanceError
        with pytest.raises(dataclasses.FrozenInstanceError):
            graph.git_manager = MagicMock(spec=GitManager)


@pytest.mark.parametrize(("token", "github_enabled"), [(None, False), ("test-token", True)])
def test_target_startup_registers_github_tools_and_resource(
    tmp_path: Path, token: str | None, github_enabled: bool
) -> None:
    """Target startup registers GitHub features according to configured credentials."""
    project_root = Path(__file__).resolve().parents[4]
    settings = Settings(
        server=ServerSettings(
            workspace_root=str(tmp_path),
            config_root=str(project_root / ".pgmcp" / "config"),
            template_root=str(project_root / ".pgmcp" / "template_suite"),
            bypass_version_check=True,
        ),
        github=GitHubSettings(token=token),
    )

    server = ServerBootstrapper(settings).bootstrap_target()

    tool_names = {tool.name for tool in server.tools}
    resource_uris = {resource.uri_pattern for resource in server.resources}
    assert ("get_pr" in tool_names) is github_enabled
    assert ("pgmcp://github/issues" in resource_uris) is github_enabled


class TestMCPServerBootstrap:
    """Test suite for MCPServer dependency injection requirements."""

    def test_mcp_server_requires_injected_dependencies(self) -> None:
        """Verify that MCPServer raises TypeError when initialized without dependencies."""
        mock_settings = MagicMock()
        # Once the fallback code is deleted, this must raise a TypeError
        # (missing required arguments)
        with pytest.raises(TypeError):
            MCPServer(settings=mock_settings)  # type: ignore[call-arg]

    def test_mcp_server_accepts_injected_dependencies(self) -> None:
        """Verify MCPServer successfully initializes with all dependencies injected."""
        mock_settings = MagicMock()
        mock_tools = []
        mock_resources = []

        server = MCPServer(
            settings=mock_settings,
            tools=mock_tools,
            resources=mock_resources,
        )
        assert server.tools is mock_tools
        assert server.resources is mock_resources
