<!-- pgmcp:v1 id=design pv=1.0.0 pf=Uk1D2XWpiag1c6nn sf=WI5iXHBKVOU91bYE -->

# Issue #528 — compact response-processing recovery

**Status:** Compact recovery contract — implementation under reviewed strategy  
**Version:** 1.3  
**Last Updated:** 2026-10-20

## Purpose

Specify the owner's approved compact recovery: known operation outcome, short notice, bounded diagnosis and optionally an already-existing successful cache reference. Show the exact response and construction responsibility before further progression.

## Scope In

Outer known-operation error boundary; minimal recover() in the existing presentation layer; shared public response models/schema; existing presentation/data channels; small invocation facts and bounded diagnostic text; focused behavior evidence.

## Scope Out

Original operation payload, source instruction fields, raw notes, attachments, new publication or retrieval, normal data/profile projection, normal rendering, parallel server presenter, another renderer/framework, metadata forwarding, per-tool schema, compatibility routes and harness/version tests. Normal successful/normalized-error output retains its existing behavior.

## Problem Statement and Decision History

Normal catalog schema publication was already delivered by #529/PR #531. The remaining defect is a bare processing error after a known operation: it hides the operation outcome and fails the connected structured contract.

The owner approved truthful recovery outside the failed call and a disclosed guidance exception. Design1.0 then reused normal profile/data projection and resent full result/attachments/raw notes. The owner correctly identified that this can repeat the same conversion/large-payload cause; it is not necessarily a separate secondary fault.

The owner's latest explicit decision supersedes that full-data promise: only known outcome, short notice, bounded diagnosis and optional already-existing reference. The owner requested this concrete amended Design first. Research1.3 records the policy; earlier Research→Design GO is not approval of this amendment or of implementation.

## Requirements

- Preserve the actual operation's known boolean outcome; do not claim it was never executed.
- Return one compact, truthful recovery response, without inspecting, serializing or resending the original payload/notes/attachments.
- Do not call normal data projection, present(), TextPresenter, collection rendering, tool execution or publication.
- Include a cache reference only from an already-successful receipt; never create or probe it during recovery.
- Use the already-resolved presentation/data channels. Do not let normal data_delivery=inline trigger full-payload replay.
- Bound diagnostic strings before envelope/SDK serialization; no native params or arbitrary diagnostic objects.
- Keep one public model/schema authority and presentation configuration source; no recovery UI/schema/profile inventory in server.py.
- Attempt recovery once; no third presenter or operation retry. Do not promise delivery through a broken SDK/transport.
- Clean break and proportionate public-boundary behavior tests; no legacy format or content snapshots.

## Chosen Design and Rejected Alternatives

Choose a separate small recover() method on existing IPresenter/ResponsePresenter. Unlike Design1.0, its interface cannot accept an operation DTO, notes, attachments, native diagnostic DTO with arbitrary params, or a failed publication receipt.

The server supplies only the known boolean outcome, native diagnostic string fields, and UUID/size from a receipt that already succeeded. recover() clips those strings, selects small values using existing channel flags, and constructs the shared PublicToolResponse directly. It does not call the normal large-data projection. Shared typed models and small channel predicates preserve SSOT; reusing the potentially failing data pipeline does not.

| Alternative | Disposition |
|---|---|
| Compact separate entrypoint using shared models/small channel flags | Chosen; independent of original payload size/conversion |
| Reuse normal profile/data projection or full DTO serialization | Rejected; may repeat the original cause |
| Retry normal renderer or introduce another renderer | Rejected; no operation/guidance replay |
| Build recovery presentation/schema in server.py | Rejected; violates the owner boundary |
| New cache publication or automatic inline dump when cache is missing | Rejected; adds work/payload to the failure route |
| Bare error with unknown operation outcome | Rejected; original defect remains |
| Unconditional dual-channel output | Not selected; preserve configured channel choices |

## Construction Ownership

| Component | Responsibility |
|---|---|
| MCPServer | Remember the known outcome before normal presentation; log/capture original exception; extract existing successful receipt scalars; invoke recovery once; transfer prepared output and actual isError |
| ResponsePresenter.recover | Short configured notice; bounded diagnostic strings; optional small ResourceOperation; selected channels; shared model construction |
| PublicToolResponse / ExecutionErrorOutput / ResourceOperation | Authoritative fields/types and JSON-schema base; no original operation object inside the recovery result |
| ResponsePresenter.output_schema | Advertise both normal profile shape and the compact recovery alternative, using the same models and resolved channels |
| Existing presentation config/loader | Validated short wording, existing diagnostic allowance and immutable channel selection; no second loader |
| Existing SDK boundary | Serialize/send only the small prepared recovery result; no interpretation of operation facts |

The server never calls operation.model_dump(), serializes attachments or notes, formats recovery advice, invents a resource URI or reconstructs a failed response. It retains the original DTO internally without sending it into recover().

## Exact Interface and Model Contracts

### Recovery entrypoint

Both production implementations of IPresenter implement this clean-break addition:

```python
def recover(
    self,
    *,
    operation_success: bool,
    error_message: str,
    traceback: str | None,
    cache_run_id: str | None,
    cache_size_chars: int | None,
) -> PresentedOutput: ...
```

operation_success is the already-known actual outcome, not inferred from the exception. error_message/traceback are native textual diagnosis only; they may be long inputs but are bounded before output construction. The server uses existing exception capture without application context and passes no error_params/params, model, notes, attachments or exception object into this method.

cache_run_id is either the already-validated 32-hex ID of a successful CachePublication or null. A missing/failed/not-yet-returned receipt yields both cache arguments null. No cache reader or publisher is called. URI construction uses the existing presentation-owned convention and ResourceOperation model, not server formatting.

### Shared response

Retain the existing PublicToolResponse fields and add:

```python
processing_error: ExecutionErrorOutput | None = None
```

Normal output sets processing_error=null. A non-null value marks the compact recovery alternative. Build a new minimal instance of the existing ExecutionErrorOutput from bounded error_message/traceback, with error_params={}, error_code=null, and params containing only diagnostic_details_truncated. Do not serialize/copy a captured diagnostic DTO with arbitrary context.

Recovery field rules:

| Field | Rule |
|---|---|
| success | Actual known operation_success |
| presentation | Complete short notice in the selected presentation channel(s) |
| data | Existing ResourceOperation reference or null; never InlineOperation |
| attachments | Always empty; do not inspect original attachments |
| delivery_error | null: recovery performs no new full-data delivery attempt; omitted full result is explicit in the processing-recovery contract/notice |
| processing_error | Minimal existing diagnostic DTO in the selected data-bearing envelope; no original result/notes/params |

Nested diagnostic.success=false describes the later failure; it does not replace the original outcome. A known failed operation produces outer success=false / isError=true; a known successful operation produces success=true / isError=false.

### Concrete default-profile response with an existing cache receipt

This is a design example, not an executed call. The referenced operation may be large; none of it is copied into this response.

```json
{
  "isError": false,
  "content": [
    {
      "type": "text",
      "text": "The operation reported success=True, but response processing failed. This recovery response does not include the full result or normal guidance. Verify the actual outcome before repeating the operation.\n\nResult: pgmcp://cache/runs/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
  ],
  "structuredContent": {
    "success": true,
    "presentation": "The operation reported success=True, but response processing failed. This recovery response does not include the full result or normal guidance. Verify the actual outcome before repeating the operation.\n\nResult: pgmcp://cache/runs/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "data": {
      "delivery": "resource",
      "uri": "pgmcp://cache/runs/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "size_chars": 1536000
    },
    "attachments": [],
    "delivery_error": null,
    "processing_error": {
      "success": false,
      "error_type": "ExecutionError",
      "error_message": "RuntimeError: presentation unavailable",
      "traceback": "Traceback (most recent call last):\n...\nRuntimeError: presentation unavailable",
      "error_params": {},
      "params": {
        "diagnostic_details_truncated": false
      },
      "error_code": null
    }
  }
}
```

### Without an existing successful cache publication

The same compact response has data=null. Replace the reference line in presentation/content with:

> No successful cache publication is available for this operation.

Keep the actual outcome and bounded processing_error; do not substitute an inline payload, create a URI, rerun publication, or claim the original operation failed. The complete result is not guaranteed recoverable.

## Channels and Advertised Schema

Normal profiles are unchanged. Recovery consults only already-resolved presentation_channel/data_channel flags; it does not evaluate the normal payload projection or use data_delivery to serialize original data.

| Selection | Compact recovery carrier |
|---|---|
| structured_inline / structured_resource defaults | Short notice per existing presentation selection; small recovery envelope in structuredContent |
| text_inline | Short notice and small fenced JSON recovery envelope in content; no structuredContent/outputSchema |
| Other supported combinations | Same existing channel controls; no profile-name/client branches or extra unconditional channel |

For a data_channel=text profile with structured presentation, the structured presentation-only envelope has data=null, processing_error=null and no attachments; the JSON text data carrier contains the bounded diagnosis and optional reference. This follows the existing separation of presentation and data.

A cached ResourceOperation reference is allowed in compact recovery even when normal data_delivery=inline. This is the owner-approved recovery exception, not a profile mutation or promise that the harness can read resources. A real existing reference is a location hint; availability, later eviction and harness access are not certified. The cache still contains only the operation, not original attachments/notes or the later diagnosis.

output_schema() remains derived from shared models and fixed for the connected catalog lifetime. Its alternatives distinguish:
- Normal output: processing_error=null; existing profile-specific normal/delivery-error variants.
- Compact recovery: processing_error present in the selected data carrier; data limited to ResourceOperation|null, attachments empty, delivery_error=null.
- A structured presentation-only projection keeps unselected data/diagnosis null; wholly textual output deliberately has no structured schema.

Do not weaken normal inline/resource constraints merely to admit recovery. Do not construct a per-call schema or duplicate the model's field inventory in server.py. SDK error-validation bypass is not conformance evidence.

## Diagnostic and Size Bounds

Use the existing resolved max_cache_failure_detail_bytes allowance (default 8000) as one shared UTF-8 budget for error_message and traceback in recovery: message first, traceback only from remaining allowance. Bound each candidate string prefix before passing it to an excerpt primitive that encodes its argument, then enforce the remaining UTF-8 byte budget. This prevents recovery from encoding an unbounded diagnostic before truncation. Do not concatenate or JSON-serialize a whole exception/operation/context and then trim it.

Set processing_error.params.diagnostic_details_truncated=true if either native string was shortened. The original full exception/cause stays in existing server logs; the optional cache reference does not point to that diagnosis. Diagnostic text may be an excerpt, while the enclosing JSON remains complete and valid.

Only bounded string fields, the known boolean, fixed empty containers, one truncation boolean, and optional UUID/size enter recovery serialization. No raw notes, native exception params, source instructions, original model fields, schema bodies or collections. Recovery output size therefore does not scale with original operation/attachment/note size.

The short configured notice, reference/no-reference line and any truncation notice are protected. Configured wording may affect their size; this is not a new hard whole-wire byte limit. JSON escaping and selected channel copies have ordinary encoding overhead. No in-process routine guarantees delivery after memory exhaustion, SDK failure or transport loss.

## Presentation Configuration

Use the existing presentation defaults/config loader; no new settings file or renderer. Add validated global.next_instruction_texts entries:

```yaml
response_processing_failed: >-
  The operation reported success={success}, but response processing failed.
  This recovery response does not include the full result or normal guidance.
  Verify the actual outcome before repeating the operation.
recovery_cache_unavailable: >-
  No successful cache publication is available for this operation.
processing_diagnostic_truncated: >-
  Response-processing diagnostic details were shortened; the full exception is retained in server logs.
```

Validate nonempty values and allow only the scalar success placeholder on the first entry. The ordinary uri_reference is reused only for a successful already-existing ID; no new cache work. No tool template, enum, collection or note formatting is invoked.

StartupRecoveryPresenter implements the same small interface in its existing configuration-independent presentation responsibility. Its normal recovery-tool output stays unchanged. If that normal presentation itself fails, this bounded response contains only outcome/notice/diagnosis; it has no cache reference and uses the already-approved fixed-both-channels startup contract. Its wording belongs in that existing presenter, not the server, and no separate fallback presenter is added.

## Error Boundaries and State

1. After execution returns, remember the known outcome before normal response processing. Do not serialize the operation to obtain that boolean.
2. If later processing fails, log the primary exception/cause and known outcome, then invoke recover() once with only the small inputs above.
3. Do not call tool.execute, publisher.put, normal presenter/data projection, resource reads or original object conversion.
4. If minimal recovery or SDK transfer fails, preserve both causes/outcome in the existing logs and terminal SDK boundary. No third response format, another recovery attempt or repeated operation.

A failure before an outcome exists does not fabricate one or enter this known-outcome method. No persistent workflow/state/cache ownership change.

The original operation is not mutated. The explicit exception means the recovery response does not promise its full data, source instructions, attachments or raw notes. Only an already-existing cache reference may offer a later read route; it is not guaranteed recovery or a new retrieval mechanism.

## Focused Behavior Evidence

Adapt the existing public SDK processing-failure test rather than promoting the temporary Research script. Cover known success and known operation failure, existing-reference/no-reference, and the three shipped profiles with a proportionate parametrized matrix. Assert actual flags and compact shape; explicitly validate advertised schemas even for error outcomes.

Decisive evidence must include:
- An original payload whose conversion raises: compact recovery still succeeds and does not call its serializer/normal data projection.
- Very large original operation/attachments/notes: none appear in the response or enter recovery, whose size remains independent of them.
- Bounded long Unicode diagnosis: only a bounded prefix enters UTF-8 encoding; valid complete JSON, explicit truncation, correct original outcome.
- No repeated tool execution/publication/normal presentation, cache probe or retrieval; an existing reference remains exact.
- No-reference case: data=null, explicit unavailable notice, no inline fallback.
- Secondary failure: one recovery attempt only, original outcome and both causes logged.

Reuse existing profile/interface/startup test seams and shared SDK client helpers; tests prove input-derived behavior rather than wording/config file snapshots, legacy output or dependency versions. Planning owns the exact grouping/run timing. No tests or production changes are claimed by this Design.

## Owner Inspection and Later Review

The prior owner-inspection stop was lifted on 2026-10-20. Coordination relayed the direct owner instruction from the Co chat: “Pak je coordinatie rol weer op en zorg dat de uitvoer verder doorloopt, er zijn naar mijn idee geen beleidsbeslissingen meer nodig van mij op dit punt.” Source: Coordinatie, thread 01a013b6-356c-7f41-a0ad-ca30b843a991; no owner message ID was supplied or invented. This releases autonomous execution only within the already-approved compact boundary; it does not select a new policy or replace independent QA. Request strategy-amendment and Design→Planning review at the exact pushed commit; progress only on actual GO and subsequent workflow gates. A genuinely new or contradictory policy/scope question still returns to the owner.

The compact concrete response has been shown to the owner. Coordination reconfirmed the existing direct owner release after this preview: continue autonomous implementation within the approved compact boundary and independent phase gates. Version1.3 clarifies pre-encoding diagnostic bounding already required by Planning; it introduces no new policy, interface or scope. No live recovery behavior or completed verification is claimed by the example.

Only documentation is changed in this revision. Later active presentation documentation must explain this bounded exception and remove obsolete wrapper-metadata repair reservations; historical #529 documents remain contextual evidence.

## Related Documents

- [Research and latest owner strategy](research.md)
- [Architecture principles](../../../docs/coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [Existing presenter interface](../../../mcp_server/core/interfaces/ipresenter.py)
- [Shared response models](../../../mcp_server/schemas/presentation_output.py)
- [Existing response presenter](../../../mcp_server/presenters/response_presenter.py)
- [Existing server boundary](../../../mcp_server/server.py)
- [Existing native diagnosis capture](../../../mcp_server/core/error_handling.py)
- [Existing SDK behavior tests](../../../tests/mcp_server/integration/test_tool_attachment_transport.py)

## Version History

| Version | Date | Author | Changes |
|---|---|---|---|
| 0.1 | 2026-10-20 | @imp designer | Record recovery seams and missing guidance guarantee pending owner choice. |
| 1.0 | 2026-10-20 | @imp designer | Define full-data recovery for owner inspection; subsequently superseded due to repeated conversion/large-payload risk. |
| 1.1 | 2026-10-20 | @imp designer | Apply owner's compact outcome/notice/bounded-diagnosis/existing-reference decision; remove full payload inputs/projection/replay and show amended response before progression. |
| 1.2 | 2026-10-20 | @imp designer | Record direct owner release relayed from Co chat, lift inspection stop within approved scope and request independent strategy-amendment/Design review; no new policy or phase GO. |
| 1.3 | 2026-10-20 | @imp designer | Clarify diagnostic bounding before encoding, show the compact response, and retain autonomous continuation under the existing owner release. |
