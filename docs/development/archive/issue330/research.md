<!-- docs\development\issue330\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-20T09:27Z updated=2026-05-20T09:27Z -->
# GitHubAdapter.list_prs head filter needs owner:branch format

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-20

---

## Problem Statement

`GitHubAdapter.list_prs()` passes bare branch names to `repo.get_pulls(head=...)`. GitHub's REST API requires the `head` parameter in `owner:branch` format for exact head-branch matching. Without the owner prefix, the API performs a substring match and may return PRs from unrelated branches, causing `PRStatus.OPEN` to be set incorrectly.

**Concrete failure:** `PRStatusCache.get_pr_status('refactor/283-ready-phase-enforcement')` returns `PRStatus.OPEN` when PR #329 (`feature/260-remove-st3-references`) is open, because GitHub matches both branches without the `owner:` prefix.

## Research Goals

- Identify the correct layer (adapter vs manager) to apply the `owner:branch` transformation
- Determine impact on existing tests
- Propose minimal fix options with rationale

---

## Root Cause

In `mcp_server/managers/github_manager.py`, `get_pr_status()` calls:

```python
prs = self.adapter.list_prs(state="open", head=branch)
```

`branch` is a bare name (e.g. `refactor/283-ready-phase-enforcement`). This is passed unchanged into `GitHubAdapter.list_prs()`, which forwards it directly to `repo.get_pulls(head=head)`. GitHub's API interprets a bare branch name without `owner:` prefix as a partial/prefix match and can return PRs from other branches.

## Affected Files

| File | Location | Role |
|------|----------|------|
| `mcp_server/adapters/github_adapter.py` | `list_prs()` L254–L272 | Passes `head` to `get_pulls()` — fix point for Option A |
| `mcp_server/managers/github_manager.py` | `get_pr_status()` L244–L253 | Calls `adapter.list_prs(head=branch)` — fix point for Option B |
| `mcp_server/state/pr_status_cache.py` | `_fetch_from_api()` L43 | Delegates to `github_manager.get_pr_status()` — unaffected |
| `tests/mcp_server/unit/adapters/test_github_adapter.py` | `test_list_prs_filter_head` L242–L247 | Asserts bare `head` forwarded — needs update for Option A |
| `tests/mcp_server/integration/test_c5_cleanup_and_prstatus.py` | `test_get_pr_status_returns_open_when_open_pr_exists` L62–L73 | Asserts manager passes bare `head` to adapter — unaffected for Option A |

## Impact

- Any call to `GitHubManager.get_pr_status(branch)` where another PR is open will return `PRStatus.OPEN` for the wrong branch.
- `PRStatusCache` cold-start path is affected (it calls `_fetch_from_api` → `get_pr_status`).
- Enforcement gate `_handle_check_pr_status` in `enforcement_runner.py` uses this to block actions on open branches — incorrect results here cause false-positive or false-negative enforcement blocks.
- Test `test_call_tool_pre_enforcement_blocks_submit_pr_outside_ready_phase` was failing because another open PR was returned.

---

## Solution Options

### Option A — Fix in `GitHubAdapter.list_prs()` (Recommended)

Transform bare `head` to `owner:branch` inside the adapter, using the owner already stored in `self._repo_name` (format: `owner/repo`).

```python
if head:
    owner = self._repo_name.split("/")[0]
    kwargs["head"] = f"{owner}:{head}"
```

**Pros:**
- Adapter is the correct boundary between domain concepts and GitHub API protocol details.
- `GitHubAdapter` already owns `self._repo_name` = `owner/repo`; extracting owner is trivial.
- All callers (present and future) automatically get correct behavior.
- No API-level format knowledge leaks into the manager layer.

**Cons:**
- A caller that already passes `owner:branch` would get double-prefixed. Inspection confirms no caller does this today.

**Test impact:**
- `test_list_prs_filter_head` in `test_github_adapter.py` currently asserts `head == "feature"` (bare). Must be updated to assert `head == "test-owner:feature"` (owner from `injected_settings`).
- Integration test `test_get_pr_status_returns_open_when_open_pr_exists` uses a `MagicMock` adapter — no change needed.

### Option B — Fix in `GitHubManager.get_pr_status()`

Prefix the branch at the manager level before calling the adapter:

```python
owner = self.adapter._repo_name.split("/")[0]
prs = self.adapter.list_prs(state="open", head=f"{owner}:{branch}")
```

**Pros:**
- Explicit: the manager controls the format it sends.

**Cons:**
- Accesses `adapter._repo_name` (private attribute) — breaks encapsulation.
- Leaks GitHub API protocol knowledge into the manager layer.
- Other callers of `adapter.list_prs(head=...)` remain broken.
- Integration test `test_get_pr_status_returns_open_when_open_pr_exists` would need update (assertion `head="feature/42-test"` becomes `head="owner:feature/42-test"`).

---

## Recommended Option

**Option A** — fix in `GitHubAdapter.list_prs()`.

Rationale: The adapter layer is the correct place for GitHub API protocol requirements. The manager should pass domain-level branch names; the adapter translates them to what the API expects. This is consistent with the ISP/adapter pattern used throughout the codebase.

## Key Architectural Constraint

`GitHubAdapter` is the boundary between domain and GitHub API. Protocol-level requirements (like `owner:branch` format) belong in the adapter, not in the manager or above.

---

## Related Documentation

- `mcp_server/adapters/github_adapter.py`
- `mcp_server/managers/github_manager.py`
- `mcp_server/state/pr_status_cache.py`

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-20 | Agent | Initial research |
