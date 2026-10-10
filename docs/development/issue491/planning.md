<!-- pgmcp:v1 id=planning pv=1.0.0 pf=CscfYyDLqj0OeHml sf=5--KpGf2wHUv2qAj -->

# Issue \#491 — Planning mutation contract execution

**Status:** DRAFT — independent Planning review requested  
**Version:** 1.1  
**Last Updated:** 2026-10-10

## Purpose

Sequence the approved Design into three coherent clean-break cycles, keeping changes and verification at their owning boundaries.

## Scope In

The seven execution deliverables below, their actual production/test consumers, necessary configuration/template changes, one representation-only workspace adjustment, required Validation and focused active documentation.

## Scope Out

Compatibility/legacy behavior, historical closed-issue cleanup, completion registries, a general mutation/transaction/migration architecture, extra content tests, unrelated tooling or broad documentation rewrites.

## Prerequisites

- Independent Design GO from Beoordeel designplan on e35987036ce1c46714b97b9d970685dc2f71ec65, no remaining findings; owner approved Planning on 2026-10-09.
- Research v1.16 Approved Strategy remains binding. Design v1.2 owns the concrete contracts; this document only sequences them.
- Before execution obtain independent Planning GO and owner authorization. No production/config/test edits or test runs have been performed in Planning.

## Summary

Three cycles follow actual dependency direction: shared codec/Git evidence → complete planning commands and readers → state entry/initialization/configuration cleanup. Do not introduce a temporary compatibility bridge between cycles.

| Cycle | Dependency | Execution deliverables |
| --- | --- | --- |
| C_1 | Approved Design | D_1.1–D_1.2: shared codec and Git evidence |
| C_2 | C_1 | D_2.1–D_2.3: planning mutation, consumers and explicit cutover |
| C_3 | C_2 | D_3.1–D_3.2: state entry, initialization and policy cleanup |

### Execution entry points

| Cycle | Production/configuration seams |
| --- | --- |
| C_1 | [ScopeEncoder](../../../mcp_server/core/scope_encoder.py), [ScopeDecoder](../../../mcp_server/core/phase_detection.py), [retained wrapper](../../../mcp_server/core/commit_phase_detector.py), [GitManager](../../../mcp_server/managers/git_manager.py), [GitAdapter](../../../mcp_server/adapters/git_adapter.py), [composition root](../../../mcp_server/bootstrap.py) |
| C_2 | [Planning values](../../../mcp_server/schemas/deliverables.py), [ProjectManager](../../../mcp_server/managers/project_manager.py), [project tools](../../../mcp_server/tools/project_tools.py), [tool outputs](../../../mcp_server/schemas/tool_outputs.py), [resolver](../../../mcp_server/managers/phase_contract_resolver.py), [checker](../../../mcp_server/managers/deliverable_checker.py), [enforcement](../../../.pgmcp/config/enforcement.yaml), [planning package](../../../.pgmcp/template_suite/planning/template.jinja2), [shared test support](../../../tests/mcp_server/test_support.py) |
| C_3 | [PhaseStateEngine](../../../mcp_server/managers/phase_state_engine.py), [phase tools](../../../mcp_server/tools/phase_tools.py), [state mutator](../../../mcp_server/managers/workflow_state_mutator.py), [read-only reader](../../../mcp_server/core/interfaces/project_plan.py), [contracts model](../../../mcp_server/config/schemas/contracts_config.py), [workspace contracts](../../../.pgmcp/config/contracts.yaml) |

These are navigation entry points; the Research register and actual diff govern complete consumer coverage.

### Evidence selection and timing

At each cycle establish only the relevant existing green baseline. Adapt valuable public behavior coverage; add intended RED only for a durable uncovered obligation under the Refactor contract. Do not add old-behavior rejection/compatibility tests, source/private-attribute assertions, test-count targets or tests that merely mirror DTO declarations. Parameterize a small set of observable cases rather than multiplying near-identical tests.

Focused execution calls use `run_tests(scope="targets", targets=<affected existing/new behavior test files>, tests=["python_tests"], timeout_seconds=600)`. Omit `args` so native arguments remain intact. The file surfaces are named per cycle; narrow to relevant cases when evidence remains sufficient. Do not run the entire helper-caller register just because its constructors share a factory.

