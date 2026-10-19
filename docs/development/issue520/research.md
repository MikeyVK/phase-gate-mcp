<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue \#520 — Concurrent startup and persistent recovery admission

**Status:** REVIEW REQUESTED  
**Version:** 1.0  
**Last Updated:** 2026-10-18

## Purpose

Establish reproduced startup-lock causality, measured three-client feasibility, proportional consumer impact and the owner's approved strategy for Design.

## Scope In

Normal startup against one server root, upgrade-lock ownership, limited admission and health diagnostics, relation to #517, and measured availability through the real proxy and MCP client.

## Scope Out

No production implementation during Research. Shared-server/reader-lock redesign, arbitrary bootstrap retries, background re-admission, unrelated mutation synchronization, release and private-harness deployment are excluded.

## Problem Statement

Concurrent normal starts compete for a nonblocking exclusive upgrade lock. A rejected process becomes a recovery-only server and keeps its original startup diagnosis after the competing process releases the lock.

## Goals

- Evidence the trigger and distinguish source defects from migration timing hypotheses.
- Measure full catalog plus healthy admission rather than treating transport readiness or uptime as startup duration.
- Present bounded strategy alternatives before Design.

## Background

The owner requested an interactive initial inventory on 2026-10-18. Branch bug/520-startup-lock-failure is initialized from main. Source baseline ed4fc25f6d342d2e355a3b43241d4fe8df692407 includes merged #517. All timestamps below use UTC.

## Findings

### Causal path

1. ServerBootstrapper.bootstrap_target acquires UpgradeLock before configuration loading and releases it in finally after constructing the complete MCPServer. Normal starts therefore serialize against both other starts and template activation, even when no upgrade occurs.
2. UpgradeLock uses Windows LK_NBLCK (POSIX LOCK_EX | LOCK_NB) without waiting or retry. Its OSError handler classifies failures inside the protected acquisition block as template_upgrade_locked / ERR_CONFIG.
3. cli.main catches that configuration error and constructs DegradedMCPServer with only health_check and restart_server. HealthCheckTool stores the immutable startup diagnosis; subsequent calls do not re-run admission.
4. Proxy server_ready establishes transport initialization, not healthy admission. The losing process can therefore be ready sooner while permanently lacking ordinary tools.

The existing lock file is not itself a stale-lock indicator. Ownership is an OS lock; release closes the stream without deleting the file.

### Diagnostic mismatch

The measured cause is PermissionError: [Errno 13] Permission denied despite a successful later lock acquisition, without any permission repair. The public diagnosis has params={} and file_path=null, and does not distinguish transient contention from other OSError causes classified by this handler. StartupRecoveryPresenter then directs the caller to correct the source externally. That advice is unsuitable for the evidenced temporary contention. This does not establish that every PermissionError is contention.

### Real startup observations

| Probe | Initialize complete | Catalog received | Health received | Catalog / health |
| --- | ---: | ---: | ---: | --- |
| One standalone start | 9.697 s | 9.734 s | 9.740 s | 49 tools / healthy |
| Concurrent A | 9.234 s | 9.275 s | 9.281 s | 49 tools / healthy |
| Concurrent B | 4.432 s | 4.435 s | 4.440 s | 2 tools / unhealthy |

Timing starts immediately before entering Client's process/session context: it includes launching the proxy, child startup and handshake, and excludes the diagnostic driver's own SDK imports. This is one single-start observation and one pair, not a latency distribution or guarantee. Proxy-native child startup_time_ms was 7945.470, 7598.843 and 2757.927 respectively.

Concurrent B reported MCPError(template_upgrade_locked, ERR_CONFIG), caused by PermissionError(Errno 13). After a barrier confirmed both clients had obtained their first health response, each client-side probe successfully acquired and released the same workspace UpgradeLock. B then still returned unhealthy with the same diagnosis and only two tools from an explicitly refreshed tools/list; A remained healthy with 49. Client caching was disabled. No ACL changes, lock deletion, template change or restart occurred between these observations.

The healthy standalone child's lifecycle messages span approximately 4.849 seconds from 'MCP server starting' (just after lock acquisition) to 'MCP server running' (after bootstrap returns). Concurrent A spans approximately 4.827 seconds. These log intervals approximate the lock-protected composition span; they are not instrumented exact acquisition/release measurements or a breakdown by config/template/adapter validation.

Health uptime_seconds starts at health_tools module import, so its approximately 5.016 seconds at the standalone health response is not the measured 9.740-second total startup duration. The proxy's existing 30-second initialization deadline is a ceiling, not a planned startup delay.

### Three-client follow-up: retry and deadline interaction

