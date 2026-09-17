<!-- C:\temp\pgmcp\temp\issue460-design-workshops-20260910\11-workflow-documentation.md -->
<!-- template=design version=5827e841 created=2026-09-10T09:24Z updated= -->
# W11 — Instructions, document carriers and live tool contracts

**Status:** HUMAN-APPROVED — consolidated in docs/development/issue460/design-workflow-documentation.md on 2026-09-12; combined independent QA pending  
**Owner:** DI-07; DI-03 owns schemas/renderers; upstream W01–W10 public decisions  
**Decision nucleus:** Update meaning and authority together, with nineteen explicit workflow/phase mappings and source-first host instructions.

## 1. Purpose and authority

**Workshop refresh, 2026-09-12:** W10 is human-closed in DI-06 §§7.6–7.7;
W11 is now human-approved and consolidated; this file remains a non-authoritative workshop record. The nineteen field mappings below are synchronized with the
independently reviewed DI-03 §7.8, not a second schema design. Earlier preparation
names such as interfaces/flows or obligation_mapping are superseded by that source.

Agents should learn exact current inputs from exposed tool/schema contracts, and learn what work must be done from phase instructions. Documentation should explain that relationship, not become a competing registry.

## 2. Scope and exclusions

All active Research/Design/Planning/Validation variants, mapped host instructions, active manuals/references and conditional documentation dispositions. No new runtime completeness checker, generated tutorial system, health-first instruction, sandbox promise or workflow rewrite.

## 3. Binding inputs

F-09, I-12/I-13/I-15, E-15/E-16/E-19, [Research nineteen-variant map](C:/temp/pgmcp/docs/development/issue460/research-findings.md:475), [instruction authority](C:/temp/pgmcp/docs/reference/copilot-agent-instructions-model.md:19), contracts.yaml and W08.

## 4. Proposed decisions

| ID | Proposal |
|---|---|
| W11-A | contracts.yaml owns substantive workflow actions; schema owns exact fields |
| W11-B | Edit docs/agents/<host> source first and synchronize its actual mapped consumer |
| W11-C | Reduce phase-workflows to navigation; consolidate obsolete validation_api |
| W11-D | Demonstrate carrier capacity per variant without copying phase prose into templates |

## 5. Responsibilities and boundaries

| Authority | Owns | Does not own |
|---|---|---|
| contracts.yaml | Phase purpose/outcomes, workflow-specific completeness, tool choice/timing and evidence scope | Full tool invocations or copied parameter inventories |
| Template package | Context schema, semantic sections and rendering | Workflow actions or QA approval |
| Runtime tool contract | Exact fields, configured choices/defaults | Startup diagnostic narrative |
| Host instruction source | Stable tool policy and role/approval boundaries | Template/adapter inventory |
| References | Explanations and navigation | A second live schema or fixed tool count |

The catalog contains old reverse source-direction wording. Current instruction-model documentation and release_manifest say docs/agents is authoritative. This draft records source-first migration as the recommendation; it does not silently edit frozen Research or reverse host files.

## 6. Options and rationale

Duplicated invocation snippets drift with public cutover. One generic phase script erases important workflow distinctions. Choose explicit variant semantics plus links to actual tool discovery, and keep generated/direct-copy parity tests distinct from semantic workflow tests.

## 7. Detailed design

### Nineteen-variant carrier record

These are required semantic capacities; W08 owns exact field shapes and whether each field is optional in a reusable initial schema.

| Workflow / phase | Persisted outcome | W08 named carriers |
|---|---|---|
| Feature / Research | Evidence, alternatives, risks, expected behavior, strategy | evidence, consumers, risks, findings, approved_strategy, expected_results |
| Bug / Research | Reproduction, causal evidence, occurrence conditions, correction boundary | problem_statement, background, evidence, findings, expected_results, approved_strategy |
| Refactor / Research | Coupling, duplication, responsibilities, invariants and preservation | consumers, findings, evidence, scope_out, approved_strategy, expected_results |
| Chore / Research | Objective, mechanical boundary, proportional risk; persistence conditional | problem_statement, scope_in/out, consumers, risks, approved_strategy; persistence stays conditional |
| Epic / Research | Initiative/workstreams, dependency/ownership and shared obligations | consumers, findings, assumptions, risks, evidence, approved_strategy, expected_results |
| Feature / Design | Interfaces, architecture, state/failures, tests, migration | production_design, contracts, flow, state_and_failures, options, test_design, transition_and_cleanup, planning_consequences |
| Bug / Design | Smallest causal fix, preservation/regression, alternatives | problem_statement, production_design, preservation, state_and_failures, test_design, validation |
| Refactor / Design | Target responsibilities, dependency/cutover/removals, test architecture | production_design, contracts, preservation, transition_and_cleanup, test_design, validation |
| Epic / Design | Cross-workstream boundaries, shared contracts, ownership/integration | production_design, contracts, flow, state_and_failures, transition_and_cleanup, test_design, planning_consequences |
| Feature / Planning | Bounded dependency-ordered implementation work and evidence | work_units deliverables/dependencies/verification/exit_criteria |
| Bug / Planning | Reproduction/regression/correction work with preserved behavior | work_units goal/scope/obligations/verification/exit_criteria |
| Refactor / Planning | Responsibility moves, preservation, deletion and validation | work_units dependencies/obligations/deliverables/stop_conditions |
| Docs / Planning | Documentation tasks and verification, not TDD cycles | work_units scope/owner/deliverables/verification/risks |
| Epic / Planning | Child ownership, prerequisites/shared obligations/acceptance | work_units owner/dependencies/obligations/deliverables/exit_criteria/stop_conditions |
| Feature / Validation | Design/strategy coverage, exact checks, demonstration/fallback | obligations, evidence, demonstration, failures, caveats, risks, deferred_work |
| Bug / Validation | Corrected reproduction, regression and preservation | scope, obligations, evidence, preservation, failures |
| Refactor / Validation | Structural completion, removal, invariant preservation | obligations, evidence, preservation, failures, caveats |
| Hotfix / Validation | Correction, containment/rollback and operational risks | scope, evidence, preservation, containment, caveats, risks |
| Chore / Validation | Objective coverage and proportional fresh evidence | scope, obligations, evidence, risks, deferred_work |

For each row, canonical integration must supply one real context/example that renders the required meaning, then review its meaning. No text-substring test can prove causal analysis or design completeness.

### Instruction wording pattern

Current `contracts.yaml` embeds V2 artifact_type/name/context invocations and
run_quality_gates calls. `test_contracts_loader.py` requires literal context= and
discovery names for selected variants. Those assertions preserve obsolete syntax,
not the underlying requirement to scaffold and complete the appropriate phase artifact.
Retain loader, workflow/phase-order and authority evidence; replace obsolete assertions
with bounded contract checks and human semantic review. Do not claim that substring
presence proves a complete Research/Design document.

Proposed refactor-Research instruction fragment (illustrative prose, not a new schema):

> Obtain the current Research template context schema if it is not already available.
> Create the initial document with scaffold_artifact and refine it with safe_edit_file.
> Record evidenced responsibility/coupling problems, preserved behavior and invariants,
> alternatives and the explicitly approved strategy. A valid scaffold is not phase completion.

Require discovery when current schema is absent/stale; require scaffold_artifact by name for initial creation; describe subsequent safe_edit_file refinement; require run_checks/run_tests/apply_fixes by role, authorization and appropriate scope. Do not embed complete invocations or demand unconditional scaffold_schema.

A valid initial scaffold is a structurally coherent basis. Phase completeness follows actual required evidence and review, not successful scaffolding. Keep Chore persistence conditional, workflow-driven TDD proportional and independent QA authority explicit.

### Source and reference dispositions

| Surface | Proposed disposition |
|---|---|
| docs/agents/<host> | Authoritative host-specific instruction sources |
| Mapped AGENTS/.agents/.github copies | Synchronize from their actual source; retain intentional host differences |
| mcp_server/assets/agents | Generated release assets, not another source |
| docs/manuals/phase-workflows.md | Short authority/navigation overview, remove fixed universal seven-phase narrative |
| docs/reference/validation_api.md | Consolidate obsolete TemplateAnalyzer/LayeredTemplateValidator reference into suite architecture and adapter contracts |
| MCP_TOOLS.md | Navigation-only to modular tools reference |
| TEMPLATE_LIBRARY_QUICK_REFERENCE/PATTERNS | Remove stale fixed inventories |
| TEMPLATE_LIBRARY_USAGE | Explain discovery, extension, restart, safe refinement and ownership |
| Root README/setup docs | V3 terminology, dependency ownership, migration and honest limitations |

