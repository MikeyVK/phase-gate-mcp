<!-- docs\development\issue295\design.md -->
<!-- template=design version=5827e841 created=2026-05-05T20:28Z updated= -->
# submit_pr Atomicity: prepare_submission + rollback_push

**Status:** DRAFT
**Version:** 1.0
**Last Updated:** 2026-05-05

---

## Purpose

Define the API contract and internal flow for the three changed files, resolve the open data-interface question, and specify test contracts for all new and changed code.

## Scope

**In Scope:**
`mcp_server/managers/git_manager.py`, `mcp_server/adapters/git_adapter.py`, `mcp_server/tools/pr_tools.py`, and their test files.

**Out of Scope:**
`enforcement.yaml`, `contracts.yaml`, `MergePRTool`, `GitCommitTool`, `initialize_project`.

## Prerequisites

1. [docs/development/issue295/research.md](research.md) — FINAL v3.1
2. [docs/coding_standards/ARCHITECTURE_PRINCIPLES.md](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)

---

## 1. Context & Requirements

### 1.1 Problem Statement

`SubmitPRTool.execute()` orchestrates git steps directly (§1.1 SRP violation) and has no atomicity. Four failure modes leave the branch in degraded non-recoverable state:

- **Failure A** — No upstream: neutralize + commit succeed, push fails → branch stranded
- **Failure B** — Dirty tree: `git add .` in `commit_with_scope` silently consumes untracked files → state.json lands on main
- **Failure C** — API failure after push: no rollback mechanism → branch permanently stranded
- **Failure D** — Push fails after commit (non-upstream): local neutralization commit stranded, second attempt finds nothing to neutralize

### 1.2 Requirements

**Functional:**
- `GitManager.prepare_submission()` encapsulates the full git transaction: is_clean preflight → has_upstream preflight → artifact-filter → neutralize → commit → push — with internal rollbacks for commit failure (Failure D partial) and push failure (Failure D)
- `GitManager.rollback_push()` handles remote rollback after push-success + create_pr failure (Failure C)
- `SubmitPRTool.execute()` reduced to 3 high-level calls: `prepare_submission` + `create_pr` + `set_pr_status`
- All four failure modes leave the branch clean and retryable

**Non-Functional:**
- `GitManager` stays git-focused: `MergeReadinessContext` must not cross the layer boundary (§10 Cohesion)
- Full compliance with ARCHITECTURE_PRINCIPLES.md §1.1, §4, §7, §8, §10, §14

### 1.3 Constraints

- `MergeReadinessContext` must not be passed to `GitManager` (§10 Cohesion — see Finding 10 in research.md)
- Tool body must not contain `neutralize_to_base`, `commit_with_scope`, `push`, `has_net_diff_for_path`, or `_git_manager.adapter` after refactor (§7 LoD)
- All test cases through public API only (§14)
- No new exception types: `PreflightError` and `ExecutionError` already exist in `mcp_server/core/exceptions.py`

---

## 2. Design Options

### Open Question: Data Interface for artifact_paths

**Question:** What type does the tool pass to `GitManager.prepare_submission()` for artifact paths?

**Constraint:** `MergeReadinessContext` (defined in `managers/phase_contract_resolver.py`) must not enter `GitManager` (§10 Cohesion — git manager must not require phase-contract knowledge).

**Options evaluated:**

| Option | Type | Pro | Con |
|--------|------|-----|-----|
| A | `frozenset[str]` | Pure data; GitManager stays git-focused; immutable; no cross-domain coupling | Tool responsible for path extraction (one line, acceptable) |
| B | Light DTO `ArtifactPaths(paths: frozenset[str])` | Named type makes intent explicit | Creates a new type for a trivial wrapper; YAGNI §9 — no behavioral need |

**Decision: Option A — `frozenset[str]`.**

Rationale: The extraction is one line (`frozenset(a.path for a in self._merge_readiness_context.branch_local_artifacts)`). A named DTO adds no behavior and no testability benefit — YAGNI §9. `frozenset[str]` is the minimal, explicit data boundary that satisfies §10 Cohesion.

---

## 3. Chosen Design

**Decision:** Introduce `GitManager.prepare_submission(artifact_paths: frozenset[str], base: str, note_context: NoteContext) -> None` encapsulating the full git transaction with internal rollbacks, and `GitManager.rollback_push(note_context: NoteContext) -> None` for remote rollback. Add `GitAdapter.hard_reset(ref: str) -> None` and `GitAdapter.force_push_with_lease(remote: str = "origin") -> None` as new adapter primitives. `SubmitPRTool.execute()` delegates to these two manager methods.

**Rationale:** Matches the canonical `GitManager.pull()`/`merge()`/`create_branch()` pattern — all encapsulate preflights internally. §1.1 SRP: tool has one axis of change (git+github+status orchestration). §7 LoD: tool does not reach into git internals. §10 Cohesion: GitManager stays git-focused.

### 3.1 Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Data interface for artifact paths | `frozenset[str]` | §10 Cohesion: GitManager must not import MergeReadinessContext. §9 YAGNI: no DTO needed. |
| Local rollback on commit failure | `hard_reset("HEAD")` | Commit failed → HEAD did not advance; reset HEAD restores working tree to pre-neutralization state |
| Local rollback on push failure | `hard_reset("HEAD~1")` | Push failed → commit exists locally but not on remote; reset HEAD~1 undoes the commit |
| Remote rollback after API failure | `hard_reset("HEAD~1")` + `force_push_with_lease()` | Must undo the pushed commit from remote. `--force-with-lease` is safe: we own that commit (BranchMutatingTool prevents concurrent mutations) |
| Rollback meta-failure | `RecoveryNote` + propagate `ExecutionError` | Never swallow; gives operator manual recovery instructions |
| commit_with_scope skip_paths | Pass `artifact_paths` as `skip_paths` instead of `files=` | Avoids `git add .` consuming untracked files (root cause of Failure B). Only the artifacts are staged; everything else is excluded via `skip_paths` postcondition |

---

## 4. API Specification

### 4.1 GitAdapter — new methods

```python
def hard_reset(self, ref: str) -> None:
    """Execute git reset --hard {ref}.

    Args:
        ref: Git reference (e.g. "HEAD", "HEAD~1", commit SHA).

    Raises:
        ExecutionError: If git reset fails.
    """

def force_push_with_lease(self, remote: str = "origin") -> None:
    """Execute git push --force-with-lease on the current branch.

    Safe to use after a hard_reset because BranchMutatingTool enforcement
    prevents concurrent mutations on the same branch.

    Args:
        remote: Remote name (default "origin").

    Raises:
        ExecutionError: If push fails (network, rejection, etc.).
    """
```

### 4.2 GitManager — new methods

```python
def prepare_submission(
    self,
    artifact_paths: frozenset[str],
    base: str,
    note_context: NoteContext,
) -> None:
    """Atomically execute the full git side of branch submission.

    Steps (in order):
        1. Preflight — is_clean(): if False → BlockerNote + PreflightError (no mutation)
        2. Preflight — has_upstream(): if False → BlockerNote + PreflightError (no mutation)
        3. Filter — for each path in artifact_paths: has_net_diff_for_path(path, base)
                    → collect to_neutralize: frozenset[str]
        4. Neutralize — neutralize_to_base(to_neutralize, base) [skipped if empty]
        5. Commit  — commit_with_scope(workflow_phase="ready", ...,
                                       skip_paths=artifact_paths)
                     On failure → hard_reset("HEAD") + RecoveryNote + re-raise ExecutionError
        6. Push    — push()
                     On failure → hard_reset("HEAD~1") + RecoveryNote + re-raise ExecutionError

    Args:
        artifact_paths: Full set of candidate branch-local artifact paths to check.
                        The method internally filters to those with a net diff.
        base:           Base branch name (e.g. "main").
        note_context:   NoteContext for BlockerNote / RecoveryNote production.

    Raises:
        PreflightError:  If working tree is not clean or no upstream is configured.
                         No mutation has occurred.
        ExecutionError:  If commit or push fails. The mutation has been rolled back;
                         working tree is clean and retryable.
    """

def rollback_push(self, note_context: NoteContext) -> None:
    """Roll back a successful push after a failed create_pr.

    Steps:
        1. hard_reset("HEAD~1") — undo neutralization commit locally
        2. force_push_with_lease() — overwrite remote with pre-submit HEAD

    On force_push_with_lease failure:
        → RecoveryNote with manual recovery instructions
        → re-raise ExecutionError (never swallow)

    Args:
        note_context: NoteContext for RecoveryNote production on meta-failure.

    Raises:
        ExecutionError: If force_push_with_lease fails.
                        Manual recovery required (see RecoveryNote for instructions).
    """
```

**Note on `skip_paths` in step 5:** `commit_with_scope` already accepts `skip_paths: frozenset[str]`. Passing `artifact_paths` (the full set, not just the filtered subset) ensures that even untracked artifact files that were missed by `has_net_diff_for_path` cannot slip into the commit via `git add .`. This is the root cause fix for Failure B.

### 4.3 SubmitPRTool.execute() — revised body

```python
async def execute(self, params: SubmitPRInput, context: NoteContext) -> ToolResult:
    branch = self._git_manager.get_current_branch()
    base = params.base or self._git_manager.git_config.default_base_branch

    artifact_paths = frozenset(
        a.path for a in self._merge_readiness_context.branch_local_artifacts
    )

    # [GIT] Full git transaction — preflights + neutralize + commit + push + local rollback
    try:
        self._git_manager.prepare_submission(artifact_paths, base, context)
    except (PreflightError, ExecutionError) as exc:
        return ToolResult.error(str(exc))

    # [GITHUB] Create PR — rollback push on failure
    try:
        result = self._github_manager.create_pr(
            title=params.title,
            body=params.body or "",
            head=params.head,
            base=base,
            draft=params.draft,
        )
    except ExecutionError as exc:
        self._git_manager.rollback_push(context)
        return ToolResult.error(str(exc))

    # [STATUS] Record PR as open
    self._pr_status_writer.set_pr_status(branch, PRStatus.OPEN)
    return ToolResult.text(f"Created PR #{result['number']}: {result['url']}")
```

---

## 5. Sequence Diagrams

### 5.1 Happy Path

```
SubmitPRTool.execute()
  │
  ├─ get_current_branch() → "feature/42-..."
  ├─ extract artifact_paths from merge_readiness_context
  │
  ├─ GitManager.prepare_submission(artifact_paths, base, ctx)
  │    ├─ adapter.is_clean() → True
  │    ├─ adapter.has_upstream() → True
  │    ├─ for path: has_net_diff_for_path → [".st3/state.json"]
  │    ├─ neutralize_to_base({".st3/state.json"}, "main")
  │    ├─ commit_with_scope(phase="ready", skip_paths=artifact_paths) → "abc1234"
  │    └─ push()
  │
  ├─ github_manager.create_pr(...) → {number: 42, url: "..."}
  ├─ pr_status_writer.set_pr_status(branch, OPEN)
  └─ ToolResult.text("Created PR #42: ...")
```

### 5.2 Failure A — No upstream (PreflightError before any mutation)

```
GitManager.prepare_submission(...)
  ├─ adapter.is_clean() → True
  ├─ adapter.has_upstream() → False
  ├─ note_context.produce(BlockerNote("No upstream tracking branch..."))
  └─ raise PreflightError("No upstream configured for current branch")

SubmitPRTool: catches PreflightError → ToolResult.error(str(exc))
No mutation. Branch is clean. Retryable after running git_push(set_upstream=True).
```

### 5.3 Failure B — Dirty tree (PreflightError before any mutation)

```
GitManager.prepare_submission(...)
  ├─ adapter.is_clean() → False
  ├─ note_context.produce(BlockerNote("Working tree is not clean..."))
  └─ raise PreflightError("Working directory is not clean")

SubmitPRTool: catches PreflightError → ToolResult.error(str(exc))
No mutation. Branch is clean. Retryable after committing all pending changes.
```

### 5.4 Failure C — GitHub API failure after successful push

```
GitManager.prepare_submission(...) → completes OK (commit + push succeeded)

github_manager.create_pr(...) → raises ExecutionError("422 PR already exists")

SubmitPRTool: catches ExecutionError
  ├─ GitManager.rollback_push(ctx)
  │    ├─ adapter.hard_reset("HEAD~1")   ← local commit undone
  │    └─ adapter.force_push_with_lease()  ← remote overwritten
  └─ ToolResult.error(str(exc))

Branch is clean locally and remotely. Retryable.
```

### 5.5 Failure D — Push failure after commit

```
GitManager.prepare_submission(...)
  ├─ adapter.is_clean() → True
  ├─ adapter.has_upstream() → True
  ├─ neutralize_to_base(...)
  ├─ commit_with_scope(...) → "abc1234"  [commit succeeded locally]
  ├─ push() → raises ExecutionError("remote rejected")
  ├─ hard_reset("HEAD~1")   ← local commit undone; working tree restored
  ├─ note_context.produce(RecoveryNote("Push failed: ..."))
  └─ re-raise ExecutionError

SubmitPRTool: catches ExecutionError → ToolResult.error(str(exc))
Branch is clean locally. Nothing reached remote. Retryable.
```

### 5.6 Failure C meta-failure — rollback_push itself fails

```
GitManager.rollback_push(ctx)
  ├─ adapter.hard_reset("HEAD~1")   ← succeeds locally
  ├─ adapter.force_push_with_lease() → raises ExecutionError("rejected")
  ├─ note_context.produce(RecoveryNote(
  │      "CRITICAL: Remote rollback failed. Manual recovery: "
  │      "git reset --hard HEAD~1 && git push --force-with-lease. "
  │      "Do not commit until resolved."
  │  ))
  └─ re-raise ExecutionError

SubmitPRTool: catches ExecutionError → ToolResult.error(str(exc))
Local branch is in pre-submit state; remote is stuck at push. Operator must intervene.
```

---

## 6. Test Design

All tests via public API (§14 — no `_private` access). All mocks via constructor injection (§11 — no monkeypatching internals).

### 6.1 GitAdapter unit tests — new methods

**File:** `tests/mcp_server/unit/adapters/test_git_adapter.py`

| Test | Input | Expected |
|------|-------|----------|
| `test_hard_reset_calls_git_reset_hard_with_ref` | `ref="HEAD"` | `repo.git.reset("--hard", "HEAD")` called |
| `test_hard_reset_calls_git_reset_hard_with_parent` | `ref="HEAD~1"` | `repo.git.reset("--hard", "HEAD~1")` called |
| `test_hard_reset_raises_execution_error_on_failure` | git raises | `ExecutionError` |
| `test_force_push_with_lease_calls_git_push` | `remote="origin"` | `repo.git.push("--force-with-lease", ...)` called |
| `test_force_push_with_lease_raises_execution_error_on_failure` | git raises | `ExecutionError` |

### 6.2 GitManager unit tests — prepare_submission

**File:** `tests/mcp_server/unit/managers/test_git_manager.py`

All tests inject a `MagicMock(spec=GitAdapter)` via `GitManager(adapter=mock_adapter, ...)`.

| Test | Scenario | Expected behavior |
|------|----------|-------------------|
| `test_prepare_submission_raises_preflight_error_when_dirty` | `adapter.is_clean()` returns `False` | `BlockerNote` produced; `PreflightError` raised; no further adapter calls |
| `test_prepare_submission_raises_preflight_error_when_no_upstream` | `is_clean()=True`, `has_upstream()=False` | `BlockerNote` produced; `PreflightError` raised; `neutralize_to_base` not called |
| `test_prepare_submission_neutralizes_only_artifacts_with_net_diff` | two artifacts: one with diff, one without | `neutralize_to_base` called with only the path that has diff |
| `test_prepare_submission_skips_neutralize_when_no_diffs` | `has_net_diff_for_path` returns `False` for all paths | `neutralize_to_base` not called |
| `test_prepare_submission_passes_full_artifact_paths_as_skip_paths` | happy path | `commit_with_scope` called with `skip_paths == artifact_paths` (full set, not filtered) |
| `test_prepare_submission_hard_resets_head_on_commit_failure` | `adapter.commit` raises | `adapter.hard_reset("HEAD")` called; `RecoveryNote` produced; `ExecutionError` re-raised |
| `test_prepare_submission_hard_resets_head_minus_one_on_push_failure` | `adapter.push` raises | `adapter.hard_reset("HEAD~1")` called; `RecoveryNote` produced; `ExecutionError` re-raised |
| `test_prepare_submission_happy_path_calls_steps_in_order` | all succeeds | adapter calls in order: is_clean → has_upstream → has_net_diff_for_path → neutralize_to_base → commit → push |

### 6.3 GitManager unit tests — rollback_push

**File:** `tests/mcp_server/unit/managers/test_git_manager.py`

| Test | Scenario | Expected behavior |
|------|----------|-------------------|
| `test_rollback_push_hard_resets_and_force_pushes` | both succeed | `adapter.hard_reset("HEAD~1")` then `adapter.force_push_with_lease()` called; no exception |
| `test_rollback_push_produces_recovery_note_and_raises_on_force_push_failure` | `force_push_with_lease` raises | `adapter.hard_reset("HEAD~1")` still called first; `RecoveryNote` produced with manual recovery text; `ExecutionError` re-raised |

