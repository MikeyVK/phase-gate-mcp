<!-- docs\development\issue345\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-24T14:11Z updated= -->
# git_delete_branch remote deletion support

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-24

---

## Purpose

Investigate the current branch-deletion behavior and capture the compatibility strategy and constraints that later design and planning must respect.

## Scope

**In Scope:**
`git_delete_branch` behavior, its input/output contract, underlying GitManager and GitAdapter deletion flow, existing remote-operation patterns, affected tests and documentation, and the compatibility policy for optional remote deletion.

**Out of Scope:**
Implementing the change, redesigning branch cleanup flows beyond this tool, adding multi-remote support, changing unrelated git tools, or introducing a generic remote-cleanup framework.

## Prerequisites

Read these first:
1. Issue #345
2. docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
3. docs/coding_standards/DOCUMENTATION_STANDARD.md
---

## Problem Statement

`git_delete_branch` currently deletes only local branches. Closing a merged branch still requires a separate host-side `git push origin --delete <branch>` command, which breaks the MCP-tool-first workflow and leaves close-out cleanup split across two execution surfaces. The requested change must preserve the existing local-only default while adding an explicit path to remove the matching remote branch as part of the same tool flow.

## Research Goals

- Identify the exact code path and contracts that currently make `git_delete_branch` local-only.
- Determine the smallest coherent blast radius across tool, manager, adapter, docs, and tests.
- Capture reusable remote-operation patterns already present in the repository.
- Record the approved compatibility strategy for adding remote deletion without widening scope into multi-remote or generic cleanup redesign.

---

## Background

Repo-only research; no external research was requested.

The issue was raised from the close-out flow after PR #344, where the local branch could be removed through MCP tooling but the remote branch still required a manual terminal command. The current execution path is narrow and evidence-backed:

- `GitDeleteBranchTool.execute()` in `mcp_server/tools/git_tools.py` calls `GitManager.delete_branch(...)` and returns a fixed local-delete success message.
- `GitManager.delete_branch()` in `mcp_server/managers/git_manager.py` enforces protected-branch policy, then delegates directly to `GitAdapter.delete_branch(...)`.
- `GitAdapter.delete_branch()` in `mcp_server/adapters/git_adapter.py` only checks `self.repo.heads`, prevents deleting the active local branch, and calls `self.repo.delete_head(...)`.
- The public tool reference in `docs/reference/mcp/tools/git.md` explicitly documents that remote branches are not deleted.

Existing remote-aware git behavior in this repository already centers on the `origin` remote. `GitAdapter.push()`, `pull()`, and `fetch()` use origin-oriented patterns, which is relevant because the issue request also names `git push origin --delete <branch>` as the desired remote deletion shape.

---

## Findings

### Current Behavior

| Surface | Evidence | Research consequence |
|---|---|---|
| Tool layer | `mcp_server/tools/git_tools.py` defines `GitDeleteBranchInput(branch, force)` and returns `Deleted branch: {branch}` after `manager.delete_branch(...)` | Public tool contract is currently local-only and additive extension is the lowest-risk path |
| Manager layer | `mcp_server/managers/git_manager.py` blocks protected branches, then delegates to the adapter | Protected-branch policy already has a single enforcement point that later phases must preserve |
| Adapter layer | `mcp_server/adapters/git_adapter.py` only checks local heads and deletes via `repo.delete_head(...)` | Local-only behavior is rooted in the adapter, not only in tool messaging |
| Public docs | `docs/reference/mcp/tools/git.md` explicitly says remote branches are not deleted | Documentation and tool contract must be updated together |

### Likely Blast Radius

**Production surfaces**
- `mcp_server/tools/git_tools.py`
- `mcp_server/managers/git_manager.py`
- `mcp_server/adapters/git_adapter.py`
- `docs/reference/mcp/tools/git.md`

**Likely affected automated coverage**
- `tests/mcp_server/unit/tools/test_git_tools.py`
- `tests/mcp_server/unit/managers/test_git_manager.py`
- `tests/mcp_server/unit/adapters/test_git_adapter.py`
- `tests/mcp_server/unit/integration/test_all_tools.py`

### Existing Patterns / Prior Art

- Remote git operations already exist in the adapter through `fetch()`, `pull()`, and `push()`.
- Those flows are `origin`-centric today; no repo evidence suggests multi-remote support is a current requirement.
- Issue #137 research and design around remote checkout already treated `origin` as the supported remote boundary and explicitly deferred broader remote behavior.

### Architectural Constraints

- Keep the change constructor-injected and inside the existing tool → manager → adapter layering.
- Preserve the existing protected-branch guard instead of duplicating branch-policy checks elsewhere.
- Do not widen this issue into a generic branch-cleanup or workflow-closeout framework.
- Preserve backward compatibility for callers that use the current local-only default path.

### Risks, Assumptions, And Unknowns

- The main compatibility risk is output and error semantics when remote deletion is requested but the remote branch is already absent.
- Repo evidence supports an `origin`-only boundary, but later phases must avoid silently implying broader multi-remote support.
- Later phases must decide where to normalize the mixed-outcome case so callers get a clear result when local deletion succeeds but remote deletion is a no-op.

### Expected Results For Design And Planning

- Add an explicit remote-deletion option without breaking existing local-only callers.
- Support the requested one-go cleanup path where local and remote deletion can be triggered together.
- Keep the change confined to the existing git deletion surfaces plus their tests and docs.

### Approved Strategy

| Boundary / consumer scope | Selected strategy | Rationale | Constraints for later phases |
|---|---|---|---|
| Existing `git_delete_branch` callers | Preserve compatibility | The default local-only contract must remain unchanged | Keep `remote=False` as the default behavior |
| Close-out callers that need one-go cleanup | Additive extension | The user explicitly wants local and remote deletion in the same flow when requested | Support a single tool path that can remove local and remote without requiring a second terminal command |
| Remote-absent case | Idempotent non-error handling | The issue text explicitly asks for a clear message instead of an error when the remote branch is already absent | Later phases must return a clear result for `remote=True` even when there is nothing left to delete remotely |
| Remote boundary | Preserve current supported contract | Repo prior art is `origin`-centric and there is no current requirement for broader remote routing | Do not widen this issue into multi-remote support without a separate decision |

## Open Questions

- ❓ How should the final success text distinguish between three materially different outcomes: local-only deletion, local-plus-remote deletion, and remote-already-absent cleanup?
- ❓ At which layer should the remote-absent case be normalized so the tool stays clear for callers without leaking adapter-specific details into the wrong abstraction?


## Related Documentation
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-1]**
- **[docs/coding_standards/DOCUMENTATION_STANDARD.md][related-2]**
- **[docs/reference/mcp/tools/git.md][related-3]**
- **[docs/development/archive/issue137/design.md][related-4]**
- **[docs/development/archive/issue137/planning.md][related-5]**

<!-- Link definitions -->

[related-1]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-2]: docs/coding_standards/DOCUMENTATION_STANDARD.md
[related-3]: docs/reference/mcp/tools/git.md
[related-4]: docs/development/archive/issue137/design.md
[related-5]: docs/development/archive/issue137/planning.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |