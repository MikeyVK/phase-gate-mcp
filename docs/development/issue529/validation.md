<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue \#529 — Response-profile validation

**Status:** Completed producer validation — independent review requested  
**Version:** 0.1  
**Last Updated:** 2026-10-20

## Purpose

Record structural completion, full native verification and the exact negative/repair history for the approved response-profile contract.

## Scope In

C_1 and C_2 profile/configuration, truthful serialization/publication, protected presentation, selected MCP envelope/schema, startup recovery and directly affected consumer tests.

## Scope Out

No harness/version certification, #528 decorator metadata repair, release/install rollout, compatibility path or opt-in coverage gate.

## Prerequisites

- Research v1.4 Approved Strategy; Design v0.2; Planning v0.1 and stored two-cycle plan.
- Independent Implementation→Validation GO on98378e6e; bounded test-consumer repair re-reviewed with GO on730bcadc.
- Full native selection/options remain unchanged; no gate exception.

## Issue Number

#529

## Validation Status

PASS

## Scope

Implementation commits1471953e(C_1),98378e6e(C_2),730bcadc(direct-consumer cleanup); workflow refactor.

## Obligations

### D\_1.1 — Explicit shared definitions and process-local profile selection

**Evidence:**

- [Profile configuration and resolution](<../../../mcp_server/config/schemas/presentation_config.py>)
- [Settings and environment](<../../../mcp_server/config/settings.py>)
- [Config/settings behavior](<../../../tests/mcp_server/unit/config/test_presentation_config.py>)

**Outcome:** Frozen, extra-forbid profiles, required literals and positive budgets; known/default/empty selector behavior; composed workspace config; two simultaneous server processes select independently without changing shared config.

### D\_1.2 — Truthful canonical serialization and original diagnosis

**Evidence:**

- [Canonical serializer](<../../../mcp_server/utils/cache_serialization.py>)
- [Publisher](<../../../mcp_server/state/response_cache.py>)
- [Cache fidelity behavior](<../../../tests/mcp_server/integration/test_cache_fidelity_v3.py>)

**Outcome:** No hidden replacement-JSON success. Original exception/cause retained by existing capture_exception and receipt union; failed serialization creates no entry/eviction. Normal canonical field-presence and window contracts retained.

### D\_1.3 — Frozen public output contracts

**Evidence:**

- [Public envelope and variants](<../../../mcp_server/schemas/presentation_output.py>)

**Outcome:** One strict envelope; inline/resource alternatives, complete direct attachments and distinct cache_publication_failed/operation_serialization_failed variants. Internal operation DTOs and ToolExecution responsibilities retained.

### D\_2.1 — Protected rendering and detail-only bounds

**Evidence:**

- [Text renderer](<../../../mcp_server/presenters/text_presenter.py>)
- [Limiter](<../../../mcp_server/presenters/text_budget_limiter.py>)
- [Composition behaviors](<../../../tests/mcp_server/unit/presenters/test_text_presenter_composition.py>)

**Outcome:** Core includes complete main template, enum explanation, next instructions and notes; collections are optional. Dynamic markers survive deliberate tiny-budget overrun; only UTF-8-safe optional details are cut, with protected truthful notices.

### D\_2.2 — Selected envelope/schema and fixed recovery

**Evidence:**

- [Response projection](<../../../mcp_server/presenters/response_presenter.py>)
- [Server transport](<../../../mcp_server/server.py>)
- [Startup recovery](<../../../mcp_server/presenters/startup_recovery_presenter.py>)
- [SDK profile/failure cases](<../../../tests/mcp_server/integration/test_execution_presentation_v3.py>)

**Outcome:** Seven representative channel/delivery combinations validate emitted output against actual SDK catalog schema. Complete operation/attachments use selected route; actual isError preserved through four independent serializer failure cases. Recovery is full dual-channel, inline and config/cache independent.

### D\_2.3 — Direct consumer migration, isolation and live activation

**Evidence:**

