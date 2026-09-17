<!-- C:\temp\pgmcp\temp\issue460-design-workshops-20260910\07-code-test-artifacts.md -->
<!-- template=design version=5827e841 created=2026-09-10T09:24Z updated= -->
# W07 — Concrete portable code and test packages

**Status:** SUPERSEDED PREPARATION — canonical W07 draft submitted for independent review  

The coordinated source-led design now lives in
[Code and Test Artifact Contracts](../../docs/development/issue460/design-code-test-artifacts.md).
This older preparation is retained as history only; its field names, example-validation wording
and provisional Worker decision are not implementation authority.

**Owner:** DI-03 code/test document; upstream DI-01/DI-02/W06; consumers DI-04/DI-06/DI-08  
**Decision nucleus:** Finite structured content, explicit native-source fragments and honest incomplete behavior; keep existing Jinja tiers.

## 1. Purpose and authority

This is more than relocating templates. Current public shapes disagree with renderer loops, TypeScript splits type strings, and some tests fabricate passing behavior. A valid scaffold must be useful without hidden consumer-project dependencies.

[DI-03 intake](C:/temp/pgmcp/docs/development/issue460/design-intake-map.md:179), [public catalog](C:/temp/pgmcp/docs/development/issue460/template-suite-catalog.md) and per-artifact Research decisions own retained responsibilities.

## 2. Scope and exclusions

Propose IDs, field families, rendering semantics, profile needs, shared patterns and removal evidence. No general programming AST/DSL, implicit imports, generated companion tests, runtime service/tool/resource APIs, YAML family or command/query scaffold family.

## 3. Binding inputs

F-01/S-02, F-14/S-12, F-17, I-7/I-8/I-13, DTO/config/Generic/Protocol/adapter/test/TypeScript responsibility decisions. Existing metadata writer remains in approved shared tiers.

## 4. Proposed identities

| V2 responsibility | Proposed template_id | Bound |
|---|---|---|
| dto | python_pydantic_dto | Immutable data container |
| schema | python_pydantic_config | Explicitly configured mutability; external config model |
| generic | python_class | Body-free bounded class |
| interface | python_protocol | Explicit Protocol signatures |
| adapter | python_adapter | Portable caller-defined boundary adapter |
| worker | python_worker | Canonical retain/adapt, subject to discrepancy below |
| unit_test | pytest_unit_test | At least one caller-authored behavioral case |
| integration_test | pytest_integration_test | At least one explicit collaboration case proposed |
| typescript_dto | typescript_dto | Structured TypeScript DTO class |
| resource / service / tool | removed | No alias or replacement |

All IDs fit the approved 24-character bound. Pytest-qualified test IDs identify the framework (and therefore Python) without an unnecessary double prefix; pytest_integration_test is 23 characters. The earlier python_pytest_integration proposal was 25 characters and has been corrected rather than relaxing the approved limit.

**Authority discrepancy:** the conversation recalled worker removal, but [catalog worker row](C:/temp/pgmcp/docs/development/issue460/template-suite-catalog.md:79) and F-14 retain/adapt it. This proposal preserves that Research baseline and asks for explicit confirmation. It does not silently remove Worker or use it as the standard example.

## 5. Responsibilities and boundaries

Concrete package owns its context and class/case rendering. Shared Python/TypeScript bases own language framing/header. Shared patterns only own repeated rendering mechanics. Output profiles own source preflight, not arbitrary application correctness. Generic runtime has no artifact-specific Python dispatch.

## 6. Options and rationale

Reject primitive signature/field strings, a universal code-body escape hatch and recursive language DSL. Choose structured names/types/defaults and narrowly allowed source fragments only where the artifact's Research responsibility includes caller behavior.

## 7. Detailed design

### Core field contracts

| Package | Required content | Optional content and behavior |
|---|---|---|
| python_pydantic_dto | class_name, description | imports, fields; no fields is valid; fields imply at least one example |
| python_pydantic_config | class_name, description, frozen:bool | imports, fields, examples; examples not automatically required |
| python_class | class_name, description | imports, bases, methods; no methods is valid; stubs raise NotImplementedError |
| python_protocol | protocol_name, description | imports, bases, methods; empty marker Protocol allowed; signatures use ellipsis |
| python_adapter | class_name, description, boundary description | explicit dependencies, contract/bases, imports and methods; no invented adapt(), logger or error mapping |
| python_worker | class_name, description, one operation | explicit dependencies and sync/async; no lifecycle/cache/translator assumptions |
| typescript_dto | class_name, description, fields | imports, implements; explicit readonly/optional, constructor from the same field records |
| pytest_unit_test | description, nonempty cases | imports, fixtures, optional class_name; no mandatory class |
| pytest_integration_test | description, collaboration intent, nonempty cases | same test primitives; no manufactured E2E setup |

Every object is closed; arrays are ordered; no implicit caller content from file_name. Required strings are nonblank unless explicit empty source is meaningful. Native identifiers receive language-appropriate lexical/keyword constraints in the package schema/profile contract, not server dispatch.

### Shared definitions with real repeated consumers

