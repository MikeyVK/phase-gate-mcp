<!-- pgmcp:v1 id=design pv=1.0.0 pf=Uk1D2XWpiag1c6nn sf=WI5iXHBKVOU91bYE -->

# Issue #528 — bounded response-processing recovery

**Status:** Design for owner inspection — not implementation approval  
**Version:** 1.0  
**Last Updated:** 2026-10-20

## Purpose

Define the exact response after a known operation when normal response processing fails, its construction owner, schema, preserved facts and limits. The owner approved the bounded guidance exception and requested this finished Design before any further progression.

## Scope In

Existing server response boundary; a minimal separate recovery entrypoint in the existing presentation layer; shared public models and profile projection; native diagnosis; directly affected behavior tests and active presentation documentation.

## Scope Out

Wrapper metadata forwarding, per-tool output schemas, a parallel server presenter, second normal renderer, independent profile/schema inventory, new exception framework, unconditional both-channel fallback, retrying the operation, harness/version matrices and compatibility paths. No production code is changed by this document.

## Problem Statement

Research on merge a7256c0a67cecb58a433861b3ed3a612bd1e3b6a shows normal schema publication was already delivered by #529/PR #531. Its remaining contract defect is the outer catch after a known operation: an unexpected presenter failure replaces the known outcome with bare isError=true and no structuredContent.

The actual operation and its attachments, raw notes and publication receipt still exist outside the failed call. Normal formatted guidance may not exist: main templates, enum explanations, next instructions and note advice are constructed inside TextPresenter. Research records independent Research→Design GO on39832b9b and the subsequent direct owner approval of a narrowly disclosed guidance exception.

## Functional Requirements

- Preserve the original operation success/error facts and available original result data.
- Report the later processing failure separately, through the existing public envelope.
- Keep isError equal to the actual operation's failure flag when an operation exists.
- Preserve source instruction fields and raw note facts; disclose that normal formatted guidance may be unavailable.
- Match the connected profile's channels and advertised schema; no unconditional extra channel.
- Catch outside the failed normal presenter invocation; do not rerun the operation or normal rendering.
- Preserve original exception/cause and distinguish processing failure from data-delivery failure.
- Do not fabricate an operation when none exists.

## Nonfunctional Requirements

- Existing models remain the authoritative field/type contract; the resolved profile remains the channel policy.
- Readable recovery wording remains in presentation configuration; server.py only orchestrates known facts and SDK transfer.
- Reuse the existing diagnostic DTOs, capture_exception, resource attachment converter, JSON conversion and text-budget primitives.
- Clean break, no legacy/compatibility path and no new per-error exception/DTO framework.
- Focused behavior coverage; adapt existing valuable tests rather than preserving old broken output or adding wording snapshots.

## Decision and Rationale

Choose one minimal separate recover() entrypoint on the existing IPresenter/ResponsePresenter. The server invokes it once after catching a response-processing exception with a known ToolExecution. It supplies the original operation, notes, attachments, any real publication receipt, and the captured native diagnosis.

The recovery method bypasses present(), TextPresenter, tool templates, enum/collection rendering and note-advice rendering. It uses one simple validated configured notice and the same internal data/profile/envelope projection used by normal responses. Calling a different independent method on the existing presenter instance does not repeat the failed normal call.

Add one nullable field, processing_error, to PublicToolResponse, using the existing ConfigErrorOutput | ExecutionErrorOutput diagnostic types. Keep delivery_error exclusively about unavailable operation-data delivery. This avoids classifying a rendering failure as serialization failure or forcing data=null when complete operation data remains available.

The owner-approved exception applies only here: normal formatted explanation/advice may be unavailable and the recovery notice must say so. Available source instruction fields and raw evidence are retained. Ordinary successful/normalized-error presentation keeps #529's full guidance requirements.

## Alternatives

| Alternative | Assessment |
|---|---|
| Minimal recovery on existing presentation responsibility | Chosen: preserves known facts and profile/schema ownership without normal rendering retry |
| Catch inside present() only | Insufficient: the observed fault can interrupt the whole call; outer boundary still needs recovery |
| Format a second response in server.py | Rejected: duplicates field/profile/presentation knowledge and violates the owner boundary |
| Rerun present_text() or a second instruction renderer | Rejected: may repeat the failing step and adds maintenance to regain a guarantee the owner has explicitly bounded |
| Use delivery_error for the presenter crash | Rejected: existing semantics concern unavailable data, while this recovery often retains full data |
| Keep bare isError=true after a known successful operation | Rejected by independent Research QA: loses operation facts and violates the structured contract |
| Repair wrapper output_model forwarding | Outside scope: current public catalog does not consume it |

## Production Design

### Construction ownership

| Component | Owns | Does not own |
|---|---|---|
| MCPServer.handle_call_tool | Original execution facts, native exception capture/logging, one recovery invocation, isError and transfer to SDK result | Recovery wording, channel policy, envelope field inventory or schema construction |
| IPresenter / ResponsePresenter.recover | Minimal configured recovery notice, bounded diagnostic projection, existing selected-profile data/envelope projection | Re-executing the tool or retrying normal text/template/collection rendering |
| PublicToolResponse / existing diagnostic models | Public fields, types and JSON-schema base | Configuration loading or workflow knowledge |
| ResponsePresenter.output_schema | Derivation/refinement for the same resolved profile | Independent tool-specific response definitions or catalog publication |
| ConfigLoader / presentation.yaml | Validated notice and existing immutable profile/budgets | Call-specific failure state |
| Existing SDK converter | Transfer of prepared text/structured output to MCP CallToolResult | Repairing or reinterpreting the operation |

Normal and recovery construction share the current projection logic inside ResponsePresenter: selecting data delivery, projecting attachments/processing diagnosis into the data channel, building PublicToolResponse and producing PresentedOutput. This is a cohesion refactor inside the existing class, not a new service, factory, policy engine or second presenter. It must not copy the current envelope construction into recover().

### Interface contracts

Add to IPresenter and its two production implementations:

```python
def recover(
    self,
    tool_name: str,
    data: BaseModel,
    diagnostic: ConfigErrorOutput | ExecutionErrorOutput,
    *,
    notes: list[NoteEntry],
    cache_pub: CachePublication | None,
    attachments: tuple[SchemaAttachment, ...],
) -> PresentedOutput: ...
```

The operation is the actual model returned by the normalized tool pipeline. diagnostic describes the later processing exception. notes and attachments are original invocation facts, not regenerated tool results. No new constructor dependency or separate fallback presenter is required.

In the shared PublicToolResponse contract, add:

```python
processing_error: ConfigErrorOutput | ExecutionErrorOutput | None = None
```

All existing fields remain. A normal response sets processing_error=null. In the selected data-bearing envelope, a non-null value means normal response processing failed and normal formatted guidance is not certified complete. It does not change operation success. There is no new processing-error subclass or success-only error union.

The existing [StartupRecoveryPresenter](../../../mcp_server/presenters/startup_recovery_presenter.py) implements the same method using its existing fixed, configuration-independent full-both-channels/inline contract and shared models. Its ordinary health/restart presentation is unchanged. It must not invoke its failed present() again. This is a required interface consumer adjustment, not a second normal-workspace recovery policy.

### Exact response semantics

| Field/fact | Known operation succeeds; later processing fails | Known operation fails; later processing fails |
|---|---|---|
| CallToolResult.isError | false | true |
| PublicToolResponse.success | true | false |
| data.operation or resource payload | Original successful operation | Original failed operation, including its own diagnosis |
| processing_error | Separate native diagnosis of the later failure | Separate native diagnosis of the later failure |
| delivery_error | null when operation data is available | null when operation data is available |
| Normal formatted guidance | Explicitly marked potentially unavailable | Explicitly marked potentially unavailable |

No operation, new cache URI or successful delivery is invented. A later error cannot turn written=true into written=false, or replace a real failed operation with a new unrelated failed DTO.

### Concrete default-profile response

Illustrative safe_edit_file success followed by RuntimeError in presentation. The operation below is intentionally shortened for readability; implementation must retain the complete original DTO. Text and JSON values shown are design examples, not an executed result.

```json
{
  "isError": false,
  "content": [
    {
      "type": "text",
      "text": "Response processing failed after the operation returned success=True. Normal formatted explanation and advice may be unavailable. Inspect the operation result before repeating an action."
    }
  ],
  "structuredContent": {
    "success": true,
    "presentation": "Response processing failed after the operation returned success=True. Normal formatted explanation and advice may be unavailable. Inspect the operation result before repeating an action.",
    "data": {
      "delivery": "inline",
      "operation": {
        "success": true,
        "path": "example.py",
        "written": true
      }
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
        "notes": [],
        "diagnostic_details_truncated": false
      },
      "error_code": null
    }
  }
}
```

The nested processing_error.success=false belongs to the existing diagnostic DTO. The top-level success=true and isError=false describe the actual operation. No new flag meaning is invented by the recovery code.

For an original failed operation, the two outer flags become success=false / isError=true; the original data remains and processing_error describes only the additional failure.

### Profiles and schema

| Existing profile | Recovery presentation | Complete original operation | Processing diagnosis / raw notes |
|---|---|---|---|
| structured_inline | Existing presentation selection (default both) | Inline in structured data | processing_error in structured data-bearing envelope |
| structured_resource | Existing presentation selection | Existing successful cache URI/size | Direct in structured data-bearing envelope, as attachments already are |
| text_inline | Text | Complete fenced JSON data segment | processing_error in that JSON segment; no structuredContent/outputSchema |

All other admitted combinations follow the same existing controls, not profile-ID branches. With data_channel=text, the full processing_error is in the JSON text data carrier. If presentation also selects structured, its presentation-only envelope has processing_error=null, data=null and empty attachments. The short recovery notice is complete in the selected presentation channel(s).

The schema is still derived from PublicToolResponse.model_json_schema() and refined by the resolved profile. Structured data admits the nullable existing diagnostic union; presentation-only structured output restricts processing_error to null just like other unselected data. The existing normal-versus-delivery_error alternatives remain about operation data availability. A retained-data processing_error does not require changing those delivery semantics.

Schemas describe the normal and recovery shape at catalog publication; no per-call schema mutation or catalog switch. Wholly textual profiles still advertise no structured schema. Do not rely on SDK is_error validation bypass.

### Raw facts and diagnosis

The original operation is neither altered nor wrapped in another operation DTO. Its phase_instructions, handover_template and post_tool_instruction fields remain where originally returned.

The server supplies capture_exception(primary_exception) without application context, so its diagnostic.params starts empty; native exception parameters remain separately in error_params. Recovery adds original notes as key/params facts under processing_error.params.notes and the diagnostic-shortening flag beside them. These are diagnostic context, not a claim that note advice was rendered. Do not overwrite native error_params or the original operation diagnosis. Use existing Pydantic JSON conversion, with textual representation for non-JSON diagnostic-context values, rather than a custom note serializer or silently dropping notes. No raw notes are added to the operation cache.

The full original processing exception/cause is logged at the existing server boundary. The existing max_cache_failure_detail_bytes allowance also bounds verbose processing diagnostic string details (error_message/traceback) supplied by recovery. Use UTF-8-safe excerpts before JSON serialization. Set params.diagnostic_details_truncated=true if shortened and append the configured processing-diagnostic truncation notice. The whole JSON carrier remains valid; never cut serialized JSON.

Original operation data, attachments, raw note facts and stable outcome/recovery notice are not diagnostic excerpts. Do not truncate them to fit that allowance. This does not introduce a new global MCP output ceiling.

### Presentation configuration

Add two validated entries to global.next_instruction_texts in the existing defaults presentation.yaml:

```yaml
response_processing_failed: >-
  Response processing failed after the operation returned success={success}.
  Normal formatted explanation and advice may be unavailable.
  Inspect the operation result before repeating an action.
processing_diagnostic_truncated: >-
  Response-processing diagnostic details were shortened; the full exception is retained in server logs.
```

The recovery notice accepts only the scalar success placeholder; validate nonempty values and placeholder syntax in the existing presentation configuration model. Use the already-loaded configuration, without tool-specific template selection or normal TextPresenter rendering. Ordinary cache guidance may refer only to an actual successful receipt. Never imply that a cache of the operation also contains the later processing traceback.

The recovery notice, any diagnostic-truncation notice and actual outcome facts are protected core. The approved exception concerns unavailable normal explanation/advice, not loss of this recovery notice.

## State and Failures

The broad existing server catch must distinguish whether ToolExecution was obtained. Before that point, keep the existing explicit error boundary; do not fabricate an operation or invoke this known-operation recovery method.

After that point, retain the operation, raw notes, raw attachments and any publication receipt. Capture/log the primary exception with known operation_success and invoke recover() once. Reuse the existing SDK transfer; do not call the tool or publisher again.

If operation data also cannot be delivered, retain existing truthful delivery_error behavior, never a fictitious reference. processing_error remains the diagnosis of the original processing failure; a failed publication receipt or serialization diagnosis is not overwritten by it. Recovering a valid cache reference must not claim that attachments or processing diagnosis are inside that cache.

This is a bounded single-failure recovery, not tolerance of arbitrary simultaneous failures in JSON conversion, attachment conversion, model construction or the SDK transport. If the minimal recovery/SDK transfer itself raises, preserve both causes and the known operation outcome in logs and propagate through the existing terminal SDK boundary. No third presenter, bespoke third wire shape, operation retry or falsely claimed recovered response. End-to-end delivery cannot be promised when delivery itself fails.

## Preservation

| Obligation | Carrier |
|---|---|
| Actual operation outcome and complete available result | Original model; existing inline/resource delivery |
| Source phase instructions and other instruction fields | Unchanged original operation |
| Original schema attachments | Existing selected data channel and identity conversion |
| Original note keys/parameters | processing_error.params.notes |
| Later failure and cause | Existing diagnostic DTO plus original server exception log |
| Unavailable normal formatted guidance | Protected configured recovery notice |
| Profile/schema authority | One resolved profile and shared envelope projection/model schema |
| Startup degraded recovery | Existing fixed configuration-independent policy |
| No repeated side effect | One tool execution; recovery has no tool/publisher dependency |

## Test Design

Adapt the existing processing-failure case in [test_tool_attachment_transport.py](../../../tests/mcp_server/integration/test_tool_attachment_transport.py), using real ResponsePresenter/profile/schema composition instead of a schema-less MagicMock. Preserve the independent unknown-tool check without treating it as the new known-operation path.

Use a small parametrized behavioral matrix: original success/original domain failure across the three shipped profiles. Supply input-derived operation fields, one raw note and one attachment. Inject a normal presenter or TextPresenter failure, assert one execution/no normal-render retry, preserve operation facts and attachments/note context, and explicitly validate advertised structured schemas even for isError responses. Read resource data through the existing resource route when selected. Assert semantics/identity, not exact production wording.

Extend the valuable existing presentation/profile tests only where necessary for the shared projection, mixed-channel diagnostic selection and UTF-8 diagnostic budget. A long native diagnostic must leave valid JSON, complete recovery notice and original data, with explicit shortening metadata. A bounded secondary recovery fault must not cause another recovery attempt or side effect.

Update the directly affected protocol test doubles in [test_presenter_interfaces.py](../../../tests/mcp_server/unit/core/interfaces/test_presenter_interfaces.py) and any targeted startup-recovery consumer. No permanent harness/version matrix, legacy-wire tests or temporary Research probe promotion. Planning owns case grouping and run timing.

## Validation Obligations

| Obligation | Planned evidence |
|---|---|
| Actual public catalog/schema remains truthful | Normal bootstrap/catalog evidence plus schema validation of new recovery responses |
| Primary defect removed | Original operation success and failure followed by presentation fault remain distinguishable |
| Failure independence | Failed normal methods not retried; one tool execution/publication |
| No parallel server presenter | Architectural review of server catch, shared models/projection, configuration and imports |
| Profile behavior | Selected presentation/data channels; deliberate text-only schema absence |
| Facts/diagnosis survive | Original DTO, notes, attachments, resource readback and original logged cause |
| Bounded diagnostics | Valid JSON and UTF-8 excerpts; no truncation of operation or protected recovery notice |
| Finite recovery | A secondary failure is terminal through existing boundary, with known outcome/cause logged |

These are requirements for later evidence, not claims of executed tests or Design approval.

## Planning Consequences and Review Boundary

No new constructor graph, persistent state, package, dependency or cache/retrieval API is required. Production surfaces are server.py, the existing presenter interface and its two implementations, presentation_output.py, and the existing presentation configuration/defaults; affected tests remain consumers of those boundaries.

Preserve the already-approved clean break. Correct the obsolete active presentation-reference reservation of wrapper metadata work during Documentation; historical #529 Research/Design remain contextual evidence. No implementation cycle sequencing is defined here.

The owner requested this Design first. Do not request a phase transition, start Planning/implementation or treat this artifact as owner Design approval. Independent Design review and any required strategy-amendment review follow only after the owner has inspected it and authorized continuation.

## Related Documents

- [Research and approved bounded strategy](research.md)
- [Architecture principles](../../../docs/coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [Current presenter interface](../../../mcp_server/core/interfaces/ipresenter.py)
- [Current response models](../../../mcp_server/schemas/presentation_output.py)
- [Current response presenter](../../../mcp_server/presenters/response_presenter.py)
- [Current text renderer](../../../mcp_server/presenters/text_presenter.py)
- [Current outer server boundary](../../../mcp_server/server.py)
- [Native diagnosis models](../../../mcp_server/schemas/error_outputs.py)

## Version History

| Version | Date | Author | Changes |
|---|---|---|---|
| 0.1 | 2026-10-20 | @imp designer | Record confirmed recovery seams and the missing guidance guarantee; leave final contract pending owner choice. |
| 1.0 | 2026-10-20 | @imp designer | Record owner-approved limits and finish concrete response, ownership, interface/model/profile contracts and bounded recovery for owner inspection before further progression. |
