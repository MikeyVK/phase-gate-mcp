<!-- docs/setup/agentic-bootstrap.md -->
<!-- template=generic_doc version=43c84181 created=2026-07-08T20:40Z updated= -->
# Agent-guided Workspace Setup and Upgrade

**Status:** Active  
**Version:** 2.0  
**Last Updated:** 2026-10-17

## Purpose

This is the authoritative agent-facing setup and upgrade checklist. The
[manual reference](README.md) supplies runtime/host details and the
[upgrade guide](workspace-upgrade.md) supplies template checkpoint/recovery details.
They do not define separate completion checklists.

Installing a package, initializing a server root and obtaining a healthy server are
different facts. Completion applies only to the capabilities the owner chose and
the operations actually demonstrated.

## Invoke and Hand Over

After installation, `pgmcp --init` or `pgmcp --upgrade`, explicitly open or resume
an agent chat in the intended workspace and give it this document. Pip and the CLI
do not start an agent or hand off a task automatically.

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

Use the selected host's existing role/instruction mechanism; no new setup role,
skill or CLI mode is required. In a checkout the distributable host sources are
under `docs/agents/`; after initialization their supplied copies are under
`<server-root>/agents/`. Review the selected host's files before deploying them
and reconcile them with existing instructions rather than copying over owner work.

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
   Installing an editable checkout does not assemble distributable assets.
2. Resolve the intended roots before invoking the CLI. For a previously absent
   server root, run `pgmcp --init` using that exact environment. It copies the
   selected package's assets and establishes managed-template state. Review the
   actual copied configuration; initialization does not make arbitrary assets
   portable or erase their existing acknowledgements.
3. Complete the workspace decisions below, reconcile the chosen host's launcher
   and instructions, then start/connect it explicitly.
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
5. Revisit the decision rows affected by the delta, their dependencies and the
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
| Host and roles | Reconcile the chosen host's MCP connection, instruction/role/workflow files and existing local settings field by field. Keep machine paths and credentials out of tracked configuration; preserve unrelated settings. Use the existing coordination/implementation/independent-QA division where selected. |
| Checks/tests/fixes | Review selected bindings, adapter IDs/capabilities, native pins/executables, source and test discovery, arguments, exclusions and intended native policy. Confirm branch `configured_targets` separately from native configuration; tests/fixes retain their own selection contracts. |
| Quality acknowledgement | Set each applicable `configuration_choice` only after that review. Missing/null may permit health but refuse selected quality use. An acknowledgement does not prove native configuration was consumed. Follow the [quality policy reference](README.md#choose-the-workspace-quality-policy). |
| GitHub, if selected | Set explicit owner/repo and optional project metadata in `github.yaml`; deliver the token through the host environment/secret facility where possible. A configured-token alternative must remain outside tracked artifacts. Verify remote identity and permissions rather than inferring them from Git remotes or the token holder. See [GitHub setup](../manuals/github-setup.md). |

Without a token some credential-dependent tools/resources are not exposed; other
GitHub-dependent paths and enforcement can still refuse a call. Inspect actual
tool discovery and operation results instead of assuming a healthy server enables
every GitHub operation.

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
& 'C:/chosen/environment/Scripts/python.exe' -c "import sys, mcp_server; from importlib.metadata import version; from mcp_server.config.settings import Settings; s=Settings.from_env().server; print(sys.executable); print(sys.version); print(version('phase-gate-mcp')); print(mcp_server.__file__); print(s.workspace_root); print(s.resolved_server_root); print(s.resolved_config_root); print(s.resolved_template_root)"
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
