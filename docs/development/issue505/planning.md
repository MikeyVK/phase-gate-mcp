<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=WI5iXHBKVOU91bYE -->

# Issue 505 — Bounded assembly safety planning

**Status:** PLANNING — QA REQUESTED  
**Version:** 0.2  
**Last Updated:** 2026-10-16

## Purpose

Execute the approved Design in one coherent behavior-correction cycle.

## Scope In

scripts/build_package.py, its existing unit test module, phase evidence and the active release-assets procedure.

## Scope Out

Manifest/content routing changes, runtime consumers, new error/transaction frameworks, release/deployment/version bumps and issues506–508.

## Summary

One cycle C_1 keeps the inseparable admission, cleanup/copy and orchestration invariants together. No migration or general fixture refactor is required. The existing isolated-staging caller remains unchanged.

## Dependencies

- Approved Research v0.2 and independent GO f5125b9c.
- Design v0.1 and independent GO4c119786.

## Risks

### Link/reparse creation differs across platforms.

Use real scratch symlink where supported and an explicit Windows junction fallback; verify the ownership case executes, not skip.

### Broad validation can reveal unrelated baseline issues.

Preserve exact findings; do not weaken the gate or expand into general cleanup. Discuss an actual policy exception if required.

## Milestones

- Implementation → Validation: independent QA checks C_1 completion and narrow evidence; QA does not execute the future full Validation in this gate.
- Validation: exactly one full native-configured test suite: run_tests(scope='configured', tests=['python_tests'], timeout_seconds=1200), preserving all native defaults and coverage options. A real timeout/incomplete run is not a pass.
- Validation: run_checks(scope='branch', checks=['python_format','python_lint','python_pyright','python_types','markdown_links','yaml_configuration','json_schema_shape','json_schema_metaschema'], timeout_seconds=600). Existing per-check configured branch filtering selects appropriate file types. No branch message check is invented.
- Validation: run_checks(scope='configured', checks=['python_types'], timeout_seconds=600) retains production-scoped Mypy. The changed builder/test files additionally retain their explicit Pyright evidence from C_1.
- Do not repeat the focused test run if the full native run exposes all builder scenarios and no later edits invalidate it. Record exact invocations, native outcomes, warnings, residuals and source snapshot in the compact validation report.
- Validation → Documentation: independent QA reads actual evidence. Required failures are FAIL; no imported #504 waiver or silent scope reduction.
- Documentation: update only the active assembly procedure's relevant order/ownership/failure passages and revision metadata; run targeted markdown_links on changed report/reference files, reuse fresh evidence otherwise.
- Documentation → Ready: independent QA. Then follow Ready instructions, submit PR closing only#505 and hand concrete merge request to Coordination. No self-merge or next issue.

## Work Units

### C\_1 — bounded\_assembly\_safety

**Goal:** Remove the evidenced fail-open behavior and enforce the explicit filesystem ownership boundary.

**Cycle Number:** 1

#### Scope In

Manifest shape/path/source preflight, generated-root cleanup safety, copy failure propagation, truthful orchestration, focused public behavior tests.

#### Scope Out

Any runtime/config-loader change, manifest grammar, broad test refactor, actual repository asset assembly/build or release.

#### Deliverables

##### D\_1.1

Correct scripts/build_package.py using shared manifest/path admission before effects, explicit disposable output, original-exception notes and no success/build after failure.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "scripts/build_package.py"

##### D\_1.2

Adapt the existing builder unit module to prove invalid-data, ownership/link, cleanup/copy error and valid staging/ordering/dotfile behavior through public functions; remove the legacy/content-only assertion.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "tests/mcp_server/unit/test_build_package.py"

#### Exit Criteria

All planned admission, ownership and IO-failure behavior is implemented; focused builder tests pass with no skips, original diagnostics and external staging/dotfiles are proved, and formatter/lint/Pyright pass on both changed Python files. No release/build of repository assets or runtime consumer rewrite.

#### Obligations

- RED: adapt tests/mcp_server/unit/test_build_package.py with stable corrected-behavior tests before production changes. Run the complete small module; failures must expose the planned defect rather than fixture errors. Commit sub_phase='red', cycle_number=1.
- GREEN: implement the approved local preparation/copy seams in scripts/build_package.py; preserve public signatures, valid external staging/dotfiles and original exception objects/details. Run the same small module; commit sub_phase='green', cycle_number=1.
- Planned cleanup: remove the old manifest-content/legacy assertion as part of meaningful behavior coverage. Avoid new permanent diagnostic probes and content snapshots. Refactor commit only if actual additional edits require it.
- Safety cases use tmp_path only, real cleanup/copy and real link/reparse evidence; inject faults at the OS/copy boundary and replace only the external build process. Windows junction fallback is confined to scratch and removed without following its target; no skipped ownership case.
- Pre-commit reality check: tests demonstrate actual state/diagnostics/build outcome through public functions; no source-string/private-helper tests and no repository state writes.

#### Verification

##### Focused corrected behavior and direct caller topology

**Method:** run_tests(scope='targets', targets=['tests/mcp_server/unit/test_build_package.py'], tests=['python_tests'], timeout_seconds=180). RED and GREEN; rerun only after relevant edits.

**Expected Result:** RED exposes planned defects; GREEN all scenarios pass without safety-case skips.

##### Python file quality

**Method:** run_checks(scope='targets', targets=['scripts/build_package.py','tests/mcp_server/unit/test_build_package.py'], checks=['python_format','python_lint','python_pyright'], timeout_seconds=600).

**Expected Result:** All selected checks pass on the changed Python files; no Markdown/JSON sent to explicit Python checks.

#### Stop Conditions

- A valid direct staging consumer needs a contract change not covered by Design.
- The fix needs a general transaction or configuration-content redesign.
- An apparent test failure comes from the harness rather than corrected behavior; repair setup before claiming RED.
- Any real repository source, state or recovery material changes during scratch proof.

## Phase Deliverables

### Validation

#### D\_1

Durable exact focused/full native-configured test and branch-check evidence, corrected behavior and preservation mapping, original diagnostics, outcome limits and independent-review navigation.

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue505/validation.md"

### Documentation

#### D\_1

Reconcile the active release-assets assembly procedure with admission order, disposable output and fail-closed exception behavior; no historical report rewrite or release claims.

**Validates:**

**Type:** file_exists

**File:** "docs/reference/release-assets-procedure.md"

## Related Documents

- [Design](<design.md>)
- [Approved Research](<research.md>)
- [Builder](<../../../scripts/build_package.py>)
- [Behavior tests](<../../../tests/mcp_server/unit/test_build_package.py>)
- [Quality evidence standards](<../../coding_standards/QUALITY_GATES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-16 | @imp planner | Plan one focused RED/GREEN cycle and phase-owned validation/documentation. |
| 0.2 | 2026-10-16 | @imp planner | Correct the full-suite execution budget to 1200 seconds within the approved 1800-second client window; selection unchanged. |

