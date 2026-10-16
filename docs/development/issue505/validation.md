<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue 505 — Asset assembly validation

**Status:** VALIDATION — FAIL, QA REVIEW REQUESTED  
**Version:** 0.1  
**Last Updated:** 2026-10-16

## Purpose

Record corrected builder behavior and the actual required full-suite outcome without waiving unrelated failures.

## Scope In

The approved C_1 builder correction, public behavior tests, complete native suite and configured branch/production gates.

## Scope Out

No runtime/configuration test migration, release/version bump, repository asset build or deployment.

## Issue Number

#505

## Cycle

C_1

## Validation Status

FAIL

## Scope

Implementation snapshot db50b1d868e6b0506bda32c07b71cc4a67b07b8d; bug/505-fail-closed-asset-assembly; main parent. Research GO f5125b9c, Design GO4c119786, Planning GOed653fbb and Implementation GOdb50b1d8. Only scripts/build_package.py and its existing unit module changed in production/test code.

## Obligations

### D\_1.1 — fail\_closed\_assembly

**Evidence:**

- [Builder](<../../../scripts/build_package.py>)
- [Builder behavior tests](<../../../tests/mcp_server/unit/test_build_package.py>)

**Outcome:** Focused proof passes: shared admission before effects, explicit roots, no source/output overlap or indirect output, original exceptions with operation/path notes, no assembly success/build after failure.

### D\_1.2 — assembly\_behavior\_evidence

**Evidence:**

- [Builder behavior tests](<../../../tests/mcp_server/unit/test_build_package.py>)

**Outcome:** 29 public behavior cases pass. Real temporary files/directories/links and required cleanup fault injection; no safety skip. Prior content/legacy assertion removed. External build is substituted in unit scenarios.

### Validation phase D\_1 — required complete evidence

**Evidence:**

- [Planning](<planning.md>)

**Outcome:** FAIL: full configured suite completed with71failed/80errors. Branch checks and configured production Mypy pass; they do not override failed tests.

## Evidence

### RED confirms the original causal failures

Initial changed module produced23failed/6passed/9warnings. Missing fields skipped, stale cleanup occurs before source validation, path/overlap/link guards absent, cleanup suppression and diagnostic gaps exposed. The first overlap proof recursively copied scratch into itself; the durable case now spies on that unsafe directory-copy action so admission must reject before it can recurse. No repository source/state was involved.

**Sources:**

- [Builder behavior tests](<../../../tests/mcp_server/unit/test_build_package.py>)

**Invocation:** run_tests(scope='targets', targets=['tests/mcp_server/unit/test_build_package.py'], tests=['python_tests'], timeout_seconds=180); then the changed overlap pair with args={'python_tests':['-k','overlap']}.

**Observed Result:** Initial RED23failed/6passed; stabilized overlap RED2failed with DID NOT RAISE ValueError. RED commit c6b7b018. Supplemental runs f54d6cea and2f1849da.

### Final focused behavior and file gates pass

After QA's sole test-evidence finding, the directory case creates child.txt and injects PermissionError through shutil.os.unlink beneath actual rmtree. It checks the original exception object, cleanup/path notes and preserved output. Reintroducing suppression would remove the expected exception. No new case or production edit was needed.

**Sources:**

- [Builder behavior tests](<../../../tests/mcp_server/unit/test_build_package.py>)

**Invocation:** run_tests(scope='targets', targets=['tests/mcp_server/unit/test_build_package.py'], tests=['python_tests'], timeout_seconds=180); run_checks(scope='targets', targets=['tests/mcp_server/unit/test_build_package.py'], checks=['python_format','python_lint','python_pyright'], timeout_seconds=600). Earlier same gates also covered scripts/build_package.py.

**Observed Result:** 29passed,9existing SchemaAttachment.schema-shadow warnings, native exit0,9.41s (358931d5). Final test file gates allpassed(dd6461c3); production+test gates allpassed before the test-only correction(b6a3bbfc). An intervening adapter_deadline_expired run with no output is incomplete, not a pass; healthy server check and the completed rerun supersede it.

### Required full native-configured suite completed and failed

Native pytest9.0.2, Python3.13.7, pyproject.toml defaults including8xdist workers;2947items. No caller args, no excluded failing scope and no coverage argument added or removed. Full result:71failed,2794passed,1skipped,1xpassed,253warnings,80errors in450.91s(7m30s), native exit1. None of the151 failure/error diagnostic blocks contains a builder stack. The installed-candidate init/migration/MCP-handshake integration test passed, exercising the real isolated staging/build consumer.

**Sources:**

- [Pytest native settings](<../../../pyproject.toml>)
- [Staged build consumer](<../../../tests/mcp_server/fixtures/installed_distribution.py>)
- [Installed candidate proof](<../../../tests/mcp_server/integration/test_target_startup.py>)

**Invocation:** run_tests(scope='configured', tests=['python_tests'], timeout_seconds=1200).

**Observed Result:** FAIL. Complete native suite, no deadline/termination failure. Supplemental operation85543f55296a4b9aa42746fcb2d40982. Operation DTO success means execution completed; it does not make the negative native test outcome a pass.

### Filtered branch gates pass

python_format,python_lint,markdown_links passed. python_pyright,python_types,yaml_configuration,json_schema_shape,json_schema_metaschema were not_executed/not_applicable because their configured branch selection had no applicable targets. These no-op rows are not represented as executed checks. Explicit C_1 Pyright covers both changed Python files.

**Sources:**

- [Workspace selection](<../../../.pgmcp/config/checks.yaml>)

**Invocation:** run_checks(scope='branch', checks=['python_format','python_lint','python_pyright','python_types','markdown_links','yaml_configuration','json_schema_shape','json_schema_metaschema'], timeout_seconds=600).

**Observed Result:** Branch run_status=passed (2cf22363), with the executed/not-applicable distinctions above.

### Required production-scoped Mypy passes

Native configured Mypy reports Success: no issues found in193source files. This is the configured mcp_server production scope, not an invented strict test-Mypy gate.

**Sources:**

- [Mypy native settings](<../../../pyproject.toml>)

**Invocation:** run_checks(scope='configured', checks=['python_types'], timeout_seconds=600).

**Observed Result:** passed, native exit0 (ab870828).

### Full-suite blockers are grouped, not silently assigned to this fix

The151native failure/error blocks have the following initial diagnosis. Counts describe observed diagnostics; they are not a reproduced baseline comparison.

| Observed family | Count | Evidence / remaining uncertainty |
| --- | ---: | --- |
| Missing defaults/contracts.yaml |107| make_project_manager/make_phase_state_engine loads explicit temporary config roots without a prepared basis; stack stops in ConfigLoader. |
| Old label list shape |14| LabelConfig or labels.yaml validation requires mappings; fixtures still supply dash-list collections. |
| Old milestone list shape |1| test_milestone_accepted_when_milestones_yaml_is_empty passes milestones=[]; current model requires a mapping. |
| Missing defaults/checks.yaml |14| Activation/proposal/renewal preparation omits the new basis; failures include diagnostic assertions masked by that absence. |
| Missing defaults/github.yaml |2| isolated_target_env copies root *.yaml only and omits defaults/; bootstrap fails before tool assertions. |
| Missing defaults/adapters.yaml or artifacts.yaml |2| One selected adapter-root fixture and one artifact resolver fixture omit the required basis. |
| Other id/mapping consumers |3| Issue-type mock still exposes MagicMock.name rather than id; planning tests iterate mapping keys as phase objects/dictionaries. |
| Renewal CLI return-code assertions |7| Native excerpts show exit1 instead of expected0/2; exact individual subprocess causes have not been established. |
| Source-startup handshake timeout |1| initialize times out after startup logging; not a builder exception and not yet causally classified. |

The first143diagnostics have concrete configuration/consumer symptoms; the7CLI exits and1handshake timeout still require cause investigation. Source inspection confirms missing basis/old shapes in the named fixtures. This issue has not run a main-baseline suite, and does not claim all151are independently proven pre-existing. No failed case has been waived, repaired or removed.

**Sources:**

- [Shared test config construction](<../../../tests/mcp_server/test_support.py>)
- [Phase fixture](<../../../tests/mcp_server/unit/managers/test_phase_state_engine.py>)
- [Label fixture](<../../../tests/mcp_server/unit/tools/test_label_tools.py>)
- [Milestone case](<../../../tests/mcp_server/integration/test_create_issue_e2e.py>)
- [Target startup fixture](<../../../tests/mcp_server/integration/test_target_startup.py>)
- [Activation fixture](<../../../tests/mcp_server/integration/test_template_activation.py>)
- [Renewal CLI cases](<../../../tests/mcp_server/integration/test_renewal_cli.py>)

**Invocation:** Read the required full run's native diagnostic windows and inspect the named unchanged test preparations; do not repeat the full suite solely for diagnosis.

**Observed Result:** All151failure/error blocks accounted for in the table;8still have unresolved individual causes. No scripts/build_package.py call in these151stacks.

## Demonstration

Use the public scratch scenarios in the existing builder module: invalid records or missing source preserve stale output and keep the external build uncalled; traversal/absolute/overlap/link/hardlink attempts preserve outside sentinels; real cleanup denial escapes with original diagnosis; valid separate staging retains hidden files; successful scratch orchestration proves copied bytes and stale removal before one external build call. The exact focused invocation above reproduces these outcomes without touching repository assets.

## Preservation

Existing public helper signatures and assets/source/target mapping shape retained. Valid separate source/stage roots and dotfiles work. Repository sources, workspace state and recovery data are outside disposable ownership. The full native suite includes a hermetic wheel build/install through its existing installed-candidate fixture; no repository release artifact, tag, upload or external rollout was created.

## Containment

Only the explicitly supplied generated root is disposable. Path admission rejects escaping/overlapping/indirect mappings, Windows reparse points and multiply linked output files. Native required IO failures abort; disposable partial output can remain. Static checks are not a hostile-concurrent-filesystem sandbox.

## Failures

- Required full configured test gate failed:71failed+80errors. Validation cannot progress under the current criteria.
- The8unclassified individual CLI/startup failures remain unresolved; the other143diagnostic families are identified but not repaired by this builder issue.

## Caveats

- No #504 targeted-only waiver is inherited. Passing focused tests/gates does not override the complete-suite failure.
- Full-suite skipped/xpassed/warning outcomes are retained in the summary; this issue does not change their policy or broadly clean warnings.
- No broad baseline rerun, test migration or production architecture change has been authorized as part of this validation result.

## Deferred Work

### Coordinate a bounded decision on the full-suite configuration/consumer failures and the8remaining individual causes.

These cross many unchanged fixture/runtime test surfaces outside the approved builder cycle. They block the required gate; a scope/repair decision or explicit owner exception must precede any progression.

## Related Documents

- [Approved Research](<research.md>)
- [Design](<design.md>)
- [Planning](<planning.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-16 | @imp validator | Record focused correction evidence and the required full-suite blocker with bounded diagnosis. |
