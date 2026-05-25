<!-- docs\development\issue293\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-25T09:08Z updated= -->
# Issue #293 — Cycle Boundary Semantics: Boundary-Explicit Gate Runner API

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-25

---

## Purpose

Define the TDD cycle breakdown for implementation of issue #293. Maps design decisions to two sequential cycles with explicit entry conditions, deliverables, and exit criteria.

## Scope

**In Scope:**
mcp_server/managers/phase_contract_resolver.py, mcp_server/core/interfaces/__init__.py, mcp_server/managers/workflow_gate_runner.py, mcp_server/managers/phase_state_engine.py, and all 8 test files containing fakes or direct calls to the old enforce/inspect/resolve API.

**Out of Scope:**
deliverables.json routing logic (_resolve_issue_checks), integration tests, acceptance tests, test_cycle_tools.py (uses real runner — updated automatically by C2 production changes), any unrelated refactoring.

## Prerequisites

Read these first:
1. design.md v1.0 approved (QA PASS)
2. Branch bug/293-cycle-transitions-wrong-phase-exit-gates active
3. Phase: planning (will transition to implementation after this document is approved)
---

## Summary

Replace the single generic resolve/enforce/inspect API with two boundary-explicit method pairs (resolve_phase_exit/resolve_cycle_exit and enforce/inspect_phase_exit/cycle_exit) to fix incorrect phase-exit gate enforcement during cycle transitions.

---

## TDD Cycles


### Cycle 1: C1: Resolver boundary methods

**Goal:** Add resolve_phase_exit() and resolve_cycle_exit() to PhaseContractResolver; update test_phase_contract_resolver.py to cover both new methods. Keep resolve() temporarily until C2 removes it.

**Tests:**
- test_resolve_phase_exit_returns_exit_requires_plus_cycle_gates_when_cycle_number_present
- test_resolve_phase_exit_returns_only_exit_requires_when_no_cycle_number
- test_resolve_cycle_exit_returns_only_cycle_exit_requires
- test_resolve_cycle_exit_excludes_phase_level_exit_requires (defect regression test)

**Success Criteria:**
- resolve_phase_exit and resolve_cycle_exit implemented on PhaseContractResolver
- All new resolver tests pass
- All existing resolver tests still pass (resolve() still present)
- Type signatures: `resolve_phase_exit(cycle_number: int | None = None)` vs `resolve_cycle_exit(cycle_number: int)` — pyright must accept both without ignores
- ruff + pyright pass on phase_contract_resolver.py and test_phase_contract_resolver.py



### Cycle 2: C2: Full migration — interface, runner, engine, all test fakes

**Goal:** Remove resolve()/enforce()/inspect() from all production classes and all test fakes; add 4 boundary-explicit methods + _run_resolved_checks to WorkflowGateRunner; update PhaseStateEngine 4 call sites; update all 8 test files.

**TDD sequence:**
1. RED: Update all fakes (and IWorkflowGateRunner) to the new interface — remove enforce/inspect, add 4 new methods. Remove resolve() from PhaseContractResolver. All phase_state_engine tests now fail (engine calls enforce() on fakes that no longer have it). This is the intended failing signal.
2. GREEN: Wire up the engine (4 call sites), implement WorkflowGateRunner (4 methods + _run_resolved_checks, remove old methods), update all remaining test call sites.
3. REFACTOR: Quality gates on all changed files.

**Tests:**
- All test_phase_state_engine_c1.py tests (FakeGateRunner updated; direct runner calls at L154/155/169/203 become enforce_cycle_exit/inspect_cycle_exit)
- All test_phase_state_engine_c2.py tests (BlockingGateRunner + InspectingGateRunner updated to enforce_phase_exit/inspect_phase_exit)
- All test_phase_state_engine_c3_issue257.py tests (PassingGateRunner + ReportingGateRunner updated)
- All test_phase_state_engine_c4_issue257.py tests (BlockingCycleGateRunner + ReportingCycleGateRunner + ConfigAwareCycleGateRunner updated to enforce_cycle_exit/inspect_cycle_exit)
- test_consumers_c4.py MagicMock patched to enforce_phase_exit
- test_phase_contract_resolver.py: remove test_resolve_merges_issue_specific_checks_without_overriding_required_gates; keep split tests from C1
- test_phase_contract_resolver_c3.py L94: resolver.resolve(…) → resolver.resolve_phase_exit(…)
- test_support.py shared fake: enforce → enforce_phase_exit, inspect → inspect_phase_exit

**Success Criteria:**
- Bug fixed: transition_cycle() enforces only cycle_exit_requires[N], not exit_requires
- Bug fixed: transition() enforces exit_requires + cycle_exit_requires[current_cycle]
- All phase_state_engine tests pass with updated fakes
- No resolve()/enforce()/inspect() references remain in production code
- IWorkflowGateRunner has only 4 boundary-explicit methods + is_cycle_based_phase
- Type signatures: enforce_phase_exit/inspect_phase_exit accept `cycle_number: int | None`; enforce_cycle_exit/inspect_cycle_exit require `cycle_number: int` — pyright clean without ignores
- ruff + pyright pass on all 4 production files and all 8 test files
- Full test suite green

**Dependencies:** C1 complete: resolve_phase_exit + resolve_cycle_exit available on PhaseContractResolver

---

## Risks & Mitigation

- **Risk:** C2 RED has large blast radius: all phase_state_engine tests fail simultaneously when fakes are updated to new interface before the engine is wired up.
  - **Mitigation:** Expected and controlled — failing tests in C2 RED are the intended signal. Proceed to GREEN promptly without partial fixes.
- **Risk:** _resolve_issue_checks routing for resolve_phase_exit: research suggested phase-scoped deliverables, but design defers this intentionally.
  - **Mitigation:** Do not change _resolve_issue_checks routing. Design §4.1 deferral note is binding. If tempted to change it, stop and raise a blocker.

## Related Documentation
- **[docs/development/issue293/research.md][related-1]**
- **[docs/development/issue293/design.md][related-2]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-3]**
- **[mcp_server/managers/phase_contract_resolver.py][related-4]**
- **[mcp_server/core/interfaces/__init__.py][related-5]**
- **[mcp_server/managers/workflow_gate_runner.py][related-6]**
- **[mcp_server/managers/phase_state_engine.py][related-7]**

<!-- Link definitions -->

[related-1]: docs/development/issue293/research.md
[related-2]: docs/development/issue293/design.md
[related-3]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-4]: mcp_server/managers/phase_contract_resolver.py
[related-5]: mcp_server/core/interfaces/__init__.py
[related-6]: mcp_server/managers/workflow_gate_runner.py
[related-7]: mcp_server/managers/phase_state_engine.py

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |