<!-- docs\development\issue371\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-06T18:29Z updated= -->
# Replace remaining direct state.json reads with IStateReader (#371)

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-06-06

---

## Purpose

Wire IStateReader into the three production modules that currently bypass it, remove dead code produced by the cleanup, and update the composition root.

## Scope

**In Scope:**
mcp_server/managers/enforcement_runner.py (2 raw read sites + _read_current_phase deletion), mcp_server/core/phase_detection.py (ScopeDecoder constructor change), mcp_server/tools/cycle_tools.py (comment annotation only for fallback sites), mcp_server/server.py (composition root wiring updates), affected test files.

**Out of Scope:**
IStateReader / IStateRepository interface changes. IStateRepository write paths. WorkflowStateMutator. QAManager. cycle_tools raw fallback reads (retained per Approved Strategy Option A).

## Prerequisites

Read these first:
1. research.md Approved Strategy captured (done)
2. Branch initialized (done)
---

## Summary

Two implementation cycles: C1 injects IStateReader into EnforcementRunner and ScopeDecoder and removes dead code; C2 annotates the cycle_tools documented exception and removes any dead code produced there. Both cycles update server.py wiring and affected tests.

---

## TDD Cycles


### Cycle 1: C1: enforcement_runner.py + phase_detection.py IStateReader injection

**Goal:** Inject IStateReader into EnforcementRunner and ScopeDecoder. Remove dead code (_read_current_phase module function, state_path constructor param from ScopeDecoder). Update server.py wiring. All enforcement and phase-detection paths now read state via IStateReader.

**Tests:**

**Success Criteria:**
- EnforcementRunner.__init__ accepts state_reader: IStateReader; raw json.loads calls on lines 39 and 391 replaced by state_reader.load(branch) field access
- _read_current_phase module-level function deleted
- ScopeDecoder.__init__ accepts state_reader: IStateReader + branch: str; state_path constructor param removed
- _read_state_json reads via state_reader.load(branch).current_phase with FileNotFoundError catch
- server.py passes self._state_repository (or BranchValidatedStateReader) and active branch to both ScopeDecoder instantiations
- server.py passes state_reader to EnforcementRunner
- All tests for enforcement_runner and phase_detection green
- run_quality_gates on changed files: lint + pyright pass



### Cycle 2: C2: cycle_tools.py dead-code cleanup + documented exception annotation

**Goal:** Annotate the two cycle_tools raw fallback reads with the documented-exception comment per Approved Strategy. Remove any variables or parameters rendered dead by the broader refactor in this file. Update server.py wiring for cycle tools if needed.

**Tests:**

**Success Criteria:**
- Both _get_current_branch fallback blocks carry # NOTE: IStateReader requires known branch; raw fallback retained intentionally
- No unused imports, variables, or constructor parameters remain in cycle_tools.py after the broader cleanup
- server.py cycle_tools wiring consistent with C1 changes
- All cycle_tools tests green
- run_quality_gates on changed files: lint + pyright pass

**Dependencies:** C1

---

## Risks & Mitigation

- **Risk:** ScopeDecoder constructor change breaks all tests that instantiate it directly with state_path
  - **Mitigation:** Search test suite for ScopeDecoder(...) instantiation; update call sites in RED before GREEN
- **Risk:** EnforcementRunner constructor change requires server.py and all test fixtures to be updated
  - **Mitigation:** Identify all instantiation sites in tests before editing production code
- **Risk:** cycle_tools fallback retained as raw read — must be clearly commented to avoid future confusion
  - **Mitigation:** Add explicit NOTE comment per Approved Strategy

---

## Milestones

- C1 GREEN: enforcement_runner.py + phase_detection.py + server.py wiring green
- C2 GREEN: cycle_tools.py cleanup + server.py wiring green
- Full suite green + branch quality gates pass

## Related Documentation
- **[docs/development/issue371/research.md][related-1]**
- **[docs/development/issue230/research.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/development/issue371/research.md
[related-2]: docs/development/issue230/research.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-06 | Agent | Initial draft |