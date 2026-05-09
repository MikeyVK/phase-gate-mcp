# Issue #260 — Remove st3 References from MCP Server: Findings

**Branch:** `feature/260-remove-st3-references`
**Phase:** Research
**Date:** 2026-05-09

---

## Problem Statement

The string `st3` is hardcoded throughout the MCP server in directory names (`.st3/`),
URI schemes (`st3://`), server name (`st3-workflow`), and display strings.
This creates coupling to the S1mpleTraderV3 project name, which is unrelated to the
MCP server's function. The `workspace_root` and `config_root` are already resolved
centrally via `Settings` / `resolve_config_root`, but the intermediate state
directory name `.st3` is not configurable.

---

## Goals

1. Map all occurrences of `st3` in production code, tests, and config files.
2. Identify which are structural (directory names, URI schemes) vs cosmetic (comments, strings).
3. Assess cross-cutting dependencies between `backend/` and `mcp_server/`.
4. Assess feasibility of splitting the repo into ST3 backend and MCP workflow server.
5. Define the minimal change set to remove `st3` references from the MCP server.

---

## Scope

**In scope:**
- All `.py` files in `mcp_server/`
- All `.py` files in `tests/mcp_server/` and `tests/backend/`
- Config files in `.st3/config/`
- `docs/setup/mcp.json` setup file
- `pyproject.toml`

**Out of scope:**
- `backend/` production code (no `mcp_server` imports, self-contained)
- Actual repo split (separate Git history operation)

---

## Findings

### F1 — State directory name hardcoded in 10+ production locations

`workspace_root / ".st3" / "<file>"` is constructed inline in:

| File | Lines | Path constructed |
|------|-------|-----------------|
| `mcp_server/server.py` | 146, 196, 250 | `template_registry.json`, `state.json`, `quality_state.json` |
| `mcp_server/managers/phase_state_engine.py` | 90, 458 | `state.json` (self.state_file + git --porcelain arg) |
| `mcp_server/managers/project_manager.py` | 107 | `deliverables.json` |
| `mcp_server/managers/enforcement_runner.py` | 40 | `state.json` (duplicate of PhaseStateEngine) |
| `mcp_server/tools/git_tools.py` | 48 | `state.json` |
| `mcp_server/tools/cycle_tools.py` | 129, 260 | `state.json` (two methods) |
| `mcp_server/managers/artifact_manager.py` | 193, 355, 576 | `template_registry.json`, `.st3/temp` (×2) |
| `mcp_server/tools/admin_tools.py` | 27 | `.restart_marker` (module-level constant, no workspace_root!) |
| `mcp_server/utils/template_config.py` | 45 | `templates/` (CWD-relative, not workspace_root) |
| `mcp_server/scaffolding/template_registry.py` | 35 | `template_registry.json` (default arg) |

**Key insight:** `config_root` is already resolved in `server.py` via `resolve_config_root()`.
`config_root.parent` IS the state root (currently `.st3/`). The derivation exists but is
not used — every callsite recomputes `workspace_root / ".st3"` independently.

**Fix approach:** Add `st3_dir: str = ".st3"` to `ServerSettings` (env: `MCP_ST3_DIR`),
derive `state_root = workspace_root / settings.st3_dir` once in `server.py`,
pass as constructor arg to all managers that need it. Alternatively, derive from
`config_root.parent` — no new setting required.

---

### F2 — URI scheme `st3://` in 3 resource files

| File | URI |
|------|-----|
| `mcp_server/resources/status.py` | `st3://status/phase` |
| `mcp_server/resources/standards.py` | `st3://rules/coding_standards` |
| `mcp_server/resources/github.py` | `st3://github/issues` |
| `mcp_server/validation/markdown_validator.py` | whitelisted as valid scheme |

These URIs are MCP protocol-level identifiers visible to clients.
Changing them is a **breaking change** for any client that hardcodes them (agent.md,
test suite, `mcp.json`-based clients).

**Fix approach:** Rename scheme to `mcp://`. Update all references including
`tests/mcp_server/integration/mcp_server/test_server_startup.py` and
`tests/mcp_server/unit/resources/test_standards.py`.

---

### F3 — Server name `st3-workflow` in settings and mcp.json

| Location | Value |
|----------|-------|
| `mcp_server/config/settings.py` L50 | `name: str = "st3-workflow"` |
| `docs/setup/mcp.json` | `"MCP_SERVER_NAME": "st3-workflow"` |
| `tests/.../test_server_startup.py` L13 | `assert server.server.name == "st3-workflow"` |

**Fix approach:** Change default to `"mcp-workflow"`. Update mcp.json and test.

---

### F4 — `normalize_config_root()` hardcodes `.st3` in detection logic

`mcp_server/config/loader.py` L37–41:
```python
if candidate.name == "config" and candidate.parent.name == ".st3":
    return candidate
if candidate.name == ".st3":
    return candidate / "config"
return candidate / ".st3" / "config"   # ← fallback
```

The function recognizes the config directory by its position relative to `.st3`.
If the directory is renamed, the auto-detection logic breaks.

