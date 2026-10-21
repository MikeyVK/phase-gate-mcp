# Setup — Runtime and Host Reference

For agent-led setup or an upgrade, start with the single
[workspace checklist](agentic-bootstrap.md). Use the checklist supplied by the selected package; an existing
server root can retain older copied guides after a package upgrade. Explicitly give
the current page to the chosen agent chat; installation, `--init` and `--upgrade`
do not launch an agent. This page supplies technical details, not a separate
readiness procedure.

Prefer the workspace-specific installation unit described by the checklist: one
selected environment, one workspace server root and explicitly bound host connections.
This reference supplies details for that route; it is not another entry procedure.

## Prerequisites

- Select a Python interpreter supported by the chosen package. Current source
  requires Python 3.15+ and MCP SDK `==2.3.0`; its
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
& 'C:/chosen/pgmcp-env/Scripts/python.exe' -m pip install 'C:/reviewed/phase_gate_mcp-4.0.0-py3-none-any.whl'
```

The example names a wheel, not a promise of PyPI availability or newly published
assets. An existing virtual environment retains its original interpreter; recreate
it when that interpreter no longer satisfies the chosen package. Install only
native tools needed by the selected bindings, at the versions their adapters
declare. Development requirements are for contributors who deliberately select
that environment, not unconditional target-workspace prerequisites.

### Dependency source builds

A portable PGMCP wheel does not guarantee binary wheels for every pinned dependency
on every supported Python/platform combination. In the external Python 3.15.1 Windows
trial, PyYAML 6.0.3 selected a source build and its optional extension failed without
the native build prerequisites. The agent completed installation with
`PYYAML_FORCE_LIBYAML=0`, which explicitly disables that optional extension in
[PyYAML 6.0.3's build contract](https://github.com/yaml/pyyaml/blob/6.0.3/setup.py).

When that specific failure occurs, either provision the native build prerequisites
or retry with that variable set to `0` only for the installation process and its
children. For example, replace the two placeholders below with the chosen
environment interpreter and wheel path:

```text
<env-python> -c "import os, subprocess, sys; e = os.environ.copy(); e['PYYAML_FORCE_LIBYAML'] = '0'; subprocess.run([sys.executable, '-m', 'pip', 'install', sys.argv[1]], env=e, check=True)" <wheel-path>
```

This keeps the declared dependency pins and Python requirement intact. Do not use
`--ignore-requires-python` or omit required dependencies to obtain an apparent pass.
Other dependency failures need their own diagnosis.

### Choose adapter executable paths

The proxy's absolute Python path selects the server interpreter. Adapter entrypoints
such as `executable: python` are resolved separately through the launch process's
`PATH`; see the [bootstrap resolver](https://github.com/MikeyVK/phase-gate-mcp/blob/main/mcp_server/bootstrap.py)
and [Python syntax entrypoint](https://github.com/MikeyVK/phase-gate-mcp/blob/main/mcp_server/bundled_adapters/python_syntax/manifest.yaml).
Launching an environment's Python directly does not itself prepend that environment's
executable directory to `PATH`.

Set the connection's actual launch environment so the intended executable directories
precede other candidates while preserving required existing entries. A virtual
environment normally uses `Scripts` on Windows or `bin` on POSIX, with the platform's
path separator. Review this against each selected adapter's native executable and pin.
Do not assume the host expands shell placeholders or inherits an activated terminal.

Verify the resolved programs and versions in the same environment as the real
connection, then demonstrate the selected check. A healthy server alone does not
prove which interpreter or executable an adapter will run. This is launcher setup;
it introduces no automatic interpreter fallback or adapter change. See the
[Python virtual-environment reference](https://docs.python.org/3/library/venv.html#how-venvs-work).

For a development checkout, the owner may choose an editable installation:
`python -m pip install -e .`. The running server obtains its version exclusively
from installed `phase-gate-mcp` metadata. Source edits are usable after restart;
reinstall after changing package metadata. Missing/unreadable metadata is an error,
not a reason to infer a version from repository files.

For a previously absent server root, invoke `pgmcp --init` through that installed
environment after resolving the roots. It requires assembled package assets;
an editable checkout does not assemble them. Package preparation remains governed
by the [Release Assets Procedure](https://github.com/MikeyVK/phase-gate-mcp/blob/main/docs/reference/release-assets-procedure.md), outside
normal target setup.

For an existing root, follow the [upgrade guide](workspace-upgrade.md) and the
checklist's delta route. `--upgrade` renews managed templates; it does not migrate
owner config, native tool policy, state or host instructions. Do not run `--init`
to replace an existing root.

The unreleased branch-registration contract requires coordination to supply an
explicit parent for a **real** issue branch. Read the
[registration/recovery guidance](workspace-upgrade.md#branch-registration-contract)
when adopting it; workspace initialization is not issue registration.

### Choose startup budgets

Normal proxy/server startup requires `defaults/server.yaml` under the effective config
root. Fresh `--init` installs it from current package assets; existing workspaces must
explicitly install/reconcile it because `--upgrade` remains template-only. Optional
root `server.yaml` contains workspace differences. The default policy is a 30-second
lock retry budget, 0.25-second interval and 60-second proxy initialize deadline.
See [the authoritative startup policy and migration note](../reference/server-configuration.md#startup-admission-policy).
A policy change requires full proxy/child relaunch; child-only `restart_server` retains
the old proxy deadline. Allow outer client startup margin (recommended 75 seconds).

### Choose the response mode

Presentation configuration version 2.0.0 requires `global.response_mode` in
`defaults/presentation.yaml`; root `presentation.yaml` holds workspace differences.
Reconcile configuration when adopting this clean contract change; `--upgrade`
remains template-only and does not migrate owner configuration.

| Mode | Agent-visible result |
| --- | --- |
| `structured` (shipped default) | Bounded inline text plus complete operation and full rendered guidance in `structuredContent`; separate native resource attachments. |
| `resource` | Bounded inline text with a successful operation-cache URI; separate native resource attachments, no normal `structuredContent` or `outputSchema`. |

Inline text ends with the appropriate full-data notice and, when applicable, a
generic notice for the supplied attachments. Attachment metadata in structured output
refers to the separate blocks without duplicating their bodies. A `schema://` attachment
identity does not by itself register a resource reader. Full operation JSON is never
appended to inline text.

Choose `PGMCP_RESPONSE_MODE=structured` or `PGMCP_RESPONSE_MODE=resource` in each
individual MCP launch environment when the shared default is unsuitable. An explicit
environment selector overrides launcher `server.response_mode`; omission uses
`global.response_mode`. Empty/unknown values reject healthy startup. There are no
old-selector aliases or independent presentation/data/channel profiles.

Selection is process-local: different hosts/chats can share one workspace without
editing shared configuration to switch another connection. No host/model detection
is performed. Shared budgets remain in presentation configuration; normal inline text
is finally limited to `max_text_response_bytes` (default 8000 UTF-8 bytes), including
footer, shortening notice and fence closure. A too-small configured reserve is rejected.
Structured presentation/data, attachments and total response size are outside that cap.
Instruction shortening is explicitly signalled; the resource cache stores operation
facts and does not add a copy of rendered instructions.

Choose by demonstrated capability, without assigning modes to host brands: use
`structured` when the actual agent receives its complete structured envelope; use
`resource` when it can read the returned cache URI through the same connection.
In either case verify inline instructions and separate attachments reach the agent.
A visible client UI attachment alone does not prove model access. If a bridge drops
structured data, try the existing resource route and demonstrate a real readback;
if neither route works, report setup blocked rather than claiming full output access.

After a mode change, relaunch the selected connection and refresh `tools/list`;
normal output-schema presence follows the selected mode. Verify that the actual agent
receives the explanation and phase instructions and can retrieve the complete operation
and separate attachments through the selected route. Server publication alone does not
prove downstream model input. For resource mode use the same server connection's cache
reader and [paging guide](../../mcp_server/resources/cache_reading.md).

Startup recovery remains a fixed exception: complete recovery text in both channels
and full inline diagnosis, without rejected configuration, mode selection or cache.
Confirm healthy admission after repair/restart before judging normal mode behavior.

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

## 3. Connect Through the Available Host Capabilities

Inspect the chosen environment's actual MCP registration and launch support. The
agent and owner select the supported configuration file or settings surface,
scope and format; this guide does not prescribe host directories or ship
host-specific launcher/rule/skill variants. The uniform source is the installed
`<server-root>/agents/` map, deployed through the checklist's section 3.3 after source reconciliation.

Configure one connection with the exact environment interpreter, module
`mcp_server.core.proxy`, working directory and explicit workspace root. Deliver
the selected response mode, executable search path and credentials through the
host's supported environment/secret mechanism. Preserve unrelated entries.
Do not assume a copied JSON file is loaded or that environment placeholders expand.

Set the outer client startup budget above the proxy initialization deadline; the
default policy recommends at least 75 seconds. Size the tool-call window for native
execution, bounded stopping and response delivery. The PGMCP development workspace
uses an owner-approved 1800-second client window with a 1200-second configured
full-suite call; another workspace chooses values for its actual workload and
host capabilities. Keep focused calls focused, retain native arguments, and report
timed-out/incomplete runs honestly. See [execution budgets](../coding_standards/QUALITY_GATES.md).
Activate connection changes and refresh discovery; child-only server restart does
not establish a changed host launcher or client timeout.

## 4. Place Shared Instructions Using the Available Capabilities

Use the [shared setup checklist](agentic-bootstrap.md) as the installation entry.
Review [shared role and review responsibilities](../reference/copilot-agent-instructions-model.md)
and the supplied coding standards with the owner. The agent determines how the
chosen environment can expose those instructions and support the intended roles,
then agrees what files, formats, locations and invocation are needed.

Reference shared material rather than maintaining copied instruction sets for each
host. Resolve documentation references against the actual selected server root;
discard example project assumptions. Preserve owner instructions and settings.
Inspect what the agent actually loads; file presence or package installation alone
does not establish instruction activation. If the environment cannot support a
selected role or independent review boundary, report that limitation for an owner
decision rather than weakening it silently.

The complete generic instruction source is authored under `docs/agents/shared/`
and installed as `<server-root>/agents/`: `agents.md`, three role protocols and
five workflow procedures. The checklist owns their deployment and activation.
Other source-workspace host examples under `docs/agents/` are not installed assets.
No automatic deployment, migration or deletion of owner-managed host files occurs.

---

## 5. Verification

Return to the [authoritative checklist's verification levels](agentic-bootstrap.md#4-activate-and-verify-three-separate-levels). Record actual health, configuration completeness for selected capabilities and representative successful operations separately. `health_check` does not establish the latter two; `/go` is an issue-phase workflow, not a workspace setup test. Do not create an invented issue to make either route available.

---

## Local Configuration and Secrets

| Item | Action |
| --- | --- |
| Selected host's active MCP configuration | Choose the supported location/scope; preserve other connections and keep machine paths/secrets outside tracked files. |
| Selected instruction surface | Agree files/formats/locations with the owner and verify actual agent loading of shared rules. |
| `GITHUB_TOKEN`, when selected | Deliver through the host environment/secret facility; never track its value. |
| Launch environment | Verify interpreter/package identity, adapter executable resolution and intended native prerequisites. |
