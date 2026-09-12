<!-- docs\development\issue460\design-integration-review.md -->
<!-- template=design version=5827e841 created=2026-09-12T14:51Z updated= -->
# Issue 460 — Design Integration Review and Exact-Path Accounting

**Status:** DESIGN INTEGRATED — INDEPENDENT CLOSURE RECHECK REQUIRED  
**Version:** 0.4
**Last Updated:** 2026-09-12

---

## Purpose

Integration evidence and bounded Design closeout accounting.

## Scope

**In Scope:**
Registered inputs, operation/attachment transport, process capture, consumer output projection, distribution/configuration seams and catalog dispositions.

**Out of Scope:**
New product roles, Research amendments, implementation cycles, native execution, phase advancement and independent QA verdicts.

## Prerequisites

Read these first:
1. Frozen Research and human-approved Design contracts.
---

## 1. Context & Requirements

### 1.1. Problem Statement

Individually approved designs still need exact cross-package transport, capture, presentation and path dispositions before a combined independent review.

### 1.2. Requirements

**Functional:**
- [ ] Preserve the frozen Research strategy and approved consumer semantics.
- [ ] Record exact integration interfaces, owners, evidence and unresolved decisions.
- [ ] Account for the existing catalog and affected supplemental dependencies without changing the Research census.

**Non-Functional:**
- [ ] Typed immutable boundaries; no DTO-specific presenter logic.
- [ ] No production/test implementation or planning cycles.
- [ ] Separate producer findings from independent QA authority.

### 1.3. Constraints

- No temporary workshop or probe file is canonical authority.
---

## 2. Design Options

Keep interface definitions with their existing canonical owners and use one integration
index for evidence and exact-path dispositions. Duplicating schemas in this index or
marking all packages complete from census totals would create competing authority.
---

## 3. Chosen Design

**Decision:** Use canonical package owners for interface definitions and this document only for the integration evidence, exact-path disposition index and review navigation.

**Rationale:** Counts and local workshop approval do not prove that independently designed interfaces compose. A single issue-local review index exposes gaps without copying product authority.

### 3.1. Integration Findings and Disposition

This is producer-owned source inspection, not independent QA or runtime evidence.
Research remains frozen. The existing catalog contains 126 consumers plus two
governing sources and 151 unique tests/helpers. Family routing is valid ownership
input, but does not replace a source-based disposition or Planning cycle assignment.

| Seam | Finding | Canonical owner / disposition |
|---|---|---|
| Registered and lazy input schemas | Current input decorator rebuilds its schema from the static model, independently of catalog admission. | DI-01/05: prepared immutable input contract in [suite resolution](design-suite-resolution.md), shared by exposure and execution. |
| Schema attachments | Operation DTOs and MCP attachments need an explicit typed transport without teaching the presenter error DTO classes. | [Shared contracts](design-shared-contracts.md) §5.5 defines normalization and attachment ownership. |
| Required nulls | Current cache serialization excludes nulls indiscriminately; this loses required-null facts from closed output contracts. | Shared contracts §5.6 requires schema-aware serialization; implementation/resource-read evidence remains outstanding. |
| Process capture | Existing bounded-capture prose does not itself establish a field carried by every attempted invocation into the cache. | DI-05 now defines ProcessCapture on shared invocation results and attempted public records; DI-04 consumes that same type. Resource-read proof remains required. |
| Public result presentation | Current presenter collection admission accepts a concrete model, not the test/fix discriminated result unions. Domain failure cannot rely on the global success=false fallback. | Human-approved and consolidated: DI-05 §13.1 concrete public records; Shared §11.1 declarative projection and generic strict/nullable annotation admission. Implementation conformance remains required. |
| Exact operation error details | DI-04 mutation and DI-05 run_checks enumerate error codes but did not map every code to an exact closed details type/null. | Human-approved and consolidated: DI-04 §7.1 and DI-05 §13.1 exact matrices; preserve manager ownership and existing success/isError semantics. Independent review requested. |

The two former output-contract gaps were closed by explicit human approval on
2026-09-12 and consolidated into the canonical owners above. No duplicate summary
fields, native parsers or DTO-specific presenter framework were added. Producer
consolidation is not independent full-Design approval.

### 3.2. Exact Test/Helper Dispositions

The following 151 entries follow frozen catalog order. Each was inspected for test
names, relevant setup and assertions. They classify the affected boundary, not every
assertion or every unrelated quality defect in a mixed file. `remove` retires the
old construction only after its stated prerequisites; it never authorizes silently
discarding the durable claim. `compliant` is limited to the inspected boundary.
Planning must assign concrete cycles and rollback/evidence boundaries per path;
these Design owners are not cycle assignments. No aggregate remaining-tests cycle.

#### Catalog rows 1–50

Source inspection covered each file's relevant test names, setup and assertions, with
additional contextual reading of the broad helpers, strict-schema, safe-edit, path and
PR-locking tests. This is a bounded Design classification, not an assertion-by-assertion
semantic proof or executed evidence. Architecture `compliant` applies only to the
inspected, affected boundary; unrelated debt is not endorsed. Behavior `remove` retires
the old suite, not the useful claims explicitly transferred in the prerequisite column.

