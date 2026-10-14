<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=KoFPQ3-cAAWFeesb -->

# Issue 319 — completed workspace validation

**Status:** CURRENT VALIDATION FAILED — TARGETED IMPLEMENTATION REPAIR REQUIRED  
**Version:** 0.3  
**Last Updated:** 2026-10-14

## Purpose

Record the current ce6a76b7 implementation attempt and preserve earlier checkpoint evidence as history. This producer report does not grant independent QA approval.

## Current attempt — 2026-10-14

Independent entry GO covered ce6a76b7d2f7c7c00ecd53054dfb3b902ab96bc1. run_tests(scope='configured', timeout_seconds=1200), without caller filters/argument overrides: 2936 items; 6 failed, 2928 passed, 1 skipped, 1 xpassed, 275 warnings; 321.22 seconds; native exit 1, no termination problem. Receipt e780297a74f0469a8708b945abc7a5ab is supplementary. Read the collection header and diagnostic windows after inspecting the 884584-character size.

Failures: test_c_loader_schema_structural.test_no_manager_imports_config_schema_directly flags GitHubManager importing GitHubSettings outside the established schema facade. Four test_project_plan_readback normal/forced cycle/phase cases reach the real PR-status gate with settings lacking credentials. test_server.test_call_tool_pre_enforcement_blocks_submit_pr_outside_ready_phase uses a dispatch helper that did not inject the new GitHub settings and also leaves PR status external. These cases fail before their intended deliverable/phase assertions. Proposed bounded repair: use the existing schema export, complete test-helper injection and explicitly isolate the external PR lookup in these existing tests. Do not weaken PR enforcement or restore identity/settings fallbacks.

run_checks(scope='branch', timeout_seconds=600) passed python_format, python_lint, python_types and python_pyright, native exit 0 each. Ruff0.15.6: 110 files formatted; Mypy1.19.1: 38 source files; Pyright1.1.408: 38 files, zero errors/warnings. Native configured arguments unchanged. Receipt 18d8546dea4542da9ddc25468cb5af96 is supplementary. This passing gate does not waive the six suite failures.

No production or test repair occurred in Validation. Return to Implementation after independent entry review; a fresh configured suite is required after correction. The new release remains explicitly postponed. Parent/head/PR-base and package-content changes remain deferred.

## Historical checkpoint — a5cdbcaa

The remaining revision-0.2 sections describe only the earlier a5cdbcaa snapshot, not the current failed attempt.

## Scope Out

Native-config assets/exporters, effective-source resolution, compatibility bridges, additional adapter protocols, publication, and repairs during Validation.

## Prerequisites

- Approved Research and compact maintenance design.
- Independent Implementation → Validation GO at a5cdbcaa after targeted review of the seven repairs; full Validation was intentionally not executed by QA.

## Issue Number

#319

## Validation Status

PASS

## Scope

Native lint G004/BLE001/SLF001, explicit configuration_choice across existing bindings and execution consumers, fresh-init ownership, exception diagnosis and bounded code/test cleanup. Chore workflow; no implementation cycles.

## Obligations

### Complete full native-configured test suite after final implementation.

**Evidence:**

- [Affected existing test expectations](<../../../tests/mcp_server/integration/test_ready_phase_enforcement.py>)

**Outcome:** Completed successfully after the repairs: 2931 passed, 1 skipped, 1 xpassed; native exit 0. No remaining test failures.

### Run the required branch quality profile.

**Evidence:**

- [Check declarations](<../../../.pgmcp/config/checks.yaml>)

**Outcome:** Passed format, lint, production Mypy and Pyright. Branch selection excludes the deleted old supervisor and filters targets per capability.

### Prove the activated native lint policy across its full configured selection.

**Evidence:**

- [Native Ruff policy](<../../../pyproject.toml>)

**Outcome:** Reuse the passed configured python_lint at 06187e57 for unchanged sources and native policy; current branch lint verifies all subsequently changed files. No temporary rule selectors or force-exclude.

### Inspect consumer scope, deferred work and evidence boundaries.

**Evidence:**

