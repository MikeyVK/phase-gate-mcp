<!-- pgmcp:v1 id=research pv=1.0.0 pf=lgBwxWMfTAmNNg_O sf=5--KpGf2wHUv2qAj -->

# Startup admission diagnostics and recovery — Research (#481)

**Status:** DRAFT — recovery strategy awaiting owner discussion  
**Version:** 0.1  
**Last Updated:** 2026-10-05

## Scope In

CLI bootstrap error boundary, admission diagnostic transport, existing degraded server, proxy subprocess/stdio/initialize/restart ownership and current recovery guidance.

## Scope Out

Admission relaxation, invalid or last-known-good snapshot activation, compatibility/legacy bridges, package deployment/sandbox, generic consumption (#476), dependency-health notices (#478), unrelated tool/error-framework redesign and regression-test additions or runs.

## Problem Statement

A rejected configured suite can terminate bootstrap before MCP initialization. The proxy can lose the diagnostic, report ready without a live initialized child and leave requests unanswered. Catching an admission exception alone does not restore a usable recovery path.

## Goals

- Preserve strict suite rejection and actionable package/template/field/line/cause evidence.
- Compare bounded recovery paths and lifecycle ownership before selecting a design.
- Keep the process proportional: one concise Research artifact, no regression-test work, no implementation before the owner chooses.

## Background

The original F6 runtime reproduction is recorded in issue473/tool-practice-findings.md: exit 1 with ERR_CONFIG, architecture, shared/templates/bases/tier2_markdown_document.jinja2, field content.document_metadata.revisions.-1, line 8; proxy subsequently reported ready/restart_completed with a null child PID. Correcting the template restored admission. This Research inspects current source and the recorded reproduction; it does not claim a fresh isolated-process run.

## Findings

| Boundary | Current evidence | Consequence |
| --- | --- | --- |
| Admission → CLI | TemplateInputValidator and TemplateGraphResolver raise MCPError(code=ERR_CONFIG); CLI catches only ConfigError/FileNotFoundError. | Valid rejection escapes the recovery boundary. |
| Diagnostic transport | MCPError retains message/code/params; str(error) retains only message. DegradedMCPServer takes a reason string. | Merely broadening the catch loses structured package/line/field/cause facts. |
| Existing degraded mode | Registers only health_check; no resources, presenter or publisher. | Health is possible after a caught error, but retry/edit is unavailable; a health-only fallback is incomplete recovery. |
| Process/streams | Popen owner waits and clears the shared process reference; stderr reader starts after replay. Readers consult the shared mutable child reference. | Early-exit stderr can be lost; process-generation/reader ownership needs explicit handling. |
| Initialization/readiness | Replay blocks on readline without its own deadline; non-JSON is logged and accepted; JSON result/error/id is not validated; ready and restart_completed follow unconditionally. Initial spawn also logs ready before client initialize. | Exit, invalid/error response and stalls are not truthful readiness outcomes. |
| Requests/retry | send_to_server returns silently during restart or when the child/stdin is absent; trigger_restart returns when no child exists. | Calls disappear and a dead child has no tool-mediated retry route. |

All viable options must preserve startup stderr from spawn through early exit, retain original diagnostic fields, require valid initialization plus a live child for transport readiness, distinguish operational health from transport readiness and provide bounded responses when forwarding is impossible. Config/admission failure may be recoverable; missing launch prerequisites or unexpected internal/process failure must remain explicit failures, not healthy recovery. Bootstrap releases its upgrade lock in finally; recovery must not bypass or mutate renewal records.

### Recovery ownership options — undecided

| Option | Repair/retry experience | Cost and risks |
| --- | --- | --- |
| A. Minimal server recovery mode | On recognized startup rejection, initialize a separately composed minimal diagnostic/health and retry surface. Correct source with the normal external editor, then explicitly retry admission. CLI/server own startup diagnostics; proxy owns child/streams and truthful forwarding. | Smallest useful operational scope and existing MCP server transport can be reused. Must compose independently of rejected suite/config and expose only available operations; no full editing service. |
| B. Proxy-owned recovery endpoint | Proxy itself answers diagnostic/retry requests when no child survives, then starts a corrected child. Source repair remains external. | Covers completely dead children, but puts MCP control/discovery and startup diagnostic interpretation into the forwarding proxy. More protocol/state ownership and a second response implementation. |
| C. Recovery mode with in-session file repair | Diagnosis, bounded repair and retry are available over MCP even when the normal suite was rejected. | Most agent autonomy; requires a separately admitted write/repair contract and safe candidate validation/commit ownership. Materially broader than diagnosis/retry; must be explicitly authorized and cannot quietly weaken normal admission or add a sandbox/deployment scope. |

A best fits a small, explicitly recoverable startup repair if external source correction is acceptable. This is a discussion recommendation, not a selected implementation. B is justified only if recovery must reside in the transport when no server can run; C requires an explicit additional write-scope decision.

## Questions

- Choose recovery ownership: minimal server mode (A), proxy control (B), or authorize in-session repair scope (C).
- Is correction in the external editor followed by MCP retry sufficient, or must MCP itself repair the source?
- Confirm a one-off isolated process demonstration as practical verification without adding or running regression tests.

## References

- [Recorded F6 runtime evidence](<../issue473/tool-practice-findings.md#f6--template-admission-failure-terminates-bootstrap-and-leaves-a-falsely-ready-proxy>)
- [CLI startup boundary](<../../../mcp_server/cli.py>)
- [Bootstrap and admission lock](<../../../mcp_server/bootstrap.py>)
- [Exception payloads](<../../../mcp_server/core/exceptions.py>)
- [Admission field diagnostics](<../../../mcp_server/services/template_catalog.py>)
- [Graph syntax diagnostics](<../../../mcp_server/services/template_graph.py>)
- [Current degraded server](<../../../mcp_server/server.py>)
- [Proxy lifecycle](<../../../mcp_server/core/proxy.py>)
- [Current administration reference](<../../reference/tools/discovery.md>)
- [Proxy guidance requiring later reconciliation](<../../reference/proxy_restart.md>)

## Approved Strategy

| Boundary | Owner decision / remaining choice |
| --- | --- |
| Changed startup/error/recovery contracts | Owner requires a clean break: no legacy routes, aliases, compatibility profile or bridge. |
| Suite admission | Strict rejection remains binding; no invalid snapshot activation or silent last-known-good fallback. |
| Recovery ownership and repair access | Pending discussion: A, B or C; whether external editing is sufficient or MCP must also repair files. Research remains open. |
| Verification/process | Owner explicitly requests no regression tests. No regression tests were created or run. A bounded one-off isolated success/failure/recovery demonstration is proposed for later verification, subject to discussion; no artificial RED/GREEN cycle or persistent test framework. |

## Expected Results

A rejected suite yields accessible original diagnostics; ordinary tools do not run against invalid content. Child early exit, invalid/error initialize and a nonresponsive initialize never become ready/restart success. Requests receive bounded actionable failures instead of disappearing. Explicit retry after source correction can activate only a newly admitted valid suite; repeated failure retains a usable diagnostic path. Later demonstration must distinguish direct CLI from proxy-mediated recovery.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-05 | @imp researcher | Record current causal evidence and compare recovery ownership options. |
