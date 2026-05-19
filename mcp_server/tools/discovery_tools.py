"""Discovery tools for AI self-orientation."""

# pyright: reportIncompatibleMethodOverride=false
from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict, Field

from mcp_server.config.settings import Settings
from mcp_server.core.exceptions import ExecutionError, MCPError
from mcp_server.core.operation_notes import NoteContext, RecoveryNote
from mcp_server.core.phase_detection import PhaseDetectionResult, ScopeDecoder
from mcp_server.managers.git_manager import GitManager
from mcp_server.managers.github_manager import GitHubManager
from mcp_server.managers.phase_state_engine import PhaseStateEngine
from mcp_server.managers.project_manager import ProjectManager
from mcp_server.managers.state_repository import StateBranchMismatchError, StateNotFoundError
from mcp_server.schemas import WorkphasesConfig
from mcp_server.services.document_indexer import DocumentIndexer
from mcp_server.services.search_service import SearchService
from mcp_server.tools.base import BaseTool
from mcp_server.tools.tool_result import ToolResult

if TYPE_CHECKING:
    from mcp_server.managers.workflow_status_resolver import WorkflowStatusResolver


# TODO(MVP): Replace with contracts.yaml instructions section on full implementation (issue #268).
_SUB_ROLE_MAP: dict[str, str] = {
    "research": "researcher",
    "design": "designer",
    "planning": "planner",
    "implementation": "implementer",
    "validation": "validator",
    "documentation": "documenter",
    "ready": "documenter",
}

# TODO(MVP): Replace with contracts.yaml instructions section on full implementation (issue #268).
# Keyed by (workflow_name, phase_name). phase_instructions embeds the hand-over format
# inline for roles that produce hand-overs. This avoids a universal handover_template field
# that would be incorrect for non-hand-over roles.
# Human-readable reference: docs/development/issue268/bug-workflow-phase-instructions.md.
# Python strings here are the runtime SSOT; the markdown is for review and refinement only.
_PHASE_INSTRUCTIONS_MAP: dict[tuple[str, str], str] = {
    # ------------------------------------------------------------------ bug --
    ("bug", "research"): (
        "Create a TODO list now and work through it step by step:\n\n"
        "[ ] Call get_issue(issue_number=N) \u2014 read problem, expected behavior,\n"
        "    and all linked code locations.\n"
        "[ ] Locate root cause: grep_search + read_file on affected files and methods.\n"
        "[ ] Identify all callers: vscode_listCodeUsages or grep_search.\n"
        "[ ] scaffold_artifact(artifact_type='research', name='issueN-research').\n"
        "    Required sections: Problem, Root Cause, Affected Files, Impact,\n"
        "    Solution Options A and B, Recommended Option + Rationale.\n"
        "[ ] Exit gate: docs/development/issueN/research*.md must exist.\n"
        "[ ] git_add_or_commit(workflow_phase='research', message='Add research: ...')\n"
        "[ ] transition_phase(branch='...', to_phase='design')\n"
        "[ ] get_work_context (mandatory after every transition)\n\n"
        "Produce this hand-over before ending the session:\n"
        "### Research \u2192 Design hand-over\n"
        "**Root cause:** <one sentence>\n"
        "**Affected method(s):** <file:method>\n"
        "**Recommended option:** <A or B> \u2014 <rationale>\n"
        "**Key constraint:** <architectural rule that applies>\n"
        "**Scope for designer:** elaborate chosen option only; do not implement yet."
    ),
    ("bug", "design"): (
        "Create a TODO list now and work through it step by step:\n\n"
        "[ ] Read: docs/development/issueN/research.md"
        " (or Research \u2192 Design hand-over).\n"
        "[ ] Elaborate chosen option:\n"
        "    - exact method signature changes (parameters, return types)\n"
        "    - new error type(s) (name, base class, message format)\n"
        "    - edge cases: state absent, branch mismatch, concurrent writes\n"
        "    - callers that need updating\n"
        "[ ] Define test strategy: which tests (unit/integration),\n"
        "    mock boundaries, coverage targets.\n"
        "[ ] scaffold_artifact(artifact_type='design', name='issueN-design').\n"
        "    Required sections: Chosen Solution, Implementation Details,\n"
        "    Affected Interfaces, Edge Cases, Test Strategy.\n"
        "[ ] Exit gate: docs/development/issueN/design*.md must exist.\n"
        "[ ] git_add_or_commit(workflow_phase='design', message='Add design: ...')\n"
        "[ ] transition_phase(branch='...', to_phase='planning')\n"
        "[ ] get_work_context (mandatory after every transition)\n\n"
        "Produce this hand-over before ending the session:\n"
        "### Design \u2192 Planning hand-over\n"
        "**Changed methods:** <file:method \u2014 before/after signature>\n"
        "**New error type:** <ClassName(BaseClass) \u2014 message format>\n"
        "**Edge cases covered:** <N edge cases listed>\n"
        "**Estimated TDD cycles:** <1\u20133>\n"
        "**Test file:** <path>\n"
        "**Implementation file:** <path>\n"
        "**Scope for planner:** split into cycles; do not write code yet."
    ),
    ("bug", "planning"): (
        "Create a TODO list now and work through it step by step:\n\n"
        "[ ] Read: research + design documents (or summaries from hand-overs).\n"
        "[ ] Decide cycle count (bugs: 1\u20132 cycles, max 3).\n"
        "[ ] Per cycle: define name, deliverables (concrete output items),\n"
        "    exit_criteria (one sentence per cycle).\n"
        "[ ] scaffold_artifact(artifact_type='planning', name='issueN-planning').\n"
        "[ ] save_planning_deliverables(issue_number=N, planning_deliverables={\n"
        "      'tdd_cycles': {'total': N, 'cycles': [\n"
        "        {'cycle_number': 1, 'name': '...', 'deliverables': ['...'],\n"
        "         'exit_criteria': '...'}\n"
        "      ]}\n"
        "    })\n"
        "[ ] Exit gate: docs/development/issueN/planning*.md must exist.\n"
        "[ ] git_add_or_commit(workflow_phase='planning', message='Add planning: ...')\n"
        "[ ] transition_phase(branch='...', to_phase='implementation')\n"
        "[ ] get_work_context (mandatory after every transition)\n\n"
        "Produce this hand-over before ending the session:\n"
        "### Planning \u2192 Implementation hand-over\n"
        "**Total cycles:** N\n"
        "**Cycle 1:** <name>\n"
        "  - Deliverables: <list>\n"
        "  - Exit criteria: <sentence>\n"
        "**Test file:** <path>\n"
        "**Implementation file:** <path>\n"
        "**Scope for implementer:**"
        " execute cycles in strict RED\u2192GREEN\u2192REFACTOR order only."
    ),
    ("bug", "implementation"): (
        "Create a TODO list now and work through it step by step:\n\n"
        "[ ] Call get_project_plan(issue_number=N) \u2014 read ALL cycle deliverables\n"
        "    before writing any code.\n\n"
        "Per cycle (repeat until all cycles complete):\n"
        "[ ] RED: write failing test first \u2014 no implementation code yet.\n"
        "    run_tests(path='<test file>') \u2014 verify it FAILS.\n"
        "    git_add_or_commit(workflow_phase='implementation', sub_phase='red',\n"
        "      cycle_number=N, message='...')\n"
        "[ ] GREEN: write minimal code to pass the test \u2014 no cleanup yet.\n"
        "    run_tests(path='<test file>') \u2014 verify it PASSES.\n"
        "    git_add_or_commit(workflow_phase='implementation', sub_phase='green',\n"
        "      cycle_number=N, message='...')\n"
        "[ ] REFACTOR: clean up while keeping tests green.\n"
        "    run_quality_gates(scope='files', files=['<changed files>'])\n"
        "    git_add_or_commit(workflow_phase='implementation', sub_phase='refactor',\n"
        "      cycle_number=N, message='...')\n"
        "[ ] If more cycles: transition_cycle(to_cycle=N+1), then get_work_context.\n\n"
        "Hard rules \u2014 never violate:\n"
        "- RED is mandatory. Never write implementation before a failing test.\n"
        "- Never skip REFACTOR. Quality gates are enforced here.\n"
        "- Never self-declare GO. QA decides after reviewing the hand-over.\n"
        "- Never call merge_pr. Human approval is required.\n\n"
        "Produce this hand-over when all cycles are complete:\n"
        "### Imp \u2192 QA hand-over\n"
        "#### Scope\n"
        "- Cycles executed: <list>\n"
        "- Out of scope: <list>\n"
        "#### Files\n"
        "**Tests:** <path> (new/modified)\n"
        "**Implementation:** <path> (new/modified)\n"
        "#### Deliverables\n"
        "- C1.D1: <name> \u2014 \u2705 satisfied | \u274c not satisfied\n"
        "#### Stop-Go Proof\n"
        "- Tests: run_tests(path='...') \u2192 <N passed, 0 failed>\n"
        "- Gates: run_quality_gates(scope='files') \u2192 <N/N green>"
    ),
    ("bug", "validation"): (
        "Create a TODO list now and work through it step by step:\n\n"
        "[ ] Read the Imp\u2192QA hand-over from the implementation session.\n"
        "[ ] get_project_plan(issue_number=N) \u2014 verify all deliverables satisfied.\n"
        "[ ] run_tests(scope='full') \u2014 full suite, zero failures required.\n"
        "[ ] run_quality_gates(scope='branch') \u2014 all branch-changed files.\n"
        "[ ] Gate 7 \u2014 Architectural review (ARCHITECTURE_PRINCIPLES.md):\n"
        "    [ ] SRP: each new/changed class has one responsibility.\n"
        "    [ ] OCP: no new if-chain on phase/workflow/action names.\n"
        "    [ ] DIP: no direct instantiation inside execute().\n"
        "    [ ] CQS: no query method calls save() or mutates state.\n"
        "    [ ] Config-First: no hardcoded phase/workflow names in production.\n"
        "    [ ] No import-time side effects.\n"
        "    [ ] ISP: read-only consumers use narrow read-only interface.\n"
        "[ ] If any check fails: produce STOP verdict, list findings, stop here.\n"
        "[ ] If all green: git_add_or_commit +"
        " transition_phase(to_phase='documentation')\n"
        "[ ] get_work_context (mandatory after every transition)\n\n"
        "Produce this hand-over before ending the session:\n"
        "### Validation hand-over\n"
        "**Verdict:** STOP | GO\n"
        "**Tests:** run_tests(scope='full') \u2192 <N passed, 0 failed>\n"
        "**Gates:** run_quality_gates(scope='branch') \u2192 <N/N green>\n"
        "**Architecture:** GO: no violations | STOP: <file>:<line> \u2014 <principle>\n"
        "**For documenter:** PR bullets: <2\u20133 key changes in plain English>"
    ),
    ("bug", "documentation"): (
        "Create a TODO list now and work through it step by step:\n\n"
        "[ ] Confirm validation verdict is GO before proceeding."
        " STOP if verdict is STOP.\n"
        "[ ] Read validation hand-over for PR description bullets.\n"
        "[ ] Check for affected reference documentation:\n"
        "    docs/reference/ \u2014 if a tool signature or behavior changed.\n"
        "    docs/coding_standards/ \u2014 if an architectural pattern was applied newly.\n"
        "    AGENTS.md \u2014 if agent workflow was affected.\n"
        "[ ] Update affected reference docs using safe_edit_file.\n"
        "[ ] git_add_or_commit(workflow_phase='documentation',"
        " message='Document: ...')\n"
        "[ ] transition_phase(branch='...', to_phase='ready')\n"
        "[ ] get_work_context (mandatory after every transition)\n\n"
        "Produce this hand-over before ending the session:\n"
        "### Documentation hand-over\n"
        "**Updated docs:** <path \u2014 what changed> (or: none required)\n"
        "**PR body:**\n"
        "## Summary\n"
        "<2\u20133 sentences: what was fixed and why>\n"
        "## Changes\n"
        "- <bullet per meaningful change>\n"
        "## Test coverage\n"
        "- <N new tests> covering: <what>"
    ),
    ("bug", "ready"): (
        "Create a TODO list now and work through it step by step:\n\n"
        "[ ] Confirm phase=ready via get_work_context output.\n"
        "[ ] submit_pr(\n"
        "      head='<current branch>',\n"
        "      base='<parent branch from get_work_context>',\n"
        "      title='fix: <description> (#N)',\n"
        "      body='<PR body from documentation hand-over>'\n"
        "    )\n"
        "    Note: submit_pr is atomic \u2014 it neutralizes branch-local artifacts,\n"
        "    commits, pushes, and creates the GitHub PR in one call.\n"
        "    Do NOT push manually before calling submit_pr.\n"
        "[ ] Report the PR URL to the user.\n"
        "[ ] STOP. Do not call merge_pr. Human approval is required."
    ),
    # --------------------------------------------------------------- feature --
    ("feature", "implementation"): (
        "Create a TODO list now and work through it step by step:\n\n"
        "[ ] Call get_project_plan(issue_number=N) \u2014 read ALL cycle deliverables\n"
        "    before writing any code.\n\n"
        "Per cycle (repeat until all cycles complete):\n"
        "[ ] RED: write failing test first \u2014 no implementation code yet.\n"
        "    run_tests(path='<test file>') \u2014 verify it FAILS.\n"
        "    git_add_or_commit(workflow_phase='implementation', sub_phase='red',\n"
        "      cycle_number=N, message='...')\n"
        "[ ] GREEN: write minimal code to pass the test \u2014 no cleanup yet.\n"
        "    run_tests(path='<test file>') \u2014 verify it PASSES.\n"
        "    git_add_or_commit(workflow_phase='implementation', sub_phase='green',\n"
        "      cycle_number=N, message='...')\n"
        "[ ] REFACTOR: clean up while keeping tests green.\n"
        "    run_quality_gates(scope='files', files=['<changed files>'])\n"
        "    git_add_or_commit(workflow_phase='implementation', sub_phase='refactor',\n"
        "      cycle_number=N, message='...')\n"
        "[ ] If more cycles: transition_cycle(to_cycle=N+1), then get_work_context.\n\n"
        "Hard rules \u2014 never violate:\n"
        "- RED is mandatory. Never write implementation before a failing test.\n"
        "- Never skip REFACTOR. Quality gates are enforced here.\n"
        "- Never self-declare GO. QA decides after reviewing the hand-over.\n"
        "- Never call merge_pr. Human approval is required.\n\n"
        "Produce this hand-over when all cycles are complete:\n"
        "### Imp \u2192 QA hand-over\n"
        "#### Scope\n"
        "- Cycles executed: <list>\n"
        "- Out of scope: <list>\n"
        "#### Files\n"
        "**Tests:** <path> (new/modified)\n"
        "**Implementation:** <path> (new/modified)\n"
        "#### Deliverables\n"
        "- C1.D1: <name> \u2014 \u2705 satisfied | \u274c not satisfied\n"
        "#### Stop-Go Proof\n"
        "- Tests: run_tests(path='...') \u2192 <N passed, 0 failed>\n"
        "- Gates: run_quality_gates(scope='files') \u2192 <N/N green>"
    ),
}


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

    async def execute(self, params: GetWorkContextInput, context: NoteContext) -> ToolResult:
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

        ctx["sub_role_hint"] = _SUB_ROLE_MAP.get(phase, "")
        ctx["phase_instructions"] = _PHASE_INSTRUCTIONS_MAP.get((workflow, phase), "")

        return ToolResult.text(self._format_context(ctx))

    def _extract_issue_number(self, branch: str) -> int | None:
        """Extract issue number from branch name."""
        patterns = [
            r"(?:feature|fix|refactor|docs)/(\d+)-",
            r"issue-(\d+)",
            r"#(\d+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, branch)
            if match:
                return int(match.group(1))

        return None

    def _detect_workflow_phase(self, commits: list[str]) -> PhaseDetectionResult:
        """
        Detect workflow phase deterministically using ScopeDecoder.

        NOTE: This method is only called when the WorkflowStatusResolver is not
        injected. When the resolver is present (standard path), phase comes from
        state.json authoritatively (Issue #298). This fallback path is retained
        for backward compatibility only.

        Args:
            commits: Recent commit messages

        Returns:
            PhaseDetectionResult dict with workflow_phase, sub_phase, source, confidence
        """
        if not commits:
            return {
                "workflow_phase": "unknown",
                "sub_phase": None,
                "source": "unknown",
                "confidence": "unknown",
                "raw_scope": None,
                "error_message": None,
            }

        # Use most recent commit for phase detection
        latest_commit = commits[0]

        # Deterministic phase detection via ScopeDecoder
        if self._workphases_config is None:
            return {
                "workflow_phase": "unknown",
                "sub_phase": None,
                "source": "unknown",
                "confidence": "unknown",
                "raw_scope": None,
                "error_message": "WorkphasesConfig not injected",
            }
        decoder = ScopeDecoder(self._workphases_config, state_path=self._state_path)
        return decoder.detect_phase(commit_message=latest_commit, fallback_to_state=True)

    def _extract_checklist(self, body: str) -> list[str]:
        """Extract checklist items from issue body."""
        if not body:
            return []

        pattern = r"- \[[ x]\] (.+)"
        matches = re.findall(pattern, body)
        return matches[:10]  # Limit to 10 items

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
            lines.append(
                f"⚠️ Phase detection: source={phase_source}, confidence={phase_confidence}"
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

        return "\n".join(lines)