- [Research strategy](<research.md>)
- [Compact design](<design.md>)
- [Existing setup instructions](<../../setup/README.md>)

**Outcome:** No missed active configuration-choice execution consumer identified by bounded read-only preflight. Documentation reconciliation remains in its next phase.

## Evidence

### The required full suite completed without timeout.

Testpaths and eight-worker scheduling came from existing pyproject.toml; no marker filters, target narrowing, argument overrides or coverage flags. Read the collection header and native summary/diagnostic tail after checking the 851464-character size. Coverage is opt-in and was not measured. Receipt 03cfb18ffa6d411eb886da5c3f564e63 is supplementary. Historical first attempt at 06187e57: 2928 items, 7 failed, 2919 passed, 1 skipped, 1 xpassed, 280 warnings, 411.29 seconds, native exit 1; recorded in report revision 0.1 / commit 3251f25f.

**Sources:**

- [Native test policy](<../../../pyproject.toml>)
- [Test binding](<../../../.pgmcp/config/tests.yaml>)

**Invocation:** run_tests(scope='configured', timeout_seconds=1200)

**Observed Result:** Pytest 9.0.2 / Python 3.13.7: 2933 items; 2931 passed, 1 skipped, 1 xpassed, 289 warnings; 322.17 seconds; native exit 0; no termination problem; args_source=configured, effective_args=[]. The five additional cases since the first run belong to the separately approved safe-edit report matrix; the seven-failure repair added no cases.

### Required branch checks passed.

args_source=configured for every check; native arguments unchanged. python_pyright effective_args=['--level','warning','--warnings']; the other checks had no caller arguments. Removed target mcp_server/#Archief/supervisor_old.py was excluded by deletion. Receipt c1aae9b456b94e418445a2b0b68678de is supplementary.

**Sources:**

- [Branch selection declarations](<../../../.pgmcp/config/checks.yaml>)

**Invocation:** run_checks(scope='branch', timeout_seconds=600)

**Observed Result:** python_review: python_format, python_lint, python_types and python_pyright all passed, each native exit 0. Ruff 0.15.6 formatted selection: 78 files already formatted. Mypy 1.19.1: 33 source files. Pyright 1.1.408: 33 files, zero errors/warnings.

### Native stricter lint policy passes workspace-wide.

Earlier configured evidence at 06187e57 covers unchanged sources/native settings; the current branch checks cover later changed files. This is evidence reuse, not a claim that configured lint was repeated at a5cdbcaa. Receipt 2349b832417347ee80376b35e0cfc655 is supplementary.

**Sources:**

- [G004/BLE001/SLF001 activation](<../../../pyproject.toml>)

**Invocation:** run_checks(scope='configured', checks=['python_lint'], timeout_seconds=180)

**Observed Result:** Ruff 0.15.6: All checks passed; native exit 0; args_source=configured; effective_args=[].

### All seven earlier failures have targeted consumer repairs.

Implementation commit a5cdbcaa changes four existing test files only. run_tests(scope='targets', targets=the four sources below, tests=['python_tests'], timeout_seconds=300): 53 passed, 21 warnings, 6.91 seconds, native exit 0. Target lint/Pyright passed; one formatting difference was fixed and format/lint rechecked. Independent entry QA found no repair blockers. The full suite above confirms the repaired cases in configured scope. No production or test code was changed during this Validation attempt.

**Sources:**

- [Planning phase admission tests](<../../../tests/mcp_server/integration/test_ready_phase_enforcement.py>)
- [Git delete flow test](<../../../tests/mcp_server/unit/integration/test_all_tools.py>)
- [Cycle expectations](<../../../tests/mcp_server/unit/tools/test_cycle_tools_business_logic.py>)
- [Initialization expectations](<../../../tests/mcp_server/unit/tools/test_initialize_project_tool.py>)

## Preservation

Previously reviewed targeted evidence remains available in implementation commit bodies: scratch diagnosis at 06187e57, safe-edit report recovery at 24c24b91 and seven consumer repairs at a5cdbcaa. The current full suite supplies the required broader evidence; no failing tests are waived.

## Containment

