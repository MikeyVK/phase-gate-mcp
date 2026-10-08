<!-- pgmcp:v1 id=research pv=1.0.0 pf=lgBwxWMfTAmNNg_O sf=5--KpGf2wHUv2qAj -->

# Issue \#491 — Planning creation and mutation contracts

**Status:** DRAFT — owner strategy discussion pending  
**Version:** 0.5  
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

The strategy table records the options originally presented. The owner subsequently defined total as the desired whole-plan size after save/update, with complete-block mutation and common result validation. Git-backed deletion protection is a tentative exploration; see Approved Strategy and the evidence below.

### Tentative Git-backed deletion protection

The owner requires completed cycles to remain non-deletable, but does not assume a reliable completed status. The proposed evidence boundary is narrower: an execution commit attributable to this issue and cycle would protect the cycle from deletion, even while work is ongoing. This is exploration, not an approved implementation or a proof of completion.

| Evidence / boundary | Observed fact or unresolved requirement |
|---|---|
| Existing commit trace | GitCommitTool requires cycle_number in a configured cycle-based phase. GitManager formats type(scope): message (#issue); ScopeEncoder emits, for example, P_IMPLEMENTATION_SP_C1_GREEN. Local history includes 631b32f0 with this scope and issue #483. |
| Missing trace without subphase | ScopeEncoder.generate_scope returns P_PHASE immediately when sub_phase is None, ignoring a supplied cycle_number. Commit admission permits this case. Absence of a cycle marker is therefore not currently proof that no cycle execution commit exists. |
| Existing decoder | ScopeDecoder detects phase and a composite sub_phase such as c1_green; PhaseDetectionResult has no cycle_number field. A trustworthy cycle query is not already provided by this decoder. |
| Existing history reader | GitAdapter.get_recent_commits returns a limited list of subject strings (default five), without commit identities or an issue-branch history boundary. It is insufficient for an exhaustive deletion decision. |
| Trace meaning | A commit merely listing a future cycle in planning is not execution evidence. Evidence must belong to the relevant issue/cycle and the issue's execution history; inherited C1 commits from other issues must not protect this issue's C1. Exact reachable-history and branch-basis semantics remain to be chosen. |
| Revert and exceptional repair | Reverting changes does not erase the execution commit from reachable history, so the proposed protection remains. Removing/replacing history is exceptional repair outside this issue; no normal-workflow bypass is proposed. Reflogs, dangling objects and unrelated refs are not assumed to define the guard. |
| Deletion versus edit | Evidence-based non-deletion does not itself freeze a cycle's name, criteria or deliverables, nor prove completion. Renumbering/replacement must not silently reinterpret an evidenced cycle identity. |
| State coherence | A no-commit conclusion cannot permit leaving current_cycle, last_cycle or lifecycle references outside the resulting plan. Handling such references is an additional boundary, not evidence of completed work. |
| Failure and existing histories | Unavailable/incomplete history or ambiguous attribution cannot establish safe deletion. Policy for these cases, and existing commits without cycle markers, requires an explicit decision; no guessed attribution or compatibility bridge is approved. |

Candidate seam: a narrow injected read-only execution-evidence boundary at the planning command, with Git access owned by the existing Git layer and shared identity/encoding conventions. Pure planning models remain free of Git/state IO. Correcting trace completeness and defining exhaustive evidence would add a bounded Git-contract surface; this cost must be weighed before adopting the route. No new completion registry or general audit architecture is implied.

### Subphase admission and cycle-trace completeness

cycle_number identifies the planning/execution cycle; sub_phase identifies the kind of work within it. They are independent inputs. Their current coupling is an encoding choice: ScopeEncoder includes Cn only inside a scope with a subphase.

| Current boundary | Source-confirmed behavior |
|---|---|
| Public input | GitCommitInput permits omitted cycle_number and sub_phase. Dynamic requirements belong to runtime resolution, not a pure input model reading configuration/state. |
| Runtime phase/cycle admission | GitCommitTool resolves the active workflow, requires cycle_number when its phase has cycle_based=true, and applies the injected phase/cycle mismatch guard. No analogous subphase-required check exists. Both explicit-phase and auto-detected-phase routes use the cycle requirement. |
| Config split | contracts.yaml defines workflow-specific cycle_based, subphases and commit_type_map; workphases.yaml defines the phase catalog and the subphase whitelist used by ScopeEncoder. Current feature/bug/hotfix/refactor implementation contracts are cycle-based with red/green/refactor; chore implementation is not cycle-based. A rule keyed only to the name implementation would be incorrect. |
| Validity versus requirement | ScopeEncoder validates a supplied subphase against the workphase catalog. resolve_commit_type uses the workflow's commit_type_map when no explicit commit_type is given. Neither makes omitted subphase mandatory. An explicit commit_type must not bypass future subphase admission. |
| Config guarantees | PhaseContractPhase currently requires a nonempty commit_type_map for cycle-based phases. It does not prove nonempty subphases or agreement between workflow subphases, mapping keys and the workphase catalog. The inspected ConfigLoader validates these models separately. |
| Intentional old encoding | test_cycle_number_without_subphase_ignored explicitly expects P_IMPLEMENTATION when cycle_number=1 and no subphase is supplied. This is existing documented behavior, not an untested accidental branch. The new trace promise would require an explicit clean-break decision. |
| Side effects | GitCommitTool performs its cycle-required check before record_sub_phase, staging and commit. The equivalent subphase admission belongs before these mutations. current_sub_phase is recorded by the commit command and cleared at phase/cycle transitions; it is not a separate enforced execution mode. |

The earlier proposed mandatory-subphase route is withdrawn as the recommendation. The owner correctly challenged its premise: a cycle is not a subphase, and requiring one merely to preserve a cycle marker would impose workflow behavior to accommodate an encoding limitation.

Historical origin is source-confirmed: #138 described cycle_number as optional multi-cycle TDD metadata and used P_TDD_SP_C1_RED; the initial encoder commit c13fdeff7caab97aeb0cd41542568c56068efb1f (2026-02-15) already returned a phase-only scope before inspecting cycle_number when sub_phase was absent. #146 then strengthened cycle admission around TDD subphases using that format. This explains the implementation history, not a necessary dependency between cycle identity and subphase.

Current state already models current_cycle and current_sub_phase independently. WorkflowStatusResolver reads those distinct fields directly from state; commit decoding is not its current status source. Conversely, ScopeDecoder has no typed cycle field and returns c1_green as a composite sub_phase for P_IMPLEMENTATION_SP_C1_GREEN. Thus both encoding and any reader used for future Git evidence must distinguish cycle identity from subphase without inferring that one requires the other.

| Independent semantic combination | Required meaning, subject to active workflow admission |
|---|---|
| Phase only | Preserve phase identity; no cycle or subphase asserted. |
| Phase + cycle | Preserve the explicit cycle identity even when subphase is absent. |
| Phase + subphase | Preserve the configured subphase; do not infer a cycle from labels such as planning subphase c1. |
| Phase + cycle + subphase | Preserve both distinct values. |

Revised bounded direction for owner review: retain the existing runtime requirement for cycle_number in cycle-based phases and remove the encoder's loss of cycle identity when sub_phase is omitted. Keep subphase validation when supplied; a future subphase requirement would need its own workflow-policy rationale, not Git trace retention. No new execution mode, forced RED/GREEN/REFACTOR sequence, completion registry or extra config flag is implied.

Two bounded representation choices remain: extend the current spelling with an unambiguous cycle-only form while leaving combined spelling unchanged, or adopt one uniform spelling with separate cycle and subphase components. The latter has a broader encoder/decoder/doc/test impact; the former minimizes changed combined scopes. Exact syntax, clean-break/migration policy and reader shape are Design inputs only after boundary-specific owner approval. Existing historical Git evidence is a separate concern: future lossless scopes cannot recover omitted cycle identity from old commits.

The earlier optional encoder rejection for cycle_number without sub_phase is also withdrawn as a preferred solution: it rejects a semantically valid combination instead of representing it. Public input DTOs and state field meanings need not be coupled or redesigned to fix this boundary. Existing behavioral tests that expect information loss would be adapted to the new contract, with proportional encoding/decoding and command admission coverage; no old-behavior compatibility tests or content-mirroring coverage are proposed.

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

- Confirm the exact complete-block replacement unit and omission/null rules, including phase-deliverable blocks. total now means the desired whole-plan size, not the number of supplied update entries.
- Decide whether execution commits define non-deletable cycles; define attributable history, missing/ambiguous evidence and existing histories without cycle markers. Decide lossless independent cycle/subphase representation and its encoder/reader strategy. Mandatory subphase solely for Git trace retention is no longer recommended.
- Define active/entered/historical reference protection when shrinking the plan, independently of a completed status; reject supplied entries outside total or give them another explicit meaning.
- Confirm compatibility policy per affected boundary and explicitly include or defer the admitted file_glob shape mismatch.

## Approved Strategy

Owner direction on 2026-10-08 confirms:
- Preserve the #229 distinction: write-once initial save and an explicit later mutation operation.
- Mutations provide complete blocks so their internal context is coherent; nested partial-field patching is not the requested route. Remaining block/omission details still need an explicit contract.
- For both save and update, total means the desired total number of cycles in the whole plan after the operation. It does not mean the number of supplied update blocks. Unprovided existing cycles within 1..total remain; supplied complete cycle blocks replace their corresponding blocks; existing cycles above total are removal candidates, subject to protection.
- Both operations apply one common complete-result validation before persistence: the final cycle sequence must be exactly C1..Ctotal, with complete valid blocks and no gaps/duplicates. Count validation uses the resulting plan; it never manufactures missing cycles.
- Completed cycles must never be deleted. The owner tentatively proposes execution commits as evidence for non-deletion, while acknowledging that such evidence does not identify completion. This evidence mechanism is not yet approved.

Current save checks a caller-supplied total against list length; it does not currently derive that input. The existing creation schema is therefore an evidence input to reconcile, not assumed flawless: the admitted file_glob/executor mismatch and identity uniqueness still require resolution.

Pending owner decisions: the Git-backed protection route and its attribution/completeness/failure policy; protection of active/entered/historical cycle references; remaining complete-block omission/null semantics, out-of-range supplied entries, nested validation alignment and boundary-specific compatibility policy. These remain product/strategy choices, not an approved implementation. Research remains open; no Design transition is requested.

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
- [Commit admission and lifecycle guard](<../../../mcp_server/tools/git_tools.py>)
- [Commit scope encoding](<../../../mcp_server/core/scope_encoder.py>)
- [Current scope decoding](<../../../mcp_server/core/phase_detection.py>)
- [Existing Git history access](<../../../mcp_server/adapters/git_adapter.py>)
- [Workflow contract schema](<../../../mcp_server/config/schemas/contracts_config.py>)
- [Workflow-specific policies](<../../../.pgmcp/config/contracts.yaml>)
- [Workphase catalog](<../../../.pgmcp/config/workphases.yaml>)
- [Encoder behavior evidence](<../../../tests/mcp_server/core/test_scope_encoder.py>)
- [Commit-tool behavior evidence](<../../../tests/mcp_server/unit/tools/test_git_tools.py>)
- [#138 original scope contract](<../archive/issue138/design.md>)
- [#146 TDD cycle admission research](<../archive/issue146/research.md>)
- [Current state-derived workflow status](<../../../mcp_server/managers/workflow_status_resolver.py>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-08 | @imp researcher | Record source-confirmed creation/update/readback gaps, historical rationale, affected consumers and unapproved boundary options. |
| 0.2 | 2026-10-08 | @imp researcher | Capture owner-confirmed complete-block mutation and shared result validation/count derivation; keep collection replacement and lifecycle protection explicit open decisions. |
| 0.3 | 2026-10-08 | @imp researcher | Refine total to desired whole-plan size and record tentative Git-backed non-deletion protection, observed trace limitations and unresolved evidence/state boundaries. |
| 0.4 | 2026-10-08 | @imp researcher | Map intentional subphase/cycle encoding, runtime/config policy boundaries and bounded enforcement options without approving or implementing them. |
| 0.5 | 2026-10-08 | @imp researcher | Trace the TDD origin and withdraw mandatory-subphase/rejection recommendations; assess independent lossless cycle/subphase representation and bounded reader impact. |
