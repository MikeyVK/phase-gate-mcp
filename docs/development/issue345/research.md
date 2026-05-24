<!-- docs\development\issue345\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-24T14:11Z updated=2026-05-24 -->
# git_delete_branch remote deletion support

**Status:** DRAFT  
**Version:** 1.2  
**Last Updated:** 2026-05-24

---

## Purpose

Investigate the current branch-deletion behavior and capture the compatibility strategy and adjacent workflow-contract findings that later design, planning, documentation, and implementation must respect.

## Scope

**In Scope:**
`git_delete_branch` behavior, its input/output contract, underlying GitManager and GitAdapter deletion flow, existing remote-operation patterns, affected tests and documentation, the compatibility policy for optional remote deletion, the current lifecycle-exit prompt contract as it relates to branch cleanup, the ready-phase PR-closeout gaps surfaced during this investigation, and the branch-local state / upstream-discipline findings approved by the user for the same branch and PR.

**Out of Scope:**
Implementing the change, writing the design document, editing `contracts.yaml` during research, changing `git_add_or_commit` semantics, redesigning branch cleanup flows beyond the bounded close-out surfaces identified here, adding multi-remote support, or changing unrelated git tools.

## Prerequisites

Read these first:
1. Issue #345
2. docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
3. docs/coding_standards/DOCUMENTATION_STANDARD.md

---

## Problem Statement

`git_delete_branch` currently deletes only local branches. Closing a merged branch still requires a separate host-side `git push origin --delete <branch>` command, which breaks the MCP-tool-first workflow and leaves close-out cleanup split across two execution surfaces. The requested change must preserve the existing local-only default while adding an explicit path to remove the matching remote branch as part of the same tool flow.

During the same investigation, adjacent workflow-contract gaps were confirmed and approved for inclusion on this branch: the current lifecycle-exit prompt still models an older `close_issue`-driven contract, the ready phase does not explicitly verify issue-body readiness or decide whether the PR should contain `Closes #N`, and active documentation still conflicts with the intended branch-local state discipline for `.phase-gate/state.json` and `.phase-gate/deliverables.json`.

## Research Goals

- Identify the exact code path and contracts that currently make `git_delete_branch` local-only.
- Determine the smallest coherent blast radius across tool, manager, adapter, docs, and tests.
- Capture reusable remote-operation patterns already present in the repository.
- Record the approved compatibility strategy for adding remote deletion without widening scope into multi-remote or generic cleanup redesign.
- Record the approved lifecycle-exit, ready-phase, and branch-state findings that this branch is now also expected to carry forward.

---

## Background

Repo-only research; no external research was requested.

The issue was raised from the close-out flow after PR #344, where the local branch could be removed through MCP tooling but the remote branch still required a manual terminal command. The current execution path is narrow and evidence-backed:

- `GitDeleteBranchTool.execute()` in `mcp_server/tools/git_tools.py` calls `GitManager.delete_branch(...)` and returns a fixed local-delete success message.
- `GitManager.delete_branch()` in `mcp_server/managers/git_manager.py` enforces protected-branch policy, then delegates directly to `GitAdapter.delete_branch(...)`.
- `GitAdapter.delete_branch()` in `mcp_server/adapters/git_adapter.py` only checks `self.repo.heads`, prevents deleting the active local branch, and calls `self.repo.delete_head(...)`.
- The public tool reference in `docs/reference/mcp/tools/git.md` explicitly documents that remote branches are not deleted.

Existing remote-aware git behavior in this repository already centers on the `origin` remote. `GitAdapter.push()`, `pull()`, and `fetch()` use origin-oriented patterns, which is relevant because the issue request also names `git push origin --delete <branch>` as the desired remote deletion shape.

During this research session, the user also supplied an approved `@co -> @imp` hand-over extending the research scope on the same branch. That hand-over added two adjacent findings to capture now rather than deferring them silently: the lifecycle-exit prompt contract should move from `close-issue.prompt.md` to a new `end-issue.prompt.md`, and the ready phase contains a PR-closeout gap around issue-body verification and explicit `Closes #N` decision-making.

---

## Findings

### F_345.1 - `git_delete_branch` is currently local-only end to end

| Surface | Evidence | Research consequence |
|---|---|---|
| Tool layer | `mcp_server/tools/git_tools.py` defines `GitDeleteBranchInput(branch, force)` and returns `Deleted branch: {branch}` after `manager.delete_branch(...)` | Public tool contract is currently local-only and additive extension is the lowest-risk path |
| Manager layer | `mcp_server/managers/git_manager.py` blocks protected branches, then delegates to the adapter | Protected-branch policy already has a single enforcement point that later phases must preserve |
| Adapter layer | `mcp_server/adapters/git_adapter.py` only checks local heads and deletes via `repo.delete_head(...)` | Local-only behavior is rooted in the adapter, not only in tool messaging |
| Public docs | `docs/reference/mcp/tools/git.md` explicitly says remote branches are not deleted | Documentation and tool contract must be updated together |

### F_345.2 - Existing remote git behavior already follows an `origin`-centric pattern

- Remote git operations already exist in the adapter through `fetch()`, `pull()`, and `push()`.
- Those flows are `origin`-centric today; no repo evidence suggests multi-remote support is a current requirement.
- Issue #137 research and design around remote checkout already treated `origin` as the supported remote boundary and explicitly deferred broader remote behavior.

Research consequence: later phases should reuse the existing `origin`-first boundary unless a separate issue deliberately broadens the remote contract.

### F_345.3 - The current GitHub PR -> merge tool path technically requires a remote branch

Repo evidence shows no blanket requirement that every local git branch must exist remotely. A fully local branch can exist as long as the workflow stays on local git operations. However, once the workflow uses the repository's GitHub PR -> merge path, a remote branch becomes a technical prerequisite on the current implementation:

- `GitManager.prepare_submission()` in `mcp_server/managers/git_manager.py` blocks when no upstream tracking branch exists and tells the caller to run `git_push(set_upstream=True)` first.
- `SubmitPRTool` in `mcp_server/tools/pr_tools.py` always calls `prepare_submission()`, always pushes, and then calls `GitHubManager.create_pr(...)`.
- `GitHubAdapter.create_pr()` in `mcp_server/adapters/github_adapter.py` calls `repo.create_pull(...)`, which depends on the head branch existing on GitHub.
- `merge_pr` operates on an existing GitHub pull request, so the merge half of that path is unavailable until the PR exists.

Research consequence: later phases should not model remote branch creation as globally mandatory for raw git branching, but they must model it as technically mandatory whenever the workflow is expected to use `submit_pr` and `merge_pr`.

### F_345.4 - The current lifecycle-exit prompt still models an older `close_issue`-driven contract

The active prompt surface in `.github/prompts/close-issue.prompt.md` does not match the approved exit model now in scope for this branch:

- the file name is still `close-issue.prompt.md`, not the approved symmetric `end-issue.prompt.md`
- the prompt still splits non-epic and epic paths instead of using one linear flow with one conditional epic step
- the non-epic path still calls `close_issue(issue_number=ISSUE_NUMBER)` directly
- the epic path treats remote cleanup as an outcome to verify because no MCP delete-both capability exists yet

The approved user direction captured during this research is narrower and different:

- replace `close-issue.prompt.md` with `end-issue.prompt.md`
- remove the old file rather than archive it
- treat prompt invocation itself as the human-approval signal
- make `close_issue` non-normative for lifecycle exit; issue closure belongs in the PR body via GitHub `Closes #N`
- use one linear end-of-issue flow with only one conditional step for epic parent branches
- rely on issue #345 to provide the local+remote branch deletion capability that the end-of-issue flow needs

Research consequence: the lifecycle-exit prompt contract is stale against the approved user direction and against the close-out cleanup capability that issue #345 is intended to add.

### F_345.5 - The ready phase has a PR-closeout gap in feature, bug, and refactor workflows

The active ready-phase instructions for `feature`, `bug`, and `refactor` workflows all share the same structure:

- they call `get_project_plan(issue_number=N)`, `get_work_context`, and `get_issue(issue_number=N)`
- they require validation evidence and PR scaffolding
- they populate PR scaffold context with `closes_issues: [N] when the PR closes the issue`

But they do not currently include the explicit closeout checks that the approved end-of-issue model depends on:

1. verify whether the original issue body still honestly reflects the intended scope when research has broadened or clarified that scope
2. explicitly review which issues claimed as in scope are actually closure-ready on this branch
3. explicitly encode only those closure-ready issues in the PR body via `Closes #N`

Research consequence: the current ready-phase contract leaves closure-readiness and `Closes #N` decisions too implicit, which makes the close-out prompt depend on work that the ready phase does not yet explicitly require.

### F_345.6 - Branch-local state discipline is modeled inconsistently across contracts, docs, and role surfaces

Several active sources agree that `.phase-gate/state.json` and `.phase-gate/deliverables.json` are branch-local artifacts that must not reach `main`, but the repository does not yet describe their branch-history discipline consistently:

- `.phase-gate/config/contracts.yaml` marks both files as branch-local artifacts under merge policy and the ready phase explicitly says to commit the final `.phase-gate/state.json` audit trail before PR preparation when present
- `submit_pr` neutralizes branch-local artifacts before PR submission
- `.github/prompts/start-issue.prompt.md` already encodes the epic-versus-child ownership split correctly: `@co` performs first commit and push on epic branches, while non-epic branches hand off to `@imp` before the first commit and push
- `docs/reference/mcp/tools/project.md` still says `.phase-gate/state.json` is runtime and not committed
- `.github/agents/imp.agent.md` and `.github/agents/co.agent.md` define who may commit and push, but do not yet state the explicit responsibility for carrying branch-local state artifacts with normal branch commits

Research consequence: the inconsistency is not about whether these files may reach `main`; that rule already exists. The unresolved gap is that the active instructions and reference docs do not yet consistently state that the state artifacts are supposed to travel with the branch history until `submit_pr` neutralizes them.

### F_345.7 - The repository already has the right role split for first push, but the first child-workphase final commit step does not yet encode it

The approved operating rule is now explicit for this branch and should be preserved in later phases:

- epic branch bootstrap remains a `@co` responsibility and already includes first commit plus `git_push(set_upstream=true)` in `.github/prompts/start-issue.prompt.md`
- child issue branches remain an `@imp` responsibility after the `@co` hand-off
- `@qa` has no role in branch bootstrapping, upstream creation, or state-artifact responsibility
- for child workflows, the first remote push should not be introduced as a separate extra todo; it should be attached to the existing final commit step of the first active workphase for that workflow

Research consequence: later phases should preserve this role boundary and encode `git_push(set_upstream=true)` inside the existing final commit checkpoint of the first child workphase in each relevant workflow, rather than flattening everything into a generic auto-push rule or a standalone push checklist item.

### F_345.8 - The adjacent findings are approved as same-branch scope, but remain secondary to the primary git-delete capability

The user explicitly approved that the lifecycle-exit prompt finding, the ready-phase gap, and the branch-state / upstream-discipline findings are to be carried in this same branch and PR. They are adjacent to the primary `git_delete_branch` scope, not a replacement for it.

Research consequence: later phases must keep `git_delete_branch` remote deletion support as the leading implementation target while treating the prompt, contract, and documentation findings as coupled follow-up surfaces in the same branch.

---

## Likely Blast Radius

**Primary production surfaces**
- `mcp_server/tools/git_tools.py`
- `mcp_server/managers/git_manager.py`
- `mcp_server/adapters/git_adapter.py`
- `docs/reference/mcp/tools/git.md`

**Adjacent workflow-contract and documentation surfaces approved for the same branch**
- `.github/prompts/close-issue.prompt.md`
- future `.github/prompts/end-issue.prompt.md`
- `.github/prompts/start-issue.prompt.md` as the symmetry and ownership reference surface
- `.phase-gate/config/contracts.yaml`
- `.github/agents/imp.agent.md`
- `.github/agents/co.agent.md`
- `docs/reference/mcp/tools/project.md`
- `docs/reference/mcp/tools/github.md`

**Likely affected automated or review-sensitive coverage**
- `tests/mcp_server/unit/tools/test_git_tools.py`
- `tests/mcp_server/unit/managers/test_git_manager.py`
- `tests/mcp_server/unit/adapters/test_git_adapter.py`
- `tests/mcp_server/unit/integration/test_all_tools.py`
- prompt and documentation review remains partly manual; no dedicated prompt-validation suite was confirmed during this research

### Existing Patterns / Prior Art

- Remote git operations already exist in the adapter through `fetch()`, `pull()`, and `push()`.
- The repository already uses an explicit role split at branch start: epic bootstrap stays with `@co`, while child issue execution hands off to `@imp`.
- `submit_pr` already models the traceability-first PR path as an atomic neutralize → commit → push → create-PR flow.
- The ready-phase scaffold pattern is shared across feature, bug, and refactor workflows, which means the current closeout gap is repeated rather than isolated.
- `start-issue.prompt.md` already provides the naming and ownership symmetry that the approved `end-issue.prompt.md` direction wants to preserve.

### Architectural Constraints

- Keep the change constructor-injected and inside the existing tool → manager → adapter layering.
- Preserve the existing protected-branch guard instead of duplicating branch-policy checks elsewhere.
- Preserve the explicit epic-versus-child ownership split: `@co` owns epic branch bootstrap, `@imp` owns child-issue execution after hand-off, and `@qa` remains outside branch-bootstrapping responsibilities.
- Treat `.phase-gate/state.json` and `.phase-gate/deliverables.json` as branch-local artifacts that travel with branch history but are prevented from reaching `main` by merge policy and `submit_pr` neutralization.
- Do not widen this issue into a generic branch-cleanup framework, a generic workflow-closeout redesign, or a multi-remote git feature.
- Do not silently redefine `git_add_or_commit` as an always-push operation; if PR-traceability workflow policy requires upstream creation, later phases should encode that explicitly in the relevant role and phase contracts.

### Risks, Assumptions, And Unknowns

- The main `git_delete_branch` compatibility risk remains output and error semantics when remote deletion is requested but the remote branch is already absent.
- Repo evidence supports an `origin`-only boundary, but later phases must avoid silently implying broader multi-remote support.
- Later phases must decide where to normalize the mixed-outcome case so callers get a clear result when local deletion succeeds but remote deletion is a no-op.
- The adjacent prompt and contract findings are already user-approved, but they still need later phases to translate them into concrete docs and contract edits without blurring role boundaries.

### Expected Results For Design And Planning

- Add an explicit remote-deletion option without breaking existing local-only callers.
- Support the requested one-go cleanup path where local and remote deletion can be triggered together.
- Replace the stale close-out prompt contract with the approved `end-issue` model in later phases.
- Add explicit issue-body verification and explicit `Closes #N` decision points to the ready-phase contract where PR closeout is prepared.
- Align active documentation and role instructions so branch-local state artifacts are described consistently as branch-tracked, branch-local inputs to the PR-driven merge workflow.

### Approved Strategy

| Boundary / consumer scope | Selected strategy | Rationale | Constraints for later phases |
|---|---|---|---|
| Existing `git_delete_branch` callers | Preserve compatibility | The default local-only contract must remain unchanged | Keep `remote=False` as the default behavior |
| Close-out callers that need one-go cleanup | Additive extension | The user explicitly wants local and remote deletion in the same flow when requested | Support a single tool path that can remove local and remote without requiring a second terminal command |
| Remote-absent case | Idempotent non-error handling | The issue text explicitly asks for a clear message instead of an error when the remote branch is already absent | Later phases must return a clear result for `remote=True` even when there is nothing left to delete remotely |
| Remote boundary | Preserve current supported contract | Repo prior art is `origin`-centric and there is no current requirement for broader remote routing | Do not widen this issue into multi-remote support without a separate decision |
| GitHub PR -> merge path | Preserve remote-branch requirement for the GitHub PR tool path | The current `submit_pr` / `merge_pr` flow technically requires upstream tracking and a GitHub-visible head branch | Do not model remote branch existence as a universal git requirement, but do model it as required whenever the workflow is expected to use `submit_pr` and `merge_pr` |
| Lifecycle-exit prompt contract | Clean break to a new `end-issue` prompt | The current `close-issue` prompt name and flow no longer fit the approved lifecycle-exit model | Remove `close-issue.prompt.md` rather than archive it; later phases should introduce `end-issue.prompt.md` with one linear flow, no normative `close_issue` call, and only one conditional epic-parent update step |
| Ready-phase PR closure decision | Make the decision explicit in ready, not implicit in close-out | The approved end-of-issue flow depends on PR body closure behavior that the current ready phase does not explicitly decide | Later phases must add explicit issue-body verification and explicit `Closes #N` decision steps to the relevant ready-phase instructions before PR scaffolding |
| Branch-local state artifacts | Preserve git-tracked branch-local state on work branches | The state artifacts are the branch-local workflow backbone across machines, but merge policy already forbids them from reaching `main` | Later phases must stop describing `.phase-gate/state.json` as runtime-only or uncommitted and must preserve `submit_pr` neutralization before merge |
| First push responsibility | Keep the role split explicit and attach first push to the existing first-workphase final commit | Epic branch startup and child branch execution have different owners by design, and the user-approved workflow does not want a separate standalone push todo | Preserve `@co` first commit + push on epic startup, preserve `@imp` ownership of first child-branch commit/push after hand-off, encode `git_push(set_upstream=true)` inside the existing final commit step of the first child workphase for each relevant workflow, and keep `@qa` out of this responsibility model |

## Open Questions

- ❓ How should the final `git_delete_branch` success text distinguish between local-only deletion, local-plus-remote deletion, and remote-already-absent cleanup?
- ❓ At which layer should the remote-absent case be normalized so the tool stays clear for callers without leaking adapter-specific details into the wrong abstraction?

## Related Documentation
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-1]**
- **[docs/coding_standards/DOCUMENTATION_STANDARD.md][related-2]**
- **[docs/reference/mcp/tools/git.md][related-3]**
- **[docs/reference/mcp/tools/github.md][related-4]**
- **[docs/reference/mcp/tools/project.md][related-5]**
- **[docs/development/archive/issue137/design.md][related-6]**
- **[docs/development/archive/issue137/planning.md][related-7]**
- **[.github/prompts/start-issue.prompt.md][related-8]**
- **[.github/prompts/close-issue.prompt.md][related-9]**
- **[.phase-gate/config/contracts.yaml][related-10]**
- **[.github/agents/imp.agent.md][related-11]**
- **[.github/agents/co.agent.md][related-12]**

<!-- Link definitions -->

[related-1]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-2]: docs/coding_standards/DOCUMENTATION_STANDARD.md
[related-3]: docs/reference/mcp/tools/git.md
[related-4]: docs/reference/mcp/tools/github.md
[related-5]: docs/reference/mcp/tools/project.md
[related-6]: docs/development/archive/issue137/design.md
[related-7]: docs/development/archive/issue137/planning.md
[related-8]: .github/prompts/start-issue.prompt.md
[related-9]: .github/prompts/close-issue.prompt.md
[related-10]: .phase-gate/config/contracts.yaml
[related-11]: .github/agents/imp.agent.md
[related-12]: .github/agents/co.agent.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.1 | 2026-05-24 | Agent | Expanded research scope with approved lifecycle-exit, ready-phase, and branch-state discipline findings; recorded additional approved strategy boundaries |
| 1.0 | 2026-05-24 | Agent | Initial draft |
