<!-- docs\development\issue292\design.md -->
<!-- template=design version=5827e841 created=2026-05-25T14:15Z updated=2026-05-25T14:15Z -->
# Fix Stale-Lambda Pattern and Quality-State Race in Concurrent State Mutations

**Status:** DRAFT
**Version:** 0.1
**Last Updated:** 2026-05-25

---

## 1. Context & Requirements

### 1.1. Problem Statement

`PhaseStateEngine._apply_state()` passes `lambda _s: pre_captured_state` to `WorkflowStateMutator.apply()`, discarding the freshly-loaded state under the lock. This creates a lost-update race across all eight production write paths to `state.json`. `FileQualityStateRepository.apply()` has no `threading.Lock`, allowing concurrent callers to race on `quality_state.json`.

See `docs/development/issue292/research.md` for the full root-cause analysis and Approved Strategy.

### 1.2. Requirements

**Functional:**
- [ ] All `PhaseStateEngine` state writes must derive the returned `BranchState` from the fresh state loaded under the `WorkflowStateMutator` lock.
- [ ] Concurrent calls to `quality_state.json` writers must be serialized at the `FileQualityStateRepository` level.
- [ ] `_save_state()` dead method must be removed from `PhaseStateEngine`.

**Non-Functional:**
- [ ] No changes to `IWorkflowStateMutator` or `IQualityStateRepository` protocol signatures.
- [ ] No version field or optimistic concurrency control added to `BranchState`.
- [ ] Lock timeout for `FileQualityStateRepository.apply()` consistent with `WorkflowStateMutator` (5 seconds).

### 1.3. Constraints

- Approved Strategy prohibits adding a version field / OCC to `BranchState`.
- `IWorkflowStateMutator` interface is already correct — must not change.
- `IQualityStateRepository` protocol must not change.

---

## 2. Design Options

### Boundary 1 — `PhaseStateEngine` → `state.json`

#### Option B1-A: Change `_apply_state()` signature to accept a callback

Change `_apply_state(branch, state: BranchState)` to `_apply_state(branch, mutate: Callable[[BranchState], BranchState])`. The method body becomes a single-line delegate: `self._workflow_state_mutator.apply(branch, mutate)`. All 8 callers are updated to pass transformer lambdas.

**Pros:** Minimal diff — the private routing helper is preserved with the same name. Callers remain slightly shorter than calling the mutator directly. Keeps the design intent from issue #231 (writes routed through a named helper).

**Cons:** `_apply_state` is a one-liner that adds no logic beyond the mutator call. Retaining it means the method has no independent value.

#### Option B1-B: Delete `_apply_state()`, call `_workflow_state_mutator.apply()` directly at all 8 sites

Remove the private helper entirely. Each of the 8 call sites calls `self._workflow_state_mutator.apply(branch, lambda _s: ...)` directly.

**Pros:** Explicit — callers directly express their use of the coordinated mutation boundary. No wrapper with zero logic. Eliminates the exact abstraction layer that hid the bug.

**Cons:** Slightly more verbose at each call site. Removes the named abstraction.

**Selected: B1-B.** The helper `_apply_state()` exists solely because of the stale-capture pattern it implemented. Removing it makes every write path explicit, exposes the mutator contract directly to callers, and eliminates the layer that obscured the bug. Verbosity is minimal: `self._workflow_state_mutator.apply(branch, lambda _s: ...)` vs `self._apply_state(branch, ...)`.

### Boundary 2 — `FileQualityStateRepository` → `quality_state.json`

#### Option B2-A: Add `threading.Lock` to `FileQualityStateRepository.apply()`

Mirror the `WorkflowStateMutator` pattern: `__init__` acquires `threading.Lock()`; `apply()` calls `lock.acquire(timeout=5.0)` before `self.load()`.

**Pros:** Proven pattern in the same codebase. Minimal change. No protocol change.

**Cons:** None material for this scope.

#### Option B2-B: Extract a shared `BaseLockingRepository` class

Deduplicate the lock pattern into a base class that both mutator and repository inherit or delegate to.

**Pros:** DRY if a third locking repository is anticipated.

