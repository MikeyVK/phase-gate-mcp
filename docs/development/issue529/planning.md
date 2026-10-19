<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=WI5iXHBKVOU91bYE -->

# Issue \#529 — Focused response-profile implementation

**Status:** PROPOSED — Planning prepared for independent review  
**Version:** 0.1  
**Last Updated:** 2026-10-19

## Purpose

Sequence the approved refactor with proportionate tests, explicit consumer cleanup and independent QA at phase boundaries.

## Scope In

Approved Design v0.2 and Research strategy, including truthful cache/inline failure contracts and the fixed startup-recovery exception.

## Scope Out

No compatibility paths, harness/version tests, generic cache or loader redesign, #528 decorator metadata fix, release or merge execution by Imp.

## Prerequisites

- Independent Design → Planning GO on 9fcf07dc963dc42bb0535bc7bd659c0df6f160d4.
- Workflow refactor; current phase Planning; branch registration/history preserved.
- Owner authorizes autonomous execution through Ready, with independent QA at phase boundaries and human decisions only for policy.

## Summary

Two implementation cycles: C_1 establishes explicit config/value contracts and truthful serialization/publication facts; C_2 performs the single live presentation/transport cutover with direct behavioral-consumer migration. No dormant compatibility route remains after C_2. Validation owns the single full suite and final broad checks; Documentation updates current guidance.

## Validation execution boundary

Run run_tests(scope='configured', tests=['python_tests'], timeout_seconds=1800) once after Implementation QA GO, preserving native test selection and options. Coverage is opt-in in pyproject.toml; no extra coverage gate is added to this issue. Run run_checks(scope='branch', timeout_seconds=900) for the active branch contract. Supplement with run_checks(scope='configured', checks=['python_types','python_format','python_lint','python_pyright'], timeout_seconds=900) for final workspace/production-configured Python gates, as required by the standing owner selection policy. Document every genuine failure; no gate exceptions or relaxed thresholds. Capture exact calls/outcomes in validation.md; run IDs may supplement, not replace them. QA independently reviews completion before Documentation.

## Documentation and Ready

Update docs/reference/presentation_architecture.md, applicable docs/setup guidance and mcp_server/resources/cache_reading.md; use current tool-reference pages only where changed behavior is described. No all-document rewrite. Markdown link checks and relevant packaged-guide checks are sufficient unless production behavior changes. Independent QA decides Documentation → Ready. Complete Ready via its live instructions, push all work and transfer the end-issue merge request to Coordinatie; Imp does not merge.

## Reversibility and stop rules

Commits isolate C_1 and C_2. A needed correction before Validation is handled within its current cycle; after entering a later phase, use the owner's standing approved forced return and normal QA progression if code must change. Do not mutate committed plan cycles to hide failed obligations. A changed architecture/strategy or new product policy is the only reason to pause for the owner; implementation defects remain producer work.

## Dependencies

- C_2 consumes C_1's profile, value and publication contracts.
- No phase transition before its independent QA GO; no per-cycle independent QA is added.
- Runtime activation follows complete C_2; existing tool input contracts do not change. Reload tools/list after activation; no human reconnect is assumed unless observed necessary.

## Risks

### Changing the config and presentation contract invalidates direct test setup.

Update only directly affected builders/helpers and consumers in the cycle owning the contract; use public behavior instead of source-string tests.

### A serialization failure can be hidden by legacy replacement JSON or misreported as operation failure.

Explicit publisher diagnostic union and separate delivery_error; exercise the existing fidelity seam plus independent inline success/failure.

### The active server continues running while its source/config is changed.

Keep input contracts stable, complete C_2 before restart, then call health/work-context/schema against the replacement and inspect actual results.

## Milestones

- C_1 explicit configuration/value and publication contracts.
- C_2 activated complete profile delivery with focused behavior evidence.
- Validation, Documentation and Ready each independently reviewed.

## Work Units

### C\_1 — Profile contracts and truthful serialization facts

**Goal:** Profile contracts and truthful serialization facts

**Cycle Number:** 1

**Owner:** @imp implementer

#### Scope Out

No tool/manager/adapter semantic changes, harness matrix, compatibility bridges, metadata-registration repair from #528 or suite-wide test cleanup.

#### Deliverables

##### D\_1.1

Implement frozen response-profile configuration, version 2.0.0 defaults, positive resolved budgets and explicit per-process selector through existing Settings/bootstrap seams; update directly affected configuration builders without old-key aliases.

**Validates:**

**Type:** file_exists

**File:** "mcp_server/config/schemas/presentation_config.py"

##### D\_1.2

Remove concealed replacement-JSON success; preserve original native errors/causes through existing capture_exception and CachePublication diagnostic union; no entry or eviction on failed serialization. Preserve normal canonical representation and cache read/window API.

**Validates:**

**Type:** file_exists

**File:** "mcp_server/schemas/cache_publication.py"

##### D\_1.3

Define the approved common envelope, inline/resource alternatives and both delivery-error codes at the existing presentation-output boundary; keep internal operation DTOs and ToolExecution intact. Prove required value/config/error invariants through focused existing tests.

**Validates:**

**Type:** file_exists

**File:** "mcp_server/schemas/presentation_output.py"

#### Exit Criteria

Focused configuration/settings, publication and cache-fidelity behavior tests pass, including original exception/cause and independent valid operation facts; changed Python files pass applicable directed format/lint/type checks; native YAML checks pass changed config. No runtime legacy/compatibility mode. Existing loaded server remains available until the complete C_2 activation.

#### Dependencies

#### Obligations

- Do not classify serialization diagnoses as complete operation publication.
- Preserve normal JSON representation and explicit diagnostics variant.
- Use existing config loader, no file-specific composition route.

#### Verification

##### Current observable behavior

**Method:** Focused existing settings/config/publication/fidelity tests, adapting current behavior requirements.

**Expected Result:** All focused behavior cases pass and required native failures retain original diagnosis.

##### Focused execution commands

**Method:** run_tests(scope='targets', targets=['tests/mcp_server/unit/config/test_presentation_config.py', 'tests/mcp_server/unit/config/test_settings.py', 'tests/mcp_server/unit/state/test_response_cache.py', 'tests/mcp_server/integration/test_cache_fidelity_v3.py', 'tests/mcp_server/unit/schemas/test_presentation_output.py'], tests=['python_tests'], args={'python_tests':['-n','0']}, timeout_seconds=300). Run an initial focused baseline, adapt/add only missing durable behavior cases and observe real failure where the new invariant is uncovered.

**Expected Result:** Focused current-contract evidence, no full suite or forced artificial RED for mechanical test setup.

##### Directed native quality checks

**Method:** Use run_checks(scope='targets', targets=[actual changed Python files], checks=['python_format','python_lint','python_pyright'], timeout_seconds=600). Run python_types only for changed production Python paths. Use yaml_configuration for changed YAML and markdown_links for Markdown; never pass mixed Markdown/YAML paths into Python gates. Reuse fresh evidence until code changes invalidate it.

**Expected Result:** Appropriate native checks pass on the changed surface without widening policy or suppressing diagnostics.

#### Stop Conditions

- Stop for an owner decision only if an approved invariant/strategy must change.
- Stop and correct the plan before committed-cycle scope changes; never silently weaken a gate.

### C\_2 — Protected presentation, profile delivery and live cutover

**Goal:** Protected presentation, profile delivery and live cutover

**Cycle Number:** 2

**Owner:** @imp implementer

#### Scope Out

No tool/manager/adapter semantic changes, harness matrix, compatibility bridges, metadata-registration repair from #528 or suite-wide test cleanup.

#### Deliverables

##### D\_2.1

Render required template/enum/instruction/note content independently from full JSON serialization, separate optional collections, and update the existing limiter to preserve mandatory core with explicit overruns and UTF-8-safe detail bounds.

**Validates:**

**Type:** file_exists

**File:** "mcp_server/presenters/text_presenter.py"

##### D\_2.2

Resolve/inject the process-local profile, route full operation data and attachments, emit the matching common output schema and truthful independent cache/inline emergency variants, retain actual isError; use fixed full dual-channel startup recovery. Remove bare structured assignment, unconditional resource copies, unlimited fallback and absent-presenter bypass.

**Validates:**

**Type:** file_exists

**File:** "mcp_server/server.py"

##### D\_2.3

Adapt existing direct presenter/transport/bootstrap tests and shared constructors to the clean contract; prove representative channel combinations, native SDK schema acceptance, full operation/resource/attachment routes, two instances sharing config, startup recovery and both serializer failure directions. Restart/reload the completed server and perform focused healthy live calls; keep temporary probes out of permanent suite.

