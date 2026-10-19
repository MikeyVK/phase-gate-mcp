<!-- docs\reference\mcp\server-configuration.md -->
<!-- template=reference version=064954ea created=2026-05-11T14:28Z updated=2026-05-11T14:28Z -->
# MCP Server — User-Facing Configuration


**Status:** DEFINITIVE
**Version:** 1.4
**Last Updated:** 2026-10-18

**Sources:** [launcher settings](../../mcp_server/config/settings.py), [ConfigLoader](../../mcp_server/config/loader.py) and [startup policy schema](../../mcp_server/config/schemas/server_config.py)
**Tests:** [tests/mcp_server/unit/config/test_settings.py](../../tests/mcp_server/unit/config/test_settings.py)

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

ConfigLoader composes defaults/github.yaml and optional root github.yaml. Identity and optional project metadata come only from this source. Bootstrap prefers a nonempty GITHUB_TOKEN over an explicit configured token. The launcher Settings has no GitHub section. See the [composition contract](config-loading-architecture.md).

---

## Startup admission policy

[ConfigLoader.load_server_config()](../../mcp_server/config/loader.py) composes
required `config_root/defaults/server.yaml` with optional
`config_root/server.yaml`, using the ordinary [composition contract](config-loading-architecture.md).
[ServerConfig](../../mcp_server/config/schemas/server_config.py) is the authoritative
closed, immutable schema. The complete basis has `version: "1.0.0"` and all fields below.

| Field | Distributed basis | Meaning |
| --- | --- | --- |
| `startup_lock.max_wait_seconds` | 30 | Maximum retry budget for ordinary startup lock contention. |
| `startup_lock.retry_interval_seconds` | 0.25 | Interval between failed native lock attempts, bounded by remaining budget. |
| `proxy.initialization_timeout_seconds` | 60 | Proxy deadline for completing the child initialize handshake. |

The first lock attempt is immediate and startup continues as soon as it acquires
the lock. All timings must be finite, positive numbers; booleans and numeric strings
are rejected. The retry interval cannot exceed the wait budget, and the proxy
deadline must exceed that budget. These bounds do not guarantee total startup latency.

For example, an optional workspace override can change just the wait budget:

```yaml
startup_lock:
  max_wait_seconds: 40
```

The proxy and child independently read this policy through the existing loader.
Only the policy is read before the child's source-admission lock; template and adapter
admission remain inside that lock. Launcher Settings still selects roots and logging.
`PGMCP_CONFIG_PATH` is a launcher overlay, not the source of these timing fields.

Fresh `--init` installs the packaged basis through the existing assets route.
Existing workspaces must explicitly install/reconcile the new required basis and
any override before normal startup. `--upgrade` renews templates and does not install
this configuration. If an existing `config_root/server.yaml` contains a launcher
overlay with `server:` or `logging:`, move that owner-managed overlay to a distinct
file and update `PGMCP_CONFIG_PATH`; the root `server.yaml` now has the startup-policy shape.

A missing/invalid policy is an admission error with its source diagnosis. If the
proxy cannot read it, no child is launched and no MCP recovery endpoint is promised.
Applying coordinated policy edits requires a full proxy/child relaunch:
`restart_server` replaces only the child and retains the proxy's current deadline.
See [proxy timing and recovery](proxy_restart.md).

---

## API Reference

### `Settings.from_env()`

Class method. Reads environment variables, applies optional YAML overlay, and returns a validated
`Settings` instance. Composition entrypoints use it to resolve launcher settings;
startup timing policy is subsequently read by `ConfigLoader.load_server_config()`.

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

This immutable resolved value is shared by GitHub consumers and is not a member of launcher Settings.

| Field | Type | Source | Requirement |
| --- | --- | --- | --- |
| owner | str or null | github.yaml | Required for GitHub operations |
| repo | str or null | github.yaml | Required for GitHub operations |
| project_number | int or null | github.yaml | Optional |
| token | str or null | Nonempty GITHUB_TOKEN, otherwise configured token | Required by token-dependent operations |

Neutral values permit startup/health; existing registration, use-time and enforcement policy still applies.

---

## YAML Configuration Overlay

Set `PGMCP_CONFIG_PATH` to the path of a YAML file to override server or logging settings:

```yaml
# .pgmcp/launcher-settings.yaml (explicit PGMCP_CONFIG_PATH example)
server:
  name: "my-workflow"
  logs_dir: "output/logs"

logging:
  level: "DEBUG"
```

Supported server/logging environment variables take precedence over this launcher overlay. Workspace declarations use the separate [defaults/root composition](config-loading-architecture.md).

---

## Checks, tests, and fixes

The server loads check, test, and fix policy from the effective configuration root.
These policies are validated and held as startup configuration; changes take effect
when the MCP server restarts. Tool responses report operation results and may publish
the complete structured result through `pgmcp://cache/runs/{run_id}`. The
`pgmcp://rules/coding_standards` resource describes configured policy, not observed
passes, numbered gates, or a coverage score. There is no `quality.yaml` authority or
QA artifact-log location in this configuration contract.

### Branch-check target policies

`checks.yaml` requires a `configured_targets` map. Each named set has a nonempty
`include` list and a required `exclude` list (which may be empty). Selection-capable
adapter check declarations name one set through their required `configured_targets`
reference. A content-only workspace can declare an empty map; content-only capabilities
must omit the reference. Mixed content/selection capabilities require it. At startup,
the server resolves every configured selection binding's reference, including bindings
outside the default profile; no fallback policy or native-config import is supplied.

Example fragments for the bundled production type-check policy:

```yaml
# checks.yaml: workspace-owned values
configured_targets:
  python_production_sources:
    include: ["mcp_server/**/*.py", "mcp_server/**/*.pyi"]
    exclude: ["**/__pycache__/**", "**/.pytest_cache*/**"]
```

```yaml
# mypy/manifest.yaml: reusable check-capability declaration
roles:
  check:
    capabilities:
      types:
        inputs: [selection]
        configured_targets: python_production_sources
```

Patterns match the complete workspace-relative POSIX path, case-sensitively on every
host. Ordinary characters, Unicode and whitespace are literal. `*` matches zero or
more characters within one component, `?` exactly one, and `**` matches zero or more
whole components. Any include must match and any matching exclude wins. Duplicate or
empty patterns, absolute paths, backslashes, empty/dot/parent components, character
classes/braces and embedded `**` are rejected. The filter preserves resolved candidate
order and does not enumerate the filesystem. Uniqueness is checked within each list;
control characters are rejected.

Only `run_checks(scope="branch")` applies these values to each check's Git candidates.
Configured/workspace/explicit targets and content requests retain their existing
meanings, as do test and fix operations. Native tools still interpret their own
configuration and arguments; these policies neither synchronize native defaults nor
override native exclusions. Owners maintain the branch policy appropriate to each
check. See [selection and no-applicable outcomes](tools/quality.md#run_checks).

This is a clean break: old selection declarations must add the required reference and
workspaces must declare the map before admission. Ruff, Mypy, Pyright and Lychee bundled
packages are 2.0.0; their native pins and role wire contract remain unchanged. There is
no automatic legacy migration. Policies and package declarations are admitted at
startup; restart after changing them.

Sources: [ChecksConfig](../../mcp_server/config/schemas/checks_config.py),
[CheckCapability](../../mcp_server/config/schemas/adapter_manifest.py),
[startup reference validation](../../mcp_server/config/validator.py) and
[generic matcher](../../mcp_server/execution/configured_targets.py).

---

## Usage Examples

### Default setup (minimal)

```bash
export PGMCP_WORKSPACE_ROOT=/repos/myproject
export GITHUB_TOKEN=ghp_...
# Configure owner/repo/project_number in .pgmcp/config/github.yaml instead.
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

## Quality binding acknowledgement

Workspace checks.yaml, tests.yaml and fixes.yaml bindings carry configuration_choice:
null/omitted is unresolved; native_discovery, configured_arguments and not_applicable
are deliberate owner declarations. Startup accepts unresolved choices, but relevant
execution requires acknowledgement. These declarations do not identify or verify the
effective native config source. Base choices are null; --init preserves choices in
supplied assets. Record reviewed choices in root workspace overrides; existing roots
remain owner-managed. Follow the [central quality setup guide](../setup/README.md#choose-the-workspace-quality-policy)
and [execution outcomes](tools/quality.md#deliberate-binding-setup).

## Related Documentation

- [Config Loading Architecture](config-loading-architecture.md) — how `Settings.from_env()` resolves config roots and merges YAML overlays
- [Setup Guide](../setup/README.md) — end-to-end setup walkthrough including GitHub token configuration

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.1 | 2026-07-20 | Agent | Document PGMCP_BYPASS_VERSION_CHECK and bypass_version_check fields |
| 1.0 | 2026-05-11 | Agent | Initial draft |
| 1.2 | 2026-10-07 | @imp documenter | Document required branch-policy declarations, matching semantics, scope boundaries and clean-break admission. |
| 1.3 | 2026-10-16 | @imp documenter | Document source layering, GitHub separation and preserved initialization choices. |
| 1.4 | 2026-10-18 | @imp documenter | Document composed startup admission policy, explicit migration and proxy relaunch boundary for #520. |
