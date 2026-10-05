<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=CT9NV5LmQjKHFGqX sf=5--KpGf2wHUv2qAj -->

# Startup admission diagnostics and recovery — Validation (#481)

**Status:** VALIDATION RECORDED — configured gate limitations accepted by owner  
**Version:** 0.4  
**Last Updated:** 2026-10-05

## Scope and authority

Evaluate the minimal recovery correction on bug/481-startup-admission-recovery at
HEAD cfe4e75d3da0f1b7f54c20258a90be8686b5f4d3. Production and mechanical caller code
did not change during Validation. No regression tests were added or executed.

The owner instructed “Door naar de validation phase”; the normal transition succeeded
(receipt 683889927e1d4f28bfa10059d963ba91). Independent QA approved Planning 0.3;
no independent Implementation or Validation verdict is claimed.

## Owner-approved acceptance refinement — 2026-10-05

After the live demonstration, the owner instructed:
“Ik ben het hiermee eens maak dit expliciet, zonder alle documentatie bij te werken.
Daarna door naar de doc phase”.

Binding acceptance for the limited recovery boundary is now:

- health_check exposes the original actionable diagnosis in its MCP text response,
  including available exception type, code, message, parameters, template/field/line,
  file path and nested cause.
- The agent repairs the source externally, then explicitly calls restart_server.
  Only newly admitted valid content enables the ordinary tools.
- outputSchema, structuredContent and parity with the healthy server's interface or
  performance are not required for this recovery surface.
- Strict admission, the clean break, truthful transport readiness, the existing
  initialization deadline and the approved no-regression-test verification remain.

This decision supersedes the contrary schema criterion in earlier Design/Planning
and the original Validation finding. Research, Design and Planning remain historical
documents at the owner's request. Stored D481.1.1/V481.1 descriptions record the same
refinement. No production or typed-output framework change is needed for this decision.

## Owner-requested live recovery demonstration

The owner explicitly requested a live fault, restart and health_check through the
active registered proxy connection.

| Step | Actual result |
| --- | --- |
| Baseline | healthy, reported server PID 28508; branch clean. |
| F6 fault | Native safe_edit_file changed revisions \| last to revisions[-1] in the shared document base; receipt b977e4dbfd364d3380c4652169e8a5a4. |
| Restart | Request accepted from PID 28508; receipt 7029f677a6a84fd0b70e773f597a366a. |
| Recovery health | unhealthy, success=true, PID 12164; original diagnostic in the text response. |
| External repair | safe_edit_file was unavailable (“Tool not found”). The exact expression was restored with a local editor. |
| Recovery retry | restart_server succeeded from PID 12164; its receipt explicitly did not confirm admission success. |
| Fresh health | healthy, PID 27016; receipt 26c6cd2dd38d41d1ad039b1f220ac86e. |
| Cleanup | Original source restored and native Git status clean; receipt d3be5d5b1179433884bf99755f401967. |

The actual public diagnostic was:

~~~json
{
  "exception_type": "mcp_server.core.exceptions.MCPError",
  "message": "template_input_undeclared",
  "code": "ERR_CONFIG",
  "params": {
    "template_id": "architecture",
    "template": "shared/templates/bases/tier2_markdown_document.jinja2",
    "field": "content.document_metadata.revisions.-1",
    "line": 8
  },
  "file_path": null,
  "cause": null
}
~~~

The health query succeeded while reporting unhealthy; the MCP result had isError=false.
Parameters were an ordinary JSON object. This response enabled diagnosis, external
repair and explicit retry without an output schema.

## Disposable process demonstration

Invocation: .venv/Scripts/python.exe .pgmcp/temp/issue481_process_demo.py.
The disposable driver used public MCP stdio initialize, tools/list and tools/call.
Real CLI/proxy children used copied configuration, templates and installation.json,
with version checks and strict admission enabled. No ordinary mutation/GitHub tools
were called. Controlled children exercised the proxy's public process_factory boundary
for failure and race observations. No permanent test/probe framework is added.

Initial capture: 2026-10-05T12:42:03.553244+00:00, issue481_demo_9zlwavtq.
Continuation: 2026-10-05T13:22:25+00:00, issue481_demo_fmae5ajs.
The continuation reused unchanged baseline evidence rather than repeating it.

| Scenario | Observed result |
| --- | --- |
| Direct CLI valid baseline | Healthy and 49 tools; launch-to-health 7.639 s. |
| Proxy valid baseline | Initialized, server_ready, healthy and 49 tools; launch-to-health 8.507 s. |
| Direct CLI repeated F6 rejection | Two launches exposed only health_check/restart_server and the complete original diagnostic; health PIDs 19440 and 30588. |
| Proxy rejected public boundary | Exactly two recovery tools; unhealthy PID 6580 with ordinary JSON diagnostic parameters. get_work_context rejected with isError=true. |
| Invalid restart input | Unexpected property rejected; readable ValidationError DTO, validation details, input schema and isError=true. |
| Proxy repeated rejection | Explicit restart created a fresh unhealthy child, health PID 20092, preserving the same diagnostic. |
| Proxy corrected admission | External source correction then explicit restart; healthy PID 24312 and 49 ordinary tools. |
| Direct CLI corrected relaunch | Healthy PID 19308 and 49 tools. |
| Original exception cause | Unknown Jinja tag on line 47 retained outer template_syntax_invalid/ERR_CONFIG plus nested jinja2.exceptions.TemplateSyntaxError and “Encountered unknown tag 'issue481_invalid_tag'.” |
| Early exit | Unavailable initialize and subsequent request, each ID answered once; final stderr without newline preserved. Elapsed 1.281 s. |
| Error / malformed / wrong-ID / invalid-shape initialize | Truthful unavailable responses, each initialize/subsequent request ID answered once. Elapsed 1.253 / 1.260 / 1.234 / 1.431 s. |
| Spawn failure | Generation 1, server_pid=null, unavailable responses; no fabricated child PID. Elapsed 1.233 s. |
| Actual initialization timeout | initialize_timeout and ERR_SERVER_UNAVAILABLE; elapsed 31.138 s including launcher startup, against the unchanged 30 s handshake deadline. |
| Pending request at child exit | ID hold answered once with unavailable; final buffered stderr retained. |
| Restart overlap and duplicate markers | IDs initialize/restart/hold/during/after each answered once. Interrupted and during-restart requests received ERR_SERVER_UNAVAILABLE. One restart_completed event, generation 2, duration 912.180 ms. Late uncorrelated response discarded; undeliverable notification received no response. |
| Startup lock ownership | Lock file remained and no recovery record was created. Public UpgradeLock.acquire/release successfully reacquired the same lock after shutdown. |

All 12 continuation launcher processes exited 0 during cleanup. Initial five launchers
also exited 0. Controlled child failures are separate from launcher exit status.
Windows launcher PID and the child's health PID are distinct identities.

The driver's lock-file-deletion predicate initially reported false. This was an invalid
probe assumption: [UpgradeLock](../../../mcp_server/services/template_activation.py)
explicitly retains its inode and releases the OS lock. Successful reacquisition of the
same lock and multiple fresh admitted starts resolve that observation; no production
correction was needed.

Timing is an observation, not a performance guarantee. The valid startup measurements
remain below the initialization budget. The capture's unavailable responses used
JSON-RPC -32000 and data.code=ERR_SERVER_UNAVAILABLE with state, generation, server_pid
and reason. No request replay was observed or required.

## Historical schema finding — superseded

The initial tools/list capture advertised inputSchema but no outputSchema for either
recovery tool. The original driver stopped at KeyError('outputSchema'). This absence
remains factual but is no longer an acceptance blocker under the explicit owner decision.

[MCPServer.setup_handlers](../../../mcp_server/server.py) advertises output metadata
only when exposed by the outer tool. The existing decorators do not expose that
metadata; the installed MCP SDK validates structuredContent if outputSchema is
advertised. Expanding those boundaries is outside the accepted practical correction.

## Static evidence

Refreshed native status and main...HEAD diff before final checks:
c867ceeb964e4d6fb465a8ddad614203 and 2bc7477c888541a9a0ecd257f9c60e53.
Only this report and stored deliverables were uncommitted. No Python evidence was
invalidated. Markdown and workflow JSON were excluded from Python-target checks.

Fresh Implementation evidence remains applicable:

| Selection | Actual outcomes | Receipt |
| --- | --- | --- |
| Eight changed production Python files, python_review | Format, lint and Pyright passed; initial Mypy annotation finding later corrected. | 8cb36f91e44f475a98429947de126c20 |
| Same eight production files, python_types | Passed after the protocol-version annotation correction. | ce1d75e87aaa471e9f3a7e9cc3a227ce |
| Final changed proxy, python_review | Format, lint, Mypy and Pyright passed. | 62a77f25305a423d84a8d3454b15031e |
| Four mechanical test callers, python_format/python_lint | Both passed; edit-content syntax preflight also passed. | 402ee81870c94747878eea615dbc80cb |

Required final calls ran once, with no explicit targets or caller arguments:

| Native configured selection | Actual outcomes | Receipt |
| --- | --- | --- |
| python_format, python_lint, python_pyright; timeout_seconds=600 | Overall incomplete. Format unavailable: access denied (OS error 5), exit 3, 473 files already formatted. Lint failed: 130 T201 print findings in three historical archive examples, exit 1, plus the same access warning. Pyright passed: 188 files, zero errors/warnings, exit 0. | 68fabcfa68e54f07a3aaf7bb742838f9 |
| Separate python_types; timeout_seconds=600 | Passed, configured production-scoped Mypy. | c2566b3cc9dc486ab3f6608de0cfa0da |

All lint findings are in docs/development/archive/issue52/archive/examples/demo.py,
docs/development/archive/issue72/mvp/demo.py and
docs/development/archive/issue72/mvp/scaffold_demo.py. Those files are absent from the
branch diff. They were not changed or suppressed. The native format access error does
not identify its path; its required selection remains incomplete, not a pass.

## Configured gate disposition — owner-approved exception

The owner explicitly accepted continuation with the recorded configured format/lint
limitations: “Ja dat mag”, while clarifying that no further Python code changes were
approved. For #481 these limitations are accepted as an exception; neither archived
examples nor check configuration are changed. The failed/unavailable native outcomes
remain recorded above and are not recast as passes.

No production or existing test Python changed after the owner's live fault/recovery
demonstration. Native comparison from the pre-demonstration Validation commit
2af9dfc908c9cd5ed2af607a5139bdc809289c9b to e58eed0379bca87e5d9efb18497fe8965392e88d
contains only this report and .pgmcp/deliverables.json
(receipt b7e019dee90b449c87a45e984a85b9f4); the worktree was clean
(receipt 990042dc2e764603a5a9a548b4e71000).
The disposable Python driver was adjusted for the refined schema criterion and
remaining planned observations, then removed; it was never committed.
The live template expression was restored before the successful recovery health check.

## Deliverable mapping and open work

D481.1.1: original diagnosis, two-tool recovery, external repair, fresh admission and
truthful receipt are demonstrated. D481.1.2: initialized live readiness, deadline,
generation/request ownership, stderr draining and restart outcomes are demonstrated.
D481.1.3: caller migration static evidence remains current.
V481.1: process evidence is complete under the refined acceptance; all required static
calls were made, but configured format/lint are not passing.

No full-suite/regression execution is pending: the owner-approved strategy excludes it.
The owner accepted the recorded configured gate limitations for continuation.
Documentation and independent review remain. No all-green Validation result,
independent GO, or readiness is asserted.

## Containment and review request

The isolated driver, captures and copied workspaces are removed after retaining these
observations. Live configuration, installation/renewal records and production sources
were untouched by the isolated runs. The authorized live fault was restored before
retry. No workflow, adapter, check configuration or regression-test expansion is made.

Review requested: assess the practical recovery evidence and the explicit configured
gate limitations. Documentation is limited to the two operational references planned
in DOC481.1; historical phase documents are not rewritten.

## Related Documents

- [Approved Research strategy](research.md)
- [Design](design.md)
- [Planning 0.3](planning.md)
- [Historical F6 evidence](../issue473/tool-practice-findings.md#f6--template-admission-failure-terminates-bootstrap-and-leaves-a-falsely-ready-proxy)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-05 | @imp validator | Record initial process observations and the original schema blocker. |
| 0.2 | 2026-10-05 | @imp validator | Record the owner-requested live diagnosis, repair and recovery restart. |
| 0.3 | 2026-10-05 | @imp validator | Explicit owner acceptance refinement, remaining process observations and truthful final configured gate outcomes; retain historical phase documents. |
| 0.4 | 2026-10-05 | @imp validator | Record the owner's configured gate exception and verify no production/existing test changes since the live recovery demonstration. |
