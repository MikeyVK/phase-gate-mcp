<!-- pgmcp:v1 id=research pv=1.0.0 pf=lgBwxWMfTAmNNg_O sf=5--KpGf2wHUv2qAj -->

# Issue 476 — Schema-to-template consumption research

**Status:** DRAFT — boundary strategy pending human approval  
**Version:** 0.1  
**Last Updated:** 2026-10-07

## Purpose

Establish what reverse schema/template analysis can reliably claim before changing package admission. This is Research, not an approved analyzer design or implementation sequence.

## Scope In

Prepared context schemas, the admitted Jinja graph, caller content and reachable render consumers; current package fixtures, authoring and startup/renewal admission boundaries.

## Scope Out

Production changes, a new public MCP tool, compatibility bridges, template-ID/field-name exceptions, whole-suite semantic completeness claims, package repairs without a demonstrated defect, and new regression tests for existing behavior.

## Problem Statement

Template admission rejects undeclared static Jinja reads but does not prove that every admitted caller field influences the artifact. No shipped silently ignored field has been demonstrated by this investigation. D-VAL-08 explicitly deferred both the mechanism and enforcement decision from #460.

## Goals

- Define consumption beyond a syntactic reference.
- Identify schema/Jinja constructs that can be resolved generically and cases that must remain uncertain.
- Compare authoring diagnostics, behavior-supported conformance and startup rejection with explicit consumer impact.
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

### Strategy alternatives — decision still open

| Strategy | Consumer / compatibility impact | Cost, risk and limitation |
| --- | --- | --- |
| A. Bounded authoring diagnostics plus existing behavior evidence — recommended | Preserve public schemas, rendering, current admission and renewal acceptance; new consumption reports do not reject startup | Moderate bounded analysis; explicit uncertainty prevents availability failures. Exact integration and diagnostic contract belong to Design |
| B. Test-supported package conformance only | Preserve admission; rely on package-owner behavior cases and reviewed traces | Lowest runtime impact; per-package effort grows with fields/branches and misses future drift without an automatic signal |
| C. Reverse startup rejection | Changes which otherwise admitted suites can start or activate | Highest blast radius; must first establish sound rejection rules and actual analyzer false-positive evidence. Uncertainty cannot silently become rejection |

No strategy is approved by opening this issue or by earlier approvals for #460/#472. Under A, do not duplicate consumption annotations in manifests or schemas merely to silence unresolved analysis. No particular analyzer API, integration command, schema extension or implementation cycle is selected here.

## Questions

- Human decision: A authoring diagnostics, B behavior-supported conformance only, or C startup rejection?
- Design-dependent: which constructs can support trustworthy output dependencies, and what is the bounded stopping rule for unresolved calls/dynamic access?
- No actual analyzer exists yet: how will its findings be compared with reviewed semantic witnesses without creating per-field test or annotation maintenance ballast?

## References

- [D-VAL-08 original deferred boundary](<../issue460/deferred-work.md#d-val-08--generic-schematemplate-consumption-analysis>)
- [Jinja Meta API](<https://jinja.palletsprojects.com/en/stable/api/#the-meta-api>)
- [Jinja import/include context rules](<https://jinja.palletsprojects.com/en/stable/templates/#import-context-behavior>)
- [JSON Schema 2020-12 applicator semantics](<https://json-schema.org/draft/2020-12/json-schema-core#section-10>)

## Approved Strategy

PENDING human decision. Proposed per-boundary policy under A: (1) preserve public caller schemas and artifact rendering without compatibility aliases or migration; (2) preserve existing admission/renewal rejection rules without reverse startup blocking; (3) add bounded generic consumption diagnostics whose absence/uncertainty are findings, not proof of a defect; (4) reuse existing behavioral evidence and add only bounded tests for genuinely new analysis behavior if implemented. Do not advance to Design or ask independent QA to authorize progression until the human decision is captured.

## Expected Results

Research closes when a human strategy is explicit for the four boundaries above and independent QA assesses the evidence. Any later mechanism must distinguish observed, absent and uncertain use; identify affected instance paths and source locations; retain schema compositions and Jinja scope/call context; avoid blanket child consumption; preserve undeclared-read rejection; and separate actual package defects from analysis limitations. No shipped silently ignored field is currently established. The 79 naive candidates are source-accounted, not a complete conformance pass. Actual AST-analyzer false-positive measurements remain unavailable until a bounded mechanism exists.

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

## Consumers

### Package authors and maintainers

Keep exposed schema fields and render behavior coherent

**Impact:** Need path- and source-based diagnostics with uncertainty; no hardcoded package vocabulary.

### Agents using scaffold\_schema/scaffold\_artifact

Supply admitted context and inspect generated output

**Impact:** Existing input/output contracts and absence/empty semantics should remain stable under the recommended strategy.

### Server startup and template renewal

Admit one coherent suite snapshot

**Impact:** Reverse blocking would reject the complete suite and affect serving, upgrades and owner-specialized packages.

### Tests and package distribution

Observe actual supplied package behavior through opaque-location fixtures

**Impact:** Reuse valuable cases; any future new coverage should prove analysis behavior rather than entire payload text or old behavior again.

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
