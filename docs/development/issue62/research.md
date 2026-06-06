<!-- docs\development\issue62\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-06T14:33Z updated= -->
# Make phase workflow tests phase-agnostic (#62)

**Status:** PRELIMINARY  
**Version:** 1.0  
**Last Updated:** 2026-06-06

---

## Scope

**In Scope:**
7 test files with confirmed stale phase name literals. String-replacement fixes only.

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
- Fix only the 7 files listed in the findings table
- No new fixtures, helpers, or abstractions introduced
- No production code changes
- `test_cycle_tools_legacy.py` and `test_deliverable_checker.py:207` (`tdd_cycles` field name) must remain unchanged
- `test_deliverable_checker.py` YAML fixture: `tdd` → `implementation` (arbitrary name, not a backward-compat concern)

<!-- Link definitions -->

[related-1]: tests/mcp_server/fixtures/workflow_fixtures.py
[related-2]: tests/mcp_server/integration/test_issue39_cross_machine.py
[related-3]: .phase-gate/config/contracts.yaml

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-06 | Agent | Initial draft |