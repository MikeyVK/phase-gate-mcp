<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue \#537 — Research outcome for simplified response delivery

**Status:** Research outcome — independent review requested  
**Version:** 0.1  
**Last Updated:** 2026-10-20

## Purpose

Adopt the owner-approved inherited analysis as the current Research outcome of #537, without repeating the client investigation.

## Scope In

The initialized refactor/537-simplify-response-delivery branch, parent main, and normal presentation/configuration/transport contracts identified by the inherited analysis.

## Scope Out

Implementation, new client probes, runtime/configuration switching, dependency migration, cache expansion, release publication, changes to #536 history or its parked owner work.

## Problem Statement

The previously approved #529 profile matrix is implemented correctly but exceeds the owner's revised need. #537 owns the clean contract change to bounded text plus structured/resource data delivery and independent attachments. Import commit 9915c2f315d448e0fd7417436917349b88c2559d preserves the inherited research; this artifact makes the Research outcome current for #537 instead of treating the import alone as phase completion.

## Goals

- Adopt the inherited evidence and explicit owner strategy per affected boundary.
- Identify stable operation/cache/recovery ownership and the actual presentation seams.
- Leave concrete interfaces and defaults for Design, with no further harness campaign.

## Findings

| Current responsibility / coupling | Evidence and consequence |
|---|---|
| Settings selects a profile; bootstrap composes one presenter from shared config | [Settings](../../../../mcp_server/config/settings.py), [config models](../../../../mcp_server/config/schemas/presentation_config.py), [bootstrap](../../../../mcp_server/bootstrap.py). Change only the selected presentation/config contract; no workflow or tool-domain coupling is needed. |
| ResponsePresenter routes presentation/data, publishes its schema and appends text JSON in text-data modes | [ResponsePresenter](../../../../mcp_server/presenters/response_presenter.py). Existing seam owns the simplified projection; server remains a transport boundary. |
| Core/details limiter deliberately permits protected-core overrun | [TextBudgetLimiter](../../../../mcp_server/presenters/text_budget_limiter.py). A final byte ceiling is a deliberate behavior change, not an incidental formatting repair. |
| Server caches operation only; resources format independently owned schema attachments | [server](../../../../mcp_server/server.py), [cache reader](../../../../mcp_server/resources/cache.py), [attachment formatter](../../../../mcp_server/presenters/schema_resource_presenter.py). Preserve ownership; restore separate embedded-resource transfer rather than expanding the cache. |
| Existing helper/config tests encode the old matrix | The inherited 14-file test/helper index remains navigation. [Presentation integration](../../../../tests/mcp_server/integration/test_execution_presentation_v3.py), [attachment transport](../../../../tests/mcp_server/integration/test_tool_attachment_transport.py) and existing config/limiter unit cases are the primary behavior seams. Adapt valuable cases and shared construction; remove obsolete matrix expectations. |

The inherited historical explanation and #536 chore statements describe their original context and remain unchanged. #537 is already registered as refactor with Research active. This is a selected public-contract simplification; internal operation behavior is preserved.

Reviewed source baseline: 9915c2f315d448e0fd7417436917349b88c2559d, confirmed by current get_work_context, get_project_plan(537), full get_issue(537), targeted repository reads and read-only history inspection. Independent QA on that baseline found one P2: a missing #537 Research outcome. Its source review found no new policy blocker. This document addresses that omission; it does not confer its own GO.

## Questions

- Design chooses the configuration/environment key and explicit default, without reopening the agreed two named modes.
- Design specifies independent attachment carrier/reference and structured schema forms, full structured presentation versus the bounded inline projection, final limiter/footer feasibility and normal compact recovery.
- Any materially changed startup exception or diagnostic-loss promise requires an explicit owner decision; there is no known unresolved strategy decision now.

## Approved Strategy

The owner-approved decisions in inherited v0.2 and issue #537 apply to this branch:

| Boundary | Approved strategy |
|---|---|
| Normal text | Always finally UTF-8-bounded inline text including route footer, truncation notice and fence closure; no full JSON dump. Instruction truncation is noted, not a separate defect, test package or blocker. |
| Config / process selection | Clean break from arbitrary profiles to two named modes, structured and resource. Keep existing defaults/override/launcher composition and per-instance selection against one workspace. No aliases, boolean or harness detection. |
| Structured transport | Full operation facts plus explanatory/instructional presentation and references to supplied separate attachments; matching outputSchema. Distinguish full structured presentation from truncated inline text in Design. |
| Resource transport | Existing operation cache/pagination supplements text; usable locator only on successful publication. No normal structuredContent/outputSchema and no rendered-text cache copy. |
| Attachments | Always separate native embedded-resource content blocks in both modes. References in text and structured presentation, no second structured body copy. Preserve producer/formatter ownership and existing operation-owned schema fields. Attachment identity does not imply an independently registered readable URI. |
| Outcome / errors / recovery | Preserve operation semantics, isError, primary diagnostic and existing exception/presenter boundaries. Normal compact recovery does not replay, republish or retry an operation/failed renderer. Retain the existing configuration-independent startup recovery exception. Reopen owner policy only for a genuine contradiction or change to that exception or loss/completeness rules. |
| Tests / documentation | Adapt focused behavior evidence and directly invalidated consumers; no compatibility suite, client/dependency matrix, prose/source snapshots or speculative regression expansion. Update only current affected references during Documentation. |

The owner explicitly authorized autonomous execution through independent phase gates to Ready. Independent QA remains the progression authority; no phase is skipped. Main merge and subsequent integration into the preserved #536 branch remain Coordination responsibilities.

## Expected Results

Normal text respects its configured final byte allowance; structured mode carries complete operation/presentation and resource mode offers real readback without structured output; both preserve separate attachments/references. Config/schema/instance behavior and failure truth are supported by existing focused behavior cases and the required later Validation. #537 reaches its own reviewed lifecycle/PR; #536 stays open for live acceptance and release.

## Evidence

### Historical import is reused, not rewritten

Imported research on 9915 is byte-identical to the owner's v0.2 from ac376396; QA independently confirmed the same Git blob. Its original metadata and historical #536 context remain intact.

- [Inherited analysis and source index](<../../issue536/response-delivery-research.md>)

### Research proof is source/decision evidence

Current context and full issue were read; direct production, config and focused test seams were inspected. No implementation test, full suite, runtime restart or active output selection was performed during Research.

- [Issue acceptance and exclusions](<https://github.com/MikeyVK/phase-gate-mcp/issues/537>)

## Risks

### A final limiter can cut instructional text.

Owner explicitly records this as noted; retain honest truncation/route notices without inventing a new instruction-cache requirement.

### Dynamic footer/reference size or error details can exceed a small budget.

Design validates feasible configured bounds and limits the normal text projection; preserve truthful route/failure facts and the separately approved startup exception.

### A new projection may drop independently supplied attachments or invent resource access.

Keep separate native embedded-resource transport and references in both modes; use existing independent-attachment and SDK boundaries for proof.

### Shared test fixtures may magnify a small configuration change.

Use the inherited consumer index and one existing presenter factory; limit fixture/assertion edits to invalidated contracts rather than rewriting the suite.

## Related Documents

- [Inherited Research v0.2 (preserved provenance)](<../../issue536/response-delivery-research.md>)
- [Issue #537](<https://github.com/MikeyVK/phase-gate-mcp/issues/537>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-20 | @imp researcher | Adopt inherited owner-approved research for #537 and address QA's exact Research-outcome omission without repeating investigation. |
