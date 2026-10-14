<!-- pgmcp:v1 id=design pv=1.0.0 pf=Uk1D2XWpiag1c6nn sf=KoFPQ3-cAAWFeesb -->

# Issue 319 — bounded quality configuration choice

**Status:** DRAFT — INDEPENDENT REVIEW REQUIRED  
**Version:** 0.6  
**Last Updated:** 2026-10-14

## Purpose

Define one truthful workspace setup acknowledgement in existing execution bindings, without a native configuration resolver.

## Scope In

Binding choices and unresolved-use refusal across checks, content preflight, tests and fixes; existing native lint/exception/test repairs from Research; focused setup guidance.

## Scope Out

Effective-source discovery, file-presence mandates, config-export/sample assets, package routing, startup blocking, adapter protocol/entrypoint changes, new workflow phases, legacy execution bridges and unrelated test expansion.

## Problem Statement

Empty native argument lists currently cannot distinguish deliberate native discovery, a legitimate no-config capability and incomplete workspace setup. The owner wants an explicit choice with truthful operational meaning.

## Functional Requirements

- Store the owner's choice in each existing checks/tests/fixes binding, not the adapter manifest.
- Keep an unresolved setup state valid at startup; reject relevant use before native invocation or fix side effects.
- Allow selected choices without rewriting args or asserting which native config was resolved.
- Apply identical semantics to selection checks, content-based scaffold/safe-edit/commit preflight, tests and fixes.
- Keep existing not-applicable/empty branch semantics and native argument-origin reporting.
- Keep selected lint cleanup bounded by the Research inventories and existing public behaviors.

## Nonfunctional Requirements

- No native-tool-specific logic in the generic gate; existing adapters/native tools continue to interpret args/config.
- Use pure frozen binding models and existing execution composition; no filesystem IO in choice schemas.
- One compact failure contract and configured presentation, not per-tool special cases.
- Adapt meaningful existing tests and helpers; no content snapshots or legacy-absence test campaign.

## Constraints

- Chore's normal transition is Research → Implementation; this artifact is a compact maintenance design, not a fabricated Design workflow phase.
- No compatibility bridge preserving execution with an unresolved choice.
- Stop if the change requires file discovery, native option rewriting, startup surveys, package config activation or wider policy architecture.

## Decision

Add configuration_choice as a declarative intent/acknowledgement at each workspace operation binding. Its sole runtime enforcement is refusal of unresolved setup before applicable execution. Keep the Chore phase sequence; review this compact design with Research before Implementation.

## Rationale

This addresses explicit setup responsibility without claiming resolved-config certainty or introducing per-tool builders and requirements.

## Production Design

### Binding contract

Illustrative pure type contract, shared by the three existing binding models:

```python
ConfigurationChoice = Literal[
    "native_discovery",
    "configured_arguments",
    "not_applicable",
]
configuration_choice: ConfigurationChoice | None = None
```

A missing field or explicit YAML null means unresolved setup. This equivalence is fail-on-use, not an execution fallback: old/unconfigured bindings do not continue automatically. Empty strings/unknown choices fail ordinary schema validation. Startup accepts the unresolved state so setup/health remain available. The exact shared type module is an implementation placement detail; it must not gain filesystem/native-tool knowledge.

| State | Truth represented | Execution |
| --- | --- | --- |
| Missing/null | Owner has not declared the setup choice | Applicable execution refused |
| native_discovery | Owner knowingly accepts the native tool's existing discovery/config behavior | Existing invocation unchanged |
| configured_arguments | Owner knowingly declares native policy through the binding arguments | Existing default/caller argument selection unchanged; actual args_source remains authoritative |
| not_applicable | Owner declares no additional native policy configuration is needed for this capability | Existing invocation unchanged |

These are owner declarations, not attestations that files exist, args are sufficient or a source was consumed. Caller overrides do not clear/fill the choice; unresolved choice cannot be bypassed by supplying args. A selected choice does not constrain native overrides in this bounded issue. No config-source field is added to native adapter requests.

### Workspace defaults and installation

The distribution source remains this repository's `.pgmcp/config`; the existing asset compiler copies it unchanged. Repository choices acknowledge this workspace only. Fresh `--init` clears `configuration_choice` to null in the newly copied checks/tests/fixes bindings before initialization completes. This is a bounded acknowledgement reset in the existing fresh-init path, using ConfigLoader's admitted binding models and preserving every other binding/config value. It does not read, discover or export native tool configuration; it does not touch an existing server root, template-only renewal, or the source assets. Thus packaged source bindings can contain the repository choices, while effective configuration in a newly initialized workspace is deliberately unresolved. No separate distribution config source, builder or routing layer is introduced. The installation guide identifies `--init` as this ownership boundary; manual copying must likewise clear declarations before choosing workspace policy.

This repository's active bindings record the actually chosen policy: Ruff/Mypy/Pyright/Pytest/Commitlint native_discovery; Lychee and schema checks configured_arguments; Python/TypeScript syntax not_applicable. Metaschema's existing explicit native binding arguments remain configured_arguments; no external file is implied. These assignments are workspace data, not hardcoded tool-name branches.

Setup guide requires provisioning native pins, selecting workspace-native policy/arguments, setting every needed binding choice and performing a scoped check. No native config files are copied/merged automatically. Existing installations missing the field remain available for setup but affected execution requires acknowledgement. Release notes must say this explicitly; review compatibility implications before deciding final release publication.

### Invocation and refusal contract

Resolve the requested binding set and applicability with existing mechanisms. Before any applicable adapter/process or content scratch/fix mutation in the selected operation, reject unresolved choices and identify their binding IDs. For selection checks, do not reject a binding already prefiltered to not_applicable; preserve empty selections. In a mixed batch, unresolved applicable bindings prevent the batch from executing, so a fix batch cannot partly mutate before setup refusal.

For refused operations, use `configuration_choice_required` as the operation error code and the unconfigured binding's consumer-owned row reason. The owner-approved edit-report continuation below retains the row reasons without an operation error after a completed write. Error details contain the ordered, unique affected `binding_ids`, not adapter IDs. Extend only the existing public consumer contracts; the adapter protocol remains unchanged. Validate that the affected IDs exactly match refused rows and that the whole batch has no invocation. Unresolved setup is not a native unavailable/failed verdict.

| Consumer | Operation outcome | Ordered rows and facts | Mutation |
| --- | --- | --- | --- |
| Selection checks | Existing operational `success=true`, `run_status=incomplete`, error `configuration_choice_required`; affected binding_ids in details | Applicable unresolved rows: `not_executed/configuration_choice_required`. Other applicable rows: `not_executed/not_started`. Prefiltered rows remain `not_executed/not_applicable` | No adapter/process invocation |
| Tests | Existing operational `success=true`, same error/details, selected_tests retained | Selected unresolved rows: `not_executed/configuration_choice_required`; selected acknowledged rows: `not_executed/not_started` | No collection/test invocation |
| Fixes | Existing operational `success=true`, same error/details, selected_fixes retained | Selected unresolved rows: `not_executed/configuration_choice_required`; selected acknowledged rows: `not_executed/not_started` | No fix invocation or partial fix effects |
| Scaffold, enforce or report | `success=false`, `written=false`, `validation_status=not_executed`, same error/details | Unresolved content rows use the same refusal reason; remaining obligations are not_started | No validation scratch allocation and no artifact creation |
| Edit, enforce | `success=false`, `written=false`, `content_changed=null`, `validation_status=not_executed`, same error/details | Same content rows; original read/profile selection may already have occurred | No validation scratch allocation and no target replacement |
| Edit, report | Completed guarded write: `success=true`, `written=true`, factual `content_changed`, `validation_status=not_executed`, no operation error/details | Preserve unresolved/not_started rows and absent native facts; the full batch remains unattempted | No validation scratch allocation or adapter execution; target replacement is allowed. File/persistence failures retain their own error and check rows. |
| Commit artifact preflight (`scaffold_artifact`, commit package) | Same scaffold refusal, `success=false`, `written=false`, `validation_status=not_executed`, same error/details | Same content obligations through the package's existing commit_preflight profile | No commit artifact created. This path does not stage/commit; direct git_add_or_commit currently has no content-check dependency and is not given a new one in this issue. |

Every unattempted row has absent adapter identity/capture, native tool versions, evidence, request rejection and termination facts. Keep actual effective_args/args_source where selection has resolved them. Refused-row messages are null; explanation/recovery is configured from the operation code and affected binding IDs. Ordinary not_started diagnostics retain their existing contract.

Owner revision, 2026-10-13: scaffold and edit-enforce block this *not executed* result. Edit-report may continue to its guarded write specifically after configuration_choice_required, retaining the unexecuted check rows without claiming validation. Both edit policies still block invalid requests, interruption and unconfirmed termination. Original-file/persistence checks remain mandatory. Empty branch/all-prefiltered selections remain neutral. Complete applicable admission still precedes every adapter invocation, content scratch allocation and fix effect; the unresolved content batch is not partly executed. The edit output contract admits this specific report state, including retained check facts when a later file/persistence error prevents the write. Presentation of absent validation comes from configuration.

Author the human explanation and recovery action in presentation.yaml using the existing generic presenter. Generic execution owns the fact; no message is hardcoded in an adapter, command or new presenter branch. Recovery tells the agent/owner to configure the relevant binding deliberately, not to fabricate a native config file.

### Existing maintenance and ownership

Retain the Research G004/BLE001/SLF001 inventory and owner-approved dispositions. The 2026-10-13 exception-ownership decision supersedes preservation of bespoke catch-to-tool-failure DTOs at the seventeen identified sites. Ordinary exceptions reach the existing wrapper; commit cleanup re-raises the primary exception with secondary diagnosis. Preserve successful operation outputs, factual negative outcomes and domain semantics. Native settings remain owner-authored; adapter metadata/pins are unchanged.

The existing ConfigErrorOutput and ExecutionErrorOutput carry optional error_code; ToolErrorOutput carries error_params separately from existing request params. Traceback includes the original exception chain and cleanup notes. The shared capture in existing core error handling has no presentation or tool/domain-specific dispatch. Existing generic presentation selects configured domain failures or its default exception text, rather than projecting an exception through a normal tool-result template.

PlanningMutationError uses the existing MCPError hierarchy and code/params. Save/update manager commands return the persisted StoredPlanningModel after readback; post-write failure raises planning_readback_failed with persisted=true and the original cause. Tools only project successful returned plans. The standalone PolicyDecision preserves allowed=false on evaluation error and retains the captured diagnosis.

RenewalResult retains its factual outcome and adds the existing typed error diagnostic, including subtype fields. RenewalPresenter owns text projection of results and direct CLI errors. Initialization preserves nonzero outcome exitcodes and facts; only a missing result is an internal exception. Terminal CLI catches retain complete diagnosis and exit1. No new wrapper class, presenter class, registry, adapter protocol or configuration resolver is added.

The remaining fallback boundaries preserve their existing output contracts. Scratch
rollback adds the full secondary traceback to original exception notes without
replacing primary failure/cancellation. Presentation/cache catches retain complete
secondary diagnosis through existing logging while keeping tool outcomes, schema
attachments and JSON fallbacks available; no new DTO or presenter pipeline is added.
The owner-approved unused label-sync method/helper and their ten exclusive tests are
removed from the configuration model. Metadata validation, lookups and conversion remain.

### Owner-retained fallback and portability repair boundary — 2026-10-14

StatusResource receives the existing read-only IGitContextReader and IStateReader interfaces. Bootstrap supplies the existing Git manager and a BranchValidatedStateReader around the existing repository. The resource reads current_phase from the matching persisted state; missing/mismatched state remains an error. There is no branch-name phase policy or new state contract.

ConfigLoader accepts config_root and the active keyword-only context_schema_reader; its unused template_root argument/attribute and incidental Settings reload are removed. Remove the unused production resolve_config_root helper and bootstrap _build_config_layer method plus their exclusive helper tests. Existing optional-root callers need no new argument; explicit unused arguments are mechanically removed. ServerSettings owns the default template_suite root; startup and renewal use that property while preserving intentional legacy-suite migration. No root probing or compatibility shim is added.

Correct existing active identity examples, machine-local source links and the stale S1mpleTrader reboot instruction. Preserve product provenance. The owner explicitly postpones any new release, version bump, package build, tagging or publication. Parent/head registration and manifest/content design remain deferred in [the scope record](deferred.md).

## Test Design

Adapt existing public configuration/execution tests with a small parametrized set across check/test/fix/content routes: unresolved setup refuses with zero invocations/side effects, all admitted choices retain native args/args_source, caller args cannot acknowledge an unresolved binding, and empty/not-applicable branch selection remains neutral. Verify scaffold and edit-enforce setup refusal, edit-report guarded writes with truthful unexecuted-check facts, and preserved original-file/persistence blockers. Use existing native-lint/CLI/setup behavior tests for repairs; avoid testing literal YAML/doc text. Reuse fresh evidence and keep the required full configured suite in Validation.

## Related Documents

- [Approved Research](<research.md>)
- [Architecture Principles](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)
- [Execution contract](<../../reference/execution-adapters.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-12 | @imp designer | Define bounded binding choice, truthful refusal and native-behavior preservation under the approved Chore strategy. |
| 0.2 | 2026-10-12 | @imp researcher | Resolve fresh-init ownership without asset builders; define consumer refusal rows, absent native facts and both content policies before implementation. |
| 0.3 | 2026-10-13 | @imp implementer | Specify approved exception ownership using existing wrapper/error DTOs and renewal presenter; preserve domain and post-write diagnosis without a new architecture. |
| 0.4 | 2026-10-13 | @imp implementer | Keep scratch and fallback diagnostics in existing boundaries; record approved unused label-sync and test cleanup. |
| 0.5 | 2026-10-13 | @imp implementer | Define approved safe-edit report continuation for unresolved setup, preserving validation facts and all write guards. |
| 0.6 | 2026-10-14 | @imp implementer | Bound retained state/config fallback and document-portability repairs to existing contracts; explicitly postpone release and preserve parent/head/manifest deferrals. |
