<!-- pgmcp:v1 id=design pv=1.0.0 pf=YApsrGTQgBUKFez2 sf=5--KpGf2wHUv2qAj -->

# Issue 483 — Native Markdown link validation

**Status:** Design — review requested  
**Version:** 0.2  
**Last Updated:** 2026-10-08

## Purpose

Define the smallest complete replacement of the owned Markdown checker within the approved Research strategy.

## Scope In

Removal of markdown_preflight; migration of Markdown check configuration, template output policies, extension routing and affected test consumers; honest native link outcomes before persistence.

## Scope Out

Runtime H1 or structure validation, Jinja introspection, compatibility wrappers, warning-only emulation, template wording changes, native parser development, historical documentation reconciliation and the separate active-document link baseline.

## Prerequisites

- Research v0.5 and the owner's clean-break/test decisions.
- Independent Research → Design GO from Beoordeel designplan on commit 507533be54f997849351da81b58185fd58b48ebf; only table-format P3 corrected in ab189a83fb1511c02f73c93a442d4d1f257345c5.

## Problem Statement

The owned markdown_preflight regex confuses valid angle delimiters with filesystem data and truncates parenthesized destinations. Its complete substantive responsibility is local-link observation and H1 detection. The owner selected a clean break: delegate links to existing Lychee and leave generated document structure with the template/package contract.

## Functional Requirements

- All delivered Markdown packages and extension-selected Markdown edits select the same native link-check profile. Explicit template identity, recognized header and extension keep their existing selection precedence.
- Use the existing markdown_links binding: lychee / links, native 0.24.2, configured args --offline, --cache=false, --include-fragments (anchor-only). Keep configured timeout_seconds=60.
- Check proposed content on its intended document location before writing. Resolve relative neighbors and self/TOC links against the new snapshot, including a still-absent target.
- Expose true missing local files/anchors as failed, and dependency/version inability as unavailable. Exclusions remain explicit native exclusions.
- Enforce writes only after required checks pass; report retains existing failed/unavailable write semantics and negative facts. Operational interruption remains a blocker under either policy.
- Retire the entire old package, its body/document check identities and profiles, and its package-only tests. No aliases, fallback checker, failure downgrade or heading emulation.

## Nonfunctional Requirements

- Generic CheckService, mutation services and wire contracts remain adapter-agnostic; no Lychee/Markdown special cases.
- Use the existing native dependency pin, materialized content transport, snapshot ownership, cleanup and atomic writer/race guards.
- Keep test additions bounded to missing behavior at public seams; reuse valuable existing coverage. No authored-content snapshots, configuration text/count assertions or old-behavior matrix.
- Historical decisions remain evidence; active documentation describes the new native dependency and mutation contract without new agent instruction layers.

## Constraints

- Approved Strategy in Research is binding. Native fragment scope must not silently change.
- H1 conformance at generation/release belongs to the existing suite procedure. Edited artifact structure is deferred to Coordination for issue121 reconciliation.
- No production/config/template/test edits or new mutation behavior evidence are claimed during Design.

## Options

### 1. Repair or relocate the custom regex

Rejected by the owner's native-tool/clean-break choice; it retains owned parser maintenance and the questioned responsibility.

**Cons:**

- Keeps the causal homegrown checker and old observation policy.

### 2. Keep a preflight shell that delegates to Lychee

Rejected: adds an unnecessary package and old identities without substantive responsibility.

**Cons:**

- Duplicates the existing Lychee adaptation and creates legacy routing.

### 3. Use the delivered native Lychee binding directly

Selected: retire the owned checker and converge Markdown consumers onto the existing native profile.

**Pros:**

- Existing content/selection support, pinned native semantics and proposed-content preparation.
- No new generic engine, protocol, dependency or parser.

## Decision

Retire markdown_preflight completely and use markdown_link_review / markdown_links for every delivered Markdown mutation consumer.

## Rationale

The defect disappears by removing the owned parser. The existing native adapter already accepts the evidenced destinations and supports proposed-content/self resolution. One native profile prevents body/document pseudo-distinctions from retaining the removed H1 contract.

## Production Design

| Surface | Resulting contract |
| --- | --- |
| .pgmcp/config/checks.yaml | Keep markdown_links with adapter_id=lychee, capability=links, timeout_seconds=60 and current native args. Keep markdown_link_review with checks=[markdown_links]. Remove checks/profiles markdown_document and markdown_body. Map .md to markdown_link_review. |
| Package policy.yaml | architecture, design, generic_doc, planning, reference, research, validation_report, issue and pr set output_profile=markdown_link_review. Workspace persistence remains unchanged. |
| Bundled packages | Remove mcp_server/bundled_adapters/markdown_preflight as a complete package. Existing Lychee package, manifest and dependencies remain authoritative. |
| Runtime consumers | Retain existing catalog admission, content preparation and run_content calls. No renamed tool API or new DTO is required. |
| Distribution | Existing directory-based bundle packaging follows the surviving package set; verify no separate delivery registry retains the retired package. Use the normal package/config activation and restart route. |

