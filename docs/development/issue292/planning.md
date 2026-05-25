<!-- docs\development\issue292\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-25T14:37Z updated= -->
# Fix concurrent state mutations - lost updates (#292)

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-25

---

## Purpose

Break down the approved design for issue #292 into implementation-sized TDD cycles that fix the lost-update race in WorkflowStateMutator callers and FileQualityStateRepository.

## Scope

**In Scope:**
phase_state_engine.py (8 caller rewrites, _apply_state() deletion), _save_state() deletion + Category A/B test migration, FileQualityStateRepository.apply() lock + QualityStateMutationConflictError, concurrent regression tests

**Out of Scope:**
BranchState schema changes, IWorkflowStateMutator interface changes, QAManager catch-block changes, cross-process or distributed locking

## Prerequisites

Read these first:
1. design.md v0.3 approved (QA GO)
2. research.md v1.2 approved (Approved Strategy complete)
3. Branch bug/292-concurrent-state-mutations-lost-updates active
4. Phase: planning (transition to implementation after this document is approved)
---

## Summary

Four TDD cycles to eliminate the stale-lambda pattern in all 8 PhaseStateEngine write paths, delete dead _save_state(), add threading.Lock to FileQualityStateRepository, and add concurrent regression tests.
---

## Approved Strategy Constraints

Implementation must observe these bindings from research.md v1.2 and design.md v0.3:

- **Boundary 1:** All 8 former `_apply_state()` call sites must pass a lambda that derives from `_s`. Six use `_s.with_updates(DELTA_FIELDS)`. Approved exception: `_load_state_or_reconstruct()` uses `lambda _s: reconstructed_state` where `reconstructed_state` comes from git history, not from a pre-lock read of `state.json`.
- **Boundary 2:** `FileQualityStateRepository.apply()` must acquire a `threading.Lock` (5s timeout) before the read-apply-write sequence. `QualityStateMutationConflictError` must be defined in `quality_state_repository.py` (no cross-import from `workflow_state_mutator.py`).
- **Boundary 3:** `_save_state()` is dead code — delete it, migrate Category A, delete Category B.
- **No schema changes:** `BranchState`, `IWorkflowStateMutator`, `IQualityStateRepository` signatures unchanged.
- **No QAManager changes:** propagation path (raises → no catch → tool layer RecoveryNote) requires no QAManager edits.

---

## Dependencies

- C2 depends on C1 (`_save_state()` deletion safe only after all production callers use inline transformer paths)
- C4 depends on C1 (concurrent regression tests require transformer lambdas in production)
- C3 is independent (execute sequentially to avoid conflicts)
- Recommended execution order: C1 → C2 → C3 → C4

---

## TDD Cycles


### Cycle 1: C1 — PSE transformer lambda migration

**Goal:** Rewrite all 8 `_apply_state()` callers in `PhaseStateEngine` to use inline transformer lambdas and delete `_apply_state()`.

**Production files:**
- `mcp_server/managers/phase_state_engine.py` — 8 caller rewrites, `_apply_state()` deleted

**Tests:**
- `tests/mcp_server/unit/managers/test_phase_state_engine.py` — existing behavioral tests for all 8 methods must remain green
- Mock assertions on `_workflow_state_mutator.apply()` updated to reflect inline lambda shape

**Success Criteria:**
- `_apply_state()` deleted from `phase_state_engine.py`
- All 8 former callers call `_workflow_state_mutator.apply()` directly with correct lambda (delta or approved exception)
- Existing PSE unit tests pass
- mypy + ruff clean on `phase_state_engine.py`
- Quality gates green


### Cycle 2: C2 — `_save_state()` removal and test migration

**Goal:** Delete `_save_state()` from `PhaseStateEngine`, migrate 9 Category A fixture sites, delete 2 Category B behaviour tests.

**Production files:**
- `mcp_server/managers/phase_state_engine.py` — `_save_state()` deleted

**Tests:**
- 9 Category A sites migrated to inject state via injected `IStateRepository`:
  - `tests/mcp_server/unit/tools/test_cycle_tools_legacy.py` (7 sites)
  - `tests/mcp_server/unit/tools/test_discovery_tools.py` (2 sites)
- 2 Category B sites deleted:
  - `tests/mcp_server/managers/test_phase_state_engine_async.py` (L63, L106)

**Success Criteria:**
- `_save_state()` deleted from `phase_state_engine.py`
- All 9 Category A sites inject state via `IStateRepository`
- 2 Category B tests deleted
- Full test suite passes
- mypy + ruff clean on changed test files
- Quality gates green

**Dependencies:** C1 complete


### Cycle 3: C3 — `FileQualityStateRepository` lock

**Goal:** Add `threading.Lock` (5s timeout) to `FileQualityStateRepository.apply()` and introduce `QualityStateMutationConflictError`.

**Production files:**
- `mcp_server/managers/quality_state_repository.py` — lock + `QualityStateMutationConflictError` added

**Tests:**
- `tests/mcp_server/unit/managers/test_quality_state_repository.py`:
  - New: lock-contention test — two concurrent `apply()` calls, assert both writes land (no lost update)
  - New: timeout test — lock held >5s, assert `QualityStateMutationConflictError` raised
  - Existing tests stay green

**Success Criteria:**
- `FileQualityStateRepository.apply()` acquires lock before read-apply-write
- `QualityStateMutationConflictError` raised on 5s timeout
- `IQualityStateRepository` protocol unchanged
- `QAManager` callers propagate exception unchanged
- mypy + ruff clean on `quality_state_repository.py`
- Quality gates green


### Cycle 4: C4 — Concurrent regression tests

**Goal:** Prove the Boundary 1 fix with `threading.Barrier`-synchronized concurrent calls covering the filed bug scenario and homogeneous writers.

**Production files:** None (test-only cycle)

**Tests:**
- Primary proof: `force_transition()` + `force_cycle_transition()` concurrent on same branch via `threading.Barrier` — assert neither mutation lost
- Secondary proof: two concurrent `force_transition()` calls on same branch — assert both transition records present in final state
- New test file: `tests/mcp_server/integration/test_phase_state_engine_concurrent.py` (or equivalent integration location)

**Success Criteria:**
- Primary concurrent regression test passes (mixed phase/cycle writers)
- Secondary concurrent regression test passes (homogeneous writers)
- Full test suite passes
- Quality gates green

**Dependencies:** C1 complete (transformer lambdas in place)

## Related Documentation
- **[docs/development/issue292/research.md][related-1]**
- **[docs/development/issue292/design.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/development/issue292/research.md
[related-2]: docs/development/issue292/design.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-25 | Agent | Initial planning document |
