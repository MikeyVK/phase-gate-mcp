<!-- docs\development\issue460\design.md -->
<!-- template=design version=5827e841 created=2026-08-27T09:19Z updated=2026-08-27 -->
# Issue 460 Scaffolding Contract Refactor Design

**Status:** DRAFT  
**Version:** 1.84
**Last Updated:** 2026-09-11  
**Issue:** #460  
**Workflow:** Refactor / Design  
**Role:** Design integration hub

---

## Purpose

Integrate the issue #460 Design decisions without duplicating the detailed contracts
owned by the package Design documents.

The [Pre-Implementation Documentation Contract](README.md) governs this document's
shape and ownership. [Research](research.md) remains authoritative for approved
behavior, strategy, invariants, and expected results. The human owner formally authorized
Design on 2026-09-04 after the F-20 amendment review and froze Research content under the
[binding manageability conditions](README.md#binding-design-and-planning-manageability-conditions).
The [Design Intake Map](design-intake-map.md) remains authoritative for package routing.

## Scope

Current override: [example-validation withdrawal](research.md#example-validation-withdrawal--2026-09-11)
is human-approved; the human reported independent QA clean GO on 2026-09-11 and
authorized Design resumption. Example
authoring/rendering and context-schema checks remain; semantic model-example validation
and its proposed adapter/profile obligations are removed. Earlier gates below are prior
deltas; the current resumption does not pre-approve remaining Design mechanisms.

Prior gate: [generation identity/file ownership](research.md#generation-identity-and-package-file-ownership-amendment--2026-09-10).
Human-approved Research amendment, with explicit third-identity clarification on
2026-09-11. The supplied QA NOGO identified active F-10/DI-06/catalog contradictions;
these are synchronized and the human reported independent QA GO on 2026-09-11.
Design resumes. W06-B context presence/value semantics are human-approved in
[DI-01/DI-02 §7.2.1](design-suite-resolution.md#721-context-presence-and-values--approved-w06-b).
No automatic defaults; concrete schema fields/rendering remain DI-03-owned. The human
also approved one schema authority per input boundary for exposure, validation and
error feedback, consolidated in [DI-01/DI-02 §7.2.2](design-suite-resolution.md#722-one-schema-authority-per-input-boundary--approved-w06-integration).
Concrete package cases, exact resolver support, URI integration and conformance remain
open; this records the approved direction, not complete W06 or Design closure.
manifest.yaml owns template_id/purpose, .version the release label, policy.yaml the
output_profile/persistence choice. pf/sf exclude complete version/policy files and
external validation; upgrade components include all files. Earlier whole-suite snapshot
claims are superseded: pf/sf identify generation, not full installed-state equality.

The human requested the [lightweight native-fix amendment](research.md#lightweight-native-fix-amendment--2026-09-10).
W05's copy/proposal/check/rollback design is withdrawn as the default. Native source
mutation and agent-controlled verification/recovery are the new bounded strategy;
Research now fixes explicit concrete-files-only scope=targets, caller fix order and
stop-on-first-non-success. The human supplied independent QA GO for the corrected delta; Design resumes.
The catalog status P3 is corrected. The human has now approved W05's Design contract,
consolidated in [DI-05 §7.18](design-execution-adapters.md#718-apply_fixes--approved-w05-contract).
Research QA GO and human Design approval are separate; independent Design/conformance
review remains outstanding. No implementation or recovery subsystem is authorized here.

Design resumed on explicit human GO after the narrow F-20 Research correction in
commit `12665147`. The required-scope and auto-retirement constraints in
[Research](research.md#narrow-check-retesting-amendment--2026-09-05) now govern DI-05;
earlier Research review-request text records the pre-resumption hand-over, not a new
product decision. Research otherwise remains frozen. The human-approved
[2026-09-10 selection amendment](research.md#narrow-native-selection-amendment--2026-09-10)
removes generic fresh/expansion controls and adapter Git knowledge; DI-05 §7.17 owns
operation/targets/args and empty-branch guarding. Public workspace intent now uses
scope=workspace; the intermediate targets=["."] convention is rejected. configured
remains distinct and passes an empty adapter target list. The human supplied independent
QA GO for this delta and authorized Design continuation. The nonblocking P2 authority
paragraph in Research Findings is corrected. W05 is now human-approved and consolidated;
its local closure does not mark DI-05 Integrated.

**In Scope:**

- overall Design rationale and selected document topology;
- package status, dependency, decision, and coverage indexes;
- cross-package integration decisions, risks, and contradictions;
- transition and cleanup coverage at integration level;
- final Design hand-over.

**Out of Scope:**

- package-local component and interface designs;
- copied Research evidence or inventory ledgers;
- Planning cycles, implementation order, estimates, or production code;
- deferred feature work.

## Prerequisites

1. Research is closed and frozen after formal human Design authorization; its F-10/S-10 and F-20 boundaries remain binding.
2. All 44 Approved Strategy rows remain binding; new product roles, compatibility choices, or consumer families require a separate issue.
3. The [Pre-Implementation Documentation Contract](README.md) defines document
   ownership and form.
4. The [Design Intake Map](design-intake-map.md) assigns every Research obligation to
   exactly one primary Design destination.

---

## 1. Context and Requirements

### 1.1 Problem Statement

Issue #460 has a large, tightly coupled Research surface spanning public artifact
schemas, renderer graphs, mutation orchestration, validation, distribution, workflow
documentation, and test architecture. A single detailed Design document would
concentrate incompatible ownership concerns and make omissions, contradictions, and
later Planning extraction difficult.

### 1.2 Requirements

**Functional:**

- [ ] Provide one navigable Design entry point for DI-01–DI-08, XC-01–XC-02, and RC-01.
- [ ] Point every integrated decision to exactly one authoritative document and section.
- [ ] Account for every Research obligation without copying its evidence ledger.
- [ ] Expose package dependencies, contract consumers, transition obligations, and
      concrete removal ownership.
- [ ] Separate public test artifact design from repository fixture/helper architecture.
- [ ] Produce an outcome-neutral Design hand-over for independent QA.

**Non-functional:**

- [ ] Remain a thin integration hub rather than a monolithic detailed design.
- [ ] Preserve Approved Strategy without silent reinterpretation.
- [ ] Prevent duplicated contract authority across documents.
- [ ] Expose contradictions and unowned obligations before Planning.
- [ ] Support bounded, hands-on design workshops.

### 1.3 Constraints

- Design defines target responsibilities, boundaries, interactions, failure/state
  semantics, migration, removals, and proof obligations; it does not sequence cycles.
- Architecture Principles and the Documentation Standard remain binding.
- A package is not `Integrated` until its upstream and downstream effects are
  reconciled.
- Detailed documents are scaffolded only after their decision nucleus is stable.
- New evidence that makes Approved Strategy unsound stops the affected design thread
  for an explicit human decision.

---

## 2. Design Options

### 2.1 Option A: Single Monolithic Design

Place every package decision, interface, test concern, and migration detail in this
file.

**Pros:**

- one physical file to open;
- no cross-file navigation.

**Cons:**

- recreates the Research monolith;
- encourages duplicate or conflicting boundary descriptions;
- makes focused review and later Planning extraction error-prone.

### 2.2 Option B: Hub-and-Spoke Design Set

Use this file as a thin integration hub, boundary-owned package documents for detailed
decisions, and one narrowly scoped shared-contract document.

**Pros:**

- one navigation and coverage authority;
- reviewable, cohesive decision packages;
- one owner per contract with explicit dependency links;
- bounded hands-on workshops.

**Cons:**

- requires disciplined link and integration bookkeeping;
- cross-document changes require an explicit impact pass.

### 2.3 Option C: Independent Package Documents Without Hub

Let each Design package stand alone without a consolidated integration authority.

**Pros:**

- maximum local autonomy;
- small individual documents.

**Cons:**

- no reliable whole-set coverage or conflict detection;
- cross-package decisions can fall between owners;
- reviewers must reconstruct dependencies manually.

---

## 3. Chosen Design

**Decision:** Adopt the hub-and-spoke Design set defined by the issue-local README.
This `design.md` is the thin integration and coverage authority; package documents own
exact decisions; `design-shared-contracts.md` owns only genuinely cross-package
contracts.

**Rationale:** This structure preserves the complete Research authority without
creating a second monolith. It enables focused workshops and reviews, gives every
contract one owner, and retains one place to detect gaps, dependency problems,
contradictions, and incomplete migration or removal coverage.

### 3.1 Key Design Decisions

| ID | Decision | Rationale | Status |
|---|---|---|---|
| D-HUB-01 | Keep `design.md` as a thin integration hub | Navigation, coverage, dependency, and review state need one authority; detailed contracts do not | Decided |
| D-HUB-02 | Give every exact contract one package or shared-contract owner | Single ownership prevents divergent copies and makes impact auditable | Decided |
| D-HUB-03 | Split DI-03 over document/tracking and code/test artifact documents | These artifact families have distinct semantics and review seams while retaining one DI-03 responsibility | Decided |
| D-HUB-04 | Separate public test artifacts from repository test architecture | DI-03 owns generated test contracts; DI-08 owns shared fixtures/helpers and cross-package assurance | Decided |
| D-HUB-05 | Draft detailed documents through bounded workshops | Decisions can stabilize incrementally without losing whole-set traceability | Decided |
| D-HUB-06 | Give DI-05 the dedicated execution-adapter document; retain DI-04 mutation ownership | The human manageability condition keeps the enlarged check/test/fix boundary independently reviewable | Decided |

---

## 4. Design Package Register

Package status uses `Not started`, `Drafting`, `Decided`, or `Integrated`.
`Decided` means the owning document contains a complete local decision.
`Integrated` additionally means all dependency, coverage, migration, removal, and
test impacts have been reconciled in this hub.

| Document | Primary Ownership | Status | Current Focus |
|---|---|---|---|
| `design.md` | Design integration, indexes, risks, and hand-over | Drafting | Hub nucleus established |
| [design-shared-contracts.md](design-shared-contracts.md) | Genuinely cross-package interfaces, DTOs, configuration shapes, and status vocabulary | Drafting | Embedded schema delivery, operation/attachment cache boundary, and isolated package-provenance DTO boundary decided; stable URI audit open |
| [design-suite-resolution.md](design-suite-resolution.md) | DI-01 and DI-02 | Drafting | `template_suite/`, strict shallow package discovery, canonical manifest `template_id`, shared topology, explicit caller-content/operation separation, package isolation, dual canonical SHA-256/96 identities, compact provenance, and syntax-only package-version policy decided; mutation mechanics and output-profile topology remain with DI-04/DI-05 |
| [design-document-tracking-artifacts.md](design-document-tracking-artifacts.md) | DI-03 document and tracking artifacts | Decided | Ten families and nineteen workflow carriers; human-supplied independent QA GO without findings; profiles/workflow/assurance integration remains open |
| [design-code-test-artifacts.md](design-code-test-artifacts.md) | DI-03 code and public test artifacts | Decided | Nine families and shared syntax/contracts; human-supplied independent QA GO without findings; profiles/distribution/assurance integration remains open |
| [design-mutation-validation.md](design-mutation-validation.md) | DI-04 | Drafting | Location, no-overwrite, and scaffold enforce/report outcomes decided; full scaffold result and safe-edit mapping consume the separate DI-05 check boundary |
| [design-execution-adapters.md](design-execution-adapters.md) | DI-05 | Drafting | Package/check and W05 native-fix local contracts decided; W04 canonical integration, policy-loading/shared serialization, native migration values and independent conformance remain open |
| `design-test-architecture.md` | DI-08 and XC-02 integration assurance | Not started | Await package proof seams |
| [design-distribution.md](design-distribution.md) | DI-06 | Decided | Component-aware renewal, trustworthy bootstrap, owner-intent CLI, immutable result/presenter split, recoverable same-filesystem activation, timestamped force backup, runtime/startup coexistence, and conditional restart hint decided |
| `design-workflow-documentation.md` | DI-07 | Not started | Await stable public decisions |

---

## 5. Dependency and Integration Model

| Upstream Authority | Supplies | Direct Consumers |
|---|---|---|
| DI-01 | Generic artifact-contract metamodel, shared primitives, and public schema shape | DI-02, DI-03, DI-04, DI-07 |
| DI-02 | Resolved graph, selected renderer/profile identities, introspection, and provenance | DI-03, DI-04, DI-06 |
| DI-03 | Concrete artifact contracts, renderer semantics, retained identities, and removals | DI-06, DI-07, DI-08 |
| DI-05 | Check evidence for output profiles; separate check/test/fix operation contracts and execution evidence | DI-04, DI-07, DI-08; public check/test/fix consumers |
| DI-08 | Shared test infrastructure and cross-package assurance | DI-01–DI-07 |
| XC-01 | Binding architecture constraints | DI-01–DI-08 |
| XC-02 | Cross-package legacy-removal integration | DI-01–DI-08 |
| RC-01 | Approved Strategy fidelity | Entire Design set |

Dependency arrows describe consumption, not ownership transfer. Each consumer records
its local consequence and links to the upstream contract.

---

## 6. Decision Index

This index points to authoritative decisions. It does not restate their exact contract.

| Decision Range | Owner | Status | Consumers |
|---|---|---|---|
| D-HUB-01–D-HUB-06 | [Design hub §3.1](#31-key-design-decisions) | Decided | Entire Design set |
| D-SHARED-01–D-SHARED-12 | [Shared Contracts Design §4](design-shared-contracts.md#4-owned-decisions) | Drafting | DI-01/DI-02, DI-04, DI-06, DI-07 |
| D-SUITE-01–D-SUITE-33 | [Suite Resolution Design §4](design-suite-resolution.md#4-owned-decisions) | Drafting | DI-03, DI-04, DI-05, DI-06, DI-07, DI-08 |
| D-ART-DOC-01–D-ART-DOC-09 | [Document/tracking §4](design-document-tracking-artifacts.md#4-owned-decisions) | Decided; bounded external QA GO reported | DI-01/02, DI-04/05, DI-06, DI-07, DI-08 |
| D-ART-CODE-01–D-ART-CODE-10 | [Code/test §4](design-code-test-artifacts.md#4-owned-decisions) | Decided; bounded external QA GO reported | DI-01/02, DI-04/05, DI-06, DI-07, DI-08 |
| D-MUT-01–D-MUT-19 | [Mutation and Persistence Design §6](design-mutation-validation.md#6-owned-decisions) | Drafting | Scaffold and safe-edit consumers; DI-05 check-evidence integration |
| D-ADAPTER-01–D-ADAPTER-29 | [Execution Adapter Design §4](design-execution-adapters.md#4-owned-decisions) | W04/W05 human-closed; D25/D26 align defaults/scope; D28/D29 close W09 configuration ownership and concrete native starting contracts. W09 independent QA, remaining role integration, shared serialization and native conformance stay tracked | DI-02, DI-04, public check/test/fix operations, DI-07, DI-08 |
| D-TEST-* | `design-test-architecture.md` | Not started | DI-01–DI-07 |
| D-DIST-01–D-DIST-24 | [Distribution Design §4](design-distribution.md#4-owned-decisions) | Decided | CLI/init/upgrade, owner migration, DI-07, DI-08 |
| D-WORKFLOW-* | `design-workflow-documentation.md` | Not started | Phase, agent, and documentation consumers |

W09's human-approved concrete adapter and native-settings contract is in
[DI-05 §7.20](design-execution-adapters.md#720-w09--concrete-starting-adapters-and-migration-contract).
The local workshop is closed; independent QA is requested in §11. This does not close
DI-05 integration or the full Design phase.

---

## 7. Coverage Accounting

Research routing is complete; Design integration is not. A routed obligation becomes
integrated only when its owner defines the target and this hub verifies its dependency
and proof consequences.

| Coverage Set | Research Total | Routed | Integrated |
|---|---:|---:|---:|
| Findings | 22 | 22 | 0 |
| Approved Strategy rows | 44 | 44 | 0 |
| Core invariants | 19 | 19 | 0 |
| Expected results | 23 | 23 | 0 |
| Consumer families | 10 | 10 | 0 |
| Conditional catalog dispositions | 4 | 4 | 0 |
| Design packages | 8 | 8 | 0 |
| Cross-cutting obligations | 2 | 2 | 0 |
| Resolved constraints | 1 | 1 | 0 |

The detailed matrices remain in the
[Design Intake Map](design-intake-map.md). Package documents will supply decision-level
coverage; this table tracks only integration completion.

---

## 8. Transition, Cleanup, and Test Integration

The exact cutover, compatibility behavior, legacy removals, and package-owned tests are
designed in the owning package documents. This hub must ultimately prove:

- every legacy production, configuration, template, export, instruction, documentation,
  and test surface has one removal or retention owner;
- no unapproved temporary bridge or dual authority remains;
- DI-01–DI-07 own their behavioral and migration evidence;
- DI-08 provides reusable test infrastructure and audits cross-package completeness
  without taking over package behavior;
- migrated check, test, and fix boundaries each have independent conformance and
  preservation evidence;
- clean-break decisions and current-owner deployment migration follow Approved Strategy.

**Current integration state:** DI-01/DI-02, DI-06, and the shared schema-delivery seam have decided nuclei. Resolved package identity remains isolated to the selected package plus transitive shared support; suite-generation identity remains persisted source context, not complete installed-state equality evidence; both retain canonical version-1 SHA-256/96 Base64url semantics. Artifact provenance remains exactly `id`/`pv`/`pf`/`sf` on the first physical line with bounded ID/version types and no wrapping and no generic lifecycle timestamps. Package versions are SemVer-syntax-checked human labels, resolved fingerprints alone establish effective-content equality, and the four possible version/fingerprint relations remain observable without bump enforcement, warnings, or history. DI-06 owns separate 16-character operational component equality for `shared/` plus every concrete package, using distinct distribution domains and package keys copied only from `manifest.yaml:template_id`. `.pgmcp/installation.json` has an exact closed minimum contract: required `pgmcp_version` and one optional complete checkpoint whose present form requires `shared` plus the `template_id`-keyed `packages` map. Component selection constructs and validates one complete off-root proposal and changes runtime authority only through recoverable complete-tree activation. The first PGMCP v3 rollout has no predecessor v3 suite or checkpoint; neither legacy `.version` nor `template_registry.json` can fabricate one, so existing pre-v3 workspaces preserve actual content and require explicit migration before the first checkpoint becomes authoritative. `.pgmcp/upgrade/` remains the flat non-runtime candidate root. `pgmcp --upgrade` owns renewal and accepts exactly one optional owner-intent modifier: `--accept-template-baseline` derives the first complete checkpoint from the current candidate without copying content, component-bounded `--resolve-template` advances named conflicted `shared` or `template_id` entries after reconciliation, and `--force-template-upgrade` performs backed-up complete candidate replacement for a managed root. Callers never supply computed fingerprints. Renewal returns one immutable factual result to a dedicated CLI presenter; exit codes `0`, `2`, and `1` distinguish complete, safe action-required, and failed attempts, while this CLI-only path adds no MCP resource, JSON mode, or persisted result report. Complete activation uses cross-process exclusion, fixed same-filesystem next/previous roots, an immutable recovery record, deterministic rollback or forward completion, and a separately retained timestamped backup only for forced replacement. Running servers retain their old immutable catalog, concurrent startups cannot enter activation, and `actual_changed` alone derives the successful-operation hint to restart any running server. External retention/versioning remains workspace-owned without PGMCP lookup or control machinery. The human-approved F-03/F-07 correction removes the generic envelope `name`, manifest `naming`, and automatic name projection: exact `file_name`, optional directory-valued `target_path`, and `force_target` are operation controls, every caller-authored renderer value is explicit artifact context, and server-authored source provenance is separately namespaced. DI-02 now discovers concrete packages by deterministic shallow enumeration under `template_suite/`; `shared/` is the sole reserved child, every other direct child must contain a valid package, and no authored `templates.yaml` duplicates that inventory. DI-04 repurposes `.pgmcp/config/artifacts.yaml` as artifact-location policy keyed by manifest `template_id`, permits loaded packages to remain unmapped, rejects configured keys that do not resolve, and safely sends an unmapped call without `target_path` to the one global temporary root without force. An explicit workspace target outside configured roots—including one for an unmapped package—requires `force_target`; force without a target is rejected. DI-04 also fixes `.pgmcp/temp/artifacts` as the shipped temporary default, exact caller file names, canonical workspace-relative `target_path` and `output_path` values, relative operation fields and routine summaries with incidental absolute paths permitted in bounded on-demand cached diagnostics under D-MUT-20, and universal create-only scaffold semantics. The legacy `project_structure.yaml` retires only through a field-by-field and consumer-by-consumer migration; the current `EnforcementRunner` has no dependency on it, while bootstrap, `ArtifactManager`, the generic resolver, the uncomposed legacy `PolicyEngine`, tests, and active documentation receive explicit dispositions. Existing files remain safe-edit territory. The suite and mutation packages remain `Drafting` pending mutation result vocabulary and DI-05 profile/evidence topology; shared contracts retain the stable URI audit; remaining package targets are routed but undesigned.

---

The [scaffold validation outcome contract](design-mutation-validation.md#44-scaffold-validation-request-and-result-contract) fixes the input/result policy mirror, all policy/status combinations, mixed-check summaries, and independent operation/commit failures. Section 4.6 extends the shared policy vocabulary to safe edit under the approved 2026-09-07 Research amendment. This is not completion of the shared executor, full mutation result DTO, or check/test/fix result contracts.

The [dedicated DI-05 document](design-execution-adapters.md) now owns F-20 integration.
The workshops selected cohesive implementation packages and shallow manifest discovery.
One authored version and one computed fingerprint are shared by a package's roles;
the latter identifies covered package content in run evidence, not full run equivalence
or automatic compatibility. Native tool configuration now owns tool settings, without
a second stricter PGMCP settings layer. DI-05 explicitly owns the existing configuration
discrepancies and their intended migration values; exact catalog/process/role contracts
remain open. Research is unchanged. The frozen catalog has 126 consumers and 151
tests/helpers requiring concrete Planning ownership.

W-ADAPTER-03 selected manifest fields with direct consumers and one entrypoint declaration
per role; the complete manifest schema remains open. W-ADAPTER-04 proposes one named
check binding reused by profiles and explicit check operations. Exact fix-to-check
relations, applicability/input requirements, and launch syntax remain owned follow-up
work. The current generation-identity amendment removes profile/binding fingerprint
projection; DI-02/DI-05 retain policy loading and validation independently.

### Current Workshop Checkpoint — 2026-09-07

**Design resumed after independent QA GO reported by the human on 2026-09-07:**
[full safe-edit validation-policy alignment](research.md#narrow-safe-edit-policy-amendment--2026-09-07),
including retirement of mode/verify_only, is now integrated in DI-04 and its DI-05
consumer references. Both mutation tools use validation=enforce/report, default enforce,
and validation_policy output, without a temporary compatibility field or replacement
preview. Research correction commit b5fc881a is the reviewed handover basis. Other decisions
remain unchanged; historical version entries do not reinstate the superseded deferral.

DI-05 remains Drafting. Its active slice is scaffolding's consumption of check/v1,
not completion of safe-edit, run_checks, test or fix contracts. The
[scaffold input nucleus](design-execution-adapters.md#scaffold-consumer-input-nucleus)
records the intended file location and exactly one text/file input, selected by the
required requires_file boolean. No separate workspace_root is justified for this slice.

Central path resolution derives temp/artifacts and temp/validation from the configured
server root. The former artifacts.yaml temporary_root field is superseded in DI-04.
Each file-requiring check receives a fresh isolated ID directory; cleanup is separately
reported housekeeping and never overrides a valid check or its persistence policy.
There is no temp monitoring or automated sweep. Native Markdown probes establish a
bounded file-route need without authoritative target pre-writes.

Server/subprocess sandboxing is explicitly [deferred](deferred-work.md#deferred-work-notice-server-and-subprocess-security-isolation),
not silently promised by application-level permissions or internal path representation.
DI-05 now records the scaffold-facing typed request/response, DI-04 failure mapping,
shared process lifecycle and explicit executable/args launch nucleus. These remain
Design specifications, not executed conformance evidence or completion of all consumers.

The human-approved [exposure correction](design-execution-adapters.md#77-configuration-based-exposure-and-on-use-availability)
replaces the earlier startup dependency preflight/filtering promise: schemas expose
valid configured choices; missing dependencies use the existing on-use failure path.
No adapters run at startup, defaults/profiles are not silently weakened, and the health
deferral cannot assume readiness evidence from issue 460. Frozen Research is unchanged.

The active consumer workshop is safe edit: assess reuse of complete proposed-content
checks while keeping edit policy and authoritative replacement in DI-04. The approved
[shared extension assignment](design-execution-adapters.md#shared-extension-to-profile-assignment)
lives at the root of `checks.yaml`, not under `safe_edit_file`. Shared ownership does not
change scaffold manifest selection or automatically extend `run_checks` selection.
The approved [extension lookup](design-execution-adapters.md#extension-lookup-semantics)
selects the longest configured suffix of the intended basename, case-insensitively,
without globs or implicit profiles for extensionless files. Missing-assignment
behavior and selection-result facts are decided in DI-04 §4.6; governing profile-selection
integration remains Q-MUT-04. The previous verify_only deferral is superseded by the
approved clean break: remove the mode without a replacement proposed-edit preview.

The [public mutation nesting audit](design-mutation-validation.md#45-public-mutation-response-nesting-audit)
now qualifies earlier serialization sketches: singleton validation/selection wrappers
cannot be assumed to render through the existing presenter. Direct summary fields and
meaningful collections are now approved through §§4.6/4.10 of DI-04. Q-MUT-06's shape
decision is closed; real presentation/resource conformance remains required. No presenter
extension, duplicated field graph or Research amendment is authorized.

The [consolidated public result workshop](design-mutation-validation.md#46-consolidated-public-result-workshop)
records human agreement on direct fields, selection outcomes, check-record combinations,
write policies and channel dispositions, now including the Research-approved common policy names.
DI-05 integrates the required failed-decision message; the public record adds no origin
field. Legacy safe-edit mode/strict/interactive/verify_only inputs are rejected without writes.
Naming alignment is closed. The [safe-edit-specific workshop](design-mutation-validation.md#47-safe-edit-operations-no-change-results-and-failure-boundaries)
now fixes the four preserved operation behaviors, explicit content_changed/write combinations,
construction-failure versus check-failure meaning and truthful complete-content validation claims.
Do not reopen the general scaffold outcome contract to cover these consumer differences.
The [V3 reader and read/check/write slice](design-mutation-validation.md#48-v3-metadata-selection-and-readcheckwrite-consistency)
is human-approved on 2026-09-08: admit a narrow reader, preserve one original/proposed
content pair, and refuse observed intervening changes without claiming universal
external-writer exclusion. Human clarification on 2026-09-10 fixes a jointly designed
[internal header reader/writer](design-suite-resolution.md#joint-internal-header-utility),
not MCP tools; header formatting is separate from file persistence. The subsequent
human refinement fixes 24-character template IDs, 11-character package SemVer labels
and a single native-comment record on the first physical line; it supersedes overflow
wrapping. Absent/invalid headers and invalid/unknown metadata template IDs are equivalent
for applicable-profile selection: all take the explicit extension/no-profile route
without weakening validation policy or swallowing independent failures. Research
remains unchanged: exact metadata representation and this selection realization are
Design-owned. The human-approved
[integrated header contract](design-suite-resolution.md#integrated-header-production-reading-and-selection-contract)
now closes shared-tier production, text-only recognized/absent/invalid reader results,
protocol framing and recognition-only BOM handling, together with real-render and
independent conformance obligations. Q-SUITE-03 is closed at Design level, not claimed
implemented. DI-04's approved
[controlled replacement contract](design-mutation-validation.md#49-integrated-original-file-and-controlled-replacement-contract)
now fixes one original bytes/text value, manager-owned orchestration, late comparison
before every replacement attempt, lock-wait/adapter-timeout separation and independent
check/write/cleanup facts over the existing atomic writer mechanics. It retains the
external-writer race limitation without adding a general transaction or history layer.
The [approved W01 integration](design-mutation-validation.md#410-complete-mutation-operation-result--approved-2026-09-10)
fixes the normal operation-result route for expected failures, typed error/detail fields,
separate housekeeping and selection explanation. Remaining integration is explicitly
DI-05's final capture declarations, required-field/null serialization and independent
evidence; W02 native provenance and W05's lightweight native-fix contract are approved.
W05 introduces no recovery subsystem: DI-07 documents agent-controlled recovery, DI-08
owns independent partial-write and stop-first evidence, and W09 owns native-settings
migration. The next workshop is W06 suite/shared contract integration.

DI-02's conditional no-replacement boundary now admits this demonstrated V3-reader
consumer. Legacy parsing, historical lookup and automatic provenance mutation stay removed.
Package integration, exact full role schemas, native migration values and independent
conformance evidence remain open.

The accepted [50-template discovery guardrail](deferred-work.md#design-escalation-threshold--50-template-ids)
keeps enum-only ID discovery bounded as a product-design assumption. A concrete need
above that count, or earlier usability evidence, triggers the separate F-18 follow-up.
It does not cap suite size, truncate enums, add startup behavior, or bring a discovery
tool into issue 460. The future route must reduce invocation-schema size as well as
provide bounded discovery results; the detailed authority remains in the notice.
This checkpoint does not mark any additional package Integrated or authorize Planning.

## 9. Open Questions and Risks

| ID | Question or Risk | Owner | Resolution Condition |
|---|---|---|---|
| Q-HUB-01 | Which minimum shared vocabulary and contract types require a central owner? | Workshop 1 | Shared only when two or more package authorities consume the exact same semantics |
| Q-HUB-02 | What responsibility boundary and dependency direction separate DI-01 modeling from DI-02 resolution? | Workshop 1 | Target alternatives compared against Research and direct source/test seams |
| R-HUB-01 | Shared-contract scope grows into a second monolith | Design hub | Every shared item must name multiple consumers and exclude package-local detail |
| R-HUB-02 | Package documents become locally correct but mutually inconsistent | Design hub | Dependency impact pass required before `Integrated` |
| R-HUB-03 | Coverage counts hide semantic omissions | Design hub | Coverage requires an owned target decision or proof obligation, not a bare link |
| Q-HUB-03 | How do the adapter package/catalog/process and three role contracts fit together? | DI-05 | Bounded workshops complete the contracts, independent evidence, and public migration mapping |
| Q-HUB-04 | Removing duplicate tool configuration could silently alter the quality standard | DI-05 | Q-ADAPTER-06 / §7.20 records human-approved native settings and intentional changes; independent QA/conformance must verify that distinction and preserve logical-target configuration for scratch checks |
| Q-HUB-05 | Profile/binding placement must remain coherent with template provenance | DI-02/DI-05 | Resolve Q-ADAPTER-08 before integrating the check-binding proposal; preserve the distinction from adapter execution evidence |
| Q-HUB-06 | A correct core-tool schema can be lost through wrappers or stale exposure | DI-05/DI-08 | Q-ADAPTER-09 proves startup construction, registered exposure, matching validation/defaults/error feedback, and supported client refresh behavior |
| Q-HUB-07 | On-use dependency failures could weaken profiles, obscure defaults, or bypass presentation policy | DI-04/DI-05/DI-08 | Q-ADAPTER-10 retains configured selections/defaults without startup probes; proves full-profile evidence, consumer policy and field-level projection under issues 456/459 |
| Q-HUB-08 | Large template enums make agent selection unwieldy | DI-02/DI-04; separate F-18 follow-up | Apply the 50-template Design escalation threshold; preserve complete current enums and runtime membership validation without introducing a suite-size cap |

---

## 10. Planning Consequences

Planning must later derive deliverables from the authoritative package decisions and
their dependencies. It may group or order implementation work, but it may not merge
contract ownership, change Approved Strategy, or treat this document's status register
as an implementation sequence.

The [nine manageability conditions](README.md#binding-design-and-planning-manageability-conditions)
are binding: independently provable cycles, contracts/catalog/conformance before legacy
runner/parser removal, separate check/test/fix proof, separate F-10 activation and F-20
fix-application cycles, and proven internal routes before public cutover. Intermediate
code coexistence establishes no supported aliases or dual reads. Every cycle needs a
bounded write set, preserved behavior, rollback point, and independent stop/go evidence.
All 126 consumers and 151 tests/helpers need concrete owners without a catch-all cycle.

No cycles or estimates are defined during Design.

---

## 11. Refactor / Design Hand-over

### W07/W08 Bounded Design Review — 2026-09-11

**Review outcome supplied by the human:** independent QA reported no P0–P3 findings and
GO for the two concrete-template contract documents at commit
8b19e0e6ec0aa787854a915e800f837adf3e6067. QA explicitly excluded whole-Design approval.
The reviewer independently checked family coverage, contract precision, architecture,
honest validation guarantees, operational planning parity and nineteen workflow variants,
including worker logging/export and pytest fixture counterexamples. No tests were run.
The earlier request below is retained as review scope/history; integration remains open.

#### Scope

- Coordinated DI-03 design for nine retained code/test and ten document/tracking families,
  preserving correct current behavior and applying approved removals. No runtime, schema,
  Jinja or test implementation; Research strategy is unchanged.
- Human delegated the bounded content choices; no per-field workshop approval is pending.

#### Deliverables

- [Code/test contracts](design-code-test-artifacts.md): D-ART-CODE-01–10, family inventory,
  exact shared records, preservation/removal mapping and CODE-E01–10.
- [Document/tracking contracts](design-document-tracking-artifacts.md): D-ART-DOC-01–09,
  shared records, retained capacities, planning projection and DOC-E01–11.
- Material authorities: [Research](research.md), [Findings](research-findings.md),
  [Catalog](template-suite-catalog.md), [Suite resolution](design-suite-resolution.md).

#### Evidence

- Source inspection covered current family configs, concrete roots, shared tier/pattern
  seams and regression-test dispositions. Two delegated read-only audits supplied findings;
  they are producer preflight, not independent QA authority.
- Explicitly repaired earlier proposal omissions include actual import forms, concrete
  override composition, document scope/prerequisites, concept-specific diagrams/subsections,
  generic section bullets/checklists, reference method/evidence grouping and validation identity.
- No runtime tests executed: these are design artifacts, with independent implementation
  evidence requirements rather than claims of working code.
- Read-only document checks found fourteen required sections in each new document,
  consistent Markdown table columns and no missing relative file-link targets.
  Delegated preflight corrections distinguish planned verification from observations,
  preserve PR prose, clarify native fixture selection and retain explicit import forms.

#### Open Work

- Bounded independent W07/W08 review is complete as reported above; subsequent integration
  and whole-Design review remain open.
- W09/DI-05 now records human-approved native profiles/checks; its independent review is below. DI-07 aligns instructions and references;
  DI-08 assigns conformance evidence. These dependencies are not marked Integrated.
- Whole-Design coverage, remaining packages and final hand-over remain open.

#### Review Request

- Historical review request (answered by the supplied verdict above): check every retained family and approved removal against the current
  graph/catalog, optionality and shared records, no template-specific pgmcp logic, source
  validity claims, planning parity and all nineteen workflow variants. Identify any
  undocumented behavior loss; do not treat this producer's inventory as proof of completeness.

### W09 Bounded Design Review — 2026-09-11

#### Scope

- Review DI-05's concrete initial adapter contracts, native settings migration and
  configuration-only composition. The human accepted these local workshop decisions;
  no independent W09 verdict or whole-Design approval is claimed.
- No production, test, native config, schema or template implementation. Research
  remains frozen; W07/W08's independent approval is a material input, not W09 approval.

#### Deliverables

- [Execution adapters §7.20](design-execution-adapters.md#720-w09--concrete-starting-adapters-and-migration-contract):
  nine packages; exact content/selection declarations; native request/result boundaries;
  initial bindings/profiles; settings and intentional changes; independent evidence.
- Same document §§7.4.1–7.4.3 and §§7.13–7.19: package/role/provenance, content/scratch,
  transport, args, selection, mutation authority and configuration ownership contracts.
- [Research](research.md), [Findings F-08/F-19/F-20](research-findings.md),
  [Design intake DI-05](design-intake-map.md), [consumer catalog](template-suite-catalog.md).
- [Code/test contracts](design-code-test-artifacts.md),
  [document/tracking contracts](design-document-tracking-artifacts.md),
  [header reader and suite contracts](design-suite-resolution.md).
- Existing seams: [PythonValidator](../../../mcp_server/validation/python_validator.py),
  [MarkdownValidator](../../../mcp_server/validation/markdown_validator.py),
  [QAManager](../../../mcp_server/managers/qa_manager.py),
  [RunTestsTool](../../../mcp_server/tools/test_tools.py),
  [PytestRunner](../../../mcp_server/managers/pytest_runner.py),
  [quality.yaml](../../../.pgmcp/config/quality.yaml),
  [pyproject.toml](../../../pyproject.toml), [Pyright config](../../../pyrightconfig.json).

#### Evidence

- Source inspection and primary native references informed the design; §7.20 G indexes
  those references. Earlier executed Lychee feasibility is explicitly bounded in §7.13.
  No new native probes, runtime tests or quality gates were run for W09.
- Producer-delegated read-only preflight identified the Mypy test-target widening and
  missing Markdown preservation cases; both were incorporated. This is findings-only
  producer assistance, not independent review authority.
- Local document checks verified section presence, table continuity and relative file
  links. They do not establish adapter behavior or native-version conformance.

#### Open Work

- Independent bounded W09 review requested. DI-06 must prove installed package and
  dependency delivery (including the commit adapter's shared header-reader dependency);
  DI-07 owns accurate guidance; DI-08 owns reusable conformance architecture.
- Full role DTO integration and whole-Design cross-package consistency remain open.
  Check/test/fix implementation evidence must precede legacy runner/parser removal.
- Existing deferred sandbox, startup-health presentation and unrelated extension work
  remain outside this slice; no new deferred product decision is introduced.

#### Review Request

- Review requested: independently test the design against source behavior, not only
  its own tables. Focus on role-safe native args, operational success versus domain
  outcomes, content-only versus selection exposure, real native configuration authority,
  warning-preserving Markdown versus explicitly stronger Lychee, metadata-aware commit
  validation and dependency/distribution feasibility.
- Distinguish approved stricter Ruff/Mypy defaults and explicit Mypy test-target
  selection from accidental behavior loss. Check native settings completeness and
  that no product decision is hidden as implementation detail.
- Use committed canonical artifacts, not the untracked temporary workshop/probe tree,
  as authority. Return bounded findings and GO/NOGO for W09, not the whole Design phase.

### Whole-Design Hand-over (still in progress)

### Scope

- Designed target structure and exclusions: In progress.

### Deliverables

- [Design](design.md)
- [Pre-Implementation Documentation Contract](README.md)
- [Research](research.md)
- [Design Intake Map](design-intake-map.md)
- Structural/test seams: To be added by the owning package documents.

### Evidence

- Target versus rejected structures: Hub-and-spoke selected over monolithic and
  uncoordinated document sets.
- Invariant and Approved Strategy preservation: Research routing complete; Design
  integration pending.
- Test architecture and cleanup design: Pending DI-01–DI-08 decisions.

### Open Work

- Resolve all package decisions, cross-package contracts, removal routes, and evidence.
- Deferred work remains governed by [Deferred Work](deferred-work.md).
- The [startup-health notice](deferred-work.md#deferred-work-notice-agent-facing-startup-health-and-recovery) excludes health logic, health-first guidance, and new general tool blockades. Complete configuration-based check/test/fix inputs and on-use dependency failures remain in issue 460, without startup adapter probes; future diagnostics are not a completion or V3-cutover prerequisite.

### Review Request

- Not yet requested; Design is in progress.

## Related Documentation

- [Pre-Implementation Documentation Contract](README.md)
- [Research](research.md)
- [Research Findings](research-findings.md)
- [Design Intake Map](design-intake-map.md)
- [Shared Contracts Design](design-shared-contracts.md)
- [Suite Resolution Design](design-suite-resolution.md)
- [Code and Test Artifact Contracts](design-code-test-artifacts.md)
- [Document and Tracking Artifact Contracts](design-document-tracking-artifacts.md)
- [Execution Adapter Design](design-execution-adapters.md)
- [Template Suite Catalog](template-suite-catalog.md)
- [Deferred Work](deferred-work.md)
- [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md)

---

The [approved diagnostic disclosure boundary](design-mutation-validation.md#diagnostic-disclosure--approved-2026-09-10)
closed W01-F: preserve relative operation fields and portable artifacts while using
existing on-demand cached native diagnostics, with no private-log replacement or claim
that resource retrieval is local-only. DI-05 applies the same boundary to check/test/fix.
The subsequent W01-A–E approval is recorded in DI-04 §4.10. Research remains frozen;
W02 is approved in
[DI-05 §§7.4.1–7.4.3](design-execution-adapters.md#741-w02-package-contract--approved-2026-09-10):
explicit adapters.yaml trust under the existing configroot and typed native-tool identity
inside ordinary cached run evidence complete the package boundary. The existing scaffold
response is explicitly amended; no new query tool or runtime config is implemented here.
W03 is approved in [DI-05 §7.14](design-execution-adapters.md#714-approved-run_checks-contract--w03-2026-09-10).
It consolidates prior scope/profile/native decisions and adds the explicit caller timeout
override; no internal termination-budget change. W04 public input/exposure is approved
in [DI-05 §7.15](design-execution-adapters.md#715-approved-run_tests-input-and-exposure--w04-2026-09-10):
flat tests IDs and addressed CLI args in one startup schema supersede native options_schema.
Only run_tests changes; the check/scaffold/safe-edit/fix inputs remain unchanged. Continue
W04 with test results and remaining configuration/transport, not a whole-pipeline redesign.
Later proposals, concrete DTO integration, actual conformance and independent Design
review remain open; Research and template/artifact authority are unchanged.

## Version History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.84 | 2026-09-11 | `@imp designer` | Record human W09 closure and bounded independent QA hand-over; preserve open DI-05 and whole-Design integration. |
| 1.83 | 2026-09-11 | `@imp designer` | Index concrete W09 adapter/configuration proposal separately from approved decisions; retain bounded open settings work. |
| 1.82 | 2026-09-11 | `@imp designer` | Index W09 configuration-only starting-set decision; retain exact native migration and integration work. |
| 1.81 | 2026-09-11 | `@imp designer` | Record independent W07/W08 GO without findings; mark local contracts Decided and retain cross-package integration and whole-Design review. |
| 1.80 | 2026-09-11 | `@imp designer` | Register source-led W07/W08 contracts and bounded independent review; preserve open whole-Design integration and Research authority. |
| 1.78 | 2026-09-11 | `@imp researcher` | Withdraw semantic model-example validation on human instruction; preserve example authoring/rendering and request targeted QA. |
| 1.77 | 2026-09-11 | `@imp designer` | Index approved shared schema authority and distinguish completed consumer decision from remaining resolver/URI/conformance work. |
| 1.76 | 2026-09-11 | `@imp designer` | Index approved W06-B unchanged-context and present/empty/absent behavior; remaining schema integration stays open. |
| 1.75 | 2026-09-11 | `@imp designer` | Record human-reported independent generation-identity QA GO and Design resumption; preserve remaining workshop decisions. |
| 1.74 | 2026-09-11 | `@imp researcher` | Route explicit operational component identity clarification and QA corrections; keep Design paused for independent re-review. |
| 1.73 | 2026-09-10 | `@imp researcher` | Route generation identity and package file split; mark targeted QA pending and preserve full operational upgrade equality. |
| 1.72 | 2026-09-10 | `@imp designer` | Record W05 human approval and DI-05 §7.18 consolidation; route native migration, presentation and conformance follow-through without Research or implementation changes. |
| 1.71 | 2026-09-10 | `@imp designer` | Correct catalog P3 and record human-supplied native-fix Research QA GO; resume Design without pre-approving W05 DTOs. |
| 1.70 | 2026-09-10 | `@imp researcher` | Resolve QA scope/stop blockers through human-approved files-only and stop-first policy; remove fix-transaction and stale gate handovers. |
| 1.69 | 2026-09-10 | `@imp designer` | Record lightweight native-fix amendment; withdraw proposal/verification/rollback promises; preserve agent-controlled recovery and request independent review. |
| 1.68 | 2026-09-10 | `@imp designer` | Correct QA P2 authority routing; record human-supplied independent QA GO and Design resumption without changing approved behavior. |
| 1.67 | 2026-09-10 | `@imp designer` | Correct public workspace intent: scope=workspace replaces dot target shorthand; configured remains native discovery; adapter transport unchanged. |
| 1.66 | 2026-09-10 | `@imp designer` | Record bounded native-selection correction: PGMCP owns Git resolution; operation/targets/args adapter requests; no generic fresh/expansion controls; targeted review requested. |
| 1.48 | 2026-09-07 | `@imp researcher` | Mark the narrow human-authorized safe-edit alignment/verify_only retirement amendment and targeted QA pause; supersede old preservation notes without further Design work. |
| 1.49 | 2026-09-07 | `@imp designer` | Record human-reported independent QA GO and Design resumption; integrate common mutation policy vocabulary and legacy-mode removal in DI-04/DI-05; retain open diagnostic/provenance integration. |
| 1.50 | 2026-09-07 | `@imp designer` | Index approved safe-edit-specific operations, no-change result and failure boundaries; move the next workshop to V3 reader and read/check/write consistency. |
| 1.51 | 2026-09-08 | `@imp designer` | Index approved V3-reader responsibility and bounded pre-write consistency guard; reconcile DI-02/04/05 references and retain explicit header/interface integration work. |
| 1.52 | 2026-09-10 | `@imp designer` | Index human-confirmed joint internal header utility with separate reader/formatter consumers; retain shared-template integration and header recognition as the next bounded design slice. |
| 1.53 | 2026-09-10 | `@imp designer` | Index bounded manifest/provenance types, first-line-only metadata and human-authorized invalid-header fallback; preserve Research scope and explicit-input/catalog failure boundaries. |
| 1.54 | 2026-09-10 | `@imp designer` | Index human-confirmed equivalence of absent/invalid headers and invalid/unknown metadata IDs for consumer profile selection; remove the exceptional unresolved-metadata-ID failure. |
| 1.55 | 2026-09-10 | `@imp designer` | Close the approved integrated header utility Design nucleus and Q-SUITE-03; route remaining original-file comparison, atomic writing and operation presentation into one DI-04 workshop. |
| 1.57 | 2026-09-10 | `@imp designer` | Index human-approved W01-F diagnostic disclosure; refine the earlier blanket cache-path prohibition without changing Research, operation paths or remaining workshop approval status. |
| 1.58 | 2026-09-10 | `@imp designer` | Index approved W01-A–E, distinguish remaining integration obligations and move human review to prepared W02 without approving its package/provenance choices. |
| 1.59 | 2026-09-10 | `@imp designer` | Index partial W02 approval, preserve separate trust/provenance review and unchanged template discovery/artifact-location configuration authority. |
| 1.60 | 2026-09-10 | `@imp designer` | Index W02 closure and explicit scaffold payload amendment; advance human review to W03 without approving its selection/scope/result proposals. |
| 1.61 | 2026-09-10 | `@imp designer` | Index approved W03 consolidation and caller timeout override; advance review to test-specific W04 decisions without approving test/fix proposals or reopening Research. |
| 1.65 | 2026-09-10 | `@imp designer` | Index D25/D-MUT-22: fixed configured mutation validation, execution defaults with explicit caller replacement and argument evidence; acknowledge W04 closure without conflating remaining integration with new approval. |
| 1.64 | 2026-09-10 | `@imp designer` | Consolidate approved W04 configured/targets, passed and native-option ownership corrections; index D23/D24 without approving remaining configuration/output proposals or non-test args routing. |
| 1.63 | 2026-09-10 | `@imp designer` | Index D-ADAPTER-22: correct run_checks success/isError conflation with domain verdicts; preserve negative results as correctly reported tool output. |
| 1.62 | 2026-09-10 | `@imp designer` | Index W04 public test input/exposure approval and scoped supersession of native options_schema; keep other consumers and remaining W04 result/configuration/transport choices separate. |
| 1.56 | 2026-09-10 | `@imp designer` | Index approved original-value and controlled-replacement contract; close consistency responsibility choices and route final typed mutation facts/cache/presentation into the next integrated workshop. |
| 1.47 | 2026-09-07 | `@imp designer` | Record consolidated result agreement with explicit exception for safe-edit policy vocabulary; retain the deferred-mode boundary and integration work. |
| 1.46 | 2026-09-07 | `@imp designer` | Index the consolidated mutation-result workshop and approved failed-message/no-public-origin correction; keep remaining proposal and integration boundaries explicit. |
| 1.45 | 2026-09-07 | `@imp designer` | Index public mutation nesting audit and unresolved projection gaps while preserving decided semantics, internal protocols and deferred scope. |
| 1.44 | 2026-09-07 | `@imp designer` | Index verify_only removal deferral and exclude further mode-specific Design except for concrete conflicts introduced by issue-460 functionality. |
| 1.43 | 2026-09-07 | `@imp designer` | Index approved extension lookup and move the active safe-edit workshop to missing-profile mode behavior without claiming complete selection integration. |
| 1.42 | 2026-09-07 | `@imp designer` | Index shared profiles_by_extension ownership and the active safe-edit lookup workshop; keep provenance-reader reconciliation and consumer policy explicitly open. |
| 1.41 | 2026-09-07 | `@imp designer` | Index the approved 50-template F-18 escalation threshold and coherent discovery/invocation follow-up without runtime limits, truncation or new issue-460 tooling. |
| 1.40 | 2026-09-07 | `@imp designer` | Index the human-approved replacement of startup availability preflight/filtering by configured selections and on-use failures; preserve full profiles, defaults, Research freeze and health deferral. |
| 1.39 | 2026-09-06 | `@imp designer` | Refresh active DI-05 scaffold checkpoint: input nucleus, derived temporary paths, per-check isolation, non-blocking cleanup and security deferral; identify response workshop next. |
| 1.38 | 2026-09-05 | `@imp designer` | Record human-authorized Design resumption and route amended required-scope/native-fresh Research into DI-05; retire earlier reuse direction. |
| 1.37 | 2026-09-05 | `@imp designer` | Index human rejection of prepared-work/session complexity and reopened reuse feasibility; preserve frozen Research and scope safeguards. |
| 1.36 | 2026-09-05 | `@imp designer` | Index internal check preparation/execution and optional reliable reuse support without adding agent-facing exposure or new adapter roles. |
| 1.35 | 2026-09-05 | `@imp designer` | Index shared cross-scope run_checks evidence reuse and explicit fresh-execution intent; keep storage and exact input/result contracts open. |
| 1.34 | 2026-09-05 | `@imp designer` | Index approved auto semantics and bounded current-state direction without selecting evidence storage or cross-scope updates. |
| 1.33 | 2026-09-05 | `@imp designer` | Index approved working-state branch selection and auto inclusion obligation without prematurely selecting incremental evidence storage. |
| 1.32 | 2026-09-05 | `@imp designer` | Index approved check-scope expansion boundary; retain exact incremental scopes and protocol design as open work. |
| 1.31 | 2026-09-05 | `@imp designer` | Index the explicit startup-health deferral while retaining complete availability-aware check/test/fix inputs and ordinary operation presentation. |
| 1.30 | 2026-09-05 | `@imp designer` | Index approved startup availability filtering and the issues 456/459 presentation constraints; route remaining consumer admission and response projection without changing Research. |
| 1.29 | 2026-09-05 | `@imp designer` | Index the startup-bound schema lifecycle and registered-wrapper/lazy-exposure proof obligation; no runtime or Research changes. |
| 1.28 | 2026-09-05 | `@imp designer` | Record manifest-nucleus agreement and index shared check binding/profile selection as proposed; route the DI-02/DI-05 provenance integration obligation. |
| 1.27 | 2026-09-05 | `@imp designer` | Index the role-organized manifest proposal and direct field consumers; retain complete capability bindings, fix/check relations, and launch syntax as explicit DI-05 follow-up. |
| 1.26 | 2026-09-05 | `@imp designer` | Index accepted discovery and native tool-configuration ownership; clarify adapter fingerprint evidence limits and route existing configuration discrepancies to DI-05 without reopening Research. |
| 1.25 | 2026-09-05 | `@imp designer` | Record the accepted DI-05 package boundary and package-wide version/fingerprint trade-off; index the next discovery and consumer-reference proposal. |
| 1.24 | 2026-09-05 | `@imp designer` | Reconcile the frozen F-20 intake, create the dedicated DI-05 navigation and decision boundary, refresh 22/44/19/23 coverage, and carry the nine manageability conditions into Design and Planning integration. |
| 1.23 | 2026-09-03 | `@imp designer` | Index the scaffold enforce/report outcome contract, mixed evidence and operation/commit boundaries; retain full DTO, safe-edit mapping, and DI-05 execution work as open. |
| 1.22 | 2026-09-03 | `@imp designer` | Make scaffold target and result paths canonically workspace-relative, reject absolute target input, keep native absolute resolution internal, and exclude the physical workspace root from normal tool/cache exposure. |
| 1.21 | 2026-09-03 | `@imp designer` | Resolve optional location registration with a safe global-temporary fallback, one-way template_id reference validation, force-gated explicit targets for unmapped packages, and no per-template temporary-root machinery. |
| 1.20 | 2026-09-03 | `@imp designer` | Make `template_id` the canonical manifest identifier, select strict shallow package discovery without a central template index, repurpose `artifacts.yaml` for artifact-oriented placement, and record the exhaustive `project_structure.yaml` consumer/field migration. |
| 1.19 | 2026-09-03 | `@imp designer` | Start DI-04 with the consumer-oriented target and mutation nucleus: configured workspace/temporary placement, exact file names, bounded force-target behavior, universal scaffold no-overwrite, and safe-edit ownership of existing-file changes. |
| 1.18 | 2026-09-03 | `@imp designer` | Remove premature concrete Worker/package examples from the suite design so DI-03 artifact identities and DI-05 profile IDs remain genuinely undecided until their owning workshops. |
| 1.17 | 2026-09-03 | `@imp designer` | Integrate the human-approved F-03/F-07 correction: remove envelope-name projection and manifest naming, make artifact context the sole caller-authored render source, keep exact file/target controls operation-only, and isolate server provenance. |
| 1.16 | 2026-09-03 | `@imp designer` | Integrate the syntax-only package-version policy: fingerprints alone establish content equality, all four version/fingerprint relations remain observable, and no bump enforcement, warning service, or historical state is introduced. |
| 1.15 | 2026-09-03 | `@imp designer` | Mark DI-06 locally decided after integrating cross-process exclusion, same-filesystem activation, deterministic interruption recovery, force-only retained backup, startup/runtime coexistence, and the conditional server-restart hint. |
| 1.14 | 2026-09-03 | `@imp designer` | Integrate the decided renewal presentation contract: immutable factual result, dedicated CLI presenter, actionable complete output, explicit `0`/`2`/`1` exits, and no MCP resource, JSON mode, or persisted result report. |
| 1.13 | 2026-09-03 | `@imp designer` | Integrate the concise owner-intent CLI: whole-candidate `--accept-template-baseline`, component-bounded `--resolve-template`, mutually exclusive force semantics, and no caller-supplied fingerprints. |
| 1.12 | 2026-09-03 | `@imp designer` | Integrate the exact manifest-`template_id` checkpoint contract, domain-separated 16-character operational fingerprints, required shared state, and explicit no-fabrication migration for the first PGMCP v3 suite rollout. |
| 1.11 | 2026-09-03 | `@imp designer` | Reconcile the reviewed F-10/S-10 amendment across the hub: separate operational component checkpoints from artifact provenance, register three-way selection plus complete-proposal activation, restore future upgrades after explicit reconciliation, and remove the superseded component-adoption deferral. |
| 1.10 | 2026-08-31 | `@imp designer` | Fix the DI-06 installation workflow: minimal `installation.json`, flat `.pgmcp/upgrade/` candidate root, thin `--upgrade` orchestration, explicit complete promotion, and no selective-reconciliation acknowledgement state. |
| 1.9 | 2026-08-31 | `@imp designer` | Register the DI-06 distribution nucleus: package-aware actual/candidate reporting and agent reconciliation with complete-suite-only automatic mutation, one bounded adopted checkpoint, and explicitly deferred component-level adoption. |
| 1.8 | 2026-08-30 | `@imp designer` | Close the fingerprint-mechanics workshop with canonical SHA-256/96 identities, compact `id`/`pv`/`pf`/`sf` provenance, deterministic overflow wrapping, and removal of generic lifecycle timestamps. |
| 1.7 | 2026-08-30 | `@imp designer` | Reconcile the independently confirmed two-fingerprint provenance and narrowed ownership promise across the suite and shared-output contracts before resuming fingerprint mechanics. |
| 1.6 | 2026-08-29 | `@imp designer` | Reconcile the reviewed F-10/F-11 amendment across the suite and shared-contract registers before resuming fingerprint mechanics. |
| 1.5 | 2026-08-28 | `@imp designer` | Register the approved `template_suite/` layout, concrete `template.jinja2` packages, flat tiered shared bases, shared patterns/definitions, TypeScript DTO consolidation, and historically recoverable deferred YAML removal. |
| 1.4 | 2026-08-27 | `@imp designer` | Close the minimum manifest field audit and register the finite generic naming resolver, immutable derived-name boundary, persistence lifetime, and remaining DI-04 explicit-path decision. |
| 1.3 | 2026-08-27 | `@imp designer` | Register the manifest identity/naming rationale, template-package version versus fingerprint nucleus, and bounded output-profile responsibility with DI-04/DI-05 follow-up. |
| 1.2 | 2026-08-27 | `@imp designer` | Register the shared schema-delivery and suite-resolution packages, their decided nuclei, remaining audits, consumers, and authoritative links. |
| 1.1 | 2026-08-27 | `@imp designer` | Establish the agreed thin hub with package, dependency, decision, coverage, risk, transition, and hand-over registers; correct scaffolded related-document paths. |
| 1.0 | 2026-08-27 | `@imp designer` | Scaffold the Design document from the approved hub-and-spoke nucleus. |
