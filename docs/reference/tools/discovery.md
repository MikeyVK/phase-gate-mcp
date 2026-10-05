<!-- template=reference -->
# Discovery and Administration

This reference covers public discovery and server-administration tools. The linked
implementations and output models own their exact contracts.

## `get_work_context`

Source: [discovery_tools.py](../../../mcp_server/tools/discovery_tools.py) and
[GetWorkContextOutput](../../../mcp_server/schemas/tool_outputs.py).

This fieldless-input tool reports the current branch and the workflow state it can
resolve, including phase, role hint, phase instructions, optional handover template,
and workflow-state status. It reads branch/workflow state through injected managers
and uses configured workflow contracts for phase instructions and valid-phase recovery
information. Missing or unreadable branch state is represented in the result; it is
not a generic workspace search tool.

get_work_context is an ordinary tool and is unavailable when startup admission has
failed. After a successful replacement, refresh the work context before continuing
workflow operations.

## `health_check`

Source: [health_tools.py](../../../mcp_server/tools/health_tools.py),
[HealthCheckOutput](../../../mcp_server/schemas/tool_outputs.py) and
[StartupDiagnostic](../../../mcp_server/schemas/startup_diagnostic.py).

The fieldless-input health tool reports status, optional startup_diagnostic, server
version, process ID, platform and uptime. startup_diagnostic replaces the former
reason field; there is no compatibility alias.

A successful health query can report status=unhealthy. success=true means the query
completed; it does not mean source admission succeeded. For a recognized bootstrap
failure, the limited recovery server exposes exactly health_check and restart_server.
Ordinary editing, Git and workflow tools remain unavailable.

The recovery health response includes a readable introduction followed by JSON in MCP
text content. startup_diagnostic preserves the original exception type, message,
optional code, ordinary JSON parameters, optional file path and nested cause.
Template/field/line information is available when supplied by the original error.
For example:

~~~json
{
  "status": "unhealthy",
  "startup_diagnostic": {
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
}
~~~

This is an excerpt, not the full health DTO. An agent can diagnose from that text,
repair the source externally and request restart. outputSchema, structuredContent
and parity with the healthy server's interface or performance are not requirements
for this limited recovery surface.

Admission remains strict: invalid content is not admitted, and restart performs a
fresh bootstrap. Failures before the recovery boundary, such as invalid Settings or
a missing server root, require external correction and launcher reconnection rather
than recovery-tool calls.

## `restart_server`

Source: [admin_tools.py](../../../mcp_server/tools/admin_tools.py).

The input contains an optional reason string, defaulting to "code changes".
The tool records the request and restart marker, returns a receipt and then signals
the supervising process. Recovery exposes the same tool with input validation;
invalid input produces a readable error response.

The receipt acknowledges the request. It does not confirm that a replacement started
or passed admission. When launched through the [restart proxy](../proxy_restart.md),
the proxy replaces the child and performs a new initialize exchange. A direct CLI
launch needs an external supervisor or a manual relaunch.

After correction and restart, query health_check again and refresh tools/list.
A fresh unhealthy response means admission still failed; use its current diagnosis.
A fresh healthy response permits ordinary tools from the newly admitted source.
Clients that retain stale tool discovery may need to reconnect.

## Related references

- [Tools reference index](README.md)
- [Server configuration](../server-configuration.md)
- [Presentation architecture](../presentation_architecture.md)
