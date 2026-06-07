<!-- docs/development/issue345/validation.md -->
<!-- template=research version=8b7bb3ab created=2026-05-25T06:40Z updated=2026-05-25 -->
# Validation — Issue #345: git_delete_branch remote deletion + lifecycle closeout

**Status:** PASS  
**Version:** 1.0  
**Last Updated:** 2026-05-25

---

## Scope and Prerequisites

**Branch:** `feature/345-git-delete-branch-remote-deletion`  
**Workflow:** feature (phases: research → design → planning → implementation → validation)  
**Parent branch:** `main`  
**Cycles executed:** C1 (mode enum + BranchDeleteResult), C2 (end-issue prompt), C3 (PR body contract), C4 (doc alignment)

**Prerequisites validated:**
- All 4 implementation cycles have internal QA: GO verdicts from `@qa` subagent
- Full test suite: 2821 passed, 0 failed (consistent across C3, C4, and this validation run)
- Branch quality gates: all active gates pass

---

## Summary Verdict

**PASS** — All planned deliverables (D1.1–D4.6) are satisfied. Full test suite green. Branch quality gates green. Design and Approved Strategy constraints preserved. No regressions.

---

## Full-Suite Test Result

**Command:** `run_tests(scope='full')`  
**Result:** `2821 passed, 11 skipped, 6 xfailed, 0 failed` (56.17s)

No failures. The 11 skipped and 6 xfailed are pre-existing and unrelated to this branch.

---

## Branch Quality Gate Result

**Command:** `run_quality_gates(scope='branch')` — 13 files  

| Gate | Status |
|------|--------|
| Gate 0: Ruff Format | ✅ PASS |
| Gate 1: Ruff Strict Lint | ✅ PASS |
| Gate 2: Imports | ✅ PASS |
| Gate 3: Line Length | ✅ PASS |
| Gate 4: Types (mypy) | ⏭ SKIPPED (global skip) |
| Gate 4b: Pyright | ✅ PASS |
| Gate 4c: Types (mcp_server) | ✅ PASS |

**Overall: PASS** (6/6 active gates pass)

---

## Planning Deliverables — Evidence Mapping

### C1: git_delete_branch mode enum

| Deliverable | Evidence |
|-------------|----------|
| D1.1 `GitDeleteBranchInput.mode` field | `mcp_server/tools/git_tools.py` — `mode: Literal["local","remote","both"] = Field(default="both")` |
| D1.2 execute passes mode; renders BranchDeleteResult | `GitDeleteBranchTool.execute` calls `manager.delete_branch(branch, ctx, force=force, mode=mode)`; output renders local/remote status |
| D1.3 `BranchDeleteResult` frozen dataclass | `mcp_server/managers/git_manager.py` — `@dataclass(frozen=True)` with `local_status` and `remote_status` |
| D1.4 `GitManager.delete_branch` orchestrates local/remote/both | Applies protected-branch check first; `mode=remote` skips current-branch check; remote absent = not an error |
| D1.5 `GitAdapter.delete_local_branch` (renamed) | Renamed from `delete_branch`; raises `ExecutionError` for missing branch, current branch, or other failure |
| D1.6 `GitAdapter.delete_remote_branch` returns `"deleted"` or `"absent"` | Returns `"absent"` when remote ref not found (not an error); raises for bad remote config |
| D1.7 `test_git_tools.py` updated + new mode tests | New tests cover mode=local/remote/both/remote-absent, BranchDeleteResult output rendering |
| D1.8 `test_all_tools.py` updated | Mode coverage tests added |
| D1.9 `test_git_manager_config.py` updated | New signature + remote/both mode tests |
| D1.10 `test_git_adapter.py` updated | `delete_local_branch` + `TestGitAdapterDeleteRemoteBranch` including remote-absent |
| D1.11 `test_git_manager.py` updated | `test_delete_branch_valid` and `test_delete_branch_protected` updated; mock assertions use `delete_local_branch` |

**Exit criteria check:**
- mode=local preserves old local-only behavior ✅
- mode=both is default ✅
- mode=remote skips current-branch check ✅
- remote-absent returns absent, not error ✅
- BranchDeleteResult is frozen dataclass ✅
- ruff + pyright clean ✅

### C2: end-issue lifecycle-exit prompt

| Deliverable | Evidence |
|-------------|----------|
| D2.1 `close-issue.prompt.md` deleted | File absent from `.github/prompts/` |
| D2.2 `end-issue.prompt.md` created | `.github/prompts/end-issue.prompt.md` — `agent: co`; human invocation = merge-approval signal; flow: `get_work_context` → `merge_pr` → `git_checkout(parent)` → `git_delete_branch(mode="both")` → read PR body → conditional epic-parent update → next-issue advisory |

**Exit criteria check:**
- `end-issue.prompt.md` declares `agent: co` ✅
- Human invocation is merge-approval signal ✅
- `close_issue()` absent from normative path ✅
- `git_diff_stat` absent from normative merge-proof ✅
- `close-issue.prompt.md` does not exist ✅

### C3: ready-phase PR body contract

