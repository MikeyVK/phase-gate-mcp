<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue \#529 — Harness delivery and complete-output access

**Status:** DRAFT — Research in progress; delivery strategy pending  
**Version:** 0.1  
**Last Updated:** 2026-10-19

## Purpose

Establish an evidence-backed client delivery contract before #528 chooses catalog output schemas.

## Scope In

Current supported harnesses, model-visible short responses and workflow instructions, complete-output access, preferred retrieval routes, and measurable payload limits. Research extends #523 rather than repeating its history.

## Scope Out

No runtime, output DTO, schema, cache or harness configuration changes have been approved. No historical-version matrix, compatibility bridge, release or #528 implementation.

## Problem Statement

A valid MCP result does not prove that its instructions or complete data reach the intended consumer. Some harnesses choose structuredContent for the model, while others prefer content blocks; additional client truncation and resource handling can change what remains accessible.

## Goals

- Preserve the complete short textual tool response and relevant phase instructions in the invoking agent's model input.
- Establish and demonstrate a usable route to the complete output for every required harness, and explicitly name its preferred route.
- Separate model delivery, user-interface visibility, programmatic access and retrievable output; do not substitute one for another.
- Compare feasible output contracts and their measurable payload/context trade-offs before asking the owner to choose a boundary-specific strategy.

## Background

The baseline is main commit 5f052254afc185693cb036700b7c34ac8fbb650c. #523 measured actual pgmcp protocol results and reconciled earlier presentation decisions; #524 corrected cache-availability wording. Those results remain source evidence and protocol measurements, not installed-harness delivery guarantees. The owner explicitly requires this decision before #528.

## Findings

### Owner acceptance requirements

| Requirement | Acceptance boundary |
|---|---|
| Direct short response | The complete short textual response must reach the agent's model input. A corresponding DTO, schema, UI detail, attachment or cache reference alone is insufficient. |
| Direct instructions | Relevant phase instructions and post-tool guidance must remain readable in the model input, including success, policy rejection and failure routes. |
| Complete output | Each required harness must have an executable, demonstrated route to the complete published output set: operation data, diagnostic details, text/instructions and attachments, including large and schema-bearing responses. Multiple channels may jointly provide that set; access to only a summary is insufficient. |
| Preferred route | Name the preferred route per harness and explain the concrete invocation, discovery, pagination or persistence behavior needed to use it. List fallback routes separately when evidenced. |
| Evidence | Distinguish execution through a real harness integration, pinned source inspection, official documentation and unresolved behavior. No supported-harness claim based only on server serialization. |
| Configuration | Harness-specific configuration is a possible solution only if investigation establishes its necessity. No model-specific configuration has been selected. |

Delivery evidence establishes what enters model input; it cannot prove that a model will obey an instruction. A behavioral probe must additionally show that the agent can use the delivered instruction and retrieve the required output.

The required scope is VS Code, Kilo Code, Claude Code, Google Antigravity, Pi, Kimi Code CLI and Z.ai/ZCode. This Codex integration supplies an additional directly observable route. The preferred-route table below separates recommendations, established evidence and missing proof; it does not declare that the current release satisfies every row.

### Proportional proof to collect

For each selected current harness integration, use a small, distinguishable short response and phase instruction, a complete schema-bearing response, a large diagnostic result and an error result. Observe the actual model-facing projection and ask the agent to recover a known item beyond any initial truncation boundary through the proposed preferred route. Retain the invocation, selected integration/build, observed result and limitations.

For cache routes, establish that the agent can discover and invoke the reader, can page to the end, and receives an explicit unavailable result after cache failure or expiry. A cache URI by itself is not retrieval evidence. For structured routes, establish that all relevant fields reach the intended consumer and that independent textual instructions remain present. For file persistence, establish that the running agent can read the saved file in its actual filesystem environment.

