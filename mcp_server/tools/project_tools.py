"""Project management tools for MCP server.

Phase 0.5: Project initialization with workflow selection.
Issue #39: Project and branch-state initialization.
Issue #79: Parent branch tracking with auto-detection.
Issue #229 Cycle 4: SavePlanningDeliverablesTool with Layer 2 validates schema validation.
"""

import contextlib
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Any, ClassVar

import anyio
from pydantic import BaseModel, ConfigDict, Field

from mcp_server.core.interfaces import ICoreTool
from mcp_server.core.interfaces.project_plan import IProjectPlanReader
from mcp_server.core.operation_notes import Note, NoteContext
from mcp_server.managers.git_manager import GitManager
from mcp_server.managers.phase_state_engine import PhaseStateEngine
from mcp_server.managers.project_manager import ProjectInitOptions, ProjectManager
from mcp_server.schemas import ContractsConfig
from mcp_server.schemas.deliverables import (
    PlanningMutationError,
    PlanningOperation,
    SavePlanningModel,
    StoredPlanningModel,
)
from mcp_server.schemas.tool_outputs import (
    InitializeProjectOutput,
    PhaseDTO,
    PlannedCycleSummary,
    PlanningDeliverablesOutput,
    ProjectPlanOutput,
)
from mcp_server.utils.schema_utils import resolve_schema_refs

logger = logging.getLogger(__name__)


class InitializeProjectInput(BaseModel):
    """Input for initialize_project tool."""

    model_config = ConfigDict(extra="forbid")

    issue_number: int = Field(..., description="GitHub issue number")
    issue_title: str = Field(..., description="Issue title")
    workflow_name: str = Field(
        ...,
        description="Workflow name; valid values are injected from contracts.yaml",
    )
    parent_branch: str | None = Field(
        default=None,
        description=(
            "Parent branch this feature/bug branches from. "
            "If not provided, attempts auto-detection from git reflog. "
            "Example: 'epic/76-quality-gates-tooling'"
        ),
    )
    custom_phases: tuple[str, ...] | None = Field(
        default=None,
        description="Optional phase sequence override for the selected configured workflow",
    )
    skip_reason: str | None = Field(
        default=None,
        description="Required justification when custom_phases overrides the configured sequence",
    )


