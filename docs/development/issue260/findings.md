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

## Decisions (2026-05-10)

All open questions are resolved. These decisions are final for this issue.

### D1 — Server product name: **PhaseGate MCP**

The server will be named **PhaseGate MCP** (`phase-gate-mcp`).

| Context | Convention | Value |
|---------|-----------|-------|
| GitHub repo name | kebab-case | `phase-gate-mcp` |
| `MCP_SERVER_NAME` env var / `mcp.json` | kebab-case | `phase-gate-mcp` |
| Python package/module directory | snake_case | `phase_gate_mcp` (future, post-split) |
| Class/type names in code | PascalCase | `PhaseGateMCP` |
| Hidden state directory on disk | kebab | `.phase-gate` |
| MCP resource URI scheme | short lowercase | `pgmcp://` |

**Work name** (used until official rename): `mcp-workflow`.
The work name is the default in `settings.py` and `mcp.json`.
Switching to the product name requires changing exactly two values:
`ServerSettings.name` default and `MCP_SERVER_NAME` in `mcp.json`.
No code changes needed beyond those two.

### D2 — State directory rename: `.st3/` → `.phase-gate/`

The hidden workspace directory is renamed from `.st3/` to `.phase-gate/`.
`MCP_CONFIG_ROOT` in `mcp.json` updated from
`${workspaceFolder}/.st3/config` to `${workspaceFolder}/.phase-gate/config`.

### D3 — URI scheme: `st3://` → `pgmcp://`

All MCP resource URIs change scheme from `st3://` to `pgmcp://`.
This is a breaking change for existing clients (agent.md, mcp.json consumers).
All references updated in this issue.

### D4 — State root derivation: use `config_root.parent`

No new `ServerSettings` field is added.
`state_root` is derived as `config_root.parent` in `server.py` once after
`resolve_config_root()` returns. This is passed to all managers as a constructor
argument, replacing all inline `workspace_root / ".st3"` constructions.
Rationale: `MCP_CONFIG_ROOT` already encodes the config path; `config_root.parent`
is always the state root without requiring a second env var.

### D5 — Repo split strategy: rename current repo, extract backend

The current `S1mpleTraderV3` repo on GitHub is renamed to `phase-gate-mcp`.
A new empty `S1mpleTraderV3` repo is created and the `backend/` directory is
pushed there. This preserves the full MCP server git history (the valuable part)
and avoids a complex `git filter-repo` operation.
Timing: deferred to post-issue-#289 (installable wheel), except the prereqs
already completed in Cycle 1 of this issue.

### D6 — `copilot_orchestration/` stays in MCP server repo

`src/copilot_orchestration/` has no production imports from either `backend/`
or `mcp_server/`. It remains in the current repo and travels with the MCP server
on split.

### D7 — Cycle 1 already completed (2026-05-09)

The following prereqs for the split were resolved in Cycle 1:
- `backend/core/scope_encoder.py` deleted (dead stub)
- `backend/core/phase_detection.py` deleted (dead stub)
- `backend/services/template_engine.py` moved to `mcp_server/services/template_engine.py`
- `tests/backend/services/test_template_engine.py` moved to
  `tests/mcp_server/unit/services/test_template_engine.py`, import updated

---

## Findings (session 2026-05-10 — C2 implementation analysis)

### F8 — `state_root` variable name is misleading

The internal variable `state_root` was introduced in C2 to inject the `.st3/`
directory path. The name implies "state storage" but the directory contains
config, templates (future), logs, temp, state, deliverables — the **complete
operational home** of the MCP server within a workspace.

**Decision (D8):** Rename to `server_root` throughout all modified files.
Rationale: analogous to `.git/` — not called "state dir" despite containing state.

---

### F9 — Chain inversion required: `server_root` must be primary

Current derivation (fragile):
```
workspace_root → resolve_config_root() → config_root → config_root.parent → server_root
```

Problem: `resolve_config_root()` uses heuristics that depend on the `.st3` directory
name. If the name changes, the heuristic in `normalize_config_root()` breaks.
`server_root` being derived from `config_root.parent` means the primary concept
is the sub-directory (`config/`), not the root — this is backwards.

**Decision (D4-revised):** Invert the chain:
```
workspace_root + settings.state_dir → server_root (PRIMARY)
server_root / "config" → config_root (DERIVED)
```

Add `state_dir: str = ".st3"` (env: `MCP_STATE_DIR`) to `ServerSettings`.
This makes `server_root` the single configured concept; `config_root` is always
`server_root / "config"`. The fragile `normalize_config_root()` heuristic is
no longer needed for the main boot path.

---

### F10 — Manager constructor fallbacks still hardcode `.st3`

After C2, all managers accept `server_root` (then `state_root`) via constructor.
BUT: all fallbacks were left in place:
```python
self.state_root = state_root if state_root is not None else workspace_root / ".st3"
```

These fallbacks mean the `.st3` hardcoding is still present in production code.
QA NOGO finding: silent fallback defeats the purpose of injection.

**Affected files:** `phase_state_engine.py`, `project_manager.py`,
`enforcement_runner.py`, `tools/phase_tools.py`, `artifact_manager.py`.

**Fix (C2 blocker):** Remove `Optional` from `server_root` param — make it required —
or raise `ValueError("server_root must be provided")` if None is passed.
The fallback must be eliminated entirely, not just bypassed in `server.py`.

---

### F11 — Template Workspace Initiative (future issue)

The three-part trinity (Pydantic context schemas + Jinja2 templates + artifacts.yaml)
must not be split. Today all three live in the wheel, which means they cannot be
customized without modifying source code.

Future capability:
- **Jinja2 templates** → workspace-owned in `server_root/templates/`, copied from
  bundled via `init_templates` command
- **Pydantic context schemas** → bundled base in wheel; external packs via
  `entry_points("phase_gate.schemas")` (plugin architecture)
- **artifacts.yaml** → merged from bundled + workspace-local overrides
- Optional web UI: local HTTP server on `localhost:7890`, same tool logic exposed as REST

**Prerequisite:** chain inversion (C3) must be complete before this initiative starts.
Reason: templates are workspace-owned content under `server_root/templates/`; the
Template Workspace Initiative only makes sense when `server_root` is the primary,
runtime-configurable concept.

**Action:** Defer to a separate issue post-C3.

---

### F12 — Two hardcoded log paths outside server_root injection scope

Two log paths are not covered by the C2 injection pattern:

| File | Line | Hardcoded path | Problem |
|------|------|----------------|---------|
| `mcp_server/core/proxy.py` | L141 | `Path("mcp_server/logs")` | CWD-relative; not in server_root |
| `mcp_server/managers/qa_manager.py` | L60 | `Path("temp/qa_logs")` | CWD-relative; not in server_root |

These should use `server_root / "logs"` and `server_root / "temp" / "qa_logs"`
respectively. However, fixing these requires the proxy and QA manager to receive
`server_root` — which is a separate injection chain from the current C2 scope.

**Action:** Defer to a separate issue. Note that the Template Workspace Initiative
(F11) and the log path fix (F12) can be combined in the same issue once C3 is done.

---

## Minimal Change Set (implementation scope)

### Structural changes (behavior-affecting):

