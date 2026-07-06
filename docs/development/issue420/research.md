<!-- docs\development\issue420\research.md -->
<!-- template=research version=8b7bb3ab created=2026-07-06T05:52Z updated=2026-07-06T21:00Z -->
# Research: Deferred Release Assets and Template Bootstrap

**Status:** APPROVED  
**Version:** 1.2  
**Last Updated:** 2026-07-06

## Prerequisites

Read these first:
1. Issue #420
2. docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
3. docs/coding_standards/DOCUMENTATION_STANDARD.md
4. docs/reference/mcp/release-assets-procedure.md
---

## Problem Statement

1. **Workspace templates initialization blocker:** Clean repository checkouts of the development repository contain the tracked `.pgmcp/config` folder but miss the untracked `.pgmcp/templates` directory. The current `pgmcp --init` command checks if `.pgmcp` exists and aborts immediately. This prevents developers from bootstrapping templates in the development workspace.
2. **CLI `--init` incomplete copy behavior:** The current implementation of `pgmcp --init` in `mcp_server/cli.py` is hardcoded to only copy the `config` and `templates` subdirectories from package assets via `shutil.copytree`. It does not perform a recursive flat copy of the entire `mcp_server/assets/` directory, causing other packaged assets (like `template_registry.json`) to be completely missed.
3. **Deferred packaging build automation:** The release packaging automation and manifest synchronization specified in `release-assets-procedure.md` (distributing files from the `docs/agents/` Single Source of Truth to `mcp_server/assets/` using a manifest file mapping) are deferred.

## Research Goals

- Support clean workspace initialization in target environments without changing product runtime CLI checks.
- Update `pgmcp --init` to perform a flat recursive copy of the entire `mcp_server/assets/` directory (including `template_registry.json` and any other assets) instead of only copying hardcoded subdirectories.
- Eliminate templates directory triplication by removing `mcp_server/scaffolding/templates` and updating the test suite to use resolved settings.
- Implement automated build-time copy/sync of release-bound assets to `mcp_server/assets/` on release builds using `.pgmcp/config/release_manifest.yaml` and a pre-build script.
- Establish a secure development isolation setup where the active running server instance operates from a packaged wheel in a stable virtual environment, fully separated from the active development codebase.

---

## Approved Strategy

### Boundary: Default Configuration Root & Workspace Initialization (`pgmcp --init`) & Dev Setup
- **Policy:** Keep the production CLI's `pgmcp --init` implementation clean and strict: it must abort if the `.pgmcp/` directory already exists (idempotency guard). Do not add dev-specific runtime bypasses in the CLI code.
- **Policy:** To resolve the chicken-and-egg problem in the development workspace, fully track `.pgmcp/templates/` under version control in Git. This ensures a clean clone of the development repository immediately contains all templates.
- **Policy:** Update `pgmcp --init` in `mcp_server/cli.py` to copy the entire contents of the packaged `assets/` folder recursively (using `shutil.copytree(assets_dir, resolved_server_root, dirs_exist_ok=True)`) rather than hardcoding individual subfolders. This ensures `template_registry.json` and other assets are correctly bootstrapped.

### Boundary: Templates Source of Truth
- **Policy:** Remove the duplicate `mcp_server/scaffolding/templates` directory.
- **Policy:** All unit and integration tests must load templates from Settings-resolved paths or test-isolated temporary paths, keeping `.pgmcp/templates` as the active dev environment SSOT.

### Boundary: Release Packaging & Automation (Build Pipeline)
- **Policy:** Add `mcp_server/assets/` to `.gitignore` so that packaged assets are not checked into Git. The only checked-in config and template files will be in `.pgmcp/`.
- **Policy:** Place the build manifest file at `.pgmcp/config/release_manifest.yaml` to ensure all configurations are co-located in the config folder.
- **Policy:** Implement a build-time pre-build sync script (e.g. `scripts/build_package.py`) that parses `.pgmcp/config/release_manifest.yaml`, clears `mcp_server/assets/`, copies the designated source files (from `.pgmcp/config`, `.pgmcp/templates`, and other locations), and then triggers the package build backend (`python -m build`). This pipeline is built as part of this issue (#420).
- **Policy:** Active development of agent instructions/workflows only modifies files under `docs/agents/`. Provide a developer-only sync script (`scripts/sync_agents.py`) that copies rules/workflows to their active runtime locations and `mcp_server/assets/` to support local testing.

### Boundary: Development Isolation
- **Policy:** Document the development isolation setup (running a stable built wheel in `pgmcp_stable_venv` pointing its working directory to the development repository root) as the **standard best practice** for developers working on the `pgmcp` repository itself. This keeps the running chat engine stable during refactoring.

---

## Expected Results

1. Clean checkouts of target repositories can be initialized via `pgmcp --init` to recursively copy all packaged assets (including `template_registry.json`, `config/`, and `templates/`) under `.pgmcp/`.
2. `mcp_server/scaffolding/templates` is deleted and all tests pass using the settings-based template paths.
3. Bundled package assets (`mcp_server/assets/`) are ignored in Git and populated automatically during package packaging by a build-time pre-build sync script using the rules defined in `.pgmcp/config/release_manifest.yaml`.
4. The running instance of the MCP server can be installed and run from a packaged wheel in a stable venv, operating independently of the active development repository's python source files.

## Related Documentation
- **[docs/reference/mcp/release-assets-procedure.md](docs/reference/mcp/release-assets-procedure.md)**
- **[docs/reference/mcp/server-configuration.md](docs/reference/mcp/server-configuration.md)**
- **[docs/development/issue385/documentation.md](docs/development/issue385/documentation.md)**
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-06 | Agent | Initial draft |
| 1.1 | 2026-07-06 | Agent | Refine strategy to preserve strict CLI initialization check, track templates in dev git, ignore assets folder, and implement flat copy |
| 1.2 | 2026-07-06 | Agent | Move release manifest to `.pgmcp/config/release_manifest.yaml`, define dev-isolation as a developer best practice, and untrack `.agents/mcp_config.json`. |
