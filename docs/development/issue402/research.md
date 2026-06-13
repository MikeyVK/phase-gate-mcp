<!-- c:\temp\pgmcp\docs\development\issue402\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-12T05:54:00Z updated=2026-06-12T06:00:00Z -->
# Research — Issue #402: Expose JSON data in MCP tools

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-06-12

---

## Purpose

Investigate the migration of MCP tools to StructuredTool and establish a stable research nucleus.

## Scope

**In Scope:**
- All registered MCP tools in the `mcp_server/tools/` directory.
- Standardisation of JSON output payloads for tools.
- Presentation of options for defining JSON schemas.
- Blast radius and test suite impact evaluation.

**Out of Scope:**
- External libraries, protocols outside MCP, or changes to client implementations.

---

## Problem Statement

Expose structured JSON data alongside human-readable text fallbacks in the ToolResult responses of MCP tools (in accordance with the design contract established in #301).

## Research Goals

- Identify how existing tools produce JSON data and standardise them.
- Formulate an exclusion list of tools that do not require JSON output.
- Compare options for defining JSON schemas (raw dicts vs Pydantic models).
- Analyse the data to be returned by each tool and design the accompanying text output.

---

## Background

Initial research under Issue #301 laid the groundwork, and Issue #390 introduced `StructuredTool` and `mcp_converters.py`.

---

## Findings

### 1. Existing Behavior and Patterns
Our MCP server uses a two-tiered tool response model:
- **`BaseTool` / `BaseTool.execute`:** Returns `ToolResult.text(...)`, which produces a single content block of type `"text"`. Standard MCP clients receive `structuredContent = None`.
- **`StructuredTool` / `StructuredTool.execute_structured`:** Returns a tuple `(data_dict, summary_text)`. The base class maps this to `ToolResult.json_data(data_dict, text=summary_text)`, creating two content blocks: `content[0]` of type `"json"`, and `content[1]` of type `"text"`. The server's `convert_tool_result_to_mcp_result` extracts the JSON block to `CallToolResult.structuredContent` and leaves the text fallback block in `CallToolResult.content`.

### 2. Comprehensive Tool-by-Tool Analysis
| Tool Class | File | Target Output | Available Data | Text Fallback Focus | Exclusion Rationale / Notes |
|---|---|---|---|---|---|
| `RestartServerTool` | `admin_tools.py` | Excluded | None | N/A | Signal tool; no domain data. |
| `TransitionCycleTool` | `cycle_tools.py` | JSON + Text | `{"success": true, "branch": str, "old_cycle": str, "new_cycle": str}` | Summary of the transition including branch name, old and new cycle phases. | |
| `ForceCycleTransitionTool` | `cycle_tools.py` | JSON + Text | `{"success": true, "branch": str, "old_cycle": str, "new_cycle": str}` | Summary of the forced transition including branch name, old and new cycle phases. | |
| `SearchDocumentationTool` | `discovery_tools.py` | JSON + Text | `{"query": str, "results": [{"title": str, "path": str, "score": float, "snippet": str}]}` | List of titles, paths, and scores of relevant found documentation matches. | |
| `GetWorkContextTool` | `discovery_tools.py` | JSON + Text | *Already Structured* | Structured overview of the currently active branch, phase, and task context. | Structured in #390. |
| `GitListBranchesTool` | `git_analysis_tools.py` | JSON + Text | `{"branches": [str], "current_branch": str}` | Overview of all available branches indicating the currently active branch. | |
| `GitDiffTool` | `git_analysis_tools.py` | JSON + Text | `{"target_branch": str, "source_branch": str, "stats": str}` | Statistical summary of modified lines and files between the target and source branches. | |
| `GitFetchTool` | `git_fetch_tool.py` | JSON + Text | `{"success": true, "remote": str}` | Confirmation of the updated remote and any pruned branches. | |
| `GitPullTool` | `git_pull_tool.py` | JSON + Text | `{"success": true, "remote": str, "branch": str}` | Status of the pulled changes including remote and branch names. | |
| `CreateBranchTool` | `git_tools.py` | JSON + Text | `{"success": true, "branch_name": str, "base_branch": str}` | Confirmation of the newly created branch and its source branch. | |
| `GitStatusTool` | `git_tools.py` | JSON + Text | `{"branch": str, "is_clean": bool, "modified_files": [str], "untracked_files": [str]}` | Overview of the current branch status and modified/untracked files. | |
| `GitCommitTool` | `git_tools.py` | JSON + Text | `{"sha": str, "branch": str, "message": str, "files": [str]}` | Details of the new commit, such as SHA, branch, commit message, and affected files. | |
| `GitRestoreTool` | `git_tools.py` | JSON + Text | `{"success": true, "files": [str]}` | List of restored files. | |
| `GitCheckoutTool` | `git_tools.py` | JSON + Text | `{"branch": str}` | Name of the newly active branch. | |
| `GitPushTool` | `git_tools.py` | JSON + Text | `{"success": true, "remote": str, "branch": str}` | Status of the push operation including remote and branch names. | |
| `GitMergeTool` | `git_tools.py` | JSON + Text | `{"success": true, "merge_sha": str}` | Confirmation of the successful merge and the resulting commit SHA. | |
| `GitDeleteBranchTool` | `git_tools.py` | JSON + Text | `{"success": true, "branch": str}` | Confirmation of the deleted branch. | |
| `GitStashTool` | `git_tools.py` | JSON + Text | `{"success": true, "action": str}` | Status of the stash operation and the executed action. | |
| `GetParentBranchTool` | `git_tools.py` | JSON + Text | `{"branch": str, "parent_branch": str}` | Name of the active branch and the identified parent branch. | |
| `CheckMergeTool` | `git_tools.py` | JSON + Text | `{"target_branch": str, "source_branch": str, "is_ancestor": bool}` | Status of whether the source branch is fully merged into the target branch. | |
| `HealthCheckTool` | `health_tools.py` | Excluded | None | N/A | Standard ping tool; no complex data. |
| `CreateIssueTool` | `issue_tools.py` | JSON + Text | `{"issue": {"number": int, "title": str, "state": str, "labels": [str]}}` | Overview of the newly created GitHub issue, including number, title, and labels. | |
| `GetIssueTool` | `issue_tools.py` | JSON + Text | *Already Structured* | Detailed information of the retrieved issue including status, description, and assignees. | Structured in #390. |
| `ListIssuesTool` | `issue_tools.py` | JSON + Text | `{"issues": [{"number": int, "title": str, "state": str}]}` | List of open/closed issues filtered by labels or milestone. | |
| `UpdateIssueTool` | `issue_tools.py` | JSON + Text | `{"issue": {"number": int, "title": str, "state": str}}` | Summary of the modified issue properties and status. | |
| `CloseIssueTool` | `issue_tools.py` | JSON + Text | `{"issue_number": int, "success": bool}` | Confirmation that the specific issue has been closed. | |
| `ListLabelsTool` | `label_tools.py` | JSON + Text | `{"labels": [{"name": str, "color": str, "description": str}]}` | Overview of available labels with their colors and descriptions. | |
| `CreateLabelTool` | `label_tools.py` | JSON + Text | `{"label": {"name": str, "color": str}}` | Details of the newly created label. | |
| `DeleteLabelTool` | `label_tools.py` | JSON + Text | `{"success": true, "label": str}` | Confirmation of the deleted label. | |
| `RemoveLabelsTool` | `label_tools.py` | JSON + Text | `{"issue_number": int, "labels": [str]}` | List of labels removed from the issue. | |
| `AddLabelsTool` | `label_tools.py` | JSON + Text | `{"issue_number": int, "labels": [str]}` | List of labels added to the issue. | |
| `ListMilestonesTool` | `milestone_tools.py` | JSON + Text | `{"milestones": [{"number": int, "title": str, "state": str}]}` | List of active milestones and their status. | |
| `CreateMilestoneTool` | `milestone_tools.py` | JSON + Text | `{"milestone": {"number": int, "title": str, "state": str}}` | Confirmation of the new milestone with its title and due date if applicable. | |
| `CloseMilestoneTool` | `milestone_tools.py` | JSON + Text | `{"milestone": {"number": int, "title": str, "state": str}}` | Confirmation of the closed milestone. | |
| `TransitionPhaseTool` | `phase_tools.py` | JSON + Text | `{"success": true, "branch": str, "old_phase": str, "new_phase": str}` | Status of the phase transition including branch name, old phase, and new phase. | |
| `ForcePhaseTransitionTool` | `phase_tools.py` | JSON + Text | `{"success": true, "branch": str, "old_phase": str, "new_phase": str, "skip_reason": str}` | Details of the forced phase transition, including branch name, old/new phase, and the skip reason. | |
| `ListPRsTool` | `pr_tools.py` | JSON + Text | `{"pull_requests": [{"number": int, "title": str, "state": str}]}` | Overview of pull requests and their current status. | |
| `MergePRTool` | `pr_tools.py` | JSON + Text | `{"success": true, "pr_number": int}` | Confirmation of the successfully merged pull request. | |
| `GetPRTool` | `pr_tools.py` | JSON + Text | *Already Structured* | Details of the retrieved pull request including status and reviews. | Structured in #390. |
| `SubmitPRTool` | `pr_tools.py` | JSON + Text | `{"pull_request": {"number": int, "title": str, "state": str}}` | Details of the submitted pull request with link and PR number. | |
| `InitializeProjectTool` | `project_tools.py` | JSON + Text | *Already Structured* | Confirmation of project initialization with the selected workflow and issues. | Structured in #390. |
| `GetProjectPlanTool` | `project_tools.py` | JSON + Text | *Already Structured* | Overview of phases and tasks in the project plan. | Structured in #390. |
| `SavePlanningDeliverablesTool` | `project_tools.py` | JSON + Text | *Already Structured* | Status of the saved planning deliverables. | Structured in #390. |
| `UpdatePlanningDeliverablesTool` | `project_tools.py` | JSON + Text | *Already Structured* | Status of the updated planning deliverables. | Structured in #390. |
| `RunQualityGatesTool` | `quality_tools.py` | JSON + Text | `{"overall_pass": bool, "gates": [dict]}` | Summary of the executed quality gates and whether they passed. | Currently custom dual-result. |
| `SafeEditTool` | `safe_edit_tool.py` | JSON + Text | `{"passed": bool, "issues": str, "diff": str}` | Result of the file modification, including diff preview and any validation errors. | |
| `ScaffoldArtifactTool` | `scaffold_artifact.py` | JSON + Text | *Already Structured* | Confirmation of the generated files and their template type. | Structured in #390. |
| `ScaffoldSchemaTool` | `scaffold_schema_tool.py` | JSON + Text | *Already Structured* | Structured schema for the specified artifact type. | Structured in #390. |
| `TemplateValidationTool` | `template_validation_tool.py` | JSON + Text | `{"passed": bool, "issues": [{"severity": str, "message": str}]}` | Report of the template validation with any warnings or errors. | |
| `RunTestsTool` | `test_tools.py` | JSON + Text | `{"exit_code": int, "summary": dict}` | Summary of the test results including the number of passed/failed tests and exit code. | Currently custom dual-result. |
To define JSON schemas for tool output data, we consider two options:

#### Option A: Raw untyped Python dicts (`dict[str, Any]`)
- **Pros:** Fast implementation, zero boilerplate, high flexibility.
- **Cons:** Violates `ARCHITECTURE_PRINCIPLES.md` §8 (Explicit over Implicit) and §5 (Command/Query Separation). Boundaries remain untyped, risking serialization errors and client incompatibilities.

#### Option B: Declarative Pydantic Models for Tool Output (Recommended)
- **Pros:** Statically typed output schemas, validation at boundaries, clear self-documenting interface, fully compliant with ARCHITECTURE_PRINCIPLES.md §8 and §5. Frozen models prevent command/query state contamination.
- **Cons:** Additional boilerplate file (`mcp_server/schemas/tool_outputs.py`) to manage.

**Architectural Alignment:** Option B is recommended because it respects type safety at system boundaries and avoids implicit data structures, fulfilling the prime directives.

### 4. Blast Radius and Test-Suite Impact
- **The Issue:** Dual-payload `ToolResult` (from `ToolResult.json_data()`) sets the JSON block as `content[0]` and the text block as `content[1]`.
- **The Blast Radius:** More than 200 unit test assertions in `tests/mcp_server/unit/tools/` check `result.content[0]["text"]` to verify text outputs. Converting all tools to `StructuredTool` will cause all these assertions to fail with a `KeyError`, as index 0 becomes a JSON block.
- **Mitigation:** Implement a custom test helper `get_text_content(result: ToolResult) -> str` that extracts the text block regardless of its index position in `content`, and update unit tests to use this helper.

---

## Open Questions

1. Should the test helper be globally registered in `tests/mcp_server/test_support.py`?
2. Do we require strict schema validation on the output payload at runtime, or only for unit test assertions?

---

## Approved Strategy

### Boundary / consumer scope
All MCP tools in `mcp_server/tools/` without exception (including admin, health, and signal tools such as `HealthCheckTool` and `RestartServerTool` to ensure 100% uniformity and avoid custom python formatters/circular logic).

### Selected strategy
Option B: Pydantic-defined schemas for tool outputs, with migration of all tools to `StructuredTool`.

### Rationale
Provides explicit boundary validation, preventing drift and ensuring client compatibility without violating SRP/CQS. Migrating all tools guarantees architectural consistency and a single presentation flow.

### Constraints for later phases
- Do not instantiate outputs inside `execute_structured` directly if they bypass defined schema models.
- All unit tests must use the new index-agnostic assertion helper.
