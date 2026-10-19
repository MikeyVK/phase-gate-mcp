<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue \#524 — Truthful cache-failure availability notices

**Status:** Research completed; independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-19

## Purpose

Establish the cache-notice defect and a narrow wording-only correction boundary under the current output contract.

## Problem Statement

The shipped truncation notice equates failed cache publication with unavailable complete result data, although MCPServer still serializes the operation DTO into structuredContent. A related cache-failure notice promises full inline details before a text-only limiter and traceback exclusion. Both statements exceed the known presentation facts.

## Goals

- Identify observed versus expected availability statements and their causal paths.
- Bound the repair to truthful cache/text notices, preserving operation results and independent channels.
- Reuse behavior evidence without wording snapshots, compatibility bridges or a cache/schema redesign.

## Findings

### Causal evidence

| Condition | Current observed source behavior | Expected boundary |
|---|---|---|
| Cache succeeds | TextPresenter emits a real cache URI; large cache payloads receive paging guidance. | Keep this access route and text ceiling intact. |
| Cache fails, short text | global.next_instruction_texts.cache_publication_failed says “Full details dumped inline”. TextPresenter appends an operation JSON fallback, excluding traceback. | Cache failure must be visible; do not promise complete inline evidence. |
| Cache fails, long text | TextBudgetLimiter reserves cache_unavailable_truncation_notice: “complete details are unavailable because cache publication failed”. | State text truncation and unavailable cached access, not missing operation data or client access guarantees. |
| Normal operation returned | MCPServer serializes the actual operation separately as structuredContent after presentation, independent of cache success. | Preserve operation outcome, all structured fields and diagnostics. |
| No operation / unknown tool / processing failure | Existing explicit text-only error path, no structured operation response. | Do not add a universal structured-data promise to fallback errors. |

Sources: [shipped presentation config](../../../.pgmcp/config/defaults/presentation.yaml), [TextPresenter](../../../mcp_server/presenters/text_presenter.py), [TextBudgetLimiter](../../../mcp_server/presenters/text_budget_limiter.py), [MCPServer](../../../mcp_server/server.py).

The root cause is an availability assertion authored for the older text/cache relationship and retained after #517 restored actual operation structuredContent. The limiter correctly limits only text and chooses a no-cache tail; operation serialization is independent. There is also an existing hardcoded fallback for an absent cache_publication_failed configuration key with the same full-inline promise. Its ownership and minimal correction must be considered in Design; no new presenter routing or tool-specific logic is justified.

### Reproduction and negative controls

The source path is decisive without another large diagnostic dump: publish CachePublication(success=False, run_id=None), present an operation whose fallback exceeds 8,000 UTF-8 bytes, then invoke it through MCPServer/connected_mcp_client. The reserved notice claims complete data unavailability while structured_content is the operation model_dump(mode="json", by_alias=True). With a small fallback, the ordinary failure warning is used instead. Successful publication is the control for a usable cache URI. Existing processing-failure and unknown-tool cases are the controls for absent structured data.

[Existing shipped-cache guidance cases](../../../tests/mcp_server/integration/test_execution_presentation_v3.py) already use the real config, presenter, cache and SDK fixture. They cover small/large cached operations but not failed publication at the same transport boundary. [Attachment transport cases](../../../tests/mcp_server/integration/test_tool_attachment_transport.py) prove real success/domain-error DTO delivery and explicit no-structured-data processing/unknown-tool failures. [Presenter unit cases](../../../tests/mcp_server/unit/test_presenter.py) assert the old hardcoded inline wording; preserve their behavioral value without maintaining prose snapshots. [Budget tests](../../../tests/mcp_server/unit/presenters/test_text_budget_limiter.py) prove selection/reservation using injected marker notices.

### Proportional blast radius

| Surface | Impact / exclusion |
|---|---|
| Default presentation config and existing generic fallback | Incorrect factual notice values; no new config-source or schema contract needed merely to correct claims. |
| Presenter/limiter/server mechanics | Trace the existing generic path; avoid expanding responsibilities or copying operation facts. Existing fallback JSON/truncation/traceback policy remains outside behavioral redesign. |
| Tests/helpers | Adapt valuable shipped-config transport evidence and affected presenter assertions; retain no-operation and limiter controls. No new framework, broad fixture rewrite or wording/content tests. |
| Active documentation | Presentation architecture cache-failure paragraph is the direct explanatory consumer; clarify cached access versus whole-result availability and client uncertainty. |
| AGENTS, workflow/enforcement, template suite | No policy/instruction/template change needed. |
| External clients / wire DTO / cache reads | No changed shape, channel, URI, success flag, retention, pagination or compatibility behavior. |

### Related decisions and limits

[#523 Research](../issue523/research.md) and [Validation](../issue523/validation.md) establish that text size is not total response size, overlapping projections do not imply duplicated ownership, and actual client/model access is not a universal server guarantee. The 2,996-test #523 result is baseline evidence, not proof this defect is repaired.

Do not reopen #462 conditional cache references or #523 metadata/client-policy questions. No schema forwarding, client routing, output-policy redesign, dependency/client matrix or release is included.

## Approved Strategy

The owner's standing autonomous correction request and clean-break instruction authorize the bounded defect repair below; no new output policy is selected. Inherited #517/#523 boundary decisions remain binding.

| Boundary | Approved strategy and rationale |
|---|---|
| Availability wording | Correct the factual scope of existing cache/text notices. A cache failure can only establish cached access failure; text truncation establishes a text projection limit. Avoid both missing-complete-data claims and client/model access promises. |
| Operation / public output | Preserve actual DTO structuredContent, original success/error outcomes and diagnostics; no compatibility facade or DTO migration. |
| Cache / text mechanics | Preserve publication visibility, no fabricated usable cache URI, current text ceiling, inline fallback and traceback exclusion. No cache redesign or conditional-link proposal. |
| Presentation ownership | Use existing generic presentation/configuration responsibility; no tool-name cases, new cross-layer dependency, or new error framework. Concrete wording/fallback decisions belong to Design within this boundary. |
| Tests | Adapt durable existing behavior cases for failed/successful publication, both text-size conditions and no-operation controls. No exact-prose snapshots, legacy-behavior cases or version matrix; keep test growth proportional. |
| Workflow | Independent QA at every phase boundary. Focused implementation checks; one native-configured full suite and branch/configured gates in Validation as the Bug contract requires. |

Stop for owner direction only if correction would require a new delivery/compatibility policy or larger responsibility change.

## Expected Results

Cache-failure and truncation remain visible without false complete-data or client-access assertions; actual structured operation and diagnostics remain unchanged. Durable behavior evidence covers publication failure with/without truncation, successful publication and no-operation errors.

## Related Documents

- [Issue #524](<https://github.com/MikeyVK/phase-gate-mcp/issues/524>)
- [Presentation architecture](<../../reference/presentation_architecture.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-19 | @imp researcher | Evidence cache/text notice inconsistency and bound a compatibility-neutral correction. |