No new fourth reference is created merely to preserve old filename counts. Public tool guidance and adapter-author documentation are distinct audiences; both link to generated/live schemas where exact facts are needed.

### V3 usage and migration guidance

| User/agent need | Required instruction meaning |
|---|---|
| Choose inputs | Inspect exposed tool/schema contracts; no guessed template inventory or requirement to read YAML for ordinary calls |
| Interpret results | Operational success is separate from domain pass/fail; failed tests/check findings are not automatically MCP errors; use the existing text/cache presentation policy |
| Refine content | Scaffold/safe-edit use configured pre-mutation profiles, not caller native args; explain enforce/report and independent blocking safety errors |
| Diagnose and fix | run_checks, explicitly authorized apply_fixes on concrete files and explicit ordered bindings, then agent-selected recheck; partial native mutation may remain after failure |
| Recover | Inspect actual changes and choose narrow safe_edit/Git recovery with owner authority; never automatic rollback or indiscriminate restore |
| Configure | Native config owns tool settings; default_args/caller replacement rules remain explicit invocation inputs, not a second generic rules layer |
| Install or extend | Distinguish bundled_adapters from owner workspace_adapters, explicit trust and provisioned native dependencies; no probe/auto-install promise |
| Upgrade | Preserve owner config; missing profile prevents suite activation; explicitly reconcile and rerun --upgrade; force does not overwrite config |
| Reload | Restart after package/catalog config changes; a changed launch environment may require a fresh client launch; no new health-first gate |

Exact input examples may live in the appropriate tool reference when checked against its
actual schema; the prohibition concerns embedding duplicate invocation inventories in
phase/always-on instructions, not banning useful targeted examples everywhere.

### Planning projection

Use W08's explicit projection for cycle-based work units to existing save_planning_deliverables. Docs/Epic narrative units do not become a new runtime cycle engine by naming them work_units. Preserve shared IDs/deliverables/exit criteria; do not copy full operational payload examples into phase instructions.

## 8. Flow and failure

Changed native config → native tools own interpretation. Changed PGMCP package/config → restart required for catalog changes. Changed launch environment may require client-level fresh launch rather than merely server restart. Missing native dependency appears on use, not guaranteed absent from schemas. Do not add health_check-first requirements: explicitly deferred.

## 9. Migration and removal

Use run_checks/apply_fixes/new role configs consistently, retain run_tests spelling with new meaning, remove safe-edit mode/strict/interactive/verify_only aliases and obsolete validate_template guidance. Preserve “quality gate” as policy terminology where genuinely correct. Historical issue docs remain historical.

## 10. Evidence

Source-to-consumer parity for mapped host files; local links; actual registered tool names/defaults; nineteen semantic carrier examples; no copied context= or full invocation parameter inventories. Current [test_contracts_loader](C:/temp/pgmcp/tests/mcp_server/unit/config/test_contracts_loader.py:337) asserts context= and unconditional discovery; replace those obsolete assertions while preserving loader/phase-order/authority/hand-over proof.

## 11. Review points

Approve source direction, reference consolidation and the semantic alignment record. Do not approve exact prose snapshots or confuse a producer hand-over with independent GO.

## 12. Planning consequences

Instruction sources, mapped host consumers, tool guidance and carrier alignment have concrete owners. Planning must assign their individual catalog rows, not a remaining-docs catchall.

## 13. Traceability

DI-07/F-09; I-12/13/15; all nineteen workflow variants; conditional phase-workflows/validation_api rows; DI-03 ownership preserved; XC-02 stale names/guidance removal.

## 14. Related documentation and history

Next: [W12 test architecture and integration](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/12-test-architecture-integration.md).  
0.1, 2026-09-10: temporary proposal.