- [Source/installed public startup](<../../../tests/mcp_server/integration/test_v3_cutover.py>)
- [Validation attachment consumers](<../../../tests/mcp_server/unit/server/test_validate_tool_arguments.py>)
- [Two-process/startup evidence](<../../../tests/mcp_server/integration/test_target_startup.py>)
- [Shared constructor](<../../../tests/mcp_server/test_support.py>)

**Outcome:** Existing public-tool, interface, presenter, pipeline, bootstrap, source/installed and schema consumers migrated. One real two-process case shares workspace/config and proves independent profiles, distinct child PIDs and unchanged config bytes. Focused native evidence and live calls below.

## Evidence

### Full native suite — initial FAIL and final PASS

Same configured binding, no caller args and no changes to pyproject/native selection. Python3.15.0,pytest9.1.1,8 xdistworkers,3060items. Initial:5failed3055passed687.07s,exit1. After two direct-consumer testfile repairs:3060passed703.45s,exit0. Earlier readiness failure did not recur; its cause is not proven fixed and no timeout/assertion/selection was changed. Native stderr included child_exited; pytest reported no warning/failure summary on final pass.

**Sources:**

- [Native test policy](<../../../pyproject.toml>)
- [Test binding](<../../../.pgmcp/config/tests.yaml>)

**Invocation:** run_tests(scope='configured',tests=['python_tests'],timeout_seconds=1800), both runs; no args parameter.

**Observed Result:** Initial receipt17eef363ca1346c89014b141564b3064; final2eb307b713734ded8a12413c9ae67dd8.

### Branch Python gates passed

Final branch scope selects check-appropriate Python sources from changed files. python_format40files,python_lint passed; production-Mypy13files and Pyright13files passed,0errors/0warnings. No Markdown/YAML passed to Python checks.

**Sources:**

- [Check bindings](<../../../.pgmcp/config/checks.yaml>)

**Invocation:** run_checks(scope='branch',timeout_seconds=900)

**Observed Result:** All four selected checks passed,c933871cf9d64ceebe11f464437bd594. Initial branchcheck also passed,8302c74af7c046c5b65877716fcec0b7.

### Configured Python gates remain applicable

python_types192productionfiles,python_format475files,python_lint and python_pyright192productionfiles all passed. Since this result only two test-consumer files changed and received fresh directed format/lint/Pyright plus final branch gates; production and native configuration are unchanged. Mypy emitted only the existing informational unused tests.* section note, not an error. No gate is relaxed.

**Sources:**

- [Typing/test quality policy](<../../coding_standards/QUALITY_GATES.md>)

**Invocation:** run_checks(scope='configured',checks=['python_types','python_format','python_lint','python_pyright'],timeout_seconds=900)

**Observed Result:** All4passed,cddd19b33ccd44d39f85a79c6bdf293f; fresh evidence reused per plan.

### C\_1 focused contract evidence

Initial unchanged baseline63passed. Missing new profile/cache/value invariants were observed RED before production. Final5filegroup117passed. Config/settings resolution, native error/cause, canonical nullable fidelity and frozen envelope contracts are covered; no full suite ran during C_1.

**Sources:**

- [Configuration cases](<../../../tests/mcp_server/unit/config/test_presentation_config.py>)
- [Cache publisher cases](<../../../tests/mcp_server/unit/state/test_response_cache.py>)

**Invocation:** run_tests(scope='targets',targets=['tests/mcp_server/unit/config/test_presentation_config.py','tests/mcp_server/unit/config/test_settings.py','tests/mcp_server/unit/state/test_response_cache.py','tests/mcp_server/integration/test_cache_fidelity_v3.py','tests/mcp_server/unit/schemas/test_presentation_output.py'],tests=['python_tests'],args={'python_tests':['-n','0']},timeout_seconds=300)

**Observed Result:** 117passed1.47s,a1978b5017eb43398a8cc747d35d85a9.

### Selected profiles, protected core and native SDK failure paths

48passed14.31s across direct transport/profile/composition/limiter files. Dynamic instructions, long data/attachments, real resource readback, seven channel combinations, four independent native serialization-failure cases and actual success/isError are asserted; envelopes validated against advertised schemas. Related direct public-tool group79passed15.97s; full final suite also includes all these cases.

