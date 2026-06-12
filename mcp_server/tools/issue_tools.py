"""Issue management tools."""

import unicodedata
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from mcp_server.config.schemas.contracts_config import ContractsConfig
from mcp_server.config.schemas.git_config import GitConfig
from mcp_server.config.schemas.label_config import LabelConfig
from mcp_server.config.schemas.scope_config import ScopeConfig
from mcp_server.core.exceptions import ExecutionError
from mcp_server.core.operation_notes import NoteContext
from mcp_server.managers.github_manager import GitHubManager
from mcp_server.schemas import (
    IssueConfig,
    MilestoneConfig,
)
from mcp_server.state.github_read_models import IssueReadModel
from mcp_server.tools.base import BaseTool, StructuredTool
from mcp_server.tools.tool_result import ToolResult

IssueState = Literal["open", "closed", "all"]


def normalize_unicode(text: str) -> str:
    """Normalize Unicode text for safe JSON-RPC transmission.

    Preserves emoji and other Unicode while fixing malformed surrogates.
    """
    try:
        utf8_bytes = text.encode("utf-8", errors="surrogatepass")
    except UnicodeEncodeError:
        utf8_bytes = text.encode("utf-8", errors="replace")

    normalized = utf8_bytes.decode("utf-8", errors="replace")
    return unicodedata.normalize("NFC", normalized)


class CreateIssueInput(BaseModel):
    """Structured input for creating a GitHub issue.

    Only structural validation happens here. Semantic validation against project
    config is delegated to GitHubManager.validate_issue_params(). No free-form
    labels are accepted; they are assembled internally by CreateIssueTool.

    The body field accepts pre-rendered markdown. Use scaffold_artifact(artifact_type='issue')
    to generate the body before calling this tool.
    """

    issue_type: str = Field(..., description="Issue type: feature, bug, hotfix, chore, docs, epic")
    title: str = Field(..., description="Issue title")
    priority: str = Field(..., description="Priority value")
    scope: str = Field(
        ...,
        description=(
            "Scope from scopes.yaml: architecture, mcp-server, platform,"
            " tooling, workflow, documentation"
        ),
    )
    body: str = Field(
        ...,
        description=(
            "Issue body as pre-rendered markdown. "
            "Use scaffold_artifact(artifact_type='issue') to generate."
        ),
    )
    is_epic: bool = Field(default=False, description="Mark this issue as an epic")
    parent_issue: int | None = Field(
        default=None, description="Parent issue number (positive integer)", ge=1
    )
    milestone: str | None = Field(default=None, description="Milestone title")
    assignees: list[str] | None = Field(default=None, description="List of GitHub logins to assign")

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "issue_type": "feature",
                    "title": "Add structured issue creation",
                    "priority": "medium",
                    "scope": "mcp-server",
                    "body": "## Problem\n\nThe create_issue tool lacks validation.",
                },
                {
                    "issue_type": "bug",
                    "title": "Login fails on Windows when username contains spaces",
                    "priority": "high",
                    "scope": "platform",
                    "body": (
                        "## Problem\n\nLogin fails with 500 error."
                        "\n\n## Expected Behavior\n\nRedirect to dashboard."
                    ),
                    "is_epic": False,
                    "parent_issue": 91,
                    "milestone": "v2.0",
                    "assignees": ["alice"],
                },
            ]
        },
    )


class CreateIssueTool(BaseTool):
    """Tool to create a new GitHub issue."""

    name = "create_issue"
    description = "Create a new GitHub issue"
    args_model = CreateIssueInput

    def __init__(
        self,
        manager: GitHubManager,
        issue_config: IssueConfig,
        milestone_config: MilestoneConfig,
        contracts_config: ContractsConfig,
        label_config: LabelConfig | None = None,
        scope_config: ScopeConfig | None = None,
        git_config: GitConfig | None = None,
    ) -> None:
        self.manager = manager
        self._issue_config = issue_config
        self._milestone_config = milestone_config
        self._contracts_config = contracts_config
        self._label_config = label_config
        self._scope_config = scope_config
        self._git_config = git_config

    @property
    def input_schema(self) -> dict[str, Any]:
        schema = super().input_schema
        schema["properties"]["issue_type"]["enum"] = [
            e.name for e in self._issue_config.issue_types
        ]
        if self._label_config is not None:
            priority_labels = self._label_config.get_labels_by_category("priority")
            schema["properties"]["priority"]["enum"] = [
                lbl.name.split(":")[-1] for lbl in priority_labels
            ]
        if self._scope_config is not None:
            schema["properties"]["scope"]["enum"] = self._scope_config.scopes
        if self._git_config is not None:
            schema["properties"]["title"]["maxLength"] = self._git_config.issue_title_max_length
        return schema

    def _assemble_labels(self, params: CreateIssueInput) -> list[str]:
        """Assemble the full label list from structured input fields."""
        issue_cfg = self._issue_config
        workflow_cfg = self._contracts_config

        type_label = "type:epic" if params.is_epic else issue_cfg.get_label(params.issue_type)
        workflow_name = issue_cfg.get_workflow(params.issue_type)
        first_phase = workflow_cfg.get_first_phase(workflow_name)
        phase_label = f"phase:{first_phase}"

        labels: list[str] = [
            type_label,
            f"scope:{params.scope}",
            f"priority:{params.priority}",
            phase_label,
        ]

        if params.parent_issue is not None:
            labels.append(f"parent:{params.parent_issue}")

        return labels

    async def execute(self, params: CreateIssueInput, context: NoteContext) -> ToolResult:
        del context  # Not used
        try:
            self.manager.validate_issue_params(
                issue_type=params.issue_type,
                title=params.title,
                priority=params.priority,
                scope=params.scope,
                milestone=params.milestone,
                assignees=params.assignees,
            )
        except ValueError as e:
            return ToolResult.error(f"Issue validation failed: {e}.")

        try:
            title_safe = normalize_unicode(params.title)
            body_safe = normalize_unicode(params.body)
            labels = self._assemble_labels(params)

            milestone_number: int | None = None
            if params.milestone is not None:
                milestone_number = next(
                    (
                        milestone.number
                        for milestone in self._milestone_config.milestones
                        if milestone.title == params.milestone
                    ),
                    None,
                )

            issue = self.manager.create_issue(
                title=title_safe,
                body=body_safe,
                labels=labels,
                milestone=milestone_number,
                assignees=params.assignees,
            )
            return ToolResult.text(f"Created issue #{issue['number']}: {issue['title']}")
        except ValueError as e:
            return ToolResult.error(f"Label assembly failed: {e}.")
        except ExecutionError as e:
            return ToolResult.error(str(e))


