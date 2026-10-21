<!-- docs/setup/agentic-bootstrap.md -->
<!-- template=generic_doc version=43c84181 created=2026-07-08T20:40Z updated= -->
# Agent-guided Workspace Setup and Upgrade

**Status:** Active  
**Version:** 2.3

**Last Updated:** 2026-10-21

## Purpose

This is the single entry document for agent-led PGMCP installation, workspace
configuration, instruction deployment and upgrades. Follow its sequence; linked
manuals explain particular steps and do not start separate setup routes. The
[manual reference](README.md) supplies runtime/host details and the
[upgrade guide](workspace-upgrade.md) supplies template checkpoint/recovery details.
They do not define separate completion checklists.

Installing a package, initializing a server root and obtaining a healthy server are
different facts. Completion applies only to the capabilities the owner chose and
the operations actually demonstrated.

## Invoke and Hand Over

Give this document, the selected artifact/version and the intended workspace to
an agent in the chosen environment. Start here before installation as well as after
`pgmcp --init` or `pgmcp --upgrade`. Pip and the CLI do not start an agent or hand
off a task automatically.

For an uninstalled wheel, this same document is the ZIP member
`mcp_server/assets/docs/setup/agentic-bootstrap.md`. Read it from the selected artifact;
do not substitute an unrelated latest-source guide. After package installation but
before initialization it is under the installed `mcp_server/assets/docs/setup/`.
For example, the selected environment's Python can locate it without starting MCP:

```text
<env-python> -c "from importlib.resources import files; print(files('mcp_server').joinpath('assets/docs/setup/agentic-bootstrap.md'))"
```

In a checkout, open `docs/setup/agentic-bootstrap.md`. In an initialized server
root, use `<server-root>/docs/setup/agentic-bootstrap.md` when that selected package
contains this guide. An older installed package keeps its own documentation;
opening the current source guide does not upgrade its behavior.

A host-independent invocation is:

> Follow the agent-guided workspace setup and upgrade checklist at the supplied
> path. Determine fresh setup or the upgrade delta, inspect existing configuration
> and preserve customizations. Establish my intended capabilities and unresolved
> workspace decisions before changing them. Use existing installation/init/upgrade
> primitives and host instructions. Do not initialize Git, commit/push on main,
> invent an issue or overwrite settings as a setup shortcut. Report each applicable
> item as done, open, blocked or N/A with decisions, operation evidence and limitations.

