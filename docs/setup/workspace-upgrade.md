# Workspace Upgrade Guide

**Purpose:** Owner-led initialization and template renewal for an existing PGMCP server root.

This guide describes the behavior of the current CLI and renewal implementation. The project release remains **2.0.0**; template-suite renewal is a separate operation and does not imply a new package release.

## Initialize a new server root

Set the workspace and server-root configuration for the intended repository, then run:

```powershell
pgmcp --init
```

Initialization copies the packaged assets to a previously absent server root and establishes its initial managed template state. If the configured server root already exists, `--init` refuses and exits with code 1. It does not merge with, replace, or repair an existing root. Normal server startup also requires the root to exist.

PGMCP does not install Python or native dependencies. Provision the package and its dependencies using your environment's chosen installation process. Workspace adapters in the server root are owner-managed; do not treat them as package-managed assets.

## Renew an existing managed template suite

Run renewal from the workspace whose configured server root should be renewed:

```powershell
pgmcp --upgrade
```

Renewal stages and validates a candidate, compares it with the active suite and recorded template checkpoint, and reports the resulting changes. It does not perform an external rollout or overwrite the external configuration root. Preserve and review owner-managed configuration and adapters as part of your change process.

### When a trustworthy template baseline is missing

If no checkpoint exists and the complete active suite cannot be established as equal to the validated candidate, renewal reports `checkpoint_required`, returns exit code `2`, leaves the active suite unchanged, and retains the staged candidate. An equal active suite can establish its initial checkpoint automatically; follow the actual CLI outcome. Exit code 2 means owner action is required; it is not a successful activation or an ordinary execution failure.

After reviewing the actual local suite and the staged candidate, choose one explicit action:

- Accept the current candidate as the adopted baseline, without replacing suite contents:
  ```powershell
  pgmcp --upgrade --accept-template-baseline
  ```
- Replace the complete managed suite with the verified candidate. This action creates a backup before activation:
  ```powershell
  pgmcp --upgrade --force-template-upgrade
  ```

Use baseline acceptance only after reconciling the local templates with the candidate. Force renewal intentionally replaces the managed template suite; review owner changes and keep the generated backup according to your recovery policy. Do not infer a trustworthy checkpoint from legacy version markers or registries.

### After renewal

When the active suite changes, restart any running PGMCP server so it loads the new suite. If renewal reports conflicts or another corrective action, follow the exact action printed by the CLI and review the affected component before resolving it. A renewal that leaves the active suite unchanged does not require a restart.

## Related documentation

- [Setup Guide](README.md) — manual IDE and workspace setup.
- [Agentic Bootstrap Guide](agentic-bootstrap.md) — agent-assisted bootstrap.
- [Server Configuration](../reference/server-configuration.md) — configuration parameters.
