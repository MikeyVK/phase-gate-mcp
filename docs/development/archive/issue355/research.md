<!-- docs\development\issue355\research.md -->
<!-- template=research version=research created=2026-05-26 updated=2026-05-26 -->
# Issue #355 — Fix _ConcurrentTestGateRunner: missing IWorkflowGateRunner methods + remove dead PSE legacy fallback

**Status:** DRAFT
**Version:** 1.0
**Last Updated:** 2026-05-26

---

## Purpose

Establish the root cause, affected surface, and Approved Strategy for two failing concurrent integration tests caused by a stale test fake and unremoved dead production code.

## Scope

**In Scope:**
`tests/mcp_server/integration/test_phase_state_engine_concurrent.py` (`_ConcurrentTestGateRunner`); `mcp_server/managers/phase_state_engine.py` (`_legacy_workphases_gate_summary`, `_workphases_config` constructor parameter); all direct callers of `PhaseStateEngine.__init__` that pass `workphases_config`.

**Out of Scope:**
`WorkphasesConfig` schema fields `get_exit_requires` / `get_entry_expects` (still used by `test_deliverable_checker.py` for schema-level verification; schema cleanup is a separate concern). `ScopeDecoder` injection of `workphases_config` (unrelated path). `IWorkflowGateRunner` interface definition (correct; no changes needed). Any other test fakes — all were updated in #293 C2-GREEN.

## Prerequisites

1. Issue #293 C2-GREEN closed: `IWorkflowGateRunner` replaced `enforce()`/`inspect()` with four boundary-explicit methods.
2. Issue #270 closed: `exit_requires` and `entry_expects` removed from `workphases.yaml` (YAML-only; PSE code changes deferred to #271).
3. Issue #271 closed: focused on `phase_contracts.yaml` SSOT and fixture migration; did not remove `_legacy_workphases_gate_summary` from PSE.

---

## Problem Statement

Two concurrent integration tests fail with `AttributeError: '_ConcurrentTestGateRunner' object has no attribute 'inspect_phase_exit'`. The immediate cause is a missing interface update. The deeper cause is that `_legacy_workphases_gate_summary` in `PhaseStateEngine` is dead code that was never cleaned up, and `_ConcurrentTestGateRunner` was designed to work around it rather than test real behavior.

## Research Goals

- Confirm the exact interface divergence between `_ConcurrentTestGateRunner` and `IWorkflowGateRunner`.
- Confirm that `_legacy_workphases_gate_summary` is dead code and why the `passing=("nop",)` workaround existed.
- Map the full blast radius of removing `_legacy_workphases_gate_summary` and the `workphases_config` constructor parameter from `PhaseStateEngine`.
- Establish an Approved Strategy for the fix scope.

---

## Background

### Timeline of relevant changes

| Issue | Change | Relevant result |
|---|---|---|
| #257 (closed) | `phase_contracts.yaml` became SSOT for exit gates via `WorkflowGateRunner` | `_legacy_workphases_gate_summary` explicitly named "legacy" — permanently bypassed in normal execution |
| #270 (closed) | Removed `exit_requires` and `entry_expects` from `workphases.yaml` (YAML-only) | `get_exit_requires()` and `get_entry_expects()` now always return `[]`; PSE code changes deferred to #271 |
| #271 (closed) | Made `phase_contracts.yaml` SSOT for workflow-phase membership; migrated fixture filenames | Did **not** remove `_legacy_workphases_gate_summary` from PSE |
| #292 C4-GREEN | `_ConcurrentTestGateRunner` created in `test_phase_state_engine_concurrent.py` | Created with old `enforce()`/`inspect()` stubs; deliberately returned `passing=("nop",)` to bypass legacy fallback |
| #293 C2-GREEN | `IWorkflowGateRunner` replaced `enforce()`/`inspect()` with four boundary-explicit methods | Updated production engine, `WorkflowGateRunner`, and `_NopGateRunner` in `test_support.py`; integration test file was out of scope |

### The legacy fallback activation condition

`force_transition()` in `phase_state_engine.py` calls `inspect_phase_exit()` and then checks:

```
if not skipped_gates and not passing_gates:
    skipped_gates, passing_gates = self._legacy_workphases_gate_summary(...)
```

The fallback is only entered when both passing and blocking gate lists are empty. Before #257 this could happen for phases without `phase_contracts.yaml` entries. After #257 it became permanently unreachable in production because all workflows have contract entries. After #270 it is also unreachable by data: `get_exit_requires()` and `get_entry_expects()` always return `[]`, so the method produces `([], [])` regardless of input.

