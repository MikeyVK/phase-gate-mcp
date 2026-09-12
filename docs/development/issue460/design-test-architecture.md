<!-- docs\development\issue460\design-test-architecture.md -->
<!-- template=design version=5827e841 created=2026-09-12T08:02Z updated= -->
# Issue 460 Test Architecture and Cross-Package Assurance Design

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-09-12  
**Primary Package:** DI-08; XC-02 cross-package assurance  
**Upstream Dependencies:** Frozen Research I-14/E-17 and catalog; all DI-01–DI-07 public contracts  
**Downstream Consumers:** Package-owned tests, shared support, canonical Design audit and Planning ownership  
**Lifecycle Status:** Human-approved W12; locally closed; canonical integration and independent review pending

## 1. Purpose and Authority

Own small shared test-support boundaries, test architecture and cross-package removal
assurance. The human approved W12 on 2026-09-12. DI-01–DI-07 retain their behavioral
contracts, migration evidence and concrete production removals. W12 approval is not
independent QA, executed conformance or whole-Design closure.

## 2. Scope and Exclusions

Cover affected fixtures/helpers, isolated dependency injection, role/process/filesystem
test support, installed-package proof, public composition, test dispositions and canonical
coverage accounting. Include directly affected plugin/factory consumers even when they
are supporting dependencies rather than original census rows.

Exclude a new runtime test framework, copied template/config registry, automatic test
generation per field, unrelated test cleanup, semantic model-example validation, native
fix rollback/proposal mechanisms, result reuse, and Planning cycle allocation.

## 3. Binding Inputs

- [Research gate/strategies](research.md), [DI-08/XC-01/XC-02/RC-01 intake](design-intake-map.md),
  [frozen 126-consumer/151-test catalog](template-suite-catalog.md), I-14 and E-17.
- [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md):
  public APIs, explicit dependencies, immutable values, no duplicated config authority.
- [Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md) and [form contract](README.md).
- [Suite/schema/header contracts](design-suite-resolution.md),
  [shared delivery](design-shared-contracts.md), [mutation](design-mutation-validation.md),
  [code/test artifacts](design-code-test-artifacts.md),
  [document/tracking artifacts](design-document-tracking-artifacts.md),
  [adapters](design-execution-adapters.md), [distribution](design-distribution.md),
  [workflow/documentation](design-workflow-documentation.md).
- Existing support: [artifact_test_harness](../../../tests/mcp_server/fixtures/artifact_test_harness.py),
  [test_support](../../../tests/mcp_server/test_support.py),
  [fake_pytest_runner](../../../tests/mcp_server/fixtures/fake_pytest_runner.py),
  [root conftest](../../../tests/conftest.py),
  [integration conftest](../../../tests/mcp_server/integration/mcp_server/conftest.py),
  [MCP conftest](../../../tests/mcp_server/conftest.py).

## 4. Owned Decisions

| ID | Decision | Status |
|---|---|---|
| D-TEST-01 | Shared setup follows narrow public dependency boundaries, not private production classes; explicit isolated state and immutable values | Human-approved |
| D-TEST-02 | Review both the durable behavior and architectural quality of every affected test; retain valuable intent even when its construction must change | Human-approved |
| D-TEST-03 | Separate adapter/native, consumer and public-composition proof; migrated tools cannot be their own sole oracle | Human-approved |
| D-TEST-04 | Use small synthetic packages for rejection/extensibility and actual delivered packages for acceptance; no second template inventory | Human-approved |
| D-TEST-05 | Legacy removals require owned replacement evidence or explicit no-retained-behavior rationale; preserve unrelated callers/plugins | Human-approved |
| D-TEST-06 | Canonical obligation/removal audit is issue-local documentation, not runtime machinery or a Planning catchall | Human-approved |
| D-TEST-07 | Real process/installed-artifact evidence proves claims doubles cannot; reuse fresh relevant evidence without per-field or per-test build inflation | Human-approved |

## 5. Responsibilities and Boundaries

| Owner | Behavioral evidence remains with |
|---|---|
| DI-01 | Schema/ref/presence semantics and exposure |
| DI-02 | Graph/catalog, identity isolation, provenance and first-line header |
| DI-03 | Every retained artifact family and approved removed families |
| DI-04 | Create-only and guarded edits, enforce/report, atomic persistence and truthful mutation results |
| DI-05 | Catalog/process/role contracts, selection/args, native settings, direct fix application and stop-first |
| DI-06 | Wheel/install, component comparison, checkpoint/admission, activation and recovery |
| DI-07 | Workflow meanings, instruction authority, reference removal and source-copy alignment |
| DI-08 | Shared support topology, dependent callers and cross-package no-gap audit |

