<!-- pgmcp:v1 id=planning pv=1.0.0 pf=CscfYyDLqj0OeHml sf=5--KpGf2wHUv2qAj -->

# Issue 483 — Native Markdown migration plan

**Status:** Planning — review requested  
**Version:** 0.3  
**Last Updated:** 2026-10-08

## Purpose

Sequence the approved Design without changing its ownership, native policy or test boundaries.

## Scope In

One implementation cycle for native consumer behavior, complete package/config migration and affected test cleanup; compact Validation and active reference updates.

## Scope Out

Compatibility/legacy, old-warning/H1 regression tests, runtime structure validation, parser development, template content changes and unrelated documentation baseline repair.

## Prerequisites

- Independent Design → Planning GO on 9a0f789ba9236a065f2126e16f8a6d9250347bb4.
- Research Approved Strategy and Design v0.3, including safely-ended invocation failures under existing report semantics and the explicit required branch Validation gate.

## Summary

C483.1 delivers the complete replacement as one coherent cycle. Behavioral RED exposes the missing native integration before GREEN migrates the real configuration and retires the owned checker. Mechanical fixture/import cleanup needs no artificial failing-test stage. Implementation proves only changed surfaces; Validation owns the complete configured check/test runs.

## Dependencies

- Existing Lychee adapter 2.0.0 and native 0.24.2 must be available in the isolated test runtime.
- Preserve --offline, --cache=false, --include-fragments and configured timeout 60.
- Reuse generic policy/lifecycle tests for unavailable and operational stop distinctions; do not introduce engine changes to satisfy invented failure policy.

## Risks

### Safe report semantics are accidentally tightened.

Use corrected Design v0.2 table: safely-ended invocation failures are unavailable without a separate blocker; preparation/request rejection/cancellation/unconfirmed termination remain blockers.

### Test cleanup becomes an expanded template-content audit.

Remove redundant checker coupling without adding authored-content assertions or native calls for every package. Central behavior cases and existing render tests provide distinct evidence.

### Full configured gates reveal unrelated existing defects.

Record precise facts and obtain explicit disposition if blocking; do not change check/native scope silently.

## Milestones

- Validation: use Git to select actual applicable changed files for per-type gates; reuse fresh implementation evidence. Always run the required run_checks(scope="branch", profile="python_review", timeout_seconds=600), using existing per-check configured-target filtering and unchanged native arguments. Also run run_checks(scope="configured", timeout_seconds=600) for the planned additional workspace-wide configured checks; this supplements and does not replace the branch gate. Run run_tests(scope="configured", tests=["python_tests"], timeout_seconds=1200) for the full native-configured suite with unchanged native args. Respect the documented 1800-second client window. Do not split, shorten or omit the full suite because the change is small or tests are mechanical.
- V483.1: scaffold one compact validation.md recording exact relevant invocation/scope/outcome, native version, changed behavior, full-run totals, warnings and limitations. Run IDs are supplemental. Any required gate failure remains a blocker unless explicitly resolved or accepted by the human; do not carry old #481 exceptions into this issue.
- DOC483.1: targeted additions in docs/reference/tools/scaffolding.md and editing.md describing Lychee local links/anchors/native availability and no runtime H1 requirement. Link the existing package maintenance procedure for generated structure; no new instruction layers. Run only affected document checks.
- Independent QA at implementation/Validation/Documentation gates follows current phase instructions; producer reports facts without self GO. Ready prepares/submits PR and pushes all approved work, then hands Coordination the exact evidence, residual/deferred tracking and end-issue merge request; no producer merge.

## Work Units

### C483.1 — Replace owned Markdown preflight with native Lychee

**Goal:** Connect proposed Markdown mutation content to native validation and remove the redundant owned checker.

**Cycle Number:** 1

**Owner:** @imp implementer

#### Scope In

Nine policy.yaml consumers; .pgmcp/config/checks.yaml; complete bundled markdown_preflight package; affected integration template/profile tests; central native mutation behavior fixture/test; bounded native snapshot witness.

#### Scope Out

Native/tool internals, generic mutation engine, heading generation and authored section wording.

#### Deliverables

##### D483.1.1

Durable native Markdown mutation behavior coverage through scaffold and safe edit, with bounded valid/enforce, invalid/enforce and invalid/report cases and existing native snapshot coverage reused.

##### D483.1.2

Complete clean-break removal of markdown_preflight and obsolete bindings/profiles, with all nine Markdown output policies and .md routing using the existing native markdown_link_review profile.

##### D483.1.3

Retired package-only tests and fixture coupling removed, valuable renderer/profile behavior retained, affected tests and scoped Python gates passing without compatibility or old-behavior coverage.

#### Exit Criteria

Six central native consumer cases pass; affected template/profile tests and selected native snapshot/dependency/lifecycle evidence pass; applicable gates pass on Git-selected changed Python files; all active Markdown routes use the delivered native binding; no compatibility path or new runtime H1 check; reviewed cleanup is complete.

