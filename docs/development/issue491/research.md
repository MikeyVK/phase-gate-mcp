<!-- pgmcp:v1 id=research pv=1.0.0 pf=lgBwxWMfTAmNNg_O sf=5--KpGf2wHUv2qAj -->

# Issue \#491 — Planning creation and mutation contracts

**Status:** DRAFT — owner strategy discussion pending  
**Version:** 0.1  
**Last Updated:** 2026-10-08

## Purpose

Establish the evidenced contract gaps and owner decisions needed for a bounded refactor of planning creation, updates and readback.

## Scope In

save_planning_deliverables/update_planning_deliverables input admission, persisted effects, merged-plan validity, identity/order, lifecycle ownership, nested validation specs and complete public readback; relevant existing tests and historical rationale.

## Scope Out

Implementation/design/cycle planning; a generic deletion tool, new event-sourcing architecture, broad workflow/fixture modernization, unrelated adapter/transport work and compatibility bridges not approved by the owner.

## Problem Statement

Planning creation validates a complete plan, while mutation validates only a partial payload and writes its merged result without complete-plan validation. Some admitted fields have no effect and historical lifecycle constraints do not map directly to current state. Research must distinguish defects from deliberate merge policy before changing the contract.

## Goals

- Map every admitted field to its persisted effect and downstream consumers.
- Separate evidenced contract gaps, deliberate constraints and owner product choices.
- Present boundary-specific strategy options with proportional cost and risk; retain a pending approval state until the owner decides.

## Background

Source inspection on 2026-10-08 uses base commit 2366ef78baaf1df79704d06133f1136399a9ea37 and follows #491's Research leads. #229 deliberately separated write-once save from iterative merge-update; its C8 decision classified cycle deletion as append-only audit policy. #390 introduced strict frozen input models and renamed tdd_cycles to cycles with a clean break. #257 described mutable open cycles and read-only completed cycles, but the current cycle history records entered events rather than completed status. Historical decisions are material inputs, not automatic present-day requirements.

## Findings

### Current responsibilities and invariants

| Boundary | Current contract / source evidence | Consequence |
|---|---|---|
| Creation | ProjectManager.save_planning_deliverables validates CyclePlanningModel, checks a prior save, and requires cycles when workflow configuration has a cycle-based phase. | Preserve explicit create-versus-update ownership unless the owner chooses otherwise. |
| Update admission | UpdatePlanningModel permits partial cycle entries and optional/null fields; tools serialize with model_dump(exclude_none=True). | Omission and explicit null collapse at the public tool boundary; no optional-field clearing intent survives. |
| Existing cycles | Lookup uses cycle_number; deliverables merge by id; exit_criteria is copied if present. name is never copied. | An admitted name-only update has no effect while the tool can report success. |
| New cycles | Unknown cycle_number entries append as partial dictionaries. | Missing required fields, gaps, zero/negative indices or invalid order can survive update admission and reach storage. |
| Derived total | Incoming cycles.total is not assigned. The updater keeps max(existing total, highest cycle_number); output total_cycles is list length. | The historical derivation was deliberate. Assertion/rejection versus removal from writable input is a product decision; silent admission is misleading. |
| Deliverable replacement | A matching id replaces the entire supplied deliverable object; description is required. Omitted validates disappears on replacement. | This is documented whole-object replacement, not nested field patching. New partial-deliverable semantics would change the public contract. |
| Empty collections | Empty cycle/deliverable lists do not delete existing entries; an empty update can still write successfully. | Deletion, clearing, idempotent no-op reporting and replacement must be explicit choices. |
| Identity | Complete save enforces sequential cycle positions and total == length; no deliverable-ID uniqueness validator exists. Updates have no equivalent final validation. | Duplicate IDs or repeated cycle updates have ambiguous lookup effects; the intended uniqueness domain needs a decision. |
| Merged-plan validity | Update validates UpdatePlanningModel before merge, then writes without CyclePlanningModel validation. StateVersionValidator validates JSON/envelope version only. | An update can persist a plan that creation and the public complete readback would reject. |
| Readback / success | get_project_plan strictly validates stored planning with CyclePlanningModel; mutation summaries contain counts, not names/specs. | Complete readback already exists. A successful mutation must yield a valid, faithful readback; expanding presentation/cache architecture is unnecessary. |
| Nested validates | ValidatesModel admits file_glob with file and forbids dir/pattern. DeliverableChecker's file_glob requires dir/pattern. | The public planning schema and existing gate executor disagree. This is a directly affected nested contract, not a request for a new checker. |
| Lifecycle protection | save/update are branch_mutating tools subject to context-loaded and PR-lock enforcement. ProjectManager.update reads no cycle history and records no per-update audit. | Those guards do not implement completed-cycle immutability. The archived guard cannot be reinstated by assuming a nonexistent completed status. |

