<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=KoFPQ3-cAAWFeesb -->

# Issue 503 — planning the explicit registration contract cutover

**Status:** PLANNING — INDEPENDENT REVIEW REQUESTED  
**Version:** 0.3  
**Last Updated:** 2026-10-15

## Purpose

Sequence the independently reviewed Design into the smallest coherent implementation cycle with focused behavior evidence, explicit runtime activation and bounded cleanup.

## Scope In

Design v0.1 contracts, approved source-preservation repair, direct production/fixture/instruction consumers, and deliberate active-branch schema cutover.

## Scope Out

Compatibility bridges, migration services, new architecture, broad test/warning cleanup, workflow redesign, full-suite execution in Implementation, packaging and releases.

## Prerequisites

- Research strategy and scope are owner-approved.
- Independent Design → Planning GO on 17a943cb2edca1696645db0e2336ac3f6ca3081a; no P0/P1/P2 blockers.
- Planning phase is active; the initial structured plan has been saved once and read back.

## Summary

C_1's coherent registration cutover and its four deliverables are preserved exactly. After its complete Validation run exposed concrete failures, the owner approved one bounded C_2 with two deliverables. Renewed Validation owns one complete configured suite and branch/configured gates; Documentation reconciles active references. No hypothetical cleanup cycle or new architecture is introduced. This plan is not implementation evidence or QA approval.

## Dependencies

- C_1 starts only after independent Planning → Implementation GO; first implementation entry selects C_1 automatically.
- Within C_1: adapt narrow preservation behavior → coherent source/API and consumer migration → focused evidence/cleanup checkpoint → single live schema activation → new-runtime evidence and activation commit.
- Do not divide C_1 into separately activated partial APIs. C_2 is allocated only for the concrete, owner-approved Validation repair below.

## Risks

### Source configuration proves feasibility but not a successful future live cutover.

Record configured connection basis now and require restarted context/health/schema/plan evidence during C_1; never infer success from a restart request.

### Full-suite warning volume is mistaken for current new regressions.

Keep historical #319 categories separate, record actual Validation results and limit repairs to approved behavior or required blockers.

## Milestones

- C_1 coherent contract and live cutover completed under the approved exit criteria.
- Validation full native suite, branch gates and production-scoped configured Mypy complete.
- Documentation/Ready follow independent phase reviews; no release is authorized.

## Work Units

### C\_1 — Explicit registration and non-mutating lifecycle contract cutover

**Goal:** Deliver the approved clean break as one reversible source/data cutover with direct behavior proof and no implicit quarantine.

**Cycle Number:** 1

**Owner:** @imp implementer

#### Scope In

Production: state_repository.py, state_version_validator.py, phase_state_engine.py, workflow_state_mutator.py, project_manager.py, git_manager.py, branch_parent_reader.py, GitHub manager/adapter, project_tools.py, pr_tools.py, tool_outputs.py, interfaces/state.py and workflow.py, bootstrap.py and git_config.py. Config: git.yaml default removal and seven Ready examples in contracts.yaml. Consumers: the refreshed Research inventory, direct kwargs, raw payloads, one possible test_support preparation helper and directly affected weak tests.

#### Scope Out

General reader tightening, new state/PR service, new transaction/repair code, nested-state collection redesign, unrelated auth/resource/restart warning repairs and new test files solely for old-behavior rejection.

#### Deliverables

##### D\_1.1 — Validated registration and one state mutation boundary

Implement explicit parent propagation, complete fresh state initialization, validated stable-identity updates, one injected mutator/lock, single-slot repository parity and branch-state schema 2.0.0, with focused existing public behavior evidence.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/managers/state_repository.py"

##### D\_1.2 — State-authorized PR targets and scoped branch readers

Use matching read-only registration for submit_pr head/base before lifecycle writes; require lower create_pr base; retain Ready/check-scope behavior and remove exhausted default-base authority.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/tools/pr_tools.py"

##### D\_1.3 — Source-preserving validation and exhausted backup cleanup

Remove automatic quarantine at the three agreed sites; preserve source, prior backup, diagnostic causes, successful planning writes and persisted readback facts; adapt existing behavior matrices and delete the unused backup command only after consumer closure.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/managers/state_version_validator.py"

