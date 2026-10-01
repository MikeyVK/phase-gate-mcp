<!-- docs/development/issue460/design-code-test-artifacts.md -->
<!-- template=design version=5827e841 created=2026-09-11T10:31Z updated= -->
# Code and Test Artifact Contracts

**Status:** DESIGN INTEGRATED — INDEPENDENT CLOSURE RECHECK REQUIRED  
**Version:** 1.2  
**Last Updated:** 2026-09-12  
**Primary package:** DI-03 (code and public test artifacts)  
**Dependencies:** DI-01/DI-02 schema, graph and provenance contracts; approved Research  
**Downstream:** DI-04/DI-05 output validation; DI-06 distribution; DI-07 references; DI-08 assurance

## 1. Purpose and Authority

Design the nine retained code/test families together with [W08](design-document-tracking-artifacts.md).
The human delegated these bounded decisions on 2026-09-11: Research and existing implementation,
not repeated field-by-field workshops, determine the result. Independent QA reviews completeness.
This is a design proposal, not a producer-issued GO.

The human supplied the independent QA verdict on 2026-09-11: no P0–P3 findings and
GO for these concrete template contracts at commit 8b19e0e6ec0aa787854a915e800f837adf3e6067.
This records external review, not producer approval, implementation evidence or whole-Design
completion. The reviewed contract is unchanged; remaining integration stays in §11.

[Research](research.md) owns behavior and strategy; [Findings](research-findings.md) supplies
evidence; [Catalog](template-suite-catalog.md) owns the complete affected-path inventory.
The [README](README.md) owns document form. Temporary W07 notes are superseded by this document.

Completeness means that each retained family, useful existing capability and approved removal has
a destination and a proof obligation. It does not mean copying every future JSON Schema keyword,
Jinja body or test case into Design. Implementation must realize these contracts without choosing
new product behavior. A discovered incompatible requirement must be escalated, not silently omitted.

## 2. Scope and Exclusions

Own caller content, family identities, shared records, rendering semantics, preservation and
migration evidence. Preserve the approved tiered architecture and self-contained packages.

Do not implement templates, JSON schemas, runtime code or tests in this workshop. Do not design
a Python/TypeScript compiler, arbitrary model DSL, example validator, project generator, automatic
test generator, or execution-adapter package generator. The Python boundary-adapter artifact below
is ordinary application code, not an official check/test/fix adapter manifest generator.

No change to Research scope, mutation policy, fingerprint meaning, upgrade strategy or deferred work.

## 3. Binding Inputs

- F-01/F-02/F-03/F-05/F-07: explicit structured content, unchanged presence/value transfer,
  introspectable shapes, one schema authority and no hidden envelope content.
- F-04/F-11/F-17: one selected root, agreed first-line provenance, qualified IDs.
- F-08/F-20: truthful source/preflight evidence, configured checks, no native-language knowledge
  in generic managers. Success is not a claim of application completeness.
- F-14/F-14A/F-14B: portable shared behavior retained; source-project specialization, agent hints
  and unreachable testing patterns removed as cataloged.
- [Example-validation withdrawal](research.md#example-validation-withdrawal--2026-09-11):
  illustrations remain; generated-model execution and semantic example checks do not.
- [DI-01/DI-02](design-suite-resolution.md), especially §7.2.1–§7.2.2, governs schema support and
  RenderInput. Only `content` and separately typed `provenance` reach Jinja.

## 4. Owned Decisions

| ID | Decision | Reason |
|---|---|---|
| D-ART-CODE-01 | Nine qualified retained identities; three approved removals | Preserve useful families, not historical counts or misleading names |
| D-ART-CODE-02 | Shared typed imports, fields and signatures; package-local composition | Reuse actual language constructs without hardcoded server fields |
| D-ART-CODE-03 | Preserve three Python import groups, module imports, from-imports and aliases | Existing capability must not shrink to the earlier illustrative example |
| D-ART-CODE-04 | DTO/config share fields but not immutability or example obligations | Similar syntax does not erase different responsibilities |
| D-ART-CODE-05 | Empty class/protocol skeletons; explicit failing class stubs versus protocol ellipsis | No fabricated behavior |
| D-ART-CODE-06 | Specialized bodies remain caller-authored; native preflight owns syntax evidence | No language parser, dependency inference or behavioral analysis in pgmcp |
| D-ART-CODE-07 | Both pytest families require at least one explicit case; grouping optional | An empty module is not an honest behavior-test scaffold |
| D-ART-CODE-08 | TypeScript class keeps object-style constructor and structured properties | Repair colon parsing without losing constructor behavior |
| D-ART-CODE-09 | Preservation proof uses the real resolved graph | Existing tests of replacement templates or headings alone are insufficient |
| D-ART-CODE-10 | Exact schema serialization and macro bodies are implementation work | Review behavior/contracts once; do not simulate implementation in prose |

## 5. Responsibilities and Boundaries

| Owner | Owns | Must not own |
|---|---|---|
| Package `context.schema.json` | Types, requiredness, finite constraints, descriptions, conditional content relationships | Tool-envelope defaults or package selection |
| Shared definitions | Records reused by actual package consumers | Central registry of every possible language feature |
| Shared Jinja bases/patterns | Literal escaping, syntax framing, imports, fields, signatures, selected fixture/logging structure | Model execution or guessing caller intent |
| Package `template.jinja2` | Family composition and fixed imports for constructs it emits | Sibling-package dependencies or fallback renderers |
| Generic pgmcp | Resolve, validate context, pass it unchanged, render, invoke configured output checks, apply persistence policy | Import classification, annotation parsing, Python identifier lists, field names or example interpretation |
| Native check adapter | Applicable source/preflight evidence under DI-05 | Semantic certification of DTO/config examples |
| DI-08 | Repository conformance harness and regression design | Public generated test-case content |

The suite, not Python code in pgmcp, owns language-specific schemas and rendering. A Python
`type` string and a TypeScript `type` string are deliberately not one server type-expression model.

## 6. Options and Rationale

Reject a full rewrite into independent templates: it discards useful tier reuse. Reject mechanical
relocation: it preserves string/object mismatches, hidden fields and accidental source-project behavior.
Choose shared language syntax plus explicit family contracts, maintaining the existing tier seams.

Reject universal raw source fields: Generic and DTO would cease to be bounded artifacts. Conversely,
do not remove caller code from specialized adapters/workers/tests merely because generic parsing
would be difficult. Their declared source fragments remain native text and are checked as source.

Reject a new all-purpose import or signature engine in pgmcp. Schema/Jinja contracts and native
checks are the existing extensibility route.

## 7. Detailed Design

### 7.1 Family inventory and required nucleus

All fields listed as optional remain absent when omitted. No field named here is a tool-envelope
alias. `class_name`, `description`, `module_description` and file name have distinct consumers:
class declaration, class documentation, optional module documentation, and persistence respectively.
A required description also supplies the module description when no separate module description is
offered; this is explicit template presentation reuse, not injected context or generated wording.

| Current ID / root | Target template_id | Required content | Optional content and rendering |
|---|---|---|---|
| dto / dto.py + hidden dto_v2.py | python_pydantic_dto | class_name, description | module_description, imports, fields, examples; §7.4 |
| schema / config_schema.py | python_pydantic_config | class_name, description, frozen:boolean | module_description, imports, fields, examples; §7.4 |
| generic / generic.py | python_class | class_name, description | module_description, imports, bases:string[], methods:Signature[] |
| interface / interface.py | python_protocol | class_name, description | module_description, imports, bases:string[], methods:Signature[] |
| adapter / adapter.py | python_adapter | class_name, description | module_description, imports, bases:string[], constructor, methods:ConcreteMethod[], logging; §7.6 |
| worker / worker.py | python_worker | class_name, description, operation:ConcreteMethod | module_description, imports, constructor, logging; §7.6 |
| unit_test / test_unit.py | pytest_unit_test | description, cases:TestCase[1..] | imports, fixtures:Fixture[], markers:string[], class_name |
| integration_test / test_integration.py | pytest_integration_test | description, cases:TestCase[1..] | imports, fixtures:Fixture[], markers:string[], class_name |
| typescript_dto / typescript_dto.ts + tier3_pattern_typescript_dto | typescript_dto | class_name, description | module_description, imports, implements:string[], fields:TsField[] |

Root names in the first column are under the current `concrete/` directory and have `.jinja2`
suffixes; they are evidence/navigation, not new package filenames. All targets fit the upstream
24-character ID limit. Resource, Service and Tool artifacts are removed; their runtime classes and
independent previously generated files are not removed. Worker is retained/adapted by Research,
not awaiting another human decision.

### 7.2 Notation, optionality and source domains

In record tables, unmarked fields are required; `?` means optional, not nullable.
`Text` is nonempty text; `Prose` is text permitting the empty string; `Symbol` is an explicit
language identifier; `TypeText` is nonempty native annotation text; `Body` is nonblank native
statement text. Symbols exclude language keywords in the suite-owned language definition.
DottedSymbol is a Symbol or dot-separated Symbol reference, with no call/subscript syntax.
JSONValue is ordinary JSON data; JSONScalar is string, number, boolean or null, never a
container or native expression. Package schemas additionally exclude reserved names at their
insertion position (for example self parameters and a conflicting constructor declaration).
No string trimming, casing, annotation splitting, scalar/list coercion or source execution occurs
in generic code. Python public class names are identifiers, not automatically PascalCased.

All finite records reject unknown properties. Collections allow [] unless explicitly stated otherwise.
Missing optional collection means no supplied component; [] means explicitly empty component.
The template emits only structural framing appropriate to that component, never invented entries.
Missing/empty field collections both allow empty class structure; this does not turn absent context
into an empty list. False/0 survive. Null is admitted only in JSON literal/default/example values.

Schema authors translate these constraints into standard JSON Schema, including required arrays,
closed records, alternatives and conditional relationships. Native `TypeText`, `Body`, marker
expressions and TypeScript import statements are not secretly certified by JSON string validation.
They must be syntactically valid for their insertion position; applicable output checks supply
that evidence. Invalid native input must never yield a claimed valid artifact. Under enforce it is
not persisted; report retains the existing explicit nonblocking validation policy. This is not a
new optional source-check bypass or a claim that JSON Schema can parse either language.

### 7.3 Python imports and documentation

`imports` is a closed object with optional `stdlib`, `third_party`, `project` arrays.
Each element is exactly one alternative:

| Form | Fields | Emits |
|---|---|---|
| Module import | kind:"import", module:Text, alias?:Symbol | import module [as alias] |
| From import | kind:"from", module:Text, names:ImportedName[1..] | from module import name [as alias], ... |
| ImportedName | name:Symbol or "*", alias?:Symbol | One imported symbol; "*" is only allowed alone, without alias |

Module grammar admits dotted names and, for from-import only, relative leading dots. An explicitly
requested wildcard remains expressible; automatic wildcard fallback is removed. No raw multi-statement
injection into these fields. These are declaration records, not instructions
for pgmcp to import modules. Python syntax support lives in suite-owned definitions.

Preserve the three labeled groups and blank separators from the Python base. Classify caller
imports only by the supplied group; do not infer a project path. Fixed imports required by emitted
constructs join the appropriate group once, e.g. Pydantic imports when rendering a model or Protocol
for a protocol. Native decorator references and their imports stay explicitly paired by the caller
(§7.7). A selected concrete root must compose with,
not overwrite, caller imports. Identical complete statements may be emitted once; do not rewrite
different aliases or merge conflicting bindings. Native checks diagnose conflicts.

Sort complete statements within each group to meet existing code style; preserve imported-symbol
order. `from __future__` statements are a declared standard-library special case emitted immediately
after the module docstring, before all ordinary groups. Do not alphabetically move them below imports.
The JSON context remains unchanged; ordering is template formatting.

Shared documentation rendering escapes quote terminators, backslashes and control characters so
caller documentation cannot terminate Python literals or TypeScript comments. Preserve multiline
content. Generic removes architectural-layer/responsibility headers; no unused logger is inserted.

### 7.4 Pydantic fields, defaults and examples

| Record | Fields |
|---|---|
| ModelField | name:Symbol, type:TypeText, description:Text, default?:JSONValue, default_factory?:DottedSymbol, ge?:number, gt?:number, le?:number, lt?:number, min_length?:integer>=0, max_length?:integer>=0, pattern?:Text |

`default` and `default_factory` are mutually exclusive. No default/factory means a required model
field. A supplied default is data: strings are quoted, null becomes None, false becomes False,
arrays/objects become literal containers through shared rendering. Dotted factory symbols are
references, not calls/bodies; caller supplies necessary imports. No typed-ID inference.
Constraint fields are flat and render as corresponding Field arguments. Native model semantics
remain Pydantic's responsibility; there is no unrestricted extra_args, validator or computed-field DSL.

Field order is preserved. Every supplied field has a description. Class identity occurs once.
Both families emit extra="forbid"; DTO always frozen=True and has no caller frozen field.
Configuration requires explicit frozen true/false, without a file loader or import-time I/O.
No fields produces a valid empty model including its model_config and documentation.

`examples` is an array of JSON objects. DTO with at least one field requires at least one example;
otherwise examples is optional. Configuration examples stays optional regardless of fields.
Nonempty examples render as explicit examples metadata; absence or [] when permitted produces no
invented example. For an empty DTO no empty examples metadata is emitted. Shared Python literal
rendering preserves supplied values; neither pgmcp nor an adapter constructs/imports the model to
test examples. No semantic completeness, runtime acceptance or example-validation evidence is claimed.

### 7.5 Signatures, Generic and Protocol

| Record | Fields |
|---|---|
| Signature | name:Symbol, description:Text, async:boolean, parameters:Parameter[], return_type:TypeText |
| Parameter | name:Symbol, type:TypeText, default?:JSONScalar |
| ConcreteMethod | All Signature fields plus body:Body |
| Constructor | parameters:Parameter[], body:Body |

Initial signatures are ordinary instance methods. Template-owned self is not caller data; no
caller parameter named self, arbitrary decorators, positional-only marker language or variadic
signature DSL. Parameters remain ordered; required parameters precede defaulted parameters.
Defaults are JSON scalars, not native expressions or mutable containers. The final rendered syntax
is independently checked. Constructors and dunders are not exposed through Generic signatures.

Generic: optional bases and methods; no methods yields pass; each declared method has documentation
and raises NotImplementedError. Protocol: always derives from Protocol, optional additional explicit
bases, and method bodies are ellipsis; an empty marker protocol is valid. It never fabricates execute.
There is no hidden body, logger or assigning constructor in either package.

The bounded initial method-kind choice is Design-owned under Research. It does not delete shared
specialized constructor/dunder support, which remains available to explicit specialized templates.
More elaborate Generic signatures are normal editing, not a parser hidden in generic pgmcp.

### 7.6 Portable adapter and worker

The adapter's explicit bases/imports express its local contract relationship. Description and
caller method documentation/body carry translation and failure behavior. Do not require a duplicate
boundary-description field without a distinct render consumer. Optional constructor preserves
explicit injection/setup assignments; no dependency name/path/assignment is inferred.

Worker has one explicit operation (name, parameters, result, sync/async and body), plus optional
constructor dependencies. No IWorkerLifecycle, BuildSpec, cache, warmup/shutdown, Translator,
logging enricher or server-manager knowledge is supplied automatically.

Optional `logging` is a closed record `{name?:Text}`, selecting the retained portable module-logger
pattern. When name is supplied it is a quoted literal logger name, never an expression; an explicitly
selected empty record uses the fixed native __name__ expression. Both bind module variable logger
and emit the logging import. Omission emits neither. This retains explicit module-name logging
without a caller expression language. It exists only on these specialized consumers, not
DTO/Generic/Protocol. It must not export
the removed translation/enrichment conventions. Caller bodies may use this explicitly selected logger.

Body indentation is applied at the declared insertion boundary, preserving internal relative
indentation and supplied code. No exception handler, successful return or do-nothing behavior is
invented. Native syntax evidence is required as described in §7.2, not source execution by pgmcp.
ConcreteMethod admits specialized dunder names; Generic's exclusion is package-local, not a ban
inside the shared Symbol definition. A constructor, when supplied, is the sole __init__ declaration.

### 7.7 Pytest families

| Record | Fields |
|---|---|
| TestCase | name:Symbol, description:Text, async:boolean, parameters:Parameter[], body:Body, markers?:Text[] |
| Fixture | name:Symbol, description:Text, async:boolean, parameters:Parameter[], return_type:TypeText, body:Body, decorator:DottedSymbol, scope?:enum(function, class, module, package, session), autouse?:boolean |

Cases require test-prefixed names; optional class_name requires pytest-discoverable class naming.
Cases render functions by default; explicit class_name groups them and adds self. Return annotation
is fixed None for tests. Fixture bodies, dependency parameters and decorator references are explicit,
for example pytest.fixture or pytest_asyncio.fixture with caller-supplied imports. The template
renders that decorator and only the supplied scope/autouse keyword arguments. It does not choose
an async plugin from async=true. If fixture
scope/autouse is absent, omit that decorator argument and leave the native pytest default to pytest.
Case/module markers are caller-supplied native expressions without an @ prefix. Case expressions
render as decorators; module expressions render as the pytestmark list. No inferred asyncio marker.
Async syntax does not itself cause an asyncio import. Caller imports cover every native decorator
and marker reference; the template does not parse those expressions to infer imports or mocks.

Both families require one or more nonblank cases. A body can express Arrange/Act/Assert or another
style; existing three-fragment inputs migrate to this one body without deleting their content.
Do not generate assertions, filesystem operations, manager imports, fixtures, mocks, test class,
TDD statements or passing placeholders. No assertion detector claims a test actually proves behavior.
Integration describes collaboration between concrete components, not automatically E2E/full-stack.

### 7.8 TypeScript DTO

| Record | Fields |
|---|---|
| TsField | name:Symbol, type:TypeText, readonly:boolean, optional:boolean, description?:Prose |

Fields preserve order. Properties are public, readonly only when requested; constructor accepts one
object `data` with the same typed members. Optional affects property and constructor member; readonly
affects the property, not input mutation. Assign required members from data. For optional members,
assign only when the property is present, preserving absence under exact optional-property rules.
Use native TypeScript evidence for this behavior, including strict optional configuration.
No default-to-string, colon splitting, optionality hidden in names, defaults or framework decorators.
Omitted fields or fields=[] intentionally yields an empty exported class with the same object-style
constructor accepting an empty object; it does not silently switch artifact kind or drop its constructor.

Explicit `implements` lists native type references; imports is an ordered array of nonblank native
TypeScript import statements. Keep language-specific import syntax native rather than pretend Python
import records cover ES modules. No fixed src/dtos directory. Remove layer/dependencies/responsibilities
metadata and Unknown/To-be-defined fallbacks as approved specialization removal.

### 7.9 Shared layout and dependency closure

Use the already approved tree; no new tier hierarchy:

- `shared/templates/bases/tier0_root.jinja2`, `tier1_code.jinja2`, `tier2_python.jinja2`,
  `tier2_typescript.jinja2` own framing.
- `shared/templates/patterns/python/` owns used imports, literal/documentation rendering,
  Pydantic fields, signatures and portable opt-in logging.
- `shared/templates/patterns/testing/` owns selected pytest/fixture/test structure.
- `shared/definitions/` owns reused Python import, model-field, parameter and signature records,
  plus TestCase and Fixture shared by both pytest packages. TypeScript-only definitions remain local.
- Each concrete package has manifest.yaml, .version, policy.yaml, context.schema.json and template.jinja2.
  The old TypeScript "pattern" becomes its concrete package content, not a reusable base by name alone.

Each macro receives explicit arguments: caller-owned values covered by the selected schema,
suite-owned syntax/constants, or the separately approved provenance namespace. No arbitrary ambient
context is permitted. Retained specialized base capabilities do not silently become fields on every
package. No cross-concrete-package edge.
Generation closures and upgrade components follow DI-02/DI-06; this document adds no fingerprint rule.

## 8. Control, Data, and State Flow

Caller discovers the selected schema → supplies content and independent file controls → generic
schema validation → unchanged content plus provenance → resolved package/shared Jinja → configured
source checks → existing enforce/report persistence decision.

No generated source is imported/executed to discover content or validate illustrations.
Ordinary test execution remains a separate run_tests consumer. No workflow state is inferred from
a generated test file. The resulting file is independently editable.

## 9. Compatibility, Migration, and Removal

Public V3 clean break: migrate the nine IDs/shapes above without aliases; remove three artifact
registrations and their roots. No requirement to regenerate existing source files. Legacy headers
remain subject to the already-designed selection fallback, not retroactive template ownership.

| Current behavior/evidence | Disposition and owner |
|---|---|
| Python grouped imports in tier2, but concrete overrides ignore caller groups | Preserve groups/forms; repair composition (§7.3); DI-03 |
| Primitive field/method strings, type splitting, dto_v2 override | Replace with structured records/one root; DI-03 + DI-02 |
| dto_name and competing name/class-name inputs | One explicit class_name where a class is rendered; independent operation file_name; no aliases or implicit casing |
| Shared Python init/dunder capabilities and opt-in logging | Preserve reusable specialized support; exclude from Generic as Research requires |
| Worker lifecycle/cache/Translator and typed-ID pattern | Remove portable-suite dependencies; historical specialization remains deferred/cataloged |
| Unit/integration AAA fragments, fixtures, markers, class/async support | Preserve expressible behavior under §7.7; remove automatic scaffolding guesses |
| TypeScript constructor/imports/implements | Preserve via real package (§7.8), not a test-owned copied renderer |
| Agent hints, unreachable assertions/fixtures, YAML branch, removed Resource/Service/Tool | Apply exact catalog dispositions; DI-03 content, DI-07 references, DI-08 tests |
| Legacy registry counts and active examples | Update intentionally; 19 retained total is this migration's census, not a future hardcoded server limit |

## 10. Test and Validation Design

Planning allocates these obligations to bounded cycles; DI-08 supplies reusable test support and audits coverage, not cycle ownership. This is not a new production fixture registry.

| Evidence ID | Required independent observable proof |
|---|---|
| CODE-E01 | All nine actual package roots: minimal accepted content, every optional capability exercised, schema reject cases; no copied replacement templates |
| CODE-E02 | Ordinary/from imports, aliases, all three groups, future placement, fixed+caller composition; assert actual statements, not just headings |
| CODE-E03 | DTO/config empty and populated models, described fields, defaults false/0/null/quoted strings/containers, factory exclusivity, immutability difference |
| CODE-E04 | DTO conditional example presence; config optionality; no generated-model execution or semantic example validation path |
| CODE-E05 | Class pass, failing method stub, protocol ellipsis/empty marker; parameters/annotations/defaults and no fabricated behavior |
| CODE-E06 | Adapter/worker explicit bodies/dependencies and opt-in logging; no source-project imports/lifecycle scaffolding |
| CODE-E07 | Function/class tests, fixtures, markers, sync/async, at least one case, no fake pass/TDD/import inference |
| CODE-E08 | Real TypeScript graph: object/function types containing colons, readonly/optional, constructor assignments, imports and implements |
| CODE-E09 | Omitted/empty/false/0/null boundaries, unknown properties, native syntax failure vs context failure, unavailable-check honesty, enforce/report |
| CODE-E10 | Shared graph closure, header reader/writer agreement, retained/removal inventory and active references; DI-02/DI-04/DI-07 integration |

Existing seams: [concrete tests](../../../tests/mcp_server/integration/test_concrete_templates.py),
[Pydantic pattern tests](../../../tests/mcp_server/scaffolding/test_tier3_pattern_python_pydantic.py),
[TypeScript scaffold test](../../../tests/mcp_server/unit/managers/test_typescript_dto_scaffold.py),
[tier2 tests](../../../tests/mcp_server/test_tier2_templates.py).
Their current token/prose/legacy assumptions are evidence to assess, not automatic acceptance criteria.
Preserve valuable behavioral tests; consolidate obsolete implementation-shaped tests under the catalog.

Schema-root example conformance is separate from forbidden semantic model-example validation.
No need to run a generated application/test suite merely to scaffold it.

## 11. Integration Risks and Open Questions

No family product decision is left to another human workshop. Remaining implementation/integration
proof is not presumed complete: escaping, native syntax handling, selected profile bindings and
finite shared-schema closure must be demonstrated. W09/DI-05 owns exact profile/binding names and
native preflight support; it may not silently omit a language or reinstate example validation.
If the existing generic schema vocabulary cannot express a required constraint, escalate to DI-01;
do not insert a package-specific branch into pgmcp.

Known limitations are explicit: bounded signatures are not the full language, source fragments need
native syntax evidence, and a scaffold is not a correct implementation. None justifies dropping the
preserved capabilities above.

## 12. Planning Consequences

Separate shared syntax/definition work from family migrations and cross-family conformance. Each
cycle names its packages, shared write-set, preserved behavior, rollback point and evidence IDs.
Shared changes rerun affected consumer proof. No "remaining templates/tests" catch-all cycle.
Adapter check/test/fix migration and F-10 renewal remain separately owned; this document does not
schedule them or grant cutover before independent evidence exists.

## 13. Traceability Matrix

| Research / source | Contract destination | Proof |
|---|---|---|
| F-01/02/03/05/07 | §7.1–§7.9; shared/leaf ownership | CODE-E01/02/09 |
| F-04; DTO approved responsibility | §7.4, §9 | CODE-E03/04/10 |
| Config-model responsibility | §7.4 | CODE-E03/04 |
| Generic/Protocol/adapter responsibilities | §7.5–§7.6 | CODE-E05/06 |
| Unit/integration responsibilities | §7.7 | CODE-E07 |
| TypeScript responsibility / F-17 | §7.8 and identity table | CODE-E08/10 |
| F-08/F-20 | §7.2, §8, DI-05 integration | CODE-E09 |
| F-14/A/B; catalog shared patterns | §7.6/7.9, §9 | CODE-E06/07/10 |
| F-11; file-ownership amendment | Upstream DI-02/DI-06, §7.9 | CODE-E10 |
| 2026-09-11 example withdrawal | §7.4 and §10 | CODE-E04 |

## 14. Related Documentation and Version History

- [Document/tracking companion](design-document-tracking-artifacts.md)
- [Suite resolution](design-suite-resolution.md), [Execution adapters](design-execution-adapters.md),
  [Mutation validation](design-mutation-validation.md), [Distribution](design-distribution.md)
- [Research findings](research-findings.md), [Catalog](template-suite-catalog.md),
  [Design intake](design-intake-map.md), [Deferred work](deferred-work.md)
- Source graph: [Python base](../../../.pgmcp/templates/tier2_base_python.jinja2),
  [TypeScript base](../../../.pgmcp/templates/tier2_base_typescript.jinja2),
  [DTO](../../../.pgmcp/templates/concrete/dto.py.jinja2),
  [Generic](../../../.pgmcp/templates/concrete/generic.py.jinja2),
  [Worker](../../../.pgmcp/templates/concrete/worker.py.jinja2),
  [Code style](../../coding_standards/CODE_STYLE.md).

| Version | Date | Change |
|---|---|---|
| 1.2 | 2026-09-12 | Reconcile canonical dependencies, closure status and proof ownership after independent QA; technical contracts unchanged, independent closure recheck required. |
| 1.1 | 2026-09-11 | Record human-supplied independent bounded QA GO; contract unchanged and integration remains open. |
| 1.0 | 2026-09-11 | Consolidate delegated W07 with source-based preservation, shared records, family contracts and independent proof obligations. |