These are source-confirmed observations, not live malformed-input reproductions or newly executed failure tests. Illustrative consequences: a rename of existing C1 is ignored; appending C3 to C1 can store total=3 with two entries; appending a number-only cycle can store a missing deliverables/exit_criteria entry. Neither invalid append outcome satisfies the complete creation/readback model.

### Structural seams and preservation limits

The two per-ID merge loops and save/update response assembly are duplicated. Candidate seams are the existing planning value models, ProjectManager's command boundary, injected read-only lifecycle state and existing public readback. No new generic mutation language or workspace deletion subsystem is required merely to reconcile these contracts. Pure models must not read state/config files; phase/workflow policy stays config-driven; persistence remains atomic and owned by the existing command path.

cycle_number is both lookup identity and execution order. PhaseStateEngine reads stored total for range checks and stores cycle number/name in entered history; PhaseContractResolver selects checks by cycle number and deliverable ID. Renumbering or reordering started cycles therefore changes the meaning of existing references. Git history preserves historical bytes, but does not itself prevent reinterpretation of active lifecycle references. Atomic file replacement protects against partial bytes, not an invalid merged plan or concurrent read/modify/write races.

### Strategy options for owner review

| Boundary | Narrow coherent option | Alternative and cost/risk |
|---|---|---|
| Public create/update ownership | Keep write-once save plus explicit update; fix ignored admitted fields and validate the resulting plan before writing. | Whole-plan replacement simplifies some edits but expands accidental deletion/overwrite risk. |
| Field intent | Preserve omitted fields; define null explicitly per optional field. Keep deliverables as complete replacement by id if desired. | Uniform deep patch needs new partial-deliverable semantics and nested clearing rules; more schema/test/consumer change. |
| total | Derive canonical count; optionally retain supplied total as a checked assertion of the resulting count. | Remove total from writable requests in a clean break, requiring mechanical caller/doc updates. Both avoid silent acceptance. |
| Identity/order | Stable cycle_number and scoped IDs; unambiguous duplicates rejected; validate a complete sequential result. | Separate stable cycle IDs from order is a larger feature/architecture change and not required for current gaps. |
| Delete/renumber/reorder | Retain append/update semantics for this issue after explicitly reassessing the original audit rationale. | Allow replacement of not-yet-started work only, with explicit reference/lifecycle validation. Feasible but a new feature with higher cost; not preapproved or permanently excluded. |
| Lifecycle | Define which cycles are protected using actual entered/current/forced/phase events and an injected narrow state reader. | Freeze all entered cycles is simpler but also freezes active work. Completed-only protection needs a precise completion/reopen policy; no guessed status field or hardcoded phase checks. |
| Nested validation specs | Align planning admission with the existing executor's supported shapes. | Deferring the mismatch keeps an admitted unusable planning rule; requires explicit exclusion rather than a false holistic-completion claim. |
| Compatibility / verification | Clean break for corrected semantics, no bridge/alias for silently ignored inputs; preserve supported create/update/readback behavior. Adapt valuable behavior tests. | Preserving ignored inputs needs an explicit compatibility promise with low functional value. No new tests for the purpose of preserving obsolete behavior. |

Recommended discussion direction: repair the existing save/update route and shared validity boundary before considering richer re-planning features. The field, lifecycle and compatibility choices above are not approved by this recommendation.

### Existing evidence and proportional test surface

| Existing coverage | Value to retain | Material gap / coupling |
|---|---|---|
| test_project_manager.py complete save tests | Prior-save guard, required cycles, total consistency, sequential numbering, nonempty deliverables/exit criteria | No final merged-plan proof in the current update route. |
| test_project_tools.py save/update groups | Append, scoped merge/replacement, phase entries, exit-criteria change and invalid validates input | No direct name/null/total-conflict/invalid-new-cycle/lifecycle protection cases among inspected tests. Several assertions inspect persisted JSON directly. |
| GetProjectPlanTool readback tests | Full stored planning, order/criteria, initialized-without-planning support, invalid stored-plan rejection | Reuse this public query to observe approved future mutation behavior. |
| DeliverableChecker file_glob tests | Existing dir + pattern execution contract | Planning input schema tests do not prove the end-to-end admitted rule is executable. |
| Cycle integration/state tests | Cycle range/order and lifecycle consumers | make_project_manager/make_phase_state_engine plus legacy_suite_workspace couple setup to injected configs/state. Refactor only fixtures/helpers invalidated by the selected boundary; avoid a broad rewrite. |

