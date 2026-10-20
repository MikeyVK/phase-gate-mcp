<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=WI5iXHBKVOU91bYE -->

# Issue \#537 — Planning

**Status:** Planning — independent review requested  
**Version:** 0.3  
**Last Updated:** 2026-10-20

## Purpose

Turn approved Design into a minimal coherent cycle, keeping phase evidence proportional.

## Scope In

Approved two named modes, final inline bound, configured route/attachment references, independent native attachments, matching schema and existing error ownership; only direct consumers and current references.

## Scope Out

Client campaigns, dependency/build/release changes, #536 branch operations, old-format compatibility, new caches/readers/frameworks, active restart/config switching and speculative instruction-loss coverage.

## Summary

One coherent implementation cycle cuts over the public configuration/presentation/transport contract, with focused behavioral proof. After failed full Validation, the appended test-only C_2 repairs four missed shared consumer surfaces; committed C_1 remains unchanged. Validation owns the full suite and branch/configured gates. Documentation and Ready follow independent QA gates.

Validation invocations (do not run early):

- run_tests(scope="configured", tests=["python_tests"], timeout_seconds=1200): full native configured suite, retaining native discovery/addopts; no selection filters, no weakened thresholds/skips.
- run_checks(scope="branch", checks=["python_format","python_lint","python_pyright"], timeout_seconds=600): configured per-check branch selection.
- run_checks(scope="branch", checks=["markdown_links","yaml_configuration"], timeout_seconds=600): document/config branch evidence.
- run_checks(scope="configured", checks=["python_format","python_lint","python_types","python_pyright"], timeout_seconds=900): workspace-wide native checks, including production-scoped Mypy from its native configuration.

Record failed/incomplete runs as such and rerun only invalidated evidence after a causal fix. Coverage remains native opt-in; do not add a new coverage threshold obligation or alter its configured threshold. Phase deliverable existence checks are navigation only; behavior is proved by the above execution evidence and independent review. Documentation edits that cannot invalidate Python proof reuse the fresh Validation results. Before the Ready/PR handover, verify no uncommitted changes, correct parent/base, full actual candidate identity and fresh independent QA. Coordinate merge and preserved #536 integration only after Ready; no release publication here.

## Dependencies

- Independent Design GO on 65f40425e9fd3a79b8309879b2e4fb9b9ed42b64.
- save_planning_deliverables readback: C_1, D_1.1–D_1.3; phase-local Validation D_1 and Documentation D_1.

## Risks

### Public config migration affects shared fixtures.

Migrate the existing helper and direct constructors during the same cycle; no old-key coercion or suitewide rewrite.

### A response-processing error can hide successful mutation or reprocess a poisoned payload.

Use reviewed no-replay guard/recover contracts and actual publisher/execution call counters.

## Milestones

- Implementation gate: coherent C_1 behavior and direct-file proof, then independent QA GO.
- Validation gate: complete native configured suite and required branch/configured checks, then independent QA GO.
- Documentation gate: current references only, then independent QA before Ready; actual PR/final QA before Coordination merge handover.

## Work Units

### C\_1 — Coherent two-mode delivery cutover

**Goal:** Switch the related contracts together and prove behavior at existing public boundaries.

**Cycle Number:** 1

#### Scope In

Settings/config/defaults/bootstrap; presentation DTO/interface seams; ResponsePresenter/TextBudgetLimiter/server transfer; startup carrier only where required; existing direct tests/helper constructors.

#### Scope Out

No broken intermediate compatibility contract, no internal operation changes or active rollout.

#### Deliverables

##### D\_1.1

Replace profile matrix/selector with typed structured/resource mode and shared budgets; migrate direct config/bootstrap/helper consumers and expose separate resources plus metadata-only attachment references.

**Validates:**

**Type:** file_exists

**File:** "mcp_server/schemas/presentation_output.py"

##### D\_1.2

Restore final text cap and configured footer, full structured presentation, real resource locator, independent embedded attachments, prior-serialization guard and preserved compact recovery/startup exception.

**Validates:**

**Type:** file_exists

**File:** "mcp_server/presenters/response_presenter.py"

##### D\_1.3

Adapt existing two-route/config/limiter/SDK/recovery cases, prove real publisher call counts and storage-failure distinction, and remove obsolete combinations without extra harness or compatibility suites.

**Validates:**

**Type:** file_exists

**File:** "tests/mcp_server/integration/test_execution_presentation_v3.py"

#### Exit Criteria

Two named modes and final UTF-8 text bounds work through real SDK delivery, separate attachments/references are preserved, publisher serialization failure is not replayed, normal recovery retains truth, directly affected tests/checks pass, and obsolete matrix/JSON-text branches are removed.

#### Dependencies

- Research and Design approval

#### Obligations

- Preserve operation DTOs/cache/attachment producers, actual isError and primary diagnostics.
- Guard a prior publisher serialization failure before normal renderer/full operation conversion; independent attachment formatting remains permitted.
- Use one existing presenter factory to contain test setup coupling; obsolete matrix expectations are removed.

#### Verification

##### Durable changed final-byte-bound behavior

**Method:** Adapt the existing oversized-core limiter case to demonstrate an actual failing end-cap obligation before production edits; use a meaningful feasible budget. Then implement against the reviewed limiter interface and prove green. No artificial RED cases for mechanical constructor migration.

**Expected Result:** A real pre-change oversize result fails the new bound; corrected limiter/footer behavior passes.

##### Focused cycle proof

**Method:**

run_tests(scope='targets', targets=<the existing 13 files listed below>, tests=['python_tests'], args={'python_tests':['-n','0']}, timeout_seconds=900). Investigate a failure through its narrow file/case; repeat broader focus only if changes invalidate its result.