- PythonImport: module, names:ordered imported-name/alias records, optional module alias; reject conflicting import forms.
- PythonParameter: name, annotation, optional default (native expression if that specialized signature explicitly allows it).
- PythonSignature: name, description, async:boolean, parameters, returns. Constructor/dependency fields are explicit; do not derive them by parsing descriptions.
- PydanticField: name, annotation, description, optional literal_default or default_factory (mutually exclusive); finite constraints ge/gt/le/lt/min_length/max_length/pattern when supported.
- TypeScriptField: name, annotation, description, optional:boolean, readonly:boolean. Annotation remains intact even with colons in object/function types.
- PytestCase: name, description, async:boolean, fixture_parameters:ordered names, markers:ordered declared native marker expressions, body:nonblank native Python source.
- PytestFixture: name, description, parameters, scope:function|class|module|package|session, autouse:boolean, body:nonblank source.

Names alone do not imply modules/imports. Specialized method-body support stays local to adapters/workers/tests; Generic rejects body, implementation and arbitrary decorators. No broad shared definition forces every package to accept the same fields.

For Pydantic defaults: absent means required field; explicit JSON null is a literal None default; factory is an explicit callable reference with explicit import, never an evaluated string. A boolean required field plus multiple default flags would duplicate contradictory truth, so omit it.

### Literal rendering and source fragments

Current [DTO source](C:/temp/pgmcp/.pgmcp/templates/concrete/dto.py.jinja2) uses JSON text in Python examples. Use one shared Python literal-rendering pattern for JSON-compatible values: true→True, false→False, null→None; recursively preserve strings, lists, mappings and finite numbers without evaluation. Test quotes, slashes and Unicode. This stays suite-owned rendering, not a DTO-specific Python service.

Ordinary descriptions/docstrings/comments are **not** native-source fragments. Shared language rendering must quote/escape ordinary text correctly, including single/double/triple quotes, backslashes, newlines and Unicode. Source syntax broken by a description is a renderer defect, not a caller-source error. The distinction is explicit in schema descriptions and acceptance cases.

JSON Schema can validate the structure of annotation/body fields but cannot prove arbitrary supplied Python/TypeScript parses. The schema descriptions explicitly identify native-source fragments; output syntax/preflight checks validate rendered content. Under enforce, invalid native fragments do not persist. Under report, rejected content may persist with honest findings.

**Promise review:** some Research wording is stronger (“every schema-valid context produces valid source”). Do not silently weaken it. The recommended interpretation is structural first-time-right plus explicit native validation for source fragments; if the owner requires literal schema-only source validity, that affected contract needs an explicit decision before canonical integration, not an invented universal parser.

Human decision 2026-09-11: semantic DTO/configuration example validation is withdrawn. Preserve example authoring/rendering and context-schema shape checks; no example adapter, model execution, hidden context channel, unavailable placeholder or profile requirement. See research.md#example-validation-withdrawal--2026-09-11. This is no longer an open implementation obligation.

### Rendering and profiles

Reuse approved bases; consolidate TypeScript DTO pseudo-pattern into its concrete template.jinja2. No technology folder or per-package patterns directory is added. Python syntax preflight belongs to the proposed python_preflight profile; specialized DTO validation is an explicitly named additional obligation, not all quality checks. TypeScript and text/Markdown profiles are completed with W09's capability inventory, not assumed from extensions.

Contract examples are schema-root examples for complete caller contexts, distinct from the DTO's context field examples (generated model examples). Schema-root examples are optional authoring aids and validated against the contract when supplied. They are **not mandatory permanent contexts per package**, a startup guarantee or a copied server-owned template inventory. Durable synthetic cases exercise shared contracts; targeted real-package examples are justified by the distinct behavior they prove. Do not generate fake production sample classes only to placate gates.

## 8. Control and failure examples

file_name=order_model.py with class_name=PurchaseRecord proves independent decisions. An empty Generic class is valid; an absent Unit case is not. A TypeScript type { id: string; } remains one annotation. A malformed case body passes string shape but fails source preflight. A missing optional collection remains omitted/declared-defaulted, never injected null.

## 9. Migration and removal

Remove resource/service/tool scaffolds, not runtime resources/services/tools. Remove implicit _v2 DTO override and Generic fallback routing. Remove six S1mpleTrader patterns, obsolete agent-hints pattern plus dead imports, and two unreachable test-placeholder patterns. Preserve YAML sources through historical Git references, not active assets. TypeScript behavior moves into its concrete package rather than being discarded.

## 10. Evidence

Use real packaged graph, not hand-copied simplified templates. Cover minimal/rich/omitted/null/empty contexts; every supplied field's semantic render location; filename/symbol independence; no backend imports; no fabricated logging/fixtures/assert True; DTO examples with null/booleans; intact TypeScript complex annotations; exact one-line metadata; negative source preflight and honest unavailable cases.

## 11. Review points

IDs including Worker discrepancy; bounded structured fields; minimum one case for integration; native-source promise; faithful example rendering without model-example validation. These are coherent artifact-family choices rather than individual-field approvals.

## 12. Planning consequences

Concrete family migrations and their public contract evidence retain DI-03 ownership; shared fixture mechanics belong DI-08. Do not create one all-templates migration cycle.

## 13. Traceability

DI-03's thirteen strategy rows → code/document split; F-01 structured items; F-14 portability; F-17 names; F-14A/B removals; I-13 valid basis vs finished implementation.

## 14. Related documentation and history

Next: [W08 document/tracking](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/08-document-tracking-artifacts.md).  
0.1, 2026-09-10: temporary proposal from catalog and direct renderer/test inspection.
