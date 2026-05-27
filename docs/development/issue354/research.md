<!-- docs\development\issue354\research.md -->
<!-- template=research version=research created=2026-05-26 updated=2026-05-27 -->
# Issue #354 — GitHub read-contract refactor for `get_issue` + `get_pr`

**Status:** DRAFT  
**Version:** 1.2  
**Last Updated:** 2026-05-27

---

## Purpose

Establish the broadened problem framing, verified architecture gaps, blast radius, and strategy-sensitive boundaries for evolving issue #354 from a narrow `get_pr` addition into a shared GitHub read-contract refactor covering both `get_issue` and `get_pr`.

## Scope

**In Scope:**
`mcp_server/adapters/github_adapter.py` read fetch surface for issues and PRs; `mcp_server/managers/github_manager.py` read-side normalization policy; `mcp_server/tools/issue_tools.py`; `mcp_server/tools/pr_tools.py`; PR and issue tool registration in `mcp_server/server.py`; public GitHub tool docs in `docs/reference/mcp/tools/github.md`; direct unit coverage for adapter, manager, tools, server, and any new read-contract models; the existing `MergePRTool` Law of Demeter violation that becomes directly fixable if `get_pr` is added.

**Out of Scope:**
`list_issues` / `list_prs` normalization; `close_issue` / `update_issue` / other command return-type normalization; no-token PR-tool registration changes; generic MCP transport redesign; introducing an `IGitHubReader` abstraction across the entire GitHub stack; generic GitHub-stack cleanup beyond the single-item read paths and the direct `MergePRTool` bypass.

## Prerequisites

1. The current GitHub issue body for issue #354 still describes the older narrow `get_pr` scope and does not yet capture the broadened `get_issue` refactor.
2. The branch was explicitly forced back from `design` to `research` on 2026-05-27 because scope broadening invalidated the prior narrow design as the active planning input.
3. QA plan-verifier gap-analysis input dated 2026-05-27 was accepted as preliminary research input; findings below record the repo-verified parts of that analysis plus explicitly marked recommendations.

---

## Problem Statement

The GitHub read side is currently inconsistent and architecture-hostile in exactly the place where issue #354 first surfaced. `get_issue` is a read query but returns a mutable PyGithub `Issue` object from the manager, `GetIssueTool` performs host-object normalization inside the tool layer, public docs already claim a JSON-like `get_issue` contract that implementation does not honor, `get_pr` does not exist yet, and `MergePRTool` bypasses the manager boundary entirely via `self.manager.adapter.repo.get_pull(...)`.

A narrow additive `get_pr` would solve the immediate `end-issue` parent-branch problem, but it would leave the existing read-contract inconsistency intact and preserve the current tool-layer leakage for `get_issue`.

## Research Goals

- Validate whether issue #354 should explicitly broaden from `get_pr` only to a shared read-contract refactor for `get_issue` + `get_pr`.
- Confirm the actual repo blast radius across adapter, manager, tools, docs, and tests.
- Identify the strategy-sensitive boundary or boundaries that require explicit human approval before design.
- Separate the minimum coherent refactor from adjacent GitHub-stack cleanup that should stay out of scope.

---

## Findings

### Finding 1 — The current GitHub issue body is now narrower than the active research scope

The live GitHub issue for #354 still describes a narrow `get_pr(pr_number)` addition for `end-issue`: `pr_number`, `title`, `state`, `base_branch`, `head_branch`, `merged_at`, `merge_sha`, and prompt migration away from `get_work_context()` for the parent branch.

That description no longer matches the active branch scope after the explicit return to research on 2026-05-27. The branch is now investigating a wider read-contract problem: `get_issue` and `get_pr` should likely be designed together rather than treating `get_pr` as an isolated exception.

### Finding 2 — The adapter fetch layer is mostly acceptable; the inconsistency starts at manager and tool level

Repo reads confirm a mixed normalization policy across the GitHub stack.

| Layer | Read path today | Verified behavior | Architectural implication |
|---|---|---|---|
| Adapter | `GitHubAdapter.get_issue()` | fetches and returns raw PyGithub `Issue` | acceptable fetch boundary |
| Adapter | `GitHubAdapter.list_issues()` | returns raw `list[Issue]` | same raw fetch pattern |
| Adapter | `GitHubAdapter.list_prs()` | returns raw `list[PullRequest]` | same raw fetch pattern |
| Adapter | `GitHubAdapter.merge_pr()` | returns normalized `dict[str, Any]` | command path already normalizes |
| Manager | `GitHubManager.get_issue()` | pass-through raw `Issue` | query returns mutable host object |
| Manager | `GitHubManager.create_issue()` / `create_pr()` / `merge_pr()` | normalized `dict` output | commands already use narrow results |

