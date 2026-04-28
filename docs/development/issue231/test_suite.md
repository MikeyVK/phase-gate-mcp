# Issue 231 — C_ENGINE_BREAK Test Suite Tracking

**Status:** ACTIVE  
**Branch:** feature/231-state-snapshot-cqrs  
**Design trace:** design.md v2.4 §3.3, §3.6, §3.9, §3.14, §3.15

---

## Test Files

| File | Scope | Coverage Target |
|---|---|---|
| `tests/mcp_server/unit/managers/test_state_repository.py` | C_READ_GUARD | `StateBranchMismatchError`, `BranchValidatedStateReader` |
| `tests/mcp_server/unit/managers/test_phase_state_engine.py` | C_ENGINE_BREAK | `get_state()` propagates `StateBranchMismatchError` |
| `tests/mcp_server/unit/tools/test_git_tools.py` | C_ENGINE_BREAK | `GitCommitTool` catches `StateBranchMismatchError` |
| `tests/mcp_server/unit/tools/test_git_checkout_state_sync.py` | C_ENGINE_BREAK | checkout sync handles `StateBranchMismatchError` |
| `tests/mcp_server/unit/tools/test_git_pull_tool_behavior.py` | C_ENGINE_BREAK | pull sync handles `StateBranchMismatchError` |
| `tests/mcp_server/unit/managers/test_workflow_status_resolver.py` | C_RESOLVER_CORE | `WorkflowStatusResolver` read-side behavior |

## Exit Criteria per Cycle

| Cycle | Criterion |
|---|---|
| C_READ_GUARD | Mismatched load raises `StateBranchMismatchError`; read paths locked ✅ |
| C_ENGINE_BREAK | Engine no longer translates mismatch to `FileNotFoundError` |
| C_RESOLVER_CORE | Resolver independently testable before consumer adoption |
| C_RESOLVER_ADOPTION | One shared resolver in `ProjectManager` and `GetWorkContextTool` |
| C_QA_STATE_SPLIT | QA baseline behind `IQualityStateRepository` |
| C_MUTATOR_CORE | Workflow writes behind one mutator seam |
| C_TOOL_CONFLICTS | Mutation failures surfaced through `ToolResult.error` |
| C_CLEANUP | No legacy shim, stale tests, or grep-visible remnants remain |