A fixture supplier does not acquire ownership of every test that consumes it.
test_support.py retains DI-05's primary catalog routing; DI-08 specifies its shared
architecture constraints. Synthetic negative data is not a replacement product schema.

## 6. Options and Rationale

| Alternative | Decision |
|---|---|
| Rename the broad existing harness and keep hidden setup | Reject: preserves duplicated schemas, environment inference and legacy collaborators |
| Rebuild the entire server in every unit test | Reject: couples unrelated tests and inflates cost; reserve full composition for integration |
| Delete shared helpers without caller tracing | Reject: can break unrelated plugin/fixture behavior |
| Prove everything through new public check/test/fix tools | Reject: producer and oracle can share the same defect |
| Narrow injected support plus independent evidence | Select: test the promised boundary with the smallest sufficient setup |

## 7. Detailed Design

### 7.1 Shared Support Contracts

These are test-only responsibilities and input/output shapes, not new production APIs.
Use existing frozen values, public interfaces and configuration models wherever applicable.

| Support | Explicit input/output contract | Consumers / exclusions |
|---|---|---|
| Isolated roots | Caller-selected temporary parent; immutable named workspace/server/config/template/bundled-adapter/workspace-adapter/temp Path values | DI-01/02/04/05/06; no ambient CWD/environment inference |
| Synthetic package-tree writer | Explicit mapping of contained relative file names to bytes; returns isolated root | Negative graph/schema/component cases; no invented default IDs/schemas/profile rules |
| Role-specific recording doubles | Explicit typed check, test or fix result/error fixtures; captured public invocation requests | DI-04/05; not a generic Pytest-shaped runner and no stringly typed result factory |
| Controlled adapter process | Selected known protocol output, stderr, exit, delay or child behavior; disposable process handles | DI-05 transport/limits/termination; not fake-only proof of OS process behavior |
| Filesystem fault support | Injected public write/guard/activation boundary, explicit failure point, observations and final bytes | DI-04/06 where their contracts promise atomicity/recovery; not native fix rollback |
| Installed-distribution fixture | Built artifact and isolated installation; public entrypoints/resources outside source checkout | DI-06 delivery and DI-05 bundled adapters; no native dependency auto-installer |
| Registered-tool composition | Real wrappers, cache and presentation; explicit domain collaborators and isolated cache | Cross-package integration only; no hidden manager construction or global singleton state |

A recording double may expose its own public call log. It does not inspect private state
of production objects. Verify ordering only where it is an observable contract, such as
explicit fix sequence/stop-first, not incidental private call order.

Environment/CWD changes are permissible in tests whose subject is that boundary, scoped
and restored. They are not default manager/schema fixture setup. Admitted config uses
production readers/models; invalid test data is explicitly authored. Never widen a public
production API solely to inspect private implementation for tests.

### 7.2 Behavior and Architecture Dispositions

Use the frozen catalog path as identity, plus one primary behavioral owner. The Design
review records each affected test's durable claim, public proof boundary, behavioral
disposition and architecture disposition, with a removal prerequisite when applicable.

Behavior vocabulary: keep, adapt, replace or remove. Architecture vocabulary: compliant,
adapt, replace or remove. These are review classifications, not a new runtime schema.
For example, a useful persistence test may retain its claim but replace its CWD-dependent
harness; a well-written test for a deliberately removed registry may be removed.

Reuse the existing ledger and package-owned dispositions; do not copy 151 inventories
into every document. The canonical integration audit must resolve ambiguous or unowned
cases. Planning later maps every exact 126/151 path and affected supplemental dependency
to a bounded cycle. This document does not claim that per-path audit has already finished.

### 7.3 Concrete Support Dispositions

| Existing file | Required disposition | Preserved boundary / owner |
|---|---|---|
| artifact_test_harness.py | Replace the broad schema/config/CWD/default-construction harness with §7.1 support | Retained caller claims must have replacement evidence before plugin/fixture retirement; DI-08 support, package owners behavior |
| test_support.py | Adapt/split affected environment/config/legacy-composition helpers | Preserve unrelated useful builders; DI-05 catalog owner, DI-08 architecture constraints |
| fake_pytest_runner.py | Replace generic runner double with test/v1 contract double | Preserve deterministic outcomes; real native Pytest behavior remains DI-05-owned |
| tests/conftest.py | Adapt old harness plugin registration and legacy templates/config session setup when dependencies migrate | DI-08 supplemental integration owner; preserve workflow_fixtures plugin and unrelated collection |
| tests/mcp_server/integration/mcp_server/conftest.py | Adapt make_test_server dependency through public composition | DI-08 supplemental integration owner; preserve existing GitHub mocking and unrelated server tests |
| tests/mcp_server/conftest.py | No unrelated cleanup | Preserve CreateBranchInput singleton reset unless a directly affected dependency demonstrates need |
| tests/mcp_server/unit/conftest.py | Preserve unrelated scoped environment fixture | No server/log/GitHub test-environment refactor is implied by suite support changes |
| tests/mcp_server/fixtures/workflow_fixtures.py | Preserve workflow plugin semantics; adapt root/loader acquisition only if the shared dependency changes | DI-08 supplemental dependency owner; public ConfigLoader-derived phase results remain unchanged |

The supplemental conftest/plugin consumers do not silently change the frozen 126/151
Research census. Track them explicitly in Design/Planning support accounting. Changes
inside a shared file must stay bounded to the affected consumers; no repository-wide
test refactor is authorized by a helper's presence in this table.

### 7.4 Independent Evidence Levels

| Level | Example | Limit |
|---|---|---|
| Adapter/native | Invoke an adapter process directly with known fixture input; inspect raw protocol/exit/native effects and validate its declared role output | Does not prove manager selection, persistence or MCP presentation |
| Consumer/domain | Feed a failed typed check to scaffold/safe-edit; inspect enforce/report and file bytes; feed a failed fix and observe later bindings unstarted | Does not prove actual native invocation |
| Public composition | Invoke registered tool and read cached structured result with normal wrapper/presentation | Necessary integration, not sole adapter/manager certification |

Use independently known expected bytes for exact header/fingerprint protocols and
relational properties for package-local/shared/policy changes. Expected values must not
be obtained from the production function under test. Do not write a second full
fingerprint engine into shared fixtures.

Native parity tests preserve only approved retained behavior. Accepted W09 Ruff/Mypy
changes are explicit deltas, not failures to imitate V2. A controlled non-Python adapter
fixture proves a generic process contract; it does not by itself establish all real
Node/native package behavior.

### 7.5 Failure and Preservation Examples

- A valid failed check remains a domain result; consumer persistence and operational
  success are asserted according to their separate DI-04/05 contracts.
- Configured targets=[] differs from an empty branch resolution: the latter makes no
  invocation and emits no false pass certificate.
- Native fix step one may write; if step two fails after writing, those bytes may remain
  and step three is unstarted. Assert no promised generic rollback or verification chain.
- A scratch cleanup warning cannot replace a valid check result; scratch unique-ID and
  intended-path rules remain DI-05-owned.
- Missing profiles reject template admission without changing actual/checkpoint;
  missing native dependencies do not introduce renewal execution probes.
- Complete activated suite/checkpoint recovery belongs to DI-06, distinct from native
  fix partial mutation. Do not share a transaction fixture that conflates these contracts.
- A wheel lacking a required schema, policy, .version or adapter entrypoint fails delivery
  proof even if the repository checkout makes a local smoke test pass.
- First-line header tests assert exact syntax and boundaries; whole document prose
  snapshots do not replace semantic rendering/field-presence evidence.

## 8. Control, Data, and State Flow

Start from an owned public claim. Select the narrowest fixture, invoke the public
boundary, and compare observed effects/results with independent expected facts.
Clean up test-created resources through their explicit ownership. Retain failed evidence
without claiming unavailable native checks were executed.

For integrated tests, follow actual request selection through domain handling, adapter
invocation, persistence when authorized, cache publication and presentation. Use distinct
cases for native domain findings and generic operational/protocol failure. This package
adds no production flow, error status or recovery state.

## 9. Compatibility, Migration, and Removal

Each legacy removal requires its package owner and either replacement behavior evidence
or explicit no-retained-behavior rationale. Trace imports, fixture requests and plugin
registration before retiring a shared helper. No source/prose snapshot is automatically
valuable merely because it currently passes.

Use the catalog's hidden-aware root search method at the relevant migration/closeout
boundary, including root project/packaging config and mapped host files. Historical
archives stay historical; temporary internal coexistence is not a supported alias or
dual-read strategy. Preserve unrelated tests and their production behavior.

## 10. Test and Validation Design

| Evidence ID | Required claim |
|---|---|
| TEST-E01 | Isolated roots and explicit config eliminate cross-test environment/CWD leakage outside dedicated environment tests |
| TEST-E02 | Synthetic invalid graphs/packages and actual delivered packages remain separate; no copied schema/catalog oracle |
| TEST-E03 | Check, test and fix each have direct role/native proof plus separate consumer/public integration |
| TEST-E04 | Real process limits, malformed responses, timeouts and descendant stopping are proven at the supported OS boundary, not only mocked |
| TEST-E05 | Public file effects prove the different DI-04 mutation, DI-05 partial-fix and DI-06 recovery promises |
| TEST-E06 | Installed artifacts resolve outside the source checkout with required files and declared dependency entrypoints |
| TEST-E07 | Shared helper/plugin changes preserve retained and unrelated callers; removals have named prerequisites |
| TEST-E08 | Canonical obligation/removal accounting has no missing owner or contradictory contract and distinguishes design from executed evidence |

These are evidence families, not a mandate for eight new files or a test per field.
Reuse valuable existing cases, public helpers and fresh results. Build/native evidence
can be shared until relevant inputs change; do not rebuild or install dependencies for
each unit test.

Performed for this consolidation: source inspection of the listed support seams and
catalog, document checks and producer consistency review. No runtime/native tests,
wheel build, deployment or complete 151-test semantic re-audit is claimed.

## 11. Integration Risks and Open Questions

No remaining W12 product choice. Canonical integration, exact per-path disposition
completion and independent review remain open. Existing status prose or TODOs must not
be treated as proof that an exact DTO/URI/removal boundary is complete.

Risks: a new tool certifies itself; shared fixtures hardcode product knowledge; removed
legacy tests lose retained behavior; broad support cleanup touches unrelated domains;
fake process proof overclaims OS guarantees. Sections 7–10 bound these risks.

A genuine new product/compatibility choice is returned to the human. Frozen Research is
not amended merely to make a proposed test easier.

## 12. Planning Consequences

Planning assigns every 126/151 catalog row and touched supplemental dependency to concrete
cycles with bounded write sets, preserved behavior, rollback points and independent
stop/go evidence. No implement-DI-05 or remaining-consumers/tests mega-cycle.

Adapter contracts, catalog and independent conformance exist before legacy runner/parser
removal. Check/test/fix migration is separately proven. F-10 activation and F-20 fix
application never share one implementation cycle. Public V3 cutover follows working
internal routes. This Design specifies constraints, not cycles or execution permission.

## 13. Traceability Matrix

| Obligation | Design/proof |
|---|---|
| I-14 / E-17 and approved test-suite architecture strategy | §§5–7 narrow injected support, two-dimensional dispositions; TEST-E01/E02/E07 |
| DI-08 | Entire document; reusable support without acquiring package behavior |
| XC-01 | Frozen values, public interfaces, explicit config, no duplicate oracle; TEST-E01/E02 |
| XC-02 | §§7.2–7.3/9 owned removals, caller/plugin tracing and complete audit; TEST-E07/E08 |
| RC-01 | §§2/11/12 preserve Research strategy and deferred exclusions |
| 151 tests/helpers | Existing ledger path authority; §§7.2–7.3 completion rules and supplemental dependencies |
| 126 consumers plus two governing sources | Distinct accounting; no census inflation or remaining-consumers cycle |
| DI-01/02/03 consumers | Real schema/graph/header/artifact evidence, synthetic negative support; TEST-E02 |
| DI-04/05 consumers | Separate persistence/role/process/partial-fix assertions; TEST-E03–05 |
| DI-06/07 consumers | Built-artifact and instruction evidence support with unchanged behavioral ownership; TEST-E06–08 |

## 14. Related Documentation and Version History

[Design hub](design.md), [intake](design-intake-map.md), [catalog](template-suite-catalog.md),
[deferred work](deferred-work.md), [workflow/documentation](design-workflow-documentation.md).

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-09-12 | @imp designer | Consolidate human-approved W12 support, evidence independence, dispositions and canonical closeout criteria; no implementation or independent verdict. |
