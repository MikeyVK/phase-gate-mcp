<!-- docs/development/issue357/validation.md -->
<!-- template=research version=8b7bb3ab created=2026-05-28T00:00Z updated=2026-05-28 -->
# Validation — Issue #357: Fix agent lifecycle — parent detection, submit_pr base, end-issue safety

**Status:** PASS  
**Version:** 1.0  
**Last Updated:** 2026-05-28

---

## Scope and Prerequisites

**Branch:** `bug/357-fix-agent-lifecycle`  
**Workflow:** bug (phases: research → design → planning → implementation → validation → documentation → ready)  
**Parent branch:** `epic/320-production-readiness-tracker`  
**Cycles executed:** C1 (IBranchParentReader Protocol), C2 (BranchStateParentReader), C3 (EnforcementRunner F6), C4 (SubmitPRTool F4), C5 (Prompt/agent doc fixes F2/F3/F5)

**Prerequisites validated:**
- All 5 implementation cycles have internal QA: GO verdicts from `@qa` subagent
- Full test suite: 2846 passed, 0 failed (this validation run)
- Branch quality gates: all active gates pass (15 branch files)

---

## Summary Verdict

**PASS** — All planned deliverables (C1.D1–C5.D3) are satisfied. Full test suite green. Branch quality gates green. All Approved Strategy constraints preserved. No regressions introduced.

---

## Full-Suite Test Result

**Command:** `run_tests(scope='full')`  
**Result:** `2846 passed, 11 skipped, 6 xfailed, 0 failed` (55.14s)

No failures. The 11 skipped and 6 xfailed are pre-existing and unrelated to this branch.

---

## Branch Quality Gate Result

**Command:** `run_quality_gates(scope='branch')`  
**Files covered:** 15 branch-changed files  
**Result:** 6/6 active gates PASS (Gate 4: Types skipped — expected for this repo configuration)

| Gate | Status |
|------|--------|
| Gate 0: Ruff Format | ✅ PASS |
| Gate 1: Ruff Strict Lint | ✅ PASS |
| Gate 2: Imports | ✅ PASS |
| Gate 3: Line Length | ✅ PASS |
| Gate 4: Types (mypy) | ⚠️ SKIPPED (expected) |
| Gate 4b: Pyright | ✅ PASS |
| Gate 4c: Types (mcp_server) | ✅ PASS |

---

## Deliverable Mapping

### C1 — IBranchParentReader Protocol

| Deliverable | Evidence | Status |
|-------------|----------|--------|
| C1.D1: IBranchParentReader(Protocol) in core/interfaces/__init__.py | `@runtime_checkable class IBranchParentReader(Protocol)` with single method `get_parent_branch(branch: str) -> str \| None` | ✅ PRESENT |
| C1.D2: mypy clean on interfaces module | Gate 4c (Types mcp_server): PASS | ✅ PASS |

**Exit criteria met:** IBranchParentReader exists with exactly one method signature. mypy clean. No other production files modified.

---

### C2 — BranchStateParentReader Implementation

| Deliverable | Evidence | Status |
|-------------|----------|--------|
| C2.D1: branch_parent_reader.py (new file) with BranchStateParentReader | `mcp_server/managers/branch_parent_reader.py` created | ✅ PRESENT |
| C2.D2: `__init__(state_reader: IStateReader, git_config: GitConfig)` | Constructor signature confirmed | ✅ PRESENT |
| C2.D3: Returns parent_branch on issue match, None on mismatch/absent | Identity validation: `state.issue_number == extracted_branch_issue` check | ✅ PRESENT |
| C2.D4: Unit tests — happy path, mismatch, None parent, StateNotFoundError | `tests/mcp_server/unit/managers/test_branch_parent_reader.py` — 4 test scenarios | ✅ PRESENT |

**Exit criteria met:** All 4 unit tests pass. mypy clean. Quality gates pass.

---

### C3 — EnforcementRunner F6: GitConfig Injection + Bootstrap Predicate

| Deliverable | Evidence | Status |
|-------------|----------|--------|
| C3.D1: `git_config: GitConfig` required param added; `default_base_branch` removed | `enforcement_runner.py` `__init__` signature updated | ✅ PRESENT |
| C3.D2: Branch resolution moved before predicate; mismatch bypass added | `_handle_check_context_loaded`: branch resolved first; `try/except` mismatch check after absent check | ✅ PRESENT |
| C3.D3: server.py EnforcementRunner wiring updated | `git_config=git_config` added; `default_base_branch` kwarg removed | ✅ PRESENT |
| C3.D4: All 9 (12 including 3 additional) test call sites updated | 7 test files updated; all pass `git_config` | ✅ PRESENT |
| C3.D5: New test: gate inactive when issue_number mismatches branch | `test_gate_inactive_when_issue_number_mismatches_branch` in `test_context_loaded_enforcement.py` | ✅ PRESENT |
| C3.D6: Existing regression tests still pass | `test_gate_inactive_on_bootstrap_no_state_json` and `test_gate_blocks_tool_when_context_not_loaded` — ✅ PASS | ✅ PASS |

**Exit criteria met:** All EnforcementRunner tests pass. New mismatch test passes. mypy clean. Quality gates pass.

---

### C4 — SubmitPRTool F4: IBranchParentReader Param + Base Resolution

| Deliverable | Evidence | Status |
|-------------|----------|--------|
| C4.D1: `branch_parent_reader: IBranchParentReader` required 5th param | `SubmitPRTool.__init__` signature confirmed | ✅ PRESENT |
| C4.D2: Base resolution chain: `params.base → reader → default_base_branch` | `base = (params.base or self._branch_parent_reader.get_parent_branch(branch) or self._git_manager.git_config.default_base_branch)` | ✅ PRESENT |
| C4.D3: server.py wiring: BranchStateParentReader injected | `branch_parent_reader=BranchStateParentReader(state_reader=self._state_repository, git_config=git_config)` | ✅ PRESENT |
| C4.D4: `_make_submit_pr_tool` helper updated | Optional `branch_parent_reader` param accepted and passed through | ✅ PRESENT |
| C4.D5: `_make_tool_for_lod` helper updated | `branch_parent_reader=MagicMock(spec=IBranchParentReader)` added | ✅ PRESENT |
| C4.D6: Unit tests: priority, reader result, fallback | `TestSubmitPRToolBaseResolution` — 3 tests, all pass | ✅ PRESENT |
| C4.D7: Integration test: PR opened against reader-provided parent branch | `TestSubmitPRBaseFromReader::test_pr_opened_against_reader_provided_parent_branch` — passes | ✅ PRESENT |

**Exit criteria met:** All SubmitPRTool tests pass including new base resolution tests. mypy clean. Quality gates pass.

---

### C5 — Prompt and Agent Doc Fixes (F2, F3, F5)

| Deliverable | Evidence | Status |
|-------------|----------|--------|
| C5.D1: start-issue.prompt.md non-epic step 6 clarifies pre-initialized boundary | Step 6: "The branch is fully initialized by the time `@co` stops: `create_branch`, `git_checkout`, and `initialize_project` have all completed. `@imp` starts on an already-initialized branch and can call `get_work_context()` unconditionally as its first action." | ✅ PRESENT |
| C5.D2: imp.agent.md precondition paragraph before startup step 1 | Precondition paragraph states: "@imp always starts on pre-initialized branch; uninitialized branch reaching @imp is process violation; do not call initialize_project as recovery; stop and report blocker if state.json absent" | ✅ PRESENT |
| C5.D3: end-issue.prompt.md git_pull + SHA reachability before git_delete_branch | Step 5: `git_pull()`; Step 6: `git merge-base --is-ancestor <merge_commit_sha> HEAD` with BLOCKED stop guard; Step 7: `git_delete_branch` | ✅ PRESENT |

**Exit criteria met:** All three files updated. Content aligns with research.md Corrected Behavior section.

---

## Corrected Behavior Alignment

| Corrected Behavior (from research.md) | Implementation | Status |
|----------------------------------------|----------------|--------|
| `@co` owns all `initialize_project` calls | start-issue.prompt.md step 4 + imp.agent.md precondition | ✅ |
| `@imp` starts on pre-initialized branch unconditionally | imp.agent.md precondition + start-issue step 6 | ✅ |
| `submit_pr` resolves base via narrow IBranchParentReader before default | params.base → reader.get_parent_branch() → git_config.default_base_branch | ✅ |
| Tool does not query full state engine for read-only lookup | IBranchParentReader (1 method); no PhaseStateEngine dependency in SubmitPRTool | ✅ |
| Post-merge cleanup runs only after parent branch locally updated | end-issue.prompt.md step 5: `git_pull()` required before branch delete | ✅ |
| Merged content verifiably reachable before branch deletion | end-issue.prompt.md step 6: `git merge-base --is-ancestor` check + BLOCKED stop | ✅ |
| Inherited parent state does not block different child initialization | F6 mismatch bypass: state.issue_number ≠ branch issue → gate inactive | ✅ |
| Prior fixes from issues #268, #345, #354 preserved | No reintroduction of F1 stale override; end-issue uses `get_pr()` for base_branch; lifecycle boundary exceptions preserved | ✅ |

---

## Approved Strategy Constraints

| Constraint | Status |
|------------|--------|
| IBranchParentReader is narrow Protocol (one method, read-only, CQS) | ✅ |
| DIP: SubmitPRTool depends on abstraction, not on FileStateRepository | ✅ |
| Constructor injection for all new dependencies | ✅ |
| GitConfig injected into EnforcementRunner via constructor | ✅ |
| `GitConfig.extract_issue_number()` reused exclusively — no duplicate parser | ✅ |
| IBranchParentReader is required param (no Optional/None default) | ✅ |
| No backward-compatibility shims; test helpers updated to new signatures | ✅ |
| Bootstrap predicate extended (absent OR mismatch), not replaced | ✅ |
| No `@imp` recovery path for uninitialized branches | ✅ |

---

## Live Demonstration Proposals

### F4 — SubmitPRTool Base Resolution (safest live demo)

**Precondition:** Python venv active; workspace `c:\temp\st3`.

**Command:**
```
pytest tests/mcp_server/unit/tools/test_submit_pr_tool.py::TestSubmitPRToolBaseResolution -xvs
```
**Observe:** All 3 tests pass — `test_params_base_wins_over_reader`, `test_reader_used_when_params_base_none`, `test_fallback_to_default_when_reader_returns_none`.  
**Before fix:** These tests would not exist; SubmitPRTool had no `branch_parent_reader` param and used `default_base_branch` unconditionally when `params.base` was None.

### F6 — Bootstrap Predicate Mismatch Bypass (safest live demo)

**Command:**
```
pytest tests/mcp_server/integration/test_context_loaded_enforcement.py::TestContextLoadedGate::test_gate_inactive_when_issue_number_mismatches_branch -xvs
```
**Observe:** Test passes — `git_commit` on `bug/357-fix-test` branch succeeds even though state.json has `issue_number=999` (mismatch).  
**Before fix:** This test would fail because the gate would activate for any branch when state.json was present, regardless of issue ownership. Epic child branches inheriting parent state.json would be blocked from any branch-mutating operation until `get_work_context()` was called — which would also fail because the inherited state was for the parent issue.

### F2/F3/F5 — Prompt/Doc Fixes (text review)

**Fallback (prompts not pytest-covered):**
- F2: Read `.github/prompts/start-issue.prompt.md` step 6 — confirm "@imp starts on an already-initialized branch"
- F3: Read `.github/agents/imp.agent.md` before startup step 1 — confirm precondition paragraph
- F5: Read `.github/prompts/end-issue.prompt.md` steps 4–7 — confirm git_pull step 5 and reachability check step 6

---

## Residual Risks and Caveats

1. **Prompt human review:** C5 deliverables (start-issue, end-issue, imp.agent) are not pytest-covered per architecture. Correctness relies on human review against research.md Corrected Behavior. Internal `@qa` subagent reviewed and returned PASS, but human sign-off is recommended before documentation phase.

2. **Live F6 behavior on real epic-child branches:** Automated tests use mock state.json. Real epic-child initialization sequence (create epic → initialize → create child → initialize child without calling `get_work_context` on child) has not been live-tested in this session. Automated coverage is strong; live test would provide additional confidence.

3. **end-issue reachability check via shell command:** Step 6 of end-issue.prompt.md uses a shell command (`git merge-base --is-ancestor`) rather than an MCP tool. This is intentional (no MCP tool exists for this check) and matches the human-invoked nature of the prompt, but it introduces a manual step in the lifecycle exit sequence.

---

## Files Changed on Branch

| File | Role | Changed |
|------|------|---------|
| `mcp_server/core/interfaces/__init__.py` | IBranchParentReader Protocol | C1 |
| `mcp_server/managers/branch_parent_reader.py` | BranchStateParentReader implementation (new) | C2 |
| `mcp_server/managers/enforcement_runner.py` | GitConfig injection + mismatch bypass | C3 |
| `mcp_server/tools/pr_tools.py` | IBranchParentReader param + base resolution | C4 |
| `mcp_server/server.py` | EnforcementRunner + SubmitPRTool wiring | C3/C4 |
| `.github/prompts/start-issue.prompt.md` | Non-epic step 6 clarity | C5 |
| `.github/agents/imp.agent.md` | Precondition paragraph | C5 |
| `.github/prompts/end-issue.prompt.md` | git_pull + SHA verification | C5 |
| `tests/mcp_server/unit/managers/test_branch_parent_reader.py` | BranchStateParentReader unit tests (new) | C2 |
| `tests/mcp_server/integration/test_context_loaded_enforcement.py` | F6 mismatch test + helper update | C3 |
| `tests/mcp_server/unit/managers/test_enforcement_runner.py` | git_config blast radius | C3 |
| `tests/mcp_server/unit/managers/test_enforcement_runner_c2.py` | git_config blast radius | C3 |
| `tests/mcp_server/unit/managers/test_enforcement_runner_c4.py` | git_config blast radius | C3 |
| `tests/mcp_server/unit/tools/test_submit_pr_tool.py` | TestSubmitPRToolBaseResolution + helper update | C4 |
| `tests/mcp_server/integration/test_submit_pr_atomic_flow.py` | TestSubmitPRBaseFromReader + helper update | C4 |
