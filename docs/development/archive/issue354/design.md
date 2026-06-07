<!-- docs\development\issue354\design.md -->
<!-- template=design version=5827e841 created=2026-05-26T20:03Z updated=2026-05-28 -->
# Issue #354 — Design: Shared Read-Contract Refactor (get_issue + get_pr + MergePR Demeter fix)

**Status:** DRAFT  
**Version:** 2.0  
**Last Updated:** 2026-05-28

---

## Purpose

Define the chosen design direction, boundaries, and validation obligations for three coupled changes in the MCP GitHub tool layer:

1. **`get_issue` clean break** — replace prose output with deterministic JSON text backed by a frozen DTO; normalization moves from the tool layer to the manager layer.
2. **`get_pr` addition** — new read-only tool exposing a stable PR contract for use by the `end-issue` prompt.
3. **`MergePRTool` Demeter fix** — eliminate the `self.manager.adapter.repo.get_pull(...)` chain by routing through the new `GitHubManager.get_pr(...)`.

These three changes share a single design contract surface — the frozen GitHub read DTO family — and are implemented as one coherent scope.

## Scope

**In Scope:**
- `mcp_server/state/github_read_models.py` (new — frozen DTO home)
- `mcp_server/adapters/github_adapter.py` (new `get_pr` method)
- `mcp_server/managers/github_manager.py` (`get_issue` normalization refactor + new `get_pr`)
- `mcp_server/tools/issue_tools.py` (`GetIssueTool` clean break)
- `mcp_server/tools/pr_tools.py` (new `GetPRTool`; `MergePRTool` Demeter fix)
- `mcp_server/server.py` (`GetPRTool` registration)
- `.github/prompts/end-issue.prompt.md` (update to use `get_pr` for `base_branch` and PR body)
- `docs/reference/mcp/tools/github.md` (rewrite `get_issue` entry; add `get_pr` entry)
- Direct unit coverage for adapter, manager, both tools, server registration, and MCP-visible result shape

**Out of Scope:**
- `merge_pr` behavior changes beyond the Demeter fix
- `submit_pr` transaction changes
- `get_work_context()` semantic changes
- Widening PR-tool availability without token
- Generic GitHub resource abstractions
- MCP transport redesign
- Implementation sequencing or TDD slicing

## Prerequisites

Read these first:
1. [docs/development/issue354/research.md][related-1]
2. [docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-2]
3. [docs/coding_standards/DOCUMENTATION_STANDARD.md][related-3]
4. [.github/prompts/end-issue.prompt.md][related-4]
5. [mcp_server/tools/tool_result.py][related-5]
6. [mcp_server/state/workflow_status.py][related-6] (frozen DTO precedent)

---

## 1. Context & Requirements

### 1.1. Problem Statement

Three interconnected problems exist in the MCP GitHub tool layer, all rooted in the same layering failure: PyGithub host-object knowledge leaks past the manager boundary.

**Problem A — `get_issue` returns prose, not a deterministic contract.**
`GetIssueTool.execute()` receives a raw `github.Issue.Issue` object from the manager, then accesses seven host-object fields directly (`.assignees`, `.labels`, `.milestone`, `.number`, `.title`, `.state`, `.created_at`, `.body`) and produces a prose markdown string. The publicly documented contract (structured JSON with all fields including `url`, `updated_at`, `closed_at`, `author`) is not what the implementation returns. The normalization work that belongs in the manager is done in the tool layer, and the output format is unvalidated prose rather than a deterministic JSON text.

**Problem B — No `get_pr` tool exists.**
The `end-issue` prompt currently depends on `get_work_context()` for `parent_branch` even though the authoritative branch and durable handover facts live on the GitHub PR object. Without a dedicated `get_pr` tool, closeout logic mixes phase-state concerns with PR-metadata concerns and the PR body is inaccessible without a raw GitHub API call.

**Problem C — `MergePRTool` violates the Law of Demeter.**
`MergePRTool.execute()` calls `self.manager.adapter.repo.get_pull(pr_number)` to retrieve `head_branch` before the merge. This bypasses the manager-adapter layering entirely and couples the tool directly to a PyGithub internal. Once `GitHubManager.get_pr(...)` exists, the Demeter violation has no remaining excuse and must be fixed within this issue.

