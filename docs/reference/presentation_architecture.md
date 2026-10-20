<!-- docs/reference/presentation_architecture.md -->
<!-- template=reference version=064954ea created=2026-08-19T19:43Z updated=2026-10-20 -->
# Presentation Architecture and Response Profiles

**Status:** DEFINITIVE  
**Version:** 3.0.1  
**Last Updated:** 2026-10-20

**Configuration basis:** [presentation.yaml](../../.pgmcp/config/defaults/presentation.yaml)  
**Composition root:** [bootstrap.py](../../mcp_server/bootstrap.py)  
**Presenter implementation:** [mcp_server/presenters](../../mcp_server/presenters)

## Purpose

The operation DTO owns tool-result facts. The presentation boundary projects those facts, configured instructions and separately owned attachments through a response profile. MCPServer transfers that projection without reconstructing DTOs from text. The cache retains the operation through its existing canonical serialization policy.

Configuration owns wording, presentation fields, collection ordering, item limits and profile definitions. Generic presenters own rendering, protected-core budgeting, selected-channel delivery and the matching public schema. This is a clean public-contract cutover; internal operation DTOs and ToolExecution retain their responsibilities.

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
    participant Resources as SchemaResourcePresenter
    Client->>Server: tools/call(name, arguments)
    Server->>Tool: execute(arguments, NoteContext)
    Tool-->>Server: ToolExecution(operation, attachments)
    Server->>Cache: publish operation only
    Cache-->>Server: CachePublication(success, run_id or diagnosis)
    Server->>Presenter: operation, notes, attachments, publication facts
    Presenter->>Text: render configured explanation and guidance
    Text-->>Presenter: RenderedPresentation(core, details)
    Presenter->>Budget: protect core; limit optional details
    Presenter->>Resources: serialize supplied attachments
    Presenter-->>Server: PresentedOutput(text?, structured_content?)
    Server-->>Client: selected channels; actual isError
```

Normal publication precedes presentation. Limits on rendered details never remove fields from a normally delivered inline operation or from a successfully published cached operation.

## Ownership Boundaries

| Concern | Owner |
| --- | --- |
| Result semantics and complete operation facts | Frozen operation DTO |
| Operation/attachment separation | ToolExecution carrier |
| Canonical cached representation and window reads | ResponseCacheManager / CachedResponseResource |
| Attachment identity/schema facts | SchemaAttachment producer |
| Attachment URI, media type and schema serialization | SchemaResourcePresenter |
| Wording, field/collection declarations, ordering and item limits | presentation.yaml |
| Profile definitions and default | PresentationConfig |
| Per-process profile selection | Existing Settings / bootstrap |
| Scalar and collection formatting | TextPresenter / CollectionTextRenderer |
| Protected core and optional-detail budget mechanics | TextBudgetLimiter |
| Selected public envelope, emergency projection and output schema | ResponsePresenter |
| Transfer to MCP and real operation isError | MCPServer |

Managers, tools and adapters do not compose user-facing policy explanations. Native diagnostics and original exception causes remain evidence at the existing error boundaries. See [Architecture Principles §15](../coding_standards/ARCHITECTURE_PRINCIPLES.md).

## Process-Local Profiles

Presentation configuration version 2.0.0 defines response_profiles and global.default_response_profile. The existing loader composes defaults with workspace overrides. Each profile requires:

| Field | Values | Meaning |
| --- | --- | --- |
| presentation_channel | text, structured, both | Where the complete short explanation and mandatory instructions appear |
| data_channel | text, structured | Where complete operation data or its resource reference and direct attachments appear |
| data_delivery | inline, resource | Whether operation data is inline or points to successful cache publication |

Shipped profiles:

| Profile | Presentation | Data channel | Operation delivery |
| --- | --- | --- | --- |
| structured_inline (default) | both | structured | inline |
| structured_resource | both | structured | resource |
| text_inline | text | text | inline |

Set PGMCP_RESPONSE_PROFILE on an individual launcher process to select a named profile. An explicit environment value overrides launcher-provided server.response_profile; omission selects the configured global default. Empty or unknown selectors fail startup admission. No harness/model detection or shared active-profile state exists. Two processes can read the same config root and select different profiles without editing shared configuration.

Profile definitions may override max_text_response_bytes, max_cache_failure_detail_bytes and cache_read_budget_chars; omitted overrides inherit global values. All resolved budgets must be positive. Invalid literals, unknown fields, empty profile maps and invalid defaults fail configuration validation.

See [setup guidance](../setup/README.md#choose-the-response-profile) for activation and client verification.

## Public Envelope and Channels

When presentation or data selects structured, structuredContent is the common envelope:

```json
{
  "success": true,
  "presentation": "Planning updated. Read the refreshed work context.",
  "data": {"delivery": "inline", "operation": {"success": true}},
  "attachments": [],
  "delivery_error": null,
  "processing_error": null
}
```

Generated envelopes include all six outer fields. presentation is null if structured presentation is unselected. data and processing_error are null and attachments is empty in a structured presentation-only projection when the data channel is text. success always represents the actual operation outcome; delivery_error describes a separate normal delivery failure, while processing_error describes a later response-processing failure. Normal output has processing_error=null.

Normal data alternatives:

- Inline: delivery=inline and the complete operation serialized in JSON mode with aliases.
- Resource: delivery=resource, a truthful pgmcp://cache/runs/<run_id> URI and optional size_chars. The resource points only to the operation.
- Attachments: complete objects with uri, mime_type and content in the selected data channel, including resource profiles.

With data_channel=text, one distinct fenced JSON segment carries the complete envelope data/attachments after any selected presentation. That segment is outside the short-presentation budget. No unconditional embedded-resource or unselected-channel copy is added. With entirely structured normal output, content can be empty. With both channels exclusively text, outputSchema and structuredContent are absent.

The presenter generates the selected outputSchema from the same frozen public models and resolved profile used for delivery. It admits normal delivery, applicable delivery errors and compact processing recovery, with channel-specific restrictions. The compact alternative requires a non-null processing_error diagnosis; merely omitting that field cannot admit otherwise invalid recovery-shaped data. Normal inline/resource restrictions remain intact. MCPServer uses this profile-derived schema for the connected tool catalog; it does not advertise each internal operation DTO as the public response shape.

Unknown-tool requests and processing/transport errors before a normalized operation exists remain genuine explicit errors at their existing boundary. They do not invent an operation DTO.

## Protected Presentation and Budgets

TextPresenter returns core and details separately:

- core: complete configured success/failure template, enum explanation, next instructions and all notes. Phase instructions and hand-over text embedded in a main template therefore remain complete.
- details: configured collection projections, retaining existing item limits.

ResponsePresenter adds truthful cache/pagination or failure notices. TextBudgetLimiter reserves the core, separators and required truncation notice before admitting optional details. It cuts only details, on UTF-8-safe boundaries, preferring complete lines/blocks and closing an intersected fence within the allowance.

The global presentation allowance is 8000 bytes by default. Protected content alone may exceed it and is never cut; optional details are then omitted with the configured notice. Complete inline data and attachments are outside this budget. This is not a universal wire/token/cost ceiling.

cache_read_budget_chars (default 6000 Unicode codepoints) controls when to display pagination advice, not a resource read limit. The actual existing window API is unchanged.

## Cache and Serialization Failures

| Situation | Delivered result |
| --- | --- |
| Cache succeeds; inline selected | Complete inline operation and attachments; truthful cache guidance |
| Cache fails; inline serialization succeeds | Complete inline operation and attachments; configured cache-unavailable warning |
| Resource selected; cache fails or publisher absent | No fabricated URI; protected emergency text, data=null and explicit delivery_error |
| Inline serialization fails | Protected emergency text and operation_serialization_failed; actual success/isError retained |
| Cache succeeds but inline serialization fails | Same explicit inline delivery error; any cache guidance remains truthful, without silently changing the selected route |

Canonical cache serialization runs once before accepting an entry. Its native failure propagates to the existing publisher boundary, which captures the original exception/cause and returns CachePublication(success=False, error_code=serialization_failed, diagnostic=...). No entry or eviction occurs on failed serialization. Other publication failures report write_failed with diagnosis. The serializer never substitutes error JSON and reports it as complete operation publication.

The distinct inline JSON projection is attempted once when needed. A failure of canonical serialization does not establish failure of inline serialization, or vice versa. No failed full serializer is retried to construct an emergency excerpt.

Emergency output retains actual outcome, explanation, instructions, notes and necessary failure/truncation notices. It emits text even for a normally structured-only presentation profile and also retains selected structured presentation. Complete attachments remain directly available. delivery_error.code is cache_publication_failed or operation_serialization_failed, with details_truncated.

Only native diagnostic details are bounded by max_cache_failure_detail_bytes (default 8000), including excerpt label/formatting closure. The core remains protected even when larger. The excerpt is labelled potentially incomplete diagnostic text, not a complete JSON result. The outer MCP response and selected structured variant remain serializable/schema-valid. These are output bounds, not streaming or memory guarantees for arbitrary objects.

## Compact Response-Processing Recovery

An unexpected failure after an operation has returned is distinct from the normal cache/serialization delivery failures above. MCPServer remembers the known boolean outcome before further processing, logs the original exception and invokes the existing presenter's recover() once. The server passes only that outcome, native diagnostic strings and optional UUID/size from an already-successful cache receipt. It owns no recovery wording, profile projection or response-schema definition.

| Recovery field | Meaning |
| --- | --- |
| success / MCP isError | Actual known operation outcome; a successful operation stays success=true / isError=false |
| presentation | Short configured notice in the selected presentation channel(s) |
| data | Already-existing ResourceOperation reference or null; never a replayed InlineOperation |
| attachments | Empty; original attachments are not inspected or converted |
| delivery_error | null; this route makes no new full-data delivery attempt |
| processing_error | Existing ExecutionErrorOutput containing only bounded native text and a diagnostic_details_truncated flag; its success=false describes the later processing failure |

Recovery does not receive or serialize the original operation, notes, source instruction fields, attachments or arbitrary exception parameters. It calls neither normal present()/rendering nor the publisher/resource reader. The explicit recovery exception therefore does not promise the full result, normal advice, raw notes or phase instructions that had not yet been rendered. Its short notice instructs the caller to verify the actual outcome before repeating an operation.

A successful existing receipt can supply a reference even when normal delivery is inline. That is an explicit small recovery alternative, not a profile change or automatic publication. The reference points only to the already-cached operation; it does not contain attachments, raw notes or the later diagnosis. Cache lifetime and client access are not guaranteed. With no successful receipt, data=null and the configured no-publication notice is shown; no replacement dump or invented URI is emitted.

Recovery consults only already-resolved presentation_channel/data_channel flags. For textual data, a complete small fenced JSON envelope carries the diagnosis/reference; a separate structured presentation-only envelope keeps data and processing_error null. A wholly textual profile still advertises no outputSchema. No extra unconditional channel or normal large-data projection is introduced.

The existing max_cache_failure_detail_bytes allowance (default 8000) is one shared UTF-8 budget: error_message first, traceback from the remainder. Candidate string prefixes are bounded before encoding, then safely excerpted. Original exception parameters/context are not copied. Shortened details set processing_error.params.diagnostic_details_truncated=true and add the configured notice. The enclosing JSON remains complete and parseable; full native cause/trace remains in existing server logs. Protected notices and ordinary JSON/channel overhead mean this is not a new whole-response byte ceiling.

The existing global.next_instruction_texts configuration owns response_processing_failed, recovery_cache_unavailable and processing_diagnostic_truncated. Startup validation requires nonempty messages and permits only plain {success} in the first; the other two are constants. Existing reference/pagination wording is reused only for an already-successful receipt.

There is one recovery attempt. A secondary recovery/SDK failure ends through existing logging and the terminal SDK boundary, retaining the known outcome and original/secondary causes in logs; there is no third format or operation retry. Unknown-tool errors and failures before a known outcome retain their existing genuine-error handling.

## Startup Recovery

When startup configuration is rejected, StartupRecoveryPresenter does not load another config, select a profile or depend on cache access. Its fixed exception is full recovery text/instructions in both content and presentation, complete inline operation diagnosis, direct attachments and delivery_error=null. Healthy startup restores the configured profile. If this fixed normal presentation itself fails after a known outcome, the compact exception above applies: outcome and short notice appear in both presentation channels, with the bounded processing diagnosis in the common structured envelope. It has a fixed 8000-byte diagnostic allowance, no cache reference and no profile/configuration dependency. This stays inside StartupRecoveryPresenter; the server does not add a fallback presenter.

A health query can succeed while reporting rejected admission; a restart receipt does not prove that the replacement admitted successfully. Check health and refresh tools/list after replacement. Raw proxy failures before an MCP response remain proxy-event presentation, without invented tool outcomes.

## Declarative Rendering and Catalog Validation

ServerBootstrapper derives SupportedToolContract entries from actual supported tool instances and output models. Settings select ToolAssembly.active_tools. This avoids a second static catalog and validates inactive supported tools too.

A tool presentation entry uses template_success/template_failure, max_items, ordered collections/children, enum_cases, next_instructions and configured note groups. Collection/child/enum identities are mapping keys with unique sibling order ranks; DTO item order remains unchanged. See [configuration composition](config-loading-architecture.md).

Only exact list[T] and variadic tuple[T, ...] sequence annotations are supported, with scalar or Pydantic model items. Flat scalar sequences can appear in templates; structured sequences use declared collections. Each depth applies max_items independently. Arbitrary iterable discovery, sorting/filtering and tool-specific renderer branches are unsupported.

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

Successful output must have the declared field/container/item shapes. Generic failure DTOs may omit success-only collections; presentation never fabricates them. Startup rejects missing/unknown tool entries, duplicate names, unresolved output models, invalid placeholders/formatting, unsupported collections/children, invalid enum cases and inconsistent max_items declarations. A tiny positive budget is valid because required content can overrun it.

## Cache Representation and Client Guidance

The cache retains required nullable fields and explicitly supplied optional nulls; only unset optional null fields are omitted. Non-null defaults and ordinary JSON values (null, false, zero, empty containers) retain their existing representation. Complete and window reads use that same canonical JSON. A later resource serialization failure propagates to the existing read-resource error boundary, without a replacement completeness claim.

Inline JSON mode with aliases and the cache's canonical field-presence policy represent the same operation, without promising byte-identical JSON. Do not reconstruct facts from rendered Markdown.

Use the selected complete inline data when available; otherwise read the successful resource reference. Check size before paging and follow the [packaged cache guide](../../mcp_server/resources/cache_reading.md). The cache is transient/process-local; a run ID alone is not durable proof. Record exact invocation, scope and observed outcome in committed evidence. Never replay a mutation merely to recover cached details.

SchemaResourcePresenter maps attachment identity to schema://validation (application/json) or schema://template/<percent-encoded-template-id>/context (application/schema+json). The complete schema content travels in the selected data channel. Attachments never enter the operation cache.

Server publication proves the selected server output, not delivery to every downstream model context. Installation must verify the chosen client's actual presentation and full-data readback route; no harness-version compatibility matrix is built into the presenter.

## Configured Execution Evidence

run_checks, run_tests and apply_fixes use the same profile boundary. Inspect operation success/error_code separately from each native result's status, reason, evidence, adapter identity and capture. An accepted operation can contain a failed native check without becoming a protocol failure.

apply_fixes runs selected fixes in request order and stops when work cannot continue or a fix does not pass. Earlier native changes may exist; rollback is not promised. Inspect the result and affected files before an authorized narrow recheck. Presentation never chains another fix/check automatically.

## Primary Implementation and Evidence

- [Profile and presentation config](../../mcp_server/config/schemas/presentation_config.py)
- [Public envelope/value models](../../mcp_server/schemas/presentation_output.py)
- [Response presenter](../../mcp_server/presenters/response_presenter.py)
- [Protected text renderer](../../mcp_server/presenters/text_presenter.py)
- [Budget limiter](../../mcp_server/presenters/text_budget_limiter.py)
- [Startup recovery presenter](../../mcp_server/presenters/startup_recovery_presenter.py)
- [Cache resource](../../mcp_server/resources/cache.py)
- [Known-outcome recovery and missing-marker SDK cases](../../tests/mcp_server/integration/test_tool_attachment_transport.py)
- [Issue #528 validation](../development/issue528/validation.md)
- [Profile/SDK/serializer behavior tests](../../tests/mcp_server/integration/test_execution_presentation_v3.py)
- [Protected composition tests](../../tests/mcp_server/unit/presenters/test_text_presenter_composition.py)
- [Startup and instance-isolation tests](../../tests/mcp_server/integration/test_target_startup.py)
- [Issue #529 validation](../development/issue529/validation.md)

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
