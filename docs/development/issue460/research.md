# Research: Issue 460 — Scaffolding Schema–Template Rendering Contract Audit

**Status:** REOPENED — F-20 SCOPE AMENDMENT AWAITS INDEPENDENT QA  
**Version:** 3.22  
**Last Updated:** 2026-09-04  
**Issue:** 460  
**Workflow:** Refactor / Research

## Purpose

Establish the observable content, compatibility, ownership, and portability boundaries required for first-time-right scaffolding by humans and LLM callers.

The public caller contract is the output of `scaffold_schema`. Template configuration, Jinja sources, loader and packaging code, tests, and reference documentation are evidence about that contract, not alternative caller authorities.

This document is the sole authority for issue-460 decision status, Approved Strategy, expected results, open work, and the Research gate. Detailed evidence is retained in [Research Findings](research-findings.md). The [Design Intake Map](design-intake-map.md) is the subordinate authority for complete primary Design coverage; it cannot change Research decisions. The [Pre-Implementation Documentation Contract](README.md) governs the form, topology, and navigation of the Research and Design set without changing this document's content authority.

## Current Status and Gate

Research was explicitly reopened by the human owner on 2026-09-04 after Design investigation showed that the approved F-19 boundary was too narrow. Sharing executable check facts between rendered-output validation and quality-gate orchestration while leaving behavioral tests in a Pytest-specific subsystem and fixes as secondary quality-gate commands would create three incompatible extension models and preserve language knowledge in generic server code.

F-20 records the human-approved scope expansion. PGMCP 3.0 will expose one language-agnostic adapter extension suite with separate versioned `check`, `test`, and `fix` contracts. Adapter packages may implement one or more roles, but shared discovery, trust, process transport, package versioning, and package fingerprinting do not collapse their distinct semantics or side-effect boundaries. The clean break renames the executable public/configuration vocabulary to `run_checks`, `run_tests`, and `apply_fixes`, backed by `checks.yaml`, `tests.yaml`, and `fixes.yaml`; no V2 alias or dual-read bridge is retained. A quality gate remains a workflow/policy consumer of evidence, not an executable adapter role.

This amendment supersedes only F-19 wording that preserved `run_quality_gates`, treated autofix as quality orchestration, or excluded behavioral tests from the shared extension boundary. It does not collapse tests into checks, authorize checks to mutate, move persistence policy into adapters, alter template-package/source-suite provenance, or require PGMCP to retain external adapter history or binaries.

- All 22 public artifact types and all 79 packaged template-suite files retain their existing dispositions.
- The affected runtime/setup/agent/documentation census expands from 102 to 117 rows.
- The affected test/helper census expands from 105 to 143 rows.
- The Design Intake Map now assigns all 22 finding IDs, 44 strategy rows, 19 invariants, and 23 expected results.
- Design is paused. The amendment requires an independent `@qa design-reviewer` verdict before Research may close or Design may resume.
- Earlier QA outcomes remain point-in-time evidence only for the scopes they reviewed and do not authorize this F-20 amendment.

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
| F-11 | Structural debt | Enabling correction | Package semantic provenance covers its complete local caller/rendering contract and every transitively reachable shared contributor; persisted artifact provenance records the source-suite identity without redefining package semantics or promising source retention, lookup, or reconstruction | Clean break | Automatically derived resolved-package and complete-suite fingerprints with owner-conditional historical verification |
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
3. Each concrete package has one authored human SemVer in its manifest and no individual suite file or shared contributor has an independent authored version. A package-local change does not alter another package's definition, version, resolved package fingerprint, schema/rendering semantics, or affected-package diagnostics; shared changes affect only transitive consumers. Newly scaffolded artifacts may truthfully carry a different source-suite fingerprint when their complete source snapshot differs, while existing artifacts remain unchanged, are never marked stale, and remain valid even when matching historical sources are unavailable.
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
| F-20 check/test/fix adapter extension suite | Human-approved scope expansion 2026-09-04; independent QA pending | Introduce one startup-resolved language-agnostic adapter extension suite. Self-contained packages declare manifest-owned `adapter_id`, one package version, supported `check/v1`, `test/v1`, and/or `fix/v1` contracts, capabilities, and executable entry points. Official packages ship with PGMCP; explicitly trusted workspace packages live under `.pgmcp/adapter_suite/`. Generic infrastructure owns discovery, trust, process transport, scratch space, timeouts, stdout/stderr capture, malformed/crashed/unavailable facts, and package fingerprints; it contains no language, extension, framework, command, or parser branches. Public/configuration vocabulary is a PGMCP 3.0 clean break: `run_checks` with `checks.yaml`, framework-neutral `run_tests` with `tests.yaml`, and `apply_fixes` with `fixes.yaml`; remove `run_quality_gates`, `auto_fix`, and `quality.yaml` without aliases or dual reads, and return actionable migration errors for obsolete config. Check is side-effect-free factual analysis, test returns framework-aware behavioral evidence, and fix returns a bounded proposed changeset that PGMCP stale-checks, authorizes, validates, and applies. A package may implement several roles but each role independently satisfies its versioned contract. Run evidence records only invoked adapter ID/version/package fingerprint/contract version and external tool identity/version; no whole-suite fingerprint or scaffold-artifact provenance is added. External/workspace owners retain their own package history, dependencies, and version policy. A new language/tool within these three roles requires adapter/config changes, not generic server code; a genuinely new product role may require a new consumer and contract |
| Safe-edit post-edit validation | Approved 2026-08-25 | Every `safe_edit_file` operation validates the complete resulting artifact content through the same injected, configured output-profile boundary used by scaffolding. In strict mode, failed or unavailable required validation leaves the original file unchanged; interactive mode may persist but returns structured findings. Exact staging, atomic-write, or rollback mechanics remain Design-owned |
| F-09 / S-15 documentation authority | Approved 2026-08-23 | Live schema and catalog own exact facts; handwritten docs explain semantics and discovery, duplicate inventories are removed, and generation remains YAGNI-driven |
| F-10 / S-10 distribution and customization | Human-approved amendment and bootstrap remediation 2026-09-03; unchanged by F-20 | Replace complete-suite-only renewal with component-wise three-way selection. Compare one current adopted checkpoint, the actual active root, and the supplied candidate for each indivisible component: shared/ is one component and every concrete manifest ID is one component. Select candidate content only for upstream-only or converged non-conflicting component changes; retain actual content or absence for local-only and conflicting changes. Component absence is a first-class state, so candidate additions and removals follow the same three-way rules. Build the selected result as a complete off-root suite, validate the entire resolved suite, and activate it only through a recoverable complete-tree replacement; validation or activation failure leaves the prior actual root authoritative. Candidate staging remains non-authoritative and runtime resolves exactly one active root. Persist one current component checkpoint with no history and no per-file versions. For a fresh managed install, install the validated candidate and establish its component states as the checkpoint in the same authoritative operation. For an existing managed workspace without a checkpoint, automatic bootstrap is permitted only when a trustworthy persisted fingerprint of the previously installed or accepted official suite exactly matches the computed actual suite, or when actual exactly equals the fully validated candidate; derive the checkpoint from that proven-equal suite. An owner-supplied trusted complete prior suite may instead be validated and used to derive adopted component states. If none of those bases is reliably available, preserve every actual byte, stage the candidate non-authoritatively, return an actionable `checkpoint_required` outcome, and perform no component selection or activation. Existing external workspaces never infer a checkpoint or activate content automatically; their owner must supply a trusted prior suite or explicitly acknowledge the validated candidate as the upstream comparison basis. Candidate acknowledgement advances only checkpoint state and leaves actual content unchanged. Explicit reconciliation may likewise advance candidate checkpoint components without copying or overwriting locally merged actual content. Bootstrap creates no history, lookup, retention, SemVer, compatibility-matrix, automatic-merge, or provenance-registry obligation. Artifact metadata and the existing resolved-package and source-suite fingerprints remain unchanged and are not repurposed as the renewal checkpoint. Exact checkpoint encoding, comparison DTOs, staging path, validation transaction, and recoverable activation mechanics remain DI-06 Design-owned. |
| F-11 / S-16 source provenance | Approved 2026-08-23; human-approved amendments 2026-08-29 and 2026-08-30; ownership corrected 2026-08-30 | Each concrete template package owns one human-readable schema-valid SemVer in its manifest; individual package files and shared templates, patterns, and definitions have no authored versions unless a future independently distributed boundary demonstrates a consumer. Two identities are computed automatically: a resolved package fingerprint over package-local semantic inputs plus exactly its transitively reachable shared contributors, and the F-10 complete-suite fingerprint over the currently supplied managed suite snapshot. Every persisted scaffolded artifact carries compact source provenance comprising template-package/artifact identity, package version, resolved package fingerprint, and source suite fingerprint. The source suite fingerprint is equality evidence when matching sources are available, never package semantic identity or a lookup promise. A package-local change does not alter any other package's definition, version, resolved package fingerprint, schema/rendering semantics, or affected-package diagnostics; it may change only the source-suite fingerprint in newly scaffolded artifacts because their complete source snapshot differs. Existing artifacts remain valid and independent even when matching historical sources are unavailable; they are never mutated or marked stale, and exact reconstruction is conditional on the relevant owner retaining matching sources. Shared changes affect only transitive package consumers. Concrete packages cannot depend on one another; packages may depend on shared support, shared support may depend on shared support, and shared support cannot depend on a concrete package. Remove template_registry.json without a replacement provenance registry or per-artifact contributor/version ledger. PGMCP validates and loads the currently supplied suite contract, computes both deterministic identities, persists the four approved provenance facts, and compares snapshots already available at the managed upgrade boundary; it does not police historical SemVer-bump correctness for external suites or introduce history inspection, retention, lookup, archival, association validation, reconstruction, or absent-history failure/evidence code. Package-directed non-artifact tool-output exposure of suite identity remains Design-owned and YAGNI-bound rather than automatic. Exact digest, canonical encoding, metadata syntax/size, reverse-dependency mechanism, available-snapshot comparison policy, version-only-bump policy, and SemVer severity remain Design-owned without implying external-history enforcement |
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
7. The system computes one complete source-suite fingerprint and one resolved fingerprint per concrete package without authored file-level versions; every persisted scaffolded artifact records package/artifact identity, package version, resolved package fingerprint, and source suite fingerprint. When the relevant owner supplies matching historical sources, the source suite fingerprint can verify equality; unavailable history neither invalidates the artifact nor creates a PGMCP discovery or reconstruction obligation. The 2026-09-03 F-10/S-10 amendment does not change this metadata or either fingerprint's meaning.
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
18. A `safe_edit_file` operation validates the complete proposed result: strict mode cannot leave a partially or invalidly modified file when required validation fails or is unavailable, while interactive mode returns structured findings for any persisted invalid result.
19. Phase instructions enforce required tool choice, timing, and evidence scope by name and intent without copying complete MCP invocations or parameters; an agent with the current artifact schema may call `scaffold_artifact` directly, while schema discovery remains available when that knowledge is absent or stale.
20. Artifact output profiles and explicit check runs resolve through one configured check-role authority and one normalized factual check-result model; pre-mutation consumers remain free of run lifecycle, presentation, and fix side effects, while `run_checks` owns requested-scope orchestration and reporting. Compatibility and migration are explicit, and independent/self-hosting evidence prevents the changed check path from being the sole proof of its own correctness.

