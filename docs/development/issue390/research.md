<!-- docs/development/issue390/research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-10T18:42Z updated=2026-06-10T19:24Z -->
# Research — Issue #390: Improve validation logic of save/update deliverables tools

**Status:** DRAFT  
**Version:** 1.2  
**Last Updated:** 2026-06-10

---

## Purpose

This document details the research findings for Issue #390, which addresses the lack of deep declarative validation for the `save_planning_deliverables` and `update_planning_deliverables` tools, as well as the hardcoded requirements for TDD cycles in non-cycle-based workflows. It also incorporates a conscious scope expansion to refactor other tools returning JSON to use structured JSON payloads, and integrates the server-level `structuredContent` mapping from Issue #301 to resolve double serialization.

## Problem Statement

The `save_planning_deliverables` and `update_planning_deliverables` tools accept malformed inputs (such as raw strings or incorrect deep structures) due to the use of a generic `dict[str, Any]` type at the tool boundary. When these malformed inputs are processed by `ProjectManager` or during merge logic, they raise unhandled Python exceptions (e.g., `TypeError: string indices must be integers` or `AttributeError`). Furthermore, `ProjectManager` strictly requires `tdd_cycles` for all projects, even for non-cycle-based workflows (e.g., `docs`), which forces operators to provide dummy structures.

## Scope

### In Scope
* Analysis of declarative validation options for `planning_deliverables` structures.
* Analysis of workflow configuration check mechanisms to conditionally enforce TDD cycle planning.
* Analysis of JSON-returning tools and truncation behaviors in the client chat UI.
* Analysis of double-serialization behaviors and the MCP `structuredContent` response field.
* Identification of the complete blast radius in code and test suites.

### Out of Scope
* Design of the concrete Pydantic schemas or base classes.
* Planning of cycles, tasks, or execution steps.

---

## Findings

### Finding 1: Observed Failure Behavior
The deliverables tools accept any `dict` at the boundary without verifying deep fields:
* If `tdd_cycles.cycles` is passed as a string or contains string values, `ProjectManager` crashes with `TypeError: string indices must be integers, not 'str'`.
* Similarly, `validates` specs are only validated at runtime during tool execution, and malformed structures can slip through or crash.
* Returning raw traceback errors to the client lacks transparency and makes debug cycles fragile.

### Finding 2: Hardcoded TDD Cycles in Workflows
`ProjectManager.save_planning_deliverables` currently asserts that the `tdd_cycles` key must be present in the deliverables dictionary. This fails for non-cycle-based workflows (such as `docs`) which have no `implementation` phase with `cycle_based: true` in `contracts.yaml`.

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
* `ProjectManager` already receives `ContractsConfig` via constructor injection, which can be used to check if the workflow requires TDD cycles.

---

## Strategy Options & Policy Analysis

### Topic 1: Deliverables Validation Strategy
* **Option 1: Complete Pydantic deep validation at tool boundary (BLOCK policy)**. 
  * *Pros*: Fail-fast, clean schema discovery, elegant error translation.
  * *Cons*: Requires writing and maintaining Pydantic models for deliverables.
* **Option 2: Preserve unstructured dict[str, Any] and add custom dictionary key checks inside tools**.
  * *Pros*: Simple, no new models.
  * *Cons*: Bypasses declarative JSON schema discovery, error formatting is ad-hoc, prone to missed edge cases.
* **Recommendation**: Option 1. It provides a first-time-right declarative contract for agents and catches all malformed inputs at the boundary.

### Topic 2: Workflow Cycle Validation
* **Option 1: Keep hardcoded tdd_cycles check in ProjectManager**.
  * *Pros*: Zero code change in validation logic.
  * *Cons*: Breaks documentation-only changes or non-cycle-based workflows.
* **Option 2: Read contracts.yaml dynamically to check if workflow is cycle-based**.
  * *Pros*: Correctly models workflow requirements.
  * *Cons*: Slightly more complex check in `ProjectManager`.
* **Recommendation**: Option 2. It adheres to Config-First principles.

### Topic 3: Structured Content Transport
* **Option 1: Consolidate Issue #301 structuredContent implementation now**.
  * *Pros*: Resolves double serialization and truncation globally for all tools, cleaner architecture.
  * *Cons*: Slightly larger upfront design effort, breaks some test assertions that need updating.
* **Option 2: Keep Issue #301 deferred and stick to ToolResult.json_data() with double-serialization fallback**.
  * *Pros*: Smaller scope for #390.
  * *Cons*: Continues to produce duplicate JSON blocks in response, does not fully resolve the user's truncation issue for the migrated tools.
* **Recommendation**: Option 1. It provides a complete, clean end-to-end fix for JSON tool outputs.

---

## Approved Strategy

### Boundary 1: Deliverables Validation Schema
* **Boundary**: Deliverables JSON file format and tool validation inputs.
* **Selected Strategy**: Clean Break.
* **Rationale**: Storing unstructured strings in `deliverables.json` was a legacy workaround. Enforcing a strict schema prevents runtime crashes. All tests will be migrated to the new dictionary-based deliverables format.
* **Constraints**: Validation must check workflow configuration to only enforce `tdd_cycles` if the workflow contains cycle-based phases.

### Boundary 2: Tool Output Serialization and Transport
* **Boundary**: Server-level MCP result serialization and tool JSON responses.
* **Selected Strategy**: Clean Break.
* **Rationale**: Eliminates truncation to `output.txt` and double-serialization cleanly at the server transport layer by extracting JSON and populating `structuredContent`. All affected tests will be updated to verify the new format.
* **Constraints**: Maintain backward compatibility of `ToolResult.json_data` signature during the migration to allow step-by-step TDD cycle verification.

---

## Open Questions

None.

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-10 | Agent | Initial findings drafted |
| 1.1 | 2026-06-10 | Agent | Consolidated Issue #301 structuredContent, tool inventory, and migration risks |
| 1.2 | 2026-06-10 | Agent | Cleaned up design/planning content, added Strategy Options analysis, and formatted Approved Strategy per boundary |
