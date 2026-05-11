<!-- docs\development\issue228\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-11T19:06Z updated= -->
# Add Issue Number to Commit Message Suffix (Issue #228)

**Status:** DRAFT  
**Version:** 1.1  
**Last Updated:** 2026-05-11 (rev: QA NOGO v2 → rewrite C_228.2, fix C_228.1 test names)

---

## Purpose

Define cycle order, size rationale, per-cycle deliverables, and JSON gatekeepers for cycle transfer. Each deliverable is a verifiable artefact that the next cycle (or the validation phase) can use as a gate.

## Scope

**In Scope:**
mcp_server/managers/git_manager.py, mcp_server/tools/git_tools.py, their direct unit tests.

**Out of Scope:**
ScopeDecoder, PhaseDetection, WorkflowStatusResolver, integration tests that parse commit messages, backend/.

## Prerequisites

Read these first:
1. research-design.md v1.1 approved (QA GO on F4/D3 and D2)
2. GitConfig.extract_issue_number() confirmed present (config/schemas/git_config.py L92)
---

## Summary

Three TDD cycles. C_228.1 adds the optional issue_number param to commit_with_scope(). C_228.2 refactors GitCommitTool.execute() to call get_state() instead of get_current_phase() so both phase and issue_number are read in one I/O call. C_228.3 wires prepare_submission() to GitConfig.extract_issue_number() so neutralize commits also carry the suffix. Each cycle is a minimal atomic unit; none can be safely skipped.

---

## Dependencies

- C_228.2 depends on C_228.1 (commit_with_scope must accept issue_number before callers can pass it)
- C_228.3 depends on C_228.1 (same reason); independent of C_228.2

---

## TDD Cycles


### Cycle 1: C_228.1 — commit_with_scope() accepts optional issue_number

**Goal:** Add issue_number: int | None = None parameter to GitManager.commit_with_scope(). Assemble suffix f' (#{issue_number})' when not None. No caller changes needed — all existing callers pass None implicitly.

**Tests:**
- NEW: test_commit_with_scope_appends_issue_suffix — commit_with_scope(issue_number=228) produces message ending with ' (#228)'
- NEW: test_commit_with_scope_no_suffix_when_none — commit_with_scope(issue_number=None) produces message without suffix (regression guard)
- UPDATE: test_commit_with_scope_phase_only — add issue_number=None to commit_with_scope call assertion
- UPDATE: test_commit_with_scope_phase_and_subphase — same
- UPDATE: test_commit_with_scope_with_cycle_number — same

**Success Criteria:**
- commit_with_scope(issue_number=228) → message ends with ' (#228)'
- commit_with_scope(issue_number=None) → no suffix
- All existing GitManager unit tests pass without modification to their fixture data
- mypy / ruff clean on git_manager.py



### Cycle 2: C_228.2 — GitCommitTool reads issue_number via two-path approach

**Goal:** Apply the two-path design from research-design.md D2.

- **Auto-detect path** (`workflow_phase is None`): replace `get_current_phase()` with
  `get_state()` to obtain both `state.current_phase` and `state.issue_number` in one read.
  Existing hard-error behavior on `FileNotFoundError` / `StateBranchMismatchError` is
  **preserved unchanged** — a mismatch is detected inconsistency, not a missing source.

- **Explicit `workflow_phase` path**: use `self.manager.git_config.extract_issue_number(
  current_branch)` — already available via `self.manager`, same helper as C_228.3.
  No state read introduced. `None` on non-conforming branch = documented contract.

**Tests:**
- NEW: test_commit_tool_auto_detect_includes_suffix — auto-detect path, get_state() returns
  issue_number=42, asserts commit_with_scope called with issue_number=42
- NEW: test_commit_tool_explicit_phase_uses_git_config — explicit workflow_phase provided,
  git_config.extract_issue_number returns 42, asserts suffix injected; no get_state call
- NEW: test_commit_tool_auto_detect_mismatch_returns_error — StateBranchMismatchError on
  auto-detect path returns ToolResult.error, not issue_number=None
- UPDATE: existing auto-detect test mocks — replace get_current_phase mock with get_state
  stub returning BranchState with .current_phase and .issue_number=None

**Success Criteria:**
- Auto-detect path: get_state() called once, phase and issue_number both consumed
- Auto-detect path: StateBranchMismatchError produces hard error (existing behavior)
- Explicit path: git_config.extract_issue_number called, no get_state call made
- commit_with_scope receives issue_number on both happy paths
- All existing GitCommitTool tests pass
- mypy / ruff clean on git_tools.py

**Dependencies:** C_228.1 merged and GREEN


### Cycle 3: C_228.3 — prepare_submission() carries issue_number via GitConfig.extract_issue_number()

**Goal:** Inside GitManager.prepare_submission(), call self._git_config.extract_issue_number(branch) and pass the result to commit_with_scope(). Returns None for main or non-conforming branches — no suffix appended.

**Tests:**
- NEW: test_prepare_submission_issue_branch_carries_suffix — branch 'feature/228-title', asserts commit_with_scope called with issue_number=228
- NEW: test_prepare_submission_main_no_suffix — branch 'main', asserts commit_with_scope called with issue_number=None

**Success Criteria:**
- prepare_submission on feature/228-* branch produces neutralize commit with ' (#228)' suffix
- prepare_submission on main (or non-conforming branch) produces no suffix
- No new dependency introduced to GitManager (uses existing self._git_config)
- All existing neutralize / prepare_submission tests pass
- mypy / ruff clean on git_manager.py

**Dependencies:** C_228.1 merged and GREEN

---

## Risks & Mitigation

- **Risk:** Existing tests that assert exact commit message format may fail if test fixtures pass a non-None issue_number inadvertently.
  - **Mitigation:** All existing callers pass None implicitly via default; grep for commit_with_scope call sites before merging each cycle.
- **Risk:** Auto-detect path get_state() mock shape differs from get_current_phase() mock — wrong mock may silently return None for issue_number.
  - **Mitigation:** C_228.2 RED test explicitly asserts suffix presence on auto-detect path; missing issue_number causes immediate RED failure.

---

## Milestones

- C_228.1 GREEN: suffix mechanic proven in isolation
- C_228.2 GREEN: normal workflow commits carry issue suffix end-to-end
- C_228.3 GREEN: neutralize commits carry issue suffix end-to-end

## Related Documentation
- **[docs/development/issue228/research-design.md][related-1]**

<!-- Link definitions -->

[related-1]: docs/development/issue228/research-design.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |