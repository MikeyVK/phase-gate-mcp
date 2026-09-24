<!-- docs\reference\mcp\server-configuration.md -->
<!-- template=reference version=064954ea created=2026-05-11T14:28Z updated=2026-05-11T14:28Z -->
# MCP Server — User-Facing Configuration


**Status:** DEFINITIVE
**Version:** 1.0
**Last Updated:** 2026-05-11

**Source:** [mcp_server/config/settings.py](../../mcp_server/config/settings.py)
**Tests:** [tests/mcp_server/unit/config/test_settings.py](../../tests/mcp_server/unit/config/test_settings.py) (12 tests)

---

## Overview

The server resolves its workspace and server-data roots at startup. `PGMCP_WORKSPACE_ROOT`
defaults to the process working directory; `PGMCP_SERVER_PROJECT_DIR` selects a child
server-data directory. Configuration and template-suite roots can independently be
redirected with `PGMCP_CONFIG_ROOT` and `PGMCP_TEMPLATE_ROOT`; when set, those paths are
authoritative even when they lie outside the server-data directory. Relative paths in
server settings resolve from the workspace root unless a setting documents another base.

---
## Path Derivation Chain

```
PGMCP_WORKSPACE_ROOT (default: cwd)
└── PGMCP_SERVER_PROJECT_DIR (default: .pgmcp) → server_root
    ├── PGMCP_CONFIG_ROOT (optional) → effective config root
    ├── PGMCP_TEMPLATE_ROOT (optional) → active template-suite root
    └── PGMCP_LOGS_DIR (default: logs) → logs_dir
        └── mcp_audit.log (unless PGMCP_AUDIT_LOG overrides it)

Without an explicit config/template root, each root is resolved under server_root.
```

| Path segment | Environment variable | Default |
|---|---|---|
| `workspace_root` | `PGMCP_WORKSPACE_ROOT` | `os.getcwd()` |
| `server_root` | `PGMCP_SERVER_PROJECT_DIR` | `.pgmcp` under workspace root |
| `config_root` | `PGMCP_CONFIG_ROOT` | `config` under server_root |
| `template_root` | `PGMCP_TEMPLATE_ROOT` | `template_suite` under server_root |
| `logs_dir` | `PGMCP_LOGS_DIR` | `logs` under server_root |

---

## Environment Variables

### Server

| Variable | Model field | Default | Description |
|---|---|---|---|
| `PGMCP_WORKSPACE_ROOT` | `server.workspace_root` | `os.getcwd()` | Repository root. All relative paths resolve from here. |
| `PGMCP_SERVER_PROJECT_DIR` | `server.server_root_dir` | `.pgmcp` | Sub-directory under workspace_root for all server data. |
| `PGMCP_LOGS_DIR` | `server.logs_dir` | `logs` | Sub-directory under server_root for log files. |
| `PGMCP_SERVER_NAME` | `server.name` | `phase-gate-mcp` | Server identifier shown in logs and API responses. |
| `PGMCP_CONFIG_ROOT` | `server.config_root` | unset | Use this configuration directory as the effective source; it remains owner-managed. |
| `PGMCP_TEMPLATE_ROOT` | `server.template_root` | unset | Use this template-suite directory as the active root; external roots remain owner-managed. |
| `PGMCP_BYPASS_VERSION_CHECK` | `server.bypass_version_check` | `False` | Set to `true` only to bypass the documented workspace-version validation. It does not migrate config or create a template-suite checkpoint. |

### Logging

| Variable | Model field | Default | Description |
|---|---|---|---|
| `LOG_LEVEL` | `logging.level` | `INFO` | Python log level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |
| `PGMCP_AUDIT_LOG` | `logging.audit_log` | *(logs_dir/mcp_audit.log)* | Override audit log path. Set to empty string to disable. |

### GitHub Integration

| Variable | Model field | Default | Description |
|---|---|---|---|
| `GITHUB_TOKEN` | `github.token` | — | Personal access token or Actions `GITHUB_TOKEN`. |
| `GITHUB_OWNER` | `github.owner` | — | Repository owner (user or organisation). |
| `GITHUB_REPO` | `github.repo` | — | Repository name. |
| `GITHUB_PROJECT_NUMBER` | `github.project_number` | — | GitHub Projects (v2) board number. |

---

## API Reference

### `Settings.from_env()`

Class method. Reads environment variables, applies optional YAML overlay, and returns a validated
`Settings` instance.  Called once at startup by `MCPServer.__init__`.

```python
settings: Settings = Settings.from_env()
```

### `ServerSettings`

| Field | Type | Env var | Default |
|---|---|---|---|
| `name` | `str` | `PGMCP_SERVER_NAME` | `"phase-gate-mcp"` |
| `workspace_root` | `str` | `PGMCP_WORKSPACE_ROOT` | `os.getcwd()` |
| `server_root_dir` | `str` | `PGMCP_SERVER_PROJECT_DIR` | `\".pgmcp\"` |
| `logs_dir` | `str` | `PGMCP_LOGS_DIR` | `"logs"` |
| `config_root` | `str \| None` | `PGMCP_CONFIG_ROOT` | `None` — resolves to `server_root/config` unless overridden. |
| `bypass_version_check` | `bool` | `PGMCP_BYPASS_VERSION_CHECK` | `False` (automatically defaults to `True` during pytest runs) |

### `LogSettings`

| Field | Type | Env var | Default |
|---|---|---|-----------|
| `level` | `str` | `LOG_LEVEL` | `"INFO"` |
| `audit_log` | `str \| None` | `PGMCP_AUDIT_LOG` | `None` (auto-derived) |

When `audit_log` is `None` the server writes to `logs_dir / "mcp_audit.log"`.
Set to an empty string `""` to disable audit logging entirely.

### `GitHubSettings`

| Field | Type | Env var | Required |
|---|---|---|---|
| `owner` | `str` | `GITHUB_OWNER` | Yes |
| `repo` | `str` | `GITHUB_REPO` | Yes |
| `project_number` | `int` | `GITHUB_PROJECT_NUMBER` | Yes |
| `token` | `str \| None` | `GITHUB_TOKEN` | No (public repos) |

---

## YAML Configuration Overlay

Set `PGMCP_CONFIG_PATH` to the path of a YAML file to override any settings field:

```yaml
# .pgmcp/config/server.yaml  (example)
server:
  name: "my-workflow"
  logs_dir: "output/logs"

logging:
  level: "DEBUG"

github:
  owner: "my-org"
  repo: "my-repo"
  project_number: 5
```

Environment variables always take precedence over YAML values.

---

## Checks, tests, and fixes

The server loads check, test, and fix policy from the effective configuration root.
These policies are validated and held as startup configuration; changes take effect
when the MCP server restarts. Tool responses report operation results and may publish
the complete structured result through `pgmcp://cache/runs/{run_id}`. The
`pgmcp://rules/coding_standards` resource describes configured policy, not observed
passes, numbered gates, or a coverage score. There is no `quality.yaml` authority or
QA artifact-log location in this configuration contract.

---

## Usage Examples

### Default setup (minimal)

```bash
export PGMCP_WORKSPACE_ROOT=/repos/myproject
export GITHUB_TOKEN=ghp_...
export GITHUB_OWNER=my-org
export GITHUB_REPO=my-repo
export GITHUB_PROJECT_NUMBER=1
```

Resulting paths:

```
/repos/myproject/
└── .pgmcp/
    ├── config/        (config_root, unless redirected)
    └── logs/
        └── mcp_audit.log (unless redirected)
```

### Custom server directory

```bash
export PGMCP_WORKSPACE_ROOT=/repos/myproject
export PGMCP_SERVER_PROJECT_DIR=.workflow
export PGMCP_LOGS_DIR=output/logs
```

Resulting paths:

```
/repos/myproject/
└── .workflow/
    ├── config/          (unless redirected)
    └── output/logs/
        └── mcp_audit.log (unless redirected)
```

---

## Related Documentation

- [Config Loading Architecture](config-loading-architecture.md) — how `Settings.from_env()` resolves config roots and merges YAML overlays
- [Setup Guide](../setup/README.md) — end-to-end setup walkthrough including GitHub token configuration

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.1 | 2026-07-20 | Agent | Document PGMCP_BYPASS_VERSION_CHECK and bypass_version_check fields |
| 1.0 | 2026-05-11 | Agent | Initial draft |
