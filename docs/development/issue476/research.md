<!-- pgmcp:v1 id=research pv=1.0.0 pf=lgBwxWMfTAmNNg_O sf=5--KpGf2wHUv2qAj -->

# Issue 476 — Schema-to-template consumption research

**Status:** DRAFT — approved strategy and bounded package audit; independent review pending  
**Version:** 0.3  
**Last Updated:** 2026-10-07

## Purpose

Establish schema-to-output coherence through a bounded review of the delivered packages. The approved direction uses LLM-assisted semantic review and existing behavior evidence before release; this is Research, not a new analyzer design or implementation sequence.

## Scope In

Prepared context schemas, the admitted Jinja graph, caller content and reachable render consumers; current package fixtures, authoring and startup/renewal admission boundaries.

## Scope Out

Production changes, a new public MCP tool, compatibility bridges, template-ID/field-name exceptions, whole-suite semantic completeness claims, package repairs without a demonstrated defect, and new regression tests for existing behavior.

## Problem Statement

Template admission rejects undeclared static Jinja reads but does not prove that every admitted caller field influences the artifact. No current V3 shipped silently ignored field has been demonstrated by this investigation. D-VAL-08 explicitly deferred both the mechanism and enforcement decision from #460.

## Goals

- Define consumption beyond a syntactic reference.
- Identify schema/Jinja constructs that can be resolved generically and cases that must remain uncertain.
- Compare authoring diagnostics, behavior-supported conformance and startup rejection with explicit consumer impact; capture the selected release-time review boundary.
- Preserve current undeclared-read rejection; obtain a boundary-specific human strategy before Design.

## Background

The source suite contains 19 concrete packages. TemplateContractLoader prepares Draft 2020-12 schemas through the existing reference resolver. TemplateGraphResolver snapshots literal extends/include/import/from-import dependencies. TemplateCatalogLoader joins these inputs and calls TemplateInputValidator for each package. Startup and renewal both consume this admission route. Runtime schema discovery and scaffolding use the immutable admitted catalog; they do not rediscover source files.

## Findings

### Consumption boundary

Consumption is an evidence-backed dependency of emitted content or structure on a caller value or its presence, including branches, iteration, ordering and downstream rendering. A validated shape, a read that is discarded, or forwarding an object without inspecting the callee is insufficient. Normalization can make some different inputs equivalent without making the field unused. Schema annotations and uninstantiated definitions are not caller fields.

| Classification | Evidence needed | Permitted claim |
| --- | --- | --- |
| Observed consumption | Traceable output/control dependency, or a valid behavior witness demonstrating influence | The identified path has a consumer; distinguish a static trace from a rendered witness |
| No observed consumer | No output dependency found within the explicitly analyzed, resolved portion | Candidate for author review; absence of evidence is not universal proof of unusedness |
| Uncertain | Dynamic access, opaque transformation, unresolved call/control flow or schema applicability | State the unresolved construct; do not mark it consumed or defective |

A reference inside an uncalled macro or overridden parent block does not establish effective output. A condition with identical branch output can read a field without consuming it semantically. A parent-object read does not establish all child paths. Presence-only selection can consume a field even when its characters are never printed. Constant/constrained branch discriminators require schema context; do not demand two different valid scalar values where the schema permits only one.

### Existing responsibilities and coupling

| Boundary | Current responsibility | Consequence for this research |
| --- | --- | --- |
| TemplateContractLoader / schema_utils | Contained finite reference resolution; references and sibling assertions retain composition scope | Reuse prepared schema semantics; do not invent a second resolver or flatten compositions |
| TemplateGraphResolver | Immutable source closure and dependency edges | A file closure is not a macro call graph or effective inheritance/block graph |
| TemplateInputValidator | Lexical binding and declared-path validation | Its read inventory includes assignments and macro bodies; it is not output dataflow |
| TemplateCatalogRenderer / TemplateEngine | Validate caller JSON and render content/provenance envelopes | Rendering consumes the same snapshot; probes must not reopen files or mutate caller content |
| Bootstrap / CLI renewal | Admit a complete suite before serving or activating it | Adding reverse rejection here affects availability, activation and third-party packages together |
| DeliveredTemplate fixtures | Copy one opaque package plus real shared sources and compose public catalog/renderer calls | Preserve behavioral evidence; avoid coupling new tests to private traversal helpers |

