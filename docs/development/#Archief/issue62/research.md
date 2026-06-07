<!-- docs\development\issue62\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-06T14:33Z updated= -->
# Make phase workflow tests phase-agnostic (#62)

**Status:** PRELIMINARY  
**Version:** 1.0  
**Last Updated:** 2026-06-06

---

## Scope

**In Scope:**
7 test files with confirmed stale phase name literals (functional string replacements) + 3 additional test files with stale TDD terminology in docstrings, comments, test names, and assertion messages. String-replacement and rename fixes only.

**Out of Scope:**
Config-driven fixture refactor (issue #282). Production code changes. New abstractions or helpers.

---

## Problem Statement

Test files contain hardcoded workflow phase names ('tdd', 'integration') that no longer exist in the current workflow configuration. This causes false confidence: tests may pass while asserting on stale phase names that production workflows do not use.

## Research Goals

- Confirm exact location and count of stale phase names
- Determine correct replacement values from contracts.yaml
- Identify intentionally unchanged references
- Establish approved strategy (minimal fix vs config-driven)

---

## Background

Originally scoped at ~200 hardcoded phase names across ~15 files. Interim refactors reduced this significantly. Remaining stale names confirmed by codebase audit (2026-06-06): 'tdd' and 'integration' in 7 test files, totalling 15 string literals.

---

## Findings

## Stale References Audit

| File | Lines | Stale name | Replacement | Fix type |
|---|---|---|---|---|
| `tests/mcp_server/fixtures/workflow_fixtures.py` | 42 | `"tdd"`, `"integration"` | `"implementation"`, `"validation"` | docstring |
| `tests/mcp_server/unit/tools/test_git_pull_tool_behavior.py` | 53, 55 | `"tdd"` | `"implementation"` | mock state |
| `tests/mcp_server/unit/managers/test_phase_state_engine_c4_issue257.py` | 388, 397 | `"tdd"` | `"implementation"` | setup + assert |
| `tests/mcp_server/unit/managers/test_deliverable_checker.py` | 74, 75, 86 | `"tdd"` | `"implementation"` | YAML fixture |
| `tests/mcp_server/core/test_scope_encoder.py` | 35-37 | `"integration"` block | remove block | definition |
| `tests/mcp_server/core/test_phase_detection.py` | 38 | `"integration"` | remove line | definition |
| `tests/mcp_server/integration/test_issue39_cross_machine.py` | 190, 197, 203, 211 | `"integration"` | `"validation"` | business logic |

**Intentionally unchanged:**
- `test_deliverable_checker.py` — 'tdd' as YAML fixture name changed to 'implementation' (was incorrectly flagged as backward-compat; name is arbitrary)
- `test_cycle_tools_legacy.py:546` — 'Discovery' is a cycle name, not a phase name
- `test_deliverable_checker.py:207` — `tdd_cycles` is a field name in planning deliverables JSON schema, not a phase name
- All `tdd_cycles` schema/payload fields across the codebase
- Generic TDD process language (e.g., "Do TDD.", process descriptions)
- Historical branch names, issue titles, planning template terminology

## Residual Terminology Cleanup (same test surface)

The following 30 items are within scope as `Residual terminology cleanup inside the same stale-phase test surface`. They cover docstrings, comments, test method names, and assertion messages in 3 test files. No functional (runtime) code changes.

### tests/mcp_server/unit/managers/test_phase_state_engine.py (items 1–16)

| # | Location | Current text | Replacement |
|---|---|---|---|
| 1 | Module header | `TDD phase lifecycle hooks` | `implementation phase lifecycle hooks` |
| 2 | Class docstring | `Tests for TDD phase entry/exit hooks.` | `Tests for implementation phase entry/exit hooks.` |
| 3 | Method docstring | `Test that entering TDD phase auto-initializes cycle 1.` | `entering implementation phase auto-initializes cycle 1.` |
| 4 | Method docstring | `Test that entering TDD phase does NOT block on missing planning deliverables.` | `entering implementation phase does NOT block...` |
| 5 | Method docstring | `Test that exiting TDD phase preserves last_cycle.` | `exiting implementation phase preserves last_cycle.` |
| 6 | Inline comment | `Initialize in TDD phase at cycle 3` | `Initialize in implementation phase at cycle 3` |
| 7 | Method docstring | `Test that exiting TDD phase validates all cycles completed.` | `exiting implementation phase validates...` |
| 8 | Inline comment | `Initialize in TDD phase at cycle 2 (not completed)` | `Initialize in implementation phase at cycle 2 (not completed)` |
| 9 | Method docstring | `transition() to 'tdd' auto-calls on_enter_implementation_phase...` | `transition() to 'implementation' auto-calls...` |
| 10 | Inline comment | `Verify no TDD cycle before transition` | `Verify no active cycle before transition` |
| 11 | Inline comment | `Transition to TDD - should auto-call on_enter_implementation_phase` | `Transition to implementation - should auto-call on_enter_implementation_phase` |
| 12 | Assertion message | `current_cycle should be 1 after entering TDD phase` | `after entering implementation phase` |
| 13 | Method docstring | `transition() from 'tdd' auto-calls on_exit_implementation_phase.` | `transition() from 'implementation' auto-calls...` |
| 14 | Inline comment | `Initialize branch in TDD phase at cycle 2` | `Initialize branch in implementation phase at cycle 2` |
| 15 | Assertion message | `last_cycle should be 2 after exiting TDD phase` | `after exiting implementation phase` |
| 16 | Assertion message | `current_cycle should be preserved after exiting TDD phase` | `after exiting implementation phase` |

### tests/mcp_server/unit/tools/test_git_tools.py (items 17–23)

| # | Location | Current text | Replacement |
|---|---|---|---|
| 17 | Test name | `test_git_commit_tdd_requires_cycle_number` | `test_git_commit_implementation_phase_requires_cycle_number` |
| 18 | Test name | `test_git_commit_tdd_subphase_requires_cycle_number` | `test_git_commit_implementation_subphase_requires_cycle_number` |
| 19 | Method docstring | `Test that non-TDD phases do NOT require cycle_number` | `non-implementation phases do NOT require cycle_number` |
| 20 | Test name | `test_git_commit_tdd_with_cycle_number_succeeds` | `test_git_commit_implementation_with_cycle_number_succeeds` |
| 21 | Method docstring | `Test that TDD commits WITH cycle_number succeed` | `implementation-phase commits WITH cycle_number succeed` |
| 22 | Inline comment | `Commit in TDD phase WITH cycle_number - should succeed` | `Commit in implementation phase WITH cycle_number - should succeed` |
| 23 | Inline comment | `phase=tdd, cycle=2 matches state.json` | `phase=implementation, cycle=2 matches state.json` |

### tests/mcp_server/unit/managers/test_cycle_tools_legacy.py (items 24–30)

| # | Location | Current text | Replacement |
|---|---|---|---|
| 24 | Inline comment | `Initialize TDD phase with cycle 1` | `Initialize implementation phase with cycle 1` |
| 25 | Test name | `test_transition_blocks_outside_tdd_phase` | `test_transition_blocks_outside_cycle_based_phase` |
| 26 | Method docstring | `Test that transition only works during TDD phase.` | `only works during cycle-based phases.` |
| 27 | Assertion message | `Expected transition to be blocked outside TDD phase` | `outside cycle-based phase` |
| 28 | Method docstring | `Create project in TDD phase at cycle 2 for forced transitions.` | `cycle-based phase at cycle 2 for forced transitions.` |
| 29 | Method docstring | `Create project in TDD phase at cycle 2.` | `cycle-based phase at cycle 2.` |
| 30 | Method docstring | `Create project in TDD phase at cycle 1.` | `cycle-based phase at cycle 1.` |

## Preservation Goals

- All tests must remain semantically equivalent after the fix
- `test_issue39_cross_machine.py` transitions must use a phase name that exists in the bug workflow (`validation` is the correct successor to `implementation`)
- `test_scope_encoder.py` and `test_phase_detection.py`: removing the stale 'integration' dict entries does not break any assertions — those entries are defined but never referenced in actual test assertions

## Architectural Constraints

- No config-driven refactor (out of scope per approved strategy)
- No new fixtures or helpers introduced
- No production code changes — test-only fix
- ARCHITECTURE_PRINCIPLES.md: hardcoded phase names in tests couple the test suite to workflow YAML content — this refactor reduces that coupling at minimal cost

## Related Documentation
- **[tests/mcp_server/fixtures/workflow_fixtures.py][related-1]**
- **[tests/mcp_server/integration/test_issue39_cross_machine.py][related-2]**
- **[.phase-gate/config/contracts.yaml][related-3]**

---

## Approved Strategy

**Boundary:** All test files containing stale hardcoded phase names (`tdd`, `integration`).

**Selected strategy:** Minimal string-replacement fix. No config-driven refactor.

**Rationale:** The remaining stale references are small in number (15 literals across 7 files) and mechanical in nature. A config-driven refactor (issue #282) is a separate complementary concern. Introducing fixture abstractions now would exceed scope and add complexity without proportional benefit.

**Constraints for later phases:**
- Fix the 7 files in the functional findings table (phase name literals in runtime code)
- Fix the 3 additional files with residual terminology (docstrings, comments, test names, assertion messages) — 30 items total
- No new fixtures, helpers, or abstractions introduced
- No production code changes
- `test_deliverable_checker.py:207` (`tdd_cycles` field name) must remain unchanged
- `test_cycle_tools_legacy.py:546` (`Discovery` cycle name) must remain unchanged
- `tdd_cycles` schema/payload fields and generic TDD process language outside this surface are out of scope

<!-- Link definitions -->

[related-1]: tests/mcp_server/fixtures/workflow_fixtures.py
[related-2]: tests/mcp_server/integration/test_issue39_cross_machine.py
[related-3]: .phase-gate/config/contracts.yaml

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-06 | Agent | Initial draft |
| 1.1 | 2026-06-06 | Agent | Scope expansion: +30 residual terminology items in test_phase_state_engine.py, test_git_tools.py, test_cycle_tools_legacy.py |