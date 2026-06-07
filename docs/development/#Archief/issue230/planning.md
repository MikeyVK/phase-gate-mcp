<!-- docs\development\issue230\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-04T12:40Z updated=2026-06-04 -->
# Issue #230 — Planning: Preserve implementation cycle across detour re-entry

**Status:** DRAFT  
**Version:** 1.1  
**Last Updated:** 2026-06-04

---

## Purpose

Define the implementation-sized TDD cycle breakdown, dependencies, stop-go boundaries, and deliverable IDs for issue #230 so implementation can proceed from the research-approved strategy without reopening design, introducing compatibility bridges, or deferring defect-dependent test updates into a separate cleanup cycle.

## Scope

**In Scope:**
Preserve `current_cycle` across implementation detour exit and re-entry in `PhaseStateEngine`; replace direct `state.json` reads in `build_phase_guard` with injected `IStateReader.load(branch)`; replace hardcoded implementation-phase checks with config-driven cycle-based detection; guard `current_cycle` exposure in `GetWorkContextTool` on phase contracts and remove the dead `state_path` parameter; update affected unit tests in the same cycles as the production changes they validate.

**Out of Scope:**
Per-phase cycle state refactor in `state.json`; direct `state.json` access in `enforcement_runner.py` and `cycle_tools.py`; compatibility or legacy bridge behavior; standalone regression-guard-only tests; redesign of workflow or cycle semantics beyond the approved fix direction.

## Prerequisites

Read these first:
1. `docs/development/issue230/research.md`
2. `docs/coding_standards/DOCUMENTATION_STANDARD.md`
3. `docs/coding_standards/ARCHITECTURE_PRINCIPLES.md`
4. `docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md`
---

## Summary

Three clean-break TDD cycles implement the approved fix direction from research: preserve `current_cycle` across implementation-phase detours, replace direct `state.json` access and hardcoded implementation checks in the phase guard with injected and config-driven behavior, and hide preserved cycle state from non-cycle-based `get_work_context` output. Test corrections are part of the same cycles as the production changes that invalidate them. No compatibility layer, no legacy alias path, and no standalone regression-guard cycle are planned.

## Approved Strategy Constraints

| Constraint | Planning consequence |
|---|---|
| Clean break at all three affected boundaries | No compatibility shim, no legacy parameter fallback, no temporary dual behavior |
| `transition_cycle` remains the only advancement mechanism | C1 preserves current cycle on detour; it does not auto-advance to `last_cycle + 1` |
| No direct `state.json` reads in the guard path | C2 must inject `IStateReader` rather than reintroduce raw file access |
| No hardcoded implementation-phase if-chain | C2 must use contract-driven cycle-based detection |
| Preserved cycle state must not mislead non-cycle-based phases | C3 must gate `current_cycle` display on `cycle_based` phase metadata |
| Defect-dependent tests are corrected behavior, not legacy contract | Test updates stay inside the production slice that changes the behavior |

## Planning Basis

| Source | Planning use |
|---|---|
| `docs/development/issue230/research.md` | Authoritative root cause, approved strategy, deferred boundaries, blast radius |
| `.phase-gate/state.json` | Confirms branch is in `planning` after a forced `research -> planning` transition |
| `docs/coding_standards/ARCHITECTURE_PRINCIPLES.md` | Binds DIP/OCP/Explicit-over-Implicit decisions for C2 and C3 |
| `docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md` | Binds typing obligations for injected interfaces and contract lookups |

No separate issue-230 design artifact exists on this branch. Planning proceeds from the research-approved strategy because the research artifact already fixes the chosen direction, affected boundaries, and deferred work clearly enough for implementation-sized cycle decomposition.

---

## Dependencies

- C2 depends on C1 because the refactored phase guard must observe preserved cycle state rather than the pre-fix reset behavior.
- C3 depends on C1 because work-context display must guard a preserved `current_cycle` instead of a cleared field.
- C3 depends on C2 for end-to-end runtime alignment between preserved cycle state and the injected/config-driven guard and discovery surfaces.

Dependency graph:

```text
C1 -> C2 -> C3
 \---------^ 
```

---

## TDD Cycles

### Cycle 1: C1 — Preserve cycle state on implementation-phase exit and re-entry

**Goal:**
Keep `current_cycle` intact across implementation detours while preserving `last_cycle` for audit purposes, and correct the defect-dependent state-engine tests in the same slice.

**Files expected to change:**

| Role | Files |
|---|---|
| Production | `mcp_server/managers/phase_state_engine.py` |
| Tests | `tests/mcp_server/unit/managers/test_phase_state_engine.py` |

**Deliverables:**