### 1.2. Requirements

**Functional:**
- [ ] Refactor `GetIssueTool` to receive a frozen `IssueReadModel` DTO from the manager and emit deterministic JSON text.
- [ ] `GitHubManager.get_issue(...)` normalizes the raw PyGithub Issue into an `IssueReadModel` (no longer a pass-through).
- [ ] `get_issue` visible output includes all docs-published fields: `number`, `url`, `title`, `body`, `state`, `labels`, `milestone` (with `number`/`title`/`state`), `assignees`, `created_at`, `updated_at`, `closed_at`, `author`.
- [ ] Expose a read-only `get_pr(pr_number)` tool returning a frozen `PRReadModel` DTO via `GitHubManager.get_pr(...)`.
- [ ] `get_pr` contract includes: `pr_number`, `title`, `state`, `base_branch`, `head_branch`, `merged_at`, `merge_sha`, `body`.
- [ ] Fix `MergePRTool.execute()` to use `self.manager.get_pr(params.pr_number)` instead of `self.manager.adapter.repo.get_pull(params.pr_number)`.
- [ ] Allow `end-issue` to use `get_pr(...)` as the authoritative source for `base_branch` and PR body.
- [ ] Preserve the current `end-issue` use of `get_work_context()` for branch, workflow, and issue fallback context.
- [ ] Expose exact MCP-visible response shapes for both `get_issue` and `get_pr` that planning and implementation can validate deterministically.

**Non-Functional:**
- [ ] Do not expose raw PyGithub objects through any tool contract.
- [ ] Do not change `get_work_context()` semantics.
- [ ] Do not widen PR-tool registration beyond the existing token-gated policy.
- [ ] Keep the blast radius bounded to the files identified in scope above.
- [ ] No legacy paths in production code or test code: all tests must test only the new DTO-based behavior.

### 1.3. Constraints

- `merge_pr(...)` remains the only authoritative merge-acceptance signal in the `end-issue` flow.
- `get_work_context()` stays branch-phase context, not host-side PR lookup.
- Both `get_issue` and `get_pr` MCP-visible contracts must be exact JSON text under the current text-only server transport.
- `merged_at` and `merge_sha` must stay nullable because closed-unmerged PRs are a valid state.
- The PR body is operationally required for closeout; the design must not force a second issue-surface lookup to recover it.
- `closed_at` is null for open issues and must not be fabricated.
- No compat bridge or migration helper anywhere — the clean break is complete within this issue.

---

## 2. Design Options

The options analysis applies to the original `get_pr` addition; it also informed the `get_issue` refactor strategy, where the Approved Strategy already mandates a clean break. Sections 2.1–2.4 are retained as rationale for the `get_pr` option selection; the `get_issue` refactor is not option-contested because the Approved Strategy in research.md explicitly requires it.

### 2.1. Option A — Keep `get_work_context()` For Branch Data And Reuse `get_issue()` For Body

Use `get_work_context()` as the source of `parent_branch` and read body-like context from the issue surface when needed.

**Pros:**
- Minimal code change.
- Reuses existing tools only.
- Lowest short-term surface-area increase.

**Cons:**
- Preserves the wrong authority boundary: `parent_branch` remains phase-state derived instead of PR-derived.
- Splits closeout facts across two different resources even though the PR already carries the durable handover.
- Conflicts with the approved strategy that the PR is the authoritative closeout surface for this workflow.
- Leaves the original blocker in place when branch-local phase state is absent or stale.

### 2.2. Option B — Add `get_pr(...)` But Return Only Human-Oriented Prose

Add a dedicated PR tool but mirror the current `GetIssueTool` pattern and return a markdown or prose summary.

**Pros:**
- Fits the dominant pattern in current GitHub tools.
- Simple to implement and easy for humans to read.
- Keeps the public surface visually consistent with the original `get_issue`.

**Cons:**
- Weakens the exact response-shape contract the issue explicitly asks for.
- Forces prompt consumers to parse prose instead of consuming a deterministic object-shaped payload.
- Makes strict validation of visible contract shape harder than necessary.

