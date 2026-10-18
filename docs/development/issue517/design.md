<!-- pgmcp:v1 id=design pv=1.0.0 pf=Uk1D2XWpiag1c6nn sf=WI5iXHBKVOU91bYE -->

# Issue 517 — Native SDK 2 Migration Design

**Status:** Design revised for independent QA recheck  
**Version:** 0.3  
**Last Updated:** 2026-10-18

## Purpose

Replace the SDK1 integration at existing owners and align the selected runtime without adding compatibility or version-test architecture.

## Scope In

The three SDK-owning production modules, runtime/development/native prerequisites, direct behavior tests and isolated installed-package acceptance.

## Scope Out

SDK1/Python3.13 production/test bridges, dependency-version assertion suites, initialization-free2026 lifecycle, #518 suppression repairs, release and automatic active host changes.

## Problem Statement

SDK1 decorators, handler shapes and Python aliases must be replaced together. A registry facade or separate tool/domain migration layer would retain coupling. Native tools and installed-package evidence must select the actual target environment without automatically replacing the active host.

## Functional Requirements

- Use the approved Python>=3.15/SDK2.3 coherent snapshot and keep exact native prerequisite checks effective.
- Preserve tool input/output schema, normal pipeline admission/enforcement/presentation/cache/attachments, wire names, error facts and cancellation propagation.
- Serve the initialized2025-11-25 route through SDK2 native handlers/stdio and preserve proxy initialize replay and generation supervision.
- Exercise valuable existing scenarios through SDK2 public client APIs and provide real application/package/proxy acceptance on that target.

## Nonfunctional Requirements

- Keep SDK-specific changes in server.py, utils/mcp_converters.py and core/proxy.py; no managers/tools/presenters framework.
- Preserve explicit covariance and meaningful runtime guards; remove only proven migration-obsolete exceptions.
- No old dependency environments or tests whose only purpose is comparing dependency versions; focused behavior tests only.
- Use the existing builder, MCP check/test tools and native adapters; no release-manifest redesign or new tool runner architecture.

## Options

### 1. Native constructor handlers at the existing server boundary

MCPServer retains its public composition and setup_handlers responsibility. Its existing nested handlers implement SDK2 context/params/result signatures; setup_handlers constructs one native Server with the4 on_* callbacks.

**Pros:**

- Keeps existing ownership and dispatch body.
- No registry emulation or public production handler facade.

**Cons:**

- Direct registry-dependent tests must move to supported client behavior.

### 2. Recreated request\_handlers or dual SDK dispatch

Retain the SDK1-shaped registry or support both SDKs through a facade.

**Pros:**

**Cons:**

- Violates approved clean break.
- Hides incomplete native SDK acceptance and preserves test coupling.

## Decision

Use native SDK2 constructor callbacks and explicit result models. Retain the existing application pipeline and proxy architecture. Use one native SDK2 client lifecycle helper in existing test_support; no request/result translation helper or registry compatibility.

## Rationale

This follows the three source owners and removes the obsolete SDK boundary rather than spreading new knowledge. Tests observe normal list/call/read results, not SDK internals. Isolated RPC acceptance can run the actual installed candidate's run_checks/run_tests while the current host remains operational.

## Production Design

| Owner | Target contract / responsibility |
| --- | --- |
| MCPServer.__init__/setup_handlers | Keep existing settings/tools/resources/presenter/publisher composition. Define callbacks after these fields are available; create exactly one Server[None] with on_list_resources, on_read_resource, on_list_tools and on_call_tool. No post-hoc registry replacement. |
| Resource listing | Return ListResourcesResult(resources=list[Resource]); use string URI and SDK2 mime_type constructor name. |
| Resource read | ReadResourceRequestParams.uri selects the existing resource. Return ReadResourceResult(contents=[TextResourceContents(uri=..., mime_type="text/plain", text=...)]). Preserve existing delivered text/plain and separately advertised resource MIME. No incidental MIME correction. |
| Tool listing | Return ListToolsResult with SDK2 input_schema/output_schema fields. Preserve operation_output_model projection so transport attachments do not pollute operation schema. |
| Tool call | Receive CallToolRequestParams, select params.name/arguments and execute the same normalized pipeline. Return CallToolResult only. Include the actual operation DTO as structured_content, serialized in JSON mode with schema-compatible aliases; retain text, resources, cache publication and operation error facts. Transport attachments/notes/presentation are not the structured operation payload. Do not enable another input validator before the existing prepared tool admission. |
| Converter | Keep application content dictionaries and convert text/JSON/image/embedded resource using native SDK2 Python fields. Preserve nested wire aliases and is_error serialization as isError. No new domain DTO. |
| Stdio run | Use SDK2 stdio_server() ownership and existing Server.run/create_initialization_options. Remove the redundant host TextIOWrapper/anyio.wrap_file output wrapper; native SDK2 owns protected wire/UTF-8 framing. No manual transport framework. |
| Proxy | Change3 InitializeResult.protocolVersion accesses to protocol_version; retain current process_factory, initialized replay, ID/generation/race checks and teardown behavior. |
| AdapterBinding | Remove only its now-unused misc ignore/comment after the target type check; explicit covariant TypeVar/Generic remains. Preserve other variance/Pydantic limitations for #518. |