The initial failed run stopped progression. Repairs occurred in Implementation, followed by independent entry GO and one fresh configured suite plus branch checks. Current runs completed with native exit 0 and no termination problem. No native configuration relaxation or test filtering was used.

## Failures

None remaining in the current required runs. Earlier failures and their completed repairs:

- Planning save/update (2): operation-appropriate StoredPlanningModel command returns replace stale get_project_plan mocks. Retain phase refusal, zero blocked command calls and returned-plan checks.
- Git deletion (1): use public BranchDeleteResult; check success, both statuses and the manager call. The old catch masked an invalid mock because success was not asserted.
- Invalid stored cycles (2): retain empty/missing exit_criteria, assert planning_stored_invalid with the original Pydantic field diagnosis, and compare complete branchstate before/after refusal.
- Bare initialization (2): assert exact original RuntimeError/OSError identity; existing wrappers retain error-presentation responsibility.

## Caveats

- One skip is the existing manual proxy test requiring RUN_MANUAL_TESTS; one non-strict xfail passed in the enforcement-runner test. No caller filters were used. These outcomes are disclosed, not counted as ordinary passed tests.
- Warnings include schema-field shadowing, collection-name collisions, synchronous functions with asyncio marks, Python pathlib deprecation, MCP resource-return deprecation, GitHub authentication deprecation, an unawaited restart-test coroutine and AnyIO cancellation-argument deprecation. These diagnostics did not change the current native exit 0; they remain disclosed housekeeping.
- Branch diff against main at a5cdbcaa contains 92 files, +5229/-4676, including approved maintenance, safe-edit report recovery and existing test migrations/removals. Raw line counts are not a claim of new behavioral scope.
- The restart-test diagnostic tail includes unobserved tasks raising mocked SystemExit(42) from tests/mcp_server/tools/test_admin_tools.py. Native exit remains 0; record this as test-harness housekeeping, not a new operational failure or a warning-free claim.
- Code snapshot is a5cdbcaa. Only workflow state and this report change after the completed runs.

## Deferred Work

### Reconcile active quality/configuration references and release notes in Documentation.

Scheduled next-phase work, not deferred implementation: explain whole-batch unresolved-setup refusal distinctly from normal execution stops; use one link to existing setup guidance where sufficient. Assess provisional v3.1.0 acknowledgement impact with owner before version/publication. Follow-up stays with @imp documenter; Coordination release/admin tracking remains pending.

**References:**

- [Quality reference](<../../reference/tools/quality.md>)
- [Adapter reference](<../../reference/execution-adapters.md>)
- [Server configuration](<../../reference/server-configuration.md>)
- [Version-scoped upgrade guidance](<../../setup/workspace-upgrade.md>)

### Existing warning and stale-marker housekeeping outside the seven required failure repairs.

Existing warnings, the non-strict xpass and mocked restart-task diagnostics do not fail the native run, but add diagnostic noise. Their source paths are retained for Coordination triage; fixing the async harness/deprecations is outside the owner-approved seven-failure repair. No new issue or separate follow-up has been assigned.

**References:**

- [Context-loaded test marks](<../../../tests/mcp_server/integration/test_context_loaded_enforcement.py>)
- [Existing xfail marker](<../../../tests/mcp_server/unit/managers/test_enforcement_runner_unit.py>)
- [Path handling warning source](<../../../mcp_server/utils/path_resolver.py>)
- [Restart test harness](<../../../tests/mcp_server/tools/test_admin_tools.py>)

## Related Documents

- [Issue 319](<https://github.com/MikeyVK/phase-gate-mcp/issues/319>)
- [Approved Research](<research.md>)
- [Compact design](<design.md>)
- [Architecture failure boundary](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-13 | @imp validator | Record completed full native suite, passing branch and configured lint gates, seven remaining failures and bounded follow-up. |
| 0.2 | 2026-10-13 | @imp validator | Record current passed configured suite and branch gates after seven targeted consumer repairs; preserve failed-attempt history and diagnostic limitations. |
| 0.3 | 2026-10-14 | @imp validator | Record six current suite failures and passing branch checks at ce6a76b7; bound proposed schema/test-wiring repair and distinguish historical evidence. |
