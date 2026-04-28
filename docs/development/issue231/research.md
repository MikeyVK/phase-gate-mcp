<!-- c:\temp\st3\docs\development\issue231\research.md -->
<!-- template=research version=8b7bb3ab created=2026-04-26T14:54Z updated=2026-04-26 -->
# Issue #231 & #292: Workflow State Hardening Research

**Status:** DRAFT  
**Version:** 2.1  
**Last Updated:** 2026-04-26

---

## Purpose

Capture the smallest serious production-hardening scope for issue #231 and issue #292 without defaulting to a full workflow-state redesign and without understating the write-integrity problem described by issue #292 itself.

## Scope

**In Scope:**
Issue #231 read-side workflow-status ambiguity exposed by issue #229 execution; issue #292 write-integrity risk from shared ownership of `.st3/state.json`, full-document replacement semantics, and direct QA baseline writes; operator-facing conflict signaling through explicit tool feedback plus a recovery hint or note; branch-local artifact hygiene for QA state; reuse of existing persistence components such as `AtomicJsonWriter` and repository patterns where they still fit the ownership model.

**Out of Scope:**
Full CQRS redesign of the workflow-state subsystem; migration of every workflow reader at once; distributed locking or cross-process coordination beyond the current server process; unrelated epic #290 items such as submit_pr atomicity or create_branch hardening; backward-compatibility shims for legacy mixed `quality_gates` data inside `.st3/state.json`.

## Prerequisites

Read these first:
1. docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
2. docs/development/archive/issue229/research.md
3. docs/development/archive/issue229/findings.md
4. GitHub issue #292 description
5. mcp_server/managers/qa_manager.py
6. mcp_server/managers/phase_state_engine.py
7. mcp_server/managers/project_manager.py
8. mcp_server/tools/discovery_tools.py
9. mcp_server/managers/state_repository.py
10. docs/development/issue290/research-issue292-state-mutation-concurrency.md
11. docs/development/issue290/research-issue231-state-snapshot.md
---

## Problem Statement

The concrete problem behind issue #231 is still not an abstract need for a nicer state API. During the live execution of issue #229, the workflow system started relying on richer branch state: phase, cycle, subphase, planning context, and commit-scope metadata. From that moment on, the answer to the question "where is this branch right now?" could come from more than one source. Persisted workflow state, commit-scope detection, and planning-derived context all contributed partial answers, and tools assembled those answers locally. That creates read-side ambiguity: different tools can surface different versions of the current branch status.

Issue #292 is the write-side companion risk, and the source issue requires a broader framing than QA-state isolation alone. The current platform can report successful workflow mutations while still losing valid state updates because multiple mutation paths load and rewrite the same `.st3/state.json` payload. One of those writers, `QAManager`, also stores incompatible top-level QA data in that same file. A narrow repository split for QA state is still necessary, but it is not sufficient by itself. The design for #292 must also define one explicit write-integrity contract so successful workflow mutations cannot silently overwrite unrelated valid changes, and conflict conditions must return explicit operator feedback plus a recovery hint or note.

## Research Goals

- Reconstruct the concrete historical path from issue #229 execution to issue #231 instead of treating #231 as a generic architecture issue.
- Record the exact, practical symptom that made #231 necessary.
- Reframe #292 from the source GitHub issue and companion research instead of reducing it to the QA baseline schema conflict alone.
- Determine the smallest serious implementation slice for #292 that addresses both ownership split and write integrity.
- Record the non-negotiable constraints for the #292 fix: reuse existing persistence components where appropriate, avoid DRY violations, surface conflicts through explicit tool feedback plus recovery hinting, and exclude the new QA state file from PR/merge artifacts.
- Determine the blast radius of the broadened #292 slice and the still-narrow #231 read-side slice before design is revised.

---

## Background

Issue #229 was not just a deliverables-enforcement branch. It was also a live trial run of the TDD cycle and workflow-state machinery introduced earlier in issue #146. The #229 branch explicitly exercised `state.json` fields such as `current_tdd_cycle` and `tdd_cycle_history`, phase transitions, and commit scopes tied to cycle/subphase work. That made workflow state richer and more useful, but it also exposed that no single read contract existed for "effective branch status".

