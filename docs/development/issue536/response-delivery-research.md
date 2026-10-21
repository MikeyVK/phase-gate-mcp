<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Response delivery simplification — issue \#536

**Status:** Owner-approved direction; impact analysis for discussion  
**Version:** 0.2  
**Last Updated:** 2026-10-20

## Purpose

Record the owner's simplified delivery direction and its focused change surface before design or implementation.

## Scope In

Normal response selection, bounded inline presentation, structured delivery, cache references, attachment reachability, existing error boundaries, and directly affected configuration/tests/documentation.

## Scope Out

Production implementation, active profile changes/restarts, cache duplication of rendered instructions, a new cache framework, client-specific branches, additional harness probes, dependency changes, release execution, and the other paused #536 work packages.

## Problem Statement

Live acceptance exposed that the three independent #529 profile controls allow configurations that are unnecessary for the owner's intended usage. In particular, text_inline appends full operation JSON after the presentation allowance. The owner approves a simpler contract: always bounded readable inline text and exactly one selected supplementary route, structured content or resource cache, with a corresponding footer. This document captures that direction and a source-based impact analysis; it does not claim implementation or complete the overall #536 Research.

## Goals

- Keep one bounded inline-text entry point for every normal tool response, without a full operation JSON dump in that text.
- Select structured or resource delivery locally to each server instance, including different harnesses sharing one workspace.
- Retain actual operation outcomes, useful diagnostics and attachment accessibility at the existing boundaries.
- Remove unnecessary profile combinations rather than introducing more toggles, client knowledge or compatibility machinery.

## Background

Before #529, TextPresenter built the rendered message, instructions and notes, appended an available cache reference, then applied one final 8,000-UTF-8-byte ceiling. Overflow reserved a complete locator and truthful truncation tail, with UTF-8-safe boundaries and Markdown-fence closure. The locator was shown whenever a usable run ID existed, even when inline information was sufficient; only pagination advice depended on the 6,000-character threshold. #462's conditional-reference optimization was closed without implementation. Since #517, complete structured operation data was also sent independently; the text ceiling never bounded structured content, attachments or total wire size. #529 changed the limiter to protect the entire rendered core even above the allowance and introduced independently selectable presentation/data/delivery controls. The current code follows that historical approved design; this is an explicitly revised owner direction.

## Findings

### Approved normal delivery behavior

| Part | Structured route | Resource route |
|---|---|---|
| Inline content | Always readable text, finally bounded by the configured UTF-8 allowance | Same |
| Footer | Configured notice that the full result is in structured content | Configured locator for a successfully published cached operation; pagination advice when applicable |
| structuredContent | Complete operation plus the inline explanation/instructions and references to the separate attachments; no separate copy of attachment bodies | Absent |
| Available attachments | Always add as separate MCP embedded-resource content blocks | Same |
| Attachment references | Name the supplied attachments in inline text and repeat those references in structured presentation | Name the supplied attachments in inline text |
| Full operation JSON in text | Never | Never |
| Rendered text duplicated in cache | Not required | Not required |
| Underlying cache publication | May remain as existing infrastructure behavior | Required for a truthful normal cache locator |

The normal footer is consistent, not conditioned on whether the presenter believes its text is sufficient. Structured content must carry the explanatory/instructional presentation because some observed clients choose that channel instead of separate text. Resource delivery supplements inline text; it does not need to be a second self-contained copy of that text. Attachment delivery is independent of the selected operation-data route. An attachment URI identifies the supplied embedded resource; it does not promise that read_resource can fetch that URI. A response-size cap for all channels or all clients is not promised.

### Focused production/configuration impact

| Boundary / source | Current behavior | Required change or bounded design question |
|---|---|---|
| [presentation config models](../../../mcp_server/config/schemas/presentation_config.py) and [shipped defaults](../../../.pgmcp/config/defaults/presentation.yaml) | ResponseProfileConfig, ResolvedResponseProfile, a profile dictionary, a default profile ID, three independent routing fields and per-profile budget overrides | Replace the routing matrix with one explicit two-way selection. Keep shared budgets and text templates in existing presentation configuration. Add structured-footer and generic attachment-reference wording and align truncation notices with the actual supplementary route; do not claim cached details in structured mode. |
| [Settings](../../../mcp_server/config/settings.py) and [bootstrap](../../../mcp_server/bootstrap.py) | PGMCP_RESPONSE_PROFILE / ServerSettings.response_profile resolve an arbitrary shared profile ID per process | Retain process-local selection and existing defaults/override/launch composition, but accept only the selected two-way contract. The owner selects two named values, structured and resource, rather than a boolean or arbitrary profiles. The exact configuration/environment key and explicit default remain Design details. No shared workflow state or harness detection. |
| [ResponsePresenter](../../../mcp_server/presenters/response_presenter.py) | Independent channel branches; unconditional normal cache guidance when publication succeeds; full JSON appended whenever data_channel=text | Always emit bounded text. Emit structured content only for the structured route, including its presentation. Resource route emits a plain configured locator, not an additional JSON text envelope. Return available attachments separately in both modes and include their references in the shared presentation. Remove obsolete routing branches, preserving actual success/isError and existing error ownership. |
| [TextBudgetLimiter](../../../mcp_server/presenters/text_budget_limiter.py), [TextPresenter](../../../mcp_server/presenters/text_presenter.py) | Protected core can exceed the budget; only optional details are cut | Restore a final normal-text ceiling, accounting for the route footer/truncation notice before admitting the readable prefix. Reuse UTF-8/fence handling. Whether the internal core/details carrier remains useful is a small design choice, not a reason to rewrite rendering. Minimum feasible budget must be validated rather than silently overrun. |
| [Presentation DTOs](../../../mcp_server/schemas/presentation_output.py) and [presenter interfaces](../../../mcp_server/core/interfaces/ipresenter.py) | Optional text and independently nullable public projections support the profile matrix | Simplify only transport/projection contracts that become unnecessary. Keep operation DTOs. Restore a separate attachment carrier on PresentedOutput and change/remove the public structured attachment-body projection in favor of references; do not copy attachment bodies into a second transport field. The existing IResourcePresenter contract already supplies the formatted attachment facts and need not be expanded solely for routing. Structured presentation versus inline truncation is specified explicitly in Design; full operation delivery must not depend on parsing text. |
| [server catalog and delivery](../../../mcp_server/server.py) / ResponsePresenter.output_schema | Catalog gets selected schema from presenter; server transfers PresentedOutput | Structured mode advertises a matching outputSchema; resource-only normal mode omits both structuredContent and that schema. Transfer the separate presented attachments into native MCP embedded-resource content blocks in both modes, reusing the pre-#529 transport pattern. Reuse the current catalog/presenter boundary; no tool-specific schema registry or second presenter in the server. Reconnection/catalog refresh remains necessary after a selection change. |
| [operation cache](../../../mcp_server/state/response_cache.py) and [reader](../../../mcp_server/resources/cache.py) | Server publishes only the operation before presentation; readers return the whole JSON or explicit windows | Reuse as-is for operation data and pagination. No reason to cache rendered inline text. Cache availability is independent of the operation outcome; unavailable publication cannot produce a usable-looking URI. |
| [attachment formatter](../../../mcp_server/presenters/schema_resource_presenter.py) / server transport | Attachment representations currently live in the structured envelope or the appended text JSON | Keep SchemaResourcePresenter's identity/MIME/body formatting and attachment producers. Always transfer available attachments as separate native MCP embedded-resource content blocks, independently of structured/resource mode. Publish references in the inline explanation and, in structured mode, its presentation. Do not expand the operation cache or duplicate the body into structured attachment fields. A schema:// identity alone is not proof of a registered readable resource. |
| Existing normal recovery and [startup recovery](../../../mcp_server/presenters/startup_recovery_presenter.py) | Normal recovery uses selected profile; startup recovery deliberately bypasses unreliable presentation configuration and publishes fixed dual-channel diagnosis | Adapt normal recovery selection and bounding without replaying a crashed renderer or full payload. Preserve existing known-outcome/error distinctions. The previously approved configuration-independent startup exception is not silently removed by a normal-mode simplification. Any change to its policy or loss/completeness rules requires an explicit owner decision. |

### Attachment facts, not a reason for wholesale cache expansion

Production attachment producers are TemplateSchemaTool, ScaffoldArtifactTool's context-invalid result and the input-validation decorator. TemplateSchemaTool also carries the schema in operation.schema_data; input-validation failures carry it in operation.input_schema. ScaffoldArtifactTool adds the selected context schema as an independent attachment on context_invalid; do not assume all attachment facts already occur in every operation DTO. Tests also deliberately exercise independent attachment content.

The owner now approves the same independent attachment route for both modes: always retain available attachments as separate MCP embedded-resource content blocks and refer to them in the inline presentation. Structured presentation repeats those references; it does not introduce another copy of the attachment body. Existing schema fields already owned by an operation DTO remain intact; this change does not strip or reconstruct operation facts.

Historical source confirms that before #529, MCPServer appended each presented resource after the text block, with its uri, mimeType and text. Historical wording did not universally name every attachment: scaffold_schema's template merely announced retrieval. Make the references consistent through existing presentation configuration; do not claim that the old wording already guaranteed them.

#529 does not prove every client's access to separate attachments when that client selects structured content. This is an evidence limitation, not an observed defect or an instruction to start another harness campaign. References must identify actual supplied attachments and must not invent an independently readable schema URI. No cache expansion or extra attachment-reader architecture is required by the accepted direction.

### Test and documentation impact

The source-reference inventory identifies 14 existing test/helper files, not 14 mandatory executions or rewrites. Primary behavior entry points are unit/config/test_presentation_config.py, unit/config/test_settings.py, unit/presenters/test_text_budget_limiter.py, unit/test_presenter.py, integration/test_execution_presentation_v3.py and integration/test_tool_attachment_transport.py, all under tests/mcp_server/. Replace the old 12-combination matrix and oversized-core-overrun expectations with two-route behavior in those existing cases. Prove UTF-8 byte bounds including footer, Unicode/fence safety, matching schema presence, structured guidance, resource readback, separate attachments in both modes and matching presentation references without a second structured body copy, truthful failure and same-workspace instance isolation. Other construction consumers are tests/mcp_server/test_support.py, integration/test_pipeline_e2e.py, integration/test_rollout_configuration.py, integration/test_v3_cutover.py, unit/core/interfaces/test_presenter_interfaces.py, unit/schemas/test_presentation_output.py, unit/server/test_validate_tool_arguments.py and unit/test_server.py. Adjust only invalidated setup/assertions; no new harness matrix, version surveillance, legacy preservation or speculative regression suite.

Update the current presentation architecture reference, server-configuration reference, setup guide and packaged cache-reading guide where their profile, budget or delivery descriptions change. Historical #529 documents remain evidence of the earlier approved contract; this dated decision supersedes it for future work. Do not spread new instructions across agent files and phase contracts.

### Scope boundary

This is behavior/configuration-contract refactoring rather than mechanical release maintenance. The current branch remains chore / Research. The owner has authorized recording and impact analysis, not production edits or an administrative workflow correction in this request. Do not implement this on the chore branch or migrate #536 merely to absorb it. Other #536 cleanup/release tasks remain paused.

### Proposed issue split and release dependency

Recommendation for owner/Coordination discussion, not an already executed issue or branch operation:

1. Keep #536 as the owner-observed acceptance, workspace housekeeping and release chore. Preserve this research as the accepted finding and source index.
2. Have Coordination create one bounded refactor issue and a separate branch from current main, with explicit parent registration. Scope: two named delivery modes, final inline byte bound, configured route/attachment references, independent attachment transport, matching catalog/schema, existing failure behavior, directly affected tests and current docs. Link the committed #536 research; do not copy state.json/deliverables.json or reset workflow history.
3. Reuse this research and the owner's approved decisions for targeted independent Research-to-Design review. Work out only remaining concrete interfaces/default/recovery details through the normal refactor workflow. Do not restart harness research or introduce compatibility routes.
4. After the refactor's QA, Ready and merge, return #536 to an updated main-based candidate and repeat only live acceptance invalidated by the change. Use the same #536 lifecycle unless a real gate/state condition requires an explicitly audited recovery.
5. Treat the refactor as a release prerequisite: #536 does not publish the old delivery contract as if the new one were accepted. The owner still accepts the exact release candidate before tagging/publication. Independent housekeeping can be sequenced separately; no release or broad validation is performed by recording this split.

## Questions

- The owner selected two named values: structured and resource. Design must finalize the configuration/environment key and explicit default; no boolean or arbitrary profile dictionary.
- Attachment policy is decided: native embedded-resource content blocks in both modes, with references in inline and structured presentation. Design specifies only the carrier/reference shape and transport transfer, including independent context-invalid attachments.
- Specify final limiter/footer validation and error/recovery projections at existing boundaries, preserving the separately approved startup recovery exception. Reopen owner policy only if evidence requires changing that exception or actual loss/completeness rules.

## Approved Strategy

Owner decision recorded on 2026-10-20:

- Normal inline text is always present and finally bounded. The selected supplement is structured content or the existing operation cache; no independent presentation/data/delivery matrix is needed. The owner selects two named values, structured and resource, rather than a boolean.
- End inline text with a configured notice identifying the selected full-data route. Keep a cache locator only when publication succeeded; no need for conditional-reference inference.
- Structured content includes explanation/instructions because the client may select it instead of separate text. Resource mode supplements the inline text and does not require caching that rendered text.
- Always deliver available attachments separately in both modes, using the pre-#529 native MCP embedded-resource route. Refer to the supplied attachments in inline text and repeat those references in structured presentation. Do not duplicate their bodies in a structured attachment field or move them into the operation cache. Existing schema values owned by operation DTOs remain unchanged.
- Retain existing operation semantics and DTOs, cache reader/pagination, separate attachment ownership and existing exception/presenter boundaries. No client-specific logic or new cache framework.
- The prior owner clean-break direction remains: no compatibility bridge or preservation of obsolete combinations; reuse valuable behavior tests and remove obsolete expectations.
- Instruction truncation is **noted**, with no observed practical failure found in the reviewed research or current acceptance. It is not a blocker, separate implementation package or reason to add tests/cache duplication. No universal client-consumption guarantee is claimed.

## Expected Results

- A large normal tool result still produces inline text within the configured UTF-8 allowance, including the truthful route footer and any truncation notice.
- Structured mode delivers full operation facts and explanatory/instructional presentation in structuredContent, without a full JSON text dump.
- Resource mode returns a usable cached-operation URI in text and omits normal structuredContent.
- Both modes retain every available separate attachment; inline presentation identifies it and structured presentation repeats that reference. Structured attachment-body duplication is removed; existing operation-owned schema fields remain.
- Different server instances can select different routes against one shared workspace.
- Delivery/response-processing problems retain truthful operation outcomes and bounded diagnostics; no fabricated complete result, cache URI or repeated failed rendering.
- Existing profile-matrix coverage becomes smaller behavior coverage for the two supported routes. No implementation or test pass is claimed by this Research artifact.

## Evidence

### Historical hard limit and unconditional available-cache locator

Read-only Git source inspection at cf6ccde6 and immediately before 98378e6e confirmed the final TextBudgetLimiter call, 8000-byte default, run-ID-based locator condition and 6000-character pagination-advice threshold. #523 records #462's closure without implementation.

- [#523 historical decisions](<../archive/issue523/research.md>)
- [#524 cache/limiter contract](<../archive/issue524/design.md>)
- [#456 original budget validation](<../archive/issue456/validation.md>)

**Invocation:** git show cf6ccde6:mcp_server/presenters/text_presenter.py; git show cf6ccde6:mcp_server/presenters/text_budget_limiter.py; git show cf6ccde6:.pgmcp/config/defaults/presentation.yaml

**Observed Result:** Source inspection only; no historical executable replay.

### \#529 does not establish inability to consume text-plus-resource output

The selected VS Code/Claude routes lost separate text when both text and structured content were present. Kilo/Pi/the tested Antigravity route received text and read resources. These observations do not establish a client that cannot process a text-only response but independently reads its cache. No demonstrated instruction-truncation harm was found.

- [#529 measured routes and acceptance limits](<../archive/issue529/research.md>)

### Current ownership explains the bounded implementation surface

Repository reads show ResponsePresenter owns projection/schema, TextBudgetLimiter protects oversized core, MCPServer caches operation only, and attachment content has separate producers. No production/configuration changes, restart, test execution or new client probe was performed for this analysis.

- [Current presenter](<../../../mcp_server/presenters/response_presenter.py>)
- [Cache reader](<../../../mcp_server/resources/cache.py>)
- [Scaffold attachment producer](<../../../mcp_server/tools/scaffold_tool.py>)
- [Schema attachment producer](<../../../mcp_server/tools/template_schema_tool.py>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-20 | @imp researcher | Record the owner's bounded-text/two-route decision, historical evidence, focused consumers and remaining design questions; no implementation. |
| 0.2 | 2026-10-20 | @imp researcher | Record named modes and owner-approved independent attachments/references in both routes; update DTO/server/test impact and propose a separate refactor issue before release. |