##### D\_1.4 — Bounded consumer migration and verified active-runtime cutover

Migrate affected code/fixtures/raw requests/Ready examples with at most one explicit setup helper, retire directly touched weak tests/ignored constructor argument, pass focused gates, and activate state 2.0.0 with identity/audit preservation and new-runtime context/health evidence.

**Owner:** @imp implementer

**Validates:**

**Type:** key_path

**File:** ".pgmcp/state.json"

**Path:** "schema_version"

#### Exit Criteria

All four deliverables satisfy Design v0.1; meaningful source-preservation RED is confirmed before implementation, remaining structural coverage is reused; relevant focused test families and type-specific gates pass without known in-scope failures; no retired production authority remains; the active new runtime reads state2.0.0 with preserved identity/audit and the stored plan remains readable. No full suite, broad warning repair, release, compatibility bridge or phase progression without independent review.

#### Dependencies

- Independent Planning → Implementation GO.

#### Obligations

- Honor Design responsibilities/signatures and the existing read-only/mutation boundaries; models have no file/Git IO.
- Explicit positive issue/attached branch/parent admission precedes deterministic metadata refusal. Complete initialization and ordinary mutation share one lock, without cross-file/cross-process claims.
- Remove reflog/metadata/default-base authorities, placeholder fallback, unchecked copies, ignored constructor parameter and exhausted backup command only with consumer closure.
- Preserve source and previous backup on failed validation; expose errors consistently on repeated direct/indirect reads; preserve successful planning writes and persisted=True readback failure.
- Keep contract tests direct. Consolidate only affected incidental setup with explicit parent; keep meaningful freshness doubles and remove obsolete inference/cascade/source-string tests where directly touched.
- Keep only branch-state fixtures at 2.0.0; unrelated config, planning and generic-validator 1.0.0 fixtures remain 1.0.0.
- Update Ready/agent signature consumers mechanically in C_1; Documentation owns final explanatory parity, not another implementation rewrite.
- Validate D_1.1–D_1.4 by behavior evidence and real cutover observations, not by treating presence/key-path descriptors as proof.

#### Verification

##### Durable uncovered source-preservation behavior

**Method:** Adapt the existing repository corrupt-file case and existing six planning-command cases to positive source/prior-backup preservation. Rename them descriptively, select only their actual node IDs and confirm intended RED with run_tests(scope='targets', tests=['python_tests'], timeout_seconds=300). Commit sub_phase='red'. No artificial RED for fixture/config/DI migration already adequately covered.

**Expected Result:** Only the intended invalid-source preservation assertions fail; collection/import/setup errors are repaired before calling it RED.

##### Core registration, mutation and consumer behavior

**Method:** Run the exact A/B/C focused groups below as relevant changes land, timeout_seconds=600; retain fresh passing results and rerun only invalidated groups. Commit coherent GREEN; complete structural cleanup and file gates before the code activation checkpoint.

**Expected Result:** Current registration/identity/absence/handover/failure-before-effects and preserved submission/planning behavior pass without old compatibility expectations.

##### Production/test/document file gates

**Method:** Use actual changed existing filenames selected from MCP git status/diff and native repository search. Python format/lint/Pyright target only changed .py/.pyi production and test files; Mypy targets production only. Markdown and YAML use their own checks as specified below.

**Expected Result:** No Markdown/JSON/YAML forwarded to Python checks, no required strict test-Mypy gate, no native-policy weakening.

##### Live activation and reversibility

**Method:** Follow the explicit old-runtime generic edit → restart → new-runtime context/health/readback sequence below. Compare parsed identity/audit and backup facts before normal new-runtime commits.

**Expected Result:** State2.0.0 is accepted by the restarted runtime with every other state field preserved, plan intact and no old engine mutation after the cutover.

#### Risks

##### Mixed source/runtime/schema can lock ordinary MCP mutations.

One activation only after coherent code/focused gates, with a last old-runtime generic edit, immediate restart and explicit reverse ordering.

##### Mechanical signature/data migration dominates test maintenance.

Use the refreshed consumer inventory and narrow explicit helper; avoid broad parametrization, new files or new production defaults.