class InitializeProjectTool(ICoreTool[InitializeProjectInput, InitializeProjectOutput]):
    """Initialize project metadata and branch state after same-branch admission.

    Project and state writes remain separate; this guard prevents overwriting
    an already initialized branch before project persistence starts.
    """

    output_model: ClassVar[type[BaseModel]] = InitializeProjectOutput

    @property
    def name(self) -> str:
        return "initialize_project"

    @property
    def description(self) -> str:
        return (
            "Initialize a project with a configured workflow and optional justified "
            "phase-sequence override."
        )

    @property
    def args_model(self) -> type[BaseModel] | None:
        return InitializeProjectInput

    def __init__(
        self,
        workspace_root: Path | str,
        manager: ProjectManager,
        git_manager: GitManager,
        state_engine: PhaseStateEngine,
        contracts_config: ContractsConfig | None = None,
    ) -> None:
        """Initialize tool with injected project dependencies."""
        self.workspace_root = Path(workspace_root)
        self.manager = manager
        self.git_manager = git_manager
        self.state_engine = state_engine
        self._contracts_config = contracts_config

    @property
    def input_schema(self) -> dict[str, Any]:
        if self.args_model is None:
            return {}
        schema = resolve_schema_refs(self.args_model.model_json_schema())
        if self._contracts_config is not None:
            schema["properties"]["workflow_name"]["enum"] = list(
                self._contracts_config.workflows.keys()
            )
        return schema

    def _detect_parent_branch_from_reflog_sync(self, current_branch: str) -> str | None:
        """Detect parent branch from git reflog.

        This is intentionally synchronous and must run in a worker thread. On Windows
        we've observed that long-running git subprocesses can make MCP (stdio) look
        "hung"; doing the subprocess work in a thread plus using robust kill logic
        keeps the server responsive.

        To keep reconciliation accurate without producing huge output, we read only
        the reflog *subject* lines via `--pretty=%gs`.
        """
        max_entries = 5000
        timeout_s = 5.0

        cmd = [
            "git",
            "--no-pager",
            "reflog",
            "show",
            "--all",
            "-n",
            str(max_entries),
            "--pretty=%gs",
        ]

        def kill_tree(pid: int) -> None:
            if os.name == "nt":
                # Kill the entire tree so `git` doesn't linger.
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(pid)],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=2,
                )
                return
            try:
                os.kill(pid, 9)
            except OSError:
                return

        try:
            with subprocess.Popen(
                cmd,
                cwd=str(self.workspace_root),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
            ) as proc:
                try:
                    stdout, _stderr = proc.communicate(timeout=timeout_s)
                except subprocess.TimeoutExpired:
                    kill_tree(proc.pid)
                    with contextlib.suppress(OSError, subprocess.TimeoutExpired, ValueError):
                        proc.communicate(timeout=1)
                    logger.warning(
                        "Git reflog failed: Command timed out after %ss",
                        timeout_s,
                    )
                    return None

                if proc.returncode:
                    logger.warning("Git reflog failed (exit %s)", proc.returncode)
                    return None

            pattern = f"checkout: moving from (.+?) to {re.escape(current_branch)}"
            for line in stdout.splitlines():
                match = re.search(pattern, line)
                if match:
                    parent = match.group(1)
                    logger.info("Detected parent branch from reflog: %s", parent)
                    return parent

            logger.warning("No parent branch found in reflog for %s", current_branch)
            return None

        except (OSError, ValueError) as e:
            logger.warning("Git reflog failed: %s", e)
            return None

    async def _detect_parent_branch_from_reflog(self, current_branch: str) -> str | None:
        return await anyio.to_thread.run_sync(
            lambda: self._detect_parent_branch_from_reflog_sync(current_branch),
            cancellable=True,
        )

    async def execute(
        self,
        params: InitializeProjectInput,
        context: NoteContext,  # noqa: ANN401, ARG002
    ) -> InitializeProjectOutput:
        """Admit the branch, then initialize project metadata and branch state.

        Project and state are persisted separately.
        Issue #79: Auto-detects parent_branch if not provided.

        Args:
            params: InitializeProjectInput with issue details

        Returns:
            InitializeProjectOutput
        """
        try:
            # Step 0: Get current branch once and reuse
            with anyio.fail_after(5):
                branch = await anyio.to_thread.run_sync(self.git_manager.get_current_branch)

            await anyio.to_thread.run_sync(
                lambda: self.state_engine.validate_branch_initialization(branch)
            )

            # Step 1: Determine parent_branch
            parent_branch = params.parent_branch

            if parent_branch is None:
                # Auto-detect from git reflog
                parent_branch = await self._detect_parent_branch_from_reflog(branch)
                if parent_branch:
                    logger.info("Auto-detected parent_branch: %s for %s", parent_branch, branch)

            # Step 2: Create deliverables.json (workflow definition)
            options = None
            if params.custom_phases or params.skip_reason or parent_branch:
                options = ProjectInitOptions(
                    custom_phases=params.custom_phases,
                    skip_reason=params.skip_reason,
                    parent_branch=parent_branch,
                )

            with anyio.fail_after(20):
                result = await anyio.to_thread.run_sync(
                    lambda: self.manager.initialize_project(
                        issue_number=params.issue_number,
                        issue_title=params.issue_title,
                        workflow_name=params.workflow_name,
                        options=options,
                    )
                )

            # Step 3: Determine first phase from workflow
            first_phase = result["required_phases"][0]

            # Step 5: Initialize branch state
            with anyio.fail_after(10):
                await anyio.to_thread.run_sync(
                    lambda: self.state_engine.initialize_branch(
                        branch=branch,
                        issue_number=params.issue_number,
                        initial_phase=first_phase,
                    )
                )

            return InitializeProjectOutput(
                success=True,
                issue_number=params.issue_number,
                workflow_name=params.workflow_name,
                branch=branch,
                initial_phase=first_phase,
                parent_branch=parent_branch,
                required_phases=result["required_phases"],
                execution_mode=result["execution_mode"],
                files_created=[
                    "deliverables.json (workflow definition)",
                    "state.json (branch state)",
                ],
            )

        except Exception as e:
            return InitializeProjectOutput(
                success=False,
                error_message=str(e),
                issue_number=params.issue_number,
                workflow_name=params.workflow_name,
                branch="",
                initial_phase="",
                execution_mode="",
            )


class GetProjectPlanInput(BaseModel):
    """Input for get_project_plan tool."""

    model_config = ConfigDict(extra="forbid")

    issue_number: int = Field(..., description="GitHub issue number")


class GetProjectPlanTool(ICoreTool[GetProjectPlanInput, ProjectPlanOutput]):
    """Tool for retrieving project plan."""

    output_model: ClassVar[type[BaseModel]] = ProjectPlanOutput

    @property
    def name(self) -> str:
        return "get_project_plan"

    @property
    def description(self) -> str:
        return "Get project phases and complete stored planning deliverables for an issue"

    @property
    def args_model(self) -> type[BaseModel] | None:
        return GetProjectPlanInput

    @property
    def input_schema(self) -> dict[str, Any]:
        if self.args_model is None:
            return {}
        return resolve_schema_refs(self.args_model.model_json_schema())

    def __init__(self, manager: IProjectPlanReader) -> None:
        """Initialize tool with the read-only project plan contract."""
        self.manager = manager

    async def execute(
        self,
        params: GetProjectPlanInput,
        context: NoteContext,  # noqa: ANN401
    ) -> ProjectPlanOutput:
        """Execute project plan retrieval.

        Args:
            params: GetProjectPlanInput with issue_number
            context: Call context
        """
        try:
            plan = self.manager.get_project_plan(issue_number=params.issue_number)
            if plan:
                required_phases = plan.get("required_phases", [])
                current_phase = plan.get("current_phase", "")
                curr_phase_name = current_phase.split(":")[0] if current_phase else ""

                phases_list = []
                current_found = False
                for p_name in required_phases:
                    if p_name == curr_phase_name:
                        status = "active"
                        current_found = True
                    elif current_found:
                        status = "pending"
                    else:
                        status = "completed" if curr_phase_name else "pending"
                    phases_list.append(PhaseDTO(name=p_name, status=status, tasks=[]))

                stored_planning = plan.get("planning_deliverables")
                planning = (
                    StoredPlanningModel.model_validate(stored_planning, strict=True)
                    if stored_planning is not None
                    else None
                )
                return ProjectPlanOutput(
                    success=True,
                    issue_number=params.issue_number,
                    workflow_name=plan.get("workflow_name", ""),
                    phases=phases_list,
                    planning_deliverables=planning,
                )

            context.produce(
                Note(
                    key="initialize_project_suggestion",
                    params={
                        "issue_number": params.issue_number,
                    },
                )
            )
            return ProjectPlanOutput(
                success=False,
                error_message=f"No project plan found for issue #{params.issue_number}",
                issue_number=params.issue_number,
                workflow_name="",
                phases=[],
            )
        except (ValueError, OSError) as e:
            return ProjectPlanOutput(
                success=False,
                error_message=str(e),
                issue_number=params.issue_number,
                workflow_name="",
                phases=[],
            )


# ---------------------------------------------------------------------------
# Planning deliverables tools
# ---------------------------------------------------------------------------


class SavePlanningDeliverablesInput(BaseModel):
    """Create the complete initial plan; names and order determine stored references."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    issue_number: int = Field(gt=0, strict=True, description="GitHub issue number")
    planning_deliverables: SavePlanningModel


class UpdatePlanningDeliverablesInput(BaseModel):
    """Mutate complete blocks by original-snapshot references; omission leaves blocks unchanged."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    issue_number: int = Field(gt=0, strict=True, description="GitHub issue number")
    operations: list[PlanningOperation] = Field(
        min_length=1,
        description=(
            "Replace/remove original C_n cycles or named phase blocks explicitly. "
            "Append cycles after surviving originals in request order. "
            "All targets resolve before renumbering; duplicate targets reject the whole request."
        ),
    )
    force: bool = Field(
        default=False,
        strict=True,
        description=(
            "Retry local Git evidence and accept continued uncertainty after investigation. "
            "Known commit-protected deletion/renumbering and invalid planning remain forbidden."
        ),
    )


def _planning_input_schema(model: type[BaseModel], manager: ProjectManager) -> dict[str, Any]:
    """Expose the same configured phase vocabulary and omission semantics as admission."""
    schema = resolve_schema_refs(model.model_json_schema())
    properties = schema["properties"]
    config = manager.workphases_config
    phases = list(config.phases) if config is not None else []
    if "planning_deliverables" in properties:
        planning = properties["planning_deliverables"]["properties"]
        cycles = planning["cycles"]
        planning["cycles"] = next(
            option for option in cycles["anyOf"] if option.get("type") != "null"
        )
        planning["phases"]["propertyNames"] = {"enum": phases}
    if "operations" in properties:
        variants = properties["operations"]["items"]["oneOf"]
        for variant in variants:
            phase = variant["properties"].get("phase")
            if phase is not None:
                phase["enum"] = phases
    return schema


