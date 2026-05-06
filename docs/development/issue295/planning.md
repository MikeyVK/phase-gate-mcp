<!-- docs\development\issue295\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-06T06:23Z updated= -->
# submit_pr Atomicity — TDD Cycle Planning

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-06

---

## Purpose

Define the TDD cycle breakdown for implementation of issue #295 (submit_pr atomicity). Maps design §6 test groups to executable cycles with explicit entry conditions, deliverables, and exit criteria.

## Scope

**In Scope:**
mcp_server/adapters/git_adapter.py (2 new methods), mcp_server/managers/git_manager.py (2 new methods), mcp_server/tools/pr_tools.py (execute() refactor), and their test files.

**Out of Scope:**
enforcement.yaml, contracts.yaml, MergePRTool, GitCommitTool, initialize_project, test_model1_branch_tip_neutralization.py (unchanged per design §6.6).

## Prerequisites

Read these first:
1. design.md v1.3 approved (QA GO)
2. Branch fix/295-submit-pr-atomicity-upstream-dirty-tree-rollback active
3. Phase: planning (will transition to implementation after this document is approved)
---

## Summary

Five TDD cycles to implement the three-layer atomicity fix for SubmitPRTool. Bottom-up order: adapter primitives first, then manager methods, then tool refactor. Derived from design.md v1.3 §6 test design and §4 API specification.

---

## Dependencies

- Cycle 4 can proceed in parallel with Cycle 2+3 (only requires Cycle 1)
- Cycle 5 requires both Cycle 3 and Cycle 4 to be complete
- Recommended execution order: 1 → 2 → 3 → 4 → 5 (sequential, avoids merge conflicts on git_manager.py)

---

## TDD Cycles


### Cycle 1: GitAdapter: hard_reset + force_push_with_lease

**Goal:** Introduce the two raw git primitives that all higher-level rollback operations depend on. No existing code is changed.

**Tests:**
- test_hard_reset_calls_git_reset_hard_with_ref
- test_hard_reset_calls_git_reset_hard_with_parent
- test_hard_reset_raises_execution_error_on_failure
- test_force_push_with_lease_calls_git_push
- test_force_push_with_lease_raises_execution_error_on_failure

**Success Criteria:**
- All 5 GitAdapter unit tests pass (tests/mcp_server/unit/adapters/test_git_adapter.py)
- No changes to git_manager.py or pr_tools.py
- mypy + ruff clean on git_adapter.py



### Cycle 2: GitManager.prepare_submission: preflights + artifact filter

**Goal:** Implement the first half of prepare_submission: is_clean preflight, has_upstream preflight, and to_neutralize filter. Method skeleton exists after this cycle but commit/push are not yet implemented.

**Tests:**
- test_prepare_submission_raises_preflight_error_when_dirty
- test_prepare_submission_raises_preflight_error_when_no_upstream
- test_prepare_submission_neutralizes_only_artifacts_with_net_diff
- test_prepare_submission_skips_neutralize_and_commit_when_no_diffs (returns False)

**Success Criteria:**
- 4 prepare_submission preflight/filter tests pass
- PreflightError raised before any mutation on dirty tree or missing upstream
- to_neutralize correctly filtered to paths with net diff
- mypy + ruff clean on git_manager.py

**Dependencies:** Cycle 1 complete


### Cycle 3: GitManager.prepare_submission: conditional commit, push, and local rollbacks

**Goal:** Complete prepare_submission: conditional commit (only when to_neutralize non-empty), push (always), hard_reset rollbacks on commit failure (HEAD) and push failure (HEAD~1 if commit was made). Method returns bool.

**Tests:**
- test_prepare_submission_hard_resets_head_on_commit_failure
- test_prepare_submission_hard_resets_head_minus_one_on_push_failure_after_commit
- test_prepare_submission_no_hard_reset_on_push_failure_when_no_commit
- test_prepare_submission_happy_path_calls_steps_in_order (returns True)

