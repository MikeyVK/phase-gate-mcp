<!-- docs\development\issue298\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-04T20:53Z updated= -->
# Planning: State.json Authoritative Status + Sub-phase Persistence

**Status:** DRAFT  
**Version:** 1.1  
**Last Updated:** 2026-05-04

---

## Purpose

Break down the two interacting changes from research into ordered, testable TDD cycles. Each cycle delivers one cohesive behavioural change; dependencies between cycles are explicit.

## Scope

**In Scope:**
WorkflowStatusResolver inversion, BranchState.current_sub_phase field, PhaseStateEngine.record_sub_phase() seam + clearing, GitCommitTool trigger, WorkflowStatusDTO type narrowing, project_manager + discovery_tools error handling, blast-radius test rewrites

**Out of Scope:**
Phase-interruption cycle-restore (separate follow-up issue), WorkflowStatusDTO public output format changes, QA baseline state, MCP tool output formats

## Prerequisites

Read these first:
1. Research doc v1.6 approved — docs/development/issue298/research-state-json-authoritative-and-subphase-persistence.md
2. Issue #292 merged — WorkflowStateMutator coordinated write seam in production
3. Issue #231 merged — WorkflowStatusResolver in production
4. Issue #271 merged — contracts.yaml SSOT
---

## Summary

Seven TDD cycles implementing resolver inversion, sub_phase persistence, and blast-radius error handling as designed in research v1.6. Cycle order follows dependency graph: schema foundation first, then type narrowing, resolver inversion, engine seam, tool wiring, consumer error handling, and finally blast-radius test rewrites.

---

## Dependencies

- BranchState (C1) must precede resolver inversion (C3) — StateNotFoundError defined in state_repository.py
- BranchState (C1) must precede PhaseStateEngine seam (C4) — current_sub_phase field must exist before engine can write it
- BranchState (C1) must precede consumer error handling (C6) — StateNotFoundError must be importable before catch blocks compile
- WorkflowStatusDTO narrowing (C2) independent of C1 but must precede test rewrites (C7)
- PhaseStateEngine seam (C4) must precede GitCommitTool wiring (C5)
- Resolver inversion (C3) must precede consumer error handling (C6)
- All production cycles (C1-C6) must pass before blast-radius test rewrites (C7)

---

## TDD Cycles


### Cycle 1: BranchState.current_sub_phase + StateNotFoundError

**Goal:** Add current_sub_phase: str | None = None to BranchState (backward-compatible Pydantic field). Define StateNotFoundError in state_repository.py (distinct from FileNotFoundError — domain event, not I/O error). Schema foundation all other cycles depend on.

**Tests:**
- test_branch_state_current_sub_phase_defaults_to_none — BranchState() without current_sub_phase deserialises correctly
- test_branch_state_current_sub_phase_persists — FileStateRepository save+load round-trips current_sub_phase='red'
- test_branch_state_current_sub_phase_none_round_trips — round-trip with current_sub_phase=None
- test_state_not_found_error_is_exception — StateNotFoundError is an Exception subclass, not FileNotFoundError
- test_state_not_found_error_carries_branch — StateNotFoundError('feature/42') message contains branch name

**Success Criteria:**
- BranchState accepts current_sub_phase without errors
- Existing state.json files without current_sub_phase deserialise without ValidationError
- StateNotFoundError is importable from mcp_server.managers.state_repository
- All 5 new tests pass; no existing BranchState tests break



### Cycle 2: WorkflowStatusDTO type narrowing

**Goal:** Narrow phase_source to Literal['state.json'] and phase_confidence to Literal['high']. Dead values 'commit-scope', 'unknown' (phase_source) and 'medium', 'unknown' (phase_confidence) removed. Mypy must reject dead-value construction.

**Tests:**
- test_workflow_status_dto_rejects_commit_scope_phase_source — ValidationError on phase_source='commit-scope'
- test_workflow_status_dto_rejects_unknown_phase_source — ValidationError on phase_source='unknown'
- test_workflow_status_dto_rejects_medium_phase_confidence — ValidationError on phase_confidence='medium'
- test_workflow_status_dto_rejects_unknown_phase_confidence — ValidationError on phase_confidence='unknown'
- test_workflow_status_dto_accepts_state_json_high — constructs without error with valid values

