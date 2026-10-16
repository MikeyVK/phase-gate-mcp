<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=WI5iXHBKVOU91bYE -->

# Issue 505 — Bounded assembly safety planning

**Status:** PLANNING — QA REQUESTED  
**Version:** 0.3  
**Last Updated:** 2026-10-16

## Purpose

Execute the approved builder Design in C_1 and the owner-approved bounded test-consumer repair in C_2.

## Scope In

scripts/build_package.py, its existing unit test module, phase evidence and the active release-assets procedure, plus the specifically approved existing test preparations/consumers listed for C_2.

## Scope Out

Manifest/content routing changes, runtime consumers, new error/transaction frameworks, release/deployment/version bumps and issues506–508.

## Summary

C_1 keeps the inseparable builder invariants together and is complete. After the required full-suite FAIL, the owner approved the separate bounded C_2 test preparation/consumer repair. The builder implementation and its valid isolated-staging caller remain unchanged; no general fixture refactor is authorized.

## Dependencies

- Approved Research v0.2 and independent GO f5125b9c.
- Design v0.1 and independent GO4c119786.

## Risks

### Link/reparse creation differs across platforms.

Use real scratch symlink where supported and an explicit Windows junction fallback; verify the ownership case executes, not skip.

### Broad validation can reveal unrelated baseline issues.

Preserve exact findings; do not weaken the gate or expand into general cleanup. Discuss an actual policy exception if required.

## Milestones

- Implementation → Validation: independent QA checks C_1 completion and narrow evidence; QA does not execute the future full Validation in this gate.
- Validation: exactly one full native-configured test suite: run_tests(scope='configured', tests=['python_tests'], timeout_seconds=1200), preserving all native defaults and coverage options. A real timeout/incomplete run is not a pass.
- Validation: run_checks(scope='branch', checks=['python_format','python_lint','python_pyright','python_types','markdown_links','yaml_configuration','json_schema_shape','json_schema_metaschema'], timeout_seconds=600). Existing per-check configured branch filtering selects appropriate file types. No branch message check is invented.
- Validation: run_checks(scope='configured', checks=['python_types'], timeout_seconds=600) retains production-scoped Mypy. The changed builder/test files additionally retain their explicit Pyright evidence from C_1.
- Do not repeat the focused test run if the full native run exposes all builder scenarios and no later edits invalidate it. Record exact invocations, native outcomes, warnings, residuals and source snapshot in the compact validation report.
- Validation → Documentation: independent QA reads actual evidence. Required failures are FAIL; no imported #504 waiver or silent scope reduction.
- Documentation: update only the active assembly procedure's relevant order/ownership/failure passages and revision metadata; run targeted markdown_links on changed report/reference files, reuse fresh evidence otherwise.
- Documentation → Ready: independent QA. Then follow Ready instructions, submit PR closing only#505 and hand concrete merge request to Coordination. No self-merge or next issue.

## Work Units

### C\_1 — bounded\_assembly\_safety

**Goal:** Remove the evidenced fail-open behavior and enforce the explicit filesystem ownership boundary.

**Cycle Number:** 1

#### Scope In

Manifest shape/path/source preflight, generated-root cleanup safety, copy failure propagation, truthful orchestration, focused public behavior tests.

#### Scope Out

Any runtime/config-loader change, manifest grammar, broad test refactor, actual repository asset assembly/build or release.

#### Deliverables

##### D\_1.1

Correct scripts/build_package.py using shared manifest/path admission before effects, explicit disposable output, original-exception notes and no success/build after failure.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "scripts/build_package.py"

##### D\_1.2

Adapt the existing builder unit module to prove invalid-data, ownership/link, cleanup/copy error and valid staging/ordering/dotfile behavior through public functions; remove the legacy/content-only assertion.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "tests/mcp_server/unit/test_build_package.py"

#### Exit Criteria

All planned admission, ownership and IO-failure behavior is implemented; focused builder tests pass with no skips, original diagnostics and external staging/dotfiles are proved, and formatter/lint/Pyright pass on both changed Python files. No release/build of repository assets or runtime consumer rewrite.

#### Obligations

- RED: adapt tests/mcp_server/unit/test_build_package.py with stable corrected-behavior tests before production changes. Run the complete small module; failures must expose the planned defect rather than fixture errors. Commit sub_phase='red', cycle_number=1.
- GREEN: implement the approved local preparation/copy seams in scripts/build_package.py; preserve public signatures, valid external staging/dotfiles and original exception objects/details. Run the same small module; commit sub_phase='green', cycle_number=1.
- Planned cleanup: remove the old manifest-content/legacy assertion as part of meaningful behavior coverage. Avoid new permanent diagnostic probes and content snapshots. Refactor commit only if actual additional edits require it.
- Safety cases use tmp_path only, real cleanup/copy and real link/reparse evidence; inject faults at the OS/copy boundary and replace only the external build process. Windows junction fallback is confined to scratch and removed without following its target; no skipped ownership case.
- Pre-commit reality check: tests demonstrate actual state/diagnostics/build outcome through public functions; no source-string/private-helper tests and no repository state writes.

