# Design: Remove st3 References from MCP Server

**Issue:** #260 | **Status:** approved | **Version:** 1.0
**Reference:** [findings.md](findings.md) (decisions D1–D7)

---

## Problem Statement

The string `st3` appears in 30+ production locations in `mcp_server/`:
state directory name (`.st3/`), URI scheme (`st3://`), server name (`st3-workflow`),
and config path detection logic. These are artefacts of the original project name
`S1mpleTraderV3` and must be replaced before the repo can be renamed to `phase-gate-mcp`.

---

## Decisions (summary — full detail in findings.md)

| ID | Decision |
|----|---------|
| D1 | Product name: **PhaseGate MCP** (`phase-gate-mcp`) |
| D2 | State dir: `.st3/` → `.phase-gate/` |
| D3 | URI scheme: `st3://` → `pgmcp://` |
| D4 | ~~`state_root = config_root.parent`~~ → **`server_root` is primary** (see D4-revised) |
| D4-revised | `server_root = workspace_root / settings.server.server_root_dir` — primary concept; `config_root = server_root / "config"` derived from it. `settings.server.server_root_dir: str = ".phase-gate"` (env: `MCP_SERVER_PROJECT_DIR`). Renamed from `state_root` → `server_root` (see D8); field `state_dir` → `server_root_dir` in C6. |
| D5 | Repo rename deferred to post-issue-#289 |
| D6 | `copilot_orchestration/` stays in MCP server repo |
| D7 | Cycle 1 prereqs already done (dead stubs deleted, template_engine moved) |
| D8 | Internal variable name: `server_root` (not `state_root`). Rationale: the directory contains config, templates, logs, temp, state — not "state" alone. Analogy: `.git/` is not called "state dir". |

---

## Requirements

### Functional

1. All runtime hardcoded `.st3` path strings in `mcp_server/` replaced with injected `server_root`.
2. URI scheme changed from `st3://` to `pgmcp://`.
3. Server default name changed from `st3-workflow` to `phase-gate-mcp` (intermediate `mcp-workflow` in C4; final rename in C7).
4. `normalize_config_root()` must not depend on the `.st3` directory name.
5. `admin_tools` restart marker resolves relative to `server_root`, not CWD.
6. `artifact_manager` temp dir uses `server_root / "temp"`, not CWD.
7. `server_root` is the primary concept; `config_root = server_root / "config"` is always derived from it — the current fragile inversion (`config_root.parent`) is eliminated.

### Non-Functional

1. URI scheme change done atomically (all client-side references in same cycle).
2. `settings.server.server_root_dir: str = ".phase-gate"` (env: `MCP_SERVER_PROJECT_DIR`) is the single configuration point for the server root directory name.
3. All existing tests pass after each cycle.
4. Quality gates (ruff, mypy, pylint) pass after each cycle.

### Future-proofing (Template Workspace Initiative — separate issue)

The `server_root` layout must support the following sub-directories as first-class assets, even if not yet implemented:

```
server_root/
  config/          ← al aanwezig
  templates/       ← toekomstig: workspace-owned Jinja2 templates
  logs/            ← toekomstig: audit + proxy logs
  temp/            ← al in gebruik (ephemeral artifacts)
  state.json       ← al aanwezig
  deliverables.json
  quality_state.json
  template_registry.json
  .restart_marker
```

This layout is the enabler for the Template Workspace Initiative (separate issue),
which adds `templates/` as a workspace-owned override layer and entry_points-based
schema discovery for custom artifact types.

---

## Rationale

**`server_root` is primary, `config_root` is derived** (D4-revised). The previous
design had `config_root` as the entry point and derived `server_root = config_root.parent`.
That design was rejected because:

1. `normalize_config_root()` heuristics depended on the `.st3` directory name, making
   a rename (C5) break the boot path.
2. The `config/` sub-directory was treated as more fundamental than the workspace home,
   which is semantically backwards.
3. Any additional sub-directory (`templates/`, `logs/`) would require new, separate
   configuration — whereas a single `server_root` makes all sub-directories derivable.

**New approach (D4-revised, as implemented):** `server_root = workspace_root / settings.server.server_root_dir`.
`config_root = server_root / "config"` is always derived. `settings.server.server_root_dir`
(env `MCP_SERVER_PROJECT_DIR`, default `.phase-gate`) is the single configuration point.
This approach is implemented in C2 (injection) and C3 (chain inversion).

URI rename is batched in C4 to keep client updates atomic.
Directory rename is last (C5) to minimise test disruption.

---

## Scope

**In scope:** `mcp_server/` production Python, `tests/mcp_server/`, `.phase-gate/config/*.yaml`, `docs/setup/mcp.json`

**Out of scope:** `backend/` production code, GitHub repo rename, `mcp_server/` package rename to `phase_gate_mcp`

---

## Prerequisites

- Cycle 1 completed: dead stubs deleted, `template_engine` moved to `mcp_server/services/`