During and after that period, follow-up improvements solved local symptoms: `get_project_plan()` started injecting `current_phase` via `ScopeDecoder`, and `get_work_context()` grew phase detection plus conditional cycle information. Those fixes improved individual tools, but they also spread workflow-status assembly across separate consumers and precedence rules.

On the write side, issue #292 was observed while forced cycle and phase transitions both reported success yet one later full-document save restored stale values. The companion research confirms that the deeper defect is shared ownership of `.st3/state.json` plus blind full-document replacement semantics. `QAManager` makes the problem worse through its direct raw JSON write path, but the broader write-integrity problem remains even after the QA schema conflict is removed.

---

## Findings

### Finding 1 — Issue #229 is still the concrete historical trace for issue #231

The clearest historical root of issue #231 is the live execution of issue #229, not a later abstract redesign discussion. In the #229 research document, the branch is described as a live exercise of issue #146 machinery, including `state.json` fields such as `current_tdd_cycle`, `tdd_cycle_history`, phase transitions, and cycle-aware commit scopes. That is the moment the platform stopped dealing with only a single coarse phase value and started depending on a richer notion of branch status.

### Finding 2 — The concrete #231 symptom was "the branch status can disagree with itself"

The most concrete documented symptom appears in issue #229 GAP-07: the agent committed with `workflow_phase="tdd"` and `cycle_number=2` while `state.json.current_phase="design"`, and the tool accepted the commit anyway. That is not just a validation gap. It is evidence that the system could hold and accept conflicting answers about the same branch state. In practical terms: one source said "design", another operation acted as if the branch was already in TDD cycle 2.

### Finding 3 — Later fixes improved individual tools, but also spread read-side assembly logic

After the #229-era problems surfaced, the codebase added partial read-side fixes instead of one shared contract:

- `ProjectManager.get_project_plan()` began adding `current_phase`, `phase_source`, and `phase_detection_error` via `ScopeDecoder`
- `GetWorkContextTool` began combining phase detection with separate state reads for cycle information and separate planning reads for cycle details

These changes improved operator experience, but they also mean the platform has no single authoritative read path for "effective workflow status". Different tools still assemble that answer differently.

### Finding 4 — Issue #292 itself reopens the previously narrowed #292 scope

The source GitHub issue for #292 is broader than the previously accepted minimal slice in this document. It explicitly states that concurrent transitions can both report success while one later full-document write restores stale fields, and it requires research to audit every `state.json` writer, including the direct `QAManager` write path. That means the narrow framing of #292 as only a QA-state isolation step is no longer an honest representation of the issue being designed.

### Finding 5 — The root problem behind #292 is shared ownership plus full-document replacement

The companion research is correct: issue #292 should not be framed only as "two transitions can race". The deeper defect is that `.st3/state.json` lacks a single ownership and mutation contract. Today at least two domains treat the same file as theirs:

- workflow state transitions via `PhaseStateEngine` and `FileStateRepository`
- quality baseline persistence via `QAManager`

That shared ownership already creates a schema conflict. On top of that, workflow transition paths still follow a load-modify-save pattern that rewrites the full serialized branch payload. Combined, those conditions allow lost updates, schema conflicts, and silent last-writer-wins behavior.

### Finding 6 — The writer audit boundary is now explicit

For the broadened #292 slice, the audited write paths are:

- workflow branch-state writes performed through `PhaseStateEngine` methods such as `initialize_branch()`, `transition()`, `force_transition()`, `transition_cycle()`, `force_cycle_transition()`, and reconstruction-triggered saves, all of which converge on the same repository-backed `_save_state()` path
- the direct QA baseline write path in `QAManager._save_state_json()`

Callers such as project and transition tools are not separate writers. They invoke the engine or manager paths above. Initialization flows are therefore not a second ownership contract, but they are still part of the same workflow mutation mechanism and must inherit the same coordinated write semantics once #292 is implemented.

### Finding 7 — The QA bypass is one concrete writer, but it is not the whole #292 defect

