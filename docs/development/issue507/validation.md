<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue 507 — Validation

**Status:** FAIL — bounded test repair approval pending  
**Version:** 0.1  
**Last Updated:** 2026-10-16

## Purpose

Record durable native evidence and the exact blockers before any repair or phase progression.

## Scope In

Owner-approved harness repair, schema-field rename, Python 3.13/SDK 1.30 maintenance and bounded Ruff/typing changes on implementation commit e805b108be375ab909e700b39b17d97a12eaea8b.

## Scope Out

No gate waiver, compatibility bridge, SDK2 migration, higher Python floor, broad test rewrite or permanent diagnostic-test additions.

## Prerequisites

- Independent QA issued GO for Implementation → Validation on exact commit e805b108; full verdict read from QA turn01a146cb-9ad2-7ed1-a2d9-a67c5d084f2f.
- Source remains at the reviewed implementation commit; before this report only the normal Validation phase transition changed tracked state.

## Issue Number

#507

## Validation Status

FAIL

## Scope

Full native configured suite; branch python_review profile; configured production Mypy; changed-document offline links; live restart and resource read.

## Obligations

### Classify and repair harness diagnostics without blanket suppression or test expansion.

**Evidence:**

- [Implementation record](<research.md>)
- [Restart task behavior](<../../../tests/mcp_server/tools/test_admin_tools.py>)

**Outcome:** The full run reports no warnings, skip or XPASS; overall Validation remains failed because of the two existing config-coupled tests.

### Preserve schema/resource and existing typing contracts.

**Evidence:**

- [Schema transport](<../../../mcp_server/core/tool_execution.py>)
- [Central SDK boundary](<../../../mcp_server/server.py>)

**Outcome:** Focused191-test implementation run passed; full run has no failure at these surfaces. Seven local UP046 exceptions preserve specified variance/library behavior; strict plugin and one Mypy exception approved.

### Execute the complete native test selection without partitioning or argument substitution.

**Evidence:**

- [Native pytest settings](<../../../pyproject.toml>)

**Outcome:** Completed2914 cases with native exit1:2912passed,2failed in458.00s. Execution was not timed out or incomplete.

### Verify branch/source gates and refreshed live server.

**Evidence:**

- [Configured gates](<../../../.pgmcp/config/checks.yaml>)
- [Runtime handler](<../../../mcp_server/server.py>)

**Outcome:** Branch formatting/lint/Mypy/Pyright, configured production Mypy and changed-document link checks passed; fresh PID healthy and resource read retains requested URI/text/plain.

## Evidence

### Full native suite completed with two actionable failures.

2912passed/2failed in458.00s;8workers,2914items; no warnings/skip/XPASS reported. Native capture exit1, no termination problem, output not truncated. Supplemental receipt b646aae98e4e4a6991cd73b107634e46.

**Sources:**

- [Pyright behavior test](<../../../tests/mcp_server/integration/adapters/test_pyright.py>)
- [Rollout test](<../../../tests/mcp_server/integration/test_rollout_configuration.py>)

**Invocation:** run_tests(scope='configured',timeout_seconds=1200); selected python_tests, requested_targets=[], args_source='configured', effective_args=[]. Native pyproject arguments unchanged; client window1800.

**Observed Result:** FAIL

### Branch Python gates pass with native per-check branch selection.

Formatting41Python files; lint passed; Mypy29production files; Pyright29production files with0errors/0warnings. Native exits0; supplemental e08c629e07124658ad8da7fe81d1510e.

**Sources:**

- [Check bindings](<../../../.pgmcp/config/checks.yaml>)

**Invocation:** run_checks(scope='branch',timeout_seconds=600); selected default profile python_review; configured arguments.

**Observed Result:** PASS

### Configured workspace production Mypy passes.

Success: no issues found in191source files; native exit0. Supplemental0852896198dd41709de6a5d323757e43.

**Sources:**

- [Native Mypy settings](<../../../pyproject.toml>)

**Invocation:** run_checks(scope='configured',checks=['python_types'],timeout_seconds=600); no caller arguments.

**Observed Result:** PASS

### Changed-document offline link gate passes.

