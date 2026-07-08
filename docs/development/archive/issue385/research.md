<!-- docs\development\issue385\research.md -->
<!-- template=research version=8b7bb3ab created=2026-07-02T09:07Z updated= -->
# Research: Package identity rename + pgmcp entry point + first-run bootstrap

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-07-02

---

## Problem Statement

The package requires a `pgmcp` entry point in `pyproject.toml`, a first-run bootstrap mechanism in `cli.py` to prevent confusing crashes on missing workspace configurations, and verification that version resolution works after the package rename. Additionally, the default root directory `.phase-gate/` must be evaluated against the new `pgmcp` package identity.

## Research Goals

- Add CLI entry point for pgmcp
- Determine mechanism for first-run bootstrap and configuration provisioning
- Analyze impact of renaming the package identity and default configuration root

---

## Findings

- **Missing Entry Point:** `pyproject.toml` currently lacks `[project.scripts]` `pgmcp`. Easy fix.
- **Server Version Logic:** `settings.py` correctly uses `packages_distributions()`, which handles the rename to `phase-gate-mcp` automatically.
- **Default Root & Configuration Bootstrap:** Currently, the server crashes via `ConfigLoader` if `.phase-gate/` is missing. The agreed strategy requires renaming this root to `.pgmcp/` and using a bundled package resources folder (`mcp_server/assets/`) which gets copied to the workspace *only* when the user runs `pgmcp --init` as a flat-copy folder.
- **Blast Radius (Path Coherence):** `mcp_server/utils/template_config.py` and `loader.py` currently bypass `Settings` for path resolution, using legacy probes and environment variables that ignore the workspace root. This breaks Dependency Injection and flat-folder loading. These decoupled probes must be removed; `Settings` must become the single source of truth for `resolved_config_root` and `resolved_template_root`.
- **Blast Radius (Tests & Technical Debt):** Over 50 test files currently hardcode `.phase-gate` strings, violating Dependency Injection principles (a leftover from PR #329). This technical debt must be resolved: tests must be refactored to dynamically inject `Settings().server.server_root_dir` (or equivalent fixtures) rather than using another lazy search-and-replace to `.pgmcp`.
- **Blast Radius (Docs/Rules):** The internal agent instructions (like `AGENTS.md`, `imp.agent.md`) still reference `.phase-gate` and must be updated.

---

## Approved Strategy

- Boundary: Default Configuration Root & First-Run Bootstrap
- Policy: Rename `.phase-gate/` to `.pgmcp/` and use explicit `pgmcp --init` command to install bundled default configs from package assets (`mcp_server/assets/`).
- Rationale: Aligns configuration root with CLI command name (Package Identity). Adheres to Fail-Fast and Explicit-over-Implicit architecture principles by failing cleanly when `.pgmcp/` is missing instead of auto-provisioning magic folders. Avoids IDE specific modifications.

---

## Expected Results

1. `pyproject.toml` contains `pgmcp` entry point mapping to `mcp_server.cli:main`.
2. Package bundles default configurations in `mcp_server/assets/` via `package-data`.
3. Server default root is `.pgmcp/`.
4. `cli.py` handles `--init` flag to provision `.pgmcp/` from bundled assets.
5. `cli.py` fails fast with an explicit error asking the user to run `pgmcp --init` if `.pgmcp/` is missing and `--init` is not provided.
6. Test suite technical debt is resolved: all hardcoded `.phase-gate` path strings in `tests/` are removed and replaced with proper Dependency Injection using `ServerSettings` or dynamic fixtures.

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-02 | Agent | Initial draft |