**Cons:** Over-engineering for a bug fix. The pattern appears in exactly two places; a shared base would increase blast radius and is out of scope for a bug fix.

**Selected: B2-A.** The lock pattern is two files deep. A shared base is deferred until a third consumer materialises.

### Boundary 3 — `_save_state()` dead method

No design options — removal is the only choice consistent with the Approved Strategy. Category A test sites migrate to the injected state repository; Category B sites are deleted.

---

## 3. Chosen Design

### 3.1. `PhaseStateEngine` — Remove `_apply_state()`, inline transformer lambdas

`_apply_state()` is deleted. Every former call site calls `self._workflow_state_mutator.apply()` directly with a lambda that derives its result from `_s`.

#### Lambda contract per caller category

**Update callers** — derive return value from `_s` via `with_updates()`:

| Method | Fields updated |
|---|---|
| `transition()` | `current_phase`, `transitions` (appends to `_s.transitions`), `current_sub_phase=None` |
| `force_transition()` | `current_phase`, `transitions` (appends to `_s.transitions`), `skip_reason`, `current_sub_phase=None` |
| `transition_cycle()` | `last_cycle`, `current_cycle`, `cycle_history` (appends to `_s.cycle_history`), `current_sub_phase=None` |
| `force_cycle_transition()` | `last_cycle`, `current_cycle`, `cycle_history` (appends to `_s.cycle_history`), `current_sub_phase=None` |
| `on_enter_cycle_based_phase()` | `current_cycle=1`, `last_cycle=0`, `cycle_history` (appends to `_s.cycle_history`) — only when `_s.current_cycle is None` |
| `on_exit_cycle_based_phase()` | `last_cycle=_s.current_cycle`, `current_cycle=None` — only when `_s.current_cycle is not None` |
| `initialize_branch()` | All initialization fields set via `_s.with_updates(workflow_name=..., current_phase=..., ...)` — complete field replacement derived from `_s` |
| `_load_state_or_reconstruct()` | `lambda _s: reconstructed_state` where `reconstructed_state` is derived from git history, not from a pre-lock read of `state.json`. This is not the stale-capture anti-pattern; the source is external to the file being locked. The lock serializes concurrent reconstructions. |

#### Redundant `get_state()` pre-reads

`on_enter_cycle_based_phase()` and `on_exit_cycle_based_phase()` currently call `get_state()` before `_apply_state()` to capture the existing state before mutating it. After the fix, `_s` in the transformer lambda provides the same fresh state. The `get_state()` pre-read in these two methods becomes redundant and is removed.

#### `_save_state()` removal

The method is deleted. No production caller exists. See test-surface impact in §3.3.

### 3.2. `FileQualityStateRepository` — Add `threading.Lock`

```
# Before (no serialization):
def apply(self, mutate):
    current = self.load()
    updated = mutate(current)
    write(updated)

# After (serialized):
def __init__(self, ...):
    self._lock = threading.Lock()

def apply(self, mutate):
    acquired = self._lock.acquire(timeout=5.0)
    if not acquired:
        raise <timeout exception>
    try:
        current = self.load()
        updated = mutate(current)
        write(updated)
    finally:
        self._lock.release()
```

The exception type for lock timeout follows the project's existing pattern: a structured typed exception with `diagnostic` and `recovery` fields, modelled on `StateMutationConflictError`. A new `QualityStateMutationConflictError` in `quality_state_repository.py` avoids importing from `workflow_state_mutator.py` and prevents a circular dependency risk.

**Propagation path:** `FileQualityStateRepository.apply()` raises `QualityStateMutationConflictError` on lock timeout. The two `QAManager` callers (`_advance_baseline_on_all_pass` at L309 and `_accumulate_failed_files_on_failure` at L321) do not catch it — the exception propagates to the MCP tool layer. The tool that invoked the quality-gate run catches `QualityStateMutationConflictError` and wraps it in an operator-facing error result with a `RecoveryNote`, following the same pattern used today for `StateMutationConflictError`. No existing `QAManager` catch blocks are modified.

`IQualityStateRepository` protocol is not changed — `apply()` signature is identical; the lock is an internal implementation detail.

