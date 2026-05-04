# mcp_server/config/schemas/workflows.py
"""
Workflow configuration schema definitions.

Defines typed value objects for workflow templates loaded by the configuration layer.
Phase ordering and transition validation are handled by ContractsConfig (contracts.yaml).

@layer: Backend (Config)
@dependencies: [pydantic, typing]
@responsibilities:
    - Define workflow template and root config schema contracts
    - Provide catalog lookup helpers for workflow metadata
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class WorkflowTemplate(BaseModel):
    """Single workflow definition — catalog metadata only.

    Phase ordering lives in contracts.yaml (ContractsConfig), not here.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(..., description="Workflow name")
    default_execution_mode: Literal["interactive", "autonomous"] = Field(
        default="interactive",
        description="Default execution mode for this workflow",
    )
    description: str = Field(default="", description="Human-readable workflow description")


class WorkflowConfig(BaseModel):
    """Root workflow configuration value object — catalog role only.

    Transition validation and phase ordering are delegated to ContractsConfig.
    """

    version: str = Field(..., description="Config schema version")
    workflows: dict[str, WorkflowTemplate] = Field(..., description="Workflow definitions")

    def get_workflow(self, name: str) -> WorkflowTemplate:
        workflows_dict: dict[str, WorkflowTemplate] = dict(self.workflows)
        if name not in workflows_dict:
            available = ", ".join(sorted(workflows_dict.keys()))
            raise ValueError(
                f"Unknown workflow: '{name}'\n"
                f"Available workflows: {available}\n"
                "Hint: Add a matching workflow definition to the workflow configuration"
            )
        return workflows_dict[name]

    def has_workflow(self, workflow_name: str) -> bool:
        return workflow_name in self.workflows