The existing validator supports direct paths, aliases, literal get(), loop item bindings, local scopes, imports and inheritance. Macro formals deliberately lose caller-path identity; a filtered iterable can also lose that identity. Computed keys retain their container. Its composition search establishes possible declaration linkage, not which schema alternative applies to a particular valid caller context.

### Bounded inventory and false-alarm evidence

Read-only source inventory on 2026-10-07 compared each package's root properties with root-template matches of the regex `\bcontent\.([A-Za-z_][A-Za-z0-9_]*)`. It found **195 package/root-property occurrences; 79 had no root dotted reference**.

| Explanation independently traced in source | Occurrences |
| --- | ---: |
| Seven shared document fields across seven document packages | 49 |
| Literal-key selection loops: Design 8, Research 4, Validation 8, Issue 4 | 24 |
| Shared tracking related_docs in Issue and PR | 2 |
| Inherited imports in two Pytest packages, Python class and TypeScript DTO | 4 |
| Total naive missing-reference candidates accounted for | 79 |

All 79 have source consumers through inheritance or finite computed keys. Calling these 79 unused fields would produce 79 source-refuted alarms in this deliberately naive baseline. This is not a measured false-positive rate for a future AST analyzer, nor evidence that all nested paths or all render branches are correct. No analyzer prototype or render probe was executed.

### Representative semantic cases

| Case and source | Evidence / unresolved work |
| --- | --- |
| Shared document purpose/scope fields | Literal tuple unpacking determines content[field]; finite key sets can be traced |
| methods[].parameters[].default, Python signatures | Root loop passes a record to a shared macro, which calls another macro; requires argument and item-path tracking |
| imports.stdlib / third_party / project | Mapping get(group) uses a finite string loop inside a shared macro; alias and call context matter |
| document_metadata.revisions | last affects the current header; all revisions affect history; track filtered selection and iteration separately |
| checklist[].checked | Shared macro selects x/space; structural consumption without printing True/False |
| Import oneOf and class-method allOf | Branch conditions and reference siblings remain meaningful; property-name union is insufficient |
| Schema additionalProperties / patternProperties | Open or patterned children are families, not a finite list of named properties; unresolved selection must remain explicit |
| Arbitrary filter/function or whole-object forwarding | Cannot infer every child consumer from the argument alone |
| Uncalled macro, unused assignment, overridden block | Syntactic reads can create false consumption claims; effective reachability matters |

Representative render probes can provide positive witnesses but cannot prove all optional values, legal branches or opaque functions. Jinja's Meta API provides possible context lookups across execution paths, not semantic output dependence. Imports and includes have different context defaults. Draft 2020-12 composition and conditional applicators preserve distinct validation scopes; the current resolver already retains these.

### Historical contract investigation — human clarification 2026-10-07

The owner's recollection is supported: explicit contracts were introduced because Jinja introspection could not reliably serve as the input-contract authority. The first investigation omitted this history. Its preliminary authoring-diagnostics recommendation was suspended pending reconciliation of the intended guarantee; the earlier A/B/C question was not an approval. The later human decision below selects a bounded release-time review.

