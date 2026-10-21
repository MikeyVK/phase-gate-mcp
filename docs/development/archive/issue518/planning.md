<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=WI5iXHBKVOU91bYE -->

# Issue \#518 — bounded source-owner repair cycles

**Status:** Planning complete — independent review requested  
**Version:** 1.1  
**Last Updated:** 2026-10-20

## Purpose

Execute approved Design by existing source responsibility without broad test rewrites or hidden gate changes.

## Scope In

C_1–C_4 / D_1.1–D_4.2 and Validation/Documentation deliverables below, matching get_project_plan(518).

## Scope Out

All approved Research/Design exclusions, especially migration, unchecked casts/new broad suppressions/frameworks, whole-test type gates, four default-none policies, #533 gate changes, Windows readiness and release/deployment.

## Summary

Four structural cycles: model-only/precise source contracts; meaningful logging behavior repair; raw-boundary typing plus production signal restoration; precise helper/local/native policy cleanup and final activation. Existing green preservation baselines replace artificial RED for mechanical changes; logging’s uncovered behavior requires genuine RED. Independent QA is requested at phase boundaries, not every internal cycle.

## Dependencies

- Accepted #517 and current main after #530; Research40d4683b and Design7322093e GOs with inherited #513 owner strategy.
- Existing configured native check/test bindings and package prerequisites; no floating upgrades or harness settings changes.

## Risks

### Current restored-policy diagnoses can differ from historical \#513 counts and reveal an unsupported strategy assumption.

Keep observed native diagnostics, classify per source boundary and stop for an actual supported-contract/scope conflict; no count quota or silent gate waiver.

### Repeated broad quality/test calls create overhead and obscure negative evidence.

One specified discovery scan per globally changed native policy, then exact affected targets; Validation owns one full suite and branch gates; reuse fresh evidence.

## Milestones

- Common cycle gates use exact changed-file targets by type. Production gets format/lint/Pyright/Mypy; test/helper Python gets format/lint. Existing branch production filters remain intact. Broader explicit test-type diagnostics never become a new mandatory whole-test gate.
- Global native policy edits justify one diagnostic production-Pyright scan in C_3 and one Ruff/RUF100 scan in C_4; initial failed findings remain negative evidence and subsequent repair is targeted. These are not full-suite or branch acceptance runs.
- Validation: run_tests(scope='configured',tests=['python_tests'],timeout_seconds=1800), one complete native suite with no args override, preserving native parallelism and configured coverage activation. No borrowed extra #517 coveragegate or new threshold.
- Validation: run_checks(scope='branch',checks=['python_format','python_lint','python_pyright','markdown_links'],timeout_seconds=600), plus run_checks(scope='configured',checks=['python_format','python_lint','python_types','python_pyright'],timeout_seconds=600). Reuse fresh exact evidence until invalidated. Do not send pyrightconfig.json or pyproject.toml to Python file checks; native parser/checker execution validates their actual usage. No YAML/schema inputs change by this plan.
- Validation report records exact calls/outcomes, positive/negative controls, actual complete suppression-family disposition/rationale/trigger, preservation mapping, safe isolated reproduction, failures/timeouts and residual/deferred work. Check post-suite planning/worktree for unexpected writes.
- Documentation updates only current type-checking and server logging references as necessary, inventories active consumers and runs only invalidated link/parity checks; preserve historical #513 research.
- Ready reuses valid evidence, inspects clean intended diff, scaffolds/submits/attaches concrete PR, requests independent final exact-head/base review and hands end-issue to Co. Imp does not merge or start another issue.

## Work Units

### C\_1 — Cut over model-only core contracts and narrow stored facts

**Goal:** Cut over model-only core contracts and narrow stored facts

**Cycle Number:** 1

**Owner:** @imp implementer

#### Scope In

ICoreTool/ITool/prepared input and three forwarding decorators; concrete tool args_model optional-return annotations; direct core/double/None consumers; four Literal exception attributes; bootstrap generic binding/schema callback/Git selected HEAD source seams.

#### Scope Out

All Research/Design exclusions; no policy/architecture drift, compatibility bridge, unrelated suite/gate/lifecycle/release work.

#### Deliverables

##### D\_1.1

Make core/outer/prepared input contracts model-only, preserve variance, forward each existing concrete model, and migrate direct None-based doubles/calls to typed-empty admission without compatibility. Preserve schema/model identity and rejection attachments. Explicitly migrate AttachedCore and ProjectionCore to typed-empty inputs and verify their existing real SDK transport/presentation files alongside all discovered direct consumers.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/core/decorators/input_validation_decorator.py"

##### D\_1.2

Annotate the four stored reason/stage exception contracts, supply existing generic-binding/schema-callback types and use the already-resolved HEAD hexsha. Preserve public values, causes, bytes and selected Git snapshot.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/core/interfaces/file_writer.py"

#### Exit Criteria

Focused existing green baseline and corrected tests include AttachedCore/ProjectionCore real SDK transport/presentation plus the actual direct model-only consumers; changed-file gates pass. No artificial RED for declaration cleanup; typed-empty/model/attachment and Literal/Git snapshot invariants hold; no None bridge, variance change or new business policy.

#### Dependencies

- Research40d4683b and Design7322093e independent GOs

#### Obligations

- Establish the selected existing green baseline before code. Annotation/call-site cleanup uses no artificial RED; replace old None-route expectations with valuable typed-empty/model/admission behavior, not tests that merely reject legacy usage.
- Update complete direct source/consumer boundaries together; retain generic variance and the optional prepared-contract injection seam. Concrete empty models keep extra=forbid.
- Use actual resolved commit.hexsha, never later HEAD. Literal storage does not change values, cause chains, housekeeping or public output. No new marker/logging behavior in this cycle.

#### Verification

##### Existing green preservation baseline and corrected core/Literal/Git behavior

**Method:** run_tests(scope='targets', targets=["tests/mcp_server/unit/decorators/test_pipeline_decorators.py","tests/mcp_server/integration/test_prepared_tool_contract.py","tests/mcp_server/unit/core/interfaces/test_interface_imports.py","tests/mcp_server/unit/utils/test_atomic_file_writer.py","tests/mcp_server/unit/execution/test_check_selection.py","tests/mcp_server/unit/adapters/test_git_adapter.py","tests/mcp_server/unit/server/test_bootstrap.py","tests/mcp_server/integration/test_edit_operation_v3.py","tests/mcp_server/integration/test_scaffold_operation_v3.py","tests/mcp_server/unit/test_server.py","tests/mcp_server/integration/test_tool_attachment_transport.py","tests/mcp_server/integration/test_execution_presentation_v3.py","tests/mcp_server/integration/test_pipeline_e2e.py","tests/mcp_server/unit/server/test_validate_tool_arguments.py","tests/mcp_server/unit/tools/test_git_fetch_tool_behavior.py","tests/mcp_server/unit/tools/test_git_pull_tool_behavior.py"], tests=['python_tests'], timeout_seconds=600), native defaults/no args override

**Expected Result:** All selected existing cases pass before structural work; after migration the valuable replacement typed-empty/admission and existing failure/snapshot cases pass. Record any baseline defect; do not manufacture RED.

##### Changed-file quality and later non-masked source contracts

**Method:** Before each cycle GREEN/refactor commit: run_checks(scope='targets', targets=<actual changed production Python files for that cycle>, checks=['python_format','python_lint','python_pyright','python_types'], timeout_seconds=600). For actual changed test/helper Python files run the same target selection with checks=['python_format','python_lint'] only. Record the concrete target arrays/outcomes in cycle evidence. These explicit sets are type-appropriate; never pass docs/JSON/TOML to Python checks. No whole-test Mypy/Pyright gate is introduced. Model-only/Literal/variance controls are completed once final restored signals are available in C_3.

**Expected Result:** Actual changed production gates and changed-test format/lint pass; source does not retain a None bridge or lose precise stored facts.

#### Stop Conditions

