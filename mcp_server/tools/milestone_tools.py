"""GitHub milestone tools."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from mcp_server.core.exceptions import ExecutionError
from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.github_manager import GitHubManager
from mcp_server.schemas.tool_outputs import (
    ListMilestonesOutput,
    MilestoneOutput,
    MilestoneSummaryDTO,
)
from mcp_server.tools.base import ILegacyTool


class ListMilestonesInput(BaseModel):
    """Input for ListMilestonesTool."""

    model_config = ConfigDict(extra="forbid")

    state: str = Field(
        default="open", description="Filter milestones by state", pattern="^(open|closed|all)$"
    )


class ListMilestonesTool(ILegacyTool):
    """Tool to list milestones in the repository."""

    @property
    def name(self) -> str:
        return "list_milestones"

    @property
    def description(self) -> str:
        return "List milestones with optional state filter"

    @property
    def args_model(self) -> type[BaseModel] | None:
        return ListMilestonesInput

    def __init__(self, manager: GitHubManager | None = None) -> None:
        self.manager = manager or GitHubManager()

    @property
    def input_schema(self) -> dict[str, Any]:
        assert self.args_model is not None
        return self.args_model.model_json_schema()

    async def execute(
        self, params: ListMilestonesInput, context: NoteContext
    ) -> ListMilestonesOutput:
        del context  # Not used
        try:
            milestones = self.manager.list_milestones(state=params.state)
            milestone_dtos = [
                MilestoneSummaryDTO(
                    number=milestone.number,
                    title=milestone.title,
                    state=milestone.state,
                )
                for milestone in milestones
            ]
            return ListMilestonesOutput(
                total_milestones=len(milestone_dtos),
                milestones=milestone_dtos,
            )
        except Exception as e:
            raise ExecutionError(str(e)) from e


class CreateMilestoneInput(BaseModel):
    """Input for CreateMilestoneTool."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., description="Milestone title")
    description: str | None = Field(default=None, description="Optional milestone description")
    due_on: str | None = Field(
        default=None,
        description="Optional due date (ISO 8601 string, e.g. YYYY-MM-DDTHH:MM:SSZ)",
    )


class CreateMilestoneTool(ILegacyTool):
    """Tool to create a new milestone."""

    @property
    def name(self) -> str:
        return "create_milestone"

    @property
    def description(self) -> str:
        return "Create a new milestone in the repository"

    @property
    def args_model(self) -> type[BaseModel] | None:
        return CreateMilestoneInput

    def __init__(self, manager: GitHubManager | None = None) -> None:
        self.manager = manager or GitHubManager()

    @property
    def input_schema(self) -> dict[str, Any]:
        assert self.args_model is not None
        return self.args_model.model_json_schema()

    async def execute(self, params: CreateMilestoneInput, context: NoteContext) -> MilestoneOutput:
        del context  # Not used
        try:
            milestone = self.manager.create_milestone(
                title=params.title,
                description=params.description,
                due_on=params.due_on,
            )
            return MilestoneOutput(
                number=milestone.number,
                title=milestone.title,
                state=milestone.state,
            )
        except Exception as e:
            raise ExecutionError(str(e)) from e


class CloseMilestoneInput(BaseModel):
    """Input for CloseMilestoneTool."""

    model_config = ConfigDict(extra="forbid")

    milestone_number: int = Field(..., description="Milestone number to close")


class CloseMilestoneTool(ILegacyTool):
    """Tool to close a milestone."""

    @property
    def name(self) -> str:
        return "close_milestone"

    @property
    def description(self) -> str:
        return "Close a milestone by number"

    @property
    def args_model(self) -> type[BaseModel] | None:
        return CloseMilestoneInput

    def __init__(self, manager: GitHubManager | None = None) -> None:
        self.manager = manager or GitHubManager()

    @property
    def input_schema(self) -> dict[str, Any]:
        assert self.args_model is not None
        return self.args_model.model_json_schema()

    async def execute(self, params: CloseMilestoneInput, context: NoteContext) -> MilestoneOutput:
        del context  # Not used
        try:
            milestone = self.manager.close_milestone(params.milestone_number)
            return MilestoneOutput(
                number=milestone.number,
                title=milestone.title,
                state=milestone.state,
            )
        except Exception as e:
            raise ExecutionError(str(e)) from e
