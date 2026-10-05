<!-- pgmcp:v1 id=design pv=1.0.0 pf=YApsrGTQgBUKFez2 sf=5--KpGf2wHUv2qAj -->

# Startup admission diagnostics and recovery — Design (#481)

**Status:** DESIGN DRAFT — review requested  
**Version:** 0.1  
**Last Updated:** 2026-10-05

## Scope In

Recognized CLI bootstrap failures, complete startup diagnostic transport, the existing degraded server and restart tool, and necessary proxy stream/initialize/request-failure handling.

## Scope Out

Proxy-owned recovery tools, in-session file repair, relaxed admission, cached invalid/last-known-good activation, compatibility bridges, unrelated exception/transport redesign, regression-test additions or runs, and implementation sequencing.

## Problem Statement

Admission raises MCPError(code=ERR_CONFIG), but the CLI catches ConfigError/FileNotFoundError only. Converting an exception to str also loses params. The current degraded server offers health only; the proxy can lose early stderr, accept an invalid initialize response as readiness and silently discard requests. Changing the error-code spelling alone corrects none of these boundaries.

## Functional Requirements

- Recognized configuration/admission rejection initializes a recovery server exposing exactly health_check and restart_server, with no ordinary tools or resources.
- Health preserves the original message, code, available package/template/field/line/path parameters and exception cause; rejected admission is reported as unhealthy.
- External source correction followed by the existing restart operation runs fresh bootstrap/admission. Repeated rejection remains diagnosable.
- Initial startup and restart become transport-ready only after a valid MCP initialize exchange and a live child. Exit, invalid/error response and initialization timeout remain failures.
- Requests blocked or interrupted by startup failure/restart receive a correlated unavailable response; notifications never receive a response.

## Nonfunctional Requirements

- Keep strict atomic admission and existing upgrade-lock/renewal ownership; recovery composition does not load the rejected suite, presentation configuration or workflow configuration.
- Inject dependencies at composition roots, use immutable diagnostic data and keep presentation outside admission/core exception logic.
- Keep the correction local; reuse existing server, tools, SDK contracts and JSON immutability types. No legacy result/constructor route.
- Use one bounded practical process demonstration after implementation; do not introduce or execute regression tests.

## Decision

Choose the lightest variant of A already approved in Research: extend existing degraded composition with complete diagnostics, restart_server and a small configuration-independent presenter. Keep the proxy a process/stdio forwarder.

## Rationale

Reusing the existing MCP transport and restart operation avoids a second recovery endpoint or editor. A localized CLI classifier preserves the current admission errors. The proxy corrections are necessary to make that recovery surface reachable and lifecycle reports truthful.

## Production Design

| Owner | Contract and dependency boundary |
| --- | --- |
| CLI composition root | Recognize ConfigError, bootstrap FileNotFoundError and MCPError with code ERR_CONFIG inside bootstrap_target only. Other MCPError codes and unexpected exceptions remain fatal. Snapshot the original diagnostic, then compose recovery dependencies. Settings/root/launch failures before this boundary remain explicit fatal outcomes. |
| Admission/bootstrap | Continue rejecting the suite atomically. No exception-code renaming or repository-wide exception-class conversion. Existing finally releases the upgrade lock before recovery. |
| DegradedMCPServer | Register the existing typed validation/error decorators around HealthCheckTool and RestartServerTool. No normal tool factory, response publisher, resources or rejected configuration loaders. |
| HealthCheckTool | Receive Settings and an optional immutable startup diagnostic at construction. Derive unhealthy from diagnostic presence; normal composition supplies Settings with no diagnostic. Query performs no repair/retry. |
| StartupRecoveryPresenter | Implement existing IPresenter for the two recovery DTOs. Render complete diagnostic JSON plus concise repair/restart guidance and an accurate restart-request receipt. No Jinja/catalog/presentation.yaml/cache dependency; wording belongs to this presentation leaf. |
| MCPProxy | Own child generations, stdio readers, initialize correlation/deadline and interrupted-request completion. Interpret transport lifecycle only; do not interpret suite diagnostics or answer MCP tool discovery itself. |

## Test Design

No regression tests are designed, added or executed. After implementation, record one temporary isolated CLI/proxy demonstration of the F6 rejection, available diagnostics, external correction and explicit restart. Include bounded early-exit/invalid-initialize/timeout probes in that same disposable demonstration where needed to establish proxy failure behavior; do not check in a harness or create artificial RED/GREEN cycles. Required static checks remain scoped to changed production files at the phase that owns them.

## Contracts

### Diagnostic and tool contracts

Signatures and data shapes only; method bodies belong to implementation.

```python
class StartupDiagnostic(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    exception_type: str
    message: str
    code: str | None
    params: FrozenJsonObject
    file_path: str | None = None
    cause: StartupDiagnostic | None = None

class HealthCheckOutput(BaseToolOutput):
    status: HealthStatus
    startup_diagnostic: StartupDiagnostic | None = None
    version: str
    pid: int
    platform: str
    uptime_seconds: float

class HealthCheckTool:
    def __init__(
        self, settings: Settings,
        startup_diagnostic: StartupDiagnostic | None = None,
    ) -> None: ...

class DegradedMCPServer:
    def __init__(
        self, settings: Settings, diagnostic: StartupDiagnostic,
        presenter: IPresenter,
    ) -> None: ...
```

Reuse FrozenJsonObject/freeze_json/thaw_json from the existing core contract; params is deeply immutable internally and an ordinary JSON object in serialized output and outputSchema. Preserve original keys and nested values, without field allowlists or invented package/line values. Preserve explicit cause, or unsuppressed exception context, including its diagnostic payload. ConfigError.file_path/FileNotFoundError.filename are retained when present. The classifier does not stringify the exception before capture.

Health is a successful query even when status is unhealthy; startup_diagnostic is populated only for recovery. Remove the old health reason field and override_status/override_reason constructor contract directly. Retain existing version/PID/platform/uptime fields. RestartServerInput and RestartServerOutput retain their current names and data shapes; their success acknowledges the request, not successful admission.

The recovery presenter renders the serialized DTO, including the complete diagnostic, directly in the MCP text result. No cache lookup or additional resource endpoint is needed.

### Proxy contracts

| Concern | Concrete rule |
| --- | --- |
| Stream ownership | Start one stdout reader and one stderr reader immediately after spawn. Each owns its captured Popen[str] and generation ID through EOF; an old reader never switches to the replacement child. Only the active generation may change current lifecycle state. |
| Diagnostic delivery | Forward all stderr, including early-exit/partial final output, and record it with its original generation/PID in existing audit logging. Do not filter diagnostics by Pydantic keywords. On exit, drain buffered streams before closing handles; raw stderr never enters protocol stdout. |
| Stdout ownership | The single reader correlates initialize responses and ordinary responses. No second blocking readline during replay. Serialize writes to client stdout so reader and unavailable responses cannot interleave JSON lines. |
| Initialization | Validate a JSON-RPC 2.0 response with matching ID, no error, and SDK InitializeResult shape. Forward the first successful response to the client and forward its notifications/initialized. On restart, consume the replay response internally and send notifications/initialized to the replacement child; require the previously negotiated protocol version. |
| Deadline | Initialization has a 30-second monotonic deadline starting when initialize is sent, including completion of the initialized notification. Before the client sends its first initialize, the proxy stays starting rather than claiming ready. No fixed sleep substitutes for handshake completion. |
| Readiness | A completed initialize exchange plus poll() is None permits ready. Check active generation/liveness atomically before readiness logging or restart completion. A ready recovery child can still report unhealthy; transport readiness never asserts admission success. |
| Request ownership | Track client requests by generation and ID from accepted forwarding until response. Complete each at most once: forward its response, or emit unavailable on failed write, exit, failed initialization or restart interruption. Ignore late replies from retired generations. Do not replay ordinary requests. |
| Unavailable result | JSON-RPC error code -32000, original request ID, and data containing code ERR_SERVER_UNAVAILABLE plus lifecycle state and generation/PID when known. Presentation owns actionable text; audit/stderr retain process details. Requests received while restarting/unavailable fail immediately. Notifications are logged/dropped when undeliverable and never answered. |
| Restart ownership | Existing restart marker initiates one serialized restart of the active generation, even if that child has just exited. Concurrent duplicate markers do not spawn multiple replacements. No automatic restart loop or new client recovery method. |
| Retry boundary | A live degraded child offers restart_server. A fatal launch/transport failure leaves no tool endpoint: correct the launch cause and reconnect/relaunch the proxy externally. Direct CLI use likewise requires the external launcher to start the next process. |

The deadline bounds initialization failures and the resulting unavailable responses; it is not a new execution timeout for healthy long-running tools. Existing subprocess termination limits remain separate. Logs emit restart_completed only for an initialized live replacement, otherwise restart_failed with the actual cause and PID/exit status.

## State and Failures

| State/event | Observable result |
| --- | --- |
| Starting | Child spawned and readers active; initialize can proceed; ordinary calls are unavailable until initialization completes. |
| Ready, admitted suite | Normal tools are available; health is healthy. |
| Ready, rejected suite | Exactly two recovery tools; health is unhealthy with the original diagnostic. |
| Restarting | Pending ordinary requests are completed as unavailable; new ordinary calls fail promptly. The already-completed restart receipt is not rewritten. |
| Exit / initialize error, invalid response or timeout | Unavailable, retained stderr/audit evidence, no ready/restart_completed event. An invalid response is never treated as an empty successful result. |
| Repeated rejection after restart | Replacement initializes in recovery mode; fresh diagnostic replaces the old one; health stays unhealthy. |
| Corrected source after restart | Fresh admission succeeds; health becomes healthy. Refresh tools/list to discover the normal surface. |
| Shutdown | Stop the active child and readers; no new restart or readiness publication. |

Clients must refresh tool discovery after replacement; a stale ordinary tool name on a recovery child is rejected by the existing server handler. No tool-list compatibility view or proxy-owned discovery is introduced. Hosts that do not refresh discovery need an external reconnect.

## Preservation

Preserve suite admission, atomic snapshot activation, upgrade locks and renewal records. Recovery cannot invoke ordinary scaffold/file/project/workflow operations against rejected content. This issue does not make fatal launch failures recoverable or make restart_server edit files.

## Transition and Cleanup

Apply a clean break to the changed health/constructor contracts: update current composition roots, documentation and existing contract callers together; add no old-field alias, dual output, wrapper or fallback path. Existing tests affected by removed contracts may receive mechanical caller/expectation adjustments only; no new regression scenarios or test runs. Reconcile current health/restart reference and proxy guidance, including false zero-downtime/fixed-duration claims. Historical F6 evidence remains historical.

## Validation

### Design matches the approved minimal strategy and existing seams.

**Method:** Read the source contracts and compare this document against approved Research and architecture/documentation standards.

**Expected Result:** Two recovery tools, one localized diagnostic capture and necessary proxy lifecycle corrections; no added repair platform or compatibility route.

### Complete diagnostics and repeated recovery.

**Method:** After implementation: one isolated process demonstration, direct CLI and proxy, using the recorded F6 failure and external source correction.

**Expected Result:** Original template/field/line/cause accessible; ordinary tools unavailable during rejection; repeated rejection remains diagnosable; corrected content admits on explicit restart.

### Truthful, bounded transport failures.

**Method:** After implementation: inspect the captured initialize/results/stderr/events and disposable process failure probes.

**Expected Result:** No false-ready/restart completion, no swallowed requests, correlated unavailable responses and drained early stderr.

## Risks

### Transparent replacement changes the available tool list.

Require fresh tools/list discovery; document reconnect for hosts with a persistent discovery cache.

### A fixed initialization deadline can reject exceptionally slow bootstrap.

Use an explicit 30-second technical budget and verify actual timings in the isolated demonstration; reopen this bounded choice if measured startup exceeds it.

## Sources

- [CLI classification boundary](<../../../mcp_server/cli.py>)
- [Exception code and payload](<../../../mcp_server/core/exceptions.py>)
- [Existing server composition](<../../../mcp_server/server.py>)
- [Health tool](<../../../mcp_server/tools/health_tools.py>)
- [Existing restart operation](<../../../mcp_server/tools/admin_tools.py>)
- [Tool output contracts](<../../../mcp_server/schemas/tool_outputs.py>)
- [Immutable JSON contract](<../../../mcp_server/core/interfaces/template_catalog.py>)
- [Presenter interface](<../../../mcp_server/core/interfaces/ipresenter.py>)
- [Proxy lifecycle](<../../../mcp_server/core/proxy.py>)
- [Recorded F6 evidence](<../issue473/tool-practice-findings.md#f6--template-admission-failure-terminates-bootstrap-and-leaves-a-falsely-ready-proxy>)

## Related Documents

- [Approved Research strategy](<research.md>)
- [Architecture contract](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-05 | @imp designer | Define the owner-approved minimal recovery contracts and truthful proxy lifecycle. |
