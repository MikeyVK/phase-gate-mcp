<!-- pgmcp:v1 id=research pv=1.0.0 pf=lgBwxWMfTAmNNg_O sf=zJbLuUrs_I33kpX4 -->

# Issue 465 — YAML, JSON Schema and architecture artifact research

**Status:** Research complete — owner strategy approved; independent review pending  
**Version:** 0.6  
**Last Updated:** 2026-10-11

## Purpose

Establish independently evidenced scope and strategy for the combined artifact-family issue. Record the YAML workspace inventory, source-based technical feasibility and separate JSON Schema/ADR/SAD conclusions; The owner strategy is complete; independent Research-to-Design review remains pending.

## Scope In

YAML source files and direct consumers in C:/temp/pgmcp and C:/1Voudig/99_Programming/ST; historical YAML seeds and issue-460 deferral. C:/temp/S1mpleTrader was also inspected as a smaller checkout. Include separate source-based conclusions for JSON Schema (#484) and portable ADR/arc42 SAD (#498), with shared rendering, provenance, native validation and distribution boundaries.

## Scope Out

No implementation, package selection, new adapter design or phase transition. No restoration of incomplete seeds, unrestricted YAML generator, YAML round-trip editor, or consumer-specific business validation in generic server code.

## Problem Statement

The official suite has no complete supported YAML artifact family after issue 460 removed incomplete seeds. The combined issue also covers JSON Schema source artifacts (#484) and ADR/arc42 SAD packages (#498), which require their own conclusions and acceptance boundaries.

## Goals

- Select a useful, bounded YAML artifact family from real workspace consumers rather than limiting it prematurely to pgmcp package metadata.
- Keep separate Research conclusions and owner-approved strategies for #465, #484 and #498.
- Reuse generic package discovery, schemas, rendering and configured validation without adding consumer-specific knowledge to the server.

## Background

The active S1mpleTrader workspace with pgmcp v2 is C:/1Voudig/99_Programming/ST. The smaller C:/temp/S1mpleTrader checkout also contains locales/en.yaml but has no installed .pgmcp directory. Sources were inventoried with rg --files --hidden (and --no-ignore for S1mpleTrader), excluding Git internals, environments, dependencies and caches. Representative files and Python readers were inspected with Get-Content and rg; no files in either S1mpleTrader checkout were changed. A denied pgmcp test-cache directory was not investigated because it is outside the first-party source boundary.

## Findings

### #465: historical disposition
Issue 460 removed two incomplete, unregistered YAML bases and explicitly deferred a complete supported YAML subset. This was not a rejection of YAML templates. The restored source at commit `4ba22137757400d975d7ab8178c508f58999fb67` emits a mandatory `name:`, raw key/value entries, an optional header comment and one nested-section layer. It provides no complete value-serialization contract; its advertised anchors are not implemented. The same two bases remain in the installed ST v2 suite. The registered `schema` artifact there produces a Python Pydantic model, not a YAML configuration file.

### #465: observed workspace families
| Actual source | Structure and direct consumer | Scope implication |
|---|---|---|
| pgmcp `.pgmcp/config/checks.yaml`, lines 1–75 | Nested mappings, scalar lists, empty lists, integer timeouts and a real anchor/alias pair; ConfigLoader loads YAML and typed check configuration. | Ordinary configuration needs more than two flat metadata packages. |
| pgmcp `.pgmcp/config/contracts.yaml`, lines 10–54 | Lists of records, nested mappings, booleans and literal multiline instruction text; ConfigLoader loads ContractsConfig. | Record lists and literal text are demonstrated needs. |
| pgmcp `.pgmcp/config/presentation.yaml`, lines 3–68 | Nested text catalogs, Unicode, numbers and placeholder-bearing strings; ConfigLoader loads presentation configuration. | Authored strings must retain their intended text and type. |
| pgmcp `mcp_server/bundled_adapters/ruff/manifest.yaml`, lines 1–37 | Role/capability mappings, lists of file names and argument records; load_adapter_manifest applies AdapterManifest validation. | Metadata is one application of structured YAML, not the whole family. |
| ST `.pgmcp/config/quality.yaml`, lines 6–65; `project_structure.yaml`, lines 7–69 | Lists of tools/arguments, integers, booleans, null and mappings of directory policies. | Installed v2 supplies additional concrete configurations; its comments alone do not prove every configuration field is currently exercised. |
| ST `locales/en.yaml`, lines 14–93 | Nested mappings ending in strings, literal dotted keys and formatting placeholders. `backend/utils/translator.py`, lines 47–51 and 72–84, loads the locale and traverses dot-separated lookup keys. Lines 100–103 separately read literal dotted parameter keys. | A non-pgmcp application consumer is present; mandatory generic `name:` would be unjustified here. |
| pgmcp template-package manifests and policies | Small closed metadata mappings; ConfigLoader explicitly validates TemplateManifest and TemplatePolicy. | Useful examples, but an insufficient standalone answer to the wider owner need. |

Outside pgmcp's installed configuration and template assets, the inspected ST checkout exposes one application YAML file: `locales/en.yaml`. This inventory does not establish deployed trading/strategy YAML consumers. Config schema classes, examples in Markdown and old YAML bases are not counted as active YAML artifacts.

### #465: evidence-backed requirements and limits
The observed common data shapes are nested mappings with string keys, scalar values, scalar lists and lists of records. The inspected examples also use empty lists, null, literal multiline text, comments and Unicode. Actual anchors demonstrate existing source syntax, but do not yet establish that new scaffolding must author anchors. Comments and anchor spelling are separate from parsed consumer data; whether their authored form belongs in the new template contract remains an owner decision.

A syntax-valid YAML document is not a guarantee of correct consumer settings. pgmcp applies consumer models after parsing; ST Translator parses YAML and checks lookup results, without a complete locale schema in that reader. Generic YAML validation must not claim either consumer's semantic guarantees.

Current `.pgmcp/config/checks.yaml` admits Python, TypeScript, commit and Markdown checks/profiles, with no YAML output check or extension profile. Existing YAML configuration loading is not already a scaffold/safe-edit output adapter. Completing YAML support therefore requires a configured output-validation route as well as templates.

### #465: options considered
| Option | Value | Disposition |
|---|---|---|
| Bounded reusable YAML configuration family | Provides ordinary configuration authoring through pgmcp, with reliable data rendering and configured output checks. | Owner-selected direction; the rendering/checking boundary recorded below is now owner-approved. |
| Consumer-specific packages sharing YAML rendering | Add prescribed structure, required fields or useful defaults for a proven consumer. | Add only where that extra value is demonstrated; no package per observed configuration file. |
| Only manifest/policy authoring packages | Small and tied to closed consumers. | Rejected as premature narrowing; does not meet the wider controlled-authoring goal. |
| No YAML family | Avoids new rendering and validation responsibility. | Not the selected direction; leaves agents without this supported pgmcp authoring route. |

The owner selected a modest complete YAML configuration family primarily for the value of the controlled authoring route, rather than for domain structure invented by a generic template. Supporting all YAML constructs or rebuilding consumer configuration models is not required.

### #465: rendering and configured output checks

| Investigated route | Source observation | Research conclusion |
|---|---|---|
| Existing Jinja/raw interpolation | The real filter registration has no YAML serializer. Direct interpolation does not supply a complete scalar/container contract. | Do not revive the old renderer or implement YAML quoting in Jinja loops. |
| PyYAML safe emission | PyYAML is already a server dependency; inspected workspace metadata reports 6.0.3. Its safe emitter serializes standard data, with formatting options and scalar representer extension points. | A small artifact-agnostic serialization filter is a viable generic capability addition; it must be registered in the real admission and rendering environments. No YAML parser/emitter implementation of our own. |
| JSON-data-shaped YAML | The existing content boundary accepts finite JSON values and detaches them to ordinary dict/list values before Jinja rendering. | Use one mapping-root document with ordinary string keys, finite scalars, mappings and lists. This excludes a free-form YAML DSL, custom objects/tags, multi-document streams and authored cyclic references. |
| Native check-jsonschema | Supports YAML/JSON instance checks against a local schema and JSON Schema metaschema checks, with native JSON diagnostics. Verified tool baseline: 0.38.2; not a claimed functional minimum. | One native-tool adapter can serve configured checks for both source families. A local output schema can express the generic YAML configuration shape; no application field knowledge belongs in the adapter. |
| yamllint | Offers syntax/style rules and native configuration; defaults include more style policy than this issue requires, and configuration can be discovered outside the workspace unless explicitly selected. | A viable optional style tool, but not required merely to add another gate when the chosen serializer and schema check cover the selected initial contract. |

Source-based feasibility is not execution proof. [PyYAML emission](https://pyyaml.org/wiki/PyYAMLDocumentation), [native checker usage](https://check-jsonschema.readthedocs.io/en/stable/usage.html) and [yamllint configuration](https://yamllint.readthedocs.io/en/stable/configuration.html) are the primary references.

The two YAML parser families are not equivalent. PyYAML recognizes additional plain scalar spellings such as on/off and timestamps. The inspected [0.38.2 YAML parser](https://github.com/python-jsonschema/check-jsonschema/blob/0.38.2/src/check_jsonschema/parsers/yaml.py) uses ruamel.yaml, treats timestamps as strings and converts mapping keys to strings. Therefore native checker success cannot prove the original key types or equality with a PyYAML consumer. The proposed initial rendering contract quotes string keys/ordinary strings consistently and preserves multiline string values; acceptance evidence must compare emitted data with both the real PyYAML consumer and the selected checker. Header comments are feasible through the package; per-entry comment authoring, anchors and exact style round-tripping are not required by the current recommendation.

### Shared scaffold/edit integration

Scaffold selects the package policy and calls CheckService.run_content before persistence. Safe edit calls the same method for proposed text; its existing selection precedence is explicit template ID, recognized original provenance, then longest matching configured filename suffix. A native adapter must declare content and selection inputs to serve both pre-write checks and run_checks. No new write service, tool DTO, phase enforcement or artifact-specific Python dispatch is needed.

YAML can use the existing hash-comment provenance carrier and configured .yaml/.yml fallback. The release manifest already distributes the complete source suite and configuration root. Precise adapter files, native arguments, profile IDs and package roots are Design work.

### #484: JSON Schema source conclusions

The shared document metadata definition and its Research/generic_doc consumers are concrete Draft 2020-12 source use cases. Native execution contracts also use that dialect, including $id. The existing Jinja tojson filter is available and already used by the Planning renderer, so the proposed object-based source package does not need a new JSON serializer or context architecture.

The proposed initial dialect is Draft 2020-12. Parsed source and native metaschema acceptance are distinct from a consumer's restrictions: TemplateContractLoader additionally requires an exact dialect URI, object root, unique keys, finite values, contained references and finite static expansion; its resolver excludes several otherwise standard schema keywords. Those restrictions must not be imposed on every JSON Schema source by an adapter. A real template-schema load and instance validation belong in acceptance evidence for that consumer.

The inspected [0.38.2 JSON parser](https://github.com/python-jsonschema/check-jsonschema/blob/0.38.2/src/check_jsonschema/parsers/json_.py) uses optional orjson, otherwise ordinary json.loads. The fallback accepts nonstandard numeric constants and repeated names. A deterministic parser environment is therefore part of the adapter-package requirement; the proposed native route installs its supported orjson dependency so ordinary JSON syntax does not silently inherit the permissive fallback. Repeated-key rejection is still a stricter consumer guarantee, not provided by this metaschema tool. [orjson's documented loads behavior](https://github.com/ijl/orjson#deserialize) supports rejecting those nonstandard constants. Exact dependency versions and native error paths need focused implementation evidence.

Metaschema validation checks the authored schema's formal vocabulary, not the availability of its authored references or representative instance acceptance. Local instance schemas can retrieve external refs; --no-cache is not an offline switch. Use local, nonremote-ref output schemas for the generic YAML check and builtin dialect metaschemas for schema-source checks. Preserve native JSON and stderr diagnostics through the existing check/v1 contract.

JSON cannot use the existing comment prefix. [The standard $comment annotation](https://json-schema.org/draft/2020-12/json-schema-core#section-8.3) is a possible persisted source-provenance carrier, separate from validation meaning.

| Provenance option | Consequence |
|---|---|
| Explicit template selection, with a configured .schema.json suffix where appropriate | Smallest code change. Persistent identity can be carried in $comment, but the current first-line reader will not reconstruct it automatically. Requires an explicit exception to automatic provenance routing for this format. |
| A canonical root $comment carrier plus bounded opening-carrier recognition | Retains persisted identity and automatic package-profile selection. Requires one generic framing/reader extension, preserving ArtifactIdentity and existing carriers; no whole-document scan or schema-specific engine knowledge. |

The owner selected the second route on 2026-10-11: extend the reader narrowly so the persisted pgmcp identity can be recognized through the root $comment carrier. At that decision point, approval covered provenance only. The later final owner decision below separately approves the bounded schema-source and native-checker strategy. Preserve the existing ArtifactIdentity and supported comment carriers, explicit template selection and configured suffix fallback. Recognition stays bounded to the opening carrier; do not scan arbitrary body content or introduce schema-validation knowledge into the reader. Caller-authored schema explanations remain distinct from the reserved technical carrier. The precise framing, budget and malformed-carrier behavior are Design work.

### #498: ADR and arc42 SAD conclusions

Keep the existing architecture package's supported concept-document contract. Add separate portable ADR/SAD packages. The owner explicitly requires both to build on the existing Jinja2 Markdown tiers: tier2_markdown_document -> tier1_document -> tier0_root, reusing shared Markdown section/link patterns. The shared tiers own provenance, the H1 heading, document metadata and revision history; the concrete packages supply their ADR/SAD body. Do not introduce parallel Markdown framing or duplicate the base responsibilities. The inspected Ypsia ADR v1.1.0 is prior art, not an input contract to preserve: its required integer ID is not rendered, its option-object schema does not specify the fields read by Jinja, its status schema does not enforce declared states, and mandatory Strategic/Tactical categories are project-specific. Do not carry those assumptions or alias fields into new packages.

The proposed ADR content covers a visible caller-owned identifier, context/problem, decision drivers, concrete alternatives, a decision and rationale, status and consequences. Optional participants, tags, supersession and verification are authored facts. A single clearly defined ADR status is sufficient initially; it is not approval or workflow evidence. Minimal valid scaffolds may have explicit empty content carriers; never invent conclusions such as "None identified" for omitted evidence.

The SAD retains all twelve official arc42 sections in order, with proportional authored content and a clear distinction between proposed and existing architecture. Its section 9 indexes linked ADRs; each linked ADR records its relevant SAD section targets. Reuse explicit label/target links; do not introduce document discovery, automatic numbering, taxonomy-derived section selection or a lifecycle engine. The supplied links and index facts are reviewed author input, not automatically synchronized state.

The inspected immutable arc42 source is **32fd461c91b184777e14f7d66b4e46db936fd3e5**, declaring **9.0-EN, July 2025**. The [pinned EN source](https://raw.githubusercontent.com/arc42/arc42-template/32fd461c91b184777e14f7d66b4e46db936fd3e5/EN/arc42-template.adoc), [revision file](https://raw.githubusercontent.com/arc42/arc42-template/32fd461c91b184777e14f7d66b4e46db936fd3e5/EN/version.properties) and [license](https://raw.githubusercontent.com/arc42/arc42-template/32fd461c91b184777e14f7d66b4e46db936fd3e5/LICENSE.txt) were read at that exact revision after resolving the official main commit through the GitHub API. Section 10 includes both overview and quality scenarios. The adapted arc42 template requires attribution to Gernot Starke and Peter Hruschka, a CC BY-SA 4.0 link, identification of adaptations and preservation of that license for the distributed adaptation. Caller-authored architecture content remains separately owned. Use a component attribution/license record rather than silently treating the adaptation as solely the repository's general license.

### Impact and proportionate evidence

| Boundary | Likely change and proof obligation |
|---|---|
| Template assets | Four bounded concrete purposes: ordinary YAML configuration, JSON Schema source, ADR and SAD. Package IDs and exact fields remain Design choices. Existing architecture and shared full-document metadata retain their contracts. |
| Generic rendering | One YAML serialization capability; reuse real filter registration and existing detached finite input. JSON uses tojson. Do not promise this entire feature is suite-only; prove later package extension is file-based once required generic capabilities exist. |
| Generic provenance | Only the selected JSON carrier can require a bounded reader/shared-format change; existing carriers remain supported. |
| Native tooling and configuration | One native-tool adapter candidate, pinned environment requirements, content/selection capabilities, check/profile bindings and release assets. Configure native semantics instead of writing application validators in the adapter. |
| Tests and helpers | Reuse delivered_templates and existing public scaffold/edit fixtures. Prove parsed type/value preservation, native acceptance/rejection and enforce/report write behavior. Prove actual consumer use separately. For ADR/SAD prove field placement, supplied status/identity, twelve-section structure and real cross-links; avoid whole-document snapshots and arbitrary prose assertions. |
| Documentation and instructions | Extend existing template/adapter usage and provenance references only where behavior changes. No general instruction rollout or new template-release procedure; use the current suite maintenance/release contract. |

No native candidate execution, benchmark or implementation test was performed in this Research step. Feasibility claims are based on direct source inspection. Production/configuration/template assets remain unchanged.

### Final boundary decisions

The owner explicitly accepted the remaining proposals on 2026-10-11 with "Akkoord", in response to the producer's three-boundary YAML, JSON Schema and ADR/SAD decision table. This supplements the earlier controlled-authoring, Markdown-inheritance and provenance decisions.

| Boundary | Owner-approved strategy |
|---|---|
| YAML rendering/checking | Add only an artifact-agnostic PyYAML rendering capability and a native check-jsonschema adapter with a deterministic supported parser environment. Start with single mapping-root, ordinary finite data, a header comment and readable multiline values; omit authored anchors/per-entry comment DSL. |
| JSON Schema source/checking | One object-based Draft 2020-12 source family, no arbitrary JSON generator or template-consumer-specific validator. The bounded $comment provenance reader extension and native metaschema-checking route with a deterministic supported parser environment are approved. |
| ADR/SAD and licensing | New portable packages, visible caller-owned ADR identity and authored status, proportional drafts and explicit ADR/SAD links. Preserve architecture; no legacy input bridges, automatic lifecycle or numbering. Distribute the arc42 adaptation with its pinned-source attribution and component license. |

These decisions complete the human strategy gate for the researched boundaries. They do not substitute for independent QA or authorize implementation. Concrete package fields, native arguments and versions, framing and operational details belong in Design.

## Questions

No Research strategy decision remains open. Design must specify package IDs and fields, the YAML serializer's concrete scalar/multiline contract, native adapter arguments and supported version/parser environment, JSON provenance framing and bounded malformed-carrier behavior, and proportional ADR/SAD draft/status/link behavior. These are refinements within the approved boundaries, not new architecture proposals.

Independent QA must evaluate the Research-to-Design gate before phase progression.

## Approved Strategy

**Owner decision, 2026-10-11:** the owner accepted the proposed controlled-authoring approach with "Ja, zo wil ik het aanpakken." The preceding proposal distinguished template structure, reliable format rendering and the pgmcp write/validation boundary.

| Affected boundary | Approved direction and limitation |
|---|---|
| Durable artifact authoring | Aim to support creation and subsequent editing through pgmcp so the owner can configure form, content constraints and quality checks. This combined issue implements its selected families, not every persistent file type. |
| YAML family scope | Pursue a modest complete reusable family for ordinary structured configuration. Do not restrict it to pgmcp manifests/policies or create a separate package for each source file. Its primary value is the supported authoring route. |
| Template content versus consumer semantics | Templates prescribe structure where useful. A generic YAML family owns supported input forms and reliable output; application-specific validity remains with an applicable schema or consumer validator. |
| Public tooling and adapter boundary | Prefer existing configurable tools for checks and formatting. Adapters integrate those tools without acquiring application-specific configuration knowledge. Owner-approved native route: one check-jsonschema adapter with distinct configured YAML instance-schema and JSON Schema metaschema checks, and a deterministic supported parser environment. Native validation does not imply every consumer's stricter admission. |
| Existing package and authoring contracts | Reuse the current discovery, context-schema, rendering and configured validation boundaries. Support the new family by additions where possible; do not redesign existing supported artifact contracts. |
| ADR/SAD Markdown inheritance | The owner explicitly requires both new packages to build on the existing Jinja2 Markdown tiers and shared patterns. Preserve base-owned provenance, heading, metadata and revision history; supply artifact-specific body content through the existing blocks. The later owner approval also covers the bounded portable content/linking and attributed component-license strategy below. |
| Historical seeds | Do not restore the incomplete v2 seeds or introduce a compatibility path for them. They are Research evidence, not a supported contract to preserve. |
| Harness enforcement | Supplying a pgmcp authoring route does not disable write tools in an external harness. General harness restrictions or an instruction rollout are not added to this issue. |
| JSON scope | Retain #484's JSON Schema source-artifact scope. General JSON configuration authoring needs a separate explicit scope decision. |
| JSON Schema provenance | Owner decision, 2026-10-11: extend the reader narrowly to derive the existing pgmcp identity from a canonical root $comment carrier. Preserve bounded recognition, ArtifactIdentity, existing comment carriers, explicit selection and configured suffix fallback. Do not add schema-validation responsibilities or a whole-document scan. Exact framing and malformed-carrier behavior are Design work. |
| YAML rendering and output scope | Owner decision, 2026-10-11: use the existing PyYAML library through one generic rendering capability. Support one mapping-root, finite ordinary data, header comment and multiline text; omit authored anchors/per-entry comment DSL. Use the configured native instance-schema check. |
| JSON Schema source and native environment | Owner decision, 2026-10-11: support an object-based Draft 2020-12 source family, reuse JSON rendering, and use the same native tool via a separate metaschema check. Specify a predictable version/parser contract in Design; do not impose a particular template consumer's restrictions in the adapter or add a general JSON generator. |
| Portable ADR/SAD and distribution | Owner decision, 2026-10-11: use new portable packages on existing Markdown tiers, supplied ADR identity/status, explicit ADR/SAD links and twelve SAD sections. Keep existing architecture supported; no legacy input bridges, automatic numbering or lifecycle engine. Distribute the pinned arc42 adaptation with attribution and its component license. |

The strategy gate is complete. Concrete DTOs, field names, serialization details and operational version/framing contracts remain Design work within these boundaries. Independent QA must supply the Research-to-Design verdict; owner strategy approval alone is not that verdict.

## Expected Results

A complete supported YAML family provides creation through scaffolding and subsequent editing through the existing safe-edit route, with schema-complete input, coherent rendering and configured output validation. It must preserve supported data structure and intended value types. Checks must report their actual guarantees: generic format acceptance is not application-semantic acceptance.

Minimal and populated examples must prove parsed-data behavior and useful configured validation; suite-only extension remains an acceptance boundary after required generic capabilities exist. Keep evidence focused and avoid whole-file snapshots or tests merely rejecting old behavior. Native candidate behavior still requires execution evidence in the owning implementation/validation phases.

| Included issue | Separate acceptance result |
|---|---|
| #465 | A supported ordinary YAML configuration package creates a single mapping-root document, preserves intended supported types/text and uses the configured native pre-write route for scaffolding and editing. Demonstrate real-consumer parsing and suite-only extension. |
| #484 | A supported object-based Draft 2020-12 source package renders parseable JSON, receives native metaschema evidence and uses the selected valid provenance/edit route. Demonstrate a generated schema through a real template consumer and representative instance validation without claiming metaschema equivalence to every consumer restriction. |
| #498 | Separate portable ADR/SAD packages consume supplied identity, status, content and references meaningfully; SAD retains twelve ordered sections and a compact ADR index. Demonstrate a real linked pair, invalid-input behavior, proportional drafts and correct attribution. Preserve the existing architecture package contract. |

## Evidence

### Issue-460 deferred a complete YAML family rather than rejecting YAML scaffolding.

Deferred-work lines 220–244 explicitly record incomplete/unregistered seeds, future consumer research and the approved removal decision.

- [Deferred notice](<../issue460/deferred-work.md#complete-yaml-artifact-package-subset>)
- [Approved strategy](<../issue460/research.md>)

### Observed pgmcp configurations require varied ordinary YAML shapes.

Direct source inspection found the real anchor/alias pair in checks.yaml, record lists and literal multiline text in contracts.yaml, and role/argument records in the Ruff adapter manifest.

- [Checks configuration](<../../../.pgmcp/config/checks.yaml>)
- [Workflow contracts](<../../../.pgmcp/config/contracts.yaml>)
- [Ruff manifest](<../../../mcp_server/bundled_adapters/ruff/manifest.yaml>)

### ST supplies a concrete non-pgmcp YAML consumer.

C:/1Voudig/99_Programming/ST/locales/en.yaml contains string catalogs; backend/utils/translator.py lines 47–51 parse the selected locale with yaml.safe_load and lines 72–84 validate string lookup results. Literal dotted parameter keys use a separate direct lookup at lines 100–103.

**Invocation:** rg --files --hidden --no-ignore C:/1Voudig/99_Programming/ST -g '*.yaml' -g '*.yml' with dependency/cache exclusions; Get-Content locales/en.yaml and backend/utils/translator.py; rg for yaml.safe_load and .yaml consumers in backend/tests.

**Observed Result:** One application YAML file outside installed pgmcp/agent assets; a direct locale reader was found. Source inspection only; no runtime execution.

### The current output-check configuration does not already offer YAML validation.

checks.yaml lines 18–73 define no YAML check, profile or extension mapping; ConfigLoader YAML parsing is a separate configuration-input boundary.

- [Output check configuration](<../../../.pgmcp/config/checks.yaml>)
- [ConfigLoader](<../../../mcp_server/config/loader.py>)

### Technical source and impact inspection

**Invocation:** Read the current TemplateEngine/filter registration, TemplateCatalogRenderer, ScaffoldOperation, EditOperation, profile selection, CheckService, TemplateContractLoader and schema resolver; inspect delivered-template/public-operation fixtures and release assets. Read the official check-jsonschema 0.38.2 parser/reporting sources and PyYAML/Jinja documentation. Resolve arc42 main via the official GitHub API and read the exact pinned source files recorded in Findings.

**Observed Result:** Shared scaffold/edit content validation and detached finite input already exist. YAML serialization, native source-family checks and the selected JSON carrier are genuine additions. Two bounded producer-delegated research tasks supplied findings for #484/#498; the producer independently checked the decisive local schemas/renderers and native parser/source evidence. Delegates issued no QA verdict or authorization.

- [Rendering and real filter registration](<../../../mcp_server/services/template_engine.py>)
- [Finite detached content](<../../../mcp_server/core/interfaces/template_catalog.py>)
- [Scaffold pre-write checks](<../../../mcp_server/services/scaffold_operation.py>)
- [Safe-edit pre-write checks](<../../../mcp_server/services/edit_operation.py>)
- [Profile selection](<../../../mcp_server/services/edit_construction.py>)
- [Bounded current provenance reader](<../../../mcp_server/services/artifact_header_reader.py>)
- [Template consumer](<../../../mcp_server/services/template_contract_loader.py>)
- [Consumer-specific schema restrictions](<../../../mcp_server/utils/schema_utils.py>)
- [Native execution schema using $id](<../../../mcp_server/execution/contracts/check_v1.schema.json>)
- [Delivered-template fixtures](<../../../tests/mcp_server/fixtures/delivered_templates.py>)
- [Existing architecture package](<../../../.pgmcp/template_suite/architecture/context.schema.json>)
- [Existing template release procedure](<../../development/schema-template-maintenance.md>)
- [Release assets](<../../../.pgmcp/config/release_manifest.yaml>)

## Consumers

### pgmcp ConfigLoader and configuration models

Parse and validate their own application and package configuration.

**Impact:** Examples guide reusable data-shape scope; their field knowledge must not move into the generic server or YAML adapter.

### ST Translator

Read locale string catalogs and resolve lookup keys.

**Impact:** Demonstrates a non-pgmcp consumer and the need to retain string values and key spelling.

### Template package discovery and configured output checks

Admit complete packages and select native output evidence.

**Impact:** The family needs complete package assets and a YAML validation route, while remaining free of artifact-ID-specific server registration.

## Risks

### Treating a directory inventory or configuration comment as proof of an active semantic consumer.

Record direct reader symbols and distinguish source observations from execution evidence.

### Expanding a reusable YAML family into unrestricted YAML authoring or consumer business validation.

Select bounded supported shapes and explicit validation guarantees before Design.

## Related Documents

- [Issue-460 deferred YAML work](<../issue460/deferred-work.md#complete-yaml-artifact-package-subset>)
- [Issue 465](<https://github.com/MikeyVK/phase-gate-mcp/issues/465>)
- [Issue 484](<https://github.com/MikeyVK/phase-gate-mcp/issues/484>)
- [Issue 498](<https://github.com/MikeyVK/phase-gate-mcp/issues/498>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-11 | @imp researcher | Record historical YAML disposition and representative pgmcp/ST sources; keep scope and combined-issue strategies open. |
| 0.2 | 2026-10-11 | @imp researcher | Capture owner-approved controlled authoring and YAML direction; retain unresolved technical and combined-issue boundaries. |
| 0.3 | 2026-10-11 | @imp researcher | Record native rendering/checking feasibility, parser/provenance limits, portable ADR/SAD and pinned arc42 evidence; present boundary strategies for owner decision. |
| 0.4 | 2026-10-11 | @imp researcher | Capture the owner's explicit requirement that ADR/SAD reuse existing Jinja2 Markdown tiers and shared framing responsibilities. |
| 0.5 | 2026-10-11 | @imp researcher | Record owner-approved bounded $comment identity recognition; separate it from remaining source/checking decisions. |
| 0.6 | 2026-10-11 | @imp researcher | Capture final owner approval for YAML/native checks, JSON Schema/parser scope and portable attributed ADR/SAD; close Research strategy questions for independent review. |
