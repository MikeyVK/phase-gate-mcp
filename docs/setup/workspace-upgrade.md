# Workspace Upgrade Guide

**Purpose:** Owner-led package migration and template renewal for an existing PGMCP server root.

This guide covers the **PGMCP 4.0.0 candidate**, including deliberate adoption from
3.0.0 or an older workspace. Publication and downloadable artifact identities remain
those recorded on [GitHub Releases](https://github.com/MikeyVK/phase-gate-mcp/releases).
Package installation, owner-managed configuration, template renewal and agent
instruction deployment are separate operations; none silently performs the others.

For the cooperative end-to-end route, explicitly invoke the
[authoritative agent checklist](agentic-bootstrap.md) in the chosen workspace chat,
using its **upgrade/delta** mode. Use the checklist from the selected new wheel or
installed package assets: an existing server root may still contain older copied
documentation. This guide owns CLI/checkpoint and recovery
details; it does not replace that checklist or declare capability readiness from
health. Neither package installation nor `--upgrade` starts an agent. Preserve
owner configuration and instructions, and revisit only the changed contracts and
their dependencies before representative verification.

## Runtime and migration order

Use Python **>=3.15** in the environment that actually launches the proxy and
server. An existing virtual environment keeps its original interpreter; create
a dedicated replacement when necessary and install the reviewed 4.0.0 wheel there.
The package declares MCP SDK 2.3.0 and its runtime pins; selected native adapter
executables have their own declared prerequisites. Follow the
[dependency/source-build guidance](README.md#dependency-source-builds) when a
dependency has no suitable binary wheel.

Before switching the active connection:

1. Record the existing interpreter/package and effective workspace, server,
   config and template roots. Preserve owner overrides, native policies,
   templates, instructions and state through a deliberate backup.
2. Prepare a coherent 4.0.0 config basis and explicit workspace overrides as
   described below. Reconcile GitHub identity, quality choices, startup policy,
   response mode and any existing branch state before normal writes.
3. Use the existing template-renewal route only for the active suite. First
   [reconcile current instruction/document sources](agentic-bootstrap.md#32-reconcile-shared-sources)
   from the selected package to the effective server-root `agents/` and relevant
   `docs/` paths, preserving owner additions. Verify those current sources before
   [deploying through the host](agentic-bootstrap.md#33-deploy-the-shared-agents-map).
   Installing the wheel or running template-only `--upgrade` does not perform
   this source reconciliation on a populated root or activate an agent.
4. Relaunch the complete proxy/child connection in the selected environment,
   refresh discovery and demonstrate the selected capabilities. Keep the previous
   environment/configuration recoverable until owner acceptance.

## Quality choices — owner acknowledgement required

Each applicable check/test/fix binding requires a deliberate configuration_choice
after review. Existing configurations with missing/null choices can start for
setup/health, but applicable quality execution is refused until acknowledged.
Shipped base choices are null; `--init` preserves choices in supplied assets
rather than resetting them. Native tool policies are configured by the owner;
this repository's native policy is not installed as the workspace baseline.
Template renewal does not refresh or overwrite owner bindings. Review the [quality setup procedure](README.md#choose-the-workspace-quality-policy)
and perform a focused first verification. Report-mode safe-edit can retain truthful
unexecuted-check facts while making a guarded edit; existing workspace admission and
PR-status gates still apply. GitHub repository owner/name no longer have personal
defaults; supply owner/repo in root github.yaml and prefer GITHUB_TOKEN for credentials.

## Configuration composition

Prepare a self-contained config root with complete `defaults/<file>.yaml` bases
from the reviewed package and optional root `<file>.yaml` workspace differences.
Convert earlier object lists to keyed mappings. Use unique integer `order` ranks
where execution/presentation order matters; YAML position is not order.
The exact `{$delete: true}` command removes an inherited mapping member; `null`
is a value, not deletion. Literal value lists are replaced as complete lists.
Follow the [configuration contract](../reference/config-loading-architecture.md)
for validation, optional enforcement and source ownership.

Move explicit owner/repo/project metadata to root `github.yaml`. A nonempty
`GITHUB_TOKEN` takes precedence over a deliberately configured token alternative.
Remove the launcher's former GitHub section and identity environment settings;
keep secrets outside tracked files and diagnostic output. Git operations bind to
the selected workspace, independently of launcher CWD. Do not inherit conflicting
Git repository selectors.

Install/reconcile the required `defaults/server.yaml` startup basis and optional
root `server.yaml` policy. Its shipped lock wait/retry/proxy values are
30 seconds / 0.25 seconds / 60 seconds. Align the outer host deadline and use the
[schema/reference](../reference/server-configuration.md#startup-admission-policy)
for valid overrides; these values do not promise startup latency. Move an old
`PGMCP_CONFIG_PATH` launcher overlay away from `config/server.yaml` if it contains
launcher `server:`/`logging:` fields.

Older standalone `policies.yaml` operation-policy files and Python APIs are no
longer consumed. After reviewing local ownership, they may be explicitly removed;
PGMCP does not delete them automatically. Template package `policy.yaml` files
and active enforcement/check declarations retain their own roles.

Existing roots require deliberate reconciliation, with no automatic converter
or compatibility reader. Stage/review the coherent files before adoption.
Do not run `--init` against a populated root; template-only `--upgrade` does not
install or migrate config bases, owner overrides or native tool policy.

## Response mode and client discovery

Choose `structured` or `resource` through `PGMCP_RESPONSE_MODE` on each connection
when needed; otherwise use `presentation.yaml: global.response_mode` (shipped
default: `structured`). Remove interim `PGMCP_RESPONSE_PROFILE`,
`server.response_profile` and profile/channel-map configuration. Different
connections may select different modes in the same workspace.

Both normal modes supply bounded inline text and separate available schema
attachments. Structured mode adds the complete operation/rendered presentation
and a matching output schema. Resource mode supplies a real operation-cache
reference without normal structured content/output schema. It does not duplicate
rendered instructions in that cache. Validate agent-visible text, instructions,
attachments and the full-data route through the actual host connection; a
`schema://` attachment identity is not automatically a resources/read route.
See [response-mode setup](README.md#choose-the-response-mode).

## Branch registration contract

Every `initialize_project` call requires an explicit `parent_branch`.

Coordination knows the branch's intended parent and performs
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
configuration. Once the reviewed 4.0.0 wheel is available, for example:

```console
python -m pip install --upgrade ./phase_gate_mcp-4.0.0-py3-none-any.whl
pgmcp --version
```

Use that environment's executable rather than an unrelated global `pgmcp`. A version
response confirms the invoked package; it does not prove workspace migration or healthy
server admission. Use the GitHub release assets; this example does not assume a PyPI
release. Source distributions follow the existing
[release assets procedure](https://github.com/MikeyVK/phase-gate-mcp/blob/main/docs/reference/release-assets-procedure.md).

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

## Reconcile an existing pre-4.0 workspace

Preserve owner changes and explicitly reconcile the 4.0.0 configuration and public tool
contracts before using the new server. Compare the shipped defaults with the effective
owner configuration rather than copying over populated roots. In particular, migrate
artifact/package declarations, execution bindings and adapter capabilities, branch
check `configured_targets` policies, and workflow/enforcement contracts. Use the
[server configuration reference](../reference/server-configuration.md) and rediscover
the exposed tool schemas; old aliases and removed inputs have no compatibility bridge.

`PGMCP_CONFIG_ROOT` selects the effective owner-managed configuration root;
`PGMCP_TEMPLATE_ROOT` selects the active suite when configured. Existing or external
roots do not become package-owned through installation. The package's complete generic `agents/` map is a separate deployment source:
review its protocol, three roles and procedures and place/activate that content through
the actual host's instruction mechanisms. Do not maintain a new host-specific policy variant.
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
the client so the proxy and child server inherit the new settings. Changes to the
[startup policy](../reference/server-configuration.md#startup-admission-policy) always
require full proxy/child relaunch. Existing workspaces explicitly install its required
basis; template-only --upgrade does not install server.yaml.

Inspect `health_check` after restart. If startup is rejected, use its diagnosis to
repair the cause, then request another restart. A restart acknowledgement alone is
not healthy-admission evidence. Follow any exact corrective action reported by renewal;
an unchanged suite alone does not require a restart.

## Related documentation

- [Setup Guide](README.md) — manual IDE and workspace setup.
- [Agentic Bootstrap Guide](agentic-bootstrap.md) — agent-assisted bootstrap.
- [Server Configuration](../reference/server-configuration.md) — effective roots and declarations.
- [Repository changelog](https://github.com/MikeyVK/phase-gate-mcp/blob/main/CHANGELOG.md) — release preparation and breaking changes.