**Sources:**

- [SDK/profile cases](<../../../tests/mcp_server/integration/test_execution_presentation_v3.py>)
- [Transport ownership](<../../../tests/mcp_server/integration/test_tool_attachment_transport.py>)

**Invocation:** run_tests(scope='targets',targets=['tests/mcp_server/integration/test_tool_attachment_transport.py','tests/mcp_server/integration/test_execution_presentation_v3.py','tests/mcp_server/unit/presenters/test_text_presenter_composition.py','tests/mcp_server/unit/presenters/test_text_budget_limiter.py'],tests=['python_tests'],args={'python_tests':['-n','0']},timeout_seconds=300)

**Observed Result:** 48passed,90dc1a43d1a44b69a0adcba44b174f8b.

### Real startup/process isolation and installed candidate

Two-file startup/bootstrap group24passed and1stale schema-reader failure; corrected installed-candidate case1passed10deselected149.56s. New single two-process case1passed26.15s separately: sameconfig/workspace,selectors structured_inline/text_inline, both markers/instructions complete, different childPIDs, first profile retained after second starts, source bytes identical. All25cases are covered again by final full suite.

**Sources:**

- [Startup and instance case](<../../../tests/mcp_server/integration/test_target_startup.py>)
- [Bootstrap constructor contracts](<../../../tests/mcp_server/unit/server/test_bootstrap.py>)

**Invocation:** run_tests(scope='targets',targets=['tests/mcp_server/integration/test_target_startup.py','tests/mcp_server/unit/server/test_bootstrap.py'],tests=['python_tests'],args={'python_tests':['-n','0']},timeout_seconds=600); corrected case targeted test_target_startup.py with args=['-n','0','-k','installed_candidate_init_migration_and_mcp_handshake'].

**Observed Result:** Corrected case c1d6b63665ae423e81e2e5242d703fd9; isolation d1a31aeeb544410bbba13273fa05e8ab.

### Test-only repair and unchanged lifecycle diagnosis

Two missing consumers migrated to direct envelope attachments, preserving existing schema/startup behavior. Unit5passed first directed repair run; after correcting template MIME expectation, source+installed2passed94.26s. Both files format/lint/Pyright passed. Lifecycle file unchanged;4parametercases passed7deselected54.00s before final full run. The latter is diagnosis, not a waiver or proven cause of the earlier parallel failure.

**Sources:**

- [Entry point cases](<../../../tests/mcp_server/integration/test_v3_cutover.py>)
- [Validation schema cases](<../../../tests/mcp_server/unit/server/test_validate_tool_arguments.py>)
- [Unchanged lifecycle case](<../../../tests/mcp_server/integration/execution/test_process_stopping.py>)

**Invocation:** run_tests(scope='targets',targets=['tests/mcp_server/integration/test_v3_cutover.py'],tests=['python_tests'],args={'python_tests':['-n','0']},timeout_seconds=600); lifecycle targets=['tests/mcp_server/integration/execution/test_process_stopping.py'],args={'python_tests':['-n','0','-k','test_failure_stops_live_children_and_keeps_primary_cause']},timeout_seconds=180.

**Observed Result:** Source/installed123fa618e768479fb3aab538203fbd1e; lifecyclee25347d8f3d241e8ac178c4b5580d700; native cases unchanged and final full suite PASS.

### Directed config/file gates

Changed Python files format/lint/Pyright passed, changed productionMypy passed; final two repaired testfiles directed all3passed. Changed presentation YAML passed native yaml_configuration. No global suppressions, lowered thresholds or quality configuration changes.

**Sources:**

- [Presentation YAML](<../../../.pgmcp/config/defaults/presentation.yaml>)

**Invocation:** run_checks(scope='targets',targets=<changed Python files>,checks=['python_format','python_lint','python_pyright'],timeout_seconds=600); production paths only for checks=['python_types']; run_checks(scope='targets',targets=['.pgmcp/config/defaults/presentation.yaml'],checks=['yaml_configuration'],timeout_seconds=300).

