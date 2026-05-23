<!-- docs\development\issue335\design.md -->
<!-- template=design version=5827e841 created=2026-05-13T10:35Z updated=2026-05-13 -->
# initialize_branch() existence guard

**Status:** FINAL  
**Version:** 1.0  
**Last Updated:** 2026-05-13

---

## 1. Context & Requirements

### 1.1. Problem Statement

`PhaseStateEngine.initialize_branch()` overwrites `state.json` without checking if a
`BranchState` for the given branch already exists, silently resetting phase history.

### 1.2. Requirements

**Functional:**
- [ ] `initialize_branch()` raises `StateAlreadyExistsError` when a `BranchState` for the
  given branch already exists in the state repository
- [ ] All other `initialize_branch()` behavior is unchanged (project lookup, parent_branch
  resolution, uncommitted-changes warning, return dict)
- [ ] `InitializeProjectTool.execute()` converts `StateAlreadyExistsError` to a
  `ToolResult.error()` with the exception message

**Non-Functional:**
- [ ] `StateAlreadyExistsError` inherits from `Exception` — consistent with peer exceptions
  `StateBranchMismatchError` and `StateNotFoundError` in `state_repository.py`
- [ ] No import-time side effects introduced
- [ ] Fix surface: 3 production files + 1 test file

### 1.3. Constraints

- Do not modify any pre-existing failing tests (issue #257 cycle failures are unrelated)
- Do not add any new public methods to `PhaseStateEngine`
- The guard must use the already-injected `_state_repository` — no new dependency

---

## 2. Design

### 2.1. New exception — `state_repository.py`

Add `StateAlreadyExistsError` as a peer to the existing domain exceptions:

```python
class StateAlreadyExistsError(Exception):
    """Raised when initialize_branch() is called for a branch that already has state.

    Prevents accidental overwrite of existing BranchState and phase history.
    """
```

**Location:** `mcp_server/managers/state_repository.py`, after `StateNotFoundError`.

### 2.2. Guard in `initialize_branch()` — `phase_state_engine.py`

Insert a guard block at the top of `initialize_branch()`, before the project lookup:

```python
# Guard: refuse to overwrite an existing BranchState for this branch
import json  # already imported at module level
try:
    loaded = self._state_repository.load(branch)
    if loaded.branch == branch:
        raise StateAlreadyExistsError(
            f"Branch '{branch}' already has an initialized state "
            f"(phase: {loaded.current_phase}). "
            "Call initialize_project only once per branch."
        )
except (FileNotFoundError, KeyError, OSError, json.JSONDecodeError, ValidationError):
    pass  # no existing state for this branch — proceed normally
```

**Why `loaded.branch == branch` comparison?** `state.json` holds state for exactly one
branch at a time. If `load()` succeeds but the stored branch name differs, the file
belongs to a *previous* branch — overwriting it is safe (normal branch-switch flow).
Only when the stored branch equals the requested branch do we have a collision.

**Exceptions caught and swallowed:**

| Exception | Reason |
|---|---|
| `FileNotFoundError` | `state.json` absent → no prior state, safe to proceed |
| `KeyError` | `InMemoryStateRepository` branch absent → no prior state |
| `OSError` | File system error reading state → fail open (do not block init) |
| `json.JSONDecodeError` | Corrupt `state.json` → reconstruction will fix it later |
| `ValidationError` | Invalid schema in `state.json` → same as corrupt |

**Import required:** `StateAlreadyExistsError` imported from `state_repository` at the
top of `phase_state_engine.py` (alongside `StateBranchMismatchError`).

### 2.3. Tool layer — `project_tools.py`

Extend the `except`-tuple in `InitializeProjectTool.execute()`:

```python
# Before
except (ValueError, OSError, RuntimeError) as e:
    return ToolResult.error(str(e))

# After
except (ValueError, OSError, RuntimeError, StateAlreadyExistsError) as e:
    return ToolResult.error(str(e))
```

`StateAlreadyExistsError` must be imported at the top of `project_tools.py`.

### 2.4. Test — `test_phase_state_engine_persistence.py`

One new test in `TestPhaseStateEnginePersistence`:

```python
def test_initialize_branch_raises_if_state_already_exists(
    self,
    state_engine: PhaseStateEngine,
) -> None:
    state_engine.initialize_branch("feature/1-first-feature", 1, "research")

    with pytest.raises(StateAlreadyExistsError, match="feature/1-first-feature"):
        state_engine.initialize_branch("feature/1-first-feature", 1, "research")
```

This test uses the existing `state_engine` fixture (which uses `FileStateRepository` via
`tmp_path`) and the already-initialized project with `issue_number=1`.

---

## 3. Chosen Design

**Decision:** Option B — `StateAlreadyExistsError(Exception)` + guard in
`initialize_branch()` + one word added to `except`-tuple in `InitializeProjectTool.execute()`

**Rationale:** Consistent with existing exception hierarchy; semantically precise;
`ValueError` semantics do not apply (the value is valid, the system state is the
problem); tool layer change is minimal and keeps error propagation clean.

### 3.1. Key Design Decisions

| Decision | Rationale |
|---|---|
| `StateAlreadyExistsError(Exception)` not `(ValueError)` | Consistent with `StateBranchMismatchError`, `StateNotFoundError`; `ValueError` semantics wrong for a state-collision scenario |
| Guard uses `_state_repository.load()`, not a new method | Uses existing injected seam; no new dependency or interface change |
| `loaded.branch == branch` comparison | Distinguishes collision from normal branch-switch overwrite |
| Fail open on `OSError`, `JSONDecodeError`, `ValidationError` | Corrupt/missing state should not block initialization; reconstruction handles it |
| Tool layer: add to `except`-tuple, not a new `except` block | Minimal change; all state errors map to `ToolResult.error(str(e))` equally |

---

## Related Documentation

- [research.md](research.md) — findings F_335.1–F_335.6
- `mcp_server/managers/state_repository.py` — exception hierarchy
- `mcp_server/managers/phase_state_engine.py` — `initialize_branch()` lines 103–155
- `mcp_server/tools/project_tools.py` — `InitializeProjectTool.execute()` except-tuple

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-13 | Agent | Initial design — Option B, all decisions documented |
