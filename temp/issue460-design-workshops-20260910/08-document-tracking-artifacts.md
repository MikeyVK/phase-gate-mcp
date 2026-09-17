<!-- C:\temp\pgmcp\temp\issue460-design-workshops-20260910\08-document-tracking-artifacts.md -->
<!-- template=design version=5827e841 created=2026-09-10T09:24Z updated= -->
# W08 — Documents that can carry the actual workflow outcome

**Status:** SUPERSEDED PREPARATION — canonical W08 draft submitted for independent review  

The coordinated source-led design now lives in
[Document and Tracking Artifact Contracts](../../docs/development/issue460/design-document-tracking-artifacts.md).
This older preparation is retained as history only; its shortened capacity inventory and
requiredness proposals are not implementation authority.

**Owner:** DI-03 document/tracking; DI-07 supplies semantic requirements  
**Dependencies:** W06 schemas/shared definitions; W11 nineteen workflow variants  
**Decision nucleus:** Named semantic sections and finite records, not one content dump or a recursive document language.

## 1. Purpose and authority

Research, Design, Planning and Validation should be scaffoldable with the information their phase requires. A structurally valid first document is not a completed phase. Tracking content must remain body content, not tunnel GitHub/MCP envelope fields.

## 2. Scope and exclusions

Seven retained document purposes plus commit/issue/pr. No workflow engine redesign, auto-history, generic lifecycle dates, editor, artifact discovery tool or implicit issue administration.

## 3. Binding inputs

DI-03/DI-07 intake, F-01/F-06/F-07/F-09/F-12, I-12/I-13/I-15, [workflow-carrier Research](C:/temp/pgmcp/docs/development/issue460/research-findings.md:474), [tracking field decisions](C:/temp/pgmcp/docs/development/issue460/research-findings.md:908).

## 4. Proposed decisions

| ID | Proposal |
|---|---|
| W08-A | Keep existing accurate document/tracking IDs |
| W08-B | Separate common semantic core from artifact-local optional sections |
| W08-C | Flat bounded records for repeated evidence/alternatives/risks; no recursive section AST |
| W08-D | Planning document projects shared operational facts explicitly to the existing planning API |
| W08-E | Persisted tracking file and downstream submitted message/body are distinct surfaces |

## 5. Responsibilities and boundaries

DI-07 says what a phase outcome must express. DI-03 owns field names, schema requiredness and rendering. contracts.yaml retains phase actions/authority. Shared link/issue/checklist definitions retain presentation-neutral values. Templates never decide workflow GO.

## 6. Options and rationale

A single content:string would make missing phase capacities undiscoverable. A recursive document AST would make authoring burdensome. Choose named optional content sections with limited reusable records and preserve authored Markdown where structure does not have a machine consumer.

## 7. Detailed design

### Required nucleus and optional capacities

| ID | Required | Optional named capacity |
|---|---|---|
| research | title, purpose, problem_statement, goals | scope, exclusions, background, evidence, consumers, findings, risks, open_questions, approved_strategy, expected_results, references, related_docs |
| design | title, purpose, problem_statement, decision, rationale | requirements, constraints, alternatives, production_design, test_design, interfaces, flows, state_and_failures, preservation, transition_and_cleanup, validation_obligations, risks, planning_consequences, open_questions, sources |
| planning | title, purpose, summary, nonempty work_units | exclusions, dependencies, milestones, risks, sources |
| validation_report | title, scope, nonempty evidence | exclusions, obligation_mapping, targeted_evidence, failures, caveats, preservation, containment, risks, deferred_work |
| architecture | title, purpose, concepts | boundaries, relationships, constraints, decisions, diagrams, bounded subsections, links |
| reference | title, purpose, nonempty sources | api_entries, usage_examples, sections, related_docs |
| generic_doc | title, purpose, summary | scope, prerequisites, key_changes, migration_steps, checklist, faq, sections, links |

Required narrative fields are nonblank. Named optional Markdown blocks are strings; omission means no section, not “None” text or a fabricated completed outcome. Collections are ordered and typed. A workflow may require an optional schema section before completion; that is not a reason to make every workflow's section mandatory in every initial scaffold.

Status/version/date in the **document body** are optional explicitly caller-authored document facts if retained; they are not automatic source-provenance created/updated fields. No author/contributor without a demonstrated consumer. Render requirements as requirements, not unchecked tasks.

### Repeated records

All records closed; source references reuse Link(label,target).

- Alternative: name, description, benefits:string[], costs:string[].
- Decision: decision, rationale, alternatives_considered:string[].
- Evidence: claim, observation, sources:Link[], optional invocation, observed_result and observed_at. No implied successful result or fabricated freshness.
- Risk: description, consequence, mitigation.
- API entry: name, description, signatures:string[], parameters:parameter records, returns, errors.
- UsageExample: description, language, code.
- Section: heading, content; no recursive child sections.
- FAQ: question, answer.
- WorkUnit: id:NonBlankText, title:NonBlankText, scope:NonBlankText, exclusions:tuple[NonBlankText,...], deliverables:nonempty tuple[Deliverable,...], obligations:tuple[NonBlankText,...], verification:nonempty tuple[EvidenceRequirement,...], exit_criteria:NonBlankText, dependencies:tuple[NonBlankText,...]; optional rollback:NonBlankText, risks:tuple[Risk,...], operational_cycle_number:PositiveInt.
- Deliverable: id:NonBlankText, description:NonBlankText, validates:ValidationRule|null. ValidationRule uses exactly the existing file_exists/file_glob/contains_text/absent_text/key_path alternatives and their required file/text/path fields; it is not a new expression language.
- EvidenceRequirement: obligation:NonBlankText, method:NonBlankText, expected_result:NonBlankText. This states evidence still to obtain, not an observed successful result.

