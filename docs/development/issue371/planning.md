<!-- docs\development\issue371\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-06T18:29Z updated= -->
# Replace remaining direct state.json reads with IStateReader (#371)

**Status:** APPROVED  
**Version:** 1.1  
**Last Updated:** 2026-06-06

---

## Purpose

Wire IStateReader into the three production modules that currently bypass it, remove dead code produced by the cleanup, and update the composition root.

## Scope

**In Scope:**
mcp_server/managers/enforcement_runner.py (2 raw read sites + _read_current_phase deletion), mcp_server/core/phase_detection.py (ScopeDecoder dead-code elimination: state_path + _read_state_json + fallback_to_state removed), mcp_server/managers/state_repository.py (branch-inject fallback removed), mcp_server/tools/cycle_tools.py (comment annotation only for fallback sites), mcp_server/server.py (composition root wiring updates), affected test files.

**Out of Scope:**
IStateReader / IStateRepository interface changes. IStateRepository write paths. WorkflowStateMutator. QAManager. cycle_tools raw fallback reads (retained per Approved Strategy Option A).

## Prerequisites

Read these first:
1. research.md Approved Strategy captured (done)
2. Branch initialized (done)
---

## Summary

Two implementation cycles: C1 injects IStateReader into EnforcementRunner, eliminates dead code from ScopeDecoder (state_path/fallback_to_state/\_read_state_json), hardens FileStateRepository.load(), and updates server.py; C2 annotates the cycle_tools documented exception and removes any dead code produced there. Both cycles update affected tests.

---

## TDD Cycles


### Cycle 1: C1: enforcement_runner.py IStateReader injection + ScopeDecoder dead-code elimination

**Goal:** Inject IStateReader into EnforcementRunner and remove the two raw json.loads call sites. Eliminate dead code from ScopeDecoder: remove `state_path` constructor param, `_read_state_json()` method, and `fallback_to_state` parameter from `detect_phase()`. Harden `FileStateRepository.load()` by removing the branch-inject fallback. Update server.py wiring. Remove dead-code-covering tests.

**Tests:**

**Success Criteria:**
- EnforcementRunner.__init__ accepts state_reader: IStateReader; raw json.loads calls on lines 39 and 391 replaced by state_reader.load(branch) field access
- _read_current_phase module-level function deleted
- ScopeDecoder.__init__ no longer has state_path parameter; _read_state_json() method deleted; detect_phase() no longer has fallback_to_state parameter
- All callers of detect_phase() (production + tests) updated to drop fallback_to_state= keyword argument
- All ScopeDecoder instantiations (server.py + tests) updated to drop state_path= argument
- FileStateRepository.load(): if "branch" not in data fallback block removed; branch field required in JSON or Pydantic raises ValidationError
- server.py passes state_reader to EnforcementRunner; ScopeDecoder instantiations no longer pass state_path=
- Tests that exercised fallback_to_state=True behaviour deleted (not just commented out)
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

- **Risk:** ScopeDecoder constructor change breaks all tests that instantiate it directly with state_path=
  - **Mitigation:** Search test suite for `ScopeDecoder(` instantiation; remove state_path= param in RED before GREEN
- **Risk:** detect_phase() signature change (fallback_to_state removed) breaks all callers
  - **Mitigation:** Search for `detect_phase(` in all files; update call sites in RED
- **Risk:** EnforcementRunner constructor change requires server.py and all test fixtures to be updated
  - **Mitigation:** Identify all instantiation sites in tests before editing production code
- **Risk:** FileStateRepository.load() branch-inject removal causes test state fixtures without branch field to fail
  - **Mitigation:** Audit test fixtures; ensure all create state.json with branch field present
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