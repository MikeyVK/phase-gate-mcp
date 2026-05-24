<!-- docs\development\issue345\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-24T18:51Z updated=2026-05-24 -->
# Planning: git_delete_branch remote deletion and lifecycle closeout alignment

**Status:** DRAFT
**Version:** 1.2
**Last Updated:** 2026-05-24

---

## Purpose

Translate the approved design and Approved Strategy for issue #345 into four sequential, implementation-sized cycles that make validation obligations explicit and prevent redesign from being hidden in implementation work.

## Scope

**In Scope:**
`GitDeleteBranchInput` mode enum and `BranchDeleteResult` value object, `GitManager.delete_branch` orchestration, `GitAdapter` remote-delete operation, lifecycle-exit prompt replacement (`end-issue.prompt.md`), ready-phase `contracts.yaml` deferred-work unification across six workflow blocks including issue-body verification and Closes #N obligations, `PRContext` schema extension, `pr.md.jinja2` template extension, and wording alignment across active documentation and agent instruction surfaces.

**Out of Scope:**
Multi-remote support, generic workflow redesign, `SubmitPRInput` tool schema changes, milestone management, exact commit-by-commit sequencing, and any production code beyond the four bounded cycle surfaces.

## Prerequisites

Read these first:
1. Approved Strategy in `docs/development/issue345/research.md` — binding for all cycles.
2. Design decisions in `docs/development/issue345/design.md` — planning boundary.
3. `docs/coding_standards/ARCHITECTURE_PRINCIPLES.md` — binding contract.
4. `docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md` — typing obligations for Cycle 1.

---

## Summary

This plan keeps issue #345 in four sequential cycles.

Cycle 1 delivers the `git_delete_branch` mode enum contract as an intentional breaking change. It is the most complex cycle because the adapter rename (`delete_branch` → `delete_local_branch` + new `delete_remote_branch`) has a hard blast radius into **five** existing test files that must be updated in the same cycle. Cycle 2 replaces the stale `close-issue.prompt.md` with a new `end-issue.prompt.md` matching the approved lifecycle-exit contract. Cycle 3 closes the design gap in the ready-phase runtime contract by updating six `contracts.yaml` workflow blocks to unify deferred-work into the PR body, add explicit Closes #N decision steps, closure-readiness review, and handover-template completeness check, and extends `PRContext` and the PR template to support deferred-work rendering. Cycle 4 aligns wording in active documentation and agent instruction surfaces.

This ordering keeps the code cycle self-contained, makes prompt and contract changes independent of each other, and leaves documentation as the final alignment pass after all behavioral surfaces are stable.

---

## Cycle Strategy

| Cycle | Focus | Why this boundary exists | Main affected surfaces | Primary proof |
|---|---|---|---|---|
| C1 | `git_delete_branch` mode enum + `BranchDeleteResult` | The adapter rename has a hard test blast radius that must be resolved in one slice; the enum contract is the foundation for `end-issue` usage in C2 | `git_tools.py`, `git_manager.py`, `git_adapter.py`, all five delete-branch test files (including `test_git_manager.py`) | All mode combinations pass; remote-absent returns `absent` not error; existing tests updated to new signature |
| C2 | `end-issue.prompt.md` — create and remove `close-issue` | Prompt replacement is isolated; no production code dependency; must be stable before C3 contracts reference it | `.github/prompts/close-issue.prompt.md` (delete), `.github/prompts/end-issue.prompt.md` (new) | Prompt file exists, matches contract-level flow from design 3.4; old file absent; @co ownership declared |
| C3 | Ready-phase PR body contract | Six `contracts.yaml` blocks + `PRContext` + `pr.md.jinja2` are one coherent surface; must be updated together to avoid partial runtime mismatches | `.phase-gate/config/contracts.yaml` (6 ready blocks), `mcp_server/schemas/contexts/pr.py`, `mcp_server/scaffolding/templates/concrete/pr.md.jinja2`, schema + template tests | Ready contracts carry deferred work into PR body; Closes #N and closure-readiness steps present; handover-template gate present; new PRContext fields round-trip through template |
| C4 | Documentation + wording alignment | Active docs and agent instructions must reflect C1 contract change and design wording decisions; deferred until behavioral surfaces are stable | `docs/reference/mcp/tools/git.md`, `docs/reference/mcp/MCP_TOOLS.md`, `docs/reference/mcp/tools/project.md`, `.github/agents/imp.agent.md`, `.github/agents/co.agent.md`, `contracts.yaml` first-push discipline | All wording checks pass; `state.json` no longer described as runtime-only; first-push on same todo line as first checkpoint commit |

