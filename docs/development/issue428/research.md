<!-- docs/development/issue428/research.md -->
<!-- template=research version=8b7bb3ab created=2026-07-21T21:11Z updated=2026-07-22 -->
# Research Document - Implement `--upgrade` CLI command and release v2.0.0

**Status:** DEFINITIVE  
**Version:** 1.1.0  
**Last Updated:** 2026-07-22  

---

## Problem Statement

Currently, there is no standardized way to upgrade an existing user workspace `.pgmcp/` directory when a newer version of the wheel package is installed. Upgrades to schemas, default templates, rules, and configurations require manual intervention, leading to startup crashes, version mismatches, or outdated workspace assets.

---

## Research Goals

- Analyze current CLI entry points and argument parsing in `mcp_server/cli.py`.
- Examine package asset distribution (`mcp_server/assets/`) and build pipelines.
- Evaluate workspace upgrade strategies (Full Asset Overwrite vs. Version-Aware Preservation).
- Formulate the binding Approved Strategy for Issue #428 (fail-safe backups, asset renewal, state preservation, upgrade logging).
- Map the blast radius across CLI, bootstrapper, services, test suites, and documentation.

---

## Codebase Findings & Evidence

### 1. CLI Entry Points & Argument Parsing
- **Script Entry Point**: Configured in `pyproject.toml` (lines 18–20): `pgmcp = "mcp_server.cli:main"`.
- **Module Entrypoint**: `mcp_server/__main__.py` (lines 1–3) invokes `main()`.
- **CLI Implementation**: `mcp_server/cli.py` (lines 13–84) uses stdlib `argparse.ArgumentParser`.
- **Existing Flags**:
  - `--version` (lines 18, 26–29): Prints `Phase-Gate MCP Server v{version}` and exits `0`.
  - `--init` (lines 20–23, 31–63): Checks if `.pgmcp/` exists. If missing, copies `mcp_server/assets/` into `.pgmcp/` and writes `.pgmcp/.version`. If present, exits `1` with error.

### 2. Bootstrapping & Version Validation Decoupling
- **Current State**: `ServerBootstrapper._validate_version()` in `mcp_server/bootstrap.py` (lines 257–285) checks `.pgmcp/.version` against `settings.server.version`. If missing or mismatched, raises `ConfigError`.
- **Decoupling Opportunity (SRP)**: To preserve `ServerBootstrapper` SRP, version checking logic should be decoupled into a dedicated validator class (`WorkspaceVersionValidator` or leveraging `StateVersionValidator`), moving version check responsibility out of the core bootstrapper orchestration.

### 3. Package Asset Distribution
- **Wheel Package Data**: `pyproject.toml` (lines 40–41) includes `mcp_server/assets/**/*` in build artifacts.
- **Build Pipeline**: `scripts/build_package.py` (lines 72–84) copies source paths (`.pgmcp/config`, `.pgmcp/templates`, `docs/agents`, `docs/coding_standards`, `docs/reference`, etc.) into `mcp_server/assets/` prior to build.
- **Workspace Runtime State**: Bestanden aangemaakt/bijgewerkt door agent-workflows in `.pgmcp/` die **dynamisch runtime state** bevatten: `state.json`, `deliverables.json`, `template_registry.json`, `logs/`.

---

## Blast Radius & Affected Boundaries

| Component / Boundary | Location | Impact Description |
|---|---|---|
| **CLI Argument Parsing** | `mcp_server/cli.py` | Add `--upgrade` flag and delegate execution to upgrader service. |
| **Workspace Upgrader Service** | `mcp_server/services/workspace_upgrader.py` | Dedicated service for fail-safe backup, asset renewal, state preservation, and upgrade logging. |
| **Version Validation (SRP)** | `mcp_server/managers/workspace_version_validator.py` | Decoupled workspace version validation service. |
| **Server Bootstrapper** | `mcp_server/bootstrap.py` | Delegate version check to `WorkspaceVersionValidator`; update guidance error message to direct user to `pgmcp --upgrade`. |
| **Unit & Integration Tests** | `tests/mcp_server/unit/test_cli.py` | Add unit tests for `pgmcp --upgrade`, backup creation, asset renewal, and state preservation. |
| **Documentation & Help** | `docs/reference/mcp/` & `AGENTS.md` | Update CLI usage reference pages and help menus. |

