<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=CT9NV5LmQjKHFGqX sf=5--KpGf2wHUv2qAj -->

# Startup admission diagnostics and recovery — Validation (#481)

**Status:** VALIDATION FAILED — public-schema acceptance blocker; review requested  
**Version:** 0.1  
**Last Updated:** 2026-10-05

## Scope

Evaluate the approved minimal recovery correction at implementation HEAD
cc4a83c30d93961716aff61c6d7fc6859e80eccb, using one disposable real-CLI/proxy
demonstration. No regression tests were added or executed. Validation stopped at a
concrete unmet Design/Planning criterion; it did not modify production or reinterpret
the acceptance contract. V481.1 remains incomplete.

The owner instructed “Door naar de validation phase”; the normal transition succeeded
(receipt 683889927e1d4f28bfa10059d963ba91). Independent QA had approved Planning 0.3;
no independent Implementation verdict is claimed.

## Process evidence

Invocation: .venv/Scripts/python.exe .pgmcp/temp/issue481_process_demo.py.
The temporary driver used subprocess stdio and public MCP initialize, tools/list and
tools/call boundaries. Children ran the changed branch's real mcp_server and
mcp_server.core.proxy entrypoints. Only copied configuration, templates and
installation.json were used; version checks and strict admission remained enabled.
No GitHub calls or ordinary mutation tools were invoked.

Captured at 2026-10-05T12:42:03.553244+00:00 in the disposable
.pgmcp/temp/issue481_demo_9zlwavtq workspace.

| Scenario | Observed result | Outcome |
| --- | --- | --- |
| Direct CLI valid baseline | Initialize, tools/list and healthy health response; 49 tools. Elapsed launch-to-health 7.639 s. | Observed |
| Proxy valid baseline | Initialize and initialized notification, server_ready, 49 tools and healthy health response. Elapsed launch-to-health 8.507 s. | Observed |
| Direct CLI F6 rejection, first launch | Only health_check/restart_server; unhealthy health query succeeded with the original diagnostic. Reported health PID 19440. | Observed |
| Direct CLI F6 rejection, second launch | Fresh launch, same complete diagnostic and two recovery tools. Reported health PID 30588. | Observed |
| Proxy F6 rejection | Successful initialize and server_ready; tools/list returned exactly the two recovery tools, without outputSchema. | Acceptance failure |

Timing includes tool discovery and health; it is not a bootstrap-only measurement or
a performance guarantee. All five demonstration launcher processes exited with code 0
during cleanup. Windows launcher PID and the child's reported os.getpid() are distinct
identities; no equality between those values is asserted.

The F6 source change was confined to the copied shared document base: replace
content.document_metadata.revisions | last with
content.document_metadata.revisions[-1]. The actual public health response contained:

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

The containing health DTO had success=true, status=unhealthy and isError=false in
the MCP result. Parameters were an ordinary JSON object. This particular admission
error had no cause/file_path; preservation of a non-null cause is not established by
this capture.

## Blocking finding: absent public outputSchema

Design requires diagnostic params to be an ordinary JSON object in serialized output
and outputSchema. Planning explicitly requires capturing the actual advertised
schema at the MCP boundary. The proxy's real tools/list response advertised these
complete tool objects:

~~~json
[
  {
    "name": "health_check",
    "description": "Check server health status",
    "inputSchema": {
      "additionalProperties": false,
      "description": "Input for HealthCheckTool.",
      "properties": {},
      "title": "HealthCheckInput",
      "type": "object"
    }
  },
  {
    "name": "restart_server",
    "description": "Restart MCP server to reload code changes",
    "inputSchema": {
      "additionalProperties": false,
      "description": "Input for RestartServerTool.",
      "properties": {
        "reason": {
          "default": "code changes",
          "description": "Description of why restart is needed (for audit logging)",
          "title": "Reason",
          "type": "string"
        }
      },
      "title": "RestartServerInput",
      "type": "object"
    }
  }
]
~~~

The driver stopped with KeyError('outputSchema') when reading the required field.
The wire capture independently confirms absence; this is not merely a driver parsing
failure or proof that a model's locally generated schema is invalid.

Source trace: [MCPServer.setup_handlers](../../../mcp_server/server.py) publishes a
schema only when the outer tool exposes output_model.
[ToolErrorHandlerDecorator](../../../mcp_server/core/decorators/tool_error_handler_decorator.py)
and [InputValidationDecorator](../../../mcp_server/core/decorators/input_validation_decorator.py)
do not expose that metadata; [ITool](../../../mcp_server/core/interfaces/itool.py) does
not declare it. The recovery composition wraps both core tools in those decorators.

Do not fix this by blindly adding schema metadata: the installed MCP SDK 1.26.0
lowlevel call handler validates structuredContent when outputSchema is advertised.
The current server returns presentation content without structuredContent. An
Implementation correction must reconcile both sides at the existing public boundary,
or explicitly reopen the approved boundary decision if that requires broader work.
Validation neither supplies such a correction nor waives the requirement.

## Static evidence and stopped work

Current Git status contained only the Validation phase-state change and this report;
no production/test Python changed during Validation. The main...HEAD inventory and
working-tree status were refreshed (receipts e9b64a75bcbf4b6294324069ba6db628 and
5794d691f4b4435fa1bb6f3be3308292). Markdown/workflow JSON were not sent to Python checks.

This report's native Markdown edit preflight and targeted markdown_link_review passed
(link receipt 195aa2c3c7eb4d5b97a944493743bccb).

Fresh Implementation evidence remains applicable to unchanged sources:

| Selection | Native outcomes | Receipt |
| --- | --- | --- |
| Eight changed production Python files, python_review | Format, lint and Pyright passed; the initial Mypy finding was subsequently corrected. | 8cb36f91e44f475a98429947de126c20 |
| Same eight production files, python_types | Passed after the protocol-version annotation correction. | ce1d75e87aaa471e9f3a7e9cc3a227ce |
| Final changed proxy, python_review | Format, lint, Mypy and Pyright passed. | 62a77f25305a423d84a8d3454b15031e |
| Four mechanical test callers, python_format/python_lint | Both passed; edit-content syntax preflight also passed. | 402ee81870c94747878eea615dbc80cb |

The phase instruction says “Stop if implementation is incomplete or contradicts
approved inputs; Validation does not redesign or patch.” Therefore the remainder
was not executed after the public-schema failure:

- Proxy repeated rejection and corrected-source restart; corrected direct CLI relaunch.
- Invalid restart input/error presentation and preservation of a non-null exception cause.
- Early exit, invalid/error/wrong-ID initialize, actual 30-second timeout and request/restart races.
- Final run_checks(scope="configured", checks=["python_format","python_lint","python_pyright"], timeout_seconds=600).
- Separate run_checks(scope="configured", checks=["python_types"], timeout_seconds=600).

No full-suite/regression execution is pending: the owner-approved strategy explicitly
excludes it. The pending items above remain required for V481.1 after correction.

## Containment and review request

Live configuration, templates, installation/renewal records and production sources
were untouched by the demonstration. Temporary children were stopped. The ephemeral
driver, captures and copied workspaces are discarded after retaining these concise
observations; no test/probe framework is committed.

The first capture attempt hit the temporary driver's Windows stdout encoding; UTF-8
was applied to that driver's output before the recorded attempt. It was not a
production failure. The later missing-outputSchema failure remains unresolved.

Review requested: confirm the public-boundary finding and route the concrete
correction back to Implementation. No Validation PASS, independent GO or readiness
is asserted.

## Related Documents

- [Approved Research strategy](research.md)
- [Design](design.md)
- [Planning 0.3](planning.md)
- [Historical F6 evidence](../issue473/tool-practice-findings.md#f6--template-admission-failure-terminates-bootstrap-and-leaves-a-falsely-ready-proxy)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-05 | @imp validator | Record real CLI/proxy observations, the public-schema blocker and explicitly unexecuted acceptance work. |
