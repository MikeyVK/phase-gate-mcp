<!-- pgmcp:v1 id=design pv=1.0.0 pf=YApsrGTQgBUKFez2 sf=FAN5Vr-4vcbMMjZ2 -->

# ASCII Python identifier contract — Design (#486)

**Status:** DESIGN COMPLETE — independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-05

## Problem Statement

The approved ASCII clean break must remove large Unicode lexical/NFKC patterns across eight shipped consumers while preserving supported ASCII grammar and Unicode content.

## Functional Requirements

- Admit only ASCII Python structured identifiers, including declarations, method/function/fixture names, parameters, model fields, imported symbols/aliases, module segments, fixture decorators and ModelField.default_factory dotted names.
- Retain full-string admission, Python hard-keyword exclusion, relative imports, star-import restrictions, reserved names and discovery prefixes.
- Preserve Unicode prose, literals/defaults/examples, logging text, raw bodies, markers and type/base expressions with their existing native validation.

## Nonfunctional Requirements

- Keep admission in the shipped schema suite and reuse shared definitions; no runtime policy branch or resolver/presentation change.
- Provide durable public loader/validator/renderer coverage, minimal/populated family evidence and actual schema-size measurements.
- Retain architecture/public-test boundaries and targeted Python quality checks.

## Constraints

- Research Approved Strategy is binding: no migration bridge, Unicode fallback, normalization or transliteration.
- Owner reports no previous non-ASCII scaffolded identifiers; no automated repository audit is asserted.
- Existing manifest identities, output templates, configured native-check policy and API envelopes remain unchanged.

## Options

### 1. Compact shared schema definitions

Replace lexical Unicode patterns and unreachable equivalence exclusions within the existing dependency graph.

**Pros:**

- One existing authority per concern; all consumers inherit the boundary.
- Compact resolved schema without new runtime behavior.

**Cons:**

- Dotted and relative module grammars still require separate schema patterns; native keyword list must remain complete.

### 2. Runtime identifier filter

Validate names in renderer/service code.

**Pros:**

- Procedural validator can inspect native syntax.

**Cons:**

- Duplicates schema admission, obscures discovery contract and expands architectural blast radius.

### 3. Independent consumer patterns

Inline compact admission into each package.

**Pros:**

- Local readability.

**Cons:**

- Duplicated lexical contract and future drift across eight packages.

## Decision

Use compact shared ASCII schema definitions and the existing consumer composition. Keep consumer-specific semantic restrictions at their current owner; simplify only unreachable Unicode-equivalence branches.

## Rationale

The payload debt is lexical schema content. Existing public loaders, validator and renderer already enforce these assertions; altering them would add responsibility without evidence. The selected direction directly implements the owner-approved clean break.

## Questions

## Production Design

Shared Symbol owns a nonempty ASCII lexical identifier and hard-keyword exclusion. DottedSymbol owns dot-separated Symbols and keyword-free segments. FromImport.module separately admits leading relative dots with an optional dotted module and requires at least one character. Symbol references continue to cover all structured fields. ModelField.default_factory and Fixture.decorator remain DottedSymbol consumers; they are not arbitrary expression fields. ModelField keeps leading-underscore exclusion and exact reserved enum; InstanceParameter forbids exact self; NonConstructorMethod forbids exact __init__; PytestClassName requires Test. Plain-class signature dunder exclusion remains in python_class/context.schema.json. Text/Prose/Body/TypeText/JSON defaults/examples and shared output templates are unchanged.

## Test Design

Adapt test_shared_python's native lexical oracle to `name.isascii() and name.isidentifier() and not keyword.iskeyword(name)`, exercising ASCII starts/continuations, all hard keywords, soft keywords, non-ASCII letters/combining/fullwidth/astral forms and final-newline/suffix rejection. Add selected shared-definition regression cases through TemplateContractLoader + Draft202012Validator for dotted/relative imports, aliases/star combinations, parameters/methods/fixtures, field/default_factory and reserved/discovery restrictions. Exercise all eight actual shipped schemas via the existing isolated DeliveredTemplate helper with accepted ASCII and rejected Unicode declarations, populated identifiers and preserved Unicode prose/literals/raw code/types. Retain AST/compile and family native syntax/Pytest evidence. Replace both pytest-family blocked-composition Unicode acceptance contexts with rejection; preserve useful native ASCII discovery evidence and remove obsolete normalization ceremony. Avoid new fixture frameworks, private access, implementation-mirroring assertions or production logic in tests. A public resolved-schema size bound protects discovery payload against reintroducing huge patterns; compare observed resource serialization exactly to Research baseline, without hardcoding current equality.

## Contracts

### Lexical schema contracts

