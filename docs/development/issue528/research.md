<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue \#528 — catalog publication after \#529

**Status:** Research findings — bounded recovery strategy recorded  
**Version:** 1.2  
**Last Updated:** 2026-10-20

## Purpose

Establish what remains of the reported missing output-schema defect on the merged #529 baseline, using normal production registration and actual SDK transport.

## Scope In

Normal tools/list publication; tokenless and credential-selected registrations; shipped response profiles; representative success and normalized errors; unexpected processing-failure boundary.

## Scope Out

Research makes no production or permanent test changes. Exclude wrapper metadata forwarding, per-tool schema refinement, authenticated GitHub calls, active harness changes, compatibility paths, and a general exception/presentation redesign.

## Problem Statement

Issue #523 observed zero output schemas because the then-current catalog inspected output_model on registration wrappers that did not expose it. Issue #529 subsequently changed the public answer and schema owner. Re-evidence #528 against merge a7256c0a67cecb58a433861b3ed3a612bd1e3b6a before designing a repair for an obsolete path. The missing catalog schema does not reproduce on normal structured profiles; a reproducible unexpected after-operation processing-error boundary remains for bounded correction and independent architecture review.

## Goals

- Compare actual tools/list with the approved #529 profile contract without injecting output metadata.
- Exercise representative actual success and normalized errors through the SDK and identify intentional schema absence.
- Separate the catalog behavior already delivered by PR #531 from the remaining processing-error contract and its architectural boundaries.

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
| scaffold_schema({artifact_type: intentionally_unregistered}) | ValidationError; success=false; isError=true | Same profile contract, one schema attachment |
| git_status({}) in copied non-Git workspace | ExecutionError; success=false; isError=true | Same profile contract; native Git diagnosis/cause present |

For structured profiles, Draft202012Validator explicitly validated both successes and errors. Removing required outer success from an actual envelope was rejected as a negative control. For structured_resource, the real SDK read_resource route returned JSON operation data from the advertised resource. The probe checked available/nonempty operation data and outcome facts, not byte-for-byte equality of every DTO field.

### Unexpected processing failure after an operation exists

The extended probe additionally injected RuntimeError("isolated528processingfault") only into the isolated presenter's present method, after actual health_check execution. A spy on the existing public cache put method observed the actual successful operation before that failure. In all six servers the wire result was isError=true, contained the processing diagnostic in text and had no structuredContent. For the four structured servers, the advertised schema rejects that absent/null value. The installed SDK call_tool returned the error because it skips automatic output validation for is_error results; that is not proof of schema conformance.

The general server catch preserves this existing processing-error response and logs the original exception. The existing [processing-failure behavior test](../../../tests/mcp_server/integration/test_tool_attachment_transport.py) also proves a presenter exception after a successful operation, but sets mock output_schema=None. It cannot establish the structured-profile contract for this path.

#529 Design explicitly preserves processing errors before an operation exists and excludes a general rewrite of all server exception paths. It does not describe the after-operation presenter-crash case equally explicitly. This is a real observed boundary limitation, not an accidental loss of catalog schemas and not evidence that the injected crash occurs during ordinary presentation. The initial Research did not choose a fallback policy or certify this path as conforming. Independent QA subsequently rejected unconditional closure; the owner discussion below bounds the correction.

### Scope residue and disposition

#529 Design and the active [presentation reference](../../../docs/reference/presentation_architecture.md) still reserve decorator-metadata work for #528. That reservation is not evidence of a current catalog defect. Forwarding unused wrapper metadata would not change the current public catalog. Claiming that such forwarding or per-tool refinement has been implemented would be false.

The independent disposition review of c5a4dfc90c91ec20722b840bf1e86d394eb42296 confirmed the original catalog omission is fixed but returned P1 NOGO for unconditional closure. Issue #528 explicitly includes processing/fallback outcomes, while #529's approved preservation rule forbids hiding an actual operation behind a presentation failure. Remain in Research until independent review accepts the bounded strategy below; no phase GO is claimed here.

### Owner direction and its limits

In the direct owner message 01a15795-3dbb-7602-b802-954e70f55df7, the owner expressed agreement with error handling that truthfully describes what happened and proposed a focused repair outside the failed presenter, for example in the server. The same message explicitly challenged whether schema provision by the presenter violates SSOT. This is the source of the bounded direction; Coordination's subsequent process message is not additional owner policy.

The producer's source-backed answer distinguishes definition, derivation and publication. It does not treat the owner's question as approval for moving schema ownership or redesigning presentation. No owner instruction selects unconditional dual-channel fallback, a second output format, or suppression of the real operation outcome.

### Bounded recovery decision after Design inspection

On 2026-10-20 the owner explicitly approved the defended boundary in the producer conversation and requested the finished Design for inspection before any further progression. The approved exception is limited to an unexpected response-processing failure after a known operation: preserve the actual outcome, available original operation/evidence and diagnosis; disclose that normal formatted explanation/advice may be unavailable. Normal instruction guarantees remain unchanged. Source instructions already in the operation, such as phase_instructions, must not be discarded or claimed lost merely because their usual text rendering failed.

The server catches and supplies known facts. Recovery remains a minimal separate entrypoint within the existing presentation responsibility, uses the shared response/profile contract, and does not rerun the operation, present(), present_text() or collection rendering. No parallel server presenter, second renderer, second schema/configuration source, unconditional dual-channel mode or chain of fallback presenters is approved. An exception from present() does not mean every independent method on the same instance has become unusable.

This closes the narrowly identified guidance-policy question; it does not approve production code, a completed Design, or a phase transition. The owner requested the concrete wire response and ownership before continuing.

### Architectural authority and blast radius

| Fact or action | Current authority | Boundary for the correction |
|---|---|---|
| Public response fields/types | [PublicToolResponse and related models](../../../mcp_server/schemas/presentation_output.py) | Reuse these models; no independently handwritten server response contract |
| Channel/delivery selection | Existing resolved response profile | No new hidden selector or duplicate configuration source |
| Normal response representation and derived schema | [ResponsePresenter](../../../mcp_server/presenters/response_presenter.py) | Derivation starts with model_json_schema(); presenter does not publish the catalog itself |
| Public catalog and outer error boundary | [MCPServer](../../../mcp_server/server.py) | Publish the supplied schema; catch failures outside the failed rendering call; retain a known actual operation |
| Diagnostic capture and readable guidance | Existing error boundaries and presentation/configuration responsibilities | Preserve original exception/cause; no tool-specific recovery strings or second general presenter in server code |

The applicable [architecture principles](../../../docs/coding_standards/ARCHITECTURE_PRINCIPLES.md) are SRP, SSOT, Config-First and pragmatic failure presentation (§§1.1, 2, 3, 15.1). An automatically derived schema is a representation of the authoritative models, not an independent field inventory. The current presenter additionally narrows the model schema using profile rules that it also applies while constructing results. That is a concrete drift-sensitive boundary for Design to keep coherent, not proof that moving schema publication into the tool wrappers would improve SSOT.

The server's broad try/catch currently covers execution, publication, presentation and transport packaging. A correction must distinguish an existing operation from a failure before one exists; it must not assume every caught exception is a presenter failure. State/workflow engines, tool domain logic, wrapper metadata, adapter contracts and dependencies need no change for this boundary.

Likely affected surfaces are the existing server response boundary, shared public response models/schema derivation if a failure variant requires it, existing presentation configuration for readable guidance, and focused transport/presentation behavior tests. The active presentation reference must eventually explain the actual boundary and remove its obsolete metadata-work reservation. Historical #529 artifacts remain evidence, not a documentation-rewrite target.

### Strategy comparison

| Direction | Benefit / impact | Disposition |
|---|---|---|
| Focused outer-boundary handling retaining real operation facts in the existing public response contract | Addresses the demonstrated misleading response; keeps model/profile/schema authority together; requires focused error-path behavior evidence | Owner-supported direction; concrete minimal contract is Design work |
| Keep a bare generic processing error after an operation exists | Little code impact, but discards known outcome from the response and conflicts with the existing preservation rule | Not accepted as unconditional closure by independent QA |
| Rebuild wrapper metadata or introduce another response/exception framework | Does not repair this catalog or demonstrated post-operation boundary; expands coupling and maintenance | Outside scope |


## Questions

The owner-approved narrow guidance exception above closes the remaining identified policy question. Concrete recovery fields, interfaces, profile/schema alignment and bounded secondary-failure behavior are specified in Design for owner inspection first. Research→Design GO on39832b9b predates that explicit exception; neither that GO nor the owner's strategy approval is a Design approval. No new compatibility, channel override, output architecture or broader data-loss policy is inferred.

## Approved Strategy

| Boundary | Binding direction and source |
|---|---|
| Normal catalog publication | Retain the already-approved #529 common envelope, profile-derived schema and intentional absence for wholly textual profiles. No wrapper-forwarding repair or per-tool refinement. |
| Unexpected failure after a known operation | Preserve actual operation success/error facts and available result evidence; expose the later response-processing failure separately. The owner approved a narrow, disclosed inability to reproduce normally formatted explanation/advice after its own rendering failure, while original instruction fields/evidence remain available. Server catches outside failed rendering; minimal recovery stays in the existing presentation layer/common contract. No retrying the operation or failed rendering, no parallel server presenter, no second renderer or fallback chain. Exact fields remain Design work for owner inspection and later QA. |
| Schema and presentation authority | Shared models define response fields; the resolved profile defines normal channel choices; presentation derives its schema; the server publishes and handles its outer boundary. No second field inventory, hidden profile rules or hardcoded recovery advice in server code. The owner explicitly requested this SSOT check; moving schema ownership is not an approved scope expansion. |
| Compatibility and tests | Clean break, no legacy/compatibility path, no harness/version matrix or dependency-surveillance tests. Adapt useful existing behavior tests proportionately; no content snapshots or suite expansion solely to preserve the current misleading fallback. |
| Scope and progression | Correct only the demonstrated after-operation boundary and necessary consumers/docs. No general exception framework or presentation redesign. Independent Research → Design GO is required; Coordination does not substitute for owner or QA. |

## Expected Results

- Actual normal catalog/profile publication remains the already-established #529 behavior.
- If an operation exists before response processing fails, the client can distinguish that operation's actual outcome from the later processing failure; it is not invited to infer the operation never happened.
- Structured responses conform to the connected catalog contract, including the designed recovery path. Text-only profiles retain their intentional schema absence. Do not use SDK error-validation bypass as evidence.
- A failure before an operation exists does not fabricate one. Original diagnostic facts/cause remain available through the established boundaries.
- Focused behavior evidence covers actual success and failure outcomes before an injected later failure, the applicable structured/text routes, and independence from retrying the failed rendering step. Exact cases and gate timing belong in Design/Planning.
- The repair does not introduce independent server field definitions, duplicated profile policy, domain-specific presentation branches or a new exception framework.
- Only this unexpected post-operation failure may disclose unavailable normal formatted guidance; it preserves original instruction facts and does not weaken normal response guarantees.

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
| 1.1 | 2026-10-20 | @imp researcher | Record independent disposition NOGO, the direct owner's bounded outer-error-handling direction, schema/SSOT responsibilities and limited correction strategy; request architecture-boundary re-review before Design. |
| 1.2 | 2026-10-20 | @imp designer | Record the direct owner's approved narrow guidance exception and recovery limits after Design inspection; owner must see the concrete finished Design before further progression. |