def _planning_response(
    manager: IProjectPlanReader, issue_number: int
) -> PlanningDeliverablesOutput:
    """Assemble one successful command response from the persisted complete plan."""
    plan = manager.get_project_plan(issue_number)
    if plan is None or plan.get("planning_deliverables") is None:
        raise ValueError("Planning deliverables unavailable after persistence")
    planning = StoredPlanningModel.model_validate(plan["planning_deliverables"], strict=True)
    cycles = planning.cycles.cycles if planning.cycles is not None else []
    summaries = [
        PlannedCycleSummary(
            cycle_id=cycle.cycle_id,
            cycle_number=cycle.cycle_number,
            cycle_name=cycle.cycle_name,
            deliverables_count=len(cycle.deliverables),
        )
        for cycle in cycles
    ]
    return PlanningDeliverablesOutput(
        success=True,
        issue_number=issue_number,
        total_cycles=len(cycles),
        total_deliverables=(
            sum(len(cycle.deliverables) for cycle in cycles)
            + sum(len(block.deliverables) for block in planning.phases.values())
        ),
        cycles=summaries,
        planning_deliverables=planning,
    )


def _planning_failure(
    issue_number: int, error: Exception, *, persisted: bool
) -> PlanningDeliverablesOutput:
    """Keep rejected commands and failed post-write readback distinct."""
    code = (
        "planning_readback_failed"
        if persisted
        else error.error_code
        if isinstance(error, PlanningMutationError)
        else "planning_command_failed"
    )
    return PlanningDeliverablesOutput(
        success=False,
        issue_number=issue_number,
        error_code=code,
        error_message=str(error),
        total_cycles=0,
        total_deliverables=0,
    )


class SavePlanningDeliverablesTool(
    ICoreTool[SavePlanningDeliverablesInput, PlanningDeliverablesOutput]
):
    """Create an initial complete plan once under configured Planning admission."""

    output_model: ClassVar[type[BaseModel]] = PlanningDeliverablesOutput

    def __init__(self, manager: ProjectManager, workspace_root: Path | str | None = None) -> None:
        del workspace_root
        self._manager = manager

    @property
    def name(self) -> str:
        return "save_planning_deliverables"

    @property
    def description(self) -> str:
        return (
            "Create the complete initial plan once. Supply cycle/deliverable names and ordered "
            "complete blocks; the server stores C_n, D_n.m and phase-local D_n references "
            "and totals."
        )

    @property
    def args_model(self) -> type[BaseModel]:
        return SavePlanningDeliverablesInput

    @property
    def input_schema(self) -> dict[str, Any]:
        return _planning_input_schema(SavePlanningDeliverablesInput, self._manager)

    async def execute(
        self, params: SavePlanningDeliverablesInput, context: NoteContext
    ) -> PlanningDeliverablesOutput:
        del context
        persisted = False
        try:
            self._manager.save_planning_deliverables(
                issue_number=params.issue_number,
                planning_deliverables=params.planning_deliverables,
            )
            persisted = True
            return _planning_response(self._manager, params.issue_number)
        except Exception as error:
            return _planning_failure(params.issue_number, error, persisted=persisted)


class UpdatePlanningDeliverablesTool(
    ICoreTool[UpdatePlanningDeliverablesInput, PlanningDeliverablesOutput]
):
    """Apply explicit complete-block operations with fresh local execution evidence."""

    output_model: ClassVar[type[BaseModel]] = PlanningDeliverablesOutput

    def __init__(self, manager: ProjectManager, workspace_root: Path | str | None = None) -> None:
        del workspace_root
        self._manager = manager

    @property
    def name(self) -> str:
        return "update_planning_deliverables"

    @property
    def description(self) -> str:
        return (
            "Mutate an existing plan using append_cycle, replace_cycle, remove_cycle, "
            "set_phase or remove_phase. Targets refer to the original snapshot; complete "
            "blocks replace their contents. The server derives references and totals, "
            "protects committed cycle numbers, and retries evidence on every force call."
        )

    @property
    def args_model(self) -> type[BaseModel]:
        return UpdatePlanningDeliverablesInput

    @property
    def input_schema(self) -> dict[str, Any]:
        return _planning_input_schema(UpdatePlanningDeliverablesInput, self._manager)

    async def execute(
        self, params: UpdatePlanningDeliverablesInput, context: NoteContext
    ) -> PlanningDeliverablesOutput:
        persisted = False
        try:
            self._manager.update_planning_deliverables(
                issue_number=params.issue_number,
                operations=params.operations,
                context=context,
                force=params.force,
            )
            persisted = True
            return _planning_response(self._manager, params.issue_number)
        except Exception as error:
            return _planning_failure(params.issue_number, error, persisted=persisted)
