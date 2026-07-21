<!-- docs/development/issue428/research.md -->
<!-- template=research version=8b7bb3ab created=2026-07-21T21:11Z updated=2026-07-21 -->
# Research Document - Implement `--upgrade` CLI command and release v2.0.0

**Status:** DEFINITIVE  
**Version:** 1.0.0  
**Last Updated:** 2026-07-21  

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

### 2. Bootstrapping & Version Validation
- **Server Bootstrapping**: `mcp_server/bootstrap.py` (lines 215–285) contains `_validate_version()`.
- **Version Mismatch**: Compares `.pgmcp/.version` against `settings.server.version`. If missing or mismatched, raises `ConfigError` ("*Workspace version mismatch... Please upgrade your workspace*").
- **Degraded Mode**: `cli.py` catches `ConfigError` and falls back to `DegradedMCPServer` (lines 78–81).

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
| **Server Bootstrapper** | `mcp_server/bootstrap.py` | Update `_validate_version()` guidance error message to direct user to `pgmcp --upgrade`. |
| **Unit & Integration Tests** | `tests/mcp_server/unit/test_cli.py` | Add unit tests for `pgmcp --upgrade`, backup creation, asset renewal, and state preservation. |
| **Documentation & Help** | `docs/reference/mcp/` & `AGENTS.md` | Update CLI usage reference pages and help menus. |

---

## Approved Strategy

**Selected Strategy:** `Smart Version-Aware Preservation with Backup & Upgrade Logging`

### Strategy Principles & Rules:

1. **Fail-Safe Timestamped Backup**:
   - Before modifying any workspace assets, generate a complete copy of the `.pgmcp/` directory to `.pgmcp_backup_YYYYMMDD_HHMMSS/`.
   - Protects custom user edits and configurations against data loss.

2. **Smart Version-Aware Preservation**:
   - Do **not** indiscriminately overwrite user configurations.
   - Files matching package defaults or passing schema validation remain intact.
   - Outdated, corrupt, or missing core assets (`config/`, `templates/`, `docs/`) are renewed from `mcp_server/assets/`.
   - `.pgmcp/.version` is updated to the target server version.

3. **Strict Dynamic State Preservation**:
   - Dynamic runtime state files (`state.json`, `deliverables.json`, `template_registry.json`, `logs/`) are **strictly preserved** and never modified or deleted during upgrades.

4. **Structured Upgrade Log Artifact**:
   - Write a detailed structured log file to `.pgmcp/logs/upgrade_YYYYMMDD_HHMMSS.json` (and update `.pgmcp/upgrade.log`).
   - Records: target version, backup path, preserved files, renewed/updated files, newly added files, and warnings/actions required.
   - Enables AI agents to audit the upgrade result via `get_work_context` and agentically reconcile any remaining custom configuration conflicts if needed.

---

## Architectural Constraints & Principles

- **CQS (Command-Query Separation)**: Separate query methods (checking version compatibility, diffing assets) from command methods (performing backup, overwriting assets).
- **Dependency Injection (DIP)**: Inject workspace paths, settings, and file writers rather than relying on module-level singletons or globals.
- **Single Responsibility Principle (SRP)**: Keep `mcp_server/cli.py` concise by delegating backup, asset renewal, and state preservation to a dedicated service class.
- **Fail-Safe Rollback**: If an unhandled exception occurs during asset renewal, clean up transient files and advise the user on restoring from the timestamped backup.

---

## Expected Results for Design & Planning

- High-level design for `WorkspaceUpgrader` service in `mcp_server/services/workspace_upgrader.py`.
- Interface for `pgmcp --upgrade` CLI command in `mcp_server/cli.py`.
- Structured Upgrade Log DTO schema and JSON format.
- Comprehensive unit test plan in `test_cli.py` covering:
  - `--upgrade` on non-existent `.pgmcp/` (should fail instructing user to run `--init`).
  - `--upgrade` creating timestamped backup `.pgmcp_backup_YYYYMMDD_HHMMSS/`.
  - Renewal of outdated templates and config contracts.
  - Preservation of user-customized valid YAML configs.
  - Preservation of `state.json` and dynamic runtime state.
  - Verification of `upgrade_YYYYMMDD_HHMMSS.json` log output.

---

## Open Questions for Design Phase

1. Should `pgmcp --upgrade` support an optional `--force` flag to force full asset replacement if a workspace is severely corrupted?
2. Should `WorkspaceUpgrader` prune old backups (e.g. keeping the last 3 backups) or leave backup retention to the user?

---

## Related Documentation

- [docs/reference/tools/README.md](../../reference/tools/README.md)
- [docs/coding_standards/ARCHITECTURE_PRINCIPLES.md](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-21 | Agent | Initial draft with Approved Strategy for Issue #428 |
