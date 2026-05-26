<!-- docs\development\issue354\research.md -->
<!-- template=research version=research created=2026-05-26 updated=2026-05-26 -->
# Issue #354 — Add get_pr tool: narrow GitHub pulls API wrapper for end-issue flow

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-26

---

## Purpose

Establish the exact upstream pull-request response shape, the local blast radius, and the strategy boundary for adding a read-only `get_pr(pr_number)` tool that gives `end-issue` the canonical PR data it actually needs after branch-local state has been neutralized: merge and branch metadata plus the PR body as the durable source for deferred-work follow-up.

## Scope

**In Scope:**
`mcp_server/adapters/github_adapter.py`; `mcp_server/managers/github_manager.py`; `mcp_server/tools/pr_tools.py`; GitHub tool registration in `mcp_server/server.py`; `.github/prompts/end-issue.prompt.md`; direct unit coverage for adapter, manager, PR tools, and server registration.

**Out of Scope:**
`merge_pr` behavior changes; `submit_pr` transaction changes; changing `get_work_context()` semantics; widening GitHub tooling availability without token; redesigning unrelated PR tooling; any compatibility bridge that keeps `parent_branch` on `get_work_context()` as the authoritative source after cleanup.

---

## Problem Statement

`.github/prompts/end-issue.prompt.md` currently loads `parent_branch` from `get_work_context()` before merge and stops if `parent_branch` is missing. That is fragile once branch-local state has been neutralized, because `parent_branch` is phase-state derived rather than host-side PR metadata. The codebase already has local access to PyGithub `PullRequest` objects, but there is no dedicated `get_pr` tool exposing the narrow PR metadata the prompt needs.

## Research Goals

- Confirm the exact GitHub pulls API response fields needed for a narrow `get_pr` tool.
- Map the production and test blast radius for adding `get_pr` and updating the `end-issue` flow.
- Identify the closest existing repo patterns for adapter, manager, tool, and server registration.
- Establish the Approved Strategy for the parent-branch retrieval boundary and surface any remaining strategy-sensitive gaps.

---

## Findings

### Finding 1 — The upstream pull-request resource already contains the required branch and merge metadata

The GitHub REST pulls docs page for API version `2026-03-10` includes the single-PR resource in the same endpoint family as `List pull requests`, `List commits on a pull request`, and `Merge a pull request`. The fetched docs content confirms that the pull-request resource shape contains the fields this issue expects, including:

- `number`
- `title`
- `state`
- `base` object, including `base.ref`
- `head` object, including `head.ref`
- `merged_at`
- `merge_commit_sha`
- `body`

The docs payload also shows that the pull-request resource schema requires `base`, `head`, `merged_at`, `number`, `state`, `title`, and `body`. This means the host-side PR resource already carries both the branch metadata needed for checkout and the body needed by the durable handover step in `end-issue`.

**Repo-local semantic mapping:**

| Upstream PR resource | Narrow local field |
|---|---|
| `number` | `pr_number` |
| `title` | `title` |
| `state` | `state` |
| `base.ref` | `base_branch` |
| `head.ref` | `head_branch` |
| `merged_at` | `merged_at` |
| `merge_commit_sha` | `merge_sha` |
| `body` | `body` |

`state` alone is not sufficient to distinguish merged vs closed-unmerged PRs. `merged_at` must remain nullable and preserved in the local contract.

### Finding 2 — The repo already has the adapter seam, but not the read-only tool surface

`GitHubAdapter` already wraps GitHub PR operations for:

- `create_pr(...)`
- `list_prs(...)`
- `merge_pr(...)`

There is no `get_pr(...)` adapter method today, but the codebase already reaches the underlying PyGithub seam directly in existing PR code. `MergePRTool.execute()` currently does:

- `self.manager.adapter.repo.get_pull(params.pr_number)`

before calling `manager.merge_pr(...)`, in order to resolve `head.ref` for PR-status cleanup. This confirms that the local integration already trusts PyGithub `PullRequest` objects as the host-side source of truth.

The missing piece is not host capability. The missing piece is a first-class read-only path that narrows the upstream PR object into a stable tool contract.

### Finding 3 — The local layering pattern is mixed, but there is a coherent narrow-contract path

Relevant existing patterns:

- `GetIssueTool` is the nearest read-only GitHub tool pattern. It calls `manager.get_issue(...)` and renders a human-readable text result.
- `ListPRsTool` renders text directly from raw PyGithub PR objects and already reads `pr.base.ref` and `pr.head.ref`.
- `GitHubManager.create_pr(...)` already normalizes a raw PR object into a narrow dict containing only `number`, `url`, and `title`.

This issue is closer to `create_pr(...)` than to `list_prs(...)`: the request is explicitly for a narrow, stable response shape rather than a raw PyGithub surface. The cleanest layering is therefore:

1. adapter fetches the raw `PullRequest`
2. manager narrows it to a small dict contract
3. tool renders only the supported fields from that dict

That keeps PyGithub object knowledge out of the prompt-facing tool contract.

### Finding 4 — Server registration and auth policy are part of the boundary

`mcp_server/server.py` currently registers PR tools only when a GitHub token is configured:

- `list_prs`
- `merge_pr`
- `submit_pr`

Without a token, the server still registers issue tools, but not PR tools.

The upstream GitHub docs note that some pull-read endpoints can read public resources without authentication. That does **not** imply this repo should change its local tool-registration policy in issue #354. Doing so would widen the auth model beyond the existing PR-tool boundary and is out of scope for this issue.

### Finding 5 — The prompt consumer change is narrow, but it does not eliminate `get_work_context()` entirely

`.github/prompts/end-issue.prompt.md` currently does this in step 1:

- call `get_work_context()`
- record `branch`, `workflow`, `issue_number`, and `parent_branch`
- stop if `parent_branch` is missing

For issue #354, only the **source of truth** for the parent branch needs to move. The most coherent consumer change is:

- `get_pr(pr_number=PR_NUMBER)` becomes the authoritative source for `base_branch`
- `get_work_context()` remains available for `branch`, `workflow`, and fallback `issue_number` derivation when the invocation omitted it
- `merge_pr(...)` remains the authoritative merge proof; `get_pr(...)` must not replace it

This keeps the change additive instead of silently redefining `get_work_context()`.

### Finding 6 — The PR body belongs in the `get_pr(...)` contract for this workflow

Step 5 of `.github/prompts/end-issue.prompt.md` says:

- read the PR body as the durable `@imp` -> `@co` transfer artifact

For this workflow, that is not incidental metadata. The PR body is the operational handover surface used to inspect delivered scope, deferred work, and any follow-up issue creation that may still be required after merge.

That makes the contract boundary explicit:

- the upstream PR resource already exposes `body`
- the `end-issue` consumer needs `body`
- the issue being closed is no longer the authoritative source at that point in the lifecycle

For issue #354, `get_pr(...)` should therefore include `body` as part of the supported contract rather than forcing a second tool lookup against the issue surface.

### Finding 7 — Validation blast radius is straightforward and already has local precedents

| Layer | Existing precedent | Expected new coverage |
|---|---|---|
| Adapter | `test_github_adapter.py` already covers `list_prs(...)` and `merge_pr(...)` | add `get_pr(...)` success, 404, and generic API error cases |
| Manager | `test_github_manager.py` already covers `create_pr(...)`, `list_prs(...)`, and `merge_pr(...)` | add `get_pr(...)` delegation and narrow-field normalization |
| Tool | `test_pr_tools.py` already covers `list_prs` and `merge_pr` | add `GetPRTool` happy-path and not-found formatting |
| Server | `test_server.py` already checks GitHub tool registration | add `get_pr` registration alongside other PR tools |
| Prompt | no automated `end-issue` prompt coverage exists | manual prompt review is required unless prompt-test infrastructure is added separately |

---

## Architectural Constraints

| Constraint | Source / rationale |
|---|---|
| Keep `merge_pr(...)` as the authoritative merge proof | `end-issue.prompt.md` guardrails and current workflow contract |
| Do not repurpose `get_work_context()` into host-side PR lookup | issue scope is additive tooling, not lifecycle-state semantic rewrite |
| Do not widen no-token PR tool availability in this issue | current server registration policy keeps PR tools token-gated |
| Avoid leaking raw PyGithub `PullRequest` objects into the tool contract | narrow response shape is the point of the issue |
| No compatibility bridge that keeps `parent_branch` from phase state as co-equal authority | issue exists because the prompt needs canonical PR metadata |

---

## Supported Contract For This Issue

For the parent-branch boundary, the stable semantic contract is:

```json
{
  "pr_number": 412,
  "title": "Close issue branch cleanly",
  "state": "closed",
  "base_branch": "epic/341-coordination",
  "head_branch": "feature/354-get-pr-tool",
  "merged_at": "2026-05-26T16:12:00Z",
  "merge_sha": "abc123...",
  "body": "Delivered scope...\nDeferred work...\nCloses #354"
}
```

Field constraints:

- `base_branch` comes from `base.ref`
- `head_branch` comes from `head.ref`
- `merged_at` is nullable
- `merge_sha` is nullable and maps from upstream `merge_commit_sha`
- `body` is the canonical PR handover text used by `end-issue` for deferred-work follow-up and closeout reasoning
- `state` is preserved as returned by GitHub; callers must not infer merged-vs-closed from `state` alone

---

## Approved Strategy

**Boundary / consumer scope:**

- add a new read-only `get_pr(pr_number)` path in adapter -> manager -> tool -> server registration
- keep `get_work_context()` unchanged
- update `.github/prompts/end-issue.prompt.md` so `get_pr(...)` is the authoritative source for `base_branch`
- include `body` in `get_pr(...)` because the PR body is the durable closeout handover used to inspect deferred work after merge
- keep `merge_pr(...)` as the authoritative merge proof
- keep PR tools under the existing token-gated registration policy

**Selected strategy:**
Additive PR tool, no compatibility bridge, no `get_work_context()` fallback as authoritative parent source, and no separate issue-surface lookup for closeout body inspection.

**Implementation-shaping constraint for later phases:**
The supported contract is the narrow semantic payload above, including `body`, not a raw PyGithub object. If the tool renders text, that text must still faithfully expose those fields.

---

## Assumptions

- PyGithub `PullRequest` exposes `base.ref`, `head.ref`, `merged_at`, and `merge_commit_sha` consistently for the existing repo integration.
- `end-issue` will continue to accept explicit `ISSUE_NUMBER` and `PR_NUMBER` from the human invocation, using `get_work_context()` only for branch/workflow context and issue-number fallback.
- No other prompt or tool currently depends on a `get_pr(...)` contract, so the consumer blast radius remains local to issue #354.

---

## Regression Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Caller treats `state="closed"` as proof of merge | Medium | preserve `merged_at` and document that merge proof stays with `merge_pr(...)` |
| Tool registration drifts from existing token-gated PR policy | Low | add server registration coverage alongside existing PR tool assertions |
| Prompt is partially migrated and still blocks on `parent_branch` from `get_work_context()` | Medium | update prompt step ordering explicitly and review the stop condition |
| `body` semantics drift between `get_pr(...)` and prompt expectations | Medium | keep `body` explicitly in the supported contract and validate prompt usage against that contract |

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-26 | Agent | Initial research draft with upstream PR-shape evidence, blast radius, and strategy checkpoint |
