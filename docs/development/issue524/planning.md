<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=WI5iXHBKVOU91bYE -->

# Issue \#524 — Cache-notice correction plan

**Status:** Planning completed; independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-19

## Summary

One compact mechanical cycle corrects three existing notice values and adapts existing behavior evidence. No interface/config admission/transport/cache policy changes. No artificial RED or prose snapshots: the fix changes authored text values, while tests prove routing and data preservation.

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
