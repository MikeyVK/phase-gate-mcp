<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=KoFPQ3-cAAWFeesb -->

# Issue 319 — workspace validation and remaining test-contract failures

**Status:** FAILED VALIDATION — IMPLEMENTATION REPAIR REQUIRED  
**Version:** 0.1  
**Last Updated:** 2026-10-13

## Purpose

Record factual workspace evidence at implementation commit 06187e57b976749deecff1d2f2b9f7f3ee49cd04 after independent GO to enter Validation. This producer report does not grant independent QA approval.

## Scope Out

Native-config assets/exporters, effective-source resolution, compatibility bridges, additional adapter protocols, publication, and repairs during Validation.

## Prerequisites

- Approved Research and compact maintenance design.
- Independent Implementation → Validation GO at 06187e57; full Validation was intentionally not executed by QA.

## Issue Number

#319

## Validation Status

FAIL

## Scope

Native lint G004/BLE001/SLF001, explicit configuration_choice across existing bindings and execution consumers, fresh-init ownership, exception diagnosis and bounded code/test cleanup. Chore workflow; no implementation cycles.

## Obligations

### Complete full native-configured test suite after final implementation.

**Evidence:**

- [Affected existing test expectations](<../../../tests/mcp_server/integration/test_ready_phase_enforcement.py>)

**Outcome:** Completed; negative native result. Seven failures remain in four existing test files. Validation cannot close.

### Run the required branch quality profile.

**Evidence:**

- [Check declarations](<../../../.pgmcp/config/checks.yaml>)

**Outcome:** Passed format, lint, production Mypy and Pyright. Branch selection excludes the deleted old supervisor and filters targets per capability.

### Prove the activated native lint policy across its full configured selection.

**Evidence:**

- [Native Ruff policy](<../../../pyproject.toml>)

**Outcome:** Passed configured python_lint with existing native defaults; no temporary rule selectors or force-exclude.

### Inspect consumer scope, deferred work and evidence boundaries.

**Evidence:**

- [Research strategy](<research.md>)
- [Compact design](<design.md>)
- [Existing setup instructions](<../../setup/README.md>)

**Outcome:** No missed active configuration-choice execution consumer identified by bounded read-only preflight. Documentation reconciliation remains in its next phase.

## Evidence

### The required full suite completed without timeout.

Testpaths and eight-worker scheduling came from existing pyproject.toml; no marker filters, target narrowing, argument overrides or coverage flags. The result was read by bounded failure/summary windows after checking its 858868-character size, rather than downloading the whole cache. Coverage is opt-in and was not measured. Supplemental receipt 49df31355a554b42b5209d658c71c7bb is navigation only.

**Sources:**

- [Native test policy](<../../../pyproject.toml>)
- [Test binding](<../../../.pgmcp/config/tests.yaml>)

**Invocation:** run_tests(scope='configured', timeout_seconds=900)

**Observed Result:** Pytest 9.0.2 / Python 3.13.7: 2928 collected; 7 failed, 2919 passed, 1 skipped, 1 xpassed, 280 warnings; 411.29 seconds; native exit 1; no termination problem; args_source=configured, effective_args=[].

### Required branch checks passed.

args_source=configured for every check; native arguments unchanged. python_pyright effective_args=['--level','warning','--warnings']; the other checks had no caller arguments. Removed target mcp_server/#Archief/supervisor_old.py was excluded by deletion. Receipt 1253b8901178484798df5da52ee40701 is supplementary.

**Sources:**

- [Branch selection declarations](<../../../.pgmcp/config/checks.yaml>)

**Invocation:** run_checks(scope='branch', timeout_seconds=600)

**Observed Result:** python_review: python_format, python_lint, python_types and python_pyright all passed, each native exit 0. Ruff 0.15.6 formatted selection: 74 files already formatted. Mypy 1.19.1: 33 source files. Pyright 1.1.408: 33 files, zero errors/warnings.

### Native stricter lint policy passes workspace-wide.

This supplemental check closes the material acceptance gap between branch-only evidence and the issue's full selected native lint policy. Receipt 2349b832417347ee80376b35e0cfc655 is supplementary.

**Sources:**

- [G004/BLE001/SLF001 activation](<../../../pyproject.toml>)

**Invocation:** run_checks(scope='configured', checks=['python_lint'], timeout_seconds=180)

**Observed Result:** Ruff 0.15.6: All checks passed; native exit 0; args_source=configured; effective_args=[].

### The remaining test failures have concrete source routes.

Failures below were read from the completed native run and checked against current source. No production or test code was changed in Validation. The report is a repair hand-over, not an assertion that all failures are harmless.

**Sources:**

