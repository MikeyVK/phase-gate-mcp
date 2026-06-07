<!-- docs\development\issue292\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-25T13:53Z updated=2026-05-25T14:00Z -->
# Root Cause Analysis: Concurrent State Mutations — Lost Updates in WorkflowStateMutator

**Status:** COMPLETE  
**Version:** 1.0  
**Last Updated:** 2026-05-25

---

## Problem Statement

`force_transition` and `force_cycle_transition` can both report success when called concurrently against the same branch, but one update is silently lost. `WorkflowStateMutator.apply()` loads a fresh `BranchState` under a `threading.Lock` and passes it to the caller-supplied callback. However, all `PhaseStateEngine` callers supply `lambda _s: pre_captured_state`, discarding the fresh read. The lock serializes writes but does not eliminate the lost-update race in the outer load→mutate→write window.

---

## Research Goals

1. Confirm the root cause and full blast radius of the stale-lambda pattern across all PSE write paths.
2. Identify every bypass of the coordinated write path (both `state.json` and `quality_state.json`).
3. Capture an Approved Strategy for the fix, covering `PhaseStateEngine` callers and `FileQualityStateRepository`.
4. Document which test locations depend on the broken pattern and will need updating.

---

## Scope

**In scope:**
- `PhaseStateEngine` write paths (`_apply_state`, `_save_state`)
- `WorkflowStateMutator.apply()` callback contract
- `FileQualityStateRepository.apply()` concurrency
- Test fixture locations using `_save_state()` directly

**Out of scope:**
- Cross-process or distributed locking
- Optimistic concurrency control / version field additions (ruled out by Approved Strategy)
- `cycle_tools.py` bypass (arch doc A-02 — already resolved in production)
- CQRS redesign

---

## Background

Issue #231 introduced `IWorkflowStateMutator` with the explicit design intent that all branch-state writes go through `WorkflowStateMutator.apply()`. The contract requires callers to supply a transformer function that receives the freshly loaded state under the lock and returns the updated state. This makes callers agnostic of locking, fresh reads, and other concurrent writers.

The `_apply_state()` helper in `PhaseStateEngine` was meant to be the single routing point for this contract. In practice, every caller pre-computes the desired new state before calling `_apply_state()`, and passes it as a constant lambda — violating the intent of the interface.

---

## Findings

### Root Cause: Stale Lambda Pattern

`WorkflowStateMutator.apply()` correctly:
1. Acquires `threading.Lock` (timeout = 5 s)
2. Calls `_load_or_bootstrap(branch)` to get fresh state
3. Passes that fresh state to `mutate(state)`
4. Saves the returned state via `IStateRepository.save()`

All eight production call sites in `PhaseStateEngine` violate this contract:

```python
# WRONG — current pattern in all _apply_state() callers:
updated_state = state.with_updates(current_phase=to_phase, ...)   # computed outside lock
self._apply_state(branch, updated_state)                          # _s (fresh read) discarded

# Inside _apply_state():
self._workflow_state_mutator.apply(branch, lambda _s: state)      # _s ignored
```

Lost-update scenario:

```
Caller A (force_transition):       Caller B (force_cycle_transition):
  load state  ← stale A              load state  ← stale B
  mutate in memory                   mutate in memory
  lock.acquire()
  fresh read  ← discarded!
  write stale A
  lock.release()                     lock.acquire()
                                     fresh read  ← discarded!
                                     write stale B  ← A's changes LOST
```

### Affected Production Write Paths — `state.json`

All eight `_apply_state()` call sites in `PhaseStateEngine` use the stale lambda pattern:

| Method | Line |
|---|---|
| `initialize_branch()` | L176 |
| `transition()` | L223 |
| `force_transition()` | L291 |
| `transition_cycle()` | L349 |
| `force_cycle_transition()` | L415 |
| `_load_state_or_reconstruct()` | L527 |
| `on_enter_cycle_based_phase()` | L726 |
| `on_exit_cycle_based_phase()` | L745 |

`_save_state()` is defined at L674 but has **zero production call sites** — it is a dead method that exists only as a test fixture shortcut.

### Affected Production Write Paths — `quality_state.json`

`FileQualityStateRepository.apply()` (`managers/quality_state_repository.py`) has no `threading.Lock`. It reads current `QualityState`, applies the callback, and writes via `AtomicJsonWriter` — all without serialization. Concurrent callers race on `quality_state.json` independently of the `state.json` lock.

**Live callers in `qa_manager.py`:**
- `_advance_baseline_on_all_pass()` at L309 — calls `_quality_state_repository.apply(lambda _s: QualityState(baseline_sha=head_sha, failed_files=[]))`
- `_accumulate_failed_files_on_failure()` at L321 — calls `_quality_state_repository.apply(_union)` to accumulate failed files

**Affected test surfaces:**
- `tests/mcp_server/unit/managers/test_quality_state_repository.py` — protocol and `apply()` behaviour tests
- `tests/mcp_server/unit/managers/test_baseline_advance.py` — baseline-advance integration tests

### Non-Violations Confirmed

- `record_sub_phase()` already uses the correct transformer pattern:
  `_workflow_state_mutator.apply(branch, lambda s: s.with_updates(current_sub_phase=sub_phase))`