Use this checklist as the sole setup route. After fresh initialization or the
[explicit upgrade-source reconciliation](#32-reconcile-shared-sources), its current
operational source is `<server-root>/agents/agents.md`, with the three roles in
`agents/roles/` and named procedures in `agents/workflows/`. The agent investigates
the environment's real MCP, instruction, role and command/skill mechanisms and
agrees deployment with the owner. Change location, registration metadata or file
format only as required; preserve the shared instruction content and permissions.
Verify loading through the actual agent connection.

## Recommended Installation Unit: One Workspace

Prefer a workspace-specific installation: a dedicated Python environment and one
`.pgmcp/` server root per workspace, with its own configuration, templates, state,
logs and instruction deployment. The environment may be inside the workspace or
in a deliberately selected external location. Its package directory is never the
workspace identity. Do not silently reuse another workspace's environment or data.

Prefer workspace-scoped MCP registration when supported. If the host only offers a
user/global registry, register an explicitly workspace-bound connection with the
owner's chosen name and absolute roots; do not treat it as one shared mutable
server for unrelated workspaces. Multiple roles or hosts for the same workspace
may launch separate processes against that workspace's selected server root.
No server/runtime behavior is changed by this recommendation.

## 1. Establish the Target and Permissions

Record these inputs without printing secrets:

| Input | Decision or observation required |
| --- | --- |
| Mode | **Fresh** means no existing server root, even in an established repository. **Upgrade/delta** means preserve and reconcile an existing installation. |
| Package | Chosen release/candidate, trusted artifact location, supported Python/SDK requirements and installed version. Distinguish a released wheel from current source. |
| Intended capabilities | Which artifact/edit, quality, workflow/Git and GitHub operations the workspace wants; which are intentionally unused. Do not install every optional native tool. |
| Roots and host | Exact workspace, server-data, config and template roots; selected host, launcher interpreter, working directory and environment delivery. Prefer absolute configured roots to avoid ambiguity. |
| Existing owner data | Configuration overrides, native tool policy, templates, workspace adapters, instructions, client settings and state/checkpoints to preserve. |
| Change authority | Authorized paths and intended edits, approved disposable verification targets and any remote or destructive action requiring a separate owner decision. |

An unknown required choice is `open`; an unavailable prerequisite or failed action
is `blocked`. Use `N/A` only with a reason tied to the selected capability set.
Do not turn an unknown value into a copied acknowledgement or a guessed default.

## 2. Follow the Appropriate Installation Route

### Fresh setup

1. Inspect the chosen package's requirements and assets. Select its launch
   interpreter and environment; install only the package and intended native
   prerequisites using the [manual reference](README.md#2-python-virtual-environment).
   Installing an editable checkout does not assemble distributable assets. Diagnose
   dependency source-build failures separately; the manual records the bounded
   PyYAML installation option established by the external trial.
2. Resolve the intended roots before invoking the CLI. For a previously absent
   server root, run `pgmcp --init` using that exact environment. It copies the
   selected package's assets and establishes managed-template state. Review the
   actual copied configuration; initialization does not make arbitrary assets
   portable or erase their existing acknowledgements.
3. Complete the workspace decisions below, configure the connection using section
   3.1, reconcile current sources through section 3.2 and deploy through section
   3.3. Then activate and demonstrate the three verification levels in section 4.
4. If the repository or usable Git history needed by a selected workflow is
   absent, mark that path blocked and return it to the owner/coordination.
   Do not automatically run Git initialization, create a main commit or push.

### Existing workspace upgrade/delta

1. Record the existing package/interpreter, roots, owner customizations and
   relevant checkpoint/state before changing anything. Inspect the selected
   version's actual contract changes and create a deliberate recoverable backup
   where the planned owner changes require one.
2. Install the chosen package in its launch environment. Recreate an environment
   whose interpreter no longer satisfies that package. Compare only the affected
   defaults/contracts and owner overrides; preserve unrelated reviewed choices.
3. Reconcile owner configuration and public tool/state inputs deliberately.
   Follow the [composition contract](../reference/config-loading-architecture.md)
   and version-specific [upgrade notes](workspace-upgrade.md). A package change
   or this document does not migrate existing configuration automatically.
4. Use `pgmcp --upgrade` for managed-template renewal when required. It does not
   update owner configuration, workspace adapters or host instructions. Review
   its actual outcome. `checkpoint_required`/exit 2 needs an owner baseline or
   replacement decision; it is not activation success. Follow the upgrade
   guide's acceptance, backup and external-root rules. Do not use `--init` on
   an existing root or overwrite custom templates to silence the outcome.
5. Reconcile the selected package's shared instruction/document sources through
   [section 3.2](#32-reconcile-shared-sources) before reading/deploying the effective
   root's agent map. Package installation and template renewal do not perform
   this step on an existing root.
6. Revisit the decision rows affected by the delta, their dependencies and the
   resulting representative operations. Retain unaffected evidence with its
   version/scope and reason for reuse; an upgrade is not an instruction to reset
   every setting or re-run every check.

## 3. Review Workspace Decisions

The [configuration reference](../reference/server-configuration.md) and actual
selected package models own field meanings. Current source uses complete
`config_root/defaults/<file>.yaml` bases and optional root overrides; older
published packages do not acquire that layout through this checklist.

| Area | Required when applicable; record the owner's decision |
| --- | --- |
| Git and identity | For branch/commit/workflow use: repository, usable branch/HEAD, author identity and any signing policy. Review remote/base/branch conventions in `git.yaml`; coordination supplies the explicit parent when registering a **real** issue branch. No default main writes. |
| Workflow and enforcement | Review workflows, phase/tool admission and branch-lock/PR-status rules against intended use. Preserve protection; explain dependencies such as GitHub lookups even for a local edit. Change policy only through an explicit workspace decision, never as an automatic bypass. |
| Roots, artifacts and labels | Choose production/test/artifact roots, configured branch target sets, workflow scopes/types/priorities and relevant label declarations. Derive them from this workspace, not the pgmcp repository's example names. Review GitHub labels/permissions separately if remote workflows are selected. |
| Host and roles | Inspect actual registration and instruction/role/command capabilities. Deploy the shared agents protocol and the coordination, implementation and independent-QA roles through section 3.3 after source reconciliation. Agree the supported locations/formats with the owner; preserve content, permissions and existing settings. Keep machine paths and credentials outside tracked configuration. |
| Checks/tests/fixes | Review selected bindings, adapter IDs/capabilities, native pins/executables, source and test discovery, arguments, exclusions and intended native policy. Verify the real launch environment's `PATH` resolves the intended adapter programs; the server's absolute interpreter path does not select them. Confirm branch `configured_targets` separately from native configuration; tests/fixes retain their own selection contracts. |
| Response delivery | Choose `structured` or `resource` per connection from actual agent-visible capabilities. Demonstrate inline instructions, complete operation data through the chosen route and separate attachments. Neither healthy startup nor client UI visibility proves the agent received those fields. See the [shared mode guidance](README.md#choose-the-response-mode). |
| Quality acknowledgement | Set each applicable `configuration_choice` only after that review. Missing/null may permit health but refuse selected quality use. An acknowledgement does not prove native configuration was consumed. Follow the [quality policy reference](README.md#choose-the-workspace-quality-policy). |
| GitHub, if selected | Set explicit owner/repo and optional project metadata in `github.yaml`; deliver the token through the host environment/secret facility where possible. A configured-token alternative must remain outside tracked artifacts. Verify remote identity and permissions rather than inferring them from Git remotes or the token holder. See [GitHub setup](../manuals/github-setup.md). |

Without a token some credential-dependent tools/resources are not exposed; other
GitHub-dependent paths and enforcement can still refuse a call. Inspect actual
tool discovery and operation results instead of assuming a healthy server enables
every GitHub operation.

### 3.1 Configure the Workspace Server Connection

Use the [runtime reference](README.md) and
[field reference](../reference/server-configuration.md) for meanings, not a
prebuilt host-specific launcher. Inspect the active host's supported configuration,
registration scope, environment delivery and activation mechanism.

| Layer | Where the selected values belong | What to set or verify |
| --- | --- | --- |
| Host connection | The actual MCP registry/settings supported by the environment | Exact environment Python; module `mcp_server.core.proxy`; workspace working directory; absolute `PGMCP_WORKSPACE_ROOT`; selected `PGMCP_SERVER_PROJECT_DIR` (normally `.pgmcp`). |
| Adapter executable environment | That connection's actual inherited/explicit `PATH` | Resolve selected programs from their intended environment at declared pins. Preserve other required entries; an absolute server interpreter does not change `PATH`. |
| Workspace policy | `<server-root>/config/defaults/<file>.yaml` plus optional root overrides `config/<file>.yaml` | Preserve the packaged basis; write reviewed workspace differences in overrides. Use the composition contract; do not copy the PGMCP repository's overrides. |
| Startup timing | `config/defaults/server.yaml` and optional root `config/server.yaml` | Validate lock/proxy timing through this startup-policy schema; align the outer host deadline. This file is not the host's MCP registry or a launcher `server:`/`logging:` overlay. |
| Response delivery | `PGMCP_RESPONSE_MODE` on this connection when needed | Select `structured` or `resource` from demonstrated agent access; preserve inline instructions and separate attachments. |
| GitHub, if selected | Workspace `github.yaml`; token through environment/secret facility where possible | Explicit owner/repo and required permissions; keep tokens outside tracked files and output. Do not put identity in the launcher. |

Omit root overrides that are not needed. Preserve unresolved quality choices as
null until the intended binding/native policy is reviewed; this can allow health
while refusing applicable quality use. Prefer the default workspace-contained
config/template roots; choose external roots only deliberately and record them.
If the host cannot express a necessary launch value, mark the connection blocked
instead of falling back to ambient CWD or another workspace's server.

### 3.2 Reconcile Shared Sources

Before host deployment, establish the current instruction/document source from
the **exact selected package**. The wheel contains it under `mcp_server/assets/`;
the selected installed distribution contains the same `assets/` directory.
Locate it with that environment's interpreter, without starting MCP:

```text
<env-python> -c "from importlib.resources import files; print(files('mcp_server').joinpath('assets'))"
```

Record the selected package/version and asset location. Do not substitute this
development repository or another environment. Installing a wheel updates package
assets; template-only `--upgrade` does not copy shared sources into an existing
server root. Fresh `--init` copies them only into a previously absent root.

Stage and inspect the applicable package sources, then reconcile them to the
effective server-root locations used by the shared protocol:

| Selected package asset | Effective source before deployment |
| --- | --- |
| `assets/agents/` | `<server-root>/agents/`, retaining the complete general protocol, three roles and five named procedures together. |
| `assets/docs/` | Applicable current guides, standards, manuals and references under `<server-root>/docs/`, preserving their relative layout and the sources referenced by the protocol. |
| `assets/README.md`, `CHANGELOG.md`, `LICENSE` | Corresponding files beside `<server-root>/docs/` when supplied by the selected package. These are server-data files, not the workspace project's own root files. |

For a fresh root whose copied sources already match the selected package, record
that fact and avoid another copy. For an upgrade, compare package-owned paths with
existing files, preserve owner additions and unrelated files, and make the intended
changes explicit. Back up customized files before an authorized replacement;
surface unresolved content/authority conflicts to the owner. Do not blindly mirror
or delete an existing directory, modify installed package assets, or copy the whole
asset root over populated config, state, templates or recovery material.

Verify that the effective `agents/` map and its required `docs/` reading paths
contain the current reviewed sources; record source → effective path and any
owner reconciliation. Missing/currently conflicting sources block the affected
deployment, rather than falling back to old copied instructions. This source
reconciliation does not register host files, activate roles or refresh runtime
configuration. Continue to host deployment only after it is complete.

### 3.3 Deploy the Shared Agents Map

After [source reconciliation](#32-reconcile-shared-sources), read the current
`<server-root>/agents/agents.md` and all three role protocols before choosing
host destinations. Inspect actual host documentation/capabilities for always-on
instructions, separate role sessions and command/skill invocation. Do not infer
registration from a familiar directory name or from copied files.

| Source under `<server-root>/agents/` | Required deployment result |
| --- | --- |
| `agents.md` | The shared general protocol is loaded for PGMCP work through the host's supported instruction mechanism. |
| `roles/co.md` | A coordination role with its lifecycle/issue authority and limits. |
| `roles/imp.md` | An implementation role consuming active phase instructions on initialized branches. |
| `roles/qa.md` | A separate, read-only independent review role; producer-delegated findings do not become GO/NOGO authority. |
| `workflows/start.md`, `go.md` | Discoverable session-start/active-phase procedures with their existing invocation modes and stop conditions. |
| `workflows/create-issue.md`, `start-issue.md`, `end-issue.md` | Discoverable coordination lifecycle procedures, preserving explicit human authorization and ownership. |

Record source → deployed destination → activation mechanism for each row.
Use references to the shared source when the host supports them; otherwise create
a traceable local derived file, adapting only required frontmatter, extension,
path references or registration. Preserve operating content, tool restrictions,
role authority and stop conditions. Keep this generic source as the maintained
truth; do not author another per-host policy variant. Preserve owner additions
and reconcile existing files rather than replacing them wholesale.

Validate all deployed links against the actual server root. Make the three role
boundaries and commands available through separate sessions, role facilities,
skills or explicit prompt invocation supported by this environment. A host without
native role/command files can use explicit document invocation; it still must
preserve independent QA. If a required boundary cannot be implemented, report that
limitation and ask the owner before changing the model.

After activation demonstrate that the real agent can access the general protocol,
adopt each named role with its boundaries and invoke a named procedure. Read-only
activation/acknowledgement is sufficient for deployment proof; do not merge a PR
or invent an issue just to exercise a command. Phase-specific instructions remain
in the workflow configuration and `get_work_context`; do not copy them into local
skills. During later upgrade/delta work revisit only affected sources and deployed
copies; initialization does not automatically install host registrations.

Before a usable MCP connection exists, preparation remains owner-controlled through
the documented installation/configuration route. After connection, use the existing
pgmcp tools. With a valid startup basis, `safe_edit_file(validation="report")` can
guard an existing config edit when quality setup is unresolved; `written=true` and
`validation_status=not_executed` are distinct facts. It does not bypass admission,
original-file safety or persistence failures. See the [editing reference](../reference/tools/editing.md).

## 4. Activate and Verify Three Separate Levels

Restart after package, active-suite or startup-loaded configuration changes using
the existing `restart_server` route when available. Reconnect/refresh client tool
discovery; an interpreter or launch-environment change may require a full host
relaunch. A [startup-policy change](../reference/server-configuration.md#startup-admission-policy)
requires full proxy/child relaunch, rather than child-only restart_server. A restart
acknowledgement is not evidence of the newly loaded process.

Verify the selected launcher interpreter, installed package version/module location
and resolved roots in that launch context, without dumping environment variables or
tokens. For example, run this read-only inspection with the exact launcher Python,
working directory and environment (replace the example executable):

```powershell
& 'C:/chosen/environment/Scripts/python.exe' -c "import sys, shutil, mcp_server; from importlib.metadata import version; from mcp_server.config.settings import Settings; s=Settings.from_env().server; print(sys.executable); print(sys.version); print(version('phase-gate-mcp')); print(mcp_server.__file__); print(s.workspace_root); print(s.resolved_server_root); print(s.resolved_config_root); print(s.resolved_template_root); print(shutil.which('python'))"
```

That command proves its own process context, not a different running server.
Compare it with the live child process/launcher and health PID/version using the
host's available inspection facilities. If live identity or roots cannot be
verified, retain that limitation as open; do not infer them from health alone.

| Level | Evidence required |
| --- | --- |
| **Health** | Actual `health_check` result after activation, new process identity where applicable and no unresolved startup diagnosis. Repair diagnosed setup explicitly and restart again when needed. |
| **Configuration completeness** | All decisions/prerequisites needed by the selected capabilities are resolved, actual tool discovery matches intent, native policy and owner overrides are reviewed. Optional unused areas have a reasoned N/A. |
| **Representative operations** | At least a successful narrow operation for each intended capability family, with actual selection, arguments and outcome. Listing a tool, a health pass or a schema read alone does not prove a check/test/fix/write/remote action works. |

Use existing operations with actual registered IDs and owner-approved targets:
read a real Git status or authorized GitHub object; inspect `scaffold_schema`
before an authorized scratch scaffold; run a named check/test on a representative
target; exercise an intended fix/edit only on an approved disposable target and
inspect the write/diff as well as validation. No-applicable, skipped, refused,
not-executed, timed-out and incomplete outcomes are not passes. Remote or destructive
verification needs its own authority; if it is not authorized, report the relevant
capability as unverified rather than performing it.

`pgmcp --init` initializes workspace assets; `initialize_project` registers a real
issue branch in its configured workflow. Never invent an issue number/title to
test setup, create branch state merely for health or use `get_work_context` as a
replacement for health. For real issue work, coordination creates/checks out and
initializes the branch with its explicit parent before implementation starts.

## 5. Return a Durable Setup/Upgrade Hand-over

Record the selected version, mode, safe root/host identities and intended
capabilities. Then provide one row per applicable decision/verification:

| Item / capability | Status | Decision / delta | Evidence | Remaining action / limitation |
| --- | --- | --- | --- | --- |
| Replace with the actual item | done / open / blocked / N/A | Explicit choice or unchanged reviewed value | Safe invocation, scope and observed outcome, or durable evidence link | Owner/action needed, failure or justified N/A |

Mark `done` only for the fact actually established. Keep secrets out of the record.
Transient run IDs/resources may supplement exact invocations/outcomes, not replace
durable evidence. Summarize health, selected-capability completeness and operation
results separately, name blockers/owners and identify what must be revisited after
a future delta. Do not call the entire workspace ready while a selected capability
remains unverified or blocked. Hand real issue lifecycle work back to coordination.

## Related Documentation

- [Manual runtime/host reference](README.md)
- [Owner-led upgrade and template recovery](workspace-upgrade.md)
- [Current source configuration contract](../reference/config-loading-architecture.md)
- [Current source runtime declarations](https://github.com/MikeyVK/phase-gate-mcp/blob/main/pyproject.toml)

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.3 | 2026-10-11 | @imp implementer | Target prepared v3 package; distinguish reviewed wheel installation, owner configuration, native prerequisites, suite renewal and server/client activation without claiming publication |
| 1.2 | 2026-10-01 | Implementation documenter | Describe current template_suite/checkpoint renewal, owner-led baseline handling and restart; retain complete-package assumption |
| 1.1 | 2026-07-20 | Agent | Document .version file creation during CLI init |
| 1.0 | 2026-07-08 | Agent | Initial draft |
| 1.4 | 2026-10-16 | @imp documenter | Separate unchanged 3.0.0 package setup from deliberate adoption of unreleased layered configuration. |
| 1.5 | 2026-10-17 | @imp documenter | Require the selected interpreter to satisfy the chosen package before creating its launch environment; link current prerequisites. |
| 2.0 | 2026-10-17 | @imp documenter | Replace unsafe automatic bootstrap with the authoritative fresh/upgrade checklist, explicit invocation, owner decisions and separate readiness evidence. |
| 2.1 | 2026-10-21 | @imp implementer | Apply external installation feedback through shared dependency, executable-resolution, capability-based instruction placement and response-delivery guidance. |
| 2.2 | 2026-10-21 | @imp implementer | Make this the sole installation/deployment route; prefer workspace-bound setup and explicitly map complete shared protocols, roles and procedures into actual host capabilities. |
| 2.3 | 2026-10-21 | @imp documenter | Close the upgrade-source handoff: locate exact package agents/docs, reconcile effective root sources with owner preservation, then deploy/activate through the host. |
