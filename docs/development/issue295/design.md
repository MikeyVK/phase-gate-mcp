<!-- docs\development\issue295\design.md -->
<!-- template=design version=5827e841 created=2026-05-05T16:33Z updated= -->
# submit_pr Atomicity: Upstream Check, Dirty-Tree Guard, and Rollback on Failure

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-05

---

## Purpose

Design phase specification for implementing issue #295 fixes. Provides the complete API contract for all new methods so the planning phase can decompose into TDD cycles without ambiguity.

## Scope

**In Scope:**
mcp_server/tools/pr_tools.py (SubmitPRTool.execute), mcp_server/managers/git_manager.py (3 new public methods), mcp_server/adapters/git_adapter.py (3 new primitives), tests/mcp_server/integration/test_submit_pr_atomic_flow.py, tests/mcp_server/unit/managers/test_git_manager.py, tests/mcp_server/unit/adapters/test_git_adapter.py

**Out of Scope:**
initialize_project changes, enforcement.yaml changes, MergePRTool, GitCommitTool, GitPushTool refactoring, IGitManager Protocol (confirmed non-existent — no interface update needed)

## Prerequisites

Read these first:
1. Research doc: docs/development/issue295/research.md (FINAL)
2. ARCHITECTURE_PRINCIPLES.md §1.1 SRP, §4 Fail-Fast, §7 LoD, §8 Explicit, §9 YAGNI
3. GitManager.pull() as canonical preflight reference (git_manager.py lines 234-265)
---

## 1. Context & Requirements

### 1.1. Problem Statement

SubmitPRTool.execute() has three (or four) atomicity failure modes that leave the branch in a non-recoverable state after a partial mutation. Research (FINAL) identified A: no upstream preflight, B: dirty-tree untracked files silently consumed, C: GitHub API failure after push with no rollback, and D (newly raised by QA): push fails for non-upstream reasons after the neutralization commit is made.

### 1.2. Requirements

**Functional:**
- [ ] FR-1: submit_pr MUST verify the working tree is completely clean (is_clean() == True) before any mutation. Any dirty state MUST produce a BlockerNote with the reason and raise PreflightError.
- [ ] FR-2: submit_pr MUST verify upstream tracking is configured (has_upstream() == True) before any mutation. Missing upstream MUST produce a BlockerNote instructing the agent to run git_push(set_upstream=True) first.
- [ ] FR-3: submit_pr MUST NOT set upstream tracking automatically (SRP §1.1 — that responsibility belongs to initialize_project / git_push tool).
- [ ] FR-4: After a successful push but failed create_pr(), submit_pr MUST roll back the remote to the pre-neutralization state: git reset --hard HEAD~1 locally + git push --force-with-lease.
- [ ] FR-5: Failure D (push fails for non-upstream reason after neutralization commit): submit_pr MUST roll back the local neutralization commit: git reset --hard HEAD~1 (local only, no force-push needed — nothing reached remote).
- [ ] FR-6: All failure paths MUST surface context to the caller via NoteContext: BlockerNote for preflights (no mutation), RecoveryNote for post-mutation rollback. RecoveryNote MUST state the post-rollback working tree state and explicit retry instruction.
- [ ] FR-7: SubmitPRTool.execute() MUST NOT access GitAdapter directly (_git_manager.adapter). All new preflight and rollback operations MUST be exposed as public GitManager methods (Law of Demeter §7).

**Non-Functional:**
- [ ] NFR-1: No backward-compatibility shim. This is a clean break. Existing tests that rely on the old 3-step flow (neutralize → commit → push) must be updated.
- [ ] NFR-2: All new GitManager public methods must be testable in isolation via mock injection (§14 Test via Public API).
- [ ] NFR-3: No extra GitHub API round-trips per submit_pr invocation. Layer 1 pre-flight dropped per §9 YAGNI — Layer 2 rollback is sufficient.
- [ ] NFR-4: rollback_neutralization() must leave the working tree clean (is_clean() == True) after execution so a retry of submit_pr passes the new FR-1 preflight.
- [ ] NFR-5: All adapter primitives (soft_reset, hard_reset, force_push_with_lease) must be individually testable.

### 1.3. Constraints

