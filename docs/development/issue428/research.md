# Issue #428 Research: CLI --upgrade command & v2.0.0 release

**Status:** PRELIMINARY  
**Version:** 1.0  
**Last Updated:** 2026-07-16

---

## Problem Statement

The CLI lacks a `--upgrade` command to update workspace templates and configurations (`.pgmcp/config/artifacts.yaml` and `.pgmcp/templates/`) without losing user modifications. This blocks users from easily consuming updates provided by new wheel releases. Furthermore, a new major release v2.0.0 must be prepared.

## Research Goals

- Determine exactly what files the `--upgrade` command should target and the backup mechanism
- Define the process for bumping the version to v2.0.0
- Establish an Approved Strategy for the upgrade behavior (fail-safes, backups, user prompts)

## Findings

1. **Current Initialization**:
   - `mcp_server/cli.py` handles `--init` by fully copying `mcp_server/assets` to the `resolved_server_root` (typically `.pgmcp/`).
   - It errors out if the directory already exists.

2. **Scope of `--upgrade`**:
   - The issue specifies overwriting `artifacts.yaml` in the user's workspace `.pgmcp/config/` directory.
   - It also specifies placing/updating the default templates in `.pgmcp/templates/`.
   - Other assets like `docs/` and `agents/` are not explicitly mentioned for the upgrade, but since they are part of the `release_manifest.yaml` syncing process, they might either be included or left alone. To be safe and adhere strictly to the issue, we will target `config/artifacts.yaml` and `templates/`.

3. **Backup Fail-safes**:
   - The issue requests "creating backups of existing files or asking for user confirmation".
   - Given this CLI tool could run in headless/automation environments, an interactive confirmation prompt is less ideal than an automated, timestamped backup.
   - We can create a backup directory (e.g., `.pgmcp/backups/upgrade_<timestamp>/`) and move the existing `artifacts.yaml` and `templates/` directory there before copying the new ones from the `assets/` bundled with the wheel.

4. **Version Bump (v2.0.0)**:
   - `pyproject.toml` is the single source of truth for the version (`version = "1.0.0"`).
   - This needs to be bumped to `2.0.0`.

## Strategy Options for `--upgrade`

### Option 1: Automated Timestamped Backups (Recommended)
- **Mechanism**: The `--upgrade` command creates `.pgmcp/backups/upgrade_<timestamp>/` and moves the current `config/artifacts.yaml` and `templates/` there.
- **Copy**: It then copies the bundled `assets/config/artifacts.yaml` and `assets/templates/` to the workspace.
- **Pros**: Zero data loss, non-interactive (safe for scripts), clear rollback path.
- **Cons**: Leaves backup folders in the workspace that the user might need to clean up manually eventually.

### Option 2: Interactive Prompts
- **Mechanism**: The CLI prompts the user (`y/N`) before overwriting `artifacts.yaml` or any template file.
- **Pros**: Keeps the workspace clean of backups.
- **Cons**: Halts execution. Since MCP servers are often started by IDEs, this could cause hangs if users run it in the wrong context, though as a CLI command it should be run manually.

### Option 3: Full Asset Directory Overwrite with Backup
- **Mechanism**: Backup the entire `.pgmcp/` directory to `.pgmcp.bak.<timestamp>` (excluding logs/runs) and then do a full `--init` style copy.
- **Pros**: Upgrades `docs/`, `agents/`, etc., in addition to templates.
- **Cons**: Overkill. Might disrupt `state.json` or `deliverables.json` if we aren't careful about which files are overwritten.

## Open Questions / Approval Request

- **Strategy**: Should we proceed with **Option 1 (Automated Timestamped Backups)** as the Approved Strategy?
- **Scope**: Should the upgrade explicitly only target `artifacts.yaml` and `templates/`, or should it also refresh the `agents/` and `docs/` folders from the wheel assets? (Option 1 targets only what the issue explicitly requested).

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-16 | Agent | Initial draft with findings and strategy options |