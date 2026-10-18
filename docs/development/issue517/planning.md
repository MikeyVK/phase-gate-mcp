<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=WI5iXHBKVOU91bYE -->

# Issue 517 — Native SDK Migration Plan

**Status:** Proposed for independent Planning review  
**Version:** 0.1  
**Last Updated:** 2026-10-18

## Purpose

Deliver the approved Python3.15/SDK2.3 clean cutover with proportional behavior evidence.

## Scope In

Approved Design v0.3 at the existing SDK owners, prerequisites/direct consumers and actual installed acceptance.

## Scope Out

Release/publication, active runtime replacement, SDK1 environments, dependency-version assertion suites and #518 broad suppression fixes.

## Prerequisites

- Research v0.4 Approved Strategy and Design v0.3; independent Design GO on f91116de.
- Existing #513 selected Python3.15 environment is preparation only; final acceptance uses a clean actual wheel.
- No production edits until independent Planning → Implementation GO.

## Summary

Two dependent implementation cycles: coherent native integration/consumer cutover, then proxy lifecycle and clean installed acceptance. Validation owns one full suite and branch/configured gates; reuse fresh focused evidence.

## Dependencies

- C_2 depends on C_1; validation follows both completed cycles.

## Risks

### Changing native pins makes the active old host unsuitable for authoritative target gates.

Use a temporary selected-stack RPC driver to call actual installed candidate run_checks/run_tests, with explicit PATH/config roots; preserve native guards and scopes.

### A package smoke can accidentally import the checkout.

Neutral working directory and explicit module/executable/metadata identity; source test imports are labeled separately.

## Work Units

### C\_1 — Native SDK and dependency cutover

**Goal:** Replace the coupled SDK boundary and its direct consumers as one coherent cutover.

**Cycle Number:** 1

#### Scope In

Three SDK production owners, direct consumers/helper, controlled metadata/native prerequisites.

#### Scope Out

SDK1 compatibility, dependency-version tests, #518 suppression policy, active host activation, release.

#### Deliverables

##### D\_1.1

Align Python/runtime/dev metadata and affected native adapter pins and language targets, preserving native guards and explicit covariance.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "pyproject.toml"

##### D\_1.2

Replace SDK1 registration and aliases at server/converter/proxy owners; deliver matching structured DTOs and explicit failure mapping, retaining initialized protocol and presentation/cache contracts.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/server.py"

##### D\_1.3

Adapt the identified direct SDK tests through an initialized native client lifecycle helper; remove obsolete API coupling and cover structured-output/error behavior proportionally.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "tests/mcp_server/test_support.py"

#### Exit Criteria

Coherent target source and prerequisites; focused migrated server/converter/schema/cache/attachment/admission tests and production typing pass on the selected stack through actual candidate MCP tools; no compatibility facade or guard bypass.

#### Dependencies

- Research v0.4; Design v0.3; Design QA GO on f91116de

#### Obligations

- Keep domain/presenter contracts and covariance; schema-compatible actual structured DTO.
- Keep source/prerequisites/test consumer cutover coherent; no temporary compatibility bridge.

#### Verification

##### Preservation and approved structured result

**Method:** Existing narrow host baseline before cutover; adapt valuable tests then candidate run_tests for affected SDK files; candidate run_checks on changed Python targets and production-scoped Mypy.

**Expected Result:** Meaningful scenarios pass on selected target; native client accepts structured DTO/schema, retains operation and processing errors and resource/cancellation behavior.

#### Stop Conditions

- Material target-stack conflict, required behavior outside approved strategy, or active host switch needed: reopen owner decision.
- Required native prerequisites unavailable or incomplete evidence: do not bypass guards or claim passing evidence.

### C\_2 — Proxy lifecycle and installed acceptance

**Goal:** Prove actual proxy lifecycle and clean installation without changing the active host.

**Cycle Number:** 2

#### Scope In

Existing proxy public behavior surface, isolated wheel/install and temporary RPC orchestration.

#### Scope Out

SDK1 compatibility, dependency-version tests, #518 suppression policy, active host activation, release.

#### Deliverables

##### D\_2.1

Replace shallow proxy cases with bounded public behavior evidence for restart/replacement, failed replacement, in-flight/cancellation/deadline and cleanup, using existing process injection.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "tests/mcp_server/core/test_proxy.py"