### 6.4 SubmitPRTool integration tests

**File:** `tests/mcp_server/integration/test_submit_pr_atomic_flow.py`

Tests inject `MagicMock(spec=GitManager)` and `MagicMock(spec=GitHubManager)` via the `SubmitPRTool` constructor. Tool body is tested via `tool.execute(params, context)`.

| Test | Scenario | Expected behavior |
|------|----------|-------------------|
| `test_failure_a_no_upstream_blocked_before_mutation` | `prepare_submission` raises `PreflightError` | `result.is_error=True`; `create_pr` not called; `set_pr_status` not called |
| `test_failure_b_dirty_tree_blocked_before_mutation` | `prepare_submission` raises `PreflightError` | `result.is_error=True`; `create_pr` not called; `set_pr_status` not called |
| `test_failure_c_create_pr_failure_triggers_rollback_push` | `prepare_submission` succeeds, `create_pr` raises | `rollback_push` called with `context`; `result.is_error=True`; `set_pr_status` not called |
| `test_failure_d_push_fails_prepare_submission_raises_execution_error` | `prepare_submission` raises `ExecutionError` | `result.is_error=True`; `rollback_push` not called; `set_pr_status` not called |
| `test_happy_path_prepare_submission_then_create_pr_then_status` | all succeed | `prepare_submission` called with `frozenset` of paths; `set_pr_status(branch, OPEN)` called |
| `test_happy_path_artifact_paths_extracted_from_merge_readiness_context` | two artifacts in context | `prepare_submission` called with `frozenset({path1, path2})` as first arg |

### 6.5 SubmitPRTool structural tests (LoD assertion)

**File:** `tests/mcp_server/unit/tools/test_submit_pr_tool.py`

| Test | Assertion |
|------|-----------|
| `test_submit_pr_tool_execute_has_no_adapter_calls` | `SubmitPRTool.execute` source must not contain `_git_manager.adapter` |
| `test_submit_pr_tool_execute_has_no_git_internal_calls` | `SubmitPRTool.execute` source must not contain any of: `neutralize_to_base`, `commit_with_scope`, `push`, `has_net_diff_for_path` |

### 6.6 test_model1_branch_tip_neutralization.py — scope decision

**Decision:** No changes needed. `test_model1_branch_tip_neutralization.py` tests the `GitCommitTool → GitManager.commit_with_scope → GitAdapter` path using `ExclusionNote`. This path is distinct from `prepare_submission`. The integration coverage is complementary, not redundant. The file remains unchanged.

---

## 7. Error Messages (canonical)

| Failure | Note type | Message |
|---------|-----------|---------|
| A — no upstream | `BlockerNote` | `"No upstream tracking branch configured. Run git_push(set_upstream=True) before submit_pr."` |
| B — dirty tree | `BlockerNote` | `"Working tree is not clean. Commit or stash all changes before submit_pr."` |
| C — create_pr failed rollback success | `RecoveryNote` | `"GitHub PR creation failed: {reason}. Remote branch has been rolled back to pre-submit state. Working tree is clean. Retry submit_pr once the API issue is resolved."` |
| D — push failed | `RecoveryNote` | `"Push failed: {reason}. Local neutralization commit rolled back. Working tree is clean. Retry submit_pr after resolving the remote issue."` |
| Meta-failure — force_push_with_lease failed | `RecoveryNote` | `"CRITICAL: Remote rollback failed: {reason}. Manual recovery: git reset --hard HEAD~1 && git push --force-with-lease. Do not commit until resolved."` |

---

## Related Documentation

- [docs/development/issue295/research.md](research.md) — FINAL v3.1
- [mcp_server/managers/git_manager.py](../../../mcp_server/managers/git_manager.py)
- [mcp_server/adapters/git_adapter.py](../../../mcp_server/adapters/git_adapter.py)
- [mcp_server/tools/pr_tools.py](../../../mcp_server/tools/pr_tools.py)
- [tests/mcp_server/integration/test_submit_pr_atomic_flow.py](../../../tests/mcp_server/integration/test_submit_pr_atomic_flow.py)
- [tests/mcp_server/unit/tools/test_submit_pr_tool.py](../../../tests/mcp_server/unit/tools/test_submit_pr_tool.py)
- [docs/coding_standards/ARCHITECTURE_PRINCIPLES.md](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |