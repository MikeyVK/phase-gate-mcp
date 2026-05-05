<!-- docs\development\issue298\research-state-json-authoritative-and-subphase-persistence.md -->
<!-- template=research version=8b7bb3ab created=2026-05-04T19:52Z updated=2026-05-04 -->
# State.json Authoritative Status + Sub-phase Persistence

**Status:** FINAL
**Version:** 1.6  
**Last Updated:** 2026-05-04

---

## Purpose

Establish design decisions and blast radius for making state.json the authoritative source for workflow status (resolver inversion) and adding current_sub_phase persistence to BranchState. Combined research+design doc — scope is bounded enough that a separate design phase adds no value; decision recorded in §1.

## Scope

**In Scope:**
WorkflowStatusResolver inversion, current_sub_phase field in BranchState, clearing semantics for sub_phase across all transition methods, PhaseStateEngine.record_sub_phase() seam, GitCommitTool trigger, blast radius production + test code, architecture principles compliance, clean-break contract.

**Out of Scope:**
Phase-interruption cycle-restore problem (separate issue), WorkflowStatusDTO public output field changes, QA baseline state (issue #292 scope), MCP tool output formats.

## Prerequisites

Read these first:
1. Issue #271 merged — contracts.yaml is SSOT for workflow-phase membership and ordering
2. Issue #231 merged — WorkflowStatusResolver, CommitPhaseDetector, BranchValidatedStateReader in production
3. Issue #292 merged — WorkflowStateMutator is coordinated write seam
---

## Problem Statement

WorkflowStatusResolver currently prefers commit-scope over state.json when confidence is high, making status reporting hybrid rather than state-owned. BranchState has no current_sub_phase field, so sub-phase context is lost when no workflow commits exist yet, and is not recoverable from state alone.

## Research Goals

- Invert resolver priority: state.json primary, commit-scope fallback/diagnostics only
- Add current_sub_phase: str | None = None to BranchState (backward-compatible)
- Add PhaseStateEngine.record_sub_phase() as the new public write seam
- Wire GitCommitTool to call record_sub_phase() after successful commit
- Clear current_sub_phase in transition(), force_transition(), transition_cycle() — NOT in on_exit_cycle_based_phase()
- Map full blast radius in production and test code
- Verify no architecture principles violations
- Confirm clean break — no backward compat retained

---

## Findings

### §1 — Decision: Combined Research + Design (no separate design phase)

The scope of this issue is bounded: two interacting but well-understood changes (resolver inversion + sub_phase persistence). The architecture contracts from issues #231, #271, and #292 are already established. All design decisions documented in this file are final and have been validated in the research session on 2026-05-04. There is no new architecture to discover in a separate design phase.

**Decision:** Force-transition from research to planning after this document is QA-approved.

---

### §2 — Resolver Inversion (state.json primary)

**Current behaviour** (`workflow_status_resolver.py` lines 43–80):

```python
# 1. Load persisted state (graceful, may return None)
branch_state = self._state.load(branch)

# 2. Parse latest commit
detection = self._detector.detect_from_commit(commit_message)

# 3. Commit-scope WINS when confidence == "high"  ← root problem
if detection["confidence"] in _HIGH_CONFIDENCE:
    return WorkflowStatusDTO(phase_source="commit-scope", ...)

# 4. Only then fall back to state
if persisted_phase is not None:
    return WorkflowStatusDTO(phase_source="state.json", ...)
```

**Required behaviour after #298:**

```
1. state.json present AND branch matches → use state (primary)
2. state.json absent (regardless of commit presence) → raise StateNotFoundError (strict: protocol violation)
3. state.json present BUT branch mismatch → raise StateBranchMismatchError
```

**Decision on fresh branches (no state.json):** STRICT. A branch without `state.json` is a protocol violation — `initialize_project` must always be called before any workflow tool. `resolve_current()` raises `StateNotFoundError` (distinct from `StateBranchMismatchError` which means "file present but wrong branch"). No silent fallback to commit-scope when state is expected.

**Exception types:**
- `StateBranchMismatchError` — state.json is present but records a different branch (existing type, unchanged semantics).
- `StateNotFoundError` — state.json is absent entirely (new type, distinct from `FileNotFoundError` to comply with §8 Explicit over Implicit — a missing workflow state file is a domain event, not a generic I/O error).

**Consumer error handling contract — two separate cases:**

*Case A — Tool layer (`discovery_tools.py`, line 152):* tool has access to `NoteContext`. Must:
1. Catch `StateNotFoundError` and `StateBranchMismatchError`.
2. Produce a `RecoveryNote` via `context.produce(RecoveryNote(...))` with actionable recovery guidance.
3. Return `ToolResult.error(...)` with a diagnostic message.

```python
context.produce(RecoveryNote(
    "No workflow state found for this branch. "
    "Run initialize_project(issue_number=<N>, workflow_name=<W>) to create state.json, "
    "or run git_checkout to a branch that has an active workflow."
))
return ToolResult.error(f"No workflow state for branch '{branch}': {e}")
```

*Case B — Manager layer (`project_manager.get_project_plan()`, line 460):* manager returns `dict | None` — no `NoteContext`, no `ToolResult`. This call is **informational phase-enrichment only** — the caller (`initialize_branch()`, line 122 of `phase_state_engine.py`) calls `get_project_plan()` **before** `state.json` is created. Making this a hard raise would break `InitializeProjectTool`. Must use **graceful degradation**:
1. Wrap `resolve_current()` in `try/except (StateNotFoundError, StateBranchMismatchError, OSError)`.
2. On exception, skip the phase-enrichment block — return `plan` without phase fields (`current_phase`, `phase_source`, `phase_detection_error` are absent from the returned dict).
3. Also fix the stale docstring: `"Uses commit-scope precedence: commit-scope > state.json > unknown"` must be rewritten to reflect the new contract.

**Recovery hint architecture:** `RecoveryNote` already exists in `mcp_server/core/operation_notes.py` and is used by `phase_tools.py` (via `StateMutationConflictError.recovery`) and `pr_tools.py`. The same pattern applies to `discovery_tools.py`.

**Impact on `WorkflowStatusDTO.phase_source` field:** the value `"state.json"` becomes the only non-error code path. `"commit-scope"` and `"unknown"` are removed from the resolver output — the resolver either returns a state-backed DTO or raises. No schema changes needed.

**Impact on `WorkflowStatusDTO.phase_confidence` field:** the state-fallback currently returns `phase_confidence="medium"` (signalling "best guess"). After inversion, state.json is the *authoritative* source — there is no ambiguity. The correct value for the state-primary path is `"high"`. The values `"medium"` and `"unknown"` are permanently dead code on the normal path. `WorkflowStatusDTO.phase_confidence` is narrowed to `Literal["high"]` (see §7). This is a **design decision**: `"high"` is chosen because state.json is written by the workflow engine itself — it is not a heuristic, it is the ground truth.

---

### §3 — current_sub_phase Field in BranchState

**Decision:** add `current_sub_phase: str | None = None` to `BranchState`.

- `frozen=True, extra="forbid"` — adding an optional field with `None` default is backward-compatible for existing persisted `state.json` files (Pydantic model_validate fills missing fields with default).
- `with_updates()` already supports additive schema evolution — no changes needed there.
- `FileStateRepository.save()` already serialises whatever the model contains.

**Persisted value format:** raw sub_phase name (`"red"`, `"green"`, `"refactor"`) — NOT the combined token (`"c1_red"`). Rationale: `current_cycle` is already persisted separately; combining them in the persisted value creates redundancy that can go stale. Consumers that need the combined token (`"c1_red"`) derive it from `current_cycle` + `current_sub_phase`.

---

### §4 — New Public Seam: PhaseStateEngine.record_sub_phase()

**Method signature:**

```python
def record_sub_phase(self, branch: str, sub_phase: str | None) -> None:
    """Persist the current sub_phase into branch state.

    Called by GitCommitTool after a successful commit.
    Passing None explicitly clears the persisted sub_phase.
    """
```

**Architecture rationale (ARCHITECTURE_PRINCIPLES.md §10 Cohesion):**
`PhaseStateEngine` already owns all workflow lifecycle mutations (enter/exit hooks, cycle tracking). Injecting `WorkflowStateMutator` directly into `GitCommitTool` would violate §1.1 SRP (tool layer reaching into state mutation infrastructure) and §7 Law of Demeter. One new engine method is the correct extension point.

**Implementation:** delegates to `self._workflow_state_mutator.apply()`:

```python
self._workflow_state_mutator.apply(branch, lambda s: s.with_updates(current_sub_phase=sub_phase))
```

---

### §5 — GitCommitTool Trigger Point

`GitCommitTool` already receives `state_engine=self.phase_state_engine` from `server.py`. The trigger is a post-commit call after `commit_hash = self.manager.commit_with_scope(...)`:

```python
if self._state_engine is not None:
    self._state_engine.record_sub_phase(current_branch, params.sub_phase)
```

`params.sub_phase` is already validated by `ScopeEncoder` inside `commit_with_scope()`; no double-validation needed.

**Intent: always-write-on-commit.** When `params.sub_phase is None` (user commits without specifying a sub_phase), `record_sub_phase(branch, None)` is called and `current_sub_phase` is explicitly cleared to `None`. Rationale: a commit without a sub_phase signals that the operator is not currently in a named sub_phase step. Retaining a stale sub_phase from a previous commit in the same cycle would misrepresent state. Always-write is simple, deterministic, and consistent with how `current_cycle` is written on every transition regardless of whether it changed.

---

### §6 — Clearing Semantics for current_sub_phase

**Key insight:** `current_sub_phase` is *phase-level* context, not *cycle-level* context. It must be cleared at every phase boundary, not just at cycle-based phase exit.

| Method | Change | Rationale |
|---|---|---|
| `transition()` | add `current_sub_phase=None` to `with_updates()` | Every phase boundary resets sub_phase |
| `force_transition()` | add `current_sub_phase=None` to `with_updates()` | Same — forced transitions are still phase boundaries |
| `transition_cycle()` | add `current_sub_phase=None` to `with_updates()` | New cycle = new TDD step, previous sub_phase no longer valid |
| `on_exit_cycle_based_phase()` | **NO CHANGE** | Hook owns only cycle-tracking (last_cycle, current_cycle). Adding sub_phase here would conflate two responsibilities and the name would become inaccurate. |

**Architecture compliance check (§1.1 SRP, §10 Cohesion):** keeping `on_exit_cycle_based_phase()` focused on cycle-tracking is correct. The clearing in `transition()` / `force_transition()` is already where `current_phase` is written — same `with_updates()` call, same responsibility (phase state transition).

---

### §7 — Blast Radius: Production Code

Files requiring changes:

| File | Change | Type |
|---|---|---|
| `mcp_server/managers/state_repository.py` | Add `current_sub_phase: str | None = None` to `BranchState`; add `StateNotFoundError` exception class | **Schema extension + new exception** |
| `mcp_server/managers/workflow_status_resolver.py` | Invert resolve logic: state primary, raise `StateNotFoundError` / `StateBranchMismatchError` when state absent or mismatched | **Logic inversion + strict error** |
| `mcp_server/managers/phase_state_engine.py` | Add `record_sub_phase()` method; add `current_sub_phase=None` to `transition()`, `force_transition()`, `transition_cycle()` | **New seam + clearing** |
| `mcp_server/tools/git_tools.py` (`GitCommitTool.execute()`) | Call `self._state_engine.record_sub_phase(branch, params.sub_phase)` after successful commit | **New call** |
| `mcp_server/managers/project_manager.py` (line 460) | Wrap `resolve_current()` call in `try/except (StateNotFoundError, StateBranchMismatchError, OSError)` → skip phase-enrichment block on error (graceful degradation, not hard error — called by `initialize_branch()` before state.json exists). Fix stale docstring. **Add imports:** `from mcp_server.managers.state_repository import StateNotFoundError, StateBranchMismatchError`. | **Graceful degradation + import** |
| `mcp_server/tools/discovery_tools.py` (line 152) | **Remove `del context` (line 137)**; add a separate `except (StateNotFoundError, StateBranchMismatchError)` clause above the existing `except (OSError, ValueError, RuntimeError)` block; produce `RecoveryNote` + return `ToolResult.error`. The existing graceful I/O error path is retained unchanged. | **Error handling + RecoveryNote** |
| `mcp_server/state/workflow_status.py` | Narrow `phase_source: Literal["commit-scope", "state.json", "unknown"]` → `Literal["state.json"]`. Narrow `phase_confidence: Literal["high", "medium", "unknown"]` → `Literal["high"]`. Both `"commit-scope"`, `"unknown"` (phase_source) and `"medium"`, `"unknown"` (phase_confidence) are permanently dead code on the normal path after inversion. See §2 for rationale on `"high"`. | **Type narrowing — clean break** |

Files with **no required changes**:

- `mcp_server/managers/workflow_state_mutator.py` — no new seam needed here; `record_sub_phase()` uses existing `apply()`
- `mcp_server/managers/git_manager.py` — `commit_with_scope()` signature unchanged
- `mcp_server/core/phase_detection.py` / `scope_encoder.py` — unchanged

---

### §8 — Blast Radius: Test Code

**Tests that assert `phase_source == "commit-scope"` — will break after inversion:**

| File | Test(s) | Change needed |
|---|---|---|
| `tests/mcp_server/unit/managers/test_workflow_status_resolver.py` | `test_resolve_uses_commit_scope_when_high_confidence` — asserts `phase_source="commit-scope"` | Rewrite: when state present, expect `phase_source="state.json"` |
| `tests/mcp_server/unit/managers/test_workflow_status_resolver.py` | `test_resolve_current_returns_dto` — asserts only `isinstance(result, WorkflowStatusDTO)`; no phase_source assertion | **No change needed** |
| `tests/mcp_server/unit/managers/test_workflow_status_resolver.py` | `test_resolve_handles_branch_mismatch_gracefully` (line 231) — asserts `phase_source in ("unknown", "state.json")`; after #298, mismatch raises rather than returning `"unknown"` | Rewrite: expect `StateBranchMismatchError` |
| `tests/mcp_server/unit/tools/test_discovery_tools.py` | Multiple `phase_source="commit-scope"` assertions (lines 230, 479, 756, 785) | Update to `"state.json"` where state is the expected source |
| `tests/mcp_server/unit/tools/test_project_tools.py` | `phase_source="commit-scope"` (lines 1020, 1034) | Update |
| `tests/mcp_server/unit/managers/test_project_manager.py` | `test_get_project_plan_uses_resolver_phase` (line 734), `test_get_project_plan_formats_phase_colon_sub_phase` (line 755) — use commit-scope mock setup | Update |
| `tests/mcp_server/unit/managers/test_project_manager.py` | `test_get_project_plan_includes_current_phase_from_commit_scope` (line 320), `test_get_project_plan_returns_unknown_when_no_commits` (line 344) — test the now-removed commit-scope/unknown code path | Rewrite: state-present → state used; state-absent → phase fields absent in result |

**Tests for `on_exit_cycle_based_phase` — must NOT change:**

| File | Test(s) | Status |
|---|---|---|
| `tests/mcp_server/unit/managers/test_phase_state_engine.py` | Lines 174, 206, 520 — assert only `last_cycle` and `current_cycle` | **No change** — correct scope |

**New tests needed:**

| Scope | Test description |
|---|---|
| `BranchState` | `current_sub_phase` defaults to `None`; persists and round-trips via `FileStateRepository` |
| `PhaseStateEngine.record_sub_phase()` | Writes sub_phase to state; calling with `None` clears it |
| `PhaseStateEngine.transition()` | After transition, `current_sub_phase` is `None` |
| `PhaseStateEngine.force_transition()` | After force-transition, `current_sub_phase` is `None` |
| `PhaseStateEngine.transition_cycle()` | After cycle transition, `current_sub_phase` is `None` |
| `GitCommitTool.execute()` | After commit with `sub_phase="red"`, engine.record_sub_phase called with `"red"` |
| `GitCommitTool.execute()` | After commit with `sub_phase=None`, engine.record_sub_phase called with `None` (always-write semantics) |
| `WorkflowStatusResolver.resolve_current()` | State present → returns `phase_source="state.json"` even when high-confidence commit exists |
| `WorkflowStatusResolver.resolve_current()` | State present → returns `phase_confidence="high"` (not `"medium"`) |
| `WorkflowStatusResolver.resolve_current()` | State absent → raises `StateNotFoundError` |
| `WorkflowStatusResolver.resolve_current()` | State present but branch mismatch → raises `StateBranchMismatchError` |
| `WorkflowStatusDTO` | `phase_source="commit-scope"` rejected at construction (Literal narrowed to `"state.json"`) |
| `WorkflowStatusDTO` | `phase_confidence="medium"` rejected at construction (Literal narrowed to `"high"`) |
| `project_manager.get_project_plan()` | State absent → returns plan `dict` without phase-enrichment fields (`current_phase` / `phase_source` / `phase_detection_error` absent, or `phase_source="unavailable"`) |
| `discovery_tools.get_work_context()` | State absent → returns `ToolResult.error` with `RecoveryNote` in context |

---

### §9 — Architecture Principles Compliance

| Principle | Check | Status |
|---|---|---|
| **§1.1 SRP** | `record_sub_phase()` on `PhaseStateEngine` keeps mutation inside engine; `GitCommitTool` does not touch `WorkflowStateMutator` directly | ✅ |
| **§1.4 ISP** | `GitCommitTool` injects `PhaseStateEngine` (already does); no new write interface injected into tool | ✅ |
| **§1.5 DIP** | No new direct instantiation inside `execute()`; `record_sub_phase()` is a method on the already-injected engine | ✅ |
| **§2 DRY/SSOT** | `current_sub_phase` stored as raw name (`"red"`); combined token derived at read time from `current_cycle` + `current_sub_phase` | ✅ |
| **§3 Config-First** | No hardcoded phase or sub_phase names; sub_phase values validated by `ScopeEncoder` against `workphases.yaml` before reaching engine | ✅ |
| **§5 CQS** | `record_sub_phase()` is a command (mutates state, returns None); `resolve_current()` is a query (reads, returns DTO) | ✅ |
| **§7 Law of Demeter** | `GitCommitTool` → `PhaseStateEngine.record_sub_phase()` (one hop); tool does not reach into mutator | ✅ |
| **§8 Explicit over Implicit** | Absent state raises `StateNotFoundError` (strict); present-but-mismatched state raises `StateBranchMismatchError`; no silent fallback to commit-scope when state is expected. Case B exception (`project_manager.get_project_plan()` graceful degradation) is a documented bootstrapping constraint — see §2 | ✅ |
| **§14 Test via Public API** | New tests call `engine.record_sub_phase()` and `resolver.resolve_current()` — both are public methods | ✅ |

---

### §10 — Clean Break Contract (No Backward Compat)

**Removed behaviour (no compat layer):**

1. `WorkflowStatusResolver` will no longer return `phase_source="commit-scope"` when state.json is present and branch matches. Tests that assert this are **rewritten**, not guarded behind a flag.
2. `WorkflowStatusResolver` will no longer silently return `phase_source="unknown"` when state is absent — it will raise. No `ignore_missing_state=False` parameter. One contract, one code path.
3. `WorkflowStatusDTO.phase_source` is narrowed from `Literal["commit-scope", "state.json", "unknown"]` to `Literal["state.json"]`. Mypy will reject any remaining uses of the dead values — including tests that are being rewritten.
4. `WorkflowStatusDTO.phase_confidence` is narrowed from `Literal["high", "medium", "unknown"]` to `Literal["high"]`. State.json is authoritative; `"medium"` (fallback heuristic) and `"unknown"` are permanently gone.

**Backward-compatible changes (no migration needed):**

1. `BranchState.current_sub_phase` defaults to `None` — existing `state.json` files deserialise without error.
2. `PhaseStateEngine.record_sub_phase()` is a new public method — no existing callers to update.
3. `on_exit_cycle_based_phase()` signature unchanged — all existing callers unaffected.

---

### §11 — Known Limitation (Out of Scope)

**Phase-interruption cycle loss:** when `force_transition()` moves from `implementation` (cycle N, sub_phase X) to another phase and back, `on_enter_cycle_based_phase()` re-initialises `current_cycle=1` and overwrites `last_cycle`. Cycle and sub_phase context from the interrupted position is lost.

This is a pre-existing limitation of the current state model. Fixing it requires a `suspended_cycle` / `suspended_sub_phase` concept and new semantics in `on_enter_cycle_based_phase()`. Tracked as a separate follow-up issue.

## Related Documentation
- **[docs/development/issue231/research-state-json-absolute-ssot-impact.md][related-1]**
- **[docs/development/issue271/design.md][related-2]**
- **[mcp_server/managers/workflow_status_resolver.py][related-3]**
- **[mcp_server/managers/phase_state_engine.py][related-4]**
- **[mcp_server/managers/state_repository.py][related-5]**

<!-- Link definitions -->

[related-1]: docs/development/issue231/research-state-json-absolute-ssot-impact.md
[related-2]: docs/development/issue271/design.md
[related-3]: mcp_server/managers/workflow_status_resolver.py
[related-4]: mcp_server/managers/phase_state_engine.py
[related-5]: mcp_server/managers/state_repository.py

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |
| 1.1 | 2026-05-04 | imp | Fixed QA annotations A1–A5: resolver contract strict (StateNotFoundError); A2 correct exception type; A3 correct mutator attribute name; A4 always-write-on-commit semantics; A5 project_manager + discovery_tools blast radius + RecoveryNote pattern |
| 1.2 | 2026-05-04 | imp | Fixed QA annotations A6–A8: A6 project_manager graceful degradation (not ToolResult.error — called before state.json exists in initialize_branch); A7 named all affected tests in blast radius table; A8 removed redundant resolver case 4 |
| 1.3 | 2026-05-04 | imp | Fixed QA annotations NEW-A–NEW-C: NEW-A correct test contract for project_manager (dict not ToolResult); NEW-B add "remove del context" to discovery_tools blast radius; NEW-C §9 §8 principle note for Case B bootstrapping exception |
| 1.4 | 2026-05-04 | imp | Fixed QA annotation A-FINAL-1: §7 discovery_tools.py entry now specifies separate catch clause (above existing OSError block), not extension of existing catch |
| 1.5 | 2026-05-04 | imp | Fixed external QA F-1–F-3: F-1 workflow_status.py added to blast radius (phase_source Literal narrowed); F-2 phase_confidence="high" decision documented in §2 + §7 + §8 + §10; F-3 import-gap for project_manager.py added to §7 |
| 1.6 | 2026-05-04 | imp | Minor post-QA corrections: §8 test_resolve_current_returns_dto no-change (isinstance only); §2 Case B simplified to single option (skip phase-enrichment, no "unavailable" alternative) |