#### Stop Conditions

- A target contract contradicts Approved Strategy/Design, requires another architecture or changes unrelated supported behavior.
- A baseline/RED fails because of unrelated imports, collection, configuration or network lookup; diagnose rather than expanding production catch/fallback behavior.
- A required focused gate remains failed, current source consumers remain or error diagnosis is discarded.
- The schema preimage/session/source launch differs from the documented cutover basis, client metadata stays stale or identity/audit/backup evidence differs.
- Any additional scope or plan change requires Planning and whole-block mutation; do not bypass committed-cycle protection or auto-add cleanup cycles.

### C_2 — Bounded validation-consumer and phase-diagnostic repair

**Owner:** @imp implementer. **Dependency:** completed C_1 implementation, observed Validation FAIL in commit 0e0baac, and the owner's explicit bounded-repair approval. C_1 and all phase blocks remain unchanged.

#### Scope and exclusions

| Surface | Bounded action |
| --- | --- |
| tests/mcp_server/unit/managers/test_workflow_status_resolver.py | Retire the duplicate branch-keyed absence expectation; retain the existing exact-branch wrapper mismatch evidence. |
| tests/mcp_server/unit/tools/test_extra_forbid.py | Correct only the current SubmitPR valid-input fixture; keep generic extra-forbid behavior coverage. |
| tests/mcp_server/tools/test_c4_description_invariants.py | Remove the obsolete base-cascade content test and exhausted import; add no replacement text assertion. |
| mcp_server/tools/phase_tools.py | Remove PlanningMutationError from the two combined catches and its exhausted import; retain PhaseEntryError handling and current outer wrapper/presenter ownership. |
| tests/mcp_server/unit/tools/test_transition_phase_tool.py | One focused normal/forced public wrapper behavior matrix for domain diagnosis, reusing current tool/wrapper seams. |

No other production change, exception framework, error alias/fallback, presenter/config mutation, compatibility or new test file. Other warning categories remain excluded.

#### Deliverables

##### D_2.1 — Complete remaining test consumer migration

Remove the duplicate branch-keyed resolver expectation in favor of existing exact-branch coverage, correct the generic SubmitPR valid-input fixture and retire the obsolete base-cascade content test; add no replacement content or legacy-rejection tests.

**Validates:** type=file_exists, file=tests/mcp_server/unit/tools/test_extra_forbid.py. Presence is navigation, not behavioral proof.

##### D_2.2 — Preserve planning-domain diagnosis through existing wrappers

Remove PlanningMutationError from the two phase-tool catches and its exhausted import, retain PhaseEntryError handling, and prove normal/forced public wrapped calls preserve the original domain code, parameters and traceback using one focused behavior matrix in an existing test file.

**Validates:** type=file_exists, file=mcp_server/tools/phase_tools.py. Presence is navigation, not behavioral proof.

#### Exit Criteria

The three reported test-consumer failures are resolved under the current contract, normal and forced planning-domain errors reach the existing exception wrapper with original diagnostic facts, focused affected tests and type-specific gates pass, no new error architecture or compatibility path is introduced, and committed C_1 plus phase deliverables remain unchanged. Full configured suite and branch/configured gates are rerun only in renewed Validation after independent review.

#### Sequence and focused evidence

1. Re-enter Implementation with resume_cycle="C_2" from the current public readback only after independent Planning GO.
2. Add/adapt the single public wrapped normal/forced characterization in the existing phase-tool test file. Select only its actual node IDs through file targets plus -k; run_tests(scope="targets", tests=["python_tests"], timeout_seconds=300). Confirm RED is the lost original PlanningMutationError code/parameters/type/traceback, not collection, schema or setup failure; commit cycle2/sub_phase="red". The three already observed test-consumer failures need no artificial second RED.
3. Apply the two catch deletions and bounded fixture/test cleanup. Run the focused existing families below with native defaults; retire only redundant/obsolete assertions identified above. Commit cycle2/sub_phase="green"; refactor commit only if further actual cleanup occurs.
4. Use the unchanged type-specific file gates: formatter/lint/Pyright on actual changed Python files, Mypy on phase_tools.py only; preserve policy/native arguments. Configured production Mypy remains mandatory in renewed Validation.
5. Restart the source server after coherent source/test commit; call get_work_context first, then health_check and get_project_plan(503), confirming Implementation/C_2 and both stored cycles. No schema edit, package build, tool-schema change or repeated state cutover.
6. Request independent Implementation → Validation review. On GO, transition normally to Validation; rerun one complete configured native suite (1200s), branch checks (600s) and configured production Mypy (600s). The earlier failed suite is invalidated by these real repairs; retain both observations in Validation v0.2 rather than replacing history.