| # | Change | Files | Cycle |
|---|--------|-------|-------|
| S1 | Derive `server_root = config_root.parent` in `server.py`; pass to managers (temporary; C3 inverts) | `server.py` | C2 |
| S2 | Replace all inline `workspace_root / ".st3"` with injected `server_root`; **rename `state_root` → `server_root` in all modified files** (C2, not C3) | 8 production files | C2 |
| S3 | Remove manager constructor fallbacks entirely (make `server_root` required — no `Optional`, no `.st3` default) | 5 manager/tool files | C2 |
| S4 | Fix `admin_tools.py`: inject `server_root` from `server.py`; `_get_restart_marker_path()` uses `server_root / ".restart_marker"` — remove `MCP_WORKSPACE_ROOT` env lookup | `tools/admin_tools.py` | C2 |
| S5 | Fix `artifact_manager.py` ephemeral temp: use `server_root / "temp"` | `managers/artifact_manager.py` | C2 |
| S6 | Fix `loader.py` bootstrap fallback: remove `.st3` from final fallback branch | `config/loader.py` | C2 |
| S7 | Add `state_dir: str = ".st3"` to `ServerSettings` (env: `MCP_STATE_DIR`) | `config/settings.py` | C3 |
| S8 | Chain inversion: `server_root = workspace_root / settings.state_dir`; `config_root = server_root / "config"` | `server.py` | C3 |
| S9 | Rewrite `normalize_config_root()`: remove heuristics, no `.st3` name-check | `config/loader.py` | C3 |
| S10 | Rename `st3://` → `pgmcp://` URI scheme | 3 resource files + validator + test files | C4 |
| S11 | Rename server default name `st3-workflow` → `mcp-workflow` | `settings.py` + `mcp.json` + test file | C4 |
| S12 | Rename `.st3/` → `.phase-gate/` on disk + all YAML config files | `contracts.yaml`, `project_structure.yaml`, `workflows.yaml` + disk | C5 |

### Cosmetic changes (comments/docstrings):

| # | Change | Files | Cycle |
|---|--------|-------|-------|
| CS1 | Update display strings in managers | 6 files | C5 |
| CS2 | Update test variable names (`st3_dir`) | 3 test files | C5 |

---

## Findings (session 2026-05-xx — post-C5 observations)

### F13 — `ServerSettings.state_dir` field name conflicts with internal naming convention

C3 added `state_dir: str = ".phase-gate"` to `ServerSettings`. The name `state_dir`
implies "directory for state files" but the directory IS the **server root** — not
just for state. Decisions D8 / D4-revised established that internally only the term
`server_root` should be used. The field name `state_dir` leaks a different concept.

Additional issues uncovered:
1. `mcp_server/resources/standards.py` (L19–21) re-derives the path via
   `os.environ.get("MCP_STATE_DIR")` instead of using `Settings.from_env()`. This
   duplicates the env-to-settings mapping and will silently diverge if the mapping
   ever changes.
2. Three error messages still reference `settings.state_dir` (stale after C3):
   - `mcp_server/managers/artifact_manager.py` L127
   - `mcp_server/managers/enforcement_runner.py` L163
   - `mcp_server/tools/phase_tools.py` L83

**Fix:** Rename `ServerSettings.state_dir` → `server_root_dir`. The env var
`MCP_STATE_DIR` stays unchanged (backward compat). Fix `standards.py` to use
`Settings.from_env()`. Fix the three stale error messages.

---

### F14 — `PhaseStateEngine.state_file` attribute name violates Python convention

`self.state_file` in `PhaseStateEngine` is a `Path` pointing to `state.json`.
Using the suffix `_file` for a `Path` object (rather than a file handle)
violates Python convention (`_path` is standard). There are also multiple state
files in `server_root` (`state.json`, `deliverables.json`, `quality_state.json`),
making the unqualified name `state_file` ambiguous.

External test access confirmed: `engine.state_file` is asserted in
`tests/mcp_server/unit/test_c260_c2_state_root_injection.py` (lines 111, 120).

**Fix:** Rename `self.state_file` → `self.state_path` in `phase_state_engine.py`.
Update the two test assertions.

---

### S13–S16 additions to Minimal Change Set

| # | Change | Files | Cycle |
|---|--------|-------|-------|
| S13 | Rename `ServerSettings.state_dir` → `server_root_dir` (env var `MCP_STATE_DIR` unchanged) | `config/settings.py`, `server.py`, `config/loader.py` (docstring) | C6 |
| S14 | Fix `standards.py` duplicate path derivation → use `Settings.from_env()` | `resources/standards.py` | C6 |
| S15 | Fix 3 stale error messages referencing `settings.state_dir` | `managers/artifact_manager.py`, `managers/enforcement_runner.py`, `tools/phase_tools.py` | C6 |
| S16 | Rename `PhaseStateEngine.state_file` → `state_path` | `managers/phase_state_engine.py`, 2 test files | C6 |
