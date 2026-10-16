<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue 506 — Unused operation-policy infrastructure

**Status:** RESEARCH — QA REVIEW REQUESTED  
**Version:** 0.2  
**Last Updated:** 2026-10-16

## Purpose

Define a coherent removal boundary and distinguish dead operation policies from live tool/workflow enforcement.

## Scope In

Engine/decision value, models/exports, layered YAML, loader/bootstrap/cross-validation, direct tests/helpers and current docs.

## Scope Out

EnforcementRunner and its declarations/decorators, workflow contracts/gates, check/test/fix and template policies, artifact persistence, native settings, release/build/upgrade mechanisms and issues507–508.

## Problem Statement

PolicyEngine has no production construction or decision consumer, while policies.yaml remains required during startup. Removing only the apparent engine or YAML would leave an inconsistent contract. Establish the complete boundary and decide the exported Python/config break explicitly.

## Goals

- Account for concrete runtime, test and inspectable external consumers.
- Propose coherent removal without a replacement framework or weaker active admission.
- Remove tests solely for dead code and adapt only direct retained consumers.
- Obtain a human-approved removal strategy before closing Research.

## Background

#319 preserved the engine's fail-closed exception handling without establishing a live caller. #504 deliberately kept startup-loaded policies.yaml pending #506, rather than removing it by assumption. Baseline main includes #505. No broad test run is repeated as Research ceremony.

## Findings

### Runtime and consumer evidence

Only tests/mcp_server/test_support.py:429–440 constructs PolicyEngine, used by two dedicated engine test modules. PolicyDecision is local to that engine. No active tool, resource, manager, service or entry point calls its decision API. The engine docstring's claim that MCP tools use it is stale.

Bootstrap currently loads policies.yaml, validates allowed phases, stores OperationPoliciesConfig in ConfigLayer and forwards it. No manager/tool consumes that field. This creates a real startup prerequisite for an engine absent from request composition.

Live admission follows Bootstrap → EnforcementRunner → ToolFactory → EnforcementDecorator → runner.run(pre/post) → configured handlers/core tool. It reads enforcement.yaml and Git/state/PR/context dependencies, not operation policies. Phase-contract gates, template policy.yaml and output-check profiles are separate active mechanisms.

### Coherent candidate inventory

| Surface | Proposed bounded change |
| --- | --- |
| Engine | Remove core/policy_engine.py including PolicyDecision, audit/reload methods and its unused exception catch. Preserve shared capture_exception/error wrappers. |
| Models and exports | Remove config/schemas/operation_policies_config.py and only its imports/exports in config/schemas/__init__.py and schemas/__init__.py. |
| Loader and startup | Remove load_operation_policies_config; Bootstrap import/load/ConfigLayer field/forwarding; ConfigValidator policies parameter and operation-phase validation. Preserve all workflow/phase/merge checks. |
| Shipped sources | Remove .pgmcp/config/defaults/policies.yaml and the empty .pgmcp/config/policies.yaml override. Existing fresh directory assembly then omits them; no manifest/builder change. |
| Dead tests/helper | Remove core/test_policy_engine.py (9 test functions), core/test_policy_engine_config.py (3), config/test_operation_policies.py (15); remove make_policy_engine/import in test_support.py. Counts describe functions, not parametrized cases. |
| Five retained test modules | Adapt unit/config/test_c_loader_schema_structural.py, test_label_startup.py, test_validator_c3.py, test_workflow_config_c6.py and unit/server/test_bootstrap.py. Remove policy-only fixture/rows, unknown-policy-phase case and two structural tests whose only subject disappears; preserve meaningful workflow/merge/startup assertions. |
| Current docs | Correct README's config table and add bounded removal/owner-cleanup guidance to the current configuration reference. |

This does not justify a general rewrite of shared factories, their callers or all structural tests. No compatibility, legacy-absence or deletion-string regression test is proposed.

### External and installation boundary

Scoped searches of C:/temp/S1mpleTrader and C:/temp/S1mpleTraderV1 found no Python/YAML/TOML caller of these symbols/config contracts. One S1mpleTrader architecture/instruction example mentions PolicyEngine.decide() at docs/architecture/VSCODE_AGENT_ORCHESTRATION.md:1489. That prose is not an execution consumer. It is an owner-workspace doc follow-up; no edit to another repository is authorized.

The models/loader are importable and re-exported. Removal technically breaks unknown direct Python imports, even though no supported external caller was found. The inventory cannot prove absence of every downstream package. No MCP tool input/output DTO refers to this engine.

Fresh package/init copies no longer include the removed source YAML. Existing owner-managed workspaces may retain unused policies.yaml; the new loader will not read it. Document deliberate owner cleanup, without automatic deletion/migration or a compatibility loader. No release, deployed workspace mutation or historical artifact rewrite.

The vision reference explicitly says HISTORICAL ARCHITECTURE CONTEXT; keep it and earlier issue reports as history. Use pinned source links for files expected to disappear. No active instruction/template reference was found that requires a synchronized change.

### Alternatives and maintenance boundary

| Strategy | Trade-off |
| --- | --- |
| Coherent clean removal (recommended) | Small explicit break to unused Python/config interfaces; direct fixtures/docs move together; actual enforcement unchanged. |
| Retain supported API | Requires an identified supported caller/purpose. None found; otherwise startup burden and misleading claims remain. |
| Remove engine but keep loader/schema bridge | Retains maintenance and required startup configuration without demonstrated value; not recommended. |

This stays a Chore as removal plus direct consumer maintenance. A discovered supported engine caller, replacement framework, enforcement alteration, general configuration refactor or automatic migration requires a new scope/workflow decision.

### Verification boundary

Implementation: narrow existing loader/validator/bootstrap modules plus public enforcement/context/PR-lock/phase-admission coverage; no dead-engine preservation tests. Validation owns one full native-configured suite and the required filtered branch/configured-production gates, with native arguments/coverage preserved. Reuse fresh narrow evidence. The #505 suite is baseline history, not a waiver or proof of this future change.

### Execution checkpoint

- Issue/branch/parent: #506; chore/506-unused-operation-policy; main.
- Phase/baseline: Research; b42b43d696ab12bb85dbb8fbf639e68569aaeee0.
- Scope/owner decisions: bounded unused-route investigation authorized; owner explicitly approved the proposed clean break on 2026-10-16 ("Akkoord!").
- Code/tests: unchanged; no tests executed during Research.
- QA boundary/verdict: Research → Implementation; independent review requested on the completed Research commit.
- Blocker/next action: no owner decision remains; request independent Research → Implementation GO/NOGO and wait before production edits.

## Questions

None remaining within the approved boundary.

## Approved Strategy

The human owner explicitly approved the complete proposal on 2026-10-16: "Akkoord!" This is the removal-strategy decision, separate from queue/merge authorization.

| Boundary | Approved strategy |
| --- | --- |
| Engine, importable models/exports and loader/bootstrap contract | Clean removal; no compatibility aliases, deprecated stubs or replacement framework. Unknown direct importers must move explicitly. |
| Shipped YAML / existing workspaces | Remove both shipped policies.yaml sources. Document deliberate owner cleanup; no automatic deletion/migration of existing workspace files. |
| Tests/helpers | Remove dead route-only tests and its factory; adapt direct retained consumers and preserve meaningful behavior. No extra legacy/deletion regression tests or suite-wide cleanup. |
| Active admission and safety | Preserve EnforcementRunner, decorators, enforcement config, workflow contracts/gates, template and check/test/fix policy without semantic changes. |

Stop and reopen scope if a supported live consumer appears or implementation requires changes to active enforcement, a replacement framework, automatic migration or a broader config refactor.

## Expected Results

Startup no longer requires unused operation-policy files; actual safety and cross-config workflow behavior remain. Focused retained behavior tests and the required full native suite pass. No dead test ballast, replacement architecture, release or target rollout.

## Evidence

### No composed production decision consumer was found.

Only test support constructs PolicyEngine; Bootstrap loads and forwards an otherwise unused field. Live wrappers use EnforcementRunner.

- [Baseline engine](<https://github.com/MikeyVK/phase-gate-mcp/blob/b42b43d696ab12bb85dbb8fbf639e68569aaeee0/mcp_server/core/policy_engine.py>)
- [Bootstrap](<../../../mcp_server/bootstrap.py>)
- [Live decorator](<../../../mcp_server/core/decorators/enforcement_decorator.py>)
- [Live runner](<../../../mcp_server/managers/enforcement_runner.py>)

**Invocation:** Host-native rg on explicit mcp_server/tests roots for PolicyEngine, PolicyDecision, operation_policies_config, load_operation_policies_config and make_policy_engine, followed by inspection of engine, bootstrap, validator, ToolFactory and EnforcementDecorator.

### No concrete external code/config caller was found in the inspectable owner projects.

One S1mpleTrader architecture/instruction example mentions the engine. Unknown downstream Python imports cannot be excluded.

**Invocation:** Scoped rg in C:/temp/S1mpleTrader and C:/temp/S1mpleTraderV1 for Python/YAML/TOML/Markdown, excluding dependencies, scratch and development history.

## Risks

### Confusing legacy operation policies with active enforcement/template policies.

Keep actual runner/decorator/config/contracts and artifact services intact; use existing public admission behavior for preservation evidence.

### Unnecessary shared-test blast radius.

Remove three dead modules/one factory and adapt five retained modules; no suite-wide cleanup.

### Historical links to removed code.

Pin new evidence links to baseline; preserve historical reports rather than dead source or broad historical rewrites.

## Related Documents

- [Issue506](<https://github.com/MikeyVK/phase-gate-mcp/issues/506>)
- [Configuration composition](<../../reference/config-loading-architecture.md>)
- [Architecture contract](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)
- [504scope](<../issue504/research.md>)
- [505baseline validation](<../issue505/validation.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-16 | @imp researcher | Trace operation-policy consumers, preserved enforcement and bounded clean-break proposal; human strategy pending. |
| 0.2 | 2026-10-16 | @imp researcher | Capture explicit owner approval per affected boundary; close open strategy question and request independent Research review. |
