<!-- pgmcp:v1 id=planning pv=1.0.0 pf=E5cXGU37lhDmDnjF sf=9PfER5JkyAoFQLRi -->

# Issue 473 — First-call Template Quality Planning

**Status:** PLANNING — independent review requested
**Version:** 0.1
**Last Updated:** 2026-10-03

## Authority, outcome and scope

Execute [Design 0.2](design.md) within [Research's Approved Strategy](research.md#approved-strategy). Independent QA returned GO Design → Planning for commit `b71a54bfadd701b9c485b0d23a8fef66a34ebfe7`; the human approved Planning on 2026-10-03. The earlier admission/filter P2 is closed at Design level, not yet proven in implementation.

Planning assigns cycles, dependencies, deliverable IDs, verification, evidence ownership and stop criteria. It does not change the selected design. The branch integrates into main; epic #72 remains an administrative parent. Generic schema/template consumption analysis remains issue #476.

The outcome is valid, useful starting points across all 19 shipped concrete packages. The approved limits remain: one main class in the six Python class families, explicit caller-authored facts, preserved caller interiors/literal values/presence semantics, clean break for changed input contracts and headings, no fallback/legacy bridge, and no additional runtime quality gate or formatter.

The human explicitly chose actual scaffolding and manual agent inspection instead of additional automated content/regression tests. This is the binding test-mode override to the generic Bug Planning/Implementation defaults. Existing valuable tests and native gates remain required; adapting existing inputs/expectations for changed contracts is permitted. Do not create snapshots, a context-matrix test harness, helper-only filter tests or tests whose only purpose is cycle administration. Keep test code under the same architecture/typing standards.

## Cycle order and ownership

| Cycle | Work unit | Dependency | Principal outcome |
| --- | --- | --- | --- |
| 1 | C_SHARED | Approved Design 0.2 | Shared filter availability, boundary normalization and template composition |
| 2 | C_CODE | C_SHARED | Six Python classes, two Pytest families and TypeScript first outputs |
| 3 | C_DOCS | C_CODE | Seven full-document and three tracking first outputs |
| 4 | C_RECONCILE | C_DOCS | Active consumer/standards consistency and complete inspection/tool evidence |

All cycles belong to `@imp implementer`. Dependencies are sequential to keep shared-source changes and evidence freshness understandable. The human/independent QA workflow owns phase approval; producer-delegated findings cannot authorize progression.

Each cycle includes its directly affected fixtures, existing assertions and active callers in the same coherent correction. It must not leave a newly changed contract depending on an old alias. Cycles 2/3 own their concrete input migrations, while cycle 4 closes cross-surface documentation/evidence. This sequencing introduces no compatibility mode.

## Durable evidence and working locations

Use `.pgmcp/temp/issue473/` for actual raw scaffold files, isolated fix probes and other disposable working output. Persistence must use the tool's admitted target path and exact filename; discover each selected context schema first. Do not manually create source/docs when a scaffold tool exists.

During cycle 1, scaffold the following English evidence documents as `generic_doc` using its then-current discovered schema; update them through `safe_edit_file`. When metadata requiredness changes later, new scaffolds use the new schema; existing authored reports do not undergo an automatic migration.

| Document under docs/development/issue473/ | Durable content | Owner |
| --- | --- | --- |
| `manual-inspection.md` | Case inventory, family/minimal/filled IDs, objective observations, generated-versus-caller attribution, native receipts, fingerprints and freshness/disposition | Every cycle; closure in C_RECONCILE |
| `first-output-evidence.md` | Exact admitted context and complete untouched output text for each final pair and material boundary/reproduction case; UTF-8 SHA256, path, tool call, source/schema identity and observation time | Every cycle that scaffolds |
| `tool-practice-findings.md` | Actual tool-route evidence, reproducible faults/friction, native/DTO facts, file effects, uncertainty, coverage limitations and follow-up ownership | Every cycle; closure in C_RECONCILE |
| `implementation.md` | Outcome-neutral completed-cycle and Design/preservation mapping with relevant evidence/test/gate indexes and deferred triage | C_RECONCILE |

Raw text in durable evidence is captured literally inside appropriately delimited fences, including boundary/newline facts described beside it. Do not turn example status/version/authors into claims about workflow approval. Preserve hashes and physical EOF/line-ending observations because Markdown display alone cannot prove exact bytes. Native/cache evidence is transient: read complete cached DTOs, preserve relevant factual rows and diagnostics durably, and retain exact replay requests. State explicitly when the DTO's own capture is bounded; do not claim unavailable native text was preserved.

An initial failing first output stays available even after a repair. A fix probe is a separately scaffolded instance with the same context, not an overwrite of the pristine evidence file. After template/source correction, scaffold anew; identify which output is the final first call. Temporary scripts/files are not added as permanent tests or included accidentally in the final diff.

## Common execution, verification and stop rules

Before each cycle, use `get_work_context` and `get_project_plan(issue_number=473)` to verify the active cycle, stored IDs and prerequisites. Read the authoritative Design and direct affected seams. Use only AGENTS-prescribed MCP writes, scaffolds, Git operations, checks/tests/fixes and workflow transitions.

### Test mode and commits

Use manual before/after scaffolds as the agreed characterization evidence. Existing tests already failing for the actual root cause may supply RED without duplication. In cycles 2/3, adapt meaningful existing context/expectation coverage before correction where this produces a genuine expected contract failure. A meaningful existing-test adaptation can be committed with `sub_phase="red"`; never create an empty/ceremonial RED commit or additional content assertions merely to satisfy a generic phase script.

Commit corrected code/contracts with `workflow_phase="implementation"`, its active `cycle_number` and `sub_phase="green"`, after that cycle's focused evidence passes. Planned cleanup earns a `refactor` commit only if it changes files and the affected checks are rerun. Mechanical documentation/test maintenance has no artificial RED. Keep branch state and tool-recorded planning data tracked where the workflow requires them; inspect the exact commit inventory.

After an objectively satisfied intermediate cycle, use `transition_cycle(to_cycle=N+1)` and refresh the work context. After cycle 4, request independent Implementation QA; do not autonomously enter Validation. Never use a forced transition as a substitute for missing evidence.

### Exact check selections

| Surface | Tool selection | Interpretation |
| --- | --- | --- |
| Changed production Python | `run_checks(scope="targets", targets=[actual changed production paths], profile="python_review")` | Configured format/lint/Mypy/Pyright; fix actual applicable findings using the typing playbook |
| Changed test/fixture Python | `run_checks(scope="targets", targets=[actual changed test paths], checks=["python_format","python_lint","python_pyright"])` | Test Mypy is not a required gate under the current documented policy |
| Pristine Python scaffold examples with baseline-clean fragments | `run_checks(scope="targets", targets=[actual raw example paths], checks=["python_format","python_lint"])` | Generated native quality; diagnose caller findings separately, no universal typing/dependency claim |
| Python syntax evidence if needed beyond scaffold preflight | `run_checks(scope="targets", targets=[actual raw example paths], checks=["python_syntax"])` | Syntax only |
| TypeScript raw example | `run_checks(scope="targets", targets=[actual raw TS paths], checks=["typescript_syntax"])` | Preserve configured/native scope; fixture strict checks and caller dependencies are separate evidence |
| Changed docs/affected links | `run_checks(scope="targets", targets=[actual changed docs and affected source consumers], profile="markdown_link_review")` | Offline fragments; no external-link reachability claim |
| Existing tests listed per cycle | `run_tests(scope="targets", targets=[listed existing paths], tests=["python_tests"])` | Native configured options remain in force; do not replace them for convenience |
| Isolated real fix use | `apply_fixes(scope="targets", targets=[isolated instance], fixes=["python_format","python_lint"])` | Read ordered results and actual changes; preserve pristine output and explicitly recheck |

The listed test sets are the default minimum impacted existing coverage. If a file does not change or a previous result remains fresh, reuse it with a source-based reason. If an additional existing consumer is invalidated, include its narrow coverage and record the reason. A shared root change affects the concrete family suite even when individual package files are untouched. Do not call this branch-wide Validation.

After a coherent filter/source/schema correction, refresh the running server/catalog through `restart_server(reason=...)` before public schema discovery and first-output evidence. Read and preserve transient run evidence before restarting. Then call `get_work_context`, verify the same branch/cycle and active package/schema/source fingerprints, and rediscover changed contexts with `scaffold_schema`. Test-fixture imports of edited files do not prove that a still-running public tool has adopted those changes. A failed refresh/admission is a cycle blocker; do not collect stale public output as corrected evidence.

Use existing enforce/report preflights according to their configured responsibilities. A report-mode raw output or a native failure may be retained for diagnosis, but is not passing cycle evidence. Any intentionally caller-owned negative case must be labelled and excluded from the clean-fragment quality claim.

### Common stop conditions

Stop before progression on an unfulfilled cycle objective, failing/unavailable required evidence, admission failure, preservation loss, unsound dependency or newly contradicted Design/Approved Strategy. An environmental limitation is missing evidence until its approved disposition is explicit. Fix within the current cycle only when the repair belongs to its approved contract; do not silently rewrite Planning, loosen checks or repair unrelated tools.

If discovery requires a new layer, generic #476 analysis, a new runtime gate, a compatibility bridge or caller-value transformation, stop and reopen the affected human decision. Tool findings unrelated to #473 are documented for later coordination; an actual #473 blocker cannot be hidden as deferred work.

## Per-cycle work and evidence

### Cycle 1: C_SHARED — shared environment and layout boundaries

**Dependency:** Approved Research and Design 0.2.

**Scope:** One generic boundary primitive and shared real filter setup; shared root/template seams for generated joins. Initialize evidence documents and exercise the existing scaffold/schema/edit/check/test routes.

**Files/seams:** mcp_server/services/template_engine.py; mcp_server/bootstrap.py; shared tier0/tier1/tier2 bases and affected existing macros; tests/mcp_server/fixtures/delivered_templates.py and installed_distribution.py; directly affected synthetic setup/valuable existing assertions.

**Exclusions:** No redesign, compatibility alias, extra automated content/regression suite, runtime quality gate, generic #476 analysis or unrelated tool repair. Full-suite and branch-wide checks remain Validation work.

| Deliverable ID | Description |
| --- | --- |
| D1_ENV | One shared real filter registration in the existing engine module exposes text_block and existing filters before admission and rendering, including delivered/installed fixtures, without a new layer or validation bypass. |
| D1_LAYOUT | Shared bases/macros own explicit joins and artifact EOF, with boundary-only normalization, retained presence semantics, first-line provenance and unchanged generic engine output. |
| D1_EVIDENCE | Actual representative scaffolds and boundary examples establish shared behavior; durable inspection/evidence and current-tool findings documents are initialized without adding automated content/regression tests. |

**Planned evidence mode:** Use Research raw outputs and actual boundary scaffolds as manual before-correction characterization. Run existing narrow coverage before edits. Reuse an existing failing assertion if it exposes the root cause; do not add filter/content tests solely to manufacture RED. This human-selected manual evidence mode overrides the default requirement for a newly added automated regression.

**Manual scaffold evidence:** Actually scaffold a representative Python class and populated adapter/model, a full document, Issue/PR, Commit and TypeScript through the registered public tool. Use additional padded text examples with spaces/tabs-only edge lines, internal CRLF/blank lines, hard-break spaces, fences, meaningful indentation and literal values. Read physical bytes/text and provenance/EOF; inspect absent versus explicitly empty cases. Remaining concrete expression/framing defects are recorded and owned by cycles 2/3, not declared corrected.

**Focused existing tests:** Use the exact target set below through run_tests; omit only with documented fresh evidence or lack of actual invalidation.

```json
{
  "scope": "targets",
  "targets": [
    "tests/mcp_server/unit/services/test_template_engine.py",
    "tests/mcp_server/unit/services/test_template_catalog.py",
    "tests/mcp_server/unit/services/test_template_graph.py",
    "tests/mcp_server/integration/test_target_startup.py",
    "tests/mcp_server/integration/test_scaffold_public_v3.py",
    "tests/mcp_server/integration/test_installed_distribution_v3.py",
    "tests/mcp_server/integration/templates"
  ],
  "tests": [
    "python_tests"
  ]
}
```

**Preservation obligations:** Design's boundary-only trimming, internal line endings/significant spaces/literal values, explicit presence, provenance and identity remain intact. Member descriptions retain their scope; facts come from callers. Re-scaffold affected cases after shared changes and record actual versions/configuration. All changes follow the clean break.

**Cycle-specific stop conditions:** Stop on admission unknown-filter failure, separate fake implementations, environment-option changes, caller-value/interior loss, provenance displacement, or a new architectural layer. Distinguish untouched generic renders from artifact-root outputs.

**Exact exit criterion (also saved structurally):** Shared filter availability is reviewed at both real admission/render seams and relevant fixtures; representative real scaffolds prove one terminal LF, generated joins and caller-value/interior preservation; narrow existing engine/catalog/startup/public-tool tests and applicable changed-file gates pass; actual tool findings and limitations are recorded. No full-suite/branch gates or new automated content tests.

### Cycle 2: C_CODE — Python and TypeScript first outputs

**Dependency:** C_SHARED.

**Scope:** Six Python class field contracts and body/model/import joins; two Pytest module-source overrides; TypeScript description/constructor layout; directly coupled known inputs and existing tests migrate in the same cycle.

**Files/seams:** .pgmcp/template_suite/{python_class,python_protocol,python_pydantic_config,python_pydantic_dto,python_adapter,python_worker,pytest_unit_test,pytest_integration_test,typescript_dto}/; affected shared Python/testing/TypeScript bases/macros; their existing family tests and test_shared_python.py; concrete active examples found to consume renamed fields.

**Exclusions:** No redesign, compatibility alias, extra automated content/regression suite, runtime quality gate, generic #476 analysis or unrelated tool repair. Full-suite and branch-wide checks remain Validation work.

| Deliverable ID | Description |
| --- | --- |
| D2_DOC_INPUTS | Six Python class packages adopt required class_description/module_description; TypeScript adopts required class_description with independently optional module_description; Pytest retains its separate module-source contract; known inputs are migrated without aliases or fallback. |
| D2_PY_LAYOUT | Python imports, method/test joins, empty indentation and composed ConfigDict/Field expressions meet the configured generated-quality objective; DTO field descriptions are not automatically repeated and Worker does not gain automatic __all__. |
| D2_TS_LAYOUT | TypeScript constructor assignments, optional blocks, brace edges and empty-field constructor match the approved presentation while preserving types/values and documentation presence. |
| D2_CODE_EVIDENCE | Six class, two Pytest and one TypeScript families have actual untouched minimal/filled first-output pairs plus targeted boundaries, manual semantic/presentation inspection and supporting current native evidence. |

**Planned evidence mode:** Where adapting existing valuable tests to the new public context first produces an intended failure, use that existing test as RED and commit the meaningful adaptation. Then correct schemas/templates and run the same scope. Do not add content/formatting assertions or automate the manual context matrix.

**Manual scaffold evidence:** Produce 18 final untouched first outputs: minimal/filled pairs for all nine code families. Inspect independent and identical explicit module/class prose, TypeScript absent/empty module cases, Pytest retained documentation, absent/filled fields, modest long composed model collections/calls, imports/aliases/future groups, methods/decorators and TypeScript zero/multiple assignments. Demonstrate required-field and removed-root-field rejection through the real tool without retaining failed writes.

**Focused existing tests:** Use the exact target set below through run_tests; omit only with documented fresh evidence or lack of actual invalidation.

```json
{
  "scope": "targets",
  "targets": [
    "tests/mcp_server/integration/templates/test_python_class.py",
    "tests/mcp_server/integration/templates/test_python_protocol.py",
    "tests/mcp_server/integration/templates/test_python_pydantic_config.py",
    "tests/mcp_server/integration/templates/test_python_pydantic_dto.py",
    "tests/mcp_server/integration/templates/test_python_adapter.py",
    "tests/mcp_server/integration/templates/test_python_worker.py",
    "tests/mcp_server/integration/templates/test_pytest_unit_test.py",
    "tests/mcp_server/integration/templates/test_pytest_integration_test.py",
    "tests/mcp_server/integration/templates/test_typescript_artifact.py",
    "tests/mcp_server/integration/templates/test_shared_python.py"
  ],
  "tests": [
    "python_tests"
  ]
}
```

**Preservation obligations:** Design's boundary-only trimming, internal line endings/significant spaces/literal values, explicit presence, provenance and identity remain intact. Member descriptions retain their scope; facts come from callers. Re-scaffold affected cases after shared changes and record actual versions/configuration. All changes follow the clean break.

**Cycle-specific stop conditions:** Stop on root/nested-description over-renaming, fallback/dedup, changed admitted empty module value, Python-body/literal modification, restored automatic Fields summary/__all__, unresolved generated native findings, or universal dependency/typing claims.

**Exact exit criterion (also saved structurally):** All nine code families have fresh inspected minimal/filled pairs under migrated contracts; clean caller examples have native-clean generated Python structure; TypeScript syntax and admitted fixture evidence are distinguished from dependency execution; existing affected family/shared tests and changed-file gates pass; context rejection/presence/value preservation are recorded and current-tool findings updated.

### Cycle 3: C_DOCS — document metadata and presentation

**Dependency:** C_CODE.

**Scope:** Seven mandatory document metadata schemas plus shared header/history; Architecture and Generic Doc presentation; document/tracking joins; affected known inputs and examples.

**Files/seams:** New shared/definitions/document-metadata.schema.json; seven full-document package context schemas/templates; shared Markdown document/section macros; tracking bases and Issue/PR/Commit where required; existing document/tracking tests and test_shared_documents.py; docs/reference/tools/scaffolding.md and concrete affected active anchors.

**Exclusions:** No redesign, compatibility alias, extra automated content/regression suite, runtime quality gate, generic #476 analysis or unrelated tool repair. Full-suite and branch-wide checks remain Validation work.

| Deliverable ID | Description |
| --- | --- |
| D3_METADATA | One shared required document_metadata revision contract and shared visible header/history serve exactly the seven full-document families, deriving current version/date from the final explicit revision without fabricated facts. |
| D3_PRESENTATION | Architecture hierarchy/concepts/constraints/decision presentation and Generic Doc direct sections preserve authored structure/order; all document/tracking joins and EOF meet the approved generated layout. |
| D3_DOC_CONSUMERS | Seven document package inputs, shared existing fixtures/tests, active scaffolding examples and concrete affected links adopt the clean break; Issue/PR/Commit retain their separate contracts. |
| D3_DOC_EVIDENCE | Seven full-document and three tracking families have actual untouched minimal/filled first-output pairs plus revision, decision, carrier/presence and whitespace boundary examples with manual inspection. |

**Planned evidence mode:** Adapt existing document fixtures/expectations to the new contract before GREEN when that yields a genuine schema/framing failure. Preserve meaningful tests for escaping/presence/structure; remove contradictory old-framing expectations by adapting their purpose. No new automated presentation/revision-content suite.

**Manual scaffold evidence:** Produce 20 final untouched first outputs: minimal/filled pairs for seven full documents and three tracking families. Inspect one/multiple explicit revisions, last-row/current-header agreement, supplied order/escaping, status/author facts, absent/empty carriers, Architecture Concepts/Constraints/numbered subsections, concise versus multiline decisions, Generic Doc custom order/lists/check state/fences, meaningful source/evidence labels and publishing body/envelope boundaries.

**Focused existing tests:** Use the exact target set below through run_tests; omit only with documented fresh evidence or lack of actual invalidation.

```json
{
  "scope": "targets",
  "targets": [
    "tests/mcp_server/integration/templates/test_architecture.py",
    "tests/mcp_server/integration/templates/test_research_artifact.py",
    "tests/mcp_server/integration/templates/test_design_artifact.py",
    "tests/mcp_server/integration/templates/test_planning_artifact.py",
    "tests/mcp_server/integration/templates/test_validation_artifact.py",
    "tests/mcp_server/integration/templates/test_reference.py",
    "tests/mcp_server/integration/templates/test_generic_document.py",
    "tests/mcp_server/integration/templates/test_shared_documents.py",
    "tests/mcp_server/integration/templates/test_issue.py",
    "tests/mcp_server/integration/templates/test_pr.py",
    "tests/mcp_server/integration/templates/test_commit_artifact.py",
    "tests/mcp_server/integration/test_installed_distribution_v3.py"
  ],
  "tests": [
    "python_tests"
  ]
}
```

**Preservation obligations:** Design's boundary-only trimming, internal line endings/significant spaces/literal values, explicit presence, provenance and identity remain intact. Member descriptions retain their scope; facts come from callers. Re-scaffold affected cases after shared changes and record actual versions/configuration. All changes follow the clean break.

**Cycle-specific stop conditions:** Stop on metadata invention, dual old/new context shapes, root fields surviving as aliases, table flattening of structured explanations, heading/link or association loss, mandatory history leaking into tracking, or changed arbitrary internal whitespace.

**Exact exit criterion (also saved structurally):** All ten document/tracking families have fresh inspected minimal/filled pairs; metadata/current revision, multiline decisions, hierarchy, lists/fences/check state and body/envelope separation are preserved; seven schemas reject removed legacy fields via existing validation; affected existing family/shared tests, edit preflights and link checks pass; practical tool findings are updated.

### Cycle 4: C_RECONCILE — active consumers and complete evidence

**Dependency:** C_DOCS.

**Scope:** Bounded active standards/instructions and source/mirror cleanup; close known consumers and freshness inventory; finalize practical current-tool findings and outcome-neutral implementation hand-over.

**Files/seams:** docs/coding_standards/CODE_STYLE.md, DOCUMENTATION_STANDARD.md and proven template-path wording in ARCHITECTURE_PRINCIPLES.md; .agents/workflows/create-issue.md and .github/prompts/create-issue.prompt.md; directly invalidated current references/links; manual-inspection.md, first-output-evidence.md, tool-practice-findings.md and implementation.md.

**Exclusions:** No redesign, compatibility alias, extra automated content/regression suite, runtime quality gate, generic #476 analysis or unrelated tool repair. Full-suite and branch-wide checks remain Validation work.

| Deliverable ID | Description |
| --- | --- |
| D4_ACTIVE_DOCS | Relevant Code Style/Documentation Standard guidance, evidenced template-path terminology, affected links and create-issue workflow/mirrored prompt agree with validated approved responsibilities, with no broad historical rewrite. |
| D4_19_FAMILIES | The inspection index accounts for all 19 shipped families and 38 final untouched minimal/filled outputs, targeted cases and evidence freshness; changed shared seams invalidate and refresh only affected evidence. |
| D4_TOOLS | Current-tool practice assessment covers real scaffold/schema/edit/check/test/fix use and bounded derived routes with reproducible findings, durable evidence, impact, uncertainty, safe isolated fixes and explicit limitations/follow-up disposition. |
| D4_HANDOVER | Implementation hand-over maps every deliverable and preservation obligation to actual evidence, known consumer closure and deferred triage; no unresolved issue473 blocker is hidden and no independent approval is claimed. |

**Planned evidence mode:** Mechanical documentation/cleanup and evidence closure need no artificial RED. Run only tests invalidated by a concrete change; preserve fresh earlier results. No production repair of unrelated findings and no new test harness.

**Manual scaffold evidence:** Reconcile all 19 families and 38 final minimal/filled pairs from cycles 2/3, plus targeted cases. Reuse them when final source/schema/filter fingerprints and context remain valid. If a shared source changes, re-scaffold every affected family/case before calling its evidence current. Read the completed findings and active publishing instructions against actual tool behavior.

**Focused existing tests:** No automatic test run for documentation-only changes; rerun only concretely invalidated existing coverage.


**Preservation obligations:** Design's boundary-only trimming, internal line endings/significant spaces/literal values, explicit presence, provenance and identity remain intact. Member descriptions retain their scope; facts come from callers. Re-scaffold affected cases after shared changes and record actual versions/configuration. All changes follow the clean break.

**Cycle-specific stop conditions:** Stop on a missing/unreadable raw output, stale evidence claimed fresh, a forgotten caller, hidden #473 blocker, unrelated tool repair, generic #476 analysis, fabricated historical facts, or content-test/runtime-gate scope expansion.

**Exact exit criterion (also saved structurally):** Active docs/instructions are reconciled with their sources and relevant links verified; final inventory contains 19 reviewed families/38 current first outputs without requiring uninvalidated reruns; all tool routes have actual evidence or an explicit justified limitation and findings have disposition; narrow invalidated tests/gates pass; independent Implementation review is requested before Validation, whose full suite/broad gates remain outstanding.

## Current-tool practice assessment

Use real work to assess `scaffold_schema`, `scaffold_artifact`, `safe_edit_file`, `run_checks`, `run_tests` and `apply_fixes`. Capture scoped selection/transport/metadata and derived-route behavior when encountered, including `get_project_plan`. This is a current correctness/usability assessment, not a pre-#460 score or an unsupported claim that every fault was introduced there.

Each route gets an evidence index with successful use, substantive outcomes and limitations. A finding records case/commit, source/server/package/native versions, prerequisites, exact request/context, expected behavior and its authority, actual envelope/rows/native diagnostics, file effects, reproduction steps, impact, uncertainty, workaround and disposition/existing follow-up. A compact response is not parsed as the full result; always read its cache for complete DTO facts.

Exercise fix behavior on an isolated separately scaffolded instance of a naturally encountered native formatting/lint finding before the template repair when available. Read the modified file and ordered fix rows; recheck through run_checks. If the real work offers no relevant mutation, a genuine successful no-op is recorded with that coverage limit rather than manufacturing a source/test defect. Fix success does not retroactively certify the untouched template output.

Reproduce the initial Design angle-bracket Markdown-preflight warning with a small admitted document case and compare the selected native/parser evidence. Its original receipt is recorded in Design. Classify/disposition it without silently repairing the adapter. Likewise, preserve any selection-invalid, missing dependency, bounded summary, transport or cache issue with its actual cause, rather than calling all nonpasses native defects.

Review the create-issue workflow and mirrored prompt against the actual authored-body/publishing envelope. Use controlled existing evidence; do not create/update a live external issue merely as a probe. If a derived route cannot be relevantly/safely exercised, record its coverage limit.

Generic schema-to-template consumption completeness remains #476. A concrete ignored-value reproduction from these actual examples is handed off with inputs/results; package-local correction is allowed only when it satisfies #473's approved contract. Broader analysis/enforcement strategy requires separate decision.

## Known-consumer and freshness closure

The explicit package/shared/test inventory in Design is the starting list. Cycle 2 owns code input migration; cycle 3 owns document input migration and affected links/examples. Cycle 4 verifies no remaining known active caller relies on removed root fields or ambiguous description fallback. Search results are inspected by context; nested member descriptions and unrelated resource metadata are not renamed.

C_RECONCILE checks relevant CODE_STYLE and DOCUMENTATION_STANDARD responsibilities, actual template source paths in ARCHITECTURE_PRINCIPLES, the active scaffolding reference and template usage guide, and both create-issue instruction copies. Reviewed valid surfaces are recorded unchanged. Preserve historical Research/#460 examples and dates; no mass authored-document conversion or broad standards cleanup.

The final family inventory is exactly:

- Full documents: architecture, research, design, planning, validation_report, reference, generic_doc.
- Python classes: python_class, python_protocol, python_pydantic_config, python_pydantic_dto, python_adapter, python_worker.
- Tests: pytest_unit_test and pytest_integration_test.
- Tracking: issue, pr and commit.
- TypeScript: typescript_dto.

Cycles 2/3 supply 18+20 = 38 final minimal/filled first outputs. C_RECONCILE accounts for all pairs and targeted cases using current shared/filter/schema/package identities. It does not rerun every pair solely because a new cycle began. A later changed shared macro or schema invalidates its dependent cases, even when their raw files still exist; refresh those cases and any affected narrow tests/gates. Documentation-only changes do not invalidate Python native evidence unless they change the rendered source or baseline.

Every pair records what was inspected, objective result, native support, caller/generated attribution and limitations. Counting files or hashes alone does not prove presentation, metadata or semantic preservation.

## Later-phase deliverables and evidence

These phase deliverables are stored alongside the cycles; they are planned obligations, not completed results.

| Phase | Deliverable ID | Description |
| --- | --- | --- |
| validation | V_FULL_TESTS | One complete native-configured run_tests(scope='configured') and exact native outcomes are recorded in Validation; rerun only when invalidated. |
| validation | V_BRANCH_CHECKS | Required branch-wide configured Python review and affected Markdown link evidence are recorded with failures/availability and parent-main scope. |
| validation | V_CORRECTED_BEHAVIOR | Validation maps 19-family manual first-output evidence, boundaries, consumer migration and current-tool findings to Design/Planning obligations and residual limitations. |
| documentation | DOC_CURRENT | Reconcile active references/instructions against validated final behavior and inspect source/mirror consistency; update only invalidated current claims and links. |
| documentation | DOC_TRIAGE | Finalize deferred current-tool findings and #476 evidence hand-off for coordination, with actual impact, reproduction and coverage limitations. |

Validation uses `run_tests(scope="configured")` for one complete native-configured run and `run_checks(scope="branch")` for the workflow-required branch-wide gates. Its configured default Python review remains in force. Run branch Markdown link review with `profile="markdown_link_review"` for affected document consumers where the Python profile cannot provide that evidence. Record the actual selected scope/rows and branch parent main; broad diagnostic selections are not silently substituted for mandated evidence.

Reuse fresh manual/context/native evidence where it proves the corrected behavior. Rerun the narrow actual scaffold reproduction if the full suite does not expose it. The human prohibition on additional automated content/regression tests remains binding in Validation; a newly discovered gap is discussed rather than silently turned into a new suite. Any failed/unavailable required gate is reported, not weakened or reinterpreted.

Documentation reconciles only current claims invalidated by validated final behavior, including source/mirror consistency and current findings disposition. Ready consumes the completed phase evidence and deferred triage; this plan does not grant PR merge approval or issue-closure authority.

## Structured payload and review discipline

The saved payload contains four sequential cycles. Cycle numbers, names, deliverable IDs/descriptions and exit criteria are identical to this document. Validation and Documentation IDs/descriptions also agree. No `contains_text` marker, file count or structural deliverable check is treated as substantive proof of an objective; manual/native review remains necessary. No automated semantic `validates` rules are added as a substitute for the agreed inspection.

Persist with `save_planning_deliverables(issue_number=473, planning_deliverables=...)`, then read the complete result and `get_project_plan` and compare the saved payload to the authored inventory. Do not hand-edit deliverables/state files. Document dependencies and stops remain binding even where the stored schema has no dependency field.

Planning-phase verification is limited to the authored document's enforce preflight, affected links, payload consistency and pre-commit reality check. No implementation tests or broad gates are run merely to approve a plan. Independent `@qa plan-verifier` reads primary sources and owns Planning → Implementation GO/NOGO.

## Risks and disposition

| Risk | Containment | Stop condition |
| --- | --- | --- |
| Filter only available after admission | Shared registration in both real environments and delivered/installed fixtures in C_SHARED | Any unknown shipped filter or fake admission implementation |
| Shared layout changes alter caller content | Boundary examples preserve full raw inputs/results and meaningful interior/literal facts | Value, internal whitespace or provenance loss |
| Base changes have broad package impact | Existing family suite and dependency-aware re-scaffolding; final 19-family inventory | Stale dependent evidence or missed consumer |
| New required inputs invalidate callers | Coupled migration in C_CODE/C_DOCS, clean schema rejection and active caller search | Alias/fallback retained or active known caller left incompatible |
| Native clean-output claim exceeds scope | Baseline-clean examples and causal finding attribution; no dependency/typing promise | Generated finding unresolved or caller defect hidden by repair |
| Large durable output evidence becomes unreadable | Separate readable index from exact raw contexts/output fences and hashes | QA cannot reproduce or identify pristine/final bytes |
| Tool finding silently expands scope | Reproducible log with issue473 blocker versus later-triage distinction | Unrelated adapter repair or generic476 analysis needed |
| Workflow defaults recreate unwanted tests | Explicit human-selected mode, valuable existing adaptations only | Additional content/regression/snapshot suite introduced |

## Planning hand-over and evidence

The scaffolded Planning nucleus and completed plan used enforce Markdown validation. The completed preflight passed without issues (`pgmcp://cache/runs/afa1f9fe4f5f4aa8b6d8a332df0264dd`). The configured targeted offline link review passed: 20 successful, 0 errors, 0 excluded, Lychee 0.24.2 (`pgmcp://cache/runs/f23dc0a36cb949f488d270588bd2dba5`). Complete DTOs were read; these checks do not certify implementation behavior.

The save returned four cycles and 20 total deliverables: 15 implementation deliverables, three Validation and two Documentation (`pgmcp://cache/runs/e90969dc8096479eb07ef69b6a6e67a9`). Complete `get_project_plan` readback (`pgmcp://cache/runs/4423ca4c6e2c4fa2b9066786ba898873`) exactly matched the submitted payload for cycle numbers/names, all 20 unique IDs/descriptions, exit criteria and later-phase deliverables. The authored tables/exit criteria were generated from those same data. Dependencies and manual obligations are explicitly documented because the stored schema has no dependency field.

Pre-commit reality check: each Design obligation has a cycle/evidence owner; shared admission/rendering and fixture responsibility are included; code/document inputs migrate with their correction; all 19 families and 38 final pairs are accounted for; no new test suite/runtime gate or generic476 work is scheduled. The plan and saved cycle payload derive from the same data. Implementation has not begun.

### Bug / Planning Hand-over

#### Scope

- Four dependency-ordered cycles with preservation, known-consumer migration, manual scaffold evidence, current-tool assessment and narrow existing verification.
- Excluded implementation execution, new design, compatibility bridge, additional automated content/regression coverage, generic476 analysis and full Validation.

#### Deliverables

- [Planning](planning.md), [Design](design.md) and [Approved Research](research.md#approved-strategy).
- Structured cycle and later-phase deliverables saved through MCP, matching the authored inventory.

#### Evidence

- Root cause and approved correction map to C_SHARED, C_CODE and C_DOCS; C_RECONCILE owns active-consumer and evidence closure.
- Human-directed actual scaffolding/manual inspection and valuable existing coverage replace any extra automated content/regression suite.
- Structured save/readback completed: four cycles and 20 total deliverables, exactly matching the submitted inventory; 20 unique IDs.
- Completed enforce preflight passed; targeted offline link review: 20 successful, 0 errors, 0 excluded. No implementation or broad tests were run for this Planning document.

#### Open Work

- Independent Planning review and authorized Implementation entry.
- Actual cycle execution must prove all planned objectives and disclose findings/limitations; broad suite and gates remain Validation work.

#### Review Request

- Review requested.

## Sources

- [Approved Design](design.md)
- [Approved Research](research.md#approved-strategy)
- [Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md)
- [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [Quality and Evidence Standards](../../coding_standards/QUALITY_GATES.md)
- [Type Checking Playbook](../../coding_standards/TYPE_CHECKING_PLAYBOOK.md)
- [Execution tool reference](../../reference/tools/quality.md)
- [Configured checks](../../../.pgmcp/config/checks.yaml)
- [Configured tests](../../../.pgmcp/config/tests.yaml)
- [Configured fixes](../../../.pgmcp/config/fixes.yaml)
- [Bug workflow contract](../../../.pgmcp/config/contracts.yaml)
- [Template engine](../../../mcp_server/services/template_engine.py)
- [Composition root](../../../mcp_server/bootstrap.py)
- [Delivered fixture](../../../tests/mcp_server/fixtures/delivered_templates.py)
- [Installed-distribution fixture](../../../tests/mcp_server/fixtures/installed_distribution.py)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-03 | @imp planner (Codex) | Four correction cycles with matching structured deliverables, bounded existing checks, actual scaffold/manual evidence, active consumer closure and current-tool findings obligations. |
