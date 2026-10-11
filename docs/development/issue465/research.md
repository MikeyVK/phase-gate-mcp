<!-- pgmcp:v1 id=research pv=1.0.0 pf=lgBwxWMfTAmNNg_O sf=zJbLuUrs_I33kpX4 -->

# Issue 465 — YAML, JSON Schema and architecture artifact research

**Status:** Draft — YAML direction approved; combined Research incomplete  
**Version:** 0.2  
**Last Updated:** 2026-10-11

## Purpose

Establish independently evidenced scope and strategy for the combined artifact-family issue. This initial draft records the YAML workspace inventory; it does not close Research.

## Scope In

YAML source files and direct consumers in C:/temp/pgmcp and C:/1Voudig/99_Programming/ST; historical YAML seeds and issue-460 deferral. C:/temp/S1mpleTrader was also inspected as a smaller checkout. Further conclusions for #484 and #498 remain separate work.

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
| Bounded reusable YAML configuration family | Provides ordinary configuration authoring through pgmcp, with reliable data rendering and configured output checks. | Owner-selected direction; concrete input shapes, renderer and native tool remain to be researched. |
| Consumer-specific packages sharing YAML rendering | Add prescribed structure, required fields or useful defaults for a proven consumer. | Add only where that extra value is demonstrated; no package per observed configuration file. |
| Only manifest/policy authoring packages | Small and tied to closed consumers. | Rejected as premature narrowing; does not meet the wider controlled-authoring goal. |
| No YAML family | Avoids new rendering and validation responsibility. | Not the selected direction; leaves agents without this supported pgmcp authoring route. |

The owner selected a modest complete YAML configuration family primarily for the value of the controlled authoring route, rather than for domain structure invented by a generic template. Supporting all YAML constructs or rebuilding consumer configuration models is not required.

### Separate combined-issue work
The controlled-authoring goal applies to evaluating all three artifact families. It does not expand #484 from JSON Schema source artifacts to arbitrary JSON configuration, or settle #498 ADR/SAD contracts and arc42 attribution. Their independent conclusions and boundary strategies remain required before combined Research closes.

## Questions

- Bound the ordinary YAML data shapes, string/type guarantees and comment/multiline behavior; determine whether authoring anchors adds enough value for the initial family.
- Identify the smallest reliable YAML rendering capability and existing native output checker that fit the current package, adapter and profile contracts.
- Determine how the selected output profile is reused for subsequent safe edits; keep format validation distinct from optional consumer-schema validation.
- Capture separate owner decisions for JSON Schema source artifacts and ADR/SAD packages before closing combined Research.

## Approved Strategy

**Owner decision, 2026-10-11:** the owner accepted the proposed controlled-authoring approach with "Ja, zo wil ik het aanpakken." The preceding proposal distinguished template structure, reliable format rendering and the pgmcp write/validation boundary.

| Affected boundary | Approved direction and limitation |
|---|---|
| Durable artifact authoring | Aim to support creation and subsequent editing through pgmcp so the owner can configure form, content constraints and quality checks. This combined issue implements its selected families, not every persistent file type. |
| YAML family scope | Pursue a modest complete reusable family for ordinary structured configuration. Do not restrict it to pgmcp manifests/policies or create a separate package for each source file. Its primary value is the supported authoring route. |
| Template content versus consumer semantics | Templates prescribe structure where useful. A generic YAML family owns supported input forms and reliable output; application-specific validity remains with an applicable schema or consumer validator. |
| Public tooling and adapter boundary | Prefer existing configurable tools for checks and formatting. Adapters integrate those tools without acquiring application-specific configuration knowledge. Tool selection and version requirements remain Research work. |
| Existing package and authoring contracts | Reuse the current discovery, context-schema, rendering and configured validation boundaries. Support the new family by additions where possible; do not redesign existing supported artifact contracts. |
| Historical seeds | Do not restore the incomplete v2 seeds or introduce a compatibility path for them. They are Research evidence, not a supported contract to preserve. |
| Harness enforcement | Supplying a pgmcp authoring route does not disable write tools in an external harness. General harness restrictions or an instruction rollout are not added to this issue. |
| JSON scope | Retain #484's JSON Schema source-artifact scope. General JSON configuration authoring needs a separate explicit scope decision. |

This approves the YAML direction and shared value criterion. It does not approve concrete DTOs, serialization details, a universal YAML generator, all remaining #484/#498 boundaries, or a transition to Design.

## Expected Results

A complete supported YAML family provides creation through scaffolding and subsequent editing through the existing safe-edit route, with schema-complete input, coherent rendering and configured output validation. It must preserve supported data structure and intended value types. Checks must report their actual guarantees: generic format acceptance is not application-semantic acceptance.

Minimal and populated examples must prove parsed-data behavior and useful configured validation; suite-only extension remains an acceptance boundary. Keep evidence focused and avoid whole-file snapshots or tests merely rejecting old behavior. The chosen renderer/profile integration and exact supported forms still require research. #484 and #498 retain separate expected results.

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
