<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=WI5iXHBKVOU91bYE -->

# Issue \#522 — Workspace-bound Git implementation plan

**Status:** REVIEW REQUESTED  
**Version:** 1.0  
**Last Updated:** 2026-10-19

## Purpose

### Verification ownership

Implementation runs only affected tests and file gates. Use run_tests(scope="targets", targets=[the actual changed test files and directly affected helper-consumer cases], tests=["python_tests"], args={"python_tests":["-q", optional native "-k" selection]}, timeout_seconds=900). Targets are literal files/directories, not pytest node IDs. Preserve native parallelism and include existing behavior guards invalidated by the helper change.

Use run_checks(scope="targets", targets=[changed Python files], checks=["python_format","python_lint"], timeout_seconds=600). Typecheck changed production Python only with python_types/python_pyright on explicit targets; do not pass Markdown/state JSON or widen Mypy to test files. Use apply_fixes only for selected mechanical format/lint fixes. Reuse fresh evidence until later changes invalidate it.

Validation owns one complete native-configured run after the final source/test edit:

```python
run_tests(
    scope="configured",
    tests=["python_tests"],
    args={"python_tests": [
        "-q", "--junitxml=.pgmcp/temp/issue522/validation.xml"
    ]},
    timeout_seconds=1200,
)
```

Keep configured testpaths and native eight workers, with an outer client window covering execution, stopping and delivery as documented in docs/setup/README.md. No added coverage opt-in/gate from517, threshold change, skip, ignore or exclusion. Repeat complete evidence only after a real invalidation/failure correction, retaining the original result.

Also run run_checks(scope="branch", checks=["python_format","python_lint","python_pyright"], timeout_seconds=900) using existing per-check target policies, then run_checks(scope="configured", checks=["python_format","python_lint","python_types","python_pyright"], timeout_seconds=1200). Markdown uses targeted markdown_links. No YAML policy change is planned; check any legitimately changed YAML on its own applicable route.

### Phase completion

Each configured boundary requires independent read-only QA in existing chat01a0f779-c66e-7ec3-9335-a833bc22f013. Do not ask QA to execute the next phase in advance. A technical NOGO is repaired causally and re-reviewed. No forward force/gate exception.

Documentation updates the smallest complete current surface; no production/test edits. Ready reuses fresh evidence, scaffolds/submits the PR and sends Coordinatie01a013b6-356c-7f41-a0ad-ca30b843a991 the PR/head/base, exact evidence/verdicts and limits. Co owns merge and the next issue lifecycle.

## Scope In

Approved Research37fa53de and Design1.1 on18653784, including the corrected MCPSystemError → history unavailable contract.

## Scope Out

Issues518/523/524, multi-repository discovery/router, dynamic MCP roots, global environment mutation, workflow/config schema changes, release/build redesign and suite-wide cleanup.

## Prerequisites

- Independent Research→Design GO on37fa53de and Design→Planning GO on18653784.
- Selected Python3.15/MCP2.3 baseline and existing native pins. Before package tests verify build/setuptools/wheel already provisioned; missing environment prerequisite is not a product failure or reason to weaken assertions.

## Summary

One coherent cycle delivers Design1.1: explicit composition, adapter-owned exact/native selection, direct/shared consumer migration and public installed isolation evidence. No new architecture, config precedence, compatibility or active-host rollout.

## Dependencies

- D_1.1 supplies explicit identity to D_1.2; D_1.3 migrates construction and preserves history failure behavior; D_1.4 validates the integrated boundaries. They form one cycle because neither constructor/admission nor shared preparation is a standalone releasable policy.
- Keep file_exists validators honest: they prove artifact presence only. Public behavior/native outcomes and independent QA establish substantive acceptance.

## Work Units

### C\_1 — Selected-workspace Git correction

**Goal:** Remove independent Git repository selection while preserving lazy availability, domain/native policy and existing error contracts.

**Cycle Number:** 1

**Owner:** @imp implementer

#### Scope In

bootstrap.py, managers/git_manager.py, adapters/git_adapter.py; test_support and only affected direct/fixture cases; existing adapter/history/bootstrap/installed behavior families.

#### Scope Out

No extra consumer-specific validation in tools, new repository selector or generic cleanup.

#### Deliverables

##### D\_1.1

Require GitManager adapter and GitAdapter absolute path, remove adapter Settings/CWD fallbacks, and bind both existing bootstrap Git consumers to the same canonical selected workspace without eager Git acquisition.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/bootstrap.py"

##### D\_1.2

Implement lazy exact-root/nonbare/native-worktree admission, bounded inherited selector refusal including cached use, persistent git-dir/work-tree binding and unpublished-handle cleanup through existing MCPSystemError diagnostics.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/adapters/git_adapter.py"

##### D\_1.3

Adapt shared test composition/direct callers and invalid native mock preparation; remove the obsolete shallow default-constructor case, retain meaningful guards, and prove actual history failure cause plus manager unavailable behavior.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "tests/mcp_server/integration/test_git_cycle_evidence.py"