---

## Approved Strategy

**Selected Strategy:** `Smart Version-Aware Preservation with Backup & Upgrade Logging`

### Strategy Principles & Rules:

1. **Fail-Safe Timestamped Backup**:
   - Before modifying any workspace assets, generate a complete copy of the `.pgmcp/` directory to `.pgmcp_backup_YYYYMMDD_HHMMSS/`.
   - Protects custom user edits and configurations against data loss. Backup pruning is intentionally left to the user.

2. **Smart Version-Aware Preservation via Existing Loader Validation**:
   - Do **not** indiscriminately overwrite valid user configurations or develop complex custom diffing helpers.
   - Leverage existing `ConfigLoader` / `ValidationService` infrastructure: files that pass schema validation and match current contracts are preserved.
   - Outdated, corrupt, or missing core assets (`config/`, `templates/`, `docs/`) are renewed from package `mcp_server/assets/`.
   - `.pgmcp/.version` is updated to the target server version.

3. **Strict Dynamic State Preservation**:
   - Dynamic runtime state files (`state.json`, `deliverables.json`, `template_registry.json`, `logs/`) are **strictly preserved** and never modified or deleted during upgrades.

4. **Single Structured Upgrade Log Artifact**:
   - Write a single structured JSON log file to `.pgmcp/logs/upgrade_YYYYMMDD_HHMMSS.json`.
   - Records: target version, backup path, preserved files, renewed/updated files, newly added files, and warnings/actions required.
   - Serves as an audit file for manual or agentic inspection when needed. (`get_work_context` remains focused on workflow state and does not load upgrade logs).

5. **Simple CLI Interface (No `--force` Flag)**:
   - CLI interface remains clean (`pgmcp --upgrade`). If a workspace is severely corrupted beyond repair, standard recovery is deleting `.pgmcp/` and running `pgmcp --init`.

---

## Architectural Constraints & Principles

- **CQS (Command-Query Separation)**: Separate query methods (checking version compatibility, diffing assets) from command methods (performing backup, overwriting assets).
- **Dependency Injection (DIP)**: Inject workspace paths, settings, and file writers rather than relying on module-level singletons or globals.
- **Single Responsibility Principle (SRP)**: Keep `mcp_server/cli.py` concise by delegating backup, asset renewal, and state preservation to a dedicated service class, and decouple version checking from `ServerBootstrapper`.
- **Fail-Safe Rollback**: If an unhandled exception occurs during asset renewal, clean up transient files and advise the user on restoring from the timestamped backup.

---

## Expected Results for Design & Planning

- High-level design for `WorkspaceUpgrader` service in `mcp_server/services/workspace_upgrader.py`.
- Decoupled `WorkspaceVersionValidator` design.
- Interface for `pgmcp --upgrade` CLI command in `mcp_server/cli.py`.
- Structured Upgrade Log DTO schema and JSON format (`.pgmcp/logs/upgrade_YYYYMMDD_HHMMSS.json`).
- Comprehensive unit test plan in `test_cli.py` covering:
  - `--upgrade` on non-existent `.pgmcp/` (fails instructing user to run `--init`).
  - `--upgrade` creating timestamped backup `.pgmcp_backup_YYYYMMDD_HHMMSS/`.
  - Renewal of outdated templates and config contracts.
  - Preservation of user-customized valid YAML configs via `ConfigLoader`.
  - Preservation of `state.json` and dynamic runtime state.
  - Verification of `upgrade_YYYYMMDD_HHMMSS.json` log output.

---

## Related Documentation

- [docs/reference/tools/README.md](../../reference/tools/README.md)
- [docs/coding_standards/ARCHITECTURE_PRINCIPLES.md](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-21 | Agent | Initial draft with Approved Strategy for Issue #428 |
| 1.1.0 | 2026-07-22 | Agent | Refined with feedback: bootstrapper SRP version check decoupling, ConfigLoader schema validation reuse, single log file, no --force flag, no backup pruning |
