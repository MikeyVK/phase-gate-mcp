"""Discovery tools for AI self-orientation."""

# pyright: reportIncompatibleMethodOverride=false
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict, Field

from mcp_server.config.settings import Settings
from mcp_server.core.exceptions import ExecutionError
from mcp_server.core.operation_notes import NoteContext, RecoveryNote
from mcp_server.managers.git_manager import GitManager
from mcp_server.managers.github_manager import GitHubManager
from mcp_server.managers.phase_state_engine import PhaseStateEngine
from mcp_server.managers.project_manager import ProjectManager
from mcp_server.schemas import WorkphasesConfig
from mcp_server.services.document_indexer import DocumentIndexer
from mcp_server.services.search_service import SearchService
from mcp_server.tools.base import BaseTool
from mcp_server.tools.tool_result import ToolResult

if TYPE_CHECKING:
    from mcp_server.config.schemas.contracts_config import ContractsConfig
    from mcp_server.core.interfaces import IContextLoadedWriter
    from mcp_server.managers.workflow_status_resolver import WorkflowStatusResolver


class SearchDocumentationInput(BaseModel):
    """Input for SearchDocumentationTool."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(
        ..., description="Search query (e.g., 'how to implement a worker', 'DTO validation rules')"
    )
    scope: str = Field(
        default="all",
        description="Optional scope to filter results",
        pattern="^(all|architecture|coding_standards|development|reference|implementation)$",
    )


class SearchDocumentationTool(BaseTool):
    """Tool to search documentation files."""

    name = "search_documentation"
    description = (
        "Semantic/fuzzy search across all docs/ files. "
        "Returns ranked results with snippets for understanding project structure."
    )
    args_model = SearchDocumentationInput

    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self._settings = settings

    async def execute(self, params: SearchDocumentationInput, context: NoteContext) -> ToolResult:
        """Execute documentation search using DocumentIndexer + SearchService."""
        # Build index from docs directory
        docs_dir = Path(self._settings.server.workspace_root) / "docs"

        if not docs_dir.exists():
            context.produce(RecoveryNote(message=f"Expected directory: {docs_dir}"))
            context.produce(RecoveryNote(message="Create docs/ directory in workspace root"))
            context.produce(RecoveryNote(message="Add markdown files to document project"))
            raise ExecutionError("Documentation directory not found")

        index = DocumentIndexer.build_index(docs_dir)

        # Map scope filter (None if 'all')
        scope_filter = None if params.scope == "all" else params.scope

        # Search index
        results = SearchService.search_index(
            index=index, query=params.query, max_results=10, scope=scope_filter
        )

        if not results:
            return ToolResult.text(
                f"No results found for query: '{params.query}'\n"
                "Try broader search terms or different scope."
            )

        # Format results for output
        output_lines = [f"Found {len(results)} results for '{params.query}':\n"]

        for i, result in enumerate(results, 1):
            output_lines.append(
                f"{i}. **{result['title']}** ({result['path']})\n"
                f"   Score: {result['_relevance']:.2f}\n"
                f"   > {result['_snippet']}\n"
            )

        return ToolResult.text("\n".join(output_lines))


class GetWorkContextInput(BaseModel):
    """Input for GetWorkContextTool."""

    model_config = ConfigDict(extra="forbid")


class GetWorkContextTool(BaseTool):
    """Tool to aggregate work context from Git and GitHub."""

    name = "get_work_context"
    description = (
        "Aggregates context from GitHub Issues, current branch, and workflow phase "
        "to understand what to work on next. Uses deterministic phase detection."
    )
    args_model = GetWorkContextInput

    def __init__(
        self,
        settings: Settings,
        git_manager: GitManager,
        project_manager: ProjectManager,
        state_engine: PhaseStateEngine,
        github_manager: GitHubManager | None = None,
        workphases_config: WorkphasesConfig | None = None,
        state_path: Path | None = None,
        *,
        workflow_status_resolver: WorkflowStatusResolver,
        contracts_config: ContractsConfig | None = None,
        context_loaded_writer: IContextLoadedWriter | None = None,
    ) -> None:
        super().__init__()
        self._settings = settings
        self._git_manager = git_manager
        self._project_manager = project_manager
        self._state_engine = state_engine
        self._github_manager = github_manager
        self._workphases_config = workphases_config
        self._state_path = state_path
        self._workflow_status_resolver = workflow_status_resolver
        self._contracts_config = contracts_config
        self._context_loaded_writer = context_loaded_writer

    async def execute(self, params: GetWorkContextInput, context: NoteContext) -> ToolResult:  # noqa: ARG002
        """Execute work context aggregation."""
        _ = params  # GetWorkContextInput has no fields after C1 (issue #268)

        branch = self._git_manager.get_current_branch()

        ctx: dict[str, Any] = {"current_branch": branch}

        # Primary state read: single source of truth (F_268.13, issue #268)
        workflow = ""
        phase = ""
        try:
            state = self._state_engine.get_state(branch)
            workflow = state.workflow_name or ""
            phase = state.current_phase or ""
            ctx["workflow_name"] = workflow
            ctx["phase"] = phase
            if state.issue_number is not None:
                ctx["issue_number"] = state.issue_number
            if state.parent_branch:
                ctx["parent_branch"] = state.parent_branch
            if state.current_cycle is not None:
                ctx["current_cycle"] = state.current_cycle
            if state.current_sub_phase:
                ctx["sub_phase"] = state.current_sub_phase
            ctx["phase_source"] = "state.json"
            ctx["phase_confidence"] = "high"
        except Exception:  # noqa: BLE001 - bootstrap: branch not yet initialized
            ctx["workflow_name"] = ""
            ctx["phase"] = ""
            ctx["phase_source"] = "unknown"
            ctx["phase_confidence"] = "unknown"

        instructions = None
        if self._contracts_config is not None and workflow and phase:
            try:
                workflow_entry = self._contracts_config.workflows.get(workflow)
                if workflow_entry is not None:
                    instructions = workflow_entry.get_phase(phase).instructions
            except (KeyError, ValueError):
                pass

        ctx["sub_role_hint"] = instructions.sub_role if instructions is not None else ""
        ctx["phase_instructions"] = (
            instructions.phase_instructions if instructions is not None else ""
        )
        if instructions is not None:
            ctx["handover_template"] = instructions.handover_template

        formatted = self._format_context(ctx)
        if self._context_loaded_writer is not None:
            self._context_loaded_writer.set_context_loaded(branch, value=True)
        return ToolResult.text(formatted)

    def _format_context(self, context: dict[str, Any]) -> str:
        """Format work context into compact orientation header + phase instructions block."""
        branch = context.get("current_branch", "")
        workflow = context.get("workflow_name", "")
        phase = context.get("phase", "")
        issue_number = context.get("issue_number")
        parent_branch = context.get("parent_branch", "")
        current_cycle = context.get("current_cycle")
        sub_phase = context.get("sub_phase")
        sub_role_hint = context.get("sub_role_hint", "")
        phase_source = context.get("phase_source", "unknown")
        phase_confidence = context.get("phase_confidence", "unknown")
        phase_instructions = context.get("phase_instructions", "")

        # Phase emoji mapping (7 workflow phases + unknown)
        phase_emoji = {
            "research": "🔍",
            "planning": "📋",
            "design": "🎨",
            "implementation": "🧪",
            "validation": "✅",
            "documentation": "📝",
            "coordination": "🤝",
        }.get(phase, "❓")

        # Sub-phase emoji (TDD-specific)
        subphase_emoji: dict[str, str] = {"red": "🔴", "green": "🟢", "refactor": "🔄"}

        lines: list[str] = []

        # Orientation line 1: branch | workflow | issue
        line1_parts = [f"Branch: `{branch}`"]
        if workflow:
            line1_parts.append(f"Workflow: {workflow}")
        if issue_number is not None:
            line1_parts.append(f"Issue: #{issue_number}")
        lines.append(" | ".join(line1_parts))

        # Orientation line 2: phase | role
        phase_display = f"{phase_emoji} {phase}" if phase else "❓ unknown"
        if sub_phase:
            emoji = subphase_emoji.get(str(sub_phase), "")
            phase_display += f" → {emoji} {sub_phase}".rstrip()
        if current_cycle is not None:
            phase_display += f" (cycle {current_cycle})"
        line2_parts = [f"Phase: {phase_display}"]
        if sub_role_hint:
            line2_parts.append(f"Role: {sub_role_hint}")
        lines.append(" | ".join(line2_parts))

        # Orientation line 3: parent branch (only if non-empty)
        if parent_branch:
            lines.append(f"Parent: {parent_branch}")

        # Orientation line 4: phase detection source (only if confidence != high)
        if phase_confidence != "high":
            lines.append(f"⚠️ Phase detection: source={phase_source}, confidence={phase_confidence}")
        lines.append(
            "TODO discipline: create or refresh your TODO list now; "
            "keep exactly one item in progress and update it after each material step."
        )

        # Separator
        lines.append("")
        lines.append("---")
        lines.append("")

        # Phase instructions block (dominant first block - F_268.13)
        lines.append("### 🎯 Phase Instructions")
        lines.append("")
        if phase_instructions:
            lines.append(phase_instructions)
        else:
            lines.append(
                f"(No instructions defined for workflow: {workflow or 'unknown'}, "
                f"phase: {phase or 'unknown'})"
            )

        handover_template = context.get("handover_template")
        if handover_template:
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append("### Hand-over Template")
            lines.append("")
            lines.append(handover_template)

        return "\n".join(lines)