Protocol result bytes, selected model-visible text, tokens and billed cost remain separate quantities. The existing 8,000-byte text ceiling does not bound structured output, attachments or the complete result.

### Preferred routes and remaining proof, 2026-10-19

These are research recommendations, not approved delivery policy. "Source" establishes a specific code path; it is not a successful live agent session.

| Harness | Preferred direct delivery under consideration | Preferred complete-output route | What is proved and what remains open |
|---|---|---|---|
| VS Code built-in MCP agent | Include the complete readable response and guidance in whichever structured result is model-facing; alternatively omit structuredContent and use text. | Structured operation for ordinary results; MCP-backed file/resource reads for larger results and attachments. | Installed 1.141.0 build 2a59476c9bfcb90b3ddc372c36762471b7dfad1c contains the structured-preference condition. Its [matching source](https://github.com/microsoft/vscode/blob/2a59476c9bfcb90b3ddc372c36762471b7dfad1c/src/vs/workbench/contrib/mcp/common/mcpLanguageModelToolContribution.ts#L328) corroborates it. Resource filesystem support exists, but autonomous cache-URI discovery/read and full agent-input execution remain unproved. Current text-only guidance does not satisfy this route. |
| Kilo Code | Content text carries the readable response and instructions. | Its agent-facing `read_mcp_resource` tool, using pgmcp windows; persisted output is secondary. | [Session tools](https://github.com/Kilo-Org/kilocode/blob/2a1903f29186e25adec0bace14f6ee589095f7eb/packages/opencode/src/session/tools.ts#L400) implement resource reads and content-based tool output. Structured-only fields are not part of that inspected conversion. Live CLI/extension execution is open. |
| Claude Code | Preserve the readable response in both candidate model-facing channels until the actual path is verified. | Native MCP resource reader with bounded pgmcp windows; successful-output files are secondary. | [Vendor documentation](https://code.claude.com/docs/en/mcp#use-mcp-resources) establishes agent-callable resource readers. Success-file persistence does not prove error preservation. Public reports disagree about text visibility; no local execution has resolved that. |
| Google Antigravity | Content text is the documented starting candidate; structured precedence is unresolved. | No accepted route yet. A standard resource reader must be demonstrated, or a normal MCP retrieval tool evaluated. | [CLI release notes](https://antigravity.google/docs/changelog?tab=cli) document an embedded-resource delivery fix in 1.1.5, not autonomous pgmcp cache reads or the IDE's routing. Those are still proof gaps. |
| Pi, built-in MCP | Content text for direct tools; explicit forwarding of response/instructions when using codemode. | Built-in `read_mcp_resource`; codemode can additionally inspect the complete `CallToolResult`. | [Built-in MCP docs](https://pi.dev/docs/latest/mcp#use-resources) name resource tools; the pinned conversion retains a complete programmatic result separately from model text. Text above 20 KiB is shortened with a saved-file pointer. Live direct/codemode execution remains open. |
| Kimi Code CLI | Content text is the conservative candidate for the inspected source. | No accepted route yet. Prove a native reader for pgmcp resources, or evaluate a normal MCP retrieval tool. | The pinned conversion reads content, caps it at 100,000 characters and returns an omission marker. It does not itself preserve an unabridged result for later reading. The newer documentary claim about both channels/attachment preservation conflicts with that source. Live execution is required. |
| Z.ai / ZCode | Content text first; structured content is appended by the inspected bridge. | No accepted route yet. Model-callable resource access or a normal MCP retrieval tool must be demonstrated. | [Pinned bridge](https://github.com/zai-org/ZCode/blob/0a1fc56d279fd1001f78387bd81aec1c26767411/apps/zcode-cli/packages/core/src/mcp/index.ts#L436) combines both channels. Ordinary MCP output has a 50,000-byte model budget with head truncation. Adapter resource access for applications exists, but does not establish agent access. Live execution is open. |
| This Codex integration | Visible text plus structured data through the existing functions orchestration. | `read_mcp_resource(server="phase_gate_mcp", uri=...)` with explicit windows. | Executed successfully here: complete schema result reconstructed, exact equality checked and SHA-256 verified once. This does not certify another Codex integration. |

### Executed pgmcp route evidence

No harness installs, authenticated model requests or active harness configuration changes were made.

1. `get_work_context()` returned the active Research contract. The 821-character phase-instruction value was also fully present in rendered text. Rendered TODO guidance included `keep exactly one item in progress and update it after each material step.`; that same guidance was absent from the structured DTO. Combining this observed result with the installed VS Code routing condition identifies a concrete text-guidance loss risk. It is not a VS Code session execution.
2. `scaffold_schema(artifact_type="python_class")` returned a visible short message, structured result and schema attachment. The complete structured JSON was 11,927 Unicode codepoints and 11,927 UTF-8 bytes. The embedded application/schema+json attachment parsed to exactly the same schema value as structured schema_data; its pretty-printed text was 12,635 characters.
3. The resource URI from that response was read first with `?offset=0&limit=1` to establish size, then with windows `offset=0, limit=6000` and `offset=6000, limit=6000`. Page lengths were 6,000 and 5,927; next offsets were 6,000 and null. The assembled string exactly matched the complete structured result, parsed successfully, and retained required schema fields `class_name`, `class_description` and `module_description`. One SHA-256 verification matched the resource identity.
4. Reading a deliberately absent 32-hex-character run ID produced MCP error 0, `No cached data found`. This proves an explicit missing-result diagnosis, not recovery of expired output.
5. The source of the current cache route is [CachedResponseResource](../../../mcp_server/resources/cache.py). It returns the operation DTO, not the independently rendered notes or every attachment. [Server assembly](../../../mcp_server/server.py) publishes those separately. Complete-output acceptance must therefore check their union, rather than describing the cache alone as a complete MCP response.

A repeat of steps 2–3 must use the URI from the new invocation. The previous run ID is transient evidence, not a durable dependency. The existing [cache guide](../../../mcp_server/resources/cache_reading.md) defines Unicode offsets, contiguous windows, full-content identity and safe recovery constraints.

### Material limits and uncertainties

- [Claude report 79944](https://github.com/anthropics/claude-code/issues/79944) remains open and reports model text loss. The [consolidation target 45575](https://github.com/anthropics/claude-code/issues/45575), closed as not planned, instead describes UI-only text hiding with model delivery retained. Neither report proves the current local integration; do not present the symptom as a verified current Claude behavior.
- ZCode's default MCP [budget declaration](https://github.com/zai-org/ZCode/blob/0a1fc56d279fd1001f78387bd81aec1c26767411/apps/zcode-cli/packages/core/src/mcp/index.ts#L150) uses truncation, while [artifact persistence](https://github.com/zai-org/ZCode/blob/0a1fc56d279fd1001f78387bd81aec1c26767411/apps/zcode-cli/packages/core/src/tool/executor/result-serialization.ts#L97) requires the separate artifact strategy and enabled setting. A complete saved copy cannot be assumed for ordinary pgmcp tools.
- The current [text limiter](../../../mcp_server/presenters/text_budget_limiter.py) reserves a truncation notice and cache reference, not a separately protected instruction region. Because [TextPresenter](../../../mcp_server/presenters/text_presenter.py) appends guidance before that final limit, mandatory-guidance preservation also needs explicit treatment at the pgmcp boundary. This is source-derived reachability analysis, not a newly executed truncation scenario.
- Only `code.cmd` and `codex.exe` were found among the requested CLI names on the current PATH. The VS Code launcher selects a versioned installation directory; an earlier check of an unversioned app path was inconclusive. Missing PATH entries do not prove that the other products are absent from all hosts or install locations.
- No installed-agent execution for the seven requested harnesses is claimed. Closed-source behavior, resource-tool discoverability, permissions and actual model requests still require integration probes.

### Feasible contract choices for owner discussion

| Option | Instruction delivery | Complete-output access and cost | Consequence |
|---|---|---|---|
| Full structured operation plus the complete readable response/guidance; concise text retained | Both channel preferences have readable instructions. | Large DTOs remain inline for structured-preferring clients. Clients can still truncate; a working retrieval route remains necessary. | Less change to current full-operation delivery; no broad initial-context bound. |
| Bounded shared result view containing readable response/guidance and an explicit complete-result locator, in both channels | A shared projection can cover both inspected preference classes without per-harness branching. | Large details are fetched in bounded pages. A proven resource or normal-tool reader is essential; cache failure and independently owned attachments must be explicit. | Changes the public structured contract chosen in #517 and determines the schema #528 must expose. |
| Harness-specific configured projections/read routes | Can accommodate demonstrated integration differences. | Each profile still needs a real retrieval mechanism; configuration alone cannot give a client a resource reader. | Additional configuration, selection and proof obligations. No necessity for this mechanism has yet been established over a shared contract. |

A normal MCP retrieval tool could reuse the existing read-only cache boundary and serialization rather than create a second cache. It is an unapproved public-tool option, not an implementation decision. Its necessity should be assessed against actual native reader gaps.

Owner decisions remain: the output contract and measurable initial-response objective; whether an additional generic retrieval tool is acceptable if required harnesses lack an agent-callable resource reader; and the execution arrangement for real harness probes. A larger public-boundary change must not be treated as mechanical chore work.

## Questions

- Which concrete output contract meets both mandatory delivery requirements across the required current harnesses?
- Can one generic contract satisfy the evidence, or is harness-specific configuration demonstrably necessary?
- What initial-response payload objective and exceptions preserve complete diagnostics and usable retrieval?
- Which integration-specific execution remains necessary where public source or documentation is incomplete or contradictory?

## Approved Strategy

The owner has confirmed the direct-instruction, direct-short-response and demonstrated complete-output requirements above, and requires an explicit preferred route per harness. Clean break remains the migration policy: no legacy bridge or historical-version tests. The supported integration/build scope, delivery mechanism, any necessary harness-specific configuration, and measurable payload objective remain PENDING OWNER DECISION. Research is not complete and must not progress on this draft.

## Expected Results

An explicit supported-harness scope with demonstrable instruction delivery and full-output access, a justified preferred route per harness, and an owner-approved contract and payload objective. Unproven integrations remain visible as open work rather than compatibility claims.

## Consumers

### Server response assembly and existing presenters

Publish operation data, rendered text, instructions and attachments through the current output boundary.

**Impact:** Investigation only; a delivery change requires an explicit approved strategy and proportional scope assessment.

### Harness model input and resource/file readers

Deliver the short response and instructions and provide access to complete output.

**Impact:** Required evidence differs by integration; server-side presence is insufficient.

### Issue \#528 catalog output schema work

Expose metadata matching the selected output contract.

**Impact:** Must follow the #529 owner decision; must not choose that policy independently.

## Risks

### Documentation and pinned source may describe different builds or integration routes.

Record both evidence classes and resolve material discrepancies with a specific integration probe.

### A harness may truncate output or hide one response channel.

Prove direct instruction delivery separately from complete-output retrieval, including error paths.

### A shared output redesign may exceed the maintenance scope of a chore.

Stop for an explicit scope/workflow decision before implementation when the selected mechanism is not bounded maintenance.

## Related Documents

- [Issue #523 baseline research](<../issue523/research.md>)
- [Issue #523 validation](<../issue523/validation.md>)
- [Current presentation architecture](<../../reference/presentation_architecture.md>)
- [Architecture principles](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-19 | @imp researcher | Capture mandatory direct instruction/text delivery, demonstrated complete-output access and explicit preferred routes for the owner-required harnesses; separate source findings from remaining execution evidence. |
