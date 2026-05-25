<!-- docs/development/issue293/design.md -->
<!-- template=design version=5827e841 created=2026-05-25T08:47Z updated=2026-05-25 -->
# Issue #293 — Cycle Boundary Semantics: Boundary-Explicit Gate Runner API

**Status:** DEFINITIVE  
**Version:** 1.0  
**Last Updated:** 2026-05-25

---

## 1. Context & Requirements

### 1.1. Problem Statement

`PhaseContractResolver.resolve()` conflates phase-exit and cycle-exit gate evaluation through one implicit API. `transition_cycle()` and `force_cycle_transition()` inherit phase-level `exit_requires` gates because the resolver always includes them when `cycle_number is not None`. The fix must make boundary intent explicit at every call site without leaving deprecated stubs in production or test code.

### 1.2. Requirements

**Functional:**

- `resolve_cycle_exit(workflow, phase, cycle_number)` returns only `cycle_exit_requires[N]` merged with cycle-scoped issue deliverables.
- `resolve_phase_exit(workflow, phase, cycle_number=None)` returns `exit_requires` plus `cycle_exit_requires[current_cycle]` when `cycle_number` is provided, merged with issue deliverables using the current routing logic.
- `enforce_cycle_exit()` and `inspect_cycle_exit()` on `IWorkflowGateRunner` and `WorkflowGateRunner` use `resolve_cycle_exit()`.
- `enforce_phase_exit()` and `inspect_phase_exit()` use `resolve_phase_exit()`.
- `transition_cycle()` and `force_cycle_transition()` call `enforce_cycle_exit()` and `inspect_cycle_exit()` respectively.
- `transition()` and `force_transition()` call `enforce_phase_exit()` and `inspect_phase_exit()` respectively.
- `resolve()`, `enforce()`, and `inspect()` are removed; no deprecated stubs retained.
- All test fakes implementing `IWorkflowGateRunner` implement the four new methods.

**Non-Functional:**

- No if-chains on boundary type in engine or runner (OCP §1.2).
- Boundary intent explicit at every call site (Explicit over Implicit §8).
- `IWorkflowGateRunner` remains the extension point; engine does not call resolver directly (Law of Demeter §7, DIP §1.5).

---

## 2. Design Options

### Option A — Single method with explicit `boundary` parameter

Add `boundary: Literal["phase_exit", "cycle_exit"]` to `resolve()`, `enforce()`, and `inspect()`. Callers pass the boundary string.

**Pros:** Minimal surface change; one entry point per operation.  
**Cons:** Boundary as a string/enum is still implicit at the point it enters a call chain; adding a third boundary type requires modifying the method (OCP violation); testing a specific boundary requires inspecting a parameter value rather than a dedicated method call.

### Option B — Separate methods per boundary (chosen)

Add `resolve_phase_exit()` / `resolve_cycle_exit()` to `PhaseContractResolver`; add `enforce_phase_exit()` / `inspect_phase_exit()` / `enforce_cycle_exit()` / `inspect_cycle_exit()` to `IWorkflowGateRunner` and `WorkflowGateRunner`. Remove all generic `resolve()`, `enforce()`, `inspect()` methods.

**Pros:** Intent explicit at every call site; ISP satisfied (each caller receives exactly the method it needs); OCP satisfied (a new boundary type adds a method, does not modify existing ones); each method has a single stated responsibility; test assertions are unambiguous; no dead stubs.  
**Cons:** Method count on the interface increases from 3 to 5; all existing fakes must be updated.

---

## 3. Chosen Direction and Rationale

**Chosen: Option B — separate methods per boundary.**

The increased method count is the only cost, and it is offset by the complete elimination of implicit boundary inference. Option A preserves one API entry point but keeps boundary intent implicit in a parameter value; it also violates OCP because a third boundary type would require modifying the existing method. The absence of a temporary bridge or alias is intentional: retaining `resolve()`, `enforce()`, or `inspect()` as stubs would introduce ambiguity about which method callers should use and create legacy surface that must be actively pruned later.

Alignment with `ARCHITECTURE_PRINCIPLES.md`:

| Principle | Alignment |
|---|---|
| Explicit over Implicit §8 | Each call site declares its boundary intent via method name |
| OCP §1.2 | New boundary type adds a method; existing methods unchanged |
| SRP §1.1 | Each method has one stated responsibility |
| ISP §1.4 | Callers use the narrowest applicable method |
| Law of Demeter §7 | Engine calls runner; runner calls resolver — layering unchanged |
| DIP §1.5 | Engine depends on `IWorkflowGateRunner`; no resolver imports in engine |

---

## 4. Interface Design

### 4.1. PhaseContractResolver

Replace `resolve(workflow, phase, cycle_number)` with:

```
resolve_phase_exit(workflow_name, phase, cycle_number=None) → list[CheckSpec]
    Gate set: exit_requires + cycle_exit_requires[cycle_number] if cycle_number present
    Issue deliverables: current _resolve_issue_checks routing (unchanged — see note below)

resolve_cycle_exit(workflow_name, phase, cycle_number) → list[CheckSpec]
    Gate set: cycle_exit_requires[cycle_number] only
    Issue deliverables: cycle-scoped (tdd_cycles.cycles[N].deliverables)
```

The private `_resolve_issue_checks()` is retained unchanged; both new methods call it. `resolve_cycle_exit()` always passes a non-None `cycle_number` for a cycle-based phase, so the existing cycle-branch of `_resolve_issue_checks` applies correctly.

**Note — deliverable routing for `resolve_phase_exit` (deferred):** The research document's corrected behavior section states that phase-exit should use *phase-scoped* deliverables (`deliverables.json[phase]`). This fix intentionally defers that routing change: the current system stores all issue deliverables for cycle-based phases under `tdd_cycles.cycles[N]`, and no `deliverables.json["implementation"]` key is populated in practice. Switching `resolve_phase_exit` to phase-scoped routing would silently produce `[]` issue checks on every phase exit from a cycle-based phase, breaking the existing merge behavior without the structural deliverable changes that would make phase-scoped routing meaningful. Correcting the deliverable routing is a follow-up concern tracked as an open question for planning. The gate-set fix (`resolve_cycle_exit` returning only cycle gates) is the primary defect addressed here.

`_resolve_checks()` (previously a bridge between runner and resolver) is removed along with `resolve()`.

### 4.2. IWorkflowGateRunner

Replace `enforce(workflow, phase, cycle_number, checks)` and `inspect(workflow, phase, cycle_number, checks)` with:

```
enforce_phase_exit(workflow_name, phase, cycle_number=None) → GateReport
inspect_phase_exit(workflow_name, phase, cycle_number=None) → GateReport
enforce_cycle_exit(workflow_name, phase, cycle_number)      → GateReport
inspect_cycle_exit(workflow_name, phase, cycle_number)      → GateReport
```

The `checks: list[CheckSpec] | None` override parameter is removed from all new methods. No production caller uses it; removing it eliminates a dead path (YAGNI §9).

`is_cycle_based_phase(workflow_name, phase)` is retained unchanged.

### 4.3. WorkflowGateRunner

Internal refactor: `_run_checks(workflow, phase, cycle_number, checks, raise_on_block)` is replaced by `_run_resolved_checks(resolved_checks, raise_on_block)`. The four public methods resolve their gate set via the resolver and then delegate to `_run_resolved_checks`.

```
enforce_phase_exit → resolve_phase_exit → _run_resolved_checks(raise_on_block=True)
inspect_phase_exit → resolve_phase_exit → _run_resolved_checks(raise_on_block=False)
enforce_cycle_exit → resolve_cycle_exit → _run_resolved_checks(raise_on_block=True)
inspect_cycle_exit → resolve_cycle_exit → _run_resolved_checks(raise_on_block=False)
```

`_resolve_checks()` is removed.

### 4.4. PhaseStateEngine

Four call sites updated:

| Method | Old call | New call |
|---|---|---|
| `transition()` L200 | `runner.enforce(…, cycle_number=state.current_cycle)` | `runner.enforce_phase_exit(…, cycle_number=state.current_cycle)` |
| `force_transition()` L242 | `runner.inspect(…, cycle_number=state.current_cycle)` | `runner.inspect_phase_exit(…, cycle_number=state.current_cycle)` |
| `transition_cycle()` L329 | `runner.enforce(…, cycle_number=state.current_cycle)` | `runner.enforce_cycle_exit(…, cycle_number=state.current_cycle)` |
| `force_cycle_transition()` L391 | `runner.inspect(…, cycle_number=state.current_cycle)` | `runner.inspect_cycle_exit(…, cycle_number=state.current_cycle)` |

No logic change in `transition()` or `force_transition()`: they still pass `cycle_number=state.current_cycle` to capture the last-active cycle's `cycle_exit_requires`. The rename alone corrects their boundary semantics.

---

## 5. Affected Surface

### 5.1. Production code

| File | Change |
|---|---|
| `mcp_server/managers/phase_contract_resolver.py` | Add `resolve_phase_exit()`, `resolve_cycle_exit()`; remove `resolve()`, `_resolve_checks()` |
| `mcp_server/core/interfaces/__init__.py` | Add 4 new methods; remove `enforce()`, `inspect()` from `IWorkflowGateRunner` |
| `mcp_server/managers/workflow_gate_runner.py` | Add 4 new methods + `_run_resolved_checks()`; remove `enforce()`, `inspect()`, `_resolve_checks()`, `_run_checks()` |
| `mcp_server/managers/phase_state_engine.py` | Update 4 call sites (L200, L242, L329, L391) |

### 5.2. Test surface

| File | Change required |
|---|---|
| `tests/mcp_server/test_support.py` | Rename `enforce()` → `enforce_phase_exit()`, `inspect()` → `inspect_phase_exit()` in shared fake |
| `tests/mcp_server/unit/managers/test_phase_contract_resolver.py` | Replace combined-behavior test (L270) with separate `resolve_phase_exit` + `resolve_cycle_exit` tests |
| `tests/mcp_server/unit/managers/test_phase_contract_resolver_c3.py` | L94: `resolver.resolve(…)` → `resolver.resolve_phase_exit(…)` (functional equivalence for non-cycle-number call) |
| `tests/mcp_server/unit/managers/test_phase_state_engine_c1.py` | Update `FakeGateRunner` (L25); update direct `runner.enforce/inspect` calls at L154, L155, L169, L203 |
| `tests/mcp_server/unit/managers/test_phase_state_engine_c2.py` | Update `BlockingGateRunner` + `InspectingGateRunner` fakes |
| `tests/mcp_server/unit/managers/test_phase_state_engine_c3_issue257.py` | Update `PassingGateRunner` + `ReportingGateRunner` fakes |
| `tests/mcp_server/unit/managers/test_phase_state_engine_c4_issue257.py` | Update `BlockingCycleGateRunner`, `ReportingCycleGateRunner`, `ConfigAwareCycleGateRunner` fakes; update enforce/inspect call assertions |
| `tests/mcp_server/unit/managers/test_consumers_c4.py` | Replace `workflow_gate_runner.enforce = MagicMock(…)` with correct boundary method |

The behavioral coverage of `test_phase_state_engine_c1.py` L203 (the `checks` override path for multi-block accumulation) migrates to an `enforce_cycle_exit` test with a resolver fixture returning multiple blocking `CheckSpec` instances, or alternatively as a direct test of `_run_resolved_checks` with a prepared list. Neither test requires the removed `checks` override parameter.

### 5.3. Update guidance for direct runner tests