class GetIssueInput(BaseModel):
    """Input for GetIssueTool."""

    model_config = ConfigDict(extra="forbid")

    issue_number: int = Field(..., description="The issue number to retrieve")


class GetIssueTool(StructuredTool):
    """Tool to get issue details."""

    name = "get_issue"
    description = "Get detailed information about a specific GitHub issue"
    args_model = GetIssueInput
    output_model = IssueReadModel

    def __init__(self, manager: GitHubManager) -> None:
        super().__init__()
        self.manager = manager

    async def execute_structured(
        self,
        params: GetIssueInput,
        context: NoteContext,  # noqa: ANN401
    ) -> tuple[dict[str, Any], str]:
        del context  # Not used
        issue = self.manager.get_issue(params.issue_number)
        data = issue.model_dump()
        summary = f"Retrieved issue #{params.issue_number}: {data.get('title', '')}"
        return data, summary


class ListIssuesInput(BaseModel):
    """Input for ListIssuesTool."""

    model_config = ConfigDict(extra="forbid")

    state: IssueState | None = Field(default=None, description="Filter by issue state")
    labels: list[str] | None = Field(default=None, description="Filter by labels")


class ListIssuesTool(BaseTool):
    """Tool to list issues."""

    name = "list_issues"
    description = "List GitHub issues with optional filtering by state and labels"
    args_model = ListIssuesInput

    def __init__(self, manager: GitHubManager) -> None:
        self.manager = manager

    async def execute(self, params: ListIssuesInput, context: NoteContext) -> ToolResult:
        del context  # Not used
        try:
            state_str = params.state
            issues = self.manager.list_issues(state=state_str or "open", labels=params.labels)
            if not issues:
                return ToolResult.text("No issues found.")

            summary = "\n".join(
                [f"#{issue.number} {issue.title} ({issue.state})" for issue in issues]
            )
            return ToolResult.text(f"Found {len(issues)} issues:\n{summary}")
        except ExecutionError as e:
            return ToolResult.error(str(e))


class UpdateIssueInput(BaseModel):
    """Input for UpdateIssueTool."""

    model_config = ConfigDict(extra="forbid")

    issue_number: int = Field(..., description="Issue number to update")
    title: str | None = Field(default=None, description="New title")
    body: str | None = Field(default=None, description="Updated description")
    state: IssueState | None = Field(default=None, description="Target state")
    labels: list[str] | None = Field(default=None, description="Replace labels with this list")
    milestone: int | None = Field(default=None, description="Milestone number to assign")
    assignees: list[str] | None = Field(
        default=None, description="Replace assignees with this list"
    )


class UpdateIssueTool(BaseTool):
    """Tool to update an issue."""

    name = "update_issue"
    description = "Update title, body, state, labels, milestone, or assignees for an issue"
    args_model = UpdateIssueInput

    def __init__(self, manager: GitHubManager) -> None:
        self.manager = manager

    async def execute(self, params: UpdateIssueInput, context: NoteContext) -> ToolResult:
        del context  # Not used
        try:
            updated = self.manager.update_issue(
                issue_number=params.issue_number,
                title=params.title,
                body=params.body,
                state=params.state,
                labels=params.labels,
                assignees=params.assignees,
                milestone=params.milestone,
            )
        except ExecutionError as e:
            return ToolResult.error(str(e))
        return ToolResult.text(f"Updated issue #{updated.number}")


class CloseIssueInput(BaseModel):
    """Input for CloseIssueTool."""

    model_config = ConfigDict(extra="forbid")

    issue_number: int = Field(..., description="Issue number to close")
    comment: str | None = Field(default=None, description="Optional closing comment")


class CloseIssueTool(BaseTool):
    """Tool to close an issue."""

    name = "close_issue"
    description = "Close a GitHub issue with an optional comment"
    args_model = CloseIssueInput

    def __init__(self, manager: GitHubManager) -> None:
        self.manager = manager

    async def execute(self, params: CloseIssueInput, context: NoteContext) -> ToolResult:
        del context  # Not used
        try:
            self.manager.close_issue(params.issue_number, comment=params.comment)
        except ExecutionError as e:
            return ToolResult.error(str(e))
        return ToolResult.text(f"Closed issue #{params.issue_number}")
