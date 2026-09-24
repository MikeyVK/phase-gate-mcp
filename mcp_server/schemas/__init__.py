# mcp_server/schemas/__init__.py
"""MCP server schema exports for current tool operations and configuration."""

from mcp_server.config.schemas.contracts_config import (
    BranchLocalArtifact,
    CheckSpec,
    ContractsConfig,
    MergePolicy,
    WorkflowEntry,
    WorkflowPhaseEntry,
)
from mcp_server.config.schemas.contributor_config import ContributorConfig, ContributorEntry
from mcp_server.config.schemas.enforcement_config import (
    EnforcementAction,
    EnforcementConfig,
    EnforcementRule,
)
from mcp_server.config.schemas.git_config import GitConfig
from mcp_server.config.schemas.issue_config import IssueConfig
from mcp_server.config.schemas.label_config import LabelConfig
from mcp_server.config.schemas.milestone_config import MilestoneConfig
from mcp_server.config.schemas.operation_policies_config import OperationPoliciesConfig
from mcp_server.config.schemas.project_structure_config import ProjectStructureConfig
from mcp_server.config.schemas.quality_config import (
    JsonViolationsParsing,
    QualityConfig,
    QualityGate,
    TextViolationsParsing,
    ViolationDTO,
)
from mcp_server.config.schemas.scope_config import ScopeConfig
from mcp_server.config.schemas.workflows import WorkflowConfig
from mcp_server.config.schemas.workphases import WorkphasesConfig
from mcp_server.schemas.error_outputs import (
    CacheErrorOutput,
    EnforcementErrorOutput,
    ExecutionErrorOutput,
    ToolErrorOutput,
    ValidationErrorOutput,
)
from mcp_server.schemas.tool_outputs import BaseToolOutput

__all__ = [
    # Infrastructure
    "BaseToolOutput",
    "ToolErrorOutput",
    "ValidationErrorOutput",
    "ExecutionErrorOutput",
    "CacheErrorOutput",
    "EnforcementErrorOutput",
    # Config schemas and value objects
    "BranchLocalArtifact",
    "CheckSpec",
    "ContractsConfig",
    "ContributorConfig",
    "ContributorEntry",
    "EnforcementAction",
    "EnforcementConfig",
    "EnforcementRule",
    "GitConfig",
    "IssueConfig",
    "JsonViolationsParsing",
    "LabelConfig",
    "MergePolicy",
    "MilestoneConfig",
    "OperationPoliciesConfig",
    "ProjectStructureConfig",
    "QualityConfig",
    "QualityGate",
    "ScopeConfig",
    "TextViolationsParsing",
    "ViolationDTO",
    "WorkflowConfig",
    "WorkflowEntry",
    "WorkflowPhaseEntry",
    "WorkphasesConfig",
]
