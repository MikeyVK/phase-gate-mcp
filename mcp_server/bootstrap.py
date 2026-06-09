# mcp_server\bootstrap.py
# template=generic version=f35abd82 created=2026-06-09T09:48Z updated=
"""Bootstrap module.

Dependency injection and bootstrap orchestration layer.

@layer: MCP Server
@dependencies: [
    mcp_server.config.schemas,
    mcp_server.scaffolding.template_registry,
    mcp_server.managers.*,
    mcp_server.state.*
]
@responsibilities:
    - Define immutable dataclasses for config models and managers.
    - Orchestrate composition root build phase.
"""

from __future__ import annotations

from dataclasses import dataclass

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
