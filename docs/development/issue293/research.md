<!-- docs/development/issue293/research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-25T08:34Z updated=2026-05-25 -->
# Issue #293 — Cycle Boundary Semantics: Phase-Exit Gates Leaking into Cycle Transitions

**Status:** DEFINITIVE  
**Version:** 1.0  
**Last Updated:** 2026-05-25

---

## Purpose

Document the root cause, affected surface, architectural constraints, solution directions, and corrected behavior for issue #293 within epic #290.

## Scope

**In Scope:**
Cycle transition gate resolution semantics; the distinction between phase-exit and cycle-exit boundaries; `PhaseContractResolver`, `WorkflowGateRunner`, `PhaseStateEngine`, and their test suites.

**Out of Scope:**
State persistence concurrency (issue #292), read-side snapshot unification (issue #231), submit_pr and create_branch atomicity.

## Prerequisites

1. Issue #293 description
2. Epic #290 context
3. `docs/coding_standards/ARCHITECTURE_PRINCIPLES.md`
4. `mcp_server/managers/phase_contract_resolver.py`, `workflow_gate_runner.py`, `phase_state_engine.py`

---

## Problem Statement

`PhaseContractResolver.resolve()` conflates two distinct workflow boundaries — phase-exit and cycle-exit — through one implicit API. The presence of `cycle_number` causes `resolve()` to include both `phase_entry.exit_requires` and `cycle_exit_requires[cycle_number]`, so `transition_cycle()` and `force_cycle_transition()` inherit phase-level exit gates when they should only enforce cycle-boundary checks.

## Research Goals

- Identify the exact code path that causes phase-exit gates to block cycle transitions
- Map the boundary distinction to `ARCHITECTURE_PRINCIPLES.md` constraints
- Evaluate two resolver API directions against architectural principles and confirm the preferred approach
- Define corrected behavior as input for design and planning

---

## Background

The platform models cycle-based phases through `contracts.yaml` with fields `cycle_based`, `subphases`, `commit_type_map`, `exit_requires`, and `cycle_exit_requires`. The design intent is:

- `exit_requires`: gates that must pass when **leaving the phase** (e.g., moving from `implementation` to `validation`)
- `cycle_exit_requires[N]`: gates that must pass when **leaving cycle N** (e.g., moving from cycle 1 to cycle 2 within `implementation`)

However, the current resolver API receives only `workflow_name`, `phase`, and optional `cycle_number`, and uses the presence of `cycle_number` to implicitly combine both sets. Boundary intent is not declared; it is inferred from call shape.

---

## Findings

### Finding 1 — Core defect: semantic overloading in resolve()

`PhaseContractResolver.resolve()` ([phase_contract_resolver.py L112–144](../../mcp_server/managers/phase_contract_resolver.py)) handles two distinct responsibilities through one API:

| Caller intent | Boundary | Expected checks |
|---|---|---|
| `transition_cycle()` / `force_cycle_transition()` | Cycle-exit | `cycle_exit_requires[N]` only |
| `transition()` / `force_transition()` | Phase-exit | `exit_requires` + `cycle_exit_requires[current_cycle]` |

The current implementation conflates these: any call with `cycle_number is not None` always returns `exit_requires + cycle_exit_requires[N]`, regardless of which boundary is being crossed.

### Finding 2 — Live code path proves cycle hops inherit phase-exit gates

The complete path for a cycle hop:

```
transition_cycle()
  → runner.enforce(workflow_name, phase=current_phase, cycle_number=current_cycle)
  → WorkflowGateRunner._run_checks()
  → PhaseContractResolver.resolve(workflow_name, phase, cycle_number)
  → config_checks = [*phase_entry.exit_requires]          # phase gates always included
  → config_checks.extend(cycle_exit_requires[cycle_number])  # cycle gates appended
```

Source: [phase_contract_resolver.py L130–136](../../mcp_server/managers/phase_contract_resolver.py), [phase_state_engine.py L329–334](../../mcp_server/managers/phase_state_engine.py).

### Finding 3 — Bug is latent in code path; would activate under non-empty exit_requires config

The `refactor` workflow defines `implementation` as `cycle_based: true`, making it susceptible to the defect. However, the checked-in `contracts.yaml` currently has `exit_requires: []` for all cycle-based implementation phases and no `cycle_exit_requires` entries. Under the current checked-in config the defect is latent: the incorrect code path exists but is not yet triggered. It would activate as soon as any cycle-based phase gains non-empty `exit_requires` or `cycle_exit_requires` entries in `contracts.yaml`.

### Finding 4 — Phase transitions also receive cycle_number (intended behavior, confirmed)

`transition()` (phase-exit, [phase_state_engine.py L200–203](../../mcp_server/managers/phase_state_engine.py)) also calls `runner.enforce(cycle_number=state.current_cycle)`. For a phase-exit boundary this is **correct**: when leaving a cycle-based phase, both `exit_requires` and `cycle_exit_requires[current_cycle]` must pass. The last cycle must be completed before the phase can be exited. This behavior is approved and must be preserved.

### Finding 5 — Existing tests encode the conflated behavior as correct

`test_phase_contract_resolver.py` ([L270–293](../../tests/mcp_server/unit/managers/test_phase_contract_resolver.py)) asserts that `resolve("feature", "implementation", cycle_number=1)` returns both the phase-level `required-design-doc` gate and the cycle-level `c1-red-test` gate in one combined result. This test currently validates the buggy behavior; it must be updated when the resolver is split.

### Finding 6 — IWorkflowGateRunner interface is the extension boundary

`PhaseStateEngine` depends on `IWorkflowGateRunner` ([core/interfaces/__init__.py L88](../../mcp_server/core/interfaces/__init__.py)), not on `PhaseContractResolver` directly. Any boundary-specific resolution must surface through the runner interface, not through direct resolver calls from the engine (Law of Demeter §7, DIP §1.5).

---

## Architecture Check

| Principle | Current state | Implication |
|---|---|---|
| **Explicit over Implicit (§8)** | Boundary type is implicit in `cycle_number is not None` | Strongest violation: intent hidden behind call shape |
| **SRP (§1.1)** | `resolve()` answers two distinct questions: "what exits this phase?" and "what exits this cycle?" | Method has two responsibilities; should split |
| **OCP (§1.2)** | A new boundary type (e.g., cycle-entry check) would require modifying `resolve()` | Separate methods are extensible without modification |
| **ISP (§1.4)** | Callers are forced to use one overloaded API regardless of their actual boundary need | Separate methods give callers the narrowest interface for their use case |
| **Law of Demeter (§7)** | Engine calls runner, runner calls resolver — correct layering | Fix must not introduce direct resolver calls from the engine |

---

## Solution Directions

### Direction A — Single method with explicit `boundary` parameter

Add `boundary: Literal["phase_exit", "cycle_exit"]` to `resolve()`, `enforce()`, and `inspect()`. Callers declare which boundary they are evaluating.

**Pros:** Minimal surface change; one entry point.  
**Cons:** A string/enum parameter that changes behavior remains implicit in tests; method signature grows; OCP violation if a third boundary type is added later.

### Direction B — Separate methods per boundary (recommended)

Add `resolve_phase_exit()` and `resolve_cycle_exit()` to `PhaseContractResolver`, and corresponding `enforce_phase_exit()` / `inspect_phase_exit()` / `enforce_cycle_exit()` / `inspect_cycle_exit()` to `IWorkflowGateRunner` and `WorkflowGateRunner`.

**Pros:** Intent is explicit at every call site; ISP satisfied; OCP satisfied; each method has one responsibility; test cases are unambiguous; adding a new boundary type only adds methods.  
**Cons:** Doubles the public method count on the runner interface; old `enforce()` / `inspect()` need a deprecation or removal plan.

### Recommendation

Direction B is architecturally superior and aligns with the user's stated preference (Option Y). The method count increase is acceptable because each method has a single, clear semantic. The Approved Strategy (below) selects this direction as a clean break: old `enforce()` / `inspect()` are removed in the same implementation cycle as `resolve()`, not retained as temporary aliases.

**Issue-specific deliverable routing also splits cleanly:**

| Resolution path | Issue deliverable source |
|---|---|
| `resolve_cycle_exit(workflow, phase, cycle_number)` | `deliverables.json → tdd_cycles.cycles[N].deliverables` |
| `resolve_phase_exit(workflow, phase, cycle_number=None)` | `deliverables.json → phase_name.deliverables` |

---

## Affected Surface

| Component | File | Change required |
|---|---|---|
| `PhaseContractResolver` | `mcp_server/managers/phase_contract_resolver.py` | Add `resolve_cycle_exit()` and `resolve_phase_exit()` |
| `IWorkflowGateRunner` | `mcp_server/core/interfaces/__init__.py` | Add `enforce_cycle_exit()`, `inspect_cycle_exit()`, `enforce_phase_exit()`, `inspect_phase_exit()` |
| `WorkflowGateRunner` | `mcp_server/managers/workflow_gate_runner.py` | Implement the 4 new runner methods |
| `PhaseStateEngine.transition_cycle()` | `mcp_server/managers/phase_state_engine.py` L329 | Use `enforce_cycle_exit()` |
| `PhaseStateEngine.force_cycle_transition()` | `mcp_server/managers/phase_state_engine.py` L391 | Use `inspect_cycle_exit()` |
| `PhaseStateEngine.transition()` | `mcp_server/managers/phase_state_engine.py` L200 | Use `enforce_phase_exit()` |
| `PhaseStateEngine.force_transition()` | `mcp_server/managers/phase_state_engine.py` L242 | Use `inspect_phase_exit()` |
| `test_phase_contract_resolver.py` | `tests/mcp_server/unit/managers/` | Update combined-behavior test; add separate cycle-exit and phase-exit tests |
| `test_phase_state_engine_c4_issue257.py` | `tests/mcp_server/unit/managers/` | Update gate runner fakes, enforce/inspect call assertions |
| `test_phase_state_engine_c1.py` | `tests/mcp_server/unit/managers/` | Update direct runner calls at L154, L169, L203 |
| `test_phase_state_engine_c2.py` | `tests/mcp_server/unit/managers/` | Update force_transition gate inspection tests |

---

## Corrected Behavior

- `transition_cycle()` and `force_cycle_transition()` evaluate only `cycle_exit_requires[N]` merged with cycle-scoped issue deliverables.
- `transition()` and `force_transition()` leaving a cycle-based phase evaluate `exit_requires` plus `cycle_exit_requires[current_cycle]` (last active cycle must also be closed out), merged with phase-scoped issue deliverables.
- Non-cycle callers (transition to/from non-cycle-based phases) continue to use `resolve_phase_exit()` with `cycle_number=None`, returning only `exit_requires`.
- Boundary intent is declared at every call site; no behavioral inference from `cycle_number is not None`.

---
## Open Questions

*Resolved — no open questions remain.*

- **enforce()/inspect() fate:** Resolved in Approved Strategy below: clean break, removed in C2 alongside resolve(). No deprecation stubs.
- **Integration test exposure:** Resolved in design §7: `test_cycle_tools.py` uses the real runner and is updated automatically by C2 production changes; no integration fixtures rely on the combined resolve(cycle_number=N) behavior.


---

## Approved Strategy

**Boundary:** `PhaseContractResolver.resolve()` and `IWorkflowGateRunner.enforce()` / `inspect()` API surface.

**Selected strategy:** Clean break — introduce separate methods per boundary type (Direction B / Option Y). No temporary bridge.

**Supported contract vs defect dependence:**
- Tests that assert combined phase+cycle resolution for `resolve(cycle_number=N)` are defect-dependent. They must be corrected, not preserved.
- Tests that assert `transition()` (phase-exit) enforces both `exit_requires` and `cycle_exit_requires[current_cycle]` represent supported behavior and must continue to pass.

**Constraints for later phases:**
- `IWorkflowGateRunner` is the extension point, not `PhaseContractResolver` (Law of Demeter §7 + DIP §1.5). New methods must appear on the interface before the engine can call them.
- Old `enforce()` / `inspect()` removal scope must be decided in design before implementation begins.
- No if-chains on boundary type inside any engine or runner method (OCP §1.2).

---

## Related Documentation

- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-1]**
- **[mcp_server/managers/phase_contract_resolver.py][related-2]**
- **[mcp_server/managers/workflow_gate_runner.py][related-3]**
- **[mcp_server/managers/phase_state_engine.py][related-4]**
- **[mcp_server/core/interfaces/__init__.py][related-5]**
- **[tests/mcp_server/unit/managers/test_phase_contract_resolver.py][related-6]**
- **[tests/mcp_server/unit/managers/test_phase_state_engine_c4_issue257.py][related-7]**
- **[docs/development/issue290/research-issue293-cycle-boundary-semantics.md][related-8]**

<!-- Link definitions -->
[related-1]: ../../docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-2]: ../../mcp_server/managers/phase_contract_resolver.py
[related-3]: ../../mcp_server/managers/workflow_gate_runner.py
[related-4]: ../../mcp_server/managers/phase_state_engine.py
[related-5]: ../../mcp_server/core/interfaces/__init__.py
[related-6]: ../../tests/mcp_server/unit/managers/test_phase_contract_resolver.py
[related-7]: ../../tests/mcp_server/unit/managers/test_phase_state_engine_c4_issue257.py
[related-8]: ../issue290/research-issue293-cycle-boundary-semantics.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-25 | Agent | Initial draft — root-cause analysis, architecture check, solution directions, approved strategy |