**Validates:**

**Type:** file_exists

**File:** "tests/mcp_server/integration/test_execution_presentation_v3.py"

#### Exit Criteria

Focused presenter/limiter/interface/schema/server tests and directly affected SDK integration consumers pass; branch-selected focused groups remain bounded to touched seams. Directed production/test checks pass. Completed server restarts healthy and preserves work-context instructions. All old-route remnants removed; no compatibility or client-specific code. Request independent QA before Validation.

#### Dependencies

- C_1

#### Obligations

- Use real presenter/SDK seams; protect full instructions and actual operation outcome.
- Keep shared profile definitions read-only and selectors process-local.
- Adapt direct consumer tests in the same contract-cutover cycle; no stale consumer debt passed to Validation.
- Record live activation and current response-shape checks; tools inputs remain stable, refresh catalog after restart.

#### Verification

##### Current observable behavior

**Method:** Targeted tests for changed presenter/SDK/startup seams; no workspace suite here.

**Expected Result:** All focused behavior cases pass and required native failures retain original diagnosis.

##### Focused execution commands

**Method:** run_tests(scope='targets', targets=["tests/mcp_server/unit/presenters/test_text_budget_limiter.py","tests/mcp_server/unit/presenters/test_text_presenter_composition.py","tests/mcp_server/unit/config/test_presentation_config.py","tests/mcp_server/unit/core/interfaces/test_presenter_interfaces.py","tests/mcp_server/unit/schemas/test_presentation_output.py","tests/mcp_server/unit/test_presenter.py","tests/mcp_server/unit/test_server.py","tests/mcp_server/unit/server/test_bootstrap.py","tests/mcp_server/integration/test_execution_presentation_v3.py","tests/mcp_server/integration/test_tool_attachment_transport.py","tests/mcp_server/integration/test_pipeline_e2e.py","tests/mcp_server/integration/test_target_startup.py","tests/mcp_server/integration/test_checks_public_v3.py","tests/mcp_server/integration/test_edit_public_v3.py","tests/mcp_server/integration/test_fixes_public_v3.py","tests/mcp_server/integration/test_tests_public_v3.py","tests/mcp_server/integration/test_schema_public_v3.py","tests/mcp_server/integration/test_scaffold_public_v3.py"], tests=['python_tests'], timeout_seconds=600). This is the concrete direct-consumer group; additionally touched direct consumers receive their own focused checks. Split by seam only to diagnose real failures, not to impose a full-suite workload during Implementation.

**Expected Result:** All directly affected consumers pass; coverage is behavioral and input-derived, no concrete harness content snapshots.

##### Directed native quality checks

**Method:** Use run_checks(scope='targets', targets=[actual changed Python files], checks=['python_format','python_lint','python_pyright'], timeout_seconds=600). Run python_types only for changed production Python paths. Use yaml_configuration for changed YAML and markdown_links for Markdown; never pass mixed Markdown/YAML paths into Python gates. Reuse fresh evidence until code changes invalidate it.

**Expected Result:** Appropriate native checks pass on the changed surface without widening policy or suppressing diagnostics.

#### Stop Conditions

- Stop for an owner decision only if an approved invariant/strategy must change.
- Stop and correct the plan before committed-cycle scope changes; never silently weaken a gate.

## Phase Deliverables

### Validation

#### D\_1

Record one full native-configured suite, branch gates, production-scoped Mypy and configured Python checks; map every deliverable/invariant, actual failure outcomes, cleanup, process isolation and live evidence without relying on transient run IDs.

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue529/validation.md"

### Documentation

#### D\_1

Update current presentation architecture, setup/launcher guidance and packaged cache guide for selected profiles, common envelope, schema boundaries, mandatory-core budget exception and fixed startup recovery; preserve historical issue reports.

**Validates:**

**Type:** file_exists

**File:** "docs/reference/presentation_architecture.md"

## Related Documents

- [Design](<design.md>)
- [Research and strategy](<research.md>)
- [Quality gates](<../../coding_standards/QUALITY_GATES.md>)
- [Type checking](<../../coding_standards/TYPE_CHECKING_PLAYBOOK.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-19 | @imp planner | Define two focused implementation cycles and exact Verification scope, direct consumer cleanup, runtime activation and operational phase deliverables. |