**Success Criteria:**
- Pydantic rejects dead Literal values at construction time
- test_dto_has_required_fields (line 36) updated to use phase_source='state.json' and phase_confidence='high'
- mypy reports no errors on workflow_status.py



### Cycle 3: WorkflowStatusResolver inversion

**Goal:** Invert resolve_current(): state.json primary. Absent state raises StateNotFoundError. Branch mismatch raises StateBranchMismatchError. No commit-scope fallback. phase_confidence='high' on success path.

**Tests:**
- test_resolve_uses_state_when_present_despite_high_confidence_commit — phase_source='state.json', phase_confidence='high'
- test_resolve_raises_state_not_found_when_absent — StateNotFoundError raised on absent state.json
- test_resolve_raises_branch_mismatch_when_present_wrong_branch — StateBranchMismatchError raised (replaces test_resolve_handles_branch_mismatch_gracefully)

**Success Criteria:**
- resolve_current() never returns phase_source='commit-scope' or 'unknown'
- StateNotFoundError raised on absent state
- StateBranchMismatchError raised on branch mismatch
- phase_confidence always 'high' on success path

**Dependencies:** Cycle 1 — StateNotFoundError must be defined


### Cycle 4: PhaseStateEngine.record_sub_phase() + clearing

**Goal:** Add `record_sub_phase(branch, sub_phase)` as a public method to PhaseStateEngine using the existing state write seam. All three phase/cycle transition methods (`transition()`, `force_transition()`, `transition_cycle()`) must clear `current_sub_phase` at the transition boundary. `on_exit_cycle_based_phase()` must not be modified — it owns only cycle-tracking.

**Tests:**
- test_record_sub_phase_writes_to_state — record_sub_phase('feature/42', 'red') persists current_sub_phase='red'
- test_record_sub_phase_none_clears_state — record_sub_phase('feature/42', None) sets current_sub_phase=None
- test_transition_clears_sub_phase — after transition(), state has current_sub_phase=None
- test_force_transition_clears_sub_phase — after force_transition(), state has current_sub_phase=None
- test_transition_cycle_clears_sub_phase — after transition_cycle(), state has current_sub_phase=None
- test_on_exit_cycle_based_phase_does_not_touch_sub_phase — on_exit_cycle_based_phase() does not modify current_sub_phase

**Success Criteria:**
- record_sub_phase() callable as public method
- sub_phase persists correctly
- All three transition methods clear sub_phase
- Existing on_exit_cycle_based_phase tests at lines 174, 206, 520 still pass

**Dependencies:** Cycle 1 — BranchState.current_sub_phase field must exist


### Cycle 5: GitCommitTool record_sub_phase trigger

**Goal:** After a successful commit, `GitCommitTool` must call the engine's `record_sub_phase()` with the current branch and the `sub_phase` parameter from the commit params. Always-write semantics: the call must happen even when `sub_phase` is `None` (explicitly clears persisted sub_phase).

**Tests:**
- test_git_commit_tool_calls_record_sub_phase_with_sub_phase — commit with sub_phase='red' calls engine.record_sub_phase(branch, 'red')
- test_git_commit_tool_calls_record_sub_phase_with_none — commit with sub_phase=None calls engine.record_sub_phase(branch, None)
- test_git_commit_tool_does_not_call_record_sub_phase_when_engine_none — no AttributeError when _state_engine is None

**Success Criteria:**
- record_sub_phase() called on every successful commit
- None sub_phase passed through
- No regression in existing GitCommitTool tests

**Dependencies:** Cycle 4 — record_sub_phase() method must exist on PhaseStateEngine


### Cycle 6: Consumer error handling: project_manager + discovery_tools

**Goal:** `project_manager.get_project_plan()`: when `resolve_current()` raises `StateNotFoundError`, `StateBranchMismatchError`, or `OSError`, skip the phase-enrichment block and return `plan` without phase fields; fix the stale docstring; add required imports. `discovery_tools.GetWorkContextTool`: enable `NoteContext` usage (currently suppressed); `StateNotFoundError` and `StateBranchMismatchError` must be handled in a separate except clause from the existing `OSError` path — the existing graceful I/O error path must be retained unchanged; on state error, produce `RecoveryNote` with actionable recovery guidance and return `ToolResult.error`.

