<!-- pgmcp:v1 id=pr pv=1.0.0 pf=hG0a9tLUxIzayxH4 sf=5--KpGf2wHUv2qAj -->

## Summary

A rejected template could escape CLI recovery and leave the proxy reporting readiness while requests had no live initialized server. This change preserves the original startup diagnosis, exposes the two existing recovery tools, and reports transport readiness and failures truthfully.

Closes #481. Administrative parent: #289; integration base: main.

## Changes

- Recognize bootstrap MCPError(code=ERR_CONFIG) alongside the existing recognized configuration/file failures, capture original parameters and nested causes, and compose recovery from injected Settings with its own presenter.
- Expose exactly health_check and restart_server during rejected admission. Agents diagnose from JSON in MCP text, correct source externally and explicitly restart; invalid content remains rejected.
- Drain generation-bound stdout/stderr through EOF, validate the live initialize exchange under the existing 30-second handshake deadline, and correlate unavailable responses once without replaying ordinary requests.
- Migrate current health/degraded callers and update only the two current health/restart and proxy references. The four existing test-file changes are mechanical caller migrations, not new regression coverage.

## Testing

Independent QA in chat 'Beoordeel designplan' gave GO for Validation and Documentation -> Ready on e88d8b81496d39c264082e0ead9e1f63c8f247d5 (review turn 01a10c4b-ee67-7932-810a-163ed13f9af0), within the explicitly approved acceptance and gate exception.

- QA's fresh targeted python_review on eight changed production files: format, lint, Mypy and Pyright passed. Targeted format/lint on four mechanical test callers passed. QA link review of Validation and both references passed.
- Recorded native configured production Mypy passed (c2566b3cc9dc486ab3f6608de0cfa0da); configured Pyright passed, 188 files, zero errors/warnings (68fabcfa68e54f07a3aaf7bb742838f9).
- The same configured run remains incomplete: Ruff-format exited 3 on access denied, reporting 473 files already formatted; Ruff-lint exited 1 with 130 T201 findings in three unchanged historical archive examples and an access warning. The owner explicitly accepted these limitations for #481; they are not reported as passes.
- One disposable process demonstration plus the owner-requested live fault/recovery showed complete F6 diagnosis, original nested cause, repeated rejection, corrected-source healthy admission, invalid restart input, ordinary-tool rejection, early exit, invalid initialization, spawn failure, timeout and request/restart races. The real timeout measured 31.138 s including launch against the unchanged 30 s handshake deadline. All temporary drivers/captures/workspaces were removed.
- No regression tests were added or run, in accordance with the owner-approved strategy. No production or existing test Python changed after the live recovery demonstration.
- Documentation edit preflights passed; reference link review passed with 16 successes, zero errors (495c0d8e0cfe44f9885cb367b060c8ce). Ready reuses fresh evidence.

## Breaking Changes

Clean break: health startup_diagnostic replaces reason without an alias; current degraded/health construction callers use the new contracts. Recovery provides actionable MCP text; outputSchema, structuredContent and healthy-server interface/performance parity are not required by the owner-refined acceptance. Historical Research/Design/Planning are retained; Validation and stored acceptance explicitly supersede their contrary schema criterion.

Residual operating limits: a restart receipt acknowledges the request, not successful admission. Check fresh health and refresh tools/list; hosts with stale discovery may need reconnect. Fatal Settings/root/launch failures before recovery composition require external correction and relaunch. No compatibility route, admission relaxation or in-session repair service is introduced.

## Deferred Work

### Configured workspace Ruff evidence remains incomplete/failed: an unidentified access-denied scan path and 130 T201 print findings in three unchanged archive examples. Coordination triage is needed; no follow-up issue was created.

Excluded from #481 because archive cleanup and workspace execution/configuration remediation are unrelated to startup recovery. The owner explicitly accepted this issue-specific exception. The impact is that workspace format/lint cannot be described as all-green; preserve these outcomes and investigate separately.

**References:**

- [Recorded outcomes and owner exception](<https://github.com/MikeyVK/phase-gate-mcp/blob/e88d8b81496d39c264082e0ead9e1f63c8f247d5/docs/development/issue481/validation.md#configured-gate-disposition--owner-approved-exception>)

## Closes

#481

## Related Documents

- [Validation evidence and owner decisions][related-1]
- [Health and restart reference][related-2]
- [Proxy reference][related-3]

[related-1]: <https://github.com/MikeyVK/phase-gate-mcp/blob/e88d8b81496d39c264082e0ead9e1f63c8f247d5/docs/development/issue481/validation.md>
[related-2]: <https://github.com/MikeyVK/phase-gate-mcp/blob/e88d8b81496d39c264082e0ead9e1f63c8f247d5/docs/reference/tools/discovery.md>
[related-3]: <https://github.com/MikeyVK/phase-gate-mcp/blob/e88d8b81496d39c264082e0ead9e1f63c8f247d5/docs/reference/proxy_restart.md>

