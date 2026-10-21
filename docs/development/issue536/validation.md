<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue \#536 — Validation of the 4.0.0 candidate

**Status:** BLOCKED — full-suite failure requires investigation  
**Version:** 0.1  
**Last Updated:** 2026-10-21

## Purpose

Record the phase-owned verification of source f28d0d1dcdd31bf627fc0dc98faa6c01c6e60cb2 without treating preliminary installation proof as final release acceptance.

## Scope In

The #536 manifest/installation/instruction changes, closed-issue archive and workspace-only release procedure; owner-approved 4.0.0 metadata; required configured tests and branch checks.

## Scope Out

Runtime or test repairs in Validation, dependency or threshold changes, release-note/migration reconciliation reserved for Documentation, final integrated-source wheel/sdist acceptance, tags and publication.

## Issue Number

#536

## Validation Status

FAIL

## Scope

chore/536-live-agent-acceptance-and-release; parent main; committed candidate f28d0d1dcdd31bf627fc0dc98faa6c01c6e60cb2. Independent QA reaffirmed Implementation → Validation on that exact source. Only the phase-transition state audit was modified during execution.

## Evidence

### Package and manifest identify the owner-approved 4.0.0 candidate.

Exactly the two version literals changed since the previously reviewed cleanup commit 6dab38d2. Both parsers report 4.0.0; manifest YAML validation and diff whitespace checks passed. QA independently reaffirmed GO for entering Validation. TOML editing used report mode because no TOML preflight profile exists; no preflight PASS is claimed.

**Sources:**

- [Package metadata](<../../../pyproject.toml>)
- [Manifest](<../../../.pgmcp/config/release_manifest.yaml>)

**Invocation:** run_checks(scope='targets', targets=['.pgmcp/config/release_manifest.yaml'], checks=['yaml_configuration'], timeout_seconds=120); read-only TOML/YAML parsing.

**Observed Result:** YAML native exit0; package_version=4.0.0; manifest_version=4.0.0.

### The required configured suite completed with a negative native result.

Python 3.15.0 / pytest 9.1.1 on Windows, eight xdist workers, 3081 collected cases. The complete structured result was inspected: capture contains 873468 stdout bytes without truncation, no termination problem or request rejection. Operation success=true means execution/reporting succeeded; the test row is failed.

**Sources:**

- [Configured test binding](<../../../.pgmcp/config/tests.yaml>)
- [Failing lifecycle test](<../../../tests/mcp_server/integration/execution/test_process_stopping.py>)

**Invocation:** run_tests(scope='configured', timeout_seconds=1800)

**Observed Result:** 1 failed, 3080 passed in 614.27s; native exit1. Failure: test_failure_stops_live_children_and_keeps_primary_cause[late-timeout], wait_for_children at lines 133–135, awaited at line235, raises TimeoutError. Native arguments were unchanged; coverage was not requested and is not claimed.

### The required branch selection completed with two passing native checks and two inapplicable bindings.

Default profile python_review. Ruff format and lint each exit0 on the selected two changed Python test files. Production-scoped Mypy and Pyright report not_executed/not_applicable because no production Python changed. No tool policy, exclusions or quality arguments were modified.

**Sources:**

- [Workspace selection](<../../../.pgmcp/config/checks.yaml>)
- [Binding defaults](<../../../.pgmcp/config/defaults/checks.yaml>)

**Invocation:** run_checks(scope='branch', timeout_seconds=900)

**Observed Result:** run_status=passed; python_format passed; python_lint passed; python_types and python_pyright not_executed/not_applicable. These two type bindings are not reported as executed passes.

### A single focused repeat does not resolve the full-suite failure.

Read-only inspection shows a one-second invocation deadline is established before Node/child readiness, while wait_for_children separately waits up to five seconds for both PID files. The failed full run never reached the result/termination assertions. This is a concrete scheduling-sensitive arrangement, not proof of the actual runtime outcome in that failed execution. The file was unchanged on #536; its latest prior edit is #517 commit e2e7ba7d.

**Sources:**

- [Lifecycle readiness and case](<../../../tests/mcp_server/integration/execution/test_process_stopping.py>)
- [Invocation deadline](<../../../mcp_server/execution/process_runtime.py>)

**Invocation:** run_tests(scope='targets', targets=['tests/mcp_server/integration/execution/test_process_stopping.py'], tests=['python_tests'], args={'python_tests':['-k','test_failure_stops_live_children_and_keeps_primary_cause and late-timeout']}, timeout_seconds=180)

**Observed Result:** 1 passed in 93.41s, native exit0, eight workers and unchanged native timeout logic. The preceding attempt to put a pytest node ID in targets was rejected before execution with scope_resolution_failed/missing; file target plus native -k is the admitted route. Neither result replaces the failed required suite.

## Preservation

The final status check showed only .pgmcp/state.json changed by the legitimate phase transition; no production/test/config/planning mutations or untracked files. Active environment, server settings, owner configuration, checkpoints/backups and preliminary downloadable wheel were preserved.

## Containment

No repair, timeout increase, exclusion, new skip, suppression, test addition or second full-suite run was performed. The negative suite result remains authoritative. Diagnosis is limited to the failing existing case and read-only runtime/test inspection.

## Failures

- Required configured suite: unresolved lifecycle readiness timeout in test_failure_stops_live_children_and_keeps_primary_cause[late-timeout]. A targeted pass does not establish cause or repair and does not permit Documentation progression.

## Caveats

- The archive link check remains the independently accepted historical baseline: 1215 occurrences, 1011 successful, 201 excluded, same three errors, native exit1 before and after archival. The separate active-document check passed. This is not a gate waiver.
- Existing package/install evidence remains bound to its reported source/artifacts. A definitive 4.0.0 wheel/sdist must be built and verified from the later selected integrated source before owner publication approval.
- Release notes and migration instructions remain planned Documentation work. No production defect is established by the current traceback; its runtime result was not captured by this failing test path.

## Deferred Work

### Three existing historical archive links point to removed sources/anchor; no new deferral or follow-up issue was created.

The owner-approved archive preserves historical evidence rather than rewriting it to current code. Impact is limited to navigation in those historical reports; independent QA accepted the unchanged baseline for entering Validation. Coordination triage was not requested for this preserved debt.

**References:**

- [Archive baseline and scope](<test-wheel-preparation.md#source-workspace-archive-and-release-procedure--2026-10-21>)

## Related Documents

- [Implementation and live-install evidence](<test-wheel-preparation.md>)
- [Live observations](<live-observations.md>)
- [Release procedure](<../../reference/release-assets-procedure.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-21 | @imp validator | Record required native suite/branch outcomes, bounded lifecycle diagnosis and the unresolved Validation blocker. |
