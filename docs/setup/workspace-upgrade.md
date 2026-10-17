# Workspace Upgrade Guide

**Purpose:** Owner-led package migration and template renewal for an existing PGMCP server root.

This guide covers **PGMCP 3.0.0**. Package installation, owner-managed configuration
and managed template-suite renewal are distinct operations. Use the reviewed artifacts
and version-specific notes from [GitHub Releases](https://github.com/MikeyVK/phase-gate-mcp/releases).

For the cooperative end-to-end route, explicitly invoke the
[authoritative agent checklist](agentic-bootstrap.md) in the chosen workspace chat,
using its **upgrade/delta** mode. This guide owns CLI/checkpoint and recovery
details; it does not replace that checklist or declare capability readiness from
health. Neither package installation nor `--upgrade` starts an agent. Preserve
owner configuration and instructions, and revisit only the changed contracts and
their dependencies before representative verification.

## Unreleased maintenance — owner acknowledgement required

The unreleased #319 changes require a deliberate configuration_choice on each relevant
check/test/fix binding. Existing configurations with missing/null choices can start for
setup/health, but applicable quality execution is refused until acknowledged. Base choices are null; --init preserves choices in supplied assets.
Template renewal does not refresh or overwrite owner bindings. Review the [quality setup procedure](README.md#choose-the-workspace-quality-policy)
and perform a focused first verification. Report-mode safe-edit can retain truthful
unexecuted-check facts while making a guarded edit; existing workspace admission and
PR-status gates still apply. GitHub repository owner/name no longer have personal
defaults; supply owner/repo in root github.yaml and prefer GITHUB_TOKEN for credentials.

A new release is explicitly postponed. These are development upgrade notes, not a new
published version or instruction to replace owner-managed native configs. The 3.0.0
release and its artifacts remain unchanged.

## Unreleased configuration composition

Prepare a coherent self-contained config root with complete defaults/<file>.yaml
bases and optional root workspace overrides. Object collections are keyed mappings;
ordered collections require explicit ranks. Follow the [configuration contract](../reference/config-loading-architecture.md).
GitHub identity/project metadata move to github.yaml. Existing roots need deliberate
owner reconciliation; no automatic config migration or new upgrade mechanism is
provided. Do not replace populated owner files by running initialization.

## Unreleased branch registration contract

The unreleased #503 change requires an explicit `parent_branch` on every
`initialize_project` call. Coordination knows the branch's intended parent and performs
`create_branch`, checkout and initialization before handing work to implementation.
The attached Git branch supplies the head identity; neither reflog nor a default base
is an authority. `submit_pr` now accepts title, body and draft only and uses matching
registered branch/parent identity before submission effects.

Branch state uses schema `2.0.0`; the deliverables envelope remains `1.0.0`.
Existing workspaces must deliberately reconcile valid state with required distinct,
nonblank branch/parent references and the actual branch/positive issue identity before
using the new runtime. Preserve progress and audit fields; changing the schema marker
alone does not repair invalid content. There is no automatic migration or compatibility
reader. See the [project reference](../reference/tools/project.md#pgmcpstatejson)
and [PR reference](../reference/tools/github.md#registered-branch-authority).

For corrupt, version-invalid or unreadable state/planning files, inspect the diagnostic
and source before choosing a repair. Failed validation leaves the original source and
any prior backup intact; retries do not silently convert the problem into absence.
Back up files deliberately when needed, then use an authorized explicit edit or other
owner-led repair and verify the result. Do not delete state merely to make initialization
succeed: existing same-branch registration is deliberately rejected, and initialization
does not unlock an open PR. The separate managed-template renewal backups described
below remain part of that procedure.

Restart after adopting the coherent source/package contract and state, then refresh
client tool discovery. Verify `get_work_context`, `health_check` and the complete
`get_project_plan` readback before normal workflow writes. Package installation,
template renewal and client refresh do not themselves migrate branch state.

## Install the intended package

Install the reviewed release wheel in the Python environment used by the MCP launch
configuration. For a downloaded 3.0.0 wheel, for example:

```powershell
python -m pip install --upgrade ./phase_gate_mcp-3.0.0-py3-none-any.whl
pgmcp --version
```

Use that environment's executable rather than an unrelated global `pgmcp`. A version
response confirms the invoked package; it does not prove workspace migration or healthy
server admission. Use the GitHub release assets; this example does not assume a PyPI
release. Source distributions follow the existing
[release assets procedure](../reference/release-assets-procedure.md).

PGMCP does not install native adapter dependencies. Provision each selected adapter's
declared executable/version through the environment's chosen installation process; see
the [native adapter contract](../reference/execution-adapters.md). Workspace adapters
and their configuration remain owner-managed.

## Initialize a new server root

Set the workspace and server-root configuration for the intended repository, then run:

```powershell
pgmcp --init
```

Initialization copies the packaged assets to a previously absent resolved server root
and establishes its initial managed template state. If that root already exists,
`--init` refuses and exits with code 1. It does not merge with, replace or repair an
existing root. Normal server startup also requires the root to exist.

## Reconcile an existing v2 workspace

Preserve owner changes and explicitly reconcile the v3 configuration and public tool
contracts before using the new server. Compare the shipped defaults with the effective
owner configuration rather than copying over populated roots. In particular, migrate
artifact/package declarations, execution bindings and adapter capabilities, branch
check `configured_targets` policies, and workflow/enforcement contracts. Use the
[server configuration reference](../reference/server-configuration.md) and rediscover
the exposed tool schemas; old aliases and removed inputs have no compatibility bridge.

`PGMCP_CONFIG_ROOT` selects the effective owner-managed configuration root;
`PGMCP_TEMPLATE_ROOT` selects the active suite when configured. Existing or external
roots do not become package-owned through installation. Host agent instructions are
separate distributable assets: review and deploy the selected host's files explicitly.
Do not use `--init` to migrate an existing root.

## Renew an existing managed template suite

Run renewal from the workspace whose configured server root should be renewed:

```powershell
pgmcp --upgrade
```

Renewal stages and validates a candidate, compares it with the active suite and recorded
template checkpoint, and reports the resulting changes. It does not refresh owner-managed
configuration or workspace adapters and does not perform an external rollout.

### When a trustworthy template baseline is missing

If no checkpoint exists and the complete active suite cannot be established as equal
to the validated candidate, renewal reports `checkpoint_required`, returns exit code
`2`, leaves the active suite unchanged and retains the staged candidate. An equal
active suite can establish its initial checkpoint automatically; follow the actual CLI
outcome. Exit code 2 requires owner action and does not claim successful activation.

After reviewing the local suite and staged candidate, choose one explicit action:

- Reconcile the complete local suite with the candidate, then accept the adopted baseline
  without replacing its contents:
  ```powershell
  pgmcp --upgrade --accept-template-baseline
  ```
- Replace the complete managed suite with the verified candidate after reviewing owner
  changes. This action creates a verified backup before activation:
  ```powershell
  pgmcp --upgrade --force-template-upgrade
  ```

Keep the backup according to your recovery policy. Do not infer a trustworthy checkpoint
from legacy version markers or registries. For an external template root, its owner
performs the required migration and checkpoint decision; force renewal does not imply
authority to replace that root.

### Restart and verify

Restart the MCP server after package installation, an active suite change or a change
to startup-loaded configuration. Reconnect or refresh the MCP client so it discovers
the new tool contracts. A launch-environment change may require closing and relaunching
the client so the proxy and child server inherit the new settings.

Inspect `health_check` after restart. If startup is rejected, use its diagnosis to
repair the cause, then request another restart. A restart acknowledgement alone is
not healthy-admission evidence. Follow any exact corrective action reported by renewal;
an unchanged suite alone does not require a restart.

## Related documentation

- [Setup Guide](README.md) — manual IDE and workspace setup.
- [Agentic Bootstrap Guide](agentic-bootstrap.md) — agent-assisted bootstrap.
- [Server Configuration](../reference/server-configuration.md) — effective roots and declarations.
- [Repository changelog](https://github.com/MikeyVK/phase-gate-mcp/blob/main/CHANGELOG.md) — release preparation and breaking changes.


