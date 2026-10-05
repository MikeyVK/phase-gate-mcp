<!-- pgmcp:v1 id=planning pv=1.0.0 pf=CscfYyDLqj0OeHml sf=FAN5Vr-4vcbMMjZ2 -->

# ASCII Python identifier contract — Planning (#486)

**Status:** PLANNING COMPLETE — independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-05

## Scope In

Shared Python definitions, plain-class dunder schema, three affected shared/pytest regression files, eight delivered-family consumers, current scaffolding reference and phase evidence.

## Scope Out

Resolver/runtime/presentation/cache redesign, TypeScript policy, normalization/bridges, generated packaged assets/release assembly, historical workflow-document reconciliation.

## Summary

One cycle changes the schema contract at its existing owner and adapts durable tests together. RED is justified by the uncovered ASCII-only admission obligation, not imposed on unrelated behavior-preserving structure. Design 88645a4f and Research d426001e received independent QA GO.

Validation selection: run_tests(scope='configured', timeout_seconds=1200), without targets or native argument overrides, retains configured coverage and workers. Run run_checks(scope='branch', profile='markdown_link_review', timeout_seconds=300) over the complete branch inventory. Reuse fresh targeted python_format/python_lint/python_pyright evidence for all changed Python tests unless invalidated; no production Python change is planned, so strict production-scoped Mypy has no changed target. Branch scope sends every changed path to selected native checks; do not send Markdown/JSON to Python type-checkers or reinterpret their resulting errors as passes.

## Dependencies

- Approved Strategy recorded in issue/Research; independent Design GO at 88645a4f.
- Existing public TemplateContractLoader, ConfigValidator and DeliveredTemplate helper; configured native Python/pytest adapters.
- First push to origin remains pending explicit trusted-destination approval after automatic review rejection; local execution continues, no egress workaround.

## Risks

### Stale immutable running catalog would produce false before/after claims.

Inspect resource identity and refresh via supported restart_server; use fresh delivered loader tests as separate evidence.

### Public push/PR is blocked by automatic egress review.

Await pending explicit human destination authorization; preserve local commits and report blocker, never route around denial.

## Milestones

- Independent Planning GO → cycle 1.
- Independent Implementation GO → Validation.
- Independent Validation and Documentation GO → Ready.

## Work Units

### C\_ASCII — Compact ASCII schema cutover

**Goal:** Implement the owner-approved lexical boundary while preserving all other supported contracts.

**Cycle Number:** 1

**Owner:** @imp implementer

#### Scope In

Production/config seams: shared/definitions/python.schema.json and python_class/context.schema.json. Test seams: test_shared_python.py, test_pytest_unit_test.py, test_pytest_integration_test.py; existing other six family files are executed without unnecessary edits.

#### Scope Out

No new fixture framework, source parser, runtime filter, resolver or template output changes.

#### Deliverables

##### D\_ASCII\_SHARED

Shared Python identifiers, dotted/relative modules, decorators/default_factory and exact ASCII reserved-name guards implement the approved contract.

**Validates:**

**Type:** file_exists

**File:** ".pgmcp/template_suite/shared/definitions/python.schema.json"

##### D\_CLASS\_DUNDER

Plain-class dunder exclusion retains its ASCII restriction and removes Unicode-equivalence alternatives.

**Validates:**

**Type:** file_exists

**File:** ".pgmcp/template_suite/python_class/context.schema.json"

##### D\_REGRESSION

Durable public-boundary shared and all-eight shipped-consumer tests cover ASCII acceptance, Unicode rejection, imports/reserved names and Unicode content preservation.

**Validates:**

**Type:** contains_text

**File:** "tests/mcp_server/integration/templates/test_shared_python.py"

**Text:** "test_shipped_python_ascii"

##### D\_CLEANUP

Both pytest-family obsolete Unicode class acceptance cases are migrated to rejection; no production helper, resolver or output-template change.

#### Exit Criteria

D_ASCII_SHARED, D_CLASS_DUNDER, D_REGRESSION and D_CLEANUP implemented; focused nine-file family suite completes with intended ASCII/content/native outcomes; changed test files pass format/lint/Pyright; actual discovery payload materially reduced for all eight packages; independent implementation review requested.

#### Obligations

- RED: adapt the native Symbol oracle and obsolete Unicode-accepting contexts; add public shared-definition cases and eight-package ASCII/rejection/content/size coverage. Run focused tests and verify failures identify intended new ASCII contract; commit implementation/red, cycle 1.
- GREEN: change only shared ASCII lexical patterns and exact reserved guards plus class dunder schema. Run all nine Python/pytest family files; commit implementation/green, cycle 1, using refactor commit type because this is a schema refactor.
- REFACTOR: remove obsolete normalization-only test ceremony and stale schema comments as planned, preferably with cutover edits. Apply only needed native formatting fixes; run changed Python format/lint/Pyright and invalidated focused tests. Commit implementation/refactor only if cleanup changes remain.
- Before exposing updated live scaffold/schema evidence, refresh the MCP catalog via restart_server if its immutable startup catalog is stale; do not patch resolver/cache/runtime. Confirm new package identity/resource, then measure all eight resource strings with Unicode codepoints and pattern lengths using the same serialization as Research.
- Representative minimal and populated scaffolds are proven through the existing delivered-family public renderer plus configured native syntax/Pytest checks. Existing AST/compile/provenance/literal ordering/frozen model tests remain valuable. Use temporary isolated output rather than adding throwaway repo artifacts.
- Pre-commit reality check: evidence must prove every deliverable and preservation boundary; no self-issued GO or tautological assertions.

#### Verification

##### New ASCII boundary and grammar

**Method:** run_tests(scope='targets', targets=[tests/mcp_server/integration/templates/test_shared_python.py]) for RED; all nine family files for GREEN and invalidated cleanup.

**Expected Result:** Intended new-contract failures in RED; no failures in final focused run. ASCII lexical oracle uses isascii/isidentifier/keyword; imports include relative dots, star and keyword segments.

##### Python test quality

**Method:** run_checks(scope='targets', targets=[three changed test files], checks=['python_format','python_lint','python_pyright'], timeout_seconds=300).

**Expected Result:** All complete and passed; strict Mypy is production-scoped and no production Python file changes are planned.

##### Public discovery payload

**Method:** Fresh scaffold_schema on all eight IDs; count codepoints and pattern codepoints as in Research. Existing active virtualenv has no tiktoken; no package installation or token estimate required.

**Expected Result:** Material reduction for all eight; public resolved-schema regression bound below 25000 codepoints per package, not exact current-size equality.

#### Stop Conditions

- Stop and reopen strategy if ASCII admission requires content filtering, runtime policy or a compatibility bridge.
- Stop if consumer inventory differs, supported ASCII behavior is weakened, native evidence is incomplete or new architecture/test helper coupling is needed.
- Do not enter Validation until independent QA reviews final cycle; no forced transitions.

## Phase Deliverables

### Validation

#### V\_FULL

One complete configured native test suite and branch gates with exact outcomes in Validation.

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue486/validation.md"

#### V\_METRICS

Before/after all-eight resource codepoint and pattern measurements, tokenizer limitation explicit; no latency/model-quality claim.

**Validates:**

**Type:** contains_text

**File:** "docs/development/issue486/validation.md"

**Text:** "Schema size"

### Documentation

#### DOC\_BOUNDARY

Current scaffolding reference explains ASCII structured names, preserved Unicode content and clean-break rediscovery.

**Validates:**

**Type:** contains_text

**File:** "docs/reference/tools/scaffolding.md"

**Text:** "ASCII"

#### DOC\_EVIDENCE

Documentation report indexes active surfaces, unchanged historical material, fresh links and QA caveats.

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue486/documentation.md"

## Related Documents

- [Design](<design.md>)
- [Research](<research.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-05 | @imp planner | Define one cohesive contract cycle and phase-owned verification. |