### 2.3. Option C — Add `get_pr(...)` With A Narrow Manager Contract And Deterministic JSON Text Output

Add a dedicated PR-read path in adapter → manager → tool, normalize the PR resource into a frozen DTO in the manager, and render that contract as a single deterministic JSON text payload at the tool boundary. Apply the same design to `get_issue` (Approved Strategy: clean break).

**Pros:**
- Matches the approved strategy for both `get_issue` and `get_pr`.
- Keeps PyGithub-specific knowledge behind the adapter and manager boundary.
- Preserves exact semantic response shapes validatable at the tool boundary.
- Aligns to the current MCP-visible transport reality: text content, not native structured JSON.
- Keeps blast radius bounded to the files already identified in research.
- Enables the Demeter fix in `MergePRTool` as a natural follow-on.

**Cons:**
- `get_issue` visible output changes from prose to JSON text — a breaking change for any consumer that parsed the prose format.
- Requires explicit validation of the visible JSON text contracts at tool and server level.

### 2.4. Option D — Widen Scope To Preserve Structured JSON End-To-End

Change the server transport or result conversion behavior so JSON items remain structured at the MCP boundary.

**Pros:**
- Would make structured tool contracts first-class across the server.

**Cons:**
- Exceeds the approved scope for issue #354.
- Turns a narrow PR-tool issue into a wider server-transport redesign.
- Reopens compatibility and validation concerns beyond this feature.

---

## 3. Chosen Design

**Decision:** Adopt Option C across all three changes. Add a shared frozen GitHub read DTO family in `mcp_server/state/`; normalize `get_issue` in the manager with a full docs-published field set; add `get_pr` with a narrow PR contract; render both as deterministic JSON text at the tool boundary; fix the `MergePRTool` Demeter violation; and update `end-issue` to use `get_pr(...)` for `base_branch` and PR body.

**Rationale:** This design eliminates three interconnected layering failures in one coherent scope, all sharing the same fix strategy: frozen DTOs created in the manager, rendered as JSON text in the tool. The clean break on `get_issue` output is mandated by the Approved Strategy from research.md. The Demeter fix in `MergePRTool` is a natural consequence of adding `GitHubManager.get_pr(...)`.

### 3.1. Shared Read-Contract DTO Family

All normalized GitHub read models live in a new file `mcp_server/state/github_read_models.py`, following the `WorkflowStatusDTO` precedent in `mcp_server/state/workflow_status.py`.

**Design pattern** (matching precedent):
```python
class <Model>(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    # fields...
```

**Three models in the family:**

`MilestoneReadModel` — nested milestone contract:
```python
class MilestoneReadModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    number: int
    title: str
    state: str
```

`IssueReadModel` — full normalized issue contract:
```python
class IssueReadModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    number: int
    url: str
    title: str
    body: str
    state: str
    labels: list[str]
    milestone: MilestoneReadModel | None
    assignees: list[str]
    created_at: str          # ISO 8601
    updated_at: str          # ISO 8601
    closed_at: str | None    # ISO 8601 or null
    author: str
```

`PRReadModel` — narrow PR contract:
```python
class PRReadModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    pr_number: int
    title: str
    state: str
    base_branch: str
    head_branch: str
    merged_at: str | None    # ISO 8601 or null
    merge_sha: str | None
    body: str
```

All datetime fields are normalized to ISO 8601 strings at the manager boundary, not at the tool boundary. Absent body fields (`None` from PyGithub) are normalized to empty string `""` in the manager.

### 3.2. `get_pr` Contract And Visible Result Shape

The MCP-visible `get_pr(...)` contract is one deterministic JSON text item:

```json
{
  "pr_number": 412,
  "title": "Close issue branch cleanly",
  "state": "closed",
  "base_branch": "epic/320-production-readiness-tracker",
  "head_branch": "feature/354-get-pr-tool",
  "merged_at": "2026-05-26T18:14:00+00:00",
  "merge_sha": "abc123...",
  "body": "Delivered scope...\nDeferred work...\nCloses #354"
}
```

