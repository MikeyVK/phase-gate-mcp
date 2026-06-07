<!-- docs\development\issue355\planning.md -->
<!-- template=planning version=planning created=2026-05-26 updated=2026-05-26 -->
# Issue #355 — Planning: fix _ConcurrentTestGateRunner interface gap + remove dead PSE legacy fallback

**Status:** DRAFT
**Version:** 1.0
**Last Updated:** 2026-05-26

---

## Purpose

Define the implementation cycle structure for issue #355: fix the interface gap in `_ConcurrentTestGateRunner` and remove `_legacy_workphases_gate_summary` dead code from `PhaseStateEngine`.

## Scope

**In Scope:**
`tests/mcp_server/integration/test_phase_state_engine_concurrent.py` — `_ConcurrentTestGateRunner` interface update;
`mcp_server/managers/phase_state_engine.py` — remove `_legacy_workphases_gate_summary`, fallback block, `workphases_config` field + constructor param;
`mcp_server/server.py`, `tests/mcp_server/test_support.py`, `tests/mcp_server/unit/managers/test_consumers_c4.py`, `tests/mcp_server/unit/test_c260_c2_state_root_injection.py` — remove `workphases_config` kwarg from PSE construction.

**Out of Scope:**
`WorkphasesConfig` schema fields `get_exit_requires` / `get_entry_expects` (retained for schema-level test coverage). `ScopeDecoder`, `GitManager` injections of `workphases_config` (unrelated paths). `IWorkflowGateRunner` interface definition (correct, no changes).

## Prerequisites

- Research artifact: [docs/development/issue355/research.md](research.md)
- Approved Strategy: clean break (confirmed by user on 2026-05-26)
- Design phase: skipped (approved by user on 2026-05-26 — research is design-complete)

## Summary

Fix the interface gap in `_ConcurrentTestGateRunner` (GREEN) and remove the dead `_legacy_workphases_gate_summary` + `workphases_config` constructor parameter from `PhaseStateEngine` (REFACTOR). One TDD cycle. RED state is the existing two failing tests.

---

## TDD Cycles

### Cycle 1 — C1: interface fix + PSE dead-code removal

**RED (existing):**
Two tests fail with `AttributeError: '_ConcurrentTestGateRunner' object has no attribute 'inspect_phase_exit'`:
- `TestPrimaryMixedConcurrentWritesC4::test_force_transition_and_force_cycle_transition_concurrent`
- `TestSecondaryHomogeneousConcurrentWritesC4::test_two_concurrent_force_transitions_both_records_present`

No new test must be written — the failing tests are the RED proof.

**GREEN:**
Fix `_ConcurrentTestGateRunner` in `test_phase_state_engine_concurrent.py`:
- Add `enforce_phase_exit(workflow_name, phase, cycle_number=None) → GateReport`
- Add `inspect_phase_exit(workflow_name, phase, cycle_number=None) → GateReport`
- Add `enforce_cycle_exit(workflow_name, phase, cycle_number) → GateReport`
- Add `inspect_cycle_exit(workflow_name, phase, cycle_number) → GateReport`
- All four gate methods return `GateReport(passing=("nop",))` temporarily (preserves thread-safety: prevents legacy fallback from entering the thread-unsafe `project_manager.get_project_plan()` call while `_legacy_workphases_gate_summary` still exists in PSE)
- Remove old `enforce()` and `inspect()` stubs
- `is_cycle_based_phase` is retained unchanged

No production files are changed in GREEN.

**REFACTOR:**
Dead-code removal and caller cleanup — no behavioral change, all tests remain green:

1. `mcp_server/managers/phase_state_engine.py`:
   - Remove `_legacy_workphases_gate_summary()` method entirely (~30 lines)
   - Remove the legacy fallback block in `force_transition()`: the `if not skipped_gates and not passing_gates:` block and its body (~10 lines)
   - Remove `self._workphases_config = workphases_config` from `__init__`
   - Remove `workphases_config: WorkphasesConfig` from `__init__` parameter list
   - Remove `WorkphasesConfig` import if no other usage remains