- `cycle_tools.py` does **not** call `_save_state()` — arch doc A-02 is stale.
- `QAManager` no longer writes to `state.json` directly; the direct `write_text` bypass described in the issue body is already resolved.
- `AtomicJsonWriter.write_json()` uses temp-file + `os.replace()` — crash-safe at disk level.
- `StateMutationConflictError` and `RecoveryNote` infrastructure already exists for operator-facing conflict reporting.

### Affected Tests — `_save_state()` call sites

Eleven test locations call `engine._save_state()`. They split into two categories:

**Category A — Fixture-injection sites (9 sites):** tests that use `_save_state()` only to inject pre-canned state before exercising unrelated behaviour.

| Test file | Sites |
|---|---|
| `tests/mcp_server/unit/tools/test_cycle_tools_legacy.py` | 7 |
| `tests/mcp_server/unit/tools/test_discovery_tools.py` | 2 |

Migration: replace each `engine._save_state(branch, state)` call with a direct write through the injected state repository that is already in scope in each test setup.

**Category B — Functional behaviour tests (2 sites):** `tests/mcp_server/managers/test_phase_state_engine_async.py` (L63, L106) test the non-blocking I/O contract of `_save_state()` itself, introduced in issue #85. Once `_save_state()` is deleted, this contract is void. These tests are to be deleted; the underlying atomic-write behaviour is already covered by `AtomicJsonWriter` unit tests.

---

## Approved Strategy

**Decision captured at interaction checkpoint — 2026-05-25.**

### Boundary 1: `PhaseStateEngine` → `state.json`

**Fix: transformer-lambda callers.**

All `_apply_state()` call sites are rewritten so the callback derives its result from the `_s` argument (the fresh state loaded under the lock) rather than from a pre-captured external object. Callers express only **what to change**, not **the full new state**.

```python
# CORRECT — after fix:
self._workflow_state_mutator.apply(
    branch,
    lambda _s: _s.with_updates(current_phase=to_phase, transitions=[...], current_sub_phase=None),
)
```

`_save_state()` is formally removed from production. Category A fixture-injection sites migrate to use the injected state repository directly; Category B functional behaviour tests are deleted.

No version field / OCC is added to `BranchState`. The lock + transformer pattern is sufficient when callers correctly use `_s`.

**Approved exception — `_load_state_or_reconstruct()`:** This is the only call site where the lambda does not express a delta from `_s`. It is reached only in error-recovery paths (corrupt or missing `state.json`), where `_s` would be a default-empty bootstrap or itself corrupted data. The reconstructed state is derived entirely from authoritative git log history and has no relationship to a pre-lock read of `state.json`. The full-replacement form `lambda _s: reconstructed_state` is the correct form for this path: there is no partial state in `_s` worth preserving, and expressing the reconstruction as `_s.with_updates(ALL_FIELDS)` would risk silently retaining corrupt fields that are not explicitly named. All other seven call sites use the standard delta pattern.

### Boundary 2: `FileQualityStateRepository` → `quality_state.json`

**Fix: add `threading.Lock` to `FileQualityStateRepository.apply()`.**

Same pattern as `WorkflowStateMutator`: lock → read → apply callback → write. No changes to `IQualityStateRepository` protocol signature.

### Boundary 3: `_save_state()` dead method

**Fix: remove from production; migrate 9 Category A fixture sites; delete 2 Category B behaviour tests.**

The method is deleted from `PhaseStateEngine`. Category A sites (9 fixture injections in `test_cycle_tools_legacy.py` and `test_discovery_tools.py`) are migrated to write directly through the injected state repository in each test's existing setup. Category B sites (2 behaviour tests in `test_phase_state_engine_async.py`) are deleted — the `_save_state()` non-blocking I/O contract from issue #85 is void once the method is removed.

### What this does NOT change

- `IWorkflowStateMutator` interface — already correct
- `WorkflowStateMutator.apply()` implementation — already correct
- `BranchState` schema — no version field added
- `record_sub_phase()` — already correct
- `QAManager` write path — already correct

---

## Open Questions

None — all strategy-sensitive boundaries resolved at interaction checkpoint.

---

## References

- `mcp_server/managers/phase_state_engine.py` (L176, L223, L291, L349, L415, L527, L726, L745)
- `mcp_server/managers/workflow_state_mutator.py`
- `mcp_server/managers/quality_state_repository.py`
- `mcp_server/managers/state_repository.py`
- `docs/development/issue231/design.md` — `IWorkflowStateMutator` design intent
- `docs/mcp_server/architectural_diagrams/02_workflow_state_subsystem.md` — A-02 (stale, cycle_tools bypass already resolved)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-25 | Agent | Initial research — root cause confirmed, approved strategy captured |
| 1.1 | 2026-05-25 | Agent | QA NOGO fixes: blast radius count 9→8, test-migration split (fixture vs behaviour), quality_state callers and test surfaces added |
| 1.2 | 2026-05-25 | Agent | Amend Approved Strategy: explicit exception for `_load_state_or_reconstruct()` full-replacement lambda (error-recovery path, git-derived) |
