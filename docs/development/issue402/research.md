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
The following table lists all 51 tools in the codebase, assessing whether they should produce JSON, the available data, and the designed chat presentation text:

| Tool Class | File | Target Output | Available Data | Designed Chat Text | Exclusion Rationale / Notes |
|---|---|---|---|---|---|
| `RestartServerTool` | `admin_tools.py` | Excluded | None | `Server restarting...` | Signal tool; no domain data. |
| `TransitionCycleTool` | `cycle_tools.py` | JSON + Text | `{"success": true, "branch": str, "old_cycle": str, "new_cycle": str}` | `Transitioned cycle on branch {branch} from {old} to {new}.` | |
| `ForceCycleTransitionTool` | `cycle_tools.py` | JSON + Text | `{"success": true, "branch": str, "old_cycle": str, "new_cycle": str}` | `Force transitioned cycle on branch {branch} from {old} to {new}.` | |
| `SearchDocumentationTool` | `discovery_tools.py` | JSON + Text | `{"query": str, "results": [{"title": str, "path": str, "score": float, "snippet": str}]}` | List of found doc results. | |
| `GetWorkContextTool` | `discovery_tools.py` | JSON + Text | *Already Structured* | Renders context. | Structured in #390. |
| `GitListBranchesTool` | `git_analysis_tools.py` | JSON + Text | `{"branches": [str], "current_branch": str}` | List of branches. | |
| `GitDiffTool` | `git_analysis_tools.py` | JSON + Text | `{"target_branch": str, "source_branch": str, "stats": str}` | Diff statistics. | |
| `GitFetchTool` | `git_fetch_tool.py` | JSON + Text | `{"success": true, "remote": str}` | `Fetched remote {remote}.` | |
| `GitPullTool` | `git_pull_tool.py` | JSON + Text | `{"success": true, "remote": str, "branch": str}` | `Pulled from {remote}/{branch}.` | |
| `CreateBranchTool` | `git_tools.py` | JSON + Text | `{"success": true, "branch_name": str, "base_branch": str}` | `Created branch {branch_name} from {base_branch}.` | |
| `GitStatusTool` | `git_tools.py` | JSON + Text | `{"branch": str, "is_clean": bool, "modified_files": [str], "untracked_files": [str]}` | Branch status details. | |
| `GitCommitTool` | `git_tools.py` | JSON + Text | `{"sha": str, "branch": str, "message": str, "files": [str]}` | Commit details. | |
| `GitRestoreTool` | `git_tools.py` | JSON + Text | `{"success": true, "files": [str]}` | `Restored files: ...` | |
| `GitCheckoutTool` | `git_tools.py` | JSON + Text | `{"branch": str}` | `Checked out {branch}.` | |
| `GitPushTool` | `git_tools.py` | JSON + Text | `{"success": true, "remote": str, "branch": str}` | `Pushed to {remote}/{branch}.` | |
| `GitMergeTool` | `git_tools.py` | JSON + Text | `{"success": true, "merge_sha": str}` | `Merged successfully.` | |
| `GitDeleteBranchTool` | `git_tools.py` | JSON + Text | `{"success": true, "branch": str}` | `Deleted branch {branch}.` | |
| `GitStashTool` | `git_tools.py` | JSON + Text | `{"success": true, "action": str}` | `Stashed changes.` | |
| `GetParentBranchTool` | `git_tools.py` | JSON + Text | `{"branch": str, "parent_branch": str}` | `Parent branch is {parent_branch}.` | |
| `CheckMergeTool` | `git_tools.py` | JSON + Text | `{"target_branch": str, "source_branch": str, "is_ancestor": bool}` | `Branch is merged: {is_ancestor}` | |
| `HealthCheckTool` | `health_tools.py` | Excluded | None | `OK` | Standard ping tool; no complex data. |
| `CreateIssueTool` | `issue_tools.py` | JSON + Text | `{"issue": {"number": int, "title": str, "state": str, "labels": [str]}}` | `Created issue #{number}: {title}` | |
| `GetIssueTool` | `issue_tools.py` | JSON + Text | *Already Structured* | Issue details. | Structured in #390. |
| `ListIssuesTool` | `issue_tools.py` | JSON + Text | `{"issues": [{"number": int, "title": str, "state": str}]}` | List of issues. | |
| `UpdateIssueTool` | `issue_tools.py` | JSON + Text | `{"issue": {"number": int, "title": str, "state": str}}` | `Updated issue #{number}` | |
| `CloseIssueTool` | `issue_tools.py` | JSON + Text | `{"issue_number": int, "success": bool}` | `Closed issue #{issue_number}` | |
| `ListLabelsTool` | `label_tools.py` | JSON + Text | `{"labels": [{"name": str, "color": str, "description": str}]}` | List of labels. | |
| `CreateLabelTool` | `label_tools.py` | JSON + Text | `{"label": {"name": str, "color": str}}` | `Created label {name}` | |
| `DeleteLabelTool` | `label_tools.py` | JSON + Text | `{"success": true, "label": str}` | `Deleted label {label}` | |
| `RemoveLabelsTool` | `label_tools.py` | JSON + Text | `{"issue_number": int, "labels": [str]}` | `Removed labels from #{issue_number}` | |
| `AddLabelsTool` | `label_tools.py` | JSON + Text | `{"issue_number": int, "labels": [str]}` | `Added labels to #{issue_number}` | |
| `DetectLabelDriftTool` | `label_tools.py` | JSON + Text | `{"github_only": [str], "yaml_only": [str], "mismatches": [dict]}` | Label drift report. | |
| `ListMilestonesTool` | `milestone_tools.py` | JSON + Text | `{"milestones": [{"number": int, "title": str, "state": str}]}` | List of milestones. | |
| `CreateMilestoneTool` | `milestone_tools.py` | JSON + Text | `{"milestone": {"number": int, "title": str, "state": str}}` | `Created milestone {title}` | |
| `CloseMilestoneTool` | `milestone_tools.py` | JSON + Text | `{"milestone": {"number": int, "title": str, "state": str}}` | `Closed milestone {title}` | |
| `TransitionPhaseTool` | `phase_tools.py` | JSON + Text | `{"success": true, "branch": str, "old_phase": str, "new_phase": str}` | Phase transition report. | |
| `ForcePhaseTransitionTool` | `phase_tools.py` | JSON + Text | `{"success": true, "branch": str, "old_phase": str, "new_phase": str, "skip_reason": str}` | Force transition report. | |
| `ListPRsTool` | `pr_tools.py` | JSON + Text | `{"pull_requests": [{"number": int, "title": str, "state": str}]}` | List of PRs. | |
| `MergePRTool` | `pr_tools.py` | JSON + Text | `{"success": true, "pr_number": int}` | `Merged pull request #{pr_number}` | |
| `GetPRTool` | `pr_tools.py` | JSON + Text | *Already Structured* | PR details. | Structured in #390. |
| `SubmitPRTool` | `pr_tools.py` | JSON + Text | `{"pull_request": {"number": int, "title": str, "state": str}}` | `Submitted pull request #{number}` | |
| `InitializeProjectTool` | `project_tools.py` | JSON + Text | *Already Structured* | Project initialization. | Structured in #390. |
| `GetProjectPlanTool` | `project_tools.py` | JSON + Text | *Already Structured* | Project plan. | Structured in #390. |
| `SavePlanningDeliverablesTool` | `project_tools.py` | JSON + Text | *Already Structured* | Deliverables saved. | Structured in #390. |
| `UpdatePlanningDeliverablesTool` | `project_tools.py` | JSON + Text | *Already Structured* | Deliverables updated. | Structured in #390. |
| `RunQualityGatesTool` | `quality_tools.py` | JSON + Text | `{"overall_pass": bool, "gates": [dict]}` | Quality gates summary. | Currently custom dual-result. |
| `SafeEditTool` | `safe_edit_tool.py` | JSON + Text | `{"passed": bool, "issues": str, "diff": str}` | Edit result details. | |
| `ScaffoldArtifactTool` | `scaffold_artifact.py` | JSON + Text | *Already Structured* | Scaffold summary. | Structured in #390. |
| `ScaffoldSchemaTool` | `scaffold_schema_tool.py` | JSON + Text | *Already Structured* | Schema output. | Structured in #390. |
| `TemplateValidationTool` | `template_validation_tool.py` | JSON + Text | `{"passed": bool, "issues": [{"severity": str, "message": str}]}` | Template validation details. | |
| `RunTestsTool` | `test_tools.py` | JSON + Text | `{"exit_code": int, "summary": dict}` | Tests summary. | Currently custom dual-result. |

### 3. JSON Schema Options & Architecture Principles
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
All MCP tools in `mcp_server/tools/` except `HealthCheckTool` and `RestartServerTool`.

### Selected strategy
Option B: Pydantic-defined schemas for tool outputs, with migration of all remaining tools to `StructuredTool`.

### Rationale
Provides explicit boundary validation, preventing drift and ensuring client compatibility without violating SRP/CQS.

### Constraints for later phases
- Do not instantiate outputs inside `execute_structured` directly if they bypass defined schema models.
- All unit tests must use the new index-agnostic assertion helper.
