# Issue #355 — Validation: Fix _ConcurrentTestGateRunner + PSE dead-code removal

**Status:** PASS
**Version:** 1.0
**Last Updated:** 2026-05-26

---

## Validation Scope and Prerequisites

**Branch:** `bug/355-concurrent-test-gate-runner-interface-gap`
**Parent:** `epic/320-production-readiness-tracker`
**Cycle:** C1 — interface fix + PSE dead-code removal

**Prerequisites:**
- Research artifact: `docs/development/issue355/research.md`
- Planning artifact: `docs/development/issue355/planning.md`
- Approved Strategy: clean break (confirmed by user on 2026-05-26)
- Design phase: skipped (approved by user — research was design-complete)

---

## Summary Verdict

**PASS**

All four C1 deliverables are satisfied. The full test suite passes on all branch-scoped tests. Two pre-existing failures (`test_load_from_env`, `test_cli_version`) exist on the parent branch and are outside this issue's scope. Quality gates pass on all 8 changed files. One latent regression risk is disclosed below but is pre-existing and outside this issue's scope.

---

## Full-Suite Test Result

**Command:** `run_tests(scope='full')`
**Result:** 2830 passed, 11 skipped, 6 xfailed, 2 failed, 26 warnings

| Test | Status | Notes |
|---|---|---|
| All branch-scoped tests | ✅ PASS | |
| `tests/mcp_server/unit/config/test_settings.py::test_load_from_env` | ❌ pre-existing | Version mismatch `1.0.0` vs `3.0.0`; file not changed on this branch |
| `tests/mcp_server/unit/test_cli.py::test_cli_version` | ❌ pre-existing | Same version mismatch; file not changed on this branch |

**Pre-existing failure confirmation:** `git log origin/epic/320-production-readiness-tracker..HEAD -- tests/mcp_server/unit/config/test_settings.py tests/mcp_server/unit/test_cli.py` → empty (no changes on this branch).

---

## Branch Quality Gate Result

**Command:** `run_quality_gates(scope='files', files=[8 changed files])`
**Result:** 6/6 active gates passed (Gate 4: Types skipped — expected)

Changed files checked:
- `mcp_server/managers/phase_state_engine.py`
- `mcp_server/server.py`
- `tests/mcp_server/integration/test_phase_state_engine_concurrent.py`
- `tests/mcp_server/test_support.py`
- `tests/mcp_server/unit/managers/test_consumers_c4.py`
- `tests/mcp_server/unit/managers/test_phase_state_engine_c3.py`
- `tests/mcp_server/unit/test_c260_c2_state_root_injection.py`
- `tests/mcp_server/unit/tools/test_force_phase_transition_tool.py`

---

## Deliverable Mapping

### C1-D1: `_ConcurrentTestGateRunner` implements all four gate methods ✅

**Evidence:** `tests/mcp_server/integration/test_phase_state_engine_concurrent.py` class `_ConcurrentTestGateRunner` now contains:
- `enforce_phase_exit(workflow_name, phase, cycle_number=None) → GateReport()` — empty report
- `inspect_phase_exit(workflow_name, phase, cycle_number=None) → GateReport()` — empty report
- `enforce_cycle_exit(workflow_name, phase, cycle_number) → GateReport()` — empty report
- `inspect_cycle_exit(workflow_name, phase, cycle_number) → GateReport()` — empty report

Returns `GateReport()` (empty), not `GateReport(passing=("nop",))`. Old `enforce()` and `inspect()` stubs are removed.

### C1-D2: `_legacy_workphases_gate_summary` and `workphases_config` removed from PSE ✅

**Evidence:**
- `grep _legacy_workphases_gate_summary mcp_server/managers/phase_state_engine.py` → 0 matches
- `workphases_config` constructor parameter absent from `PhaseStateEngine.__init__`
- `self._workphases_config` field assignment absent
- Fallback if-block in `force_transition()` removed

### C1-D3: All four PSE construction sites updated ✅

| Site | File | `workphases_config=` |
|---|---|---|
| Production server | `mcp_server/server.py` | Absent |
| Test support | `tests/mcp_server/test_support.py` | Absent |
| Unit test (C4) | `tests/mcp_server/unit/managers/test_consumers_c4.py` | Absent |
| Unit test (state root) | `tests/mcp_server/unit/test_c260_c2_state_root_injection.py` | Absent |

### C1-D4: Both concurrent tests pass ✅

Both previously failing tests now pass:
- `TestPrimaryMixedConcurrentWritesC4::test_force_transition_and_force_cycle_transition_concurrent`
- `TestSecondaryHomogeneousConcurrentWritesC4::test_two_concurrent_force_transitions_both_records_present`

These tests are part of the 2830 that pass in the full-suite run.

---

## Corrected Behavior

**Before:** The two concurrent tests raised `AttributeError: '_ConcurrentTestGateRunner' object has no attribute 'inspect_phase_exit'` because the class still had the pre-#293 `enforce()`/`inspect()` stubs. The `GateReport(passing=("nop",))` workaround existed to prevent the thread-unsafe `_legacy_workphases_gate_summary` fallback from being entered.

**After:** `_ConcurrentTestGateRunner` implements the full `IWorkflowGateRunner` protocol. `_legacy_workphases_gate_summary` and its fallback block are removed from PSE, so returning `GateReport()` is safe — there is no longer a legacy code path that would be triggered by an empty gate report.

---

## Approved Strategy Alignment

**Approved Strategy:** Clean break (no backward-compatible bridge).

**Preserved constraints:**
- `IWorkflowGateRunner` interface definition unchanged
- `WorkphasesConfig` schema fields `get_exit_requires` / `get_entry_expects` retained (still used by `test_deliverable_checker.py` for schema-level verification — explicitly out of scope per planning)
- `ScopeDecoder` and other unrelated `workphases_config` consumers untouched

---

## Live Demonstration Proposal

**The old failure cannot be safely reproduced.** Reproducing it would require reverting `_ConcurrentTestGateRunner` to the broken state and re-adding `_legacy_workphases_gate_summary` to PSE — a destructive reversal.

**Closest observable proof:**

1. Open `tests/mcp_server/integration/test_phase_state_engine_concurrent.py`
2. Observe that `_ConcurrentTestGateRunner` has all four methods returning `GateReport()` (not `passing=("nop",)`)
3. Run the concurrent tests directly:
   ```
   pytest tests/mcp_server/integration/test_phase_state_engine_concurrent.py -v
   ```
   Both `test_force_transition_and_force_cycle_transition_concurrent` and `test_two_concurrent_force_transitions_both_records_present` pass.

4. Open `mcp_server/managers/phase_state_engine.py` and search for `_legacy_workphases_gate_summary` — no match. Search for `workphases_config` in `__init__` — no match.

---

## Residual Risks and Caveats

### Latent LSP gap in `test_phase_state_engine_c2.py` (pre-existing, out of scope)

`BlockingGateRunner` and `InspectingGateRunner` in `tests/mcp_server/unit/managers/test_phase_state_engine_c2.py` implement only `enforce_phase_exit` and `inspect_phase_exit`. Methods `enforce_cycle_exit` and `inspect_cycle_exit` are missing.

- **Current impact:** None — these runners are used only in phase-transition tests, not cycle-transition tests.
- **Future impact:** If a test in `test_phase_state_engine_c2.py` ever calls `force_cycle_transition()`, it will raise `AttributeError`.
- **Pre-existing:** This gap was not introduced by this branch; it predates issue #355.
- **Recommendation:** File a follow-up chore issue to complete these test fakes.

### No design artifact

Design phase was skipped by user approval (research was design-complete). There is no `design.md` to verify against. Planning document served as the design authority.