- **§7 Law of Demeter**: `SubmitPRTool.execute()` source must not contain `_git_manager.adapter` — enforced by existing structural test `test_submit_pr_tool_execute_has_no_adapter_calls`
- **§4 Fail-Fast**: both preflights must execute before `neutralize_to_base()` is called — no mutation before all invariants verified
- **§9 YAGNI**: no Layer 1 GitHub pre-flight (duplicate PR check already handled by `check_pr_status` enforcement in `enforcement.yaml`)
- **`PreflightError`** already exists in `mcp_server/core/exceptions.py:112` — no new exception type needed
- **No `IGitManager` Protocol/ABC** exists in codebase — confirmed by QA. No interface layer update needed.
---

## 2. Design Options

Only one viable option exists given the constraints. The option space was collapsed during research.

**Considered but rejected: Expose adapter methods directly from SubmitPRTool**
SubmitPRTool calling `self._git_manager.adapter.is_clean()` would violate §7 LoD and break the existing `test_submit_pr_tool_execute_has_no_adapter_calls` structural test. Rejected.

**Considered but rejected: Two-step rollback (soft_reset + hard_reset_to_head)**
Research initially proposed `git reset --soft HEAD~1` + `git reset --hard HEAD`. QA correctly noted this is identical to `git reset --hard HEAD~1`. The two-step form adds conceptual complexity without benefit. Rejected in favor of a single `git reset --hard HEAD~1`.

**Considered but rejected: Separate rollback methods for Failure C vs Failure D**
Failure C needs local + remote rollback (hard reset + force-push). Failure D needs only local rollback (hard reset, no push since nothing reached remote). A single `rollback_neutralization(remote: bool)` flag handles both cleanly. Separate methods would duplicate the hard-reset logic. Rejected.

---

## 3. Chosen Design

**Decision:** Extend GitManager with three new public methods (is_clean, has_upstream, rollback_neutralization) and GitAdapter with three new primitives (soft_reset, hard_reset_to_head, force_push_with_lease). SubmitPRTool.execute() gains two preflights at entry and two rollback branches: one for push failure (local rollback only) and one for create_pr failure (local + remote rollback). Failure D (push fails for non-upstream reason) is handled by the same rollback_neutralization() method with a local-only flag.

**Rationale:** GitManager.pull() already uses the exact preflight pattern (is_clean → has_upstream → mutate) — the design mirrors it. A single rollback_neutralization() method on GitManager keeps the multi-step rollback transaction encapsulated at the manager layer (§1.1 SRP). SubmitPRTool only calls one method; it does not orchestrate individual adapter primitives. Using git reset --hard HEAD~1 (single command) instead of soft+hard two-step eliminates ambiguity and aligns with QA recommendation. Force-push-with-lease is safe because BranchMutatingTool prevents concurrent branch mutations.

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| `is_clean()` and `has_upstream()` as **separate** GitManager public methods | Each check maps to a distinct FR (FR-1, FR-2). Combining them would violate CQS and make test isolation harder. |
| `rollback_neutralization(remote: bool = False)` with a single `remote` flag | One method, two behaviors. Failure C: `remote=True` → hard reset + force-push. Failure D: `remote=False` → hard reset only. Avoids duplication, keeps §1.1 SRP: manager owns the transaction boundary. |
| `git reset --hard HEAD~1` (single command) instead of soft + hard two-step | Functionally identical, less conceptual overhead. QA-validated. |
| `force_push_with_lease()` as **separate** adapter method (not extending existing `push()`) | Adding a `force_with_lease: bool` param to `push()` would create a boolean flag anti-pattern. A dedicated method has an unambiguous contract. |
| Rollback on **Failure C** uses `force_push_with_lease` (safe) | `BranchMutatingTool` prevents concurrent mutations. The commit we're overwriting is the one we just pushed in this very `execute()` call — lease will never fail due to concurrent writes. |
| Rollback on **Failure D** does **not** force-push | Nothing reached remote. Only local state needs correction. Force-pushing would be unnecessary and potentially harmful. |
| `rollback_neutralization()` failure semantics: **raise ExecutionError, produce RecoveryNote** | If the rollback itself fails (e.g., `force_push_with_lease` rejected), the system cannot self-heal. The tool must surface a `RecoveryNote` with manual recovery steps and propagate the error — never swallow it. Manual recovery: `git reset --hard HEAD~1` + `git push --force-with-lease`. |

---

## 4. API Contract

### 4.1. GitAdapter — New Methods