| Exact path | Primary owner | Behavior | Architecture | Public proof boundary / durable claim and source basis | Removal prerequisite |
|---|---|---|---|---|---|
| `tests/mcp_server/acceptance/test_issue56_acceptance.py` | DI-04 | remove | remove | Public scaffold-to-persisted-file outcome. Lines 21–115 duplicate Design/DTO examples and exact prose through the broad harness. | DI-04 public scaffold/persistence acceptance covers file/result claims; DI-03 owns actual package content acceptance. |
| `tests/mcp_server/config/test_component_registry.py` | DI-02 | remove | remove | Catalog lookup, unknown ID, repeated loading and schema constraints. Lines 19–23 infer repository config root; lines 35–89 duplicate concrete IDs. | Canonical loader/catalog tests cover lookup, invalid configuration and references using isolated roots; no second config fixture authority. |
| `tests/mcp_server/config/test_project_structure.py` | DI-04 | adapt | adapt | Public location/directory-policy lookup and cross-reference validity. Lines 27–46 infer config roots; lines 55–75 encode Backend directories and concrete IDs. | None; migrate retained directory/operation-policy responsibilities under DI-04's field/consumer mapping before old layout assertions disappear. |
| `tests/mcp_server/fixtures/artifact_test_harness.py` | DI-08 | replace | replace | Support for public scaffold tests. Lines 47–58 mutate environment/CWD; lines 64–246 duplicate schema/config authority; fixture graph constructs broad defaults. | Narrow injected builders and isolated-root support; trace every fixture request and plugin registration before retiring helpers. |
| `tests/mcp_server/integration/mcp_server/test_scaffold_tool_execute_e2e.py` | DI-04 | replace | replace | Tool result corresponds to an actual persisted artifact. Lines 23–119 repeat two hardcoded Design/DTO examples and prose assertions. | Consolidated public scaffold-to-file evidence using DI-08 support; DI-03 package tests retain actual content contracts. |
| `tests/mcp_server/integration/mcp_server/test_server_tool_registration.py` | DI-05 | adapt | adapt | Public names, obsolete-name absence and frozen schema exposure. Lines 15–57 unwrap `_tool` and compare classes; lines 87–94 already use public names. | None. Preserve unrelated cycle/search-removal assertions; adapt affected registration/schema slice through DI-05 §7.6. This clarifies the catalog's older Exclude wording. |
| `tests/mcp_server/integration/mcp_server/validation/test_safe_edit_validation_integration.py` | DI-04 | replace | replace | Complete-content checks control enforce/report persistence. Lines 30–32 default-construct tool; lines 61–69 infer expected outcome from file existence; old strict/tier claims do not establish their named behavior. | Deterministic injected profile outcomes prove no-write on enforce failure, report writes, operational failures and retained edit operations. |
| `tests/mcp_server/integration/test_artifact_e2e.py` | DI-04 | remove | remove | Scaffold writes nonempty content at its reported location. Lines 22–124 duplicate two artifact examples and hermetic-template prose. | Consolidated DI-04 tool-to-filesystem acceptance plus DI-03 actual-package coverage. |
| `tests/mcp_server/integration/test_concrete_templates.py` | DI-03 | replace | replace | Retained actual package roots produce declared content. Lines 123–238 snapshot old headers/import labels; lines 254–435 mandate source-project worker lifecycle/cache behavior. | CODE-E01/02/05/06/10 and document-root coverage; explicit removal proof for Resource/Service/Tool and source-project assumptions. |
| `tests/mcp_server/integration/test_config_error_e2e.py` | DI-02 | adapt | compliant | Public loader raises actionable ConfigError and identifies source. Lines 20–30 use an isolated explicit config path and public loader; lines 33–85 verify errors. | None; adapt invalid declarations to V3 manifest/schema/reference contracts while preserving bounded source diagnostics. |
| `tests/mcp_server/integration/test_document_templates.py` | DI-03 | remove | remove | Document fields, omission, links, concepts and Planning projection. Direct Jinja fixtures and prose/layout assertions; lines 192–227 retain obsolete dual success_criteria representations. | DOC-E01–06/08/10; approved operational exit_criteria replaces old union forms, not a compatibility obligation. |
| `tests/mcp_server/integration/test_exception_propagation.py` | DI-04 | adapt | replace | Unknown template and invalid context produce actionable public failures. Lines 23–73 assert layer-specific exceptions and hardcoded Design fields through broad harness. | None; injected admitted catalog/context and public operation failures, retaining reason/schema recovery without duplicate layer assertions. |
| `tests/mcp_server/integration/test_metadata_e2e.py` | DI-02 | replace | replace | Persisted first-line provenance is readable; invalid/missing header gives no recognition. Lines 73–81 require old timestamps/two lines; lines 193–254 require mutable TemplateRegistry. | DI-02 id/pv/pf/sf reader/writer agreement and invalid-header fallback; DI-04 retains temporary/location-result proof separately. |
| `tests/mcp_server/integration/test_pr_status_lockdown.py` | DI-08 | keep | compliant | Existing configured PR-lock enforcement and merge escape hatch. Public EnforcementRunner uses explicit config, state reader and PR-status double, lines 117–141. | None; preserve excluded behavior and adapt shared setup only if dependencies change. Fixed 17-tool inventory and unrelated legacy debt are outside this bounded assessment, not endorsed for copying. |
| `tests/mcp_server/integration/test_provenance_e2e.py` | DI-02 | replace | replace | Artifact evidence identifies selected package and source suite. Lines 61–111 parse obsolete two-line timestamps; lines 194–210 expect eight-character hashes. | DI-02 id/pv/pf/sf, generation inclusion/exclusion and lateral isolation evidence; DI-06 independently proves operational hashes, not pf/sf, authorize upgrade comparison. |
| `tests/mcp_server/integration/test_scaffold_validation_e2e.py` | DI-01 | adapt | replace | Invalid context carries discovery's complete schema; success does not attach schema; envelope remains separate. Lines 28–106 use shared harness/old fields; success-schema test name does not actually assert schema. | None; W06 public embedded-resource parity, with DI-04 operation/persistence contribution. |
| `tests/mcp_server/integration/test_smoke_all_types.py` | DI-03 | replace | replace | Every retained actual package has accepted minimal/optional examples and valid output. Lines 51–66 mutate environment/CWD; hand-maintained context map precedes nonempty-file checks at 304–342. | CODE-E01 and DOC-E01 real-package acceptance using isolated DI-08 support; no copied template/context registry as alternative authority. |
| `tests/mcp_server/integration/test_strict_input_validation_response.py` | DI-01 | adapt | replace | Registered tool rejects extra input and returns whole-tool schema resource. Lines 70–76 call private bootstrap stages; lines 105/129 patch jsonschema.validate. | None; public registered/decorated invocation with real validation; preserve schema://validation distinct from selected-context identity. |
| `tests/mcp_server/integration/test_template_missing_e2e.py` | DI-02 | replace | replace | Missing/unresolved dependencies are rejected at catalog construction. Lines 94–96 replace manager/scaffolder registries after construction, then expect first-use failure. | Startup admission tests over incomplete package roots; on-use tests only for failures legitimately discovered after admission. |
| `tests/mcp_server/integration/test_tool_error_contract_e2e.py` | DI-04 | replace | replace | Public scaffold failures preserve actionable typed facts. Lines 53/78 replace manager behavior with exception side effects; repeated exception types duplicate coverage. | Consolidated operation/error projection using injected failing boundaries, not patched manager methods. |
| `tests/mcp_server/integration/test_tool_error_e2e.py` | DI-04 | remove | remove | Unknown-template failure preserves error context, lines 19–36; duplicates canonical public failure suite. | Consolidated DI-04 unknown-template/invalid-context/operational-error evidence. |
| `tests/mcp_server/integration/test_validation_policy_e2e.py` | DI-04 | replace | replace | Findings and validation policy independently govern persistence. Lines 37–231 hardcode code-block/doc-warning defaults and custom template forms. | Injected pass/fail/unavailable plus enforce/report and operational-failure cases; actual file/result assertions without language dispatch. |
| `tests/mcp_server/scaffolding/test_concrete_code_templates.py` | DI-03 | remove | remove | No durable requirement for particular tier imports or GUIDELINE metadata. Lines 78–112 inspect source import strings/enforcement tokens. | CODE-E01/09/10 cover actual resolved output and declared profiles; obsolete metadata removal explicit. |
| `tests/mcp_server/scaffolding/test_concrete_test_integration.py` | DI-03 | replace | replace | Integration-test template supports explicit fixtures, imports, signatures and sync/async cases. Direct Jinja/source assertions; line 120 infers asyncio marker. | CODE-E01/02/05/07/09; no automatic marker/plugin/import inference or fabricated passing test. |
| `tests/mcp_server/scaffolding/test_concrete_test_unit.py` | DI-03 | replace | replace | Unit-test template has real caller-selected cases and valid signatures/fixtures. Direct Jinja/tier assertions; lines 120–121 infer async marker; lines 132–134 snapshot AAA prose. | CODE-E01/02/05/07/09; optional fixture/marker behavior remains explicit. |
| `tests/mcp_server/scaffolding/test_doc_template_pattern_imports.py` | DI-03 | remove | remove | No retained exact seven/six-pattern import-count contract; lines 21–75 inspect source imports only. | DI-02 graph missing/cycle/reachability and DOC-E01 actual roots; no macro-count replacement test. |
| `tests/mcp_server/scaffolding/test_doc_template_rendering.py` | DI-03 | replace | replace | Caller document fields/links survive schema-to-render. Direct Jinja fixture; lines 52–204 snapshot headings, universal TDD and history prose. | DOC-E01–06/10 preserve semantic presence, links and operational projection without prose snapshots. |
| `tests/mcp_server/scaffolding/test_tier1_base_document.py` | DI-03 | remove | remove | No independent public contract for block names. Lines 25–71 assert purpose/scope/prerequisite/history source blocks. | DOC-E01/02 actual document output and DI-02 graph; no block-name replacement obligation. |
| `tests/mcp_server/scaffolding/test_tier3_document_patterns.py` | DI-03 | remove | remove | File-existence inventory alone is not retained behavior; lines 22–67 include removed agent hints. | DOC-E01 retained roots and DI-02 dependency resolution; approved obsolete patterns absent. |
| `tests/mcp_server/scaffolding/test_tier3_pattern_python_assertions.py` | DI-03 | remove | remove | Removed empty placeholder has no public functionality. Lines 52–100 test metadata/changelog, no macros and empty output. | Approved placeholder removal; CODE-E07 retains caller-owned test content, not a recreated assertions helper. |
| `tests/mcp_server/scaffolding/test_tier3_pattern_python_async.py` | DI-03 | adapt | replace | Explicit async signatures remain supported. Lines 44–97 check macro names, fixed imports and rendered tokens. | CODE-E05/07 explicit async signatures and caller-owned imports before macro-level cases retire; no inferred async-context-manager feature. |
| `tests/mcp_server/scaffolding/test_tier3_pattern_python_di.py` | DI-03 | remove | remove | Removed source-project DI: WorkerInitializationError, strategy_cache and capability assignments, lines 96–109. | Approved removal and CODE-E06/10 absence of source-project dependencies; no retained operational framework. |
| `tests/mcp_server/scaffolding/test_tier3_pattern_python_error.py` | DI-03 | remove | remove | Removed source-project error macros, lines 81–89; no retained generic exception-wrapper contract. | Approved removal and CODE-E06/10 absence proof. |
| `tests/mcp_server/scaffolding/test_tier3_pattern_python_lifecycle.py` | DI-03 | remove | remove | Removed IWorkerLifecycle/strategy_cache initialize/shutdown macros, lines 82–90. | Approved removal; CODE-E06 retains explicit portable worker content only. |
| `tests/mcp_server/scaffolding/test_tier3_pattern_python_log_enricher.py` | DI-03 | remove | remove | Removed LogEnricher/event taxonomy, lines 111–137. | Approved removal and CODE-E06/10; ordinary opt-in logging proved separately. |
| `tests/mcp_server/scaffolding/test_tier3_pattern_python_logging.py` | DI-03 | adapt | replace | Explicit caller-selected logging remains renderable. Lines 61–79 inspect macro declarations/fixed getLogger/info tokens. | CODE-E06 opt-in versus omitted logging through actual packages before macro assertions retire. |
| `tests/mcp_server/scaffolding/test_tier3_pattern_python_mocking.py` | DI-03 | adapt | replace | Caller-declared testing imports/doubles remain expressible. Lines 77–128 mandate all unittest.mock imports and macro topology. | CODE-E02/07 explicit imports/fixture content; no forced all-mock import set. |
| `tests/mcp_server/scaffolding/test_tier3_pattern_python_pydantic.py` | DI-03 | adapt | replace | DTO/config constraints and explicitly authored fields/defaults. Lines 92–110 mix fixed Pydantic tokens with source-project Signal factory/converter. | CODE-E03/04 distinguish DTO/config policy and explicit values; remove hidden ID/validator inference. |
| `tests/mcp_server/scaffolding/test_tier3_pattern_python_pytest.py` | DI-03 | adapt | replace | Explicit pytest content/imports. Lines 71–126 test macro importability and automatically included pytest/Path. | CODE-E02/07 actual unit/integration packages; no macro-name or unconditional-import promise. |
| `tests/mcp_server/scaffolding/test_tier3_pattern_python_test_fixtures.py` | DI-03 | remove | remove | Orphan macro removed; fixture scope/autouse/params remain useful declared capabilities. Lines 67–112 exercise them through direct Jinja. | Remove orphan source; CODE-E07 covers approved fixture fields, including combined options, through actual packages; no incidental auto/QualityState preservation. |
| `tests/mcp_server/scaffolding/test_tier3_pattern_python_test_structure.py` | DI-03 | remove | remove | AAA comment text/macro counts are not durable behavior, lines 67–149. | CODE-E07 retains caller-selected test structure, not comment wording/macro shape. |
| `tests/mcp_server/scaffolding/test_tier3_pattern_python_translator.py` | DI-03 | remove | remove | Removed Translator/get_param_name conventions, lines 84–95. | Approved removal and CODE-E06/10 no implicit project Translator. |
| `tests/mcp_server/scaffolding/test_tier3_pattern_python_typed_id.py` | DI-03 | remove | remove | Removed project ID generator defaults, lines 79–85. | Approved removal; CODE-E03 retains explicitly supplied factories/defaults, never automatic typed-ID imports. |
| `tests/mcp_server/scaffolding/test_tracking_templates.py` | DI-03 | adapt | replace | Conventional commits, explicit PR/issue content, refs/checklists/deferred state. Direct Jinja/existence fixtures; lines 249–261 retain obsolete absent-deferred behavior. | None; DOC-E01/02/05/09/11 actual tracking semantics, explicit none/populated deferred state replaces omission. |
| `tests/mcp_server/test_design_e2e.py` | DI-03 | remove | remove | Requirements/options/rationale/links remain; lines 100–181 snapshot old provenance, headings, positions and sample text. | DOC-E01–05/10 actual Design content; DI-02 separately owns provenance. |
| `tests/mcp_server/test_design_template.py` | DI-03 | remove | remove | Caller values and optional open-question omission, lines 178–229, remain useful; exact sections/tables/enforcement metadata are obsolete authority. | DOC-E01/02/03/10 before duplicate suite removal. |
| `tests/mcp_server/test_scaffolder_output_path_validation.py` | DI-04 | adapt | replace | Explicit input/path-policy failures versus configured/temporary persistence. Lines 38–39 monkeypatch filesystem method; positive cases swallow arbitrary failures. | None; injected filesystem and exact expected success/error/no-write under file_name/target_path policy; no broad exception swallowing. |
| `tests/mcp_server/test_support.py` | DI-05 | adapt | adapt | Preserve unrelated builders while splitting execution/scaffold/metadata support. Lines 427–525 fallback-load configs/construct legacy managers and auto-state; lines 541–548 derive settings from environment. | Trace helper imports; narrow role doubles/builders and explicit roots before retirement. DI-08 architecture, DI-04 scaffold behavior and DI-02 metadata contribute. |
| `tests/mcp_server/test_template_registry.py` | DI-02 | remove | remove | Historical mutable registry explicitly retired. Lines 85–115 migrate YAML/delete source; lines 121–333 persist/current-index/hash-chain semantics. | Production registry/read/write/import removal proved; pf/sf tests must not recreate history storage or migration. |
| `tests/mcp_server/test_tier0_conditional_header.py` | DI-02 | remove | remove | Path-dependent one/two-line header switches retired. Lines 39–148 select compact versus path/timestamp layout. | DI-02 first-line id/pv/pf/sf reader/writer agreement independent of target, no created/updated, invalid-header fallback. |