```text
run_tests(scope="targets", targets=["tests/mcp_server/unit/managers/test_workflow_status_resolver.py","tests/mcp_server/unit/tools/test_extra_forbid.py","tests/mcp_server/tools/test_c4_description_invariants.py","tests/mcp_server/unit/tools/test_transition_phase_tool.py","tests/mcp_server/unit/tools/test_force_phase_transition_tool.py"], tests=["python_tests"], timeout_seconds=600)
```

#### Preservation, rollback and stops

The existing wrapper must receive the original domain exception and retain code, error_params and traceback. Separate PhaseEntryError outcomes and successful normal/forced transitions remain covered by existing tests. No policy text, exception attribute extraction or diagnosis mapping is added in the tools. Net test coverage stays focused: two obsolete/duplicate cases retire; the one behavior matrix covers both affected routes.

The new Planning commit is the C_2 source anchor. Restore only the five named source/test paths if rollback is necessary; do not reset state2, committed C_1, the plan or its phase audit. Stop for any new boundary/strategy need, non-diagnostic RED, unrelated required-gate failure, changed C_1/phase block, or wrapper behavior that would require a new architecture. Do not weaken gates or silently accept the existing Mypy bug.

## Phase Deliverables

### Validation

#### D\_1 — Complete configured validation and preservation report

Record final native-configured full suite, branch gates, configured production Mypy, deliverable/cleanup mapping, active-cutover evidence, warnings and truthful limitations in one durable report.

**Owner:** @imp validator

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue503/validation.md"

### Documentation

#### D\_1 — Current registration and PR references

Reconcile project/GitHub/Git references and setup/upgrade guidance with explicit registration, source-preserving errors, state envelope2.0.0 and removed target defaults.

**Owner:** @imp documenter

**Validates:**

**Type:** file_exists

**File:** "docs/reference/tools/project.md"

#### D\_2 — Existing instruction and unreleased-note parity

Update existing AGENTS source/tracked bundled copies and seven Ready examples proportionately; preserve role split and document current changes without a release/version promise.

**Owner:** @imp documenter

**Validates:**

**Type:** file_exists

**File:** "AGENTS.md"

## Evidence schedule and exact scopes

### Focused existing test groups

These groups are execution targets, not new tests. Select only the group invalidated by a change; do not repeat all groups after each edit. Narrow the initial RED to the actual adapted preservation node IDs after inspecting their current names.

Group A:
```text
run_tests(scope="targets", targets=["tests/mcp_server/unit/managers/test_state_repository.py","tests/mcp_server/unit/managers/test_workflow_state_mutator.py","tests/mcp_server/unit/managers/test_phase_state_engine.py","tests/mcp_server/unit/managers/test_phase_state_engine_parent_branch.py","tests/mcp_server/unit/managers/test_project_manager.py","tests/mcp_server/unit/tools/test_project_tools.py","tests/mcp_server/unit/tools/test_initialize_project_tool.py"], tests=["python_tests"], timeout_seconds=600)
```

Group B:
```text
run_tests(scope="targets", targets=["tests/mcp_server/unit/tools/test_submit_pr_tool.py","tests/mcp_server/integration/test_submit_pr_atomic_flow.py","tests/mcp_server/unit/managers/test_branch_parent_reader.py","tests/mcp_server/unit/execution/test_check_selection.py"], tests=["python_tests"], timeout_seconds=600)
```