Existing focused target files:
- tests/mcp_server/unit/config/test_presentation_config.py
- tests/mcp_server/unit/config/test_settings.py
- tests/mcp_server/unit/presenters/test_text_budget_limiter.py
- tests/mcp_server/unit/test_presenter.py
- tests/mcp_server/unit/schemas/test_presentation_output.py
- tests/mcp_server/unit/core/interfaces/test_presenter_interfaces.py
- tests/mcp_server/unit/server/test_validate_tool_arguments.py
- tests/mcp_server/unit/test_server.py
- tests/mcp_server/integration/test_execution_presentation_v3.py
- tests/mcp_server/integration/test_tool_attachment_transport.py
- tests/mcp_server/integration/test_pipeline_e2e.py
- tests/mcp_server/integration/test_rollout_configuration.py
- tests/mcp_server/integration/test_v3_cutover.py

**Expected Result:** Affected behavior and direct callers pass without full-suite execution in Implementation.

##### Changed-file gates

**Method:** Derive current changed Python paths from Git before each call. Run run_checks(scope='targets', targets=<all changed production/test/helper .py/.pyi files>, checks=['python_format','python_lint'], timeout_seconds=600). Separately run run_checks(scope='targets', targets=<only changed production .py/.pyi files under mcp_server>, checks=['python_pyright'], timeout_seconds=600). Test/helper typechecks are narrow diagnostics, not a new required strict gate over existing wider mock/Unknown debt; investigate concrete new contract violations without widening the cycle. Check changed YAML separately via yaml_configuration; Markdown uses its document link checks. Configured Mypy/Pyright in Validation retain their native production selection and strictness.

**Expected Result:** Suitable file types per check; no Markdown/YAML routed to Python checks.

#### Stop Conditions

- Stop for a genuinely changed owner policy, unsound invariant or requirement to alter startup recovery completeness.
- Keep technical defects within the approved seams; no gate waiver, skip, lowered threshold or new suppression to hide them.
- A committed cycle cannot be rewritten. If a new concrete corrective cycle is needed, return to Planning with the standing backward-transition authorization and independent QA.

### C\_2 — Correct shared test transport consumers

**Goal:** Preserve the valuable public-operation/cache evidence while removing four stale transport assumptions exposed by complete Validation.

**Dependency:** C_1 and the failed Validation report at b0f082da3801bb7c9448dd4c408d1246f909b9d0. Audited return to Planning uses the owner's standing 2026-10-18 backward-transition authorization.

#### Scope and deliverables

- **D_2.1 — Shared public-response helper migration:** Adapt the two public helpers in test_scaffold_public_v3.py and test_schema_public_v3.py to structured-route summaries and separate embedded attachments; preserve cached DTO/write/schema assertions in their dependent cases.
- **D_2.2 — Explicit cache-mode bootstrap proof:** Select resource mode explicitly in planning-cache and installed-paging tests, read schema attachments from native content, and retain exact readback, restart and identity evidence.

Exactly four editable test surfaces: tests/mcp_server/integration/test_scaffold_public_v3.py, test_schema_public_v3.py, test_project_plan_readback.py and test_target_startup.py. Adapt shared helpers rather than 85 independent cases; keep assertions of operation facts, write effects, raw cached DTOs and exact schemas. Do not delete/skip cases, add a compatibility branch, change the default or patch production. Source code and native checker settings remain unchanged.

#### Exit criteria

The 85 failed Validation cases pass through four bounded consumer-file fixes, with no production/default/native-gate changes, no test deletions/skips and a fresh complete native Validation run afterward.

#### Verification and cleanup

- The complete negative baseline already proves the missed consumer assumptions; this is test maintenance, with no artificial RED or new synthetic test suite.
- Run the seven affected public/plan files through run_tests(scope="targets", tests=["python_tests"], args={"python_tests":["-n","0","--tb=short"]}, timeout_seconds=600): test_edit_public_v3.py, test_scaffold_public_v3.py, test_checks_public_v3.py, test_fixes_public_v3.py, test_tests_public_v3.py, test_schema_public_v3.py and test_project_plan_readback.py, all under tests/mcp_server/integration/.
- Run only the affected installed startup scenario in test_target_startup.py with -k test_installed_candidate_init_migration_and_mcp_handshake, -n 0 and timeout_seconds=300. It uses an isolated installed candidate, not the active environment.
- Format/lint the four modified test files; test typing remains bounded diagnosis. No production typing/native configuration changes are intended.
- After independent C_2 Implementation→Validation GO, rerun the complete native configured suite with timeout_seconds=1200, preserving the established 1800-second client window and stop/delivery headroom per docs/setup/README.md. Repeat affected branch and configured format/lint evidence. Reuse the unchanged production Mypy/Pyright evidence where its exact source remains valid; no waiver.
- Stop and re-plan if evidence requires production changes, more than these four test surfaces or a real strategy change. Re-enter implementation explicitly with resume_cycle="C_2". Preserve the failed Validation and all C_1 history.

## Phase Deliverables

### Validation

#### D\_1

Durable full validation evidence.

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue537/validation.md"

### Documentation

#### D\_1

Current response delivery references.

**Validates:**

**Type:** file_exists

**File:** "docs/reference/presentation_architecture.md"

## Related Documents

- [Approved Design v0.2](<design.md>)
- [Research outcome](<research.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-20 | @imp planner | Register one coherent cycle and phase deliverables with focused implementation evidence and full Validation obligations. |
| 0.2 | 2026-10-20 | @imp planner | Resolve QA P2 by separating production Pyright gates from test/helper format/lint and bounded diagnostic typechecks. |
| 0.3 | 2026-10-20 | @imp planner | Preserve failed full Validation and append bounded test-only C_2; retain C_1 and align native execution allowance with tracked setup headroom. |


