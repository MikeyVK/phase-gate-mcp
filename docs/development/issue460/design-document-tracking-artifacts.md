<!-- docs/development/issue460/design-document-tracking-artifacts.md -->
<!-- template=design version=5827e841 created=2026-09-11T10:31Z updated= -->
# Document and Tracking Artifact Contracts

**Status:** DRAFT — W08 design submitted for independent review  
**Version:** 1.0  
**Last Updated:** 2026-09-11  
**Primary package:** DI-03 (document and tracking artifacts)  
**Dependencies:** DI-01/DI-02; approved Research; active workflow content obligations  
**Downstream:** DI-04/DI-05 validation; DI-06 distribution; DI-07 instructions; DI-08 assurance

## 1. Purpose and Authority

Complete W08 together with [W07](design-code-test-artifacts.md), under the human's 2026-09-11
delegation to use Research and existing behavior rather than request every field decision.
Independent QA assesses completeness; this draft is not producer approval.

[Research](research.md) owns approved behavior, [Findings](research-findings.md) its evidence,
[Catalog](template-suite-catalog.md) the path census, and [README](README.md) document form.
Temporary W08 proposals are superseded. In particular, their shortened capacity table was not
a complete preservation inventory and is not the implementation baseline.

Design fixes families, semantic fields, shared records, presence rules, rendering responsibilities,
migration and proof. Implementation writes exact JSON Schema declarations and Jinja bodies.
It may not drop an existing capability, introduce a required field or invent content merely because
a concise design table did not repeat a source template line.

## 2. Scope and Exclusions

Seven full documents: architecture, research, design, planning, validation_report, reference,
generic_doc. Three tracking artifacts: issue, pr, commit. All ten IDs remain unchanged.

Include full resolved inheritance/import behavior, shared links/checklists/issue identities,
workflow-neutral semantic carriers and operational planning identity.

Exclude new workflow engines, GitHub/Git operations, document ASTs, automatic evidence/status/history,
template-specific Python, semantic model-example validation and automatic diagram tool installation.
A truthful initial scaffold need not be a completed phase deliverable.

## 3. Binding Inputs

- F-01/F-02/F-03/F-05/F-07: fully described structured values, no coercion/default injection,
  every caller field rendered, no operation-envelope leakage.
- F-06/F-12: explicit Link(label,target), positive issue identity and explicit checklist state.
- F-07 tracking: body-only issue/PR, explicit PR deferred-none/populated outcome,
  conventional commit semantics and downstream ownership.
- Research's nineteen workflow/phase variants and general-document responsibilities.
- F-08/F-20: output profiles differ for full documents, body fragments and text; syntax/link
  evidence is separate from formatting and persistence policy.
- F-11/F-14/A/B: approved first-line provenance, removed lifecycle/hint/specialization debt.
- DI-01/DI-02 §7.2.1–§7.2.2: unchanged context and one authoritative resolved schema.

## 4. Owned Decisions

| ID | Decision | Reason |
|---|---|---|
| D-ART-DOC-01 | Ten retained families, separate document/tracking bases | Keep real consumer purposes, not one catch-all document |
| D-ART-DOC-02 | Named optional semantic sections; small required nucleus | Discovery must show capacity without demanding completed research at scaffold time |
| D-ART-DOC-03 | Finite shared records and one bounded subsection level only where evidenced | Introspectability without a recursive document DSL |
| D-ART-DOC-04 | Shared links with deterministic reference IDs and complete definitions | Repair dangling references and shadowed related-doc lists |
| D-ART-DOC-05 | Planning narrative shares operational identities, not a synchronization engine | Prevent two incompatible deliverable vocabularies |
| D-ART-DOC-06 | No invented status, evidence, checklist state, authors or version history | A scaffold is content, not proof or workflow authority |
| D-ART-DOC-07 | Preserve native document capabilities with explicit old-to-new dispositions | Short illustrative examples cannot establish completeness |
| D-ART-DOC-08 | Nineteen variant capacity checks remain DI-07/DI-08 evidence | Do not duplicate workflow instructions in schemas |
| D-ART-DOC-09 | Saved tracking provenance and downstream body/message are distinct surfaces | Do not redesign header or invent automatic publication/stripping |

## 5. Responsibilities and Boundaries

