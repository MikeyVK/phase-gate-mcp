<!-- docs\development\issue357\design.md -->
<!-- template=design version=5827e841 created=2026-05-28T13:44Z updated= -->
# Fix agent lifecycle: @co-owns-init contract, IBranchParentReader, bootstrap predicate, end-issue safety

**Status:** DRAFT  
**Version:** 1.1  
**Last Updated:** 2026-05-28

---

## Purpose

Define the fix direction and interface contracts for the five lifecycle coordination defects in issue #357, so planning can decompose into TDD cycles without ambiguity about boundaries, responsibilities, or affected test surfaces.

## Scope

**In Scope:**
Prompt files (start-issue, end-issue), agent instruction files (imp.agent.md), SubmitPRTool base resolution, check_context_loaded bootstrap predicate in EnforcementRunner, and the `check_merge` MCP tool — the new read-only tool that implements the reachability gate referenced in `end-issue` step 6 (F9).

**Out of Scope:**
Epic workflow redesign, new merge orchestration, automated end-issue execution, changes to issues #268/#345/#354 contracts, get_work_context bootstrap degradation behavior beyond the F6 predicate fix.

## Prerequisites

Read these first:
1. docs/development/issue357/research.md — defect framing, Approved Strategy, corrected behavior
2. docs/coding_standards/ARCHITECTURE_PRINCIPLES.md — binding contract
3. docs/coding_standards/DOCUMENTATION_STANDARD.md
---

## 1. Context & Requirements

### 1.1. Problem Statement

Five lifecycle coordination surfaces contain defects that interact: (1) start-issue.prompt.md encodes two competing ownership models (F2); (2) imp.agent.md startup protocol has no precondition that the branch is pre-initialized by @co (F3); (3) SubmitPRTool.execute() falls back directly to git_config.default_base_branch without reading state.json.parent_branch (F4); (4) end-issue.prompt.md deletes the child branch immediately after checkout without verifying the parent has received the merged content (F5); (5) _handle_check_context_loaded bootstrap predicate only checks state.json absence, not whether the stored issue_number matches the current branch (F6); (6) end-issue.prompt.md step 6 calls check_merge(merge_sha=MERGE_SHA) as the reachability gate before branch deletion, but no such tool exists in the MCP server (F9). F6 is the enabler: without it the @co-always-initializes model cannot function on epic-child branches.

### 1.2. Requirements

**Functional:**
- [ ] F2 — start-issue.prompt.md expresses the @co-owns-init model without ambiguity; the non-epic section explicitly states the branch is pre-initialized and @imp starts on an already-initialized branch
- [ ] F3 — imp.agent.md startup protocol states the @co-must-initialize precondition before step 1; an uninitialized branch reaching @imp is a process violation, not a recoverable startup scenario
- [ ] F4 — SubmitPRTool resolves the PR base via IBranchParentReader.get_parent_branch() before falling back to default_base_branch; caller-supplied params.base still takes priority
- [ ] F5 — end-issue.prompt.md inserts git_pull and merge-SHA reachability verification between git_checkout(base_branch) and git_delete_branch
- [ ] F6 — _handle_check_context_loaded bootstrap predicate bypasses the gate when state.json is absent OR when the stored issue_number does not match the current branch's issue number
- [ ] F9 — `CheckMergeTool` (read-only, `BaseTool`) added to `mcp_server/tools/git_tools.py`; `GitAdapter.is_ancestor(sha: str) -> bool` and `GitManager.is_ancestor(sha: str) -> bool` added; tool registered in `server.py`; `end-issue` step 6 `check_merge(merge_sha=MERGE_SHA)` call is fulfilled

**Non-Functional:**
- [ ] IBranchParentReader is a narrow Protocol (one method) in core/interfaces/ — not IStateReader, not PhaseStateEngine (ISP §1.4/§6, DIP §1.5/§11, CQS §5)
- [ ] Constructor injection for all new dependencies; no direct instantiation inside execute() (DIP §1.5/§11)
- [ ] GitConfig injected into EnforcementRunner via constructor following the StateReconstructor pattern (DIP, DRY §2, §10 Cohesion)
- [ ] No backward-compatibility shims; test helpers updated to new signatures
- [ ] IBranchParentReader is a required constructor parameter in SubmitPRTool (not optional with None default)
- [ ] CheckMergeTool inherits BaseTool (not BranchMutatingTool); enforcement_event = None; no new Protocol interface needed

### 1.3. Constraints

