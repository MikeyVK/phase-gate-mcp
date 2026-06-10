<!-- docs/development/issue390/research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-10T18:42Z updated=2026-06-10T19:18Z -->
# Research — Issue #390: Improve validation logic of save/update deliverables tools

**Status:** DRAFT  
**Version:** 1.1  
**Last Updated:** 2026-06-10

---

## Purpose

This document details the research findings for Issue #390, which addresses the lack of deep declarative validation for the `save_planning_deliverables` and `update_planning_deliverables` tools, as well as the hardcoded requirements for TDD cycles in non-cycle-based workflows. It also incorporates a conscious scope expansion to refactor other tools returning JSON to use structured JSON payloads, and integrates the server-level `structuredContent` mapping from Issue #301 to resolve double serialization.

## Problem Statement

The `save_planning_deliverables` and `update_planning_deliverables` tools accept malformed inputs (such as raw strings or incorrect deep structures) due to the use of a generic `dict[str, Any]` type at the tool boundary. When these malformed inputs are processed by `ProjectManager` or during merge logic, they raise unhandled Python exceptions (e.g., `TypeError: string indices must be integers` or `AttributeError`). Furthermore, `ProjectManager` strictly requires `tdd_cycles` for all projects, even for non-cycle-based workflows (e.g., `docs`), which forces operators to provide dummy structures.

## Scope