No tests were added or run in this Research pass. No production/configuration/agent source was modified. Concrete behavioral counterexamples can be demonstrated with isolated fixtures after the contract scope is agreed; do not corrupt #491's live planning as an exploratory probe.

## Questions

- Which update intent is required: complete deliverable replacement by id, or partial field patching; what must explicit null and empty collections mean?
- Should supplied total be a checked assertion or disappear from writable input; what identity/duplicate/order guarantees must hold?
- Do delete/renumber/reorder of not-started work belong in #491, and how are active/completed/reopened cycles protected using actual lifecycle evidence?
- Approve clean break versus compatibility per affected input/storage/readback/lifecycle boundary, and explicitly include or defer the admitted file_glob shape mismatch.

## Approved Strategy

Pending owner discussion. No boundary strategy is recorded as approved by the initial Research GO. Research remains open; Design and implementation must not start until the owner choices are explicit.

## Expected Results

Every supported planning mutation has an explicit observable effect or a truthful rejection; creation and resulting-update plans obey one coherent validity contract; failed validation leaves persisted planning unchanged; identity/order and lifecycle protection match the owner decision; complete public readback faithfully represents saved state. No generic deletion architecture or compatibility layer is assumed.

## Consumers

### Planning agents and native save/update callers

Create and evolve authoritative planning through public tools.

**Impact:** Field/null/total/replacement changes alter request meaning; migration must be explicit.

### ProjectManager and existing atomic writer

Read/validate/merge/persist issue plans.

**Impact:** Final-plan validation and policy coordination must remain at proper command boundaries.

### GetProjectPlanTool / IProjectPlanReader

Read complete typed planning without mutation.

**Impact:** Existing readback is an observable validity and fidelity boundary to preserve.

### PhaseStateEngine / workflow state and cycle history

Execute numbered cycle progression and record lifecycle evidence.

**Impact:** Structural mutation must preserve reference meaning and define protection without assuming completed status.

### PhaseContractResolver / DeliverableChecker

Select and execute issue-specific checks.

**Impact:** Cycle/ID identity and admitted validates shapes must agree with downstream selection/execution.

### Existing test support, active project reference and phase instructions

Exercise and describe planning contracts.

**Impact:** Update only directly invalidated behavior tests/docs/instructions; historical artifacts remain reviewed context.

## Risks

### A nominally successful update can persist a plan rejected by complete readback.

Agree one resulting-plan validity promise before Design; observe mutation through the public query.

**Consequence:** Agents may rely on invalid planning or require direct repairs.

### Renumbering/deletion changes the meaning of lifecycle and gate references.

Obtain explicit owner policy; preserve stable references and assess not-started-work boundaries.

**Consequence:** Historical/current execution evidence can be reinterpreted.

### A guessed completion guard recreates archived intent inaccurately.

Use actual entered/current/forced/phase evidence and define reopened-cycle handling explicitly.

**Consequence:** Valid active edits could be blocked or completed work left mutable.

### A holistic issue can grow into general mutation/audit/concurrency infrastructure.

Keep shared plan semantics in scope; document unproven concerns separately and avoid hypothetical architecture.

**Consequence:** Effort grows beyond evidenced contract defects.

## Related Documents

- [ProjectManager create/update/readback](<../../../mcp_server/managers/project_manager.py>)
- [Planning value models](<../../../mcp_server/schemas/deliverables.py>)
- [Public project tools](<../../../mcp_server/tools/project_tools.py>)
- [Current project-tool reference](<../../reference/tools/project.md>)
- [#229 original update design](<../archive/issue229/design-c5-c7.md>)
- [#229 append-only decision](<../archive/issue229/planning.md>)
- [#257 historical lifecycle decision](<../archive/issue257/%23archive/research_config_first_pse.md>)
- [#390 strict-schema design](<../archive/issue390/design.md>)
- [Existing project-tool behavior tests](<../../../tests/mcp_server/unit/tools/test_project_tools.py>)
- [Existing complete-save tests](<../../../tests/mcp_server/unit/managers/test_project_manager.py>)
- [Existing gate executor](<../../../mcp_server/managers/deliverable_checker.py>)
- [Current cycle lifecycle](<../../../mcp_server/managers/phase_state_engine.py>)
- [Issue gate selection](<../../../mcp_server/managers/phase_contract_resolver.py>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-08 | @imp researcher | Record source-confirmed creation/update/readback gaps, historical rationale, affected consumers and unapproved boundary options. |
