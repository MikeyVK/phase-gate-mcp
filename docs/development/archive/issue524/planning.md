<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=WI5iXHBKVOU91bYE -->

# Issue \#524 — Cache-notice correction plan

**Status:** Planning completed; independent review requested  
**Version:** 1.1  
**Last Updated:** 2026-10-19

## Summary

C_1 remains completed and unchanged. Add only C_2 to repair a missed existing pipeline-test consumer exposed by the required full suite. The correction remains mechanical test maintenance; no production, interface, configuration-admission or output-policy change.

## Milestones

- Validation after final implementation: run_tests(scope="configured", timeout_seconds=1200), no caller args; run_checks(scope="branch", checks=["python_format","python_lint","python_pyright","yaml_configuration","markdown_links"], timeout_seconds=600); run_checks(scope="configured", checks=["python_types"], timeout_seconds=600). Per-check native branch preselection applies the configured file types. Read relevant cached results after checking size; record exact outcomes, failures and limitations. Reuse fresh focused evidence; no duplicate broad scopes.
- Documentation: clarify only the active presentation_architecture.md cache/text availability paragraph; verify invalidated links and record unchanged consumers. No instruction expansion.
- Independent QA GO/NOGO at every phase boundary. Ready: scaffold PR, inspect final diff/status and hand off to Co for merge.

## Work Units

### C\_1 — truthful-cache-notices

**Goal:** Correct cache/text availability claims and retain current response behavior.

**Cycle Number:** 1

#### Scope In

.pgmcp/config/defaults/presentation.yaml; existing fallback literal in mcp_server/presenters/text_presenter.py; tests/mcp_server/unit/test_presenter.py and tests/mcp_server/integration/test_execution_presentation_v3.py.

#### Scope Out

No server/cache/limiter algorithm, schema, config admission, public DTO or response-channel changes. No new test module/framework.

#### Deliverables

##### D\_1.1

Correct the two existing configured notice values and the existing generic presenter fallback literal without changing interfaces or behavior paths.

**Validates:**

**Type:** file_exists

**File:** ".pgmcp/config/defaults/presentation.yaml"

##### D\_1.2

Adapt existing shipped-config transport and presenter tests for failed/successful cache publication, bounded text, exact structured DTO/outcome and optional-key fallback; retain no-operation controls without prose snapshots.

**Validates:**

**Type:** file_exists

**File:** "tests/mcp_server/integration/test_execution_presentation_v3.py"

#### Exit Criteria

The three notice values are truthful; focused cache/text/operation controls and changed-file gates pass; no interface/transport/cache redesign, legacy tests or configuration admission change.

#### Obligations

- D_1.1 corrects two shipped config strings and the existing generic fallback per approved Design; review factual meaning directly.
- D_1.2 adapts existing transport cases for successful/failed publication, small/large DTO, exact structured data, original outcome and cache URI/readback; unit assertions use injected config markers and preserve omitted optional-key path.
- Retain existing no-operation transport cases and limiter marker/byte tests. Preserve inline traceback exclusion and all structured diagnostics.
- Commit GREEN with cycle_number=1. Mechanical literal/config correction and test maintenance need no artificial failing prose test or RED commit. REFACTOR commit only when planned cleanup actually changes files.

#### Verification

##### Focused behavior proof

**Method:** run_tests(scope="targets", targets=["tests/mcp_server/unit/test_presenter.py","tests/mcp_server/unit/presenters/test_text_budget_limiter.py","tests/mcp_server/integration/test_execution_presentation_v3.py","tests/mcp_server/integration/test_tool_attachment_transport.py"], tests=["python_tests"], timeout_seconds=300)

**Expected Result:** Changed cases and existing publication, limiter, no-operation and diagnosis controls pass; native arguments retained.

##### Appropriate changed-file gates

**Method:** run_checks(scope="targets", targets=["mcp_server/presenters/text_presenter.py","tests/mcp_server/unit/test_presenter.py","tests/mcp_server/integration/test_execution_presentation_v3.py"], checks=["python_format","python_lint","python_pyright"], timeout_seconds=300); separately run_checks(scope="targets", targets=[".pgmcp/config/defaults/presentation.yaml"], checks=["yaml_configuration"], timeout_seconds=120)

**Expected Result:** Native file gates pass without sending Markdown/YAML to Python checks.

#### Stop Conditions

- Stop for owner if a new delivery/config-admission policy or larger responsibility change is needed.
- Do not weaken criteria or excuse failing evidence. Return causally through the authorized earlier-phase route when required.

### C_2 — pipeline-test-consumer-repair

**Cycle Number:** 2

**Goal:** Repair the missed existing test consumer without expanding production scope.

**Depends on:** Completed C_1; do not replace or mutate its committed block.

#### D_2.1

Adapt the missed pipeline cache-fallback consumer to configured marker and structured/JSON behavior assertions; remove unconditional cache-reference instruction from its test configurations and preserve cache-success controls.

**Validates:** file_exists — tests/mcp_server/integration/test_pipeline_e2e.py

#### Exit Criteria

Existing pipeline cases pass without old-prose assertions or fabricated cache references; exact operation, fallback JSON and publisher calls remain verified; focused checks pass with no production changes.

#### Scope and verification

- Only tests/mcp_server/integration/test_pipeline_e2e.py. Replace the old-prose assertion with configured marker / exact structured DTO and JSON checks. Use the existing automatic cache-reference path rather than unconditionally rendering uri_reference as a follow-up instruction.
- Existing suite failure is retained: 1 failed / 2999 passed in 579.99s, native exit 1, receipt 1f1a5644fb0e405fa413a07002e7e610. The failure is the old fallback sentence assertion at line 231; it is a missed consumer, not a second product defect.
- Mechanical test maintenance requires no new RED case or prose snapshot. Use the existing failure as negative evidence and commit GREEN with cycle_number=2.
- run_tests(scope="targets", targets=["tests/mcp_server/integration/test_pipeline_e2e.py"], tests=["python_tests"], timeout_seconds=300).
- run_checks(scope="targets", targets=["tests/mcp_server/integration/test_pipeline_e2e.py"], checks=["python_format","python_lint","python_pyright"], timeout_seconds=300).
- Validation repeats the required configured suite after this repair and the branch gate for its expanded file inventory. Reuse the fresh configured production-Mypy result (192 source files, passed) while production/native configuration remains unchanged.
- The initial broad Python/YAML/Markdown gates all passed. No test failure or skipped gate is waived. Resume Implementation explicitly with resume_cycle="C_2", after independent Planning QA.
- A Planning-update information note emitted an unrelated scalar-sequence formatting error. Structured save/readback succeeded and confirmed both complete cycles; leave that generic note-formatting issue for Co triage, outside this notice-value correction.

## Phase Deliverables

### Validation

#### D\_1

Persist native configured full-suite, relevant branch/configured gates, focused behavior evidence and limitations.

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue524/validation.md"

### Documentation

#### D\_1

Clarify cache-failure wording versus actual operation delivery and client access limits in the active presentation reference.

**Validates:**

**Type:** file_exists

**File:** "docs/reference/presentation_architecture.md"

## Related Documents

- [Design](<design.md>)
- [Research and strategy](<research.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-19 | @imp planner | Record one mechanical correction cycle, exact file gates and phase-owned validation. |
| 1.1 | 2026-10-19 | @imp planner | Append C_2 for the missed pipeline-test consumer; retain failed Validation and C_1 unchanged. |

