<!-- pgmcp:v1 id=design pv=1.0.0 pf=WCiT2npbapCBexKy sf=9PfER5JkyAoFQLRi -->

# Issue 473 — First-call Template Quality Design

**Status:** DESIGN — independent review requested
**Version:** 0.2
**Last Updated:** 2026-10-03

## Purpose and authority

Define the correction architecture for the human-approved first-call objectives in [Research's Approved Strategy](research.md#approved-strategy). Research revision 0.23 is binding input. Independent Research QA returned GO for Research → Design against commit `36e40db4dbe9d5248b51feec2c51014ffa878897`; the human approved Design on 2026-10-03. This document proposes the concrete contracts and assigns verification obligations. It does not assert that the implementation already meets them.

The deliverable is a useful, valid starting point for subsequent editing. It does not promise a complete application, runnable application dependencies, arbitrary caller-code quality, or generic proof that every admitted field is consumed. The agreed clean break applies separately to changed context fields, full-document metadata, generated presentation and affected known consumers. Issue #476 remains separate.

The human explicitly rejected additional automated content/regression tests. The configured Design instruction to identify regression coverage is satisfied here by identifying existing coverage that must remain valuable and by specifying actual scaffolding, manual agent inspection and supporting native evidence. No new snapshot, content-assertion or workflow-only test suite is proposed.

## Scope and constraints

In scope are the 19 shipped concrete packages, their shared layout/schema dependencies, narrowly necessary generic text-boundary support, affected active examples/instructions and existing test inputs/expectations, and relevant coding/documentation standards. Runtime changes are limited to enabling the approved rendering and input contracts through existing seams.

Out of scope are historical document mass migration, generic AST-based schema consumption analysis, unknown external caller migration, additional runtime lint/format/presentation gates, new execution dependencies, broad tool repair, package/distribution redesign, multiclass scaffolds and implementation cycle ordering. Unrelated practical tool findings are documented for later triage.

The existing [architecture contract](../../coding_standards/ARCHITECTURE_PRINCIPLES.md) remains binding: injected collaborators, artifact-agnostic services, immutable admitted catalog descriptions, configuration-owned policy, separation of commands and queries, and shared ownership of common template structure. The [Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md) assigns mechanisms and failure contracts to Design; Planning will choose execution boundaries and evidence collection steps.

## Requirements and ownership

| Surface | Objective | Owner |
| --- | --- | --- |
| Generated layout | Remove generated blank residue; preserve meaningful caller interiors | Shared bases/macros and explicit fragment joins |
| Full-document framing | Mandatory visible status, version, date and populated version history | One shared schema and Markdown document base |
| Python class documentation | Distinct required module and class descriptions, without fallback | Six concrete schemas and Python inheritance contracts |
| TypeScript documentation | Required class description; independently optional module description | TypeScript package schema/template |
| Python native quality | Generated structure meets configured Ruff baseline when admitted caller fragments meet it | Template expressions/import/layout composition |
| Python model descriptions | Preserve field descriptions without automatic duplicated class Fields summary | Pydantic DTO package and shared model macros |
| Architecture/Generic Doc | Meaningful hierarchy and direct custom sections | Concrete document templates and common section rendering |
| Tracking artifacts | Preserve their distinct body/envelope responsibilities; normalize generated joins/EOF | Tracking bases and concrete packages |
| Input transition | Adopt new contracts with no aliases or compatibility mode | Known active callers/examples/fixtures |
| Verification | Preserve first outputs; inspect actual artifacts and meaningful boundaries | Implementation executor, supported by existing native tools |
| Current tool assessment | Reproducible correctness/usability findings from real use | Execution evidence and follow-up findings |

## Selected architecture and alternatives

Correct the shared tiered templates first and add one pure generic text-boundary filter to the existing template-engine layer. Concrete templates retain domain field selection. Shared bases own artifact framing; macros own repeated language structure. The catalog, schema admission, provenance, persistence and preflight pipeline retain their responsibilities.

| Alternative | Benefit | Cost or boundary conflict | Disposition |
| --- | --- | --- | --- |
| Global Jinja trimming/lstrip environment change | Small configuration change | Alters every seam, including caller-sensitive contexts; does not express language spacing or metadata ownership | Rejected |
| Whole-output Ruff or whitespace formatter inside scaffold execution | Easily produces some formatted examples | Rewrites caller internals, adds execution dependencies/gates and obscures raw first output | Rejected |
| Recursively trim every context string | Uniform input processing | Changes literal/data values and optional presence semantics; cannot distinguish prose from data | Rejected |
| Repeat framing/normalization in 19 packages | Local fixes are straightforward | Reintroduces DRY violations and inconsistent contracts | Rejected |
| Artifact-specific Python renderer dispatch | Central control | Couples generic rendering to package identities and context field names | Rejected |
| Shared schema/bases/macros plus one generic boundary filter | Clear ownership; preserves caller interiors; uses existing template-engine support | Requires deliberate composition at language seams and consistent environment setup | Selected |

The rendering environment remains constructor-injected. Its current whitespace options are not globally changed. Production and test environments currently differ in strictness/trailing-newline settings; shared artifact framing must work through both without changing unrelated generic engine consumers.

## Generic text and composition contract

The only new Python filter is `text_block(value: str) -> str`, owned by the existing template-engine layer. It performs the boundary-only text operation below. Fragment selection, joining separators and artifact EOF remain in shared Jinja bases/macros. There is no separate `join_blocks` or `artifact_eof` Python filter, new registry/manager, environment factory, validator policy or post-render pipeline.

### Shared environment capabilities before admission and rendering

The existing `TemplateEngine` registers generic name filters in its constructor. That registration currently happens after catalog admission. Bootstrap instead gives the catalog graph/input validators a separate bare Jinja environment. `TemplateInputValidator` calls `meta.find_undeclared_variables`, which uses the compiler and can reject unknown filters. Registering `text_block` only in the later renderer is therefore insufficient.

One shared registration routine in the existing `template_engine.py` module owns the callable definitions/registration for existing generic filters and `text_block`. Its interface is `register_template_filters(environment: Environment) -> None`. This is an explicit setup operation on the supplied environment, not a new object or abstraction layer. It performs no filesystem/configuration reads, template rendering, package discovery or import-time setup. Exact private helper decomposition remains an implementation choice.

The existing composition root calls that routine on the admission environment before any graph/input analysis, and on the runtime environment before template compilation/rendering. The `TemplateEngine` constructor delegates its current registration to the same routine, preserving support for existing direct engine consumers. Registration uses the same names and real callable implementations on both environments; a repeated call does not create a second vocabulary or change native environment options.

The two environments remain distinct: admission owns source analysis, runtime loads the admitted immutable source snapshot. Their loaders, strictness and trailing-newline options retain their existing responsibilities. No temporary render engine is created merely to configure admission. The validators continue receiving their existing parser dependency and gain no artifact knowledge, filter-specific branch, fake callable, unknown-filter suppression or bypass.

The delivered-template fixture and installed-distribution admission probe use the same shared registration before their catalog validation. Synthetic consumers that only parse a graph are distinguished from consumers that also run compiler-backed input validation; every relevant analysis/render environment must expose the same custom filter definitions through the existing engine setup. The changed root must consequently remain admissible through real source-suite and installed-suite routes.

This is the proposed correction to the independent P2 design finding, submitted for targeted re-review. QA's NOGO on revision 0.1/commit `1ae94137` identified missing admission availability, not a need for a new layer. On 2026-10-03 the human approved minimizing the mechanism: one bounded text function in the existing layer and composition/EOF in tiered templates. Research's behavior and clean-break choices remain unchanged.

### Text block edges

A boundary blank line contains only spaces and tabs, or has no characters before its line ending. `text_block` removes consecutive such lines at the beginning and end of a supplied text block. It retains the complete meaningful interior: internal blank lines, internal CRLF/LF spelling, Markdown hard-break spaces, indentation, fenced content, quoted strings and significant leading/trailing spaces on nonblank lines. A block consisting only of boundary blank lines becomes an empty string.

The final line terminator of the last retained line is treated as an insertion boundary, so the joining template owns the separator following that line. Other retained line endings remain unchanged. This is line-boundary normalization, not whole-string `.strip()`, line-by-line right trimming, recursive JSON rewriting or internal whitespace collapse.

Apply it only where the selected input role is a text block: prose, method/constructor/test bodies and supplied code-fence content, before language indentation or escaping. Do not apply it to literal data, default/example string values, enumeration members, identifiers, type annotations, link targets or similar scalar facts. Documentation text may normalize its boundary lines before quoting without changing its meaningful content.

Normalization does not redefine presence. A supplied empty or whitespace-only optional field still follows the existing defined-versus-absent rendering/validation contract. For example, a defined empty module description may intentionally produce an empty documentation literal. A template must not silently turn that into absence by testing only truthiness.

### Fragment joins and indentation

Shared Jinja bases/macros normalize already selected rendered fragments with `text_block`, omit fragments with no rendered structure/content, and use existing Jinja selection/join capabilities or explicit macro composition with the template's chosen separator. A heading, empty literal or deliberately generated empty comment is a real fragment even when its input prose is empty.

Separators are language-owned. Markdown independent generated blocks receive one empty line; Python methods receive the configured native spacing inside the class, and top-level declarations receive Python top-level spacing. Decorators stay attached to the declaration they decorate. TypeScript constructor assignment statements remain consecutive, with one empty line before a logically distinct optional block.

A text/body macro must decide whether there is anything to indent before applying indentation. Indenting an empty fragment must not generate a spaces-only line. Blank lines authored inside a nonempty caller body remain caller-owned, including an internal spaces-only line; the objective applies to generated residue, not a hidden repair of caller interiors.

### Artifact EOF and provenance

All 19 concrete packages inherit the shared artifact root. That root captures the assembled artifact once, starting with the existing provenance line, applies the same `text_block` boundary operation and appends exactly one explicit LF as rendered content. This removes trailing blank-line residue and the retained last line's boundary terminator before appending LF; it preserves significant spaces on nonblank lines and every internal line ending. Because the assembled fragment begins with the provenance line, leading caller content is not an artifact-edge trimming target. No separate EOF algorithm/filter is introduced.

The existing first physical provenance line remains intact and first. Shared framing must not render blocks twice or add template-source whitespace after the explicitly appended LF. EOF is determined by the root's rendered content, independent of whether an environment retains the template file's final newline. The boundary filter is invoked by the root, rather than automatically post-processing every `TemplateEngine.render`/`render_context` result. Generic engine consumers that render strings such as `False|0` therefore retain their existing output contract. Arbitrary non-artifact templates do not acquire an implicit newline.

## Full-document metadata contract

Apply the following shared root property to exactly these seven packages: `architecture`, `research`, `design`, `planning`, `validation_report`, `reference` and `generic_doc`.

```json
{
  "document_metadata": {
    "status": "DESIGN — review requested",
    "revisions": [
      {
        "version": "0.1",
        "date": "2026-10-03",
        "author": "Example author",
        "change": "Initial design."
      }
    ]
  }
}
```

This is a contract illustration, not default content. All displayed facts must come from the caller. The shared definition resides in a cohesive `shared/definitions/document-metadata.schema.json`; each of the seven root schemas references it. The object and revision objects are closed. Required fields are `status` and `revisions`, and each revision requires `version`, `date`, `author` and `change`. The array has at least one item. String facts are nonempty under the existing schema conventions; dates use the existing ISO date spelling constraint. This does not introduce semantic version sorting, calendar-date certification or a new status enumeration.

The array is an explicitly supplied revision sequence. Its last item is the current revision. Header `Version` and `Last Updated` derive from that same item, so they cannot disagree with the final history row through independently supplied duplicate facts. `Status` comes from the explicitly supplied status. Preserve revision order; do not infer chronology or sort values.

The former root `status`, `version` and `last_updated` fields are removed from these seven context schemas. They are not aliases. Old contexts fail existing schema validation and must adopt `document_metadata`. No default author, date, revision or workflow status is inferred from the machine, Git or active issue.

The shared Markdown document base emits visible Status, Version and Last Updated immediately after the title, and a `Version History` section at the end, after related-document links when present. The table has Version, Date, Author and Changes columns and at least one supplied row. Shared escaping protects table delimiters without replacing the caller's underlying fact. Metadata and version-history rendering are implemented once through the shared tier; concrete document packages do not duplicate it.

Issue and PR are tracking bodies, and Commit is text tracking content. They do not acquire full-document metadata/history. Python/TypeScript packages also do not acquire this contract. Provenance remains independent technical identification and does not substitute for visible document metadata.

## Python and TypeScript description contracts

| Packages | Class documentation | Module documentation | Migration |
| --- | --- | --- | --- |
| Python Class, Protocol, Pydantic Config, Pydantic DTO, Adapter, Worker | Required root `class_description` replaces root `description` | `module_description` becomes required | Clean break, no fallback |
| TypeScript DTO | Required root `class_description` replaces root `description` | `module_description` remains optional | Clean break, no fallback |
| Pytest Unit and Integration | Existing description contract retained | Explicitly retain their existing module-description source | No class-field rename |

Preserve existing value constraints for the renamed class description and the existing module-description prose value. Making the Python module field required changes presence, not its previously admitted empty value. Nested method/field descriptions are distinct contracts and remain named `description`.

Each selected class package explicitly supplies its own module and class documentation. Identical explicit values are allowed and are not deduplicated. A missing module field must not fall back to the class field. TypeScript renders a module comment only when the optional field is defined, including its admitted empty case.

The Python shared base establishes an explicit module-documentation block contract instead of a hidden default reading a generic root `description`. The two Pytest packages explicitly satisfy that block using their retained input contract. This prevents the six-class rename from incidentally breaking test scaffolding or reintroducing ambiguous ownership.

Six Python class packages still produce one main class per scaffold. The DTO no longer automatically repeats field descriptions in a class-level Fields summary; field descriptions remain attached to fields, while independently authored class prose is preserved. Worker does not regain automatic `__all__`; named imports remain available and the approved legacy wildcard difference remains accepted.

## Python generated structure

Use the configured Ruff baseline as the objective for generated Python layout; the current Research evidence used Ruff 0.15.6, target Python 3.11 and line length 100. Obtain current configured versions during execution rather than treating these observations as permanent deployment assumptions.

The shared Python base and import macro jointly own module-documentation/import/declaration spacing. Existing import-record values, aliases, group meanings and future-import placement remain intact. Correct composition boundaries before attributing every I001 finding to sorting: Research demonstrated findings caused by blank framing even in a single fixed import. Do not introduce a speculative replacement for native import sorting when the evidenced seam correction is sufficient.

Pydantic macros render composed `ConfigDict` and `Field` calls in multiline form with trailing commas. Structured example/default collections may use multiline generated layout while preserving element order and literal values. The template must avoid creating overlong composed lines when the constituent admitted values can be laid out within the baseline. It does not split or rewrite indivisible caller strings, annotations, raw expressions, default factories or method bodies to promise arbitrary E501 compliance.

Methods, constructors, decorators, fields, optional sections and top-level tests are composed as explicit fragments. Absent optional blocks contribute no generated blank residue. A class or constructor that is intentionally empty retains its valid language placeholder. Preserve the existing logging, mutability and example semantics; the layout change is not permission to revive legacy behavior.

A clean caller fragment may cease to be clean when composed incorrectly; that remains a template defect. A caller-authored internal style finding remains caller content unless the template altered its semantics or misplaced indentation. Record that distinction in evidence rather than erasing it with post-render formatting.

## Markdown presentation and TypeScript constructor layout

### Architecture and Generic Doc

Architecture retains distinct Concepts and Constraints sections. Subsections follow their parent numbering, such as 1.1, and meaningful names become headings directly. Suppress labels such as Diagram and Subsections when they are merely rendering mechanics; do not suppress an explicitly meaningful authored heading.

Concise decisions render as a comparison table. The table path is suitable for single-line plain text fields. Structured or multiline explanations, including lists, headings and fences, retain a full section presentation instead of being flattened into table cells. The fallback preserves content rather than imposing a new arbitrary length limit or compatibility mode. Escaping table characters must not cause loss of explanation.

Generic Doc renders supplied custom sections directly as H2 sections in caller order, without a redundant Sections wrapper. Avoid mechanical Content, Bullets and Checklist subheadings when they merely label input containers. Preserve actual groups, list order, checklist state, links and fenced content. Keep optional absent-versus-empty semantics and the shared one-empty-line generated block joins.

### Other document and tracking families

Research, Design, Planning, Validation Report and Reference retain their substantive current section contracts except the approved shared framing and generated layout. Issue and PR retain body/envelope separation and meaningful content. Commit retains text syntax and existing publishing semantics. All share the artifact EOF objective.

### TypeScript

Use explicit constructor fragments to avoid generated empty lines between ordinary field assignments. A distinct optional block receives one separator; braces have no generated blank line at their inner edges. The existing empty-field constructor remains valid and is not removed. Documentation source ownership follows the table above. No new TypeScript formatter or style standard is introduced by this issue.

## Admission, execution and failure contracts

Startup configures the admission environment with the shared real filter definitions before graph/input analysis and catalog admission, then constructs the runtime environment over the admitted snapshot with the same definitions. The existing per-call flow remains: caller requests a registered artifact ID; schema discovery exposes the prepared context schema; the existing catalog validates the context; the renderer augments it with owned provenance; injected engine/templates render; existing selected preflight runs; existing persistence and edit policy applies.

The schema admission boundary resolves the new shared metadata reference through the existing contained-reference mechanism. Prepared schema/catalog descriptions remain immutable. The boundary filter does not own package loading, ID dispatch, context migration, preflight policy or persistence.

| Condition | Behavior and responsibility |
| --- | --- |
| Missing mandatory metadata, class description or Python module description | Existing context-validation rejection; no fallback/default or partial success |
| Removed legacy root fields supplied | Existing closed-schema rejection; caller must adopt the new contract |
| Invalid revision shape/empty revision list | Existing schema rejection before rendering |
| Optional field absent or explicitly empty | Retain the selected contract's distinction; normalization does not revalidate or infer intent |
| Caller literal/data containing whitespace | Preserve its value; no generic trimming |
| Caller block with boundary blank lines | Normalize its boundary at the selected insertion role; no new padding error |
| Native check identifies generated defect | Preserve pristine output and causally classify; correct the template within approved scope |
| Native check identifies caller-authored finding | Preserve/report it; do not silently repair caller content |
| Unknown filter or shared reference cannot be admitted | Retain existing admission failure; no dummy filter, suppression or alternate legacy path. Shipped filters are explicitly registered before analysis. |
| Post-change server/catalog is stale | Refresh through the supported restart boundary and record active versions/fingerprints before interpreting evidence |
| Existing preflight or write fails | Retain existing result/error/evidence semantics; this issue adds no alternate failure family |
| Unrelated current-tool defect/friction | Record reproducible finding and disposition; do not silently expand repairs |

There is no global context migration, persistent state migration or new cleanup lifecycle. Schema/package identity and provenance protocols stay unchanged. Source graph/schema changes flow through existing admission/fingerprinting and server refresh; this issue does not introduce a separate distribution mechanism or automatic package version bump policy.

## Known consumers and standards reconciliation

The implementation inventory is defined by actual consumed contracts, not a repository-wide replacement of words such as `description` or `last_updated`.

| Consumer group | Required bounded treatment |
| --- | --- |
| Seven full-document package schemas/templates | Adopt shared required metadata and shared framing |
| Six Python class schemas/templates; TypeScript DTO | Adopt explicit class/module fields with agreed requiredness |
| Two Pytest roots and shared Python consumers | Explicitly retain module-description source under the changed base contract |
| Existing concrete template integration fixtures/tests | Update inputs and assertions that conflict with changed public fields/framing; preserve useful semantics/native evidence |
| Shared document/Python synthetic consumers | Supply newly required base contracts; remove expectations that explicitly prohibit mandatory framing |
| Generic engine/catalog consumers | Preserve their artifact-independent contracts, including no implicit root newline for arbitrary templates |
| Tool scaffolding reference example | Replace old full-document root metadata with the new shape |
| Create-issue workflow and mirrored prompt | Use exact `file_name` and admitted body context; keep title/labels in publishing envelope; exclude recognized saved provenance from published authored body |
| Relevant coding/documentation standards | State approved ownership/objectives; reconcile evidenced stale paths, framing and concrete affected links |
| Historical Research/issue460 evidence | Retain original facts, inputs and first outputs; do not rewrite them to look compliant |
| Unknown external callers | Adopt the new contract; no automatic conversion/alias or compatibility mode |

Concrete consumer inventory under `tests/mcp_server/integration/templates/`:

- Metadata migration: `test_architecture.py`, `test_research_artifact.py`, `test_design_artifact.py`, `test_planning_artifact.py`, `test_validation_artifact.py`, `test_reference.py` and `test_generic_document.py`.
- Class/module migration: `test_python_class.py`, `test_python_protocol.py`, `test_python_pydantic_config.py`, `test_python_pydantic_dto.py`, `test_python_adapter.py`, `test_python_worker.py` and `test_typescript_artifact.py`.
- Shared inheritance contracts: `test_shared_documents.py` and `test_shared_python.py`; the retained Pytest module contract is exercised by `test_pytest_unit_test.py` and `test_pytest_integration_test.py`.
- Tracking joins/EOF: `test_issue.py`, `test_pr.py` and `test_commit_artifact.py`. Adapt only existing assertions invalidated by the approved layout; do not add a new content suite.

For each listed concrete package, its colocated `context.schema.json` and `template.jinja2` are the public source entry points. The shared file surface is `tier0_root`, `tier1_code`, `tier1_document`, `tier1_tracking` and their affected Python/Markdown/TypeScript/text tier-2 bases, plus existing Python import/signature/model, pytest and Markdown section macros. The new metadata definition is shared. Do not move language/domain fields into `TemplateEngine`.

Catalog/unit/public-tool tests are reviewed for actual coupling to these inputs and root output. They are not declared migration targets merely because they mention templates. The delivered-template fixture and installed-distribution fixture's admission probe retain their admitted-suite setup while registering the same real filters before input analysis; update directly affected fixture contexts. Parser/render setup in shared synthetic consumers is reviewed against the shared capability contract. Concrete affected active links are discovered from heading changes and corrected at their actual consumers, not by migrating historical artifacts wholesale.

The actual Create Issue tool already separates an authored body from a saved artifact/provenance. Correct the evidenced active caller instructions, not the tool's envelope semantics. Do not create a new publication tool or perform a live issue mutation merely to probe it.

[CODE_STYLE.md](../../coding_standards/CODE_STYLE.md) and [DOCUMENTATION_STANDARD.md](../../coding_standards/DOCUMENTATION_STANDARD.md) must describe the same responsibilities as the engine/templates. Reconcile only related requirements and evidenced stale information, including the architecture document's legacy template-source paths and affected relative links. Do not fabricate historical dates/authors while correcting a standard's current header/history. Add an explicitly authored current revision where appropriate and preserve known historical facts.

The current generic usage guide already states that scaffolds are starting points; retain that boundary. Unrelated resource metadata named `last_updated`, administrative instructions and historical quality configurations are not consumers of the changed document context contract.

## Manual evidence and existing test responsibilities

Implementation must actually scaffold each package, inspect the pristine result as an agent and preserve reproducible inputs/results. Use minimal admitted contexts and representative filled contexts under the new contracts; minimal full documents now include an explicitly supplied initial metadata revision, and minimal Python class contexts include both description fields.

| Batch | Packages | First-output inspection |
| --- | --- | --- |
| Full documents | Architecture, Research, Design, Planning, Validation Report, Reference, Generic Doc | Visible metadata/history, correct current revision, substantive hierarchy/content, generated separators and EOF |
| Python classes | Class, Protocol, Pydantic Config, Pydantic DTO, Adapter, Worker | Distinct docs, field/value preservation, imports/spacing, models, absence handling, one main class |
| Python tests | Pytest Unit and Integration | Retained description semantics, fixtures/cases/decorators, joins and valid Python structure |
| Tracking | Issue, PR, Commit | Body/text presentation, publishing boundary and EOF |
| TypeScript | DTO | Independent docs, constructor assignments/optional blocks, empty fields and EOF |

Use targeted additional contexts where the first two do not exercise the relevant boundary. These are manual scaffold examples and evidence, not a new automated regression suite:

- Text padding with empty and spaces/tabs-only boundary lines, internal blank lines, meaningful indentation, LF/CRLF, Markdown hard-break spaces, fences and caller literal values.
- Absent, empty and whitespace-only optional text; confirm presence remains distinct while generated residue disappears.
- Python empty/filled model configuration and fields, composed collections, fixed and supplied import groups, decorators and caller bodies whose interiors must remain untouched.
- Document one/multiple revision rows, delimiter characters, concise/multiline decision explanations, custom section order and checked/unchecked items.
- TypeScript absent/empty/filled module documentation and zero/multiple field assignments with a distinct optional block.
- Render through the real scaffold tool and applicable admitted fixture path where useful; record differences instead of treating a fixture render as production proof.

Retain the first output before applying a fix. A repaired file is not evidence that the template's first call was correct. After a template correction, scaffold anew and inspect the new first output. Native Ruff, language syntax and Markdown/link checks provide factual support; their success does not prove header content, meaning, semantic preservation or presentation quality.

Existing tests remain first-class code under the architecture and typing contract. Adapt valuable existing input/expectation coverage only where this issue changes the behavior it covers. Existing tests and relevant narrow gates remain required; do not add automated content/regression coverage to satisfy a generic phase instruction. Planning will assign the smallest checks to changed surfaces and reserve the full configured suite/broad gates for Validation.

## Current-tool practice assessment and #476 boundary

Actively evaluate correctness and usability of the #460-derived tools during real execution: `scaffold_schema`, `scaffold_artifact`, `safe_edit_file`, `run_checks`, `run_tests` and `apply_fixes`, plus bounded derived routes encountered in the work. Record `get_project_plan` or transport/metadata friction when encountered. The Create Issue boundary can use controlled existing evidence and its actual authored-body contract; no unrelated external mutation is needed.

A finding contains the active commit, server/package/native versions when relevant, prerequisites, exact tool request or selected context, expected behavior and its authority, compact outcome plus complete cached DTO/native evidence, file effects, reproducibility, impact, uncertainty, available workaround and linked follow-up/disposition. Distinguish a genuine fault, caller misuse, unsupported selection, presentation limitation and usability friction. Do not infer a regression from #460 without evidence or compute a pre/post score.

Preserve pristine scaffolds before exploratory repairs, isolate fix probes from sources, and read complete cached run resources. Reuse observations when sufficiently fresh; do not create tests or production edits merely to manufacture a tool exercise. A route that cannot be exercised safely/relevantly receives an explicit coverage limitation.

One current Design observation is reproducible already: the existing Markdown preflight reports broken links for valid angle-bracket Markdown targets in the initial Design scaffold, while still returning passed. The complete scaffold DTO is `pgmcp://cache/runs/7dc10b74f07948518abf5f16ddcb3c91`. Its warnings treat angle brackets as filename characters. This is a preliminary tooling finding to reproduce and disposition during implementation; it is not a reason to change the metadata contract or silently repair the Markdown adapter here.

Issue #473 owns concrete value/effect inspection and package-local ignored-input defects within its approved objectives. Issue #476 owns generic consumption analysis, ambiguous/uncertain versus absent consumption, false-positive handling and related enforcement strategy. Shared evidence is a hand-off, not automatic integration. If a later finding requires generic analysis or invalidates the approved clean break, reopen the human strategy decision explicitly.

## Verification obligations

| Obligation | Evidence method | Expected result and limit |
| --- | --- | --- |
| All shipped packages produce reviewed first outputs | Actual minimal/filled scaffolds with preserved inputs/results and manual inspection | All 19 covered; objective-specific findings are explained, not hidden by repairs |
| Generated whitespace is controlled | Targeted examples and physical line/EOF inspection, supported by native format output | Language-owned joins and one terminal LF; caller interiors/literals preserved |
| Full-document facts are explicit and coherent | Schema discovery plus inspected one/multiple-revision outputs | Required metadata; header derives from final row; no invented facts |
| Description separation is real | Independent values, identical explicit values and empty/absent examples | No fallback/dedup; agreed requiredness and Pytest exception |
| Generated Python baseline | Configured native checks on clean-fragment examples and causal reading of findings | Generated structure passes; caller findings remain attributed |
| Presentation preserves meaning | Agent reads rendered/raw Architecture/Generic Doc examples | Hierarchy, decisions, lists/fences, order and checklist state retained |
| Known consumers adopt the clean break | Source inventory and relevant existing fixture/test execution | No active known caller relies on removed contracts; no aliases |
| Admission/render capabilities agree | Review shared registration in bootstrap and relevant delivered/installed/synthetic fixtures; actually scaffold through admitted packages | Same real filter names/callables before analysis and rendering; no validation bypass or separate layer |
| Generic boundaries remain narrow | Review engine/catalog/bootstrap and existing relevant coverage | One boundary primitive; composition/EOF stay in templates; no artifact-specific renderer policy or added runtime gate |
| Current tool practice is useful | Reproducible findings log and route coverage/limitations | Current behavior documented for later triage; no speculative scoring |
| Standards agree with behavior | Relevant standards/active instructions diff and affected link review | Single responsibility model; historical evidence preserved |
| Strategy remains binding | Research-to-Design/Planning traceability and independent reviews | #476 separate; additional automated content tests absent |

## Risks and planning consequences

The largest implementation risk is normalization applied at the wrong role, silently altering caller literal values or internal whitespace. Keep the boundary function generic, apply it explicitly at selected insertion seams, and demonstrate preservation with manual boundary examples. A whole-output formatter would conceal this risk and is excluded.

A shared base correction has a wide package blast radius. All 19 first-output pairs and targeted optional cases must be inspected; shared synthetic consumers and the two Pytest roots are material migration inputs. Update valuable existing tests where contracts changed, rather than creating a duplicate content suite.

The metadata input is deliberately incompatible with old optional root facts. Its explicit revision sequence eliminates duplicate header facts but requires known callers to provide their own history/status. Preserve old authored files; migrate only actual active inputs and affected references.

Multiline formatting of generated expressions can be bounded by caller values that cannot sensibly wrap. Record that limit rather than silently rewriting values or weakening the configured native baseline. Architecture decisions containing structured explanations must remain outside the concise table path.

Stale server/catalog graphs or test-environment differences can invalidate observations. Record the active context and use the supported refresh boundary after changes. Preserve complete DTO/native evidence when summaries lose detail.

Planning must assign implementation boundaries, consumer migration, narrow existing test/gate execution, manual scaffold inventory and the durable current-tool findings location. It must also identify how independent QA will verify representative evidence without granting producer-delegated reviewers workflow authority. The broad configured suite and full gates remain Validation work.

## Sources and review request

Primary behavior/approval inputs:

- [Approved Research](research.md#approved-strategy)
- [First-output survey](first-output-survey.md)
- [Python class comparison](python-class-comparison.md)
- [Design document comparison](design-document-comparison.md)
- [Document-family comparison](document-family-comparison.md)
- [Python-family comparison](python-family-comparison.md)
- [Whitespace comparison](whitespace-comparison.md)
- [Tracking/TypeScript comparison](tracking-typescript-comparison.md)
- [Native tooling follow-up](native-tooling-follow-up.md)

Material implementation entry points:

- [Template engine](../../../mcp_server/services/template_engine.py)
- [Catalog and renderer](../../../mcp_server/services/template_catalog.py)
- [Schema contract loader](../../../mcp_server/services/template_contract_loader.py)
- [Injected environment/bootstrap](../../../mcp_server/bootstrap.py)
- [Shared artifact root](../../../.pgmcp/template_suite/shared/templates/bases/tier0_root.jinja2)
- [Shared Markdown document base](../../../.pgmcp/template_suite/shared/templates/bases/tier2_markdown_document.jinja2)
- [Shared Python base](../../../.pgmcp/template_suite/shared/templates/bases/tier2_python.jinja2)
- [Python model macros](../../../.pgmcp/template_suite/shared/templates/patterns/python/pydantic.jinja2)
- [Document section macros](../../../.pgmcp/template_suite/shared/templates/patterns/markdown/sections.jinja2)
- [Delivered-template fixtures](../../../tests/mcp_server/fixtures/delivered_templates.py)
- [Installed-distribution admission probe](../../../tests/mcp_server/fixtures/installed_distribution.py)
- [Shared document consumers](../../../tests/mcp_server/integration/templates/test_shared_documents.py)
- [Shared Python consumers](../../../tests/mcp_server/integration/templates/test_shared_python.py)
- [Generic engine tests](../../../tests/mcp_server/unit/services/test_template_engine.py)
- [Active scaffolding reference](../../reference/tools/scaffolding.md)
- [Template usage guide](../../reference/TEMPLATE_LIBRARY_USAGE.md)
- [Create-issue workflow](../../../.agents/workflows/create-issue.md)
- [Mirrored Create-issue prompt](../../../.github/prompts/create-issue.prompt.md)
- [Create Issue tool boundary](../../../mcp_server/tools/issue_tools.py)

Review requested: independently assess this Design against the approved Research boundaries, architecture contract, real schema/template seams, preservation/failure obligations, bounded migration and human-selected manual evidence strategy. No producer approval is claimed. Implementation and Planning have not started.

## Design-phase evidence and reality check

The initial artifact was created through `scaffold_artifact(artifact_type="design", file_name="design.md", target_path="docs/development/issue473", validation="enforce")` using the currently shipped schema, then completed through `safe_edit_file` with enforce validation. The existing scaffold does not yet implement this Design; its provenance remains unchanged.

The revised document's Markdown preflight returned passed with no issues (`pgmcp://cache/runs/7be522daabff4740ace6533899a33964`). The targeted configured `markdown_link_review` on `docs/development/issue473/design.md` returned passed: 35 successful links, 0 errors and 0 excluded, with offline fragment checking and Lychee 0.24.2 (`pgmcp://cache/runs/79f8bfc99f024ab5ba8dbe5e496d7bbe`). Complete cached DTOs were read. These checks prove the authored document's checked structure/links, not implementation behavior or independent Design approval.

Revision 0.2 narrows the proposed Python addition from three filters to one boundary primitive and makes shared registration before admission/rendering explicit, including delivered/installed fixture consumers. Its targeted review must assess whether this resolves the previous independent P2; the producer does not close that finding by assertion.

Pre-commit reality check: Research's per-boundary decisions remain intact; mechanism ownership is traced to actual engine/catalog/template seams; known affected inputs and existing coverage are enumerated; preservation, failure and manual evidence obligations are explicit. The initial Design commit changed this artifact and the MCP-recorded phase transition; revision 0.2 changes only this Design artifact. No production, template, schema, test or standard has been edited, and no new automated content/regression tests or runtime gates have been introduced.

### Bug / Design Hand-over

#### Scope

- Completed correction architecture, public metadata/description contracts, layout ownership, bounded consumer inventory and manual evidence responsibilities.
- Excluded production implementation, Planning sequencing, full Validation, generic #476 analysis and unrelated tool repairs.

#### Deliverables

- [Design](design.md), with [Approved Research](research.md#approved-strategy) and source entry points above as material inputs.
- MCP-recorded branch state reflects the human-approved Research → Design transition.

#### Evidence

- Initial scaffold and completed-document enforce preflight accepted.
- Targeted configured offline link review: 35 successful, 0 errors, 0 excluded; complete cached evidence inspected.
- Producer source/strategy review completed with the limits described above.

#### Open Work

- Targeted independent Design re-review of shared filter availability and minimized composition ownership, followed by the authorized phase decision.
- Implementation evidence must establish the proposed mechanisms; current-tool finding requires reproducible disposition during execution.
- Planning will specify execution boundaries, durable evidence destinations and narrow existing checks.

#### Review Request

- Review requested.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-03 | @imp designer (Codex) | Initial correction architecture, explicit metadata/description contracts, preservation boundaries, consumer inventory and manual verification obligations. |
| 0.2 | 2026-10-03 | @imp designer (Codex) | Record human-approved minimization to one boundary filter, shared real registration before admission/rendering, template-owned joins/EOF and affected installed/delivered fixture setup for independent P2 re-review. |
