# Validation Report — Issue #353

**Branch:** `bug/353-create-branch-remove-auto-checkout`  
**Date:** 2026-05-25  
**Validator:** @imp validator  
**Verdict:** CONDITIONAL PASS — branch-changed surface clean; 2 pre-existing full-suite failures unrelated to this issue

---

## Scope and Prerequisites

**Bug fixed:** `GitAdapter.create_branch()` implicitly called `new_branch.checkout()` after
creating a branch, causing a silent side-effect (auto-checkout) that violated SRP and
made `create_branch` non-composable.

**Approved Strategy:** Clean break — remove `checkout()` unconditionally; no optional flag,
no backward-compat shim, no bridge.

**Cycle completed:** C1 "Remove auto-checkout" (single cycle; no further cycles planned).

**Prerequisites verified:**
- Research artifact present: `docs/development/issue353/research.md`
- Planning artifact present: `docs/development/issue353/planning.md` v1.1
- Design phase force-skipped with human approval (no architectural decisions pending)
- Phase state: `implementation` completed → forced to `validation` (state.json commit gap
  caused by transient branch-switch detour to `hotfix/355`; RED+GREEN+REFACTOR commits
  confirm cycle completion)

---

## Summary Verdict

| Check | Result |
|---|---|
| Branch quality gates (4 changed files) | ✅ 6/6 PASS |
| Changed-surface tests (89 tests) | ✅ 89/89 PASS |
| Full suite | ⚠️ 2830/2832 — 2 pre-existing failures unrelated to #353 |
| C1 deliverables satisfied | ✅ C1.D1–C1.D4 all confirmed |
| Approved Strategy constraints preserved | ✅ No flag, no shim, no bridge |
| Architecture alignment | ✅ SRP violation removed |

**Overall:** CONDITIONAL PASS. The 2 full-suite failures are pre-existing
(`_ConcurrentTestGateRunner` interface gap from issue #293, tracked separately as hotfix #355).
They fail identically on unmodified `main` (confirmed via `git stash` + run during
implementation session).

---

## Full-Suite Test Result

```
2830 passed, 2 failed, 11 skipped, 6 xfailed
```

**Failing tests (pre-existing, unrelated to #353):**

| Test | Root cause |
|---|---|
| `TestPrimaryMixedConcurrentWritesC4::test_force_transition_and_force_cycle_transition_concurrent` | `_ConcurrentTestGateRunner` missing `inspect_phase_exit()` (issue #293 gap) |
| `TestSecondaryHomogeneousConcurrentWritesC4::test_two_concurrent_force_transitions_both_records_present` | same |

Both fail on `main` without any #353 changes (verified: `git stash` → run → 2 failed →
`git stash pop`). Tracked as hotfix issue #355.

---

## Branch Quality Gate Result

Scope: 4 files changed on this branch vs `main`.

| Gate | Result |
|---|---|
| Gate 0: Ruff Format | ✅ PASS |
| Gate 1: Ruff Strict Lint | ✅ PASS |
| Gate 2: Imports | ✅ PASS |
| Gate 3: Line Length | ✅ PASS |
| Gate 4: Types (DTOs) | ⏭ SKIPPED (DTOs-only scope, not applicable) |
| Gate 4b: Pyright | ✅ PASS |
| Gate 4c: mypy mcp_server | ✅ PASS |

---

## Deliverable Mapping

| Deliverable | Description | Evidence |
|---|---|---|
| C1.D1 | `new_branch.checkout()` absent from `GitAdapter.create_branch()` | `git_adapter.py` line 119: `self.repo.create_head(branch_name, base_ref)` — no `.checkout()` call; `new_branch` variable also removed (F841 fix) |
| C1.D2 | Tool return text `"✅ Created branch: {name}"` (no "switched") | `git_tools.py` line 167: `return ToolResult.text(f"✅ Created branch: {branch_name}")` |
| C1.D3 | Adapter log `"Created branch"` | `git_adapter.py` logger.info call: `"Created branch"` |
| C1.D4 | 4 tests updated: `checkout.assert_not_called()` + corrected return text | `test_git_adapter.py` lines 551, 567, 584; `test_git_tools.py` line 80 |

**Exit criteria satisfied:**
- `new_branch.checkout()` absent ✅
- Return text `"Created branch"` ✅
- 4 tests green ✅
- Full suite green on #353 surface ✅
- Quality gates PASS ✅

---

## Corrected Behavior and Regression Alignment

**Before fix:** Calling `create_branch("feature/x", base="main")` would:
1. Create the branch `feature/x` pointing at `main`
2. Silently check out `feature/x` as the active branch (undeclared side-effect)

**After fix:** Calling `create_branch("feature/x", base="main")` will:
1. Create the branch `feature/x` pointing at `main`
2. Leave the active branch unchanged

**Regression obligations verified:**

- `test_create_branch_with_head` — creates from HEAD, no checkout ✅
- `test_create_branch_with_branch_name` — creates from branch name, no checkout ✅
- `test_create_branch_with_commit_hash` — creates from commit hash, no checkout ✅
- `test_create_branch_tool_calls_manager_with_explicit_base` — tool returns `"Created branch"` ✅
- `test_create_branch_requires_explicit_base` — base still required ✅
- `test_create_branch_already_exists_raises_error` — duplicate guard intact ✅
- `test_create_branch_with_branch_name_as_base` — full branch name path unaffected ✅

---

## Approved Strategy Alignment

| Constraint | Status |
|---|---|
| No optional `checkout: bool` flag added | ✅ Confirmed — no new parameters |
| No backward-compat shim | ✅ Confirmed — no shim function or wrapper |
| No bridge or cutover | ✅ Confirmed — single clean removal |
| `.github/prompts/start-issue.prompt.md` left unchanged | ✅ Confirmed — file not in branch diff |

---

## Live Demonstration Proposal

The old failure **cannot be safely reproduced live** on this branch because the fix is
already applied. A live recreation would require temporarily reverting the fix in a
throwaway environment.

**Closest observable fallback:**

1. Read `git show HEAD:mcp_server/adapters/git_adapter.py` vs
   `git show ecd55c0a:mcp_server/adapters/git_adapter.py` — the diff shows
   `new_branch.checkout()` present before, absent after.

2. Run the 4 regression tests:
   ```
   pytest tests/mcp_server/unit/adapters/test_git_adapter.py::TestGitAdapterCreateBranch \
          tests/mcp_server/unit/tools/test_git_tools.py::test_create_branch_tool_calls_manager_with_explicit_base \
          -v
   ```
   Expected: 7/7 PASS. These tests assert `checkout.assert_not_called()` and
   `"Created branch"` in return text — they would fail against the old code.

3. Inspect `git_adapter.py` directly:
   [mcp_server/adapters/git_adapter.py](../../../mcp_server/adapters/git_adapter.py) —
   `create_branch()` body contains only `self.repo.create_head(branch_name, base_ref)`
   with no subsequent `.checkout()` call.

---

## Residual Risks and Caveats

| Risk | Severity | Notes |
|---|---|---|
| Pre-existing full-suite failures (#355) | Low | Not caused by #353; tracked separately as hotfix; fix: add 4 methods to `_ConcurrentTestGateRunner` |
| Phase state.json commit gap | Informational | State was force-transitioned to validation with human approval; no implementation evidence lost |
| Consumers that depended on implicit checkout | Low | Research confirmed no external callers relied on the checkout side-effect; `start-issue.prompt.md` step 3 (`git_checkout`) was already the intended explicit checkout |
