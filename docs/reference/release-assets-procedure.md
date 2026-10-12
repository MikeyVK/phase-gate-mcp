<!-- docs\reference\mcp\release-assets-procedure.md -->
<!-- template=generic_doc version=43c84181 created=2026-07-05T20:37Z updated= -->
# Reference Guide: Release Assets Procedure and Manifest Specification

**Status:** ACTIVE  
**Version:** 1.2  
**Last Updated:** 2026-10-11

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

### 3.1 Prepare reviewable release artifacts

GitHub Releases is the selected publication destination for 1.0.0, 2.0.0 and 3.0.0.
Prepare a wheel and source distribution (sdist) for each version. PyPI publication
is outside this procedure's approved scope. Run the existing
`scripts/build_package.py` assembly before building; the sdist must retain the
assembled assets so it can rebuild a complete wheel.

Reconstruct notes from the selected Git revision, merged PRs and durable issue
evidence. The mixed `docs/development/` inventory is not a release-change source
of truth. State breaking contracts, native prerequisites, owner migration and known
limits. For v3, record the final source SHA; prepare notes and artifact identities
for review before requesting publication approval.

### 3.2 Reconstruct the historical releases

| Release | Canonical source | Source date |
|---------|------------------|-------------|
| 1.0.0 | `3bfcef80fa97303d2b51738005b022edbcb0afbd`, [PR #426](https://github.com/MikeyVK/phase-gate-mcp/pull/426) | 2026-07-08 |
| 2.0.0 | `ee32667ca95bf17ffb4ecd59062ef8cbed930e0b`, [PR #441](https://github.com/MikeyVK/phase-gate-mcp/pull/441) | 2026-07-22 |

Build in isolated source copies. Preserve the historical runtime and manifest-mapped
asset contents. The sole approved historical packaging correction is to include
declared hidden assets in `pyproject.toml` through `assets/**/*`,
`assets/**/.*` and `assets/**/.github/**/*`. Record this overlay; do not insert
later runtime, templates, configuration or agent assets.

Historical `mcp>=1` declarations admit today's incompatible MCP 2.3 API. The
bounded historical installation proof uses an explicit `mcp==1.25.0` environment
constraint alongside the exact wheel, preserving its original dependency metadata
and runtime. Record the resolved dependencies and constraint with the evidence.
Identify the PGMCP release through installed distribution metadata and CLI output;
the old MCP handshake's `serverInfo.version` reports SDK version `1.25.0`.

Keep historical source dates separate from present reconstruction and publication
dates. GitHub generates source archives from the tagged commit; reconstructed wheel
and sdist assets containing the packaging overlay must be described explicitly.
They are not the original historical binaries or an unmodified tag-source build.

### 3.3 Verify artifacts and obtain publication approval

Record each artifact's filename, SHA-256, source SHA, reconstruction/build date,
toolchain, dependency constraints and any overlay. Verify the exact wheel and sdist
against the manifest, including hidden files; rebuild a wheel from the sdist and
check its payload. In isolated installations, record installed module origins,
asset/catalog parity, CLI/package version, fresh initialization and startup/MCP
handshake. For v3 also record managed and external renewal outcomes, checkpoint and
backup behavior, and owner-config preservation. A test-built candidate does not
substitute for evidence about the files offered for download.

Keep exact invocations, outcomes and limitations in durable validation evidence.
Stop on missing assets, failed installation/admission/startup, incompatible
dependencies or owner-root overwrite. No unperformed v3 outcome is implied by this
procedure. The approved boundaries are recorded in the
[#500 Research artifact](https://github.com/MikeyVK/phase-gate-mcp/blob/0b228c336b6e8413327b84f15acf1f0fb2280c43/docs/development/issue500/research.md);
historical issue reports are intentionally not installed package assets.

Creating tags, publishing releases, uploading assets and external rollout require
separate human approval of the reviewed notes, exact source SHAs, artifact hashes
and concrete execution procedure. Select the intended latest release explicitly
when publishing historical versions.

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
| 1.2 | 2026-10-11 | @imp documenter | Define bounded GitHub release preparation, historical reconstruction provenance, exact-artifact verification and separate publication approval. |
