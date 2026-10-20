<!-- pgmcp:v1 id=design pv=1.0.0 pf=Uk1D2XWpiag1c6nn sf=WI5iXHBKVOU91bYE -->

# Issue \#528 — response-processing recovery boundary

**Status:** Design draft — mandatory-guidance recovery decision pending  
**Version:** 0.1  
**Last Updated:** 2026-10-20

## Purpose

Design the smallest correction after a known operation when normal presentation fails. Record the remaining mandatory-guidance policy choice before selecting a recovery contract.

## Scope In

Outer response-processing boundary, actual outcome preservation, common model/profile/schema coherence and independence from failed rendering.

## Scope Out

Wrapper metadata forwarding, per-tool output schemas, compatibility routes, a second renderer, new exception framework, harness-specific behavior, and implementation before the owner decision.

## Problem Statement

The server currently catches an unexpected post-operation presenter failure and returns only isError=true/text diagnosis. It loses the known outcome from the response and omits structuredContent despite a connected structured schema. Research→Design was independently approved on39832b9b. Design inspection exposes a remaining constraint: a rendering-free recovery can preserve the actual operation, but some mandatory guidance exists only in presentation configuration and has not yet been rendered.

## Functional Requirements

- Retain an existing actual operation's success/error facts and distinguish the later processing failure.
- Keep the connected schema truthful for structured recovery responses; retain intentional text-only schema absence.
- Reuse shared public models, selected profile and presentation configuration; no second server schema/profile inventory.
- Do not repeat the tool operation, normal present(), failed text rendering or collection rendering as the recovery strategy.
- Preserve native exception/cause and attachments/available publication facts through existing boundaries.
- Do not silently claim all mandatory guidance survived when its rendering failed; owner decision is required for a narrowly disclosed exception.

## Nonfunctional Requirements

- Keep the repair bounded to existing server/presentation/contracts and directly affected behavior tests.
- Clean break; no legacy/compatibility paths, version/harness surveillance tests or wording snapshots.
- Do not turn server.py into a second presenter or add an independent configuration reader.
- Prefer adapting existing transport/profile tests and reuse Research probes until source changes invalidate them.

## Constraints

- Existing #529 policy requires short text and mandatory instructions to survive selected routes.
- The direct owner supports truthful recovery outside the failed presenter and explicitly requested the SSOT check. This does not itself approve dropping normally rendered mandatory guidance.
- The owner has not approved unconditional dual-channel recovery, a protocol-only exception, or a new renderer.
- No production/configuration/permanent test changes are included in this draft.

## Options

### 1. Rendering-free recovery through the existing response contract

Server catches outside the failed present() call. A separate recovery entrypoint on the existing presentation responsibility can reuse the same model/profile projection, retain the actual operation and original evidence, and issue a configured processing-failure notice. It does not run the failed normal renderer again. Missing normal rendered guidance must be explicitly disclosed.

**Pros:**

- Small, focused repair within existing layers.
- Actual operation and the later processing failure remain distinguishable.
- No independent server schema or duplicated normal renderer.

**Cons:**

- Requires a bounded owner-approved exception to the normal mandatory-guidance guarantee.
- Raw note facts are not equivalent to rendered advice; carrying them directly requires a shared response-contract decision.

### 2. Regenerate the full normal protected core

Attempt to produce all main-template, enum-case, instruction and note text again through another rendering route.

**Pros:**

- A successful independent renderer could reproduce more normal explanation.

**Cons:**

- The current system has no such independent route.
- Calling the same renderer/helper again can repeat the original defect.
- A second general renderer broadens architecture and maintenance; it is not the focused correction requested.

### 3. Keep the existing bare processing error

Return the present catch response without a known operation or structured envelope.

**Pros:**

- No implementation cost.

**Cons:**

- Independent QA already rejected unconditional closure on this behavior.
- Does not satisfy known-outcome preservation or the published structured contract.

## Decision

Pending one explicit owner choice: may an unexpected post-operation presentation failure disclose that normal rendered explanation/guidance is unavailable, while preserving the actual operation and available original evidence via the selected output routes? Recommend the bounded rendering-free direction; do not implement or treat the exception as approved before the answer.

## Rationale

The server still owns the actual operation, notes, attachments, publication receipt and caught exception. The existing presenter owns the immutable profile and configuration. These are enough for bounded delivery recovery without forwarding wrapper metadata. They are not proof that configured advice which never rendered has survived.

## Questions

- Owner: accept the narrow disclosed exception that normal rendered guidance may be unavailable after its own unexpected rendering failure, while preserving original operation/evidence and a truthful configured recovery notice? If not, select the required stronger guarantee before architecture is expanded.

## Production Design

### Confirmed available facts versus generated guidance

| Carrier | Available outside failed present() | Limit |
|---|---|---|
| Original operation DTO | Yes, after tool.execute returns | Includes phase_instructions/handover_template for get_work_context, but not every configured next instruction |
| NoteContext.entries | Yes | Contains note keys/parameters, not their configured human-readable advice |
| Original attachments | Yes | Formatting them is separate from already having the original immutable schema facts |
| CachePublication | Yes if publication returned | Use only real successful receipts; do not invent a URI |
| Native exception | Yes at server catch | Capture existing error DTO/cause and log original exception |
| Normal protected presentation | Not necessarily | Main template, enum cases, next instructions and note text are generated inside TextPresenter |

### Concrete source constraints

[TextPresenter](../../../mcp_server/presenters/text_presenter.py) renders the main template and enum cases, then collections, then next instructions and notes. A collection error can therefore prevent the entire RenderedPresentation from being returned, including guidance not yet appended. Moving only next_instructions and notes into a helper would not recover all protected core. Calling an instruction helper again also repeats failed rendering when that helper caused the original exception.

[ResponsePresenter](../../../mcp_server/presenters/response_presenter.py) already owns profile selection and common envelope construction. Its existing emergency method expects presentation text already to exist and addresses publication/serialization failure. It is not a complete substitute for the missing post-operation recovery boundary.

The [public response models](../../../mcp_server/schemas/presentation_output.py) currently have no raw-notes carrier. DeliveryFailure admits only cache_publication_failed / operation_serialization_failed. The selected schema permits non-null delivery_error only with data=null. A processing failure with retained data therefore requires a deliberate small shared-contract adjustment; simply changing an error label is insufficient.

A shared recovery/projection seam belongs with the existing presentation responsibility. The server remains the catcher/orchestrator and supplies known facts, rather than inventing field lists, channel rules or recovery advice. Concrete signatures, additional fields, schema alternatives and secondary-failure semantics remain unfinished until the policy choice is resolved.

## Test Design

After the policy decision, adapt the existing processing-failure transport case to use the actual selected schema and real profile composition. Prove original success and original failure followed by an injected presentation error; assert actual operation facts and distinct processing diagnosis, not wording. Explicitly validate structured error results because the SDK skips automatic validation on is_error. Include applicable text-only/resource delivery and preserved attachment/guidance facts. Prove no repeated operation or failed normal rendering; use existing public-boundary helpers. Final case count and execution scopes belong in Planning.

## State and Failures

No workflow or persistent state model change is proposed. Before-operation errors must not fabricate an operation. After-operation recovery must not convert an already completed operation into an unexecuted one. The secondary-failure behavior and exact recovery schema are not approved merely by this draft.

## Preservation

Retain #529's ordinary profile/schema behavior, internal DTOs, raw-operation cache ownership, attachment identities, native diagnosis and immutable configuration. The proposed exception affects only the ability to reproduce normal rendered guidance after an unexpected rendering failure; it is not permission to discard source instructions or silently truncate operation data/raw notes.

## Planning Consequences

Do not plan or implement the recovery until the owner choice is explicit and the completed Design receives independent QA. No phase progression on this decision-pending artifact.

## Sources

- [Approved Research and QA boundaries](<research.md>)
- [Shared public response models](<../../../mcp_server/schemas/presentation_output.py>)
- [Outer server boundary](<../../../mcp_server/server.py>)
- [Response projection and schema](<../../../mcp_server/presenters/response_presenter.py>)
- [Configured text rendering](<../../../mcp_server/presenters/text_presenter.py>)
- [Presentation configuration](<../../../.pgmcp/config/defaults/presentation.yaml>)
- [Architecture principles](<../../../docs/coding_standards/ARCHITECTURE_PRINCIPLES.md>)
- [Existing processing failure behavior](<../../../tests/mcp_server/integration/test_tool_attachment_transport.py>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-20 | @imp designer | Record confirmed recovery seams and the exact missing guidance guarantee; leave policy and final recovery contract pending owner decision. |