2. All four PSE construction sites — must be updated atomically with step 1 (removing the param and all callers in the same commit prevents `TypeError: unexpected keyword argument`):
   - `mcp_server/server.py` line 257: remove `workphases_config=workphases_config` kwarg
   - `tests/mcp_server/test_support.py` (~line 372): remove `workphases_config=workphases_config` kwarg from `make_phase_state_engine`
   - `tests/mcp_server/unit/managers/test_consumers_c4.py` (~lines 94, 107): remove `workphases_config = MagicMock(spec=WorkphasesConfig)` setup variable and the kwarg; remove `WorkphasesConfig` import if unused
   - `tests/mcp_server/unit/test_c260_c2_state_root_injection.py` (~lines 93, 443): remove `workphases_config=MagicMock()` kwarg from both PSE construction calls

3. `tests/mcp_server/integration/test_phase_state_engine_concurrent.py`:
   - Switch all four gate methods from `GateReport(passing=("nop",))` to `GateReport()`
   - Update the class docstring to remove the legacy fallback mention

**Exit Criteria:**
- Both concurrent tests pass
- `_legacy_workphases_gate_summary` is absent from `phase_state_engine.py`
- `workphases_config` parameter is absent from `PhaseStateEngine.__init__`
- `_ConcurrentTestGateRunner` gate methods return `GateReport()` not `GateReport(passing=("nop",))`
- Quality gates pass on all changed files (pylint 10/10, pyright type-check pass)

**Deliverables:**

| ID | Description |
|---|---|
| C1-D1 | `_ConcurrentTestGateRunner` implements `enforce_phase_exit`, `inspect_phase_exit`, `enforce_cycle_exit`, `inspect_cycle_exit` returning `GateReport()` (final state after REFACTOR) |
| C1-D2 | `_legacy_workphases_gate_summary` method and legacy fallback `if`-block removed from `phase_state_engine.py`; `workphases_config` field and constructor parameter removed |
| C1-D3 | All four `PhaseStateEngine` construction sites updated: `server.py`, `test_support.py`, `test_consumers_c4.py`, `test_c260_c2_state_root_injection.py` |
| C1-D4 | Both previously failing concurrent tests pass without `GateReport(passing=("nop",))` workaround |

---

## Approved Strategy Execution

| Constraint | Implementation consequence |
|---|---|
| Clean break — no `workphases_config` optional param | PSE constructor parameter removed entirely; no default value |
| `GateReport()` not `GateReport(passing=("nop",))` in final state | Temporary `GateReport(passing=("nop",))` in GREEN; changed to `GateReport()` in REFACTOR after legacy fallback is removed |
| `WorkphasesConfig` schema out of scope | Schema methods `get_exit_requires` / `get_entry_expects` retained; only PSE's usage is removed |
| Atomicity of PSE param + callers | REFACTOR PSE param removal and all caller updates committed together |

---

## Typing Obligations

| File | Change |
|---|---|
| `phase_state_engine.py` | `WorkphasesConfig` import becomes unused → remove |
| `test_consumers_c4.py` | `WorkphasesConfig` import (`from mcp_server.config.schemas.workphases import WorkphasesConfig`) → remove if no other use in file |
| `test_support.py` | `WorkphasesConfig` import → remove from `make_phase_state_engine` factory if unused elsewhere in file |

All changed files must pass pyright type-check with no new errors or ignores.

---

## Quality Gate Obligations

Run quality gates on all changed files after each sub-phase commit (GREEN and REFACTOR). Changed files:
- GREEN: `tests/mcp_server/integration/test_phase_state_engine_concurrent.py`
- REFACTOR: `mcp_server/managers/phase_state_engine.py`, `mcp_server/server.py`, `tests/mcp_server/test_support.py`, `tests/mcp_server/unit/managers/test_consumers_c4.py`, `tests/mcp_server/unit/test_c260_c2_state_root_injection.py`, `tests/mcp_server/integration/test_phase_state_engine_concurrent.py`

---

## Regression Obligations

- Run full integration test suite for `test_phase_state_engine_concurrent.py` after GREEN and after REFACTOR
- Run unit tests for `test_consumers_c4.py` and `test_c260_c2_state_root_injection.py` after REFACTOR
- Run full test suite before requesting QA review

No behavioral change is expected. Regression surface is limited to PSE callers that pass `workphases_config`.

---

## Risks

| Risk | Mitigation |
|---|---|
| A hidden PSE construction site not in the blast-radius list | `grep_search` for `PhaseStateEngine(` and `workphases_config=` before committing REFACTOR |
| `WorkphasesConfig` import still needed elsewhere in `phase_state_engine.py` | Verify with `grep_search` before removing import |
| Intermediate broken state if PSE param removed before callers updated | Commit PSE param removal + all caller updates atomically in one REFACTOR commit |

---

## Related Documents

- [research.md](research.md)
