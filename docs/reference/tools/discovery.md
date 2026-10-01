<!-- template=reference -->
# Discovery and Administration

This reference covers the public discovery and server-administration tools. Exact schemas and result fields are owned by each linked implementation and output model.

## `get_work_context`

Source: [`discovery_tools.py`](../../../mcp_server/tools/discovery_tools.py) and [`GetWorkContextOutput`](../../../mcp_server/schemas/tool_outputs.py).

This fieldless-input tool reports the current branch and the workflow state it can resolve, including phase, role hint, phase instructions, optional handover template, and workflow-state status. It reads branch/workflow state through injected managers and uses configured workflow contracts for phase instructions and valid-phase recovery information. Missing or unreadable branch state is represented in the result; it is not a generic workspace search tool.

## `health_check`

Source: [`health_tools.py`](../../../mcp_server/tools/health_tools.py).

The fieldless-input health tool reports status, optional reason, server version, process ID, platform, and uptime. Its output contract is [`HealthCheckOutput`](../../../mcp_server/schemas/tool_outputs.py). It does not promise a tool count, memory metrics, or workspace paths.

## `restart_server`

Source: [`admin_tools.py`](../../../mcp_server/tools/admin_tools.py).

The input contains an optional `reason` string, defaulting to `"code changes"`. The tool records the request and restart marker, then asks the supervising server process to restart. This is a process lifecycle operation; do not assume a zero-downtime proxy, a fixed client wait interval, or a separate restart-verification tool.

## Related references

- [Tools reference index](README.md)
- [Server configuration](../server-configuration.md)
- [Presentation architecture](../presentation_architecture.md)