- Approved Strategy: no `@imp`-side recovery path for uninitialized branches
- Bootstrap predicate extended (`absent OR mismatch`), not replaced
- Prior contracts from issues `#268`, `#345`, `#354` preserved
- No broad lifecycle redesign
- Reuse `GitConfig.extract_issue_number()` exclusively — no duplicate branch parser

---

## 2. Design Options

### 2.1. F4 — IBranchParentReader: narrow Protocol (chosen)

New `IBranchParentReader(Protocol)` in `mcp_server/core/interfaces/` with a single method `get_parent_branch(branch: str) -> str | None`. Implement `BranchStateParentReader` in `mcp_server/managers/` backed by `IStateReader`. Identity validation: if `state.issue_number` does not match `GitConfig.extract_issue_number(branch)`, return `None`. Inject into `SubmitPRTool` as a required 5th constructor parameter. Base resolution chain in `execute()`: `params.base → reader.get_parent_branch(branch) → git_config.default_base_branch`.

**Pros:**
- ✅ ISP compliant — one method, read-only, no write exposure (ISP §1.4/§6)
- ✅ DIP compliant — `SubmitPRTool` depends on an abstraction, not on `FileStateRepository` (DIP §1.5/§11)
- ✅ CQS compliant — pure query, no state mutation (CQS §5)
- ✅ Law of Demeter satisfied — tool does not navigate state internals to get one field
- ✅ Required param forces explicit wiring at composition root and in tests — no silent `None` path
- ✅ Identity validation prevents cross-issue parent leakage

**Cons:**
- ❌ New interface + new implementation class adds a small surface
- ❌ Composition root (`server.py`) and test helpers must be updated (acceptable: no compat shims needed)

### 2.2. F4 — Direct IStateReader injection into SubmitPRTool (rejected)

Inject the existing `IStateReader` directly into `SubmitPRTool` and read `BranchState.parent_branch` from it.

**Pros:**
- ✅ No new interface required
- ✅ `IStateReader` already exists in `core/interfaces/`

**Cons:**
- ❌ ISP violation — `SubmitPRTool` is a read-only consumer of one field; `IStateReader` exposes the full state load contract
- ❌ Law of Demeter violation — tool navigates `BranchState` internals to extract one field
- ❌ Couples `SubmitPRTool` to the full state schema; any `BranchState` field change affects this consumer unnecessarily
- ❌ Makes it harder to fake in tests — full `BranchState` object needed instead of a one-method fake

### 2.3. F6 — GitConfig constructor injection into EnforcementRunner (chosen)

Add `git_config: GitConfig` as a required constructor parameter to `EnforcementRunner`. In `_handle_check_context_loaded`, after the `.exists()` check, read `issue_number` from `state.json` directly (JSON load, single field), call `git_config.extract_issue_number(branch)`, and return early if they differ. Follows the `StateReconstructor` pattern exactly. Branch name is resolved using the same `context.get_param('current_branch') or _get_current_git_branch(workspace_root)` call already present in the handler — move resolution before the predicate.

**Pros:**
- ✅ Follows the established `StateReconstructor` injection pattern — no new pattern introduced (§10 Cohesion, DRY §2)
- ✅ `extract_issue_number()` is the single authoritative parser — no duplication
- ✅ Predicate remains inline; no new reader interface required for a bootstrap check
- ✅ Direct `state.json` read is consistent with the existing `.exists()` predicate style

**Cons:**
- ❌ `EnforcementRunner` constructor gains a new required param — composition root and test setup updated
- ❌ Branch name resolution must move before the predicate (minor reorder in the method)

### 2.4. F9 — Thin read-only CheckMergeTool in git_tools.py (chosen)

New `CheckMergeInput(merge_sha: str)` and `CheckMergeTool(BaseTool)` placed in `mcp_server/tools/git_tools.py`.
`GitAdapter.is_ancestor(sha: str) -> bool` calls `self.repo.git.merge_base("--is-ancestor", sha, "HEAD")`.
GitPython raises `GitCommandError` on any non-zero exit. The method catches `GitCommandError` and checks
`exc.status == 1` to return `False` (not ancestor, expected case). Status ≥2 raises `ExecutionError`.
`GitManager.is_ancestor(sha: str) -> bool` delegates to `self._adapter.is_ancestor(sha)`.
`CheckMergeTool.execute()` calls `self._manager.is_ancestor(params.merge_sha)` and returns
`ToolResult.text` (reachable) or `ToolResult.error` (not reachable). Registered in `server.py` as
`CheckMergeTool(manager=self.git_manager)`.

**Pros:**
- ✅ No new Protocol needed — `GitManager` is already the correct abstraction boundary (YAGNI §9)
- ✅ Inherits `BaseTool`; `enforcement_event = None`; no enforcement registration required
- ✅ `GitAdapter.is_ancestor` introduces a new `GitCommandError` import and selective status check: `status == 1` returns `False` (not ancestor, expected case); status ≥2 raises `ExecutionError`. This pattern does NOT currently exist in `git_adapter.py` — all existing error handling uses `except Exception as e:` — and must be added explicitly in implementation.
- ✅ `anyio.to_thread.run_sync` not needed for a fast boolean read; direct synchronous call is acceptable
- ✅ Placement in `git_tools.py` avoids new file for a thin tool (YAGNI §9)
- ✅ Constructor injection: `CheckMergeTool(manager: GitManager)` — single dependency

**Cons:**
- ❌ `CheckMergeTool` tests live alongside other git tool tests in `test_git_tools.py` — acceptable, same pattern

### 2.5. F9 — New git_adapter_reader interface + dedicated CheckMergeManager (rejected)

Extract `IGitAncestorReader` Protocol for `is_ancestor`, implement a dedicated `GitAncestorManager`.

**Cons:**
- ❌ YAGNI violation — one thin boolean method does not justify a new Protocol + manager pair
- ❌ `GitManager` already wraps `GitAdapter`; a second manager wrapping the same adapter creates DRY/SSOT violation

### 2.6. F6 — IStateReader injection for issue_number lookup (rejected)

Inject `IStateReader` into `EnforcementRunner` and use it to load `BranchState` in the bootstrap predicate.

**Pros:**
- ✅ Cleaner abstraction — no direct file read in enforcement handler

**Cons:**
- ❌ Creates a circular concern: checking if state is trustworthy before trusting it, yet using the state subsystem to do so
- ❌ `IStateReader.load(branch)` expects the correct branch; in bootstrap context the inherited state is filed under the child branch path but belongs to the parent issue
- ❌ Heavier than necessary for a single-integer bootstrap check
- ❌ Not the established pattern — `StateReconstructor` reads `state.json` directly for bootstrap inference

---

## 3. Chosen Design

**Decision:** Six targeted fixes, each at the narrowest surface: (A) New `IBranchParentReader` Protocol in `core/interfaces/` + `BranchStateParentReader` implementation in `managers/` injected as required param into `SubmitPRTool`. (B) `GitConfig` injected into `EnforcementRunner`; bootstrap predicate extended with issue-number mismatch check reading `state.json` directly. (C) `end-issue.prompt.md`: `git_pull` after `git_checkout(base_branch)`, then `check_merge(merge_sha=MERGE_SHA)` as the reachability gate before `git_delete_branch`. (D) `start-issue.prompt.md` non-epic section: explicit statement that branch is pre-initialized and `@imp` starts on an already-initialized branch. (E) `imp.agent.md`: explicit `@co`-must-initialize precondition paragraph before startup step 1. (F) New `CheckMergeTool` + `GitAdapter.is_ancestor` + `GitManager.is_ancestor` + `server.py` registration.