For each cycle independently select actually changed `.py` files from Git. Apply `run_checks(scope="targets", targets=<changed Python production and test files>, checks=["python_format","python_lint","python_pyright"], timeout_seconds=600)`. Mypy applies to changed production targets only (`python_types`), not test mocks. Markdown uses `markdown_links`; YAML/JSON/template changes use real loader/schema/renderer behavior and their owning checks, never Python target lists. Reuse fresh evidence until an applicable subsequent change invalidates it.

Validation owns these required broad calls after all cycles and live cutovers:
- `run_tests(scope="configured", tests=["python_tests"], timeout_seconds=1800)`: one complete native-configured suite; retain configured parallelism, slow/hermetic coverage and native arguments. Increase timing if the observed workload requires it; a timeout is incomplete.
- `run_checks(scope="branch", checks=["python_format","python_lint","python_types","python_pyright","markdown_links"], timeout_seconds=600)`: existing per-check configured_targets policies perform type-appropriate branch preselection. Do not supply mixed branch targets manually to Python checks.
- `run_checks(scope="configured", checks=["python_format","python_lint","python_types","python_pyright"], timeout_seconds=600)`: final workspace native-configured Python run, including the production-scoped strict Mypy definition. This supplements the mandatory branch run; it does not replace it.
- Document the changed Markdown selection/outcome from scaffold/edit validation and the final branch link run; recheck later document edits only when invalidated.

Use the client execution window described in setup guidance so the configured run can complete and deliver its response. Record exact calls, scope, meaningful native outcomes and limitations in one compact Validation report. Run IDs/cache URIs are supplementary navigation, never the sole durable evidence. Required failures/incomplete runs stop progression; no exclusions, weakened assertions or speculative repairs.

### Storage bootstrap and reversal

The installed tools still expose the old planning schema. Save this plan once through that schema during Planning, with explicit total=3, ordered numbers and ids matching this document. The bootstrap payload is not the new target API. At C_2's clean break, manually adjust only #491's nested existing storage with safe_edit_file as allowed by the approved workspace-upgrade strategy. Future stored cycle_name equals each work-unit name; deliverable_name equals the description prefix before “ — ”. Persist the exact existing descriptions/exit criteria/rules, C_n/D_n.m references and phase-local D_1 values. Preserve envelope/version, other issues and workflow state; compare complete native readback after restart. This operation changes representation only; any semantic re-planning stops for a new decision.

Each cycle has a committed boundary and remains independently reversible through native Git restore of the complete affected source/config/test slice plus server restart. C_2 reversal must restore its matching plan representation as well. Do not use partial rollback or add compatibility paths; if a reversal would discard meaningful later work, stop and coordinate. No cross-process/cross-file transaction guarantee is claimed.

### Planning preparation evidence

On 2026-10-09, scaffold_artifact(artifact_type="planning", file_name="planning.md", target_path="docs/development/issue491", validation="enforce") and the focused document refinement reported written/passed Markdown validation. save_planning_deliverables(issue_number=491, planning_deliverables=<the three work units and two phase blocks above>) succeeded: three cycles and nine deliverables, with execution counts 2/3/2. get_project_plan(491)'s complete DTO was read and compared with that submitted payload: identical order, IDs, descriptions, exit criteria and phase validation rules. Planning is active. No production/config/test files were edited and no tests were run in this phase.

### Authoritative inputs and review status

Research consumer inventory is the discovery bound; the actual changed-file inventory belongs to Implementation. Generic planning-document work-unit IDs remain authoring metadata, distinct from server-generated operational identifiers. Validation D_1 and Documentation D_1 are local to their respective phase blocks. Planning is DRAFT until separately invoked independent QA returns its verdict; no implementation approval is claimed.

## Dependencies

- Configuration-first policy, constructor injection, CQS, frozen values and narrow read interfaces remain the applicable architecture obligations.
- Cycle C_1 wires shared codec/Git seams without changing ProjectManager's constructor; C_2 introduces its required evidence reader and updates its actual factories in the same cutover.
- C_2 migrates PSE's affected read shape only; C_3 owns behavioral transition composition and IProjectPlanReader narrowing.
- Implementation gates/tests are focused; one complete configured test run plus branch/configured gates belong to Validation. No tests are executed to approve a paper plan.

## Risks

### The branch changes the planning and scope contracts it is using.

Reload the codec before first execution commit; use one explicit representation-only #491 storage adjustment before the new model is loaded, then verify health/context/full plan. Stop on mismatches.

**Consequence:** A failed cutover blocks progression; no runtime compatibility route is permitted.

### Constructor and storage changes affect shared fixtures and operational template projections.

Use the verified consumer register and actual direct callers; migrate factories centrally and adapt public behavior coverage at the same cycle boundary.

**Consequence:** Hidden consumers require a targeted inventory extension, not a blanket test rewrite.

### Incomplete Git evidence or write/readback failures may be mistaken for success.

Preserve known positives and structured uncertainty. Verify failure effects and emit successful override only after persistence.

**Consequence:** Force does not authorize protected deletion, stale plans or invalid phase selection.

## Milestones

- C_1: shared codec/evidence and decodable execution metadata.
- C_2: one complete planning contract and identical stored/public references.
- C_3: safe explicit phase entry, initialization and configured cleanup.
- Validation: full configured suite, branch gates and final configured Python gates with durable evidence.
- Documentation and Ready: narrow validated reference reconciliation, independent review and eventual Coordinatie hand-over.

## Work Units

### C\_1 — Shared scope and local execution evidence

**Goal:** Make issue-attributed execution evidence trustworthy at the existing Git boundary before planning commands consume it.

**Cycle Number:** 1

**Owner:** @imp implementer

#### Scope In

ScopeContract and vocabulary admission, encoder/decoder/result and retained wrapper, Git title normalization, captured-HEAD history, ICycleEvidenceReader/CycleEvidence, GitManager/bootstrap and directly affected fixture/constructor callers.

#### Scope Out

Planning DTO/storage changes, state transition semantics and public planning admission. Keep bounded recent-commit display unchanged.

#### Deliverables

##### D\_1.1

Shared lossless scope contract — One configured grammar round-trips independent phase/cycle/subphase, immutable results and unknown outcomes; retained CommitPhaseDetector receives its decoder. Direct Git wiring and actual constructor consumers use that contract.

**Owner:** @imp implementer

##### D\_1.2

Captured-HEAD cycle evidence — Existing GitAdapter/GitManager implement the narrow read-only evidence contract with complete ancestry, exact issue/configured execution-phase qualification, completeness reasons and retained positives; matching issue markers are normalized in the title only.

**Owner:** @imp implementer

#### Exit Criteria

Shared codec and actual Git evidence behavior pass focused tests and applicable Python gates; native bootstrap loads and a cycle-bearing implementation commit is produced with the new codec. No duplicate grammar, query-time decoder/config loading or recent-commit cutoff remains in the evidence route.

#### Dependencies

- Approved Design v1.2; no Implementation work before independent Planning GO and owner progression.

#### Obligations

- Shared pure vocabulary admission must not create a runtime schema/core import cycle; ConfigLoader remains the sole configuration loader.
- Known positives survive incomplete classification; no last-N/all-refs/first-parent/merge-base/network dependency and no hardcoded execution phase.
- GitAdapter returns opaque metadata; GitManager qualifies issue/scope and owns title normalization. Preserve different issue numbers, larger numeric references and the body.
- Keep the producer's first execution commit decodable: migrate and restart the live codec before making any Implementation-scoped commit. Treat the codec cutover as structural adaptation with its existing adequate coverage, not an artificial RED exercise. A genuine uncovered Git-evidence behavior receives intended RED after that seam is available.

#### Verification

##### Lossless configured codec and retained wrapper

**Method:** Establish the focused existing baseline; adapt tests/mcp_server/core/test_scope_encoder.py, core/test_phase_detection.py and unit/managers/test_workflow_status_resolver.py. Adapt the real integration/test_workflow_cycle_e2e.py assertions and relevant real GitManager callers from the Research register. Cover phase only, independent cycle, independent subphase, combined values and unknown input using a synthetic admitted vocabulary.

**Expected Result:** Semantic values survive encode/decode; unknown input stays unknown. Wrapper uses an injected decoder; state-only tests remain state-only.

**References:**