71occurrences/58unique,32successful,39excluded,0errors. External URLs are excluded by the existing offline policy, not verified online. Supplemental adb2ced9d9974e64956e38330c05abf5.

**Sources:**

- [Research](<research.md>)
- [Setup policy](<../../setup/README.md>)

**Invocation:** run_checks(scope='targets',targets=['README.md','docs/setup/README.md','docs/setup/dev-isolation.md','docs/development/issue507/research.md'],checks=['markdown_links'],timeout_seconds=180).

**Observed Result:** PASS

### Loaded server and resource connection refreshed after implementation.

health_check before restart: PID66008 healthy. restart_server returned success; after3.5s, health_check returned PID31008 healthy, uptime9.97s. get_work_context, git/issue/check/test tools work. read_mcp_resource for pgmcp://cache/runs/bbbcf149f57f4d8698d1e38d5d1d017d?offset=0&limit=2000 returned the same requested URI with text/plain. Installed/test environment metadata: Python3.13.7, MCP1.30.0, Pydantic2.11.7; package evidence is separate from product version3.0.0 in health output.

**Sources:**

- [SDK resource boundary](<../../../mcp_server/server.py>)
- [Supported dependency declarations](<../../../pyproject.toml>)

**Invocation:** health_check(); restart_server(reason='Issue #507 Validation...'); wait3.5s; health_check(); get_work_context(); read_mcp_resource(server='phase_gate_mcp',uri='<health cache URI above>').

**Observed Result:** PASS

## Demonstration

Live restart changed PID and preserved tool/resource use through the current client connection; the configured native suite exercised real internal runtime and adapter boundaries in isolated test workspaces.

## Preservation

No production edits during Validation. The two failures preserve the exact approved3.13 config; they demand obsolete3.11 repository contents. Other3.11 fixture values are deliberate native analyzer test inputs, not a server compatibility promise.

## Containment

Only the phase transition changed tracked state before this report. Repairs must return to Implementation. A force transition requires explicit human approval; no approval is inferred from QA GO or elapsed time.

## Failures

- tests/mcp_server/integration/adapters/test_pyright.py::test_native_configuration_preservation_and_editor_target, line577: asserts repository config pythonVersion=='3.11'. The subsequent native-versus-adapter/version-override behavior is valuable; proposed repair isolates its explicit scenario config instead of inheriting the live repository's Python baseline.
- tests/mcp_server/integration/test_rollout_configuration.py::TestRolloutConfiguration::test_pyrightconfig_native_settings_preservation, line499: asserts the same3.11 repository value. This method executes no product behavior; proposed repair removes the content-only duplicate rather than updating another snapshot.

## Caveats

- Validation is FAIL despite passing quality gates. No full-suite pass, QA Validation approval or Ready claim.
- Native coverage was not requested; existing addopts contain no --cov. No numeric coverage claim.
- The temporary negative typing probes are diagnostic evidence and are not permanent suite additions or substitutes for the full run.
- The branch's implementation commit is local at this checkpoint; the new report records executed outcomes independent of cache availability.

## Risks

### Current repository settings are embedded in two test expectations, so approved deployment policy changes can invalidate unrelated tests.

Pending owner approval: isolate the genuine native-behavior scenario and remove the pure configuration snapshot, with no new test cases.

**Consequence:** Validation cannot progress until the bounded repair is reviewed and invalidated tests/full evidence rerun.

## Deferred Work

### MCP SDK2/higher Python assessment and substantive reassessment of global/local checker suppressions.

Explicitly deferred from507; #513 owns independent options, version-specific evidence and a human Approved Strategy. No automatic removal or permanent acceptance of current exceptions.

**References:**

- [Tracked follow-up513](<https://github.com/MikeyVK/phase-gate-mcp/issues/513>)
- [Approved current boundary](<research.md>)

## Related Documents

- [Approved strategy and implementation evidence](<research.md>)
- [Issue507](<https://github.com/MikeyVK/phase-gate-mcp/issues/507>)
- [Deferred assessment513](<https://github.com/MikeyVK/phase-gate-mcp/issues/513>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-16 | @imp validator | Record completed native full suite, two stale configuration-test failures, passing gates and live server refresh. |