Group C:
```text
run_tests(scope="targets", targets=["tests/mcp_server/integration/test_context_loaded_enforcement.py","tests/mcp_server/integration/test_project_plan_readback.py","tests/mcp_server/unit/test_server.py","tests/mcp_server/config/test_git_config.py","tests/mcp_server/unit/managers/test_github_manager.py","tests/mcp_server/unit/tools/test_git_tools.py"], tests=["python_tests"], timeout_seconds=600)
```

### Type-specific file gates

Obtain actual changed paths from MCP Git status/diff and repository search. Let P be changed existing production .py/.pyi files, T changed existing test .py/.pyi files, M changed Markdown files and Y changed YAML files. Exclude deleted paths. Execute only nonempty target sets; expand these symbols to explicit filenames in actual calls.

```text
run_checks(scope="targets", targets=P+T, checks=["python_format","python_lint","python_pyright"], timeout_seconds=600)
run_checks(scope="targets", targets=P, checks=["python_types"], timeout_seconds=600)
run_checks(scope="targets", targets=M, checks=["markdown_links"], timeout_seconds=120)
run_checks(scope="targets", targets=Y, checks=["yaml_configuration"], timeout_seconds=120)
```

Preserve native arguments and configuration. Do not forward documents or workflow JSON to Python checks, or impose production Mypy policy on tests.

### Validation-owned final verification

After independent Implementation → Validation GO, use one complete configured test invocation with the existing native selection, workers and coverage. The configured client window is 1800 seconds; do not split the suite to fit a shorter call.

```text
run_tests(scope="configured", timeout_seconds=1200)
run_checks(scope="branch", timeout_seconds=600)
run_checks(scope="configured", checks=["python_types"], timeout_seconds=600)
```

The current default branch review uses check-specific configured preselection; the separate configured Mypy run covers production scope. Retain fresh file-level document/YAML evidence and rerun it only after relevant edits. Record failed/incomplete outcomes honestly, with causes and any necessary explicit decision. No unrelated warning cleanup or repeated full suite without invalidating evidence.

## Runtime activation and rollback

### Controlled live-state activation

This order addresses QA's specific Planning attention point. It uses existing tools and adds no migration script.

1. Keep live state at 1.0.0 and the existing process running while implementing source targeting 2.0.0. Do not restart during partial source/config migration. Run focused tests in their isolated roots against the new source. Finish consumer migration and the focused file gates, then commit the coherent code/config/test checkpoint with git_add_or_commit(workflow_phase="implementation", cycle_number=1, sub_phase="refactor", ...). Use the last appropriate green checkpoint instead if no separate refactor change exists.
2. Confirm the actual connection uses this workspace-source launch basis and that no unintended edits are pending. Load get_work_context while the old envelope is still valid. Read the state artifact for the explicit schema/identity comparison after the last old-runtime state-writing operation; capture its parsed fields and any existing backup for comparison without publishing a giant snapshot.
3. Make the **last old-runtime state-related write** with safe_edit_file(path=".pgmcp/state.json", operation={"op":"replace","target_content":"\"schema_version\": \"1.0.0\"","replacement":"\"schema_version\": \"2.0.0\""}, validation="report"). Match the actual unique root-field spelling; if the preimage differs, inspect and stop instead of broad replacement. Require written=True. Report mode honestly permits the unprofiled generic JSON edit; it is not a schema-validation claim.
4. Immediately call restart_server(reason="Activate issue #503 registration contract and branch-state 2.0.0"). Between the version edit and restart, do not call old-runtime context, state, phase, commit/push or other branch-mutating tools. Read-only native file inspection is available if a write result is ambiguous; do not guess which envelope is present.
5. After the proxy starts a new session, call get_work_context first. Confirm issue #503, exact branch, implementation/C_1 and parent main; health_check must be healthy and identify the restarted process. Read the artifact for the explicit comparison: schema_version is 2.0.0, every other field equals the step 2 snapshot, and the previous backup is untouched. get_project_plan(503) must still return the saved C_1 and phase blocks.
6. Confirm client tool metadata for changed public calls is refreshed before using those calls. If stale, use the normal client refresh and reload context; do not send obsolete fields or add a compatibility route. Only then commit the schema-only activation/audit using the new runtime and push normal completed work.