The names in this table are selected configuration contracts, not aliases for retired capabilities. Jinja source, input schemas and heading generation do not change. The removed H1 distinction is not reintroduced through another runtime adapter.

## Test Design

| Boundary | Coverage choice |
| --- | --- |
| Native syntax and snapshot semantics | Reuse tests/mcp_server/integration/adapters/test_lychee.py::test_native_self_toc_and_neighbor_snapshot. Adapt its valid/invalid fixture only if needed to include angle, reference and space/parenthesis destinations alongside relative/self/neighbor cases. Assert actual decisions and relevant diagnostics; no new broad grammar suite. |
| Scaffold and safe edit connected to delivered config | One shared isolated native fixture and six meaningful cases: each consumer has valid/enforce, invalid/enforce and invalid/report. Use delivered configuration/catalog/policy with the real CheckService and actual pinned native tool. Scaffold covers one full-document package and a body-package route without multiplying cases per package; safe edit covers header selection and extension fallback across its cases. Valid self-links must observe the proposed snapshot, not stale/absent target bytes. |
| Persist/isolate | Valid proposals persist; failed enforce leaves target absent or original bytes intact; failed report writes and retains failed evidence. Own scratch allocations are removed on normal native completion and source/neighbor bytes are unchanged by validation. Byte identity proves persistence/isolation, not a snapshot of authored document wording. |
| Unavailable/operational/cleanup policy | Reuse existing adapter dependency tests, generic mutation policy tests in test_scaffold_operation_v3.py and test_edit_operation_v3.py, and execution/test_content_input.py lifecycle tests. Do not duplicate their full matrices for Lychee. One additional consumer unavailable case is justified only if inspection shows the changed route is otherwise unproved. |
| Affected template tests | Remove imports/fixtures and repeated old preflight invocations from the nine package test modules and test_shared_documents.py. Retain valuable existing rendering/context/provenance tests without adding content assertions. Remove fixed old binding assertions; do not replace them with another editorial/configuration snapshot. Central native consumer evidence owns the new check connection. |
| Profile composition | Adapt execution/test_check_profiles.py to compose markdown_links with python_syntax through public run_content. Keep ordered independent outcomes and actual native execution; remove the fixed global check-count assertion. |
| Retired checker | Delete its package-only test module. No absence-of-name/source tests or checks that the old checker now rejects something. |

Test data may contain Markdown whose links cause an observable native outcome; assertions must concern decisions, diagnostics, persistence and isolation. Existing renderer tests retain their own contract but are not expanded for this issue.

## Contracts

### Existing content check interface

CheckService.run_content(profile_id: str, *, target_path: str, content: str) -> ContentExecution remains unchanged. ContentInputPreparer reads capability.requires_file, not a tool name. For Lychee it materializes proposed UTF-8 content in an owned scratch file.

### Existing check/v1 file transport

The request uses operation='links', absolute target_path, absolute input_path, configured args and execution_context.scratch_directory. Lychee adapter 2.0.0 declares inputs content/selection and requires_file=true. The intended target supplies the base URL; an exact self-URL remap points at the proposed input file. The engine does not parse Markdown or resolved native configuration.

### Native result and consumer contract

Native successful links yield passed; native link errors yield failed with actual diagnostics; missing/wrong native version yields unavailable. Native exit 2 is mapped to check failed/adapter exit 1 by the delivered adapter. Mutation DTOs retain profile, argument source/effective args, tool version, evidence, write facts and housekeeping. H1 presence is outside this result contract.

## Flow

Template render or edit proposal → configured profile selection → CheckService → owned proposed-content file → Lychee adapter/native 0.24.2 → result and scratch cleanup → existing consumer policy → atomic create/replace if admitted. The intended document never serves as a temporary validation file.

## State and Failures

| Observation | enforce | report |
| --- | --- | --- |
| passed | Persist the admitted proposal | Persist the admitted proposal |
| failed link/anchor | No write; retain diagnostics | Persist with failed validation facts |
| unavailable dependency/version | No write; retain inability | Existing documented write route with unavailable facts |
| Invocation failure (including transport/timeout) without unconfirmed termination | No write; unavailable facts remain visible | Existing write route with unavailable facts; no separate operational blocker |
| Input preparation failure, request rejection, cancellation or unconfirmed termination | Existing blocker; no write | Existing blocker; report does not bypass it |
| Cleanup problem | Existing separate housekeeping facts; no invented result | Same existing housekeeping contract |

