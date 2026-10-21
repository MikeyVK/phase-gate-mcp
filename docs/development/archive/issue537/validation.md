<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue \#537 — Validation

**Status:** Validation completed — independent review requested  
**Version:** 0.2  
**Last Updated:** 2026-10-21

## Issue Number

#537

## Cycle

C_1 and bounded C_2

## Validation Status

PASS

## Scope

Final source/test candidate 9e85bbdc524dc86c6fa05f4a08e3d9443a79392c after independently admitted C_2. Full native-configured suite and planned branch/workspace gates; source tests are isolated and active runtime was not switched. The earlier failed candidate ce4b668b remains recorded below.

## Evidence

### Repaired candidate: complete native suite passed

**Invocation:** run_tests(scope='configured', tests=['python_tests'], timeout_seconds=1200), no caller argument override; native discovery/addopts and eight workers retained.

**Observed Result:** 3081 passed in 546.48s (9m06s), native exit 0. No failed/skipped/xfail/warning summary. Captured stderr retained two child_exited lifecycle notices; these did not change native success. The 85 failures from the first full run are resolved on the repaired candidate.

### Refreshed final gates and reused production typing

**Invocations:** run_checks(scope='branch', checks=['python_format','python_lint','python_pyright'], timeout_seconds=600); run_checks(scope='branch', checks=['markdown_links','yaml_configuration'], timeout_seconds=600); run_checks(scope='configured', checks=['python_format','python_lint'], timeout_seconds=900).

**Observed Result:** All selected checks passed, native exit 0. Branch Ruff format covered 25 Python files, lint passed; Pyright covered eight changed production files with zero errors/warnings. Markdown reported 45 successful occurrences, two native offline GitHub exclusions, zero errors; YAML passed. Configured Ruff format covered 475 files and lint passed.

The earlier required configured python_types/python_pyright proof is reused: Mypy passed all 192 production files; Pyright analyzed 192 with zero errors/warnings, both exit 0. Read-only git diff ce4b668bcd0cef0d3f934a66180413169b537121 HEAD -- mcp_server .pgmcp/config pyproject.toml pyrightconfig.json was empty, so C_2 did not invalidate that native policy/source evidence. A fresh branch Pyright also passed. No gate exception was requested.

### Earlier full native suite was negative

The complete native configured run finished, without selection filters or weakened native arguments. 85 failed, 2996 passed in 486.12s, exit 1. This is FAIL, not a timeout or accepted exception.

**Sources:**

- [Shared public response helper](<../../../../tests/mcp_server/integration/test_scaffold_public_v3.py>)
- [Schema query helper](<../../../../tests/mcp_server/integration/test_schema_public_v3.py>)
- [Planning cache tests](<../../../../tests/mcp_server/integration/test_project_plan_readback.py>)
- [Installed startup test](<../../../../tests/mcp_server/integration/test_target_startup.py>)

**Invocation:** run_tests(scope='configured', tests=['python_tests'], timeout_seconds=1200)

**Observed Result:** 85 failed / 2996 passed; native exit 1.

### Branch and configured quality gates pass

Branch format/lint passed on 22 Python files; Pyright passed on eight production sources, no errors/warnings. Branch Markdown: 38 successful occurrences, two offline GitHub exclusions, zero errors; YAML passed. Configured format passed on 475 files, lint passed, Mypy passed on 192 production sources and Pyright passed on 192 with zero errors/warnings. Native exit 0 for each.

**Sources:**

**Invocation:** run_checks(scope='branch', checks=['python_format','python_lint','python_pyright'], timeout_seconds=600); run_checks(scope='branch', checks=['markdown_links','yaml_configuration'], timeout_seconds=600); run_checks(scope='configured', checks=['python_format','python_lint','python_types','python_pyright'], timeout_seconds=900)

**Observed Result:** All selected checks passed on the earlier candidate; those checks did not override its failed suite.

## Demonstration

Failure classification from the native traceback: 73 failures stop at the same old cache-URI assertion in test_scaffold_public_v3.invoke; five stop at the old single-content/structured-attachment helper in test_schema_public_v3.invoke; six planning-readback cases expect an advertised cache URI despite default structured selection; one installed-startup case expects resource paging/URI and structured attachment bodies. These are missed test consumers of the approved contract. Preserve all valuable operation/write/cache assertions and adapt the shared transport assumptions; do not repair 85 cases individually or change production behavior to satisfy obsolete expectations.

## Deliverable and strategy mapping

| Obligation | Evidence and boundary |
| --- | --- |
| D_1.1: mode/config/carriers | Existing config/settings and envelope cases prove required shared default, per-process selection, invalid selection and independent attachment references. ResponseMode lives once in pure Settings to avoid the measured import cycle; consumers import its actual owner. |
| D_1.2: bounded delivery/attachments | Existing limiter, real SDK and attachment tests prove final UTF-8 cap including footer/fence handling, full structured rendering, resource readback, native attachment bodies and metadata-only references. |
| D_1.3: error/cleanup evidence | Existing poisoned serializer and recovery cases prove no second full serialization after prior publisher serialization failure, distinct cache storage failure, truthful outcome and no execution/publication replay. Old matrix/JSON-text branches were removed. |
| D_2.1: public helpers | Real operation/cache/write/schema assertions remain. Native EmbeddedResource contents are compared with structured URI/MIME metadata; no obsolete mandatory cache footer under structured mode. |
| D_2.2: explicit cache proof | Both planning-cache setups select resource. Installed paging/schema context selects resource locally; later launch-isolation assertions retain their own structured environment. |
| Architecture/preservation | Tools/managers/adapters, operation DTOs, operation-only cache, paging and configured startup-recovery exception unchanged. No new reader, server presenter, harness knowledge, compatibility bridge, skip or suppression. |

Read-only remnant search over production, tests and shipped presentation defaults found no old selector/profile classes or independent channel/delivery fields. The C_2 diff contains only four test files and normal state audit; production/config/native checker files match ce4b668b exactly.

## Preservation

C_1's focused proof remains recorded: intended final-cap RED (12032 >8000); 116 unit cases passed; first 13-file run 203 passed/4 failed, corrected via nine targeted cases; six additional composition/instance cases passed; QA corrections were proved through an existing long cached-recovery case (two intended cached failures then green), 82 affected cases passed and native production checks passed. Two initial import-cycle attempts and an earlier long-single-paragraph diagnostic probe were negative, not passes. The shared ResponseMode definition is in pure Settings to avoid an observed eager schema-export cycle; its imports now use that owner. No broad package-export cleanup or suppressions.

## Recovery-cycle evidence

The audited return to Planning used the owner's standing backward-transition authorization. C_1 stayed unchanged; independent QA admitted the appended four-file C_2 and later approved its actual implementation at 9e85bbdc for Validation.

- Seven affected public/plan files: run_tests(scope='targets', targets=<seven files in Planning C_2>, tests=['python_tests'], args={'python_tests':['-n','0','--tb=short']}, timeout_seconds=600): 80 passed / 5 failed in 115.30s. Four remaining failures missed resource selection in the second setup; one new assertion incorrectly required a literal schema URI instead of the designed generic attachment notice.
- After correcting those five within the four-file boundary, run_tests(scope='targets', targets=['tests/mcp_server/integration/test_schema_public_v3.py','tests/mcp_server/integration/test_project_plan_readback.py'], tests=['python_tests'], args={'python_tests':['-n','0','--tb=short']}, timeout_seconds=300): 12 passed in 62.16s, exit 0. The other 73 successful public cases were not invalidated by these two-file changes.
- Installed startup scenario: run_tests(scope='targets', targets=['tests/mcp_server/integration/test_target_startup.py'], tests=['python_tests'], args={'python_tests':['-n','0','-k','test_installed_candidate_init_migration_and_mcp_handshake','--tb=short']}, timeout_seconds=300): 1 passed / 10 deselected in 127.21s, exit 0. Real isolated candidate installation, full paged-plan/hash comparison and native schema attachment readback retained.
- Format/lint on the four C_2 test files: passed, exit 0. No case deletion/skip and no production/default/native policy changes.

## Containment

No active runtime/profile switch, restart, installation replacement, external rollout or release. Current selected source and exact invocations are the durable evidence; cache run IDs are not required for reproduction. The native execution allowance is 1200s inside the existing 1800s client window, following the tracked setup policy; Planning v0.3 aligns that allowance without filtering the full suite or changing native arguments.

## Failures

- Earlier full suite: 85 failed / 2996 passed, exit 1. Preserved and causally corrected through C_2; no gate waiver.
- The original 14-file research inventory was a navigation index, not a complete transitive consumer inventory. Shared public test helpers exposed the additional coupling.

## Caveats

- Independent QA admitted the repaired candidate to Validation; final phase acceptance is requested against this report and current committed head.
- Coverage remains native opt-in. No new threshold, skip, native suppression or client/version matrix was introduced.
- Instruction truncation remains noted; final text cap does not bound structured data, attachment sizes or every client's model input.

## Deferred Work

### No remaining technical recovery cycle.

C_2 completed through independent phase gates and a fresh complete Validation. C_1 and negative history remain intact. Current reference updates still belong to Documentation.

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

| 0.2 | 2026-10-21 | @imp validator | Record bounded C_2 recovery, final full native result, refreshed gates and deliverable/strategy mapping while preserving all material negative evidence. |