Source feasibility: .codex/config.toml selects .venv Python, proxy module, cwd and PYTHONPATH at C:/temp/pgmcp; proxy launch_server starts the same interpreter with -m mcp_server. The installed dist-info records a wheel, not an editable install; source precedence comes from cwd/PYTHONPATH, while installed metadata supplies package version 3.0.0. No wheel build/install or installation.json change is required by this cutover. The configured 1800-second client window is present.

safe_edit's branch-mutating enforcement runs before the edit, when state 1.0.0 is valid; the current YAML has no post rule. The guarded writer returns without a workflow-state reload. restart_server is not in that category and reads no workflow state, so it remains callable immediately after the envelope changes. Bootstrap constructs the repository without reading workflow state. These are source/config feasibility facts, not proof of a future live activation; step 5 is mandatory runtime evidence.

### Failure and reversal

Stop on an unexpected preimage, ambiguous write, wrong connection/session, invalid context, client metadata that cannot refresh, identity/audit difference or backup mutation. Do not reset/reinitialize planning or invoke force to make the cutover appear successful.

The pre-cycle source commit and pre-activation code checkpoint are recovery anchors. Before activation, restore only cycle-owned source/config/test paths to a recorded anchor if needed; live state remains 1.0.0. After activation, reverse the pair deliberately: while the new runtime still reads 2.0.0, restore coherent old source/config paths first; make the final generic schema-only2→1 edit; immediately restart old code, verify context/identity and resume only afterward. Never expose an old state engine to 2.0.0 or a new state engine to 1.0.0 for ordinary mutations. If the process is unavailable or the envelope is uncertain, report the actual source/data pair and use deliberate existing-tool/operator recovery; no blind branch reset, automatic migration or fictional rollback guarantee.

## Stored planning readback

Initial Planning v0.1–v0.2: save_planning_deliverables(503) saved one C_1 with D_1.1–D_1.4, plus Validation D_1 and Documentation D_1/D_2. get_project_plan(503) returned the same complete blocks: authored names, descriptions, validation descriptors and exit criteria were compared exactly. This document's work-unit and phase descriptions were rendered from that readback. Server-generated IDs are references within their cycle/phase; the two phase-local D_1 references are distinguished by phase.

Current repair readback: update_planning_deliverables(503, operations=[append_cycle]) returned C_2/D_2.1/D_2.2. Complete get_project_plan(503) confirmed total2, the exact C_2 fields and byte-for-byte-equal serialized C_1/phase model blocks. The append's informational note reported a presentation formatting error; operation/readback persistence succeeded. That note-formatting issue is recorded for later triage, not repaired by this cycle.

The file_exists/key_path descriptors support navigation and bounded presence checks only. The behavior evidence, cleanup inspection, cutover comparison and independent review establish the actual obligations. No production behavior or future gate outcome is claimed by saving this plan.

## Planning verification

All 17 existing test targets above were checked for existence. run_checks(scope="targets", targets=["docs/development/issue503/planning.md"], checks=["markdown_links"], timeout_seconds=120) reported passed with configured arguments; subsequent final edits also passed safe_edit_file's Markdown link validation. A bounded producer-delegated findings-only review reported no concrete cutover/reversal/evidence-schedule blockers; it grants no workflow authority. No tests, Python checks, production changes or live schema activation were performed in Planning.

## Related Documents

- [Approved Design](<design.md>)
- [Research / strategy / consumer inventory](<research.md>)
- [Architecture Principles](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)
- [Quality Gates](<../../coding_standards/QUALITY_GATES.md>)
- [Typing Playbook](<../../coding_standards/TYPE_CHECKING_PLAYBOOK.md>)
- [Client execution budgets](<../../setup/README.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-15 | @imp planner | Define one coherent cycle, exact focused evidence groups, native gate scopes and reviewed live-schema activation/reversal order; mirror saved C\_1 and phase references. |
| 0.2 | 2026-10-15 | @imp planner | Correct the Validation path and restore literal C_1 exit-criteria parity after independent Planning review; no stored plan or execution scope change. |
| 0.3 | 2026-10-15 | @imp planner | Append owner-approved C_2 after complete Validation failures; preserve C_1/phase blocks, bound wrapper repair and test cleanup, and require independent review plus renewed configured evidence. |
