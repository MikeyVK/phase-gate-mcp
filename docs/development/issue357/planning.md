<!-- docs\development\issue357\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-28T18:55Z updated=2026-05-29T00:00Z -->
# Fix agent lifecycle: @co-owns-init contract, IBranchParentReader, bootstrap predicate, end-issue safety

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-28

---

## Scope

**In Scope:**
IBranchParentReader Protocol, BranchStateParentReader, EnforcementRunner constructor + bootstrap predicate, SubmitPRTool constructor + execute() base resolution, server.py composition root wiring, all EnforcementRunner and SubmitPRTool test helpers, prompt/agent doc files (start-issue.prompt.md, end-issue.prompt.md, imp.agent.md)

**Out of Scope:**
Epic workflow redesign, issues #268/#345/#354 contracts, get_work_context bootstrap degradation beyond F6, open-issue/close-issue prompts (on different branch)

## Prerequisites

Read these first:
1. docs/development/issue357/research.md (v1.3) — defect framing, Approved Strategy, corrected behavior
2. docs/development/issue357/design.md (v1.1) — interface contracts, key design decisions, blast radius map
3. docs/coding_standards/ARCHITECTURE_PRINCIPLES.md — binding contract
---

## Summary

Six targeted bug-fixes across agent lifecycle coordination surfaces. C1-C2 establish the IBranchParentReader Protocol and BranchStateParentReader implementation. C3 injects GitConfig into EnforcementRunner and extends the bootstrap predicate with issue-number mismatch bypass. C4 adds IBranchParentReader as a required SubmitPRTool constructor param and updates base resolution. C3 and C4 each include their full blast-radius test updates and server.py wiring in the same atomic GREEN step. C6 adds CheckMergeTool, GitAdapter.is_ancestor, and GitManager.is_ancestor with server.py registration (F9); C6 must complete before C5. C5 updates the three prompt/agent doc files (F2, F3, F5) with no pytest coverage.

---

## TDD Cycles


### Cycle 1: IBranchParentReader Protocol

**Goal:** Introduce the IBranchParentReader narrow Protocol in core/interfaces/__init__.py so that subsequent cycles can depend on it as a stable import.

**Tests:**
- No pytest tests required — Protocol definitions are structural contracts, not executable logic. Verified implicitly by C2 and C4 when the concrete implementations and consumers are type-checked.

**Success Criteria:**
IBranchParentReader(Protocol) exists in mcp_server/core/interfaces/__init__.py with exactly one method get_parent_branch(branch: str) -> str | None. mypy passes on the interfaces module. No other production files changed.



### Cycle 2: BranchStateParentReader implementation

**Goal:** Implement BranchStateParentReader in mcp_server/managers/branch_parent_reader.py backed by IStateReader and GitConfig, with identity validation (issue_number mismatch returns None).

**Tests:**
- Unit: happy path — state.issue_number matches branch issue number, parent_branch returned
- Unit: identity mismatch — state.issue_number differs from branch issue number, returns None
- Unit: parent_branch is None in state — returns None regardless of issue_number match
- Unit: state load raises (branch unknown) — returns None (or propagates per design decision)

**Success Criteria:**
BranchStateParentReader.get_parent_branch() returns parent_branch when issue matches, None in all other cases. All 4 unit tests pass. mypy passes on the new module. Quality gates pass on changed files.

**Dependencies:** C1 — requires IBranchParentReader to exist as the implemented Protocol


### Cycle 3: EnforcementRunner F6: GitConfig injection + bootstrap predicate + blast radius

**Goal:** Add git_config as a required constructor param to EnforcementRunner, retire default_base_branch standalone param, extend _handle_check_context_loaded with issue-number mismatch bypass, update server.py wiring, and update all 12 EnforcementRunner test call sites (7 test files) — all in one atomic GREEN step.

**Tests:**
- Unit: gate inactive when state.json absent (existing test_gate_inactive_on_bootstrap_no_state_json must still pass)
- Integration: gate inactive when state.json present but issue_number in state mismatches branch issue number (new test)
- Integration/Unit: gate active when issue_number matches — existing test_gate_blocks_tool_when_context_not_loaded must still pass
- All existing EnforcementRunner tests in 7 files must pass with updated constructor call sites

**Success Criteria:**
EnforcementRunner.__init__ accepts git_config: GitConfig (required) and no longer has default_base_branch param. _handle_check_context_loaded bypasses gate on absent state.json OR issue_number mismatch. server.py passes git_config=git_config and omits default_base_branch kwarg. All 12 test call sites in 7 files updated (add git_config, drop default_base_branch where present). All EnforcementRunner tests pass. mypy passes. Quality gates pass.

**Dependencies:** No dependency on C1 or C2 — this cycle is independent and can run in parallel in theory, but runs sequentially after C2 for safety


### Cycle 4: SubmitPRTool F4: IBranchParentReader param + base resolution + blast radius

**Goal:** Add branch_parent_reader: IBranchParentReader as required 5th constructor param to SubmitPRTool, update execute() base resolution chain (params.base -> reader.get_parent_branch() -> default_base_branch), wire BranchStateParentReader in server.py, and update both SubmitPRTool test helpers — all in one atomic GREEN step.

