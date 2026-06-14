# mcp_server/schemas/tool_outputs.py
# template=schema version=74378193 created=2026-06-12T20:49Z updated=2026-06-12T21:00Z
"""Base tool output schemas.

@layer: Schemas
"""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class BaseToolOutput(BaseModel):
    """Base class for all structured tool outputs."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    success: bool = True

    error_message: str | None = None
    post_tool_instruction: str | None = None


class AutoFixOutput(BaseToolOutput):
    """Output for AutoFixTool."""

    modified_files: list[str] = Field(
        default_factory=list, description="List of files modified by the tool"
    )
    modified_files_count: int = Field(default=0, description="Count of modified files")
    formatted_modified_files: str = Field(
        default="", description="Pre-formatted bullet list of modified files"
    )
    gates_executed: list[str] = Field(
        default_factory=list, description="List of quality gates executed"
    )
    gates_executed_count: int = Field(default=0, description="Count of executed gates")
    run_id: str | None = Field(default=None, description="Cache run ID for the tool execution")


class HealthStatus(StrEnum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class HealthCheckOutput(BaseToolOutput):
    status: HealthStatus = HealthStatus.HEALTHY
    version: str
    pid: int
    platform: str
    uptime_seconds: float


class RestartServerOutput(BaseToolOutput):
    reason: str
    pid: int
    timestamp: float
    iso_time: str


class GateTransitionOutput(BaseToolOutput):
    """Base class for workflows verifying gates during phase or cycle transitions."""

    branch: str
    passing_gates: list[str] = Field(default_factory=list)
    skipped_gates: list[str] = Field(default_factory=list)
    passing_gates_count: int = 0
    skipped_gates_count: int = 0


class CycleTransitionOutput(GateTransitionOutput):
    from_cycle: int | None = None
    to_cycle: int
    total_cycles: int
    cycle_name: str


class ForceCycleTransitionOutput(CycleTransitionOutput):
    skip_reason: str
    human_approval: str


class SearchResultDTO(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    title: str
    path: str
    score: float
    snippet: str
    start_line: int
    end_line: int


class SearchDocumentationOutput(BaseToolOutput):
    query: str
    scope: str
    results_count: int
    results: list[SearchResultDTO] = Field(default_factory=list)


class GetWorkContextOutput(BaseToolOutput):
    current_branch: str
    workflow_name: str
    phase: str
    issue_number: int | None = None
    parent_branch: str | None = None
    current_cycle: int | None = None
    sub_phase: str | None = None
    phase_source: str
    phase_confidence: str
    sub_role_hint: str
    phase_instructions: str
    handover_template: str | None = None
    invalid_phase_warning: str | None = None


class InitializeProjectOutput(BaseToolOutput):
    issue_number: int
    workflow_name: str
    branch: str
    initial_phase: str
    parent_branch: str | None = None
    required_phases: list[str] = Field(default_factory=list)
    execution_mode: str
    files_created: list[str] = Field(default_factory=list)


class PhaseTaskDTO(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    id: str
    title: str
    status: str


class PhaseDTO(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    name: str
    status: str
    tasks: list[PhaseTaskDTO] = Field(default_factory=list)


class ProjectPlanOutput(BaseToolOutput):
    issue_number: int
    workflow_name: str
    phases: list[PhaseDTO] = Field(default_factory=list)


class PlannedCycleSummary(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    cycle_number: int
    deliverables_count: int


class PlanningDeliverablesOutput(BaseToolOutput):
    issue_number: int
    total_cycles: int
    total_deliverables: int
    cycles: list[PlannedCycleSummary] = Field(default_factory=list)
