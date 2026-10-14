<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=KoFPQ3-cAAWFeesb -->

# Issue 319 — completed workspace validation

**Status:** VALIDATION COMPLETE — INDEPENDENT REVIEW REQUIRED  
**Version:** 0.4  
**Last Updated:** 2026-10-14

## Purpose

Record final workspace evidence for implementation 18095d0e0b6055b3fa1f4680298999947e444b8a after independent entry GO. Preserve failed attempts and their repairs as history. This producer report does not grant independent QA approval.

## Scope Out

The new release is explicitly postponed: no version bump, release artifact preparation, tags or publication. Parent/head/PR-base contracts, state-mutator redesign, release-manifest content policy, native-config assets and broad test-harness housekeeping remain outside this closeout. See [the scope and deferred index](deferred.md).

## Prerequisites

Approved Research v0.11, compact design v0.6, owner-directed scope cap and independent Implementation → Validation GO at 18095d0e. No production/test repairs occurred during this final Validation run.

## Issue Number

#319

## Validation Status

PASS — required native runs completed; independent phase review requested.

## Scope

Native G004/BLE001/SLF001 maintenance; configuration_choice admission across existing check/test/fix/content routes; fresh-init acknowledgement reset; approved exception/CLI/renewal diagnosis; safe-edit report recovery; explicit GitHub settings injection; bounded status/config fallback and active document-portability repairs. Chore, without implementation cycles.

## Obligations

| Obligation | Observed outcome |
| --- | --- |
| Full native-configured test suite after final implementation | 2936 collected: 2934 passed, 1 skipped, 1 xpassed; native exit 0. |
| Required branch quality profile | python_format, python_lint, python_types and python_pyright passed; native exit 0 each. |
| Stricter lint policy across configured selection | Reuse passed configured python_lint at 06187e57 for unchanged sources/policy; final branch lint covers subsequent changes. No rule override or force-exclude. |
| Consumer and boundary review | Independent entry review plus targeted config/status/startup and repair evidence; no stale ConfigLoader template-root arguments found in the bounded source/embedded-script inventory. |
| Deferred work and release boundary | Explicit in deferred.md; Coordination owns follow-up triage. Release postponed, no publishing/build changes. |

## Evidence

### Complete configured test suite

Invocation: `run_tests(scope="configured", timeout_seconds=1200)`.

Python 3.13.7 / Pytest 9.0.2, native pyproject.toml testpaths and eight-worker scheduling. No caller target/marker filters, native argument overrides or coverage flags. Observed: **2934 passed, 1 skipped, 1 xpassed, 283 warnings; 311.68 seconds; native exit 0**, no termination problem; args_source=configured, effective_args=[].

Read the collection header and native diagnostic tail after checking the 851440-character result size. Receipt f04f4e3a5bb74fd187eab663a7f29ee8 supplements these durable invocation/outcome facts; it is not the sole evidence.

Sources: [native policy](../../../pyproject.toml), [test binding](../../../.pgmcp/config/tests.yaml).

### Required branch checks

Invocation: `run_checks(scope="branch", timeout_seconds=600)`, selected profile python_review.

| Check | Native outcome |
| --- | --- |
| python_format | Ruff 0.15.6: 112 files already formatted; exit 0. |
| python_lint | Ruff 0.15.6: All checks passed; exit 0. |
| python_types | Mypy 1.19.1: 39 source files, no issues; exit 0. |
| python_pyright | Pyright 1.1.408: 39 files, zero errors/warnings; exit 0. |

args_source=configured throughout. Pyright effective_args=['--level','warning','--warnings']; other checks effective_args=[]. The deleted old supervisor is removed from branch selection by deletion, not an exclusion change. No termination problem. Read the complete small result; receipt 6df86c87a79645dda3c762b7febc1961 is supplementary.

Sources: [bindings/branch policies](../../../.pgmcp/config/checks.yaml), [strict native rules](../../../pyproject.toml).

### Focused evidence and six-failure repair

At ce6a76b7, the configured suite completed with 6 failed, 2928 passed, 1 skipped, 1 xpassed, 275 warnings; 321.22 seconds; native exit 1. Its branch gates passed. Report revision 0.3 / ce0fa6ab preserves this failed checkpoint.

The failures were one existing schema-facade guard, four planning-readback matrix cases and one Ready-refusal test. Repair 18095d0e exports the same GitHubSettings type through the existing facade, supplies settings.github in the dispatch helper and locally mocks only the external public PR-status lookup in the existing integration/Ready tests. Production gates, their order and existing state/deliverable/refresh assertions remain. No new tests/cases/files.

Invocation: `run_tests(scope="targets", targets=[tests/mcp_server/unit/config/test_c_loader_schema_structural.py, tests/mcp_server/integration/test_project_plan_readback.py, tests/mcp_server/unit/test_server.py], tests=["python_tests"], timeout_seconds=600)`: **33 passed, 47 warnings, 37.56 seconds; native exit 0**. Target format/lint/Pyright on five changed Python files and Mypy on two production sources passed. The final full suite above confirms the repair in configured scope.

Earlier implementation evidence remains: b1069a55 GitHub repair (115 passed); ce6a76b7 config/status/startup/CLI selection (58 passed, 9 warnings, 14.36 seconds) and focused format/lint/Pyright/Mypy plus Markdown links. All are bounded evidence, not substitutes for the final suite.

## Preservation

Earlier checkpoints remain in Git: revision 0.1 / 3251f25f recorded seven failures; revision 0.2 / c4e4155a recorded 2931 passed, 1 skipped, 1 xpassed at a5cdbcaa after their repair. Those outcomes apply only to their own snapshots. Current evidence above covers the final identity/fallback/test-wiring implementation.

## Containment

Failed Validation stopped progression. Repairs occurred only after independent entry GO back to Implementation; independent re-entry GO preceded the final complete configured rerun and branch gates. No failing tests were waived, selection narrowed or native policy weakened. After the final runs, only the expected phase-state edit was modified; no test-created source/deliverables mutation was reported by git_status.

## Failures

None remaining in the current required runs. Completed consumer repairs and the prior failed attempt are retained above, not recast as successful runs.

## Caveats

- One existing manual skip and one non-strict xpass remain disclosed; neither is counted as an ordinary passed test. No caller filters were used.
- Warnings include schema-field shadowing, collection-name collisions, async marks, deprecations and an unawaited restart-test coroutine. Native exit is 0; this is not a warning-free claim.
- The diagnostic tail still contains mocked restart tasks raising SystemExit(42) from [admin-tool tests](../../../tests/mcp_server/tools/test_admin_tools.py). This remains test-harness housekeeping, not a new production failure.
- Coverage is opt-in and was not measured; no coverage percentage is claimed.
- GitHub startup/health availability does not bypass configured PR-status enforcement before branch mutations. Offline tests isolate that external lookup; production remains unchanged.
- Installed-distribution tests may build temporary test artifacts. No new release/version/tag/asset was prepared or published.
- Implementation snapshot is 18095d0e; subsequent report/phase/documentation changes do not claim new implementation evidence.

## Deferred Work

[deferred.md](deferred.md) is the single follow-up index: explicit parent/head/PR contracts; package-content/manifest policy; existing harness-warning housekeeping. It records sources, impact and Coordination triage. The formerly deferred status/config/document findings are implemented inside #319. The owner explicitly postponed the new release.

Remaining next-phase work: bounded active quality/setup/upgrade/Unreleased reconciliation, then independent Documentation/Ready progression. Do not reopen deferred production work.

## Related Documents

- [Research](research.md)
- [Compact design](design.md)
- [Scope and deferred work](deferred.md)
- [Setup](../../setup/README.md)
- [Architecture principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-13 | @imp validator | Record completed full native suite, passing branch and configured lint gates, seven remaining failures and bounded follow-up. |
| 0.2 | 2026-10-13 | @imp validator | Record current passed configured suite and branch gates after seven targeted consumer repairs; preserve failed-attempt history and diagnostic limitations. |
| 0.3 | 2026-10-14 | @imp validator | Record six current suite failures and passing branch checks at ce6a76b7; bound proposed schema/test-wiring repair and distinguish historical evidence. |
| 0.4 | 2026-10-14 | @imp validator | Record final passed configured suite and branch gates after bounded repair; retain failed checkpoints, caveats and explicit release/deferred boundary. |
