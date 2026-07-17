<!-- docs\development\issue429\research.md -->
<!-- template=research version=8b7bb3ab created=2026-07-17T07:43Z updated= -->
# Issue 429: Template Package Bundling

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-07-17

---

## Problem Statement

The configuration YAMLs for artifacts currently live in `.pgmcp/config/artifacts/` while their corresponding Jinja2 templates live in `.pgmcp/templates/`. This artificial separation breaks cohesion, as they form a tight 1-to-1 pair. Issue #429 aims to bundle them together into cohesive Template Packages, but this requires refactoring the `ConfigLoader` and handling backward compatibility.

## Research Goals

- Identify blast radius of migrating artifacts configs to templates/
- Resolve architectural tension in ConfigLoader scanning presentation paths
- Determine a migration policy for legacy workspaces
- Establish version-pairing logic between templates and yaml configs

---

## Findings

## Current State
- `ConfigLoader` loads `artifacts.yaml` as an index, then scans `config_root / "artifacts"` to merge modular configurations into `ArtifactRegistryConfig`.
- `ArtifactManager` uses this registry to resolve scaffolding requests, locating the Jinja2 templates via its own `_get_template_root()` logic.

## Blast Radius & Dependencies
- `ConfigLoader` currently only knows about `config_root`. Changing it to scan `templates/` introduces presentation layer knowledge into the config loader, which creates an architectural tension.
- Heavy reliance on the old path in test suites: `test_modular_loader.py`, `artifact_test_harness.py`, and multiple integration tests.
- The `mcp_server/assets/config/artifacts.yaml` is currently one monolithic file that needs to be broken up and moved to `assets/templates/`.

## Architecture Preservation
- The internal representation and Pydantic validation of `ArtifactRegistryConfig` must remain unchanged.
- The `ConfigLoader` must receive `template_root` via its constructor (Dependency Injection) from `bootstrap.py` to preserve the Domain vs Presentation separation defined in `ARCHITECTURE_PRINCIPLES.md`.

## Seams
The refactor can be split into safely testable steps:
1. Update `ArtifactDefinition` to support version-pairing.
2. Update `ConfigLoader` to accept `template_root` and scan the new location (removing the old one).
3. Refactor all affected tests and harnesses to mock/provide a `template_root`.
4. Migrate the physical assets (`assets/config/artifacts.yaml` to `assets/templates/concrete/...`).

---

## Approved Strategy

### Template Package Migration Strategy
**Policy:** Clean Break (No backward compatibility for legacy `config/artifacts/`)
**Rationale:** The v2.0.0 release is already breaking compared to v1.0.0. Maintaining a dual-loader fallback for the old `config/artifacts/` directory adds technical debt and architectural contamination (mixing domain loaders with presentation fallbacks). Instead, we enforce a clean break where old workspaces must use the `pgmcp --upgrade` command to align their structures.

### Version-Pairing Strategy
**Policy:** Strict Version Pairing
**Rationale:** To prevent templates and their YAML configurations from drifting out of sync, `ArtifactDefinition` will receive a `version` (or `template_version`) field. The system will enforce alignment between the YAML configuration and the corresponding Jinja2 template.

---

## Expected Results

1. `ArtifactRegistryConfig` successfully loads its modular configs directly from the `templates/` directory (e.g., `templates/concrete/`).
2. `ConfigLoader` remains architecturally clean by accepting `template_root` via dependency injection from the composition root, rather than hardcoding presentation paths.
3. Legacy loading from `config/artifacts/` is strictly removed.
4. `ArtifactDefinition` includes explicit version-pairing logic to ensure the Jinja2 template and its YAML schema are structurally aligned.
5. All test suites (e.g., `test_modular_loader.py`, `artifact_test_harness.py`, `test_concrete_templates.py`) are refactored to use the new `templates/` structure.

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-17 | Agent | Initial draft |