`QAManager` still matters because it bypasses the typed workflow-state contract completely and writes top-level `quality_gates` data that `BranchState(extra="forbid")` rejects. That bypass must be removed. But the write-integrity problem does not disappear once QA data moves out of `.st3/state.json`. The workflow transition engine can still lose updates if multiple valid workflow mutations are applied from stale reads and then persisted as whole-document replacements.

### Finding 8 — The smallest serious #292 slice is now broader than QA-state isolation

The smallest serious design for #292 now has to include both halves of the problem:

- restore single ownership boundaries by moving QA baseline state out of workflow state
- introduce one explicit workflow-state mutation contract so successful workflow writes cannot silently discard unrelated valid changes
- surface stale-write, lock-contention, or conflict conditions through explicit tool feedback and a recovery hint or note instead of treating silent last-writer-wins as success

That is still not a full subsystem redesign. It is a focused hardening slice. But it is materially broader than "add `quality_state.json` and stop there".

### Finding 9 — Issue #231 stays narrow even after #292 broadens

The broadened write-side scope for #292 does not force issue #231 into a broad redesign. The research basis for #231 is still the same: user-facing consumers compute overlapping workflow-status answers through separate local assembly logic. The correct #231 move remains a small read-side unification for the user-facing consumers that actually surface branch status.

### Finding 10 — The single source of truth for branch-local PR neutralization is already known

For the QA-state portion of #292, the operational SSOT is confirmed: branch-local artifacts are defined in `.st3/config/phase_contracts.yaml` under `merge_policy.branch_local_artifacts`, and `SubmitPRTool` consumes that config to neutralize runtime files before PR creation. If `.st3/quality_state.json` is introduced, it must be added there rather than in ad hoc code branches or duplicate config.

---

## Blast Radius

### Issue #231 — Narrow Read-Side Unification

For this research, the #231 slice remains one shared, read-only branch-status contract adopted by the user-facing consumers that currently assemble workflow status independently.

**Direct production impact:**
- `mcp_server/managers/project_manager.py` because `get_project_plan()` currently injects `current_phase`, `phase_source`, and `phase_detection_error` locally.
- `mcp_server/tools/discovery_tools.py` because `GetWorkContextTool` currently composes phase, cycle, and planning context from multiple reads.
- one new small helper or value-object module that exposes the shared read contract.

**Conditional production impact:**
- `mcp_server/server.py` if the new helper is injected at composition time instead of constructed locally.
- `mcp_server/core/phase_detection.py` if precedence rules move down into `ScopeDecoder` rather than being unified above it.
- `mcp_server/managers/state_reconstructor.py` if the first slice expands from read unification into reconstruction semantics.

**Direct test impact:**
- `tests/mcp_server/unit/managers/test_project_manager.py` for explicit `get_project_plan()` phase-detection assertions.
- `tests/mcp_server/unit/tools/test_discovery_tools.py` as the primary hotspot because many `get_work_context` tests assert rendered phase and cycle behavior.
- `tests/mcp_server/unit/tools/test_project_tools.py` because the project-plan tool stubs the manager response shape.

**Secondary or conditional test impact:**
- `tests/mcp_server/integration/test_issue39_cross_machine.py` as regression coverage around `get_project_plan()`, but not the primary blast-radius driver because the flow mainly reads required phases rather than user-facing branch-status fields.
- `tests/mcp_server/core/test_phase_detection.py` only if the implementation changes `ScopeDecoder` behavior rather than wrapping it.
- `tests/mcp_server/unit/test_server.py` and `tests/mcp_server/test_support.py` if new constructor injection is introduced.

**Size assessment:**
If public output fields stay stable and precedence logic stays above `ScopeDecoder`, #231 remains a small-to-medium change with most of the test churn concentrated in `test_discovery_tools.py` and a small set of project-manager assertions.

### Issue #292 — Ownership Split Plus Conflict-Safe Workflow Writes

For this research, the smallest serious #292 refactor is no longer QA-state isolation alone. It is a combined write-integrity slice: move QA baseline state out of `.st3/state.json`, route workflow-state writes through one explicit mutation contract, and make stale-write or lock/conflict conditions operator-visible through explicit tool feedback plus a recovery hint or note.