**Rationale:** Each fix targets the narrowest surface that satisfies the corrected behavior without broadening scope. `IBranchParentReader` follows ISP (one method, read-only) and DIP (abstract Protocol) and avoids Law of Demeter violations. `GitConfig` injection into `EnforcementRunner` follows the `StateReconstructor` pattern already established in the codebase. Prompt-only fixes (C, D, E) have no code blast radius. No backward-compatibility shims; test helpers are updated to reflect the actual interface contracts.

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| `IBranchParentReader` is a required (not optional) `SubmitPRTool` constructor param | Optional-with-`None` default would introduce a `None`-guard in `execute()`. Required param forces explicit composition at the server root and in tests — the correct DIP pattern. |
| `BranchStateParentReader` uses identity validation before returning `parent_branch` | Returning `parent_branch` from a state belonging to a different issue would silently misdirect PRs. If `state.issue_number` ≠ `GitConfig.extract_issue_number(branch)`, return `None` and let the fallback chain continue. |
| Base resolution chain: `params.base → reader.get_parent_branch() → default_base_branch` | `params.base` preserves caller override. `reader.get_parent_branch()` consults branch-local state. `default_base_branch` is the repo-wide last resort. |
| `GitConfig` injected into `EnforcementRunner` via constructor; `state.json` read directly in predicate | Follows the `StateReconstructor` pattern. Avoids circular dependency on `IStateReader` in a context where state trust is the thing being established. |
| Bootstrap predicate extended: both `absent` and issue-number `mismatch` bypass the gate | The `absent` case must be preserved — stateless branches still bootstrap freely. The `mismatch` case is the new bypass. Predicate is extended, not replaced, per the research Approved Strategy. |
| `end-issue`: `git_pull` after checkout, then `check_merge(merge_sha=MERGE_SHA)` reachability gate, then delete | `check_merge` is the authoritative tool gate per F9 decision; it wraps `git merge-base --is-ancestor` so `@co` never executes raw git commands. After `git_pull` on the base branch, the SHA being reachable confirms the merged content is locally present before destructive cleanup. |
| `CheckMergeTool` inherits `BaseTool`, not `BranchMutatingTool`; `enforcement_event = None` | Read-only operation; must not trigger enforcement events; `BaseTool` is the correct base. |
| `GitAdapter.is_ancestor` distinguishes `GitCommandError.status == 1` from status ≥2 | Exit 1 from `merge-base --is-ancestor` means "not an ancestor" — expected, return `False`. Exit ≥2 is a real git error — raise `ExecutionError`. Conflating them would make all unreachable SHAs appear as git errors. |
| No new `IGitAncestorReader` Protocol | One thin boolean method on an already-injected `GitManager` does not justify a new Protocol + manager pair (YAGNI §9). |
| `imp.agent.md` precondition is a paragraph before step 1, not a numbered startup step | A precondition is a prerequisite that must be true before the protocol runs — not a runtime action. Placing it as a step would imply `@imp` should check or fix it, which contradicts the `@co`-owns-init model. |
| No backward-compatibility shims; test helpers and call sites updated to new signatures | No compat needed. Clean interface contracts in tests reflect actual production wiring and prevent false confidence from tests covering stale behavior. |
| `default_base_branch` standalone param retired from `EnforcementRunner` when `git_config` is injected | `self.default_base_branch` is stored but never read by any `EnforcementRunner` method — dead code in the class body. `server.py` currently passes `git_config.default_base_branch` as a plain string — DRY duplication. Once `GitConfig` is injected, the standalone param is removed; any internal use reads `self._git_config.default_base_branch` directly. |

---

## 4. Affected Interfaces And Call Sites

| Surface | Change | Files |
|---|---|---|
| `IBranchParentReader` | New `Protocol` in `core/interfaces/__init__.py` | `mcp_server/core/interfaces/__init__.py` |
| `BranchStateParentReader` | New implementation class | `mcp_server/managers/branch_parent_reader.py` (new) |
| `SubmitPRTool.__init__` | New required 5th param: `branch_parent_reader: IBranchParentReader` | `mcp_server/tools/pr_tools.py` |
| `SubmitPRTool` composition root | Wire `BranchStateParentReader` | `mcp_server/server.py` |
| `EnforcementRunner.__init__` | Add required param `git_config: GitConfig`; retire `default_base_branch` standalone param (stored but never read — dead code) | `mcp_server/managers/enforcement_runner.py` |
| `EnforcementRunner._handle_check_context_loaded` | Extend bootstrap predicate with mismatch bypass | `mcp_server/managers/enforcement_runner.py` |
| `start-issue.prompt.md` | Non-epic section: clarify `@co`-owns-init; `@imp` starts on pre-initialized branch | `.github/prompts/start-issue.prompt.md` |
| `end-issue.prompt.md` | Insert `git_pull` + SHA verification before branch delete | `.github/prompts/end-issue.prompt.md` |
| `imp.agent.md` | Add `@co`-must-initialize precondition paragraph before startup step 1 | `.github/agents/imp.agent.md` |
| `GitAdapter.is_ancestor` | New method: `is_ancestor(sha: str) -> bool` | `mcp_server/adapters/git_adapter.py` |
| `GitManager.is_ancestor` | New delegating method: `is_ancestor(sha: str) -> bool` | `mcp_server/managers/git_manager.py` |
| `CheckMergeInput` + `CheckMergeTool` | New input model + read-only tool | `mcp_server/tools/git_tools.py` |
| `CheckMergeTool` composition root | Register `CheckMergeTool(manager=self.git_manager)` | `mcp_server/server.py` |

---

## 5. Test Blast Radius