| Owner | Responsibility |
|---|---|
| Package schema | Discoverable fields, requiredness, closed records, conditional structure, descriptions |
| Shared definitions | Link, issue reference, checklist and reused document records |
| Jinja base/pattern | Framing, escaping, link definitions, sections, tables/lists, explicit optional rendering |
| Concrete template | Family-specific section order and meaning; no hidden context |
| Generic pgmcp | Standard schema validation, graph/render orchestration, existing checks/persistence |
| Workflow configuration | Phase obligations, tools by purpose, evidence and completion gates |
| Downstream Git/GitHub tools | External title, labels, assignees, branch/base, commit execution, publication |
| Planning/QA consumers | Review content and proof; a document status never grants authority |

No field named problem_statement, sources, work_units or deferred_work enters a generic server
dispatch table. Named prose is legitimate content; an unbounded full_document/body override for
every artifact would hide the contract and is not introduced.

## 6. Options and Rationale

Keep family-specific sections and shared tiered rendering. A single Markdown blob would evade
Research's discovery problem. A deeply nested document model would increase cognitive and
implementation cost. Finite named prose/list/record sections provide sufficient structure.

Do not preserve every accidental truthiness fallback or placeholder. Preserve useful content,
relationships and ordering; repair primitive/object mismatches and disclose empty sections honestly.
Do not tighten requiredness merely to make a scaffold look finished.

## 7. Detailed Design

### 7.1 Common rules and full-document framing

Notation: unmarked record members are required; ? means optional, not nullable.
Text is nonempty text; Prose permits ""; arrays permit [] unless explicitly constrained.
Closed records reject unknown fields. No null except where the existing operational planning
payload explicitly admits it (§7.5). No inferred headings, author, dates, status or link display labels.

Full documents require title:Text and emit one H1. All seven support optional caller-authored
status, version, last_updated, purpose, scope_in, scope_out, prerequisites:Text[], related_docs:Link[].
Generic Document additionally requires purpose and summary. Family additions are in §7.3.
The optional body status is caller-authored nonempty text, for example DRAFT or DRAFT — awaiting
review, not a revived lifecycle enum/engine. Version is an explicit document version; last_updated
an ISO date.
These values are authored content, not package pv, provenance timestamps or workflow transition inputs.

Presence behavior for every optional section:

- Absent: omit the section and its heading.
- Explicit "" or [] where admitted: emit the section heading/empty structural container, no invented
  "None", task, evidence or placeholder. An empty supplied purpose does not become a guessed summary.
- Populated: render supplied content in the declared order.
- False is meaningful checklist state; zero is not missing. Null is not absence.

Exceptions are explicit: PR deferred_work=[] means "No deferred work identified"; optional commit
scope cannot be empty because empty parentheses are not meaningful; body metadata values, identity
fields and link targets are nonempty if supplied. No semantic evidence is inferred from these rules.

The required nucleus is not a phase completion gate. Empty required arrays below are allowed unless
marked otherwise. Existing status/version/date availability is preserved but their former unconditional
requiredness is relaxed: optional authored content must not force invented lifecycle facts.

### 7.2 Shared semantic records

| Record | Fields and rendering consumer |
|---|---|
| Link | label:Text, target:Text; display label and explicit URI/path/fragment target |
| IssueReference | Positive integer, not "#123"; renderer supplies punctuation |
| ChecklistItem | text:Text, checked:boolean; renderer emits [x] or [ ] |
| Alternative | name:Text, description:Prose, pros?:Text[], cons?:Text[]; alternatives section |
| Decision | decision:Text, rationale:Prose, alternatives?:Text[]; decision narrative/table |
| Evidence | claim:Text, observation:Prose, sources:Link[], invocation?:Prose, observed_result?:Prose, observed_at?:ISO-date-time; evidence index |
| Risk | description:Text, mitigation:Prose, consequence?:Prose; risks section |
| Section | heading:Text, content?:Prose, bullets?:Text[], checklist?:ChecklistItem[]; flat custom section |
| FAQ | question:Text, answer:Prose |
| UsageExample | description:Text, language:Text, code:Prose |
| Consumer | name:Text, responsibility:Prose, impact:Prose |
| EvidenceRequirement | obligation:Text, method:Text, expected_result:Text, references?:Link[]; planned proof, not an observed result |
| ObligationEvidence | obligation:Text, evidence:Link[], outcome?:Prose |
| DeferredItem | description:Text, rationale:Prose, references?:Link[] |

