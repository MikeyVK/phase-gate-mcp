<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue \#537 — Validation

**Status:** Failed Validation — bounded recovery required  
**Version:** 0.1  
**Last Updated:** 2026-10-20

## Issue Number

#537

## Cycle

C_1

## Validation Status

FAIL

## Scope

Source candidate ce4b668bcd0cef0d3f934a66180413169b537121. Full native-configured suite and planned branch/workspace gates; source tests are isolated and active runtime was not switched.

## Evidence

### Full native suite is negative

The complete native configured run finished, without selection filters or weakened native arguments. 85 failed, 2996 passed in 486.12s, exit 1. This is FAIL, not a timeout or accepted exception.

**Sources:**

- [Shared public response helper](<../../../tests/mcp_server/integration/test_scaffold_public_v3.py>)
- [Schema query helper](<../../../tests/mcp_server/integration/test_schema_public_v3.py>)
- [Planning cache tests](<../../../tests/mcp_server/integration/test_project_plan_readback.py>)
- [Installed startup test](<../../../tests/mcp_server/integration/test_target_startup.py>)

**Invocation:** run_tests(scope='configured', tests=['python_tests'], timeout_seconds=1200)

**Observed Result:** 85 failed / 2996 passed; native exit 1.

### Branch and configured quality gates pass

Branch format/lint passed on 22 Python files; Pyright passed on eight production sources, no errors/warnings. Branch Markdown: 38 successful occurrences, two offline GitHub exclusions, zero errors; YAML passed. Configured format passed on 475 files, lint passed, Mypy passed on 192 production sources and Pyright passed on 192 with zero errors/warnings. Native exit 0 for each.

**Sources:**

**Invocation:** run_checks(scope='branch', checks=['python_format','python_lint','python_pyright'], timeout_seconds=600); run_checks(scope='branch', checks=['markdown_links','yaml_configuration'], timeout_seconds=600); run_checks(scope='configured', checks=['python_format','python_lint','python_types','python_pyright'], timeout_seconds=900)

**Observed Result:** All selected checks passed; the failed suite is not overridden by these checks.

## Demonstration

Failure classification from the native traceback: 73 failures stop at the same old cache-URI assertion in test_scaffold_public_v3.invoke; five stop at the old single-content/structured-attachment helper in test_schema_public_v3.invoke; six planning-readback cases expect an advertised cache URI despite default structured selection; one installed-startup case expects resource paging/URI and structured attachment bodies. These are missed test consumers of the approved contract. Preserve all valuable operation/write/cache assertions and adapt the shared transport assumptions; do not repair 85 cases individually or change production behavior to satisfy obsolete expectations.

## Preservation

C_1's focused proof remains recorded: intended final-cap RED (12032 >8000); 116 unit cases passed; first 13-file run 203 passed/4 failed, corrected via nine targeted cases; six additional composition/instance cases passed; QA corrections were proved through an existing long cached-recovery case (two intended cached failures then green), 82 affected cases passed and native production checks passed. Two initial import-cycle attempts and an earlier long-single-paragraph diagnostic probe were negative, not passes. The shared ResponseMode definition is in pure Settings to avoid an observed eager schema-export cycle; its imports now use that owner. No broad package-export cleanup or suppressions.

## Containment

No active runtime/profile switch, restart, installation replacement, external rollout or release. Current selected source and exact invocations are the durable evidence; cache run IDs are not required for reproduction. The native execution allowance is 1200s inside the existing 1800s client window, following the tracked setup policy; this corrects Planning's 1800s execution figure without filtering the full suite or changing native arguments.

## Failures

- Full suite: 85 failed / 2996 passed, exit 1. No gate waiver or phase progression.
- The original 14-file research inventory was a navigation index, not a complete transitive consumer inventory. Shared public test helpers exposed the additional coupling.

## Caveats

- Independent QA has admitted this candidate to Validation, not approved its failed Validation outcome.
- Coverage remains native opt-in. No new threshold, skip, native suppression or client/version matrix was introduced.
- Instruction truncation remains noted; final text cap does not bound structured data, attachment sizes or every client's model input.

## Deferred Work

### Return to Planning for a narrowly defined test-consumer correction cycle, then independent review, implementation and a new complete Validation run.

The committed C_1 plan stays unchanged; failed Validation is retained as evidence.

### After accepted \#537 merge, Coordination integrates main into the preserved \#536 branch and resumes owner-observed acceptance/release.

No #536 branch work or release publication belongs to this refactor.

## Related Documents

- [Planning](<planning.md>)
- [Design](<design.md>)
- [Research](<research.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-20 | @imp validator | Preserve the failed complete native run, passing gates, causal helper classification and required recovery without a waiver. |
