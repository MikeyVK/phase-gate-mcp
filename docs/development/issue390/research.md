<!-- docs/development/issue390/research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-10T18:42Z updated= -->
# Research — Issue #390: Improve validation logic of save/update deliverables tools

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-10

---

## Purpose

This document details the research findings for Issue #390, which addresses the lack of deep declarative validation for the `save_planning_deliverables` and `update_planning_deliverables` tools, as well as the hardcoded requirements for TDD cycles in non-cycle-based workflows. It also incorporates a conscious scope expansion to refactor four other tools to return structured JSON payloads instead of flat text blocks.

## Problem Statement

The `save_planning_deliverables` and `update_planning_deliverables` tools accept malformed inputs (such as raw strings or incorrect deep structures) due to the use of a generic `dict[str, Any]` type at the tool boundary. When these malformed inputs are processed by `ProjectManager` or during merge logic, they raise unhandled Python exceptions (e.g., `TypeError: string indices must be integers` or `AttributeError`). Furthermore, `ProjectManager` strictly requires `tdd_cycles` for all projects, even for non-cycle-based workflows (e.g., `docs`), which forces operators to provide dummy structures.

## Scope

### In Scope
* **Declarative Pydantic validation**: Define a deep Pydantic validation schema for `planning_deliverables` at the tool boundary.
* **Dynamic cycle-based workflow validation**: Inspect the active workflow configuration via the injected `ContractsConfig` to determine whether `tdd_cycles` are required, eliminating hardcoding for non-cycle-based workflows.
* **Refactoring text-json tools**: Refactor `get_project_plan`, `get_issue`, `get_pr`, and `initialize_project` to return structured JSON payloads using `ToolResult.json_data()`.
* **Clean Break migration**: Migrate all tests that verify old text-based deliverables or JSON outputs to the new dictionary-based deliverables and structured JSON format.

### Out of Scope
* **Global `structuredContent` refactoring**: Resolving the server-level double-serialization issue (which belongs to the deferred Issue #301 work).

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

### Finding 3: Scope Expansion — Truncated Text Responses
The following tools return JSON data serialized as a single string inside `ToolResult.text()`:
* `get_project_plan`
* `get_issue`
* `get_pr`
* `initialize_project`

Because these outputs are often large, the client chat UI (VS Code) truncates them and saves them to a file (like `output.txt`). This forces agents to make extra tool calls to inspect the file. Returning structured JSON data using `ToolResult.json_data()` allows the client to receive the fields directly without truncation.

### Finding 4: Double Serialization and `structuredContent` (Issue #301)
As investigated in the deferred Issue #301:
* `ToolResult.json_data()` creates two content blocks: `{"type": "json"}` and `{"type": "text"}` (which is a JSON string fallback).
* The MCP server's `_convert_tool_result_to_content()` converts the `type="json"` block into a second `TextContent` block, sending the same JSON data twice.
* The planned resolution is to pop the `type="json"` block at the server layer and populate the `structuredContent` field of `CallToolResult`.
* Because implementing this globally is a larger refactoring affecting many tools and tests, we will adopt a **Clean Break** strategy: we refactor the four tools to return `ToolResult.json_data()`, acknowledging the double serialization as a known transport-level behavior that will be resolved once Issue #301 is implemented.

### Finding 5: Config Injection Architecture Pattern
Adhering to `ARCHITECTURE_PRINCIPLES.md` §12:
* Classes must never load configuration files directly from the filesystem inside methods.
* All configuration must be loaded at the composition root and injected via constructor injection.
* `ProjectManager` already receives `ContractsConfig` via constructor injection, which will be used to check if the workflow requires TDD cycles.

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
* **Clean Break**: We do not maintain backward compatibility for legacy string deliverables format, nor do we provide text-based fallbacks for the JSON-returning tools. We migrate all tests to use the new dictionary-based deliverables and structured JSON outputs.
* **Double Serialization**: We accept the double serialization of JSON payloads under the current server transport as an expected side-effect that will be definitively fixed when Issue #301 is implemented.

---

## Open Questions

None.

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-10 | Agent | Initial findings drafted |