The owner rejected15seconds as an insufficiently justified default for the existing three-agent operating model and requested three-start measurements before Design. The following follow-up uses the same Python3.15/MCP2.3 source baseline and launches three real proxy/server/client chains concurrently per cohort.

| Cohort | Lock wait / retry interval | Proxy initialization deadline | Time to catalog and health, ascending | Result |
| --- | --- | --- | --- | --- |
| Current behavior, three starts |0seconds / no retry |30seconds |4.843s,4.843s,9.932s |Two unhealthy servers with2tools; one healthy with49 |
| Retry prototype, normal composition |30seconds /0.25seconds |60seconds |9.155s,13.950s,19.168s |All three healthy with49tools |
| Retry prototype, controlled extra6seconds holding each lock |30seconds /0.25seconds |30seconds |15.653s,26.490s; third rejected at31.941s |Third received ERR_SERVER_UNAVAILABLE / initialize_timeout after obtaining the lock |
| Same controlled slowdown with larger proxy budget |30seconds /0.25seconds |60seconds |15.277s,26.123s,37.058s |All three healthy with49tools |

Normal retry-cohort lock waits were0.0005s,4.7798s and9.5544s (1,20 and39acquisition attempts); hold durations were4.6692s,4.6217s and5.0721s. With the controlled slowdown and60second proxy budget, waits were0.0006s,10.8167s and21.8941s (1,44 and88attempts); hold durations were10.8363s,10.7584s and10.7229s. The6second slowdown is deliberately injected experimental delay, not measured production overhead. It establishes deadline sensitivity without claiming a statistical worst case or hardware-load equivalence.

The source is unchanged. A temporary inline Python driver launches each real MCPProxy through its existing injected process_factory and sets initialization_timeout_seconds explicitly. Only those diagnostic child processes wrap UpgradeLock.acquire/release: the wrapper measures original calls, retries MCPError(template_upgrade_locked) with an OSError cause errno13/11 until a monotonic30second budget is exhausted, sleeps at most0.25seconds between attempts, and optionally holds the acquired lock for6additional seconds before calling the original release. It then invokes the unchanged cli.main. Instrumentation goes to stderr; the protocol and actual49-tool/healthy observations come from the real server. This temporary cause predicate is sufficient for the controlled known-contention experiment; it is not a production-ready classification of all native IO/access failures. The client uses cache=None, mode='legacy' and a90second read window. Cohorts execute sequentially, clients within each cohort via asyncio.gather; each performs tools/list and health_check. All12probe outcomes, including both baseline rejections and the proxy-timeout rejection, are retained above. The driver exited0 because it records expected negative outcomes rather than asserting universal success. No suite run or permanent test was added.

Total start time and lock hold time are distinct: imports/proxy setup can overlap across the three processes, while exclusive composition cannot. The approximately9–10second individual total therefore does not imply that three starts need exactly27–30seconds, and the approximately5second lock hold does not justify ignoring the rest of startup. The30second proxy counter starts on forwarding initialize, after proxy startup, and must allow both lock waiting and remaining child admission/handshake.

### Configuration placement and budget ownership

Final owner decision: put startup policy in required config_root/defaults/server.yaml with an optional config_root/server.yaml workspace override, using the existing ConfigLoader and ordinary defaults/root composition. No independent YAML loader or second startup-policy configuration path is allowed. The earlier proposal to load these new values through Settings.from_env / PGMCP_CONFIG_PATH is superseded.

Existing launcher settings still determine the workspace/configuration roots before this read. Once the root is known, the composition entrypoint can use ConfigLoader to load only server policy before lock acquisition, then load remaining declarations under the existing admission lock. New startup-policy fields must not also be accepted from the old launcher YAML route or independently copied into that route. This decision does not silently authorize rewriting unrelated existing launcher/logging settings. Concrete pure models, a public server-config load method and injection ownership belong in Design.

A bounded read-only feasibility probe on the selected Python3.15 environment instantiated the actual source ConfigLoader with a context_schema_reader that raises if invoked. Construction read no configuration files. Its existing public load_github_config() then succeeded and an audit hook observed exactly defaults/github.yaml and github.yaml, with no template-reader call or unrelated config reads. The returned type was GitHubSettings; no credential values were printed. This demonstrates existing per-file composition independence, not an implemented server.yaml loader or admission of the future server schema.

The standalone proxy currently calls MCPProxy().run() and uses a constructor default of30seconds; it does not load workspace server policy. Configurability therefore requires a bounded change at its composition entrypoint to resolve the root, use the same ConfigLoader server-policy contract and inject the resulting deadline. The server entrypoint receives its retry policy through the same reader/model boundary. Retain constructor injection for direct tests/callers; do not make the lock service or domain models discover config files.

The now-approved defaults are30seconds maximum lock wait,0.25seconds retry interval and60seconds proxy initialization timeout, with validation rejecting nonfinite/invalid intervals and a proxy deadline that cannot accommodate its configured lock wait. Merely requiring proxy_timeout > lock_wait is necessary but does not guarantee startup success under arbitrary load; the measured normal and controlled-slowdown cohorts provide the bounded feasibility evidence.

A third budget belongs to the harness. Official Codex documentation lists startup_timeout_sec (default10seconds) and an optional-server startup grace setting. A pgmcp-only timeout increase cannot override an earlier client deadline or initial-catalog grace policy. The corresponding current pgmcp entry was not present in the inspected ~/.codex/config.toml, so no actual active-client startup budget was established. Do not claim the active deployment uses10seconds or has been adjusted. Document an outer client window larger than the proxy budget (for example75seconds for a60second proxy), verify the actual harness configuration during deployment, and preserve harness ownership. No private launcher configuration was changed.

Source: [current runtime configuration contract](../../reference/server-configuration.md), [Settings](../../../mcp_server/config/settings.py), [proxy entrypoint and deadline](../../../mcp_server/core/proxy.py), and [official Codex MCP timeout settings](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

### Concrete change surface and preservation boundaries

| Surface | Existing consumers and impact |
| --- | --- |
| ConfigLoader / pure policy schema | Add one public server-policy read through the existing generic _load_workspace composition. The constructor is independent of other file reads. Preserve the current dependency direction: loader imports GitHubSettings from settings; do not create a module-level Settings-to-loader import cycle. |
| CLI / bootstrap | cli.main invokes ServerBootstrapper.bootstrap_target; direct bootstrap consumers include test_support.make_test_server, unit/server/test_bootstrap.py, unit/test_server.py, integration/test_target_startup.py, integration/test_project_plan_readback.py and integration/mcp_server/conftest.py. Keep first-time --init and repair/--upgrade possible before the new basis is installed; the ordinary start must require it. |
| Proxy | Standalone main currently supplies no policy. Constructor injection and direct test/installed-probe callers must remain explicit; real startup entrypoints must not retain an independent implicit30second timing policy. No forwarding, session, generation or cancellation redesign. |
| Shared lock | UpgradeLock is used by bootstrap and cli_renewal.build_default_operation. TemplateRenewalService._fail maps template_upgrade_locked to upgrade_busy. Narrowing classification must not relabel all OS failures as busy or change renewal admission policy by accident. |
| Existing tests / fixtures | Adapt the current startup-lock exclusion case to bounded behavior; retain actual activation exclusion and unresolved-recovery protection. Use existing config loader tests, core/test_proxy.py, integration/test_target_startup.py and integration/test_template_activation.py, plus current recovery/health cases as needed. copy_server_startup_inputs and isolated_target_env already copy the config tree; missing-basis fixtures may need a deliberate new basis. Direct registration/helpers unrelated to startup are outside the blast radius. |
| Assets / documentation / agents | release_manifest.yaml already registers the entire .pgmcp/config tree; add the new basis there without a builder/manifest redesign. Current docs/reference/server-configuration.md, config-loading-architecture.md, proxy_restart.md and the applicable setup instructions own the changed contract. No new agent role, workflow phase, enforcement or template behavior is required. |

### Native contention classification feasibility

Microsoft's _locking contract assigns EACCES to a locking violation at that operation, while EBADF/EINVAL describe descriptor/argument errors. Python msvcrt.LK_NBLCK raises immediately rather than applying LK_LOCK's internal fixed retry schedule. This supports a narrow decision at the native acquisition call; the current wrapper's broader try block also includes file write/flush/seek and must not treat their PermissionError as contention. POSIX remains its existing nonblocking flock path; classification and platform-specific verification must reflect that implementation. Research's timing prototype used a broader known-contention predicate and is not evidence that a production predicate already exists.

Sources: [Microsoft _locking error contract](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/locking?view=msvc-170), [Python msvcrt](https://docs.python.org/3.15/library/msvcrt.html), [Python fcntl](https://docs.python.org/3.15/library/fcntl.html).

### Relation to migration #517

The pre-#517 snapshot 4a302d773a9bad2760a53429b12b678b89049c94 already contains the identical acquisition/error classification, the same bootstrap lock ownership and the same CLI recovery composition. PR #519's complete 87-file inventory contains no bootstrap.py, cli.py, health_tools.py or startup_recovery_presenter.py change. template_activation.py changes concern typing and Python exception syntax, not lock semantics. server.py migrates SDK handlers but does not change DegradedMCPServer composition.

The architecture comes from #460 DI-06: startup protects recovery-state inspection and immutable catalog construction with the activation lock. #481 supplies the recovery-only server. The defect mechanism therefore predates #517; changes in runtime/import or startup scheduling may affect encounter frequency, but no comparative old/new timing experiment has established that effect. No claim is made that the same natural overlap was reproduced on the old runtime.

### Alternatives for owner discussion

| Route | Benefit | Cost / unresolved boundary |
| --- | --- | --- |
| Bounded startup waiting/retry for demonstrated contention | Keeps existing lock and admission structure; avoids immediately making a temporary collision permanent | Distinguish busy from real IO/access failure; define total waiting versus proxy deadline and multi-chat queueing |
| Re-attempt admission from a recovery server | Can recover after the initial wait budget, including a longer-lived temporary condition | Dynamic catalog, client refresh, retry ownership and lifecycle become additional responsibilities |
| Shared startup readers with exclusive activation | Parallelizes read-only admission | A different cross-process locking contract across startup, activation and recovery; materially larger change |
| Improve diagnosis alone | Makes manual restart advice accurate | Leaves permanent recovery admission after a transient collision, so does not satisfy #520 expected behavior |

The owner subsequently selected preserving separate servers and exploring bounded startup waiting/retry for lock contention, potentially configurable. Shared-server and shared-reader redesigns are not the chosen direction. The final Approved Strategy below settles the policy and budgets; exact operation/diagnostic contracts remain Design work. Removing the lock or treating a recovery child as healthy would lose the existing admission/integrity boundary.

## Questions

No blocking owner-strategy choice remains. Design must specify the pure policy schema and public load seam, early CLI/proxy/bootstrap injection and initialization ordering (including --init/--upgrade), native busy-versus-IO classification, deadline combination validation and the precise bounded-exhaustion diagnostic/presentation contract. It must identify proportional fixture/test changes and existing-workspace setup steps without adding a second configuration path.

## Approved Strategy

The owner's final "Akkoord, ga verder" confirms the preceding configuration decision and the tested budget proposal. The following boundary decisions govern Design; earlier unselected proposals in this document are superseded.

| Boundary | Approved strategy |
| --- | --- |
| Server topology and transport | Preserve an independent stdio proxy/server per client connection. No shared service, HTTP migration, general tool queue or background re-admission loop. |
| Startup lock and integrity | Preserve the existing OS lock, stable file and complete admitted snapshot. Change ordinary startup from immediate busy rejection to bounded lock acquisition: maximum wait **30 seconds**, interval **0.25 seconds**, immediate first attempt and immediate continuation on success. Retry actual contention only; preserve genuine filesystem/access failures and unresolved-recovery rejection. |
| Configuration source | Clean addition of required config_root/defaults/server.yaml plus optional config_root/server.yaml, using the existing ConfigLoader, generic composition and typed admission. Resolve roots first, load only this policy before the lock, inject into startup consumers. No separate YAML parser, alternative policy source through PGMCP_CONFIG_PATH, duplicate timing policy in Python, or compatibility bridge for workspaces missing the new required basis. Existing unrelated launcher/root/logging behavior is not silently refactored. |
| Proxy and harness deadlines | Inject **60 seconds** as configured proxy initialization policy. Keep transport initialization distinct from healthy admission and retain existing restart/request ownership. Document an outer harness window greater than the proxy budget, initially **75 seconds** recommended. Do not change private harness settings or claim the inspected active deployment has this window. |
| Failure and presentation | After the bounded lock budget, fail closed through the existing recovery/error boundaries with actionable diagnostic facts and original cause. A budget-exhausted recovery server requires an explicit later restart; bounded waiting does not promise recovery after arbitrarily long contention. Use existing diagnostic models/presenters; no domain-authored recovery prose or new error framework. Invalid required early policy can fail before an endpoint exists; expose the configuration diagnosis instead of choosing an undeclared fallback timeout. |
| Template activation/renewal | Preserve command-owned locking and recovery integrity. Startup waiting must not silently introduce waiting/retries into activation or renewal. Narrowing shared native error classification must keep these consumers truthful and preserve genuine error causes. |
| Consumers, migration and verification | Clean break for the new required configuration and changed startup behavior. Fresh installations receive the basis through the existing registered config asset tree; existing workspaces require an explicit config update. Reuse/adapt focused behavior tests and shared startup fixtures; no legacy-behavior preservation tests, compatibility/version matrix or new permanent diagnostic suite. Broad gates belong to Validation. No release, active-host switch or unrelated concurrency audit. |

The native error predicate, exact schemas/signatures, exhausted-budget code/params, early-load composition and presentation arrangements are Design work within these decisions, not unresolved owner policy. No implementation has been made during Research. Current source and the active server retain the old startup behavior until implementation/activation.

## Expected Results

Several supported chats against one server root must not remain unusable solely due to a completed temporary startup collision. Invalid configuration, genuine access failure and unresolved activation recovery must remain accurately diagnosed with ordinary tools unadmitted.

## Evidence

### A temporary concurrent-start lock collision leaves one server persistently in recovery-only admission.

Python 3.15.0, MCP 2.3.0, current repository source. Standalone actual health PID56468; concurrent healthy PID27548 and unhealthy PID55280. Reproduce by launching the two clients concurrently and retaining both sessions until the post-barrier checks. Normal timing is scheduler-dependent; the first observed pair reproduced the failure.

- [Bootstrap lock and release](<../../../mcp_server/bootstrap.py>)
- [Lock implementation](<../../../mcp_server/services/template_activation.py>)
- [Recovery composition](<../../../mcp_server/server.py>)
- [Health implementation](<../../../mcp_server/tools/health_tools.py>)

**Invocation:** C:/temp/pgmcp/.pgmcp/temp/issue517/installed-py315/Scripts/python.exe executed a temporary inline asyncio driver from C:/temp/pgmcp. MCP Client(cache=None, mode='legacy', read_timeout_seconds=60) launched each real -m mcp_server.core.proxy using that same interpreter, explicit workspace/config/template environment roots and no PYTHONPATH/NODE_PATH. One client was run alone, followed by asyncio.gather of two clients. Each listed tools and called health_check. Both waited at an asyncio.Barrier before a real UpgradeLock acquire/release and fresh health_check/tools/list(cache_mode='refresh'). 'legacy' is the SDK 2 initialized protocol mode, not an SDK 1 compatibility path.

**Observed Result:** Single 49/healthy at9.740s; pair49/healthy at9.281s versus2/unhealthy at4.440s. Both lock probes later succeeded. Unhealthy diagnosis and two-tool catalog persisted. The inline driver exited0. On client shutdown the proxy also logged child_exited(exit_code=1) for both concurrent children; shutdown behavior was not investigated or claimed clean by this startup probe.

**Observed At:** 2026-10-18T16:54:48Z

## Consumers

### Bootstrap and template activation

Own one coherent admitted snapshot and mutation/recovery exclusion.

**Impact:** Any wait or locking strategy must preserve the existing integrity boundary.

### CLI, recovery presenter and health

Classify startup outcomes and expose actionable original diagnoses.

**Impact:** Temporary contention needs distinct truthful handling; invalid config and real access failures remain rejected.

### Proxy and harness

Negotiate transport and refresh the exposed catalog.

**Impact:** Existing30-second initialization budget and transport/domain distinction constrain a proposed wait.

### Existing startup/activation/proxy tests and reference docs

Prove process, admission and lock behavior.

**Impact:** Existing cross-process activation test proves exclusion, not competing normal-start recovery. Adapt only the behavior coverage required by an approved strategy.

## Related Documents

- [Issue #520](<https://github.com/MikeyVK/phase-gate-mcp/issues/520>)
- [Proxy admission contract](<../../reference/proxy_restart.md>)
- [#460 original activation-lock rationale](<../archive/issue460/design-distribution.md>)
- [#481 recovery research](<../archive/issue481/research.md>)
- [Pre-migration lock implementation](<https://github.com/MikeyVK/phase-gate-mcp/blob/4a302d773a9bad2760a53429b12b678b89049c94/mcp_server/services/template_activation.py>)
- [#517 migration diff](<https://github.com/MikeyVK/phase-gate-mcp/pull/519/files>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-18 | @imp researcher | Record reproduced concurrent-start failure, real availability timings, pre-migration evidence and bounded strategy alternatives. |
| 0.2 | 2026-10-18 | @imp researcher | Record owner-selected parallel-server direction, twelve three-client probe outcomes, runtime configuration seam and proxy/harness deadline boundaries; retain negative controls and pending decisions. |
| 0.3 | 2026-10-18 | @imp researcher | Adopt owner-selected ConfigLoader defaults/override route, supersede the separate launcher-policy proposal and record read-only evidence of per-file loading without template/server activation. |
| 1.0 | 2026-10-18 | @imp researcher | Close Research with the approved strategy per boundary, concrete consumer/migration impact and native-classification feasibility; request independent transition review. |
