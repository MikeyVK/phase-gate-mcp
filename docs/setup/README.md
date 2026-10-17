# Setup — Runtime and Host Reference

For agent-led setup or an upgrade, start with the single
[workspace checklist](agentic-bootstrap.md). After installation, `--init` or
`--upgrade`, explicitly give that page to the chosen agent chat; none of those
commands launches an agent. This page supplies technical details, not a separate
readiness procedure.

## Prerequisites

- Select a Python interpreter supported by the chosen package. Current source
  requires Python 3.13+ and MCP SDK `>=1.30.0,<2`; its
  [dependency declarations](https://github.com/MikeyVK/phase-gate-mcp/blob/main/pyproject.toml)
  are authoritative for source installs. Read the actual artifact's metadata for
  an older published release.
- Choose the host and intended capabilities before installing native dependencies.
  Git/repository/identity are prerequisites for selected Git/workflow operations;
  GitHub identity/token/permissions are prerequisites for selected GitHub paths
  and any enforcement that depends on them.
- Preserve existing owner configuration, host settings and customizations. The
  command/config examples below require chosen paths and permission; they are not
  instructions to overwrite an existing setup.

## 1. Credentials and Environment

For selected GitHub functionality, supply owner/repo in the effective
`github.yaml`; prefer host delivery of `GITHUB_TOKEN` from the owner's environment
or secret facility. See [GitHub setup](../manuals/github-setup.md) for precedence,
permissions and the configured-token alternative. Keep token values out of tracked
files, command history, copied transcripts and setup evidence.

Do not add GitHub identity to the MCP launcher. Verify the selected host actually
delivers the intended environment to its child process; a host environment change
may require a full relaunch. Do not assume placeholder expansion works in every
host, and do not print the token to prove delivery.

## 2. Python Virtual Environment

Use the exact interpreter chosen for the launch environment, for example
(replace the example executable, destination and reviewed wheel path):

```powershell
& 'C:/chosen/Python/python.exe' -m venv 'C:/chosen/pgmcp-env'
& 'C:/chosen/pgmcp-env/Scripts/python.exe' -m pip install 'C:/reviewed/phase_gate_mcp-3.0.0-py3-none-any.whl'
```

The example names a wheel, not a promise of PyPI availability or newly published
assets. An existing virtual environment retains its original interpreter; recreate
it when that interpreter no longer satisfies the chosen package. Install only
native tools needed by the selected bindings, at the versions their adapters
declare. Development requirements are for contributors who deliberately select
that environment, not unconditional target-workspace prerequisites.

For a development checkout, the owner may choose an editable installation:
`python -m pip install -e .`. The running server obtains its version exclusively
from installed `phase-gate-mcp` metadata. Source edits are usable after restart;
reinstall after changing package metadata. Missing/unreadable metadata is an error,
not a reason to infer a version from repository files.

For a previously absent server root, invoke `pgmcp --init` through that installed
environment after resolving the roots. It requires assembled package assets;
an editable checkout does not assemble them. Package preparation remains governed
by the [Release Assets Procedure](../reference/release-assets-procedure.md), outside
normal target setup.

For an existing root, follow the [upgrade guide](workspace-upgrade.md) and the
checklist's delta route. `--upgrade` renews managed templates; it does not migrate
owner config, native tool policy, state or host instructions. Do not run `--init`
to replace an existing root.

The unreleased branch-registration contract requires coordination to supply an
explicit parent for a **real** issue branch. Read the
[registration/recovery guidance](workspace-upgrade.md#unreleased-branch-registration-contract)
when adopting it; workspace initialization is not issue registration.

### Choose the workspace quality policy

Provision each required adapter's pinned native dependencies, then choose the native
policy for this workspace: source/test roots, language/platform versions, rules,
severities, exclusions and any native CLI arguments. Native discovery, a native
file, explicit schema/arguments or a capability requiring no extra policy are all
legitimate; pgmcp does not determine the effective native configuration for you.

The new defaults/checks.yaml, defaults/tests.yaml and defaults/fixes.yaml leave
acknowledgements null. Declare reviewed choices in root workspace overrides.
Initialization copies supplied assets without clearing choices; it does not make
arbitrary assets neutral. Unresolved choices permit startup/health but refuse
applicable quality execution. See [source composition](../reference/config-loading-architecture.md).

| configuration_choice | Owner declaration |
| --- | --- |
| null or omitted | Setup is unresolved; applicable use is refused |
| native_discovery | Deliberately accept the native tool's discovery behavior |
| configured_arguments | Deliberately use the binding's native argument policy |
| not_applicable | This capability needs no additional native policy configuration |

Record the choice only after reviewing the relevant binding. It does not prove
that a particular file exists or was consumed. Caller arguments still replace
configured defaults and are reported through args_source; they cannot acknowledge
an unresolved binding. A mixed applicable batch with an unresolved choice starts
no checks/tests/fixes. Scaffold and safe-edit enforce refuse writing when setup
prevents an obligation from starting. With a valid server startup basis,
`safe_edit_file(validation="report")` may instead perform a guarded edit of existing
configuration files while choices are unresolved. It returns `written=true` only
for a completed write and `validation_status=not_executed`, preserving each check's
reason without native invocation or validation scratch. Use this route for initial
configuration; then restart/reload the server as required and verify the chosen
bindings. Original-file and persistence errors still block the edit. Report also
retains its existing behavior for executed failed/unavailable check outcomes.

Use a small representative `run_checks(scope="targets", ...)` and, when needed,
a focused `run_tests(scope="targets", ...)` to verify the installed tool, intended
policy and target selection. Review the returned diagnostics before expanding
scope. Template-only renewal preserves the owner's bindings and does not reset
acknowledgements.

---

## 3. IDE Configuration: VS Code vs. Google Antigravity

There are critical structural differences in how **VS Code** and **Google Antigravity** handle MCP server registration and agent rules. Choose the section below corresponding to your IDE:

The host examples describe destination formats. Resolve supplied templates from
`<server-root>/agents/` (or `docs/agents/` in a checkout); adapt the launcher to the
chosen installed interpreter and roots. Use copies only for absent destinations.
For existing files, review and merge the relevant fields/instructions while
preserving unrelated settings. Do not copy a whole settings file over owner work.
The host's actual configuration support determines environment/path expansion.

### Option A: VS Code Setup

The supplied VS Code assets use these destinations:

| Supplied material | Workspace destination / action |
| --- | --- |
| `agents/vscode/copilot/mcp.json` | Review/adapt the PGMCP entry in `.vscode/mcp.json`; choose the exact interpreter, working directory and roots. |
| `agents/vscode/copilot/AGENTS.md` | Reconcile `AGENTS.md` with existing workspace rules. |
| Selected Copilot role/prompt files | Reconcile their corresponding `.github/` destinations; preserve unrelated files. |
| Always-on instruction setting | Add `"chat.useAgentsMdFile": true` to the existing settings object if this is the chosen instruction mechanism; do not replace the object. |

The supplied connection uses workspace/environment placeholders. Verify that the
installed host resolves them and delivers the intended token without exposing it;
otherwise use the owner's supported path/environment mechanism. Reload/reconnect
as needed and inspect actual startup and tool discovery.

### Option B: Google Antigravity Setup

The supplied Antigravity material is under `agents/antigravity/`: review
`mcp_config.json`, `AGENTS.md`, `rules/` and `workflows/`. The workspace-local
example destinations are `.agents/mcp_config.json`, root `AGENTS.md`,
`.agents/rules/` and `.agents/workflows/`.

Replace the launch-path placeholders with the chosen absolute interpreter/workspace
paths and use the installed host's actual MCP registration and environment delivery
mechanism. Keep credential values outside tracked files. Reconcile existing files
instead of overwriting them; inspect which instructions/roles the host really
loaded. Reload/relaunch and connect explicitly when required. File presence alone
does not prove automatic rule loading or MCP activation.

### Option C: Codex Setup

- Keep machine-specific paths and secrets in the Git-ignored `.codex/config.toml`.
- Set the existing PGMCP connection's client window to the approved value:

```toml
[mcp_servers.phase_gate_mcp]
tool_timeout_sec = 1800
```

- Preserve the connection's existing command, cwd, environment and other settings.
- Activate the changed setting in the Codex client connection; restarting only PGMCP does not prove activation.
- Keep normal check/test/fix calls focused and retain their configured default execution budgets.
- For the required full native-configured suite, use `run_tests(scope="configured", timeout_seconds=1200)`. Keep native execution arguments unchanged.
- The client window covers the complete MCP call, including adapter execution, bounded stopping and result delivery. Account for all selected bindings when choosing per-call budgets.
- Do not partition a required full run solely because its known workload exceeds a short default timeout. A timed-out or incomplete run remains incomplete evidence.
- Rationale: the client previously stopped waiting before the full-suite result could be delivered. The owner approved a 1800-second client window and a 1200-second full-test execution budget on 2026-10-04, superseding the [issue460 300-second/partition decision](https://github.com/MikeyVK/phase-gate-mcp/blob/8770607492aeb6d076dfe5aae1dc78f79515dd07/docs/development/issue460/validation.md#owner-decision--client-timeout-2026-09-26). Neither setting promises completion of an arbitrarily long run.

This tracked setup policy and the tracked AGENTS.md instructions survive cloning and branch integration. On every host using main, apply this policy to the local connection and activate it. A Git merge cannot update or activate a Git-ignored client configuration; retain existing machine paths and secrets.

## 4. Agent Files and Selected Host Instructions

The distributed source material is `docs/agents/` in a checkout and
`<server-root>/agents/` after initialization with those assets. Review the chosen
host's `AGENTS.md`, roles, workflows and, for Codex, supplied skills. Copy only
absent destinations; merge into existing instructions with owner changes preserved.
Use that host's actual invocation/discovery mechanism rather than assuming every
file is automatically loaded.

The repository's current agent protocol remains [AGENTS.md](https://github.com/MikeyVK/phase-gate-mcp/blob/main/AGENTS.md).
The checklist's invocation works by giving the installed/local document to a chosen
agent chat. A package install, copied role file or Git merge does not start that chat.

### Workspace Rule Synchronization

When owner changes affect equivalent instructions for more than one selected host,
reconcile those consumers deliberately and verify the host loaded the intended
revision. Installing all host variants or replacing their unrelated settings is not
a setup requirement. No instruction content changes are introduced by this guide.

---

## 5. Verification

Return to the [authoritative checklist's verification levels](agentic-bootstrap.md#4-activate-and-verify-three-separate-levels). Record actual health, configuration completeness for selected capabilities and representative successful operations separately. `health_check` does not establish the latter two; `/go` is an issue-phase workflow, not a workspace setup test. Do not create an invented issue to make either route available.

---

## Untracked Files Overview

| File | Description | Action |
|---|---|---|
| `.vscode/mcp.json` | Selected VS Code connection | Review the supplied VS Code template; copy only if absent, otherwise reconcile the existing entry |
| `.agents/mcp_config.json` | Antigravity local MCP config | Create under `.agents/` directory (Antigravity only) |
| `.codex/config.toml` | Codex local MCP config | Apply Option C; set tool_timeout_sec=1800 and activate the client connection |
| `GITHUB_TOKEN` | Credential when GitHub paths are selected | Deliver through the host environment/secret facility; never track its value |
| Launch environment | Selected Python environment | Install the chosen package and only intended native prerequisites; verify interpreter/package identity |



