<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue 506 — Operation-policy removal validation

**Status:** VALIDATION — PASS, QA REVIEW REQUESTED  
**Version:** 0.2  
**Last Updated:** 2026-10-16

## Purpose

Record coherent removal and preserved active admission with exact focused and complete native evidence.

## Scope In

Approved clean removal, direct retained consumers, real startup and live enforcement preservation.

## Scope Out

No replacement framework, compatibility layer, automatic existing-workspace migration, release/build/deployment or issues507–508.

## Issue Number

#506

## Validation Status

PASS

## Scope

Branch chore/506-unused-operation-policy, parent main. Tested production/test snapshot f5eaf4b39bb694c979ceea2a5b3958b596366115; no production/test edits after verification. Research v0.2 records the explicit owner-approved clean break. This non-cycle Chore introduces no synthetic TDD cycle or extra tests.

## Obligations

### Remove the entire unused operation-policy route coherently.

**Evidence:**

- [Approved boundary and inventory](<research.md>)
- [Current loader](<../../../mcp_server/config/loader.py>)
- [Current bootstrap](<../../../mcp_server/bootstrap.py>)

**Outcome:** Engine/decision module, operation models/exports, loader/startup field/validation, both shipped YAML sources, three dead test modules and unused factory removed. Five retained tests adapted only at their direct seam. No functional symbol consumer remains in the explicit production/test/config scan.

### Preserve live tool/workflow enforcement and meaningful tests.

**Evidence:**

- [Startup validator](<../../../mcp_server/config/validator.py>)
- [Enforcement runner](<../../../mcp_server/managers/enforcement_runner.py>)
- [Tool decorator](<../../../mcp_server/core/decorators/enforcement_decorator.py>)
- [Planning/Ready admission](<../../../tests/mcp_server/integration/test_ready_phase_enforcement.py>)

**Outcome:** No runner/decorator/enforcement configuration/workflow contract/template/check-policy change. Existing bootstrap, context-blocking, PR-lock block/allow and save/update phase-admission tests pass. Removed tests solely cover the removed subject; no added tests, skips or suppressions.

## Evidence

### Focused direct consumers and live preservation pass.

115 passed, 9 SchemaAttachment.schema-shadow warnings, 21.44s, native exit 0. Real bootstrap executes without the removed source configs; existing public admission cases retain allowed/blocked behavior. Supplemental run 1ff9452033e3403ba26b591c3a7e304a.

**Sources:**

- [Bootstrap behavior](<../../../tests/mcp_server/unit/server/test_bootstrap.py>)
- [Context enforcement](<../../../tests/mcp_server/integration/test_context_loaded_enforcement.py>)
- [PR lock](<../../../tests/mcp_server/integration/test_pr_status_lockdown.py>)

**Invocation:** run_tests(scope='targets', targets=["tests/mcp_server/unit/config/test_c_loader_schema_structural.py","tests/mcp_server/unit/config/test_label_startup.py","tests/mcp_server/unit/config/test_validator_c3.py","tests/mcp_server/unit/config/test_workflow_config_c6.py","tests/mcp_server/unit/server/test_bootstrap.py","tests/mcp_server/integration/test_context_loaded_enforcement.py","tests/mcp_server/integration/test_pr_status_lockdown.py","tests/mcp_server/integration/test_ready_phase_enforcement.py"], tests=['python_tests'], timeout_seconds=300), no caller args.

### Changed Python files pass their direct gates.

Formatter: 11 files; Ruff passes; Pyright: 11 files, zero errors/warnings; all native exits0. Supplemental run bacdae19733241f785a45788d29c7692. Formatting was applied first. No later Python edit.

**Sources:**

**Invocation:** run_checks(scope='targets', targets=["mcp_server/bootstrap.py","mcp_server/config/loader.py","mcp_server/config/validator.py","mcp_server/config/schemas/__init__.py","mcp_server/schemas/__init__.py","tests/mcp_server/test_support.py","tests/mcp_server/unit/config/test_c_loader_schema_structural.py","tests/mcp_server/unit/config/test_label_startup.py","tests/mcp_server/unit/config/test_validator_c3.py","tests/mcp_server/unit/config/test_workflow_config_c6.py","tests/mcp_server/unit/server/test_bootstrap.py"], checks=['python_format','python_lint','python_pyright'], timeout_seconds=600).

### Initial required complete native suite completed with one failure.

1 failed, 2,914 passed, 1 skipped, 1 xpassed, 253 warnings; 2,917 items; 491.37s;native exit 1. Python3.13.7/pytest9.0.2/eightworkers;no callerargs, coverage reduction or deadline/termination problem. Failure: test_failure_stops_live_children_and_keeps_primary_cause[late-timeout] in unchanged integration/execution/test_process_stopping.py. Supplemental run ccd003b2369b4839ac4dd5615afeee61.

**Sources:**

- [Existing process lifecycle test](<../../../tests/mcp_server/integration/execution/test_process_stopping.py>)

**Invocation:** run_tests(scope='configured',tests=['python_tests'],timeout_seconds=1200).

### The same failing variant passes in isolation without changes.

1 passed, 9 warnings, 7.83s,native exit 0;oneitem, original eightworker defaults. Supplemental run abe3a5a575fe46d8bb0a92cb0ef9cff2. Full-run stack fails in wait_for_children's 5-second PID wait before stop assertions. Runtime invocation already has a 1-second deadline starting before process launch. Startup/load timing can prevent the PID precondition; full-run output does not prove the exact process outcome. No claim of demonstrated load cause or altered timeouts. One unchanged complete confirmation is warranted; not a rerun-until-green loop.

