<!-- pgmcp:v1 id=design pv=1.0.0 pf=Uk1D2XWpiag1c6nn sf=WI5iXHBKVOU91bYE -->

# Issue \#530 — connect note rendering to existing policy

**Status:** Design complete — independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-20

## Purpose

Correct the evidenced missing dependencies in normal note rendering with the smallest existing-layer change.

## Scope In

TextPresenter.present_notes and direct behavior/persistence evidence.

## Scope Out

New configuration/defaults, note DTO/schema, producer conversions, cache/channel/envelope changes, compact recovery, error-framework changes, unused-helper cleanup and unrelated lifecycle tests.

## Problem Statement

The note route constructs SafeNoneFormatter without FormattingConfig or the selected tool's max_items. A genuine list value from planning-cycle evidence is therefore displayed as an internal formatter error after successful persistence.

## Functional Requirements

- Planning updates with supported list-valued evidence notes render readable information using existing configuration.
- Use the selected tool's existing max_items and global formatting for list/tuple order, separator, empty/None value and omission text; preserve source parameters.
- Keep independent stored-plan readback and all existing mutation/protection semantics intact.
- Missing limits and unsupported structured note values retain honest native diagnostics; a malformed note does not hide the normal operation result.

## Nonfunctional Requirements

- One existing presentation boundary; no per-tool branching or new helper/framework/constructor graph.
- Unchanged public interfaces, DTOs, schemas, channels and cache semantics under the approved #529/#528 contracts.
- Proportional public-behavior coverage and reuse of existing fixtures/tests; no durable prose snapshots or harness/version matrices.

## Options

### 1. Use existing policy at the note formatter boundary

The current TextPresenter already owns global formatting and selected tool config. Give its existing formatter the same inputs used for main text/instructions.

**Pros:**

- Removes causal dependency omission for global/local notes.
- No new policy or API.

**Cons:**

- Tools without a declared limit still cannot render sequence-valued notes; preserve their explicit native diagnosis.

### 2. Stringify planning evidence in its producer

Reject: masks one symptom, moves presentation into domain code and leaves other note consumers broken.

### 3. New note-specific settings or formatter abstraction

Reject: no demonstrated need beyond already available configuration; increases maintenance and policy surface.

## Decision

Connect the existing SafeNoneFormatter used by TextPresenter.present_notes to the current global FormattingConfig and the selected ToolPresentationConfig.max_items. Keep the formatter, templates, data and error boundary unchanged.

## Rationale

The isolated counterfactual proves these missing inputs are sufficient. Both are already available at the same presentation owner and already used by adjacent formatting paths.

## Production Design

TextPresenter remains the sole changed production component. Its existing selected tool config can serve both formatter construction and local-note lookup. FormattingConfig/ToolPresentationConfig stay under the existing loader; no second reader, source default or startup-inference rule. Dynamic note values are not statically typed in config, so unsupported runtime combinations retain the existing formatter diagnostic rather than introducing a blanket requirement for all 49 tools.

## Test Design

Reuse configured_workspace and existing factory/SDK helpers for one durable isolated planning append test in an existing integration surface: retain a full original-block snapshot, perform a real update, require readable evidence fields without the logged formatter failure, and query get_project_plan independently to compare original/appended identifiers/descriptions/criteria. Controlled read-only Git evidence/admission isolates external effects; existing domain/protection tests cover their unchanged behavior. At the public present_notes surface, use a small parametrization for global/local list/tuple ordering and configured bounds plus empty values. Preserve explicit diagnostics for a missing limit and nested values, reusing native formatter/syntax tests rather than copying their implementation. No fixed project-prose assertions and no permanent copy of the exploratory counterfactual probe.

## Contracts

### Unchanged public entrypoint

```python
def present_notes(self, tool_name: str, notes: list[NoteEntry]) -> str | None: ...
```
No signature or model addition. Empty/unmatched notes still produce no text; scalar notes remain renderable even without a sequence limit.

### Policy and resolution

- Resolve the current tool configuration consistently for the whole note render; its local template still has priority over the matching global template.
- Use global_config.formatting and that tool's max_items. If the tool/limit is absent, pass no invented limit; sequences remain unsupported in that context.
- SafeNoneFormatter remains the scalar-sequence authority: source order, configured separator/omission and none_value; no string repr, sorting or producer joining.
- Do not change group order/headings, template lookup, parameter lookup, missing-key behavior or public delivery selection.

## Flow

Real update persists its complete block → produces raw evidence Note → normal TextPresenter renders that note using existing policy → normal ResponsePresenter and SDK preserve the existing outcome/envelope. A separate get_project_plan call proves persistence independently of text.

## State and Failures

No state or IO is added to the presenter. A valid note renders; a missing sequence limit, nested collection or malformed template still follows the current logged native exception and visible formatting-error path. No catch is removed, new fallback invented, failure relabeled, or #528 compact recovery changed.

## Preservation

ProjectManager, Git evidence/protection, command/readback DTOs, source Note.params, main/instruction rendering and normal/compact public schema/channel/cache behavior remain unchanged. Existing scalar/None and malformed-template tests stay meaningful. The 21 tool entries without max_items are not globally assigned one.

## Validation

### Causal corrected behavior

**Method:** Durable SDK append/readback case fails on the current note-rendering defect before correction and passes afterward.

**Expected Result:** Operation remains successful, readable evidence includes supplied values, C_1 is intact and appended C_2/D_2.1 facts match inputs.

### Existing policy and honest failures

**Method:** Public note cases plus existing formatter/presenter cases with non-default policy values.

**Expected Result:** Configured order/bounds/omission/empty representation observed; source parameters unchanged; missing-limit/nested/malformed input remains diagnosable.

### Preservation

**Method:** Workflow-owned native full suite and configured/branch checks after focused implementation verification.

**Expected Result:** Required evidence passes without scope/deadline/quality relaxation. Planning assigns exact timing and targets.

## Planning Consequences

One coherent correction cycle is sufficient; bind meaningful public RED before the small production correction, use narrow affected-file evidence in Implementation and reserve native full-suite/branch checks for Validation. Documentation should clarify note policy only in the existing common presentation reference.

## Sources

- [Approved Research](<research.md>)
- [Note owner](<../../../mcp_server/presenters/text_presenter.py>)
- [Existing formatter](<../../../mcp_server/presenters/collection_text_renderer.py>)
- [Configuration models](<../../../mcp_server/config/schemas/presentation_config.py>)
- [Existing SDK surface](<../../../tests/mcp_server/integration/test_execution_presentation_v3.py>)
- [Reusable workspace fixture](<../../../tests/mcp_server/fixtures/suite_roots.py>)
- [Public presenter cases](<../../../tests/mcp_server/unit/test_presenter.py>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-20 | @imp designer | Specify the existing formatter-policy connection, unchanged boundaries and proportional behavior evidence. |
