<!-- docs\development\issue335\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-13T10:46Z updated=2026-05-13 -->
# initialize_branch() existence guard

**Status:** FINAL  
**Version:** 1.0  
**Last Updated:** 2026-05-13

---

## Summary

Single TDD cycle. Three production files and one test file change.
Reference design: [design.md](design.md).

---

## Scope

**In:**
- `mcp_server/managers/state_repository.py` — `StateAlreadyExistsError`
- `mcp_server/managers/phase_state_engine.py` — guard + import
- `mcp_server/tools/project_tools.py` — `except`-tuple + new import
- `tests/mcp_server/unit/managers/test_phase_state_engine_persistence.py` — one new test

**Out:**
- Pre-existing failing tests from issue #257 cycle
- `InitializeProjectTool` tool-layer tests
- `enforcement.yaml`, discovery tools, anything from issue #268

---

## TDD Cycles

### Cycle 1: StateAlreadyExistsError guard

**Goal:** `initialize_branch()` raises `StateAlreadyExistsError` when called for a branch
that already has persisted state.

#### RED — Failing test

Add to `TestPhaseStateEnginePersistence` in
`tests/mcp_server/unit/managers/test_phase_state_engine_persistence.py`:

```python
from mcp_server.managers.state_repository import StateAlreadyExistsError

def test_initialize_branch_raises_if_state_already_exists(
    self,
    state_engine: PhaseStateEngine,
) -> None:
    state_engine.initialize_branch("feature/1-first-feature", 1, "research")

    with pytest.raises(StateAlreadyExistsError, match="feature/1-first-feature"):
        state_engine.initialize_branch("feature/1-first-feature", 1, "research")
```

Import `StateAlreadyExistsError` — which does not exist yet — causes `ImportError`.
Test must fail (red) before any production change.

#### GREEN — Minimal implementation

**Step 1 — `state_repository.py`**: add after `StateNotFoundError` (line 27):

```python
class StateAlreadyExistsError(Exception):
    """Raised when initialize_branch() is called for a branch that already has state.

    Prevents accidental overwrite of existing BranchState and phase history.
    """
```

**Step 2 — `phase_state_engine.py`**: extend existing import (line 42):

```python
# Before
from mcp_server.managers.state_repository import BranchState, StateBranchMismatchError

# After
from mcp_server.managers.state_repository import (
    BranchState,
    StateAlreadyExistsError,
    StateBranchMismatchError,
)
```

Insert guard as the first statement inside `initialize_branch()` body (before
`project = self.project_manager.get_project_plan(issue_number)`):

```python
try:
    _loaded = self._state_repository.load(branch)
    if _loaded.branch == branch:
        raise StateAlreadyExistsError(
            f"Branch '{branch}' already has an initialized state "
            f"(phase: {_loaded.current_phase}). "
            "Call initialize_project only once per branch."
        )
except (FileNotFoundError, KeyError, OSError, json.JSONDecodeError, ValidationError):
    pass
```

**Step 3 — `project_tools.py`**: add import after line 25
(`from mcp_server.managers.project_manager import ...`):

```python
from mcp_server.managers.state_repository import StateAlreadyExistsError
```

Extend `except`-tuple (currently line ~286):

```python
# Before
except (ValueError, OSError, RuntimeError) as e:

# After
except (ValueError, OSError, RuntimeError, StateAlreadyExistsError) as e:
```

#### REFACTOR

No refactor expected. Guard is minimal and already clean.
Run quality gates to confirm.

#### Exit criteria

- `test_initialize_branch_raises_if_state_already_exists` passes ✅
- `test_initializing_second_branch_overwrites_state_json_completely` still passes ✅
  (uses two **different** branch names — must not be affected)
- All other previously-passing tests remain green ✅
- Quality gates: ruff format, ruff lint, mypy strict on changed files ✅

---

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| `InMemoryStateRepository.load()` raises `KeyError` instead of `FileNotFoundError` | Certain | Both caught in guard `except`-tuple |
| Corrupt `state.json` (`JSONDecodeError`, `ValidationError`) blocks init | Possible | Both caught — fail open |
| Import cycle between `project_tools` and `state_repository` | Low | `state_repository` has no upstream deps within `mcp_server` |

---

## Related Documentation

- [design.md](design.md) — chosen design and all key decisions
- [research.md](research.md) — findings F_335.1–F_335.6
- `mcp_server/managers/state_repository.py` — exception hierarchy (lines 17–27)
- `mcp_server/managers/phase_state_engine.py` — `initialize_branch()` (lines 103–155)
- `mcp_server/tools/project_tools.py` — `except`-tuple (~line 286)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-13 | Agent | Initial planning — single cycle, all steps specified |
