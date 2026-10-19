<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue \#528 — catalog publication after \#529

**Status:** Research findings — independent disposition review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-19

## Purpose

Establish what remains of the reported missing output-schema defect on the merged #529 baseline, using normal production registration and actual SDK transport.

## Scope In

Normal tools/list publication; tokenless and credential-selected registrations; shipped response profiles; representative success and normalized errors; unexpected processing-failure boundary.

## Scope Out

No production changes, wrapper metadata forwarding, per-tool schema refinement, permanent test additions, authenticated GitHub calls, active harness changes, or new output policy.

## Problem Statement

Issue #523 observed zero output schemas because the then-current catalog inspected output_model on registration wrappers that did not expose it. Issue #529 subsequently changed the public answer and schema owner. Re-evidence #528 against merge a7256c0a67cecb58a433861b3ed3a612bd1e3b6a before designing a repair for an obsolete path. The missing catalog schema does not reproduce on normal structured profiles; a separate unexpected processing-error boundary remains explicit for independent disposition review.

## Goals

- Compare actual tools/list with the approved #529 profile contract without injecting output metadata.
- Exercise representative actual success and normalized errors through the SDK and identify intentional schema absence.
- Expose counterevidence and limitations before asking whether #528 has already been delivered by PR #531.

## Background

Baseline: main after PR #531, merge a7256c0a67cecb58a433861b3ed3a612bd1e3b6a. Branch: bug/528-publish-tool-output-schemas; workflow bug; phase Research. No production, configuration, or permanent test changes were made during this investigation. Existing #529 Research/Design are policy inputs, not new owner approval for a different contract.

## Findings

### Normal publication

[MCPServer](../../../mcp_server/server.py) obtains every catalog entry's output_schema directly from presenter.output_schema(). It no longer reads output_model from the outer registration wrapper. [ResponsePresenter](../../../mcp_server/presenters/response_presenter.py) derives that schema from the selected common envelope/profile. In contrast, [ToolAssembly](../../../mcp_server/bootstrap.py) resolves supported core operation models before wrapping and uses them for composition/alignment validation. Missing metadata on an outer wrapper therefore does not imply that public schema publication or core model validation is missing.

The real bootstrap/SDK probe observed:

| Profile | Selection | Registered / published | Published schemas | Outer wrappers with output_model |
|---|---|---:|---:|---:|
| structured_inline | Tokenless | 37 / 37 | 37 | 0 |
| structured_inline | Placeholder token | 49 / 49 | 49 | 0 |
| structured_resource | Tokenless | 37 / 37 | 37 | 0 |
| structured_resource | Placeholder token | 49 / 49 | 49 | 0 |
| text_inline | Tokenless | 37 / 37 | 0 | 0 |
| text_inline | Placeholder token | 49 / 49 | 0 | 0 |

All advertised schemas equal the actual selected presenter's schema. The text-only omission is intentional under #529: both outputSchema and structuredContent are absent. Its complete data segment remains JSON text. The generic schema describes the public envelope; operation is an arbitrary JSON object. It does not promise the success model of each individual tool or a specific per-tool error union.

### Representative actual calls

Each of the six isolated normal servers executed all three calls below (18 calls per successful probe run). No output_model was attached to wrappers.

| Call | Actual result | Observation |
|---|---|---|
| health_check({}) | success=true; isError=false | Valid selected structured envelope, or parseable complete text data segment |
| scaffold_schema({artifact_type: intentionally_unregistered}) | ValidationError; success=false; isError=true | Same profile contract, one complete schema attachment |
| git_status({}) in copied non-Git workspace | ExecutionError; success=false; isError=true | Same profile contract; native Git diagnosis/cause present |

For structured profiles, Draft202012Validator explicitly validated both successes and errors. Removing required outer success from an actual envelope was rejected as a negative control. For structured_resource, the real SDK read_resource route returned JSON operation data from the advertised resource. The probe checked available/nonempty operation data and outcome facts, not byte-for-byte equality of every DTO field.

### Unexpected processing failure after an operation exists

The extended probe additionally injected RuntimeError("isolated528processingfault") only into the isolated presenter's present method, after actual health_check execution. A spy on the existing public cache put method observed the actual successful operation before that failure. In all six servers the wire result was isError=true, contained the processing diagnostic in text and had no structuredContent. For the four structured servers, the advertised schema rejects that absent/null value. The installed SDK call_tool returned the error because it skips automatic output validation for is_error results; that is not proof of schema conformance.

The general server catch preserves this existing processing-error response and logs the original exception. The existing [processing-failure behavior test](../../../tests/mcp_server/integration/test_tool_attachment_transport.py) also proves a presenter exception after a successful operation, but sets mock output_schema=None. It cannot establish the structured-profile contract for this path.

#529 Design explicitly preserves processing errors before an operation exists and excludes a general rewrite of all server exception paths. It does not describe the after-operation presenter-crash case equally explicitly. This is a real observed boundary limitation, not an accidental loss of catalog schemas and not evidence that the injected crash occurs during ordinary presentation. Research does not silently choose a new fallback policy or certify this path as conforming.

### Scope residue and disposition

#529 Design and the active [presentation reference](../../../docs/reference/presentation_architecture.md) still reserve decorator-metadata work for #528. That reservation is not evidence of a current catalog defect. Forwarding unused wrapper metadata would not change the current public catalog. Claiming that such forwarding or per-tool refinement has been implemented would be false.

Request independent QA to assess whether the original schema-publication issue is already delivered by #529/PR #531, and whether the explicitly recorded processing-error limitation prevents that disposition. Do not infer universal response conformance from catalog completeness. Remain in Research until that assessment and Coordination's administrative hand-off; do not manufacture Design/Implementation phases to close an absent normal-path defect.

## Questions

- Does independent QA accept already-delivered disposition for the original omission, with intentional text-only absence and the observed unexpected processing boundary explicitly retained? If not, identify the exact unmet approved contract and any owner policy decision required before Design.

## Approved Strategy

Retain the owner-approved #529 clean break: one general public envelope; internal operation DTOs unchanged; profile-selected schema publication; no outputSchema for wholly textual output; no compatibility bridge or harness/version test matrix. Reuse that decision for the original catalog-publication boundary. No new per-tool schema or unexpected-after-operation fallback policy is approved here. The current Research contract requires stopping when the reported defect is not evidenced; Coordination has requested independent QA disposition before administrative handling.

## Expected Results

Independent review can distinguish three factual claims: (1) the old normal catalog omission is no longer present, (2) intentional text-only absence is the approved behavior, and (3) unexpected presenter failure after a successful operation remains a separate response-contract limitation. No Design transition or administrative closure is claimed by the producer.

## Evidence

### Normal production registration publishes the approved profile schema for both supported selection sizes.

First successful isolated run: six servers, six SDK catalogs, 18 actual calls; one test passed in 42.17s, native exit 0. Extended run repeated those observations and added six after-operation presenter-failure cases: one test passed in 43.42s, native exit 0. Receipts b89c86a88e5c4eceb79c216a78db8720 and f969421177774387ae841d2c851e622b supplement these recorded facts. An initial probe-only marker setup mistake (asyncio instead of pytest.mark.asyncio) caused collection failure; corrected before both successful runs.

- [Normal bootstrap and core contracts](<../../../mcp_server/bootstrap.py>)
- [SDK transport helper and isolated workspace inputs](<../../../tests/mcp_server/test_support.py>)
- [Catalog and call boundary](<../../../mcp_server/server.py>)

**Invocation:** run_tests(scope="targets", targets=[".pgmcp/temp/issue528/test_catalog_probe.py"], tests=["python_tests"], args={"python_tests":["-n","0","-s"]}, timeout_seconds=300)

**Observed Result:**

Reproduction recipe (temporary diagnostic test, not a permanent suite addition):

1. Copy startup inputs with existing copy_server_startup_inputs(repository, tmp_path / unique_profile_selection). This supplies config, template_suite and installation.json, without a Git repository.
2. Build Settings/ServerSettings with explicit isolated workspace/config/template roots, bypass_version_check=False and each shipped response_profile: structured_inline, structured_resource, text_inline.
3. Remove GITHUB_TOKEN for the tokenless case; set only an inert placeholder for the second selection. Patch load_github_config to explicit probe-owner/probe-repo. Patch the GitHubAdapter constructor and assert it is never called; make no authenticated operations.
4. Call actual ServerBootstrapper(settings).bootstrap_target(), then connected_mcp_client(server); call SDK list_tools. Count server.tools and returned tools; compare each returned output_schema to server.presenter.output_schema(). Observe outer wrapper metadata without changing it.
5. Call the three tools/arguments in the table. For advertised schemas validate response.structured_content with Draft202012Validator, including isError responses. Remove success from a copy and require rejection. For text-only parse the distinct fenced JSON segment. Check actual operation success/error facts and schema attachment count.
6. For resource delivery call SDK read_resource at data.uri, parse returned text as JSON, and check the operation facts.
7. For the additional boundary case patch only server.presenter.present to raise the marker RuntimeError; wrap server.response_cache_manager.put with a spy. Call health_check again. Require one publication of an actual success=true operation, text marker, isError=true and no structuredContent. Validate that absent value against an advertised schema and observe rejection.
8. Preserve the six-row observations and native outcome shown here. The ignored temporary probe is not the sole evidence carrier; this recipe, source links and exact measured results survive in this document.

Scope: no domain-error catalogue exhaustiveness, no authenticated GitHub behavior, no permanent per-tool DTO guarantee, no full suite rerun, and no claim that the artificial presenter crash happens naturally.

## Consumers

### MCP tools/list clients

Read the connected public schema.

**Impact:** Already receive the selected common envelope schema; wholly textual profiles intentionally advertise none.

### Bootstrap/presentation alignment

Validate supported core tool output models and configured presentation.

**Impact:** Existing SupportedToolContract remains useful before wrapping; no forwarding repair is required by the current public catalog.

### SDK callers and response validators

Consume actual success/error responses.

**Impact:** Representative normalized outputs conform. Unexpected post-operation processing fallback is explicitly outside the demonstrated conformance; SDK automatic error bypass must not hide this distinction.

### Existing tests and current documentation

Provide durable behavioral evidence and explain current ownership.

**Impact:** Existing listing test manually attaches now-unused metadata; current normal-bootstrap probe supplies the missing evidence. #529 metadata reservation is documentary residue to reconcile only after disposition.

## Risks

### Treating a skipped SDK validation as proof that the fallback matches its schema.

Record direct schema rejection and actual successful operation before the injected error; ask independent QA to assess disposition.

**Consequence:** A blanket closure statement would overclaim response conformance.

### Designing wrapper forwarding because a historical note says \#528 will do it.

Use actual public catalog consumer and approved generic envelope as the baseline.

**Consequence:** Dead metadata work and unnecessary test coupling.

## Related Documents

- [#529 Research](<../issue529/research.md>)
- [#529 approved Design](<../issue529/design.md>)
- [Merged PR #531](<https://github.com/MikeyVK/phase-gate-mcp/pull/531>)
- [Issue #528](<https://github.com/MikeyVK/phase-gate-mcp/issues/528>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-19 | @imp researcher | Re-evidence #528 after merged #529; record normal catalog contract, representative SDK calls and unexpected after-operation processing limitation without production changes. |