`test_phase_state_engine_c1.py` tests for `WorkflowGateRunner` behavior (direct runner tests at L154–203) are redesigned per the new interface, not just renamed. The test at L154 calls `runner.enforce(…, cycle_number=1)` — after the fix this becomes `runner.enforce_cycle_exit(…, cycle_number=1)` since cycle-number-bearing calls from a cycle gate test are cycle-exit semantics.

---

## 6. Regression and Validation Strategy

### 6.1. Preserved contracts

The following behaviors must continue to pass after the fix:

| Behavior | Validated by |
|---|---|
| `transition()` leaving a cycle-based phase enforces `exit_requires` + `cycle_exit_requires[current_cycle]` | `test_phase_state_engine_c2.py` (updated) |
| `transition_cycle()` raising `GateViolation` when cycle gate blocks | `test_phase_state_engine_c4_issue257.py` (updated) |
| `force_cycle_transition()` returning gate inspection report | `test_phase_state_engine_c4_issue257.py` (updated) |
| `resolve_phase_exit` returns combined phase + cycle gates when `cycle_number` present | New test in `test_phase_contract_resolver.py` |

### 6.2. Corrected behaviors (defect-dependent tests must be updated)

| Old behavior | New behavior | Test requiring correction |
|---|---|---|
| `resolve(…, cycle_number=1)` → phase + cycle gates | `resolve_cycle_exit(…, 1)` → cycle gates only | `test_resolve_merges_issue_specific_checks_without_overriding_required_gates` |

### 6.3. Failure modes and containment

- **Incomplete fake update**: A fake implementing only the old `enforce()` / `inspect()` will fail at import time or at the first `runner.enforce_phase_exit()` call site. No silent behavioral degradation.
- **Caller using wrong boundary method**: A test calling `enforce_phase_exit()` where `enforce_cycle_exit()` is intended will produce an incorrect gate set; caught by the updated resolver unit tests which verify each method's output independently.
- **`_resolve_issue_checks` routing**: Both new resolver methods call `_resolve_issue_checks` with the same parameters as before. No routing change; no new regression surface.

---

## 7. Open Questions

No open questions remain. Integration and acceptance tests verified: `tests/integration/` and `tests/acceptance/` contain no calls to `WorkflowGateRunner.enforce()` or `inspect()`. `test_cycle_tools.py` exercises the real `WorkflowGateRunner` via `gate_runner=server.workflow_gate_runner` and requires no fake update — it will exercise the new `enforce_cycle_exit` / `inspect_cycle_exit` methods directly once the production code is updated. The full out-of-scope test surface is limited to the 8 files listed in §5.2.

---

## Related Documentation

- **[docs/development/issue293/research.md][related-1]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-2]**
- **[mcp_server/managers/phase_contract_resolver.py][related-3]**
- **[mcp_server/core/interfaces/__init__.py][related-4]**
- **[mcp_server/managers/workflow_gate_runner.py][related-5]**
- **[mcp_server/managers/phase_state_engine.py][related-6]**
- **[tests/mcp_server/unit/managers/test_phase_contract_resolver.py][related-7]**
- **[tests/mcp_server/unit/managers/test_phase_state_engine_c4_issue257.py][related-8]**

<!-- Link definitions -->
[related-1]: research.md
[related-2]: ../../docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-3]: ../../mcp_server/managers/phase_contract_resolver.py
[related-4]: ../../mcp_server/core/interfaces/__init__.py
[related-5]: ../../mcp_server/managers/workflow_gate_runner.py
[related-6]: ../../mcp_server/managers/phase_state_engine.py
[related-7]: ../../tests/mcp_server/unit/managers/test_phase_contract_resolver.py
[related-8]: ../../tests/mcp_server/unit/managers/test_phase_state_engine_c4_issue257.py

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-25 | Agent | Initial draft — clean-break design, boundary-explicit API, full blast radius |
