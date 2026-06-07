<!-- docs\development\issue388\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-07T13:31Z updated= -->
# Research: Separate ST3 backend into its own repository (#388)

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-06-07

---

## Scope

**In Scope:**
All top-level folders and files in the current repo. Repo rename sequence. Git history strategy. tests/unit/ migration path. Grey-area folders: scripts/, src/copilot_orchestration/, tests/copilot_orchestration/, proof_of_concepts/, locales/, temp/. Documentation split. Coding standards duplication policy. AGENTS.md ownership.

**Out of Scope:**
Implementation details of the migration (filter-repo command sequences belong in design/planning). New repo CI/CD setup for S1mpleTrader. Package naming for PyPI publication of phase-gate-mcp.

## Prerequisites

Read these first:
1. docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
2. Issue #388 body
---

## Problem Statement

The S1mpleTraderV3 repository contains two unrelated codebases — phase-gate-mcp (MCP workflow server) and the ST3 backend (trading platform) — in a single package. This blocks independent release lifecycles, clean dependency management, and publication of phase-gate-mcp as a standalone package.

## Research Goals

- Identify the full boundary between phase-gate-mcp and ST3 backend content
- Classify grey-area folders with explicit verdicts
- Establish the correct repo rename sequence
- Determine git history preservation strategy for ST3 backend
- Identify all pre-migration cleanup items
- Identify strategy-sensitive boundaries requiring explicit approval before design phase

---

## Background

Repo started 2025-10-26 as pure ST3 trading platform. MCP server was added 2025-12-08. Since then MCP development dominated (817 commits vs 100 for backend/). The two codebases have zero Python import coupling. They share a single pyproject.toml under the package name simpletraderv3 3.0.0.

---

## Findings

### 1. Boundary Classification

#### 1a. Definitive phase-gate-mcp content (stays in current repo)

| Path | Evidence |
|---|---|
| `mcp_server/` | MCP server core, tools, managers, config, services, scaffolders |
| `tests/mcp_server/` | All MCP test suites including fixtures, parity, unit, integration |
| `tests/unit/config/test_c_loader_structural.py` | Imports `mcp_server.config.loader`, `mcp_server.managers`, `mcp_server.core.exceptions` — MCP test |
| `tests/unit/config/test_c_settings_structural.py` | Imports `mcp_server.config.settings` — MCP test |
| `docs/mcp_server/` | MCP server architecture reference |
| `docs/reference/mcp/` | MCP tools reference, agent coordination model |
| `docs/coding_standards/` | Shared standards — duplicated to ST3 repo (see §3) |
| `.phase-gate/` | Workflow state and config — MCP-only |
| `.github/` | Agent files (co/imp/qa), CI config — MCP-only |
| `AGENTS.md` | MCP workflow contract — NOT duplicated (see §3) |
| `scripts/` | `capture_baselines.py` imports `mcp_server.scaffolding.renderer` — 100% MCP |

#### 1b. Definitive ST3 backend content (migrates to new S1mpleTrader repo)

| Path | Evidence |
|---|---|
| `backend/` | Trading platform: enums, eventbus, flow_initiator, strategy_cache, DTOs, services, workers |
| `tests/backend/` | Backend tests; `conftest.py` is empty — no MCP coupling |
| `locales/` | `en.yaml` — belongs to ST3 (user decision) |

#### 1c. Dead code — delete, not migrated

| Path | Reason |
|---|---|
| `src/copilot_orchestration/` | Dead code — not used by either codebase (user confirmed) |
| `tests/copilot_orchestration/` | Tests for dead code |
| `temp/` | Work artifacts: diffs, migration scripts, test results — not source code |
| `proof_of_concepts/` | ST3 experimental POCs — not worth preserving (user decision) |

#### 1d. Pre-migration cleanup (before filter-repo runs)

| Path | Action |
|---|---|
| `tests/unit/config/test_c_loader_structural.py` | Move to `tests/mcp_server/unit/config/` — last stranded MCP test file |
| `tests/unit/config/test_c_settings_structural.py` | Move to `tests/mcp_server/unit/config/` — last stranded MCP test file |
| `tests/unit/` remainder | Delete (pycache-only after the 2 moves above) |
| `tests/integration/`, `tests/acceptance/`, `tests/regression/` | Delete (pycache-only, no source files) |
| `src/copilot_orchestration/`, `tests/copilot_orchestration/` | Delete (dead code) |
| `temp/` | Delete |
| `proof_of_concepts/` | Delete |

#### 1e. Documentation split

| Path | Destination |
|---|---|
| `docs/architecture/` | ST3 repo |
| `docs/coding_standards/` | Both repos (duplicated) |
| `docs/mcp_server/` | phase-gate-mcp |
| `docs/reference/mcp/` | phase-gate-mcp |
| `docs/reference/platform/`, `docs/reference/dtos/` | ST3 repo |
| `docs/system/` | ST3 repo |
| `docs/implementation/` | ST3 repo |
| `docs/setup/` | phase-gate-mcp (or both) |
| `docs/development/` | phase-gate-mcp (issue tracking history) |
| `docs/archive/`, `docs/temp/` | Delete |
| `AGENTS.md` | phase-gate-mcp only — not duplicated |
| `README.md` | Rewrite for each repo |

---

### 2. Git History

| Metric | ST3 backend | phase-gate-mcp |
|---|---|---|
| First commit | 2025-10-26 | 2025-12-08 |
| Last commit | 2026-05-09 | 2026-06-07 (ongoing) |
| Commits touching codebase | ~100 | ~817 |

ST3 backend history is meaningful (~100 commits, 6.5 months). Preserving it via `git filter-repo` is correct. Zero import coupling means a path-based filter produces a clean history for both repos without breakage.

---

### 3. AGENTS.md and Coding Standards Policy

| Document | Policy | Rationale |
|---|---|---|
| `AGENTS.md` | phase-gate-mcp only — not duplicated | Workflow contract specific to phase-gate-mcp agent protocol. Arrives in consumer repos via server installation only. |
| `docs/coding_standards/` (all files) | Duplicated to both repos | Binding contract for code quality; applies to any codebase |

---

### 4. Repo Rename Sequence

| Step | Action | Prerequisite |
|---|---|---|
| 1 | Rename `S1mpleTrader` → `ST1` | Frees the `S1mpleTrader` name |
| 2 | Rename `S1mpleTraderV3` → `phase-gate-mcp` | None; GitHub preserves redirect URLs |
| 3 | Create new `S1mpleTrader` repo (empty) | Step 1 must complete first |
| 4 | Migrate ST3 content to `S1mpleTrader` via `git filter-repo` | Steps 1–3 complete + pre-migration cleanup done |

---

### 5. pyproject.toml Split

Current single package `simpletraderv3 3.0.0` includes both codebases. After separation:

| Repo | Package name | Includes | Key runtime deps |
|---|---|---|---|
| `phase-gate-mcp` | TBD (packaging scope deferred) | `mcp_server*` | `pydantic`, `pyyaml`, `mcp`, `gitpython`, `PyGithub` |
| `S1mpleTrader` | `simpletraderv3` (or TBD) | `backend*` | `pydantic`, `pyyaml` |

The current `testpaths = ["tests/mcp_server"]` in pyproject.toml is already correct for the MCP repo.

---

### 6. Coupling Summary

| Coupling type | Status | Risk |
|---|---|---|
| Python import coupling (backend ↔ mcp_server) | **None** | ✅ Clean split |
| Test fixture coupling | **None** | ✅ Isolated conftest.py per codebase |
| Stranded MCP test files in tests/unit/ | **2 files** | 🟡 Must move before filter-repo |
| Single pyproject.toml | **Present** | 🟡 Managed by split |
| Shared docs/coding_standards/ | **Present** | 🟡 Managed by duplication |
| Dead code (copilot_orchestration, temp) | **Present** | 🟢 Delete before split |

---

### 7. Candidate Seams

| Seam | Description |
|---|---|
| Pre-migration cleanup | Move 2 MCP test files; delete dead code, temp, pycache-only test dirs |
| Repo renames (Steps 1–2) | GitHub rename operations |
| New repo creation (Step 3) | GitHub API or UI |
| filter-repo migration (Step 4) | ST3 paths → new S1mpleTrader repo with history |
| phase-gate-mcp cleanup | Remove ST3 content from current repo; update pyproject.toml |
| pyproject.toml splits | Two independent package configs |
| Docs split | Copy/move per §1e |

---

## Approved Strategy

### Codebase separation
**Strategy:** Clean break
**Rationale:** Zero import coupling. `git filter-repo` path filter is exact. No bridge needed.
**Constraints:** Pre-migration cleanup must precede filter-repo run.

### AGENTS.md ownership
**Strategy:** phase-gate-mcp only — not duplicated
**Rationale:** Workflow contract for phase-gate-mcp agent protocol. Not a general-purpose document.

### docs/coding_standards/
**Strategy:** Duplicate to both repos
**Rationale:** Binding architectural contract applicable to any codebase.

### Repo identity
**Strategy:** ST1 ← S1mpleTrader (existing rename), phase-gate-mcp ← S1mpleTraderV3 (current repo rename), S1mpleTrader (new, receives ST3 backend)
**Constraints:** Step 1 (rename to ST1) must precede Step 3 (create new S1mpleTrader).

### Git history
**Strategy:** Preserve via `git filter-repo`
**Rationale:** ~100 meaningful ST3 commits over 6.5 months. Issue requires preservation.

### Grey-area folders
| Folder | Decision |
|---|---|
| `src/copilot_orchestration/` | Delete — dead code |
| `tests/copilot_orchestration/` | Delete — dead code tests |
| `scripts/` | Stays with phase-gate-mcp only |
| `proof_of_concepts/` | Delete — not worth preserving |
| `locales/` | Migrates with ST3 backend |
| `temp/` | Delete |

---

## Open Questions

All grey-area decisions resolved by user on 2026-06-07. No open questions remaining.


## Related Documentation
- **[https://github.com/newren/git-filter-repo — git-filter-repo documentation][related-1]**

<!-- Link definitions -->

[related-1]: https://github.com/newren/git-filter-repo — git-filter-repo documentation

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-07 | Agent | Initial draft |