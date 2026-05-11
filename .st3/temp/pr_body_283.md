## Summary

Closes #283 — state.json/deliverables.json contamination + ready-phase enforcement.

This PR replaces the two-step ready-phase flow (`git_add_or_commit → create_pr`) with an atomic `submit_pr` tool, adds post-PR branch lockdown via `PRStatusCache` + `BranchMutatingTool` ABC, and structurally eliminates branch-local artifact contamination.

**Scope:** 242 files changed, ~15 900 insertions, ~4 000 deletions.

---

## Problem (recap)

Three compounding root causes caused `state.json`/`deliverables.json` to land on `main`:

1. `.gitattributes` merge=ours introduced on feature branch instead of `main` first — unprotected merge window.
2. `merge=ours` only protects against overwrites; it does not block fresh additions (deleted-on-main, added-on-branch).
3. GitHub server-side merges do not reliably respect `.gitattributes` merge drivers.

A deeper structural problem: no automated guard existed to prevent branch-local runtime artifacts from entering commits or PRs.

---

## What Changed

### Model 1 — Branch-tip neutralization (C1–C4)

Established the neutralization mechanism in the existing two-step flow as a baseline:

- **NoteContext protocol** (`mcp_server/core/operation_notes.py`) — typed note classes (`ExclusionNote`, `SuggestionNote`, `CommitNote`, `RecoveryNote`), replacing untyped hint-fields on exceptions.
- **GitAdapter** — `commit(skip_paths)` + `neutralize_to_base(paths, base)` — restores branch-local artifacts to their merge-base state before committing.
- **GitManager** — `commit_with_scope()`, `has_net_diff_for_path()`, `neutralize_to_base()` facade methods (LoD-compliant; no direct adapter calls from tool layer).
- **EnforcementRunner** — declarative rewrite; `default_base_branch` injection; `_handle_check_phase_readiness` replacing the old `_handle_check_merge_readiness` handler.
- **GitCommitTool** terminal route — 3-tier base resolution; reads `ExclusionNote` entries and calls neutralize before commit.
- **server.py** — `NoteContext` threading per tool call; `MergeReadinessContext` injected at composition root.
- **Config** — `enforcement.yaml`, `phase_contracts.yaml`, `workphases.yaml` ready-phase entries updated.

### submit_pr atomic tool (C5)

Resolved the chicken-and-egg problem: neutralize restores `state.json` to merge-base, causing `create_pr` enforcement to read the wrong phase.

- **`SubmitPRTool`** (`mcp_server/tools/pr_tools.py`) — single atomic tool: neutralize artifacts → commit → push → create PR → write `PRStatus.OPEN`.
- **`CreatePRTool` deleted** — `SubmitPRTool` calls `GitHubManager.create_pr()` directly.
- **`BranchMutatingTool` ABC** (`mcp_server/tools/base.py`) — zero-method ABC; sets `tool_category = "branch_mutating"`. 18 tools inherit it. One `enforcement.yaml` rule (`tool_category: branch_mutating → check_pr_status`) replaces 18 individual entries (DRY fix).
- **`PRStatusCache`** (`mcp_server/state/pr_status_cache.py`) — in-memory cache; cold-start GitHub API fallback; injected via `IPRStatusReader`/`IPRStatusWriter` interfaces.
- **`MergePRTool` deliberately excluded** from `BranchMutatingTool` — it is the only escape hatch that clears `PRStatus.OPEN`; including it would create a deadlock.
- **Terminal route removed** from `GitCommitTool.execute()` — neutralization moved entirely to `SubmitPRTool`.
- **`enforcement.yaml`** — two new rules: `tool: submit_pr → check_phase_readiness` (pre) + `tool_category: branch_mutating → check_pr_status` (pre). Old `create_pr → check_merge_readiness` rule removed.

### LoD fix (C6)

`SubmitPRTool.execute()` was calling `self._git_manager.adapter.*` directly (Law of Demeter violation):

- `GitManager.has_net_diff_for_path()` + `GitManager.neutralize_to_base()` added as proper facade delegates.
- All `self._git_manager.adapter.*` calls in `SubmitPRTool.execute()` replaced with facade calls.
- Unit tests updated accordingly.

### Documentation synchronization (6 rounds)

- **issue283 docs** — research, design (3 docs), planning (2 docs), README, session overdracts.
- **Reference layer** — `docs/reference/mcp/tools/github.md`, `docs/reference/mcp/MCP_TOOLS.md`, `docs/mcp_server/TOOLS.md`, `docs/mcp_server/README.md`.
- **Architecture docs** — `ARCHITECTURE.md`, `PHASE_WORKFLOWS.md`, `04_enforcement_layer.md`.
- **agent.md** — `submit_pr` flow, `BranchMutatingTool`, `PRStatus` lifecycle, `workflow_phase=` parameter.
- **Research doc** — step table updated to GitManager facade methods; stale `check_merge_readiness`/`CreatePRTool`/`5c test section`/`GitAdapter.*` references corrected.

---

## Key Architectural Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Phase gate location | Enforcement.yaml (external) | Policy gates belong in config, not tool logic |
| `CreatePRTool` | Deleted | No reuse case; `SubmitPRTool` → `GitHubManager.create_pr()` directly |
| Post-PR lockdown | `PRStatusCache` + `BranchMutatingTool` | Cold-start API fallback; DRY — one rule covers 18 tools |
| `MergePRTool` exclusion | Not a `BranchMutatingTool` | Deadlock prevention; it is the escape hatch |
| LoD compliance | GitManager facade methods | Tool layer must not reach through manager into adapter |

---

## Test Coverage

New test files (selection):

- `tests/mcp_server/integration/test_submit_pr_atomic_flow.py` (286 lines)
- `tests/mcp_server/integration/test_pr_status_lockdown.py` (237 lines)
- `tests/mcp_server/integration/test_model1_branch_tip_neutralization.py` (286 lines)
- `tests/mcp_server/integration/test_ready_phase_enforcement.py` (120 lines)
- `tests/mcp_server/integration/test_c5_cleanup_and_prstatus.py` (148 lines)
- `tests/mcp_server/integration/test_blocker_recovery_note_dispatch.py` (146 lines)
- `tests/mcp_server/unit/tools/test_submit_pr_tool.py`
- `tests/mcp_server/unit/tools/test_branch_mutating_tool.py`
- `tests/mcp_server/unit/state/test_pr_status_cache.py`
- `tests/mcp_server/unit/core/test_note_context_unit.py`
- `tests/mcp_server/unit/adapters/test_git_adapter_neutralize_to_base.py`
- `tests/mcp_server/unit/adapters/test_git_adapter_skip_paths.py`
- `tests/mcp_server/unit/managers/test_enforcement_runner_c2.py` (468 lines)
- `tests/mcp_server/unit/managers/test_git_manager_skip_paths.py`
- `tests/mcp_server/unit/managers/test_git_manager_no_file_open.py`

---

## FLAG DAY

This is a clean break. No backward-compat shims, no transitional code paths, no skipped or commented-out tests. The pre-#283 sequential flow (`git_add_or_commit → create_pr`) is fully removed. Every legacy test has been rewritten or deleted.
