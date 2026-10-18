<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=WI5iXHBKVOU91bYE -->

# Issue \#520 — Bounded startup implementation plan

**Status:** REVIEW REQUESTED  
**Version:** 1.0  
**Last Updated:** 2026-10-18

## Purpose

### Validation route

Run exactly one complete native-configured suite after the last production/test edit:

```python
run_tests(
    scope="configured",
    tests=["python_tests"],
    args={"python_tests": [
        "-q", "--junitxml=.pgmcp/temp/issue520/validation.xml"
    ]},
    timeout_seconds=1800,
)
```

Preserve native testpaths/parallelism and existing selected dependency pins. Coverage is opt-in in current pyproject.toml and is not made a new gate by this issue. This plan does not inherit #517's issue-specific extra90% gate.

Validation also runs run_checks(scope="branch", checks=["python_format","python_lint","python_pyright"], timeout_seconds=900) with the implemented per-check branch configured-target preselection, plus a final run_checks(scope="configured", checks=["python_format","python_lint","python_types","python_pyright"], timeout_seconds=1200). Markdown uses targeted markdown_links; the new YAML basis uses targeted yaml_configuration. Do not route documentation/state JSON through Python checks or broaden Mypy to tests.

After integration run one non-instrumented three-start observation with the actual30/0.25/60policy, report per-client healthy/catalog facts and timing, and retain the negative timeout/classification evidence from focused behavior controls. Verify the effective source/runtime rather than treating an orchestration receipt as proof of outcomes.

Record exact selections, native outcomes, material failures and reproduction facts in one compact validation.md; transient run IDs are supplemental. No separate permanent evidence suite.

### Documentation and Ready

Update only current server-configuration/config-loading/proxy/setup references needed for required basis/override, outer deadline, explicit migration, neutral diagnostics and complete proxy relaunch. Retain historical artifacts except this issue's authoritative deliverables. Existing assets mapping already includes config; no release_manifest/build redesign.

At each phase boundary request an independent GO/NOGO from existing chat QA (01a0f779-c66e-7ec3-9335-a833bc22f013, formerly Beoordeel designplan). QA remains read-only and does not pre-run the complete next phase. Repair technical findings within the approved boundary and re-review. After Ready use submit_pr and hand off to Coordinatie (01a013b6-356c-7f41-a0ad-ca30b843a991) for end-issue/merge; the implementation agent does not merge main.

## Scope In

Design1.0 on09e8eef: required defaults/server.yaml plus optional override through existing ConfigLoader;30s/0.25s lock policy;60s proxy deadline; truthful recovery; direct consumer/fixture migration and focused behavior evidence.

## Scope Out

Shared service, new loader/retry framework, activation waiting, compatibility/legacy preservation, broad test rewrite, dependency migration, release, active-host config switch or unrelated repairs.

## Prerequisites

- Independent Research→Design GO ondd4d146 and Design→Planning GO on09e8eef.
- The selected Python3.15/MCP2.3 toolchain and native checker pins from merged517 remain the evidence baseline. Verify actual native receipt/runtime identity; do not substitute stale host checker results.

## Summary

One coherent implementation cycle delivers the approved composed startup policy, bounded native locking and proxy/recovery integration. Focused behavior evidence precedes one Validation-owned complete native-configured run. The owner authorized autonomous completion through Ready and handoff to Coordinatie for merge.

## Dependencies

- D_1.1 defines the policy consumed byD_1.3; D_1.2 supplies bounded acquisition used byD_1.3; D_1.4 verifies the integrated boundary.
- Public bootstrap interfaces remain stable; direct proxy constructor call sites migrate through the single existing shared harness and explicit installed probe.
- No source activation is required to execute tests/checks against current files; use existing selected-runtime MCP orchestration when host tool identities differ. Tool calls remain via run_tests/run_checks/apply_fixes.

## Risks

### Native/source identity may differ from the active harness environment.

Inspect receipts and selected executable/tool versions; reuse the already installed Python3.15/MCP2.3 environment and existing MCP RPC route as needed. No active-host switch.

### Coverage/process instrumentation can lengthen functional startup.

Use explicitly labeled generous isolated test fixture budgets while preserving separate uninstrumented30/60second acceptance; never silently change defaults.

## Milestones

- Implementation→Validation independent QA on final C_1 snapshot.
- Validation→Documentation independent QA after complete required native evidence.
- Documentation→Ready independent QA, atomic PR submission and Coordinatie merge handoff.

## Work Units

### C\_1 — Configured bounded startup admission

**Goal:** Correct transient concurrent-start admission without weakening existing source/activation integrity.

**Cycle Number:** 1

**Owner:** @imp implementer

#### Scope In

Policy schema/read/basis; lock acquisition/time/error boundary; CLI/bootstrap/proxy/presenter integration; directly affected tests/fixtures.

#### Scope Out

Everything excluded by Scope Out; no unrelated cleanups or expansion of native checker policy.

#### Deliverables

##### D\_1.1