Only share definitions between packages when semantics actually match. There is no phase-document/ namespace or generic field registry by convenience. Source references and related_docs render separately when both supplied; the current conditional choice must not discard one.

Reference-style Markdown rendering assigns collision-free labels and emits complete definitions for every used label. Issue IDs are positive integers; renderer adds #. ChecklistItem always has text and checked:boolean. Presentation never invents state.

### Planning ↔ operational planning

[CycleModel and CyclePlanningModel](C:/temp/pgmcp/mcp_server/schemas/deliverables.py) remain the operational tool contract. For workflows that use cycles, a work unit has an explicit operational_cycle_number when it represents a cycle; its deliverables and direct exit_criteria project to the corresponding existing cycle fields. title projects to name. Dependency/narrative/risk/rollback facts stay in the document if no runtime consumer exists. Non-cycle units carry no cycle number.

Do not infer operational numbers by document order, rename exit criteria through prose, or claim a generic docs/epic unit can be saved by an API that accepts only CyclePlanningModel. [save_planning_deliverables](C:/temp/pgmcp/mcp_server/tools/project_tools.py:398) remains separately called with its exact schema. No automatic document parser/synchronizer is proposed; human/agent authors keep shared facts equal, with a design-time parity check for examples and later boundary tests.

The proposed Deliverable/ValidationRule records preserve the existing operational shape without adding runtime planning behavior. Operational projection must also satisfy PhaseCyclesModel's total=count and sequential 1-based numbers; non-cycle work units are excluded from that projection, not silently renumbered. There is no stop_go wrapper with a single exit_criteria field. This proposed schema is checked against the operational model before canonical schema authoring.

### Tracking artifacts

| ID | Required | Optional / prohibited |
|---|---|---|
| commit | type, subject | scope, body, breaking_change:boolean, conditional breaking_description, footer, issue references; no tool routing/branch controls |
| issue | problem | summary, expected, actual, context, ordered reproduction_steps, links; no title/labels/milestone/assignees envelope |
| pr | changes, deferred_work:array | summary, testing/evidence, checklist, breaking_changes, links, closing issue IDs; no tracking_state or mandatory tracking issue |

PR deferred_work is explicitly [] for “None”; populated entries carry descriptions and relevant evidence. Avoid a duplicate has_deferred_work boolean. Commit punctuation is renderer-owned, but content is not silently recased or line-wrapped. Repository-specific commit-type vocabulary remains configured content, not generic server Python.

### Commit first-line seam

Every persisted artifact begins with approved provenance. A conventional commit message begins with its subject. Therefore **the complete saved commit artifact is not promised to be directly usable as a git commit message**. Current GitManager constructs a message through separate inputs; no existing file-stripping consumer proves otherwise.

Recommendation: describe the file as a persisted draft whose message content begins after its one metadata line; the caller supplies the downstream tool's ordinary message/body input. No new generic stripping tool or mutation of header format. If direct whole-file submission is required, it needs an explicit approved consumption seam before claiming compatibility. Issue/PR bodies likewise exclude operation metadata from submitted content where their consumer requires pure body.

## 8. Flow and failure examples

Refactor Design supplies both production_design and test_design; both render. Research references and related_docs both survive. An empty PR deferred list renders an explicit none declaration. Validation records a failed observed test without declaring QA NOGO/GO. Requirements remain plain requirements; only checked items produce checkboxes.

## 9. Migration and removal

Replace opaque nested strings, arbitrary record shapes, stale tracking envelope fields, copied workflow instructions and automatic lifecycle history. Keep old documents historical; do not resaffold existing artifacts automatically. Remove embedded example_context metadata when schema-root examples become the one discoverable example authority.

## 10. Evidence

For each of nineteen workflow/phase variants, populate named carriers and verify meaningful rendered sections, not copied prose. Minimal vs complete phase distinction; all constraints rendered; shared links complete; explicit checkbox state; language-labelled code examples; no source/related-doc shadowing; PR deferred statement; planning projection parity; tracking downstream content boundary.

## 11. Review points

Required nuclei versus workflow-required optional sections; Planning API parity; explicit PR deferred declaration; commit draft/message distinction. Native-source fragments in code examples remain literal documentation, not executed validation inputs.

## 12. Planning consequences

Document families and workflow semantic alignment are distinct deliverables with linked acceptance evidence. No implementation cycle names or delivery order here.

## 13. Traceability

DI-03 document/tracking obligations; DI-07 supplies nineteen semantic rows; F-06/F-12 shared primitives; I-12/13/15 phase boundaries; F-07 body/envelope separation.

## 14. Related documentation and history

Next: [W09 native settings](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/09-native-settings-migration.md); [W11 workflow](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/11-workflow-documentation.md) supplies the exact variant matrix.  
0.1, 2026-09-10: temporary proposal.
