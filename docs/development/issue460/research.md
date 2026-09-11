# Research: Issue 460 — Scaffolding Schema–Template Rendering Contract Audit

**Status:** RESEARCH FROZEN — GENERATION IDENTITY QA GO REPORTED; DESIGN RESUMED  
**Version:** 3.40  
**Last Updated:** 2026-09-11  
**Issue:** 460  
**Workflow:** Refactor / Research

## Purpose

### Generation Identity and Package File Ownership Amendment — 2026-09-10

The human approved separating template generation sources, release labels and acceptance/
persistence policy into distinct package files. This is a bounded amendment to F-11/S-16,
I-03 and E-07 plus F-10 comparison safeguards; no new adapter role or consumer family.

| Boundary | Approved strategy |
|---|---|
| Generation contract | manifest.yaml owns only template_id and purpose; context.schema.json and template.jinja2 retain caller-contract and rendering ownership |
| Release label | One package-local .version file owns the existing human SemVer; this is a package version, not per-file versioning. Existing syntax/length and persisted pv semantics remain |
| Acceptance/persistence policy | policy.yaml owns output_profile and persistence exclusively; profile selection/validation and enforce/report behavior remain unchanged |
| Package fingerprint pf | Includes complete admitted generation-source/contract files and transitively reached shared support, including descriptive content/comments; excludes whole .version and policy.yaml files and all external validation config |
| Suite fingerprint sf | Includes all admitted generation-source/contract files across the supplied suite, including shared support; applies the same whole-file exclusions. It no longer proves complete installed-suite equality |
| Upgrade equality | Operational shared/package component fingerprints continue to compare ALL admitted component files, including .version and policy.yaml. Neither pf nor sf may authorize overwrite, checkpoint advancement or whole-installed-snapshot equality |
| Metadata | id/pv/pf/sf and their first-line/length rules remain; pv comes from .version. Identifier metadata does not recursively enter fingerprint calculation |
| Compatibility | V3 clean break: no old five-field manifest read, duplicate fields, fallback version source or compatibility alias. Existing V2 migration boundary remains |
| Adapter packages | Unchanged: this amendment concerns template packages only, not adapter manifests, versions, fingerprints or default_args behavior |

All included generation files contribute as a whole under the established deterministic
normalization rules, including their descriptive comments. No per-field fingerprint
filter, dead-code analysis, or comparison of example render output is introduced.
Canonicalization must not silently discard comments in included manifest/schema sources;
Design must reconcile the earlier semantic-only serialization description accordingly.
policy.yaml cannot acquire rendering inputs/defaults/switches: that would violate its
exclusion rationale. purpose is included as the description of the generation contract.
Moving validation policy out of identity does not make that policy optional or bypass
startup coherence, on-use checks, or the existing persistence decision.

**Trade-off and rejected alternatives.** Keeping the five-field manifest requires opaque
per-field exceptions. Hashing all of it conflates release/policy changes with generation.
The accepted split adds two small authored files but gives each fact one visible owner.
Equal pf/sf now means equal fingerprinted generation inputs, not equal complete workspace,
validation results, package release labels or artifact bytes (caller data and pv vary).
The suite label/source context does not promise retention, lookup or full reconstruction.
Git/retained full sources remain owner responsibilities, not a new registry or proof service.

**Preservation evidence.** Change only .version, only output_profile, only persistence,
or external profile/default_args: pf and sf remain equal. The first three still change
operational package comparison; external configuration remains outside suite-component
ownership. Change an included comment/description/template/schema: the appropriate pf
and sf change; unrelated packages keep pf. Shared generation changes affect exactly
transitive package consumers. Prove policy/version-only local edits participate in
adopted/actual/candidate conflict detection and cannot be lost through generation equality.
Prove one source per field, V3 old-field rejection, unchanged profile consumers, and pv
loaded from .version. This is required evidence, not an executed implementation test.

**Direct evidence.** [version_hash.py](../../../mcp_server/scaffolding/version_hash.py)
extracts template version labels with fallbacks and computes tier-based hashes;
[template_registry.py](../../../mcp_server/scaffolding/template_registry.py) persists
hash-to-tier/version mappings. [test_version_hash.py](../../../tests/mcp_server/test_version_hash.py)
asserts version sensitivity and eight-character results. These are existing V2 seams,
not proof of V3 generation or operational-component equality. Their already-catalogued
replacement obligations must cover the new policy/version exclusions and upgrade guards.

**Blast radius and ownership.** Existing loader/catalog/hash/header/introspection tests
and source seams stay with DI-01/DI-02; DI-04 still consumes catalog policy; DI-05 resolves
profiles but contributes no external validation projection to template identity; DI-06
owns complete operational comparison; DI-07 guidance and DI-08 conformance follow through.
The 126-consumer/151-test catalog is unchanged; this amendment changes dispositions, not
the existing-source census. W06 default materialization is not approved by this amendment.

**Current gate:** the human reported independent QA GO on 2026-09-11 and authorized
Design resumption. The generation-identity strategy is frozen; remaining Design is not pre-approved.
No production/config files or implementation cycles are changed by this amendment.

#### Fingerprint consumers and upgrade authority — human clarification 2026-09-11

The human explicitly confirmed that three identity kinds are intended, not two names
for one comparison. They have separate consumers and may never substitute for one another.

| Identity | Contents | Consumer / persistence |
|---|---|---|
| pf | Selected generation files plus transitively used shared generation sources; no .version, policy.yaml or external validation config | Generation provenance in artifacts and existing package-directed evidence |
| sf | All included generation files across the supplied suite; same exclusions | Suite-generation provenance in artifacts; never complete installed-state equality |
| Operational component fingerprint | Every admitted local source file of one package, including .version and policy.yaml, or every admitted file of shared/; package records do not include shared transitively | Adopted component map in .pgmcp/installation.json; actual/candidate values computed for upgrade decisions, never artifact metadata |

Full installed-state equality requires equal component presence/key sets and every
operational component fingerprint. A legacy or ambiguous persisted hash and pf/sf do
not prove that condition. Any trustworthy persisted evidence used for bootstrap must
explicitly have this full operational scope and match the available source tree;
otherwise preserve actual and require the existing owner-directed baseline path.
No new whole-suite hash, history registry or per-file digest ledger is introduced.

A policy-only or version-only local edit changes operational package comparison even
when pf/sf stay equal. If candidate also changed that package and differs from actual,
retain the whole actual package as a conflict. If only upstream changed it, select the
candidate. If only actual changed it, preserve actual. No automatic per-file policy merge.
A version-only change is protected directly, never through an assumption that a version
bump must also change generation sources. The same full operational evidence governs
checkpoint advancement and activation/recovery identities; generation equality cannot
authorize a write. Exact bytes versus source normalization must be described honestly:
the existing BOM/line-ending normalization is not literal byte identity. No admitted
source/policy field or descriptive comment may be dropped from operational coverage.

**QA follow-up:** the supplied review returned NOGO for conflicting active F-10,
DI-06 and catalog instructions. Those passages are synchronized with this clarification;
the human subsequently reported independent QA GO and authorized Design on 2026-09-11.
This records external review authority, not producer GO.

### Lightweight Native-Fix Amendment — 2026-09-10

The human explicitly requested developing the lightweight native-fix direction after
rejecting mandatory fix/check interleaving and generic copy/transaction machinery.
This amends only the existing F-20 fix application strategy and E-23; no new role,
consumer family, census row or compatibility bridge is introduced.

- apply_fixes is an explicitly requested source-mutation operation. PGMCP resolves
  selected bindings/targets and invokes trusted fix adapters in a defined order.
  Adapters invoke native fixers directly on authorized source targets.
- Native configuration remains the settings SSOT. Binding default_args and addressed
  caller replacement retain the approved rule; arguments do not grant additional
  filesystem or role authority. Generic PGMCP does not parse native switches.
- Do not require replacement proposals, generic workspace copies, pre-application
  verification, stale-byte transactions, rollback journals or automatic restoration.
  A failure, timeout or malformed result after launch may leave source changes.
  No all-or-nothing, no-lost-update or failure-means-no-write guarantee is offered.
- Agentic sequencing remains check, assess, fix, recheck and possibly safe_edit.
  No automatic repair loop, required post-fix check, or safe-edit autofix mode is added.
  A fix/check capability relation is discovery information, not an execution dependency.
- Git checkpoints and targeted restoration are explicit agent/human actions using
  existing tools, not hidden apply_fixes behavior. No required clean worktree, automatic
  commit/stash/reset or private backup system. Only captured content is recoverable
  from a checkpoint; later unrelated edits must not be discarded during recovery.
- Report per-execution native outcomes and process diagnostics without certifying
  check correctness. Do not invent an exact changed-file list from Git dirty state.
  Operational success remains inverse MCP isError, independent of native exit/verdict.
- Explicit target containment and adapter role conformance remain mandatory; direct
  native execution is not an OS sandbox or a guarantee against a misbehaving trusted
  extension. The separate sandbox deferral is unchanged.

#### Approved fix scope and stop policy — human decision after QA

These are binding Research product decisions, not Design-owned options.

| Boundary | Approved behavior | V2 preservation or deliberate V3 break |
|---|---|---|
| Public scope | Require scope=targets on every apply_fixes call; reject omitted scope and auto, branch, project, workspace and configured | Removes implicit auto/default and broad selection through the approved clean break |
| Target set | Require a nonempty list of concrete existing workspace files; no directories, globs, recursive expansion or "." workspace shorthand | Caller determines a visible bounded file set instead of bulk discovery |
| Fix selection/order | Require an explicit nonempty ordered selection of fix bindings; execute in caller order | Replaces implicit all-fix-capable-gates/configuration order |
| Stop | Stop before the next fix after the first non-success: failed, unavailable, invalid request, timeout, crash, malformed response, cancellation or unconfirmed termination | Deliberately replaces current continue-on-error |
| Mutation after failure | Earlier changes remain; the failed attempted fix may also have changed source; report honestly | Retains native mutation, adds no rollback or no-write guarantee |
| Follow-up | Agent decides checks, safe edits or targeted Git recovery | No mandatory prior-check token, automatic recheck or recovery loop |

Non-success is the adapter's declared operation outcome or a generic execution fault,
not a raw native exit code or the public success/isError flag. A native-successful
no-change operation permits the next fix. Reject an invalid public request before
starting any fix; remaining known obligations after a stop are reported as unstarted,
not fabricated native failures. No continue-on-error switch is added.

The human reports fixes normally follow identified fixable check findings. This is
usage rationale, not measured telemetry or a required dependency on a prior check.
Files-only admission trades bulk convenience for explicit mutation bounds; stopping
trades automatic completion of independent later fixes for agent assessment of partial
state. Broader scope and continue-on-error were considered and not selected for V3.

Trade-off: this preserves native behavior and avoids copying/recovery machinery, but
accepts partial mutations and external recovery decisions. The scope, explicitness,
caller order and stop policy above are decided. DI-05 owns their schemas, typed outcomes,
evidence representation and ordering mechanisms, not a new policy choice. DI-07 documents the agentic
flow and limitations; DI-08 proves authorization and truthful failure reporting.
F-10 renewal and DI-04 mutation policies remain unchanged, with separate evidence.

The human supplied independent QA GO for the corrected native-fix strategy and
explicit scope/order/stop policy. The sole nonblocking P3 concerns the catalog status
heading, now corrected. Design resumes; this GO does not approve future DTOs or mechanisms.
All other Research remains frozen.

### Narrow Native-Selection Amendment — 2026-09-10

The human owner explicitly approved this bounded F-20 correction during Design.
Remove generic fresh and expansion controls; preserve native configuration and
explicit per-use/default or caller args instead. Default checking remains narrow.
Broader native checking requires deliberate configured-use/profile selection of such
arguments or an explicit caller request, never automatic fallback. No generic native
flag parser, cache-bypass guarantee, or permission-negotiation mechanism is required.

PGMCP owns branch target resolution, including working-state changes, deletions and
renames. Selection adapters receive only existing resolved targets, or an explicitly
empty target list for native configured selection, plus operation and effective args.
Adapters receive no removed_targets or other Git information and perform no Git
selection. If branch resolution leaves no existing targets, do not invoke adapters:
return an empty selection with PGMCP-owned deletion evidence, not a configured run or
a passing certificate. Git resolution failure remains distinct from empty selection.

Keep scope mandatory for run_checks. Its choices are configured, workspace, targets and branch;
run_tests uses configured, workspace and targets. workspace explicitly selects the
workspace directory; public targets must not encode that intent as ".". PGMCP supplies
the resolved root as an ordinary adapter target. configured still supplies targets=[].
No project alias or subproject model is retained.
Scaffold/safe-edit retain fixed configured proposed-content validation, without caller
native args or selection controls. Native configuration remains the tool-settings SSOT.

This supersedes only the 2026-09-05 generic fresh/expansion promises and scope spelling.
No new role, consumer family, strategy row, census entry, persistence policy, fingerprint
or renewal mechanism is introduced. DI-05 owns contracts/resolution, DI-07 guidance and
DI-08 independent proof. All other Research stays frozen. The human has supplied
independent QA GO for this amendment, including explicit workspace scope, and authorized
Design continuation. The sole nonblocking P2 concerned stale authority wording in
Research Findings; that paragraph is corrected without changing the approved strategy.

### Narrow Safe-Edit Policy Amendment — 2026-09-07

The human owner explicitly reopened this boundary after rejecting a temporary
preservation boundary for the already-deferred `verify_only` mode. Earlier Design GO
remains historical authority for all other scope. The human reported independent QA GO
on the corrected delta (b5fc881a) on 2026-09-07 and authorized Design resumption.
This exception does not reopen F-20 roles, template
provenance/renewal, consumer families or the complete census.

Amend the existing Safe-edit post-edit validation strategy, rather than adding another
strategy row: both scaffold and safe edit expose `validation: enforce|report`, default
enforce, and report the effective policy as `validation_policy`. Retire safe-edit
`mode`, `strict`, `interactive` and `verify_only` at the V3 cutover, without aliases,
dual reads, a replacement dry-run flag or a new preview tool. This intentionally removes
the ability to validate a proposed edit without writing when it passes. Existing
read-only check operations are not claimed as an equivalent proposed-edit preview.

Preserve complete proposed-content validation, the existing edit operations, safety and
atomic persistence, and policy-independent check facts. Enforce blocks mutation when
required validation does not pass; report retains findings without treating a negative
or unavailable verdict alone as a write prohibition. Independent operational/safety
failures still block both policies. No adapter execution or native validation rule changes.

Evidence and alternatives are in the
[bounded finding amendment](research-findings.md#safe-edit-policy-alignment-amendment--2026-09-07).
DI-04 owns the public mutation-contract change; DI-05 preserves check facts, DI-07
updates active guidance and DI-08 verifies removal. Existing catalog paths receive
updated dispositions; no new finding ID, strategy count or consumer family is introduced.
The previous verify_only deferral is explicitly superseded, not a continuing constraint.

Establish the observable content, compatibility, ownership, and portability boundaries required for first-time-right scaffolding by humans and LLM callers.

The public caller contract is the output of `scaffold_schema`. Template configuration, Jinja sources, loader and packaging code, tests, and reference documentation are evidence about that contract, not alternative caller authorities.

This document is the sole authority for issue-460 decision status, Approved Strategy, expected results, open work, and the Research gate. Detailed evidence is retained in [Research Findings](research-findings.md). The [Design Intake Map](design-intake-map.md) is the subordinate authority for complete primary Design coverage; it cannot change Research decisions. The [Pre-Implementation Documentation Contract](README.md) governs the form, topology, and navigation of the Research and Design set without changing this document's content authority.

## Current Status and Gate

The [generation identity amendment](#generation-identity-and-package-file-ownership-amendment--2026-09-10)
is the current reviewed gate. The human supplied independent QA GO on 2026-09-11
and authorized Design resumption; this is not producer approval.

The [2026-09-10 native-selection amendment](#narrow-native-selection-amendment--2026-09-10)
is a prior reviewed delta: the human supplied independent QA GO and authorized
Design resumption. Its nonblocking P2 authority-paragraph correction is recorded in
Research Findings; no new product decision or producer-issued approval is added. The prior
[2026-09-07 narrow safe-edit policy amendment](#narrow-safe-edit-policy-amendment--2026-09-07)
records the prior reviewed gate; the human reported independent QA GO on the
corrected delta (b5fc881a) and Design resumed on 2026-09-07. The earlier check-retesting decisions remain binding but are not the
current review gate. All other Research remains frozen; the following 2026-09-04
account is historical.

Research was explicitly reopened by the human owner on 2026-09-04 after Design investigation showed that the approved F-19 boundary was too narrow. Sharing executable check facts between rendered-output validation and quality-gate orchestration while leaving behavioral tests in a Pytest-specific subsystem and fixes as secondary quality-gate commands would create three incompatible extension models and preserve language knowledge in generic server code.

F-20 records the human-approved scope expansion. PGMCP 3.0 will expose one language-agnostic adapter extension suite with separate versioned `check`, `test`, and `fix` contracts. Adapter packages may implement one or more roles, but shared discovery, trust, process transport, package versioning, and package fingerprinting do not collapse their distinct semantics or side-effect boundaries. The clean break renames the executable public/configuration vocabulary to `run_checks`, `run_tests`, and `apply_fixes`, backed by `checks.yaml`, `tests.yaml`, and `fixes.yaml`; no V2 alias or dual-read bridge is retained. A quality gate remains a workflow/policy consumer of evidence, not an executable adapter role.

This amendment supersedes only F-19 wording that preserved `run_quality_gates`, treated autofix as quality orchestration, or excluded behavioral tests from the shared extension boundary. It does not collapse tests into checks, authorize checks to mutate, move persistence policy into adapters, alter template-package/source-suite provenance, or require PGMCP to retain external adapter history or binaries.

- All 22 public artifact types and all 79 packaged template-suite files retain their existing dispositions.
- The affected runtime/setup/project-configuration/agent/documentation census expands from 102 to 126 consumers; two separately catalogued governing-standard source rows are explicitly excluded from that count.
- The affected test/helper census expands from 105 to 151 rows.
- The Design Intake Map now assigns all 22 finding IDs, 44 strategy rows, 19 invariants, and 23 expected results.
- Independent QA accepted the substantive F-20 direction but returned NOGO on commit `5e465868d6779838929dd1f9b16a1d97306515d4` because the former 117/143 catalog claim was incomplete and not reproducible.
- The first producer remediation added six active consumer/reference paths and eight test/helper paths and made the counting rule explicit.
- Targeted QA on commit `d92a2ca4dbe1ba2b8523389e051fc1179191318f` confirmed those corrections but returned NOGO because the enumerated search roots excluded active root-level project/package configuration.
- The workspace-root, hidden-aware repetition found and routed three further direct hits—`pyproject.toml`, root `README.md`, and the generated VS Code/Copilot coordination-agent variant—raising the active-consumer census to 126 while leaving the test census unchanged.
- The final targeted QA gate is reported closed, and the human owner formally authorized Design on 2026-09-04.
- Research is now content-frozen. The approved direction and complete catalog remain binding Design input; any newly proposed product role, compatibility choice, or consumer family requires a separate issue.

## Narrow Check-Retesting Amendment — 2026-09-05

**Historical approval, amended by the 2026-09-10 native-selection decision above:** the owner explicitly approved removal of `auto`, no PGMCP
execution-result reuse, native optimization with an explicit `fresh` request, and a
bounded return to Research followed by independent QA. The rest of Research remains
frozen. This amends the existing F-20 strategy, not the issue's product roles or census.

### Approved Strategy Refinement

- Remove `auto` from `run_checks`, including its implicit default, baseline advancement,
  and automatic failed-file replay. Keep branch, workspace, and explicitly selected
  path coverage. `scope` is required on every `run_checks` call. Omitting it produces
  an input validation error before any check or adapter execution; there is no implicit
  branch/workspace fallback or auto alias. The owner explicitly approved this omission
  behavior after QA identified the missing caller decision. A profile selects checks,
  not scope; neither profiles nor native args supply a default scope.
  Requiring selection avoids unexpectedly broad workspace work or unexpectedly limited
  branch coverage. Design owns the concrete schema/error presentation, not this decision.
- Do not build PGMCP execution-result reuse, cross-scope validity tracking, adapter
  reuse keys, or prepared-work/session protocols for that purpose. Cached operation
  DTOs/resources, logs, presentation and invoked adapter provenance remain supported:
  storing a report is not skipping execution based on an old result.
- Normally respect native configuration for caching/incremental analysis. Do not
  force caching on through a second hidden PGMCP tool-settings layer.
- Native config and effective args own analysis reuse; no generic fresh input or
  unsupported-fresh guarantee survives. Preserve default narrow checking and truthful
  requested/actual native coverage. Broader native work requires deliberate configured
  use or explicit caller args, not automatic scope fallback. PGMCP owns branch resolution
  and deletion evidence; adapters receive no Git metadata. See the 2026-09-10 amendment.
- Retire only the auto-specific state responsibility and its consumers. Keep unrelated
  workflow/phase state, report resources, test state, and template-suite
  renewal checkpoints. Existing obsolete check-state data is not migrated into a new
  validity cache; Design must specify its safe inert-data cleanup disposition.
- Keep adapters language-agnostic and practical to author. This amendment does not
  impose prepare/execute sessions or a dependency-validity oracle on extension authors.

This expressly supersedes the former catalog requirement to retain public auto-scope
behavior and the conditional preservation of auto baseline/failed-file state.
[Detailed evidence and alternatives](research-findings.md#f-20-narrow-amendment--bounded-retesting-and-native-optimization)
and [catalog dispositions](template-suite-catalog.md#bounded-retesting-amendment--2026-09-05)
record the exact affected boundary. DI-05 owns contracts/state removal; DI-07 owns
active guidance; DI-08 owns cross-package evidence. F-10 and all unrelated decisions
remain unchanged. Counts remain 22 findings, 44 strategy rows, 19 invariants, 23
expected results, 126 consumers plus two governing sources, and 151 tests/helpers.

### Human-Approved Scope Terminology Clarification

Historical terminology decision, refined by the 2026-09-10 amendment: explicit
workspace selection uses scope=workspace, not targets=["."]. The human rejected the
intermediate dot-as-workspace proposal and approved explicit public workspace selection.
The no-subproject and orthogonal-profile boundaries below remain unchanged.

The owner explicitly authorized this surgical Research correction and continuation
of Design: the V3 `run_checks` scope value is `workspace`, replacing `project` without
an alias. It denotes the whole workspace selection under the applicable inclusion,
exclusion and check-applicability rules; the rename does not expand its coverage.
File/directory selection and branch selection remain independent of check/profile
selection. Ordinary profiles may select only one language's checks or mix languages;
this adds no language selector, special profile type, or PGMCP subproject model.
Native tools may retain their own project/configuration concepts. Historical evidence
using the existing `project` value is not rewritten as if V2 already used `workspace`.
DI-05 owns the V3 schema/rejection contract and DI-07 the terminology migration;
the existing catalog owners and all census/strategy totals remain unchanged.

### Gate and Review

The owner subsequently authorized Design resumption after commit `12665147`, and
explicitly authorized the terminology-only clarification above while continuing
Design. The review-request account below is the historical pre-resumption hand-over,
not a renewed pause or a producer-issued QA verdict. Other Research remains frozen.

The latest independent QA verdict was NOGO with one blocker: unspecified behavior when
scope is omitted. The human-approved required-scope rule above addresses that gap;
independent confirmation is still requested. No Design GO is inferred from this edit.

Independent QA is requested for this amendment. The prior Design GO remains historical
approval for the earlier baseline, not approval of this change. Do not resume Design
until the targeted review has been completed and progression is authorized. No
production, test, active-config, or Design implementation is performed by this amendment.

## Human Design Authorization and Binding Manageability Conditions

The human owner formally authorized Design on 2026-09-04 subject to the following binding phase-management conditions. These conditions constrain document ownership, proof order, and later implementation decomposition; they do not add a product role, compatibility strategy, consumer family, or implementation mechanism to Research.

1. Research is content-frozen. Any new product role, compatibility choice, or consumer family requires a separate issue.
2. DI-05 receives its own Design document. Combining its adapter execution boundary with scaffold/safe-edit mutation would obscure separate responsibilities.
3. Planning decomposes DI-05 and the consumer migration into multiple independently provable cycles; neither `implement DI-05` nor `migrate all consumers` is an acceptable single cycle.
4. Adapter contracts, the resolved catalog, and independent conformance evidence exist before legacy runners or parsers are removed.
5. Check, test, and fix migration are proven separately.
6. F-10 renewal activation and F-20 fix application occur in different implementation cycles because each has distinct atomicity and recovery risk.
7. Public PGMCP 3.0 cutover occurs only after the new internal routes are proven. Intermediate commits may contain new and legacy code together, but may not establish a supported dual-read or alias strategy.
8. Every implementation cycle has a bounded write set, explicit preserved behavior, its own rollback point, and independent stop/go evidence.
9. Planning assigns every one of the 126 catalogued consumers and 151 tests/helpers to a concrete cycle owner. A catch-all `remaining consumers/tests` cycle is a Planning blocker.

## Scope

### In scope

- All 22 artifact types currently exposed through `scaffold_schema`.
- All 79 files in the active packaged template suite.
- Configured and embedded examples, resolved inheritance/import graphs, unreachable sources, and runtime overrides.
- Schema discoverability, representability, determinism, consumption, completeness, optional safety, and portability.
- Runtime, setup, packaging, renewal, test/helper, agent-instruction, and active-documentation consumers.
- Compatibility and migration strategy per affected public boundary.
- Observable responsibilities that must be retained, adapted, or removed.
- The human-approved F-19 reconciliation of rendered-output validation and check execution at one factual check boundary, including safe-edit pre-mutation validation.
- The human-approved F-20 scope expansion to one language-agnostic adapter extension suite with separate `check`, `test`, and `fix` contracts, generic process/discovery/trust infrastructure, clean-break public/configuration vocabulary, bounded fix application, and independent migration evidence.

### Out of scope

- Production fixes or implementation sequencing.
- Target class topology, parser APIs, provider containers, staging paths, or digest serialization.
- Snapshot tests or a server-owned matrix of template-specific prose.
- Cross-repository implementation.
- New YAML or Python artifact types deferred from issue 460.
- Subjective artifact-quality evaluation beyond declared contracts and output profiles.

## Problem Statement

Issue 460 began with four confirmed PR scaffolding defects:

1. `related_docs` has no reliable schema-valid clickable-link representation.
2. `closes_issues` accepts ambiguous strings while the renderer adds its own prefix.
3. `tracking_state` is exposed but not rendered.
4. `checklist_items` cannot express the checked state consumed by the template.

The audit established that these are suite-level contract failures. Some schema-valid values fail during rendering or produce malformed, incomplete, ambiguous, or machine-specific output. Some renderer-required values cannot be constructed from `scaffold_schema`, while other exposed values are ignored.

## Research Questions

1. What does `scaffold_schema` expose for every public artifact type?
2. Can every renderer-consumed value be constructed from that introspection alone?
3. Does every exposed value have one deterministic meaning and observable effect?
4. Do minimal and property-complete valid contexts render substantively correct output?
5. Does the resolved graph include every inherited and imported contract contributor?
6. Can the suite own and evolve its content contract independently from pgmcp-server?
7. Which compatibility, migration, and preservation decisions require human approval before Design?
8. Which executable check facts and factual result semantics must rendered-output validation and public check execution share without collapsing their distinct policies, scopes, side effects, or evidence responsibilities?
9. How can check, behavioral-test, and fix extensions share one package/discovery/process infrastructure while retaining separate contracts and allowing new languages or tools without generic server-code changes?

## Evidence Authority

| Evidence | Authority |
|---|---|
| [Research Findings](research-findings.md) | Detailed observations, option analysis, blast radius, and historical rationale |
| [Template Suite Work Catalog](template-suite-catalog.md) | Complete inventory and per-component disposition state |
| [Probe Evidence](probe-evidence.yaml) | Exact durable minimal/property-complete contexts and outcomes for 44 calls |
| Live `scaffold_schema` and `scaffold_artifact` tools | Reproduction of the current public caller behavior |
| [Deferred Work](deferred-work.md) | All future work explicitly excluded from issue 460 |
| [Design Intake Map](design-intake-map.md) | Complete primary Research-to-Design coverage without target-design or implementation authority |
| This document | Decision status, Approved Strategy, expected results, open work, and Research gate |

Cached tool resources and ignored temporary outputs are supplementary diagnostics only. They are not durable evidence authorities.

## Executive Findings

| ID | Finding | Human/LLM impact | Affected boundary |
|---|---|---|---|
| F-01 | Nested collection members are absent or typed as strings where templates consume objects. | A caller cannot infer valid shapes; schema-valid inputs can fail or render blank content. | scaffold_schema, template content |
| F-02 | Optional values are normalized to null-equivalent values while templates often distinguish only undefined values. | Omission can become render failure, literal None-like content, or changed defaults. | context preparation, template content |
| F-03 | Unknown caller fields are filtered before strict validation. | Undiscoverable template capabilities cannot be supplied, and caller mistakes can disappear silently. | scaffold_artifact context handling |
| F-04 | The active DTO renderer differs from the template described by the public registration. | scaffold_schema and provenance can describe a renderer that is not used. | runtime selection, provenance |
| F-05 | Inheritance and imports are incompletely analyzed. | Tiered behavior, metadata, and version provenance are not fully visible as one resolved contract. | template graph analysis |
| F-06 | Link-valued fields have no canonical representation and some macros emit unresolved references. | Generated Markdown can contain dead or nested links. | cross-template macros, schema semantics |
| F-07 | Some fields are exposed but ignored; other rendered fields are hidden. | Caller intent is silently lost or only available through undocumented knowledge. | individual artifact contracts |
| F-08 | Several templates produce syntactically invalid source from schema-valid rich contexts. | A successful scaffold operation does not imply a usable artifact. | Python artifact templates |
| F-09 | Reference examples contradict live scaffold_schema responses. | Humans and LLMs receive competing instructions; examples encourage invalid calls. | documentation |
| F-10 | Workspace renewal can update templates while preserving their contract configuration separately. | A valid package can become a mixed-version contract/template installation. | distribution and upgrades |
| F-11 | Current metadata dialects and version hashes do not cover the complete resolved graph. | Consumers cannot reliably determine which selected template package and reachable shared contributors produced an artifact. | template-package metadata and provenance |
| F-12 | The four issue-460 PR defects are manifestations of representation ambiguity, not isolated formatting errors. | Local template edits would leave the same failure class elsewhere. | suite-wide content model |
| F-13 | Successful scaffolding can still emit visibly null, blank, concatenated, or machine-specific content. | Callers receive artifacts that require immediate manual repair despite tool success. | cross-cutting acceptance, output profiles, concrete templates |
| F-14 | Some code templates embed project-specific imports and architecture assumptions absent from scaffold_schema. | The advertised generic template suite is not independently reusable in other environments. | template-suite portability |
| F-15 | Absolute host paths are embedded in every generated artifact header. | Output is machine-specific, noisy in review, and can disclose local directory structure. | provenance presentation |
| F-16 | Suite-owned artifact purpose descriptions are dropped by `scaffold_schema`. | Callers see field mechanics but must infer why and when the artifact type is useful. | artifact registry, schema introspection |
| F-17 | Eleven Python- or framework-specific contracts use language-agnostic public IDs. | Callers infer the wrong construct semantics and future language extensions cannot occupy an unambiguous namespace. | public artifact identity, configs, docs, consumers |
| F-18 | Runtime tool schemas enumerate artifact IDs but expose no runtime ID-to-purpose discovery surface. | Agents can see available names but still depend on static docs or guesswork to select the right contract. | MCP discovery, active registry, harness instructions |
| F-19 | Rendered-output validation and public check execution define overlapping executable capabilities and outcomes through separately composed authorities. | Identical checks can drift in command, availability, parsing, or result meaning; scaffold/edit evidence can disagree with explicit check evidence. | output profiles, validation runtime, check configuration and orchestration, safe edit, composition root |
| F-20 | Executable checks, behavioral tests, and fixes use separate Python-oriented extension paths and inconsistent public vocabulary. | New languages or tools require generic server changes; a check can own mutation commands while a generic test tool exposes Pytest semantics. | adapter extension packages, check/test/fix contracts, tools, configuration, state, presentation, composition root |

## Canonical Finding Classification

This matrix classifies the primary nature and issue-460 disposition of every finding. A finding can have a structural root and still be classified as a behavior defect when a supported or schema-valid call already produces observable failure. The Design hypotheses are navigation inputs only; they are not selected mechanisms.

| ID | Classification | Issue-scope disposition | Observable invariant | Compatibility strategy | Non-binding Design hypothesis |
|---|---|---|---|---|---|
| F-01 | Behavior defect | Required by issue 460 | `scaffold_schema` alone describes every renderer-consumed caller shape | Clean break | Suite-owned resolved standard JSON Schema |
| F-02 | Behavior defect | Equivalent defect | Omitted, null, empty, false, zero, defaulted, and populated values remain distinct | Clean break | Omission-preserving validation and explicit default materialization |
| F-03 | Behavior defect | Enabling correction | Original caller content reaches strict validation unchanged; no caller-authored operation value becomes rendered content, and server provenance is composed separately afterward | Clean break | Separate caller-content, operation-control, and server-provenance stages |
| F-04 | Behavior defect | Required by issue 460 | Public contract, selected DTO renderer, provenance, and validation describe the same artifact | Clean break | One declaratively selected DTO renderer |
| F-05 | Structural debt | Enabling correction | One complete inheritance/import/include graph is resolved consistently for schema, rendering, and identity | Clean break | Parser-supported startup graph resolution |
| F-06 | Behavior defect | Required by issue 460 | One documented link input always produces a complete clickable link | Clean break | Presentation-neutral structured link value |
| F-07 | Behavior defect | Required by issue 460 and equivalent defects | Every exposed caller field is consumed; every rendered caller value is declared | Clean break | Startup input-source and consumption coherence checks |
| F-08 | Behavior defect | Equivalent defect | Every accepted context produces profile-valid output or explicit pre-persistence failure/unavailable evidence | Clean break | Declarative output profile with on-use validator capability resolution |
| F-09 | Structural debt | Enabling correction | Active documentation cannot compete with live schema and catalog facts | Not applicable — authority cleanup | Remove duplication; derive exact views only when retained value is proven |
| F-10 | Structural debt | Enabling correction | Renewal selects whole non-conflicting components through adopted/actual/candidate comparison, preserves conflicting actual components, and activates only a fully validated complete suite without overwriting external ownership | Staged migration | One active root, one current component checkpoint, non-authoritative candidate staging, and recoverable complete-tree activation |
| F-11 | Structural debt | Enabling correction | pf/sf identify generation-source contracts, including descriptions and transitive shared support, excluding release/policy files and external validation; separate full operational component equality protects upgrades | Clean break | Two generation identities plus distribution-only operational component fingerprints; no history/lookup/reconstruction promise |
| F-12 | Behavior defect | Required by issue 460 | Issue references and checklist state each have one canonical input representation | Clean break | Positive issue IDs and structured checklist items |
| F-13 | Behavior defect | Equivalent defect | Tool success distinguishes contract, render, validation, persistence, and unavailable evidence | Clean break | Structured result states rather than inferred success |
| F-14 | Behavior defect | Equivalent portability defect | Portable package artifacts contain no hidden consumer-project dependencies | Clean break | Portable package baseline plus workspace-owned specialization |
| F-14A | Structural debt | Enabling correction | Dormant metadata cannot act as duplicate agent/workflow guidance | Clean break | Remove unused pattern/imports and stale commented hints |
| F-14B | Structural debt | Enabling correction | Unreachable placeholders do not imply unsupported test capabilities | Clean break | Remove placeholders; any future fixture capability is explicit and reachable |
| F-15 | Behavior defect | Equivalent portability defect | Generic artifact bodies do not embed their persistence target | Clean break | Report paths through tool/result evidence only |
| F-16 | Structural debt | Enabling correction | Existing suite-owned artifact purpose remains visible through selected-artifact introspection | Preserve existing semantic data | Carry the registered root description through the current introspection response |
| F-17 | Structural debt | Enabling correction | Public identity states language/framework semantics that materially determine the contract | Clean break | Language/technology-qualified IDs; exact names remain Design-owned |
| F-18 | Feature request | Deferred / out of scope | Issue 460 adds no new purpose-aware runtime discovery capability | Deferred decision | Future Research compares a new tool, extension of existing introspection, and documentation-only discovery |
| F-19 | Architecture defect and approved scope expansion | Retained and narrowed by F-20 | Output profiles and public check execution share one side-effect-free check authority and factual result seam while consumer policies remain separate | Clean break, superseded where F-20 changes the public/configuration boundary | Check-role catalog and normalized factual executor inside the wider F-20 adapter suite |
| F-20 | Architecture defect and approved scope expansion | Retained in issue 460 by human decision | Check, test, and fix share generic extension packaging/discovery/process infrastructure but keep separate versioned contracts, results, and side-effect rules | PGMCP 3.0 clean break | Self-contained adapter packages with manifest identity, role declarations, package fingerprints, and official/workspace ownership |

## Core Invariants

1. Every renderer-consumed caller value is discoverable through `scaffold_schema`.
2. Every exposed caller-content field has one declared meaning and an observable rendering effect.
3. Each concrete package has one authored human SemVer in its package-local .version file and no individual suite file or shared contributor has an independent authored version. A package-local change does not alter another package's definition, version, resolved package fingerprint, schema/rendering semantics, or affected-package diagnostics; shared changes affect only transitive consumers. Newly scaffolded artifacts may truthfully carry a different source-suite fingerprint when their fingerprinted suite generation sources differ, while existing artifacts remain unchanged, are never marked stale, and remain valid even when matching historical sources are unavailable.
4. Caller context is the sole source of caller-authored rendered content and is validated unchanged; operation controls never enter content, while server-authored provenance is composed separately afterward.
5. Public client schemas remain finite, self-contained, and reference-free.
6. Optional, omitted, empty, null, and defaulted values remain semantically distinct.
7. Generic package artifacts contain no hidden consumer-project dependencies.
8. Suite-owned content truth does not migrate into artifact-specific pgmcp Python code or prose snapshots.
9. Generated content is portable across machines and does not embed persistence targets by default.
10. Compatibility and migration strategy is explicit per affected boundary.
11. Generic runtime code contains no hardcoded artifact IDs, template field names, workflow/phase names, template paths, output-profile choices, provider mappings, or install policy that belongs to suite or workflow configuration.
12. Every active Research, Design, Planning, and Validation phase-instruction variant has a semantically suitable persisted carrier in the corresponding artifact schema and renderer, without templates duplicating workflow action or authority.
13. First-time-right scaffolding means one valid call produces a truthful, structurally coherent, persistable artifact basis without schema/render repair; it does not promise final phase completeness or replace normal content development through `safe_edit_file`.
14. Template and scaffolding tests are first-class code: each retained test proves durable public behavior or an architectural invariant and itself complies with every applicable Architecture Principle; passing tests do not justify private-boundary coupling, duplicated config truth, hidden dependency construction, global mutable state, or implementation-shaped harnesses.
15. Phase instructions may enforce the correct MCP tool, timing, and evidence scope, but never duplicate a complete invocation or its input parameters; `scaffold_schema` is conditional on the agent not already holding the current artifact schema.
16. Rendered-output validation and quality gates do not maintain parallel capability, provider, command, or result-normalization authorities; workspace is an execution scope, not a qualification of the gates.

17. Renewal treats shared/ and each manifest ID as indivisible components, compares adopted/actual/candidate states without per-file merging, and can change the sole active runtime root only by validating and recoverably activating one complete result tree.
18. An existing workspace without a component checkpoint never treats actual as adopted by assumption: automatic bootstrap requires reliable equality evidence, while unavailable or untrusted evidence preserves actual bytes, leaves candidate non-authoritative, and requires an explicit owner checkpoint decision before renewal selection or activation.
19. PGMCP generic server code contains no language, file-extension, test-framework, fixer-command, or parser dispatch for executable tooling: one resolved adapter catalog provides shared packaging and process infrastructure, while `check`, `test`, and `fix` retain separate versioned contracts and authorization boundaries.

## Approved Strategy and Decision Status

The table below is the canonical strategy and status register. Supporting rationale and option analysis live in [Research Findings](research-findings.md). A row marked pending is not binding input for Design.

| Boundary | Status | Decision |
|---|---|---|
| F-01 / S-01 public context ownership | Approved 2026-08-23 | Template suite owns complete standard JSON Schema contracts; pgmcp validates and exposes one resolved contract generically |
| F-01 / S-02 nested collections | Approved 2026-08-23 | Structured items replace primitive and opaque forms through a clean break; no compatibility bridge |
| F-01 client compatibility | Approved 2026-08-23 | Client-facing schemas remain self-contained and reference-free; internal composition is acyclic and fail-fast |
| F-02 / S-03 optionality and nullability | Approved 2026-08-23 | Optional permits omission, null is explicit, empty typed values remain distinct, and defaults have deterministic behavior |
| F-03 caller context and operation/provenance ownership | Approved 2026-08-24; human-approved correction 2026-09-03 | Validate caller context unchanged against the selected artifact schema. Caller-authored operation controls remain outside rendering and may not supply, transform, or derive artifact content; every caller-authored rendered value, including a symbol, title, subject, or other content name, is an explicit artifact-context field and is rendered as supplied after validation. Server-authored provenance is composed separately only for its declared metadata consumer. The former deterministic envelope-name projection allowance is superseded |
| F-04 / S-08 DTO runtime selection | Approved 2026-08-23 | One declaratively selected richer DTO contract drives schema, rendering, graph identity, and provenance; remove implicit V2 override without a bridge |
| F-05 / S-09 resolved template graph | Approved 2026-08-23 | Server startup resolves one coherent restart-stable suite view through parser-supported Jinja semantics; runtime tools share it, suite mutations require restart, and JSON Schema remains the data-shape authority; concrete APIs and topology remain Design-owned |
| F-06 / S-04 link semantics | Approved 2026-08-23 | Required label and target form one presentation-neutral link object; concrete artifacts choose inline or complete reference-style rendering |
| F-07 / S-07 input ownership and consumption | Approved 2026-08-23; clarified 2026-09-03 | Artifact context contains every caller-authored rendered value and only artifact content; operation controls never tunnel into rendering, downstream tool envelopes never tunnel through bodies, server provenance is a separate declared metadata source, and hidden routing or unconsumed values are removed |
| F-08 / S-14 output validation and strictness | Approved 2026-08-23 | Applicable output evidence is declared per artifact/profile; passed, failed, and unavailable remain distinct; strict persistence requires executed passing evidence; dormant artifacts impose no provider availability requirement. Provider discovery, injection, and call topology remain Design-owned |
| F-19 shared output-validation and check authority | Approved scope expansion 2026-08-25; narrowed and superseded in part by F-20 on 2026-09-04 | Retain one injected, config-first, side-effect-free authority for executable check facts and normalized factual check results, shared by artifact output profiles and explicit check execution. Scaffold and safe-edit consumers validate complete proposed content before mutation without check-run lifecycle or presentation side effects. F-20 supersedes the former promises that `run_quality_gates` remains public, that autofix belongs to quality orchestration, and that behavioral tests sit outside the shared extension architecture. F-19 still owns check facts and check-result semantics; it does not collapse input-schema, startup-graph, behavioral-test, fix, workflow-gate, or persistence policy responsibilities |
| F-20 check/test/fix adapter extension suite | Independent QA GO reported for corrected lightweight native-fix scope/order/stop strategy; Design resumed | Introduce one startup-resolved language-agnostic adapter extension suite. Self-contained packages declare manifest-owned `adapter_id`, one package version, supported `check/v1`, `test/v1`, and/or `fix/v1` contracts, capabilities, and executable entry points. Official packages ship with PGMCP; explicitly trusted workspace packages live under `.pgmcp/adapter_suite/`. Generic infrastructure owns discovery, trust, process transport, scratch space, timeouts, stdout/stderr capture, malformed/crashed/unavailable facts, and package fingerprints; it contains no language, extension, framework, command, or parser branches. Public/configuration vocabulary is a PGMCP 3.0 clean break: `run_checks` with `checks.yaml`, framework-neutral `run_tests` with `tests.yaml`, and `apply_fixes` with `fixes.yaml`; remove `run_quality_gates`, `auto_fix`, and `quality.yaml` without aliases or dual reads, and return actionable migration errors for obsolete config. Check is side-effect-free factual analysis, test returns framework-aware behavioral evidence, and fix adapters execute native mutation on PGMCP-authorized targets, without mandatory verification, proposal/copy staging or rollback; failures may leave changes and recovery is agent-controlled. A package may implement several roles but each role independently satisfies its versioned contract. Run evidence records only invoked adapter ID/version/package fingerprint/contract version and external tool identity/version; no whole-suite fingerprint or scaffold-artifact provenance is added. External/workspace owners retain their own package history, dependencies, and version policy. A new language/tool within these three roles requires adapter/config changes, not generic server code; a genuinely new product role may require a new consumer and contract The [2026-09-05 refinement](#narrow-check-retesting-amendment--2026-09-05) additionally removes auto and PGMCP execution-result reuse, preserves native optimization, and uses native configured/caller args without generic fresh or expansion controls; PGMCP alone resolves branch targets; report caching and all other F-20 boundaries remain unchanged |
| Safe-edit post-edit validation | Approved 2026-08-25; narrow human amendment 2026-09-07, independent QA requested | Every safe edit validates complete proposed content through the shared configured output-profile boundary. Scaffold and safe edit expose validation=enforce/report (default enforce) and return validation_policy. Enforce preserves the original on failed/unavailable required validation; report may persist with structured findings, never bypassing independent safety/operation failures. V3 removes safe-edit mode, strict/interactive labels and verify_only without aliases or replacement dry-run functionality. Exact staging/atomic-write/rollback mechanics remain Design-owned |
| F-09 / S-15 documentation authority | Approved 2026-08-23 | Live schema and catalog own exact facts; handwritten docs explain semantics and discovery, duplicate inventories are removed, and generation remains YAGNI-driven |
| F-10 / S-10 distribution and customization | Human-approved amendment and bootstrap remediation 2026-09-03; unchanged by F-20 | Replace complete-suite-only renewal with component-wise three-way selection. Compare one current adopted checkpoint, the actual active root, and the supplied candidate for each indivisible component: shared/ is one component and every concrete manifest ID is one component. Select candidate content only for upstream-only or converged non-conflicting component changes; retain actual content or absence for local-only and conflicting changes. Component absence is a first-class state, so candidate additions and removals follow the same three-way rules. Build the selected result as a complete off-root suite, validate the entire resolved suite, and activate it only through a recoverable complete-tree replacement; validation or activation failure leaves the prior actual root authoritative. Candidate staging remains non-authoritative and runtime resolves exactly one active root. Persist one current component checkpoint with no history and no per-file versions. For a fresh managed install, install the validated candidate and establish its component states as the checkpoint in the same authoritative operation. For an existing managed workspace without a checkpoint, automatic bootstrap is permitted only when trustworthy persisted full operational component evidence for the previously installed or accepted official suite matches actual in component presence and every complete component fingerprint (never pf/sf), or when actual equals the fully validated candidate under that same complete operational comparison; derive the checkpoint from that proven-equal suite. An owner-supplied trusted complete prior suite may instead be validated and used to derive adopted component states. If none of those bases is reliably available, preserve every actual byte, stage the candidate non-authoritatively, return an actionable `checkpoint_required` outcome, and perform no component selection or activation. Existing external workspaces never infer a checkpoint or activate content automatically; their owner must supply a trusted prior suite or explicitly acknowledge the validated candidate as the upstream comparison basis. Candidate acknowledgement advances only checkpoint state and leaves actual content unchanged. Explicit reconciliation may likewise advance candidate checkpoint components without copying or overwriting locally merged actual content. Bootstrap creates no history, lookup, retention, SemVer, compatibility-matrix, automatic-merge, or provenance-registry obligation. Artifact metadata retains id/pv/pf/sf, but pf/sf now have the generation-only meaning approved in the 2026-09-10 amendment. They are not renewal checkpoints and never authorize overwrite, bootstrap, advancement or full installed-state equality; operational component fingerprints alone supply that comparison. Exact checkpoint encoding, comparison DTOs, staging path, validation transaction, and recoverable activation mechanics remain DI-06 Design-owned. |
| F-11 / S-16 source provenance | Human-approved generation-identity amendment 2026-09-10; independent QA GO reported 2026-09-11 | manifest.yaml owns template_id/purpose, .version owns the one bounded human SemVer, policy.yaml owns output_profile/persistence. pf includes selected generation files and transitive shared support; sf includes all suite generation files. Both exclude whole version/policy files and external validation configuration. Comments/descriptions in generation sources count. Preserve id/pv/pf/sf metadata, package isolation and owner-controlled history; no registry, lookup or retention service. Full operational component equality, not pf/sf, protects upgrades. No five-field-manifest alias or field-level exclusion; see the current amendment for trade-offs and required evidence |
| F-12 / S-05 issue references | Approved 2026-08-23 | Positive integers carry issue identity; renderers own # and other presentation syntax |
| F-12 / S-06 checklist items | Approved 2026-08-23 | Required text and explicit checked state form one structured item; primitive strings and bridges are rejected |
| F-12 original-issue coverage | Covered 2026-08-23 | All four PR defects map to approved suite-wide boundaries; no PR-only strategy remains |
| F-13 success semantics | Approved 2026-08-23 | Objective contract, render, output-profile, and persistence evidence define success; no subjective artifact-quality engine is introduced |
| F-14 / S-12 package portability | Approved 2026-08-23 | Generic package types become portable through a clean break; six confirmed S1mpleTrader patterns are removed from PGMCP and migrated only in that owning workspace after its upgrade |
| F-14A agent hints | Approved 2026-08-23 | Remove the unused pattern, three dead imports, and stale commented workflow guidance; contracts.yaml remains workflow authority |
| Runtime architecture compliance | Approved 2026-08-24 | Audit every affected runtime/setup component against the complete Architecture Principles, with explicit emphasis on Config-First/DRY/OCP hardcoding, fail-fast startup, SRP/DIP/ISP, composition-root ownership, no import-time I/O, CQS, Law of Demeter, presentation separation, and YAGNI; artifact-specific knowledge remains in the packaged suite |
| Legacy parallel scaffolding and validation surfaces | Approved 2026-08-24 | Remove the artifact-specific component-scaffolder stack, duplicate renderer/result/base utilities, source-header metadata parser/config/lifecycle exports, and the public always-pass `validate_template` tool with its dedicated DTOs/tests/instruction references. Retained behavior is owned by one resolved generic scaffold path, fail-fast startup graph validation, and declared output-profile validation; no compatibility shell is justified |
| Workflow/template semantic alignment | Approved 2026-08-25 | Compare every active Research, Design, Planning, and Validation `phase_instructions` variant with its final artifact schema and renderer. The shared schema provides a common core plus semantically named optional sections; each workflow instruction determines which sections its outcome requires. Phase instructions retain substantive actions, authority, workflow-specific completeness, and enforcement of the correct MCP tool, timing, and evidence scope, but never embed full invocations or duplicate tool-input parameters. `scaffold_schema` is required only when the agent does not already hold the current schema. Explicitly reject wording that conflates a valid first scaffold with a final complete artifact or obscures normal `safe_edit_file` refinement |
| Test-suite architecture compliance | Approved 2026-08-24 | Audit every affected test and helper twice: first for durable public behavior/invariant value, then against every applicable Architecture Principle. Retained coverage must use public boundaries, explicit dependencies, isolated state, config-derived facts, proportionate helpers, and production-equivalent typing/quality; valuable intent does not excuse architectural coupling, and clean structure does not justify behaviorless tests |
| Deferred YAML artifact subset | Deferred 2026-08-23 | Remove the two incomplete unreachable bases now; coordination should create the complete package subset as the first post-460 PGMCP issue on its own branch |
| [Portable Python artifact coverage](deferred-work.md) | Deferred 2026-08-24 | Add no new Python artifact types in issue 460; preserve the inventory centrally; the approved Generic plain-class artifact remains bounded and may not absorb those deferred responsibilities |
| F-14B unreachable test patterns | Approved 2026-08-23 | Remove the empty assertions placeholder and unreachable incomplete fixture decorator; future fixture support must be first-class test-artifact behavior |
| F-15 / S-13 output path semantics | Approved 2026-08-23; clarified 2026-09-03 | Persistence target and exact file-name controls remain tool-envelope inputs, the resolved output path remains result evidence, and none of these operation values enters generic artifact content |
| F-16 artifact-purpose introspection | Approved 2026-08-24 | Expose the suite-owned concise artifact description through scaffold_schema; exact carrier is Design-owned and speculative catalog metadata remains out of scope |
| F-17 language/technology-qualified identity | Approved 2026-08-24 | Language/framework semantics belong to artifact identity, not caller context; rename eleven implicit-Python IDs through a clean break without aliases |
| [F-18 purpose-aware runtime artifact discovery](deferred-work.md#purpose-aware-runtime-artifact-discovery) | Deferred 2026-08-24 | Classify as a feature request and add no new runtime capability in issue 460; future Research must compare a new discovery tool, extension of an existing introspection surface, and improved existing/static discovery |
| DTO artifact responsibility | Approved 2026-08-24; naming corrected 2026-09-03 | Retain/adapt one language-qualified immutable Python/Pydantic DTO; preserve valid empty skeletons, require descriptions, and conditionally require at least one JSON-compatible example whenever concrete fields exist. Its rendered class symbol is explicit caller-owned artifact context, while its exact file name is an independent operation control; neither is derived from the other |
| Generic Python class responsibility | Approved 2026-08-24 | Retain/adapt a bounded language-qualified plain-class skeleton with required self-documentation, valid empty classes, optional structured imports, bases, and body-free method signatures; remove hidden routing, forced project behavior, and specialized fallbacks through a clean break. Caller-supplied method bodies are excluded only from Generic and this creates no suite-wide rule for specialized Python artifacts |
| Python/pytest integration-test responsibility | Approved 2026-08-24 | Retain/adapt a language- and framework-qualified integration-test module for observable collaboration across concrete components or boundaries; do not equate integration with E2E, infer project imports, force async/classes/filesystem fixtures, or fabricate passing tests. Exact structured test-case and honest incomplete-test mechanics remain Design-owned |
| Resource artifact responsibility | Approved 2026-08-24 | Remove through a clean break: Python has no general resource code construct, the current artifact duplicates Generic without durable semantics, no real scaffold consumer is evidenced, and its output does not implement the pgmcp `BaseResource` boundary. Existing runtime resource code remains unchanged |
| Python/Pydantic configuration-model responsibility | Approved 2026-08-24 | Retain/adapt a language- and framework-qualified model for declarative external configuration, distinct from DTO and Generic; expose structured described fields, explicit defaults/factories/constraints/imports, strict extra handling, explicit immutability, and optional valid examples without building a complete Pydantic DSL. Exact ID and finite schema remain Design-owned |
| Service artifact responsibility | Approved 2026-08-24 | Remove the over-broad Service artifact, concrete command renderer, legacy scaffolder, and hidden command/query/orchestrator routing through a clean break; service is an architectural agreement rather than one defensible Python structure, and retained portable behavior is covered by Generic. Existing generated production files remain unchanged |
| [Command/query service artifact family](deferred-work.md#commandquery-service-artifact-family) | Deferred 2026-08-24 | Add no replacement service templates in issue 460; a future issue may independently research explicit command and query responsibilities, consumer demand, and whether separate artifact contracts are justified |
| Tool artifact responsibility | Approved 2026-08-24 | Remove through a clean break without a replacement or deferred pgmcp/MCP tool artifact: pgmcp `ICoreTool` is repository-specific, MCP SDK forms are framework-specific, and a framework-neutral Python tool has no structure beyond Generic. Existing production tools remain unchanged |
| TypeScript DTO-class responsibility | Approved 2026-08-24 | Retain/adapt one framework-neutral TypeScript data-carrier class with structured typed properties, explicit optionality and immutability, constructor initialization, and optional explicit interface implementation; remove string mini-language parsing, hidden project architecture, and undeclared inherited values. Exact finite schema and rendering mechanics remain Design-owned |
| Python/pytest unit-test responsibility | Approved 2026-08-24 | Retain/adapt a language- and framework-qualified unit-test module that requires at least one explicit concrete behavior case; make imports, fixtures, markers, sync/async, and test doubles explicit, and never fabricate placeholders, passing assertions, project dependencies, class grouping, or a universal TDD phase. Exact structured case representation remains Design-owned |
| Deployment compatibility | Approved 2026-08-23 | Sole current owner accepts manual migration across two machines and approximately four workspaces; repository evidence cannot prove absence of future external consumers, so the clean break is explicit and documented rather than silently generalized |

## Expected Results

Issue 460 should be considered substantively resolved only when:

1. A fresh human or LLM caller can use scaffold_schema alone to construct every supported context shape.
2. The schema describes the actual resolved runtime renderer, including relevant inherited and imported contributions.
3. Every accepted context passes the complete selected contract, renders successfully, satisfies its applicable output-profile policy, and is persisted only when the approved strictness rules permit it.
4. Optionality, nullability, emptiness, and defaults have one declared meaning.
5. Links, issue references, and checklist items each have one canonical representation.
6. Every caller-authored rendered value is exposed in the selected context schema, every exposed field has an explicit role, and no operation-control value is an implicit render source.
7. The system computes one suite-generation fingerprint (sf) and one resolved generation fingerprint (pf) per concrete package without authored file-level versions; every persisted scaffolded artifact records package/artifact identity, package version, resolved package fingerprint, and source suite fingerprint. When the relevant owner supplies matching historical sources, the source suite fingerprint can verify equality; unavailable history neither invalidates the artifact nor creates a PGMCP discovery or reconstruction obligation. The 2026-09-10 generation-identity amendment narrows both identities; full operational component equality remains separate.
8. pgmcp-server does not become the owner of template-specific content truth.
9. Human documentation cannot contradict the live scaffold_schema field surface.
10. Generic artifact names do not conceal consumer-project imports, lifecycle assumptions, or prerequisites.
11. Generated content is reproducible across host machines and does not embed absolute local paths by default.
12. Compatibility choices are approved per affected boundary before design.
13. Output validity, validator availability, and strict persistence policy remain distinct observable states.
14. Runtime and setup implementation passes an explicit Architecture Principles sweep and contains no template/workflow hardcoding outside its authoritative configuration boundary.
15. A workflow-by-phase alignment record proves that active Research, Design, Planning, and Validation instructions can persist their required outcomes through the corresponding schemas/renderers without duplicated workflow authority.
16. Phase instructions and schema guidance distinguish a valid first scaffold from the completed phase deliverable, so agents can scaffold once and refine normally without repair calls, false completeness assumptions, or avoidable reasoning/token churn.
17. Every retained template/scaffolding test protects durable public behavior or an architectural invariant and itself passes the applicable Architecture Principles; obsolete claims and architecturally coupled test implementations are removed or replaced rather than carried forward.
18. A `safe_edit_file` operation validates the complete proposed result: validation=enforce cannot leave a partially or invalidly modified file when required validation fails or is unavailable; validation=report retains structured findings for a persisted invalid result. Both mutation tools expose the same validation vocabulary and policy mirror. Legacy safe-edit mode/strict/interactive/verify_only inputs are rejected without writes; no replacement proposed-edit dry run is introduced.
19. Phase instructions enforce required tool choice, timing, and evidence scope by name and intent without copying complete MCP invocations or parameters; an agent with the current artifact schema may call `scaffold_artifact` directly, while schema discovery remains available when that knowledge is absent or stale.
20. Artifact output profiles and explicit check runs resolve through one configured check-role authority and one normalized factual check-result model; pre-mutation consumers remain free of run lifecycle, presentation, and fix side effects, while `run_checks` owns requested-scope orchestration and reporting. Compatibility and migration are explicit, and independent/self-hosting evidence prevents the changed check path from being the sole proof of its own correctness.

21. Renewal compares one current adopted checkpoint with actual and candidate states for shared/ and each manifest-ID component, selects whole non-conflicting candidate components while preserving local/conflicting actual components, validates one complete off-root result, and activates it recoverably as the sole runtime root. Explicit reconciliation can advance candidate checkpoint state without overwriting locally merged content; external ownership and all prohibited merge/version/provenance mechanisms remain preserved.
22. A fresh managed install creates its initial checkpoint with the installed candidate; an existing checkpoint-less workspace bootstraps automatically only from trusted equality evidence. Otherwise actual content remains byte-for-byte unchanged, candidate remains non-authoritative, and an actionable `checkpoint_required` outcome requires the owner to supply a trusted prior suite or acknowledge the validated candidate as comparison basis without activating or overwriting it.
23. `run_checks`, `run_tests`, and `apply_fixes` consume one resolved adapter-package catalog and generic process runtime while preserving separate check/test/fix contracts; official Pytest and retained check/fix behavior migrate into adapters, one non-Python fixture proves configuration-only language extension, fix execution requires explicit scope=targets, concrete existing files and ordered fix selection, stops at the first non-success, and native mutations may remain after failure, and per-execution reporting supports explicit agent-controlled checks and Git recovery without a tool rollback guarantee, and obsolete V2 tool/config vocabulary is rejected rather than bridged.

## Deferred Work

Detailed deferred evidence is centralized in [Deferred Work](deferred-work.md).

| Boundary | Issue-460 decision |
|---|---|
| S1mpleTrader-local specialization | Remove consumer-specific behavior from the portable suite; perform no cross-repository implementation |
| Complete YAML artifact subset | Remove the two incomplete unreachable seeds; create the capability only through a future full Research/Design cycle |
| Portable Python artifact coverage | Introduce no new Python artifact types; preserve the non-exhaustive inventory for future Research |
| Command/query service artifact family | Remove the current broad Service artifact and hidden subtype routing; create no replacement until a future issue proves distinct command/query consumers and contracts |
| Purpose-aware runtime artifact discovery | Add no new discovery tool or overloaded introspection mode; preserve the option comparison for a future issue |

The approved Generic Python class responsibility remains bounded to a body-free plain-class skeleton and may not absorb the deferred Python artifact responsibilities. Its artifact-local body exclusion does not constrain the independently researched contracts of specialized Python templates.

## Design-Owned Questions After the F-20 Amendment

Research is frozen except for the authorized 2026-09-05 check-retesting amendment, which pauses Design pending independent QA. Both census remediations and the exact repository-root search remain durable evidence. Existing approved boundaries remain binding except where F-20 explicitly supersedes F-19 vocabulary and extension ownership. The questions below are authorized Design inputs; answering them may refine mechanisms within those boundaries but may not introduce a new product role, compatibility choice, or consumer family:

1. Which standard JSON Schema draft and composition form produce one resolved reference-free public artifact contract, and how do typed caller-content, operation-control, and server-provenance inputs remain collision-free?
2. How are template schema/Jinja dependency edges resolved, ordered, validated, fingerprinted, and compared without authored file-level versions?
3. Which portable compact artifact-metadata form carries package/artifact identity, package version, resolved package fingerprint, and source suite fingerprint?
4. How does DI-06 encode and compare adopted, actual, and candidate template-suite component states and safely bootstrap, reconcile, validate, and activate them?
5. Which package-directed non-artifact DTOs, if any, have a demonstrated consumer for suite identity, and which omit it under YAGNI?
6. How does DI-05 define one resolved adapter-package catalog and generic process runtime while giving `check`, `test`, and `fix` separate versioned inputs, results, policy consumers, and side-effect boundaries?
7. How do `run_checks`, framework-neutral `run_tests`, and `apply_fixes` expose short coherent public contracts, configuration, cached evidence, presentation, verbose output, and actionable unavailability without leaking tool-specific concepts into generic server code?
8. How are the approved explicit files-only scope, caller order and stop-on-first-non-success rules represented in typed requests/results, including partial mutation and unstarted steps, without automatic checks, copies, commits or rollback?
9. How do package discovery, trust, dependencies, one package version, computed package fingerprint, restart loading, and official-versus-workspace ownership work without a whole-suite run fingerprint or PGMCP-owned external history?
10. Which independent/conformance evidence proves Pytest preservation, non-Python extensibility, contract failure behavior, fix safety, and complete removal of old tool/config names?

### Historical Refactor / Research Amendment Hand-over — 2026-09-04

This historical hand-over does not close the new targeted review requested above.

#### Scope

- Reopened Research by explicit human direction after Design exposed the wider execution boundary.
- Added F-20: one language-agnostic adapter extension suite with separate `check`, `test`, and `fix` role contracts.
- Recorded the PGMCP 3.0 clean break from `run_quality_gates`/`auto_fix`/`quality.yaml` to `run_checks`/`run_tests`/`apply_fixes` and `checks.yaml`/`tests.yaml`/`fixes.yaml`.
- Preserved consumer-specific policies: output-profile validation, explicit check execution, behavioral testing, controlled fix application, workflow evidence consumption, and scaffold/safe-edit persistence remain distinct.
- Included adapter package ownership, trust, version, fingerprint, invoked-run provenance, restart loading, external ownership, explicitly authorized native fixes, and independent/self-hosting evidence.
- Preserved all unrelated template-suite, artifact provenance, renewal, and deferred-work decisions.
- Excluded production/test implementation and did not modify the in-progress Design package documents.

#### Deliverables

- [Primary Research](research.md)
- [Detailed Research Findings](research-findings.md)
- [Design Intake Map](design-intake-map.md)
- [Template Suite Work Catalog](template-suite-catalog.md)
- [Deferred Work](deferred-work.md)
- [Research-to-Design QA Audit History](research-to-design-qa-audit.md)
- [Historical Validation/Quality Brainstorm](validation-quality-gates-brainstorm-handover.md)

#### Evidence

- Current `run_tests` input and execution are Pytest-specific despite the generic name.
- Current fixes are secondary quality-gate commands executed directly against authoritative workspace files.
- Current check, test, and fix paths have separate composition, configuration, parsing, result, state, and presentation authorities.
- The catalog now contains 126 active consumers/references plus two explicitly excluded governing-standard sources and 151 test/helper paths.
- The QA-directed repeat sweep now starts at repository root, includes hidden source paths, preserves normal ignore rules, excludes only Git internals, archived prompts, and issue-local work products, and compares exact paths.
- The unchanged old-name and semantic-consumer term sets return 71 and 82 paths respectively, 115 unique; every result has an explicit catalog row and the three latest additions have DI-05 or DI-07 ownership.
- Prior issue-402 auto-fix Research is retained as valid historical context for its narrower architecture, not as authority for PGMCP 3.0.
- Architecture Principles require configuration-owned language/tool facts, generic-code OCP, injected composition, explicit mutation authority, and one source of executable truth.
- No changed executable path is used as the sole substantive evidence for this Research amendment.

#### Open Work

- The human reported independent QA GO for the generation-identity/file-ownership amendment and authorized Design resumption. Remaining Design/conformance work is not pre-approved.
- DI-05 must receive its own Design document and remain separate from DI-04 scaffold/safe-edit mutation ownership.
- Exact role schemas, adapter manifest fields, discovery/index layout, process protocol, authorized native fix execution, typed partial-mutation outcomes, external recovery guidance, DTO shapes, and status mapping remain Design-owned within the approved boundaries.
- Implementation sequencing remains Planning-owned under the binding manageability conditions above, including separate check/test/fix proof, separate F-10 activation and F-20 fix-application cycles, and concrete cycle ownership for all 126 consumers and 151 tests/helpers.

#### Review Request

- Targeted independent QA GO reported by the human on 2026-09-11 for synchronized F-10, DI-06 and catalog instructions.
- Specifically review policy-only/version-only local changes versus changed candidate, bootstrap rejection of pf/sf or ambiguous hashes, complete operational recovery maps, and the documented source-normalization boundary.
- Earlier independent Research review returned GO for native-fix scope/order/stop only; it is not approval of the current fingerprint amendment.
- Design resumption authorized by the human; retain independent review at the Design gate.
- Independent Design review remains required at the Design phase gate; this close-out does not pre-approve Design mechanisms or later implementation cycles.

## References

- [Pre-Implementation Documentation Contract](README.md)
- [Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md)
- [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [Scaffolding Tool Reference](../../reference/tools/scaffolding.md)
- [Template Metadata Format](../../reference/template_metadata_format.md)
- [Template Library Usage](../../reference/TEMPLATE_LIBRARY_USAGE.md)
- [Scaffolding Subsystem](../../manuals/architectural_diagrams/09_scaffolding_subsystem.md)
- [Configuration Loading Architecture](../../reference/config-loading-architecture.md)
- [Schema–Template Maintenance](../schema-template-maintenance.md)
- [Release Assets Procedure](../../reference/release-assets-procedure.md)

## Version History

| Version | Date | Changes |
|---|---|---|
| 3.40 | 2026-09-11 | Record human-reported independent generation-identity QA GO and Design resumption; preserve remaining workshop decisions. |
| 3.39 | 2026-09-11 | Clarify the three identity consumers and full operational upgrade/bootstrap authority; synchronize QA-requested active F-10 and request independent re-review. |
| 3.38 | 2026-09-10 | Record human-approved whole-file generation fingerprint boundaries and manifest/.version/policy ownership; retain full upgrade comparison and request targeted QA. |
| 3.37 | 2026-09-10 | Correct catalog P3 and record human-supplied native-fix Research QA GO; resume Design without pre-approving W05 DTOs. |
| 3.36 | 2026-09-10 | Resolve QA scope/stop blockers through human-approved files-only and stop-first policy; remove fix-transaction and stale gate handovers. |
| 3.35 | 2026-09-10 | Record lightweight native-fix amendment; withdraw proposal/verification/rollback promises; preserve agent-controlled recovery and request independent review. |
| 3.34 | 2026-09-10 | Correct QA P2 authority routing; record human-supplied independent QA GO and Design resumption without changing approved behavior. |
| 3.33 | 2026-09-10 | Correct public workspace intent: scope=workspace replaces dot target shorthand; configured remains native discovery; adapter transport unchanged. |
| 3.32 | 2026-09-10 | Record bounded native-selection correction: PGMCP owns Git resolution; operation/targets/args adapter requests; no generic fresh/expansion controls; targeted review requested. |
| 3.30 | 2026-09-07 | Correct the stale current-gate reference after QA: the narrow safe-edit amendment owns the pending review; prior approved decisions remain binding |
| 3.31 | 2026-09-07 | Record human-reported independent QA GO on the corrected narrow safe-edit amendment and authorized Design resumption; no strategy change |
| 3.28 | 2026-09-05 | Apply explicitly authorized project-to-workspace V3 scope rename without alias or coverage change; distinguish native project concepts and ordinary language-specific profiles; record Design continuation |
| 3.29 | 2026-09-07 | Amend only safe-edit policy strategy/E-18 after human scope expansion: unify validation=enforce/report, retire mode and verify_only without bridge/replacement, supersede deferral and request targeted independent QA |
| 3.27 | 2026-09-05 | Record human-approved required run_checks scope and pre-execution validation error on omission; remove deferred default decision in response to QA; request recheck |
| 3.26 | 2026-09-05 | Amend F-20 only: remove auto and PGMCP execution-result reuse, retain native configuration and fresh intent, route directly affected consumers, and request independent QA before resuming Design |
| 3.25 | 2026-09-04 | Record formal human Design authorization, freeze Research content, require a dedicated DI-05 Design document, and bind Design/Planning to independently provable migration, cutover, rollback, and complete 126/151 cycle-ownership conditions |
| 3.24 | 2026-09-04 | Record the workspace-root QA NOGO on `d92a2ca4`, replace the enumerated-root search with a hidden-aware exact-path repository-root search, add three direct consumers, correct the inventory to 126 consumers plus two governing sources and 151 tests/helpers, and request short targeted re-review without claiming Design authorization |
| 3.23 | 2026-09-04 | Record the independent F-20 QA census NOGO, repeat the sweep with old names and semantic consumer terms, correct the inventory to 123 consumers plus two governing sources and 151 tests/helpers, and request targeted independent re-review without claiming Design authorization |
| 3.22 | 2026-09-04 | Reopen Research by human direction and add F-20: one language-agnostic adapter extension suite with separate check/test/fix contracts, PGMCP 3.0 clean-break tool/config vocabulary, bounded fix application, package/run provenance boundaries, complete consumer/test census expansion, and independent QA as the active gate |
| 3.21 | 2026-09-03 | Apply the human-approved F-03/F-07 correction: supersede envelope-name projection, make artifact context the sole caller-authored render source, keep operation controls out of content, and preserve separately composed server provenance without claiming a new QA verdict |
| 3.20 | 2026-09-03 | Close Research after the human owner explicitly authorized Design continuation on the remediated F-10/S-10 boundary; retain the QA NOGO as history and claim no independent re-review outcome |
| 3.19 | 2026-09-03 | Address the targeted QA bootstrap blocker through human-approved rules for fresh installs, reliable equality-based managed bootstrap, owner-supplied or candidate-acknowledged baselines, safe `checkpoint_required` refusal, and external-owner control; request independent re-review |
| 3.18 | 2026-09-03 | Reopen only F-10/S-10 and replace complete-suite-only renewal with human-directed component-wise adopted/actual/candidate selection, one current component checkpoint, full-suite validation, recoverable one-root activation, and fresh independent QA review |
| 3.17 | 2026-08-30 | Close Research after the user reported targeted independent QA approval of the third ownership correction; record unconditional Design GO without changing the approved boundary |
| 3.16 | 2026-08-30 | Address the independent QA ownership finding: retain two fingerprints and compact artifact provenance while removing any PGMCP promise or Design obligation for external historical retention, association validation, lookup, archival, reconstruction, or missing-history controls; request targeted confirmation |
| 3.15 | 2026-08-30 | Reopen Research for the human-approved second F-10/F-11 amendment: two automatic identities, compact artifact source-suite provenance, semantic package isolation, immutable Git/release snapshot authority, no authored file versions or replacement registry, and fresh independent review |
| 3.14 | 2026-08-29 | Close the bounded F-10/F-11 amendment after fresh independent QA GO and require the superseded global-provenance Design passages to be reconciled first |
| 3.13 | 2026-08-29 | Reopen Research and record the human-approved F-10/F-11 amendment that separates complete-suite management identity from isolated selected-template-package provenance; request fresh independent review |
| 3.12 | 2026-08-27 | Link the issue-local pre-implementation documentation contract as the form and navigation authority |
| 3.11 | 2026-08-27 | Close the Research gate after unconditional independent QA GO and supersede all earlier transition reservations |
| 3.10 | 2026-08-26 | Complete the formal Research hand-over, repair the canonical strategy table, assign conditional catalog decisions, and align the approved deferred-work lifecycle for independent re-review |
| 3.9 | 2026-08-26 | Add the authoritative Design Intake Map with exactly one primary destination for every finding, strategy, invariant, expected result, consumer family, and conditional catalog disposition |
| 3.8 | 2026-08-25 | Govern the human-approved validation and quality-gate scope expansion as standalone F-19, including compatibility, migration, consumer-policy separation, and independent/self-hosting evidence obligations |
| 3.7 | 2026-08-25 | Unify rendered-output validation and quality gates under one configured executable-capability authority while preserving their distinct policies, side effects, and non-overlapping validation responsibilities; extend the affected-consumer census accordingly |
| 3.6 | 2026-08-25 | Define optional workflow-selected artifact sections and preserve named tool enforcement while removing full invocation/parameter duplication from phase instructions |
| 3.5 | 2026-08-25 | Make post-edit output-profile validation and strict no-write behavior an explicit safe-edit strategy and expected result |
| 3.4 | 2026-08-24 | Complete the 94-consumer/105-test audit, add the legacy parallel-stack clean break, reconcile deferred ownership, and request independent QA |
| 3.3 | 2026-08-24 | Separate first-time-right scaffold validity from final artifact completeness and require the contracts alignment audit to protect normal safe-edit refinement and LLM efficiency |
| 3.2 | 2026-08-24 | Make the complete Architecture Principles/hardcoding sweep and workflow-phase/template alignment record explicit Research completion obligations |
| 3.1 | 2026-08-24 | Close artifact-specific config and concrete-renderer audit in two controlled batches; all 79 suite files now have explicit dispositions |
| 3.0 | 2026-08-24 | Clarify envelope/content naming ownership: deterministic representation derivation is valid, semantic inference or non-trivial composition requires an explicit artifact field |
| 2.9 | 2026-08-24 | Approve an explicit behavior-oriented Python/pytest unit-test responsibility and close all 22 public artifact dispositions |
| 2.8 | 2026-08-24 | Approve a structured framework-neutral TypeScript DTO-class responsibility and reject the current string mini-language and hidden project metadata |
| 2.7 | 2026-08-24 | Approve clean-break removal of Tool without a pgmcp/MCP replacement or deferred tool capability |
| 2.6 | 2026-08-24 | Approve clean-break removal of broad Service scaffolding and defer any explicit command/query artifact family to separate Research |
| 2.5 | 2026-08-24 | Approve the bounded Python/Pydantic configuration-model responsibility and reduce the remaining dispositions |
| 2.4 | 2026-08-24 | Approve clean-break removal of the semantically redundant Resource artifact and reduce the remaining dispositions |
| 2.3 | 2026-08-24 | Approve the portable Python/pytest integration-test responsibility and reduce the remaining public and suite-file dispositions |
| 2.2 | 2026-08-24 | Add the canonical F-01–F-18 classification matrix and defer F-18 purpose-aware runtime discovery as an explicitly approved feature request outside issue 460 |
| 2.1 | 2026-08-24 | Record explicit approval of the bounded Generic Python plain-class responsibility and clarify that its body-free contract creates no suite-wide rule for specialized Python artifacts |
| 2.0 | 2026-08-24 | Reconcile Research into one decision authority with separate findings, catalog, probe, and deferred-work responsibilities; restore Generic to pending human approval |
| 1.40 | 2026-08-24 | Last pre-reconciliation research state |
| 1.18 | 2026-08-23 | Reopen Research after independent QA found incomplete evidence, preserved behavior, blast radius, and phase separation |
| 1.0 | 2026-08-22 | Initial standalone schema-first semantic audit |
