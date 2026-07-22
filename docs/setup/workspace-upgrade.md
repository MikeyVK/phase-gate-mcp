<!-- docs/setup/workspace-upgrade.md -->
<!-- template=generic_doc version=43c84181 created=2026-07-22T18:44Z updated=2026-07-22T18:44Z -->
# Workspace Upgrade Guide: v1.0.0 to v2.0.0

**Status:** APPROVED  
**Version:** 1.0.0  
**Last Updated:** 2026-07-22  
**Purpose:** Step-by-step guide for upgrading an existing workspace from v1.0.0 to v2.0.0 using pgmcp --upgrade.  

---

## 1. Executive Summary

This guide provides clear, step-by-step instructions for upgrading an existing `phase-gate-mcp` workspace directory (`.pgmcp/`) from version `1.0.0` to `2.0.0`.

The workspace upgrade is executed via the `pgmcp --upgrade` CLI command. The upgrade procedure is fully automated, version-aware, and fail-safe.

---

## 2. Prerequisites & Package Installation

1. **Active Virtual Environment**: Ensure your target workspace's virtual environment is activated (`.venv\Scripts\Activate.ps1`).
2. **Install Package Version 2.0.0**: Choose one of the following methods based on your deployment environment:

   - **A. Local Wheel Installation (Offline / Local Build)**:
     ```powershell
     pip install C:\path\to\phase_gate_mcp-2.0.0-py3-none-any.whl --force-reinstall
     ```

   - **B. Local Editable Installation (Development Repository)**:
     ```powershell
     pip install -e .
     ```

   - **C. PyPI Registry (If Published)**:
     ```powershell
     pip install --upgrade phase-gate-mcp
     ```

3. **Open Target Workspace**: Open a terminal in the root directory of the repository containing the `.pgmcp/` workspace directory to upgrade.

---

## 3. Upgrade Procedure (Step-by-Step)

### Step 1: Run the Upgrade CLI Command

Execute the following command in your terminal:

```powershell
# Windows PowerShell / CMD:
.\.venv\Scripts\pgmcp --upgrade

# Linux / macOS:
pgmcp --upgrade
```

### Step 2: Observe Automated Upgrade Operations

The command automatically executes 5 fail-safe upgrade stages:

1. **Fail-Safe Timestamped Backup**: Creates a complete pre-mutation copy of your workspace configuration at `.pgmcp_backup_YYYYMMDD_HHMMSS/`.
2. **Smart Configuration Preservation**: Preserves your custom user YAML configurations in `.pgmcp/config/` (`workflows.yaml`, `git.yaml`, `quality.yaml`, etc.).
3. **Core Asset & Template Renewal**: Renews core package templates (`.pgmcp/templates/`), schemas, and IDE agent rules (`docs/agents/`) from the `2.0.0` release assets.
4. **Strict Dynamic State Retention**: Preserves active runtime state files untouched (`state.json`, `deliverables.json`, `template_registry.json`, and `.pgmcp/logs/`).
5. **Version Parity & Telemetry**: Updates `.pgmcp/.version` to `2.0.0` and writes a structured upgrade log to `.pgmcp/logs/upgrade_YYYYMMDD_HHMMSS.json`.

---

## 4. Output Verification & Confirmation

### Success Output Example

Upon completion, `pgmcp --upgrade` outputs a summary to standard output and exits with code `0`:

```text
============================================================
           Phase-Gate MCP Workspace Upgrade Complete        
============================================================
  Server Root: c:\temp\my-project\.pgmcp
  Backup Dir:  c:\temp\my-project\.pgmcp_backup_20260722_204430
  New Version: 2.0.0
  Status:      SUCCESS
  Log File:    .pgmcp\logs\upgrade_20260722_204430.json
============================================================
  Renewed Assets:   14 file(s)
  Preserved Config: 11 file(s)
============================================================
```

### Step 3: Verify Version File

Confirm that `.pgmcp/.version` contains `2.0.0`:

```powershell
Get-Content .pgmcp/.version
# Expected output: 2.0.0
```

---

## 5. Maintenance & Post-Upgrade Advice

1. **Backup Directory Pruning**: The timestamped backup directory (`.pgmcp_backup_YYYYMMDD_HHMMSS/`) is retained to allow easy rollback if custom templates were modified. After verifying your workspace, you may safely prune older backup folders.
2. **MCP Server Startup**: Start or reload your MCP server (`python -m mcp_server.core.proxy`). The bootstrapper will validate version parity (`2.0.0`) and boot cleanly into active mode.

---

## Related Documentation

- **[Setup Guide](README.md)** — Manual IDE and workspace setup walkthrough.
- **[Agentic Bootstrap Guide](agentic-bootstrap.md)** — Automated AI agent bootstrap guide.
- **[Server Configuration](../reference/server-configuration.md)** — Detailed configuration parameters.