##### D\_2.2

Build/install the real wheel in an isolated Python3.15 environment; prove module/process identity, pip consistency, initialized actual pgmcp tool/resource/error and proxy lifecycle behavior; retain active host.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "scripts/build_package.py"

#### Exit Criteria

Focused lifecycle/installation evidence succeeds on the clean installed target; no orphaned children, SDK1 bridge, launcher mutation or release. Relevant file checks pass; independent QA requested before Validation.

#### Dependencies

- C_1

#### Obligations

- Use existing process_factory; deterministic observations and bounded teardown.
- Actual installed pgmcp and proxy on initialized2025 route, not only a minimal SDK example.

#### Verification

##### Lifecycle/install acceptance

**Method:** Focused tests/mcp_server/core/test_proxy.py through candidate run_tests; existing builder, clean install, pip consistency and actual stdio/proxy RPC.

**Expected Result:** Restart success/failure and in-flight/cancel/deadline/cleanup observed; installed identity correct and no child leak.

#### Stop Conditions

- Material target-stack conflict, required behavior outside approved strategy, or active host switch needed: reopen owner decision.
- Required native prerequisites unavailable or incomplete evidence: do not bypass guards or claim passing evidence.

## Phase Deliverables

### Validation

#### D\_1

Compact durable validation report with target identity, exact scopes/native outcomes, one full configured suite/coverage and branch/configured checks, installed/proxy acceptance and remaining risks.

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue517/validation.md"

### Documentation

#### D\_1

Correct active setup/isolation/tooling docs invalidated by the delivered baseline; record outcome and handoff without rewriting historical research.

**Validates:**

**Type:** file_exists

**File:** "docs/setup/README.md"

## Evidence Timing and Rollback

During C_1, establish the narrow current-host baseline on existing server/converter/schema/attachment scenarios before changing their dependency contract. This uses the already operational host, not a new SDK1 compatibility environment. Retain that baseline only as preservation input. For genuinely uncovered structured-output/processing-failure obligations, demonstrate a meaningful failing assertion before the fix; do not manufacture RED for mechanical call-site changes.

After coherent cutover, use the selected-stack candidate's actual MCP run_tests/run_checks with the explicit targets for the changed SDK tests and Python files. Production Mypy uses scope="configured", checks=["python_types"]; tests do not become strict-Mypy targets. Ruff format/lint and Pyright use applicable Python targets. Keep Markdown under markdown_links and changed YAML/JSON under their appropriate checks. Temporary orchestration does not bypass adapters or native version guards. A C_1 build/install may prepare candidate RPC verification; C_2 still owns clean final installed acceptance.

Validation performs one full run_tests(scope="configured", tests=["python_tests"], args={"python_tests":["--cov=mcp_server","--cov-branch"]}, timeout_seconds=1800) through the installed selected-stack candidate. Keep native parallelism/configured coverage and use a client window longer than execution plus termination/delivery. Then run run_checks(scope="branch", checks=["python_format","python_lint","python_pyright"], timeout_seconds=600), relying on the approved per-check configured branch selection, and run_checks(scope="configured", checks=["python_types"], timeout_seconds=600). Run the final workspace-configured Python format/lint/Pyright selection once; reuse unchanged Mypy evidence. Check only changed documents/configs with applicable adapters. Record incomplete/unavailable runs as such; no gate exception.

Cycle rollback uses the prior coherent branch commit; do not keep a hybrid SDK1/SDK2 source or loosen prerequisites to get a pass. Isolated build/install output is disposable. Active host/client and credentials are not modified. Real lifecycle gaps may be repaired at their existing owner only within Design; new behavioral policy reopens the owner decision.

Independent QA is used only at phase boundaries. After cycle evidence, request Implementation → Validation GO; after Validation request Documentation GO; after active docs and final clean pushed state request Ready GO. Ready submission and end-issue merge handoff belong to the existing workflow and Coordinatie.

## Related Documents

- [Approved Research](<research.md>)
- [Design](<design.md>)
- [Quality evidence rules](<../../coding_standards/QUALITY_GATES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-18 | @imp planner | Sequence native cutover, focused behavior evidence and clean installed proxy acceptance within the approved strategy. |
