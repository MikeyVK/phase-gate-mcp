<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=WI5iXHBKVOU91bYE -->

# Issue \#528 — compact recovery execution plan

**Status:** Planning — independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-20

## Purpose

Execute the approved bounded correction in one coherent implementation cycle, with narrow implementation evidence and full native/configured Validation.

## Scope In

Research1.3 / Design1.2 compact known-outcome recovery, affected interface/model/config/server consumers and focused behavior evidence.

## Scope Out

Full DTO/notes/attachments replay, normal payload projection or rendering in recovery, publication/retrieval, parallel server presenter/framework, compatibility paths, harness/version tests, release/dependency changes and suite-wide cleanup.

## Summary

One cycle C_1, three deliverables D_1.1–D_1.3. Start with the existing SDK post-operation failure test exposing the actual-outcome loss (RED), then implement the approved contract and server boundary together to GREEN. Align only affected consumers and run exact focused tests/target checks. Independent QA governs phase progression. Preserve negative evidence and use no gate waivers.

## Dependencies

- Research1.3 approved compact recovery strategy and Design1.2 (independent strategy-amendment/Design→Planning GO on1318728e47016ca7bad1961ee994102e69e2e678).
- Existing native tool bindings/configuration and test helpers; no new dependency or constructor graph.
- Quality standards: no mandatory test-Mypy expansion; production-scoped Mypy remains configured.

## Risks

### Full-payload conversion hides behind a shared recovery helper.

Small recovery signature, poisoned/large original-payload tests and architectural review; no normal projection call.

### Old fixtures/doubles encode old six-field envelope or lack recover().

Align directly affected setup/assertions in same cycle using real existing test factories where possible; no suite-wide rewrite.

## Milestones

- Validation: run_tests(scope="configured", tests=["python_tests"], timeout_seconds=1800), no args override. One complete native full suite; preserve existing native defaults/parallelism/coverage if configured. Do not split or add an unapproved coverage gate. Earlier #529 full run was3060passed/703.45s; it is context, not #528 validation.
- Validation: run_checks(scope="branch", checks=["python_format","python_lint","python_pyright","markdown_links","yaml_configuration"], timeout_seconds=600); branch selection uses current per-check configured target filters. Then run_checks(scope="configured", checks=["python_format","python_lint","python_types","python_pyright"], timeout_seconds=600) for the workspace-wide configured Python gates, including production-scoped Mypy. Record every outcome; reuse fresh evidence until changes invalidate it.
- Validation: scaffold the compact durable validation report with exact calls/outcomes and retained negative history; independent Validation→Documentation QA. A timeout/termination problem is incomplete, not a pass. Repair only within approved boundaries; no waiver.
- Documentation: update the active presentation architecture reference for processing_error, compact reference/null recovery, missing full result/guidance, diagnostics budget and normal-profile preservation; remove obsolete metadata-forwarding reservation. Run targeted Markdown link checks; historical529 docs stay contextual.
- Ready: obtain independent Documentation→Ready QA, transition/get fresh context, complete configured Ready steps and concrete PR. Independent final review and full handoff to Coordination; no producer merge or next issue start.

## Work Units

### C\_1 — Compact post-operation response recovery

**Goal:** Remove the misleading post-operation error response without replaying potentially failing large payload or rendering.

**Cycle Number:** 1

**Owner:** @imp implementer

#### Scope In

server.py; core/interfaces/ipresenter.py; schemas/presentation_output.py; presenters/response_presenter.py and startup_recovery_presenter.py; config/schemas/presentation_config.py; config/defaults/presentation.yaml; directly affected tests/support.

#### Scope Out

No changes to tool domain operations, workflow/state engines, adapters, cache ownership/API, normal rendering behavior, dependencies or native quality policy.

#### Deliverables

##### D\_1.1

Implement the approved small IPresenter.recover contract in existing presenters, nullable processing_error on shared models, normal/recovery schema alternatives and configured notices. Bound Unicode candidate prefixes before encoding. No operation/notes/attachments/context objects or normal data projection enter recovery.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/presenters/response_presenter.py"

##### D\_1.2

Remember actual outcome before presentation; on later exception pass only outcome, native diagnostic strings and successful cache receipt scalars to one recovery attempt. Preserve original cause/outcome and finite terminal behavior, no second server presenter, payload conversion or side effect retry.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/server.py"

##### D\_1.3