Add required immutable ServerConfig, public ConfigLoader read and defaults/server.yaml; prove basis/override admission and constraints through focused public behavior tests.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/config/schemas/server_config.py"

##### D\_1.2

Classify native contention separately from IO, remove unnecessary pre-lock byte write and add bounded startup acquisition with injected time; prove release, exhaustion and fresh-empty-file exclusion.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/services/template_activation.py"

##### D\_1.3

Load server policy before admission lock, inject proxy deadline without fallback, retain init/upgrade routing and neutral generic recovery projection; update only direct consumers and shared fixtures.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/core/proxy.py"

##### D\_1.4

Prove three concurrent clients, timeout/cause delivery and activation/recovery preservation on the selected baseline; complete focused formatting, lint and production typing checks with no legacy/content test additions.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "tests/mcp_server/integration/test_target_startup.py"

#### Exit Criteria

All D_1.1–D_1.4 behavior obligations pass focused native tests and applicable file checks; required server policy is the only timing source, three-client admission succeeds within selected budgets, native IO causes and activation/recovery integrity are preserved, no compatibility or unrelated cleanup remains, and pre-commit review confirms tests prove behavior rather than document/source contents.

#### Obligations

- Add/adapt valuable public behavior cases first and observe focused failure for the missing/new contract before GREEN. Commit meaningful RED and GREEN within C_1; mechanical constructor/fixture cleanup needs no artificial RED.
- Scaffold new production/config artifacts with the actual registered schemas; edit existing files with safe_edit_file. Use no raw file writes, pytest/linters or shell Git.
- Keep all policy fields required and frozen; retain existing ConfigLoader composition; preserve init/upgrade dispatch, stable lockfile/region and native causes.
- Keep immediate activation acquire/hold separate from normal startup acquire_with_wait; no per-code presenter or alternative timing source.
- Do not permanently assert exact tool count49 or implementation/source strings: verify complete healthy catalogs and representative ordinary capabilities through public MCP.49 is the observed Research catalog size.
- Retain one real fresh-empty-file process-exclusion behavior proof and one3-client startup scenario, consolidate duplicate cases and keep deterministic time-boundary tests small.
- Review test usefulness and architecture before committing; do not add skips, blanket ignores, broad fallback or new dependency/version matrices.

#### Verification

##### RED and focused behavioral GREEN.

**Method:** run_tests(scope='targets', tests=['python_tests'], targets=<only the edited config/lock/startup/proxy/recovery cases or families>, args={'python_tests':['-q']}, timeout_seconds=900). Preserve native parallelism; use exact case selection when useful. Target paths are actual files, selection options stay native args.

**Expected Result:** RED exposes missing corrected behavior; GREEN passes the affected public contracts, native exclusion and original-cause cases.

##### Focused file gates.

**Method:** run_checks(scope='targets', targets=<changed .py/.pyi files>, checks=['python_format','python_lint'], timeout_seconds=600). Separately run python_pyright only for changed production Python; production-scoped python_types uses scope='configured' when required. YAML basis and Markdown use their own checks/profiles and safe_edit/scaffold evidence.

**Expected Result:** Applicable changed-surface checks pass; no Markdown/YAML targets are sent to Python gates, and tests are not added to strict Mypy scope.

##### Integrated boundary without expensive repeat suites.

**Method:** Run the smallest combined affected config/startup/proxy/activation/recovery selection once after integration; include CLI init/renewal and fresh-installed startup only when its directly changed path needs proof. Reuse fresh evidence until later changes invalidate it.

**Expected Result:** Current-runtime integration is factual and preserves existing initialization, renewal and process lifecycle.

#### Stop Conditions

- Stop and reopen the owner strategy if source evidence contradicts required integrity or the one-loader boundary.
- Any unrelated product failure, requested gate waiver or policy/dependency change requires explicit triage; do not hide it with timeouts, fallback, skip or suppression.
- If a code repair is discovered after Implementation, return to Planning using the owner's standing force-back approval and update complete blocks before continuing; no gate exception.

## Phase Deliverables

### Validation

#### D\_1

Durable compact report maps all deliverables to focused evidence, complete configured native suite and configured/branch quality gates, plus non-instrumented30/60second three-start acceptance; record negative attempts and actual runtime identity.

**Owner:** @imp validator

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue520/validation.md"

### Documentation

#### D\_1

Update current server/config-loading/proxy/setup references with new required basis, override/deadline ownership, explicit existing-workspace migration, full proxy relaunch and timeout diagnostics; preserve historical artifacts.

**Owner:** @imp documenter

**Validates:**

**Type:** file_exists

**File:** "docs/reference/server-configuration.md"

## Related Documents

- [Approved Research](<research.md>)
- [Approved Design](<design.md>)
- [Quality/evidence standards](<../../coding_standards/QUALITY_GATES.md>)
- [Architecture contract](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-18 | @imp planner | Define one bounded correction cycle, focused behavior/gate evidence, final native Validation and independent review/Ready handoff. |