The registration-test clarification above follows the existing DI-05 prescription; it
does not reopen Research or change its census. Removing the orphan fixture-macro suite
does not remove scope/autouse/params from approved public template contracts: CODE-E07
is its explicit successor evidence. No independent approval or executed result is
claimed by these classifications.

#### Catalog rows 51–100

Direct review covered test names, relevant setup and assertions; long mixed files also received a remaining-test inventory scan. Paths are exact workspace-relative paths. Architecture disposition concerns the affected boundary, not permission to redesign unrelated behavior. This is producer review, not independent QA or executed test evidence.

| Row | Exact path | Primary owner | Behavior | Architecture | Durable claim / public evidence boundary | Removal condition |
|---|---|---|---|---|---|---|
| 51 | tests/mcp_server/test_tier0_template.py | DI-02 | remove | remove | Existing assertions bind filepath line, timestamps, universal comment mappings and source metadata. Retain V3 first-line header/comment-wrapper validity in public render/read evidence. | V2 tier metadata retired; retained V3 header assertions covered independently. |
| 52 | tests/mcp_server/test_tier0_two_line_format.py | DI-02 | remove | remove | Fixed filepath-plus-metadata two-line output is superseded by the first-line V3 contract. | First-line V3 output/read contract proven. |
| 53 | tests/mcp_server/test_tier1_document.py | DI-03 | remove | remove | Prerequisite omission and supplied section content retain value; defaults for author/history and exact shared prose do not. Route presence cases to DOC evidence through admitted packages. | DI-03 omission/presence cases covered; source-level shared-prose assertions retired. |
| 54 | tests/mcp_server/test_tier1_templates.py | DI-03 | remove | remove | Exact extends strings, token snapshots and the YAML branch are not target authority. Retain declared imports/class/document behavior at concrete package public rendering. | CODE/DOC coverage replaces durable portions; deferred YAML branch not revived. |
| 55 | tests/mcp_server/test_tier2_markdown.py | DI-03 | replace | replace | Supplied structured references render usable Markdown links; omitted links do not invent content. Test concrete document packages, not direct tier loading. | DOC link/presence cases pass on admitted packages. |
| 56 | tests/mcp_server/test_tier2_templates.py | DI-03 | remove | remove | Typed parameters, constructors and supplied content remain CODE/DOC claims; exact tier inheritance, V2 header and YAML snapshots are retired. | CODE/DOC preservation covers signatures/imports/content; no copied tier fixtures. |
| 57 | tests/mcp_server/test_validation_enforcement.py | DI-05 | remove | remove | Verifies embedded STRICT/GUIDELINE metadata rather than actual enforcement. Target behavior is profile checks plus consumer enforce/report policy. | Embedded validation language retired; DI-04/DI-05 public policy evidence exists. |
| 58 | tests/mcp_server/test_validation_metadata.py | DI-05 | remove | remove | Metadata dictionaries, regex/prose presence and manually enumerated templates have no retained role. | Legacy analyzer/metadata language removed; profile/capability evidence replaces actual validation claims. |
| 59 | tests/mcp_server/test_version_hash.py | DI-02 | replace | replace | Determinism and dependency sensitivity remain; eight-hex and label-sensitive expectations do not. Prove generation pf/sf exclusions/inclusions and unaffected-package isolation using independent vectors. | New identity evidence plus DI-06 complete operational-component overwrite protection. |
| 60 | tests/mcp_server/tools/test_a4_schema_overrides.py | DI-01 | adapt | adapt | Keep unrelated workflow/issue enum behavior. Scaffold cases at lines 181–192 inspect legacy artifact enums: use admitted template choices and registered-schema/admission agreement, not core-property-only assertions. | None; selectively migrate scaffold fixtures. |
| 61 | tests/mcp_server/unit/config/test_artifact_definition_no_version.py | DI-01 | replace | replace | Current assertions bind legacy field layout and include a no-op pass test. Prove .version SSOT, closed manifest and absence of context injection. | Package-version/closed-manifest/context-separation evidence present; delete the empty test without inventing replacement coverage for it. |
| 62 | tests/mcp_server/unit/config/test_artifact_registry_config.py | DI-01 | adapt | adapt | Public loading, lookup, duplicate/invalid config and arbitrary IDs remain valuable. Remove lifecycle/category/name-suffix/YAML-field-schema expectations; use isolated package/config fixtures and immutable admitted catalog. | None; obsolete assertion groups removed as replacement contracts land. |
| 63 | tests/mcp_server/unit/config/test_artifacts_type_field.py | DI-01 | remove | remove | Tests only require legacy type=code/doc plus hardcoded inventories. DI-02 section 5.2 removes type because it has no consumer. | Closed manifest rejects removed type; do not reintroduce category to preserve tests. |
| 64 | tests/mcp_server/unit/config/test_c_loader_schema_structural.py | DI-01 | adapt | adapt | Preserve single-reader loading, immutable schema values, no hidden self-loading and actionable invalid inputs. Replace exact fifteen-method inventories/source scanning with public contracts; preserve unrelated config tests. | None; remove source-layout/method-count assertions after equivalent public evidence. |
| 65 | tests/mcp_server/unit/config/test_scaffold_metadata_config.py | DI-02 | remove | remove | Configurable regexes/fields/timestamps protect the removed header-configuration mechanism, not V3 reader behavior. | Legacy metadata config retired; V3 reader has its own contract tests. |
| 66 | tests/mcp_server/unit/config/test_contracts_loader.py | DI-07 | adapt | adapt | Retain public schema errors, configured phase ordering, authoritative workflow semantics and structured handovers. Replace literal instruction phrases/fixed workflow assertions where W11 changes their source. | None; preserve unrelated workflow/merge-policy behavior. |
| 67 | tests/mcp_server/unit/config/test_label_startup.py | DI-04 | adapt | adapt | Keep label/workflow startup failures. Artifact-registry fixtures and project_structure artifact-reference test at line 328 onward are affected: prove new placement/template cross-references through public startup validation. Retain parent-directory policy. | None; not a whole-file exclusion. |
| 68 | tests/mcp_server/unit/config/test_loader_behaviors.py | DI-01 | adapt | adapt | Explicit roots, missing/nonmapping config and cross-reference errors remain. Replace registry/structure fallback setup with final explicit ownership; preserve unrelated enforcement-policy behavior. | None. |
| 69 | tests/mcp_server/unit/config/test_modular_loader.py | DI-01 | adapt | adapt | Public config/package discovery, invalid declaration rejection and clean break remain. Replace merged artifacts-file model with declared manifests, arbitrary IDs and complete-reference admission. Existing temporary roots are reusable. | None. |
| 70 | tests/mcp_server/unit/config/test_settings.py | DI-06 | adapt | adapt | Keep owner-facing env/YAML settings and resolved-root semantics. Environment use tests the public Settings boundary and is not inherently a violation. Adjust affected defaults/roots only; remove private-helper coupling if touched. | None; unrelated version/log/token behavior preserved. |
| 71 | tests/mcp_server/unit/config/test_template_path_resolution.py | DI-02 | replace | replace | Explicit resolved template root selects exactly that suite. Mutable environment override and deleted-directory checks do not prove target injection. | Explicit-root resolver/composition tests replace both current cases. |
| 72 | tests/mcp_server/unit/config/test_tool_presentation_rollout.py | DI-05 | adapt | adapt | Keep bounded findings, no traceback/stderr leakage, truthful domain failure with transport success and real config/model admission. Replace quality-tool matrix entries; do not maintain hardcoded total 29. Preserve issue/PR/health/project-plan portions. | None. |
| 73 | tests/mcp_server/unit/config/test_validator_c3.py | DI-01 | adapt | adapt | Retain unknown merge-policy phase rejection through validate_startup; remove private _validate_merge_policy_phase calls and broad untyped legacy fixtures. Add suite/profile coherence in owning tests, not a second composition-root fixture. | None. |
| 74 | tests/mcp_server/unit/config/test_workflow_config_c6.py | DI-08 | keep | adapt | Preserve unrelated workflow metadata/phase-SSOT behavior. Shared startup fixture contains old artifact/structure objects: adapt only fixture interface changes. | None. |
| 75 | tests/mcp_server/unit/integration/test_all_tools.py | DI-05 | adapt | adapt | Public tool schemas/names/descriptions, request-to-manager results and role separation. Replace legacy quality/test factories and names with scoped typed fakes; preserve Git/GitHub/health behavior. | None. |
| 76 | tests/mcp_server/unit/managers/test_artifact_manager_metadata.py | DI-04 | replace | replace | Preserve unmodified caller context and emitted provenance, not injected timestamp/output_path/name or mock-call enrichment. Test public operation plus rendered bytes. | Public envelope/context isolation and V3 provenance evidence replaces enrichment assertions. |
| 77 | tests/mcp_server/unit/managers/test_artifact_manager_registry.py | DI-02 | remove | remove | Registry-save ordering, registry YAML creation and eight-character hashes are retired behavior. | TemplateRegistry runtime writes removed; generation provenance covered elsewhere. |
| 78 | tests/mcp_server/unit/managers/test_artifact_manager.py | DI-04 | replace | replace | Retain selected-contract validation, render/write result and structured issue preservation. Replace manager attribute/private-collaborator assertions, hidden defaults, envelope projection and dynamic legacy schema fields with injected narrow public seams. | Public manager/tool scenarios cover validation/render/persistence/schema recovery before deletion. |
| 79 | tests/mcp_server/unit/managers/test_c3_note_context_scaffold_chain.py | DI-04 | replace | replace | Actionable missing-field diagnosis remains, but signature inspection and NoteContext diagnostic chain are not target authority. Prove normal operation DTO, selected-schema attachment and bounded presentation. | Public failure/schema recovery tests cover guidance; obsolete NoteContext-chain assertions removed. |
| 80 | tests/mcp_server/unit/managers/test_directory_resolution.py | DI-04 | adapt | adapt | Selected location, explicit filename, containment and configured/temp routing remain. Remove private _project_structure_config patching, first-directory choice and exposed absolute-path expectations. | None. |
| 81 | tests/mcp_server/unit/managers/test_typescript_dto_scaffold.py | DI-03 | adapt | adapt | Caller-supplied typed property shape and readonly/mutable distinction through real scaffold output. Replace copied TS template/YAML with admitted official package and structured context; use target ID/header contract. | None. |
| 82 | tests/mcp_server/unit/scaffolders/test_filesystem_integration.py | DI-02 | adapt | adapt | Missing/unreadable declared template yields the owning boundary's factual failure; successful render yields content. Replace hidden real-root defaults/mock registry with explicit root; distinguish admission failure from later I/O failure. | None. |
| 83 | tests/mcp_server/unit/scaffolders/test_template_registry.py | DI-02 | adapt | adapt | Arbitrary manifest ID resolves its declared template and missing definition is rejected. Remove get_artifact.call_count == 2 and naming implying historical registry ownership. | None. |
| 84 | tests/mcp_server/unit/scaffolders/test_template_scaffolder_introspection.py | DI-01 | replace | replace | Optional omission and complete recovery schema remain; introspection instead of YAML and skipping system fields are obsolete. Admitted JSON owns caller schema and complete-reference recovery. | JSON-schema ownership/optionality/recovery tests present. |
| 85 | tests/mcp_server/unit/scaffolders/test_template_scaffolder_no_hardcoded_fallback.py | DI-02 | replace | replace | Arbitrary IDs select declared graphs without artifact branches. Service, context template override and default Generic fixtures contradict target. Use isolated synthetic IDs/packages. | Generic graph selection and undeclared-override rejection proven. |
| 86 | tests/mcp_server/unit/scaffolders/test_template_scaffolder.py | DI-02 | replace | replace | Generic render, missing context, optional omission and missing dependency remain; retire service dispatch, suffix inference, version mismatch, caller template override and production-template-directory mutation. | Narrow renderer/admission and DI-03 concrete output evidence replace durable claims. |
| 87 | tests/mcp_server/unit/scaffolding/test_components.py | DI-03 | remove | remove | Legacy DTO/Worker Python defaults and template-specific renderer arguments are forbidden generic behavior. | Per-artifact scaffolders removed; retained concrete families covered by CODE evidence. |
| 88 | tests/mcp_server/unit/scaffolding/test_metadata_parser.py | DI-02 | remove | remove | Old parser contract is removed, but malformed/absent/not-first-line/comment-wrapper cases are useful adversarial inputs for the new reader. Port meanings, not old fields or regex configuration. | V3 reader independently covers those meanings before old parser/test removal. |
| 89 | tests/mcp_server/unit/scaffolding/test_template_introspector.py | DI-02 | replace | replace | Parser-supported dependency/undeclared-variable/syntax behavior remains. Remove inferred public required/optional fields, system-field filtering and inherited inventories. Use isolated AST/reference fixtures. | New dependency/coherence parser evidence exists. |
| 90 | tests/mcp_server/unit/schemas/test_lifecycle.py | DI-01 | remove | remove | Tests bind mixin inheritance, mutable lifecycle enrichment and legacy hash validation. No retained lifecycle hierarchy. | Retired types removed; context/provenance separation covered through target contracts. |
| 91 | tests/mcp_server/unit/server/test_bootstrap.py | DI-05 | adapt | adapt | Preserve immutable supported/active tool contracts, injected dependencies and inactive GitHub laziness. Adapt composition to catalog/holder/no-native-startup-probe; replace affected private graph/method patches; retain unrelated config/version failures. | None. |
| 92 | tests/mcp_server/unit/services/test_template_engine.py | DI-02 | adapt | adapt | Explicit-root Jinja load/render/list, relative identities and syntax/missing-variable/missing-template errors. Use isolated sources. Remove template_dir alias and universal naming/filter assumptions; language behavior belongs to packages. | None. |
| 93 | tests/mcp_server/unit/services/test_workspace_upgrader.py | DI-06 | replace | replace | Backups, preserved owner config/state and factual upgrade results remain. Replace SemVer/default 0.0.0/blanket-copy/registry-preservation fixtures with adopted/actual/candidate operational components, checkpoint and recovery. | Complete DI-06 classification/activation/recovery tests before old suite removal. |
| 94 | tests/mcp_server/unit/templates/test_generic_doc_template.py | DI-03 | replace | replace | Structured section/link/checklist presence remains. Retire V2 header, scalar-to-list coercion and silently ignored legacy-content assertion. Test admitted Generic Document schema/render contract. | DOC Generic Document presence/rejection/link evidence covers retained claims. |
| 95 | tests/mcp_server/unit/test_c260_c2_state_root_injection.py | DI-08 | adapt | adapt | Preserve state/project/enforcement/cycle/restart root injection and no-CWD behavior. Adapt scaffold temp placement to resolved roots; remove only TemplateRegistry cases. Replace affected private/broad mocks with narrow injected values. | None; registry-specific cases removed only with registry retirement. |
| 96 | tests/mcp_server/unit/test_cli.py | DI-06 | adapt | adapt | CLI init/upgrade exits, explicit root, owner-config preservation and degraded-start behavior remain. Replace copytree call-shape/registry-ignore/legacy template-path assertions with resulting files and delegated renewal outcomes. | None. |
| 97 | tests/mcp_server/unit/test_server.py | DI-08 | keep | adapt | Preserve public MCP registration, pre/post enforcement, advisory suppression, log correlation and injected settings. Adapt shared private bootstrap/template-registry fixtures; retain unrelated enforcement/GitHub tests. | None. |
| 98 | tests/mcp_server/unit/tools/test_cycle_tools.py | DI-08 | keep | adapt | Preserve transitions, force-approval validation, pre/post checks and advisories. Shared _build_config_layer/_build_manager_graph plus registry fixtures must change; no cycle-contract redesign. | None. |
| 99 | tests/mcp_server/unit/tools/test_extra_forbid.py | DI-05 | adapt | adapt | Preserve closed public inputs, including nested safe-edit operations. Update legacy quality/template-validation/scaffold/test imports and valid inputs; add check/fix inputs through actual typed contracts. | None; remove obsolete model rows only at cutover and retain unrelated rows. |
| 100 | tests/mcp_server/unit/tools/test_template_validation_tool.py | DI-05 | remove | remove | Removed tool's fake-validator responses and argument contract are not retained. Useful success-versus-domain-failure distinction belongs in check/test/fix public response evidence. | Public validate_template removed; role-result/operational-error evidence present elsewhere. |