Do not turn a missing native prerequisite into a link error or add an H1 failure. Existing collision/race protections and post-write reporting remain unchanged.

## Preservation

Preserve caller destinations, shared link macro output, rendered content, mutation policy meanings, configured selection precedence and writer concurrency guarantees. Deliberately cease the old warning-only link and runtime H1 contracts. No promise of identical diagnostics, native performance or stdlib-only execution.

## Transition and Cleanup

The package removal and all active consumer references form one coherent change. Remove stale fixture imports without carrying an emulation helper under a new name. The existing Lychee pin becomes a prerequisite for enforced Markdown mutation. Runtime activation must use updated package/config bytes. No compatibility period or bridge. If native behavior contradicts the approved baseline, stop for explicit human re-decision.

## Validation

### Causal/native feasibility

**Method:** Reuse the exact requests, witnesses, native version and observed outcomes in Research; these remain bounded feasibility evidence, not consumer-swap proof.

**Expected Result:** No custom parser remains responsible for the evidenced false positives.

**References:**

- [Durable Research evidence](<research.md#fresh-lychee-feasibility-evidence>)

### Changed consumers and native behavior

**Method:** Run focused affected behavior tests through run_tests, with real native prerequisites and isolated filesystem effects. Add/adapt only the missing cases above.

**Expected Result:** Correct proposals and failures reach persistence policy through delivered native bindings; no network requests.

### Integration and workspace acceptance

**Method:** Planning selects changed Python files with Git for applicable targeted checks, Markdown for documentchecks; final Validation uses scope=configured checks and the required complete configured test suite with adequate timeout. Do not pass mixed branch files blindly to Python checks.

**Expected Result:** Required runs complete and results are recorded honestly, including existing warnings or operational limits.

## Risks

### Native anchor checks can expose real defects that the old warning-only checker skipped.

Keep the stated baseline and report real failures. Do not weaken flags or silently repair unrelated documentation. Separate unrelated baseline work (#471).

### Template tests currently validate fictitious links through a warning-only fixture.

Remove that redundant preflight coupling and use a central temporary native-link fixture; do not fabricate dozens of neighbor files solely to preserve obsolete calls.

### Retired source paths can leave broken links in current issue artifacts.

For this issue's authoritative artifacts, use commit-pinned historical links when referring to deleted sources. Update only active affected references; historical #460/#473 records remain reviewed context.

### Scaffolding guarantees are confused with post-edit structure guarantees.

Keep H1 at the existing package release procedure and the artifact-edit structural finding deferred. No runtime heading workaround.

## Planning Consequences

Plan one bounded migration rather than a native parser project. Keep consumer/config/package/test cleanup coherent, with explicit meaningful behavior evidence. Implementation uses focused checks; Validation owns complete configured checks/tests. Active docs need only the changed link/native prerequisite contract and relevant reference repairs. Deferred structural work goes to Coordination for issue121 reconciliation; Design does not sequence its implementation.

## Sources

- [Delivered check configuration](<../../../.pgmcp/config/checks.yaml>)
- [Native adapter and version mapping](<../../../mcp_server/bundled_adapters/lychee/check.py>)
- [Native dependency pin](<../../../mcp_server/bundled_adapters/lychee/dependencies.json>)
- [Content preparation](<../../../mcp_server/execution/content_input.py>)
- [Generic check execution](<../../../mcp_server/execution/check_service.py>)
- [Scaffold consumer](<../../../mcp_server/services/scaffold_operation.py>)
- [Edit consumer](<../../../mcp_server/services/edit_operation.py>)
- [Existing native snapshot test](<../../../tests/mcp_server/integration/adapters/test_lychee.py>)
- [Mutation policy tests](<../../../tests/mcp_server/integration/test_edit_operation_v3.py>)
- [Quality obligations](<../../coding_standards/QUALITY_GATES.md>)

## Related Documents

- [Research and durable feasibility evidence](<research.md>)
- [Existing Lychee adapter contract](<../../reference/execution-adapters.md>)
- [Mutation validation policy](<../../reference/tools/editing.md#validation-and-result>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-08 | @imp designer | Define complete native link-check migration and bounded behavioral evidence within the approved clean break. |
| 0.2 | 2026-10-08 | @imp designer | Correct the report contract for invocation failures without unconfirmed termination after independent QA finding. |
