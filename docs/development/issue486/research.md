<!-- pgmcp:v1 id=research pv=1.0.0 pf=lgBwxWMfTAmNNg_O sf=FAN5Vr-4vcbMMjZ2 -->

# ASCII Python identifier contract — Research (#486)

**Status:** RESEARCH COMPLETE — independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-05

## Scope In

Shared Python definitions; eight shipped Python/pytest schemas; delivered-family regression tests and current scaffolding documentation.

## Scope Out

TypeScript identifiers, arbitrary text/type/body parsing, schema resolver architecture, presentation/cache protocols (#462), universal consumption analysis (#476), historical artifact reconciliation.

## Problem Statement

Shared Unicode XID and NFKC-equivalence regular expressions dominate resolved Python template schemas. This is structural schema payload debt; no resolver defect, latency regression or model-quality measurement is asserted.

## Goals

- Inventory every shared Python identifier consumer.
- Record explicit human strategy and preserved contracts.
- Establish measurable size baseline and durable evidence gaps.

## Background

Schemas own admission, shared Jinja patterns own output and TemplateContractLoader resolves references. Repeated expansion is existing supported behavior; the size problem originates in shared lexical patterns rather than dispatch or orchestration.

## Findings

| Boundary | Current responsibilities / coupling | Invariant / evidence gap |
|---|---|---|
| shared/definitions/python.schema.json | Symbol drives declaration names, parameters, fields, imported names and aliases; DottedSymbol drives modules and fixture decorators; FromImport adds relative modules | Full-string admission and keyword rejection must remain; current Symbol oracle accepts native Unicode identifiers |
| python_class / python_protocol | Signature plus InstanceParameter; plain class forbids dunder stubs | Preserve ASCII self and dunder exclusions; type-expression bases remain unrestricted content |
| python_adapter / python_worker | Concrete methods, constructors and injected parameters | Preserve sole __init__ and supplied self restrictions, constructor/body ordering |
| python_pydantic_dto / python_pydantic_config | ModelField with underscore and binding collisions | Preserve reserved names; eliminate unreachable NFKC alternatives |
| pytest_unit_test / pytest_integration_test | TestCase, Fixture, PytestClassName, InstanceTestCase | Preserve test_ / Test discovery and instance self; existing unit-test class case explicitly accepts normalized Unicode spellings |
| tests / helpers | DeliveredTemplate composes real isolated catalog snapshots and native syntax/pytest adapters | Reuse public loader/validator/renderer evidence; avoid duplicated fixtures and private access |
| resolver / config / enforcement | Generic reference expansion, configured admission and native checks | No algorithm, phase/config, manifest registration or deployment-interface change required |

Candidate seams are the shared identifier definitions and consumer-specific exclusion schemas. Test debt is confined to now-obsolete Unicode acceptance oracles; existing rendering and native execution evidence remains valuable. Current reference documentation describes context migration but lacks this lexical boundary.

## Questions

## Approved Strategy

Human decision recorded in [issue #486](https://github.com/MikeyVK/phase-gate-mcp/issues/486), 2026-10-05:

| Affected boundary | Approved strategy | Cost / risk / consumer impact |
|---|---|---|
| Structured Python identifiers | ASCII-only clean break; no compatibility profile, bridge, fallback, normalization or transliteration | Existing non-ASCII caller contexts are rejected. Owner reports no previously scaffolded files with non-ASCII identifiers; this is owner-provided context, not an independent repository audit. Small direct schema contract and payload; hypothetical Unicode callers are intentionally unsupported. |
| Prose / literals / examples / raw code and type expressions | Preserve existing Unicode support and validation contracts | Prevent accidental content restriction; no migration cost for these values. |
| Schema discovery / scaffolding / resolver interfaces | Preserve public envelope, reference semantics, output conventions and native-check policy | Smaller resolved schemas without consumer API migration beyond identifier admission. |

Compatibility-preserving Unicode and a transitional dual profile were viable alternatives, but retain payload or add migration complexity and conflict with the explicit human decision. The approved boundary decisions are binding; no open strategy decision remains.

## Expected Results

All eight packages reject non-ASCII structured identifiers while accepting valid ASCII boundaries, rejecting keywords/reserved spellings and preserving import/relative/star grammar. Unicode prose, literal/default/example and raw body/type values survive validation and rendering. Durable public-API tests and representative minimal/populated native scaffolds prove the contract. Report actual before/after codepoints and, if a tokenizer is available, identified actual token counts; make no latency/model-quality claim.

## Evidence

### Resolved schema payload baseline

Measured via scaffold_schema resource text on 2026-10-05. Count Unicode codepoints, not bytes/UTF-16 units. python_class 107615 (27 patterns / 96952 pattern codepoints); python_protocol 107412 (26 / 96914); python_adapter 126860 (35 / 112433); python_worker 126764 (35 / 112433); python_pydantic_dto 107957 (27 / 98219); python_pydantic_config 107839 (27 / 98219); pytest_unit_test 135575 (38 / 121314); pytest_integration_test 135582 (38 / 121314). Token counts not yet measured.

- [Shared definitions](<../../../.pgmcp/template_suite/shared/definitions/python.schema.json>)
- [Reference resolver](<../../../mcp_server/utils/schema_utils.py>)

### Durable public consumer evidence exists

Family tests exercise isolated delivered catalog validation/rendering, AST/compile round trips and native syntax or pytest adapters. test_shared_python currently compares Symbol admission to native isidentifier/keyword semantics; pytest_unit_test contains normalized Unicode Test-class acceptance.

- [Shared tests](<../../../tests/mcp_server/integration/templates/test_shared_python.py>)
- [Unit-test package tests](<../../../tests/mcp_server/integration/templates/test_pytest_unit_test.py>)
- [Delivered helper](<../../../tests/mcp_server/fixtures/delivered_templates.py>)

## Consumers

### Eight shipped Python and pytest packages

Validate caller context before rendering structured names into Python.

**Impact:** Clean break for non-ASCII names; smaller schema discovery and diagnostics.

### Agents and catalog callers

Discover context schemas and submit contexts.

**Impact:** Rediscover schema; use ASCII names while retaining Unicode content.

### Existing scaffolded files

Caller-owned previously rendered artifacts.

**Impact:** No automatic rewrite or migration; owner reports no non-ASCII identifiers.

## Risks

### Over-restricting Unicode content

Keep Text, Prose, Body, TypeText and JSON values outside identifier policy; verify literal/code preservation.

### Losing ASCII grammar or reserved-name guards

Independent native/lexical boundary assertions and existing consumer-specific tests.

### Misrepresenting schema-size evidence as speed

Fixed serialization/tokenizer methodology; state latency and model quality unmeasured.

## Assumptions

- Owner-provided absence of existing non-ASCII scaffolded identifiers is accepted scope context; no repository-wide audit was performed.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-05 | @imp researcher | Inventory structural schema expansion, preserved boundaries and owner-approved strategy. |