This means the biggest architectural inconsistency is not at fetch time. It is at the read-query boundary above the adapter: commands normalize, but `get_issue()` does not.

### Finding 3 — `GetIssueTool` currently performs host-object normalization in the tool layer

`GetIssueTool.execute()` currently receives the raw `Issue` from `GitHubManager.get_issue()` and directly reads host-specific fields such as:

- `issue.assignees` and `a.login`
- `issue.labels` and `label.name`
- `issue.milestone.title`
- `issue.created_at.isoformat()`

This is a direct cohesion and interface-segregation problem:

- the tool knows PyGithub field names and nested shape
- the tool performs normalization that belongs closer to the read-contract boundary
- a read-only tool receives a write-capable object with methods and mutable host-side behavior not needed for this query

The current unit test in `tests/mcp_server/unit/tools/test_issue_tools.py` mirrors that same host shape by mocking `created_at`, `assignees`, `labels`, and `milestone` directly on the returned issue object.

### Finding 4 — `MergePRTool` currently bypasses the manager boundary

`MergePRTool.execute()` still resolves the head branch by reaching through multiple layers:

- `self.manager.adapter.repo.get_pull(params.pr_number)`

This is a direct Law of Demeter violation and a strong signal that a first-class single-PR read seam is missing. If issue #354 grows to include `get_pr`, this one-line bypass becomes directly fixable inside the same scope.

### Finding 5 — Public docs already claim a structured `get_issue` contract that implementation does not honor

`docs/reference/mcp/tools/github.md` documents `get_issue` as if it returns a JSON-style issue payload including fields such as:

- `url`
- `body`
- `state`
- `labels`
- `milestone`
- `assignees`
- `created_at`
- `updated_at`
- `closed_at`
- `author`

The current tool implementation does not return that documented shape. It emits prose text with headings and labeled lines.

This matters because it weakens the argument for treating the current prose output as a normative public contract. Repo search found semantic consumers of `get_issue` in:

- `.github/prompts/start-issue.prompt.md`
- `.github/agents/co.agent.md`

Those consumers describe `get_issue` as a source of issue context, title, labels, scope, or body, but repo evidence did **not** show a downstream parser depending on the current `**Labels:**` / `**Assignees:**` / `**Milestone:**` prose markers. The clearest coupling to the current prose formatting is in the direct tool unit test and in the mismatch with the published docs.

### Finding 6 — There is already a local precedent for a frozen read-side DTO under `mcp_server/state`

`mcp_server/state/workflow_status.py` defines `WorkflowStatusDTO` as:

- `ConfigDict(frozen=True, extra="forbid")`
- a read-side model used as a stable immutable query result

That does not prove the exact final home or name for GitHub read models, but it does provide a strong local precedent for the missing pattern: a frozen read-side DTO living under `mcp_server/state` instead of a raw host object flowing into the tool layer.

### Finding 7 — The coherent minimum scope is broader than `get_pr`, but still narrower than a full GitHub-stack cleanup

Current repo evidence supports a bounded scope expansion instead of a generic cleanup campaign.

| Surface | Why it now belongs in scope | Risk |
|---|---|---|
| `GitHubManager.get_issue()` | current query-return inconsistency is part of the same read-contract problem | medium |
| `GetIssueTool` | today leaks PyGithub shape and contradicts docs contract | medium |
| `GetPRTool` | missing tool is still the original issue trigger | low |
| `MergePRTool` head-branch fetch | direct consequence of the absence of `get_pr` | low |
| GitHub docs reference page | current public contract is false for `get_issue` | low |
| Adapter/manager/tool/server tests | must shift from raw host-shape assumptions to read-contract assertions | low |

Adjacent gaps remain real but are still separate concerns for now:

- list-query normalization
- command return normalization
- whole-stack `IGitHubReader` abstraction
- transport-layer redesign so MCP-visible tool results are not text-based

---

## Architectural Constraints

