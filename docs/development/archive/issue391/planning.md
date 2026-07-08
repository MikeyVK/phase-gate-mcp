<!-- C:\temp\pgmcp\docs\development\issue391\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-10T06:08Z updated= -->
# refactor(mcp-server): Cleanup legacy naming, docs, tests, and archive files

**Status:** APPROVED  
**Version:** 1.1  
**Last Updated:** 2026-06-10

---

## Purpose

To systematically remove all legacy references to ST3 and SimpleTraderV3 across active documentation and tests, and completely rewrite the main ARCHITECTURE.md, preparing the standalone phase-gate-mcp server for its first release.

## Scope

**In Scope:**
- Deletion of deprecated docs in docs/archive/.
- Systematic cleanup of st3 and simpletrader names in active docs.
- Complete rewrite of docs/mcp_server/ARCHITECTURE.md.
- Refactoring of legacy variable/fixture names in tests/.

**Out of Scope:**
- Historical issue artifacts in docs/development/.
- Rest of the codebase (mcp_server/ is already clean).

**Approved Strategy Constraints:**
- **Historical Issue Preservation**: The historical issue artifacts in `docs/development/` will be kept on the active branch during development of this issue and deferred to the final release issue for branch archiving.
- **docs/archive/ Deletion**: Clean break; permanently delete the folder from `main` but it remains preserved in git reflog/history.
## Prerequisites

Read these first:
1. docs/development/issue391/research.md is approved and committed.
---

## Summary

Plan to perform a clean break on all legacy name occurrences across active docs and test suites to finalize the phase-gate-mcp release-ready state.

---

## Dependencies

- Cycle 2 depends on Cycle 1.
- Cycle 3 depends on Cycle 2.
- Cycle 4 depends on Cycle 3.

---

## TDD Cycles

### Cycle 1: C_CLEANUP.1
- **Deliverable ID:** `del_archive_deletion`
- **Goal:** Delete all deprecated design files in docs/archive/
- **Tests:**
  - Verify directories are physically deleted from main branch
- **Success Criteria:**
  - `docs/archive/` does not exist on main branch.

### Cycle 2: C_CLEANUP.2
- **Deliverable ID:** `del_active_docs_cleanup`
- **Goal:** Clean up all legacy references and URIs in active documentation files and pyproject.toml
- **Tests:**
  - Run custom validation or grep checks for `st3` and `simpletrader` in `docs/` (excl. `docs/development/`)
- **Success Criteria:**
  - Active docs contain zero `st3` / `simpletrader` terms.
  - Active resources use `pgmcp://` URIs instead of `st3://`.
  - `run_quality_gates` executed and passes on all changed doc files.

### Cycle 3: C_CLEANUP.3
- **Deliverable ID:** `del_architecture_rewrite`
- **Goal:** Rewrite `docs/mcp_server/ARCHITECTURE.md` completely to represent the current server architecture and phase-gate identity
- **Tests:**
  - Verify links validation and quality gates pass on `ARCHITECTURE.md`
- **Success Criteria:**
  - `ARCHITECTURE.md` is fully updated, accurate, and has zero legacy references.
  - All Mermaid diagrams compile without syntax errors.

### Cycle 4: C_CLEANUP.4
- **Deliverable ID:** `del_test_refactoring`
- **Goal:** Refactor test variables/fixtures containing `st3` or `simpletrader`, delete obsolete tests, and rename legacy test file.
- **Tasks:**
  - Rename the **82 legacy naming occurrences** in the test suite (e.g., `_ST3_CONFIG` -> `_PGMCP_CONFIG`, `st3_dir` -> `phase_gate_dir`, `SimpleTraderV3` -> `pgmcp`).
  - Delete **10 obsolete tests** that are functionally dead:
    - 6 skipped tests in `tests/mcp_server/unit/managers/test_qa_manager.py` (which mock old hardcoded gates).
    - 3 xfail tests in `test_enforcement_runner_unit.py` and `test_model1_branch_tip_neutralization.py` (which expect neutralization in `GitCommitTool`).
    - 1 xfail test in `test_server.py` (which expects `submit_pr` to block instead of automatically neutralizing).
  - Rename `tests/mcp_server/unit/tools/test_cycle_tools_legacy.py` to `tests/mcp_server/unit/tools/test_cycle_tools_business_logic.py` to match its active function.
- **Tests:**
  - Run the entire `pytest` test suite locally.
  - Run static type checking gate (`pyright` or quality gates) on all modified test files.
- **Success Criteria:**
  - Test suite is fully green.
  - Static type checking passes cleanly on modified test files.
  - All variables renamed (e.g. `_PGMCP_CONFIG`, `phase_gate_dir`).
  - The 10 obsolete tests are removed.
  - The legacy test file is renamed.

## Typing & Quality Gate Obligations

- **Typing Standards**: All modified Python test files must conform to `docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md`. Type gates must pass cleanly with zero errors on changed test files.
- **Quality Gates**: At the end of every cycle, `run_quality_gates` must be executed on all changed files (both documentation and tests). Each cycle must pass quality gates before proceeding.
- **Final Validation**: The final codebase must achieve 10.0/10 linting and pass all static type checking on changed surfaces.

## Cleanup Verification

At the end of Cycle 4, a systematic grep search across active directories (`docs/mcp_server/`, `docs/reference/`, `docs/coding_standards/`, `docs/setup/`, `mcp_server/`, `tests/`) must be run to guarantee 100% clean break:
- `grep_search` query `st3` (case-insensitive) -> must return zero matches (excl. `docs/development/`).
- `grep_search` query `simpletrader` (case-insensitive) -> must return zero matches (excl. `docs/development/`).

## Risks & Mitigation

- **Risk:** Over-renaming '.phase-gate' string literals to '.st3' in test files.
  - **Mitigation:** Only rename variables (e.g. st3_dir -> phase_gate_dir), keeping string literal directory paths intact as expected by production code.

---

## Milestones

- Deprecated docs deleted (Cycle 1)
- Active documentation cleanup complete (Cycle 2)
- ARCHITECTURE.md rewrite complete (Cycle 3)
- Test variables and fixtures cleanup complete (Cycle 4)

## Related Documentation
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-1]**
- **[docs/coding_standards/DOCUMENTATION_STANDARD.md][related-2]**
- **[docs/development/issue391/research.md][related-3]**

<!-- Link definitions -->

[related-1]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-2]: docs/coding_standards/DOCUMENTATION_STANDARD.md
[related-3]: docs/development/issue391/research.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-10 | Agent | Initial draft |