<!-- docs\development\issue62\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-06T14:47Z updated= -->
# Make phase workflow tests phase-agnostic (#62)

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-06-06

---

## Purpose

Eliminate hardcoded stale phase names and terminology from the test suite so tests accurately reflect current workflow phase names and are easier to maintain.

## Scope

**In Scope:**
10 test files: 7 with functional stale phase-name literals + 3 with residual TDD terminology in docstrings, comments, test method names, and assertion messages. Total: ~45 replacements.

**Out of Scope:**
Production code changes. New fixtures or helpers. tdd_cycles field names. Generic TDD process language. Historical branch names, issue titles, planning templates. Config-driven refactor (issue #282).

## Prerequisites

Read these first:
1. research.md approved strategy captured (done)
2. Branch initialized and in planning phase (done)
---

## Summary

One implementation cycle: replace all stale phase names (tdd, integration) and residual TDD terminology in 10 test files. String-replacement and method-rename only. No production code changes, no new abstractions.

---

## TDD Cycles


### Cycle 1: C1: Stale phase name and terminology cleanup

**Goal:** Replace all stale 'tdd' / 'integration' phase-name literals and residual TDD terminology across 10 test files. All tests remain semantically equivalent after the fix.

**Tests:**
- tests/mcp_server/fixtures/workflow_fixtures.py — docstring: tdd→implementation, integration→validation
- tests/mcp_server/unit/tools/test_git_pull_tool_behavior.py:53,55 — mock state: tdd→implementation
- tests/mcp_server/unit/managers/test_phase_state_engine_c4_issue257.py:388,397 — setup+assert: tdd→implementation
- tests/mcp_server/unit/managers/test_deliverable_checker.py:74,75,86 — YAML fixture key: tdd→implementation
- tests/mcp_server/core/test_scope_encoder.py:35-37 — remove stale 'integration' block
- tests/mcp_server/core/test_phase_detection.py:38 — remove stale 'integration' line
- tests/mcp_server/integration/test_issue39_cross_machine.py:190,197,203,211 — integration→validation
- tests/mcp_server/unit/managers/test_phase_state_engine.py — 16 docstring/comment/assertion fixes (items 1-16)
- tests/mcp_server/unit/tools/test_git_tools.py — 7 test-name/docstring/comment fixes (items 17-23)
- tests/mcp_server/unit/managers/test_cycle_tools_legacy.py — 7 comment/test-name/docstring fixes (items 24-30)

**Success Criteria:**
- grep -r '"tdd"' tests/ returns only tdd_cycles field references and test_cycle_tools_legacy.py:546 Discovery cycle name — zero stale phase-name hits
- grep -r '"integration"' tests/ returns zero stale phase-name hits
- grep -ri 'TDD phase' tests/ returns zero hits
- grep -r 'tdd_requires_cycle\|tdd_subphase\|tdd_with_cycle\|outside_tdd_phase' tests/ returns zero hits (test method renames applied)
- All existing tests pass with no changes to test logic or assertions
- run_quality_gates on changed files: lint 10.00/10 + mypy pass


---

## Risks & Mitigation

- **Risk:** test_deliverable_checker.py YAML fixture key rename (tdd→implementation) may break downstream fixture-loading if any test references the key by name
  - **Mitigation:** Inspect all tests in test_deliverable_checker.py for dict lookups by key; update any that reference 'tdd' as a key
- **Risk:** test_scope_encoder.py / test_phase_detection.py: removing 'integration' entries may leave the list shorter than expected by parametrize or loop assertions
  - **Mitigation:** Read the full test context before removing; verify assertion counts remain valid
- **Risk:** test_cycle_tools_legacy.py method rename test_transition_blocks_outside_tdd_phase may be referenced externally (pytest -k, CI config)
  - **Mitigation:** Search for the old name in CI/pytest config before renaming

---

## Milestones

- C1 RED: identify exact lines in all 10 files, run tests to confirm baseline green
- C1 GREEN: apply all replacements, run full test suite green
- C1 REFACTOR: run quality gates on changed files — lint 10.00/10 + mypy pass
- Transition to validation

## Related Documentation
- **[docs/development/issue62/research.md][related-1]**

<!-- Link definitions -->

[related-1]: docs/development/issue62/research.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-06 | Agent | Initial draft |