### Dependency ownership

pyproject.toml remains package metadata authority. Runtime direct dependencies select the tested snapshot: mcp2.3.0, Pydantic2.14.1, pydantic-settings2.16.0, PyYAML6.0.3, jsonschema4.26.0, GitPython3.2.1, PyGithub2.10.0, Jinja2 3.1.6 and AnyIO4.15.1 (already imported directly by production). Use exact direct versions for this controlled cutover, not floating latest or an untested transitive lock framework.

Development/tool provisioning follows the tested pytest9.1.1/pytest-asyncio1.4.0/pytest-cov7.1.0/pytest-xdist3.8.0/coverage7.16.2/Mypy2.4/Ruff0.17.1 and recorded YAML/jsonschema stubs. Native Node Pyright1.1.414 remains owned by its adapter package.json. Eliminate duplicate runtime/dev requirement lists by pointing their existing install routes to project metadata/extras. Remove unbound Black/Python-Pyright-wrapper development provisioning: active bindings use Ruff and native Node Pyright, and source search finds no Black consumer beyond those requirement declarations. Do not upgrade unrelated native tools.

Align the affected adapter requirements/package.json, including check_jsonschema's jsonschema pin, with one satisfiable selected environment; keep existing tool guards. Python syntax prerequisite evidence/comments must reflect the actual target after execution. Set Ruff/Mypy/Pyright language target3.15, retaining existing diagnostic suppressions. Only exact SDK-migration obsolescence and actual target-induced diagnostics are repaired here; no broader #518 policy.

No package version/release change, release_manifest transform, owner config replacement or automatic native installation is introduced.

## Test Design

Adapt the12 registry-dependent files and other direct SDK consumers while preserving their meaningful application assertions. Do not preserve obsolete handler-shape/type-wrapper asserts; remove unused imports. Existing stdio startup/conversion/cache/schema/attachment tests become native SDK2 behavior evidence, without static tests asserting API removal or version strings.

Replace shallow cases in the existing proxy test surface with compact controlled-process behavior tests for restart success, failed replacement, in-flight outcome, cancellation/deadline and cleanup. Inject the existing process_factory and isolate logs/files under tmp_path. Use native SDK2 servers/clients only. Avoid sleep-based correctness: bound waits and use observed responses/process state.

A small shared native client lifecycle helper reduces repeated boilerplate; it is not a new test-only production interface. Deterministic converter tests can remain direct because conversion is their public boundary. Preserve exact error/URI/MIME/content facts and meaningful positive/negative variance/admission checks. Do not add tests that assert dependency metadata equals a particular version.

Temporary orchestration for selected-environment smoke/tool RPC belongs under ignored .pgmcp/temp/issue517, not the permanent suite. It may connect to the real installed candidate and invoke its existing run_checks/run_tests over MCP, preserving scopes/arguments/native outcomes. It must not call raw pytest/lint as a substitute, synthesize a success summary or install old-SDK compatibility environments. This allows authoritative target-stack verification without silently switching the active host.

## Contracts

### Native callback signatures

The callback contracts are async handle_list_resources(_ctx: ServerRequestContext[None], _params: PaginatedRequestParams | None) -> ListResourcesResult; async handle_read_resource(_ctx: ServerRequestContext[None], params: ReadResourceRequestParams) -> ReadResourceResult; async handle_list_tools(_ctx: ServerRequestContext[None], _params: PaginatedRequestParams | None) -> ListToolsResult; async handle_call_tool(_ctx: ServerRequestContext[None], params: CallToolRequestParams) -> CallToolResult. The SDK context is a genuine native context; no cast/None test substitute is required.

### Test lifecycle seam

In existing tests/mcp_server/test_support.py, an async context manager connected_mcp_client(server: MCPServer) -> AsyncGenerator[Client] owns only Client(server.server, mode="legacy", cache=None) enter/exit. It exposes native SDK2 Client/results directly. Tests call list_tools/call_tool/read_resource and inspect snake_case fields, without .root wrappers, request_handlers, rewritten request objects or a pgmcp test dispatcher. Local helpers may retain their application-specific return shapes; they must consume real SDK results.

### Installed acceptance boundary

Build the actual wheel through scripts/build_package.py and install into a clean selected Python3.15 environment with recorded controlled prerequisites and the supported process-local PYYAML_FORCE_LIBYAML=0 route. Launch from neutral CWD with explicit workspace/config/template roots, record sys.executable, module path and package metadata, and verify pip consistency. Use selected-stack native Client with the SDK's initialized-handshake mode for protocol acceptance. SDK2 names that mode legacy; this is the approved2025 protocol operation on SDK2, not an SDK1/dependency compatibility test.

## Flow

Existing tool composition -> native SDK2 callback -> normalized tool pipeline -> cache/presenter -> application ToolResult -> native CallToolResult. Resource read -> existing resource -> explicit SDK2 resource result. Native stdio owns framing. Proxy still captures/replays initialized requests around child generation replacement.

## State and Failures

No state/workflow schema change. SDK2 native initialized stream mode is mandatory in both the shared test helper and installed acceptance; the SDK's mode name legacy does not select an old SDK/dependency environment.

### Explicit error mapping at the server boundary

| Case | Observed prior outcome | SDK2 contract |
| --- | --- | --- |
| Normal operation | Explicit converter result with isError=false, but no structured output despite published schema. | Return is_error=false with the actual operation DTO as structured_content, matching output_schema. Preserve text/resources/cache. |
| Existing operation/input error DTO | Explicit result with isError=true and original presenter/schema facts. | Return is_error=true and the actual operation DTO with the same error facts. Do not validate it as a successful operation or fabricate success. |
| Unknown tool | SDK1 catches application ValueError("Tool not found: ...") into an error tool result. | Return explicit CallToolResult is_error=true, original message as text. No operation DTO exists; no fabricated structured content and no JSON-RPC error substitution. |
| Unknown resource / resource-read exception | SDK1 outer request boundary yields ErrorData(code=0, message=str(error), data=None), without a tool isError field. | Preserve this through SDK2 MCPError/ErrorData at the existing server boundary, retaining the original exception as cause/traceback. No tool DTO or new exception framework. |
| Response-processing exception | The application logs the traceback and returns "Error processing tool response: ...". SDK1 turns a schema-less list into a false-error-flag result; for declared output schemas it instead masks that diagnosis with an output-validation error and isError=true. | Return an explicit failed tool result with is_error=true and the original processing-error text; retain the logged exception/traceback. There is no valid completed response to label successful. Do not reconstruct schema-dependent SDK1 normalization or invent operation data after failure. |
| Cancellation | CancelledError propagates. | Preserve propagation and native cancellation; no fabricated success after timeout or cleanup failure. |

The error mapping belongs to server.py, where the SDK boundary already exists. Domain tools, presenters and converters retain their existing responsibilities. Error responses preserve application diagnosis instead of reproducing the old incidental output-validation masking.

### Owner-approved structured output contract

On2026-10-18 the owner chose the improved route: retain outputSchema and deliver the real operation DTO as structuredContent. This explicitly amends the preservation strategy at the public output boundary; [Research](research.md#approved-strategy) records the decision. SDK1 and SDK2 native clients both reject the prior schema/content inconsistency. The selected-stack initialized2025-11-25 probe independently observed null rejected and matching {"success":true} accepted.

The existing server handler owns this projection because it already has execution.operation and publishes its schema through operation_output_model. Its JSON-mode, alias-aware model serialization supplies the structured object; no parsing of presented text, cache readback or ToolExecution transport wrapper. Optional null fields follow the declared DTO schema rather than the cache's independent omission policy. Existing text, embedded resources, attachment URI/MIME and full cache publication remain available.

The converter continues converting the existing ToolResult content/error flag to SDK models; it does not infer an operation schema or reconstruct a DTO. The server attaches the known operation projection to the completed SDK result. Unknown-tool and response-processing failures carry explicit error text/flag without invented structured data. Native client validation remains enabled.

Adapt existing public schema/cache/attachment scenarios to assert matching structured operation data through Client.call_tool. Cover a meaningful response-processing failure at the existing server-test boundary, including its error flag and original diagnosis; do not add dependency-version tests or SDK1 comparison fixtures. The isolated diagnostic is research evidence only, not permanent coverage.

## Preservation

Preserve current tool names/schema and admission order, operation/cache fidelity, attachments and MIME/URI, configured failure projection, initialized wire protocol, child generations and meaningful covariance/guard behavior. Add matching structured operation output as explicitly approved. The existing resource list/read MIME difference is deliberately retained. No old SDK Python API is preserved as a consumer contract.

## Transition and Cleanup

Perform a single clean cutover of the SDK boundary and its direct consumers. Remove decorators/ReadResourceContents imports, obsolete constructor spellings, registry access/root-wrapper assumptions and migration-obsolete ignores. Do not add a bridge between commits. Source preparation may be verified in the isolated target; final acceptance requires a clean installed package. Native adapter prerequisite consistency must be established before configured gates are claimed. The active host/client remains untouched; any later active-runtime/launcher switch requires explicit owner approval.

## Validation

### SDK/application invariants

**Method:** Focused existing native SDK2 server/converter/schema/cache/admission tests, adding only uncovered public behavior.

**Expected Result:** Valid operations and expected rejection preserve declared schema, URI/MIME/content/error facts; no fake registry or old dependency matrix.

### Proxy lifecycle

**Method:** Existing proxy test surface with controlled real children and bounded waits using process_factory.

**Expected Result:** Restart succeeds only after readiness; failed replacement/in-flight/cancellation/deadline/cleanup have deterministic observable outcomes and no child leak.

### Installed application

**Method:** Existing builder plus clean Python3.15 installation, neutral launch and initialized MCP calls into actual pgmcp/proxy.

**Expected Result:** Package/module/process identity correct; pip consistent; actual tool/resource/error and lifecycle behavior passes.

### Workflow quality

**Method:** Focused checks/tests during implementation. Validation owns full native-configured tests, branch/per-type checks and configured workspace run using actual candidate MCP tool calls.

**Expected Result:** Native results/required coverage reported faithfully. No passing outer driver hides failed/timed-out/incomplete target results; no gate exception or suppression-policy expansion.

## Risks

### Native client behavior can expose real application differences

Preserve the approved application contract; distinguish a direct-consumer migration from a new policy decision. Stop on necessary behavior change.

### Native SDK2 stdio must own Windows wire descriptors

Remove redundant wrapper and prove installed stdio/proxy behavior; retain process isolation and cleanup.

### Installation prerequisite conflict

Align explicit target declarations, preserve guards and verify a clean installed package; report material target drift before changing the approved set.

## Planning Consequences

Plan bounded structural cutover/consumer adaptation and real package/lifecycle acceptance, with cleanup and focused evidence. Do not sequence SDK1 and SDK2 compatibility phases or add a broad suppression cycle. Full-suite/coverage belongs to Validation; active host activation is not a dependency of isolated candidate RPC acceptance and remains separately authorized.

## Sources

- [Approved Research](<research.md>)
- [Inherited snapshot and controls](<../issue513/research.md>)
- [Server](<../../../mcp_server/server.py>)
- [Converter](<../../../mcp_server/utils/mcp_converters.py>)
- [Proxy](<../../../mcp_server/core/proxy.py>)
- [Test support](<../../../tests/mcp_server/test_support.py>)
- [Existing build procedure](<../../reference/release-assets-procedure.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-18 | @imp designer | Specify native typed SDK2 callbacks/results, target-only test access, prerequisite ownership and isolated installed-package acceptance. |
| 0.2 | 2026-10-18 | @imp designer | Make initialized test mode and source-based error mapping explicit; hold Design for reproduced public output-schema/content policy conflict. |
| 0.3 | 2026-10-18 | @imp designer | Apply owner-approved structured operation output, explicit SDK2 error mapping and initialized native client contract for targeted QA recheck. |