- [Planning phase admission tests](<../../../tests/mcp_server/integration/test_ready_phase_enforcement.py>)
- [Git delete flow test](<../../../tests/mcp_server/unit/integration/test_all_tools.py>)
- [Cycle expectations](<../../../tests/mcp_server/unit/tools/test_cycle_tools_business_logic.py>)
- [Initialization expectations](<../../../tests/mcp_server/unit/tools/test_initialize_project_tool.py>)

## Preservation

Previously reviewed targeted evidence remains available in implementation commit bodies, including the 59-test scratch outcome-conversion repair at 06187e57. The full suite now supplies the broader evidence that was deliberately reserved for this phase. Passing gates do not override seven failing tests.

## Containment

The failed native suite completed with exit 1, not timeout. No repair, native config relaxation, workflow forcing or phase progression was performed after discovering failures. Fresh full-suite evidence must be rerun after any implementation repair; other evidence may be reused while still valid.

## Failures

- Two failures: test_planning_commands_use_configured_phase_admission[False-planning-True] and [True-planning-True]. The manager mock configures get_project_plan, but save/update now return StoredPlanningModel directly. Their unconfigured command return values are MagicMock objects, rejected by PlanningDeliverablesOutput. Restore truthful command-return fixtures and retain admission/no-invocation assertions.
- One failure: TestGitToolsIntegration.test_git_delete_branch_tool_flow. Its delete_branch mock returns MagicMock rather than the current result contract; local_status and remote_status are rejected by the output schema. Inspect the actual manager contract and supply the appropriate public value object.
- Two failures: TestTransitionCycleExitCriteria.test_transition_blocked_when_current_cycle_missing_exit_criteria and ...has_empty_exit_criteria. StoredPlanningModel rejects these deliberately invalid persisted cycles in ProjectManager._stored_plan; PlanningMutationError('planning_stored_invalid') propagates before the later cycle criterion check. The tests expect the earlier tool-owned failure outcome. Resolve the current valid-planning/exception-boundary intent in Implementation; do not weaken the stored schema or add compatibility handling just to satisfy old expectations.
- Two failures: TestInitializeProjectToolMode1.test_error_handling_state_creation_failure and ...git_failure. Direct tool execution now propagates the injected OSError/RuntimeError under the approved wrapper-ownership policy; the tests still expect result.success=false from that bare tool. Adapt public exception/wrapper behavior evidence rather than restoring bespoke tool catches.

## Caveats

- One skip is the existing manual proxy test requiring RUN_MANUAL_TESTS; one non-strict xfail passed in the enforcement-runner test. No caller filters were used. These outcomes are disclosed, not counted as ordinary passed tests.
- Warnings include schema-field shadowing, collection-name collisions, synchronous functions with asyncio marks, Python pathlib deprecation, MCP resource-return deprecation, GitHub authentication deprecation, an unawaited restart-test coroutine and AnyIO cancellation-argument deprecation. They did not cause native exit 1; the seven listed failures did.
- Branch diff against main contains 86 files, +4518/-4300, including approved mechanical test migrations, test removal, existing manager/tool formatting changes, config declarations and tool-owned workflow records. Raw line counts are not a claim of new behavioral scope.
- Code snapshot is 06187e57. The phase-transition state and this report are the only subsequent mutations; no new implementation evidence is claimed.

## Deferred Work

### Reconcile active quality/configuration references and release notes in Documentation.

Scheduled next-phase work, not deferred implementation: explain whole-batch unresolved-setup refusal distinctly from normal execution stops; use one link to existing setup guidance where sufficient. Assess provisional v3.1.0 acknowledgement impact with owner before version/publication. Follow-up stays with @imp documenter; Coordination release/admin tracking remains pending.

**References:**

- [Quality reference](<../../reference/tools/quality.md>)
- [Adapter reference](<../../reference/execution-adapters.md>)
- [Server configuration](<../../reference/server-configuration.md>)
- [Version-scoped upgrade guidance](<../../setup/workspace-upgrade.md>)

### Existing warning and stale-marker housekeeping outside the seven required failure repairs.

Warnings are disclosed rather than expanding #319 into a dependency/runtime cleanup. A narrow check of touched asyncio marks and the xpassing old expectation is reasonable during repair; broader deprecation changes need Coordination triage. No new issue has been created and no separate follow-up has been assigned yet.

**References:**

- [Context-loaded test marks](<../../../tests/mcp_server/integration/test_context_loaded_enforcement.py>)
- [Existing xfail marker](<../../../tests/mcp_server/unit/managers/test_enforcement_runner_unit.py>)
- [Path handling warning source](<../../../mcp_server/utils/path_resolver.py>)

## Related Documents

- [Issue 319](<https://github.com/MikeyVK/phase-gate-mcp/issues/319>)
- [Approved Research](<research.md>)
- [Compact design](<design.md>)
- [Architecture failure boundary](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-13 | @imp validator | Record completed full native suite, passing branch and configured lint gates, seven remaining failures and bounded follow-up. |