A record's list may be empty without supplying imaginary evidence. A Section must supply at least
one of content/bullets/checklist; explicitly empty content is an honest structural basis.
These are content DTO shapes expressed by JSON Schema, not new Pydantic classes in pgmcp.
Definitions are extracted to shared/definitions only when actually reused. Artifact-local types
stay local. There is no artificial common superclass or mandatory nesting for all sections.

### 7.3 Complete family capacity and required nucleus

Each row includes common fields from §7.1 plus its listed fields. All additions not marked R are
optional. Textual narrative is Prose unless a nonempty Text/record is explicitly specified.

| Family | Required addition (R) | Additional named content and rendering destination |
|---|---|---|
| architecture | concepts:Concept[] (R) | constraints:Text[], decisions:Decision[], sources:Link[]; constraints render explicitly |
| research | problem_statement:Text (R), goals:Text[] (R) | background, findings, questions:Text[], references:Link[], approved_strategy, expected_results, evidence:Evidence[], consumers:Consumer[], risks:Risk[], assumptions:Text[] |
| design | problem_statement:Text (R), requirements_functional:Text[] (R), requirements_nonfunctional:Text[] (R) | constraints:Text[], options:Alternative[], decision, rationale, key_decisions:Decision[], questions:Text[], production_design, test_design, contracts:Section[], flow, state_and_failures, preservation, transition_and_cleanup, validation:EvidenceRequirement[], risks:Risk[], planning_consequences, sources:Link[] |
| planning | summary:Text (R), work_units:WorkUnit[] (R) | dependencies:Text[], risks:Risk[], milestones:Text[], phase_deliverables (§7.5) |
| validation_report | No addition to required title | issue_number:IssueReference, cycle:Text, validation_status:PASS/FAIL/PARTIAL, scope, obligations:ObligationEvidence[], evidence:Evidence[], demonstration, preservation, containment, failures:Text[], caveats:Text[], risks:Risk[], deferred_work:DeferredItem[] |
| reference | sources:Link[1..] (R), api_reference:ApiEntry[] (R) | test_evidence:Link[], usage_examples:UsageExample[] |
| generic_doc | purpose:Text (R), summary:Text (R) | key_changes:Text[], migration_steps:Text[], validation_checklist:ChecklistItem[], faq:FAQ[], sections:Section[] |

Required functional/nonfunctional lists, concepts, goals, work_units and API lists may be empty
for an initial scaffold. We do not preserve a hidden assumption that a schema-valid call contains
all final decisions. Design's formerly required decision/rationale/options/key_decisions become
optional authored sections: a decision may legitimately follow comparison, not precede it.

Research keeps external references distinct from related_docs and renders both. Naming questions
is the single V3 contract; questions_list/open_questions aliases are removed, not accepted in parallel.
Validation Report retains its issue/cycle/outcome semantics; none is populated from runtime context.
Its reported outcome is producer content, not an independent QA verdict or MCP success flag.

Named scope/exclusions, evidence/consumers/risks and narrative fields expose required workflow concepts
without copying workflow-specific names or instructions into the schema. No requirement to call a
tool with a hardcoded pseudo-invocation is embedded in any template.

### 7.4 Architecture and Reference records

| Record | Fields |
|---|---|
| Concept | name:Text, description:Prose, diagram?:Prose, subsections?:ConceptSection[] |
| ConceptSection | name:Text, description:Prose |
| ApiEntry | name:Text, description:Prose, methods?:ApiMethod[], sources?:Link[] |
| ApiMethod | signature:Text, parameters:Prose, returns:Prose, description?:Prose, errors?:Prose, sources?:Link[] |

Concepts retain ordered numbering and associated diagrams/subsections; subsections do not nest again.
Mermaid diagram text is rendered only when supplied, with no generic server parser. Constraints are
not discarded or conditional on decisions. Diagram presence may require a selected output check,
but dormant capability does not impose a startup dependency on every workspace (DI-05 ownership).

Reference preserves component/method grouping, native signatures, parameter/return descriptions,
errors and implementation links. Sources is a nonempty replacement for source_file; test_evidence
replaces the mandatory single test_file with optional repeatable evidence links. Remove test_count.
Usage examples always name their language; no Python fallback. No interpretation or execution of code.

### 7.5 Planning work units and operational parity

| Record | Fields |
|---|---|
| WorkUnit | id:Text, name:Text, goal:Text, deliverables:Deliverable[1..], exit_criteria:Text, scope_in?:Prose, scope_out?:Prose, owner?:Text, dependencies?:Text[], obligations?:Text[], verification?:EvidenceRequirement[], risks?:Risk[], stop_conditions?:Text[], cycle_number?:positive-integer |
| Deliverable | id:Text, description:Text, owner?:Text, validates?:ValidationSpec or null |
| ValidationSpec | Existing operational fields type, file, text, path with their current conditional requirements |
| phase_deliverables | Optional design, validation, documentation arrays of Deliverable |

Narrative work-unit IDs identify dependencies. Cycles, documentation tasks and epic child work use
the same bounded carrier; active workflow instructions decide which content is required at completion.
No universal TDD heading. Dependencies and input order are explicit; template does not topologically
sort or create a schedule. Unit owner supplies its ownership context; a deliverable owner expresses
a deliberate different owner, not a required duplicate.

[deliverables.py](../../../mcp_server/schemas/deliverables.py) remains the operational schema owner:
ValidationSpec uses file_exists/file_glob/contains_text/absent_text/key_path and its exact file/text/path
requirements. validates may be absent or explicitly null (no executable validation specification).
Within a supplied spec, non-applicable file/text/path may be omitted or null; file is non-null for
all five variants, text additionally for contains_text/absent_text, path for key_path. Values are
preserved, not filled. Do not invent a second validation expression language. The template exposes that shape
as declarative content; it does not execute it.

For work units explicitly mapped to operational cycles, cycle_number is caller-supplied sequential
one-based identity, not a number inferred from a heading. name, deliverable id/description/validates
and exit_criteria retain their exact meaning in save_planning_deliverables. Operational total equals
the mapped cycle count; narrative-only id/owner/scope/evidence is not sent as undeclared operational
fields. phase_deliverables preserves corresponding design/validation/documentation deliverable meaning.

This is a reviewed semantic projection, not an automatic parser/synchronizer or a new runtime tool.
The caller explicitly supplies the operational payload; independent tests must demonstrate matching
IDs/content/order and count. Changes to that operational shape require DI-07 coordination, not a
silently diverging planning template. A draft can have work_units=[] without pretending execution is planned.

### 7.6 Tracking contracts

Tracking does not inherit full-document purpose, H1 title, lifecycle or version-history sections.

| Family | Required content | Optional content |
|---|---|---|
| issue | problem:Text | summary, expected, actual, context, reproduction_steps:Text[], related_docs:Link[] |
| pr | changes:Prose, deferred_work:DeferredItem[] | summary, testing, checklist:ChecklistItem[], breaking_changes, related_docs:Link[], closes:IssueReference[] |
| commit | type:Text, subject:Text | scope:Text, body:Prose, breaking_change:boolean, breaking_description:Text, footer:Prose, refs:IssueReference[] |

Issue emits a body without an external H1 title. Reproduction steps retain order and numbering.
No title, labels, milestone, assignees, routing or hidden issue-creation options.

PR explicitly renders the deferred section every time. [] is an explicit none declaration; populated
entries describe possible follow-up, not issue-creation orders. Coordination owns triage/linkage.
No tracking_state, has_deferred flag or required tracking_issue. Changes preserves caller-authored Markdown paragraphs and may be "" for a draft;
there is no fabricated testing statement, default checklist or automatic check state.
testing is authored prose; evidence can be expressed as ordinary explicit links in that prose and
related_docs, not an ambiguous testing/evidence input alias.

Commit renders type[(scope)][!]: subject, optional body, BREAKING CHANGE footer when its description
is supplied, refs with # punctuation, and caller footer. Type is an explicit conventional type token,
not workflow-phase-derived; subject/scope/type reject embedded newlines/punctuation that breaks this
framing. Case is preserved. breaking_description requires breaking_change=true; true without a
description remains valid marker-only intent. No automatic wrapping, phase prefix, casing or guessed refs.
Free body/footer content remains multiline.