| Stage | Established decision / evidence | Guarantee boundary |
| --- | --- | --- |
| [#52 introspection research](../archive/issue52/archive/jinja2_introspection_research.md) — 2025-12-30 | Static AST cannot determine exact output, condition outcomes or dynamic references; proposed source metadata, pattern checks and representative rendering | Explicit output structure/rules, not exhaustive field influence |
| [#135 Pydantic-first Research](../archive/issue135/research-pydantic-v2.md) and [strategy](../archive/issue135/SCAFFOLDING_STRATEGY.md) — February 2026 | Stop guessing requiredness from Jinja/default filters; explicit schemas validate before rendering, Jinja owns presentation | Authored input rules replace inferred input rules |
| [#286 three-layer contract](../archive/issue286/research.md#7-the-three-layer-ssot-model-is-confirmed-in-code-but-absent-from-all-reference-documentation) — June 2026 | Context owns caller input; RenderContext adds system lifecycle; Jinja owns output structure | Responsibility separation; does not itself enforce reverse consumption |
| [#260 asset trinity](../archive/issue260/findings.md#f11--template-workspace-initiative-future-issue), [#349 Research](../archive/issue349/research.md) and [Design](../archive/issue349/design.md) — workspace transition, July 2026 | Schemas + Jinja + artifacts.yaml remain a joint unit. Python Context/RenderContext classes are replaced with declarative schemas and dynamic Pydantic models; lifecycle enrichment remains | The declarative successor called effectively V3 changed representation, not the intended validation/rendering responsibilities |
| [#460 invariant and migration](../issue460/research.md#core-invariants) | Package-local JSON Schema owns input; separate provenance owns system data; selected Jinja owns rendering; policy selects output checks; one immutable catalog binds them | Input acceptance/exposure remain explicit. Generic reverse consumption was expressly deferred as D-VAL-08 |

Template-pipeline V1/V2/V3 labels and the installed PGMCP package version are different axes. Pydantic-first V2 introduced the explicit runtime contract; it did not remove it. The installed S1mpleTrader PGMCP 2.0.0 already uses the later dynamic YAML-model implementation. Current V3 continues schema-first acceptance; its AST linkage check does not infer requiredness or field types.

Historical success promises were stronger than the evidence established. #135's strategy claimed that model-valid input guarantees rendering success. Its [Design §6.3](../archive/issue135/design-pydantic-v2-architecture.md#63-cycle-4-parity-test-scope-re-baseline-2026-02-17) later narrowed parity to smoke, documented skipped V2 default-value syntax failures and retained semantic-parity risk. #286 documented schema-valid nonempty string methods failing because Jinja expected records, despite the three-layer model; its planning notes that the full fixture omitted methods. These are historical defects, not findings against current V3.

Read-only verification of the installed V2 at C:/1Voudig/99_Programming/ST confirmed:
- managers/artifact_manager.py builds dynamic Pydantic input and RenderContext models, enriches lifecycle data, then calls scaffolding with skip_validation=True because schema validation already occurred (line 665). This bypasses inferred input validation; it does not bypass all later output checks.
- scaffolding/template_introspector.py:188 unions context-variable names across the inheritance chain and classifies required/optional inputs. It has no all-declared-fields-to-output check.
- templates/config/pr.yaml:56 declares tracking_state. Searching the installed template suite for tracking_state found that YAML declaration only; the PR rendering body has no consumer. [#460's original Problem Statement](../issue460/research.md#problem-statement) records this same ignored field. The current PR package removes that field.

No V2 tool was invoked, no installation was changed, and no historical test result was rerun. Source reading confirms that a silently ignored schema field existed before current V3; a universal reverse guarantee cannot therefore be assumed from the old architecture. The source lookup is reproducible with rg -n tracking_state over the installed templates directory, selecting *.yaml and *.jinja2.

Research consequence: preserve the original schema-first principle and integrated package ownership. Decide whether #476 needs clearer package-conformance evidence, or a new bounded authoring capability with a demonstrated consumer. Reintroducing Jinja-derived acceptance schemas is outside scope. Restoring old Python RenderContext classes does not automatically solve missing output consumption. No automatic analyzer or startup-blocking policy is approved.

### Delivered-package contract audit — 2026-10-07

Read-only LLM-assisted review covered each of the **19 package schemas and effective root templates: 195 exposed root-property occurrences**, plus their referenced nested records and shared render consumers. Source baseline: commit 65abf827d3982fa2024872e89b8d4e2e941f5716; this issue has changed only Research and workflow state. Two bounded delegated reviews supplied findings only; the producer verified all root templates, shared consumers and relevant schema records directly. Counts are a review inventory, not a semantic completeness score.

**Observed result:** every exposed root property has an effective source-traced output/control consumer. No silently ignored field or declared-meaning mismatch was demonstrated, and no unresolved consumer path required a new render probe. This does not certify every valid input combination or caller-authored code. All evidence below is source inspection; existing tests were inspected, not executed.

| Package root consumer entry | Root properties reviewed | Effective consumer routes |
| --- | ---: | --- |
| [architecture](../../../.pgmcp/template_suite/architecture/template.jinja2) | 11 | concepts and subsections; decision table/detail; constraints and sources |
| [commit](../../../.pgmcp/template_suite/commit/template.jinja2) | 8 | header, breaking marker/description, body/footer and numeric refs |
| [design](../../../.pgmcp/template_suite/design/template.jinja2) | 27 | prose/key loops; options, decisions, contract sections, validation and risks |
| [generic_doc](../../../.pgmcp/template_suite/generic_doc/template.jinja2) | 13 | summary, lists, FAQ, custom sections and checklist states |
| [issue](../../../.pgmcp/template_suite/issue/template.jinja2) | 7 | problem, optional prose loop, numbered steps and inherited related links |
| [planning](../../../.pgmcp/template_suite/planning/template.jinja2) | 13 | work units, deliverables/null validation, verification and finite phase collections |
| [pr](../../../.pgmcp/template_suite/pr/template.jinja2) | 8 | change prose, deferred groups, checklist states, closes and inherited related links |
| [pytest_integration_test](../../../.pgmcp/template_suite/pytest_integration_test/template.jinja2) | 6 | module description/imports, cases, fixtures, markers and optional class |
| [pytest_unit_test](../../../.pgmcp/template_suite/pytest_unit_test/template.jinja2) | 6 | module description/imports, cases, fixtures, markers and optional class |
| [python_adapter](../../../.pgmcp/template_suite/python_adapter/template.jinja2) | 8 | declarations, imports/bases, constructor, concrete methods and opt-in logging |
| [python_class](../../../.pgmcp/template_suite/python_class/template.jinja2) | 6 | declarations, imports/bases and supplied signatures with fixed raise stubs |
| [python_protocol](../../../.pgmcp/template_suite/python_protocol/template.jinja2) | 6 | declarations, caller imports/bases plus Protocol and signatures with ellipsis stubs |
| [python_pydantic_config](../../../.pgmcp/template_suite/python_pydantic_config/template.jinja2) | 7 | declarations/imports, fields, frozen flag and examples |
| [python_pydantic_dto](../../../.pgmcp/template_suite/python_pydantic_dto/template.jinja2) | 6 | declarations/imports, fields and examples; frozen is a fixed package choice |
| [python_worker](../../../.pgmcp/template_suite/python_worker/template.jinja2) | 7 | declarations/imports, constructor, concrete operation and opt-in logging |
| [reference](../../../.pgmcp/template_suite/reference/template.jinja2) | 11 | sources, nested API entries/methods, test links and language/code examples |
| [research](../../../.pgmcp/template_suite/research/template.jinja2) | 19 | prose/key loops, goals/questions, evidence, consumers, risks and links |
| [typescript_dto](../../../.pgmcp/template_suite/typescript_dto/template.jinja2) | 6 | JSDoc/imports, implements and typed fields/constructor assignments |
| [validation_report](../../../.pgmcp/template_suite/validation_report/template.jinja2) | 20 | status/prose loops, obligations, evidence, risks and deferred groups |

Each linked template is paired with its co-located context.schema.json. The seven document packages share effective heading/before/after/metadata blocks; none overrides them away. The code and tracking bases similarly compose the overridden blocks into final output. Review followed actual calls, branch applicability and explicit finite key sets, rather than merely counting read syntax.

| Nested contract / paths reviewed | Effective consumption evidence |
| --- | --- |
| Document metadata: status; revisions[].version/date/author/change | [Document base](../../../.pgmcp/template_suite/shared/templates/bases/tier2_markdown_document.jinja2): last revision supplies current version/date; all revisions supply history rows |
| Links: label/target; checklist: text/checked; issue-reference integers | [Link macros](../../../.pgmcp/template_suite/shared/templates/patterns/markdown/links.jinja2) emit both link fields; [section macros](../../../.pgmcp/template_suite/shared/templates/patterns/markdown/sections.jinja2) emit text and x/space state, or numeric issue references |
| Document package records: concepts/subsections, alternatives, FAQ, sections, decisions, risks, evidence and evidence requirements | Linked package bodies emit each record field, with optional-presence branches and shared list/link consumers; section anyOf alternatives remain separate admitted carriers |
| Planning work_units[] and nested deliverables/validates/verification; phase_deliverables | [Planning macros](../../../.pgmcp/template_suite/planning/template.jinja2) consume all 14 work-unit fields, deliverable id/description/owner/validates, null versus object and validation type/file/text/path; all three admitted phase keys are iterated |
| Reference api_reference[].methods[] and usage_examples[] | [Reference macros](../../../.pgmcp/template_suite/reference/template.jinja2) emit signatures, parameters, returns, optional description/errors and separate entry/method source namespaces; examples emit description/language/code |
| Deferred items: description/rationale/references | PR and Validation bodies emit each field within the corresponding item; references reach actual link emitters |
| Python Imports: stdlib/third_party/project; import/from variants and names[] | [Import macros](../../../.pgmcp/template_suite/shared/templates/patterns/python/imports.jinja2) iterate the finite groups; kind controls the applicable statement, module/alias and names[].name/alias are emitted, including the constrained star variant |
| Signature/ConcreteMethod/Constructor/Parameter; pytest TestCase/Fixture | [Signature macros](../../../.pgmcp/template_suite/shared/templates/patterns/python/signatures.jinja2) emit applicable names/descriptions/async/return types, parameters/defaults and supplied bodies; [pytest macros](../../../.pgmcp/template_suite/shared/templates/patterns/testing/pytest.jinja2) additionally emit case markers and fixture decorator/scope/autouse |
| ModelField: name/type/description/default/default_factory and seven constraint keys; examples' open objects | [Pydantic macros](../../../.pgmcp/template_suite/shared/templates/patterns/python/pydantic.jinja2) emit every field property, use the mutually exclusive default branches and recurse through mapping keys/values and arrays; examples reach ConfigDict |
| Logging.name; TypeScript fields[].name/type/readonly/optional/description | [Logging macro](../../../.pgmcp/template_suite/shared/templates/patterns/python/logging.jinja2) emits the explicit name or package default; [TypeScript root](../../../.pgmcp/template_suite/typescript_dto/template.jinja2) emits properties/JSDoc and makes optional presence control constructor assignments |

Representative existing behavior assertions are in [shared documents](../../../tests/mcp_server/integration/templates/test_shared_documents.py), [shared Python](../../../tests/mcp_server/integration/templates/test_shared_python.py), [PR](../../../tests/mcp_server/integration/templates/test_pr.py), [pytest unit](../../../tests/mcp_server/integration/templates/test_pytest_unit_test.py), [pytest integration](../../../tests/mcp_server/integration/templates/test_pytest_integration_test.py), [Pydantic config](../../../tests/mcp_server/integration/templates/test_python_pydantic_config.py) and [reference](../../../tests/mcp_server/integration/templates/test_reference.py). They inspect rendered values, AST structure, explicit states, defaults, grouping and presence behavior. Their current execution outcome is not asserted by this audit.

No defect repair is proposed from these findings. Explicit normalization, sorted/deduplicated imports, empty collections and fixed package choices can make distinct inputs produce equal bytes; that is not an ignored schema declaration. [text_block](../../../mcp_server/services/template_engine.py) removes blank edge lines while retaining meaningful interiors. The release review must assess declared meaning, not demand injectivity. Runtime validity of arbitrary caller-authored expressions and exhaustive combinations remains outside this source-audit claim.

### Strategy comparison and selected direction

| Strategy | Consumer / compatibility impact | Cost, risk and limitation |
| --- | --- | --- |
| Automated authoring diagnostics | Preserve admission but introduce a new analysis capability | Requires bounded inference rules and evaluation; semantic uncertainty remains |
| LLM-assisted package review with existing behavior evidence — selected | Preserve admission and runtime; review supplied packages before release | Uses contextual judgment without claiming exhaustive proof; review must retain sources, unresolved cases and focused witnesses |
| Reverse startup rejection | Reject otherwise admitted suites at startup/renewal | Highest availability impact; sound generic rejection rules and demonstrated defects are absent |

The owner approved the previously proposed bounded audit and clarified that package conformance can belong to the release procedure and its stated promise. The intended review uses an LLM's contextual reasoning rather than a new static analysis attempting to overcome Jinja's known semantic limits.

The audit covers all 19 delivered packages and relevant nested fields. Shared records and macros are reviewed once and traced to package callers. Existing behavior evidence is reused; focused render probes are reserved for unresolved material questions. Findings distinguish silently discarded input, meaning different from the declared contract, and insufficient evidence. Actual defects return to the owner before repair Design. No new engine, consumption annotations or per-field regression matrix is selected.

## Questions

- How should the eventual release procedure retain the review's scope, findings and limitations with minimal maintenance? Exact integration belongs to Design.

## References

- [D-VAL-08 original deferred boundary](<../issue460/deferred-work.md#d-val-08--generic-schematemplate-consumption-analysis>)
- [Jinja Meta API](<https://jinja.palletsprojects.com/en/stable/api/#the-meta-api>)
- [Jinja import/include context rules](<https://jinja.palletsprojects.com/en/stable/templates/#import-context-behavior>)
- [JSON Schema 2020-12 applicator semantics](<https://json-schema.org/draft/2020-12/json-schema-core#section-10>)

## Approved Strategy

Human approval on 2026-10-07: "Ja deze route spreekt me aan." The owner explicitly places package validation in the release procedure and its stated promise, using LLM judgment rather than a new static analyzer. This approves the following boundaries, not any unobserved package repair:

| Boundary | Approved decision | Rationale / consumer impact |
| --- | --- | --- |
| Public caller schemas and rendering | Preserve supported input/output behavior during the audit. Any demonstrated defect is discussed before repair Design; approved repairs use a clean break without legacy/compatibility layers | No silent contract change on the strength of a syntactic suspicion |
| Admission, startup, renewal and each scaffold call | Preserve current schema validation and undeclared-read checks. Add no reverse-consumption gate to startup or individual uses | Package coherence is reviewed before release; serving and usage retain existing behavior |
| Package authoring and release assurance | Perform a bounded LLM-assisted contract audit of the 19 delivered packages, including effective shared and nested consumers; retain traceable findings and honest uncertainty | Contextual semantic review fits agentic authoring; a reviewed release promise is bounded by evidence, not an exhaustive theorem |
| Evidence and tests | Reuse relevant existing behavior evidence. Use focused tool/render demonstrations only for material unresolved cases; no new regression tests for old behavior, duplicate annotations or per-field coverage matrix | Evidence supports declared behavior while keeping maintenance and test volume controlled |
| Production mechanism and instructions | No new analyzer, public MCP tool or instruction proliferation is approved. Exact minimal release integration remains a Design question after findings | Keep tool knowledge and authored contracts in their existing boundaries |

## Expected Results

A compact durable audit records package coverage, effective consumption evidence for relevant root and nested fields, demonstrated defects separately from uncertainty, and remaining limitations. LLM inference is a reviewed claim, not automatic proof; whole-object forwarding and mere syntactic references do not establish all child consumers. Existing schema compositions and Jinja scope/call semantics remain authoritative. No current V3 shipped silently ignored field has yet been established. The 79 naive candidates are source-accounted, not a completed package-conformance review.

Research proceeds to independent QA after the bounded audit and findings are recorded. Demonstrated defects are presented to the owner before repair Design. The eventual release promise must identify what was reviewed and proven and must not imply that every valid input combination or opaque function was exhaustively verified.

## Evidence

### Current admission is one-way declaration linkage

TemplateInputValidator.validate checks discovered reads through _declares_path. It never enumerates all declarations and compares output dependencies. The existing snapshot test admits a replacement literal template 'Updated' with the same field schema; this demonstrates the intentionally missing reverse requirement in a fixture, not a shipped-package defect.

- [Catalog and input validator](<../../../mcp_server/services/template_catalog.py>)
- [Catalog behavior cases](<../../../tests/mcp_server/unit/services/test_template_catalog.py>)

### Prepared graph and schemas already provide reusable boundaries

The graph carries exact source bytes, roots and edges. Schema resolution preserves referenced assertions in allOf branches and rejects unsupported/cyclic reference forms. A consumption analysis should not widen admitted Jinja dependency syntax or JSON Schema support.

- [Template graph](<../../../mcp_server/services/template_graph.py>)
- [Schema contract loader](<../../../mcp_server/services/template_contract_loader.py>)
- [Reference resolver](<../../../mcp_server/utils/schema_utils.py>)

### Existing tests observe real rendered behavior

Inspected, not rerun: test_common_document_fields_preserve_absent_empty_and_populated_content; test_shared_records_validate_before_render_and_preserve_explicit_check_state; test_explicit_bases_imports_and_ordered_sync_async_signatures; composed-schema and native-scope catalog cases. These protect selected invariants but do not establish exhaustive reverse coverage.

- [Shared document cases](<../../../tests/mcp_server/integration/templates/test_shared_documents.py>)
- [Python class cases](<../../../tests/mcp_server/integration/templates/test_python_class.py>)
- [Delivered fixture composition](<../../../tests/mcp_server/fixtures/delivered_templates.py>)

### Research document checks

On 2026-10-07, safe_edit_file(path="docs/development/issue476/research.md", validation="enforce") reported written=True and validation=passed for the approved-strategy/audit update. run_checks(scope="targets", targets=["docs/development/issue476/research.md"], checks=["markdown_links"], timeout_seconds=120) reported markdown_links=passed with configured arguments. No production/test source changed and no tests or render probes were run. These document checks do not validate the semantic audit claims; independent QA is requested separately.

## Consumers

### Package authors and maintainers

Keep exposed schema fields and render behavior coherent

**Impact:** Receive reviewed, source-based conformance findings with explicit uncertainty; no hardcoded package vocabulary or duplicated consumption metadata.

### Agents using scaffold\_schema/scaffold\_artifact

Supply admitted context and inspect generated output

**Impact:** Existing input/output contracts and absence/empty semantics should remain stable under the recommended strategy.

### Server startup and template renewal

Admit one coherent suite snapshot

**Impact:** Reverse blocking would reject the complete suite and affect serving, upgrades and owner-specialized packages.

### Tests and package distribution

Observe actual supplied package behavior through opaque-location fixtures

**Impact:** Reuse valuable behavior cases and retain the release review's scope and evidence; no new per-field regression matrix or old-behavior test additions.

## Related Documents

- [Public scaffolding contracts](<../../reference/tools/scaffolding.md>)
- [Architecture contract](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)
- [Shared document consumers](<../../../.pgmcp/template_suite/shared/templates/bases/tier2_markdown_document.jinja2>)
- [Shared Python signature consumers](<../../../.pgmcp/template_suite/shared/templates/patterns/python/signatures.jinja2>)
- [Shared Python import consumers](<../../../.pgmcp/template_suite/shared/templates/patterns/python/imports.jinja2>)
- [Shared checklist consumers](<../../../.pgmcp/template_suite/shared/templates/patterns/markdown/sections.jinja2>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-07 | @imp researcher | Map existing admission, semantic consumption limits and strategy alternatives. |
| 0.2 | 2026-10-07 | @imp researcher | Reconcile historical explicit contracts, pipeline migration and installed V2 evidence; suspend the preliminary strategy recommendation. |
| 0.3 | 2026-10-07 | @imp researcher | Capture human-approved release-assurance boundaries and source audit of all 19 delivered packages and effective nested consumers. |
