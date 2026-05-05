<!-- docs\development\issue295\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-05T15:52Z updated= -->
# submit_pr Atomicity: Upstream Check, Dirty-Tree Guard, and Rollback on Failure

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-05

---

## Purpose

Research phase findings and expected result for issue #295. Provides the factual foundation for design and planning phases. Does not prescribe implementation details beyond what is needed to scope design choices.

## Scope

**In Scope:**
SubmitPRTool.execute() in mcp_server/tools/pr_tools.py; GitManager public API expansion; GitAdapter public API (read-only, identify gaps); existing test files test_submit_pr_atomic_flow.py and test_submit_pr_tool.py

**Out of Scope:**
initialize_project changes (belongs to issue #283/upstream); GitPushTool refactoring; enforcement.yaml changes; MergePRTool; any backward-compatibility shim — this is a clean break

## Prerequisites

Read these first:
1. Understanding of the GitManager/GitAdapter layering (§7 Law of Demeter: tools talk to managers, not adapters)
2. GitManager.pull() preflight pattern as the canonical model for pre-mutation safety checks
3. branch_local_artifacts config in contracts.yaml and MergeReadinessContext dataclass
4. commit_with_scope() behavior: calls git add . when files=None (stages all untracked+modified)
---

## Problem Statement

SubmitPRTool.execute() has three distinct atomicity failure modes that leave the branch in a degraded, non-recoverable state after a partial mutation:

**Failure A — No upstream configured:**
neutralize_to_base() + commit_with_scope() succeed, then push() raises ExecutionError('no upstream tracking branch'). The branch is now on local only, HEAD has the neutralization commit (state.json gone), and a second submit_pr call finds no artifacts to neutralize — branch is stranded.

**Failure B — Unexpected untracked files consumed silently:**
initialize_project writes state.json and deliverables.json to disk without committing them. has_net_diff_for_path checks committed git history only and returns False for untracked files — so neutralize_to_base is correctly skipped for those files. However, commit_with_scope calls `git add .` which blindly stages ALL untracked files. They land in the ready commit and propagate to main after merge. This is precisely how state.json ended up on main after PR #310.

**Failure C — GitHub API failure after successful push:**
After push() succeeds, create_pr() may fail (e.g., 422 PR already exists, 403 insufficient scope, 5xx GitHub outage). The branch is already on remote at HEAD with the neutralization commit. State.json is gone from HEAD. There is no rollback. A second submit_pr attempt finds no artifact to neutralize and tries to create a second PR, potentially duplicating.

## Research Goals

- Determine the correct preflight sequence for SubmitPRTool (what checks, in what order, before any mutation)
- Clarify responsibility boundary: submit_pr must NOT set upstream automatically — that belongs to initialize_project or the agent (SRP §1.1)
- Define dirty-tree guard semantics: what constitutes an acceptable working tree state at the entry of submit_pr
- Specify rollback mechanism for Failure C: post-push API failure must not leave the branch stranded
- Map the blast radius: which production files change and which test files need to be added or updated
- Verify compliance with ARCHITECTURE_PRINCIPLES.md §1.1 (SRP), §4 (Fail-Fast), §7 (Law of Demeter), §8 (Explicit over Implicit), §14 (Test via Public API)

---

## Background

## Existing Code Context

### GitAdapter public API (adapter layer)
- `is_clean() -> bool`: `not self.repo.is_dirty() and not self.repo.untracked_files` — returns True only if working tree has zero staged/unstaged/untracked changes
- `has_upstream() -> bool`: `self.repo.active_branch.tracking_branch() is not None`
- `neutralize_to_base(paths, base)`: `git restore --source=<merge_base_sha>` per path — silently does nothing for paths that never existed in merge-base (new untracked files)
- `has_net_diff_for_path(path, base)`: `git diff --name-only merge-base..HEAD` — checks committed history only, misses untracked
- `push(set_upstream=False)`: `origin.push()` — raises ExecutionError if no upstream tracking branch

### GitManager public API (manager layer)
- `push(set_upstream=False)` → delegates to adapter
- `pull(note_context, ...)` → preflight: is_clean + has_upstream + not detached HEAD → then pull
- `merge(branch_name, note_context)` → preflight: is_clean → then merge
- `has_net_diff_for_path(path, base)` → delegates to adapter
- `neutralize_to_base(paths, base)` → delegates to adapter
- `commit_with_scope(...)` → delegates to adapter.commit() which does git add . when files=None
- **MISSING**: `is_clean()` not exposed as public GitManager method
- **MISSING**: `has_upstream()` not exposed as public GitManager method

### SubmitPRTool.execute() current sequence (pr_tools.py ~L130)
1. get_current_branch()
2. For each branch_local_artifact: has_net_diff_for_path → collect paths_to_neutralize
3. neutralize_to_base(paths_to_neutralize) — may be skipped
4. commit_with_scope(...) ← git add . here, untracked files consumed
5. push() ← may fail if no upstream
6. create_pr(...) ← may fail after successful push
7. set_pr_status(OPEN)

### Law of Demeter constraint
The existing test `test_submit_pr_tool_execute_has_no_adapter_calls` (test_submit_pr_atomic_flow.py:218) asserts that SubmitPRTool.execute() must NOT contain `_git_manager.adapter`. Any new preflight methods (is_clean, has_upstream) must be exposed via GitManager, not accessed from SubmitPRTool directly on the adapter.

### GitManager.pull() as canonical preflight pattern
```python
def pull(self, note_context, ...):
    if not self.adapter.is_clean():
        note_context.produce(BlockerNote('Commit or stash changes before pulling'))
        raise PreflightError('Working directory is not clean')
    if not self.adapter.has_upstream():
        note_context.produce(BlockerNote('Set upstream tracking ...'))
        raise PreflightError('No upstream configured for current branch')
    return self.adapter.pull(...)
```
This is the exact pattern that SubmitPRTool must adopt, implemented via new GitManager public methods.

---

## Findings

## Finding 1: Preflight sequence must match GitManager.pull() pattern

GitManager already implements the canonical preflight pattern in pull() and merge(): check invariants → produce BlockerNote → raise PreflightError → return without mutating. SubmitPRTool must adopt the same pattern. The correct preflight sequence before any mutation:

1. **is_clean check**: `git_manager.is_clean()` — if False, produce `BlockerNote` listing dirty files, raise `PreflightError`. ANY uncommitted/untracked file that is not in the list of artifacts already being neutralized is a problem. But simpler and safer: require COMPLETELY clean tree before submit_pr starts. If state.json is untracked, the agent must commit it first. This makes the contract explicit and aligns with §8 Explicit over Implicit.
2. **has_upstream check**: `git_manager.has_upstream()` — if False, produce `BlockerNote('Run git_push with --set-upstream before submit_pr')`, raise `PreflightError`. submit_pr must NOT auto-push or auto-set upstream. Responsibility belongs to initialize_project or the agent explicitly.

Both checks require new public methods on GitManager. Current adapter-level methods cannot be called from SubmitPRTool (LoD constraint).

## Finding 2: Dirty-tree guard semantics

The dirty-tree check (is_clean) must run BEFORE neutralize_to_base, not after. Rationale: neutralize_to_base itself modifies files (it is a mutation). If the tree is dirty before neutralization, it means uncommitted work exists that was not authored by submit_pr. That work should be committed explicitly by the agent before invoking submit_pr.

The branch_local_artifacts exclusion for the dirty-tree check is NOT needed: the artifacts (state.json, deliverables.json) SHOULD be committed into the branch history. The neutralization removes them from the HEAD commit just before the PR. If they are untracked at submit_pr time, it means the agent ran initialize_project but forgot to commit — this must be caught and surfaced explicitly.

Conclusion: `is_clean()` must return True for the entire working tree. No exceptions, no exclusions. This is the simplest, most robust contract.

## Finding 3: Rollback mechanism for post-push API failure

After push() succeeds but create_pr() fails:
- The branch is on remote with the neutralization commit at HEAD
- state.json is in merge-base content (or absent) from the last commit  
- A retry of submit_pr will find no artifacts to neutralize (has_net_diff_for_path returns False) — broken state

Rollback strategy (single layer — Layer 2 only):

**Why Layer 1 (GitHub API pre-flight for duplicate PR check) is dropped:** The existing `check_pr_status` enforcement in `enforcement.yaml` already blocks `submit_pr` if an open PR exists on the current branch. Adding a redundant GitHub API round-trip would violate §9 YAGNI. The "does base exist?" check is also unnecessary — base is always `main` and always exists. Layer 2 rollback handles the edge case correctly.

**Layer 2 (post-push rollback):** If create_pr() raises ExecutionError after successful push:
  1. `git reset --soft HEAD~1` — undoes the neutralization commit; HEAD moves back one commit; staged index now holds the neutralization changes
  2. `git reset --hard HEAD` — discards staged index entirely and restores working tree to the new HEAD state (pre-neutralization). This is safe because `is_clean()` was True before execute() started, so no in-flight user changes exist.
  3. `git push --force-with-lease` — force-push to overwrite remote, reverting it to the pre-neutralization HEAD
  4. Produce `RecoveryNote` explaining: "PR creation failed: {reason}. Remote branch rolled back to pre-submit state. Working tree is clean. Retry submit_pr once the API issue is resolved."

The combined `soft HEAD~1` + `hard HEAD` is equivalent to `git reset --hard HEAD~1` but more explicit about the two concerns it addresses (commit history vs. working tree). The design phase may simplify to `hard HEAD~1` if preferred.

**Why NOT `git restore --staged <artifact_paths>`:** After soft-reset, the staged index contains artifact deletions/restorations. `git restore --staged` on specific paths would only unstage those paths to the HEAD state but leave the working tree in the merge-base artifact state (neutralize_to_base modified the working tree). `is_clean()` would return False post-rollback, causing Failure B on retry — the exact problem we are fixing.

The `--force-with-lease` is safe: we own the commit we just pushed (neutralization commit from this execute() call). No concurrent pushes can occur because BranchMutatingTool blocks concurrent branch mutations.

## Finding 4: API changes needed on GitManager and GitAdapter

New public methods required on GitManager (tools must not access adapter directly per §7 LoD):
- `is_clean() -> bool` (wraps adapter.is_clean())
- `has_upstream() -> bool` (wraps adapter.has_upstream())
- `rollback_neutralization(artifact_paths: frozenset[str]) -> None` (single method: soft-reset + hard-reset + force-push-with-lease; single manager method ensures the multi-step transaction is atomic from the caller's perspective — §1.1 SRP: manager owns the multi-step transaction, adapters own individual git operations)

New methods needed on GitAdapter:
- `soft_reset(steps: int = 1)` — `git reset --soft HEAD~N`
- `hard_reset_to_head()` — `git reset --hard HEAD` (restores working tree to current HEAD after soft-reset)
- `force_push_with_lease()` — `git push --force-with-lease`

Note: `is_clean()` and `has_upstream()` already exist on GitAdapter. No adapter changes needed for those.

## Finding 5: Error transparency requirements

All three failure paths must use the NoteContext pattern:
- Failure A (no upstream): `BlockerNote('No upstream tracking branch configured. Run git_push(set_upstream=True) before submit_pr.')` + `PreflightError`
- Failure B (dirty tree): `BlockerNote(f'Working tree is not clean. Uncommitted/untracked files prevent submit_pr. Commit all changes before submit_pr.')` + `PreflightError`
- Failure C rollback: `RecoveryNote('GitHub PR creation failed: {reason}. Remote branch has been rolled back to pre-submit state. Working tree is clean. Retry submit_pr once the API issue is resolved.')`

Note: Fix A and B are preflights (no mutation occurred) → use `BlockerNote + PreflightError`. Fix C is post-push recovery (mutation was undone) → use `RecoveryNote + ToolResult.error()`.

## Expected Result (Design Contract)

After all three fixes, the SubmitPRTool.execute() contract is:
1. **[PREFLIGHT]** assert working tree is clean → `BlockerNote` + `PreflightError` if not
2. **[PREFLIGHT]** assert upstream is configured → `BlockerNote` + `PreflightError` if not
3. [NEUTRALIZE] detect + neutralize branch-local artifacts (unchanged)
4. [COMMIT] commit_with_scope (unchanged)
5. [PUSH] push (unchanged)
6. **[CREATE PR]** create_pr → if fails: **[ROLLBACK]** `rollback_neutralization(artifact_paths)` on GitManager + `RecoveryNote` + `ToolResult.error()`
7. [STATUS] set_pr_status(OPEN) (unchanged)

Layer 1 GitHub pre-flight (duplicate PR check / base existence) is **dropped** per §9 YAGNI: `check_pr_status` enforcement already blocks submit_pr if an open PR exists; base is always `main`. Layer 2 rollback is sufficient.

## Blast Radius

### Production Code

| File | Change | Scope |
|------|--------|-------|
| `mcp_server/managers/git_manager.py` | Add `is_clean() -> bool` public method (wraps adapter.is_clean()) | ~5 lines |
| `mcp_server/managers/git_manager.py` | Add `has_upstream() -> bool` public method (wraps adapter.has_upstream()) | ~5 lines |
| `mcp_server/managers/git_manager.py` | Add `rollback_neutralization(artifact_paths: frozenset[str])` method: soft-reset + hard-reset-to-head + force-push-with-lease | ~20 lines |
| `mcp_server/adapters/git_adapter.py` | Add `soft_reset(steps: int = 1)` for `git reset --soft HEAD~N` | ~5 lines |
| `mcp_server/adapters/git_adapter.py` | Add `hard_reset_to_head()` for `git reset --hard HEAD` (restore working tree after soft-reset) | ~5 lines |
| `mcp_server/adapters/git_adapter.py` | Add `force_push_with_lease()` for `git push --force-with-lease` | ~5 lines |
| `mcp_server/tools/pr_tools.py` | `SubmitPRTool.execute()`: add 2 preflight guards at entry + rollback branch after create_pr failure | ~25 lines |

**Total production change estimate: ~65 lines across 3 files**

### Test Code

| File | Change |
|------|--------|
| `tests/mcp_server/integration/test_submit_pr_atomic_flow.py` | Add 3 test cases: Failure A (no upstream → BlockerNote + no mutation), Failure B (dirty tree → BlockerNote + no mutation), Failure C (API failure after push → rollback verified) |
| `tests/mcp_server/unit/managers/test_git_manager.py` | Add tests for new public methods: `is_clean()`, `has_upstream()`, rollback method |
| `tests/mcp_server/unit/adapters/test_git_adapter.py` | Add tests for `soft_reset()` and force-push-with-lease capability |
| `tests/mcp_server/unit/tools/test_submit_pr_tool.py` | Minor updates if structural assertions change |

**No changes needed to:** `enforcement.yaml`, `contracts.yaml`, `MergePRTool`, `GitCommitTool`, `test_ready_phase_enforcement.py`

## Open Questions

- ❓ Should `GitManager.rollback_neutralization()` be a single atomic method (recommended per §1.1 SRP) or split into `soft_reset()` + `force_push_with_lease()` separate manager methods? Recommendation: single method — prevents half-rollback state exposure to caller.
- ❓ What if `force_push_with_lease()` itself fails during rollback? This meta-failure is unaddressed. Design phase must specify failure semantics for the rollback method.
- ❓ Does `GitManager` implement a formal `Protocol` or `ABC` in `backend/core/interfaces/`? If so, `is_clean()` and `has_upstream()` must be added to the interface before writing TDD tests.
- ✅ `PreflightError` already exists in `mcp_server/core/exceptions.py` — no new exception type needed.


## Related Documentation
- **[mcp_server/tools/pr_tools.py — SubmitPRTool.execute() (current implementation)][related-1]**
- **[mcp_server/managers/git_manager.py — GitManager.pull() preflight pattern (lines 234-265)][related-2]**
- **[mcp_server/adapters/git_adapter.py — is_clean() line 70, has_upstream() line 299][related-3]**
- **[mcp_server/core/operation_notes.py — BlockerNote, RecoveryNote, PreflightError][related-4]**
- **[tests/mcp_server/integration/test_submit_pr_atomic_flow.py — existing integration tests][related-5]**
- **[tests/mcp_server/unit/tools/test_submit_pr_tool.py — existing unit tests][related-6]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md — §1.1 SRP, §4 Fail-Fast, §7 LoD, §8 Explicit, §14 Public API only][related-7]**

<!-- Link definitions -->

[related-1]: mcp_server/tools/pr_tools.py — SubmitPRTool.execute() (current implementation)
[related-2]: mcp_server/managers/git_manager.py — GitManager.pull() preflight pattern (lines 234-265)
[related-3]: mcp_server/adapters/git_adapter.py — is_clean() line 70, has_upstream() line 299
[related-4]: mcp_server/core/operation_notes.py — BlockerNote, RecoveryNote, PreflightError
[related-5]: tests/mcp_server/integration/test_submit_pr_atomic_flow.py — existing integration tests
[related-6]: tests/mcp_server/unit/tools/test_submit_pr_tool.py — existing unit tests
[related-7]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md — §1.1 SRP, §4 Fail-Fast, §7 LoD, §8 Explicit, §14 Public API only

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |