# PhaseGate MCP Server - User Guide

**Status:** v1.0 (Foundation)
**Last Updated:** 2025-01-21

> [!WARNING]
> **DEPRECATED / UNDER REVIEW**
> This user guide represents the legacy v1.0 architecture and is currently under review.
> For the authoritative server configuration and settings, please refer to [docs/reference/server-configuration.md](../reference/server-configuration.md).
> For the complete list of tools and categories, see [docs/reference/tools/README.md](../reference/tools/README.md).
---

## 1. Introduction

The PhaseGate MCP Server (`phase-gate-mcp`) is a Model Context Protocol server designed to assist with the development of the phase-gate-mcp project. It provides AI agents with context about the project's state, coding standards, and facilitates workflows like TDD and GitHub integration.

## 2. Installation

The MCP server is part of the repository. You can install it in editable mode:

```bash
# From the root of the repository
pip install -e .

# To include development dependencies (for running tests)
pip install -e ".[dev]"
```

## 3. Configuration

Runtime server/logging settings use supported environment variables and an optional launcher overlay selected explicitly by PGMCP_CONFIG_PATH. There is no automatic mcp_config.yaml selection. Current workspace policy and GitHub identity use the [configuration layers](../reference/config-loading-architecture.md).

### 3.1 Environment Variables
| Variable | Description | Default |
|----------|-------------|-------|
| `GITHUB_TOKEN` | GitHub Personal Access Token (required for GitHub integration) | None |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO |
| `PGMCP_SERVER_PROJECT_DIR` | Sub-directory under workspace_root for all server data | `.pgmcp` |
| `PGMCP_LOGS_DIR` | Sub-directory under server_root for log files | `logs` |
| `PGMCP_CONFIG_PATH` | Explicit optional server/logging overlay path | unset |
### 3.2 Explicit launcher overlay

Example configuration:

```yaml
server:
  name: "phase-gate-mcp"
  workspace_root: "."

logging:
  level: "INFO"
  # audit_log is auto-derived as <server_root>/<logs_dir>/mcp_audit.log
  # (default: .pgmcp/logs/mcp_audit.log)

```

Select that file explicitly with PGMCP_CONFIG_PATH. In the unreleased configuration
contract, owner/repo and optional project metadata belong in layered github.yaml;
a nonempty GITHUB_TOKEN takes precedence over its configured token alternative.
Use the [current source contract](../reference/config-loading-architecture.md), not
this legacy guide, for complete setup instructions.

## 4. Running the Server

To run the server using the `mcp` SDK's standard I/O transport:

```bash
python -m mcp_server
```

This command starts the server and listens on `stdin` for JSON-RPC messages, writing responses to `stdout`. Logs are written to `stderr` and the audit log file.

## 5. Claude Desktop Integration

To use this MCP server with Claude Desktop, add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "phase-gate-mcp": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "cwd": "/absolute/path/to/phase-gate-mcp",
      "env": {
        "GITHUB_TOKEN": "your-github-token"
      }
    }
  }
}
```

Replace `/absolute/path/to/phase-gate-mcp` with the actual path to your repository.

## 6. Current tools and resources

This legacy guide does not enumerate the current runtime contract. Use the
[tool reference](../reference/tools/README.md) for registered tools and their schemas,
[resource reference](../reference/resources.md) for implemented and planned resource
URIs, and [server configuration](../reference/server-configuration.md) for current
settings and root resolution.

Tool responses may include a run-specific `pgmcp://cache/runs/{run_id}` URI containing
the complete structured result. Large results can be read in bounded windows; use the
`pgmcp://docs/cache-reading` resource for limits, integrity checks, and safe retry rules.
A cache entry records the result returned by that tool call. It is not, by itself, a
quality-gate pass or test result.

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.1 | 2026-07-20 | Agent | Mark user guide as deprecated in favor of server-configuration.md and tools/README.md |
| 1.0 | 2025-01-21 | Agent | Initial draft |