21. Renewal compares one current adopted checkpoint with actual and candidate states for shared/ and each manifest-ID component, selects whole non-conflicting candidate components while preserving local/conflicting actual components, validates one complete off-root result, and activates it recoverably as the sole runtime root. Explicit reconciliation can advance candidate checkpoint state without overwriting locally merged content; external ownership and all prohibited merge/version/provenance mechanisms remain preserved.
22. A fresh managed install creates its initial checkpoint with the installed candidate; an existing checkpoint-less workspace bootstraps automatically only from trusted equality evidence. Otherwise actual content remains byte-for-byte unchanged, candidate remains non-authoritative, and an actionable `checkpoint_required` outcome requires the owner to supply a trusted prior suite or acknowledge the validated candidate as comparison basis without activating or overwriting it.
23. `run_checks`, `run_tests`, and `apply_fixes` consume one resolved adapter-package catalog and generic process runtime while preserving separate check/test/fix contracts; official Pytest and retained check/fix behavior migrate into adapters, one non-Python fixture proves configuration-only language extension, fix application remains PGMCP-authorized and recoverable, and obsolete V2 tool/config vocabulary is rejected rather than bridged.

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

Research is open only for independent review of the 2026-09-04 F-20 scope amendment. Existing approved boundaries remain binding except where F-20 explicitly supersedes F-19 vocabulary and extension ownership. Design is paused; the questions below are navigation inputs for later continuation, not authorization to resume it:

1. Which standard JSON Schema draft and composition form produce one resolved reference-free public artifact contract, and how do typed caller-content, operation-control, and server-provenance inputs remain collision-free?
2. How are template schema/Jinja dependency edges resolved, ordered, validated, fingerprinted, and compared without authored file-level versions?
3. Which portable compact artifact-metadata form carries package/artifact identity, package version, resolved package fingerprint, and source suite fingerprint?
4. How does DI-06 encode and compare adopted, actual, and candidate template-suite component states and safely bootstrap, reconcile, validate, and activate them?
5. Which package-directed non-artifact DTOs, if any, have a demonstrated consumer for suite identity, and which omit it under YAGNI?
6. How does DI-05 define one resolved adapter-package catalog and generic process runtime while giving `check`, `test`, and `fix` separate versioned inputs, results, policy consumers, and side-effect boundaries?
7. How do `run_checks`, framework-neutral `run_tests`, and `apply_fixes` expose short coherent public contracts, configuration, cached evidence, presentation, verbose output, and actionable unavailability without leaking tool-specific concepts into generic server code?
8. How are fix proposals bounded, stale-checked, path-authorized, validated, and recoverably applied without granting an adapter direct authority over workspace mutation?
9. How do package discovery, trust, dependencies, one package version, computed package fingerprint, restart loading, and official-versus-workspace ownership work without a whole-suite run fingerprint or PGMCP-owned external history?
10. Which independent/conformance evidence proves Pytest preservation, non-Python extensibility, contract failure behavior, fix safety, and complete removal of old tool/config names?

### Refactor / Research Amendment Hand-over

#### Scope

- Reopened Research by explicit human direction after Design exposed the wider execution boundary.
- Added F-20: one language-agnostic adapter extension suite with separate `check`, `test`, and `fix` role contracts.
- Recorded the PGMCP 3.0 clean break from `run_quality_gates`/`auto_fix`/`quality.yaml` to `run_checks`/`run_tests`/`apply_fixes` and `checks.yaml`/`tests.yaml`/`fixes.yaml`.
- Preserved consumer-specific policies: output-profile validation, explicit check execution, behavioral testing, controlled fix application, workflow evidence consumption, and scaffold/safe-edit persistence remain distinct.
- Included adapter package ownership, trust, version, fingerprint, invoked-run provenance, restart loading, external ownership, bounded fix proposals, and independent/self-hosting evidence.
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
- The catalog now includes the directly affected runtime/documentation consumers and test/helper files omitted from the earlier F-19-only census.
- Prior issue-402 auto-fix Research is retained as valid historical context for its narrower architecture, not as authority for PGMCP 3.0.
- Architecture Principles require configuration-owned language/tool facts, generic-code OCP, injected composition, explicit mutation authority, and one source of executable truth.
- No changed executable path is used as the sole substantive evidence for this Research amendment.

#### Open Work

- Independent QA has not yet reviewed F-20. Design must not resume until that authority returns its evidence-backed verdict.
- If QA identifies a contradiction or missing migration boundary, Research remains active and the amendment is corrected here.
- After QA GO, Design must reconcile the existing F-19/DI-05 material and obtain explicit human agreement on whether DI-05 receives a dedicated document or remains navigable in the current owner; superseded quality-gate/autofix vocabulary may not return.
- Exact role schemas, adapter manifest fields, discovery/index layout, process protocol, fix transaction, DTO shapes, status mapping, and implementation sequence remain Design-owned.

#### Review Request

- Review requested.
- Invoke an independent interactive `@qa design-reviewer` to assess the F-20 amendment, its clean-break strategy, blast-radius completeness, catalog dispositions, Design routing, and self-hosting evidence.
- No Research PASS, GO, close-out, or Design authorization is claimed by this producer hand-over.

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