| ID | Deliverable |
|---|---|
| `C1.engine.preserve-current-cycle` | `on_exit_cycle_based_phase()` no longer clears `current_cycle` on implementation-phase exit |
| `C1.engine.audit-last-cycle` | `last_cycle` remains updated for audit/history without changing cycle advancement semantics |
| `C1.tests.detour-reentry-behavior` | State-engine tests assert preserved cycle behavior instead of reset-to-`None` behavior |
| `C1.validation.state-engine-slice` | Focused state-engine validation proves detour exit/re-entry preserves cycle state |

**Corrected behavior:**
- Exiting implementation for a planning or design detour preserves the active cycle number.
- Re-entering implementation after a detour does not reset to cycle 1.
- Cycle advancement still requires explicit `transition_cycle`; detour re-entry is not treated as cycle completion.

**Test-suite impact:**
- Existing state-engine tests that asserted `current_cycle is None` after exit are defect-dependent and must be rewritten in this cycle.
- No new regression-guard-only test surface is introduced beyond the behavior slice already covered by the state-engine unit suite.

**Typing obligations:**
- No new public types required.
- Existing state object semantics must remain type-consistent; no `Any`, no casts, no ignores expected.

**Quality-gate obligations:**
- Run the focused state-engine unit slice first.
- Apply quality gates to the touched production and test files before leaving implementation work on this slice.

**Exit Criteria:**
- `C1.engine.preserve-current-cycle`: leaving implementation no longer writes `current_cycle=None`.
- `C1.engine.audit-last-cycle`: audit semantics remain explicit and do not auto-advance cycles.
- `C1.tests.detour-reentry-behavior`: defect-dependent assertions are updated in the same cycle and pass.
- `C1.validation.state-engine-slice`: the focused state-engine validation is green.

### Cycle 2: C2 — Refactor phase guard to injected state reader and config-driven cycle-based detection

**Goal:**
Replace direct `state.json` access and hardcoded implementation checks in `build_phase_guard` with injected `IStateReader` and `PhaseContractResolver` usage, including the required same-slice test and call-site updates.

**Dependencies:** C1

**Files expected to change:**

| Role | Files |
|---|---|
| Production | `mcp_server/tools/git_tools.py`, `mcp_server/server.py` |
| Tests | `tests/mcp_server/unit/test_c260_c2_state_root_injection.py` |

**Deliverables:**

| ID | Deliverable |
|---|---|
| `C2.guard.inject-state-reader` | `build_phase_guard` reads branch state through injected `IStateReader.load(branch)` |
| `C2.guard.contract-driven-cycle-detection` | Cycle-based enforcement uses `PhaseContractResolver` instead of hardcoded implementation-phase literals |
| `C2.server.phase-guard-wiring` | `server.py` passes the existing state repository and contract resolver into the guard builder |
| `C2.tests.guard-signature-and-behavior` | Guard-related tests are updated to the injected signature and corrected behavior in the same slice |
| `C2.validation.guard-slice` | Focused guard validation proves the new signature and behavior remain correct |

**Corrected behavior:**
- The guard path no longer performs raw file reads outside the state-repository abstraction.
- Cycle-based enforcement is decided by workflow contracts, not by the literal phase name `implementation`.
- Guard behavior remains aligned with the preserved cycle state introduced in C1.

**Test-suite impact:**
- Existing guard tests with the old `build_phase_guard(server_root)` shape must be updated in this cycle.
- No compatibility overload or legacy signature is allowed.

**Typing obligations:**
- Injected interface usage must stay within existing protocol types.
- Resolver and reader usage should type-check without ignores or ad hoc casts.

**Quality-gate obligations:**
- Run the focused phase-guard test slice first.
- Apply quality gates to changed production and test files before leaving the slice.

**Exit Criteria:**
- `C2.guard.inject-state-reader`: direct `json.loads(state_file.read_text())` style access is gone from `build_phase_guard`.
- `C2.guard.contract-driven-cycle-detection`: the guard no longer checks for `workflow_phase == "implementation"` directly.
- `C2.server.phase-guard-wiring`: the live server call-site uses injected existing dependencies only.
- `C2.tests.guard-signature-and-behavior`: same-slice tests pass against the new signature and behavior.
- `C2.validation.guard-slice`: focused guard validation is green.

### Cycle 3: C3 — Guard work-context cycle display and remove dead `state_path` parameter

**Goal:**
Show `current_cycle` only for cycle-based phases and remove the dead `GetWorkContextTool.state_path` parameter without adding fallback aliases or compatibility paths.

**Dependencies:** C1, C2

**Files expected to change:**

| Role | Files |
|---|---|
| Production | `mcp_server/tools/discovery_tools.py`, `mcp_server/server.py` |
| Tests | `tests/mcp_server/unit/tools/test_discovery_tools.py` |

**Deliverables:**

| ID | Deliverable |
|---|---|
| `C3.discovery.cycle-based-output-guard` | `get_work_context` exposes `current_cycle` only when the active phase contract is `cycle_based` |
| `C3.discovery.remove-dead-state-path` | `GetWorkContextTool` no longer accepts or stores the dead `state_path` parameter |
| `C3.server.discovery-wiring` | Live server wiring drops the obsolete `state_path` argument |
| `C3.tests.discovery-cycle-visibility` | Discovery-tool tests validate the corrected cycle visibility contract in the same slice |
| `C3.validation.discovery-slice` | Focused discovery validation proves planning/design detours do not leak cycle state |

**Corrected behavior:**
- During planning or design detours, `get_work_context` does not show a preserved `current_cycle`.
- During the cycle-based implementation phase, `current_cycle` remains visible.
- The obsolete constructor parameter disappears cleanly; no alias or fallback path remains.

**Test-suite impact:**
- Discovery-tool tests must prove the visibility boundary, not preserve the old leakage behavior.
- If the existing suite already omits `state_path`, the cycle still owns the explicit visibility assertions for the corrected output contract.

**Typing obligations:**
- Contract lookups for `cycle_based` must remain narrow and explicit.
- Any optional contract access must be handled by narrowing rather than casting.

**Quality-gate obligations:**
- Run the focused discovery-tool slice first.
- Apply quality gates to the changed production and test files before leaving the slice.

**Exit Criteria:**
- `C3.discovery.cycle-based-output-guard`: `current_cycle` is absent in planning/design output and present in cycle-based implementation output.
- `C3.discovery.remove-dead-state-path`: the obsolete parameter is removed with no fallback alias.
- `C3.server.discovery-wiring`: live wiring no longer passes `state_path`.
- `C3.tests.discovery-cycle-visibility`: same-slice discovery tests pass.
- `C3.validation.discovery-slice`: focused discovery validation is green.

---

## Validation Strategy

| Cycle | Narrowest expected validation |
|---|---|
| C1 | `tests/mcp_server/unit/managers/test_phase_state_engine.py` focused to the detour exit/re-entry slice |
| C2 | `tests/mcp_server/unit/test_c260_c2_state_root_injection.py` |
| C3 | `tests/mcp_server/unit/tools/test_discovery_tools.py` focused to work-context behavior |

Branch-level quality gates for implementation should cover all changed production and test files after each slice is green locally.

## Risks & Mitigation

| Risk | Mitigation |
|---|---|
| `build_phase_guard` contract changes touch live composition-root wiring and could accidentally reintroduce direct file access or hardcoded phase knowledge | Keep C2 narrow: inject only the existing abstractions, change the single live call-site, and treat any compatibility fallback as out of scope |
| Preserved cycle state could leak into non-cycle-based contexts and mislead agents | Make C3 explicitly own the output guard and validate both planning/design absence and implementation presence |
| Defect-dependent tests may still encode the reset-to-`None` behavior | Treat those test updates as mandatory deliverables of C1 and C2, not as follow-up cleanup |
| Missing design artifact could cause planning drift | Keep planning locked to the research-approved strategy and do not reopen the preserve-vs-bridge-vs-break decision |

## Assumptions

- The research artifact is authoritative for the approved direction on this branch.
- Only the implementation phase is currently cycle-based for the affected workflow surfaces.
- Existing unit suites around state engine, guard wiring, and discovery tools are sufficient to validate the corrected behavior without adding broad new regression suites.

## Open Questions

- Whether `tests/mcp_server/unit/tools/test_discovery_tools.py` already contains enough explicit phase-sensitive `current_cycle` assertions, or whether C3 needs a small same-slice assertion expansion.
- Whether any additional guard-path tests outside `test_c260_c2_state_root_injection.py` depend on the pre-refactor signature and need to be pulled into C2 once implementation begins.

## Out-of-Scope Follow-ups

- Phase-owned cycle state refactor in persisted workflow state.
- Direct `state.json` access still present in other modules identified during research.
- Any broader workflow-phase or enforcement redesign.

## Related Documentation
- **[docs/development/issue230/research.md][related-1]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-2]**
- **[docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md][related-3]**
- **[docs/coding_standards/DOCUMENTATION_STANDARD.md][related-4]**

<!-- Link definitions -->

[related-1]: docs/development/issue230/research.md
[related-2]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-3]: docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md
[related-4]: docs/coding_standards/DOCUMENTATION_STANDARD.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.1 | 2026-06-04 | Agent | Reworked to 3 clean-break cycles; same-slice test updates; explicit deliverable IDs and exit criteria |
| 1.0 | 2026-06-04 | Agent | Initial scaffolded draft |