Bounded-review qualifications:

- Rows 60, 67 and 99 are not wholly unaffected despite the frozen candidate ledger's exclusion shorthand: they contain scaffold choices, placement references or changed/removed input-model imports.
- Row 63 follows the approved removal of the manifest type/category field, not the older candidate disposition to preserve category constraints.
- Row 79 preserves actionable diagnostics without preserving NoteContext as their authority. Row 88 removes the legacy parser without discarding useful adversarial input categories for the new reader.
- This pass does not certify every untouched assertion in large mixed files as architecture-compliant. The adapt disposition identifies affected fixture boundaries without expanding issue 460 into unrelated test redesign.

#### Catalog rows 101–151

Rows retain the frozen catalog order. Dispositions distinguish durable behavior from
the current test construction; replacement does not discard the named evidence claim.

Removal-condition legend for this table:

- **P**: replacement public-contract coverage exists.
- **A**: relevant native adapter conformance exists; obsolete generic parser assertions
  do not require equivalent replacement assertions.
- **R**: the corresponding V2 runtime and imports have been removed, and necessary
  removal checks have been consolidated.
- **C**: independent cache, presentation, or general infrastructure claims have been
  retained under their existing owner.
- **none**: no file removal is proposed.

| Row / exact path | Primary DI | Behavior disposition | Architecture disposition | Durable claim / public evidence boundary | Removal condition |
|---|---|---|---|---|---|
| 101 `tests/mcp_server/unit/tools/test_issue_template_h1.py` | DI-03 | adapt | replace | Preserve an issue body without H1 and its supplied content. Current tests render Jinja directly and assert exact heading prose; prove public scaffolding and the body profile instead. | P |
| 102 `tests/mcp_server/unit/tools/test_safe_edit_tool.py` | DI-04 | adapt | adapt | Preserve replace/append/rewrite/pattern operations, no write on rejection, concurrency and content. Replace strict/interactive/verify_only, fallback setup and old issue-identity expectations with the approved policies/results. | none |
| 103 `tests/mcp_server/unit/tools/test_scaffold_artifact.py` | DI-04 | adapt | adapt | Preserve selected-artifact execution, unchanged nested context and operation failures through a narrow injected manager fake. Unpacking context into manager kwargs is not a caller contract to retain. | none |
| 104 `tests/mcp_server/unit/tools/test_scaffold_schema_tool.py` | DI-01 | adapt | adapt | Preserve selection enums and complete schema transfer. Replace named research/dto fixtures with an injected catalog; separately prove actual embedded-resource/cache equality. | none |
| 105 `tests/mcp_server/unit/validation/test_template_analyzer.py` | DI-02 | replace | replace | Dependencies, variables and inheritance have durable intent. Metadata-rule/prose merging retires; the replacement boundary is public parser-supported graph resolution. | P, R |
| 106 `tests/mcp_server/fixtures/fake_pytest_runner.py` | DI-08 | replace | replace | Preserve deterministic outcomes and request observation. The current fake captures only cmd and ignores cwd/timeout/verbose; replace it with an explicit role/runtime-contract fake. | All old fake imports migrated |
| 107 `tests/mcp_server/integration/test_qa.py` | DI-05 | adapt | replace | Prove configuration selection changes the checks actually executed. Replace a real workspace target, fixed Ruff name and at-least-six-gates assertions with isolated public run_checks integration. | P |
| 108 `tests/mcp_server/integration/test_submit_pr_atomic_flow.py` | DI-05 | adapt | adapt | Preserve PR atomicity, parent selection and existing PR recovery. Remove only quality-state-registration expectations; do not project native-fix rollback policy onto the unrelated PR flow. | none; obsolete cases after R |
| 109 `tests/mcp_server/unit/config/test_quality_config.py` | DI-05 | replace | replace | Preserve missing/invalid configuration, extra-field and coherence checks through ConfigLoader and role schemas. Gate commands, parser settings, logging configuration and fixed native selections retire or move to their native owner. | P, A, R |
| 110 `tests/mcp_server/unit/core/interfaces/test_interface_imports.py` | DI-05 | adapt | compliant | Preserve public importability. Remove IPytestRunner/IQualityStateRepository expectations and cover retained narrow interfaces; keep unrelated state/git/context exports. | none |
| 111 `tests/mcp_server/unit/managers/test_auto_scope_resolution.py` | DI-05 | replace | replace | Retain useful deterministic selection/deduplication intent. Auto unions, baseline fallbacks and .py filtering retire; prove explicit scopes and rejection of auto. | P, R |
| 112 `tests/mcp_server/unit/managers/test_autofix_propagation.py` | DI-05 | replace | replace | Current tests prove fixable_when/gate-support propagation, not native mutation. Replace them with explicit fix selection and actual role outcomes; no generic fixability census. | P, R |
| 113 `tests/mcp_server/unit/managers/test_baseline_advance.py` | DI-05 | remove | remove | Baseline/replay and private advance/accumulate calls retire. Preserve independent negative evidence that new checks do not read/write this state, without duplicating general state-integrity tests. | R; retain public no-state-touch evidence |
| 114 `tests/mcp_server/unit/managers/test_c8_cleanup_grep_closure.py` | DI-08 | replace | replace | Current source-string assertions partly require old repository wiring. Consolidate bounded active V2 import/wiring removal checks with behavioral evidence. | R |
| 115 `tests/mcp_server/unit/managers/test_execute_gate_dispatch.py` | DI-05 | replace | replace | Preserve execution outcomes through public catalog/runtime boundaries. Do not preserve generic JSON/text-to-violations dispatch or empty-parsed-list-means-pass. | P, A, R |
| 116 `tests/mcp_server/unit/managers/test_extract_violations_array.py` | DI-05 | replace | replace | Current calls use public ViolationParser methods despite the old private-method docstring. Preserve native Pyright evidence; dotted-path DSL and missing-key-to-empty-list behavior are not generic V3 contracts. | A, R |
| 117 `tests/mcp_server/unit/managers/test_files_for_gate.py` | DI-05 | replace | replace | Preserve literal targets/order and role applicability through public selection. Do not move the current server-side extension filter into the new generic manager. | P, R |
| 118 `tests/mcp_server/unit/managers/test_filter_files_removed.py` | DI-08 | remove | remove | Only asserts that QAManager lacks _filter_files; it supplies no current missing/deleted-path behavioral coverage. That evidence belongs to public scope tests. | R |
| 119 `tests/mcp_server/unit/managers/test_legacy_parsers_removed.py` | DI-08 | replace | replace | Current claims concern absent symbols only. Consolidate absence of generic native parsing and old imports without retaining individual private-method tombstones. | R |
| 120 `tests/mcp_server/unit/managers/test_parse_json_violations_nested.py` | DI-05 | replace | replace | Preserve native nested diagnostics in adapter evidence. Generic field-map-to-ViolationDTO conversion and synthesized nulls are not retained contracts. | A, R |
| 121 `tests/mcp_server/unit/managers/test_parse_json_violations_options.py` | DI-05 | replace | replace | Preserve native locations/fix details when reported. Retire the generic offset/fixable-override DSL; do not require automatic +1 normalization under the native-evidence contract. | A, R |
| 122 `tests/mcp_server/unit/managers/test_parse_json_violations.py` | DI-05 | replace | replace | Single and multiple native diagnostics remain available. Cross-tool ViolationDTO normalization and fixability defaults retire. | A, R |
| 123 `tests/mcp_server/unit/managers/test_parse_text_violations_defaults.py` | DI-05 | remove | remove | Static/interpolated parser defaults concern only the obsolete generic DSL; no separate durable public V3 claim was found. | R; any actually required adapter interpretation through A |
| 124 `tests/mcp_server/unit/managers/test_parse_text_violations.py` | DI-05 | replace | replace | Preserve Mypy/native text as native evidence. Do not reconstruct generic line regexes, default severity or omission of unmatched lines. | A, R |
| 125 `tests/mcp_server/unit/managers/test_pyright_severity_mapping.py` | DI-05 | adapt | replace | Preserve error/warning/information, message/rule/location in Pyright-native evidence. Exercise adapter results without generic parser configuration or unused manager fixtures. | A, R |
| 126 `tests/mcp_server/unit/managers/test_pytest_helpers_removed.py` | DI-08 | replace | replace | Two private-helper absence checks consolidate into proof that generic execution contains no Pytest-specific knowledge. | R |
| 127 `tests/mcp_server/unit/managers/test_pytest_runner.py` | DI-05 | adapt | replace | Preserve native failure/collection/no-tests/coverage/LF/CRLF/xdist detail behind test/v1. Retire the old numeric DTO, native-exit-to-MCP-error mapping and generic verbose caps. | A, P |
| 128 `tests/mcp_server/unit/managers/test_qa_manager.py` | DI-05 | replace | replace | Split scope, native failure, missing executable, timeout and bounded diagnostics across public role/runtime evidence. Do not retain health surveys, baseline state, monolithic parsing, automatic log spill or generic verbose policy. | P, A, R; cache claims through C |
| 129 `tests/mcp_server/unit/managers/test_quality_state_repository.py` | DI-05 | remove | remove | The auto-state repository retires. Concurrent apply/locking/atomic-writer claims may be independently useful; establish their existing general-infrastructure coverage before removal, without creating new check state. | R, C |
| 130 `tests/mcp_server/unit/managers/test_skip_reason_unified.py` | DI-08 | remove | remove | Only asserts absence of _get_skip_reason; no current status-semantics coverage exists here. Prove the new status combinations independently at public boundaries. | R |
| 131 `tests/mcp_server/unit/managers/test_summary_c39.py` | DI-05 | replace | replace | Preserve truthful incomplete-work reporting, scope and available diagnostics. All-skipped-green, auto and native-message sanitation expectations explicitly retire. | P, C |
| 132 `tests/mcp_server/unit/managers/test_summary_line_formatter.py` | DI-08 | replace | replace | Preserve bounded correct presentation through the actual configured presenter. Exact emoji/gate-name/ratio assertions and old failed-versus-skipped precedence are not V3 contracts. | C |
| 133 `tests/mcp_server/unit/managers/test_violation_path_normalization.py` | DI-05 | adapt | replace | Keep typed public operation paths relative/safe and native raw evidence unchanged within approved disclosure rules. Do not require blanket removal of absolute paths from native cached evidence. | P |
| 134 `tests/mcp_server/unit/schemas/test_structured_tool_output_migration.py` | DI-08 | adapt | adapt | Preserve immutable JSON results, absence of presentation fields and unrelated workflow facts. Replace old ValidationIssue/RunTests scalar expectations with closed role contracts and actual resource round-trips. | none |
| 135 `tests/mcp_server/unit/state/test_quality_state.py` | DI-05 | remove | remove | Covers only the obsolete baseline/failed-files value object and ordinary Pydantic behavior; it does not justify a replacement reuse/history DTO. | R |
| 136 `tests/mcp_server/unit/tools/test_autofix_tool.py` | DI-05 | replace | replace | Move fix flow to explicit apply_fixes. FIFO eviction and cached-resource matching/read tests are independent durable cache claims and must be retained separately. | P, C, R |
| 137 `tests/mcp_server/unit/tools/test_dev_tools.py` | DI-05 | replace | replace | The file contains only one RunTestsTool/Pytest-command test; no unrelated developer-tool behavior was found. Consolidate role request/result proof under W04 and remove the dual-output fallback. | P |
| 138 `tests/mcp_server/unit/tools/test_discovery_tools.py` | DI-07 | keep | adapt | Actual tests cover GetWorkContext branch/phase/cycle/instructions/state fallback, not execution-tool registration. Preserve that behavior; adapt private injection, deep state mutation and copied workflow-fixture knowledge where affected. | none |
| 139 `tests/mcp_server/unit/tools/test_quality_tools.py` | DI-05 | replace | replace | Preserve explicit scopes, args, binding results, operational success and actual failure routing through run_checks. Remove auto/conflict-state/generic-verbose/gate-DTO expectations. | P, R |
| 140 `tests/mcp_server/unit/tools/test_test_tools.py` | DI-05 | adapt | replace | Preserve W04 operation/result evidence and move native flags to adapter coverage. The autouse fixture replaces execute with a test-authored payload/text wrapper; replace it with actual decorator/cache/presentation evidence. | P, A |
| 141 `tests/mcp_server/unit/tools/test_tool_result_contract.py` | DI-08 | replace | replace | Prove the actual public wrapper/cache contract. The current autouse wrapper itself creates exactly two content items, emoji and compact payload, so those assertions certify test code. | C, P |
| 142 `tests/mcp_server/unit/validation/test_python_validator.py` | DI-05 | replace | replace | Preserve complete proposed content, real syntax outcomes and intended paths. Current tests chiefly prove QAManager score mapping and temporary .py routing, not pure AST conformance. | P, A, R |
| 143 `tests/mcp_server/validation_fixtures/violations.py` | DI-05 | adapt | replace | Move useful actual negative snippets to owning adapter fixtures. The typed-add mismatch remains, but import/format/line-length comments do not fully match current content; establish effects independently. | A; remove unused snippets |
| 144 `tests/mcp_server/unit/config/test_json_violations_parsing.py` | DI-05 | remove | remove | Covers only JSON field-map DSL/defaults and Ruff/Pyright configuration shapes. Native output preservation belongs to adapter conformance, not a replacement generic parser schema. | R, A |
| 145 `tests/mcp_server/unit/config/test_quality_config_scope.py` | DI-05 | replace | replace | Preserve public path normalization/selection. Gate include/exclude filtering must not become a second native selector inside role configuration. | P, R |
| 146 `tests/mcp_server/unit/config/test_text_violations_parsing_defaults_validator.py` | DI-05 | remove | remove | Covers only regex-placeholder/default-DSL validation; no independent retained V3 behavior was found. | R |
| 147 `tests/mcp_server/unit/config/test_text_violations_parsing.py` | DI-05 | remove | remove | Covers patterns/default severity/default maps. Preserve Mypy evidence at its adapter; do not infer a Pylint-adapter commitment from an old fixture. | R, A |
| 148 `tests/mcp_server/unit/config/test_violation_dto.py` | DI-05 | replace | replace | Preserve genuinely present/absent native facts through closed role responses/evidence. Do not reproduce cross-tool line/rule/fixability defaults. | P, R |
| 149 `tests/mcp_server/unit/managers/test_compact_payload_builder.py` | DI-08 | replace | replace | Preserve complete cache versus bounded text, ordering and absence of automatic debug dumps through the actual presenter. Retire overall_pass, skipped-plus-passed and empty-gates-success assumptions. | C, P |
| 150 `tests/mcp_server/unit/managers/test_scope_resolution.py` | DI-05 | replace | replace | Preserve parent/merge-base, existing targets and deterministic deduplication through public scopes. Remove .py filtering, implicit main, Git-error-to-empty and project-glob scanning. | P, R |
| 151 `tests/mcp_server/unit/resources/test_standards.py` | DI-05 | adapt | adapt | Preserve the public standards resource, URI/matching and current policy facts. Fixed seven-gate and coverage=80 assertions must not remain a second native-policy authority. | none |

This audit establishes preservation/removal conditions, not proof that replacement
suites or general cache/state coverage already satisfy them. In particular, rows 129
and 136 require comparison with their existing infrastructure owner before removal.

### 3.3. Supplemental Design Seams

The frozen census is not inflated to hide later integration dependencies. Existing
families discovered here receive explicit supplemental ownership; no new product
role or Research compatibility strategy is introduced.

| Exact path | Primary owner | Preserved behavior / affected seam |
|---|---|---|
| mcp_server/core/decorators/input_validation_decorator.py | DI-01 | Existing typed admission and actionable invalid-input response; use the same prepared contract as registration. Normalize optional internal attachments once. |
| mcp_server/utils/schema_utils.py | DI-01 | Resolve supported references without dropping constraints; reject unsupported references, never fetch network schemas. |
| mcp_server/server.py | Shared contracts | Existing enforcement, cache publication, configured text and MCP success mapping; transport attachments without treating them as operation data. |
| mcp_server/presenters/text_presenter.py | Shared contracts | Generic declarative admission/rendering, bounded summaries and no native/error-class dispatch; concrete public records and Shared §11.1 generic type admission resolve the designed projection constraint; conformance remains required. |
| mcp_server/presenters/collection_text_renderer.py | Shared contracts | Approved generic Annotated/scalar recognition preserves existing supported collection/container shapes, ordering and text limits; no native/DTO-specific branches. |
| tests/mcp_server/unit/presenters/test_collection_text_renderer.py | Shared contracts | Preserve public classifier/renderer behavior and unsupported-shape rejection; add strict scalar/nullable-inline boundary cases without allowing model unions. DI-08 contributes architecture. |
| tests/mcp_server/unit/presenters/test_text_presenter_composition.py | Shared contracts | Prove registered concrete rows and optional enum-case admission with actual configured text/cached evidence; preserve existing composition and byte-budget claims. |
| pyrightconfig.json | DI-05 | Native Pyright configuration stays authoritative; no second generic representation of native rules. |
| tests/mcp_server/unit/decorators/test_pipeline_decorators.py | Shared contracts | Adapt real decorator tests for the internal carrier while preserving input, enforcement and existing error DTO behavior; no test-defined substitute execute route. DI-08 contributes test architecture. |
| tests/mcp_server/unit/resources/test_cache_resource.py | Shared contracts | Preserve resource URI validation/read semantics; add required-null and nested-variant round-trips at the real resource boundary. DI-08 contributes test architecture. |
| tests/mcp_server/unit/utils/test_schema_utils.py | DI-01 | Preserve definition/constraint/description inlining; add bounded static-reference rejection and no silent constraint loss. DI-08 contributes test architecture. |

Catalogued files may also appear here to make a cross-package seam explicit; this
table is not an assertion that every row was absent from Research. Supplemental
tests are recorded only after their exact paths are verified, not guessed.

### 3.4. Evidence and Review Boundary

- Baseline before this integration pass: commit `76640db4bb10c1186cb03c491bf76265fff5c43b`.
- Read-only inspection covered the real registration/decorator/cache/presentation
  path and the 151 test/helper paths, with focused inspection of risky fixtures.
- Important Design clarifications: the registration test is affected despite older
  Exclude shorthand; schema-override and extra-forbid tests contain real scaffold/V3
  inputs; two test wrappers replace the actual execute route and cannot establish
  public transport conformance. Preserve useful assertions through real boundaries.
- Research's historical search counts are not represented as today's execution
  evidence. Temporary workshop/probe/vendor files are not canonical inputs.
- No production/test edits or test runs were performed by this Design audit.
- Mechanical verification after integration: all 151 entries match the frozen test
  ledger exactly, in order, without omissions, extras or duplicates; all paths exist.
  Eight edited Design documents contain 320 checked inline local link targets with
  no missing files and balanced code fences. This check does not validate anchor
  fragments, external URLs or runtime semantics.
- Final output consolidation verification (2026-09-12): six edited documents, 295
  inline local file targets, no missing files and balanced code fences. All five new
  consolidation/navigation heading anchors match their targets. The exact error tables
  contain 14 mutation and 8 run_checks codes. Repeated ledger comparison confirms 151
  unique existing test/helper paths in identical frozen-catalog order; no omissions or
  extras. These are mechanical documentation checks, not runtime or native proof.
- Independent combined Design review is requested through the Design hub. Runtime
  preservation and client/native conformance remain implementation evidence obligations.

## Combined Output Workshop Consolidation — 2026-09-12

The human approved this complete workshop; the active contracts now reside in:

