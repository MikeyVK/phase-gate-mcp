<!-- C:\temp\pgmcp\temp\issue460-design-workshops-20260910\01-mutation-results.md -->
<!-- template=design version=5827e841 created=2026-09-10T09:24Z updated= -->
# W01 — A mutation result that tells the whole story

**Status:** REVIEWED — W01/W02 approved; W05 recovery remains a proposal  
**Owner after approval:** DI-04; process facts stay DI-05; delivery stays Shared Contracts  
**Review dependency:** Existing approved header and checked-write decisions. Read this first.  
**Decision nucleus:** Keep the normal operation result on expected failures; add the missing typed facts, not a new exception/presenter framework.

## 1. Purpose and authority

An agent needs to distinguish “the proposed content passed” from “the file was written.” If a file changes externally after validation, the response must preserve both the passing check and the refusal to overwrite. This workshop closes Q-MUT-03/06 and the remaining integration portion of Q-MUT-04.

[Approved mutation contract](C:/temp/pgmcp/docs/development/issue460/design-mutation-validation.md) §4.6–4.9 is binding. [Adapter contract](C:/temp/pgmcp/docs/development/issue460/design-execution-adapters.md) owns process failures, not this document.

## 2. Scope and exclusions

Complete accepted-operation DTOs, expected operation failures, selection explanation, process provenance and presentation. No header redesign, new mutation mode, diff/preview feature, extra check or whole-presenter refactor. W05 separately proposes fix-recovery records; their narrow effect on overlapping mutation admission is explicitly cross-referenced below, not treated as approved DI-04 behavior.

## 3. Binding inputs

Research F-03/F-07/F-13/F-15, E-18, I-4/I-9; latest safe-edit amendment. Retain first-line-only recognition, original-file selection, original-byte replacement guard, four edit operations, default enforce and report's limited permission.

[Presentation architecture](C:/temp/pgmcp/docs/reference/presentation_architecture.md), issues 456/459, and [actual presenter](C:/temp/pgmcp/mcp_server/presenters/text_presenter.py) constrain the shape.

## 4. Approved decisions

| ID | Proposal | Why the consumer needs it |
|---|---|---|
| W01-A | Expected failures remain in ScaffoldOutput/SafeEditOutput | Preserve already collected checks and actual write outcome |
| W01-B | Add direct nullable error_code; no second outcome/status envelope | One primary operation-blocking cause selects configured explanation |
| W01-C | Keep one concrete public check item with typed cache-only invocation detail | Existing generic collection projection works without union-item support |
| W01-D | Separate housekeeping from blocking errors | Cleanup cannot falsify a verdict or completed write |
| W01-E | Preserve recognition fallback as a selection fact | Explain invalid/unknown metadata without inventing a failed check |
| W01-F | Approved: retain bounded raw/native diagnostics in the existing on-demand cache, including incidental absolute paths; keep operation fields relative | Preserve useful troubleshooting without an extra private-log route or a false local-only guarantee |

Human approval on 2026-09-10 closes W01-A–E following the earlier W01-F approval. Canonical ownership is DI-04 §4.10 (operation results) and §4.6 (disclosure), referenced by DI-05. W01 did not approve W02/W05 implicitly. W02's external_tools amendment is now separately approved; W05 recovery remains a proposal. Shared invocation/capture declarations and resource round-trip evidence remain explicit integration obligations.

## 5. Responsibilities and boundaries

Manager constructs domain outcomes and consequences. The filesystem boundary observes create collision, stale original and write failure. Generic invocation management owns timeout/stop/capture. The adapter owns its rejection message and native evidence. The tool transfers structure only. Presentation configuration owns wording.

No manager imports tool-output types. Prefer reusing inward-owned immutable records; the outward model adds only operation-specific fields needed by the public contract.

## 6. Options and rationale

| Option | Assessment |
|---|---|
| Raise every expected failure into an exception DTO | Loses completed check/selection/write facts or duplicates them across error classes |
| Add an outcome field plus per-variant presenter dispatch | Duplicates existing success/written facts and introduces an unnecessary framework |
| Complete the existing typed result graph | Recommended; aligns with the recent structured-result route |

## 7. Detailed design

All models are frozen, strict and extra-forbid; sequences are immutable tuples; JSON decoding does not coerce scalar types. Nullable below means required explicit null, not an accidental default.

Keep approved direct fields: success, written, validation_policy, validation_status, profile_id, checks; scaffold output_path and package identity/version/fingerprint; safe-edit path, content_changed, selected_source, template_id and extension.

Approved operation-field additions:

| Field | Type | Consumer / channel |
|---|---|---|
| error_code | MutationErrorCode or null | Manager consequence; configured failure text and cache |
| error_details | Closed typed detail variant or null | Complete cache; no arbitrary dictionary |
| housekeeping | tuple[HousekeepingIssue, ...] | Actual write-stage cleanup failures; bounded text + cache |
| selection_reason, safe edit only | MetadataFallbackReason or null | Factual fallback explanation; direct scalar text when useful + cache |
| checks[].invocation | InvocationEvidence or null | Invoked package/tool provenance and bounded diagnostics; cache |
| checks[].termination_problem | existing TerminationProblem or null | Additional stop fact; direct scalar + cache |
| checks[].housekeeping | tuple[HousekeepingIssue, ...] | Check scratch cleanup only; bounded child collection + cache |

MutationErrorCode approved closed values: context_invalid, target_invalid, target_exists, original_unreadable, edit_invalid, render_failed, preparation_failed, validation_blocked, original_changed, original_missing, persistence_failed, adapter_request_rejected, termination_unconfirmed, operation_interrupted. Earlier invalid public template IDs stay outer input errors when rejected there; do not add an accepted-operation failure just to mirror them.

Details are a closed union keyed by their existing code: context issues (JSON Pointer + schema keyword + factual message), target/write information (relative affected path + typed cause), edit problem (missing_match/missing_anchor/invalid_pattern/invalid_replacement), adapter request issues (existing RequestValidationIssue values + check_id), or no additional detail. Do not repeat whole input values, file contents or the complete result inside details. At canonical integration, reuse equivalent existing inward types before introducing a new name.

HousekeepingIssue has required purpose enum validation_input|write_staging, relative path and factual message. The collection is justified by independently possible failures, not a singleton wrapper. Termination-unconfirmed is not housekeeping.

InvocationEvidence has adapter_id, package_version, package_fingerprint, contract_version, external_tools: tuple[ExternalToolIdentity,...], and capture: ProcessCaptureFacts. It exists for an attempted invocation, including a failed launch; never for a not-started check. ExternalToolIdentity has required tool_id:NonBlankText and version:NonBlankText|null; unknown version stays unknown, never guessed. W02 now approves the explicit external_tools return field from which this evidence is populated; generic PGMCP does not scrape native evidence for versions. A launch/protocol failure can have an empty observed-tools list. Multiple native tools are possible within one adapter. Proposed ProcessCaptureFacts retains the observed exit code or null, observed/retained stream byte counts, truncation facts and bounded captured diagnostics in the existing result cache. The accepted fact placement is fixed; final shared carrier declarations remain DI-05 integration. Preserve DI-05's 8 MiB response ceiling and 256 KiB stderr head/tail retention; no second retention mechanism is introduced. Raw malformed/partial stdout is process capture, never accepted native evidence. Do not duplicate accepted response bytes beside the already retained decision/evidence. Incidental absolute paths are permitted in diagnostic content under approved W01-F; no diagnostic_id or private-log substitute is proposed.

MetadataFallbackReason is absent|invalid|unknown_template; null means metadata fallback was not evaluated (for example explicit input won). Unknown and invalid still select the same extension/no-profile route as absent. Do not expose parsed fragments of an invalid header. The reason does not affect policy. Routine absence need not occupy prominent text.

## 8. Control, data and state flow

| Example | Facts retained | Mutation |
|---|---|---|
| Safe edit passes; original bytes changed before replace | validation_status=passed, error_code=original_changed, written=false, content_changed=null | Refused |
| Report writes content rejected by an adapter | success=true, validation_status=failed, original adapter message, error_code=null | Written |
| No profile, report | selected_source=none, empty checks, validation_status=not_executed, error_code=null | Allowed if safe |
| No profile, enforce | Same selection/check facts, validation_blocked | Refused |
| Timeout and stop unconfirmed | timeout in its check plus termination_unconfirmed; operation error mirrors the blocking consequence | Refused under both policies |
| Write completed; cleanup failed | success/written remain true; housekeeping retained | Not undone |
| Adapter rejects PGMCP request | Structured rejection details; no fabricated content verdict | Refused |
| Outer malformed MCP input | Existing framework error route | No manager operation |

Primary error is the first authoritative operation blocker in the actual flow. Additional process/cleanup observations retain their own records rather than racing to replace it. Never relabel cache-publication failure as failed persistence.

### Presentation feasibility, not a new framework

The current per-tool template_failure overrides global.failures. Recommendation: use the existing global error-code route for these expected failures, with **constant configured explanations**; select additional scalar/collection facts through the tool's normal declaration. Constant explanations avoid the current global-placeholder admission gap.

Optional enums are not supported by current enum_cases admission. Do not pretend error_code:null can use that mechanism unchanged; ordinary scalar formatting and existing global selection suffice. New failure reasons require DTO/YAML/tests, not presenter branches. Do not introduce new registered response classes. A broader cleanup of the legacy error_class_fields table is not a prerequisite.

### Diagnostic disclosure — W01-F approved

Human approval on 2026-09-10 chose the alternative to this draft's original private-log proposal. The canonical owner is [DI-04 §4.6](C:/temp/pgmcp/docs/development/issue460/design-mutation-validation.md#diagnostic-disclosure--approved-2026-09-10); DI-05 applies it across shared execution consumers. The earlier blanket prohibition of host paths in cached diagnostics is explicitly superseded, not silently reinterpreted.

Keep operation path fields workspace-relative in inline text and cached DTOs; PGMCP adds no host paths to generated artifacts. Ordinary output stays concise and does not automatically embed or dump raw streams/stack traces. Existing on-demand cached diagnostics may contain incidental absolute paths because actual locations can be important for troubleshooting. Retain bounded raw/native data without an extra private archive, exposure flag, diagnostic-ID-only replacement or generic path scrubber.

A resource cache is agent/client-accessible output, not a private local boundary. Reading it can send diagnostic content to a model/provider or client logs, and clients can retrieve resources automatically. This accepted disclosure does not authorize credentials, full environment dumps or unrelated sensitive collection, and does not promise universal secret redaction. Research's generated-artifact portability contract and deferred security work remain unchanged.

### Conditional dependency on W05 recovery

If W05's durable multi-file recovery proposal is approved, scaffold/safe-edit write admission also needs a narrow injected RecoveryConflictReader: given intended relative targets, it returns unresolved overlapping fix-recovery facts or none. It does not apply fixes, own journals or perform a startup/temp sweep. An overlap produces the proposed MutationErrorCode recovery_pending with relative affected paths and a recovery reference; unreadable/invalid recovery state that prevents safe admission instead uses recovery_state_invalid. Both are conditional additions to MutationErrorCode; no check verdict is invented. This is an explicit addition to the current DI-04 write admission and error vocabulary, requiring joint W01/W05 review. Rejecting or narrowing W05 removes this dependency; it is not a free consequence of reusing a filesystem utility.

## 9. Compatibility, migration and removal

Replace legacy SafeEditOutput mode/passed/diff/has_diff claims and ScaffoldArtifactOutput name/files_created/schema duplication as their approved replacements take authority. Preserve wrapper-level unexpected-error behavior. Remove stale static failure wording that hides the selected code. No NoteContext diagnostics for the new operation graph.

## 10. Test and validation design

Exercise real decorated tools, complete DTO cache and real presentation config: every row above; JSON-only native rejection; truncated text with complete cache; missing cache publication; exact nullable combinations; invalid projections; retained check order; no schema attachment on success/output failure. Reuse safe-edit operation tests and issue459 collection tests. For approved W01-F, verify workspace-relative operation fields in cached DTOs, incidental native paths retained in bounded cached diagnostics, no automatic raw-stream/stack-trace embedding or inline dump, and unchanged verdict/write facts. No production code or runtime test was executed for this proposal.

## 11. Integration risks and review

W01-F is approved with an explicit risk boundary: cached raw/native diagnostics may reveal host locations after retrieval. No arbitrary-data sanitization or private-storage guarantee is implied. Remaining implementation evidence must verify the operation-field versus diagnostic-content distinction without changing native verdicts or introducing presenter-specific error knowledge.

Review outcome: normal failure DTO route, error_code choice, invocation/cleanup placement and selection explanation are approved. Follow DI-04 §4.10 for canonical ownership; do not reopen those choices while completing DI-05 declarations, required-null serialization or independent evidence.

## 12. Planning consequences

One mutation-result contract can be integrated after its DI-05 evidence types exist. It is distinct from adapter execution, header utilities and controlled filesystem writes; no cycles are assigned here.

## 13. Traceability

DI-04 Q-MUT-03/04/06 → §§7–10; DI-05 factual evidence → InvocationEvidence and unchanged verdict fields; Shared Contracts → context schema attachments; XC-01 → inward ownership and declarative presentation; E-18 → state examples and preservation tests.

## 14. Related documentation and history

Next: [W02 packages](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/02-adapter-packages.md), then [W03 checks](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/03-run-checks.md).  
0.3, 2026-09-10: integrate human approval of W01-A–E; W02/W05 dependencies remain unapproved and review advances to W02.  
0.2, 2026-09-10: integrate human-approved W01-F disclosure policy and withdraw the private-log/diagnostic-ID alternative; W01-A–E and downstream amendments remained proposals at that time.  
0.1, 2026-09-10: initial temporary proposal; replaced no canonical decision.