- New/contradictory owner policy, changed supported runtime/schema/protocol/config/admission behavior, unchecked cast, lost guard/variance/primary diagnostic, new broad suppression/framework or unrelated repair is required: stop and expose the concrete conflict.
- A required passing check/test fails or is incomplete: retain its exact status and diagnose causally; do not relabel it, alter scope after failure, weaken a threshold or repeat broad runs until green.
- A planned structural slice is impossible: stop and use a documented earlier-phase repair under the owner’s standing18Oct approval plus independent QA; no silent plan edits, forced forward transition or gate exception.

### C\_2 — Preserve primary logging events with typed payload admission

**Goal:** Preserve primary logging events with typed payload admission

**Cycle Number:** 2

**Owner:** @imp implementer

#### Scope In

Existing core/logging.py plus the nine indexed producer modules; existing logging/admin restart/process-cleanup tests. Keep marker/result/signaling schemas, business admission and logging handler ownership.

#### Scope Out

All Research/Design exclusions; no policy/architecture drift, compatibility bridge, unrelated suite/gate/lifecycle/release work.

#### Deliverables

##### D\_2.1

Adapt existing logging tests to expose missing malformed/collision guarantees with meaningful RED, then implement the approved small typed carrier and standard strict per-property JSON admission in the existing formatter. Preserve base metadata/traceback, valid flat siblings, safe diagnosis and valid reserved values; no custom recursive framework. Complete producer positive/negative controls within C_2 using strict native Mypy and explicitly enabled relevant Pyright rules in temporary control files; C_3 later repeats applicable controls under restored native Pyright defaults.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/core/logging.py"

##### D\_2.2

Migrate the current nine producer modules to known typed props, retain per-event ISO time as event_timestamp, and ensure cleanup directory/cause are emitted. Preserve restart marker/result/timestamps/event identities/exit42 and handler ownership; no new marker business schema.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/tools/admin_tools.py"

#### Exit Criteria

Meaningful logging RED recorded before repair; focused formatter/restart/cleanup behavior passes, including raw extra bypass, invalid roots/nested data/keys/nonfinite/cycles, collisions, primary trace and sibling/context/time preservation. Before C_2 exit, strict native Mypy and temporary-file-enabled Pyright producer controls prove clean positives and intended negatives; source gates pass. Natural-policy Pyright replay is explicitly C_3 evidence, not a prerequisite silently deferred from C_2.

#### Dependencies

- C_1 completed with its objective focused evidence

#### Obligations

- Adapt the existing formatter test file first, run only the new behavior cases and confirm the intended malformed/collision preservation failure before committing cycle2/red. No new test module or content snapshots.
- Use one existing logging owner + standard strict JsonValue validate_python, not custom recursive admission. Raw Logger.extra bypass has the same runtime protection; preserve valid siblings and emit only safe loc/type facts.
- Typed carriers must not leave known producer fields behind unchecked Any. Preserve event_timestamp as the same per-event ISO fact and really emit process cleanup context. Do not add marker business schema or change lifecycle semantics to satisfy typing.

#### Verification

##### Meaningful logging RED

**Method:** run_tests(scope='targets', targets=['tests/mcp_server/unit/core/test_logging.py'], tests=['python_tests'], args={'python_tests':['-n','0','-k','payload or metadata']}, timeout_seconds=180). Name the new relevant cases accordingly; record exact selected failures, then cycle2/red commit.

**Expected Result:** Failure proves absent required primary-event/valid-sibling/collision/malformed-data behavior in the existing formatter, not a setup error or exact prose mismatch.

##### Corrected formatter/audit/process behavior

**Method:** run_tests(scope='targets', targets=["tests/mcp_server/unit/core/test_logging.py","tests/mcp_server/tools/test_admin_tools.py"], tests=['python_tests'], timeout_seconds=600), native defaults/no args override; run_tests(scope='targets', targets=['tests/mcp_server/integration/execution/test_process_runtime.py'], tests=['python_tests'], args={'python_tests':['-k','cleanup']}, timeout_seconds=600). Before each cycle GREEN/refactor commit: run_checks(scope='targets', targets=<actual changed production Python files for that cycle>, checks=['python_format','python_lint','python_pyright','python_types'], timeout_seconds=600). For actual changed test/helper Python files run the same target selection with checks=['python_format','python_lint'] only. Record the concrete target arrays/outcomes in cycle evidence. These explicit sets are type-appropriate; never pass docs/JSON/TOML to Python checks. No whole-test Mypy/Pyright gate is introduced.

**Expected Result:** All chosen cases pass; actual emitted JSON retains primary fields/trace/time/process context, marker/three-event/exit42 and handler ownership. Standard validator rejects invalid nested objects/keys/nonfinite/cycles explicitly.

##### Producer type sensitivity within C_2

**Method:** run_checks(scope='targets', targets=<named temporary control files below .pgmcp/temp/issue518>, checks=['python_types','python_pyright'], args={'python_types':['--show-error-codes'],'python_pyright':['--outputjson']}, timeout_seconds=180). Use actual logging_extra declarations and valid/null-property versus invalid None-root/non-JSON producer calls. Native Mypy already has strict argument/call checking without production disables. At the top of these temporary Pyright control files explicitly enable reportArgumentType, reportCallIssue, reportAttributeAccessIssue, reportUnknownArgumentType, reportUnknownVariableType and reportUnknownMemberType; no disabling directives. These are already-approved diagnostic signals, not a production policy change or one of the four default-none rules.

**Expected Result:** Before C_2 can exit, positive producer cases have zero relevant diagnoses and negative calls produce the intended argument/type codes in both checkers. Native negative exit1 is intentional diagnostic sensitivity, not a passing gate. C_3 removes those temporary enabling headers and repeats applicable producer controls under the actually restored native Pyright policy; C_4 does not own this prerequisite.

#### Stop Conditions

- New/contradictory owner policy, changed supported runtime/schema/protocol/config/admission behavior, unchecked cast, lost guard/variance/primary diagnostic, new broad suppression/framework or unrelated repair is required: stop and expose the concrete conflict.
- A required passing check/test fails or is incomplete: retain its exact status and diagnose causally; do not relabel it, alter scope after failure, weaken a threshold or repeat broad runs until green.
- A planned structural slice is impossible: stop and use a documented earlier-phase repair under the owner’s standing18Oct approval plus independent QA; no silent plan edits, forced forward transition or gate exception.

### C\_3 — Describe raw boundaries and restore production strict signals

**Goal:** Describe raw boundaries and restore production strict signals

**Cycle Number:** 3

**Owner:** @imp implementer

#### Scope In

Eight existing Python adapter files and their native tests; source groups in Research/Design for config/model/stored/context/presentation/cache/local inference/factories/YAML/remaining metadata, and approved Pyright false-flag deletion. No generic execution knowledge or independent adapter host dependency.

#### Scope Out

All Research/Design exclusions; no policy/architecture drift, compatibility bridge, unrelated suite/gate/lifecycle/release work.

#### Deliverables

##### D\_3.1

Repair existing raw object/container inference and carry proved native request/report/context values across the eight Python adapter files. Preserve exact wire/root/index/order/version/config/native-write behavior and package isolation; no host models, assumed schemas, framework or silent coercion.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/bundled_adapters/ruff/check.py"

##### D\_3.2

Repair config/model/context/presentation/cache/local collections/factories/YAML/remaining SDK metadata at their existing owners. Restore the approved Pyright strict defaults without enabling the four native-default-none policies; preserve runtime guards/nullability/variance/default freshness and use precise justified library boundaries only where source evidence requires. Complete model-only/Literal/variance/library controls within C_3 and replay applicable logging controls under restored native policy with temporary enabling headers removed.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "pyrightconfig.json"

#### Exit Criteria

Focused existing owner tests and changed-file gates pass; current restored-policy findings are causally classified/fixed within approved owners. Before C_3 exit, model-only/Literal/variance/library controls and applicable logging replay under actual restored native Pyright defaults show clean positives/intended negatives. Useful guards/native diagnosis/default freshness and precise exception rationale remain; no unchecked cast, blanket disable or extra four-rule policy.