```python
def soft_reset(self, steps: int = 1) -> None:
    """Run `git reset --soft HEAD~{steps}`.
    
    Moves HEAD back by `steps` commits, keeps changes in index (staged).
    Raises ExecutionError on git failure.
    """

def hard_reset_to_head(self) -> None:
    """Run `git reset --hard HEAD`.
    
    Discards all staged and unstaged changes, restores working tree to HEAD.
    Raises ExecutionError on git failure.
    """

def hard_reset(self, ref: str = "HEAD~1") -> None:
    """Run `git reset --hard {ref}`.
    
    Moves HEAD to ref, discards all staged and unstaged changes.
    Primary use: rollback_neutralization.
    Raises ExecutionError on git failure.
    """

def force_push_with_lease(self, remote: str = "origin") -> None:
    """Run `git push --force-with-lease {remote}`.
    
    Fails if remote has commits this branch does not know about.
    Raises ExecutionError on rejection.
    """
```

> **Note:** `soft_reset` and `hard_reset_to_head` are kept as separate primitives for individual testability (NFR-5). However, `rollback_neutralization()` on GitManager internally uses `hard_reset(ref="HEAD~1")` directly — combining both steps in a single git command.

### 4.2. GitManager — New Public Methods

```python
def is_clean(self) -> bool:
    """Return True if the working tree has no staged, unstaged, or untracked changes.
    
    Query method (§5 CQS — no side effects).
    Delegates to adapter.is_clean().
    """

def has_upstream(self) -> bool:
    """Return True if the current branch has a remote tracking branch configured.
    
    Query method (§5 CQS — no side effects).
    Delegates to adapter.has_upstream().
    """

def rollback_neutralization(
    self,
    note_context: NoteContext,
    *,
    remote: bool,
) -> None:
    """Roll back the most recent neutralization commit.
    
    Resets HEAD~1 hard (discards neutralization commit and restores working tree).
    If remote=True, also force-pushes to overwrite the remote ref.
    
    Produces RecoveryNote explaining the post-rollback state and retry steps.
    Raises ExecutionError if rollback fails (including force-push failure).
    
    Called by SubmitPRTool:
    - Failure C (create_pr failed after push): remote=True
    - Failure D (push failed for non-upstream reason): remote=False
    """
```

### 4.3. SubmitPRTool.execute() — New Control Flow

```python
async def execute(self, params: SubmitPRInput, context: NoteContext) -> ToolResult:
    branch = self._git_manager.get_current_branch()
    base = params.base or self._git_manager.git_config.default_base_branch

    # === PREFLIGHT (no mutation before this point) ===
    
    # FR-1: dirty-tree guard
    if not self._git_manager.is_clean():
        context.produce(BlockerNote(
            message="Working tree is not clean. Commit all changes before submit_pr."
        ))
        raise PreflightError("Working directory is not clean")
    
    # FR-2: upstream guard
    if not self._git_manager.has_upstream():
        context.produce(BlockerNote(
            message=(
                "No upstream tracking branch configured. "
                "Run git_push(set_upstream=True) before submit_pr."
            )
        ))
        raise PreflightError("No upstream configured for current branch")

    # === NEUTRALIZE (safe: preflight passed, tree was clean) ===
    paths_to_neutralize = frozenset(
        artifact.path
        for artifact in self._merge_readiness_context.branch_local_artifacts
        if self._git_manager.has_net_diff_for_path(artifact.path, base)
    )
    if paths_to_neutralize:
        self._git_manager.neutralize_to_base(paths_to_neutralize, base)

    # === COMMIT ===
    try:
        self._git_manager.commit_with_scope(...)
    except ExecutionError as exc:
        # Commit failed: neutralize_to_base mutated the working tree.
        # Hard-reset restores working tree to pre-neutralization HEAD.
        self._git_manager.rollback_neutralization(context, remote=False)
        return ToolResult.error(str(exc))

    # === PUSH (Failure D: push fails for non-upstream reasons) ===
    try:
        self._git_manager.push()
    except ExecutionError as exc:
        # Nothing reached remote. Roll back local commit only.
        self._git_manager.rollback_neutralization(context, remote=False)
        return ToolResult.error(str(exc))

    # === CREATE PR (Failure C: API fails after successful push) ===
    try:
        pr = self._github_manager.create_pr(...)
    except ExecutionError as exc:
        # Push succeeded. Roll back local commit AND overwrite remote.
        self._git_manager.rollback_neutralization(context, remote=True)
        return ToolResult.error(str(exc))

    # === STATUS ===
    self._pr_status_writer.set_pr_status(branch, PRStatus.OPEN)
    return ToolResult.text(f"PR #{pr['number']} created: {pr['url']}")
```