Contract field sources:

| Field | PyGithub source | Local type | Notes |
|---|---|---|---|
| `pr_number` | `pr.number` | `int` | identity field |
| `title` | `pr.title` | `str` | preserved as PR title |
| `state` | `pr.state` | `str` | preserved as returned by GitHub |
| `base_branch` | `pr.base.ref` | `str` | authoritative checkout target |
| `head_branch` | `pr.head.ref` | `str` | authoritative branch-match check |
| `merged_at` | `pr.merged_at` | `str \| null` | datetime → ISO 8601 string or `null` |
| `merge_sha` | `pr.merge_commit_sha` | `str \| null` | preserved as nullable |
| `body` | `pr.body` | `str` | `None` normalized to `""` |

### 3.3. `get_issue` Contract And Visible Result Shape

The MCP-visible `get_issue(...)` contract after the clean break is one deterministic JSON text item with all docs-published fields:

```json
{
  "number": 354,
  "url": "https://github.com/owner/repo/issues/354",
  "title": "Add get_pr tool and refactor get_issue",
  "body": "## Description\n\nDetailed issue body...",
  "state": "open",
  "labels": ["type:feature", "priority:high"],
  "milestone": {
    "number": 5,
    "title": "v2.0",
    "state": "open"
  },
  "assignees": ["username1"],
  "created_at": "2026-02-01T10:00:00+00:00",
  "updated_at": "2026-05-28T12:00:00+00:00",
  "closed_at": null,
  "author": "username2"
}
```

This is a **flat JSON object** — no `"success"` wrapper, no `"issue"` nesting. Both `get_issue` and `get_pr` follow the same flat pattern for consistency.

Contract field sources:

| Field | PyGithub source | Local type | Notes |
|---|---|---|---|
| `number` | `issue.number` | `int` | identity field |
| `url` | `issue.html_url` | `str` | direct HTML URL |
| `title` | `issue.title` | `str` | preserved |
| `body` | `issue.body` | `str` | `None` normalized to `""` |
| `state` | `issue.state` | `str` | preserved |
| `labels` | `[l.name for l in issue.labels]` | `list[str]` | label names only |
| `milestone` | `issue.milestone` | `MilestoneReadModel \| None` | nested object when present |
| `assignees` | `[a.login for a in issue.assignees]` | `list[str]` | logins only |
| `created_at` | `issue.created_at` | `str` | datetime → ISO 8601 |
| `updated_at` | `issue.updated_at` | `str` | datetime → ISO 8601 |
| `closed_at` | `issue.closed_at` | `str \| None` | datetime → ISO 8601 or `null` |
| `author` | `issue.user.login` | `str` | issue creator login |

The existing `GetIssueTool` accesses only 7 of these 12 fields (missing `url`, `updated_at`, `closed_at`, `author`). All 12 fields must be added to the manager normalization.

### 3.4. Layering And Responsibility Split

**Before (current state):**

```
GetIssueTool.execute()
  ├── GitHubManager.get_issue(n)  → pass-through → returns raw Issue
  ├── accesses 7 host-object fields directly
  └── produces prose markdown text

MergePRTool.execute()
  ├── self.manager.adapter.repo.get_pull(n)  ← Demeter violation
  └── head_branch = pr.head.ref
```

**After (designed state):**

```
GetIssueTool.execute()
  └── GitHubManager.get_issue(n) → normalization → IssueReadModel
      └── GitHubAdapter.get_issue(n) → raw Issue
  → renders JSON text (model.model_dump()) → ToolResult.text(...)

GetPRTool.execute()
  └── GitHubManager.get_pr(n) → normalization → PRReadModel
      └── GitHubAdapter.get_pr(n) → raw PullRequest
  → renders JSON text (model.model_dump()) → ToolResult.text(...)

MergePRTool.execute()
  └── GitHubManager.get_pr(n) → PRReadModel
  → head_branch = pr_model.head_branch  ← Demeter fix
```

**Boundary responsibilities:**