| Test file | Impact | Action required |
|---|---|---|
| `tests/mcp_server/integration/test_submit_pr_atomic_flow.py` | `_make_submit_pr_tool` helper: new required param | Update helper; wire a test fake for `IBranchParentReader` |
| `tests/mcp_server/unit/tools/test_submit_pr_tool.py` | `_make_tool_for_lod` helper: new required param | Update helper same way |
| `tests/mcp_server/integration/test_context_loaded_enforcement.py` | Missing test for issue-number mismatch scenario | Add new test; `test_gate_inactive_on_bootstrap_no_state_json` must still pass |
| Any file constructing `EnforcementRunner(...)` directly | `git_config` required param added; `default_base_branch` param removed | Update all `EnforcementRunner` call sites in tests (add `git_config` fake; drop `default_base_branch` kwarg where present) |
| Prompt / agent doc files (F2, F3, F5) | Not pytest-covered | Human review; treat as first-class deliverables per research F8 |
| `tests/mcp_server/unit/tools/test_git_tools.py` | New tests needed for `CheckMergeTool` | Add: reachable case, not-reachable case, git-error case (status ≥2) |

---

## 6. Design-Level Validation Strategy

| Requirement | How to prove |
|---|---|
| F4: `IBranchParentReader` called before `default_base_branch` | Integration test: reader returns a non-default parent; PR opened against that parent |
| F4: Identity validation on mismatch | Unit test: `BranchStateParentReader` returns `None` when `state.issue_number` ≠ branch issue number |
| F4: `params.base` override still takes priority | Existing tests supplying `params.base` must continue to pass |
| F6: Gate inactive when `state.json` absent | Existing `test_gate_inactive_on_bootstrap_no_state_json` must still pass |
| F6: Gate inactive when issue-number mismatch | New test: `state.json` present with `issue_number=1`, branch is `feature/2-other`; `initialize_project` must not be blocked |
| F6: Gate active when issue-number matches | Existing `test_gate_blocks_tool_when_context_not_loaded` must still pass |
| F2, F3, F5: Prompt and doc correctness | Human review of updated files against corrected behavior framing in research.md |
| F9: `CheckMergeTool` returns reachable for a reachable SHA | Unit test: mock `GitManager.is_ancestor` returns `True`; assert `ToolResult` is not error and text contains "reachable" |
| F9: `CheckMergeTool` returns error for unreachable SHA | Unit test: mock returns `False`; assert `ToolResult.is_error` is `True` |
| F9: `GitAdapter.is_ancestor` exit 1 returns False, not exception | Unit test: mock `repo.git.merge_base` raises `GitCommandError(status=1)`; assert method returns `False` |
| F9: `GitAdapter.is_ancestor` exit ≥2 raises `ExecutionError` | Unit test: mock raises `GitCommandError(status=2)`; assert `ExecutionError` is raised |

---

## 7. Open Questions

| # | Question | Direction |
|---|---|---|
| 1 | Does `EnforcementRunner` already receive `GitConfig` at its composition root in `server.py`, or is a new wiring step needed? | **RESOLVED** — `EnforcementRunner.__init__` has no `git_config` param today; `server.py` passes only `git_config.default_base_branch` as a string. New wiring needed: add `git_config=git_config` to `EnforcementRunner(...)` in `server.py` and retire the `default_base_branch` kwarg there. |
| 2 | Should `BranchStateParentReader` live in `mcp_server/managers/` or alongside `SubmitPRTool` in `mcp_server/tools/`? | **RESOLVED** — `mcp_server/managers/` confirmed. Consistent with `IStateReader` → `FileStateRepository` pattern; all interface implementations live in `managers/`. |

## Related Documentation
- **[Research — issue #357](docs/development/issue357/research.md)**
- **[Architecture Principles](docs/coding_standards/ARCHITECTURE_PRINCIPLES.md)**
- **[Issue #268 — lifecycle boundary model](docs/development/issue268/research.md)**
- **[Issue #354 — end-issue get_pr() fix](docs/development/issue354/validation.md)**

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-28 | Agent | Initial draft — five fix surfaces, IBranchParentReader, GitConfig injection, prompt/doc fixes |
| 1.1 | 2026-05-28 | Agent | Address QA aandachtspunten: OQ1+OQ2 resolved, `default_base_branch` retirement decision added |
| 1.2 | 2026-05-29 | Agent | Add F9: CheckMergeTool design — options 2.4/2.5, decision update, affected interfaces, test blast radius, validation strategy |