| Definition | Positive contract | Negative contract |
|---|---|---|
| Symbol | `^[A-Za-z_][A-Za-z0-9_]*(?![\\s\\S])` | Existing hard-keyword enum; soft keywords `match`, `case`, `type` remain valid |
| DottedSymbol | `^[A-Za-z_][A-Za-z0-9_]*(?:\\.[A-Za-z_][A-Za-z0-9_]*)*(?![\\s\\S])` | Existing per-segment hard-keyword pattern |
| FromImport.module | `^\\.*(?:[A-Za-z_][A-Za-z0-9_]*(?:\\.[A-Za-z_][A-Za-z0-9_]*)*)?(?![\\s\\S])`, minLength 1 | Existing per-segment hard-keyword pattern; no trailing module dot |
| ImportedName / aliases | Symbol | Star only as sole unaliased FromImport name |
| ModelField.default_factory / Fixture.decorator | DottedSymbol | No calls, whitespace, Unicode segments or keywords |

The negative end assertion requires absolute end of input; final newlines/CR, suffixes and whitespace cannot match.

### Consumer-specific contracts

| Concern | Retained restriction |
|---|---|
| InstanceParameter | `not: {const: self}` |
| NonConstructorMethod | `not: {const: __init__}` only where a separate constructor exists |
| ModelField.name | No leading `_`; exact reserved names `model_config`, `Config`, `Field`, `model_dump`, `model_dump_json`, `model_validate`, `model_validate_json`, `model_validate_strings`; prefixed variants such as model_dump_custom remain valid |
| Plain class Signature.name | Exclude full dunder names with `^__.*__(?![\\s\\S])` |
| TestCase.name | Existing `^test_` plus Symbol |
| PytestClassName | `^Test` plus Symbol |

Keep class/protocol/adapter/worker distinctions: a concrete __init__ without a supplied constructor remains admitted where currently supported.

## Flow

Caller context → existing resolved package schema → ConfigValidator admission → existing shared Jinja rendering → configured native syntax check/persistence. Invalid identifiers fail as existing context-validation failures. No state, external network call, auto-rewrite or identifier normalization is introduced.

## State and Failures

No new state or error envelope. Schema rejection remains the early boundary. Free invalid raw code/type expressions continue to fail the existing native syntax check rather than being reclassified as invalid identifiers. Unicode-equivalent reserved spellings are rejected by ASCII admission before they need normalization-specific guards.

## Preservation

Every supported ASCII contract remains stable except the explicitly approved rejection of non-ASCII structured names. Existing metadata/provenance, ordering, frozen DTO/config output, injected self/constructors, native syntax failures and caller-owned content retain their prior evidence. Python built-in/native syntax is an independent oracle for ASCII lexical and rendering behavior; schema output equality is not sufficient evidence alone.

## Transition and Cleanup

Direct schema cutover; no bridge or migrated-file rewriting. Remove Unicode lexical ranges/NFKC-equivalence branches and stale comments only on affected Python schemas. Adapt obsolete accepting tests. No release version or packaged generated assets are rebuilt as part of this issue; release assembly consumes the configured source suite through the existing packaging procedure.

## Validation

### ASCII structured admission across every consumer

**Method:** Focused delivered-family and shared schema regression tests through public interfaces; include default_factory/decorator and import variants.

**Expected Result:** ASCII accepted; Unicode and keyword/reserved counterexamples rejected.

### Unicode content preservation

**Method:** Validate/render populated class, DTO and pytest/body contexts; AST literal/docstring/type round trips and existing native family tests.

**Expected Result:** Unicode data unchanged and valid raw content remains accepted.

### Reduced discovery payload

**Method:** Compare scaffold_schema resource text using Unicode codepoints and pattern codepoints with Research baselines; named tokenizer only if available.

**Expected Result:** All eight schemas materially smaller; no token, speed or quality claim without measurement.

### Required integration evidence

**Method:** Focused tests during implementation; complete configured suite in Validation, configured arguments retained and adequate timeout; targeted format/lint/Pyright on changed test code; current Markdown links.

**Expected Result:** Native complete results with failures/warnings/skips explicit.

## Risks

### Accidentally applying ASCII to raw type/body values

Separate schema contracts and Unicode-preservation tests.

### Weakening consumer exclusions

Retain all ASCII negative/positive boundaries and native family cases.

## Planning Consequences

One cohesive contract cutover is appropriate; planning owns RED/GREEN/REFACTOR timing, commit boundaries and later validation/documentation gates. No unresolved target-structure or human-strategy choice remains.

## Related Documents

- [Research and Approved Strategy](<research.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-05 | @imp designer | Define compact shared ASCII admission and preservation evidence. |