---

## Dependencies

- C2 is logically before C3: the `end-issue` prompt should exist before the ready-phase contracts reference the end-issue ownership model in their wording. There is no hard code dependency.
- C1 is independent of C2, C3, and C4.
- C4 is independent but should follow C1 so the `git.md` documentation reflects the final mode enum contract.
- C3 is independent of C1 technically, but the `BranchDeleteResult` naming and mode semantics from C1 inform the wording in the ready-phase contracts.

---

## Cross-Cycle Obligations

### Approved Strategy Constraints

- C1 is an **intentional contract break** for existing callers: `mode="both"` becomes the default. All callers that relied on local-only behavior must explicitly pass `mode="local"`. No compatibility alias is permitted.
- C1 must preserve idempotent behavior: `mode="remote"` when the remote branch is already absent returns `absent`, not an error. `mode="both"` when either side is absent returns `absent` for that side, not a failure.
- C2 must not retain `close_issue()` as a normative step. It remains recovery-only when a merged PR body claimed closure but the issue is still open.
- C2 must not use `git_diff_stat(...)` as default merge-proof. `merge_pr(...)` is the authoritative merge signal.
- C3 must not modify `SubmitPRInput`; all deferred-work and tracking-state content travels as markdown sections within the existing free `body` field.
- C4 must correct `project.md` wording about `state.json` from "runtime, not committed" to "branch-local, committed with branch history until `submit_pr` neutralizes".

### Architecture Obligations

- `BranchDeleteResult` is a frozen value object. It must not carry workflow policy or adapter-internal details.
- `GitAdapter.delete_remote_branch` must not know about protected branches, workflow policy, or mode selection — those remain in `GitManager`.
- `GitManager.delete_branch` remains the single policy-enforcement boundary. The protected-branch guard applies before any deletion side is attempted.
- For `mode="remote"`, the current-branch check does **not** apply (local branch is not touched). For `mode="local"` and `mode="both"`, the current-branch check applies.
- No manager creation inside `execute()` paths. `GitDeleteBranchTool` receives `GitManager` by constructor injection, unchanged.
- `PRContext` fields must be optional with `None` defaults — existing callers that omit them must not break.

### Typing Obligations

- `mode: Literal["local", "remote", "both"]` on `GitDeleteBranchInput`. No string-typed fallback.
- `BranchDeleteResult`: `@dataclass(frozen=True)` with `local_status: Literal["deleted", "absent", "skipped"]` and `remote_status: Literal["deleted", "absent", "skipped"]`.
- `GitAdapter.delete_remote_branch` return type: `Literal["deleted", "absent"]`.
- No `# type: ignore` additions. No global mypy relaxations. Use `TYPE_CHECKING_PLAYBOOK.md` if a typing issue requires a targeted ignore.

### Quality Gate Obligations

- Run `run_quality_gates(scope="auto")` after each cycle's GREEN step and before committing REFACTOR.
- Ruff and mypy must pass at 10.00 / no errors on changed files after each cycle.
- Coverage: changed production lines must be exercised by new or updated tests.

---

## Cycle 1 — `git_delete_branch` Mode Enum

### Goal

Extend `git_delete_branch` with an explicit `mode` enum (`local`, `remote`, `both`) with `both` as the default, add `BranchDeleteResult` to carry per-side outcomes, add `GitAdapter.delete_remote_branch`, and update all **five** affected test files to the new signature.

### Deliverables

| ID | Deliverable | File |
|---|---|---|
| D1.1 | `GitDeleteBranchInput.mode: Literal["local","remote","both"] = "both"` | `mcp_server/tools/git_tools.py` |
| D1.2 | `GitDeleteBranchTool.execute` passes `mode` to manager; renders result per `BranchDeleteResult` | `mcp_server/tools/git_tools.py` |
| D1.3 | `BranchDeleteResult(frozen=True)` with `local_status` and `remote_status` typed as `Literal["deleted","absent","skipped"]` | `mcp_server/managers/git_manager.py` |
| D1.4 | `GitManager.delete_branch` orchestrates local/remote/both based on `mode`; returns `BranchDeleteResult`; current-branch check skipped for `mode="remote"` | `mcp_server/managers/git_manager.py` |
| D1.5 | `GitAdapter.delete_local_branch` (renamed from `delete_branch`) | `mcp_server/adapters/git_adapter.py` |
| D1.6 | `GitAdapter.delete_remote_branch(branch, remote="origin")` — returns `"deleted"` or `"absent"`; not an error when remote branch is already gone | `mcp_server/adapters/git_adapter.py` |
| D1.7 | `test_git_delete_branch_tool` updated; new tests for `mode="local"`, `mode="remote"`, `mode="both"`, remote-absent | `tests/mcp_server/unit/tools/test_git_tools.py` |
| D1.8 | `test_git_delete_branch_tool_flow` updated; new mode-coverage tests | `tests/mcp_server/unit/integration/test_all_tools.py` |
| D1.9 | `test_delete_branch_uses_git_config_protected` updated to new signature; new tests for remote/both modes | `tests/mcp_server/managers/test_git_manager_config.py` |
| D1.10 | `TestGitAdapterDeleteBranch` updated to `delete_local_branch`; new `TestGitAdapterDeleteRemoteBranch` tests including remote-absent | `tests/mcp_server/unit/adapters/test_git_adapter.py` |
| D1.11 | `TestGitManager.test_delete_branch_valid` and `test_delete_branch_protected` updated; mock assertions `delete_branch` → `delete_local_branch` | `tests/mcp_server/unit/managers/test_git_manager.py` |

### Exit Criteria

- All existing delete-branch tests green with the renamed adapter method.
- New tests cover: `mode="local"` (remote skipped), `mode="remote"` (local skipped, no current-branch check), `mode="both"` (both sides), remote-absent returns `absent` not error.
- `mode="both"` with missing local side returns `local_status="absent"`, not an error.
- `BranchDeleteResult` is a frozen dataclass with correct Literal types.
- mypy and ruff pass on all changed files.

---

## Cycle 2 — `end-issue.prompt.md` Lifecycle Exit Prompt

### Goal

Replace `close-issue.prompt.md` with a new `end-issue.prompt.md` that matches the approved contract-level flow from design section 3.4: one linear path, `git_delete_branch(mode="both")` for cleanup, PR-body `Closes #N` as the normative closure path, `close_issue()` recovery-only, no `git_diff_stat` as merge proof, and one conditional epic-parent step.

### Deliverables

| ID | Deliverable | File |
|---|---|---|
| D2.1 | `close-issue.prompt.md` deleted (not archived) | `.github/prompts/close-issue.prompt.md` |
| D2.2 | `end-issue.prompt.md` created with approved contract-level flow | `.github/prompts/end-issue.prompt.md` |

### Exit Criteria

- `close-issue.prompt.md` does not exist.
- `end-issue.prompt.md` exists with: `get_work_context()` → `merge_pr()` → `git_checkout(<parent>)` → `git_delete_branch(mode="both")` → read PR body → conditional epic-parent update → advisory next-issue recommendation.
- `end-issue.prompt.md` declares `@co` as the owning agent; human invocation is the merge-approval signal (no automated merge trigger).
- `close_issue()` is absent from the normative path and present only in the recovery section.
- `git_diff_stat` is absent from the normative merge-proof step.

---

## Cycle 3 — Ready-Phase PR Body Contract

### Goal

Close the runtime gap: update six `contracts.yaml` ready blocks to (1) unify deferred work into the PR body, (2) require explicit PR-body completeness verification including `Closes #N` decision steps, (3) mandate a closure-readiness review for all in-scope issues before merge, and (4) establish the handover template as the completeness-check gate. Also add `deferred_work` and `tracking_state` optional fields to `PRContext` and the corresponding rendering section to `pr.md.jinja2`.

### Deliverables

| ID | Deliverable | File |
|---|---|---|
| D3.1 | Six ready blocks updated: "Keep the PR narrative and the deferred-work transfer separate" instruction replaced by unified deferred-work-in-body instruction | `.phase-gate/config/contracts.yaml` (feature, bug, refactor, docs, hotfix, epic) |
| D3.2 | `PRContext.deferred_work: str \| None = None` | `mcp_server/schemas/contexts/pr.py` |
| D3.3 | `PRContext.tracking_state: str \| None = None` | `mcp_server/schemas/contexts/pr.py` |
| D3.4 | `pr.md.jinja2` renders a deferred-work section when `deferred_work` is set; renders tracking state when `tracking_state` is set | `mcp_server/scaffolding/templates/concrete/pr.md.jinja2` |
| D3.5 | Template tests extended to cover new deferred-work section rendering | `tests/mcp_server/scaffolding/test_task37_tracking_templates.py` |
| D3.6 | PRContext schema test extended to cover new optional fields | `tests/mcp_server/unit/schemas/test_tracking_artifact_v2_parity.py` |
| D3.7 | Six ready blocks updated: explicit `Closes #N` decision step (verify PR body contains correct close signals for all in-scope issues), closure-readiness review step, and handover-template-as-completeness-check obligation | `.phase-gate/config/contracts.yaml` (feature, bug, refactor, docs, hotfix, epic) |
| D3.8 | Six ready blocks updated: original issue body honesty check — before PR creation, verify that the original issue body still accurately describes branch intent and in-scope breadth; update the issue body when research widened or changed the scope | `.phase-gate/config/contracts.yaml` (feature, bug, refactor, docs, hotfix, epic) |

### Exit Criteria

- All six `contracts.yaml` ready blocks carry the unified deferred-work-in-body instruction; the "separate" instruction is absent from all six.
- All six `contracts.yaml` ready blocks include an explicit `Closes #N` decision step requiring the implementer to verify that the PR body contains correct close signals for every in-scope issue before the PR is submitted.
- All six `contracts.yaml` ready blocks include a closure-readiness review step (in-scope issues are in the expected open state at the time of merge; no orphan open issues).
- All six `contracts.yaml` ready blocks treat the handover template as a completeness check: the handover must be produced and checked as the final gate before PR submission.
- All six `contracts.yaml` ready blocks include an original-issue-body honesty check: before PR creation the implementer must verify whether the original issue body still accurately describes the branch intent and in-scope breadth; if research widened or changed the intended scope, the issue body must be updated before the PR is created.
- `PRContext` accepts `deferred_work` and `tracking_state` as optional string fields; existing callers that omit them still pass validation.
- Template renders a `## Deferred Work` section when `deferred_work` is provided; the section is absent when the field is `None`.
- All existing template and schema tests green; new tests green.
- mypy and ruff pass on all changed files.

---

## Cycle 4 — Documentation and Wording Alignment

### Goal

Align active documentation and agent instruction surfaces with the C1 contract change, the `state.json` wording decision, and the first-push discipline from the design.

### Deliverables

| ID | Deliverable | File |
|---|---|---|
| D4.1 | `git_delete_branch` entry updated: `mode` parameter documented, migration note added ("existing callers that omit `mode` now receive `both`; pass `mode="local"` to preserve local-only behavior"), examples for each mode | `docs/reference/mcp/tools/git.md` |
| D4.2 | `git_delete_branch` entry updated with same mode parameter and migration note | `docs/reference/mcp/MCP_TOOLS.md` |
| D4.3 | Line ~36: "`state.json`: Current branch state (runtime, not committed)" → "branch-local, committed with branch history; neutralized by `submit_pr` before merge" | `docs/reference/mcp/tools/project.md` |
| D4.4 | Explicit statement added: branch-local state artifacts (`.phase-gate/state.json`, `.phase-gate/deliverables.json`) travel with normal branch commits until `submit_pr` neutralizes them | `.github/agents/imp.agent.md` |
| D4.5 | Same branch-local state wording added | `.github/agents/co.agent.md` |
| D4.6 | feature/bug/refactor research commit step: `git_push(set_upstream=True)` added on the same todo line; docs planning commit step: same; hotfix first implementation commit step: same | `.phase-gate/config/contracts.yaml` |

### Exit Criteria

- `docs/reference/mcp/tools/git.md` and `docs/reference/mcp/MCP_TOOLS.md` document `mode` with all three values and the migration note.
- `project.md` no longer says "runtime, not committed" for `state.json`.
- Both `imp.agent.md` and `co.agent.md` contain an explicit branch-local state wording statement.
- `contracts.yaml` research/planning/implementation commit steps for feature/bug/refactor/docs/hotfix include `git_push(set_upstream=True)` on the same todo line as the commit.
- No ruff or mypy impact (documentation-only cycle).

---

## Risks and Unknowns

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Adapter rename impact exceeds the five planned test files — additional call sites exist in the codebase | Low | High | D1.11 explicitly covers `test_git_manager.py`; grep the full codebase before RED to confirm no other call sites remain outside planning scope |
| `mode="remote"` edge case: protected branch guard behavior when local branch does not exist | Low | Medium | Protected-branch check applies by branch name regardless of local existence; document the guard scope in the test |
| `contracts.yaml` six-block update introduces inconsistency between workflow-specific wording | Medium | Medium | Treat all six blocks as a single atomic edit; verify each block after edit |
| GitPython remote-push-delete API differs from local delete API | Medium | Low | Use `repo.git.push(remote, f"--delete {branch}")` pattern; check existing `push()` implementation in adapter for API reference |

## Open Questions

- **`BranchDeleteResult` location**: placed in `git_manager.py` as a module-level frozen dataclass (no `models/` package exists). Acceptable given the narrow blast radius and single consumer (tool → manager boundary).
- **Remote-absent normalization layer**: adapter returns `"deleted"` or `"absent"`; manager wraps into `BranchDeleteResult`; tool renders. The design question of "which layer normalizes" is resolved: adapter produces the raw side-outcome, manager assembles the result object.

## Related Documentation

- [docs/development/issue345/research.md](research.md)
- [docs/development/issue345/design.md](design.md)
- [docs/coding_standards/ARCHITECTURE_PRINCIPLES.md](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md](../../coding_standards/TYPE_CHECKING_PLAYBOOK.md)
- [docs/reference/mcp/tools/git.md](../../reference/mcp/tools/git.md)
- [docs/reference/mcp/tools/project.md](../../reference/mcp/tools/project.md)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-24 | Agent | Initial planning draft |
| 1.1 | 2026-05-24 | Agent | QA fixes: D1.11 added, C1 exit criteria tightened (mode=both absent), C2 exit criteria @co-owned + human-approval signal, C3 expanded with Closes #N / closure-readiness / handover-template gate, adapter rename risk reformulated |
| 1.2 | 2026-05-24 | Agent | QA fix: D3.8 added (issue-body honesty check before PR creation) |