**Success Criteria:**
- All 8 prepare_submission tests pass (4 from Cycle 2 + 4 new)
- hard_reset(HEAD) on commit failure; hard_reset(HEAD~1) on push failure only when commit was made
- Returns True when commit made, False when no commit
- mypy + ruff clean on git_manager.py

**Dependencies:** Cycle 1 complete, Cycle 2 complete


### Cycle 4: GitManager.rollback_push: remote rollback for Failure C

**Goal:** Implement rollback_push: hard_reset(HEAD~1) + force_push_with_lease to undo a pushed commit after create_pr fails. Both failure modes (hard_reset failure + force_push failure) produce RecoveryNote and re-raise.

**Tests:**
- test_rollback_push_hard_resets_and_force_pushes
- test_rollback_push_produces_recovery_note_and_raises_on_force_push_failure
- test_rollback_push_produces_recovery_note_and_raises_on_hard_reset_failure

**Success Criteria:**
- All 3 rollback_push tests pass
- RecoveryNote produced for force_push_with_lease failure (manual: git push --force-with-lease)
- RecoveryNote produced for hard_reset failure (manual: git reset --hard HEAD~1, then git push --force-with-lease)
- ExecutionError always re-raised; nothing swallowed
- mypy + ruff clean on git_manager.py

**Dependencies:** Cycle 1 complete


### Cycle 5: SubmitPRTool.execute(): delegate to manager + commit_made guard + LoD

**Goal:** Refactor execute() to 3 high-level calls (prepare_submission + create_pr + set_pr_status). Wire commit_made guard so rollback_push is only called when a neutralization commit was made. Produce RecoveryNote on successful rollback. Verify LoD boundary.

**Tests:**
- test_failure_a_no_upstream_blocked_before_mutation
- test_failure_b_dirty_tree_blocked_before_mutation
- test_failure_c_create_pr_failure_triggers_rollback_push
- test_failure_c_no_rollback_when_no_neutralization_commit
- test_failure_c_meta_rollback_failure_surfaced_via_recovery_note
- test_failure_d_push_fails_prepare_submission_raises_execution_error
- test_happy_path_prepare_submission_then_create_pr_then_status
- test_happy_path_artifact_paths_extracted_from_merge_readiness_context
- test_submit_pr_execute_does_not_call_git_internals_directly
- test_submit_pr_execute_does_not_access_adapter

**Success Criteria:**
- All 10 tests pass (8 integration + 2 LoD structural)
- Existing test_submit_pr_tool_execute_has_no_adapter_calls (inspect.getsource) still passes
- execute() contains no direct calls to neutralize_to_base, commit_with_scope, push, has_net_diff_for_path
- mypy + ruff clean on pr_tools.py
- Full test suite (tests/mcp_server/) passes with no regressions

**Dependencies:** Cycle 3 complete, Cycle 4 complete

---

## Risks & Mitigation

- **Risk:** Cycles 2 and 3 both modify git_manager.py. Parallelization would cause merge conflicts.
  - **Mitigation:** Execute sequentially (1→2→3→4→5). Cycles 1-4 are small (3-5 new tests each). Cycle 5 is larger (10 tests) because all tests exercise the same `execute()` entry point across different failure modes (A/B/C/D/happy-path + LoD structural); splitting would require a half-implemented refactor state that breaks the invariant that every GREEN commit passes all previously written tests.
- **Risk:** GitManager constructor injection of GitAdapter may require checking existing test fixtures.
  - **Mitigation:** Read test_git_manager.py fixtures before Cycle 2 RED phase to reuse existing mock setup.

---

## Milestones

- After Cycle 1: GitAdapter complete — rollback primitives ready
- After Cycle 3: GitManager.prepare_submission complete — all 8 unit tests pass
- After Cycle 4: GitManager.rollback_push complete — Failure C fully handled
- After Cycle 5: SubmitPRTool complete — all 26 tests pass, LoD verified, no regressions

---

## Deliverables JSON