### 4.4. RecoveryNote Templates

| Scenario | RecoveryNote message |
|----------|---------------------|
| Commit failed + local rollback | `"Neutralization commit failed: {reason}. Working tree has been reset to pre-submit state (hard reset HEAD~1). Retry submit_pr after resolving."` |
| Push failed (Failure D) + local rollback | `"Push failed: {reason}. Local neutralization commit rolled back (hard reset HEAD~1). Working tree is clean. Retry submit_pr after resolving network/remote issue."` |
| create_pr failed (Failure C) + remote rollback | `"GitHub PR creation failed: {reason}. Remote branch has been rolled back (force-push HEAD~1). Working tree is clean. Retry submit_pr once the API issue is resolved."` |
| rollback_neutralization itself fails | `"CRITICAL: Rollback failed: {reason}. Branch may be in degraded state. Manual recovery: git reset --hard HEAD~1 && git push --force-with-lease. Do not commit until resolved."` |

---

## 5. Test Coverage Plan

### New tests to add

| Test file | Test case | Assertion |
|-----------|-----------|-----------|
| `test_submit_pr_atomic_flow.py` | Failure A: no upstream → BlockerNote + error, no git mutation | `git_manager.is_clean` called; `neutralize_to_base` NOT called; `BlockerNote` in context |
| `test_submit_pr_atomic_flow.py` | Failure B: dirty tree → BlockerNote + error, no git mutation | `git_manager.is_clean` returns False; `neutralize_to_base` NOT called; `BlockerNote` in context |
| `test_submit_pr_atomic_flow.py` | Failure C: create_pr fails after push → `rollback_neutralization(remote=True)` called, `RecoveryNote` in context | push called; create_pr raises; rollback called with remote=True |
| `test_submit_pr_atomic_flow.py` | Failure D: push fails (non-upstream) → `rollback_neutralization(remote=False)` called, `RecoveryNote` in context | push raises; rollback called with remote=False, NOT remote=True |
| `test_submit_pr_atomic_flow.py` | Happy path (unchanged): preflights pass → full flow executes, PRStatus.OPEN written | existing test updated with new mock calls for is_clean/has_upstream |
| `test_git_manager.py` | `is_clean()` returns True/False from adapter | adapter.is_clean() delegated |
| `test_git_manager.py` | `has_upstream()` returns True/False from adapter | adapter.has_upstream() delegated |
| `test_git_manager.py` | `rollback_neutralization(remote=False)` calls hard_reset only | force_push_with_lease NOT called |
| `test_git_manager.py` | `rollback_neutralization(remote=True)` calls hard_reset + force_push | both adapter methods called in order |
| `test_git_manager.py` | `rollback_neutralization` failure → ExecutionError + RecoveryNote | critical RecoveryNote contains manual recovery instruction |
| `test_git_adapter.py` | `hard_reset(ref)` calls `git reset --hard {ref}` | git command verified |
| `test_git_adapter.py` | `soft_reset(steps)` calls `git reset --soft HEAD~{steps}` | git command verified |
| `test_git_adapter.py` | `force_push_with_lease()` calls `git push --force-with-lease` | git command verified |

### Existing tests to update

| Test | Change |
|------|--------|
| `test_submit_pr_happy_path` | Add mocks for `is_clean()` (returns True) and `has_upstream()` (returns True) |
| `test_submit_pr_skips_neutralize_when_no_exclusions` | Same: add is_clean/has_upstream mocks |
| `test_submit_pr_pr_status_written_open` | Same: add is_clean/has_upstream mocks |
| `test_push_failure_produces_recovery_note` | Add is_clean/has_upstream mocks + assert `rollback_neutralization(remote=False)` called |
| `test_create_pr_failure_produces_recovery_note` | Add is_clean/has_upstream mocks + assert `rollback_neutralization(remote=True)` called |
- **[docs/development/issue295/research.md][related-1]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-2]**
- **[mcp_server/managers/git_manager.py — pull() preflight pattern lines 234-265][related-3]**
- **[tests/mcp_server/integration/test_submit_pr_atomic_flow.py][related-4]**

<!-- Link definitions -->

[related-1]: docs/development/issue295/research.md
[related-2]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-3]: mcp_server/managers/git_manager.py — pull() preflight pattern lines 234-265
[related-4]: tests/mcp_server/integration/test_submit_pr_atomic_flow.py

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |