<!-- pgmcp:v1 id=design pv=1.0.0 pf=Uk1D2XWpiag1c6nn sf=WI5iXHBKVOU91bYE -->

# Issue \#537 — Two response modes and independent attachments

**Status:** Design — independent review requested  
**Version:** 0.2  
**Last Updated:** 2026-10-20

## Problem Statement

Replace the previous independent profile matrix with one process-local structured/resource choice, keep a hard final normal-text byte bound and restore independently delivered attachments. Preserve the approved operation/cache/error ownership and startup exception.

## Functional Requirements

- Always emit readable normal inline text within the configured UTF-8 allowance, including footer/notices/fence closure; never append a full JSON text envelope.
- Use exactly structured/resource modes with instance-local launcher selection and an explicit shared default.
- Structured output includes complete operation facts, full rendered presentation and attachment references; resource mode has no normal structuredContent/outputSchema.
- Always deliver available attachments separately as MCP embedded-resource blocks, with configured references in both presentations.
- Keep truthful operation/error/cache/recovery semantics without replay, republish, instruction-cache duplication or new client knowledge.

## Nonfunctional Requirements

- Clean break: remove profile dictionary/classes/aliases/combination branches, reuse existing rendering/DTO/cache seams.
- Share pure typed configuration through ConfigLoader and constructor injection; keep all normal wording in presentation.yaml.
- Adapt existing behavior tests and construction helpers without a new client/version matrix or broad test rewrite.

## Constraints

- No active server/profile change, restart, external rollout or release action is part of this source change.
- Configuration-independent startup recovery retains its fixed dual-channel complete diagnosis exception.
- Instruction truncation remains noted; no new speculative instruction-preservation package.

## Options

### 1. Keep arbitrary named profiles with only two shipped definitions

Retains independent-channel state and invalid/unneeded combinations despite a smaller example config.

**Cons:**

- Does not remove the evidenced structural complexity or enforce the owner's selected contract.

### 2. Two modes at existing presentation boundary (selected)

One literal selection, shared budgets, separate attachments and one final text projection.

**Pros:**

- No extra dispatch framework or loader; aligns transport and schema with the two supported modes.

## Decision

Use two modes in the existing presenter. Default to structured, preserving the current default's text-plus-structured operation route while removing arbitrary profile combinations. Restore native attachments independently of this choice.

## Rationale

The owner delegated concrete key/default/interface decisions within the approved strategy. Keeping the current default's delivery family minimizes unrelated installation changes. Resource is an explicit deployment choice requiring an agent-accessible cache reader; it cannot safely be inferred from a client name.

## Production Design

### Ownership and concrete configuration

Define ResponseMode = Literal["structured", "resource"] once in presentation_config.py. GlobalPresentationConfig.response_mode is required; shipped defaults explicitly set structured. Retain max_text_response_bytes=8000, max_cache_failure_detail_bytes=8000 and cache_read_budget_chars=6000 as shared values. Remove ResponseProfileConfig, ResolvedResponseProfile, response_profiles and default_response_profile.

ServerSettings.response_mode: ResponseMode | None = None is the process-local selector. Settings.from_env reads PGMCP_RESPONSE_MODE, overriding the optional launcher YAML server.response_mode; absent selection uses the loaded presentation global.response_mode. PresentationConfig.resolve_response_mode(selector: ResponseMode | None = None) -> ResponseMode returns this pure composition. Bootstrap passes mode and global_config into ResponsePresenter. There is no old-key alias/translation, shared workflow selector or unknown-mode fallback.

### Concrete internal/public contracts

| Contract | Shape / change |
|---|---|
| ResponsePresenter constructor | Existing text_presenter and resource_presenter plus mode: ResponseMode and global_config: GlobalPresentationConfig. Shared config owns budgets/wording; no resolved-profile object. |
| RenderedPresentation | Keep core/details for the text renderer's useful separation. They no longer imply protected-overrun privilege. Full presentation is their shared rendering before the final inline limiter. |
| PresentationResource | Existing frozen uri, mime_type and content; use only for independent attachment transport. |
| AttachmentReference | Frozen uri and mime_type, derived from the same formatted attachment; no content field or independent schema lookup. |
| PresentedOutput | text: str or None retained for startup/interface compatibility of meaning; resources: tuple[PresentationResource, ...] added; structured_content unchanged. Normal present/recover always provide text. |
| PublicToolResponse | Keep success, presentation, data, delivery_error, processing_error. Change attachments to tuple[AttachmentReference, ...]. Keep full operation-owned schema values. |
| TextBudgetLimiter | Constructor max_text_response_bytes: int. limit(body: str, *, footer: str, truncation_notice: str) -> BoundedPresentation. excerpt remains the existing bounded native-string primitive. No mode/cache/template knowledge in this class. |

Normal server delivery transfers the already presented text, then each resources item as a native MCP embedded resource with uri/mimeType/text, and assigns structured_content. It does not format guidance or select schema. SchemaResourcePresenter and attachment producers retain their current contracts; IResourcePresenter requires no new routing responsibility.

### Configured footer and attachment references

Keep existing uri_reference and pagination_reference, and add literal structured_reference and attachment_reference entries under global.next_instruction_texts. attachment_reference generically points to the supplied separate resource blocks, without manufacturing read_resource support for schema:// identities. The structured attachments metadata supplies exact URI/MIME facts as well. Text and structured presentation use the same attachment notice.

Use formatting.truncation_notice for the availability-neutral notice that text was shortened and the indicated supplementary route/attachments should be consulted. Keep the existing no-cache/unavailable truncation notice for cases with no complete supplementary result. The footer names structured output only when the full inline operation serialization succeeded; resource guidance appears only for an existing successful publication. Do not promise that optional notes excluded by a deliberate projection are in the raw-operation cache.

Footer ordering: generic attachment notice when resources exist, then the selected complete-data route notice, with pagination guidance joined to a real cache reference when needed. A successful structured result need not advertise an additional cache locator even if infrastructure still publishes one.

### Full structured presentation versus bounded text

Render normal text once. Compose its complete core/details, applicable attachment notice and truthful route footer. In structured mode, PublicToolResponse.presentation receives that full rendered value before final inline truncation; data is complete InlineOperation and attachments are metadata references only. Independently limit the inline text body while reserving the same footer and any required truncation notice. This protects structured instructions without implying an unbounded inline channel.

In resource mode, data stays in the existing operation cache. Only bounded text plus independent attachments are transmitted. Full rendered text is not added to that cache. The cache's existing serialized operation and paging identity remain unchanged.

### Publisher serialization guard

MCPServer publishes before presentation. Treat CachePublication.error_code=serialization_failed as a prior failed full operation serializer in either mode. At ResponsePresenter entry, inspect that receipt before calling TextPresenter or any full operation model_dump/model_dump_json, traversal or JSON conversion. Do not attempt the structured operation projection after that failure. Only known success, the existing bounded native diagnostic and independent attachment facts may be processed; never feed the original operation into the compact failure assembly. Format separate attachments independently once if available, without touching or retrying the operation.

Reuse the presenter's existing compact configured failure machinery, not a server-side replacement presenter. Add a fixed outcome notice with the same restricted success scalar vocabulary as response_processing_failed; pair it with operation_serialization_failed and the truthful unavailable footer. The structured delivery-failure variant has data=null, delivery_error.code=operation_serialization_failed, its details_truncated fact, processing_error=null and attachment references. The primary publisher diagnosis is retained as a bounded labelled excerpt in presentation; the raw operation is not claimed to be available. Resource mode emits the corresponding bounded readable facts and separate attachments without structured content. No mode promises normal rendered instructions after its full operation input cannot safely be processed; this is the existing explicit delivery-failure exception, not successful complete delivery.

A cache storage/publication failure after successful canonical serialization is different: write_failed (or another non-serialization publication failure) does not preclude one independent structured JSON-mode conversion. If that succeeds, deliver the actual complete structured result; if it fails, retain its original diagnosis in the existing delivery-failure variant. The guard does not retry either serializer or republish. A later presenter/transport exception retains the separate server-to-recover path and processing_error variant below.

### Final limiter and feasible budgets

The limiter counts UTF-8 bytes after joining all text parts. If body plus footer fits, preserve it. Otherwise reserve truncation notice, separators and the complete footer, shorten only the body prefix with existing readable UTF-8/fence handling, and report truncation. Never slice serialized MCP JSON or attachment content.

At config validation, require nonempty route/attachment/recovery notices and validate their small literal/scalar placeholder vocabulary. uri_reference may interpolate only run_id without width/conversion; response_processing_failed may interpolate success. The other footer notices are literal. For minimum-budget feasibility, use the conservative sum of all configured fixed footer/recovery notices, an expanded 32-character cache ID, both bool spellings' larger recovery notice, separators and fence-closure reserve. Reject a budget that cannot hold this configured reserve at startup; do not silently enlarge it. This is a derived validation, not another user setting. The limiter also refuses an impossible supplied footer budget through ConfigError, because it is a generic public seam.

Attachment-reference wording is fixed-size: one generic notice points to all actually supplied embedded blocks; exact per-attachment identities live on the blocks and in structured metadata. No unbounded list of URIs is reserved inside a small footer.

## Test Design

Use the existing make_response_presenter helper with a typed optional mode selector, not a parallel testing renderer. Existing config/settings cases prove the explicit default/launcher/env path, invalid values and feasible budgets. Existing limiter cases become final byte-bound tests including UTF-8, fences, footer and exact under-budget preservation; the oversized-core expectation is replaced rather than retained as an old-behavior rejection. Existing SDK integrations exercise both modes, full structured instructions beyond inline clipping, exact operation roundtrip/cache paging and independent attachment bodies plus URI/MIME references. Adapt the existing independent serialization-failure case with the real serializing ResponseCacheManager and call counters: a failing canonical serializer is called once, normal rendering and the subsequent JSON-mode operation serializer are not called, and the original outcome/diagnosis/unavailable footer remain. Keep a separate storage-failure case proving successful inline delivery is still allowed. Reuse the existing processing-failure tests to verify known outcome, schema-valid recovery, no duplicate execution/publication/normal rendering and bounded native diagnosis. Test dynamic markers and facts, not production prose snapshots. No harness-specific tests or speculative instruction loss case.

## State and Failures

| Case | Normal text / structured result |
|---|---|
| Structured, no earlier serialization failure | Complete structured operation and full presentation; bounded text ends with structured notice. A cache storage failure after successful serialization may remain visible but cannot negate available inline facts. |
| Publisher reports serialization_failed, either mode | No normal renderer or further full operation serialization/traversal. Known outcome plus bounded publisher diagnosis and independently formatted attachments only. Structured: data=null, delivery_error.code=operation_serialization_failed, processing_error=null. Footer says complete data unavailable; resource mode has no structured content or fake URI. |
| Resource, publication succeeds | Bounded text with real URI and optional paging advice; no structuredContent/schema. |
| Resource publication fails | Preserve actual operation outcome and configured failure notice; append only bounded labelled diagnostic excerpt, then apply the final text bound with truthful unavailable footer. Do not retry serialization/publication or emit fictitious resource access. |
| Structured serialization fails | Preserve delivery_error and actual outcome; existing cache reference may be offered if already published. Otherwise mark full data unavailable. Keep a schema-valid failure variant and bounded diagnostic projection; no repeat full serializer. |
| Presenter/transport processing fails after operation | Existing server boundary calls compact recover once with known success, bounded native diagnostic and any existing cache reference. No normal renderer, attachment formatter, operation or publisher replay. Recovery emits bounded text in either mode; structured mode also retains existing compact processing_error facts and optional ResourceOperation. Failed/unavailable recovery still uses existing terminal error/log boundary. |
| Unknown tool / failure before known operation outcome | Existing entrypoint behavior remains; no fabricated success or result cache. |
| Startup configuration recovery | Retain its fixed text + structured diagnosis, without reliable config/cache/mode selection. The shared attachment carrier/reference types may change mechanically, but health/restart diagnosis completeness and recovery behavior do not. |

The normal recover path uses the same final limiter but only fixed notice strings plus bounded message/traceback facts. Detailed native diagnosis remains in structured processing_error when selected; resource mode exposes the bounded readable diagnosis and only an already existing operation cache locator. No new storage claim or diagnostic-loss policy is introduced.

## Preservation

Tools/managers/adapters and public operation DTOs remain unchanged. ResponseCacheManager still publishes only the operation before presentation and CachedResponseResource still handles complete/paged reads. ToolExecution/SchemaAttachment remain the ownership contract. isError stays derived from operation_success. ConfigLoader remains the sole shared config reader. Startup exception, cancellation, primary/secondary error ownership and existing serialization-failure variants remain.

## Transition and Cleanup

One source/config cutover removes the old selector, profile classes/dictionary and JSON text path. Remove obsolete profile combinations/oversized-core expectations, preserving valuable negative/error cases. Update existing shared presenter factory and directly affected constructors. Current docs cover PGMCP_RESPONSE_MODE, shared default, two routes, separate attachments, final text budget and startup exception. No bridge, new reader or legacy-only negative suite. Active deployed configuration/runtime is not switched by tests or source edits.

## Validation

### Final normal text cap

**Method:** Existing limiter/public presenter behavior cases with Unicode, fences, configured footer and oversized input.

**Expected Result:** Measured UTF-8 length including notices/footer never exceeds configured allowance; exact small result preserved.

### Two-mode delivery and attachment separation

**Method:** Existing real SDK execution and independent-attachment integration cases, both modes.

**Expected Result:** Same operation outcome; native separate attachment content present; structured metadata has no body; resource readback real; schema presence matches mode.

### Error ownership and bounded recovery

**Method:** Existing failure/poisoned-payload cases and same-workspace isolation case.

**Expected Result:** No operation replay, republish, fake URI or second full serializer; truthful schema-valid outcome and bounded normal text; startup exception intact.

## Planning Consequences

Keep production/config and their direct tests together at coherent contract boundaries; use focused Implementation gates and full configured/native Validation at its owning phase. No active restart/profile switch. Preserve the #536 branch; main merge and subsequent #536 integration remain Coordination responsibilities after Ready.

## Related Documents

- [Approved Research](<research.md>)
- [Inherited owner decisions](<../../issue536/response-delivery-research.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-20 | @imp designer | Define two-mode configuration/transport, final text budgets, independent attachments and preserved recovery at existing seams. |
| 0.2 | 2026-10-20 | @imp designer | Resolve QA P2 with an explicit prior-serialization guard, distinct storage-failure route, bounded diagnostic/schema variant and real publisher call-count proof. |