**Tests:**
- Unit: params.base override still takes priority over reader result
- Unit: reader.get_parent_branch() called and result used when params.base is absent and reader returns a value
- Unit: fallback to git_config.default_base_branch when reader returns None
- Integration: PR opened against parent branch returned by reader (non-default value)
- Integration: existing params.base tests pass unchanged
- Both _make_submit_pr_tool and _make_tool_for_lod helpers updated; all existing SubmitPRTool tests pass

**Success Criteria:**
SubmitPRTool.__init__ accepts branch_parent_reader: IBranchParentReader as required 5th param. execute() base resolution chain follows params.base -> reader -> default. server.py wires BranchStateParentReader(state_reader=self._state_repository, git_config=git_config). Both test helpers updated. All SubmitPRTool tests pass. mypy passes. Quality gates pass.

**Dependencies:** C1 — IBranchParentReader Protocol required, C2 — BranchStateParentReader required for server.py wiring


### Cycle 5: Prompt and agent doc fixes (F2, F3, F5)

**Goal:** Update the three prompt/agent doc files to express the @co-owns-init model without ambiguity: start-issue.prompt.md (F2), imp.agent.md (F3), end-issue.prompt.md (F5). No code changes. No pytest coverage.

**Tests:**
- No automated tests — human review is the only validation gate for these files

**Success Criteria:**
start-issue.prompt.md non-epic section step 6 explicitly states the branch is pre-initialized and @imp starts on an already-initialized branch. imp.agent.md contains a precondition paragraph before startup step 1 stating @co must initialize the branch and an uninitialized branch reaching @imp is a process violation. end-issue.prompt.md inserts git_pull after git_checkout(base_branch) and a merge_commit_sha reachability verification step before git_delete_branch. Human review confirms all three files against research.md Corrected Behavior section.

**Dependencies:** C6 must complete before C5 — end-issue.prompt.md step 6 references `check_merge(merge_sha=MERGE_SHA)` and C5 must reference a registered tool. No other code dependencies relative to C1–C4.

---

### Cycle 6: CheckMergeTool + GitAdapter.is_ancestor + server.py registration (F9)

**Goal:** Add `CheckMergeInput` + `CheckMergeTool` (read-only `BaseTool`) in `mcp_server/tools/git_tools.py`, implement `GitAdapter.is_ancestor(sha: str) -> bool` (catches `GitCommandError.status == 1` → `False`; status ≥2 → `ExecutionError`), add `GitManager.is_ancestor(sha: str) -> bool` delegating to the adapter, and register `CheckMergeTool(manager=self.git_manager)` in `server.py` — all in one atomic GREEN step.

**Tests:**
- Unit: SHA is an ancestor of HEAD → `ToolResult.text` returned (reachable message)
- Unit: SHA is not an ancestor (`GitCommandError.status == 1`) → `ToolResult.error` returned (not reachable)
- Unit: Git command fails with status ≥2 (`GitCommandError.status == 2`) → `ExecutionError` raised
- Unit: `GitManager.is_ancestor` delegates to `GitAdapter.is_ancestor` and propagates return value

**Success Criteria:**
`CheckMergeTool` inherits `BaseTool`; `enforcement_event = None`. `CheckMergeInput` has a single field `merge_sha: str`. `GitAdapter.is_ancestor` uses `self.repo.git.merge_base("--is-ancestor", sha, "HEAD")`, catches `GitCommandError`, returns `False` on `status == 1`, raises `ExecutionError` on status ≥2. `GitManager.is_ancestor` delegates to `self._adapter.is_ancestor(sha)`. `CheckMergeTool` registered in `server.py`. All 4 new tests pass. mypy passes on changed files. Quality gates pass on changed files.

**Dependencies:** No code dependency on C1–C4; must complete before C5 so end-issue.prompt.md references a registered tool

---

## Risks & Mitigation

- **Risk:** 11 test call sites broken simultaneously when constructor signatures change
  - **Mitigation:** Update all sites in the same atomic GREEN step as the production change; grep all sites before starting the cycle
- **Risk:** Branch-resolution order in _handle_check_context_loaded must precede mismatch check
  - **Mitigation:** Move branch resolution before the new mismatch predicate; test both bypass paths (absent, mismatch) and the active path
- **Risk:** Prompt/agent files have no pytest coverage — correctness cannot be verified by test suite
  - **Mitigation:** Human review of all three files against corrected behavior framing in research.md section Corrected Behavior
- **Risk:** `GitCommandError.status` distinction — status 1 vs ≥2 conflation would silently mask real git errors
  - **Mitigation:** Test all three `is_ancestor` paths explicitly (ancestor, not-ancestor, git error); verify status check logic in implementation

## Related Documentation
- **[docs/development/issue357/research.md][related-1]**
- **[docs/development/issue357/design.md][related-2]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-3]**

<!-- Link definitions -->

[related-1]: docs/development/issue357/research.md
[related-2]: docs/development/issue357/design.md
[related-3]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-28 | Agent | Initial draft |
| 1.1 | 2026-05-29 | Agent | Added C6: CheckMergeTool (F9); updated C5 dependency; updated risks |
