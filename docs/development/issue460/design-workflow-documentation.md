<!-- docs\development\issue460\design-workflow-documentation.md -->
<!-- template=design version=5827e841 created=2026-09-12T07:43Z updated= -->
# Issue 460 Workflow and Documentation Alignment Design

**Status:** DESIGN INTEGRATED — INDEPENDENT CLOSURE RECHECK REQUIRED  
**Version:** 1.1  
**Last Updated:** 2026-09-12  
**Primary Package:** DI-07  
**Upstream Dependencies:** Frozen Research F-09/F-20; DI-01/02 exposure; DI-03 document contracts; DI-04/05 operations; DI-06 delivery  
**Downstream Consumers:** Phase instructions, host instruction sources/copies, active references, DI-08 assurance  
**Lifecycle Status:** Integrated; dependency/removal/evidence reconciliation in [Integration §4](design-integration-review.md#4-semantic-integration-closure); independent closure recheck required

## 1. Purpose and Authority

Own the workflow, instruction and documentation alignment needed to use the approved V3
contracts correctly. The human approved W11 on 2026-09-12. This is Design, not an edit
to current runtime instructions, an implementation plan or independent QA approval.

## 2. Scope and Exclusions

Cover all nineteen active Research/Design/Planning/Validation variants, their DI-03
document carriers, host instruction sources and mapped consumers, and catalogued active
manual/reference removals. Preserve workflow-specific outcomes and authority.

Do not redesign DI-03 fields or rendering, invent workflow phases, add a runtime
completeness checker, require health_check before normal calls, promise sandboxing,
or rewrite historical issue archives. No new runtime tool or tutorial generator.

## 3. Binding Inputs

- [Research](research.md), [F-09/F-20 findings](research-findings.md) and
  [DI-07 intake](design-intake-map.md): instruction authority and semantic alignment.
- [Consumer catalog](template-suite-catalog.md): exact path inventory and conditional
  phase-workflows/validation_api dispositions; the 126/151 census remains unchanged.
- [Document/tracking contracts §7.8](design-document-tracking-artifacts.md):
  nineteen exact carrier mappings; bounded independent QA GO is an input, not DI-07 approval.
- [Mutation design](design-mutation-validation.md), [adapter contracts](design-execution-adapters.md)
  and [distribution §§7.6–7.7](design-distribution.md): approved user-facing behavior.
- [Instruction authority](../../reference/copilot-agent-instructions-model.md) and
  [release assets procedure](../../reference/release-assets-procedure.md): source-first
  host synchronization, existing lifecycle exceptions and generated release assets.
- [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md),
  [Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md) and
  [issue documentation contract](README.md).

## 4. Owned Decisions

| ID | Decision | Status |
|---|---|---|
| D-WORKFLOW-01 | Phase contracts own required work/evidence; exposed schemas own exact inputs; templates carry content without duplicating workflow authority | Human-approved |
| D-WORKFLOW-02 | Edit docs/agents host sources first and synchronize their actual mapped consumers; retain intentional host differences | Human-approved; existing instruction-model authority |
| D-WORKFLOW-03 | Remove complete invocation inventories from phase/always-on instructions; require schema discovery only when needed and keep role/scope/authorization explicit | Human-approved |
| D-WORKFLOW-04 | Preserve nineteen distinct workflow meanings through DI-03 carriers without changing their schema or treating scaffolding as phase completion | Human-approved |
| D-WORKFLOW-05 | Reduce phase-workflows and MCP_TOOLS to navigation; consolidate and remove obsolete validation_api; remove frozen template/pattern inventories and rewrite durable usage guidance | Human-approved |
| D-WORKFLOW-06 | Preserve independent workflow, semantic, source-copy and link evidence; retire obsolete literal-syntax assertions, not valuable loader/behavior tests | Human-approved; implementation evidence pending |

## 5. Responsibilities and Boundaries

| Authority | Owns | Must not duplicate |
|---|---|---|
| contracts.yaml | Phase purpose, required outcomes, stop conditions, evidence timing/scope and review handover | Full tool schemas or universal workflow scripts |
| Exposed tool/template schemas | Accepted input fields and configured choices | Operational diagnostics narrative or workflow authority |
| Template packages | Context schema, content sections and rendering | Phase actions or approval |
| Host instruction sources | Stable tool policy, startup/role/approval boundaries, navigation | Template/adapter inventories |
| Tool/developer references | Focused usage, extension, configuration and limitations | Another authoritative live schema or fixed inventory |
| DI-07 tests/review | Public instruction behavior, nineteen semantic obligations and documentation authority | A new schema implementation or prose-completeness engine |

This package changes configuration/instruction/document consumers, not domain managers
or presentation DTOs. DI-08 supplies reusable public composition and documentation-check
support; DI-07 owns the behavior asserted.

## 6. Options and Rationale

| Alternative | Assessment |
|---|---|
| Copy updated V3 calls into every phase and host file | Repeats field knowledge and recreates drift on the next interface change; rejected |
| Replace every phase with a generic scaffold/check instruction | Loses causal Bug analysis, Refactor preservation and other workflow distinctions; rejected |
| Put phase instructions in templates | Makes renderer structure a competing workflow authority; rejected |
| Explicit workflow outcomes plus current schema discovery | Selected: strong direction without duplicated invocation contracts |
| Keep a standalone reference for removed validator classes | No surviving API to document; consolidate useful concepts into current references |

## 7. Detailed Design

### 7.1 Phase Instruction Contract

Keep the exact existing workflow/phase selection and handover authority. Specify required
actions by tool role/name and purpose, not serialized argument inventories. Discovery is
needed when the applicable current schema is not already available; it is not an
unconditional extra call. Keep first-invocation get_work_context and the documented
open-issue/end-issue exceptions; returned phase instructions do not recursively request
another get_work_context.

Illustrative Refactor Research wording:

> Obtain the current Research context schema if it is not already available. Create the
> initial document with scaffold_artifact and refine it with safe_edit_file. Record
> evidenced responsibility/coupling problems, preserved behavior and invariants,
> alternatives and the explicitly approved strategy. A valid scaffold is not phase completion.

Preserve proportional workflow-driven testing, conditional Chore persistence, explicit
human strategy approval and outcome-neutral handovers. Do not prescribe universal TDD,
rerun fresh evidence unconditionally, or allow producer-authored GO to replace independent QA.

### 7.2 Nineteen Workflow Meanings

DI-03 §7.8 owns exact carrier field names, requiredness and rendering. The following
requirements define what those carriers must express, not another field schema.

| Variant | Meaning that must survive in the persisted document |
|---|---|
| Feature Research | Evidence, affected consumers, alternatives/risks, expected results and approved strategy |
| Bug Research | Reproduction/occurrence context, causal evidence, correction boundary, expected results and strategy |
| Refactor Research | Responsibility/coupling problems, preservation invariants, exclusions and strategy |
| Chore Research | Bounded objective, scope, consumers, risks and strategy; persistence remains conditional |
| Epic Research | Workstream/consumer boundaries, assumptions, dependencies, risks and shared strategy |
| Feature Design | Production responsibilities, interfaces, flow/failures, alternatives, test design and migration |
| Bug Design | Smallest causal correction, preserved behavior, failure behavior and regression evidence design |
| Refactor Design | Target responsibilities/interfaces, preservation, cutover/removals and test architecture |
| Epic Design | Cross-workstream interfaces, ownership, integration/failures and shared evidence obligations |
| Feature Planning | Dependency-ordered work, deliverables, verification and exit criteria |
| Bug Planning | Reproduction/regression/correction obligations and exit evidence |
| Refactor Planning | Responsibility moves, preservation/removal obligations, dependencies and stop conditions |
| Docs Planning | Documentation scope/ownership, sources, deliverables, risks and verification; no invented TDD cycles |
| Epic Planning | Child ownership, shared obligations/dependencies, acceptance and stop conditions |
| Feature Validation | Observed requirement coverage, demonstration, failures, caveats/risks and deferred work |
| Bug Validation | Observed reproduction correction, regression and preserved behavior |
| Refactor Validation | Observed structural completion/removal, invariants and outstanding failures/caveats |
| Hotfix Validation | Correction, containment, preservation and operational risks/caveats |
| Chore Validation | Bounded objective coverage and proportionate observed evidence/risks/deferred work |

Reuse meaningful DI-03 contexts and public rendering evidence to demonstrate these
capacities; do not invent nineteen runtime validators or duplicate the template inventory.
Planned verification is not observed evidence. Cycle-based Planning projects only the
approved explicit fields into save_planning_deliverables; narrative Docs/Epic work units
do not create a second cycle engine.

### 7.3 Host Source Synchronization

| Source | Mapped consumer |
|---|---|
| docs/agents/vscode/copilot | AGENTS.md and applicable .github agent/prompt files |
| docs/agents/codex | Corresponding .agents rules, workflows and skills |
| docs/agents/antigravity | Corresponding host-managed rules/workflows |
| docs/agents | Generated mcp_server/assets/agents release content |

Follow the actual existing mappings, not a blind whole-directory overwrite. Credentials,
local MCP connection config and machine-specific settings are excluded. Direct-copy
source/consumer pairs must remain byte-equivalent; deliberate host differences belong
between their respective sources. Do not generate Codex instructions from an unrelated
VS Code source.

The frozen catalog's reverse/generated wording does not create a second authority:
the inspected instruction model and release-assets procedure explicitly own source-first
direction. This Design records that direction without rewriting Research history.

### 7.4 Consumer Guidance

| Need | Required guidance |
|---|---|
| Select inputs | Use exposed schemas/configured selections; no YAML reading needed for ordinary calls and no copied inventory |
| Interpret output | success concerns operational execution, not domain pass/fail; test/check findings are not automatically MCP errors; use existing text/cache presentation |
| Scaffold/refine | Configured pre-mutation checks; enforce/report and independent safety failures; no caller native args on scaffold/safe-edit |
| Diagnose/fix/recheck | run_checks, authorized apply_fixes on explicit files and ordered bindings, then agent-selected recheck; no automatic choreography |
| Recover | Failure may leave native changes; inspect actual changes and use owner-authorized narrow safe-edit/Git recovery, not indiscriminate restore |
| Configure | Native settings SSOT, transparent default_args and per-binding caller replacement; no generic native-flag reinterpretation |
| Install/extend | bundled_adapters versus workspace_adapters, explicit workspace trust and owner-provisioned dependencies |
| Upgrade | Existing config remains owner-controlled; reconcile missing profiles explicitly and rerun; force does not overwrite config |
| Reload | Restart after relevant package/config changes; launch-environment changes may require a fresh client launch; no new health-first gate |

Targeted examples may appear in the appropriate tool reference and must match the real
schema. The prohibition is on duplicated invocation inventories in phase/always-on
instructions, not on all useful examples. Native tool option semantics remain native.

### 7.5 Active Reference Dispositions

| Surface | Disposition / destination |
|---|---|
| docs/manuals/phase-workflows.md | Retain as short authority/navigation overview pointing to runtime workflow contracts; remove the obsolete universal phase narrative |
| docs/reference/validation_api.md | Remove standalone old TemplateAnalyzer/LayeredTemplateValidator API; retain applicable suite/schema concepts in TEMPLATE_LIBRARY_USAGE and check-consumer concepts in modular tools references; rewrite active inbound links |
| docs/reference/MCP_TOOLS.md | Navigation-only to tools/README.md, no second exact tool inventory |
| docs/reference/TEMPLATE_LIBRARY_QUICK_REFERENCE.md | Remove fixed IDs/fields/paths inventory; route active readers to discovery and usage guidance |
| docs/reference/TEMPLATE_LIBRARY_PATTERNS.md | Remove stale project-specific pattern inventory; no replacement copied inventory |
| docs/reference/TEMPLATE_LIBRARY_USAGE.md | Rewrite durable discovery, schema, extension, valid-basis scaffolding, refinement and restart/ownership guidance |
| docs/reference/tools modules | Correct V3 tool/config/input/result explanations in their existing consumer modules; retain accurate policy use of the words quality gate |
| Root README and setup/release guides | Align delivery roots, native dependency ownership, first-V3 migration, config preservation and honest limitations |

All other catalogued active instructions/references retain their explicit DI-07
disposition. This table resolves the conditional choices, not a replacement path census.

## 8. Control, Data, and State Flow

An agent reads the active phase instructions, discovers missing current input knowledge,
scaffolds and refines the required artifact, gathers phase-appropriate evidence, then
produces an outcome-neutral handover. Schema validity proves input shape, not completeness.
Independent QA determines the bounded verdict.

Missing native dependencies follow DI-05 on-use results. Domain findings, blocked
persistence, protocol failures and partial native fixes retain their upstream meanings;
documentation cannot normalize them into a single pass/fail claim. No new runtime state,
failure DTO, cache or presenter is introduced here.

## 9. Compatibility, Migration, and Removal

Apply the approved V3 clean break consistently: run_checks, framework-neutral run_tests,
apply_fixes and their role configs; safe-edit validation=enforce|report; remove obsolete
mode/strict/interactive/verify_only and validate_template usage instructions. Do not
install aliases or resurrect a removed operation through documentation.

Current contracts.yaml contains V2 scaffold invocations and run_quality_gates calls.
Current test_contracts_loader requires literal context= and selected discovery names.
Replace those obsolete literal expectations while preserving loader behavior, phase
order, authority and meaningful tool-use obligations. Update source and mapped host
copies together at the public cutover; do not advertise V3 before its internal routes work.

Historical issue records remain historical. No unrelated GitHub/workflow behavior changes.

## 10. Test and Validation Design

| Evidence ID | Independent claim / boundary |
|---|---|
| DOCFLOW-E01 | Public contract loading/get_work_context preserves workflow phase order, required actions, startup exceptions, handover and approval roles without obsolete invocation syntax |
| DOCFLOW-E02 | Every §7.2 variant can express its required meaning through real DI-03 public schema/rendering; review meaning, not merely field/substring presence |
| DOCFLOW-E03 | Actual direct-copy host mappings remain equal while unrelated host-specific/local config remains unchanged |
| DOCFLOW-E04 | Active links and reference dispositions resolve; removed API/inventory pages have no active authoritative callers |
| DOCFLOW-E05 | Targeted examples agree with registered tool/schema contracts, including absent legacy modes, explicit scopes and args/default behavior |
| DOCFLOW-E06 | Guidance preserves domain-versus-operational outcomes, native partial mutation, explicit recovery, config ownership and restart limitations |

Reuse existing loader/integration and DI-03 evidence where still valid. No per-word tests,
full phase-prose snapshots or second parser implementing the tool/schema contract.
DI-08 supports isolated public composition, parity and link checks; DI-07 owns the claims.
Concrete wording must receive semantic review: a passing substring assertion is not
evidence of good instructions.

Inspected sources: contracts.yaml, test_contracts_loader.py, instruction-model and
release-assets documentation, active phase-workflows and validation_api, the catalog and
DI-03 §7.8. No runtime tests, host synchronization, document removals or new tool behavior
were executed during this Design consolidation.

## 11. Integration Risks and Open Questions

No remaining W11 product choice. Independent combined review and implementation evidence
remain open. Risks: active docs advertise unavailable V3 behavior too early; stale source
direction overwrites the wrong host file; examples drift; configuration guidance implies
automatic installation or recovery. Sections 7–10 define their prevention and proof.

W12 and the cross-package reconciliation are recorded in DI-08 and
[the semantic ledger §4](design-integration-review.md#4-semantic-integration-closure).
Independent closure review, not another product workshop, remains required. Refer to
[deferred work](deferred-work.md) for health, sandbox and unrelated expansion exclusions.

## 12. Planning Consequences

Allocate concrete catalog paths to bounded owners for source instruction updates, mapped
consumer parity, reference cleanup and semantic alignment. No remaining-docs catchall.
Preserve public-cutover ordering and separate check/test/fix evidence. This document
allocates no cycles and does not authorize a phase transition.

## 13. Traceability Matrix

| Obligation | Design / proof |
|---|---|
| F-09; documentation-authority strategy | §§5–7 source authority and reference cleanup; DOCFLOW-E01/E03/E04 |
| Workflow/template semantic-alignment strategy | §7.2 nineteen meanings with DI-03 §7.8; DOCFLOW-E02 |
| I-12 / E-15 | Explicit phase actions and workflow-specific persisted meaning; §§7.1–7.2 |
| I-13 / E-16, consuming DI-04's invariant | Valid initial scaffold is not final phase completion; §§7.1/8 and DOCFLOW-E02 |
| E-09 | Active documentation cannot contradict live schemas; §§5/7.5 and DOCFLOW-E04/E05 |
| I-15 / E-19 | Tool enforcement without invocation duplication; §7.1 and DOCFLOW-E01/E05 |
| DI-07 | Entire document; exact conditional phase-workflows/validation_api choices in §7.5 |
| F-20 downstream consumers | §7.4/§9 separate check/test/fix, native settings, clean-break vocabulary and recovery |
| XC-01 | No duplicate schema/config authority or new domain/presenter logic; public-boundary test design |
| XC-02 | Active old API/inventory/invocation removal and inbound-link proof; DOCFLOW-E04/E05 |
| RC-01 | Frozen Research and existing ownership; no new role, compatibility shell or deferred feature |
| DI-08 dependency | §10 reusable support only; behavioral evidence remains DI-07-owned |

## 14. Related Documentation and Version History

[Design hub](design.md), [Research](research.md), [intake](design-intake-map.md),
[catalog](template-suite-catalog.md), [document contracts](design-document-tracking-artifacts.md),
[adapters](design-execution-adapters.md), [distribution](design-distribution.md).

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.1 | 2026-09-12 | @imp designer | Reconcile semantic integration, canonical status and proof ownership after independent QA; no phase approval or executable conformance claimed. |
| 1.0 | 2026-09-12 | @imp designer | Consolidate human-approved W11, nineteen semantic obligations, source-first synchronization, reference dispositions and independent evidence; combined QA pending. |
