<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue \#536 — Validation of the 4.0.0 candidate

**Status:** Completed with owner-accepted known risk; independent GO for Documentation  
**Version:** 0.3  
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

PARTIAL

The native configured suite remains FAIL (exit1). The owner accepted its known
readiness failure as non-blocking for #536, tracked by #533; independent QA owns
the phase verdict. No all-tests-passed claim is made.

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

No repair, timeout increase, exclusion, new skip, suppression, test addition or second full-suite run was performed. The negative suite result remains authoritative. Diagnosis is limited to the failing existing case, read-only runtime/test inspection and comparison with the existing #533 tracking and prior #529/#528 evidence.

## Failures

- Required configured suite: unresolved lifecycle readiness timeout in test_failure_stops_live_children_and_keeps_primary_cause[late-timeout], native exit1. The owner-approved non-blocking disposition and existing #533 follow-up are recorded below. A targeted pass does not establish cause or repair; independent QA decides phase progression against the explicit owner decision.

## Caveats

- Independent QA reviewed the native results, matching #529/#528 history and the owner's explicit disposition, and gave GO for Validation → Documentation on exact pushed commit 1b2c9787c8b80dfbb1556a257c90ba38b75452bf (review turn 01a15f35-9376-7341-b3ce-fcf40dc91e63). Native FAIL/PARTIAL and the open #533 risk remain unchanged; publication is not approved by this verdict.
- The archive link check remains the independently accepted historical baseline: 1215 occurrences, 1011 successful, 201 excluded, same three errors, native exit1 before and after archival. The separate active-document check passed. This is not a gate waiver.
- Existing package/install evidence remains bound to its reported source/artifacts. A definitive 4.0.0 wheel/sdist must be built and verified from the later selected integrated source before owner publication approval.
- Release notes and migration instructions remain planned Documentation work. No production defect is established by the current traceback; its runtime result was not captured by this failing test path.

## Deferred Work

### Known Windows lifecycle readiness risk — tracked by #533

The current failure has the same test ID and readiness wait as the retained
#529/#528 failures: `test_failure_stops_live_children_and_keeps_primary_cause[late-timeout]`
times out waiting for child PID files before the stop-result assertions.
The [#529 record](../archive/issue529/validation.md#failures) and
[#528 record](../archive/issue528/validation.md#failures) retain those negative
observations. The [#528 caveats](../archive/issue528/validation.md#caveats)
also record independent QA's prior non-blocking disposition for that issue.
This is a matching failure signature, not proof of an identical underlying cause.

[Open epic #533](https://github.com/MikeyVK/phase-gate-mcp/issues/533) explicitly
owns investigation of recurring Windows child-process readiness and its still
unknown timing cause. On 2026-10-21 the owner reviewed this match and approved
keeping repair under #533 while treating this recurrence as non-blocking for #536.
This is an explicit, issue-specific acceptance disposition for the recorded
failure; it does not change the native exit1, global quality policy, test selection
or any other release/publication approval requirement. The targeted pass is not
the basis for declaring a fix or a green full suite.

Impact: the failed execution does not prove its intended child-stop assertions;
this run supplies no demonstrated production regression. The timing risk remains
unresolved and visible. Existing test/runtime code is unchanged on #536.
Follow-up/triage state: #533 is open under Coordination's epic ownership; this
recurrence is indexed here, with no duplicate issue, child creation or #533
implementation on this branch. Independent QA must assess the Validation exit
using this owner decision and the unchanged native evidence.

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
| 0.2 | 2026-10-21 | @imp validator | Link the matching prior readiness failures and open #533; record the owner's issue-specific non-blocking disposition without changing native outcomes or quality policy. |
| 0.3 | 2026-10-21 | @imp documenter | Record the independent Validation exit GO while preserving native failure, accepted risk and publication boundaries. |
