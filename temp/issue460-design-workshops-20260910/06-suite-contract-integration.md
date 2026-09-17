<!-- C:\temp\pgmcp\temp\issue460-design-workshops-20260910\06-suite-contract-integration.md -->
<!-- template=design version=5827e841 created=2026-09-10T09:24Z updated= -->
# W06 — Close the seams between suite, profile and public schema

**Status:** W06 schema closeout human-approved and consolidated 2026-09-12; implementation/client conformance and combined QA remain open  
**Owners:** DI-01/DI-02 and Shared Contracts; DI-05 owns bindings, DI-04 owns mutation  
**Dependencies:** W03 profile contract; W07/W08 concrete schemas  
**Decision nucleus:** One admitted suite view, unchanged caller context and one startup tool contract.

## 1. Purpose and authority

The template contract is largely decided. This workshop closes remaining interface and delivery gaps; it does not revisit template_suite/, Jinja tiers, the manifest/.version/policy.yaml split, ID/version bounds, fingerprints or first-line metadata.

## 2. Scope and exclusions

Resolved schema dialect, unchanged-context semantics, graph/read interfaces, startup input validation and embedded-schema identity. No runtime discovery tool, watcher, recursive schema promise, second registry, extra metadata field or header serialization implementation.

## 3. Binding inputs

[Suite Design](C:/temp/pgmcp/docs/development/issue460/design-suite-resolution.md), [Shared Contracts](C:/temp/pgmcp/docs/development/issue460/design-shared-contracts.md), F-01–F-06/F-11/F-16/F-17, I-1–I-6 and current DI-05 configuration decisions. W06-B forbids generic default insertion; caller context stays unchanged. [JSON Schema annotations](https://json-schema.org/understanding-json-schema/reference/annotations).

## 4. Proposed decisions

| ID | Proposal |
|---|---|
| W06-A | Approved: JSON Schema 2020-12 with bounded local acyclic references; canonical DI-01/02 §7.2.3 |
| W06-B | Human-approved: preserve present/empty/absent context and typed values; canonical DI-01/DI-02 §7.2.1 |
| W06-C | Superseded: exclude whole .version/policy.yaml and all external validation config from pf/sf; full operational component comparison includes all package files |
| W06-D | A single constructed tool-input contract supplies exposure, validation and input-error feedback |
| W06-E | Approved: schema://template/<encoded-template-id>/context without pf for retrieval/context errors; preserve schema://validation; canonical Shared §7.6 |

## 5. Responsibilities and boundaries

SuiteLoader owns I/O and declarations; GraphResolver owns parser-supported static edges; ContextContract owns validation and declared omission behavior; ResolvedSuiteCatalog supplies read-only views. Consumer managers cannot re-open package files.

Proposed signatures:

```python
class TemplateSchemaReader(Protocol):
    def schema(self, template_id: TemplateId) -> ResolvedSchemaView: ...

class TemplateRenderer(Protocol):
    def render(self, template_id: TemplateId, content: ValidatedContext,
               provenance: ArtifactProvenance) -> RenderedText: ...

class TemplateProfileReader(Protocol):
    def profile(self, template_id: TemplateId) -> ResolvedProfile: ...
```

ValidatedContext preserves supplied keys and values after validation, with no default insertion. It is not a dynamic Python class per template. Pure context validation performs no filesystem I/O. Immutable wrapping preserves JSON meaning.

## 6. Options and rationale

Naive ref dictionary merging can discard constraints. Arbitrary dynamic Jinja references make startup identity incomplete. Per-access dynamic schemas let decorators and execution disagree. Reject all three. Preserve standard syntax and make admission limitations explicit rather than promising every possible schema/Jinja program.

## 7. Detailed design

### Schema and graph admission

Root contexts are closed objects with finite fields. Standard local properties, arrays, definitions and combinators remain available. Resolve local JSON Pointers and admitted shared definition identities only; no HTTP fetch at startup, recursion or dynamic references. Preserve ref siblings and their constraints instead of overwriting either object. Validate equivalence through authored-versus-exposed representative cases, including additional/unevaluated-property interactions; do not claim arbitrary ref removal is automatically semantics-preserving. [JSON Schema 2020-12 reference semantics](https://json-schema.org/draft/2020-12/json-schema-core).

Use Jinja AST parsing for extends/include/import/from-import, including trim syntax and single/double quotes. Only statically enumerable targets are admitted; reject an unresolved dynamic target. Import/include context behavior is part of the edge. For a constant fallback include list, resolve the actual deterministic choice and include its selection semantics; never silently choose a different file during runtime. Forbidden package-to-package/shared-to-package edges and cycles fail admission.

Top-level undeclared renderer inputs must be declared content or the separate provenance input. AST analysis is not proof of nested field typing or of all rich contexts rendering; DI-03 schema/renderer conformance supplies that evidence. No authored contributors list or inference of JSON types from dotted Jinja access.

Store admitted sources/compiled environment and schemas in the immutable startup view so later file edits do not change an already running renderer.

### Omission/default contract — human-approved, canonical §7.2.1

Validate caller content without adding, removing or coercing properties. Pass the
validated values unchanged to rendering; immutable wrapping must preserve JSON meaning.

| Caller state | Contract behavior |
|---|---|
| Required property absent | Context validation error; do not render |
| Optional property absent | Remains absent; template explicitly handles omission |
| Explicit null | Accepted only if schema permits null; remains null |
| Explicit false, zero, empty string/list/object | Validate declared constraints; retain supplied value |
| Unknown property in a closed object | Reject, never silently filter |
| Schema default annotation | Never inserted by generic PGMCP; no second context-materialization pass |

The former automatic-default proposal is withdrawn. No synthetic null, absent parent
object, recursively inserted default, envelope-to-context injection or default ledger.
Template-authored omission behavior must be explained in the relevant schema description.
A template may omit an optional section; required output data must instead be required
caller input. Do not solve unsafe optional iteration with generic null/empty injection.

If valid omitted input makes a template crash, report the rendering failure through the
existing route; it is a package contract/rendering defect, not a missing caller obligation.
Concrete DI-03 conformance must cover omission, allowed null and allowed empty values.
There is no universal static proof of every Jinja path and no startup render-everything test.

Consumer ownership: DI-01 validates unchanged JSON; DI-02 supplies the admitted renderer;
DI-03 owns optional-field rendering and package conformance; DI-04 persists only after
existing rendering/check/persistence conditions. Safe edit selects output checks; it does
not reconstruct a template context or gain context defaults. Binding default_args remain
a separate, already approved invocation policy and are not changed here.

### Generation identity — superseding human decision

The [Research amendment](C:/temp/pgmcp/docs/development/issue460/research.md#generation-identity-and-package-file-ownership-amendment--2026-09-10)
owns the current decision: manifest.yaml contains template_id/purpose; .version contains
the package release label; policy.yaml contains output_profile/persistence. Exclude the
whole version/policy files and external validation settings from both pf and sf. No
profile/binding projection remains. Operational upgrade fingerprints include all files.
Included generation-source comments/descriptions count. Independent Research QA GO was
reported by the human; W06-B subsequently rejected automatic context defaults.
### Startup-built input contract

Introduce an inward-owned immutable EffectiveInputContract[TInput] exposing schema, validate(raw)->TInput, and structured validation issues. Construct once after catalog/config resolution. Tool instances, InputValidationDecorator and error-schema feedback use this same value; no override-only core schema that decorators replace with args_model output.

Preserve static tool contracts for unaffected tools through the same existing mechanism; do not create a parallel authored tool catalog. Derived supported output contracts remain unchanged for presentation. Per-instance schema objects must be immutable or protected copies; no mutable class state.

W03 selector enums and W04's approved tests enum/args-recipient properties come from that resolved view. W04 no longer uses per-suite native option alternatives: all configured recipients are visible together, each accepting a string array. Template selectors keep complete IDs. The existing **50-template escalation threshold** is a Design follow-up trigger, not a runtime cap/truncation policy; larger catalogs require separately scoped discovery work, not silently removed options in issue460.

### Schema attachments

Approved: use schema://template/<encoded-template-id>/context for both successful
scaffold_schema retrieval and selected-template context rejection.
Retain schema://validation for existing whole-tool input errors outside this selected
context route. Schema attachments use application/schema+json. No machine path, new
fingerprint or resource-reader fetch guarantee is implied; section 15 supplies the audit.

Schema retrieval cache includes the schema as its primary result. Scaffold context error attaches the exact schema separately and caches only operation issues. Scaffold success and output/persistence failure carry no schema. ResponseComposition has exactly operation DTO plus zero-or-more structured attachments; it is not an alternative error taxonomy.

## 8. Flow and counterexamples

Package A generation edit → B pf/schema unchanged, sf may change. Profile/binding or
policy/.version changes → pf/sf unchanged; policy/.version still affect operational
package comparison. Included comments/descriptions change generation identity. Schema
queried without restart still uses the admitted startup view, not partial reload.

## 9. Migration and removal

Remove DynamicModelFactory optional-None behavior, legacy YAML caller schemas, implicit DTO override, regex graph inference and template_registry. Keep no aliases. Normalize stale “manifest id” and “gate-set” wording in canonical docs only after approval, without changing the manifest's template_id field.

## 10. Evidence

Schema reference sibling/constraint preservation; finite cycles rejected; default/null/false/zero distinctions; caller unknown fields not dropped; actual compiled source snapshot stability; dependency isolation; policy/version exclusion from generation identity; real decorators and delayed listing; schema attachment equality; URI path-safety and current schema://validation consumer tests.

## 11. Review points

Human approval 2026-09-11 covers the consumer-facing shared-source contract, now canonical
in DI-01/DI-02 section 7.2.2: two input boundaries, complete shared definitions, identical
exposure/validation/error rules and unchanged caller values. Section 15's exact resolver
support and URI mechanics remain technical proposals, not independently approved details.

Automatic default materialization and profile fingerprint projection are withdrawn.
The canonical omission/value contract is approved in DI-01/DI-02 §7.2.1. Remaining
schema resolution, exposure/validation wiring and URI choices require review. No claim
of hosted-client refresh behavior without separate evidence.

## 12. Planning consequences

Shared schema/contract holder, suite resolution and consumer wiring are separable deliverables. No implementation methods or cycle sequence here.

## 13. Traceability

D-SHARED-10; Q-ADAPTER-08/09; DI-01 schema/default obligations; DI-02 graph/provenance; DI-04 selected-context delivery; XC-01 no repeated authority.

## 14. Related documentation and history

Next: [W07 code/test artifacts](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/07-code-test-artifacts.md) and [W08 document/tracking](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/08-document-tracking-artifacts.md).  
0.1, 2026-09-10: temporary proposal.

## 15. Remaining schema integration — concrete proposal, 2026-09-11

### A. Standard and bounded reference resolution

Select JSON Schema 2020-12 explicitly for authored template context contracts. The MCP
2025-11-25 tools specification also uses 2020-12 by default; this does not certify any
particular client's rendering of all keywords. Keep the approved finite local acyclic
graph, with no network retrieval or recursive/dynamic-reference promise.

Flattening means removing indirection, not flattening the caller's nested data. Preserve
complete referenced constraints and descriptions. Never overwrite a constraint merely
because it shares a keyword with a referenced schema. Illustrative counterexample:
a shared string schema requires minLength=5 and a referencing use adds minLength=2;
both apply, so two-character input remains invalid. The current merge helper can lose
the stronger condition. Do not replace it with a universal dictionary-merge recipe.

Use one prepared resolved context schema for context validation, scaffold_schema and
context-error attachments. Resolution must preserve authored validation semantics within
the admitted schema subset; authored-versus-resolved conformance covers relevant nested
and combined constraints. Unsupported constructs fail schema preparation explicitly,
not a permissive fallback, silent constraint removal or caller-data normalization.
No general runtime theorem-prover for arbitrary schema equivalence is proposed.
JSON number/integer and format behavior require alignment with the selected validator;
do not let a second Pydantic reconstruction silently impose different context semantics.
Exact supported keyword/format combinations require the concrete DI-03 cases before
claiming complete conformance.

### B. Two distinct input boundaries, no duplicated authority

| Boundary | Authority | Consumer |
|---|---|---|
| Tool call envelope (selection, scope, targets, args, validation mode) | The existing typed input contract, enriched once with admitted catalog/config choices | Registered inputSchema, wrapper validation and whole-tool input-error schema |
| Selected template context | The prepared schema derived from context.schema.json and admitted shared definitions | Scaffold context validation, scaffold_schema result and context-error attachment |

Do not insert every template's full context into scaffold_artifact's inputSchema.
The approved scaffold_schema discovery route remains; selected context is validated
after resolving the template ID. Caller JSON keys/values pass unchanged to rendering.

Replace the wrapper's independent args_model schema reconstruction with consumption
of the tool's startup-bound input contract. The same contract owns constraints and
typed conversion, including selected-ID admission, without two independently authored
validators. Ordinary static tools retain their current typed definitions. Dynamic
selection errors stay with the already designed consumer error semantics; schema
construction is not permission to redesign success/isError or presentation.

An immutable catalog snapshot supplies all derived enums and args recipient properties.
Delayed/lazy listing reads that snapshot; it does not rebuild choices from edited files.
A client may retain stale schema metadata: the server still validates against its own
active contract and never executes an unknown selection. No live reload, forced client
refresh, startup dependency probing or health expansion is added.

### C. Schema identity and delivery

Human-approved identity: schema://template/<encoded-template-id>/context.
Use it on scaffold_schema success and scaffold context failure. It identifies the
active catalog contract, not an immutable historical version. The fingerprint-bearing
proposal is withdrawn; same URI can carry changed content after a catalog-changing
restart. The embedded response content is authoritative, not a URI-only historical cache.

The schema is embedded, not fetched by following that URI. Existing operation cache
IDs continue to identify each tool invocation. No URI becomes an absolute filesystem
path, historical retention promise, endpoint or extra public tool. Existing generic
whole-tool input-error schema://validation remains a distinct unaffected route.

Preserve the approved presentation split: schema retrieval caches its primary schema
result; scaffold context failure caches issues and separately attaches the complete
selected schema; scaffold success/render/check/persistence failures do not attach one.
Attachment/cache schema content must be structurally equal to the prepared catalog view.
Resource composition owns URI/MIME/serialization; managers own typed facts, and the
presenter must not acquire template- or error-DTO-specific dispatch knowledge.

### Direct seams and required evidence

| Observed seam | Required integration/proof |
|---|---|
| mcp_server/tools/scaffold_schema_tool.py input_schema adds a registry enum | Verify the real decorated/listed tool retains the admitted enum, not only the core property |
| mcp_server/core/decorators/input_validation_decorator.py reconstructs model schema for exposure/errors and uses model_validate | One effective contract for listing, validation and error feedback; no coercion/default insertion into template context |
| mcp_server/utils/schema_utils.py resolves only final definition names, missing definitions as empty objects and overwrites siblings | Replace unsafe behavior for admitted template schemas; prove proper identity/pointer resolution, missing-ref rejection and sibling constraints |
| mcp_server/presenters/validation_resource_presenter.py emits schema://validation with application/json | Preserve unrelated tool error routing; selected context attachment uses shared composition and explicit schema media type |
| tests/mcp_server/integration/test_strict_input_validation_response.py asserts schema://validation | Keep the whole-tool error contract; add selected-context attachment identity/equality assertions without a broad legacy-error rewrite |
| tests/mcp_server/unit/tools/test_scaffold_schema_tool.py inspects the core schema | Retain useful tests and add registered-wrapper and snapshot/restart evidence |

No runtime tests or production edits were performed for this proposal. No client-specific
lazy exposure compatibility is claimed from a specification alone. After human agreement,
consolidate A/D/E into DI-01/DI-02 and Shared Contracts. W07/W08 subsequently received
independent QA GO; preserve those contracts and add resolver-specific conformance
obligations rather than reopening the concrete fields. Full W06 conformance is not proven.

Primary references:
- [MCP tools specification](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)
- [JSON Schema 2020-12 core, reference-removal caveat B.2](https://json-schema.org/draft/2020-12/json-schema-core#appendix-B.2)

## 16. Schema closeout — human-approved 2026-09-12

Consolidated in canonical DI-01/02 §7.2.3 and Shared §7.6. Research stays frozen.
W07/W08 concrete field contracts remain independently reviewed inputs, not new decisions.

### 16.1 Identity and delivery

Use `schema://template/<encoded-template-id>/context` for the selected context
attachment. Percent-encode manifest template_id as one URI path segment. No pf, version
or run ID: no demonstrated consumer requires immutable URI identity, and pf also changes
on template-only edits. The same URI can contain a new schema after a catalog-changing
restart. Use the response's embedded content; retain existing operation DTO provenance.

Both scaffold_schema success and selected-context rejection use that same URI and
`application/schema+json`. The complete schema is embedded in the response; the agent
does not need to fetch it. This identifier adds no resources/read endpoint, retention
guarantee or filesystem location. Per-invocation cached results retain their existing
run URIs. Preserve `schema://validation` for the whole-tool input-error boundary.
No schema is attached to a successful scaffold or unrelated downstream failure.

### 16.2 Dialect and validation behavior

Require `"$schema": "https://json-schema.org/draft/2020-12/schema"` on authored schema
documents. Do not infer a dialect from a library default or silently accept another
draft. Use a standards-compliant validator, not a PGMCP implementation of validation
keywords or a generated template-specific Pydantic model. The selected library must
be an explicit runtime dependency, not an accidental transitive dependency.

| Standard constructs | Contract |
|---|---|
| Types, enum/const, numeric bounds/multipleOf, string length/pattern | Standard 2020-12 assertions; no type coercion |
| properties, required, additionalProperties, patternProperties, propertyNames, property counts | Standard object assertions/applicators; concrete DI-03 records remain closed |
| items, prefixItems, contains/minContains/maxContains, uniqueItems, item counts | Standard array assertions/applicators |
| allOf, anyOf, oneOf, not, if/then/else, dependentRequired/dependentSchemas | Standard combined/conditional constraints, not PGMCP business rules |
| unevaluatedProperties/unevaluatedItems | Preserve their standard evaluated-member semantics across reference resolution; never approximate with additionalProperties/items |
| Boolean subschemas | Standard accept/reject meaning; do not mistake false for an absent schema |
| title, description, $comment, examples, default, deprecated, readOnly/writeOnly | Metadata, not data insertion, example execution or mutation authority |
| format | Standard annotation-only behavior; no hidden FormatChecker or custom template-specific formats |
| contentEncoding/contentMediaType/contentSchema | No decoding or embedded-content validation promise |

An unknown extension keyword supplies no executable constraint under this dialect.
Do not imply arbitrary custom vocabularies are supported. Schema shape checks cannot
prove that an author's intended constraint was expressed; conformance examples remain
necessary. Numeric integer semantics follow JSON Schema (an integral JSON number can
qualify as integer); validation does not rewrite the caller's value or representation.

For example, `format: "date"` alone does not reject `"tomorrow"`. An actual acceptance
condition must be expressed as a supported assertion; a regular expression can constrain
date spelling but is not a full calendar validator. Do not invent such a validator in
generic PGMCP. The reviewed DI-03 Link contract uses explicit nonempty text and does
not silently acquire URI, filesystem-existence or anchor validation here.

### 16.3 Reference admission and faithful exposure

Allow static `$ref` references to the current document, package-local schema documents
and admitted shared/definitions documents. Allow a whole-document reference or a JSON
Pointer fragment such as `#/$defs/Link`. Resolve relative to the referring document,
not the server working directory. Enforce the existing dependency direction and resolved
filesystem containment; no escape through traversal or symlinks, cross-package reference,
shared-to-package reference, absolute file reference or network fetch.

For this package format, do not admit authored `$id` rebasing, named `$anchor` fragments,
`$dynamicRef`/`$dynamicAnchor`, dialect changes in subschemas or custom `$vocabulary`.
Document location plus JSON Pointer is sufficient for the approved shared definitions;
the derived embedded URI already supplies the public resource identity. These are explicit
authoring restrictions, not claims that the JSON Schema standard lacks those features.

Reject unresolved pointers and cyclic reference chains during schema preparation.
Finite nested records/arrays remain supported; an arbitrarily self-referential schema
cannot satisfy the approved finite reference-free exposure promise. No truncation or
empty-schema replacement is permitted. Traversal distinguishes schema positions from
literal JSON data: a property name or example containing `$ref` is not itself an edge.

Resolve once into the immutable catalog view, retaining complete referenced constraints
and useful descriptions. Validate context and supply both schema response paths from
that same view. Referenced and adjacent constraints both apply; do not merge dictionaries
by overwriting keys. A referenced minLength=5 plus adjacent minLength=2 still rejects a
two-character value. Preserve combinators and unevaluated-member behavior rather than
flattening caller object structure or simplifying assertions. No generic runtime schema
equivalence prover or silent fallback to a weaker representation is introduced.

### 16.4 Evidence and integration ownership

- DI-01/02: selected dialect/schema checks, contained pointer resolution, forbidden forms,
  cycles/missing targets, ref siblings, combinations with existing allOf and unevaluated
  constraints, boolean schemas and literal data containing schema-looking keys.
- DI-03: preserve approved required/optional/null/empty/false/zero/unknown-field cases;
  compare authored and resolved acceptance without recreating a second field authority.
- Shared/DI-04: retrieval and context-error attachments have identical URI/content for
  the same admitted package; catalog changes may change content without changing URI; ordinary
  whole-tool errors retain schema://validation; successful scaffold has no schema.
- Registration integration: the real wrapper and delayed listing consume one prepared
  contract; no separate Pydantic reconstruction may weaken the exposed selection rules.

No production changes, tests, client compatibility proof or phase transition are claimed.
Canonical owners now contain the approved contract; next closeout is the exact tests.yaml
and test request/result DTO graph, without reopening approved run_tests behavior.

Primary sources: [JSON Schema core](https://json-schema.org/draft/2020-12/json-schema-core),
[validation and annotation semantics](https://json-schema.org/draft/2020-12/json-schema-validation),
[MCP embedded resources](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#embedded-resources).