### 3.3. Affected Interfaces and Callers

#### Interfaces — unchanged

| Interface | Change |
|---|---|
| `IWorkflowStateMutator.apply()` | None — already correct |
| `IQualityStateRepository.apply()` | None — protocol unchanged |
| `BranchState.with_updates()` | None |
| `QualityState` | None |

#### `PhaseStateEngine` — internal surface change

| Symbol | Change |
|---|---|
| `_apply_state(branch, state)` | **Deleted** |
| `_save_state(branch, state)` | **Deleted** |
| All 8 former `_apply_state()` callers | Now call `self._workflow_state_mutator.apply()` directly |
| `on_enter_cycle_based_phase()` | `get_state()` pre-read removed (absorbed by `_s`) |
| `on_exit_cycle_based_phase()` | `get_state()` pre-read removed (absorbed by `_s`) |

#### `FileQualityStateRepository` — internal change only

| Symbol | Change |
|---|---|
| `__init__` | Gains `self._lock = threading.Lock()` |
| `apply()` | Gains lock acquisition and `QualityStateMutationConflictError` on timeout |

### 3.4. Affected Test Surfaces

| Test file | Impact | Action |
|---|---|---|
| `tests/mcp_server/unit/managers/test_phase_state_engine.py` | Exercises all 8 callers via integration paths | New concurrent-write regression test added; existing tests verify corrected behaviour |
| `tests/mcp_server/unit/tools/test_cycle_tools_legacy.py` | 7 Category A `_save_state()` fixture sites | Migrated: replace `engine._save_state(branch, state)` with injected state-repository write |
| `tests/mcp_server/unit/tools/test_discovery_tools.py` | 2 Category A `_save_state()` fixture sites | Migrated: same pattern as above |
| `tests/mcp_server/managers/test_phase_state_engine_async.py` | 2 Category B `_save_state()` behaviour tests (L63, L106) | **Deleted** — non-blocking I/O contract is void once `_save_state()` is removed |
| `tests/mcp_server/unit/managers/test_quality_state_repository.py` | Protocol and `apply()` behaviour tests | New lock-contention test added |
| `tests/mcp_server/unit/managers/test_baseline_advance.py` | `QAManager` integration tests | Verify no regressions from lock addition |

### 3.5. Validation Strategy

**Lost-update regression test (Boundary 1) — primary proof (mixed phase/cycle writers):**
The filed bug scenario is `force_transition()` and `force_cycle_transition()` running concurrently. Thread A calls `force_transition()` to change phase; Thread B calls `force_cycle_transition()` to change cycle, against the same branch. Use `threading.Barrier` to synchronize entry. Assert the final state contains the phase change from A **and** the cycle-history entry from B — neither mutation is lost.

**Lost-update regression test (Boundary 1) — secondary proof (homogeneous writers):**
Two concurrent `force_transition()` calls against the same branch. Assert both transition records appear in the final state.

**Lock-contention test (Boundary 2):**
Two threads concurrently call `FileQualityStateRepository.apply()` with an accumulation callback. Assert the final accumulated result reflects both writes (neither lost).

**Standard regression guard (all callers):**
Each of the 8 former `_apply_state()` call sites has an existing unit test. After the fix, existing tests continue to pass unchanged, providing a regression guard that the corrected lambdas compute the same result as the stale-lambda pattern under single-threaded conditions.

---

## Open Questions

None — all design-sensitive decisions resolved from the Approved Strategy.

---

## Related Documentation

- `docs/development/issue292/research.md` — root cause, blast radius, and Approved Strategy
- `docs/development/issue231/design.md` — `IWorkflowStateMutator` original design intent
- `mcp_server/managers/workflow_state_mutator.py` — reference lock + callback implementation

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-05-25 | Agent | Initial draft |
| 0.2 | 2026-05-25 | Agent | QA NOGO fixes: creation-caller framing removed, mixed-writer proof added, QualityStateMutationConflictError propagation path added |
| 0.3 | 2026-05-25 | Agent | QA NOGO fix: _load_state_or_reconstruct() now references explicit approved exception in research.md v1.2 |
