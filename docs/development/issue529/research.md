<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue \#529 — Harness delivery and complete-output access

**Status:** DRAFT — Research in progress; delivery strategy pending  
**Version:** 0.5  
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

### What each inspected harness gives its agent

The table describes observed or documented behavior, not a recommendation or an accepted support guarantee. "Source" means code inspection; this Codex integration, isolated Pi 1.3.0, Kilo 7.8.12, Kimi Code 2.2.0 and Claude Code 2.1.303 CLIs, and Antigravity SDK 0.1.22's native local harness were exercised here. A VS Code 1.142.0 built-in Local-agent attempt stopped before the first model request.

| Harness / route | Model-facing result when text and structuredContent are both present | Agent access to additional/full output | Evidence and remaining gap |
|---|---|---|---|
| VS Code 1.142.0, Local harness | Source suggests structuredContent replaces text; native model delivery remains unmeasured. | The isolated real built-in agent attempt discovered the MCP tool and selected the probe model, but stopped with no default agent registered / agentReady=false before any provider request. | Earlier [release-tag source](https://github.com/microsoft/vscode/blob/d956e8a6ac5d904486557eea07e1d6bd62a4d36f/src/vs/workbench/contrib/mcp/common/mcpLanguageModelToolContribution.ts#L328) is distinct from the downloaded archive commit 6d62b1d5dace93a33b3a6d3eca1317bd5e15bcb1 and bundled Copilot Chat 0.70.0. Failed startup is not a measured channel result. |
| VS Code 1.142.0, Copilot harness / Agent Host | Not established by this research. The Local conversion must not be applied to this route by inference. | Not established. | [Official 1.142 release notes](https://code.visualstudio.com/updates/v1_142#_copilot-harness) document Copilot SDK routing and progressive default rollout. [Session launcher](https://github.com/microsoft/vscode/blob/d956e8a6ac5d904486557eea07e1d6bd62a4d36f/src/vs/platform/agentHost/node/copilot/copilotSessionLauncher.ts#L90) supplies MCP servers to the SDK. The SDK/CLI result-to-model path still needs verification. |
| Kilo Code CLI 7.8.12, direct tools | Executed: short text and instruction present; independent structuredContent marker absent. | Executed: native `read_mcp_resource` recovered all 22,086 characters in four windows. Preferred measured route: short text plus paged resource access. | Official npm CLI, actual model-provider requests; scoped probe below. This does not certify the IDE extension or codemode. |
| Claude Code CLI 2.1.303 | Executed: structuredContent marker present; independent short text and instruction absent. The same result occurred with and without `--bare`. | Executed: `ReadMcpResourceTool` recovered all 22,086 characters. Preferred measured data retrieval: structured result plus resource reading. Direct text/instruction acceptance remains unmet. | Official native CLI; source-report disagreement resolved for this exact execution, not every client integration. |
| Antigravity SDK 0.1.22 → bundled native localharness.exe | Executed: text and independent instruction present; structuredContent marker absent. | Executed: native read_resource saves each resource page to a file; native view_file returns it to model input. Four pages recovered all 22,086 characters exactly. Preferred measured route: text plus resource/file reading. | Actual SDK Agent.chat with LocalOpenAIAgentConfig and localhost provider capture. Does not certify the Antigravity app, IDE or CLI. |
| Pi 1.3.0, built-in MCP direct tools | Executed: text and the independent instruction reached the model request; the structured-only marker did not. Fallback without content and codemode are still source evidence, not executed cases. | Executed: native read_mcp_resource retrieved four windows, reconstructing all 22,086 characters exactly. | Real npm-installed CLI through its declared bin entry, stdio MCP and a deterministic localhost model peer; details below. |
| Kimi Code CLI 2.2.0 | Executed: both independent text and JSON markers and the instruction present. | A second probe delivered the complete 22,086-character payload inline in structuredContent. Preferred measured route: inline structured output. No resource reader was offered in the captured tool catalog; resource-based rereading remains unproved. | Official `@moonshot-ai/kimi-code` CLI. The old Python kimi-cli source describes a different, retired product and is not current-release evidence. |
| Z.ai / ZCode | Content followed by informative structuredContent, then the ordinary MCP model budget of 50,000 bytes. | Adapter resources exist for applications; agent-callable cache reading remains unproved. Ordinary MCP truncation does not itself promise a complete saved copy. | [Pinned bridge and budget](https://github.com/zai-org/ZCode/blob/0a1fc56d279fd1001f78387bd81aec1c26767411/apps/zcode-cli/packages/core/src/mcp/index.ts#L436). No live harness run. |
| This Codex functions integration | Both channels are available to orchestration; this chat has received the rendered instructions. | MCP resource windows were actually read and reconstructed completely. | Executed evidence below; no claim about every Codex integration. |

**Version correction:** on 2026-10-19 the current stable VS Code is 1.142.0, released on October 14. The local launcher selects installed 1.141.0. Inspection of an installed older version was valid local evidence but insufficient for a current general VS Code conclusion. The Local routing condition is independently confirmed in the 1.142.0 tag. Copilot Agent Host is a distinct, still unresolved path.

Rows without executed version-specific evidence remain dated source/documentation observations, not current released-binary guarantees.

### Executed pgmcp route evidence

The initial Codex observations below used existing tooling. Subsequent isolated CLI probes installed official distributions locally; they used local deterministic model peers and separate harness configuration, without external model accounts or changes to active harness configuration.

1. `get_work_context()` returned the active Research contract. The 821-character phase-instruction value was also fully present in rendered text. Rendered TODO guidance included `keep exactly one item in progress and update it after each material step.`; that same guidance was absent from the structured DTO. Combining this observed result with the installed VS Code routing condition identifies a concrete text-guidance loss risk. It is not a VS Code session execution.
2. `scaffold_schema(artifact_type="python_class")` returned a visible short message, structured result and schema attachment. The complete structured JSON was 11,927 Unicode codepoints and 11,927 UTF-8 bytes. The embedded application/schema+json attachment parsed to exactly the same schema value as structured schema_data; its pretty-printed text was 12,635 characters.
3. The resource URI from that response was read first with `?offset=0&limit=1` to establish size, then with windows `offset=0, limit=6000` and `offset=6000, limit=6000`. Page lengths were 6,000 and 5,927; next offsets were 6,000 and null. The assembled string exactly matched the complete structured result, parsed successfully, and retained required schema fields `class_name`, `class_description` and `module_description`. One SHA-256 verification matched the resource identity.
4. Reading a deliberately absent 32-hex-character run ID produced MCP error 0, `No cached data found`. This proves an explicit missing-result diagnosis, not recovery of expired output.
5. The source of the current cache route is [CachedResponseResource](../../../mcp_server/resources/cache.py). It returns the operation DTO, not the independently rendered notes or every attachment. [Server assembly](../../../mcp_server/server.py) publishes those separately. Complete-output acceptance must therefore check their union, rather than describing the cache alone as a complete MCP response.

A repeat of steps 2–3 must use the URI from the new invocation. The previous run ID is transient evidence, not a durable dependency. The existing [cache guide](../../../mcp_server/resources/cache_reading.md) defines Unicode offsets, contiguous windows, full-content identity and safe recovery constraints.

### Isolated real-harness feasibility: Pi 1.3.0

The owner asked whether Codex could create isolated environments and execute real harnesses. This was demonstrated on 2026-10-19, rather than left as a proposed test.

| Item | Executed setup or observation |
|---|---|
| Harness | Official npm package `@earendil-works/pi-coding-agent`, resolved to 1.3.0; launched through the package manifest's declared `bin.pi` entry with Node 24.14.0. |
| Local installation | `.pgmcp/temp/issue529/pi-runtime`; npm cache, agent configuration and working directory are separate siblings under the same issue directory. No global install or PATH change. Initial sandbox network access failed with EACCES; the scoped download then succeeded through the approved network escalation. |
| Isolation boundary | Separate process/configuration/workspace, not a VM or OS security boundary. No inherited provider credentials; explicit local-only provider. Context-file discovery, discovered extensions, skills and prompt templates disabled; only built-in MCP explicitly enabled. Automatic network activity and telemetry disabled using Pi's documented controls. |
| MCP peer | Temporary stdio server using the installed Python MCP SDK's public Server callbacks. One tool returned independent random text/JSON markers and an instruction. One resource exposed a larger payload in explicit windows. |
| Model peer | A localhost OpenAI-compatible streaming endpoint, not a language model. It recorded real provider requests from Pi and returned predetermined tool calls. No real-model reasoning, tool choice or instruction obedience is claimed. |
| Direct delivery | Text marker and instruction present in captured tool-result model input; JSON marker absent. |
| Full output | Four real `read_mcp_resource` calls at offsets 0, 6000, 12000 and 18000; all 22,086 characters recovered with exact equality. Six provider requests captured in total. |
| Native execution | `run_tests(scope="targets", targets=[".pgmcp/temp/issue529/test_pi_probe.py"], tests=["python_tests"], args={"python_tests":["-n","0","-q","--tb=short"]}, timeout_seconds=180)`: one passed in 2.58 seconds, exit 0, Python 3.15.0 / pytest 9.1.1. |
| Local inspection | Fixture `.pgmcp/temp/issue529/test_pi_probe.py`; report and captured requests under `pi-run/report.json` and `pi-run/model-requests.json`. These ignored temporary files supplement this committed invocation/outcome record; they are not permanent suite coverage or guaranteed future assets. |
| Limits | One mixed-channel successful result and complete resource reading. Structured-only fallback, errors, schema attachments, truncation, codemode, another provider format and every other harness still need their own evidence. |

To reproduce the method, install the pinned official Pi package locally, use a fresh `PI_CODING_AGENT_DIR`, define a localhost `openai-completions` provider and a direct-exposure stdio MCP server, and launch Pi with `--no-context-files --no-extensions --extension builtin:mcp --no-session --offline`. The local protocol peer first requests the mixed-channel tool and then the four resource windows. Compare actual role=tool messages in the provider requests against independently generated server markers and the full source payload. The installed harness performs its normal discovery, tool execution and result conversion; a copied converter is not substituted.

The process/config isolation and custom provider route are documented by [Pi environment variables](https://pi.dev/docs/latest/environment-variables), [model configuration](https://pi.dev/docs/latest/models-configuration) and [CLI options](https://pi.dev/docs/latest/cli). Read-only inspection and a deterministic local peer are sufficient to measure result delivery, but not to certify model behavior or GUI variants.

### Isolated CLI execution: Kilo, Kimi and Claude Code

On 2026-10-19 the owner requested the same real-harness measurement for these three CLIs. Official locally installed entry points executed against the same public stdio MCP callbacks and a localhost provider capture peer as the Pi method. Independent random markers distinguish short content from structuredContent; the instruction exists only in text. Resource pages use offsets 0, 6000, 12000 and 18000, limit 6000, for a 22,086-character payload. The provider peer selects tools deterministically; no claim is made about autonomous LLM choices or instruction obedience.

| Native execution | Text / instruction in model input | JSON marker | Complete data observed |
|---|---|---|---|
| Kilo 7.8.12, direct MCP | Present / present | Absent | Four native resource reads; exact recovery of 22,086 characters. |
| Kimi Code 2.2.0, mixed-channel result | Present / present | Present | No native resource-reading tool offered in the captured catalog. |
| Kimi Code 2.2.0, additional full-inline result | Present / present | Present | All 22,086 source characters present inline in the model's tool-result input. |
| Claude Code 2.1.303, isolated bare invocation | Absent / absent | Present | Four native resource reads; exact recovery of 22,086 characters. |
| Claude Code 2.1.303, control without bare mode | Absent / absent | Present | Same complete four-window recovery. Text loss is not explained by bare mode. |

The text/JSON/instruction observations were additionally checked across **all** captured model messages, not only the extracted tool-result blocks. Resource output can include native descriptive wrappers; decoding those wrappers correctly was part of measurement, not a harness patch. Claude's ordinary reader was selected by its exact public name, excluding the separate directory reader.

**Reproduction:** local installations live under ignored .pgmcp/temp/issue529/ in kilo-runtime, kimi-code-runtime and claude-runtime. Kilo launches the manifest-declared bin.kilo via Node 24.14.0 with run --pure --format json --model openai-compatible/probe --auto and an isolated KILO_CONFIG_DIR, XDG directories and KILO_CONFIG_CONTENT. Its openai-compatible provider points only to the local capture endpoint. Kimi launches manifest bin.kimi via Node with --model probe --output-format stream-json --prompt, separate KIMI_CODE_HOME/config.toml and mcp.json, an openai provider, telemetry and automatic upgrade disabled. Claude launches the official claude-code-win32-x64/claude.exe with --print --verbose --output-format stream-json, explicit local ANTHROPIC_BASE_URL/API_KEY, separate CLAUDE_CONFIG_DIR, --strict-mcp-config, empty --setting-sources, --no-session-persistence and explicitly allowed probe/resource tools. The second Claude execution removes --bare. OpenAI Chat Completions and Anthropic Messages SSE are served by the local peer; actual provider requests are captured after MCP processing.

Kimi's official current [installation instructions](https://www.kimi.com/code/docs/en/kimi-code-cli/guides/getting-started) identify @moonshot-ai/kimi-code. The initially installed Python kimi-cli 1.52.0 prints a retirement notice and was not used as current-harness evidence. Its earlier source-based conclusion is superseded. [Kimi configuration](https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/config-files) and [Kilo custom providers](https://kilo.ai/docs/code-with-ai/agents/custom-models) document the local-endpoint routes.

**Exact focused invocation:** run_tests(scope="targets", targets=[".pgmcp/temp/issue529/test_cli_probes.py"], tests=["python_tests"], args={"python_tests":["-n","0","-q","--tb=short"]}, timeout_seconds=300). Final native result: five measurement cases passed in 43.78 seconds, exit 0, Python 3.15.0 / pytest 9.1.1. Passing means that measurement executed successfully; it does not convert Claude's missing instructions or Kimi's absent reader into accepted behavior.

The temporary fixture and per-variant report.json, model-requests.json and CLI output under *-run are supplemental local inspection aids, not permanent test-suite additions or durable dependencies. Process/configuration/workspace isolation is not a VM or security sandbox. Production code, active harness configuration and the pgmcp delivery contract remain unchanged.

**Remaining proof:** ordinary data retrieval does not establish the complete response union. Schema attachments, error routes, client truncation limits and missing/expired resources still require targeted evidence. Kimi's inline result proves this payload size, not unlimited output or a later cache-reading route. Claude currently fails the owner's direct text/instruction requirement for the measured mixed response even though resource retrieval works. No remediation has been selected.

### Unattended routes and executed boundaries

The VS Code and Antigravity routes below have now been attempted or executed. CLI/SDK and graphical-agent proof remain distinct:

| Harness | Concrete unattended route | Proof boundary / unresolved step |
|---|---|---|
| VS Code | Executed a separate 1.142.0 Extension Test Host with isolated profile/workspace and a registered capture-model provider; invoked the actual built-in Local agent via workbench.action.chat.open. | Provider selection and MCP discovery succeeded, but the native default agent did not become ready; zero model requests. No output-delivery conclusion. Neither lm.invokeTool nor a custom agent loop was substituted. Copilot/Agent Host remains a separate, untested delivery route. |
| Antigravity | Executed official SDK 0.1.22 LocalOpenAIAgentConfig → native localharness.exe with the same localhost capture peer. | Text/instruction delivery and exact resource/file recovery proven on this route. This does not certify graphical app, IDE or CLI behavior. |
| Cursor | A dedicated profile and the official headless agent/ACP route can drive the synthetic MCP server; retain provider-input evidence where exposed, otherwise a native-agent marker recovery plus server request trace. | [Headless operation](https://cursor.com/docs/cli/headless) is documented, and [authentication](https://cursor.com/docs/cli/reference/authentication) requires a Cursor login or API key. A fully local, account-free provider capture route for Cursor's native agent is not established. CLI/ACP success alone would not certify the IDE. Do not substitute VS Code's implementation for Cursor's agent. |

VS Code's built-in Local-agent readiness remains an environment/integration blocker, requiring a working matching runtime before delivery can be measured. Do not repair or bypass its conversion and then present that as stock-harness evidence. Antigravity app/IDE delivery and VS Code Copilot/Agent Host still require separate proof. These findings do not yet select a harness-specific pgmcp configuration or production workaround.

### Executed unattended probes: Antigravity and VS Code

**Antigravity: positive native SDK-route evidence.** Installed google-antigravity 0.1.22 in its own Python 3.13.7 environment. Public Agent.chat runs LocalOpenAIAgentConfig against the localhost OpenAI-compatible capture peer and a stdio MCP server. The SDK starts its bundled native localharness.exe; no converter or agent loop was replaced. Explicit workspaces, app_data_dir, save_dir and policies apply only to this isolated run. Native provider messages contain the random text marker and independent instruction, but not the structuredContent marker.

Resource reads take two actual native calls per page: read_resource with ServerName/Uri returns a generated file URI, then view_file with AbsolutePath reads the saved resource into model input. The deterministic peer followed those pointers for all four pages; source payload and recovered model-visible payload match exactly at 22,086 characters. Ten provider requests carried the initial tool result and four resource/file pairs. The final focused invocation was run_tests(scope="targets", targets=[".pgmcp/temp/issue529/test_antigravity_probe.py"], tests=["python_tests"], args={"python_tests":["-n","0","-q","--tb=short"]}, timeout_seconds=180): one passed in 5.55 seconds, exit 0, including exact-recovery assertion. Temporary fixture, report and captured requests are under .pgmcp/temp/issue529/ and antigravity-channels-run. This proves the SDK/native local-harness route, not the graphical app, IDE or CLI. [Official SDK local-provider configuration](https://antigravity.google/docs/sdk/local-models/) and [MCP setup](https://antigravity.google/docs/sdk/mcp/) describe the public entry points.

**VS Code: real built-in agent attempt, delivery blocked.** The official test-electron downloader resolved stable to 1.142.0 and downloaded a separate Windows archive. Actual product commit is 6d62b1d5dace93a33b3a6d3eca1317bd5e15bcb1, distinct from the earlier GitHub release-tag inspection. The archive bundles Copilot Chat 0.70.0. The Marketplace installation command offered an older 0.48.1 and refused the downgrade; no downgrade was performed. A temporary LanguageModelChatProvider was registered in an actual Extension Test Host, with dedicated user-data, extensions and workspace directories. Workspace MCP configuration started the public stdio probe and discovered one tool. The real command workbench.action.chat.open selected mode=agent, the explicit issue529/probe model and blockOnResponse=true. Local-harness preference and signed-out/BYOK settings were explicit; no real account was used.

The final attempt additionally loaded the archive's unchanged Copilot extension as a development extension so its activation was observable. It registered as GitHub.copilot-chat 0.70.0, yet the built-in chat still failed before invoking the capture model. Renderer diagnostics include No default agent registered and a setup timeout with agentReady=false, languageModelHasRequestedModel=true and toolsModelReady=true. The archive also reports a product/extension API-proposal mismatch. These are observed startup diagnoses, not a proven root-cause attribution to authentication or MCP delivery. Zero provider requests means text, instruction, structuredContent and resource recovery remain **unmeasured**, not absent.

Exact focused invocation: run_tests(scope="targets", targets=[".pgmcp/temp/issue529/test_vscode_probe.py"], tests=["python_tests"], args={"python_tests":["-n","0","-q","--tb=short"]}, timeout_seconds=180). Final measurement case completed in 68.79 seconds; the application exited 0 after the fixture recorded Native chat did not complete within 65 seconds. The fixture's passed measurement status is **not** a passed agent-delivery result. Local diagnostics are under vscode-local-run/report.json, extension/execution.json and user-data/logs. No model-result claim is based on a manual lm.invokeTool call or custom agent loop. All probe-launched Code and localharness processes had exited at the final inventory.

Automatic approval review rejected a proposed test-child HOME/USERPROFILE override because the agent rules forbid repurposing those variables, and rejected the dependent execution. Those edits were not applied. The safer final fixture retained those variables and used only VS Code-specific directories plus COPILOT_HOME; that execution was admitted. Isolation remains process/profile based, not a VM or general filesystem boundary. No active harness configuration, production code or delivery mechanism was changed.

### Material limits and uncertainties

- Earlier [Claude report 79944](https://github.com/anthropics/claude-code/issues/79944) and [report 45575](https://github.com/anthropics/claude-code/issues/45575) described conflicting model/UI behavior. The executed 2.1.303 probe now proves model-input text/instruction loss for the mixed-channel response, both with and without `--bare`; the issue reports remain historical context.
- ZCode's default MCP [budget declaration](https://github.com/zai-org/ZCode/blob/0a1fc56d279fd1001f78387bd81aec1c26767411/apps/zcode-cli/packages/core/src/mcp/index.ts#L150) uses truncation, while [artifact persistence](https://github.com/zai-org/ZCode/blob/0a1fc56d279fd1001f78387bd81aec1c26767411/apps/zcode-cli/packages/core/src/tool/executor/result-serialization.ts#L97) requires the separate artifact strategy and enabled setting. A complete saved copy cannot be assumed for ordinary pgmcp tools.
- The current [text limiter](../../../mcp_server/presenters/text_budget_limiter.py) reserves a truncation notice and cache reference, not a separately protected instruction region. Because [TextPresenter](../../../mcp_server/presenters/text_presenter.py) appends guidance before that final limit, mandatory-guidance preservation also needs explicit treatment at the pgmcp boundary. This is source-derived reachability analysis, not a newly executed truncation scenario.
- Only `code.cmd` and `codex.exe` were found among the requested CLI names on the current PATH. The VS Code launcher selects a versioned installation directory; an earlier check of an unversioned app path was inconclusive. Missing PATH entries do not prove that the other products are absent from all hosts or install locations.
- Pi 1.3.0 has now been exercised through its actual CLI and model-provider request boundary. No installed execution is claimed for the other six required harnesses. GUI variants and provider-specific behavior remain separate evidence obligations.

### Decision status after owner correction

The owner rejected the early move to contract options. The earlier A/B recommendation is withdrawn. No output mechanism, generic retrieval tool or harness-specific configuration is selected. Complete the factual channel/read-route inventory and resolve material integration/version gaps before presenting solutions or requesting a boundary strategy. The mandatory direct text/instruction delivery and complete-output access requirements remain unchanged.

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
| 0.2 | 2026-10-19 | @imp researcher | Withdraw premature contract options; distinguish VS Code 1.142 Local and Copilot harnesses, correct the version basis and Kilo structured-only fallback, and replace route recommendations with a compact factual inventory. |
| 0.3 | 2026-10-19 | @imp researcher | Execute an isolated official Pi 1.3.0 CLI probe; record captured model input, complete four-window resource retrieval, exact verification and the limits of a deterministic model peer. |
| 0.4 | 2026-10-19 | @imp researcher | Execute Kilo 7.8.12, current Kimi Code 2.2.0 and Claude Code 2.1.303; prove channel differences, resource recovery, Kimi full-inline delivery and Claude normal-mode control; record bounded unattended IDE probe routes. |
| 0.5 | 2026-10-19 | @imp researcher | Prove Antigravity SDK/native local-harness text and resource/file recovery; execute the real VS Code 1.142.0 Local-agent attempt and record its pre-model readiness failure without claiming delivery success. |