Adapt existing public SDK failure test and directly affected model/profile/config/interface/startup tests. Prove success/failure, reference/null, channel/schema truth, poisoned/large payload independence, bounded Unicode diagnosis and finite recovery; no snapshots/legacy tests or broad test rewrite.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "tests/mcp_server/integration/test_tool_attachment_transport.py"

#### Exit Criteria

Meaningful RED then GREEN evidence for the post-operation defect; compact outcome/notice/bounded-diagnosis/existing-reference recovery conforms to selected schemas/channels without original-payload conversion, normal projection/render retry, publication or retrieval; affected consumers aligned; focused tests and applicable target checks pass; no waiver or new policy.

#### Dependencies

- Approved Research/Design and independent Planning→Implementation GO.

#### Obligations

- Adapt useful existing behavior tests; initial RED must fail on actual known-outcome/structured recovery behavior, not import/setup failure.
- Commit RED then GREEN under C_1 using configured subphases. Consumer edits share the cycle; do not preserve old bare-failure assertions or add legacy tests.
- Explicitly require a bounded code-point prefix before existing excerpt/UTF8 helpers; no full diagnostic encoding first. Use existing allowance, no global output ceiling or original-object serialization.
- Normal shared models remain field/schema SSOT; recovery shares only small channel facts, never normal data projection. Server owns no presentation wording/profile/schema inventory.
- Known success and known operation failure, existing reference and null, structured/text/resource profiles, poisoned/large payload conversion guard, Unicode shortening and one recovery attempt must have behavior evidence.
- Restart the existing server route after focused GREEN, before final activation evidence, and verify health/work context; refresh actual catalog through existing supported client route if needed. No install/build/release or client-profile policy change. Public inputs stay unchanged; do not invent dependency-version surveillance.

#### Verification

##### RED defect evidence

**Method:** run_tests(scope="targets", targets=["tests/mcp_server/integration/test_tool_attachment_transport.py"], tests=["python_tests"], args={"python_tests":["-n","0","-k","processing_failure"]}, timeout_seconds=300)

**Expected Result:** The adapted existing case fails on the missing/wrong compact recovery behavior. Save factual failure before production correction.

##### Focused GREEN

**Method:** run_tests(scope="targets", targets=<actual changed tests plus directly relevant existing companion files>, tests=["python_tests"], timeout_seconds=600). Primary files: integration/test_tool_attachment_transport.py, unit/schemas/test_presentation_output.py, unit/config/test_presentation_config.py, unit/core/interfaces/test_presenter_interfaces.py, unit/test_presenter.py, integration/test_target_startup.py; include integration/test_execution_presentation_v3.py and test_cache_fidelity_v3.py only as relevant consumers. Do not select whole test directories.

**Expected Result:** All selected cases complete/pass; outcome, schema and independence proved, not just method presence.

##### Target gates

**Method:** Select actual changed Python production/test files explicitly for run_checks(scope="targets", checks=["python_format","python_lint","python_pyright"], timeout_seconds=600); add python_types only on changed production sources when useful. Check changed presentation YAML with yaml_configuration and current phase Markdown with markdown_links separately. No Markdown/workflow JSON targets passed to Python checks.

**Expected Result:** Applicable focused checks passed with actual captured outcomes. No test-Mypy gate or broad scope added.

#### Stop Conditions

- Unexpected policy/scope conflict or recovery needs original payloads, normal renderer/data pipeline, new publisher/retrieval/parallel presenter: stop and reopen exact Design boundary, do not improvise.
- Required gates unavailable/incomplete/failed remain unresolved evidence, not passes; technical defects get bounded repair/review.
- Active runtime/client catalog cannot be refreshed through supported existing routes: preserve status and identify required external action; do not claim new runtime behavior from tests alone.

## Phase Deliverables

### Validation

#### D\_1

Record exact native full-suite and configured/branch checks, focused evidence, negative outcomes and independent review entrypoints; no transient run IDs as sole proof.

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue528/validation.md"

### Documentation

#### D\_1

Document compact recovery/output schema and original-data/guidance limitations; remove obsolete active wrapper-metadata reservation without rewriting historical529 docs.

**Validates:**

**Type:** file_exists

**File:** "docs/reference/presentation_architecture.md"

## Related Documents

- [Approved Design](<design.md>)
- [Research strategy/evidence](<research.md>)
- [Quality standards](<../../../docs/coding_standards/QUALITY_GATES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-20 | @imp planner | One bounded RED/GREEN cycle, exact focused and native/configured gates, runtime activation, evidence/documentation/Ready obligations and no-waiver stops. |