The `save_planning_deliverables` tool persists a structured cycle manifest to `.st3/deliverables.json`. This is consumed by `get_work_context` during the implementation phase to show TDD cycle progress in context.

**Rationale for structure:**
- `cycle_number` enables `transition_cycle` tooling to track progress against the plan
- `deliverables` are human-readable artefacts (methods + test files) — not test names (those live in planning.md)
- `exit_criteria` is the single gating condition for REFACTOR → next cycle transition

**Planned JSON payload:**

```json
{
  "tdd_cycles": {
    "total": 5,
    "cycles": [
      {
        "cycle_number": 1,
        "name": "GitAdapter: hard_reset + force_push_with_lease",
        "deliverables": [
          "GitAdapter.hard_reset(ref: str) -> None",
          "GitAdapter.force_push_with_lease(remote: str = 'origin') -> None",
          "5 unit tests in tests/mcp_server/unit/adapters/test_git_adapter.py"
        ],
        "exit_criteria": "All 5 GitAdapter unit tests pass; mypy + ruff clean on git_adapter.py"
      },
      {
        "cycle_number": 2,
        "name": "GitManager.prepare_submission: preflights + artifact filter",
        "deliverables": [
          "GitManager.prepare_submission() — preflight + filter skeleton (no commit/push yet)",
          "4 unit tests (dirty/no-upstream/filter/skip) in tests/mcp_server/unit/managers/test_git_manager.py"
        ],
        "exit_criteria": "4 preflight/filter tests pass; PreflightError raised before mutation; mypy + ruff clean"
      },
      {
        "cycle_number": 3,
        "name": "GitManager.prepare_submission: conditional commit, push, and local rollbacks",
        "deliverables": [
          "GitManager.prepare_submission() — complete (commit + push + hard_reset rollbacks, returns bool)",
          "4 unit tests (commit failure, push failure x2, happy path) in tests/mcp_server/unit/managers/test_git_manager.py"
        ],
        "exit_criteria": "All 8 prepare_submission tests pass; returns True/False correctly; mypy + ruff clean"
      },
      {
        "cycle_number": 4,
        "name": "GitManager.rollback_push: remote rollback for Failure C",
        "deliverables": [
          "GitManager.rollback_push(note_context: NoteContext) -> None",
          "3 unit tests (happy path, force_push failure, hard_reset failure) in tests/mcp_server/unit/managers/test_git_manager.py"
        ],
        "exit_criteria": "All 3 rollback_push tests pass; RecoveryNote for both failure modes; mypy + ruff clean"
      },
      {
        "cycle_number": 5,
        "name": "SubmitPRTool.execute(): delegate to manager + commit_made guard + LoD",
        "deliverables": [
          "SubmitPRTool.execute() — refactored to 3 high-level calls",
          "8 integration tests in tests/mcp_server/integration/test_submit_pr_atomic_flow.py",
          "2 LoD structural tests in tests/mcp_server/unit/tools/test_submit_pr_tool.py"
        ],
        "exit_criteria": "All 10 tests pass; inspect.getsource guardrail retained; no direct git-internal calls in execute(); mypy + ruff clean on pr_tools.py; full mcp_server test suite clean"
      }
    ]
  }
}
```

## Related Documentation
- **[docs/development/issue295/design.md — design v1.3 (API contracts + test table)][related-1]**
- **[docs/development/issue295/research.md — research v3.1 FINAL (failure modes + constraints)][related-2]**
- **[mcp_server/adapters/git_adapter.py][related-3]**
- **[mcp_server/managers/git_manager.py][related-4]**
- **[mcp_server/tools/pr_tools.py][related-5]**

<!-- Link definitions -->

[related-1]: docs/development/issue295/design.md — design v1.3 (API contracts + test table)
[related-2]: docs/development/issue295/research.md — research v3.1 FINAL (failure modes + constraints)
[related-3]: mcp_server/adapters/git_adapter.py
[related-4]: mcp_server/managers/git_manager.py
[related-5]: mcp_server/tools/pr_tools.py

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |