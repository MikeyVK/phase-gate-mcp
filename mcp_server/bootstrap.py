# mcp_server\bootstrap.py
# template=generic version=f35abd82 created=2026-06-09T09:48Z updated=
"""Bootstrap module.

Dependency injection and bootstrap orchestration layer.

@layer: MCP Server
@dependencies: [
    pathlib,
    dataclasses,
    mcp_server.config.loader,
    mcp_server.config.schemas,
    mcp_server.config.settings,
    mcp_server.config.validator,
    mcp_server.core.*,
    mcp_server.managers.*,
    mcp_server.state.*
]
@responsibilities:
    - Define immutable dataclasses for config models and managers.
    - Orchestrate composition root build phase.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp_server.server import MCPServer
from mcp_server.config.loader import ConfigLoader
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
from mcp_server.config.settings import Settings
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.commit_phase_detector import CommitPhaseDetector
from mcp_server.core.logging import get_logger, setup_logging
from mcp_server.core.phase_detection import ScopeDecoder
from mcp_server.managers.artifact_manager import ArtifactManager
from mcp_server.managers.deliverable_checker import DeliverableChecker
from mcp_server.managers.enforcement_runner import EnforcementRunner
from mcp_server.managers.git_manager import GitManager
from mcp_server.managers.github_manager import GitHubManager
from mcp_server.managers.phase_contract_resolver import PhaseConfigContext, PhaseContractResolver
from mcp_server.managers.phase_state_engine import PhaseStateEngine
from mcp_server.managers.project_manager import ProjectManager
from mcp_server.managers.qa_manager import QAManager
from mcp_server.managers.quality_state_repository import FileQualityStateRepository
from mcp_server.managers.state_reconstructor import StateReconstructor
from mcp_server.managers.state_repository import BranchValidatedStateReader, FileStateRepository
from mcp_server.managers.workflow_gate_runner import WorkflowGateRunner
from mcp_server.managers.workflow_state_mutator import WorkflowStateMutator
from mcp_server.managers.workflow_status_resolver import WorkflowStatusResolver
from mcp_server.scaffolding.template_registry import TemplateRegistry
from mcp_server.state.context_loaded_cache import ContextLoadedCache
from mcp_server.state.pr_status_cache import PRStatusCache

logger = get_logger("bootstrap")
lifecycle_logger = get_logger("server_lifecycle")


@dataclass(frozen=True)
class ConfigLayer:
    """Immutable layer containing all validated configurations."""

    git_config: GitConfig
    workflow_config: WorkflowConfig
    workphases_config: WorkphasesConfig
    quality_config: QualityConfig
    label_config: LabelConfig
    issue_config: IssueConfig
    scope_config: ScopeConfig
    milestone_config: MilestoneConfig
    contributor_config: ContributorConfig
    artifact_registry: ArtifactRegistryConfig
    project_structure_config: ProjectStructureConfig
    operation_policies_config: OperationPoliciesConfig
    enforcement_config: EnforcementConfig
    contracts_config: ContractsConfig


@dataclass(frozen=True)
class ManagerGraph:
    """Immutable graph of instantiated managers and services."""

    template_registry: TemplateRegistry
    git_manager: GitManager
    state_repository: FileStateRepository
    workflow_status_resolver: WorkflowStatusResolver
    project_manager: ProjectManager
    phase_contract_resolver: PhaseContractResolver
    workflow_gate_runner: WorkflowGateRunner
    state_reconstructor: StateReconstructor
    workflow_state_mutator: WorkflowStateMutator
    context_loaded_cache: ContextLoadedCache
    phase_state_engine: PhaseStateEngine
    quality_state_repository: FileQualityStateRepository
    qa_manager: QAManager
    github_manager: GitHubManager
    artifact_manager: ArtifactManager
    pr_status_cache: PRStatusCache
    enforcement_runner: EnforcementRunner


class ServerBootstrapper:
    """Orchestrates configuration loading and manager graph instantiation."""

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize bootstrapper with settings."""
        self._settings = settings or Settings.from_env()

    def bootstrap(self) -> MCPServer:
        """Bootstrap logging, config, registry, and managers, and return MCPServer."""
        settings = self._settings

        # Configure logging
        _server_root_early = Path(settings.server.workspace_root) / settings.server.server_root_dir
        _logs_dir_early = _server_root_early / settings.server.logs_dir
        _audit_log = settings.logging.audit_log or str(_logs_dir_early / "mcp_audit.log")
        setup_logging(settings.logging.level, _audit_log)

        lifecycle_logger.info("MCP server starting via bootstrapper")

        # Initialize template registry
        workspace_root = Path(settings.server.workspace_root)
        server_root = workspace_root / settings.server.server_root_dir
        registry_path = server_root / "template_registry.json"

        if not registry_path.exists():
            registry_path.parent.mkdir(parents=True, exist_ok=True)
            lifecycle_logger.info("Bootstrapping template registry: %s", registry_path)

        template_registry = TemplateRegistry(registry_path=registry_path)
        lifecycle_logger.info("Template registry initialized")

        # Build ConfigLayer
        configs = self._build_config_layer()

        # Build ManagerGraph
        managers = self._build_manager_graph(configs, template_registry)

        # Import dynamically to avoid circular dependencies
        from mcp_server.server import MCPServer  # noqa: PLC0415

        return MCPServer(
            settings=settings,
            configs=configs,
            managers=managers,
        )

    def _build_config_layer(self) -> ConfigLayer:
        """Load and validate all configurations."""
        workspace_root = Path(self._settings.server.workspace_root)
        server_root = workspace_root / self._settings.server.server_root_dir
        config_root = server_root / "config"

        config_loader = ConfigLoader(config_root=config_root)
        git_config = config_loader.load_git_config()
        workflow_config = config_loader.load_workflow_config()
        workphases_config = config_loader.load_workphases_config()
        quality_config = config_loader.load_quality_config()
        label_config = config_loader.load_label_config()
        issue_config = config_loader.load_issue_config()
        scope_config = config_loader.load_scope_config()
        milestone_config = config_loader.load_milestone_config()
        contributor_config = config_loader.load_contributor_config()
        artifact_registry = config_loader.load_artifact_registry_config()
        project_structure_config = config_loader.load_project_structure_config(
            artifact_registry=artifact_registry
        )
        operation_policies_config = config_loader.load_operation_policies_config()
        enforcement_config = config_loader.load_enforcement_config()
        contracts_config = config_loader.load_contracts_config()

        ConfigValidator().validate_startup(
            policies=operation_policies_config,
            workflow=workflow_config,
            structure=project_structure_config,
            artifact=artifact_registry,
            contracts=contracts_config,
            workphases=workphases_config,
        )

        return ConfigLayer(
            git_config=git_config,
            workflow_config=workflow_config,
            workphases_config=workphases_config,
            quality_config=quality_config,
            label_config=label_config,
            issue_config=issue_config,
            scope_config=scope_config,
            milestone_config=milestone_config,
            contributor_config=contributor_config,
            artifact_registry=artifact_registry,
            project_structure_config=project_structure_config,
            operation_policies_config=operation_policies_config,
            enforcement_config=enforcement_config,
            contracts_config=contracts_config,
        )

    def _build_manager_graph(
        self, configs: ConfigLayer, template_registry: TemplateRegistry
    ) -> ManagerGraph:
        """Instantiate all managers and services."""
        workspace_root = Path(self._settings.server.workspace_root)
        server_root = workspace_root / self._settings.server.server_root_dir
        logs_dir = server_root / self._settings.server.logs_dir

        git_manager = GitManager(
            git_config=configs.git_config,
            workphases_config=configs.workphases_config,
        )
        state_repository = FileStateRepository(state_file=server_root / "state.json")
        branch_validated_reader = BranchValidatedStateReader(inner=state_repository)
        commit_phase_detector = CommitPhaseDetector(
            workphases_config=configs.workphases_config,
        )
        workflow_status_resolver = WorkflowStatusResolver(
            git_context_reader=git_manager,
            state_reader=branch_validated_reader,
            commit_phase_detector=commit_phase_detector,
        )
        project_manager = ProjectManager(
            workspace_root=workspace_root,
            contracts_config=configs.contracts_config,
            git_manager=git_manager,
            workphases_config=configs.workphases_config,
            workflow_status_resolver=workflow_status_resolver,
            server_root=server_root,
        )
        phase_contract_resolver = PhaseContractResolver(
            PhaseConfigContext(
                workphases=configs.workphases_config,
                contracts=configs.contracts_config,
            )
        )
        workflow_gate_runner = WorkflowGateRunner(
            deliverable_checker=DeliverableChecker(workspace_root),
            phase_contract_resolver=phase_contract_resolver,
        )
        state_reconstructor = StateReconstructor(
            workspace_root=workspace_root,
            git_config=configs.git_config,
            project_manager=project_manager,
            scope_decoder=ScopeDecoder(
                workphases_config=configs.workphases_config,
            ),
        )
        workflow_state_mutator = WorkflowStateMutator(
            state_repository=state_repository,
            state_reconstructor=state_reconstructor,
        )
        context_loaded_cache = ContextLoadedCache()
        phase_state_engine = PhaseStateEngine(
            workspace_root=workspace_root,
            project_manager=project_manager,
            git_config=configs.git_config,
            contracts_config=configs.contracts_config,
            state_repository=state_repository,
            scope_decoder=ScopeDecoder(
                workphases_config=configs.workphases_config,
            ),
            workflow_gate_runner=workflow_gate_runner,
            state_reconstructor=state_reconstructor,
            workflow_state_mutator=workflow_state_mutator,
            context_loaded_writer=context_loaded_cache,
            server_root=server_root,
        )
        quality_state_repository = FileQualityStateRepository(
            backing_file=server_root / "quality_state.json"
        )
        qa_manager = QAManager(
            workspace_root=workspace_root,
            quality_config=configs.quality_config,
            logs_dir=logs_dir,
            quality_state_repository=quality_state_repository,
            git_context_reader=git_manager,
            state_reader=branch_validated_reader,
        )
        github_manager = GitHubManager(
            issue_config=configs.issue_config,
            label_config=configs.label_config,
            scope_config=configs.scope_config,
            milestone_config=configs.milestone_config,
            contributor_config=configs.contributor_config,
            git_config=configs.git_config,
        )
        artifact_manager = ArtifactManager(
            workspace_root=workspace_root,
            server_root=server_root,
            template_registry=template_registry,
            registry=configs.artifact_registry,
            project_structure_config=configs.project_structure_config,
        )
        pr_status_cache = PRStatusCache(github_manager=github_manager)
        enforcement_runner = EnforcementRunner(
            workspace_root=workspace_root,
            config=configs.enforcement_config,
            git_config=configs.git_config,
            state_reader=state_repository,
            pr_status_reader=pr_status_cache,
            server_root=server_root,
            context_loaded_reader=context_loaded_cache,
        )

        return ManagerGraph(
            template_registry=template_registry,
            git_manager=git_manager,
            state_repository=state_repository,
            workflow_status_resolver=workflow_status_resolver,
            project_manager=project_manager,
            phase_contract_resolver=phase_contract_resolver,
            workflow_gate_runner=workflow_gate_runner,
            state_reconstructor=state_reconstructor,
            workflow_state_mutator=workflow_state_mutator,
            context_loaded_cache=context_loaded_cache,
            phase_state_engine=phase_state_engine,
            quality_state_repository=quality_state_repository,
            qa_manager=qa_manager,
            github_manager=github_manager,
            artifact_manager=artifact_manager,
            pr_status_cache=pr_status_cache,
            enforcement_runner=enforcement_runner,
        )
