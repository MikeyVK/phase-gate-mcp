<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue \#529 — Harness delivery and complete-output access

**Status:** FINAL — Research content approved by independent QA; workflow aligned for Design  
**Version:** 1.2  
**Last Updated:** 2026-10-19

## Purpose

Establish an evidence-backed client delivery contract before #528 chooses catalog output schemas.

## Scope In

Configurable response profiles built on the existing presentation configuration, independent selection for multiple harnesses sharing a workspace, preservation of short text and mandatory instructions, complete-output routes and proportionate validation of pgmcp's delivery contract. Existing client probes remain explicitly scoped supporting evidence; the owner has stopped further probing. Research extends #523 rather than repeating its history.

## Scope Out

No production implementation or active harness configuration changes in this Research step. The configurable-profile direction and a safely bounded emergency text response on cache-publication failure are approved directions. The owner has approved the common public structured envelope and preservation of the mandatory core outside the diagnostic-detail budget. No historical-version matrix, compatibility bridge, release or #528 implementation.

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

The table describes observed or documented behavior, not a recommendation or an accepted support guarantee. "Source" means code inspection; this Codex integration, isolated Pi 1.3.0, Kilo 7.8.12, Kimi Code 2.2.0 and Claude Code 2.1.303 CLIs, and Antigravity SDK 0.1.22's native local harness were exercised here. The VS Code 1.142.0 built-in Local agent now completed actual MCP tool turns through its stock Custom Endpoint provider; the earlier startup failure was a probe-setup problem.

| Harness / route | Model-facing result when text and structuredContent are both present | Agent access to additional/full output | Evidence and remaining gap |
|---|---|---|---|
| VS Code 1.142.0, built-in Local agent, stock Custom Endpoint provider | Executed: the small result's structuredContent marker reaches the model; independent text and instruction do not. | A 22-KB result is saved as content.json and schema.json. Native read_file truncates long lines. Full 22,086-character recovery is now executed through native grep_search with the result-storage folder explicitly inside the workspace; outside-workspace control fails. Native terminal paging requires first-use approval in a fresh profile and was not executed. | Actual github.copilot.editsAgent tool rounds and captured HTTP model requests. Earlier blocked Test Host attempts are superseded by the ordinary Development Host probe below. Copilot/Agent Host is a different route. |
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

**Limits of these earlier probes:** ordinary data retrieval did not establish the complete response union, schema attachments, error routes, client truncation limits or missing/expired resources. These are limits on the observations, not additional probe requirements after the owner's later scope decision. Kimi's inline result proves this payload size, not unlimited output or a later cache-reading route. Claude currently fails the owner's direct text/instruction requirement for the measured mixed response even though resource retrieval works. No remediation has been selected.

### Unattended routes and executed boundaries

The VS Code and Antigravity routes below have now been attempted or executed. CLI/SDK and graphical-agent proof remain distinct:

