<!-- docs\development\issue354\validation.md -->
<!-- created=2026-05-27 -->
# Issue #354 — Validation Report

**Branch:** `feature/354-get-pr-tool`  
**Parent:** `epic/320-production-readiness-tracker`  
**Phase:** validation  
**Date:** 2026-05-27

---

## Verdict

**PASS** — with one pre-existing full-suite failure noted and one blast-radius gap remediated.

---

## Validation Scope and Prerequisites

This validation covers the full three-cycle implementation on `feature/354-get-pr-tool`:

- **C1** — `PRReadModel`, `GitHubAdapter.get_pr()`, `GitHubManager.get_pr()`, `GetPRTool`, server registration, `MergePRTool` Demeter fix
- **C2** — `IssueReadModel`, `MilestoneReadModel`, `GitHubManager.get_issue()` normalization, `GetIssueTool` flat JSON clean break
- **C3** — `docs/reference/mcp/tools/github.md` updated, `end-issue.prompt.md` updated, `start-issue.prompt.md` updated

**Prerequisites read:** `design.md` (v2.0), `planning.md`, `research.md`, `ARCHITECTURE_PRINCIPLES.md`.  
**Approved Strategy (binding):**
- B1 `get_issue`: clean break — no compat bridge
- B2 `get_pr`: additive addition
- B3 `MergePRTool`: bounded Demeter fix, no merge-flow redesign

---

## Full-Suite Test Result

**Command:** `run_tests(scope='full')`  
**Result:** 2 failed, 2835 passed, 11 skipped, 6 xfailed in 32.13s

**Pre-existing failures (not caused by this branch):**
- `tests/mcp_server/unit/config/test_settings.py::test_load_from_env` — asserts version `3.0.0`; actual `1.0.0`. Neither file is in the branch diff.
- `tests/mcp_server/unit/test_cli.py::test_cli_version` — same version mismatch. Neither file is in the branch diff.

These two failures exist on the parent branch and are outside the scope of issue #354.

**Blast-radius gap remediated during validation:**
- `tests/mcp_server/unit/tools/test_github_extras.py::test_merge_pr_tool` — was failing because `mock_adapter.get_pr.return_value` was not set up after the C1 Demeter fix. Fixed by adding a proper typed mock PR object. Test now passes (1 passed, 0 failed).

**Branch-specific tests all pass:**
- `tests/mcp_server/unit/adapters/test_github_adapter.py` — `test_get_pr_success`, `test_get_pr_not_found`, `test_get_pr_api_error`
- `tests/mcp_server/unit/managers/test_github_manager.py` — `test_get_pr_normalization`, `test_get_issue_normalization`
- `tests/mcp_server/unit/tools/test_pr_tools.py` — `test_merge_pr_tool`, `test_get_pr_tool`
- `tests/mcp_server/unit/tools/test_issue_tools.py` — `test_get_issue_tool`
- `tests/mcp_server/unit/test_server.py` — `get_pr` registration assertions

---

## Branch Quality Gate Result

**Command:** `run_quality_gates(scope='branch')`  
**Result:** 6/6 active gates pass (Gate 4 mypy skipped — expected)

| Gate | Status |
|------|--------|
| Gate 0: Ruff Format | ✅ pass |
| Gate 1: Ruff Strict Lint | ✅ pass |
| Gate 2: Imports (isort) | ✅ pass |
| Gate 3: Line Length | ✅ pass |
| Gate 4: mypy | skipped |
| Gate 4b: Pyright | ✅ pass |
| Gate 4c: Types (mcp_server) | ✅ pass |

---

## Planning Deliverables Alignment

### Cycle 1 Exit Criteria

| Criterion | Evidence |
|-----------|----------|
| `GetPRTool` registered, returns JSON text | `server.py` registers `GetPRTool` inside token guard; `execute()` returns `ToolResult.text(json.dumps(...))` |
| `MergePRTool.execute()` zero `self.manager.adapter` references | Confirmed via code review; uses `self.manager.get_pr()` |
| `test_merge_pr_tool` uses `PRReadModel` fixture | `test_pr_tools.py` uses `PRReadModel` fixture; `test_github_extras.py` remediated with typed mock |
| `PRReadModel` frozen | `ConfigDict(frozen=True, extra="forbid")` in `github_read_models.py` |
| Quality gates pass | ✅ confirmed |

**C1 deliverables:** C1.1–C1.11 all satisfied.

### Cycle 2 Exit Criteria

| Criterion | Evidence |
|-----------|----------|
| `GetIssueTool.execute()` zero PyGithub host-object field access | Confirmed; calls `manager.get_issue()` then `json.dumps(issue.model_dump())` |
| `GitHubManager.get_issue()` returns `IssueReadModel` | Return type annotation + normalization code present |
| JSON output: 12 fields, flat, no `"success"` wrapper | `model_dump()` produces flat dict; `github.md` example shows flat JSON |
| `IssueReadModel` + `MilestoneReadModel` frozen | `ConfigDict(frozen=True, extra="forbid")` confirmed |
| `test_get_issue_tool` asserts JSON text output | `test_issue_tools.py` asserts `json.loads(result.content[0]["text"])["number"] == 1` |

**C2 deliverables:** C2.1–C2.5 all satisfied.

### Cycle 3 Exit Criteria

| Criterion | Evidence |
|-----------|----------|
| `github.md` `get_issue` example has no `"success"` key | Flat JSON from line 131 |
| `github.md` has `get_pr` section with all 8 fields | Section present at line 620 with all 8 `PRReadModel` fields |
| `end-issue` calls `get_pr()` after `merge_pr`, before `git_checkout` | Steps 2 → 3 (`get_pr`) → 4 (`git_checkout`) |
| `end-issue` compares `head_branch` with active branch, stops on mismatch | Step 3 explicit guard |
| `end-issue` uses `base_branch` from `get_pr` for `git_checkout` | Step 4: `git_checkout(branch=<base_branch from step 3>)` |
| `start-issue` step 1 references `title` and `labels` as JSON fields | "read the result as flat JSON; record the `title` and `labels` fields" |

**C3 deliverables:** C3.1–C3.6 all satisfied.

---

## Design and Approved Strategy Alignment

| Constraint | Status |
|------------|--------|
| B1: `get_issue` clean break, no compat bridge | ✅ — normalization in manager; tool has zero host-object access |
| B2: `get_pr` additive, no existing contract changes | ✅ — `GetPRTool` added; no existing tool signatures changed |
| B3: Demeter fix bounded, no merge-flow redesign | ✅ — `MergePRTool` routes through `manager.get_pr()`; `merge_pr` behavior unchanged |
| No raw PyGithub objects through tool boundary | ✅ — all tools receive or return `*ReadModel` DTOs |
| Frozen DTOs in `mcp_server/state/` | ✅ — `github_read_models.py` follows `workflow_status.py` precedent |
| `get_pr` token-gated (same policy as other PR tools) | ✅ — registered inside `if github_token:` block only |
| `from __future__ import annotations` not in runtime-Pydantic files | ✅ — absent from `github_manager.py`, `issue_tools.py`, `pr_tools.py` |

---

## Live Demonstration Proposal

No true live path exists — the MCP server requires a real GitHub token and repository connection.

**Closest observable fallback:**

1. **Unit test execution (direct evidence):**
   ```
   run_tests(path="tests/mcp_server/unit/managers/test_github_manager.py::test_get_pr_normalization")
   run_tests(path="tests/mcp_server/unit/tools/test_pr_tools.py::test_get_pr_tool")
   run_tests(path="tests/mcp_server/unit/tools/test_issue_tools.py::test_get_issue_tool")
   ```
   These tests exercise the full normalization path and assert the exact JSON shape returned to the MCP client.

2. **JSON contract inspection:**
   - `mcp_server/state/github_read_models.py` — defines `PRReadModel` (8 fields), `IssueReadModel` (12 fields), `MilestoneReadModel` (3 fields)
   - `docs/reference/mcp/tools/github.md` — shows the exact serialized output shape for both tools

3. **Server registration proof:**
   ```
   run_tests(path="tests/mcp_server/unit/test_server.py")
   ```
   Confirms `get_pr` appears in the tool list when a token is present and is absent without one.

---

## Residual Risks and Caveats

1. **Pre-existing version failures**: `test_settings.py::test_load_from_env` and `test_cli.py::test_cli_version` fail on both this branch and its parent. These are out of scope for issue #354 but should be addressed in a separate issue.

2. **`test_github_extras.py` blast-radius gap**: Fixed during validation. The test now correctly sets up `mock_adapter.get_pr.return_value` before exercising `MergePRTool`. This fix is included in the validation commit.

3. **No integration / live-server test**: All evidence is unit-level. A live GitHub token + repository connection would be required to exercise the MCP server end-to-end. This is a project-wide limitation, not specific to issue #354.

4. **`merged_at` and `merge_sha` nullable on open PRs**: The `get_pr` tool is intended for use after `merge_pr`. Calling it before merge will yield `merged_at: null`. The `end-issue` prompt already gates on `merge_pr` completion before calling `get_pr`, so this is by design.