The saved artifact uses the approved DI-02 first-line provenance and the appropriate text/Markdown
wrapper. That line is not the conventional commit subject or the downstream GitHub body contract.
There is no promise that blindly submitting the complete saved file is a valid downstream operation.
Caller uses its authored message/body with the downstream tool's explicit inputs; issue460 introduces
no automatic publication, header-stripping route or new Git consumer. DI-05 profile design must
distinguish saved-artifact framing from its tracking content without changing the header contract.

### 7.7 Shared Markdown rendering and links

Reuse document and tracking branches separately:

- shared/templates/bases/tier0_root.jinja2
- tier1_document.jinja2 → tier2_markdown_document.jinja2 for full documents
- tier1_tracking.jinja2 → tier2_markdown_tracking.jinja2 or tier2_text_tracking.jinja2
- shared/templates/patterns/markdown/ for genuinely shared links, lists, sections and escaping
- shared/definitions/link.schema.json, issue-reference.schema.json, checklist-item.schema.json
  and actually reused document records

Each concrete package composes its own schema and template; no cross-package inheritance.
No per-template patterns directory or technology-driven replacement tree.

Links always supply nonempty label and target; do not accept Markdown link strings as structured
Link values or infer label from target. Both inline and reference-style renderers remain first-class:
generic/research/architecture/design/planning/validation related-links lists use inline form;
reference sources/test_evidence and tracking related_docs use reference form to preserve those uses.
A future package can select either shared renderer without generic server changes.

Reference IDs are generated by suite-owned rendering from fixed field namespace plus one-based
structural occurrence indexes, e.g. src-1, test-1, api-2-method-1-src-1, related-1. Namespaces are unique
within the concrete root. Every use emits its matching definition exactly once in that section.
No cross-section deduplication or global link registry is needed; identical targets may have distinct
IDs. This avoids deduplication state and collisions while keeping every use resolvable.

Escape labels/targets for their Markdown positions, including brackets, backslashes, spaces and
table delimiters. Never absolutize targets, infer title slugs, rewrite self-fragments or resolve files
during rendering. A caller-supplied #section or own-file.md#section remains exactly that target.
Reference completeness is a renderer obligation; existence/anchor correctness is a separate check.

Tables escape pipes and render embedded prose newlines without breaking rows. Code/diagram fences
use a delimiter longer than any conflicting delimiter in the supplied content; language info is a
single line. Inline code/signatures similarly use a safe delimiter. Prose fields remain authored
Markdown rather than HTML-escaped plain text. List indentation preserves multiline items.
These helpers belong to shared Jinja, not a new pgmcp Markdown formatter/parser.

### 7.8 Workflow carrier coverage (nineteen variants)

Use the named fields below with active instructions; do not make each workflow its own template.

| Variant | Discoverable content carriers |
|---|---|
| Feature Research | evidence, consumers, risks, findings, approved_strategy, expected_results |
| Bug Research | problem_statement, background, evidence, findings, expected_results, approved_strategy |
| Refactor Research | consumers, findings, evidence, scope_out, approved_strategy, expected_results |
| Chore Research | problem_statement, scope_in/out, consumers, risks, approved_strategy; persistence stays conditional |
| Epic Research | consumers, findings, assumptions, risks, evidence, approved_strategy, expected_results |
| Feature Design | production_design, contracts, flow, state_and_failures, options, test_design, transition_and_cleanup, planning_consequences |
| Bug Design | problem_statement, production_design, preservation, state_and_failures, test_design, validation |
| Refactor Design | production_design, contracts, preservation, transition_and_cleanup, test_design, validation |
| Epic Design | production_design, contracts, flow, state_and_failures, transition_and_cleanup, test_design, planning_consequences |
| Feature Planning | work_units deliverables/dependencies/verification/exit_criteria |
| Bug Planning | work_units goal/scope/obligations/verification/exit_criteria |
| Refactor Planning | work_units dependencies/obligations/deliverables/stop_conditions |
| Docs Planning | work_units scope/owner/deliverables/verification/risks |
| Epic Planning | work_units owner/dependencies/obligations/deliverables/exit_criteria/stop_conditions |
| Feature Validation | obligations, evidence, demonstration, failures, caveats, risks, deferred_work |
| Bug Validation | scope, obligations, evidence, preservation, failures |
| Refactor Validation | obligations, evidence, preservation, failures, caveats |
| Hotfix Validation | scope, evidence, preservation, containment, caveats, risks |
| Chore Validation | scope, obligations, evidence, risks, deferred_work |

Design.validation and WorkUnit.verification describe planned method and expected result, never
fabricated observations. Validation obligations/evidence record observed proof; targeted regression
proof is an explicit obligation-to-evidence entry. containment describes containment/rollback evidence.
Named narrative sections may express root cause or child dependencies within their
documented role; no catch-all override is needed. Exact variant emphasis remains in contracts.yaml.
Schema descriptions identify the current work-context phase instructions as the authority for phase
completion, without copying tool parameter syntax, phase order or mandatory TDD language.

## 8. Control, Data, and State Flow

Schema discovery → explicit content → standard context validation → unchanged content plus
provenance → selected tier graph → profile-appropriate checks → enforce/report persistence.
Later reasoning/evidence gathering and safe_edit refine the document. No document status triggers a
phase transition, QA approval or external publication. No link target is converted into write authority.

## 9. Compatibility, Migration, and Removal

| Existing capability or defect | Target disposition |
|---|---|
| Common title/purpose/scope/prerequisites/related docs | Preserve available content across full documents; optionality explicit (§7.1) |
| Architecture concept diagrams/subsections/numbering and decisions | Preserve relationships; replace string items with records; render ignored constraints |
| Research background/findings/goals/strategy/results and two reference lists | Preserve all; remove list shadowing and question aliases |
| Design distinct functional/nonfunctional requirements, alternatives, key decisions | Preserve distinctions; remove fake task state and ten-option lettering limit; use numbered alternatives |
| Planning cycles goal/tests/success criteria/dependencies, overall risks/milestones | cycles→work_units, tests→verification, success_criteria→exit_criteria; preserve intent, no scalar/list dual read |
| Validation issue_number/cycle/validation_status/scope | Preserve explicit content; remove invented scope fallback; add evidence-index sections |
| Reference source_file/test_file/API methods/usage examples | sources/test_evidence/structured API and language-aware examples; remove test_count |
| Generic custom_sections with content, bullets and checklists; FAQ | custom_sections→sections; preserve all three capacities and checked state; no recursive sections or scalar-to-list repair |
| Commit message/body/breaking/footer/refs | message→subject, positive IDs; preserve marker-only breaking intent and native multiline content |
| Issue steps_to_reproduce; PR checklist_items/closes_issues | reproduction_steps/checklist/closes respectively, with declared sequence/record/positive-ID shapes; no aliases |
| Issue/PR body title and envelope metadata | Remove; downstream tool owns external envelope |
| PR deferred_work/tracking_state | Explicit structured none/populated; remove inert tracking_state and fabricated defaults |
| Auto Agent/Initial draft history, timestamps/path headers, agent hints | Apply approved removal/header replacement; no second history mechanism |
| Inherited code_section block that is never rendered | Do not advertise as working generic code_blocks; concrete UsageExample/diagram carriers own real behavior |

Clean break means no simultaneous old/new names or primitive/object alternatives. Existing documents
remain ordinary files; do not mass-rewrite their provenance or contents to justify new schemas.
All changes map to the authoritative catalog; no change to its 126/151 consumer/test census.

## 10. Test and Validation Design