- [DI-05](design-execution-adapters.md#131-public-result-projection-and-exact-check-error-details):
  exact concrete test/fix row fields, valid observation combinations, preserved role
  differences and the run_checks code/details matrix.
- [DI-04 §7.1](design-mutation-validation.md#71-exact-error-details-and-rejected-adapter-requests):
  mutation code/details matrix, retained edit feedback and the explicit public
  not_executed/invalid_request combination for rejected internal adapter requests.
- [Shared §11.1](design-shared-contracts.md#111-output-presentation-integration):
  existing declarative projection and the limited strict/nullable type-admission
  correction. No new native parser, DTO-specific presenter logic, summary DTO or
  conditional-expression language.

One concrete model per consumer follows the already-approved mutation design.
Adapter wire unions remain unchanged. W04/W05 now reference concrete public rows,
and DI-04's active closed reason set includes the approved internal-request rejection.
The rejected null-status alternative would require special aggregation rules;
not_executed/invalid_request instead fits the existing reducers and preserves the
actual attempted process without pretending native work occurred.

Source inspection: current collection classifier and enum alignment; runtime enum
lookup has no matching case for null under the existing operation-error enums, while
explicit generic null handling remains required; local Pydantic StrictStr is Annotated;
issues 456/459 retain concrete rows, direct fields, bounded text and full cache facts;
safe-edit already limits mismatch suggestions to three lines and preview to ten lines.
Producer-assisted critique found the non-null not_executed representation smaller and
consistent with the minimal before-native invalid_request protocol. No approval or
executed conformance is inferred from that critique. Research and code remain unchanged.

Independent whole-phase QA is now requested via the [joint hand-over](design.md#whole-design-hand-over--combined-review-request).
The earlier bounded DI-03 QA GO does not pre-approve these integration contracts.
No production/test changes or Research amendment are included.

## 4. Semantic Integration Closure

**Producer reconciliation after the independent closure NOGO, 2026-09-12.**
The positive technical assessment is not a Planning GO. This ledger records the
actual cross-package decisions, consequences, removal conditions and proof owners;
the hub derives its integration accounting from these rows. Integrated means Design
reconciled, not implemented, independently approved or runtime-proven.

### 4.1 Research Obligation Sets and Semantic Dispositions

Primary ID sets follow the frozen intake exactly. The Strategy column names all
44 existing rows by their Research subject; it introduces no replacement IDs.
Each row's downstream and proof consequences are completed in §4.2, not inferred
from a navigation link. F-18 and four deferred strategies are reconciled exclusions,
not delivered functionality. Cross-cutting consumers do not acquire primary ownership.

| Primary owner | Findings / invariants / expected results | Exact strategy subjects (count) | Selected contract and semantic disposition |
|---|---|---|---|
| DI-01 | F-02, F-06, F-12, F-17; I-05, I-06, I-08; E-04, E-05, E-08 | F-01/S-01 public context; F-01 client compatibility; F-02/S-03 optionality/nullability; F-06/S-04 links; F-12/S-05 issue references; F-12/S-06 checklists; F-17 qualified identity (7) | [Suite §§5.1–5.2/7.2](design-suite-resolution.md) and DI-03 shared records: literal JSON context, finite closed records, positive issue IDs, explicit checked state, qualified template IDs. No coercion/default materialization or primitive compatibility bridge; omitted/empty/null/false/zero retain distinct meaning. |
| DI-02 | F-04, F-05, F-11, F-16; I-03; E-02, E-07 | F-04/S-08 DTO selection; F-05/S-09 resolved graph; F-11/S-16 provenance; F-16 purpose (4) | [Suite §§5.3–5.6/7.5](design-suite-resolution.md): one startup-resolved renderer/catalog, parser-supported contained edges, one package .version, generation pf/sf and first-line header. Remove override/registry/hash authority; purpose survives introspection. Historical reconstruction remains owner-dependent, never a PGMCP lookup promise. |
| DI-03 | F-01, F-07, F-14, F-14A, F-14B; I-01, I-02, I-07; E-01, E-06, E-10 | F-01/S-02 nested collections; F-14/S-12 portability; DTO; Generic; integration-test; Resource; configuration-model; Service; Tool; TypeScript DTO; unit-test responsibilities; F-14A agent hints; F-14B unreachable patterns (13) | [Code §§7/9](design-code-test-artifacts.md) and [Documents §§7/9](design-document-tracking-artifacts.md) fix nine code/test and ten document/tracking families, structured fields/imports/fixtures/links and requiredness. Resource/Service/Tool templates, project assumptions, hints and dead patterns retire; existing runtime classes/generated files do not. DTO examples remain authored illustrations, not model-validated instances. |
| DI-04 | F-03, F-13, F-15; I-04, I-09, I-13; E-03, E-11, E-18 | F-03 caller/operation/provenance ownership; F-07/S-07 consumption; F-13 success; F-15/S-13 target/file name; safe-edit validation (5) | [Mutation §§3–4/7.1](design-mutation-validation.md): exact file name, unchanged context, separate provenance, configured placement, create-only scaffold and complete-content safe edit. Enforce/report share factual checks; independent safety failures block both. Direct results distinguish validation, actual persistence and operational defects; no hidden name projection, preview alias or nested result duplicate. |
| DI-05 | F-08, F-19, F-20; I-16, I-19; E-13, E-20, E-23 | F-08/S-14 output validation; F-19 shared check authority; F-20 check/test/fix suite (3) | [Adapters §§7.3–7.20/13.1](design-execution-adapters.md): one catalog/process base, distinct role contracts, native-owned settings/results, configured mutation checks and explicit execution scopes/args. Native fixes mutate only admitted explicit files, in caller order, stopping first non-success without rollback. Configured startup exposure performs no native availability survey. |
| DI-06 | F-10; I-17, I-18; E-21, E-22 | F-10/S-10 distribution/customization; deployment compatibility (2) | [Distribution §§5/7–9](design-distribution.md): full operational component equality includes policy/version; adopted/actual/candidate selection builds one validated off-root proposal and recoverably activates one root. Checkpoint-less actual is preserved absent trustworthy equality or explicit owner action; no fabricated V2 checkpoint, implicit merge or external retention service. |
| DI-07 | F-09; I-12, I-15; E-09, E-15, E-16, E-19 | F-09/S-15 documentation authority; workflow/template semantic alignment (2) | [Workflow §§5/7–9](design-workflow-documentation.md): canonical instruction sources, mapped host copies, nineteen carrier meanings, conditional schema discovery, no copied invocations or fake phase completion. Modular live tool/schema references replace obsolete API/inventory authority. |
| DI-08 | I-14; E-17 | Test-suite architecture compliance (1) | [Test architecture §§7–10](design-test-architecture.md) and §3.2 here: each test has a durable behavior and architecture disposition; narrow fixtures and independent native/domain/public oracles replace global/private/fake-execute coupling. Planning, not DI-08, assigns cycles. |
| XC-01 | I-11; E-14 | Runtime architecture compliance (1) | Package responsibility/option sections plus Shared §§5/11.1 require pure injected config, immutable catalogs, narrow read interfaces, separate mutation authority and declarative presentation. A new template/native tool extends assets/config rather than generic ID/language/parser dispatch; tests obey the same boundaries. |
| XC-02 | No separate finding/invariant/result primary set | Legacy parallel scaffolding and validation surfaces (1) | Package §9 removals, DI-07 §7.5, DI-04 §3.3 and §3.2 here link replacement authority to retained claims. No shell/alias/dual read, unowned removed behavior or catch-all migration cycle; separate proof precedes removal. |
| RC-01 | I-10; E-12 | F-12 original-issue coverage (1) | Frozen Research remains strategy authority. DI-01/03's structured checklist/issue/link contracts and DI-04 unchanged-context route cover the original PR defects within suite-wide boundaries; no PR-only special case or later strategy choice. New contradictory evidence stops the affected Design rather than becoming a Planning workaround. |
| Explicit exclusions | F-18 | Deferred YAML subset; additional portable Python artifact coverage; F-18 runtime discovery; command/query service family (4) | [Deferred register](deferred-work.md), Suite §5.1/§9 and DI-03 inventory keep these out. YAML source is recoverable through Git; retained Generic does not absorb deferred service families. Existing complete template enums are not a new discovery tool. |

Totals derived from these primary sets: 22 findings (21 designed + one excluded),
44 strategies (40 designed + four excluded), 19 invariants and 23 expected results.
This counts resolved dispositions, not executed acceptance tests.

### 4.2 Cross-Package Consequence and Proof Reconciliation

| Integrated dependency | Reconciled contract / consumer consequence | Migration or removal prerequisite and independently owned evidence |
|---|---|---|
| DI-01/02 → Shared → DI-04 and registered tools | Suite §7.2's immutable prepared tool contract is shared by registration, lazy exposure, admission and whole-tool error feedback. The selected context remains a separate reference-free schema; Shared §5.5 carries it only in the approved attachment cases. DI-04 never repairs or projects envelope values into context. | Suite §9 removes independent schema/default/override authorities. Suite §10, Shared §10, CODE-E01/09 and DOC-E01/02/04/05 require authored/resolved acceptance parity, unchanged values and actual decorated tool/resource reads; static model-only checks cannot certify wrappers. |
| DI-02 → DI-03 → DI-04 | One resolved Jinja entry and permitted shared edges supply generation identity. DI-03 preserves tiered native framing; the same first-line four-field contract is read by DI-02's text-only reader. DI-04 uses original recognized current ID or explicit/extension selection; invalid/unknown metadata yields no template match. | Old registry, override, graph/hash and metadata-history paths retire only with Suite §10, CODE-E10, DOC-E11 and DI-04 §8 evidence. Test actual graph/framing, invalid recognition and lateral/shared identity impact; do not obtain expected protocol bytes from the producer itself. |
| DI-02 ↔ DI-06 | Generation pf/sf excludes whole .version/policy files; operational component equality includes them. Manifest ID, not directory name, keys checkpoint packages. Policy-only or label-only edits therefore cannot become invisible overwrite authorization. | DI-06 §§5.2/7.2/8–10 proves all component-presence/equality cases, safe bootstrap, reconciliation and interruption recovery. Existing artifact provenance/history is neither rewritten nor a checkpoint. No F-10 activation and F-20 native-fix cycle is shared. |
| DI-03/DI-05 → DI-06 admission | Template policy.yaml selects profiles; DI-05 §7.20 supplies a configurable startset, not hardcoded server dispatch. DI-06 §7.7 resolves candidate/proposal references against effective actual config, including an external config root; force cannot inject profiles or install dependencies. | CODE-E09/DOC-E11, DI-06 §7.7/§10 and TEST-E05/06 distinguish missing-reference refusal before activation from on-use native unavailability. Existing config/trust/native settings remain unchanged during renewal. |
| DI-05 content checks → DI-04 persistence | Same typed check facts, distinct consumer policy. Complete proposed text is passed directly or materialized under unique temp/validation child; never temporarily overwrite the target. Runtime attempt/capture and housekeeping survive projection. Internal rejection blocks both policies; cleanup alone does not invalidate a verdict/write. | DI-04 §§4.9–4.10/7.1/8 and DI-05 §7.13/§10 require original/proposed consistency, no-write enforcement, create/replace safety, timeout/termination and nonblocking cleanup. Fake adapters prove policy only; separate native/process tests prove the execution seam. |
| DI-05 explicit roles → Shared output | run_checks, run_tests and apply_fixes keep their own scopes, reducers and stop rules. §13.1 concrete rows transfer adapter facts without native parsing; Shared §§5.5–5.6/11.1 transports attachments, required nulls and bounded text. Native negative results remain operational success; internal request rejection is not a user CLI refusal. | Real registered tools/resources must preserve 14 mutation and 8 check error-detail shapes, test/fix matrices, native evidence/capture, nullability and success/isError. Generic Annotated/nullable admission replaces no DTO with presenter-specific branches or a second summary authority. |
| DI-05/DI-06 → DI-07/DI-08 installed adapters | Bundled packages live outside copied assets; owner workspace packages are explicitly trusted, distinct, immutable during a server run. Native dependency/config ownership remains with its ecosystem/workspace. | DI-06 §§7.6–7.7/§10 owns manifests/scripts/schemas/dependency files in a built and separately installed distribution. DI-05 owns real adapter behavior, including commit header-reader dependency; DI-08 supplies installation/process support without source-checkout fallback. |
| DI-03 documents ↔ DI-07 workflow | Document §7.8 and Workflow §7.2 match nineteen phase/workflow meanings. Planning identities use operational cycle_number/name/deliverables/validates/exit_criteria without turning narrative into hidden tool payload; scaffold content never grants phase approval. | DOC-E06/07/10 and DOCFLOW-E01/02/05 exercise real schema/render capacity and public workflow loading, not heading counts. Source-copy mappings and inbound links are independently checked before old invocation/API text retires. |
| DI-01–DI-07 removals ↔ DI-08 support | Technical packages own retained behavior and specific removals; DI-08 owns reusable roots/process/filesystem/registered-tool fixtures and audits dependencies. The §3.2 151-row index retains each claim and removal prerequisite. | TEST-E07/08, package §9 and the frozen 126-consumer ledger prevent unowned removals. Preserve unrelated conftest/plugin/cache behavior, including FIFO claims and existing wrapper semantics. Planning maps exact paths to bounded cycles; no invented remaining-consumers/tests cycle. |

### 4.3 Consumer Families and Conditional Dispositions

The 126 active consumer/reference paths plus two governing sources remain in the
frozen catalog; they are not duplicated or inflated here. Its ten primary consumer
families now resolve as follows. These are Design handoff owners, not cycle names.

| Frozen consumer family | Integrated authority, removal and proof consequence |
|---|---|
| Contract metamodel/schema/IDs | DI-01: Suite §§5.1–5.2/7.2/9/10, DI-03 finite definitions and Shared schema delivery replace YAML/independent schema authorities; preserve registered input parity. |
| Graph/catalog/provenance | DI-02: Suite §§5.3–5.6/9/10 replaces override/registry/metadata inference; DI-04 selector consumes current ID and DI-06 consumes full admission, not generation hashes as checkpoint. |
| Concrete artifacts/macros/examples | DI-03: both family §7 inventories and §9 dispositions preserve explicit content, remove rejected families/patterns and identify native preflight/evidence dependencies. |
| Scaffold/safe edit/location policy | DI-04: §§3.3/4/7.1/8 replaces hidden naming/CWD helpers and old modes, keeps exact filenames and separate create/edit atomicity; no adapter-owned persistence. |
| Adapter/quality/test/fix/config/state/presentation | DI-05: §§7.3–7.20/13.1/9/10 plus Shared transport replaces V2 runner/parser/config paths; native settings and check/test/fix migration prove separately before cutover. |
| CLI/init/upgrade/assets/checkpoints | DI-06: §§5/7–10 replaces old copy/overwrite heuristics with full operational comparison, admission and recoverable activation; no runtime overlays or native probes. |
| Contracts/instructions/references/host copies | DI-07: §§5/7–10 selects source authority and exact reference dispositions, retains workflow/approval behavior and verifies mapped copies without schema duplication. |
| Cross-package legacy removal | XC-02: package-owned §9 dispositions plus §3.2 here and DI-08 TEST-E07/08 account for preserved claims before removal; neither a compatibility shell nor a removal subsystem. |
| Shared test architecture/helpers | DI-08: §§7.1–7.4/9/10 replaces broad/private/global support; supplementary conftests remain separately listed and unrelated fixture behavior is preserved. |
| Current-owner/external deployment | DI-06 §9 and DI-07 guidance: explicit owner migration/bootstrap/reconciliation, no silent actual adoption, retention lookup or automatic external rollout. |

| Conditional catalog path | Selected disposition / authoritative contract | Downstream proof |
|---|---|---|
| .pgmcp/config/artifacts.yaml | DI-02 removes inventory use; DI-04 §3.3 uses only manifest-ID artifact placement. No dual read of the old meaning. | Discovery/placement and absence of legacy readers; DI-06 delivers defaults without overwriting owner config. |
| docs/manuals/phase-workflows.md | DI-07 §7.5 retains only a contracts-owned navigation/authority overview. | DOCFLOW-E01/E04/E05: no universal copied phase/TDD rules or complete stale invocations. |
| docs/reference/validation_api.md | DI-07 §7.5 removes standalone obsolete API, moves retained concepts to current modular references and rewrites active inbound links. | DOCFLOW-E04/E05; history stays historical, no obsolete active authority. |
| mcp_server/scaffolding/utils.py | DI-04 exact file_name and filesystem boundaries replace hidden naming/PascalCase/CWD behavior; no alternative config-derived naming resolver. | DI-04 §8: same caller filename, independent content, resolved roots and no overwrite/escape. |

### 4.4 Closure Boundary and Remaining Evidence

All eight DI packages, XC-01/XC-02 and RC-01 have reconciled Design dispositions in
§§4.1–4.3. Shared is a cross-package document, not a ninth DI package. The four
conditional choices are selected; dependency and removal conditions are explicit.

The independent review's two P1 findings remain subject to an independent recheck.
The producer records Integrated in the hub only for this substantive Design
reconciliation. Native/client/runtime conformance is not claimed; Planning still
assigns bounded write sets, preserved behavior, rollback points and independent
stop/go evidence for every 126/151 path plus separately accounted support dependencies.
Research and its Approved Strategy remain frozen.

### 4.5 Documentation-Only Verification — 2026-09-12

- Primary obligation-set comparison against the frozen intake: 22 unique findings,
  19 unique invariants and 23 unique expected results; no missing or extra IDs.
  The twelve primary strategy groups total 44, with the four deferred strategies
  and F-18 separately identified. Semantic treatment is the §4.1–4.3 review,
  not a consequence of the numeric check.
- Exact catalog/index comparison: 151 entries, 151 unique, identical ordering,
  no missing/extra/duplicate or nonexistent test/helper paths. No change to the
  frozen 126-consumer/two-governing-source catalog or Research/intake files.
- Read-only local-document verification across the twelve changed Design/README
  documents: 458 local inline file-link targets exist, 33 checked closure/index
  fragment references resolve to their headings, and fenced blocks balance.
  This is not an external-link, native-tool or complete Markdown-rendering test.
- Targeted active-text search and owner review replaced obsolete Drafting/open
  contract claims. Historical version entries and explicitly superseded review
  requests remain history; implementation/conformance obligations remain open.
- MCP Git status identifies only the twelve canonical Design/README documents as
  modified. The 2,898 pre-existing untracked workshop/probe/vendor files remain
  outside this correction. No production/test/config/Research write or phase
  transition is part of the correction.

## Related Documentation

- **[docs/development/issue460/design.md][related-1]**
- **[docs/development/issue460/template-suite-catalog.md][related-2]**

<!-- Link definitions -->

[related-1]: design.md
[related-2]: template-suite-catalog.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.4 | 2026-09-12 | @imp designer | Address independent closure NOGO with semantic obligation, dependency, removal, consumer-family and conditional-disposition reconciliation; request independent recheck. |
| 0.3 | 2026-09-12 | @imp designer | Record human-approved output closure, point to consolidated canonical contracts and request combined independent review without claiming runtime evidence. |
| 0.2 | 2026-09-12 | @imp designer | Index the combined concrete-output/error-detail proposal, explicit approval boundary and source-based rationale. |
| 0.1 | 2026-09-12 | Agent | Initial draft |