The `passing=("nop",)` convention in `_ConcurrentTestGateRunner` existed specifically to prevent the fallback from being entered in concurrent tests, because `_legacy_workphases_gate_summary` calls `self.project_manager.get_project_plan(issue_number)` — a gitpython-backed call that is not thread-safe.

---

## Findings

### Finding 1 — Interface gap in `_ConcurrentTestGateRunner`

`_ConcurrentTestGateRunner` (`test_phase_state_engine_concurrent.py`) implements:
- `is_cycle_based_phase(workflow_name, phase)` — correct, delegates to `ContractsConfig`
- `enforce(workflow_name, phase, cycle_number, checks)` — old method, no longer in `IWorkflowGateRunner`
- `inspect(workflow_name, phase, cycle_number, checks)` — old method, no longer in `IWorkflowGateRunner`

`IWorkflowGateRunner` (`mcp_server/core/interfaces/__init__.py`) currently requires:
- `enforce_phase_exit(workflow_name, phase, cycle_number=None) → GateReport`
- `inspect_phase_exit(workflow_name, phase, cycle_number=None) → GateReport`
- `enforce_cycle_exit(workflow_name, phase, cycle_number) → GateReport`
- `inspect_cycle_exit(workflow_name, phase, cycle_number) → GateReport`
- `is_cycle_based_phase(workflow_name, phase) → bool`

**Failure path:** `force_transition()` in `phase_state_engine.py` calls `self._workflow_gate_runner.inspect_phase_exit(...)` (line 247). `_ConcurrentTestGateRunner` has no such method → `AttributeError`.

**Second failure path:** `force_cycle_transition()` calls `runner.inspect_cycle_exit(...)`. Thread B in `test_force_transition_and_force_cycle_transition_concurrent` calls `force_cycle_transition()` — also absent from `_ConcurrentTestGateRunner`.

Both failing tests:
- `TestPrimaryMixedConcurrentWritesC4::test_force_transition_and_force_cycle_transition_concurrent`
- `TestSecondaryHomogeneousConcurrentWritesC4::test_two_concurrent_force_transitions_both_records_present`

### Finding 2 — `_legacy_workphases_gate_summary` is dead code (doubly)

**Dead by YAML:** Issue #270 removed `exit_requires` and `entry_expects` from `workphases.yaml`. After this, `WorkphasesConfig.get_exit_requires(phase)` and `get_entry_expects(phase)` always return `[]`. The loops in `_legacy_workphases_gate_summary` never iterate. Return value is always `([], [])`.

**Dead by activation condition:** The fallback is only entered when both `skipped_gates` and `passing_gates` are empty after `inspect_phase_exit()`. This never occurs in production because all workflows have `phase_contracts.yaml` entries that produce non-empty reports.

**Retained thread-unsafe call:** `_legacy_workphases_gate_summary` still calls `self.project_manager.get_project_plan(issue_number)` before the empty loops. Even though the return value is always `([], [])`, this gitpython-backed call is made every time the fallback is entered — which in concurrent tests (using properly injected fakes that returned empty `GateReport()`) would trigger thread-unsafe gitpython access.

**Sole remaining use of `_workphases_config` in PSE:** `_workphases_config` is set in PSE's `__init__` and accessed only in `_legacy_workphases_gate_summary`. It is not used by any other PSE method.

### Finding 3 — Blast radius for removing `_workphases_config` from PSE

Removing `_legacy_workphases_gate_summary` makes `_workphases_config` an unused field in PSE, which in turn makes the `workphases_config` constructor parameter dead.

| File | Change required |
|---|---|
| `mcp_server/managers/phase_state_engine.py` | Remove `workphases_config` param, `self._workphases_config` assignment, `_legacy_workphases_gate_summary()` method, and the fallback if-block in `force_transition()` |
| `mcp_server/server.py` | Remove `workphases_config=workphases_config` kwarg from PSE construction (line 257) |
| `tests/mcp_server/test_support.py` | Remove `workphases_config=workphases_config` from `make_phase_state_engine` factory (line ~372) |
| `tests/mcp_server/unit/managers/test_consumers_c4.py` | Remove `workphases_config=MagicMock(spec=WorkphasesConfig)` setup and kwarg from PSE constructor (lines ~94, ~105) |
| `tests/mcp_server/unit/test_c260_c2_state_root_injection.py` | Remove `workphases_config=MagicMock()` kwarg from PSE constructor (lines ~93, ~439) |
| `tests/mcp_server/integration/test_phase_state_engine_concurrent.py` | Replace `enforce()`/`inspect()` with four current interface methods; `passing=("nop",)` workaround no longer needed |

