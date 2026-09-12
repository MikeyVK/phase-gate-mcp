<!-- docs\development\issue460\design-shared-contracts.md -->
<!-- template=design version=5827e841 created=2026-08-27T12:05Z updated=2026-08-27 -->
# Issue 460 Shared Tool and Schema Contracts Design

**Status:** DRAFT  
**Version:** 1.8  
**Last Updated:** 2026-09-12  
**Primary Package:** Shared contracts consumed by DI-01, DI-02, and DI-04  
**Upstream Dependencies:** Issue 456 presentation contract, DI-01/DI-02 resolved catalog  
**Downstream Consumers:** `scaffold_schema`, `scaffold_artifact`, cache publication,
response presentation, DI-07 documentation  
**Lifecycle Status:** Drafting

---

## 1. Purpose and Authority

This document owns the exact cross-package delivery contract for resolved artifact
schemas. It distinguishes:

- concise human/agent-facing text;
- the complete cached operation DTO;
- structured embedded MCP resource attachments.

The [Suite Resolution Design](design-suite-resolution.md) owns schema content,
resolution, artifact identity, purpose, package version, resolved package fingerprint,
and persisted source suite fingerprint.
[Mutation and Persistence Design](design-mutation-validation.md) owns scaffold
validation policy and mutation mechanics; [Execution Adapter Design](design-execution-adapters.md)
owns DI-05 check/test/fix execution and its role-specific evidence. This document owns
only the schema-delivery semantics shared by the template and mutation packages.

## 2. Scope and Exclusions

### In Scope

- successful `scaffold_schema` output;
- successful `scaffold_artifact` output with respect to context schemas;
- artifact-context validation failure output;
- ownership and duplication rules for text, cache DTOs, and embedded resources;
- the structured application/presentation seam required to keep failure attachments out
  of cached operation DTOs.

### Out of Scope

- exact prose wording in `presentation.yaml`;
- outer MCP argument-schema validation performed before an artifact is selected;
- render, output-profile, persistence, or filesystem failure payloads;
- mutation atomicity, rollback, and strictness;
- schema resolution algorithms;
- unrelated tools and validation resources.

## 3. Binding Inputs

- [Issue 456 Design](../issue456/design.md).
- [Issue 456 Tool Presentation Field Audit](../issue456/tool-presentation-field-audit.md).
- [Presentation Architecture](../../reference/presentation_architecture.md).
- [Suite Resolution Design](design-suite-resolution.md).
- [Research](research.md): F-01, F-03, F-04, F-05, F-09, F-11, F-16, and Approved
  Strategy.
- [Design Intake Map](design-intake-map.md): DI-01, DI-02, DI-04, DI-07, XC-01, and
  RC-01.
- [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md):
  presentation separation, SRP, CQS, DIP, ISP, DRY, and YAGNI.
- [Pre-Implementation Documentation Contract](README.md).

Issue 456 remains binding: frozen tool-output DTOs own operation facts, cached resources
provide the complete operation record, and text is a bounded actionable projection.
This document clarifies that an embedded resource attachment is a distinct response
part and need not be duplicated into the cached operation DTO when it is not itself an
operation fact.

## 4. Owned Decisions

| ID | Decision | Status |
|---|---|---|
| D-SHARED-01 | Text, cached operation DTO, and embedded resource attachment have distinct ownership | Decided |
| D-SHARED-02 | `scaffold_schema` returns the complete resolved schema immediately as an embedded resource | Decided |
| D-SHARED-03 | The same schema remains in the `scaffold_schema` cached DTO because it is that operation's primary result | Decided |
| D-SHARED-04 | Successful `scaffold_artifact` output contains no context schema in any channel | Decided |
| D-SHARED-05 | Artifact-context validation failure returns the selected complete schema immediately as an embedded resource | Decided |
| D-SHARED-06 | The failure schema is not duplicated into the cached `scaffold_artifact` failure DTO | Decided |
| D-SHARED-07 | Full schemas never appear in text output | Decided |
| D-SHARED-08 | Every exposed schema is complete, self-contained, and free of unresolved `$ref` values | Decided |
| D-SHARED-09 | Embedded schemas use `application/schema+json` | Decided |
| D-SHARED-10 | Selected-context attachments use schema://template/<encoded-template-id>/context; active-catalog identity without pf/version; whole-tool schema://validation remains distinct | Human-approved 2026-09-12; §7.6 |
| D-SHARED-11 | Package-directed schema/scaffold DTOs report selected package version and resolved package fingerprint; source suite fingerprint remains in persisted artifact provenance and is omitted from non-artifact DTOs because no separate consumer is demonstrated | Decided |
| D-SHARED-12 | Distribution-only component fingerprints and adopted checkpoint facts are confined to DI-06 renewal results/state and never enter scaffold/schema DTOs, embedded schema resources, or generated artifact metadata | Decided |
| D-SHARED-13 | A selected context schema describes every caller-authored renderer value and no operation-control value; scaffold operation/result DTOs may report exact file/target facts, while only separately sourced server provenance may accompany context into the declared metadata renderer | Decided |

## 5. Responsibilities and Boundaries

### 5.1 Text Presenter

The text presenter receives the operation DTO, notes, success state, and cache
publication facts. It renders bounded actionable text from configured presentation
rules.

It never serializes a full schema, parses an embedded attachment, or reads the cache to
build text.

### 5.2 Cache Publisher

The cache publisher stores the complete structured operation DTO before presentation.

For `scaffold_schema`, the resolved schema is primary operation data and therefore
belongs in that DTO and its cache resource.

For `scaffold_artifact`, a context schema is not an operation result:

- success reports contract, render, validation, and persistence facts;
- context failure reports selected artifact identity and structured validation errors;
- the schema is a recovery attachment delivered with the response.

The cache publisher therefore receives no failure attachment and performs no
tool-specific field exclusion or projection.

### 5.3 Embedded Resource Presenter

The embedded resource presenter receives structured attachments separately from the
operation DTO. It owns resource URI selection, MIME type, and JSON serialization.

Domain and tool layers provide schema data, not preformatted JSON strings or
human-facing resource prose.

### 5.4 Application Response Composition

The response composition seam carries two distinct values:

1. one immutable operation DTO;
2. zero or more immutable structured attachments.

Cache publication consumes only the operation DTO. Text presentation consumes only the
operation DTO and publication facts. Embedded-resource presentation consumes the
attachments. Final MCP response assembly combines the rendered text, cache link, and
presented embedded resources.

This separation prevents both undesirable alternatives:

- putting large diagnostic attachments into every complete cached operation record;
- asking presenters to rediscover schemas through filesystem, catalog, or tool calls.

The exact implementation type names remain open. Any implementation must use narrow
interfaces and constructor injection and must not add generic fields to unrelated DTOs
without consumers.

## 6. Options and Rationale

### Option A — Cache-Only Schema Delivery

The tool returns compact text and a cache URI; the agent reads the cache to obtain the
schema.

Rejected as the primary interaction because schema retrieval is the explicit purpose of
`scaffold_schema`, and a context failure should be recoverable without a second
`scaffold_schema` invocation. The extra cache read is an avoidable interaction step.

### Option B — Inline Text Schema Delivery

Serialize the schema into tool text.

Rejected because it defeats issue 456's bounded presentation contract, mixes
machine-readable data with prose, and makes field-oriented presentation configuration
own a deep payload.

### Option C — Embedded Schema with Operation/Attachment Separation

Return schemas as embedded JSON Schema resources and retain compact text. Cache primary
operation data, while failure-only recovery attachments remain outside the operation
DTO.

Selected because it provides direct machine-readable output, preserves issue 456's text
boundary, and avoids systematic or failure-path cache bloat.

## 7. Detailed Design

### 7.1 Channel Contract

