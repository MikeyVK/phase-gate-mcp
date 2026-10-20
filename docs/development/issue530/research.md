<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue \#530 — normal planning-note formatting

**Status:** Research complete — independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-20

## Purpose

Establish the cause of the successful planning-update note defect without redesigning presentation or planning.

## Scope In

Normal TextPresenter note formatting, existing scalar-sequence policy and tool limits, isolated update/readback evidence and directly affected consumers.

## Scope Out

Planning mutations/protection redesign; new note schema, defaults, formatter framework, output/channel/cache policy, compatibility layer, harness matrices, Windows lifecycle timing repair or release work.

## Problem Statement

An otherwise successful update_planning_deliverables returns an internal formatter error in its planning_cycle_evidence informational note. Two previous observations (#524 and #528) showed correct persistence. Current source and isolated SDK evidence now separate the missing presentation dependency from the successful mutation.

## Goals

- Identify causal conditions and counterevidence through actual public rendering/SDK paths.
- Verify complete original/appended cycle facts through an independent readback.
- Bound the correction to the existing configuration-driven presentation responsibility and preserve genuine diagnostics.

## Background

Co initialized bug/530-fix-planning-update-note-formatting from explicit main after #528/PR532 merged at e4608103bc94f0ae60f08e5e2c719ae830b8de18. Initial worktree contained only Co-created untracked state.json/deliverables.json. No live planning mutation was replayed. Historical records are context; current evidence below is decisive.

## Findings

### Causal path

| Path | Current formatter inputs | Observation |
| --- | --- | --- |
| Main data template | global FormattingConfig and tool max_items | Existing supported flat-sequence route |
| Next instruction | Same global policy and tool max_items | Existing supported flat-sequence route |
| present_notes | none_value only | Missing both inputs required for any list/tuple |

ProjectManager produces planning_cycle_evidence with protected_cycle_numbers=list(evidence.protected_cycle_numbers). Its configured note references that value. SafeNoneFormatter._format_sequence rejects missing formatting/max_items before checking whether a sequence is empty. Thus both [] and [1] fail. present_notes catches the native ConfigError, logs its traceback and returns Format error text in the Information group. The operation has already persisted and keeps success=true; this is a handled normal-rendering defect, not #528 compact recovery.

### Input range and existing policy

The causal defect applies to flat scalar list/tuple values referenced by global or local note templates across all four existing note groups. Scalar/None note values do not enter _format_sequence. Nested sequences, dictionaries, sets and models remain unsupported values under the existing formatter contract.

The current planning-update entry already has max_items=10; global formatting already defines separator, empty/None representation and omission wording. The generic formatter already bounds flat sequences with that policy. No numeric policy default is missing for the observed case.

Current defaults contain 49 tool entries: 28 declare max_items and 21 do not; the workspace presentation override is {}. Scalar-only entries need no new limit. Active Git/enforcement notes such as allowed types/bases/protected branches already supply strings, and transition recovery_steps is a string. No producer conversion or broad configuration migration is justified. Arbitrary future/custom note parameters remain dynamic; this is not a claim that startup can infer every possible note type.

### Reproduction route

1. Create a temporary workspace and copy only stable config inputs. Reuse make_project_manager with an explicit fixed Git reader and ICycleEvidenceReader reporting complete evidence; separately cover protected_cycle_numbers=() and (1,).
2. Initialize temporary issue 530, feature workflow, explicit parent main. Save C_1 with a named deliverable, description and exit criterion; retain a typed full-block snapshot.
3. Compose real UpdatePlanningDeliverablesTool/GetProjectPlanTool through ToolFactory and the real ResponsePresenter/TextPresenter. Only admission/evidence adapters are controlled doubles; this does not claim production enforcement or Git traversal coverage.
4. Through connected_mcp_client, append C_2 with a distinct deliverable and criterion. Observe isError=false, success=true and the recorded formatter error in normal text.
5. Independently call get_project_plan over the SDK. Compare C_1's complete stored model to the snapshot and C_2's assigned C_2/D_2.1 identifiers, supplied description and exit criterion.
6. Without another mutation, replay only the captured note through public present_notes while supplying the existing configuration inputs to the formatter in the isolated probe. The note becomes readable with the same source values. Stored-plan readback remains unchanged.

The ignored research probe is .pgmcp/temp/issue530/test_note_probe.py; the steps, public seams, inputs, assertions and observed results here are durable evidence. A later durable behavior case belongs in the existing test surface, not an archive of this temporary probe.

## Approved Strategy

Authority: the owner's standing autonomous execution/independent phase-QA authorization and explicit clean-break/no-legacy policy, reaffirmed by Co's #530 delegation. Reuse the approved #529/#528 public output boundary; no new boundary-specific policy is selected.

| Boundary | Binding strategy |
| --- | --- |
| Project mutation, Git protection and readback | Preserve operational facts and source note parameters; no joining/presentation in managers/tools or persistence changes |
| Public inputs/DTOs/envelope/channels/cache | Preserve current #529/#528 contracts; no additions, compatibility bridge or migration |
| Internal note formatting | Correct conformance to existing global formatting and per-tool limit policy at the presentation boundary; no new setting, numeric fallback or per-tool branch |
| Native exceptions | Preserve existing logging/cause and visible genuine failure behavior; do not suppress or relabel failures |
| Tests | Public behavior and independent readback; prefer existing helpers/surfaces, no durable prose snapshots or legacy/version/harness matrices |

A tool-specific stringify/join workaround crosses §15 and leaves the generic defect; a new global note budget/schema/framework adds policy and maintenance without evidence of need. Neither is justified. A missing tool limit remains missing; this issue must not manufacture one for unsupported list-note configurations. If Design finds that a new limit/default, exception, public schema/channel/cache behavior or scope is required, stop for the owner before progression.

## Expected Results

Supported planning updates render truthful readable informational notes using already-declared policy. Existing/appended cycle IDs, deliverable names/descriptions/criteria and protection/validation are unchanged. Flat sequence order, empty/None display and configured omission behavior are honored; source values remain intact. Genuine invalid-note diagnostics and original operation outcomes remain visible. No public DTO/channel/cache or compatibility policy changes are needed.

## Evidence

### Real SDK reproduction with independent persistence readback and local counterfactual

2 passed in 2.98 s (513394ad359644739cca5a1ddd11695b). These are characterization/control passes, not a production fix: both protected=() and (1,) reproduce the visible error with success=true; independent readback has unchanged C_1 and appended C_2/D_2.1. Injecting only existing formatting/max_items into note rendering yields protected=- or protected=1 and HEAD=probe-head, without another write.

- [Mutation and note producer](<../../../mcp_server/managers/project_manager.py>)
- [Public planning tools](<../../../mcp_server/tools/project_tools.py>)
- [Note presenter](<../../../mcp_server/presenters/text_presenter.py>)
- [Existing SDK/factory helpers](<../../../tests/mcp_server/test_support.py>)

**Invocation:** run_tests(scope='targets', targets=['.pgmcp/temp/issue530/test_note_probe.py'], tests=['python_tests'], args={'python_tests':['-n','0','-s']}, timeout_seconds=180)

### Initial probe setup failure distinguished from defect evidence

First attempt: 2 failed in 48.39 s (3c27d56189774cfd8f9b12a9340adf62) before mutation because the temporary workspace lacked config/defaults/contracts.yaml. Copying the stable config inputs into that temporary workspace corrected setup. No production file or config was changed.

- [Strict test configuration factory](<../../../tests/mcp_server/test_support.py>)

### Shared formatter already implements the required scalar-sequence behavior

The source requires both FormattingConfig and max_items, handles empty values via none_value, preserves source order, and uses configured separator/omission text. Existing tests exercise list/tuple bounds and unsupported nested values. The note route alone omits its required dependencies.

- [Formatter and guard](<../../../mcp_server/presenters/collection_text_renderer.py>)
- [Existing formatter behavior tests](<../../../tests/mcp_server/unit/presenters/test_collection_text_renderer.py>)
- [Current presentation defaults](<../../../.pgmcp/config/defaults/presentation.yaml>)

## Consumers

### TextPresenter.present\_notes / present\_text

Generic global/local note selection and normal short response

**Impact:** Direct causal boundary; current main/next-instruction formatting already receives existing policy. Interface remains unchanged.

### ProjectManager and planning command/readback tools

Persist complete blocks, protect Git evidence and publish native note facts

**Impact:** Evidence only; no change to parameters, stored data, mutation/protection or diagnostics.

### ITextPresenter / ResponsePresenter / MCPServer / startup presenter

Presentation interface and current common output contract

**Impact:** No public shape or channel change. Normal ResponsePresenter delegates to TextPresenter; compact recovery and startup routes remain outside the correction.

### NoteContext.render\_to\_response

Public note-helper seam

**Impact:** No production callers found beyond its declaration/docstring; tests call it. Same unchanged ITextPresenter surface; no cleanup proposed.

### Tests and fixtures

Generic note behavior plus update/persisted readback

**Impact:** Existing presenter/formatter tests and public planning/tool SDK helpers are reusable. No manager-constructor or suite-wide fixture change is indicated.

### Active docs/agents/configuration

Configuration-owned presentation boundaries

**Impact:** A targeted note-policy clarification in the active presentation reference may be needed. No new config field, agent instruction, phase contract, template or enforcement is justified; historical issue docs stay context-only.

## Risks

### Accidentally introduce a numeric note default or stringify facts in a producer.

Consume existing declared policy at the current presentation boundary; leave missing limits and genuinely invalid values diagnosable.

### A rendering-only test could mask persistence or protection corruption.

Use an isolated real planning update and an independent public readback, plus existing domain/protection cases. Preserve source facts.

### Tests become brittle prose/config snapshots or multiply whole harness matrices.

Assert input-derived values, order, configured bounds, diagnostics and persisted models through existing public seams; no wording snapshots.

## Related Documents

- [Issue #530](<https://github.com/MikeyVK/phase-gate-mcp/issues/530>)
- [Earlier #524 observation](<../issue524/validation.md>)
- [#528 retained evidence](<../issue528/validation.md>)
- [Architecture §15](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)
- [Current presentation contract](<../../reference/presentation_architecture.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-20 | @imp researcher | Reproduce handled note failure and intact persistence; establish missing formatter inputs, bounded consumer impact and inherited strategy. |