No test directly tests `_legacy_workphases_gate_summary` behavior. The only test reference is a docstring comment in `_ConcurrentTestGateRunner` explaining the workaround.

### Finding 4 — Reference implementation

`_NopGateRunner` in `tests/mcp_server/test_support.py` is the authoritative reference for a minimal compliant test fake. It implements all four boundary-explicit methods plus `is_cycle_based_phase`, returning `GateReport()` from each gate method.

After removing the legacy fallback, `_ConcurrentTestGateRunner` can use the same pattern — `GateReport()` (empty) — without needing `passing=("nop",)`.

---

## Architectural Constraints

| Constraint | Source |
|---|---|
| No `if phase_name == "..."` dispatch in production code | `ARCHITECTURE_PRINCIPLES.md` §OCP |
| Constructor injection — no manager creation inside `execute()` | `ARCHITECTURE_PRINCIPLES.md` §DIP |
| Test fakes must satisfy the current interface contract, not a historical one | `ARCHITECTURE_PRINCIPLES.md` §ISP — consumer must use narrowest applicable interface |
| No backward-compat bridge or optional parameter to preserve old behavior | Issue #293 design.md — "retaining stubs would introduce ambiguity" |
| Dead code must be removed, not worked around | `ARCHITECTURE_PRINCIPLES.md` §YAGNI §9 |

---

## Corrected Behavior

After the fix:
- `_ConcurrentTestGateRunner` satisfies the current `IWorkflowGateRunner` protocol: four boundary-explicit methods + `is_cycle_based_phase`.
- `force_transition()` in PSE has no legacy fallback branch; it uses only the gate report from `inspect_phase_exit()`.
- `PhaseStateEngine.__init__` does not accept or store `workphases_config` — the parameter is gone.
- Both failing concurrent tests pass.
- No test relies on the `passing=("nop",)` bypass pattern.

---

## Approved Strategy

**Boundary / consumer scope:**
- `PhaseStateEngine` (production): remove `_legacy_workphases_gate_summary`, `_workphases_config` field, and `workphases_config` constructor parameter.
- `_ConcurrentTestGateRunner` (test-infra): update to current `IWorkflowGateRunner` interface; return `GateReport()` from all gate methods.
- All direct `PhaseStateEngine` construction sites: remove `workphases_config` kwarg.

**Selected strategy:** Clean break — remove dead code from production, correct test-infra interface. No optional parameter, no backward-compat bridge, no temporary stub.

**Supported contract vs defect dependence:**
- No external consumer relies on the legacy fallback — it was permanently bypassed since #257.
- The `passing=("nop",)` pattern in `_ConcurrentTestGateRunner` was a workaround for dead production code, not a supported contract. It must not be preserved.

**Constraints for later phases:**
- Design and planning must not introduce an optional `workphases_config` parameter or default value to PSE.
- `_ConcurrentTestGateRunner` gate methods must return `GateReport()` (empty), not `GateReport(passing=("nop",))`.
- `WorkphasesConfig.get_exit_requires()` and `get_entry_expects()` are out of scope — they remain for schema-level test coverage (`test_deliverable_checker.py`).

---

## Open Questions

None. The fix scope, affected boundaries, and strategy are fully determined by code evidence and the Approved Strategy above.

---

## Assumptions

- `WorkphasesConfig` schema fields `exit_requires` / `entry_expects` are out of scope for this fix. They are tested at schema level in `test_deliverable_checker.py` and retained there.
- `ScopeDecoder` receives `workphases_config` for subphase whitelist enforcement — unrelated to PSE's dead field. Not in scope.

---

## Regression Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A caller of PSE passes `workphases_config` as positional arg | Low — all callers use keyword args | Static analysis (pyright) catches missing/extra params immediately |
| `force_transition()` audit payload changes (empty gate lists instead of legacy summary) | Low — legacy always returned `([], [])` anyway | No behavior change; audit payload was already semantically empty |
| Concurrent test false positive after fix | Low — concurrent logic tested via `threading.Barrier`; gate stub behavior is incidental | Both test assertions check `state.transitions` / `state.cycle_history` counts, not gate behavior |
