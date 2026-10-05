# MCP Restart Proxy

**Component:** mcp_server.core.proxy  
**Status:** Current operational reference

The proxy holds the client's stdio connection while replacing its server child.
Transport readiness and source admission are separate: an initialized recovery child
can be reachable while health_check reports unhealthy.

Source: [proxy.py](../../mcp_server/core/proxy.py),
[CLI recovery composition](../../mcp_server/cli.py) and
[restart_server](../../mcp_server/tools/admin_tools.py).

## Launching

Configure the MCP client to launch the workspace Python interpreter with these
arguments and the repository as its working directory:

~~~json
{
  "command": "C:/path/to/workspace/.venv/Scripts/python.exe",
  "args": ["-m", "mcp_server.core.proxy"],
  "cwd": "C:/path/to/workspace"
}
~~~

This fragment shows the launch fields; the enclosing configuration format belongs
to the client. On other platforms, use that environment's Python executable.
Launch the proxy for managed child replacement. Direct mcp_server execution has no
proxy to replace the process after a restart request.

The proxy sets PYTHONUTF8=1 for children and uses UTF-8 stdio. Its Windows entrypoint
also configures the proxy's own streams for UTF-8.

## Initialization and readiness

| State | Meaning |
| --- | --- |
| starting | Child launched; initialization has not completed. |
| ready | A validated initialize result and the initialized notification have completed for the active live child. |
| restarting | The old generation is being replaced; ordinary requests cannot be forwarded. |
| unavailable | Launch, initialization or transport failed; inspect stderr/audit evidence. |
| stopped | Proxy lifecycle ended. |

The default initialization deadline is 30 seconds. It starts when the initialize
request is sent to the child and covers completing the handshake, including
notifications/initialized. It is not a planned startup sleep or a delay added to
every request. Before the first client initialize request, the transport remains
starting; no initialization timer has yet begun.

The initial initialize response is validated and forwarded to the client. The proxy
marks ready only after forwarding notifications/initialized and confirming that the
active child is still live. A restart replays only the captured initialize request,
validates the replacement's response and matching protocol version, consumes that
response internally, then sends notifications/initialized. There is no second reader
competing for stdout and no fixed wait used as proof of readiness.

server_ready and restart_completed describe transport initialization. They do not
establish healthy admission. Query health_check for the domain result.

## Admission failure and recovery

Recognized bootstrap configuration failures produce a limited server exposing exactly
health_check and restart_server. Its health text contains the original structured
diagnosis, including available parameters and cause. Ordinary tools remain unavailable.

1. Read health_check and locate the failing source from its diagnostic.
2. Repair that source with an external editor.
3. Call restart_server with a reason.
4. Read fresh health_check and refresh tools/list after replacement.
5. Continue ordinary work only after healthy admission.

Invalid content remains rejected. Another restart without correction can produce a
new unhealthy child with the same diagnostic. The restart receipt confirms only that
the request was accepted. The limited surface does not require an advertised
outputSchema, structuredContent or healthy-server performance/interface parity.
See [health and restart contracts](tools/discovery.md).

Failures before recovery composition, including invalid Settings or a missing server
root, may leave no MCP tool endpoint. Correct those externally and reconnect/relaunch.
The proxy does not automatically restart every crashed or unavailable child.

## Restart and request ownership

restart_server emits the exact stderr line __MCP_RESTART_REQUEST__ after returning its
receipt. The proxy claims at most one restart for the active generation, including a
marker drained just after that child exits. Duplicate or retired-generation markers
do not create another restart.

Each child generation owns its process, pending request IDs and captured stdout/stderr
readers. Readers drain their captured streams through EOF, including final stderr
without a newline. The proxy serializes client stdout writes and ignores late,
uncorrelated responses from an obsolete generation.

Pending requests interrupted by restart or child failure receive one unavailable
response per registered request ID. Requests arriving while forwarding is unavailable
also receive an error. Notifications have no response; undeliverable messages are
logged. Ordinary requests are not queued or replayed across generations. Callers
should inspect the outcome before deciding whether to retry a mutation.

A transport-unavailable response uses JSON-RPC error code -32000 with data such as:

~~~json
{
  "code": "ERR_SERVER_UNAVAILABLE",
  "state": "unavailable",
  "generation": 1,
  "server_pid": null,
  "reason": "forwarding_unavailable"
}
~~~

A failed spawn has no child PID. Other failures report the relevant process identity
and reason, for example initialize_timeout or restart_interrupted. On Windows, the
launcher PID recorded by the proxy can differ from the server's health PID.

Process termination waits up to five seconds before escalating to kill, then waits
up to five seconds for termination. These waits are separate from the initialization
deadline and are not a promised total restart duration.

## Logging and troubleshooting

Proxy events are written to stderr and the audit log at:

~~~text
<PGMCP_WORKSPACE_ROOT>/<PGMCP_SERVER_PROJECT_DIR>/<PGMCP_LOGS_DIR>/mcp_audit.log
~~~

Defaults are the current working directory, .pgmcp and logs respectively.
Server stderr is retained as server_stderr with its generation and process identity.

| Evidence | Interpretation and action |
| --- | --- |
| server_spawned without server_ready | Spawn is not readiness. Inspect subsequent initialization/exit evidence. |
| initialize_timeout | The handshake exceeded its deadline. Inspect startup stderr and correct the cause. |
| initialize_response_failed / initialize_stdout_invalid | Error, invalid result/ID/protocol or malformed initialization output. Correct the launch/source and retry externally if no recovery endpoint exists. |
| server_start_failed | Process launch failed; server_pid is null. Correct interpreter/launch configuration. |
| child_exited / stdout_closed | Child transport ended; pending requests receive unavailable responses. |
| restart_initiated followed by restart_completed | Replacement transport initialized; health still needs inspection. |
| restart_failed | Replacement did not become ready. Use current stderr and generation evidence. |
| uncorrelated_response | A response no longer owns a pending request; it is not forwarded to the client. |

Clients may retain stale tool lists after unhealthy-to-healthy replacement. Refresh
tools/list; reconnect when the host does not refresh discovery. The stable proxy
connection does not promise uninterrupted request service or a fixed restart latency.

## Related references

- [Discovery and administration](tools/discovery.md)
- [Server configuration](server-configuration.md)