#### Dependencies

- C_2 completed with its objective focused evidence

#### Obligations

- Apply source-local object-container narrowing and precise construction types, preserving exact runtime checks/error/order/config/write behavior; before-validators remain object→object until Pydantic admission.
- After known source repairs restore the approved Pyright strict defaults. One configured production Pyright diagnostic scan is permitted because the edited native policy affects that whole selection; keep its initial failure facts and then recheck actual diagnosed/edited files, not the whole workspace per edit.
- Native guard/variance/library exceptions require exact source evidence/trigger; standard annotation or supported callable/protocol view precedes a last-resort precise exception. Do not enable the four default-none policies or remove useful guards.

#### Verification

##### Adapter package and host owner preservation

**Method:** run_tests(scope='targets', targets=["tests/mcp_server/integration/adapters/test_ruff_checks.py","tests/mcp_server/integration/adapters/test_ruff_fixes.py","tests/mcp_server/integration/adapters/test_mypy.py","tests/mcp_server/integration/adapters/test_pytest.py","tests/mcp_server/integration/adapters/test_python_syntax.py","tests/mcp_server/integration/adapters/test_check_jsonschema.py","tests/mcp_server/integration/adapters/test_lychee.py","tests/mcp_server/integration/adapters/test_commitlint.py"], tests=['python_tests'], timeout_seconds=600), native defaults/no args override; split only by an actual changed source owner when useful. For changed host groups select the directly corresponding existing files from unit/config/test_composition.py, test_checks_config.py, test_contracts_config.py; unit/services/test_template_catalog.py; unit/state/test_response_cache.py; unit/server/test_bootstrap.py; relevant public presentation/scaffold/admission files. Record exact files and outcomes; no directory-wide run.

**Expected Result:** All chosen package/host behavior remains correct, including invalid/root/index/native/version/order/write refusal, null/immutability/default freshness/query/diagnostic invariants.

##### Measure restored globally affected production policy, then focused checks

**Method:** run_checks(scope='configured', checks=['python_pyright'], timeout_seconds=600), once after source fixes/policy restoration as a diagnostic discovery call; preserve complete outcome. Then Before each cycle GREEN/refactor commit: run_checks(scope='targets', targets=<actual changed production Python files for that cycle>, checks=['python_format','python_lint','python_pyright','python_types'], timeout_seconds=600). For actual changed test/helper Python files run the same target selection with checks=['python_format','python_lint'] only. Record the concrete target arrays/outcomes in cycle evidence. These explicit sets are type-appropriate; never pass docs/JSON/TOML to Python checks. No whole-test Mypy/Pyright gate is introduced.

**Expected Result:** Diagnoses grouped causally by approved source owner, not counted as runtime defects; changed-file required gates pass with no masked signal or four-rule policy expansion. Final configured acceptance belongs Validation.

##### Native-policy contract sensitivity within C_3

**Method:** run_checks(scope='targets', targets=<named temporary control files below .pgmcp/temp/issue518>, checks=['python_types','python_pyright'], args={'python_types':['--show-error-codes'],'python_pyright':['--outputjson']}, timeout_seconds=180). Use actual model-only/prepared typed-empty, Literal consumer, variance and necessary library declarations. Remove temporary enabling headers from the applicable C_2 logging controls and replay them using restored native Pyright defaults. No global/local disabling directive or assumed valid raw-input cast is allowed.

**Expected Result:** Before C_3 can exit, correct controls are clean and deliberately wrong model/producer/Literal/variance calls produce intended native codes; applicable retained-library/runtime/schema controls remain sound. This evidence belongs to C_3, not a future C_4. If the native signal or contract cannot be demonstrated, retain the failure and stop this cycle.

#### Stop Conditions

- New/contradictory owner policy, changed supported runtime/schema/protocol/config/admission behavior, unchecked cast, lost guard/variance/primary diagnostic, new broad suppression/framework or unrelated repair is required: stop and expose the concrete conflict.
- A required passing check/test fails or is incomplete: retain its exact status and diagnose causally; do not relabel it, alter scope after failure, weaken a threshold or repeat broad runs until green.
- A planned structural slice is impossible: stop and use a documented earlier-phase repair under the owner’s standing18Oct approval plus independent QA; no silent plan edits, forced forward transition or gate exception.

### C\_4 — Finish precise local exceptions and bounded test policy

**Goal:** Finish precise local exceptions and bounded test policy

**Cycle Number:** 4

**Owner:** @imp implementer

#### Scope In

Indexed ordinary helper/lambda/private/mock/invalid/frozen/B017 and remaining local/import/dormant/unused groups; native test ANN/ARG and Mypy untyped override; source comments/triggers, temporary type sensitivity controls and final activation.

#### Scope Out

All Research/Design exclusions; no policy/architecture drift, compatibility bridge, unrelated suite/gate/lifecycle/release work.

#### Deliverables

##### D\_4.1

Correct the three untyped helpers, indexed lambdas/private/mock/B017 cases and ordinary annotations; remove broad tests ANN/ARG and tests.* untyped relaxations only with exact necessary interface/fixture/invalid cases handled. Preserve public keyword contracts and invocation-time Settings/fixture behavior; no whole-test Mypy gate or suite rewrite.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "pyproject.toml"

##### D\_4.2

Resolve each remaining equivalent local group against final combined policy: remove dormant/unused/dead directives/helpers, keep source-demonstrated terminal/variance/library/timing exceptions with rationale/trigger, and reuse fresh C_2/C_3 sensitivity evidence, completing only remaining test-policy/local controls here without permanent diagnostic tests. Review actual final inventory, activate final source via restart/fresh context/health and prepare the Implementation handover.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "tests/mcp_server/unit/core/interfaces/test_interface_imports.py"

#### Exit Criteria

Affected helper/import/fixture/public behavior tests and target gates pass; seven-independent/twelve-masked distinction resolved under final policy; actual remaining directives all have rationale/trigger. Reuse fresh completed C_2/C_3 controls and complete only invalidated/remaining final-local/test-policy evidence; unused-code scan is honestly classified, final source activated, no stale runtime claim or expanded gate policy.

#### Dependencies

- C_3 completed with its objective focused evidence

#### Obligations

- Type ordinary helpers/private parameters, narrow B017 and necessary invalid/fixture/interface cases, and remove obsolete/dormant directives. Do not delete twelve comments just because old ANN/ARG policy masked them.
- After helper repairs remove the broad native ANN/ARG and untyped overrides. One configured Ruff diagnostic scan with RUF100 added is permitted for this globally affected policy; preserve the complete initial outcome and target subsequent repairs.
- Move ordinary imports only with corresponding startup/fixture/patch evidence. Retain route-specific CLI delay and invocation-time Settings lookup. No unrelated mass hoisting or public keyword rename.
- Record actual removed/narrowed/retained groups and rationale/trigger in source/evidence for the final Validation table. Restart once final source and focused checks are complete, then wait as instructed, get_work_context before commit/push, and health_check. No universal client/server refresh claim.

#### Verification

##### Precise final local/native test policy

**Method:** run_checks(scope='configured', checks=['python_lint'], args={'python_lint':['--extend-select','RUF100','--output-format','json']}, timeout_seconds=600), once after helper/policy repair as a diagnostic scan; retain initial findings and narrow follow-ups to actual affected files. Before each cycle GREEN/refactor commit: run_checks(scope='targets', targets=<actual changed production Python files for that cycle>, checks=['python_format','python_lint','python_pyright','python_types'], timeout_seconds=600). For actual changed test/helper Python files run the same target selection with checks=['python_format','python_lint'] only. Record the concrete target arrays/outcomes in cycle evidence. These explicit sets are type-appropriate; never pass docs/JSON/TOML to Python checks. No whole-test Mypy/Pyright gate is introduced.

**Expected Result:** Actual final-policy redundant comments removed; necessary interface/fixture/invalid/library/variance/timing comments remain precise with rationale/trigger. No blanket test exemption or unchecked cast.

##### Proportional helper/import/runtime behavior

**Method:** run_tests(scope='targets', targets=<actual changed helper/import consumer test files>, tests=['python_tests'], timeout_seconds=600); include unit/test_cli.py, unit/decorators/test_pipeline_decorators.py, unit/core/interfaces/test_interface_imports.py, unit/tools/test_git_tools.py, test_issue_tools.py and the specific affected fixture/resource/manager cases. Reuse fresh evidence where source unchanged; no broad directory/suite run.

**Expected Result:** Existing fixtures/patches, public keyword calls, invalid/frozen rejection, route-dependent imports and invocation-time Settings continue to work; ordinary helpers are typed without new legacy tests.

##### Fresh controls and final source activation

**Method:** Reuse the completed fresh C_2 producer and C_3 native-policy controls without deferring their cycle exits. Only invalidated or remaining local/test-policy/library controls are completed here, through run_checks(scope='targets', targets=<named temporary control files below .pgmcp/temp/issue518>, checks=['python_types','python_pyright'], args={'python_types':['--show-error-codes'],'python_pyright':['--outputjson']}, timeout_seconds=180) with actual restored native policy and no disabling directives; negative exit1 remains diagnostic evidence. Then restart_server(reason=<final source activation>), prescribed wait, get_work_context(), health_check().

**Expected Result:** All earlier required controls were already completed in their owning cycles. Remaining/invalidated final local-policy controls show clean positives and intended negative codes, with exact outcomes retained; no permanent diagnostic suite or new test-type gate. Health identifies the current instance only; no live planning mutation or harnas config switch.

#### Stop Conditions

- New/contradictory owner policy, changed supported runtime/schema/protocol/config/admission behavior, unchecked cast, lost guard/variance/primary diagnostic, new broad suppression/framework or unrelated repair is required: stop and expose the concrete conflict.
- A required passing check/test fails or is incomplete: retain its exact status and diagnose causally; do not relabel it, alter scope after failure, weaken a threshold or repeat broad runs until green.
- A planned structural slice is impossible: stop and use a documented earlier-phase repair under the owner’s standing18Oct approval plus independent QA; no silent plan edits, forced forward transition or gate exception.

## Phase Deliverables

### Validation

#### D\_1

Record one full native suite and all required gates, preserved behavior/type/source mapping, actual remove/narrow/retain dispositions with exact rationale and triggers, negative/incomplete history, safe reproduction and residual/deferred work.

**Owner:** @imp validator

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue518/validation.md"

### Documentation

#### D\_1

Reconcile the existing type-checking playbook with implemented source-first/precise exception policy and actual model-only boundaries without duplicating per-issue instructions.

**Owner:** @imp documenter

**Validates:**

**Type:** file_exists

**File:** "docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md"

#### D\_2

Document actual formatter-owned metadata, event_timestamp, flat valid props and explicit safe payload/collision diagnosis in the existing server configuration reference; preserve unrelated launcher/config documentation.

**Owner:** @imp documenter

**Validates:**

**Type:** file_exists

**File:** "docs/reference/server-configuration.md"

## Related Documents

- [Approved Design](<design.md>)
- [Research and inherited strategy](<research.md>)
- [Evidence/gate scope](<../../../coding_standards/QUALITY_GATES.md>)
- [Type resolution order](<../../../coding_standards/TYPE_CHECKING_PLAYBOOK.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-20 | @imp planner | Save/read back four complete named cycles and eleven total deliverables; define focused preservation/type evidence, bounded global-policy diagnostic scans, native final verification and explicit stops. |
| 1.1 | 2026-10-20 | @imp planner | Resolve two QA P2 blockers: assign unmasked type controls to C_2/C_3 before their exits and include actual model-only SDK/direct consumers in C_1 baseline/GREEN; replace complete stored cycle blocks and verify readback. |
