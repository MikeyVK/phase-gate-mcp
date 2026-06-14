<!-- c:\temp\pgmcp\docs\development\issue402\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-12T19:45Z updated=2026-06-14T17:30Z -->
# Planning — Issue #402: Expose JSON data in MCP tools

**Status:** APPROVED  
**Version:** 2.0  
**Last Updated:** 2026-06-14

---

## Purpose

Slice the implementation of the `ITool` refactoring and MCP JSON data exposure (Issue #402) into safe, sequential TDD cycles.

## Scope

**In Scope:**
- Implementation of the `ITool` interface, `ToolExecutionEnvelope`, and `ToolFactory`.
- The `ResourcePublishingDecorator` for caching.
- Server pipeline refactoring (Controller/Presenter pattern).
- Migration of all 51 tools to the new architecture.

**Out of Scope:**
- Unregistered or legacy tools.

## Prerequisites

Read these first:
1. Approved Research Document
2. Approved Design Document
3. `dto_contracts.md` (SSOT for all DTO schemas and templates)

---

## Summary

The planning follows the Approved Strategy: we will first build the core architectural pipeline (ITool, Decorator, Factory, MVP Server) and migrate a pilot tool. Subsequently, we will migrate all remaining tool batches to the new architecture, concluding with a massive cleanup of the legacy base classes.

---

## Dependencies

- Cycle 1 (Core Pipeline) is the hard dependency for all subsequent migration cycles.
- Migration cycles (2-5) can technically be parallelized but will be executed sequentially to maintain branch stability.

---

## TDD Cycles

### Cycle 1: Core Architecture Pipeline (`ITool` & Factory)

**Goal:** Implement the `ITool` interface, `ToolExecutionEnvelope`, `ToolFactory`, `ResourcePublishingDecorator`, and the MVP server pipeline, replacing the `structuredContent` logic.

**Deliverables:**
- **[D1.1]** Define `ITool` protocol and `ToolExecutionEnvelope` in `mcp_server/tools/base.py`.
- **[D1.2]** Implement `ResourcePublishingDecorator` in `mcp_server/tools/decorators.py` to cache DTOs using `ResponseCacheManager`.
- **[D1.3]** Implement `ToolFactory` in `mcp_server/bootstrap.py` to assemble tools and decorators.
- **[D1.4]** Refactor `MCPServer.handle_call_tool()` to use the MVP pipeline: execute tool -> extract DTO and `run_id` from envelope -> format with `TextPresenter` -> return pure `TextContent`.
- **[D1.5]** Remove `structuredContent` injection and `QUICKFIX` markdown JSON duplication from `mcp_converters.py`.
- **[D1.6]** Ensure all pure domain DTOs enforce `frozen=True` for immutability.
- **[D1.7]** Update test helpers (e.g., `assert_structured_tool_result`) to assert against the new `TextContent` and envelope structures.

**Tests:**
- `tests/mcp_server/unit/test_server.py`
- `tests/mcp_server/unit/tools/test_base.py`

**Success/Exit Criteria:**
The server successfully routes a tool call through the factory-assembled decorated pipeline, caches the DTO, and returns pure text to the client.

### Cycle 2: Batch 1 (Admin, Health & Cycle Tools)

**Goal:** Migrate Cycle transition, Health, and Admin tools to `ITool`.

**Deliverables:**
- **[D2.1]** Migrate `HealthCheckTool` and `RestartServerTool`.
- **[D2.2]** Migrate `TransitionCycleTool` and `ForceCycleTransitionTool`.
- **[D2.3]** Enforce `frozen=True` on all newly defined Batch 1 DTOs.

**Tests:**
- `tests/mcp_server/unit/tools/test_health_tools.py`
- `tests/mcp_server/unit/tools/test_cycle_tools.py`

**Success/Exit Criteria:**
All Batch 1 tools return frozen DTOs via `ITool.execute()`, with green tests.

### Cycle 3: Batch 2 (Discovery & Project Tools)

**Goal:** Migrate Discovery, Search, and Project management tools to `ITool`.

**Deliverables:**
- **[D3.1]** Migrate Discovery & Search tools (`GetWorkContextTool`, `SearchDocumentationTool`).
- **[D3.2]** Migrate Project tools (`InitializeProjectTool`, `GetProjectPlanTool`, `SavePlanningDeliverablesTool`, `UpdatePlanningDeliverablesTool`).
- **[D3.3]** Enforce `frozen=True` on all Batch 2 DTOs.

**Tests:**
- `tests/mcp_server/unit/tools/test_discovery_tools.py`
- `tests/mcp_server/unit/tools/test_project_tools.py`

**Success/Exit Criteria:**
All Batch 2 tools return frozen DTOs via `ITool.execute()`, with green tests.

### Cycle 4: Batch 3a (Git Analysis & Info Tools)

**Goal:** Migrate Git analysis tools.

**Deliverables:**
- **[D4.1]** Migrate Git list, diff, parent, merge check, and status tools.
- **[D4.2]** Enforce `frozen=True` on Batch 3a DTOs.

**Tests:**
- `tests/mcp_server/unit/tools/test_git_tools.py`

**Success/Exit Criteria:**
Git analysis tools successfully migrated and return frozen DTOs, verified by tests.

### Cycle 5: Batch 3b (Git Mutation & Action Tools)

**Goal:** Migrate Git mutation tools.

**Deliverables:**
- **[D5.1]** Migrate Git branch creation, commit, restore, checkout, push, merge, delete, stash, fetch, and pull tools.
- **[D5.2]** Enforce `frozen=True` on Batch 3b DTOs.

**Tests:**
- `tests/mcp_server/unit/tools/test_git_tools.py`

**Success/Exit Criteria:**
Git mutation tools successfully migrated and return frozen DTOs.

### Cycle 6: Batch 4a (GitHub Issues & PRs)

**Goal:** Migrate GitHub Issue and PR tools.

**Deliverables:**
- **[D6.1]** Move GitHub read models to `github_models.py`.
- **[D6.2]** Migrate Issue and PR tools.
- **[D6.3]** Enforce `frozen=True` on Issue/PR DTOs.

**Tests:**
- `tests/mcp_server/unit/tools/test_issue_tools.py`
- `tests/mcp_server/unit/tools/test_pr_tools.py`

**Success/Exit Criteria:**
GitHub Issue & PR tools successfully migrated and return flattened frozen DTO presentation fields.

### Cycle 7: Batch 4b (GitHub Labels & Milestones)

**Goal:** Migrate GitHub Label and Milestone tools.

**Deliverables:**
- **[D7.1]** Migrate Label tools.
- **[D7.2]** Migrate Milestone tools.
- **[D7.3]** Enforce `frozen=True` on Label/Milestone DTOs.

**Tests:**
- `tests/mcp_server/unit/tools/test_label_tools.py`
- `tests/mcp_server/unit/tools/test_milestone_tools.py`

**Success/Exit Criteria:**
Label & Milestone tools successfully migrated and return frozen DTOs.

### Cycle 8: Auto-Fix Tool & MCP Resource Pilot

**Goal:** Implement the new `AutoFixTool`, the `ResponseCacheManager` and `CachedResponseResource` provider as the resource pilot.

**Deliverables:**
- **[D8.1]** Implement `AutoFixTool` and its DTOs with `frozen=True`.
- **[D8.2]** Implement `ResponseCacheManager` with FIFO eviction (OrderedDict).
- **[D8.3]** Implement `CachedResponseResource` (matching `pgmcp://cache/runs/.*`), register it in `bootstrap.py`.
- **[D8.4]** Add declarative presentation template for `auto_fix` referencing the uniform resource URI.

**Tests:**
- `tests/mcp_server/unit/tools/test_quality_tools.py`

**Success/Exit Criteria:**
AutoFixTool modifies files correctly; cache evicts oldest runs correctly; and the model successfully retrieves the run's JSON data using `read_resource`.

### Cycle 9: Batch 5 (Phase, Scaffold, Quality & Testing Tools)

**Goal:** Migrate the remaining complex tools involving gates, validation, and file editing.

**Deliverables:**
- **[D9.1]** Migrate Phase transition tools.
- **[D9.2]** Migrate Scaffold artifact and schema tools.
- **[D9.3]** Migrate Quality gates, Pytest, Safe edit, and Template validation tools.
- **[D9.4]** Enforce `frozen=True` on all Batch 5 DTOs. Ensure verbose/diff outputs are isolated to JSON.

**Tests:**
- `tests/mcp_server/unit/tools/test_phase_tools.py`
- `tests/mcp_server/unit/tools/test_quality_tools.py`
- `tests/mcp_server/unit/tools/test_test_tools.py`
- `tests/mcp_server/unit/tools/test_safe_edit_tool.py`

**Success/Exit Criteria:**
Batch 5 tools migrated; JSON separation implemented correctly.

### Cycle 10: Validation, Quality Gates & Cleanup

**Goal:** Finalize the migration by removing legacy structures and ensuring codebase integrity.

**Deliverables:**
- **[D10.1]** Delete legacy `StructuredTool` and unused `BaseTool` execution paths from `mcp_server/tools/base.py`.
- **[D10.2]** Clean up any unused legacy converter functions in `mcp_converters.py`.
- **[D10.3]** Green full test suite run.
- **[D10.4]** Clean quality gates check (Ruff, MyPy).

**Tests:**
- Run full test suite: `pytest`
- Run quality gates: `ruff check` and `mypy`

**Success/Exit Criteria:**
Legacy classes completely removed. All tests pass, and quality gates pass with zero violations.