**Observed Result:** Python df59f6ec229d473388322e0e9d68e015; production8e3da1012a904c9e8dd6feba9e2575c3; YAML d8f83437328c41699b67ae1def1be4fc; final repair6a157b130b644308b50bec4f4dac5f66.

## Demonstration

After C_2 commit98378e6e, restart_server(reason='Activate completed issue529 C_2 response-profile cutover...') replaced PID61796 with6348. health_check() returned healthy; all five common envelope keys were present and delivery_error=null. get_work_context() returned Implementation/C_2/green and the complete phase_instructions verbatim in both text content and presentation, with original operation fields in data.operation. scaffold_schema(artifact_type='validation_report') returned a complete schema://template/validation_report/context attachment whose parsed content equaled operation.schema_data. Live call receipts:eb32dcc1836d458e82108551252f7438,76b4d900670c47bc98fa8e7c5775a725,bff1aaa1004d4a969470cac99898a673. Later repair changed tests only; this production evidence remains applicable.

## Preservation

Operation semantics, note sources, configured item ordering/limits, normal cache field-presence/window semantics and attachment identity/MIME remain authoritative. Actual operation success is separate from delivery failure. No DTO reconstruction from Markdown or cache replay of mutations.

## Containment

Removed concealed serializer-error replacement, destructive final-text cutting, unlimited fallback JSON, bare structured assignment, unconditional embedded attachment copies and absent-presenter bypass. Reused existing loader/Settings, wrappers, error capture, presenters and SDK boundaries; no compatibility alias, client fingerprinting, second cache or new exception framework. Obsolete unlimited-fallback tests/constructor mirrors removed; valuable existing behavior tests adapted. Temporary probe tree removed.

## Failures

- Initial full native run on98378e6e:5failed,3055passed in687.07s,exit1. Four omitted direct test consumers still expected embedded resources: source+installed test_v3_cutover and two test_validate_tool_arguments schema cases. Corrected in730bcadc, preserving actual attachment identity/MIME/schema/description and startup assertions.
- Fifth initial failure: unchanged test_process_stopping.py late-timeout reached its5s wait_for_children timeout before child-stop assertions; its adapter deadline was1s. Focused unchanged four-parameter rerun with -n0:4passed,7deselected in54.00s. That serial pass does not explain or waive the original parallel failure; no cause such as CPU/SDK/client transport is claimed.
- First directed consumer-repair run:5unitpassed,2entrypointfailed in88.27s because the newly edited template-schema MIME expectation was incorrectly application/json. Corrected to the producer's application/schema+json; validation MIME remains application/json. Source+installed rerun:2passed in94.26s; both files format/lint/Pyright passed. These are test-only migrations, no production or timeout change.

## Caveats

- Server output/profile tests do not certify downstream model context for every present/future client; setup must verify actual presentation and full-data readback.
- Cache references are transient/process-local, not durable proof. Exact calls/outcomes are recorded here; run IDs are supplementary.
- Complete inline operation data, attachments and protected core may exceed the short-presentation budget. Diagnostic bounds do not promise streaming/memory bounds.
- Native coverage is opt-in; #529 adds no coverage gate and makes no coverage-percent claim.
- Initial parallel child-readiness timeout remains a historical negative finding; final unchanged native run passed. No production lifecycle correction or causal explanation is claimed. A recurrence requires focused investigation, not acceptance by a serial-only pass.

## Deferred Work

### Issue \#528 output-model/decorator registration metadata work

Independent scoped issue; #529 establishes selected public envelope/schema policy without repairing decorator metadata.

**References:**

- [Issue #528](<https://github.com/MikeyVK/phase-gate-mcp/issues/528>)

## Related Documents

- [Planning](<planning.md>)
- [Design](<design.md>)
- [Approved strategy](<research.md>)
- [Quality standards](<../../coding_standards/QUALITY_GATES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-20 | @imp validator | Record approved contract mapping, full native suite failures and bounded repair, final 3060-pass run, broad checks and live delivery evidence. |