- [Codec design](<design.md#shared-scope-codec-and-issue-title-convention>)

##### Deep local history and exact attribution

**Method:** Use one isolated native temporary Git repository at the real history/qualification boundary; include an older qualifying execution commit behind more than five newer commits, merge-reachable evidence, another issue/phase, body-only marker and an exactly attributed undecodable subject. Controlled adapter failures/shallow metadata cover unavailable evidence without live network or workspace mutation. Adapt existing Git adapter/manager tests; add only the uncovered public-behavior gap.

**Expected Result:** Traversal begins at captured HEAD, reaches all parents and retains qualified positive cycles; excluded attribution does not protect; incomplete evidence is explicitly unavailable.

**References:**

- [Evidence design](<design.md#git-execution-evidence-and-protection>)

##### Title normalization and live cutover

**Method:** Adapt existing real GitManager message tests for equal issue markers, other/larger numbers and a multiline body. After focused green/gates, restart_server, health_check and get_work_context; use native git_add_or_commit with cycle_number=1 and verify the resulting subject decodes under the new contract.

**Expected Result:** One canonical matching issue suffix, preserved body and unrelated references; the branch's new execution commits carry an independent cycle.

#### Stop Conditions

- Stop on an unregistered real codec/result consumer and extend the existing inventory before changing it.
- Do not commit Implementation metadata through the old live encoder; stop if the restarted bootstrap/health/context fails.
- If evidence requires a new service, config loader inside values or a network/alternate-history search, stop and reopen the discrepancy.

### C\_2 — Complete planning command and consumer cutover

**Goal:** Replace partial merges with explicit complete-block commands, one complete-result boundary and identical persistent/public references.

**Cycle Number:** 2

**Owner:** @imp implementer

#### Scope In

Frozen input/stored/operation models; ProjectManager commands and narrow evidence injection; planning tool schemas/outputs/shared assembly; phase/discovery/task read consumers; split glob admission; planning enforcement/presentation; direct helpers, operational template projections and this issue's storage-format cutover.

#### Scope Out

No completion register, generic patch/migration service, old-format aliases, query repair or planning-to-state writes. State re-entry composition belongs to C_3.

#### Deliverables

##### D\_2.1

Complete-block planning commands — Write-once creation and five explicit operation variants compose a validated complete result; generated names/references/totals persist and read back; fresh evidence protection/force retry and NoteContext facts follow Design.

**Owner:** @imp implementer

##### D\_2.2

Planning consumers and admission — Tools, outputs, resolver, task/discovery/cycle-name readers, enforcement and presentation consume one stored shape. Only Planning admits public save/update. dir/pattern validation reaches the unchanged checker.

**Owner:** @imp implementer

##### D\_2.3

Fixture and workspace format cutover — Actual helpers/callers and planning-template operational projections use the new contract; remove obsolete partial-merge expectations. Mechanically translate this issue's existing plan without changing its cycles, obligations, order, counts or envelope; restart and verify full readback.

**Owner:** @imp implementer

#### Exit Criteria

Save/update/readback, protection/force, public admission and glob route pass focused behavior tests and applicable gates. All actual stored-model consumers and relevant fixtures use the new shape. This issue's native plan still describes these same three cycles and nine deliverables after its single explicit format adjustment; no compatibility route or state-pointer write was added.

#### Dependencies

- C_1 complete: actual ICycleEvidenceReader provider and shared codec exist.

#### Obligations

- Pure models do no Git/state/config IO. ProjectManager uses required keyword-only ICycleEvidenceReader; commands return None; successful tool output comes from stored-plan query, not a last-result cache.
- All operation targets refer to the original snapshot; duplicate/missing targets reject the complete call. Omission is unchanged; explicit removal only; survivor order then append order.
- Every update, including phase-only/force, attempts fresh evidence. Known positive replacement/deletion/renumbering protection always wins, including under force. Only continued uncertainty can be overridden; accepted override facts appear only after successful persistence.
- Generate C_n, cycle D_n.m and local phase D_n in storage. Names are not lookup keys. Complete resulting-plan validation and configured membership apply to save and update.
- Preserve query purity, existing envelope/metadata and initialized-without-planning readback. Readback failure after a successful write must not claim rollback.
- Retain normal numeric total/cycle consumers while migrating name/id and phases-map readers. Adjust helper construction centrally; do not rewrite all 28 helper-caller files.
- Planning-template context is document authoring, not a second planning-command API. Change only its affected validation-spec/projection fields and actual examples; preserve its authored structure.
- The current running tool schema is the pre-cutover schema: initial native save necessarily supplies total/cycle_number/id. These are bootstrap facts, not retained v3 request fields.

#### Verification

##### Whole-block behavior and shared result validity

**Method:** Adapt unit/managers/test_project_manager.py, unit/tools/test_project_tools.py and integration/test_project_plan_readback.py with compact complete-block fixtures. Exercise initial names/numbering, write-once save, all five operation variants, original-snapshot remove+replace, unrelated preservation and invalid/missing/duplicate/final-empty results. Observe queries and persisted bytes; rejected commands leave the plan unchanged. Do not retain caller-total mismatch, old merge or content/source tests as new evidence.

**Expected Result:** Direct storage and tool readback share generated references/counts; accepted operations are complete and rejected operations have no persistence effect.

**References:**

- [Input/stored contract](<design.md#stored-planning-shared-validation-and-readback>)

##### Protection and force retries

**Method:** Inject a small controllable immutable-evidence fake through the public manager boundary. Cover C_1/C_3 protected with C_2 removal, unworked compaction, rejecting complete-block replacement of a protected cycle with unchanged numbering, both with and without force, default unavailable rejection, force retry that becomes complete/positive, and force with continued uncertainty plus retained positives. Assert per-call attempts and observable outcome/notes, including write failure without successful-override note.

**Expected Result:** Every call retries evidence; positive protection cannot be forced; only uncertainty override is explicitly reported after success.

##### Configured admission and actual glob execution

**Method:** Adapt existing enforcement public-route tests for Planning acceptance/outside rejection using synthetic configured phase policy. Extend existing schema/resolver/checker behavior coverage for one admitted/saved nonempty dir+pattern rule reaching the real gate route. Keep other validation-kind behavior and type-specific field requirements; no YAML text assertion or checker rewrite.

**Expected Result:** Existing configured enforcement blocks public planning writes outside Planning. The sole admitted glob form reaches the unchanged executor.

**References:**

- [Configuration/glob design](<design.md#initialization-configuration-and-glob-admission>)

##### Consumer and template projection parity

**Method:** Adapt shared helpers plus actually affected direct constructors, integration/templates/test_planning_artifact.py operational projection and affected output/discovery/cycle/resolver tests. Inspect remaining imports/field reads against the Research consumer index, distinguishing generic document ids from operational planning refs.

**Expected Result:** No active reader expects the removed partial models/fixed phase fields; no speculative rewrite of passive callers or historical artifacts.

##### Self-hosted clean break

**Method:** Before restart, use safe_edit_file on the existing .pgmcp/deliverables.json as the owner-approved manual workspace format adjustment. Preserve the entire envelope/other issues; translate only #491's nested plan to StoredPlanningModel with the exact IDs/order/descriptions and the explicit names listed in this plan. This is a one-time representation change, not a public planning mutation or a bypass for changing approved deliverables. Do not create a migration tool/fallback or modify state. Restart, health/context and get_project_plan(491); compare the complete result with this document.

**Expected Result:** Three unchanged cycles, seven execution deliverables plus Validation D_1 and Documentation D_1, total three; state/history unchanged and the new server can continue cycle work.

#### Stop Conditions

- If an operation needs nested patches, implicit deletion, another identifier scheme or different force behavior, stop rather than redesign.
- Stop if a new consumer falls outside the registered boundaries or admission would require hardcoded workflow names.
- If this branch's representation-only adjustment changes planning semantics or is not admitted safely, stop; do not force an unapproved planning transition or hide a fallback.

### C\_3 — Explicit phase re-entry and safe initialization

**Goal:** Validate current-plan cycle selection and initialization before writes, then complete configuration and dependency cleanup.

**Cycle Number:** 3

**Owner:** @imp implementer

#### Scope In

Normal/forced phase inputs and outputs, PhaseStateEngine transition composition and existing mutator, IProjectPlanReader narrowing, initialization preflight, zero/one cycle-phase validation, compact Hotfix, targeted phase instructions, passive injections and docstring.

#### Scope Out

No resumetool, plan-revision tracking, completion inference, cross-process transaction framework, open-PR unlock or historical state/commit rewriting.

#### Deliverables

##### D\_3.1

Explicit cycle entry and initialization guard — Normal/forced transitions validate plan, selection and approval before one composed state mutation; first entry C_1 and explicit re-entry reset current/last/subphase as designed. Initialization rejects existing same-branch state before project writes.

**Owner:** @imp implementer

##### D\_3.2

Configured cycle policy and dependency cleanup — Zero/one cycle-based phase, compact non-cycle Hotfix, retained Chore, surgical instructions, existing read-only plan constructor, passive decoder/detector cleanup and corrected subphase-timing docstring complete the approved boundaries.

**Owner:** @imp implementer

#### Exit Criteria

Public normal/forced re-entry, rejection-before-write initialization, configured zero/one phase policy and compact-workflow behavior pass focused tests and applicable gates. Bootstrap and direct helpers use narrow dependencies; passive injections and independent state-writing hooks are gone. Implementation hand-over maps all seven execution deliverables and complete cleanup before independent QA.

#### Dependencies

- C_2 complete: stored plan/readback and configured membership are available.

#### Obligations

- PhaseStateEngine uses existing IProjectPlanReader through the unchanged project_manager keyword; no concrete manager import or write-capable engine dependency.
- Validate target, approval, complete current plan and resume selection before exit effects/history/context reset. Revalidate assumptions in one fresh-state WorkflowStateMutator.apply. Context resets only after success.
- First entry starts C_1; re-entry with prior cycle state requires existing current-plan C_n. Valid entry sets current_cycle selected, last_cycle=None and subphase=None; factual history is preserved. Force skips gates only, not selection/validity.
- Initialization guard runs before ProjectManager persistence and remains on direct initialize_branch. Preserve verified post-PR-close recovery and open-PR enforcement; no cross-file rollback claim.
- Zero/one cycle-based workflow phase is configured, not a hardcoded implementation name. Hotfix loses planning/cycle requirements while useful subphases and proportional evidence remain; Chore stays non-cycle.
- Remove passive injections in bootstrap/test_support and actual direct constructors (including test_consumers_c4.py and test_c260_c2_state_root_injection.py). Retain actual decoder-wrapper behavior; docstring correction does not alter registration/rollback.
- Remove matching issue-marker requirements only from affected current commit examples; keep lifecycle guidance in its existing authoritative locations.

#### Verification

##### Public phase entry/re-entry without premature writes

**Method:** Adapt unit/managers/test_phase_state_engine.py and affected phase/cycle tool tests. Replace obsolete direct entry/exit hook assertions with public normal/forced transitions. Cover first entry, required/missing/stale/valid resume, invalid plan/approval and a removed current cycle selected anew. Observe state bytes/history/context, chosen cycle, last_cycle and subphase. One existing entry fixture supplies only get_project_plan to prove the read-only dependency through behavior.

**Expected Result:** Rejected calls leave state/history/context unchanged; valid explicit re-entry chooses the current-plan cycle and preserves history without completion inference.

**References:**

- [Re-entry design](<design.md#explicit-cycle-re-entry-and-mutation-free-validation>)

##### Initialization and compact workflows

**Method:** Adapt unit/tools/test_initialize_project_tool.py and relevant project/engine tests using isolated storage. Prove same-branch rejection before either file changes, admitted new/other-branch initialization and the verified closed-PR recovery boundary. Adapt config/runtime tests for zero/one/two cycle phases and a synthetic cycle-phase name, plus native compact Hotfix behavior with no planning/cycle prerequisite.

**Expected Result:** No early plan overwrite; configuration controls cycle admission; Hotfix/Chore remain compact without adding Planning.

##### Cleanup and integration

**Method:** Inspect registered passive constructor sites and actually changed helpers; run the affected state/status/consumer/cycle/enforcement tests and the real workflow-cycle E2E. Apply focused file gates, restart and verify health/work context after final runtime/config changes. Review production and test diff for boundaries, no execute-time construction, no compatibility bridge and no unrelated cleanup.

**Expected Result:** One bootstrap dependency direction, no query-time loading or passive injections, and the new operational path works through real internal layers.

#### Stop Conditions

- Stop if a transition rejection changes state/history/context, if force bypasses selection validity, or if planning writes change state.
- Stop if compact Hotfix needs a Planning phase or a Python special case.
- Stop on cross-file transaction claims, new persistent resume/completion fields or helper rewrites without an actual affected call site.

## Phase Deliverables

### Validation

#### D\_1

Validation report — Durable mapping of all execution deliverables/cleanup, exact configured full-suite and required gate outcomes, public behavior evidence and material limitations.

**Owner:** @imp validator

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue491/validation.md"

### Documentation

#### D\_1

Active reference reconciliation — Update the smallest complete project/Git/phase/config/template reference surface to validated behavior and record reviewed-but-unchanged material.

**Owner:** @imp documenter

**Validates:**

**Type:** file_exists

**File:** "docs/reference/tools/project.md"

## Related Documents

- [Approved Design](<design.md>)
- [Research and Approved Strategy](<research.md#approved-strategy>)
- [Architecture contract](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)
- [Documentation standard](<../../coding_standards/DOCUMENTATION_STANDARD.md>)
- [Quality and evidence](<../../coding_standards/QUALITY_GATES.md>)
- [Execution tool reference](<../../reference/tools/quality.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-09 | @imp planner | Sequence approved Design into three coherent cycles, focused behavior evidence, explicit live cutovers and required broad Validation. |
| 1.1 | 2026-10-10 | @imp planner | Apply owner-approved cycle immutability with a narrow existing guard/test adjustment; preserve the three-cycle plan and broad Validation obligations. |