#### Dependencies

#### Obligations

- First add/adapt durable central mutation coverage in tests/mcp_server/integration/test_markdown_mutations.py using real delivered config/catalog and native Lychee. Prove a focused expected-new-behavior RED on current routing; no characterization of old warning/H1 rules.
- Then perform D483.1.2 as a complete migration: remove owned package/checks/profiles; all nine Markdown policy.yaml use markdown_link_review; .md maps to that profile; existing markdown_links binding and native args/pin stay unchanged.
- Finally D483.1.3 removes test_markdown_preflight.py, retired fixture imports/invocations and fixed binding/count assertions in affected tests. Retain valuable existing renderer behavior. Recompose test_check_profiles through native markdown_links and python_syntax. Central native coverage avoids per-template checker multiplication.
- Six consumer cases cover each of scaffold/edit with valid-enforce, invalid-enforce and invalid-report; distribute full-document/body and header/extension selection within these cases. Use real missing file/anchor observations and proposed self/neighbor resolution. Add one unavailable consumer case only if existing layered evidence leaves a concrete gap.
- Adapt existing native snapshot data only for missing angle/reference/space-parenthesis coverage. Keep diagnostics/persistence/isolation assertions; no full-document snapshots or deletion inventories.
- Commit RED, GREEN and REFACTOR as required by live implementation context. Keep incomplete RED evidence explicit. Mechanical cleanup follows the cycle's behavior migration.
- Update references to removed sources only in the current authoritative issue artifacts using commit-pinned historical source links; no mass rewrite of historical issue documentation.

#### Verification

##### Focused RED

**Method:** run_tests(scope="targets", targets=["tests/mcp_server/integration/test_markdown_mutations.py"], tests=["python_tests"], args={"python_tests":["-k","enforce"]}, timeout_seconds=180)

**Expected Result:** A meaningful new consumer-contract failure before native routing; no fixture/import or unavailable prerequisite failure accepted as RED.

##### Focused GREEN and cleanup

**Method:** run_tests(scope="targets", targets=<existing affected test files selected from Git>, tests=["python_tests"], timeout_seconds=300). Run test_lychee.py with -k test_native_self_toc_and_neighbor_snapshot when that case changes; reuse still-valid dependency/lifecycle facts and run only unresolved surfaces.

**Expected Result:** Changed consumer, template and profile behavior passes; native version and outcomes observed, no live external network.

##### Applicable Python gates

**Method:** From Git changes versus main and pending work, select existing changed .py/.pyi files (exclude deleted paths). run_checks(scope="targets", targets=<ChangedPy>, checks=["python_format","python_lint","python_pyright"], timeout_seconds=600). If production Python changes beyond deletions, separately use python_types on applicable production targets. Never send Markdown/YAML to Python checks.

**Expected Result:** Scoped gates pass with native configuration intact; no global typing/lint disables.

##### Document gate

**Method:** run_checks(scope="targets", targets=<changed current Markdown artifacts>, checks=["markdown_links"], timeout_seconds=120)

**Expected Result:** Native local links/anchors pass; deleted source references use historical commit-pinned URLs where applicable.

#### Stop Conditions

- Native prerequisite/version unavailable, operational test interruption or a test setup failure: stop and report incomplete evidence rather than claim RED/GREEN.
- Proposed-content/base/self mapping contradicts Research, or changes to the existing Lychee adapter, generic runtime or DTO/API contracts appear required: stop and explicitly reopen the design question with the owner; do not add ad-hoc functionality.
- Actual native link failures in unrelated active docs: report and route to #471, do not weaken flags or repair unrelated scope.
- Any need for compat/legacy or restored H1 checking: human re-decision required.

## Phase Deliverables

### Validation

#### V483.1

Compact durable Validation evidence: focused changed behavior, required branch-scoped gates, additional workspace configured checks and full configured native test suite; exceptions/blockers explicit.

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue483/validation.md"

### Documentation

#### DOC483.1

Active scaffold/edit references state native local-link/anchor validation and prerequisite; current issue source references remain valid and structural follow-up is indexed.

**Validates:**

**Type:** file_exists

**File:** "docs/reference/tools/editing.md"

## Related Documents

- [Design v0.3](<design.md>)
- [Research and deferred structure finding](<research.md>)
- [Execution budgets](<../../setup/README.md#option-c-codex-setup>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-08 | @imp planner | Plan one coherent native-check migration with focused behavior evidence and mandatory complete Validation runs. |
| 0.2 | 2026-10-08 | @imp planner | Make the owner's stop boundary explicit for existing adapter, generic runtime and DTO/API changes. |
| 0.3 | 2026-10-08 | @imp planner | Restore mandatory branch gates and mirror the Validation obligation in the stored deliverable. |
