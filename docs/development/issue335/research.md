<!-- docs\development\issue335\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-13T09:46Z updated=2026-05-13 -->
# initialize_project silently overwrites state.json on existing branch

**Status:** FINAL  
**Version:** 1.0  
**Last Updated:** 2026-05-13

---

## Problem Statement

`PhaseStateEngine.initialize_branch()` creates a fresh `BranchState` and overwrites `state.json`
without checking if a state for the branch already exists, silently resetting phase history.

## Research Goals

- Document exact code path responsible for the bug
- Identify the minimal fix location
- Identify what exception to raise and where
- List all test files that must be updated

---

## Findings

### F_335.1 — Bug location: `initialize_branch()` has no existence check

**File:** `mcp_server/managers/phase_state_engine.py`  
**Class:** `PhaseStateEngine`  
**Method:** `initialize_branch()` (line 103)

The method unconditionally builds a fresh `BranchState` and calls `_apply_state()`, which
routes through `IWorkflowStateMutator.apply()` → `IStateRepository.save()`. There is no check
whether the repository already holds a state for the given `branch` parameter.

```python
# Current code — no guard before write
state = BranchState(branch=branch, ...)
self._apply_state(branch, state)          # ← always overwrites
```

### F_335.2 — State existence can be probed via `_state_repository.load()`

The injected `_state_repository` exposes a `load(branch)` method (part of `IStateReader`):

| Repository | "Not found" signal |
|---|---|
| `FileStateRepository` | `FileNotFoundError` (file absent) |
| `InMemoryStateRepository` | `KeyError` (key absent) |

After a successful load, the loaded state's `branch` field must be compared with the
requested branch. If they differ, `state.json` holds state for a *different* branch — it is
safe to overwrite (this is the normal branch-switch scenario).

Guard pseudo-code:
```python
try:
    loaded = self._state_repository.load(branch)
    if loaded.branch == branch:
        raise StateAlreadyExistsError(branch)
except (FileNotFoundError, KeyError, OSError, json.JSONDecodeError, ValidationError):
    pass  # no state for this branch — proceed
```

### F_335.3 — `StateAlreadyExistsError` does not yet exist; add it to `state_repository.py`

`mcp_server/managers/state_repository.py` already defines the domain-exception hierarchy
for state errors:

- `StateBranchMismatchError` — loaded state branch ≠ requested branch
- `StateNotFoundError` — state.json absent for the requested branch

The new exception `StateAlreadyExistsError` belongs in the same module as a peer of these.
Callers (tool layer and tests) import it from there.

### F_335.4 — `InitializeProjectTool` needs no change

`mcp_server/tools/project_tools.py` calls `state_engine.initialize_branch()` inside a
`lambda`. The exception will propagate naturally; the tool's existing error formatting
path handles it. No changes needed in the tool layer.

### F_335.5 — Affected test files

| File | Action needed |
|---|---|
| `tests/mcp_server/unit/managers/test_phase_state_engine_persistence.py` | Add: `test_initialize_branch_raises_if_state_already_exists` |
| `tests/mcp_server/unit/managers/test_phase_state_engine_persistence.py` | Keep: `test_initializing_second_branch_overwrites_state_json_completely` — different branch, must still pass |
| `tests/mcp_server/unit/managers/test_phase_state_engine_parent_branch.py` | Keep unchanged — all use unique branch names per test |

No existing passing test calls `initialize_branch` twice with the **same** branch name,
so the fix introduces zero new test breakage for currently-passing tests.

### F_335.6 — Pre-existing test failures are unrelated

`temp/test_results.txt` records ~100 failing tests from the active issue #257 cycle.
None of these concern `initialize_branch()` existence-guard logic. The fix for #335
must not touch those test files.

---

## Conclusions

| # | Finding | Decision |
|---|---|---|
| F_335.1 | No guard before write in `initialize_branch()` | Add guard check |
| F_335.2 | Existence detected via `_state_repository.load()` + branch compare | Use this pattern |
| F_335.3 | New exception `StateAlreadyExistsError` needed | Add to `state_repository.py` |
| F_335.4 | Tool layer (`project_tools.py`) unchanged | Confirmed out of scope |
| F_335.5 | One new test needed; no existing passing test breaks | Confirmed |
| F_335.6 | Pre-existing #257 failures are unrelated | Do not touch |

**Minimal fix surface:**
1. `mcp_server/managers/state_repository.py` — add `StateAlreadyExistsError`
2. `mcp_server/managers/phase_state_engine.py` — add guard in `initialize_branch()`
3. `tests/mcp_server/unit/managers/test_phase_state_engine_persistence.py` — add one test

---

## Related Documentation

- Issue #335: initialize_project silently overwrites state.json on existing branch
- Issue #268 research finding F_268.10 (identified the bug prerequisite)
- `mcp_server/managers/phase_state_engine.py` — `initialize_branch()` lines 103–155
- `mcp_server/managers/state_repository.py` — exception hierarchy, `IStateReader.load()`

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-13 | Agent | Initial research — all findings complete |