**Fix approach:** Accept any directory named `config` whose parent contains the
required YAML files, OR derive `state_root` from `config_root.parent` without
name-checking. The fallback line L41 must use the configurable name.

---

### F5 — `admin_tools.py`: restart marker has no workspace_root

```python
RESTART_MARKER_PATH = Path(".st3/.restart_marker")   # module-level, CWD-relative
```

`_get_restart_marker_path()` returns this constant unconditionally. The tool has
no access to `workspace_root` or `Settings`. It will write/read relative to
whatever the CWD is at runtime.

**Fix approach:** Read `MCP_WORKSPACE_ROOT` env var at call time (same pattern as
`resources/standards.py` does), or inject workspace_root via constructor.

---

### F6 — `artifact_manager.py` ephemeral temp dir is CWD-relative

```python
# Lines 355, 576:
temp_dir = Path(".st3/temp")   # ← no workspace_root
```

This is a latent bug independent of naming: the temp path resolves to CWD,
not the workspace root. The named part (`".st3"`) happens to work because the
server is started from the workspace directory.

**Fix approach:** Use `self.workspace_root / ".st3" / "temp"` (already available
as `self.workspace_root`).

---

### F7 — Display strings and comments (cosmetic only)

The following contain `.st3/` as display text in error messages or docstrings:
- `mcp_server/managers/phase_contract_resolver.py` L18–20 (display paths)
- `mcp_server/managers/enforcement_runner.py` L6, 30 (docstring + constant)
- `mcp_server/managers/qa_manager.py` L103, 160 (docstring + error message)
- `mcp_server/tools/project_tools.py` L279–280 (error message)
- `mcp_server/state/quality_state.py` L13 (docstring)
- `mcp_server/managers/quality_state_repository.py` L21 (docstring)

These are cosmetic. They do not affect behavior but should be updated for consistency.

---

### F8 — Config YAML files contain `.st3/` literal paths

`contracts.yaml` registers branch-local artifacts by path:
```yaml
branch_local_artifacts:
  - path: .st3/state.json
  - path: .st3/deliverables.json
  - path: .st3/quality_state.json
```

`project_structure.yaml` has a `.st3:` directory entry with policy rules.
`workflows.yaml` references `phase_source: ".st3/config/workphases.yaml"`.

These must be updated in sync with any directory rename — they are data files,
not code, but they drive runtime behavior.

---

### F9 — Repo split feasibility

**Result: clean split is possible with 3 file changes.**

| Dependency direction | Status |
|---------------------|--------|
| `backend/` → `mcp_server/` (production) | **NONE** |
| `mcp_server/` → `backend/` (production) | **NONE** |
| `tests/backend/` → `mcp_server/` (Python import) | **NONE** |
| `tests/mcp_server/` → `backend/` (Python import) | **NONE** |
| `tests/backend/services/test_template_engine.py` → `mcp_server/scaffolding/templates/` | Path string fixture (not import) |

**Blockers for split (minimal):**
1. `backend/core/scope_encoder.py` + `backend/core/phase_detection.py` — dead stubs,
   raise `ImportError`, can be deleted.
2. `backend/services/template_engine.py` — Jinja2 wrapper used only by MCP server.
   Tests point to MCP template dir. Move to `mcp_server/` on split.
3. `pyproject.toml` — bundles `backend*` and `mcp_server*` in one package. Split into two.

**Recommendation:** Repo split is deferred to post-issue-#289 (installable wheel).
This issue (#260) only removes `st3` string references from the MCP server codebase.

---

## Open Questions

1. **Directory name:** What replaces `.st3/`? Options: `.mcp`, `.workflow`, `.copilot`
2. **Server name:** What replaces `st3-workflow`? Options: `mcp-workflow`, `workflow-server`
3. **URI scheme:** What replaces `st3://`? Breaking change for clients.
4. **Derive from config_root.parent or add new Setting?** See F1 fix approach.

---

## Minimal Change Set (implementation scope)

### Structural changes (behavior-affecting):

| # | Change | Files |
|---|--------|-------|
| S1 | Add `MCP_ST3_DIR` setting, derive `state_root` in `server.py` | `settings.py`, `server.py` |
| S2 | Pass `state_root` to managers (replace all inline `.st3` path construction) | 8 production files |
| S3 | Fix `normalize_config_root()` fallback to use configurable name | `config/loader.py` |
| S4 | Fix `admin_tools.py` marker path to be workspace-aware | `tools/admin_tools.py` |
| S5 | Fix `artifact_manager.py` ephemeral temp to use `self.workspace_root` | `managers/artifact_manager.py` |
| S6 | Rename `st3://` URI scheme | 3 resource files + validator + 4 test files |
| S7 | Rename server default name | `settings.py` + `mcp.json` + 1 test file |
| S8 | Update `contracts.yaml`, `project_structure.yaml`, `workflows.yaml` | 3 YAML files |

### Cosmetic changes (comments/docstrings):

| # | Change | Files |
|---|--------|-------|
| C1 | Update display strings in managers | 6 files |
| C2 | Update test variable names (`st3_dir`) | 3 test files |