##### D\_1.4

Prove selected-target reads/mutations with foreign repository unchanged, absent/unsupported/nested/linked and native-conflict controls, ordinary Git policy, non-Git bootstrap and externally installed neutral/foreign-CWD operation using existing families.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "tests/mcp_server/integration/test_target_startup.py"

#### Exit Criteria

All D_1.1–D_1.4 pass focused public behavior and applicable file gates under Design1.1; selected-root Git/context/check consumers agree, controlled writes affect only the selected repository, native and history refusal preserves diagnosis/unavailable contracts, and no compatibility path, new router, unrelated cleanup or shallow/content/version test remains.

#### Obligations

- Inspect exact current seams; read applicable architecture/type rules before code. Add/adapt durable selected-target/native-conflict behavior tests before GREEN. Use disposable repositories A/B, never mutate the owner's nonselected repository to demonstrate the defect.
- Run a focused causal RED: bootstrap/public status from a foreign or neutral CWD must expose the current mismatch; inherited-context/history refusal supplies another meaningful control. Commit implementation/red cycle1 after observing the intended failure. Do not add a default-signature test solely to reject old construction.
- Implement minimal approved composition/native admission with no new loader/context/error hierarchy. Ordinary mutation wrappers stay unchanged; admission uses MCPSystemError so existing read_issue_history conversion and manager unavailable result remain intact.
- Update shared test_support once to supply explicit selected context; preserve explicit fakes for tests avoiding Git IO and real adapters for history/integration. Adapt invalid adapter mocks through reusable preparation; do not weaken root validation to accommodate them. Mechanical fixture migration needs no artificial RED.
- Use existing installed-distribution build/startup fixture; cover an external package, separate target and neutral/foreign launch roots. Supply isolated test credentials/policy and never depend on real network/GitHub identity. Prove selected mutation and B's unchanged observable state, not presence-only markers or source strings.
- Include meaningful exact-root/native/linked/nested/non-Git and history controls from Design; parameterize equivalent cases instead of building duplicate modules. Remove shallow test_init_default when superseded; keep valuable branch/commit/index/history/restore guards.
- Run focused affected tests and file format/lint/production typing gates, perform diff/behavior reality check, and commit GREEN cycle1. Refactor only if changed files require cleanup; rerun only invalidated evidence.
- Request independent Implementation→Validation review on the final coherent source snapshot. Do not enter Validation with stale/failing/incomplete behavior evidence.

#### Verification

##### D\_1.1–D\_1.2 selected root and fail-closed admission

**Method:** Existing adapter/bootstrap behavior with isolated exact/nested/linked and missing/container/subdirectory/bare/admin inputs, native overrides including after cached use, plus ordinary identity/config controls.

**Expected Result:** Correct target reads/writes or accurate refusal; no alternate mutation and original diagnosis/cleanup retained.

##### D\_1.3 history unavailable and focused consumers

**Method:** One existing history-family case exercises actual adapter cause and actual manager unavailable result; affected shared helpers/fakes and direct constructor callers execute their relevant behavior.

**Expected Result:** No new history exception escapes as a generic failure, no fabricated history facts and no setup depending on production fallback.

##### D\_1.4 installed public isolation

**Method:** Extend reusable installed candidate/source startup family through public MCP tools from neutral/foreign CWD with external roots and distinct selected repositories; compare foreign HEAD/index/files/refs around a controlled mutation.

**Expected Result:** Installed provenance and selected policy/root are observed; the nonselected repository is unchanged.

#### Stop Conditions

- Approved Strategy/Design contradiction or a genuinely new owner policy choice; do not silently redesign.
- Native behavior makes the selected boundary unsound or adequate proof requires release/host activation/scope expansion.
- A focused failure indicates lost actual behavior, an unclassified IO/cleanup problem or shared helper dependence; diagnose and repair in scope before claiming completion. New contractual gaps require reviewed planning/design correction, not skips or fake success.

## Phase Deliverables

### Validation

#### D\_1

Compact report maps exact native full-suite/branch/configured outcomes and installed/source isolation plus native/history refusal evidence to Design1.1; preserve negative attempts and operational limits.

**Owner:** @imp validator

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue522/validation.md"

### Documentation

#### D\_1

Reconcile current developer-isolation, configuration and applicable Git/setup references with exact-root selection, external roots, lazy refusal/native selectors and the validated neutral-CWD correction; historical artifacts remain unchanged.

**Owner:** @imp documenter

**Validates:**

**Type:** file_exists

**File:** "docs/setup/dev-isolation.md"

## Related Documents

- [Research / Approved Strategy](<research.md>)
- [Design1.1](<design.md>)
- [Architecture](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)
- [Execution budget policy](<../../setup/README.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-19 | @imp planner | Plan one causal correction cycle, proportional public coverage and phase-owned native acceptance. |