**Tests:**
- test_get_project_plan_returns_plan_without_phase_fields_when_state_absent — StateNotFoundError from resolver → plan dict without phase keys
- test_get_project_plan_returns_plan_without_phase_fields_on_mismatch — StateBranchMismatchError → same graceful result
- test_get_work_context_returns_error_with_recovery_note_when_state_absent — StateNotFoundError → ToolResult.error + RecoveryNote in context
- test_get_work_context_returns_error_with_recovery_note_on_mismatch — StateBranchMismatchError → ToolResult.error + RecoveryNote in context
- test_get_work_context_graceful_io_error_path_unchanged — OSError → existing graceful path still works

**Success Criteria:**
- InitializeProjectTool still works on fresh branches
- GetWorkContextTool returns actionable RecoveryNote on absent state
- Existing OSError graceful path unaffected
- No UnboundLocalError from del context removal

**Dependencies:** Cycle 1 — StateNotFoundError, Cycle 3 — resolver raises instead of returning


### Cycle 7: Blast-radius test rewrites

**Goal:** Rewrite all existing tests asserting phase_source='commit-scope', phase_source='unknown', phase_confidence='medium'/'unknown'. Target: test_workflow_status_resolver.py, test_discovery_tools.py, test_project_tools.py, test_project_manager.py.

**Tests:**
- test_workflow_status_resolver.py test_resolve_uses_commit_scope_when_high_confidence — rewrite to expect phase_source='state.json' when state present
- test_discovery_tools.py lines 230, 479, 756, 785 — update phase_source assertions to 'state.json'
- test_project_tools.py lines 1020, 1034 — update phase_source assertions
- test_project_manager.py test_get_project_plan_uses_resolver_phase (line 734) + test_get_project_plan_formats_phase_colon_sub_phase (line 755) — update mock setup
- test_project_manager.py test_get_project_plan_includes_current_phase_from_commit_scope (line 320) + test_get_project_plan_returns_unknown_when_no_commits (line 344) — rewrite for new contract

**Success Criteria:**
- No test asserts phase_source in ('commit-scope', 'unknown') as valid success value
- No test constructs WorkflowStatusDTO with dead Literal values
- Full test suite passes with zero failures
- mypy --strict passes on all affected test files

**Dependencies:** Cycle 2 — DTO narrowing (mypy catches dead values), Cycle 3 — resolver behaviour changed, Cycle 6 — consumer error handling

---

## Risks & Mitigation

- **Risk:** WorkflowStatusDTO Literal narrowing (C2) may break test fixtures that construct DTOs with dead values outside the blast-radius table
  - **Mitigation:** Run mypy after C2 merge to surface all remaining dead-value usages before C7 rewrite pass
- **Risk:** del context removal in discovery_tools.py (C6) may be missed if implementer only reads the catch-block instruction
  - **Mitigation:** C6 test test_get_work_context_returns_error_with_recovery_note will catch UnboundLocalError immediately at RED stage
- **Risk:** get_project_plan() graceful degradation (C6) may accidentally suppress genuine errors from other parts of the method
  - **Mitigation:** Catch block is tightly scoped to (StateNotFoundError, StateBranchMismatchError, OSError) — not a bare except

## Related Documentation
- **[docs/development/issue298/research-state-json-authoritative-and-subphase-persistence.md][related-1]**
- **[mcp_server/managers/workflow_status_resolver.py][related-2]**
- **[mcp_server/managers/phase_state_engine.py][related-3]**
- **[mcp_server/managers/state_repository.py][related-4]**
- **[mcp_server/state/workflow_status.py][related-5]**

<!-- Link definitions -->

[related-1]: docs/development/issue298/research-state-json-authoritative-and-subphase-persistence.md
[related-2]: mcp_server/managers/workflow_status_resolver.py
[related-3]: mcp_server/managers/phase_state_engine.py
[related-4]: mcp_server/managers/state_repository.py
[related-5]: mcp_server/state/workflow_status.py

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.1 | 2026-05-04 | Agent | QA v1.0 annotations: A1 add C1→C4 + C1→C6 deps; A2 remove test_resolve_uses_commit_scope from C3 (owned by C7); A3 remove test_dto_has_required_fields from C7 (owned by C2); A4-A6 de-HOW goals for C4/C5/C6 |
| 1.0 |  | Agent | Initial draft |