| Constraint | Source / rationale |
|---|---|
| Read queries should not expose mutable host objects | `ARCHITECTURE_PRINCIPLES.md` §1.4 ISP and §5 CQS |
| Tool layer should not know nested host-object field shape | `ARCHITECTURE_PRINCIPLES.md` §7 Law of Demeter and §10 Cohesion |
| No broad abstraction layer just because the GitHub stack is imperfect today | `ARCHITECTURE_PRINCIPLES.md` §9 YAGNI |
| Keep scope bounded to the immediate read-contract problem | explicit issue-354 scope broadening, not whole-stack redesign |
| Public docs and actual tool contract should not silently diverge | `ARCHITECTURE_PRINCIPLES.md` §8 Explicit over Implicit |

---

## Approved Strategy

### Boundary 1 — `get_issue` visible output contract

**Selected strategy:** clean break

**Approved by:** user decision on 2026-05-27

**Decision:** change `get_issue` visible output from prose to deterministic JSON text.

**Rationale:**
- the public docs already describe a structured issue payload rather than the current prose format
- repo evidence did not find a downstream parser depending on the current prose markers
- the direct blast radius appears bounded to docs, direct tool tests, and human/agent expectations rather than production code parsers
- a shared visible pattern for `get_issue` and `get_pr` reduces special cases in later phases

**Constraints for later phases:**
- do not build a prose/JSON bridge for `get_issue`
- design and planning must treat deterministic JSON text as the visible contract for both `get_issue` and `get_pr` under the current MCP transport
- docs, tests, and prompt expectations must be updated as part of the same coherent refactor

### Boundary 2 — `get_pr` addition

**Selected strategy:** additive, no compatibility bridge

**Rationale:**
- this is additive behavior
- the original issue already justified a narrow PR-read tool
- the broadened scope only changes the fact that `get_pr` should be designed as part of a shared read-contract family instead of as a one-off exception

**Constraints for later phases:**
- keep `get_pr` inside the same shared read-contract family as `get_issue`
- do not widen scope into generic GitHub browsing or no-token PR reads

### Boundary 3 — `MergePRTool` Demeter fix

**Selected strategy:** include in issue #354 as an internal follow-on refactor

**Rationale:**
- the existing direct traversal in `MergePRTool` is already an architectural defect
- if a single-PR read seam is added, fixing that traversal is a natural internal follow-on rather than an independent feature scope

**Constraints for later phases:**
- the fix must remain bounded to removing the direct manager→adapter→repo traversal
- do not use this as a reason to broaden issue #354 into wider merge-flow redesign

---

## Open Questions

- Should the GitHub issue body for #354 be updated to reflect the broadened `get_issue` + `get_pr` scope before design starts?

---

## Assumptions

- The broadened scope is intended to remain bounded to single-item read queries and the directly related `MergePRTool` bypass, not to all GitHub query surfaces.
- The current text-based MCP result transport remains in place; research is not reopening server transport behavior in issue #354.
- `WorkflowStatusDTO` is precedent for model style and package placement direction, not yet a binding decision on final file path or class names for GitHub read contracts.

---

## Regression Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Hidden consumer expects current `get_issue` prose shape | Medium | explicit approval on Boundary 1 before design; targeted repo search and direct test updates |
| Scope balloons into generic GitHub-stack redesign | Medium | keep list queries, command returns, and `IGitHubReader` explicitly out of scope |
| Docs and implementation drift again during refactor | Medium | treat `docs/reference/mcp/tools/github.md` as part of the same scoped change |
| `get_pr` ships but `MergePRTool` keeps the manager bypass | Low | keep the Demeter fix explicitly in scope with the new PR read seam |

---

## Expected Results For Design And Planning

Design should answer the following with the broadened scope now explicit:

- what the shared read-contract family for `get_issue` and `get_pr` should look like
- where the frozen read models belong in the codebase
- what the visible tool contract should be under the current text-only MCP transport
- how `GetIssueTool`, `GetPRTool`, and `MergePRTool` should align to the same layering rules
- how tests and docs move from host-shape or prose assumptions to stable read-contract assertions

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-26 | Agent | Initial narrow research draft for `get_pr` only |
| 1.1 | 2026-05-27 | Agent | Broadened research scope to shared `get_issue` + `get_pr` read-contract refactor using repo-verified QA preliminary analysis |
| 1.2 | 2026-05-27 | Agent | Recorded approved clean-break strategy for `get_issue` visible output and finalized research decision boundary |
