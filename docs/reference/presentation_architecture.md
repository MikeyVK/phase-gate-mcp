<!-- docs/reference/presentation_architecture.md -->
<!-- template=reference version=064954ea created=2026-08-19T19:43Z updated=2026-10-20 -->
# Presentation Architecture and Response Modes

**Status:** DEFINITIVE  
**Version:** 4.0.0

**Last Updated:** 2026-10-21

**Configuration basis:** [presentation.yaml](../../.pgmcp/config/defaults/presentation.yaml)  
**Composition root:** [bootstrap.py](../../mcp_server/bootstrap.py)  
**Presenter implementation:** [mcp_server/presenters](../../mcp_server/presenters)

## Purpose

The operation DTO owns tool-result facts. The presentation boundary supplies bounded readable text, one selected supplementary operation-data route and independently owned attachments. MCPServer transfers that projection without reconstructing DTOs from text. The existing cache retains only the operation.

Configuration owns wording, field/collection declarations, ordering, item limits, shared budgets and the default mode. Generic presenters own rendering, final text limiting, mode selection and matching public schema. Internal operation DTOs and ToolExecution retain their responsibilities.

## End-to-End Flow

```mermaid
sequenceDiagram
    participant Client as MCP client
    participant Server as MCPServer
    participant Tool as Wrapped ITool
    participant Cache as ResponseCacheManager
    participant Presenter as ResponsePresenter
    participant Text as TextPresenter
    participant Budget as TextBudgetLimiter
    Client->>Server: tools/call(name, arguments)
    Server->>Tool: execute(arguments, NoteContext)
    Tool-->>Server: ToolExecution(operation, attachments)
    Server->>Cache: publish operation only
    Cache-->>Server: CachePublication(run_id or diagnosis)
    Server->>Presenter: operation, notes, attachments, publication facts
    Note over Presenter: Prior serialization failure bypasses normal rendering/conversion
    Presenter->>Text: render configured explanation and guidance once
    Text-->>Presenter: RenderedPresentation(core, details)
    Presenter->>Budget: bound body plus reserved footer and notices
    Presenter-->>Server: text, optional structured content, separate resources
    Server-->>Client: text + embedded resources + optional structuredContent; actual isError
```

Normal publication precedes presentation. The final text limit does not remove fields from a complete structured operation or successfully cached operation. Attachment formatting remains in SchemaResourcePresenter.

## Ownership Boundaries

| Concern | Owner |
| --- | --- |
| Result semantics and complete operation facts | Frozen operation DTO |
| Operation/attachment separation | ToolExecution carrier |
| Canonical cached representation and window reads | ResponseCacheManager / CachedResponseResource |
| Attachment identity/schema facts | SchemaAttachment producer |
| Attachment URI, media type and schema serialization | SchemaResourcePresenter |
| Wording, field/collection declarations, ordering and item limits | presentation.yaml |
| Default mode and shared budgets | PresentationConfig |
| Per-process mode selection | Existing Settings / bootstrap |
| Scalar and collection formatting | TextPresenter / CollectionTextRenderer |
| Final UTF-8 text bound, footer reserve and safe excerpts | TextBudgetLimiter |
| Selected public envelope, emergency projection and output schema | ResponsePresenter |
| Transfer to MCP and real operation isError | MCPServer |

Managers, tools and adapters do not compose user-facing policy explanations. Native diagnostics and original exception causes remain evidence at the existing error boundaries. See [Architecture Principles §15](../coding_standards/ARCHITECTURE_PRINCIPLES.md).

## Process-Local Modes

Presentation configuration version 2.0.0 requires global.response_mode with exactly two values. The existing loader composes defaults with workspace overrides.

| Mode | Inline text | Supplementary operation data | outputSchema |
| --- | --- | --- | --- |
| structured (shipped default) | Finally bounded; ends with structured-result notice | Complete operation and full rendered presentation in structuredContent | Matching common envelope |
| resource | Finally bounded; ends with a real cache URI and paging advice when applicable | Existing operation cache, read through the same server connection | Absent for normal tools |

Both modes deliver available attachments as separate native embedded-resource content blocks. No complete operation JSON is appended to text.

Set PGMCP_RESPONSE_MODE=structured or resource on an individual launcher process. An explicit environment selector overrides launcher server.response_mode; omission uses global.response_mode. ResponseMode is defined once in pure [Settings](../../mcp_server/config/settings.py) and reused by presentation configuration. Invalid or empty values reject healthy startup admission. There is no profile dictionary, channel matrix, old-selector alias, harness detection or shared active-mode state. Different processes can select different modes against the same workspace without rewriting shared configuration.

Shared max_text_response_bytes, max_cache_failure_detail_bytes and cache_read_budget_chars remain in global settings, with defaults 8000 UTF-8 bytes, 8000 UTF-8 bytes and 6000 Unicode codepoints respectively. Budgets must be positive; final-text feasibility is additionally validated against configured fixed notices and footer reserves.

See [setup guidance](../setup/README.md#choose-the-response-mode) for activation and client verification.

## Public Envelope and Channels

Structured mode supplies the common envelope:

```json
{
  "success": true,
  "presentation": "Planning updated. Read the refreshed work context.\n\nFull result available in the structured response.",
  "data": {"delivery": "inline", "operation": {"success": true}},
  "attachments": [],
  "delivery_error": null,
  "processing_error": null
}
```

All six fields are emitted. Normal data is a complete JSON-mode operation with aliases. presentation contains the full configured rendering before inline clipping, plus the same attachment/route notices. success is the actual operation outcome; delivery_error describes a separate delivery failure and processing_error a later response-processing failure. Normal processing_error is null.

Resource mode emits bounded text and separate attachments without normal structuredContent or outputSchema. Its locator identifies only a successfully published operation. It does not duplicate rendered instructions in the cache.

Each available attachment is independently emitted after the text as a native MCP EmbeddedResource with uri, mimeType and text. In structured mode, attachments contains only uri/mime_type references to those same supplied blocks; there is no second body copy in this field. Existing schema fields owned by an operation DTO remain intact. A configured generic attachment notice appears in inline text and full structured presentation. A schema:// identity does not imply a registered resources/read route.

ResponsePresenter derives outputSchema from the same frozen public models and selected mode used for delivery. Structured schema admits complete InlineOperation, explicit delivery failure or compact processing recovery. The recovery alternative requires non-null processing_error; omitting it cannot admit recovery-shaped data. MCPServer transfers the selected schema to tools/list and does not add an internal-DTO schema or another presenter.

Unknown tools and errors before a normalized operation remain explicit errors at their existing boundary; they do not invent operation facts.

## Final Presentation Budget

TextPresenter still returns core (main templates, enum explanations, instructions and notes) and details (configured collection projections). ResponsePresenter renders once, adds configured notices, and applies TextBudgetLimiter to the final inline projection.

The default normal text allowance is 8000 UTF-8 bytes **including** route/attachment footer, separators, truncation notice and any required fence closure. The limiter reserves the complete footer and truthful truncation notice, then shortens the body prefix on safe UTF-8 boundaries. There is no protected-core overrun. The structured presentation retains the complete rendering; the operation cache retains only operation data.

Startup rejects an allowance too small for the conservative configured fixed-notice/footer reserve, expanded cache ID and fence closure. It does not silently enlarge the budget. The generic limiter also rejects an impossible supplied footer. Configured URI and outcome messages admit only their limited scalar placeholders; attachment wording is fixed-size rather than an unbounded URI list.

Text shortening is explicitly signalled. Instruction truncation remains an owner-noted limitation, with no demonstrated practical failure in the reviewed investigation; this is not a universal guarantee of instructions reaching every model. Complete structured data, structured presentation, attachments and total wire/token size are outside the inline cap.

cache_read_budget_chars controls pagination advice, not resource read limits. A notice about supplementary data depends on actual availability, including an already-successful cache receipt when inline serialization or later processing fails.

## Cache and Serialization Failures

| Situation | Delivered result |
| --- | --- |
| Structured conversion succeeds | Complete operation/full presentation in structuredContent; bounded text and separate attachments. A cache storage failure remains visible without negating complete structured facts. |
| Resource mode, publication succeeds | Bounded text with real URI and optional paging advice; separate attachments, no structuredContent/schema. |
| Resource mode, publication fails | Actual outcome and bounded labelled diagnosis; no fabricated URI or JSON dump. |
| Publisher reports serialization_failed, either mode | Before normal TextPresenter or full operation conversion, use only known outcome, bounded publisher diagnosis and independently formatted attachments. Structured mode has data=null and operation_serialization_failed; resource mode stays text plus attachments. |
| Later structured conversion fails | Explicit operation_serialization_failed with truthful existing cache guidance if available; otherwise complete data is unavailable. No repeat serializer. |

Canonical cache serialization runs once before accepting an entry. Its failure is captured at the existing publisher boundary as serialization_failed with the native diagnosis; no entry/eviction occurs and no substitute error JSON is claimed as the operation.

That prior failure is a guard against further full operation traversal/rendering/conversion. A storage failure after successful serialization (write_failed) is distinct: one independent structured JSON-mode conversion may still deliver complete data. No failed serializer, publisher or operation is retried.

Delivery failure retains actual success/isError. Its diagnosis is a labelled potentially incomplete native-text excerpt under max_cache_failure_detail_bytes; normal inline text also obeys its final cap. Structured failure fields remain complete valid JSON, not sliced serialized output. These bounds do not promise streaming or bounded memory for arbitrary objects.

## Compact Response-Processing Recovery

An unexpected failure after an operation has returned is distinct from the normal cache/serialization delivery failures above. MCPServer remembers the known boolean outcome before further processing, logs the original exception and invokes the existing presenter's recover() once. The server passes only that outcome, native diagnostic strings and optional UUID/size from an already-successful cache receipt. It owns no recovery wording, mode projection or response-schema definition.

| Recovery field | Meaning |
| --- | --- |
| success / MCP isError | Actual known operation outcome; a successful operation stays success=true / isError=false |
| presentation | Short configured notice in text and, for structured mode, structured presentation |
| data | Already-existing ResourceOperation reference or null; never a replayed InlineOperation |
| attachments | Empty; original attachments are not inspected or converted |
| delivery_error | null; this route makes no new full-data delivery attempt |
| processing_error | Existing ExecutionErrorOutput containing only bounded native text and a diagnostic_details_truncated flag; its success=false describes the later processing failure |

Recovery does not receive or serialize the original operation, notes, source instruction fields, attachments or arbitrary exception parameters. It calls neither normal present()/rendering nor the publisher/resource reader. The explicit recovery exception therefore does not promise the full result, normal advice, raw notes or phase instructions that had not yet been rendered. Its short notice instructs the caller to verify the actual outcome before repeating an operation.

A successful existing receipt can supply a reference even when normal delivery is inline. That is an explicit small recovery alternative, not a mode change or automatic publication. The reference points only to the already-cached operation; it does not contain attachments, raw notes or the later diagnosis. Cache lifetime and client access are not guaranteed. With no successful receipt, data=null and the configured no-publication notice is shown; no replacement dump or invented URI is emitted.

Recovery uses the already-resolved mode. Both modes emit finally bounded text. Structured mode additionally carries the compact diagnosis and optional existing ResourceOperation in the common envelope; resource mode adds no structured channel or JSON text envelope.

max_cache_failure_detail_bytes (default 8000) is one UTF-8 diagnosis budget: error_message first, traceback from the remainder. Prefixes are bounded before encoding and safely excerpted. Original exception parameters/context are not copied. Shortened details set processing_error.params.diagnostic_details_truncated=true and add the configured notice. Full native cause/trace remains in existing server logs. The outer JSON remains parseable; there is no total-response-size promise.

The existing global.next_instruction_texts configuration owns response_processing_failed, recovery_cache_unavailable and processing_diagnostic_truncated. Startup validation requires nonempty messages and permits only plain {success} in the first; the other two are constants. Existing reference/pagination wording is reused only for an already-successful receipt.

There is one recovery attempt. A secondary recovery/SDK failure ends through existing logging and the terminal SDK boundary, retaining the known outcome and original/secondary causes in logs; there is no third format or operation retry. Unknown-tool errors and failures before a known outcome retain their existing genuine-error handling.

## Startup Recovery

When startup configuration is rejected, StartupRecoveryPresenter does not load another config, select a mode or depend on cache access. Its fixed exception is full recovery text/instructions in both content and presentation, complete inline operation diagnosis, direct attachments and delivery_error=null. Healthy startup restores the configured mode. If this fixed normal presentation itself fails after a known outcome, the compact exception above applies: outcome and short notice appear in both presentation channels, with the bounded processing diagnosis in the common structured envelope. It has a fixed 8000-byte diagnostic allowance, no cache reference and no mode/configuration dependency. This stays inside StartupRecoveryPresenter; the server does not add a fallback presenter.

A health query can succeed while reporting rejected admission; a restart receipt does not prove that the replacement admitted successfully. Check health and refresh tools/list after replacement. Raw proxy failures before an MCP response remain proxy-event presentation, without invented tool outcomes.

## Declarative Rendering and Catalog Validation

ServerBootstrapper derives SupportedToolContract entries from actual supported tool instances and output models. Settings select ToolAssembly.active_tools. This avoids a second static catalog and validates inactive supported tools too.

A tool presentation entry uses template_success/template_failure, max_items, ordered collections/children, enum_cases, next_instructions and configured note groups. Collection/child/enum identities are mapping keys with unique sibling order ranks; DTO item order remains unchanged. See [configuration composition](config-loading-architecture.md).

Only exact list[T] and variadic tuple[T, ...] sequence annotations are supported, with scalar or Pydantic model items. Flat scalar sequences can appear in templates; structured sequences use declared collections. Each depth applies max_items independently. Arbitrary iterable discovery, sorting/filtering and tool-specific renderer branches are unsupported.

Normal note templates use the same global formatting policy and the selected tool's max_items as other flat scalar sequence formatting. Lists and tuples retain source order; the configured separator, omission text and none_value determine their textual projection. Rendering does not modify note parameters. A tool without max_items receives no invented limit: a sequence requiring that policy, or an unsupported nested value, retains the existing visible formatting diagnostic. All successfully rendered notes remain part of the shared rendered body; this formatting policy does not remove fields from the operation or change its persisted facts.

For example:

```yaml
list_issues:
  category: query
  max_items: 10
  template_success: "Found {issues_count} issues matching criteria."
  collections:
    issue_rows:
      order: 10
      field: issues
      heading: "Issues:"
      item_template: "- #{number} [{state}] {title} — {html_url}"
```

Successful output must have the declared field/container/item shapes. Generic failure DTOs may omit success-only collections; presentation never fabricates them. Startup rejects missing/unknown tool entries, duplicate names, unresolved output models, invalid placeholders/formatting, unsupported collections/children, invalid enum cases and inconsistent max_items declarations. Configured global text budgets must also satisfy the fixed-notice/footer feasibility validation.

## Cache Representation and Client Guidance

The cache retains required nullable fields and explicitly supplied optional nulls; only unset optional null fields are omitted. Non-null defaults and ordinary JSON values (null, false, zero, empty containers) retain their existing representation. Complete and window reads use that same canonical JSON. A later resource serialization failure propagates to the existing read-resource error boundary, without a replacement completeness claim.

Inline JSON mode with aliases and the cache's canonical field-presence policy represent the same operation, without promising byte-identical JSON. Do not reconstruct facts from rendered Markdown.

Use the selected complete inline data when available; otherwise read the successful resource reference. Check size before paging and follow the [packaged cache guide](../../mcp_server/resources/cache_reading.md). The cache is transient/process-local; a run ID alone is not durable proof. Record exact invocation, scope and observed outcome in committed evidence. Never replay a mutation merely to recover cached details.

SchemaResourcePresenter maps attachment identity to schema://validation (application/json) or schema://template/<percent-encoded-template-id>/context (application/schema+json). The complete schema content travels in separate native MCP embedded-resource blocks in both modes. Structured attachment metadata references those blocks without another body copy. Attachments never enter the operation cache; existing operation-owned schema values remain.

Server publication proves the selected server output, not delivery to every downstream model context. Installation must verify the chosen client's actual presentation and full-data readback route; no harness-version compatibility matrix is built into the presenter.

## Configured Execution Evidence

run_checks, run_tests and apply_fixes use the same mode boundary. Inspect operation success/error_code separately from each native result's status, reason, evidence, adapter identity and capture. An accepted operation can contain a failed native check without becoming a protocol failure.

apply_fixes runs selected fixes in request order and stops when work cannot continue or a fix does not pass. Earlier native changes may exist; rollback is not promised. Inspect the result and affected files before an authorized narrow recheck. Presentation never chains another fix/check automatically.

## Primary Implementation and Evidence

- [Mode and presentation config](../../mcp_server/config/schemas/presentation_config.py)
- [Public envelope/value models](../../mcp_server/schemas/presentation_output.py)
- [Response presenter](../../mcp_server/presenters/response_presenter.py)
- [Configured text renderer](../../mcp_server/presenters/text_presenter.py)
- [Budget limiter](../../mcp_server/presenters/text_budget_limiter.py)
- [Startup recovery presenter](../../mcp_server/presenters/startup_recovery_presenter.py)
- [Cache resource](../../mcp_server/resources/cache.py)
- [Known-outcome recovery and missing-marker SDK cases](../../tests/mcp_server/integration/test_tool_attachment_transport.py)
- [Issue #528 validation](../development/archive/issue528/validation.md)
- [Mode/SDK/serializer behavior tests](../../tests/mcp_server/integration/test_execution_presentation_v3.py)
- [Rendering composition tests](../../tests/mcp_server/unit/presenters/test_text_presenter_composition.py)
- [Startup and instance-isolation tests](../../tests/mcp_server/integration/test_target_startup.py)
- [Issue #529 historical validation](../development/archive/issue529/validation.md)
- [Issue #537 validation](../development/archive/issue537/validation.md)

## Related Documentation

- [MCP tools navigation](tools/README.md)
- [Quality and validation tools](tools/quality.md)
- [Discovery and admin tools](tools/discovery.md)
- [Architecture principles](../coding_standards/ARCHITECTURE_PRINCIPLES.md)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 2.3.0 | 2026-09-24 | @imp | Align execution evidence and runtime catalog guidance with the V3 check/test/fix surface |
| 2.1.0 | 2026-08-22 | Agent | Document nested structured quality-gate findings and complete cached evidence |
| 2.2.0 | 2026-09-13 | Agent | Document operation/attachment transport and required-null cache fidelity |
| 2.0.0 | 2026-08-22 | Agent | Document bounded declarative projection, runtime catalog alignment, ordered collections, and final byte limiting |
| 1.1.0 | 2026-08-19 | Agent | Document composite text and validation-resource presentation |
| 2.4.0 | 2026-10-18 | @imp documenter | Document server-owned structured operation delivery, SDK2 ownership and retained cache/attachment semantics. |
| 2.4.1 | 2026-10-19 | @imp documenter | Distinguish cache/text availability notices from operation delivery and client access. |
| 3.0.0 | 2026-10-20 | @imp documenter | Document process-local profiles, selected common envelope/schema, protected core, independent serialization failures and fixed recovery. |
| 3.0.1 | 2026-10-20 | @imp documenter | Document compact known-outcome processing recovery, required schema marker, channel/budget/cache limitations and fixed startup exception; remove obsolete wrapper-metadata reservation. |
| 3.0.2 | 2026-10-20 | @imp documenter | Clarify existing global formatting and selected-tool limits for normal notes, immutable source parameters and visible invalid-policy/value diagnostics. |
| 4.0.0 | 2026-10-21 | @imp documenter | Replace independent profiles with two named modes, final inline bounds, separate attachment bodies/metadata references and the prior-serialization guard; preserve compact/startup recovery ownership. |