**Direct production impact:**
- `mcp_server/managers/qa_manager.py` because baseline persistence and auto-scope resolution currently read and write `quality_gates` inside `.st3/state.json`.
- `mcp_server/managers/phase_state_engine.py` because transition and cycle paths currently load state, mutate subsets of fields, and persist the resulting full branch payload.
- `mcp_server/managers/state_repository.py` or a new adjacent write-coordination component because workflow mutations need deterministic update semantics rather than blind last-writer-wins persistence.
- `mcp_server/core/interfaces/__init__.py` or an equivalent interface location because the broadened slice needs an explicit narrow seam for coordinated workflow-state mutation and the dedicated QA-state repository.
- `mcp_server/server.py` because the new write-coordination collaborator and QA repository must be composed and injected centrally.
- transition, forced-transition, and cycle tool modules because conflict conditions must now return explicit operator feedback rather than silent success.
- `.st3/config/phase_contracts.yaml` because `.st3/quality_state.json` still needs branch-local artifact neutralization.

**Conditional production impact:**
- quality tool modules if recovery hints or notes are surfaced through returned results rather than solely through the manager layer.
- `mcp_server/tools/pr_tools.py` behavior changes automatically via config for QA artifact neutralization, so code changes are not required unless tests or diagnostics demand them.

**Direct test impact:**
- `tests/mcp_server/unit/managers/test_baseline_advance.py` because it currently writes and asserts `quality_gates` inside `.st3/state.json`.
- `tests/mcp_server/unit/managers/test_auto_scope_resolution.py` because auto-scope currently reads `baseline_sha` and `failed_files` from the mixed workflow state file.
- `tests/mcp_server/managers/test_phase_state_engine_async.py` because it is the clearest existing test anchor for state-write races and async persistence behavior.
- `tests/mcp_server/unit/tools/test_transition_phase_tool.py` and `tests/mcp_server/unit/tools/test_force_phase_transition_tool.py` because explicit conflict feedback changes success and error expectations on phase mutation paths.
- `tests/mcp_server/unit/tools/test_cycle_tools.py` and `tests/mcp_server/unit/tools/test_cycle_tools_legacy.py` for the same reason on cycle mutation paths.
- `tests/mcp_server/integration/test_submit_pr_atomic_flow.py` because helper defaults and configured branch-local artifact sets must still grow to include the new QA state file.
- `tests/mcp_server/unit/test_server.py` and `tests/mcp_server/test_support.py` because server wiring and shared test factories will gain the broadened mutation and repository seams.

**Likely lower or no direct change if boundaries stay disciplined:**
- `tests/mcp_server/unit/managers/test_project_manager.py` and `tests/mcp_server/unit/tools/test_discovery_tools.py` remain primarily #231-facing, not #292-facing.
- workflow read-path tests outside the touched consumers should not change merely because write integrity is tightened.

**Size assessment:**
The broadened #292 slice is now a medium-to-large change. It is still bounded if it stops at workflow-state ownership, conflict-safe mutation semantics, and operator-visible conflict handling. It becomes a subsystem redesign only if it starts reworking all readers, all workflow reconstruction semantics, or unrelated PR and branch orchestration at the same time.

### Combined Picture

The combined picture after reopening the scope is now:

- issue #231 remains a narrow read-side ambiguity problem with concentrated blast radius in `get_project_plan()`, `get_work_context()`, and their tests.
- issue #292 is no longer honestly described as QA-state isolation only. It is a write-integrity problem that includes shared ownership, full-document replacement semantics, and operator-facing conflict signaling.
- the two issues are still complementary but asymmetric: #231 should stay read-side, while #292 should own write integrity and ownership boundaries.
- the smallest serious combined program is therefore not a broad state-subsystem rewrite, but it is also not the earlier minimal slice.

---

## Open Questions

