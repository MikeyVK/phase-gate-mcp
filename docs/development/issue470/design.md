<!-- pgmcp:v1 id=design pv=1.0.0 pf=YApsrGTQgBUKFez2 sf=zJbLuUrs_I33kpX4 -->

# Issue 470 — One LF safe-edit proposal

**Status:** Design complete; independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-11

## Purpose

Define the smallest clean cutover within the existing edit service.

## Prerequisites

- Research v1.0 Approved Strategy; independent Research→Design GO on 6e6e05ce.

## Problem Statement

Intermediate logical/physical representations and terminator reconstruction produce inconsistent change facts. The owner approved one LF output policy, retaining check/write identity and byte-based race protection.

## Functional Requirements

- All four operations produce LF text before checks, including rewrite and no-match.
- Literal target_content, anchors and non-regex patterns use LF matching; regex syntax retains native Python meaning.
- content_changed compares final UTF-8 proposal bytes with original bytes only after completed replacement.
- Preserve operation cardinality, source-profile selection, append separators, enforce/report, locks and factual failures.

## Nonfunctional Requirements

- One original file read; no second read for reporting.
- No new modes, config flags, public fields, adapters or persistence abstractions.
- Cut over internal consumers without aliases; shrink preservation-only coverage.

## Options

### 1. Single text value in existing pure construction

Keep operation dispatch and patch application; return one LF string used directly by service.

**Pros:**

- Removes proposal duality and source reconstruction
- Reuses existing injection and safety boundaries

**Cons:**

- First successful edit can normalize the full file

### 2. Retain a one-field proposal object

Wrap the same string after deleting preservation machinery.

**Pros:**

- Smaller initial signature migration

**Cons:**

- No remaining responsibility beyond wrapping a string

### 3. New edit-plan/configuration architecture

Generalize representation and per-file policy.

**Pros:**

**Cons:**

- Unneeded structure and modes; conflicts with bounded clean break

## Decision

Use one LF string returned by construct_edit. Remove EditProposal and construct_edit_proposal rather than retaining a wrapper or alias.

## Rationale

The current construction route is already pure and injected. The writer and adapters need the final content, not operation intent. One string eliminates the opportunity for divergent check/write/report representations.

## Production Design

| Owner | Contract |
|---|---|
| OriginalFileSnapshot | Frozen original_bytes: bytes and original_text: str (universal LF view), both from one byte read. Remove original_source_text. |
| construct_edit(original: str, operation: EditOperation) -> str | Sole pure construction API. Interpret original and literal operands as LF text; retain operation dispatch/cardinality; normalize final emitted text to LF. No IO/profile/persistence. |
| EditOperation constructor | construct: Callable[[str, EditCommand], str]. Pass snapshot.original_text and retain the returned string. |
| EditOperation execute | Select from original, check final string, pass the same string to writer with snapshot.original_bytes guard. On completed write compare its UTF-8 encoding to snapshot.original_bytes. |
| OriginalFileReader | Retain single byte read and existing UTF-8/universal-newline decoding failure behavior; remove unused extra source decoding. |
| CheckedFileWriter | Unchanged verbatim UTF-8 persistence and exact-original-byte guard. |
| bootstrap and two integration compositions | Inject construct_edit directly, with no fallback/alias. |
| Public tool/output schema | Shape unchanged; explain LF input/output policy and byte meaning through schema descriptions and active reference. |

Normalization changes only CRLF and CR into LF. It does not alter Unicode characters, BOM, whitespace or final-newline policy. Append operates on normalized content/anchor before its existing separator logic. Replace normalizes target_content; literal pattern_replace normalizes pattern. Regex pattern/replacement syntax is not rewritten: native matching/expansion runs against the LF source, and emitted text is normalized afterward. Therefore a regex escape for CRLF does not match an LF-normalized source; callers match \n for line endings. Missing match/anchor and malformed regex retain existing typed outcomes.

## Test Design

Adapt the existing pure operation cases to LF expectations and add literal-operand normalization through those cases, without expanding the case count. Replace the existing preservation integration matrix with at most eight named behavior cases: replace/window with literal CRLF input; append from mixed input; rewrite with CR output; literal-pattern newline matching; regex expansion producing CRLF; no-match normalization; LF identity; anchored append. Assert real persisted bytes, actual changed fact, and exact check-input bytes. Keep unit regex backreference/zero-width/error coverage, policy blocked/write matrix, public DTO transport, original-byte race, single-read and writer failures. Do not duplicate those safety tests or add new files. The existing policy test's CRLF→LF rewrite must now report changed=true. Mechanical composition imports in Markdown integration cut over; public operation coverage is reused.

## Flow

```mermaid
flowchart LR
  A[One original byte snapshot] --> B[Pure LF edit construction]
  B --> C[Checks on final text]
  C --> D[Guard original bytes and write same text]
  D --> E[Completed write and proposed byte difference]
```

## State and Failures

No workflow/state changes. A completed check can remain passed when race or persistence blocks writing. No completed replacement means written=false/content_changed=null; completed same bytes means true/false; different bytes means true/true. Checks are not skipped for no-op proposals. Existing report semantics and cleanup outcomes remain.

## Preservation

Preserve original-byte comparison, exact check/write text identity, profile selection from original, frozen models, constructor injection and operation cardinality. Supersede only source terminator preservation, exact non-LF rewrite and logical-only content_changed.

## Transition and Cleanup

One internal cutover removes source terminator mapping/preferred-terminator selection, physical-text dispatch, unchanged-logical preservation shortcut, dual proposal, wrapper function and unused snapshot field. Keep operation patches/dispatch as the current construction mechanism. No historical doc edits or Git/editor mutation.

## Validation

### LF and actual byte change across operations

**Method:** Existing focused construction/operation/public/Markdown tests

**Expected Result:** LF only; correct changed values; no preservation-only matrix growth.

### Safety and check/write identity

**Method:** Existing real reader/writer integration assertions, including race and write failures

**Expected Result:** Checked UTF-8 content equals persisted bytes; external byte changes block writes.

### Cleanup and typing

**Method:** Source consumer search and appropriate targeted format/lint/type gates

**Expected Result:** No old representation consumers/aliases; production type gates pass.

## Planning Consequences

One coherent implementation cycle is sufficient. Establish a focused green baseline, adapt existing behavior expectations, cut over and delete obsolete structure. No new old-policy regression coverage. Reserve the mandatory configured full suite and branch gates for Validation; reuse fresh evidence through Documentation/Ready.

## Sources

- [Research](<research.md>)
- [Construction](<../../../mcp_server/services/edit_construction.py>)
- [Operation](<../../../mcp_server/services/edit_operation.py>)
- [Existing integration coverage](<../../../tests/mcp_server/integration/test_edit_operation_v3.py>)
- [Checked-writer behavior](<../../../tests/mcp_server/integration/test_edit_operation_v3.py>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-11 | @imp designer | Define one LF construction value, direct consumer cutover and bounded test cleanup. |
