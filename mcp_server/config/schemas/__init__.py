"""Pure config schema package for C_LOADER migration."""

from mcp_server.config.schemas.checks_config import ChecksConfig
from mcp_server.config.schemas.contracts_config import (
    BranchLocalArtifact,
    CheckSpec,
    ContractsConfig,
    MergePolicy,
    PhaseContractPhase,
    WorkflowEntry,
    WorkflowPhaseEntry,
)
from mcp_server.config.schemas.contributor_config import ContributorConfig, ContributorEntry
from mcp_server.config.schemas.enforcement_config import (
    EnforcementAction,
    EnforcementConfig,
    EnforcementRule,
)
from mcp_server.config.schemas.fixes_config import FixBinding, FixesConfig, FixId
from mcp_server.config.schemas.git_config import GitConfig
from mcp_server.config.schemas.issue_config import IssueConfig, IssueTypeEntry
from mcp_server.config.schemas.label_config import Label, LabelConfig, LabelPattern
from mcp_server.config.schemas.milestone_config import MilestoneConfig, MilestoneEntry
from mcp_server.config.schemas.operation_policies_config import (
    OperationPoliciesConfig,
    OperationPolicy,
)
from mcp_server.config.schemas.presentation_config import PresentationConfig
from mcp_server.config.schemas.scope_config import ScopeConfig
from mcp_server.config.schemas.tests_config import TestBinding, TestId, TestsConfig
from mcp_server.config.schemas.workflows import WorkflowConfig, WorkflowTemplate
from mcp_server.config.schemas.workphases import PhaseDefinition, WorkphasesConfig

__all__ = [
    "TestBinding",
    "TestId",
    "TestsConfig",
    "FixesConfig",
    "FixBinding",
    "FixId",
    "BranchLocalArtifact",
    "ChecksConfig",
    "CheckSpec",
    "ContractsConfig",
    "ContributorConfig",
    "ContributorEntry",
    "EnforcementAction",
    "EnforcementConfig",
    "EnforcementRule",
    "GitConfig",
    "IssueConfig",
    "IssueTypeEntry",
    "Label",
    "LabelConfig",
    "LabelPattern",
    "MergePolicy",
    "MilestoneConfig",
    "MilestoneEntry",
    "OperationPoliciesConfig",
    "OperationPolicy",
    "PhaseContractPhase",
    "PhaseDefinition",
    "PresentationConfig",
    "ScopeConfig",
    "WorkflowConfig",
    "WorkflowEntry",
    "WorkflowPhaseEntry",
    "WorkflowTemplate",
    "WorkphasesConfig",
]
