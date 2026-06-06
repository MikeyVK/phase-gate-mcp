<!-- docs\development\issue371\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-06T18:21Z updated= -->
# Replace remaining direct state.json reads with IStateReader (#371)

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-06-06

---

## Scope

**In Scope:**
Three production files: mcp_server/managers/enforcement_runner.py (2 sites), mcp_server/tools/cycle_tools.py (2 sites, in TransitionCycleTool and ForceCycleTransitionTool), mcp_server/core/phase_detection.py (1 site, ScopeDecoder._read_state_json). Constructor injection of IStateReader and wiring in server.py composition root.

**Out of Scope:**
IStateRepository write paths. WorkflowStateMutator. QAManager, QAStateRepository. ScopeDecoder state_path used for workphases.yaml or any path other than state.json. Refactoring IStateReader interface itself.

---

## Problem Statement

Three production modules bypass IStateRepository/IStateReader and read state.json via raw file I/O (json.loads + Path.read_text / json.load + Path.open). This leaves a race window against concurrent WorkflowStateMutator writes and violates the Dependency Inversion Principle.

## Research Goals

- Identify all raw state.json read sites in production code
- Determine a uniform IStateReader injection strategy across all sites
- Confirm preserved behavior and invariants per call site
- Establish Approved Strategy before planning

---

## Background

Deferred from issue #230 research (DEFERRED-2). The IStateReader/IStateRepository abstraction and FileStateRepository implementation are already in place. BranchValidatedStateReader wraps IStateReader and enforces branch-match semantics. The composition root in server.py already wires a shared FileStateRepository into QAManager, WorkflowStatusResolver, and GitCommitTool. The pattern is established; three consumers were left behind.

---

## Findings

## Call-Site Audit

| File | Lines | Field read | Context |
|---|---|---|---|
| `mcp_server/managers/enforcement_runner.py` | 39 | `current_phase` | Module-level function `_read_current_phase(server_root)` called from `EnforcementRunner.run()` |
| `mcp_server/managers/enforcement_runner.py` | 391 | `issue_number` | Method `_check_context_loaded()` — mismatch bypass: compares state issue_number to branch issue |
| `mcp_server/tools/cycle_tools.py` | 132 | `branch` | `TransitionCycleTool._get_current_branch()` — git fallback when `get_current_branch()` raises |
| `mcp_server/tools/cycle_tools.py` | 265 | `branch` | `ForceCycleTransitionTool._get_current_branch()` — identical git fallback |
| `mcp_server/core/phase_detection.py` | 226 | `current_phase` | `ScopeDecoder._read_state_json()` — one of several phase-detection sources; takes `state_path: Path` as constructor arg |

## Uniform Fix Strategy

All five sites read one or two fields from `BranchState`. The uniform replacement pattern is:

1. **Inject `IStateReader`** via constructor parameter (existing pattern: `QAManager`, `GitCommitTool`, `BranchParentReader`).
2. **Replace raw read** with `state_reader.load(branch) -> BranchState`, then access the typed field.
3. **Handle `FileNotFoundError` / `StateNotFoundError`** where the original code handled missing file — the `IStateReader.load()` contract raises `FileNotFoundError` when state is absent.
4. **Wire in server.py** composition root using the shared `FileStateRepository` instance (same instance already used by other consumers).

### Per-site specifics

**enforcement_runner.py line 39** (`_read_current_phase`): This is a module-level helper that takes `server_root`. After the refactor it becomes unnecessary — `EnforcementRunner` already has `self.server_root`; inject `state_reader: IStateReader` into `EnforcementRunner.__init__` and inline the read as `self._state_reader.load(branch).current_phase` (catching `FileNotFoundError` → return None).

**enforcement_runner.py line 391** (`_check_context_loaded`): Same injected reader; replace `json.loads(...)` with `self._state_reader.load(branch)` and read `.issue_number`.

**cycle_tools.py lines 132 + 265**: Both `_get_current_branch` methods are structurally identical. Inject `state_reader: IStateReader` into each tool's constructor. Replace the fallback block: catch `FileNotFoundError` from `state_reader.load(branch_hint)` or use a list-branches approach — but since the fallback needs to know the branch to call `load(branch)`, the most defensible fix is to keep the fallback as-is if no branch hint is available, or inject a `IStateReader` that exposes a `list_branches()` variant. Simpler: since `FileStateRepository.load()` requires a branch, and the fallback is used precisely when git cannot tell us the branch, the correct fallback is to scan `state.json` directly only here, or to introduce a `load_any() -> BranchState | None` method. **Alternative**: keep the raw read for the branch-unknown fallback only, wrap it in a narrow private helper, and accept it as a documented exception. This preserves the race-window fix for the main path (enforcement, phase detection) while acknowledging the cycle_tools fallback is structurally constrained.

