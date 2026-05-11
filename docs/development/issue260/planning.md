# Planning: Remove st3 References from MCP Server

**Issue:** #260 | **Branch:** `feature/260-remove-st3-references`
**Reference:** [findings.md](findings.md) · [design.md](design.md)

---

## Cycle Overview

| Cycle | Scope | Type | Status |
|-------|-------|------|--------|
| C1 | Delete dead stubs, move template_engine | Structural | ✅ Done (commit `fccfe74`) |
| C2 | `server_root` injection — eliminate inline `.st3` path construction + manager fallbacks | Structural | ✅ Done |
| C3 | Chain inversion — `server_root` primary, `settings.server_root_dir` added, `config_root` derived | Structural | ✅ Done |
| C4 | URI scheme + server name rename (`st3://` → `pgmcp://`, `st3-workflow` → `mcp-workflow`) | Breaking | ✅ Done (commit `6df9847f`) |
| C5 | Directory rename `.st3/` → `.phase-gate/` + YAML config + cosmetics | Rename | ✅ Done (commits `13ab7425`, `35df0b24`, `b17a7d29`) |
| C6 | Naming cleanup: `state_dir` → `server_root_dir`; fix `standards.py` duplication; fix stale error messages; rename `state_file` → `state_path` | Cleanup | ✅ Done (commit `bf213c09`) |
| Post-C6 | Log centralization: `logs_dir` setting, audit_log under `server_root/logs/`, F12 resolved, `MCP_STATE_DIR` → `MCP_SERVER_PROJECT_DIR` | Extras | ✅ Done (2026-05-11) |

### Scope

Replace all inline `workspace_root / ".st3"` constructions with injected `server_root`.
**C2 does NOT yet invert the chain** (that is C3). C2 uses `state_root = config_root.parent`
as temporary derivation and renames it `server_root` in all callsites.

**C2 blocker (QA NOGO ×2):** Constructor fallbacks `workspace_root / ".st3"` must be
eliminated entirely — not just bypassed by injection in server.py. If a manager is
constructed without `server_root`, it must not silently fall back to `.st3`.
Fix: make `server_root` a required parameter (no default `None`) or raise explicitly.

### Files changed

| File | Change |
|------|--------|
| `mcp_server/server.py` | Derive `server_root = config_root.parent` (temporary; C3 inverts this), pass to managers |
| `mcp_server/managers/phase_state_engine.py` | Accept `server_root` via constructor (required, no fallback), replace L90, L458 |
| `mcp_server/managers/project_manager.py` | Accept `server_root` (required, no fallback), replace L107 |
| `mcp_server/managers/enforcement_runner.py` | Accept `server_root` (required, no fallback), replace L40 |
| `mcp_server/tools/git_tools.py` | Accept `server_root` (required, no fallback), replace L48 |
| `mcp_server/tools/cycle_tools.py` | Accept `server_root` (required, no fallback), replace L129, L260 |
| `mcp_server/managers/artifact_manager.py` | Accept `server_root` (required, no fallback), replace L193, L355, L576 |
| `mcp_server/tools/admin_tools.py` | Receive `server_root` injected from server.py; `_get_restart_marker_path()` uses `server_root / ".restart_marker"` — no `MCP_WORKSPACE_ROOT` env lookup |
| `mcp_server/utils/template_config.py` | Use `server_root / "templates"` instead of CWD-relative path, L45 |
| `mcp_server/scaffolding/template_registry.py` | Replace default arg `Path(".st3/...")` with explicit `server_root`-based path, L35 |
| `mcp_server/config/loader.py` | Fix `normalize_config_root()` fallback (L41): remove `.st3` name-check; final fallback must not hardcode `.st3` |

### Test files affected

| File | Change |
|------|--------|
| `tests/mcp_server/unit/managers/test_phase_state_engine.py` | Update constructor call with `server_root` |
| `tests/mcp_server/unit/managers/test_project_manager.py` | Update constructor call |
| `tests/mcp_server/unit/managers/test_enforcement_runner.py` | Update constructor call |
| `tests/mcp_server/unit/tools/test_git_tools.py` | Update constructor call |
| `tests/mcp_server/unit/tools/test_cycle_tools.py` | Update constructor call |
| `tests/mcp_server/unit/managers/test_artifact_manager.py` | Update constructor call |
| `tests/mcp_server/unit/tools/test_admin_tools.py` | Remove `MCP_WORKSPACE_ROOT` mock; inject `server_root` instead |

### Exit criteria

- [ ] `grep -r '\.st3' mcp_server/ --include='*.py'` returns zero hits (excluding comments)
- [ ] `grep -r '\bstate_root\b' mcp_server/ --include='*.py'` returns zero hits (renamed to `server_root` in C2)
- [ ] No manager constructor has a `workspace_root / ".st3"` fallback
- [ ] `run_tests(path="tests/mcp_server/")` — all tests pass
- [ ] `run_quality_gates(scope="branch")` — 0 errors

---

## Cycle 3 — Chain Inversion + `settings.state_dir`

### Scope

Invert the `config_root → server_root` derivation chain. Currently `server_root` is
derived from `config_root.parent` (fragile). After C3, `server_root` is the primary
concept derived directly from `workspace_root` and a new `settings.state_dir` field.
`config_root` is always `server_root / "config"` — no longer the entry point.

This is the enabler for the Template Workspace Initiative: once `server_root` is
primary and configured via `settings.state_dir`, the directory name is runtime-
configurable and the full sub-directory layout (`templates/`, `logs/`, `temp/`) can
be built on top without touching the wheel.

### Changes

| File | Change |
|------|--------|
| `mcp_server/config/settings.py` | Add `state_dir: str = ".st3"` (env: `MCP_STATE_DIR`) |
| `mcp_server/server.py` | `server_root = workspace_root / settings.state_dir`; `config_root = server_root / "config"`; remove `resolve_config_root()` call or replace with new derivation |
| `mcp_server/config/loader.py` | `normalize_config_root()` rewritten: input is always `server_root / "config"`, no heuristic needed |
| `MCP_CONFIG_ROOT` env var | Keep for backward compat but mark deprecated; derive `server_root` from `MCP_STATE_DIR` + `MCP_WORKSPACE_ROOT` instead |

### Exit criteria

- [ ] `server_root = workspace_root / settings.state_dir` — no `config_root.parent` derivation anywhere
- [ ] `normalize_config_root()` no longer contains heuristics or `.st3` references
- [ ] `run_tests(path="tests/mcp_server/")` — all tests pass
- [ ] `run_quality_gates(scope="branch")` — 0 errors

---

## Cycle 4 — URI Scheme + Server Name Rename

### Scope

Atomic rename of `st3://` → `pgmcp://` and `st3-workflow` → `mcp-workflow`.
All client references updated in the same commit.

### Files changed

| File | Change |
|------|--------|
| `mcp_server/resources/status.py` | `st3://status/phase` → `pgmcp://status/phase` |
| `mcp_server/resources/standards.py` | `st3://rules/coding_standards` → `pgmcp://rules/coding_standards` |
| `mcp_server/resources/github.py` | `st3://github/issues` → `pgmcp://github/issues` |
| `mcp_server/validation/markdown_validator.py` | `"st3:"` → `"pgmcp:"` in whitelist |
| `mcp_server/config/settings.py` | `name: str = "st3-workflow"` → `"mcp-workflow"` |
| `docs/setup/mcp.json` | `MCP_SERVER_NAME: "st3-workflow"` → `"mcp-workflow"` |
| `agent.md` | All `st3://` URI references → `pgmcp://` |
| `.github/.copilot-instructions.md` | All `st3://` URI references → `pgmcp://` |

### Test files affected

| File | Change |
|------|--------|
| `tests/mcp_server/integration/mcp_server/test_server_startup.py` | Assert `"mcp-workflow"` instead of `"st3-workflow"` |
| `tests/mcp_server/unit/resources/test_standards.py` | Update URI assertions |
| Any other test asserting `st3://` URIs | Update URI assertions |

### Exit criteria

- [x] `grep -r 'st3://' . --include='*.py' --include='*.md' --include='*.json'` returns zero hits
- [x] `grep -r 'st3-workflow' . --include='*.py' --include='*.json' --include='*.yaml'` returns zero hits
- [x] `run_tests(path="tests/mcp_server/")` — all tests pass
- [x] `run_quality_gates(scope="branch")` — 0 errors
- [x] MCP server starts and exposes resources under `pgmcp://` scheme

---

## Cycle 5 — Directory Rename + YAML + Cosmetics

### Scope

Physical rename of `.st3/` directory to `.phase-gate/` (on dev machines, the dir
must be moved manually or via a migration script). YAML config files updated to
match. Cosmetic string updates in comments and docstrings.

### Files changed

**YAML config (runtime-critical — must stay in sync with directory rename):**

| File | Change |
|------|--------|
| `.st3/config/contracts.yaml` | `path: .st3/...` → `path: .phase-gate/...` for all branch_local_artifacts |
| `.st3/config/project_structure.yaml` | `.st3:` entry → `.phase-gate:` |
| `.st3/config/workflows.yaml` | `phase_source: ".st3/config/..."` → `".phase-gate/config/..."` |

**Cosmetic (comments/docstrings/display strings):**

| File | Lines | Change |
|------|-------|--------|
| `mcp_server/managers/phase_contract_resolver.py` | L18–20 | Display paths |
| `mcp_server/managers/enforcement_runner.py` | L6, 30 | Docstring + constant |
| `mcp_server/managers/qa_manager.py` | L103, 160 | Docstring + error message |
| `mcp_server/tools/project_tools.py` | L279–280 | Error message |
| `mcp_server/state/quality_state.py` | L13 | Docstring |
| `mcp_server/managers/quality_state_repository.py` | L21 | Docstring |

**Test variable names (cosmetic):**

| File | Change |
|------|--------|
| Up to 3 test files | `st3_dir` variable references → `phase_gate_dir` |

### Exit criteria

- [ ] `grep -rn '\.st3' . --include='*.py' --include='*.yaml' --include='*.json'` returns zero hits (excluding `.git/`)
- [ ] `grep -rn '"st3"' . --include='*.py'` returns zero hits
- [ ] `run_tests(path="tests/mcp_server/")` — all tests pass (with `.phase-gate/` dir on disk)
- [ ] `run_quality_gates(scope="branch")` — 0 errors
- [ ] MCP server starts with `.phase-gate/` directory structure

---

## Risk Register

| Risk | Mitigation |
|------|------------|
| URI rename breaks existing `@imp`/`@qa` sessions | Cycle 3 updates agent.md + mcp.json atomically; existing sessions need restart |
| Directory rename breaks local dev environments | Document migration step: `mv .st3/ .phase-gate/` in PR description |
| `normalize_config_root()` fallback incorrect after fix | Add test for each of the 3 candidate forms (config, .phase-gate, bare path) |
| Constructor signature changes break tests | Update tests in same cycle as production code |

---

## Dependency Order

```
C2 (server_root injection — eliminate .st3 fallbacks)
  └─► C3 (chain inversion — server_root primary, settings.state_dir)
      └─► C4 (URI + name rename) — independent of C2/C3 but logically after
          └─► C5 (dir rename) — must come last; server must already be dir-name-agnostic from C2+C3
```

C2 and C4 are logically independent but C5 depends on both C2 and C3

---

## Cycle 6 — Naming Cleanup

### Scope

Fix the `state_dir` field name introduced in C3 (finding F13) and the `state_file`
attribute naming in `PhaseStateEngine` (finding F14). Also fix two code-quality
issues uncovered post-C5: `standards.py` duplicates the state-dir resolution logic,
and three error messages reference the now-renamed `settings.state_dir`.

### Changes

| File | Change | Finding |
|------|--------|---------|
| `mcp_server/config/settings.py` | `state_dir: str` → `server_root_dir: str`; update dict key in `from_env()` | F13 |
| `mcp_server/server.py` | `settings.server.state_dir` → `settings.server.server_root_dir` | F13 |
| `mcp_server/config/loader.py` | Update docstring: `settings.state_dir` → `settings.server.server_root_dir` | F13 |
| `mcp_server/resources/standards.py` | Replace manual `MCP_STATE_DIR` env lookup with `Settings.from_env()` | F13 |
| `mcp_server/managers/artifact_manager.py` | Fix stale error message (L127) | F13 |
| `mcp_server/managers/enforcement_runner.py` | Fix stale error message (L163) | F13 |
| `mcp_server/tools/phase_tools.py` | Fix stale error message (L83) | F13 |
| `mcp_server/managers/phase_state_engine.py` | `self.state_file` → `self.state_path` (L90, L449, L464) | F14 |

### Test files affected

| File | Change |
|------|--------|
| `tests/mcp_server/unit/config/test_settings.py` | `state_dir` → `server_root_dir` in test names + assertions (L96–108) |
| `tests/mcp_server/unit/server/test_validate_tool_arguments.py` | `.state_dir` → `.server_root_dir` (L30) |
| `tests/mcp_server/unit/test_c260_c2_state_root_injection.py` | `engine.state_file` → `engine.state_path` (L111, L120) |

### Deferred (separate issue)

- F12: `proxy.py` + `qa_manager.py` CWD-relative log paths (require `server_root` injection into proxy/QA manager chain)
- F11: `template_config.py` workspace-local template path (Template Workspace Initiative)

### Exit criteria

- [ ] `grep -r 'state_dir' mcp_server/ --include='*.py'` returns zero hits (excluding `MCP_STATE_DIR` string literals)
- [ ] `grep -r '\.state_file\b' mcp_server/ --include='*.py'` returns zero hits
- [ ] Three error messages no longer reference `settings.state_dir`
- [ ] `run_tests(path="tests/mcp_server/")` — all tests pass
- [ ] `run_quality_gates(scope="branch")` — 0 errors
(dir-name-agnostic paths + runtime-configurable name via `settings.state_dir`).