| Operation State | Text | Cached Operation DTO | Embedded Resource |
|---|---|---|---|
| `scaffold_schema` success | Artifact identity, purpose summary where bounded, success, cache URI | Artifact identity, purpose, selected package version, resolved package fingerprint, complete resolved schema | Complete resolved schema |
| `scaffold_artifact` success | Created files and concise outcome evidence, cache URI | Complete scaffold operation facts, selected package version, and resolved package fingerprint; no context schema | None |
| `scaffold_artifact` artifact-context failure | Artifact identity, failing JSON pointers/keywords, recovery instruction, cache URI | Artifact identity, selected package version, resolved package fingerprint, structured validation errors; no context schema | Exact complete selected context schema |
| Outer MCP envelope failure | Framework-owned bounded validation response | Tool may not execute or publish an artifact-specific cache DTO | No selected artifact schema unless selection completed safely |
| Render/output-profile/persistence failure | Relevant concise diagnostics, cache URI | Complete failure facts for that stage | No context schema |

For scaffold operation success versus output-validation status, consume the
[DI-04 validation outcome contract](design-mutation-validation.md#44-scaffold-validation-request-and-result-contract).
The full validation report belongs in the cached operation DTO. Bounded text must
distinguish creation from validation and expose failed, unavailable, or incomplete
evidence even when the operation successfully creates an artifact. This adds no context
schema attachment and does not define the separate safe-edit or check/test/fix operation results.

The created artifact itself persists the source suite fingerprint under the Suite
Resolution contract. That fact does not make the complete-suite identity primary output
of `scaffold_schema`, a scaffold failure, or the non-artifact scaffold operation DTO.
No cache or attachment duplicates it without a demonstrated consumer.

The amended F-10/S-10 operational component fingerprints and adopted checkpoint are
likewise not scaffold operation facts. They belong only to DI-06 renewal state and
renewal results. Their existence does not change this channel matrix, the four-field
artifact provenance contract, or the schema attachments.

### 7.2 `scaffold_schema` Success

The tool obtains one immutable selected-artifact schema view from the resolved catalog.
The operation DTO includes:

- artifact identity;
- artifact purpose;
- selected package version;
- resolved package fingerprint;
- complete resolved context schema.

The response embeds the schema directly. The cache URI identifies a secondary per-run
record while retained by the existing bounded in-memory cache. It is not durable
history and may expire through eviction or server restart. An agent does not need to
read it to receive the schema; no historical schema-reconstruction promise is added.

Immediate schema tokens are intentional: the caller invoked a schema-retrieval tool.

### 7.3 `scaffold_artifact` Success

The context schema was used for validation but is not output data. Neither successful
operation DTO nor embedded resources contain it. The implementation must not flatten or
copy a schema solely for successful response presentation.

The resolved catalog may already retain a reusable exposed view; that does not justify
copying the view into the run cache.

### 7.4 Artifact-Context Validation Failure

This path applies only after a valid artifact identity selected a catalog contract and
the caller's `context` failed that artifact's JSON Schema.

The failure DTO contains structured facts such as:

- artifact identity;
- selected package version;
- resolved package fingerprint;
- JSON Pointer instance location;
- schema keyword or constraint;
- concise machine-readable error code and message facts.

A separate structured schema attachment contains the exact selected resolved schema
used to define the contract. Response presentation serializes it as
`application/schema+json`.

The full schema is delivered immediately and intentionally consumes model context on
this exceptional path. That cost is justified by first-response recovery and does not
affect valid scaffolding calls.

### 7.5 Schema Completeness

“Resolved” means every reference required to interpret the selected contract is
present inline. Resolution may not omit definitions for brevity, retain inaccessible
external references, or return only the failing subtree.

The embedded and cached `scaffold_schema` copies must be structurally equal. The
validation-failure attachment must be structurally equal to the selected catalog view.
No output path recomputes or independently transforms schema semantics.

### 7.6 Resource Identity

Human-approved 2026-09-12. Use `schema://template/<encoded-template-id>/context`
for both successful scaffold_schema retrieval and selected-template context rejection.
Percent-encode manifest.yaml's template_id as one URI path segment. Do not derive
identity from the package directory, include an absolute filesystem path, or append
a fingerprint, release label or cache run ID. Distinct template IDs identify distinct
attachments; no multi-version schema response is introduced.

This identifies the template's context schema in the active catalog, not an immutable
historical schema. After a catalog-changing restart, the same URI may accompany new
content. Consumers use the complete embedded content delivered for the response, not
a historical schema cached solely under this URI. Startup snapshot consistency remains
binding. No resources/read endpoint, source retention or historical lookup is added.

The existing per-run cache identifies each operation record. A scaffold_schema record
includes its schema; scaffold context failures deliberately cache issues without the
schema attachment (§7.1). Do not claim that every cached scaffold failure retains a
historical schema. Package provenance already present in operation DTOs is unchanged.

Retain `schema://validation` for whole-tool input errors; do not repurpose it for a
selected context. Selected attachments use application/schema+json and the existing
operation/attachment composition seam, without DTO-specific presenter dispatch.

Rejected: pf in this URI. It adds version-bound identity without a demonstrated URI
versioning consumer and changes on Jinja-only edits. Omitting it changes neither
artifact provenance nor operational upgrade fingerprints. URI naming never changes
schema content, validation rules or the existing cache/attachment ownership boundary.

## 8. Control, Data, and State Flow

### `scaffold_schema`

Tool → resolved catalog selection → immutable schema operation DTO plus schema
attachment → cache operation DTO → render concise text → serialize attachment → assemble
one MCP response.

### Successful `scaffold_artifact`

Tool → select resolved contract → validate context → render/validate/persist through
DI-04/DI-05 → operation DTO without attachment → cache → text presentation → assemble
response.

### Invalid Artifact Context

Tool → select resolved contract → validation fails → structured failure DTO plus
selected-schema attachment → cache failure DTO only → render concise error text →
serialize attachment → assemble response.

No presenter calls `scaffold_schema`, reads suite files, resolves `$ref`, or queries
the runtime catalog.

## 9. Compatibility, Migration, and Removal

Issue 456's field-oriented text presentation remains unchanged in principle. The
required refinement is structural:

- current `ValidationErrorOutput.input_schema` couples the embedded attachment to the
  cached failure DTO;
- current `ValidationResourcePresenter` extracts and serializes that DTO field;
- target composition carries the schema as a separate structured attachment;
- remove schema duplication from cached artifact-context failures;
- add direct embedded-resource presentation to successful `scaffold_schema`;
- retain the complete schema in the `scaffold_schema` operation DTO/cache;
- update the presentation architecture reference to document operation-versus-attachment
  completeness.

No compatibility bridge should emit both legacy cache-only and new direct schema
instructions as competing authorities. Text may mention the embedded resource but may
not require a cache read as the normal next step.

## 10. Test and Validation Design

Package-owned tests must prove:

- `scaffold_schema` returns one complete embedded JSON Schema resource;
- its cached DTO contains a structurally equal schema plus the selected package's
  version and resolved package fingerprint;
- its text remains bounded and does not contain schema JSON;
- successful `scaffold_artifact` output contains no context schema in text, cache DTO,
  or embedded resources;
- artifact-context failure embeds the exact selected resolved schema;
- the cached failure DTO retains structured errors and omits the schema;
- outer envelope and non-context failures do not attach an irrelevant artifact schema;
- resource presentation performs serialization but no catalog/filesystem lookup;
- cache publication occurs before presentation and stores only the operation DTO;
- schema identity and content do not diverge across delivery paths;
- encoded IDs remain unambiguous URI segments and distinct templates remain distinct;
- a catalog-changing restart can return changed schema under the same URI, with the
  response's embedded content authoritative; no pf-derived identity or historical reuse;
- existing whole-tool schema://validation assertions remain valid.

Tests should inspect structured MCP content and cached DTOs. Full text snapshots and
parsing prose to recover facts are rejected.

## 11. Integration Risks and Open Questions

| ID | Item | Owner | Resolution |
|---|---|---|---|
| Q-SHARED-01 | What URI identifies selected context schema resources? | Shared contract | Closed by human approval on 2026-09-12: §7.6, active-catalog template identity without fingerprint; implementation/client conformance remains required |
| R-SHARED-01 | Separating attachments creates a broad generic response wrapper | Shared contract | Keep the seam narrow and require at least cache and resource-presenter consumers |
| R-SHARED-02 | Schema is flattened differently for validation and exposure | DI-01/DI-02 | One catalog-owned resolved schema view with structural equality tests |
| R-SHARED-03 | Embedded schemas make routine scaffold calls token-heavy | DI-04 | Attach only for explicit schema retrieval or selected artifact-context failure |

## 12. Planning Consequences

Planning must separate:

- structured operation/attachment response composition;
- successful `scaffold_schema` embedded-resource presentation;
- artifact-context failure attachment migration;
- cache DTO cleanup and issue 456 architecture-reference updates;
- bounded text presentation updates;
- structured response/cache tests.

Planning may not add schemas to successful `scaffold_artifact` DTOs as a temporary
shortcut.

## 13. Traceability Matrix

| Obligation | Design Coverage |
|---|---|
| F-01 public context ownership | The selected resolved schema is the caller contract and direct schema payload |
| F-03 caller context | Validation errors reference original caller JSON Pointers; exact file/target controls remain operation facts and never enter schema or render content; server provenance stays separately namespaced |
| F-04/F-05 renderer and graph authority | All schema deliveries originate from the one resolved catalog |
| F-09 documentation authority | Live embedded schema owns exact fields; prose explains discovery only |
| F-10 renewal checkpoint | Distribution-only component fingerprints and adopted state remain outside scaffold/schema channels and artifact metadata |
| F-11 provenance | Persisted artifacts carry both fingerprints; package-directed non-artifact DTOs retain selected package version and resolved package fingerprint and omit source suite identity under YAGNI |
| F-16 purpose introspection | `scaffold_schema` operation DTO retains selected artifact purpose |
| DI-01/DI-02 | Own schema content, resolution, catalog, purpose, both computed identities, and persisted artifact provenance inputs |
| DI-04 | Consumes failure attachment semantics without owning schema authority |
| DI-07 | Updates tool/reference guidance after the public contract is final |
| XC-01 | Separates presentation, caching, catalog reads, and operation facts through narrow dependencies |
| RC-01 | Preserves issue 456 except for the explicit attachment-completeness clarification |

## 14. Related Documentation and Version History

### Related Documentation

- [Design Hub](design.md)
- [Suite Resolution Design](design-suite-resolution.md)
- [Pre-Implementation Documentation Contract](README.md)
- [Research](research.md)
- [Design Intake Map](design-intake-map.md)
- [Issue 456 Design](../issue456/design.md)
- [Issue 456 Tool Presentation Field Audit](../issue456/tool-presentation-field-audit.md)
- [Presentation Architecture](../../reference/presentation_architecture.md)
- [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)

### Version History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.8 | 2026-09-12 | `@imp designer` | Consolidate approved active-catalog schema URI without pf; preserve whole-tool validation URI and operation/attachment cache ownership; define restart and identity evidence. |
| 1.7 | 2026-09-05 | `@imp designer` | Link the exclusive DI-04 and DI-05 owners after F-20; keep existing artifact-schema delivery semantics unchanged. |
| 1.6 | 2026-09-03 | `@imp designer` | Link the DI-04 validation outcome authority and require truthful success-with-validation-findings presentation without changing schema attachment/cache ownership. |
| 1.5 | 2026-09-03 | `@imp designer` | Align schema delivery with the corrected F-03/F-07 boundary: context schemas expose all caller-authored renderer values, operation controls remain operation/result facts, and only separately namespaced provenance reaches the metadata renderer. |
| 1.4 | 2026-09-03 | `@imp designer` | Keep the amended F-10/S-10 operational component checkpoint strictly inside DI-06 renewal state/results; scaffold/schema channels and four-field artifact provenance remain unchanged. |
| 1.3 | 2026-08-30 | `@imp designer` | Preserve source suite fingerprint in created artifact provenance while retaining package-only identity facts in non-artifact schema/scaffold DTOs under the demonstrated-consumer and issue-456 output boundaries. |
| 1.2 | 2026-08-29 | `@imp designer` | Replace superseded global provenance in package-directed DTOs with selected package version and resolved package fingerprint while excluding F-10 suite-management identity. |
| 1.1 | 2026-08-27 | `@imp designer` | Record direct embedded schema delivery, operation-versus-attachment completeness, success/failure cache boundaries, and issue 456 migration consequences. |
| 1.0 | 2026-08-27 | `@imp designer` | Scaffold the shared-contract package from the agreed schema-delivery nucleus. |