- `GitHubAdapter.get_issue(n)` — remains thin; fetches raw `Issue` from PyGithub; handles 404/API errors.
- `GitHubAdapter.get_pr(n)` — new; fetches raw `PullRequest`; follows same error pattern as `get_issue`.
- `GitHubManager.get_issue(n)` — **changed**: normalizes raw `Issue` → `IssueReadModel`; no longer a pass-through.
- `GitHubManager.get_pr(n)` — **new**: normalizes raw `PullRequest` → `PRReadModel`.
- `GetIssueTool.execute(...)` — **changed**: receives `IssueReadModel`; emits one JSON text item.
- `GetPRTool` — **new**: receives `PRReadModel`; emits one JSON text item.
- `MergePRTool.execute(...)` — **changed**: calls `manager.get_pr(n)` to get `head_branch`; eliminates adapter chain.
- `mcp_server/server.py` — registers `GetPRTool` alongside other PR tools under existing token guard.

**Rejected boundary placements:**

- Normalizing in the adapter would mix external API access with business contract shaping.
- Reading `repo.get_pull(...)` directly inside any tool violates existing layering.
- Keeping normalization in the tool layer (current `GetIssueTool` pattern) is the bug being fixed.
- Redesigning server transport to preserve structured JSON exceeds issue scope.

### 3.5. `GetIssueTool` Refactor: Tool-Layer Clean Break

The current `GetIssueTool.execute()` contains all normalization logic and renders prose. After the refactor:

- The method calls `self.manager.get_issue(params.issue_number)` and receives an `IssueReadModel`.
- It calls `ToolResult.text(json.dumps(issue.model_dump(), indent=2))` to emit one JSON text item.
- All host-object field access (`issue.assignees`, `issue.labels`, etc.) is removed from the tool.
- No fallback prose rendering path exists — there is no compat bridge.

The tool shrinks significantly; the normalization logic moves entirely into the manager.

### 3.6. `MergePRTool` Demeter Fix

The current violation in `MergePRTool.execute()`:
```python
# VIOLATION — line 101:
pr = self.manager.adapter.repo.get_pull(params.pr_number)
head_branch = pr.head.ref
```

Replaced by:
```python
# CLEAN:
pr_model = self.manager.get_pr(params.pr_number)
head_branch = pr_model.head_branch
```

The tool no longer holds a reference to the adapter or repo. No other behavior in `MergePRTool` changes.

The test for `MergePRTool` must be replaced: the old mock (`mock_github_manager.adapter.repo.get_pull.return_value = mock_pr`) is a legacy pattern that reinforced the violation. The new test mocks `manager.get_pr()` to return a `PRReadModel(...)` directly.

### 3.7. Tool Result Design Under Current Server Transport

Current server behavior converts `ToolResult` content into MCP text content. JSON content items from `ToolResult.json_data(...)` produce two content items (a JSON item + a text fallback), which is not the exact contract for `get_issue` and `get_pr`.

Both tools must emit one deterministic JSON text blob:
```python
return ToolResult.text(json.dumps(model.model_dump(), indent=2))
```

- `model_dump()` serializes the frozen Pydantic model to a dict.
- `json.dumps(..., indent=2)` renders it as a formatted JSON string.
- `datetime` fields are already normalized to ISO 8601 strings in the manager, so no `default=str` serializer is needed.
- `None` values (`closed_at`, `merged_at`, `merge_sha`) serialize to `null` naturally.

`ToolResult.json_data(...)` must **not** be used for these tools — it would produce duplicate output under the current transport.

### 3.8. Prompt Consumer Design For `end-issue`

The prompt keeps `get_work_context()` for branch/workflow/issue context, but stops treating it as the source of `parent_branch`.

| Prompt concern | Source of truth | Reason |
|---|---|---|
| active branch | `get_work_context()` | branch-local workflow context |
| workflow | `get_work_context()` | workflow context, not PR metadata |
| issue fallback | `get_work_context()` | existing prompt behavior remains valid |
| base branch | `get_pr(...)` | host-side PR metadata is authoritative |
| PR body | `get_pr(...)` | durable closeout handover lives on the PR |
| merge acceptance | `merge_pr(...)` | authoritative merge proof remains unchanged |

Design-level prompt consequences:

- `end-issue` calls `get_pr(pr_number=PR_NUMBER)` after `merge_pr(...)` and records `base_branch`, `head_branch`, and `body`.
- The prompt compares the active branch from `get_work_context()` with `head_branch` from `get_pr(...)` and stops on mismatch rather than risking cleanup against the wrong branch.
- `git_checkout(...)` uses `base_branch` from the PR contract rather than `parent_branch` from phase state.
- Step 5 of the prompt consumes the already-captured PR `body` as the durable transfer artifact; it does not switch to `get_issue(...)` for that purpose.
- `merge_pr(...)` remains the only merge-proof step; the prompt must not skip it based on `state="closed"` or non-null `merged_at`.

### 3.9. Error Model

Both `get_issue` and `get_pr` follow the existing GitHub tool error conventions:
- PR/issue not found → `ExecutionError("Pull request/Issue #N not found")` → `ToolResult.error(...)`
- GitHub API failure → existing adapter/system error mapping
- Token missing → no registration in `server.py`, consistent with current policy

For `MergePRTool` after the Demeter fix: if `manager.get_pr(n)` raises `ExecutionError` (e.g., PR not found), the existing `except ExecutionError` block in `MergePRTool.execute()` already handles it correctly — no change needed to the error handling structure.

Compatibility semantics for `get_pr`:
- `merged_at = null` and `merge_sha = null` are valid for non-merged PRs.
- `state = "closed"` does not imply merged.
- `body = ""` is valid and not an error.

Compatibility semantics for `get_issue`:
- `closed_at = null` is valid for open issues.
- `milestone = null` is valid for unassigned issues.
- `body = ""` is valid for issues without a description.

### 3.10. Test Migration Design

**Governing rule:** No legacy paths in production code or test code. All tests must test only the new DTO-based behavior. There must be no evidence of migration in the test suite — no legacy mock patterns, no dual assertions, no compatibility checks.

#### Adapter tests (`test_github_adapter.py`)

| Test | Action | Notes |
|---|---|---|
| `test_get_issue` | Keep as-is | Adapter still returns raw Issue; test is valid |
| `test_get_pr` (new) | Add success, 404, and API-error paths | Mirrors `test_get_issue` structure |

The adapter tests do not change shape because the adapter contract (raw PyGithub object out) does not change for `get_issue`.

#### Manager tests (`test_github_manager.py`)

| Test | Action | Notes |
|---|---|---|
| `test_get_issue` | **Replace** | Old test checked delegation only; new test checks that manager returns `IssueReadModel` with all 12 fields populated correctly from mock Issue |
| `test_get_pr` (new) | Add | Manager normalization test: mock `PullRequest` → assert `PRReadModel` fields |

The new `test_get_issue` mocks `adapter.get_issue()` to return a `MagicMock` with all relevant fields set, then asserts the returned `IssueReadModel` has the expected values for all 12 fields.

#### Tool tests (`test_issue_tools.py`)

| Test | Action | Notes |
|---|---|---|
| `TestGetIssueTool` | **Replace** | Old tests mock host-object fields on the returned issue; new test mocks `manager.get_issue()` to return an `IssueReadModel` and asserts `ToolResult.content[0]["text"]` is valid JSON matching the contract |

The new test verifies: `json.loads(result.content[0]["text"])` contains the expected field values. No mock of PyGithub host-object fields in tool tests.

#### Tool tests (`test_pr_tools.py`)

| Test | Action | Notes |
|---|---|---|
| `test_merge_pr_tool` | **Replace** | Old mock: `mock_github_manager.adapter.repo.get_pull.return_value = mock_pr`; new mock: `mock_github_manager.get_pr.return_value = PRReadModel(...)` |
| `test_get_pr_tool` (new) | Add | Mocks `manager.get_pr()` → `PRReadModel`; asserts one JSON text item with correct fields |

#### Server tests (`test_server.py`)

| Test | Action | Notes |
|---|---|---|
| Existing GitHub tool registration checks | Add `GetPRTool` assertion | `get_pr` registered when token is set; not registered in no-token branch |

### 3.11. Planning-Relevant Consequences

Planning and implementation must preserve these design obligations:

- The normalized `IssueReadModel` and `PRReadModel` contracts above are the supported semantic boundaries — field names and types are binding.
- Both MCP-visible contracts are deterministic JSON text (one content item each) under the current server transport.
- `end-issue` must use `get_pr(...)` for `base_branch` and PR body after this issue lands.
- `docs/reference/mcp/tools/github.md` must be updated: the `get_issue` entry must be rewritten to the flat `IssueReadModel` JSON shape (removing `"success"` wrapper and `"issue"` nesting); a new `get_pr` entry must be added documenting the `PRReadModel` fields.
- Branch/PR `head_branch` mismatch must be treated as a stop condition in the prompt flow.
- `MergePRTool` must have zero references to `self.manager.adapter` after this issue lands.
- No implementation step may introduce a compat bridge, a conditional path, or a `try`-fallback that preserves the old prose output for `get_issue`.
- No test may assert on PyGithub host-object fields as an indirect way of testing tool or manager behavior.
- `model_dump()` output format is the binding rendered contract — planning must treat it as exact.

### 3.12. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Shared frozen DTO family in `mcp_server/state/` | Follows `WorkflowStatusDTO` precedent; read-side models belong in the state package; both tools import from one canonical location |
| Normalization in `GitHubManager`, not in tools | Manager is the layer that translates raw host objects into stable business contracts; tool is input validation + rendering only |
| Flat JSON contract (no `"success"` wrapper or `"issue"` nesting) | Consistent between `get_issue` and `get_pr`; the `"success"` wrapper in existing docs is a documentation artifact not present in the implementation |
| `ToolResult.text(json.dumps(...))` not `ToolResult.json_data(...)` | Avoids duplicated content under current server transport; preserves one exact JSON text item |
| All 12 `get_issue` fields including `url`, `updated_at`, `closed_at`, `author` | Closes the gap between documented and actual contract; user explicitly confirmed full docs-published field set |
| `MilestoneReadModel` as nested frozen DTO | Milestone is not just a string; its `number` and `state` are needed by consumers; mirrors the docs-published contract |
| No legacy paths in production or test code | User requirement: test suite tests only new behavior; no evidence of migration; no compat bridges |
| `MergePRTool` Demeter fix in this issue | The violation has no remaining excuse once `manager.get_pr(...)` exists; fixing it outside this issue would create a temporary window where the adapter chain is published |
| `closed_at` and `merged_at` normalized as strings | Avoids datetime serialization concerns at the tool boundary; ISO 8601 strings are portable and match existing `created_at` pattern |
| `body` normalized to `""` not `None` | Tool consumers (prompt) need text processing; empty string is a valid stable value; null would require null-check logic in every consumer |

---

## 4. Open Questions

None. Research resolved all strategy-sensitive boundaries. User confirmed frozen DTOs, full docs-published field set, and no-legacy-residue requirement.

## Related Documentation

- [docs/development/issue354/research.md][related-1]
- [docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-2]
- [docs/coding_standards/DOCUMENTATION_STANDARD.md][related-3]
- [.github/prompts/end-issue.prompt.md][related-4]
- [mcp_server/tools/tool_result.py][related-5]
- [mcp_server/state/workflow_status.py][related-6]

<!-- Link definitions -->

[related-1]: docs/development/issue354/research.md
[related-2]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-3]: docs/coding_standards/DOCUMENTATION_STANDARD.md
[related-4]: .github/prompts/end-issue.prompt.md
[related-5]: mcp_server/tools/tool_result.py
[related-6]: mcp_server/state/workflow_status.py

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-26 | Agent | Initial design draft: `get_pr` tool, narrow manager contract, deterministic JSON text, `end-issue` prompt integration |
| 2.0 | 2026-05-28 | Agent | Broadened scope: shared frozen DTO family (`IssueReadModel`, `PRReadModel`, `MilestoneReadModel`); `get_issue` clean break (prose → JSON, normalization to manager); full docs-published field set; `MergePRTool` Demeter fix design; test migration design (no legacy residue) |