**Sources:**

- [Original runtime deadline](<../../../mcp_server/execution/process_runtime.py>)

**Invocation:** run_tests(scope='targets',targets=['tests/mcp_server/integration/execution/test_process_stopping.py'],tests=['python_tests'],args={'python_tests':['-k','test_failure_stops_live_children_and_keeps_primary_cause and late','--tb=long']},timeout_seconds=180).

### Required filtered branch gates pass.

Format11files,lint,Pyright: 5 production files0 errors/warnings,Mypy: 5 files and Markdownlinks7 successful, 2 native excludes, 0 errors passed/native exit 0. yaml_configuration,json_schema_shape,json_schema_metaschema not_executed/not_applicable. Supplemental run 4311048b71c846ee81488a8ef33cc9ae.

**Sources:**

**Invocation:** run_checks(scope='branch',checks=['python_format','python_lint','python_pyright','python_types','markdown_links','yaml_configuration','json_schema_shape','json_schema_metaschema'],timeout_seconds=600).

### Configured production Mypy passes.

Success: no issues in 191 source files, Mypy1.19.1, native exit 0. Supplemental run 146cf8a3a56a477eb70628292eb9b19f.

**Sources:**

**Invocation:** run_checks(scope='configured',checks=['python_types'],timeout_seconds=600).

### Unchanged complete confirmation passes

**Invocation:** run_tests(scope='configured', tests=['python_tests'], timeout_seconds=1200).

**Observed result:** **2,915 passed, 1 skipped, 1 xpassed, 253 warnings**, 2,917 items,
**453.31s (7m33s), native exit 0**, no rejection/deadline/termination problem.
Native Python 3.13.7, pytest 9.0.2, eight xdist workers and pyproject.toml settings.
No caller args, reduced scope, coverage change or production/test/environment/timeout
adjustment. Snapshot remains f5eaf4b39bb694c979ceea2a5b3958b596366115.
Supplemental operation 11b767ba0f0641099cc88066d141035f; this report preserves the
invocation and native outcome without depending on cache persistence.

This was one confirmation after the failed full run and passing isolated diagnostic,
not a rerun-until-green loop. The first failure remains evidence: its exact cause is
unproven. The full selection is 30 cases smaller than the #505 baseline (2,947),
matching 27 dedicated dead-route test functions and three policy-only retained-file
tests removed; no extra tests, skips or suppressions were added. Existing filtered
branch and configured Mypy evidence remains fresh: no relevant code changed.

## Demonstration

Reproduce the eight-module focused call above. Bootstrap's three credential variants construct the real target server; the existing public runner/tool tests demonstrate blocked/allowed PR/context/Planning admission. No live GitHub call or repository state mutation is required; tests isolate external effects.

## Preservation

Public MCP DTOs and active enforcement unchanged. The owner explicitly accepts removal of unused direct Python imports/config-loader API. Existing owner roots are not mutated automatically. Fresh directory assembly naturally omits deleted sources; no builder, manifest-content routing or package rollout is performed.

## Containment

Only the approved source files, direct test preparations and phase artifacts changed. Seven exact files were deleted; native file deletion was used because MCP has no file-delete operation. Existing legacy-wrapper guard remains unchanged after an optional extra row-removal was rejected; no workaround was attempted.

## Failures

- Initial full-suite failure is retained above. One unchanged full confirmation subsequently passes; isolated evidence alone was not used to override the failed broad result. No required gate currently fails; independent review requested.

## Caveats

- The Research scan cannot prove absence of unknown downstream Python importers; the explicit clean break is approved.
- README and current configuration-reference cleanup are the next Documentation deliverables; historical vision and old issue reports remain historical.
- One skip, one xpass and 253 warnings retained, including schema-shadow/collection/deprecation and restart-coroutine warnings. No new skips or suppressions.

## Deferred Work

### One S1mpleTrader architecture/instruction example still mentions PolicyEngine.decide().

Source observed in that repository's docs/architecture/VSCODE_AGENT_ORCHESTRATION.md:1489. No code consumer was found. Editing another repository is outside #506; misleading example may be corrected during owner workspace reconciliation. Coordination triage, no new issue created.

**References:**

- [Consumer scope and limitations](<research.md#external-and-installation-boundary>)

### Process-lifecycle setup timing and existing warning policy

The initial full run failed while waiting for child PID publication; the unchanged
isolated variant and full confirmation pass. The one-second invocation budget starts
before process launch, so startup/readiness timing is a concrete risk, not a proven
full-run cause. A recurrence needs exact process outcome/stderr and readiness/deadline
evidence before any fixture/runtime policy change. Source:
tests/mcp_server/integration/execution/test_process_stopping.py:132,234 and
mcp_server/execution/process_runtime.py:226. Broader lifecycle-test stabilization is
outside this operation-policy removal; Coordination triage, no new issue created.

The current one skip, one xpass and 253 warnings remain disclosed. Collection,
schema-shadow, resource/path deprecations and an unawaited restart coroutine are the
existing deferred warning family (DF-319.4), not new cleanup scope. Coordination may
triage; no blanket suppression or gate exception was introduced.

## Related Documents

- [Research and Approved Strategy](<research.md>)
- [Configuration reference](<../../reference/config-loading-architecture.md>)
- [Native test settings](<../../../pyproject.toml>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-16 | @imp validator | Record removal, focused preservation tests, complete native suite and gates with remaining owner-workspace/documentation boundaries. |
| 0.2 | 2026-10-16 | @imp validator | Retain initial full failure and isolated diagnosis; record one unchanged complete passing confirmation, fresh gates and explicit timing/warning caveats. |