**phase_detection.py line 226** (`ScopeDecoder._read_state_json`): `ScopeDecoder` currently takes `state_path: Path` from the composition root. Replace with `state_reader: IStateReader` and a `branch: str` parameter (the active branch) so `load(branch)` can be called. The composition root already knows the active branch for this call site. Alternatively, keep `state_path` and only wrap in a thin adapter — but this is less uniform.

## Preservation Goals

- `_read_current_phase` returning `None` when state absent → `FileNotFoundError` catch → return None
- `_check_context_loaded` mismatch bypass on exception → wrap `load()` in try/except same as existing `except Exception: pass`
- `_get_current_branch` fallback returning `state.branch` field → preserve semantics, constrained by load(branch) signature
- `ScopeDecoder._read_state_json` graceful degradation on missing/malformed state → wrap `load()` in try/except OSError/FileNotFoundError → return None

## Risky Boundaries

- `cycle_tools._get_current_branch`: the fallback reads state.json when git is unavailable and no branch is known yet — `IStateReader.load(branch)` requires a branch argument, creating a chicken-and-egg problem. This is the only call site that cannot be trivially unified without either a `load_any()` extension or a documented narrow exception.
- `ScopeDecoder`: currently receives `state_path` from the composition root. Changing to `IStateReader + branch` widens its constructor signature and changes the wiring in server.py.
- `EnforcementRunner`: module-level `_read_current_phase` is called with `server_root` at multiple points; injecting reader into the class and removing the module-level function changes the external call surface (if tested directly).

## Related Documentation
- **[docs/development/issue230/research.md][related-1]**
- **[docs/development/issue230/planning.md][related-2]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-3]**

<!-- Link definitions -->

[related-1]: docs/development/issue230/research.md
[related-2]: docs/development/issue230/planning.md
[related-3]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md

---

## Approved Strategy

**Boundary:** All raw state.json read sites in `enforcement_runner.py`, `cycle_tools.py`, and `phase_detection.py`.

**Selected strategy:** Constructor-inject `IStateReader` uniformly across 4 of 5 sites. Accept one documented exception.

**Rationale and per-site decisions:**

| Site | Strategy | Rationale |
|---|---|---|
| `enforcement_runner.py:39` — `_read_current_phase` | Inject `IStateReader` into `EnforcementRunner.__init__`; replace module-level helper | Eliminates raw I/O on main enforcement path; removes `_read_current_phase` module function |
| `enforcement_runner.py:391` — `_check_context_loaded` | Same injected reader; replace `json.loads(...)` with `self._state_reader.load(branch).issue_number` | Same instance, no extra constructor param needed |
| `cycle_tools.py:132` — `TransitionCycleTool._get_current_branch` | **Documented exception**: raw read retained for git-unavailable fallback | `IStateReader.load(branch)` requires a branch arg — precisely what is unknown in this fallback path. Race risk is absent when git is unavailable. Wrap in narrow private helper with explanatory comment. |
| `cycle_tools.py:265` — `ForceCycleTransitionTool._get_current_branch` | Same documented exception as above | Structurally identical situation |
| `phase_detection.py:226` — `ScopeDecoder._read_state_json` | Replace `state_path: Path` constructor arg with `state_reader: IStateReader` + `branch: str`; call `load(branch)` | Composition root already knows the active branch; uniform with other consumers |

**Dead-code cleanup constraint:** After injecting `IStateReader`, any methods, variables, or constructor parameters rendered unused by the removal of raw reads must be deleted. Specifically: `_read_current_phase` module-level function in `enforcement_runner.py` (deleted after inlining), and any unused `state_path` / `server_root` references in `ScopeDecoder` that become dead after the reader injection.

**Constraints for later phases:**
- Inject using the shared `FileStateRepository` instance from `server.py` composition root — same instance as `QAManager`, `GitCommitTool`, `BranchParentReader`
- `EnforcementRunner` constructor signature changes — update all call sites in `server.py`
- `ScopeDecoder` constructor signature changes — update all call sites in `server.py` and tests
- Wrap all `state_reader.load(branch)` calls in try/except matching the semantics of the replaced file-not-found checks
- The two cycle_tools fallback sites retain raw reads — document with `# NOTE: IStateReader requires known branch; raw fallback retained intentionally`

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-06 | Agent | Initial draft |
| 1.1 | 2026-06-06 | Agent | Approved Strategy added: Option A for cycle_tools, dead-code cleanup added to scope |