### In Scope
* **Declarative Pydantic validation**: Define a deep Pydantic validation schema for `planning_deliverables` at the tool boundary.
* **Dynamic cycle-based workflow validation**: Inspect the active workflow configuration via the injected `ContractsConfig` to determine whether `tdd_cycles` are required, eliminating hardcoding for non-cycle-based workflows.
* **Refactoring text-json tools**: Refactor `get_project_plan`, `get_issue`, `get_pr`, and `initialize_project` to return structured JSON payloads using `ToolResult.json_data()`.
* **Server-level `structuredContent` mapping**: Implement the server-level extraction of `type="json"` blocks to populate the MCP `structuredContent` field (from Issue #301).
* **Clean Break migration**: Migrate all tests that verify old text-based deliverables or JSON outputs to the new dictionary-based deliverables and structured JSON format.

### Out of Scope
* None (the previously deferred Issue #301 scope is now consolidated into this issue).

---

## Findings

### Finding 1: Observed Failure Behavior
The deliverables tools accept any `dict` at the boundary without verifying deep fields:
* `tdd_cycles.cycles` is assumed to be a list of dicts. If it is passed as a string or contains string values, `ProjectManager` crashes with `TypeError: string indices must be integers, not 'str'`.
* Similarly, `validates` specs are only validated at runtime during tool execution, and malformed structures can slip through or crash.
* Returning raw traceback errors to the client lacks transparency and makes debug cycles fragile.

### Finding 2: Hardcoded TDD Cycles in Workflows
`ProjectManager.save_planning_deliverables` currently asserts:
```python
if "tdd_cycles" not in planning_deliverables:
    raise ValueError("planning_deliverables must contain 'tdd_cycles' key")
```
This fails for non-cycle-based workflows (such as `docs`) which have no `implementation` phase with `cycle_based: true` in `contracts.yaml`. 

### Finding 3: Complete Tool Inventory
Out of 50 registered tools in `bootstrap.py`, only **7 tools** produce structured JSON payloads. These are:
1. `GetIssueTool` (returns JSON dump of issue)
2. `GetPRTool` (returns JSON dump of PR)
3. `InitializeProjectTool` (returns JSON success details)
4. `GetProjectPlanTool` (returns JSON phase plan)
5. `RunTestsTool` (returns structured test stats and failures)
6. `RunQualityGatesTool` (returns structured gate violations)
7. `ScaffoldSchemaTool` (returns JSON Schema of artifact contexts)

All other 43 tools return simple text messages (`ToolResult.text()`), meaning our migration is fully bounded and no other tools are affected.

### Finding 4: Double Serialization and `structuredContent` (Issue #301)
As investigated in the deferred Issue #301:
* `ToolResult.json_data()` creates two content blocks: `{"type": "json"}` and `{"type": "text"}` (which is a JSON string fallback).
* The MCP server's `_convert_tool_result_to_content()` converts the `type="json"` block into a second `TextContent` block, sending the same JSON data twice.
* The clean resolution is to pop the `type="json"` block at the server layer and populate the `structuredContent` field of `CallToolResult`. This natively prevents double serialization and stops VS Code from saving large text outputs into `output.txt`.

### Finding 5: Config Injection Architecture Pattern
Adhering to `ARCHITECTURE_PRINCIPLES.md` §12:
* Classes must never load configuration files directly from the filesystem inside methods.
* All configuration must be loaded at the composition root and injected via constructor injection.
* `ProjectManager` already receives `ContractsConfig` via constructor injection, which will be used to check if the workflow requires TDD cycles.

---

## Regression Risks & Mitigation

### Risk: Step-by-step Signature Breakage
If we modify the signature of `ToolResult.json_data` to require a `text` parameter immediately:
* Existing tools like `ScaffoldSchemaTool` and several unit tests will fail compilation or crash during execution because they do not supply the `text` parameter.
* The server would crash mid-refactoring, preventing step-by-step TDD verification.

### Mitigation: Backward Compatible Signature
To mitigate this risk:
* We will keep the `text` parameter optional in `ToolResult.json_data` signature initially (`text: str | None = None`).
* If `text` is omitted, the method falls back to serializing the JSON payload as the text summary, preserving backward compatibility.
* Once all tools and tests have been migrated, we can make the `text` parameter strictly required.

---

## Blast Radius

### Production Code
* [project_tools.py](file:///c:/temp/pgmcp/mcp_server/tools/project_tools.py):
  - Update `SavePlanningDeliverablesInput` and `UpdatePlanningDeliverablesInput` to use the new `PlanningDeliverablesModel` and `UpdatePlanningDeliverablesModel`.
  - Refactor `GetProjectPlanTool` and `InitializeProjectTool` to return `ToolResult.json_data()`.
* [issue_tools.py](file:///c:/temp/pgmcp/mcp_server/tools/issue_tools.py):
  - Refactor `GetIssueTool` to return `ToolResult.json_data()`.
* [pr_tools.py](file:///c:/temp/pgmcp/mcp_server/tools/pr_tools.py):
  - Refactor `GetPRTool` to return `ToolResult.json_data()`.
* [project_manager.py](file:///c:/temp/pgmcp/mcp_server/managers/project_manager.py):
  - Update `save_planning_deliverables` and `update_planning_deliverables` signature and validation.
  - Determine `cycle_based` requirement dynamically from the injected `ContractsConfig`.
* [server.py](file:///c:/temp/pgmcp/mcp_server/server.py):
  - Update `_convert_tool_result_to_mcp_result` to extract `type="json"` blocks and populate the `structuredContent` field.

### Test Code
* [test_project_tools.py](file:///c:/temp/pgmcp/tests/mcp_server/unit/tools/test_project_tools.py): Update assertions verifying `get_project_plan` and `initialize_project` to check `content[0]["json"]` instead of `content[0]["text"]`, and update deliverables tool tests to align with the new Pydantic schema validation.
* [test_issue_tools.py](file:///c:/temp/pgmcp/tests/mcp_server/unit/tools/test_issue_tools.py): Update assertions verifying `get_issue` to check `content[0]["json"]` instead of `content[0]["text"]`.
* [test_pr_tools.py](file:///c:/temp/pgmcp/tests/mcp_server/unit/tools/test_pr_tools.py): Update assertions verifying `get_pr` to check `content[0]["json"]` instead of `content[0]["text"]`.
* [test_project_manager.py](file:///c:/temp/pgmcp/tests/mcp_server/unit/managers/test_project_manager.py): Update unit tests verifying deliverables validation in `ProjectManager`.
* [test_workflow_cycle_e2e.py](file:///c:/temp/pgmcp/tests/mcp_server/integration/test_workflow_cycle_e2e.py): Align integration tests with JSON outputs and deliverables validation.

---

## Approved Strategy

### Boundary / consumer scope
`planning_deliverables` format validation and JSON tool output formats.

### Selected strategy
* **Clean Break + Issue #301 Consolidation**: We consolidate Issue #301 into this issue. We will refactor the server to natively support `structuredContent` and prevent double serialization.
* **Migration Strategy**: We use a backward-compatible signature for `ToolResult.json_data` to ensure step-by-step TDD migration is safe and does not break the server mid-run. All tools will eventually be migrated to use `StructuredTool` and return structured JSON and summaries.

---

## Open Questions

None.

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-10 | Agent | Initial findings drafted |
| 1.1 | 2026-06-10 | Agent | Consolidated Issue #301 structuredContent, tool inventory, and migration risks |