#### Verification

##### Focused corrected behavior and direct caller topology

**Method:** run_tests(scope='targets', targets=['tests/mcp_server/unit/test_build_package.py'], tests=['python_tests'], timeout_seconds=180). RED and GREEN; rerun only after relevant edits.

**Expected Result:** RED exposes planned defects; GREEN all scenarios pass without safety-case skips.

##### Python file quality

**Method:** run_checks(scope='targets', targets=['scripts/build_package.py','tests/mcp_server/unit/test_build_package.py'], checks=['python_format','python_lint','python_pyright'], timeout_seconds=600).

**Expected Result:** All selected checks pass on the changed Python files; no Markdown/JSON sent to explicit Python checks.

#### Stop Conditions

- A valid direct staging consumer needs a contract change not covered by Design.
- The fix needs a general transaction or configuration-content redesign.
- An apparent test failure comes from the harness rather than corrected behavior; repair setup before claiming RED.
- Any real repository source, state or recovery material changes during scratch proof.

### C_2 — current_config_test_consumers

**Goal:** Complete the owner-approved adoption of existing config contracts in the failed test preparations/consumers, with no production redesign.

**Cycle Number:** 2

**Owner decisions:** The owner directly approved the bounded repair in Coordination on 2026-10-16, then explicitly approved force_phase_transition to Planning in the implementation chat. No gate exception. C_1 and the complete failed Validation run remain unchanged.

#### Deliverables

- **D_2.1 — explicit_fixture_and_consumer_adoption:** Repair existing failed test preparations and keyed/id/order consumers, using an explicit config-only configured_workspace fixture where delivered config is intended; preserve synthetic defaults and absence tests.
- **D_2.2 — cli_and_handshake_diagnosis:** Record the seven in-process CLI admission causes and the unreproduced source handshake; repair proven fixture causes only and verify existing lifecycle tests without speculative production or timeout changes.

#### Scope and preparation ownership

| Group | Planned correction |
| --- | --- |
| Workflow/state/tool setups | Request explicit config-only configured_workspace preparation for delivered-contract scenarios. Keep factories and loader queries read-only. Preserve existing complete synthetic defaults and missing-config negative tests. |
| Custom gate tests | Author intended complete bases in defaults; convert nested ordered objects to keyed/order form. Do not use deep-merged overrides as complete replacement fixtures. |
| Label/milestone/id consumers | Key authorable objects by id, retain legitimate payload/API names, use milestones={} for an empty collection and values() when examining phase objects. Keep the behavior asserted by each test. |
| Selected catalog/artifact roots | Place complete synthetic bases under defaults. Ensure invalid-value/duplicate tests reach the defect they intend, rather than passing on an unrelated missing file. |
| Proposal/activation/renewal | Prepare complete checks/adapters bases and explicit configuration_choice in the existing setup commands. Do not replace public services, CLI composition or diagnostics. |
| Startup | Copy the whole config tree in isolated_target_env. The separate subprocess helper already does so; its unchanged targeted diagnostic returned passed. Its original timeout is unexplained, and receives no speculative timeout/environment/production patch. |

**Permitted files:** the existing fixture module tests/mcp_server/fixtures/suite_roots.py and only these recorded failed test modules (not every source-discovery candidate):

- tests/mcp_server/unit/managers/test_phase_state_engine.py
- tests/mcp_server/unit/managers/test_phase_state_engine_c3_issue257.py
- tests/mcp_server/unit/managers/test_phase_state_engine_c4_issue257.py
- tests/mcp_server/unit/managers/test_phase_state_engine_parent_branch.py
- tests/mcp_server/unit/managers/test_phase_state_engine_persistence.py
- tests/mcp_server/unit/managers/test_phase_state_engine_workflow.py
- tests/mcp_server/unit/managers/test_project_manager.py
- tests/mcp_server/unit/managers/test_state_repository.py
- tests/mcp_server/unit/tools/test_c7_tool_conflict_handling.py
- tests/mcp_server/unit/tools/test_force_phase_transition_tool.py
- tests/mcp_server/unit/tools/test_initialize_project_tool.py
- tests/mcp_server/unit/tools/test_transition_phase_tool.py
- tests/mcp_server/unit/tools/test_cycle_tools.py
- tests/mcp_server/unit/tools/test_github_extras.py
- tests/mcp_server/unit/tools/test_label_tools.py
- tests/mcp_server/unit/tools/test_label_tools_integration.py
- tests/mcp_server/unit/execution/test_catalog.py
- tests/mcp_server/unit/services/test_artifact_target_resolver.py
- tests/mcp_server/tools/test_a4_schema_overrides.py
- tests/mcp_server/integration/test_issue39_cross_machine.py
- tests/mcp_server/integration/test_create_issue_e2e.py
- tests/mcp_server/integration/templates/test_planning_artifact.py
- tests/mcp_server/integration/test_renewal_cli.py
- tests/mcp_server/integration/test_template_activation.py
- tests/mcp_server/integration/test_template_proposal.py
- tests/mcp_server/integration/test_target_startup.py

No new test module or suite-wide autouse setup. No production file, native config, timeout policy, release or #506–508 work is authorized by C_2. No obsolete behavior-preservation/negative-legacy tests are added.

#### Dependencies and test mode

- Depends on completed C_1 and the recorded Validation FAIL at f20966e6.
- Existing full-run failures provide the failing evidence; this is test-maintenance/consumer adoption, so no artificial RED or duplicate permanent regressions.
- After independent QA GO, re-enter Implementation with resume_cycle='C_2' from get_project_plan readback.
- Commit bounded actual repair chunks with workflow_phase='implementation', cycle_number=2 and sub_phase='refactor'. Producer owns integration and commits; any bounded delegates edit only assigned files and return findings, never workflow approval.
- No broad configured test run during Implementation. Group narrow runs by state/tool setup, keyed/model consumers and lifecycle fixtures; select only affected existing modules from the inventory above. Use run_tests(scope='targets', targets=<affected modules>, tests=['python_tests'], timeout_seconds=300), preserving native arguments.
- For the repaired Python files use run_checks(scope='targets', targets=<changed Python files>, checks=['python_format','python_lint','python_pyright'], timeout_seconds=600). Do not send docs/JSON to Python gates.
- Keep the seven CLI cases distinct: fresh install; checkpointless baseline; external checkpoint/force refusal; verified backup force; conflict resolution; completed recovery; first legacy migration. Their shared initial missing-defaults cause is evidenced by the real admission call chain; post-repair outcomes must still pass.
- The one unchanged handshake diagnostic used run_tests targets=[tests/mcp_server/integration/test_target_startup.py], python_tests args=['-k','test_real_server_process_handshake_default_target','--tb=long'], timeout180. Returned tool summary: passed/reason=-/args_source=caller. Native counts, timing and exit details were not available; do not reconstruct them from the summary or depend on its expired cache.
- Do not repeat focused evidence after unrelated changes. No blanket skip, selection/coverage reduction or broad suppression.

#### Exit Criteria

Existing affected behavioral modules pass without added skips/suppressions or weakened assertions; explicit config preparation and keyed/id/order consumers match current contracts; seven CLI cases reach their intended behaviors; unchanged handshake is rechecked without speculative timeout changes. Relevant changed-file format/lint/Pyright pass. No production change or gate exception.

#### Stops and resumed Validation

- Stop for an actual new production behavior/architecture cause or an unanticipated scope expansion; investigate/read-only evidence first and request an owner decision only where necessary.
- If a targeted test still fails after admission repair, diagnose its intended existing contract; do not weaken its behavioral assertions merely to pass.
- If the source-handshake timeout recurs, preserve exact stderr and locate the stalled startup stage. No increased timeout or production workaround without causal evidence and the required scope decision.
- Independent QA must review C_2 Implementation → Validation. Then repeat the required complete native suite once after these relevant changes: run_tests(scope='configured', tests=['python_tests'], timeout_seconds=1200), within the unchanged1800-second client window. Preserve native args/coverage.
- Repeat the existing planned filtered branch gates and configured Mypy after the repair. Update Validation with the new outcome while retaining the original full FAIL and its diagnosis. Progress only on actual independent GO.

## Phase Deliverables

### Validation

#### D\_1

Durable exact focused/full native-configured test and branch-check evidence, corrected behavior and preservation mapping, original diagnostics, outcome limits and independent-review navigation.

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue505/validation.md"

### Documentation

#### D\_1

Reconcile the active release-assets assembly procedure with admission order, disposable output and fail-closed exception behavior; no historical report rewrite or release claims.

**Validates:**

**Type:** file_exists

**File:** "docs/reference/release-assets-procedure.md"

## Related Documents

- [Design](<design.md>)
- [Approved Research](<research.md>)
- [Builder](<../../../scripts/build_package.py>)
- [Behavior tests](<../../../tests/mcp_server/unit/test_build_package.py>)
- [Quality evidence standards](<../../coding_standards/QUALITY_GATES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-16 | @imp planner | Plan one focused RED/GREEN cycle and phase-owned validation/documentation. |
| 0.2 | 2026-10-16 | @imp planner | Correct the full-suite execution budget to 1200 seconds within the approved 1800-second client window; selection unchanged. |
| 0.3 | 2026-10-16 | @imp planner | Preserve C_1 and add the owner-approved bounded C_2 test-consumer repair, diagnosis and unchanged full Validation gates. |


