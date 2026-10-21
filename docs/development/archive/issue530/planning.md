<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=WI5iXHBKVOU91bYE -->

# Issue \#530 — one-cycle note policy correction

**Status:** Planning complete — independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-20

## Purpose

Execute approved Design without expanding policy or presentation architecture.

## Scope In

TextPresenter.present_notes; directly affected public note and SDK/readback tests; one common-reference clarification.

## Scope Out

Producer/persistence/protection/API/config changes, new defaults/frameworks, compatibility, harness/version matrices and Windows lifecycle repair.

## Summary

One cycle C_1 with D_1.1–D_1.2. Add the real public defect reproduction, confirm RED before source correction, connect existing policy, verify focused behavior and target gates. Validation owns full native/branch/configured runs. Independent QA governs every phase boundary.

## Dependencies

- Research1.0 GO c9b57d91 and Design1.0 GO d52e9708; inherited owner clean-break/public-contract strategy remains binding.
- Existing configured_workspace, factories, real SDK helpers and current native tool configuration; no new fixture graph.

## Milestones

- Validation: run_tests(scope='configured', tests=['python_tests'], timeout_seconds=1800), no args override, one complete native suite preserving defaults/parallelism/coverage activation. No split, new coverage threshold or suppressed failure.
- Validation: run_checks(scope='branch', checks=['python_format','python_lint','python_pyright','markdown_links'], timeout_seconds=600); per-check configured selection. No YAML/schema files changed, so do not request empty YAML/JSON gates.
- Validation: run_checks(scope='configured', checks=['python_format','python_lint','python_types','python_pyright'], timeout_seconds=600). Mypy remains production-only; no mandatory test-Mypy expansion.
- Scaffold/update compact validation report and request independent Validation→Documentation review. Document only validated behavior and preserve negative/incomplete evidence.
- Documentation: update only the common active presentation reference as needed; targeted markdown_links and independent Documentation→Ready review. Reuse fresh implementation evidence.
- Ready: inspect clean intended branch/diff; scaffold concrete PR with closure, evidence/residuals; submit/attach PR, independent final review and end-issue handoff to Co. Producer does not merge or start next issue.

## Work Units

### C\_1 — Restore configured normal note rendering

**Goal:** Remove the causally proven normal note failure using existing policy at its owner.

**Cycle Number:** 1

**Owner:** @imp implementer

#### Scope In

mcp_server/presenters/text_presenter.py; tests/mcp_server/integration/test_execution_presentation_v3.py; tests/mcp_server/unit/test_presenter.py. Existing formatter/composition tests are verification companions.

#### Scope Out

No manager/tool/DTO/schema/config/loader/enforcement changes, no hidden default or producer-side stringify, no unrelated timing repair.

#### Deliverables

##### D\_1.1

Supply existing global FormattingConfig and selected tool max_items at TextPresenter.present_notes; preserve template priority, grouping, raw parameters and native error handling. No defaults, producer, public contract or config change.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "mcp_server/presenters/text_presenter.py"

##### D\_1.2

Use existing SDK/fixture surfaces for one isolated append plus independent get_project_plan readback; retain full original/appended facts. Add a small public note policy parametrization and missing-limit/nested-value diagnostic checks; reuse existing scalar/syntax/formatter coverage without prose snapshots or copying the research probe.

**Owner:** @imp implementer

**Validates:**

**Type:** file_exists

**File:** "tests/mcp_server/integration/test_execution_presentation_v3.py"

#### Exit Criteria

Meaningful public SDK RED then GREEN; readable evidence note follows existing policy and independent readback proves preserved C_1/new C_2 facts; focused note/formatter/composition behavior and exact changed-file gates pass; no policy/default/public-shape change or unrelated fix.

#### Obligations

- Start with one real SDK append/readback case in the existing integration surface. Use configured_workspace/shared factories and controlled read-only evidence/admission, with no live mutation. Preserve complete existing block, append references/descriptions/criteria and successful operation outcome.
- Add only small note policy cases for global/local list/tuple order, configured omission/empty values and honest missing-limit/nested diagnostics. Existing scalar, malformed-template and native formatter cases remain useful; no prose snapshots.
- Keep note inputs untouched, local/global priority and group order unchanged. Reuse existing config; tools without max_items receive no fabricated limit.
- After focused GREEN, restart through existing server route, load fresh get_work_context and verify health before final activation claims. Tool inputs/outputs/schema are unchanged.
- Before commit/review, inspect substantive outcomes, not only tool success; stop if a required check fails. Reuse fresh evidence after semantic-preserving formatting only with explicit justification.

#### Verification

##### Behavioral RED

**Method:** run_tests(scope='targets', targets=['tests/mcp_server/integration/test_execution_presentation_v3.py'], tests=['python_tests'], args={'python_tests':['-n','0','-k','planning_update_note']}, timeout_seconds=300)

**Expected Result:** The new isolated real SDK append reaches success and persists correctly but fails on readable note evidence; record actual intended RED, then commit cycle_number=1/sub_phase='red'.

##### Focused GREEN

**Method:** run_tests(scope='targets', targets=['tests/mcp_server/integration/test_execution_presentation_v3.py','tests/mcp_server/unit/test_presenter.py','tests/mcp_server/unit/presenters/test_collection_text_renderer.py','tests/mcp_server/unit/presenters/test_text_presenter_composition.py'], tests=['python_tests'], timeout_seconds=600), native defaults/no args override.

**Expected Result:** All selected cases complete/pass; preserve diagnostics and normal composition. No broad directories or full-suite run during Implementation.

##### Target gates

**Method:** run_checks(scope='targets', targets=['mcp_server/presenters/text_presenter.py','tests/mcp_server/integration/test_execution_presentation_v3.py','tests/mcp_server/unit/test_presenter.py'], checks=['python_format','python_lint','python_pyright'], timeout_seconds=300)

**Expected Result:** All pass on actual changed files. Commit/push GREEN under cycle1 and request independent Implementation→Validation; no forward waiver.

#### Stop Conditions

- New output/schema/channel/cache/default/compatibility policy or broader fix needed: return to owner, do not invent it.
- Required checks/tests fail or are incomplete: retain FAIL, diagnose and use bounded repair/review; no automatic rerun-until-green, exclusions or threshold changes.
- Unexpected implementation gap after phase entry: auditable earlier-phase return under owner's standing18Oct approval, with independent review. No forward gate exception.

## Phase Deliverables

### Validation

#### D\_1

Record exact full native run, branch/configured gates, behavioral proof, preservation and honest negative/incomplete history.

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue530/validation.md"

### Documentation

#### D\_1

Clarify the existing global formatting/per-tool limit semantics for normal notes in the common presentation reference; no agent instruction expansion.

**Validates:**

**Type:** file_exists

**File:** "docs/reference/presentation_architecture.md"

## Related Documents

- [Approved Design](<design.md>)
- [Research and evidence](<research.md>)
- [Quality standards](<../../../coding_standards/QUALITY_GATES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-20 | @imp planner | One bounded RED/GREEN cycle, exact target/native gates and durable phase deliverables. |