- ❓ What is the narrowest explicit write-coordination seam for workflow state: a repository-level mutation API, a dedicated mutation coordinator, or another injected write-only contract?
- ❓ Is an in-process mutation lock sufficient for the currently observed race, or do we need optimistic concurrency/version checks at the repository boundary as well?
- ❓ For #231, what is the minimum field set for a uniform branch-status contract: `current_phase`, `sub_phase`, `current_cycle`, `phase_source`, and `phase_confidence`, or less?
- ❓ Which user-facing consumers must adopt the #231 contract in the first implementation slice to eliminate real ambiguity without widening scope again?

## Related Documentation
- **[docs/development/archive/issue229/research.md][related-1]**
- **[docs/development/archive/issue229/findings.md][related-2]**
- **[docs/development/issue290/research-issue231-state-snapshot.md][related-3]**
- **[docs/development/issue290/research-issue117-get-work-context-phase-detection.md][related-4]**
- **[docs/development/issue231/research-issue231-292-state-cqrs.md][related-5]** — historical exploratory CQRS context only, not the target architecture
- **[docs/development/issue290/research-issue292-state-mutation-concurrency.md][related-6]**
- **[mcp_server/managers/project_manager.py][related-7]**
- **[mcp_server/tools/discovery_tools.py][related-8]**
- **[mcp_server/managers/phase_state_engine.py][related-9]**
- **[mcp_server/managers/qa_manager.py][related-10]**
- **[mcp_server/managers/state_repository.py][related-11]**
- **[.st3/config/phase_contracts.yaml][related-12]**
- **[tests/mcp_server/unit/managers/test_baseline_advance.py][related-13]**
- **[tests/mcp_server/unit/managers/test_auto_scope_resolution.py][related-14]**
- **[tests/mcp_server/managers/test_phase_state_engine_async.py][related-15]**
- **[tests/mcp_server/unit/tools/test_discovery_tools.py][related-16]**

<!-- Link definitions -->

[related-1]: docs/development/archive/issue229/research.md
[related-2]: docs/development/archive/issue229/findings.md
[related-3]: docs/development/issue290/research-issue231-state-snapshot.md
[related-4]: docs/development/issue290/research-issue117-get-work-context-phase-detection.md
[related-5]: docs/development/issue231/research-issue231-292-state-cqrs.md
[related-6]: docs/development/issue290/research-issue292-state-mutation-concurrency.md
[related-7]: mcp_server/managers/project_manager.py
[related-8]: mcp_server/tools/discovery_tools.py
[related-9]: mcp_server/managers/phase_state_engine.py
[related-10]: mcp_server/managers/qa_manager.py
[related-11]: mcp_server/managers/state_repository.py
[related-12]: .st3/config/phase_contracts.yaml
[related-13]: tests/mcp_server/unit/managers/test_baseline_advance.py
[related-14]: tests/mcp_server/unit/managers/test_auto_scope_resolution.py
[related-15]: tests/mcp_server/managers/test_phase_state_engine_async.py
[related-16]: tests/mcp_server/unit/tools/test_discovery_tools.py

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-26 | Agent | Initial draft for minimal workflow-state hardening across issues #231 and #292 |
| 1.1 | 2026-04-26 | Agent | Added the issue #229 historical trace, concrete #231 symptom framing, SSOT confirmation for branch_local_artifacts, and narrowed the first #231 slice to eliminating branch-status ambiguity |
| 1.2 | 2026-04-26 | Agent | Added explicit blast-radius mapping for the minimal #231 read-contract slice and the minimal #292 QA-state-isolation refactor, including direct and conditional test impact |
| 1.3 | 2026-04-26 | Agent | Incorporated QA review feedback: made the #292 schema conflict explicit, widened artifact-helper test impact, and reclassified the cross-machine #231 integration test as secondary impact |
| 2.0 | 2026-04-26 | Agent | Reopened #292 scope after validating the source issue: broadened the research from QA-state isolation only to ownership split plus conflict-safe workflow writes while keeping #231 read-side scope narrow |
| 2.1 | 2026-04-26 | Agent | Locked operator-facing conflict signaling as a hard requirement, made the writer audit boundary explicit, and demoted the broad CQRS document to historical context only |
