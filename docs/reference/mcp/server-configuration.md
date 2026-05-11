<!-- docs\reference\mcp\server-configuration.md -->
<!-- template=reference version=064954ea created=2026-05-11T14:28Z updated=2026-05-11T14:28Z -->
# MCP Server — User-Facing Configuration


**Status:** DEFINITIVE
**Version:** 1.0
**Last Updated:** 2026-05-11

**Source:** [mcp_server/config/settings.py](../../../mcp_server/config/settings.py)
**Tests:** [tests/mcp_server/unit/config/test_settings.py](../../../tests/mcp_server/unit/config/test_settings.py) (12 tests)

---

## Overview

The MCP server derives **all file-system paths** from a single root (`MCP_WORKSPACE_ROOT`).  
Paths are composed at startup by `Settings.from_env()` — no hard-coded locations exist in the
server code.  Override any segment via environment variable; use a YAML overlay for bulk
configuration.

---
## Path Derivation Chain

```
MCP_WORKSPACE_ROOT          (default: cwd)
└── MCP_SERVER_PROJECT_DIR  (default: .phase-gate)    → server_root
    ├── config/                                        → config_root  (always server_root/config)
    └── MCP_LOGS_DIR        (default: logs)            → logs_dir
        ├── mcp_audit.log                              → audit log    (LOG_LEVEL controls verbosity)
        └── qa_logs/                                   → QA artifact logs (gate failures only)
```

| Path segment | Environment variable | Default |
|---|---|---|
| `workspace_root` | `MCP_WORKSPACE_ROOT` | `os.getcwd()` |
| `server_root` | `MCP_SERVER_PROJECT_DIR` | `.phase-gate` |
| `logs_dir` | `MCP_LOGS_DIR` | `logs` |

---

## Environment Variables

### Server

| Variable | Model field | Default | Description |
|---|---|---|---|
| `MCP_WORKSPACE_ROOT` | `server.workspace_root` | `os.getcwd()` | Repository root. All relative paths resolve from here. |
| `MCP_SERVER_PROJECT_DIR` | `server.server_root_dir` | `.phase-gate` | Sub-directory under workspace_root for all server data. |
| `MCP_LOGS_DIR` | `server.logs_dir` | `logs` | Sub-directory under server_root for log files. |
| `MCP_SERVER_NAME` | `server.name` | `phase-gate-mcp` | Server identifier shown in logs and API responses. |

### Logging

| Variable | Model field | Default | Description |
|---|---|---|---|
| `LOG_LEVEL` | `logging.level` | `INFO` | Python log level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |
| `MCP_AUDIT_LOG` | `logging.audit_log` | *(logs_dir/mcp_audit.log)* | Override audit log path. Set to empty string to disable. |

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
| `name` | `str` | `MCP_SERVER_NAME` | `"phase-gate-mcp"` |
| `workspace_root` | `str` | `MCP_WORKSPACE_ROOT` | `os.getcwd()` |
| `server_root_dir` | `str` | `MCP_SERVER_PROJECT_DIR` | `".phase-gate"` |
| `logs_dir` | `str` | `MCP_LOGS_DIR` | `"logs"` |
| `config_root` | `str \| None` | `MCP_CONFIG_ROOT` | `None` — **dead field; not used by `server.py`.** Kept in `settings.py` for backward compat only. |

### `LogSettings`

| Field | Type | Env var | Default |
|---|---|---|-----------|
| `level` | `str` | `LOG_LEVEL` | `"INFO"` |
| `audit_log` | `str \| None` | `MCP_AUDIT_LOG` | `None` (auto-derived) |

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

Set `MCP_CONFIG_PATH` to the path of a YAML file to override any settings field:

```yaml
# .phase-gate/config/server.yaml  (example)
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

## Quality Gate Artifact Logs

The QA manager writes artifact logs **only on gate failure**.  Location:

```
logs_dir / "qa_logs" / <timestamp>_<gate_name>.log
```

By default this resolves to `.phase-gate/logs/qa_logs/`.

To override, add `output_dir` to `.phase-gate/config/quality.yaml`:

```yaml
artifact_logging:
  enabled: true
  max_files: 200
  output_dir: "custom/qa_logs"   # relative to workspace_root
```

---

## Usage Examples

### Default setup (minimal)

```bash
export MCP_WORKSPACE_ROOT=/repos/myproject
export GITHUB_TOKEN=ghp_...
export GITHUB_OWNER=my-org
export GITHUB_REPO=my-repo
export GITHUB_PROJECT_NUMBER=1
```

Resulting paths:

```
/repos/myproject/
└── .phase-gate/
    ├── config/        (config_root)
    └── logs/
        ├── mcp_audit.log
        └── qa_logs/   (written only on gate failure)
```

### Custom server directory

```bash
export MCP_WORKSPACE_ROOT=/repos/myproject
export MCP_SERVER_PROJECT_DIR=.workflow
export MCP_LOGS_DIR=output/logs
```

Resulting paths:

```
/repos/myproject/
└── .workflow/
    ├── config/
    └── output/logs/
        ├── mcp_audit.log
        └── qa_logs/
```

---

## Related Documentation

- [Config Loading Architecture](config-loading-architecture.md) — how `Settings.from_env()` resolves config roots and merges YAML overlays
- [USER_GUIDE](../../mcp_server/USER_GUIDE.md) — end-to-end setup walkthrough including GitHub token configuration

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-11 | Agent | Initial draft |