| Harness | Concrete unattended route | Proof boundary / unresolved step |
|---|---|---|
| VS Code | Executed the real built-in Local agent in ordinary Development Host mode, with isolated native Custom Endpoint configuration and localhost provider capture. | Small mixed-channel delivery and native large-result file handling are measured. Text/instruction loss remains. Complete long-line retrieval is proved with explicitly added workspace read scope; automatic recovery in a default fresh profile is not proved. No copied converter or custom agent loop. |
| Antigravity | Executed official SDK 0.1.22 LocalOpenAIAgentConfig → native localharness.exe with the same localhost capture peer. | Text/instruction delivery and exact resource/file recovery proven on this route. This does not certify graphical app, IDE or CLI behavior. |
| Cursor | A dedicated profile and the official headless agent/ACP route can drive the synthetic MCP server; retain provider-input evidence where exposed, otherwise a native-agent marker recovery plus server request trace. | [Headless operation](https://cursor.com/docs/cli/headless) is documented, and [authentication](https://cursor.com/docs/cli/reference/authentication) requires a Cursor login or API key. A fully local, account-free provider capture route for Cursor's native agent is not established. CLI/ACP success alone would not certify the IDE. Do not substitute VS Code's implementation for Cursor's agent. |

The VS Code Local-agent startup problem has been resolved in the probe setup. Antigravity app/IDE delivery and VS Code Copilot/Agent Host still require separate proof. Neither the native text loss nor the large-result read limitation selects a pgmcp production workaround.

### Executed unattended probes: Antigravity and VS Code

**Antigravity: positive native SDK-route evidence.** Installed google-antigravity 0.1.22 in its own Python 3.13.7 environment. Public Agent.chat runs LocalOpenAIAgentConfig against the localhost OpenAI-compatible capture peer and a stdio MCP server. The SDK starts its bundled native localharness.exe; no converter or agent loop was replaced. Explicit workspaces, app_data_dir, save_dir and policies apply only to this isolated run. Native provider messages contain the random text marker and independent instruction, but not the structuredContent marker.

Resource reads take two actual native calls per page: read_resource with ServerName/Uri returns a generated file URI, then view_file with AbsolutePath reads the saved resource into model input. The deterministic peer followed those pointers for all four pages; source payload and recovered model-visible payload match exactly at 22,086 characters. Ten provider requests carried the initial tool result and four resource/file pairs. The final focused invocation was run_tests(scope="targets", targets=[".pgmcp/temp/issue529/test_antigravity_probe.py"], tests=["python_tests"], args={"python_tests":["-n","0","-q","--tb=short"]}, timeout_seconds=180): one passed in 5.55 seconds, exit 0, including exact-recovery assertion. Temporary fixture, report and captured requests are under .pgmcp/temp/issue529/ and antigravity-channels-run. This proves the SDK/native local-harness route, not the graphical app, IDE or CLI. [Official SDK local-provider configuration](https://antigravity.google/docs/sdk/local-models/) and [MCP setup](https://antigravity.google/docs/sdk/mcp/) describe the public entry points.

**Earlier VS Code attempt: blocked Test Host setup, superseded by the resolved ordinary-host probe below.** The official test-electron downloader resolved stable to 1.142.0 and downloaded a separate Windows archive. Actual product commit is 6d62b1d5dace93a33b3a6d3eca1317bd5e15bcb1, distinct from the earlier GitHub release-tag inspection. The archive bundles Copilot Chat 0.70.0. The Marketplace installation command offered an older 0.48.1 and refused the downgrade; no downgrade was performed. A temporary LanguageModelChatProvider was registered in an actual Extension Test Host, with dedicated user-data, extensions and workspace directories. Workspace MCP configuration started the public stdio probe and discovered one tool. The real command workbench.action.chat.open selected mode=agent, the explicit issue529/probe model and blockOnResponse=true. Local-harness preference and signed-out/BYOK settings were explicit; no real account was used.

The final attempt additionally loaded the archive's unchanged Copilot extension as a development extension so its activation was observable. It registered as GitHub.copilot-chat 0.70.0, yet the built-in chat still failed before invoking the capture model. Renderer diagnostics include No default agent registered and a setup timeout with agentReady=false, languageModelHasRequestedModel=true and toolsModelReady=true. The archive also reports a product/extension API-proposal mismatch. These are observed startup diagnoses, not a proven root-cause attribution to authentication or MCP delivery. Zero provider requests means text, instruction, structuredContent and resource recovery remain **unmeasured**, not absent.

Exact focused invocation: run_tests(scope="targets", targets=[".pgmcp/temp/issue529/test_vscode_probe.py"], tests=["python_tests"], args={"python_tests":["-n","0","-q","--tb=short"]}, timeout_seconds=180). Final measurement case completed in 68.79 seconds; the application exited 0 after the fixture recorded Native chat did not complete within 65 seconds. The fixture's passed measurement status is **not** a passed agent-delivery result. Local diagnostics are under vscode-local-run/report.json, extension/execution.json and user-data/logs. No model-result claim is based on a manual lm.invokeTool call or custom agent loop. All probe-launched Code and localharness processes had exited at the final inventory.

Automatic approval review rejected a proposed test-child HOME/USERPROFILE override because the agent rules forbid repurposing those variables, and rejected the dependent execution. Those edits were not applied. The safer final fixture retained those variables and used only VS Code-specific directories plus COPILOT_HOME; that execution was admitted. Isolation remains process/profile based, not a VM or general filesystem boundary. No active harness configuration, production code or delivery mechanism was changed.

### VS Code startup diagnosis and working native Local-agent probe

The owner requested a targeted repair of the isolated probe, without interaction or changes to the active installation. The final route is stock VS Code 1.142.0 / bundled Copilot Chat 0.70.0, ordinary Extension Development Host, built-in **github.copilot.editsAgent**, and the built-in Custom Endpoint provider using a localhost Chat Completions peer. A temporary extension only initiates the real chat through workbench.action.chat.open; it does not implement the agent loop or convert MCP results.

| Diagnosed probe issue | Correction / evidence |
|---|---|
| Copilot's compiled activation entry returns early in ExtensionMode.Test unless its own special activation controls apply. | Removed extensionTestsPath; ordinary host logs show BYOK availability and conversation contributions activating. No Copilot code or internal activation hook was changed. |
| A fresh profile needs first-run chat setup before built-in providers are discoverable. | Used the native triggerSetupAnonymousWithoutDialog command and explicit Custom Endpoint configuration. No existing account or owner interaction. Initialization and metadata traffic are distinct from inference; earlier title fallback attempts returned model_not_supported. |
| The probe enabled global automatic tool approval without its first-use opt-in. Native _checkGlobalAutoApprove can wait on a warning dialog. | Returned global approval to false and truthfully annotated the synthetic tool readOnlyHint=true. Actual native MCP tool calls then completed. No consent flag was forged and no warning was clicked through. |
| The deterministic peer returned ordinary text to background requests that require a JSON array. | Added a valid deterministic JSON-array response for the progress-message requests; corrected utility references to vendor/id. Utility requests remain excluded from delivery proof. |
| user-data-dir alone does not isolate the new application-wide shared storage. | Added the native shared-data-dir option and retained COPILOT_HOME. Each final case uses fresh random profile/workspace directories, avoiding stale session/server evidence. No HOME/USERPROFILE override. |

The API-proposal mismatch warning still appears in the downloaded distribution, but it does not prevent these successful native tool rounds. It was not repaired or used as an unsupported root-cause claim. Windows Computer Use did not expose a targetable probe window; no UI consent or authentication action was automated.

**Measured output:**

| Case | Actual agent/model observation |
|---|---|
| Small successful mixed response | Native Local agent invokes mcp_isolated-outp_probe_channels and sends its result to the local model. JSON marker present; independent short text and REQUIRED NEXT STEP instruction absent. Five captured provider requests include utility calls; the MCP call and returned tool-result messages separately establish agent delivery. |
| Large structured response, 22,086 source characters | Native result tells the model to read generated content.json and schema.json files. No direct MCP resource reader is exposed in this route's captured tool catalog. |
| Native file recovery | The agent invokes native read_file for both supplied paths. The 137-character generated schema is received exactly. The data file physically retains all 22,086 payload characters, but read_file returns a prefix and explicitly reports One or more long lines were truncated at 2000 characters. Complete model-side payload recovery therefore fails. |

The final focused invocation was run_tests(scope="targets", targets=[".pgmcp/temp/issue529/test_vscode_probe.py"], tests=["python_tests"], args={"python_tests":["-n","0","-q","--tb=short"]}, timeout_seconds=240). Result: **one passed, one failed in 31.49 seconds**, native exit 1. Both native agent executions reached complete; the negative case is the explicit full-payload assertion, not agent startup. No gate exception or phase progression follows from this measurement.

Temporary reports are indexed by vscode-native-http-latest-report.json and vscode-native-http-inline-latest-report.json; each identifies its unique run directory and captured provider requests. The committed invocation, route, values and negative result above are the durable evidence. The old no-MCP control produced title/progress requests only and is not evidence of a working main agent.

[Official BYOK documentation](https://code.visualstudio.com/docs/agent-customization/language-models) describes stock Custom Endpoint configuration, vendor/model utility settings and account-independent local models. Preferred measured data access on this Local route is inline structured data for small results, generated data/schema files for larger results. **The conditional native-search recovery below supersedes the previous absence of any complete long-line recovery proof; default-profile recovery remains unproved.** Direct text/instruction delivery remains unmet independently of that recovery gap. Copilot/Agent Host, errors and schema attachments are not certified by these cases. Production pgmcp behavior and the active VS Code installation were not modified.

### VS Code complete-output recovery through existing harness tools

The owner's follow-up required an actual isolated readback route, without new pgmcp functionality. The same released Local-agent route now executed native search calls and delivered the entire long JSON field to the localhost model peer. The synthetic field stayed one long line; its 22,000-character body used random hexadecimal data between independent boundary markers, for 22,086 characters total. The source was neither split nor rewritten to evade read_file's limit.

| Route / condition | Executed observation |
|---|---|
| Native read_file | The generated 137-character schema reaches the model exactly. The data prefix and JSON marker are readable, but the long value is cut at 2,000 characters. |
| Native run_in_terminal with bounded Python read commands | The fresh profile recognizes an exact, read-only command-line approval rule, but still returns a native tool confirmation. First-use terminal approval needs owner interaction. The probe did not forge the approval flag or accept the warning. This establishes an admission limit, not successful terminal execution. |
| Native grep_search with result storage added as a workspace folder | A public workspace.updateWorkspaceFolders call adds only this probe's isolated User/workspaceStorage directory. The actual agent executes 74 native searches, each matching at most 300 characters, in batches of eight tool calls. All 22,086 characters are reconstructed exclusively from captured model-facing tool messages and equal the source exactly. The schema also equals its source exactly. |
| Native grep_search with the original workspace only | The same agent requests the external content.json absolute path, without the extra folder. Search returns empty output; zero payload characters are recovered. The successful condition must not be presented as default outside-workspace search capability. |

The native search output itself bounds long matches to 300 characters and includes preceding/following context. Each query uses a fixed-offset lookbehind against the full_output value, for example (?<=^  "full_output": ".{6000}).{300}. The measurement uses the returned match column and the stock 150-character preceding-context bound to extract the requested slice. It never fills missing characters from host-side source data. The final 186-character slice reaches the independently generated end marker. There are 74 distinct slices, 17 captured provider requests including utility traffic, and a maximum of 947 characters per search-result message. This is a capability proof with substantial call overhead, not a proposed default retrieval algorithm.

Exact successful invocation: run_tests(scope="targets", targets=[".pgmcp/temp/issue529/test_vscode_probe.py"], tests=["python_tests"], args={"python_tests":["-n","0","-q","--tb=short","-k","grep"]}, timeout_seconds=240), at the four-case fixture snapshot before the external control was added. Result: **one passed, three deselected in 26.56 seconds**, native exit 0; report vscode-native-http-inline-grep-latest-report.json identifies unique run vscode-native-http-inline-grep-437f11e8-run. At the final five-case snapshot, select this positive case with -k "grep and not external". The separately executed external control uses -k external: **one failed, four deselected in 22.91 seconds**, native exit 1, solely on full recovery; native chat completed. Its report is vscode-native-http-inline-external-grep-latest-report.json, run vscode-native-http-inline-external-grep-653c0510-run.

The final terminal attempt uses -k terminal: **one failed, two deselected in 15.58 seconds**, native exit 1; execution stopped at the native confirmation, with no recovered pages. Two preceding PowerShell admission attempts also failed: one initially targeted the wrong storage location; the corrected location still required confirmation and the compound syntax was not safely auto-approved. These are probe admission failures, not pgmcp production defects. The final Python command's native allow-list match does not substitute for first-use consent. [VS Code's approval documentation](https://code.visualstudio.com/docs/agents/run/approvals) describes exact/regex command rules and distinguishes terminal permissions from other tool permissions. [The upstream long-line issue](https://github.com/microsoft/vscode/issues/321578) documents the same read_file limit and suggests script-based file parsing as a workaround.

**Preferred-route evidence:** the native generated data/schema files are the established large-result carrier. Native terminal parsing into bounded pages is the practical candidate after normal terminal consent, but this unattended probe did not execute it. Native search is a demonstrated read-only alternative when the generated storage is included in workspace scope, with significant overhead. Neither precondition is silently enabled for target installations. No final support policy or harness-specific pgmcp configuration is selected by this capability experiment.

The peer deterministically supplies tool calls; it proves what the real agent executes and sends back to its model, not whether an autonomous LLM will choose this workaround. Independent short text and REQUIRED NEXT STEP remain absent even in the successful recovery case. Therefore complete structured-data reachability does not solve the separate instruction-delivery defect. These results certify neither the Copilot/Agent Host route nor arbitrary payload sizes, error delivery or schema attachments. No production files, new pgmcp retrieval tool, permanent test, active VS Code profile or active installation changed. The final process inventory found zero processes using the isolated downloaded Code.exe.

### Material limits and uncertainties

- Earlier [Claude report 79944](https://github.com/anthropics/claude-code/issues/79944) and [report 45575](https://github.com/anthropics/claude-code/issues/45575) described conflicting model/UI behavior. The executed 2.1.303 probe now proves model-input text/instruction loss for the mixed-channel response, both with and without `--bare`; the issue reports remain historical context.
- ZCode's default MCP [budget declaration](https://github.com/zai-org/ZCode/blob/0a1fc56d279fd1001f78387bd81aec1c26767411/apps/zcode-cli/packages/core/src/mcp/index.ts#L150) uses truncation, while [artifact persistence](https://github.com/zai-org/ZCode/blob/0a1fc56d279fd1001f78387bd81aec1c26767411/apps/zcode-cli/packages/core/src/tool/executor/result-serialization.ts#L97) requires the separate artifact strategy and enabled setting. A complete saved copy cannot be assumed for ordinary pgmcp tools.
- The current [text limiter](../../../mcp_server/presenters/text_budget_limiter.py) reserves a truncation notice and cache reference, not a separately protected instruction region. Because [TextPresenter](../../../mcp_server/presenters/text_presenter.py) appends guidance before that final limit, mandatory-guidance preservation also needs explicit treatment at the pgmcp boundary. This is source-derived reachability analysis, not a newly executed truncation scenario.
- Only `code.cmd` and `codex.exe` were found among the requested CLI names on the current PATH. The VS Code launcher selects a versioned installation directory; an earlier check of an unversioned app path was inconclusive. Missing PATH entries do not prove that the other products are absent from all hosts or install locations.
- Executed delivery evidence is limited to the explicitly named CLI, SDK/native and VS Code Local routes above. ZCode, Antigravity app/IDE and VS Code Copilot/Agent Host do not inherit another route's result; GUI variants and provider-specific behavior remain unproved; after the owner stopped probing, they are limits on claims rather than additional Research tasks.

### Decision status after owner correction

The earlier A/B recommendation remains withdrawn. After the capability probes, the owner stopped further probing and approved investigation of a minimal configurable response policy built on presentation.yaml. The owner requires short text and mandatory instructions to survive every supported profile, and explicitly requires independent use by multiple harnesses sharing one workspace. The owner subsequently approved presentation_channel and reiterated a clean break with no compatibility paths and profile/result-focused tests instead of harness-specific tests. The factual investigation is complete; there is no remaining probe campaign. The owner subsequently accepted the emergency text route subject to safe configurable diagnostic limits and no size-induced crash. This replaces the earlier unlimited-inline recommendation. The owner has now explicitly approved the common public structured envelope and confirmed that the mandatory core must always remain complete; only diagnostic details may be bounded. No strategic owner choice remains open.

### Minimal response-profile proposal

The owner-approved direction uses three independent delivery controls:

| Proposed profile field | Values | Meaning |
|---|---|---|
| presentation_channel | text, structured, both | Publish the complete short explanation and mandatory instructions in the selected channel(s). There is no off value. |
| data_channel | structured, text | Put the operation data or its resource reference, and an accessible representation of attachments, into structuredContent or text content. |
| data_delivery | inline, resource | Include the complete operation DTO directly, or reference the existing cached operation resource. Resource mode requires an agent-accessible MCP resource route in the selected installation; server startup cannot infer that route from the client name. |

A proposed presentation.yaml excerpt, to be added beside existing global/tools declarations, is:

~~~yaml
global:
  default_response_profile: structured_inline
  max_text_response_bytes: 8000
  cache_read_budget_chars: 6000

response_profiles:
  structured_inline:
    presentation_channel: both
    data_channel: structured
    data_delivery: inline
  structured_resource:
    presentation_channel: both
    data_channel: structured
    data_delivery: resource
  text_inline:
    presentation_channel: text
    data_channel: text
    data_delivery: inline
~~~

These are capability profiles, not client-name branches or a certification list. Earlier assertions that presentation must always be duplicated into both channels are superseded by the owner's explicit presentation_channel decision. Profile keys supply identity; no ordering behavior or duplicated id field is required. Existing templates, notes, collection declarations and wording stay shared. Existing numeric controls can remain global with optional overrides of those same fields within a profile; resolving them is explicit profile composition, not a new file loader. The cache_read_budget_chars setting currently determines when pagination guidance is shown; it is not a resource-read page-size limit. Resource windows still use the existing explicit offset/limit contract. Do not silently turn that field into a new paging control.

Proposed selection is one new launcher environment value, PGMCP_RESPONSE_PROFILE. Each harness sets it only on its own PGMCP process. The selector uses Settings.from_env and the existing ConfigLoader/assembly boundary; it is not a tool argument or a shared state.json setting. Definitions use the existing defaults/workspace-override chain. If the selector is absent, the explicitly declared global.default_response_profile applies; unknown IDs are configuration errors through the existing startup recovery path. The code must not contain a hidden default ID or infer a profile from clientInfo.

The source supports this direction: [Settings](../../../mcp_server/config/settings.py) owns launcher environment resolution; [proxy](../../../mcp_server/core/proxy.py) passes its environment into each child generation; [bootstrap](../../../mcp_server/bootstrap.py) loads presentation configuration and constructs the presenter. Selection stays local to one server instance and unchanged across its ordinary child restarts. A changed launch selector requires reconnect/relaunch. A profile edit affecting the response schema requires catalog refresh/reconnection; do not change shapes during calls under a stale catalog.

#### Fixed preservation rules

- Render explanatory text and mandatory instructions once from the existing DTO/configuration sources. Publish them completely according to presentation_channel. Both uses the same rendered value in both places; text or structured deliberately avoids that duplication. There is no off setting and no separate setting to discard instructions.
- Preserve phase instructions embedded in get_work_context's template as well as configured next-instruction and recovery guidance. Do not recover these by parsing rendered Markdown or duplicating workflow text in a second configuration.
- Presentation budgets may shorten optional details, not the protected explanation or instructions. When protected material exceeds the configured presentation budget, preserve it and permit an explicitly documented overrun. Inline mode also promises complete operation data; its bulk data is not truncated to fit the short-presentation budget. This is a proposed change from the current hard final-text ceiling, mandated by the owner's preservation requirement.
- Keep attachment facts complete in the selected data channel. The cache currently stores operation DTOs only; resource mode must not imply that schema attachments are in that cache. Keep attachments directly available, with the existing embedded-resource representation where appropriate, rather than expanding cache ownership.
- Preserve operation outcome, isError and mandatory explanation/instructions for success, policy failures and system exceptions. Normal delivery retains complete diagnostic facts; the explicitly approved cache-publication emergency route may bound verbose diagnostic details and must disclose their omission. A presentation problem after a mutation must not be reported as though the mutation never occurred.
- Keep tools, managers, adapters and internal operation models free of client/profile branches. No automatic client fingerprinting, per-call profile switching, expression language, extra profile files, generic cache tool, or compatibility bridge is proposed.

#### Owner decisions

| Boundary | Approved direction | Consequence |
|---|---|---|
| Public structured response shape | Owner approves one common transport envelope containing the selected protected presentation, the actual operation data or its reference, and attachment representations. Internal operation DTOs remain intact. | Clean break at the public response boundary, without a dual-format path. The selected projection governs the advertised outputSchema and guides #528. Exact envelope fields belong in Design. |
| Cache publication failure in resource mode | Owner approves emergency text delivery: always preserve the mandatory core, including the actual operation outcome, explanation/instructions, cache-failure notice and any truncation notice; bound only diagnostic details configurably. | Mandatory material may exceed the detail/presentation budget. A labelled diagnostic excerpt need not parse as the original JSON, but the surrounding MCP response remains valid. No complete-result guarantee or fictitious resource reference. |

StructuredContent is needed when either the presentation channel or the data channel selects structured delivery. For example, presentation_channel=structured with data_channel=text still needs structured content for the explanation/instructions. Only a profile routing both presentation and data exclusively to text omits structuredContent and its advertised outputSchema. The advertised schema follows the actually selected structured projection. The resource profile's schema must admit a truthful delivery-failure/incomplete-result variant from the outset when that variant includes structured content. Preserve the configured mandatory structured presentation where selected. An emergency text block cannot replace schema-required structured data without a schema-valid alternative; do not change the catalog after a call.

The illustrative default remains structured_inline with presentation_channel=both; its two presentation copies are a configurable conservative choice, not a fixed requirement. text_inline routes both presentation and data to text; structured_resource is an explicit installation choice for environments with resource access. Exact profile IDs, default selection, field schema and validation combinations are Design details within this approved direction, not activated configuration.

Impact is concentrated at PresentationConfig/ConfigLoader composition, Settings and bootstrap selection, ResponsePresenter/PresentedOutput, TextBudgetLimiter and MCP response/catalog serialization. Reuse the existing error boundaries and raw-operation cache. Existing config, presenter and transport behavior tests should be adapted, with one focused same-workspace/two-instance isolation case. No permanent harness/version matrix or tests preserving the old public response shape are required. No tests or production changes were made for this proposal. This is no longer mechanical maintenance; the workflow/scope must be aligned before any implementation.

### Consumer and protocol clarification

Repository search of production mcp_server and scripts found only producers of structuredContent: server.py serializes it and mcp_converters.py initializes the SDK result. The five matching test modules assert transport behavior; no separate production reader of the existing bare structured DTO shape was found. Do not invent downstream consumer migration work or retain a compatibility path. Harnesses remain actual external consumers whose channel behavior motivates profiles.

The [official 2026-07-28 tools specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools#structured-content) allows server-defined JSON values in structuredContent. Its [output-schema rules](https://modelcontextprotocol.io/specification/2026-07-28/server/tools#output-schema) require conformance when a schema is advertised and recommend client validation. It also recommends a serialized text copy for backwards compatibility; this is SHOULD, not MUST. The clean-break/profile policy must explicitly document its channel choice. The proposed object envelope is admissible; MCP does not mandate its application field names.

Current pyproject.toml pins MCP SDK 2.3.0. Read-only inspection of its installed mcp_types definitions permits arbitrary structured JSON; the older 2025-11-25 wire definition restricts it to an object, which the proposed object envelope also satisfies. This is protocol context, not a new dependency/version-support matrix. The SDK client's public validate_tool_result path checks presence and schema conformance. #528 owns normal-registration metadata exposure; #529 supplies the selected response policy and required emergency variant.

### Bounded emergency text policy

The actual cache in [ResponseCacheManager](../../../mcp_server/state/response_cache.py) is in memory. Its publication failure returns success=false/run_id=null while retaining the underlying tool outcome. This is not a failed filesystem write. [TextPresenter](../../../mcp_server/presenters/text_presenter.py) already appends warning/JSON text on cache-publication failure, and [TextBudgetLimiter](../../../mcp_server/presenters/text_budget_limiter.py) provides UTF-8-safe cuts and Markdown-fence closure. Reuse these boundaries; their current composition does not yet prove preservation of all mandatory text or parseable truncated JSON.

Owner-approved direction, with exact field names and defaults deferred to Design:

- Provide a readable emergency text response containing the actual operation outcome, cache-publication failure, required explanation/instructions and diagnostic details up to a configurable limit.
- Add one explicit limit for emergency diagnostic detail, globally configured with optional profile override. A candidate name is max_cache_failure_detail_bytes; it limits UTF-8 detail bytes, not protected instructions. The existing 8,000-byte magnitude is a possible default, not a new global wire ceiling or an approved final field.
- Truncate diagnostic strings or select bounded fields before final transport serialization. A labelled plain-text diagnostic excerpt may contain an incomplete JSON-derived fragment and need not parse as the original operation JSON. Do not present that excerpt as a complete DTO or application/json resource. Serialize the enclosing MCP/JSON-RPC response normally and completely; never slice its serialized bytes. Preserve valid Unicode and formatting closure.
- A size overrun must not raise a new presentation failure. If the details do not fit, shorten those details. The mandatory core includes actual operation facts, explanation/instructions, cache-failure notice and any truncation notice. Always preserve it completely, even when that core alone exceeds the configured presentation budget; only diagnostic details consume the emergency detail allowance.
- Mark cache availability and truncation truthfully. Do not emit a usable-looking URI with no published result, claim completeness after shortening, or claim the omitted result is available in a log/file unless that storage is actually established.
- Retain the selected mandatory structured presentation and a schema-valid emergency indicator where the profile exposes structured content. Do not cause a second schema-validation failure while trying to deliver the text fallback.
- This explicit emergency exception may lose verbose operation/error details when no complete result can be published. It does not change ordinary complete inline/resource delivery. If the publication failure involves serialization, the fallback must not simply retry the same failed full serializer.

Profile-focused tests should prove the operation outcome is retained, oversized emergency details are safely bounded, Unicode/protocol output stays valid, instructions and truncation status survive, and no unavailable resource is advertised. Test the public response/error behavior rather than production strings or concrete harnesses. No implementation or test execution was performed for this clarification.

## Questions

None at the Research strategy boundary. On 2026-10-19 the owner explicitly approved the general envelope and instructed: preserve the mandatory core always and bound only diagnostic details. These decisions close the two earlier policy questions.

Exact field names, default limits, envelope/schema variants and validation of supported profile combinations are Design work within this approved strategy. The branch was originally registered as chore. On 2026-10-19 the owner explicitly authorized a one-time direct registration correction to refactor because no existing-workflow migration tool exists. Both registrations now use the configured refactor phase sequence; this resolves the operational precondition without reinitialization. There is no further client probe campaign or downstream consumer migration requirement.

## Approved Strategy

| Boundary | Owner-approved direction and breakage strategy |
|---|---|
| Presentation/configuration | Reuse presentation.yaml and the existing defaults/workspace-override loader. Use presentation_channel=text/structured/both, data_channel=text/structured and data_delivery=inline/resource. Preserve all short explanatory text and mandatory instructions in the selected presentation route. Clean break for changed configuration contracts; no old-key aliases or compatibility translation. |
| Shared workspace / instance selection | Support independent harnesses on one workspace. Keep profile definitions shared and active selection local to each server instance; do not persist it into shared workflow state or infer behavior from client names. Use the existing launch/configuration composition boundary. Exact selector schema and diagnostics are Design work. |
| Public response shape | Owner approves the common public envelope for selected presentation, operation data/reference and attachments. Internal operation DTOs remain intact. Clean break with no dual old/new public format or legacy response bridge. #528 must publish the schema appropriate to that shape, actual channel projection and emergency variants. |
| Tool/manager/adapter internals | Keep operation DTOs, operation semantics and domain consumers intact. Route/serialize at the existing presentation and transport boundaries; do not add harness knowledge to tools or adapters. This unchanged surface is not a compatibility layer. |
| Cache / diagnostics / errors | Reuse the raw-operation cache and paging contract. On publication failure, provide emergency text with a configurable bound only on diagnostic details; always preserve the mandatory core, including operation outcome, explanation/instructions and failure/truncation notices, even beyond the presentation budget. Label diagnostic excerpts as potentially incomplete and non-parseable as the original JSON; retain schema-valid structured presentation where selected and disclose incompleteness. No size-induced presentation crash, fictitious cache URI or malformed transport JSON. Normal full-data guarantees have this explicit failure exception. No cache ownership expansion or new generic retrieval tool is selected. |
| Tests | Test profiles and their observable results, including representative valid/invalid routes, preservation, error/attachment behavior and same-workspace instance isolation. Adapt valuable existing tests and remove obsolete assertions as needed. No concrete-harness/version matrix, dependency-version surveillance, legacy-path tests or tests whose only purpose is rejecting the old shape. |
| Client evidence and support claims | Further probing is stopped. Existing observations prove only their exact routes and conditions. Validate pgmcp's own configurable contract and document installation prerequisites; do not claim delivery into every present or future client's model context. |

Research is complete. Independent QA reviewed commit 3d919b27172b016eaceb278f81060a80373d6a9f and gave content GO for Design, with workflow alignment as the sole process blocker. The owner subsequently approved refactor and explicitly permitted the narrow registration repair. Only workflow_name and required_phases were changed in state.json and project 529 in deliverables.json. A before/after field comparison confirmed that identity, parent, creation timestamps, current phase and all history were unchanged. get_project_plan(529) and get_work_context() both reported refactor with Research still active before the normal phase transition. The branch name remains unchanged to preserve its identity. No new production behavior is claimed by this administrative correction.

## Expected Results

- The selected profile's presentation channel(s) contain the complete short explanation and mandatory instructions; an unselected presentation channel does not get a duplicate. Structured presentation can coexist with text data and vice versa.
- Normal inline delivery retains the full authoritative operation data in the selected data channel. Normal resource delivery retains a truthful reference to the complete cached operation and keeps attachments directly accessible. A failed publication instead uses the explicitly bounded, visibly incomplete emergency policy above.
- The existing presentation budget remains measurable for the rendered presentation, with mandatory material protected: optional details fit the available budget; protected material alone may exceed it and is never cut. Complete inline operation data and attachments are separate from the short-presentation budget. Do not claim a universal wire/token/cost ceiling. Existing numeric defaults can be retained; no further owner choice of an arbitrary new global limit is required for Research.
- Two server instances selecting different profiles against the same configuration root produce their respective projections without changing shared configuration or workflow state.
- Available structured output schemas match the selected public shape and applicable outcome variants. #529 defines the policy; #528 retains the normal-registration metadata repair.
- Evidence consists of proportionate behavior-focused tests of the approved contract. Reuse real rendering/assembly boundaries and check dynamic input-derived data and guidance, rather than production wording snapshots or test copies of renderer logic.

## Consumers

### Server response assembly and existing presenters

Publish operation data, rendered text, instructions and attachments through the current output boundary.

**Impact:** The owner-approved strategy is recorded above. Design must specify the bounded presentation/transport change and its affected tests before implementation; no production changes have been made in Research.

### Harness model input and resource/file readers

Deliver the short response and instructions and provide access to complete output.

**Impact:** Tests cover the server's profile contract. Existing integration observations and documented prerequisites remain bounded; server publication is not proof of every client's downstream model context.

### Issue \#528 catalog output schema work

Expose metadata matching the selected output contract.

**Impact:** Must follow the #529 owner decision; must not choose that policy independently.

## Risks

### Documentation and pinned source may describe different builds or integration routes.

Retain both evidence classes and their scope. After the owner stopped probing, do not turn them into universal compatibility claims or add a client matrix as a completion gate.

### A harness may truncate output or hide one response channel.

Validate complete instruction/presentation publication and full-data access under pgmcp's selected profiles. Client-side routing remains an explicit installation prerequisite; it cannot be guaranteed by a server-only test.

### A shared output redesign may exceed the maintenance scope of a chore.

The owner approved refactor and the one-time registration correction before Design. Follow the existing refactor contract for further phases; no general workflow-migration feature is added.

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
| 0.6 | 2026-10-19 | @imp researcher | Resolve isolated VS Code Local-agent startup through normal activation and default approvals; measure actual model input and native large-result files; retain text/instruction loss and 2,000-character read_file line truncation as negative findings. |
| 0.7 | 2026-10-19 | @imp researcher | Prove complete 22,086-character VS Code readback through native scoped search; record the failed external-path control and fresh-profile terminal-consent limit without claiming default recovery or fixing independent instruction loss. |
| 0.8 | 2026-10-19 | @imp researcher | Record owner-approved configurable-profile direction; propose two delivery controls, per-instance selection, protected text/instructions and explicit public-envelope/cache-failure decisions without production changes. |
| 0.9 | 2026-10-19 | @imp researcher | Add approved presentation_channel, replace fixed duplication with selected routing, record clean-break strategy per boundary and profile-focused tests; finish investigation while retaining the two explicit owner policy decisions before Design. |
| 1.0 | 2026-10-19 | @imp researcher | Confirm no production structured-result readers in scope, verify official protocol/schema rules and record owner-directed bounded emergency text delivery; retain public-envelope approval as the sole policy question. |
| 1.1 | 2026-10-19 | @imp researcher | Record explicit owner approval of the public envelope and mandatory-core preservation with only diagnostic details bounded; close Research policy questions and request independent QA for Design, subject to workflow alignment. |
| 1.2 | 2026-10-19 | @imp researcher | Record independent content GO and the owner-authorized chore-to-refactor registration repair; verify preservation of all unrelated state and history before normal Design transition. |