| Evidence ID | Required observable proof |
|---|---|
| DOC-E01 | All ten real package roots, minimal required contexts, each optional capability; unknown/legacy fields rejected |
| DOC-E02 | Common omitted vs explicit empty vs populated sections; caller metadata preserved; no synthetic history or lifecycle |
| DOC-E03 | Architecture constraints, numbered concepts, associated diagrams/subsections; >10 Design options; distinct requirement groups |
| DOC-E04 | Research references and related_docs together; all reference source/test/API links get definitions; self-fragments unchanged |
| DOC-E05 | Label/target metacharacters, spaces, table pipes/newlines, nested source namespaces, fences inside code; no generic formatting parser |
| DOC-E06 | Planning operational projection: IDs, cycle order/count, exit criteria, validates variants and phase deliverables; narrative extras not forwarded |
| DOC-E07 | Validation identity/outcome/evidence fields, absent/unobtained evidence, no producer-to-QA authority conversion |
| DOC-E08 | Generic FAQ, custom content/bullets/checked and unchecked lists, ordered migration steps; native non-Python reference example |
| DOC-E09 | Issue/PR no external H1/envelope leakage; PR explicit none/populated; conventional commit marker/body/footer/positive refs |
| DOC-E10 | All nineteen workflow variants have discoverable named capacity and instruction-side alignment; no final-evidence requirement on initial scaffold |
| DOC-E11 | Full-doc versus tracking/text profile applicability, metadata reader/writer seam, enforce/report and unavailable-check honesty |

Existing seams include [document tests](../../../tests/mcp_server/integration/test_document_templates.py),
[tracking tests](../../../tests/mcp_server/scaffolding/test_tracking_templates.py),
[generic doc tests](../../../tests/mcp_server/unit/templates/test_generic_doc_template.py),
[issue H1 invariant](../../../tests/mcp_server/unit/tools/test_issue_template_h1.py).
Use their meaningful behavior, not complete prose snapshots or permissive checks that ignore missing
reference definitions. A test of an imported macro alone does not prove the selected root invokes it.

Implementation proof must cover all optional fields/record branches without requiring a permanent
production example catalog. Runtime-generated examples are not semantic model-example validation.
No runtime tests were executed for this documentation-only design work.

## 11. Integration Risks and Open Questions

No additional family product choice awaits a human field workshop. External QA must assess the
source-to-design preservation mappings, initial-scaffold requiredness and nineteen-variant coverage.

Pending integration work: DI-05/W09 binds exact profiles/checks (including saved tracking framing);
DI-07 aligns instructions and operational planning references; DI-08 realizes independent evidence.
No claim of fully integrated Design precedes those checks. If an existing operational planning
constraint cannot be represented without contradicting DI-01, resolve that shared boundary explicitly,
not with a template-specific server repair.

## 12. Planning Consequences

Bound shared-link/schema changes separately from family migrations. Every affected consumer needs
explicit cycle ownership and its relevant DOC-E evidence. Pair schema and renderer changes within
each bounded write-set, preserve unrelated documents, and name rollback/stop-go evidence. Do not
create one "remaining documents/tests" cycle. Initial scaffold, refined phase deliverable and saved
operational plan are distinct verification surfaces.

## 13. Traceability Matrix

| Research/source | Design | Proof |
|---|---|---|
| F-01/02/03/05/07 | §7.1–§7.6, field dispositions | DOC-E01/02 |
| F-06/F-12 | §7.2/7.6/7.7 | DOC-E04/05/08/09 |
| General-document responsibilities | §7.3/7.4, §9 | DOC-E03/04/08 |
| Workflow × phase comparison (5+4+5+5) | §7.3/7.5/7.8 | DOC-E06/07/10 |
| Existing CyclePlanningModel/ValidatesModel | §7.5 | DOC-E06 |
| Tracking responsibility F-07 | §7.6 | DOC-E09/11 |
| F-08/F-20 profile boundary | §7.4/7.6, §8 | DOC-E11 |
| F-11/F-14/A/B and catalog | §7.7, §9 | DOC-E02/11 |

## 14. Related Documentation and Version History

- [Code/test companion](design-code-test-artifacts.md), [Suite resolution](design-suite-resolution.md),
  [Execution adapters](design-execution-adapters.md), [Mutation validation](design-mutation-validation.md)
- [Research findings](research-findings.md), [Catalog](template-suite-catalog.md),
  [Design intake](design-intake-map.md), [Deferred work](deferred-work.md)
- [Current document base](../../../.pgmcp/templates/tier1_base_document.jinja2),
  [Markdown base](../../../.pgmcp/templates/tier2_base_markdown.jinja2),
  [Tracking base](../../../.pgmcp/templates/tier1_base_tracking.jinja2),
  [Workflow contracts](../../../.pgmcp/config/contracts.yaml)

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-09-11 | Consolidate delegated W08 with preservation dispositions, finite records, nineteen-variant coverage and proof obligations. |
