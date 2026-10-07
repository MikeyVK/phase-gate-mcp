<!-- docs\reference\mcp\release-assets-procedure.md -->
<!-- template=generic_doc version=43c84181 created=2026-07-05T20:37Z updated= -->
# Reference Guide: Release Assets Procedure and Manifest Specification

**Status:** ACTIVE  
**Version:** 1.1  
**Last Updated:** 2026-10-07

---

## Purpose

Specify the folder structure, manifest format, and build-time synchronization procedure for packaging default configuration assets, the v3 template suite, agent instructions, and workflows into the installable pip wheel.

## Prerequisites

Read these first:
1. docs/setup/README.md
---

## Summary

Defines a strict build-time copy regime from the workspace sources (including docs/agents/ and slash commands) to mcp_server/assets/ driven by a release_manifest.yaml, ensuring a clean and IDE-agnostic bootstrapping process.

---

- Define docs/agents/ as the SSOT for rules and slash commands
- Introduce release_manifest.yaml to declare release-bound files
- Automate assets folder compilation in the package build pipeline

---

## 1. Specification: Agent Instruction Sources (SSOT)

To avoid duplication debt across host-specific layouts, the repository designates
`docs/agents/` as the single source of truth for distributable agent instructions,
workflows, and Codex skills:

```text
docs/agents/
├── antigravity/                   # Google Antigravity instructions and workflows
├── vscode/
│   └── copilot/                   # VS Code/Copilot agents and prompts
└── codex/                         # Codex rules, workflows, and discoverable skills
```

Each host directory preserves the structure needed to deploy that host's active files.
Local MCP connection configuration, absolute workspace paths, credentials, runtime
state, and other machine-specific settings are not part of this SSOT.

### 1.1. Local Development Synchronization (Dev Sync)

Authoritative changes are made under the appropriate `docs/agents/<host>/` directory
and are then deployed to the host's active runtime locations:

- `docs/agents/antigravity/` → the active Antigravity rules and workflows.
- `docs/agents/vscode/copilot/` → `AGENTS.md`, `.github/agents/`, and
  `.github/prompts/`.
- `docs/agents/codex/` → `.agents/`, excluding local files such as
  `mcp_config.json`.

Active runtime copies may remain version-controlled when the host requires them in a
repository checkout, but they are derived copies and must remain byte-equivalent to
their authoritative source. The build manifest packages `docs/agents/` directly; it
does not package active runtime locations.

---

## 2. Release Manifest Specification (`release_manifest.yaml`)

The authoritative manifest is `.pgmcp/config/release_manifest.yaml`. The current
manifest maps these repository sources into `mcp_server/assets/`:

```yaml
assets:
  - source: ".pgmcp/config"
    target: "config"
  - source: ".pgmcp/template_suite"
    target: "template_suite"
  - source: "docs/agents"
    target: "agents"
  - source: "docs/coding_standards"
    target: "docs/coding_standards"
  - source: "docs/manuals"
    target: "docs/manuals"
  - source: "docs/reference"
    target: "docs/reference"
  - source: "docs/development/schema-template-maintenance.md"
    target: "docs/development/schema-template-maintenance.md"
  - source: "docs/setup"
    target: "docs/setup"
  - source: "CHANGELOG.md"
    target: "docs/CHANGELOG.md"
  - source: "README.md"
    target: "docs/README.md"
  - source: "LICENSE"
    target: "LICENSE"
```

The single active maintenance guide is included at its existing documentation path so the template library and identity guides retain a delivered reading route. This mapping does not include the development archive or issue reports. Before distributing new or changed template packages, follow its [development and release review](../development/schema-template-maintenance.md#develop-and-release-a-package); asset assembly does not itself establish semantic conformance.

The repository manifest is the source of truth for package asset mappings. Keep
consumer copies of host instructions synchronized with their declared direct-copy
sources; build assets are generated outputs, not separately edited sources.

Official adapters are authored under `mcp_server/bundled_adapters/` and remain in
that package path in the wheel. They are package data, not release-manifest assets,
and are never copied into a workspace's `.pgmcp/` root. Workspace adapters and
workspace-owned configuration remain outside the build input.

---

## 3. Build-Time Assembly Procedure

During the Python wheel compilation step:
1. The packaging utility clears `mcp_server/assets/` completely.
2. It parses `release_manifest.yaml`.
3. It copies specified paths from the repository sources to the subdirectories under `mcp_server/assets/`.
4. The `pyproject.toml` file bundles `mcp_server/assets/` and `mcp_server/bundled_adapters/` via `package-data`, including nested files and dotfiles, resulting in a clean standalone wheel.

---

## 4. Bootstrapping and renewal

### 4.1 Fresh initialization (`pgmcp --init`)

`pgmcp --init` resolves the server root from `PGMCP_WORKSPACE_ROOT` and
`PGMCP_SERVER_PROJECT_DIR` (default: `<workspace>/.pgmcp`). It exits with an error if
that resolved root already exists. Otherwise, it creates the root, copies packaged
assets into it, then runs the normal renewal operation to validate the active suite and
publish installation state. This is fresh initialization, not an in-place migration.

The asset copy is rooted at the resolved server root; do not describe it as always
writing to a literal `.pgmcp/` or as a general guarantee about unrelated workspace
paths. An explicit `PGMCP_CONFIG_ROOT` remains the effective owner-managed configuration
root, and `PGMCP_TEMPLATE_ROOT` selects the active suite root when set. External roots
remain owner-controlled. Defaults shipped in the wheel seed a fresh installation and
serve as references for an explicit migration; they do not silently replace populated
configuration.

Official adapter packages remain in `mcp_server/bundled_adapters/` inside the wheel and
are not copied into the workspace. Their native executables are installed and maintained
by the environment owner. Renewal does not install or probe those dependencies.

### 4.2 Existing pre-v3 workspace

For an existing workspace, use `pgmcp --upgrade`, not `--init`. On first v3 suite
migration, the command preserves the existing actual suite, stages and validates the
candidate, and may report `checkpoint_required` with exit code 2. That result requires an
owner decision; it does not activate the candidate or authorize configuration overwrite.

For a managed root, `--force-template-upgrade` performs a verified backup before
replacing the complete suite. If local customization must be retained, reconcile a
complete valid v3 suite first, then use `--accept-template-baseline` to acknowledge the
baseline without copying candidate files over that suite. For an external template root,
the external owner controls the equivalent migration and checkpoint decision; PGMCP does
not assume force-replacement authority.

There is no automatic external rollout or deployment in this procedure. After a package
install, active suite change, or startup-loaded configuration change, restart the MCP
server. A change to launch environment variables may require closing and relaunching the
client so the proxy and child server inherit the new environment. No health-first gate is
part of this procedure.

---

## Related Documentation

- [Workspace upgrade guide](../setup/workspace-upgrade.md)
- [Developer isolation guide](../setup/dev-isolation.md)
- [Server configuration](server-configuration.md)
- **[docs/manuals/user-guide.md][related-1]**
- **[Adding a First-Class Workflow][related-2]**

<!-- Link definitions -->

[related-1]: ../manuals/user-guide.md
[related-2]: workflow-extension-guide.md

---

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-07-05 | Agent | Initial draft |
| 1.0.0 | 2026-07-08 | Agent | Document build automation, manifest paths, and schema matching implementation #420 |
| 1.1 | 2026-10-07 | @imp documenter | Include the active template maintenance guide as one asset and connect package review to distribution without changing activation behavior. |