| Deliverable | Evidence |
|-------------|----------|
| D3.1 Six ready blocks: unified deferred-work-in-body instruction | All 6 workflows (feature/bug/refactor/docs/hotfix/epic) updated in `.phase-gate/config/contracts.yaml` |
| D3.2 `PRContext.deferred_work: str \| None = None` | `mcp_server/schemas/contexts/pr.py` |
| D3.3 `PRContext.tracking_state: str \| None = None` | `mcp_server/schemas/contexts/pr.py` |
| D3.4 `pr.md.jinja2` Deferred Work section | Template renders `## Deferred Work` section conditionally when `deferred_work` is set |
| D3.5 Template tests extended | `tests/mcp_server/scaffolding/test_task37_tracking_templates.py` — 2 new rendering tests |
| D3.6 PRContext schema test extended | `tests/mcp_server/unit/schemas/test_tracking_artifact_v2_parity.py` — new optional fields test |
| D3.7 Six ready blocks: Closes #N + closure-readiness review + handover-as-completeness-check | Applied to all 6 ready blocks |
| D3.8 Six ready blocks: original issue body honesty check | Applied to all 6 ready blocks |

**Exit criteria check:**
- All six ready blocks carry unified instructions ✅
- `PRContext` optional fields do not break existing callers (default=None) ✅
- Template renders deferred-work section conditionally ✅
- All existing and new tests green ✅

### C4: documentation and wording alignment

| Deliverable | Evidence |
|-------------|----------|
| D4.1 `git.md`: mode param + migration note | `⚠️ Breaking Change` callout + migration note + examples for local/remote/both |
| D4.2 `MCP_TOOLS.md`: git_delete_branch with mode | Both call sites annotated with `# mode="both"` |
| D4.3 `project.md`: state.json branch-local wording | Changed from `(runtime, not committed)` to `(branch-local artifact, committed with branch history; neutralized by \`submit_pr\`)` |
| D4.4 `imp.agent.md`: branch-local state wording | Step 8 in Startup Protocol |
| D4.5 `co.agent.md`: branch-local state wording | Step 5 in Startup Protocol |
| D4.6 `contracts.yaml`: first-push in feature/bug/refactor/docs/hotfix | `git_push(set_upstream=True)` instruction added after first commit step in all 5 workflows; hotfix additionally covered at setup step |

**Regression test coverage:** `tests/documentation/test_c4_doc_alignment.py` — 9 tests, all passing.

---

## Design and Approved Strategy Alignment

The Approved Strategy (from research) was:

> **Clean break** on the `mode` default: change from local-only to `mode="both"`. Breaking change documented with migration note. Protected-branch check always applies regardless of mode. Current-branch check skipped only for `mode="remote"`. Remote-absent is not an error.

All implementation choices honor this strategy:
- No backward-compat shim or legacy local-only fallback was added ✅
- Breaking change documented in `git.md` with `⚠️` callout and migration note ✅
- Architecture: tool → manager → adapter layering preserved; no cross-layer leakage ✅
- `BranchDeleteResult` is a frozen dataclass (pure value object) ✅
- No manager construction inside `execute()` paths ✅
- No hardcoded phase/workflow names introduced ✅

---

## Live Demonstration Proposal

The new behavior is directly observable via the MCP tool. A safe demo against a throwaway branch:

**Precondition:** a branch `demo/345-test` exists locally and has a remote tracking branch on `origin`.

**Demonstration steps:**
```text
1. git_delete_branch(branch="demo/345-test")
   → Expected: "Deleted branch: demo/345-test (local: deleted, remote: deleted)"
   → Before: only local deletion; remote would persist

2. git_delete_branch(branch="demo/345-test", mode="local")
   → Expected: "Deleted branch: demo/345-test (local: deleted)"
   → Confirms mode=local preserves old behavior

3. git_delete_branch(branch="demo/345-test", mode="remote")
   → Expected: "Deleted branch: demo/345-test (remote: deleted)"
   → No current-branch check; works even when demo/345-test is the active branch
```

**Observable evidence when no live remote exists:**  
The adapter unit tests `TestGitAdapterDeleteRemoteBranch` in `tests/mcp_server/unit/adapters/test_git_adapter.py` directly verify all three mode paths and the remote-absent no-error behavior against mocked git subprocess output.

---

## Residual Risks and Caveats

| Item | Risk | Severity |
|------|------|----------|
| Breaking default | Any caller passing no `mode` will now delete remote too. `git.md` documents this with a `⚠️ Breaking Change` note and migration path. | Low — documented; existing callers in the repo already use `mode="both"` intent |
| Epic workflow in `contracts.yaml` | D3.1 epic ready block was updated with a separate search/replace (different boilerplate wording). The 9 C4 regression tests do not cover the epic ready block explicitly. | Low — verified by @qa in C3 QA GO verdict |
| mypy gate skipped globally | Gate 4 (mypy) is globally skipped. Pyright (4b) and typed-mcp_server (4c) both pass. | Low — consistent with project-wide policy |
| `end-issue.prompt.md` has no automated test | The prompt is a @co operational script and is validated by human review. No pytest coverage. | Low — by design; prompts are not machine-testable |

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-25 | Agent (imp) | Initial validation report |
