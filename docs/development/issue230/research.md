<!-- docs\development\issue230\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-03T14:27Z updated= -->
# TDD Cycle Counter Resets on Re-entry After Mid-Stream Detour

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-03

---

## Scope

**In Scope:**
on_exit_cycle_based_phase / on_enter_cycle_based_phase in PhaseStateEngine; cycle guard in build_phase_guard (git_tools.py) including replacement of direct state.json read with IStateReader.load() and injection of PhaseContractResolver; cycle display in GetWorkContextTool (discovery_tools.py) including removal of dead state_path parameter; build_phase_guard call-site in server.py; GetWorkContextTool call-site in server.py

**Out of Scope:**
Phase-owned cycle state refactor (per-phase cycle_state in state.json); enforcement_runner.py direct state.json access; cycle_tools.py direct state.json access

---

## Problem Statement

When an agent exits the implementation phase mid-stream (e.g. tdd→planning→tdd), on_exit_cycle_based_phase() sets current_cycle=None. On re-entry, on_enter_cycle_based_phase() sees None and initializes to cycle 1, discarding the cycle the agent was on. This forces use of force_cycle_transition as a workaround and breaks deterministic cycle progression.

## Research Goals

- Identify root cause of cycle counter reset on TDD phase re-entry
- Evaluate and select fix strategy for preserving cycle state across non-linear phase transitions
- Assess blast radius of each affected boundary
- Identify and explicitly defer related architectural issues out of scope

---

## Findings

### Root Cause

`on_exit_cycle_based_phase()` (L735–752 in `phase_state_engine.py`) sets `current_cycle=None`
and snapshots it into `last_cycle`. On re-entry, `on_enter_cycle_based_phase()` (L711–731) sees
`current_cycle is None` and hard-initializes to 1 — `last_cycle` is ignored. A detour
(tdd→planning→tdd) is treated as a complete phase exit and fresh entry, which is wrong.
A phase detour is never a cycle completion event.

**Strategy rejected:** Resume at `last_cycle + 1` on `on_enter` — too eager. It conflates a
logistical phase detour with actual cycle completion and removes the agent's authority to decide
when a cycle is done.

---

### Approved Strategy

Three affected boundaries, each with a clean-break fix:

#### Boundary 1 — `PhaseStateEngine.on_exit_cycle_based_phase`

Remove the `current_cycle=None` assignment on exit. `on_exit` only updates `last_cycle` for
audit purposes; `current_cycle` is preserved as-is. `on_enter` already has the correct guard
(`if current_cycle is None`) — first entry initializes to 1, re-entry after detour is a no-op.
`transition_cycle` remains the only valid mechanism for advancing the cycle counter.

**Files:** `mcp_server/managers/phase_state_engine.py`

#### Boundary 2 — `build_phase_guard` in `git_tools.py`

Replace the direct `json.loads(state_file.read_text())` read with `IStateReader.load(branch)`.
Replace `if workflow_phase == "implementation"` with a config-driven check:
`phase_contract_resolver.is_cycle_based_phase(workflow_name, workflow_phase)`.

`build_phase_guard` signature changes: `server_root: Path` is dropped; `state_reader: IStateReader`
and `phase_contract_resolver: PhaseContractResolver` are injected instead.
The call-site in `server.py` passes the existing `self.phase_contract_resolver` and the
`FileStateRepository` (or its `IStateReader` abstraction) already constructed during assembly.

This eliminates both the hardcoded phase-name assumption (OCP/DIP) and the direct unprotected
file read (DIP, race condition risk).

**Files:** `mcp_server/tools/git_tools.py`, `mcp_server/server.py`

#### Boundary 3 — `GetWorkContextTool` in `discovery_tools.py`

Condition `current_cycle` injection into context on `phase_entry.cycle_based`, using the already-
injected `self._contracts_config`. Without this guard, a preserved `current_cycle` from Boundary 1
would appear in `get_work_context` output during detour phases (planning, design, etc.),
misleading the agent about its current cycle.

**Files:** `mcp_server/tools/discovery_tools.py`

---

### Deferred Work (Out of Scope — Separate Issues Required)

> These findings were surfaced during research. They are **not addressed** by this fix and must
> not be conflated with the scope above. Each requires its own issue and branch.

#### DEFERRED-1: Phase-Owned Cycle State (Latent Architecture)

`state.json` stores a single global `current_cycle` / `last_cycle` / `cycle_history` — not
per-phase. Only one `cycle_based: true` phase exists today (implementation) across all workflows,
so this is latent. If a second cycle-based phase is added, state will silently corrupt.

Blast radius: 15+ production files, 200+ references. Requires a dedicated refactor issue with
full design and migration plan.

#### DEFERRED-2: Direct `state.json` Access — DIP Violation

`enforcement_runner.py` L43 and `cycle_tools.py` L134 + L267 read `state.json` directly via
`json.loads(file.read_text())`, bypassing `IStateRepository` and the `WorkflowStateMutator`
mutex. This creates a race condition window against concurrent writes. Confirmed violation of DIP
per `ARCHITECTURE_PRINCIPLES.md`.

Requires a separate bug/chore issue. Pattern fix: inject `IStateReader`, call `.load(branch)`.

#### DEFERRED-3: Dead `state_path` Parameter in `GetWorkContextTool` ~~(promoted to in-scope)~~

`GetWorkContextTool.__init__` accepts `state_path: Path | None`, stores it in `self._state_path`,
and never uses it. `server.py` still passes `server_root / "state.json"` at the call-site.
Refactor omission from issue #268/#352 when direct file access was replaced by
`self._state_engine.get_state(branch)`.

**Resolution:** Promoted to in-scope since `discovery_tools.py` and `server.py` are already
touched in Boundary 3. The parameter is removed in the same cycle.

## Related Documentation

- `mcp_server/managers/phase_state_engine.py` — `on_enter_cycle_based_phase` (L711), `on_exit_cycle_based_phase` (L735)
- `mcp_server/tools/git_tools.py` — `build_phase_guard` (L43)
- `mcp_server/tools/discovery_tools.py` — `GetWorkContextTool._build_context` (L162)
- `docs/coding_standards/ARCHITECTURE_PRINCIPLES.md` — DIP, OCP, ISP
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |