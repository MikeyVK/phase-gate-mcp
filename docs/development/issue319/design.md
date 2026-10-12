<!-- pgmcp:v1 id=design pv=1.0.0 pf=Uk1D2XWpiag1c6nn sf=KoFPQ3-cAAWFeesb -->

# Issue 319 — bounded quality configuration choice

**Status:** DRAFT — INDEPENDENT REVIEW REQUIRED  
**Version:** 0.1  
**Last Updated:** 2026-10-12

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

Newly shipped default bindings declare null so an installer makes the choice. This repository's active bindings record the actually chosen policy: Ruff/Mypy/Pyright/Pytest/Commitlint native_discovery; Lychee and schema checks configured_arguments; Python/TypeScript syntax not_applicable. Metaschema's existing explicit native binding arguments remain configured_arguments; no external file is implied. These assignments are workspace data, not hardcoded tool-name branches.

Setup guide requires provisioning native pins, selecting workspace-native policy/arguments, setting every needed binding choice and performing a scoped check. No native config files are copied/merged automatically. Existing installations missing the field remain available for setup but affected execution requires acknowledgement. Release notes must say this explicitly; review compatibility implications before deciding final release publication.

### Invocation and refusal contract

Resolve the requested binding set and applicability with existing mechanisms. Before any applicable adapter/process or content scratch/fix mutation in the selected operation, reject unresolved choices and identify their binding IDs. For selection checks, do not reject a binding already prefiltered to not_applicable; preserve empty selections. In a mixed batch, unresolved applicable bindings prevent the batch from executing, so a fix batch cannot partly mutate before setup refusal.

The public check/test/fix output envelopes should carry one stable consumer-side configuration_choice_required code with the affected binding identities and factual no-invocation outcome. Extend their existing typed failure vocabulary only as needed; do not fabricate adapter versions, captures, native verdicts or evidence. This is a bounded additive refusal fact, not a native protocol change. Content preflight maps the same fact through existing validation outcomes: enforce prevents writing/scaffolding, report retains its established reporting/write semantics. The input policy validation flag itself is not redefined.

Author the human explanation and recovery action in presentation.yaml using the existing generic presenter. Generic execution owns the fact; no message is hardcoded in an adapter, command or new presenter branch. Recovery tells the agent/owner to configure the relevant binding deliberately, not to fabricate a native config file.

### Existing maintenance and ownership

Retain the Research G004/BLE001/SLF001 inventory and scoped repair dispositions. Preserve failure DTOs, primary errors/cleanup notes and public testing; remove proven orphan setup and test-only escape access. Native settings remain owner-authored; adapter metadata/pins are unchanged by the choice feature. No config resolution, package-copy flow or source-consumer catalogue is added.

## Test Design

Adapt existing public configuration/execution tests with a small parametrized set across check/test/fix/content routes: unresolved setup refuses with zero invocations/side effects, all admitted choices retain native args/args_source, caller args cannot acknowledge an unresolved binding, and empty/not-applicable branch selection remains neutral. Verify content enforce/report retain their existing write policy when validation refuses. Use existing native-lint/CLI/setup behavior tests for repairs; avoid testing literal YAML/doc text. Reuse fresh evidence and keep the required full configured suite in Validation.

## Related Documents

- [Approved Research](<research.md>)
- [Architecture Principles](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)
- [Execution contract](<../../reference/execution-adapters.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-12 | @imp designer | Define bounded binding choice, truthful refusal and native-behavior preservation under the approved Chore strategy. |
