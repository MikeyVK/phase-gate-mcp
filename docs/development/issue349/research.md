<!-- docs\development\issue349\research.md -->
<!-- template=research version=8b7bb3ab created=2026-07-14T20:52Z updated= -->
# Template Workspace Initiative: workspace-owned templates, schema packs

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-07-14

---

## Problem Statement

The three-part scaffolding trinity (schemas, Jinja2 templates, artifacts.yaml) is currently bundled inside the wheel. Users have no supported path to adapt scaffolding to their projects or to reuse template schema packs across arbitrary projects without modifying the core server.

## Research Goals

- **Decoupled Template Architecture**: Templates are no longer bundled. The server operates as an engine that resolves scaffolding from a single configured template root.
- **Folder-Contained Scaffolding**: The "scaffolding trinity" (Jinja2 templates, `artifacts.yaml` metadata, and schema logic) is fully resolved from the workspace configuration paths (`resolved_template_root` and `resolved_config_root`).
- **Single Source of Truth**: There is exactly one `artifacts.yaml` (no merging needed) and one template directory. Users can override these paths via the existing `PGMCP_TEMPLATE_ROOT`, `PGMCP_CONFIG_ROOT` or `settings.yaml` mechanisms.
- Enable agentic orchestration of project-specific templates reusable across projects by configuring the server to point to a shared template repository folder.

## Background

*   **Current State of Templating**: The Jinja2 templates are bundled in the MCP server wheel, loaded directly via `FileSystemLoader` pointing to a single bundled directory. Schema validation uses Python imports dynamically loaded from the internal `mcp_server.schemas` package. `artifacts.yaml` configuration is loaded strictly from the `server_root/config/artifacts.yaml` path.
*   **Settings Architecture**: The system already supports path overrides via `ServerSettings` (`workspace_root`, `config_root`, `template_root`), which resolve to standard locations (e.g. `.pgmcp/templates` and `.pgmcp/config`).
*   **Reusability across Projects**: The user wishes to establish a template workspace initiative where specific templates designed for one project via agentic orchestration can be shared and reused in other projects.

## Findings

*   **Blast Radius**: Implementing these changes impacts `JinjaRenderer` and `TemplateEngine` initialization. `ArtifactManager._enrich_schema_context` must be refactored to discover schemas externally rather than from internal `sys.modules`. `ConfigLoader` will load a single `artifacts.yaml` from `resolved_config_root` without attempting to merge with internal defaults. Tests such as `test_concrete_templates.py`, `test_template_scaffolder.py`, and `test_artifact_registry_config.py` will also need significant updates.
*   **Architectural Constraints**:
    *   **SSOT (Single Source of Truth)**: The single `artifacts.yaml` at the configured `resolved_config_root` is the definitive SSOT. No fallback merging logic is allowed. Downstream services and validation logic should consume a unified `ArtifactRegistryConfig`.
    *   **Law of Demeter**: `ArtifactManager` should be injected with a `SchemaRegistry` rather than using `getattr(sys.modules, ...)` directly.
*   **Configuration Simplicity**: The server leverages the existing `Settings.from_env()` to determine `template_root` and `config_root`. By default, this is `.pgmcp/templates` and `.pgmcp/config`. Workspaces that want a different root simply use `.env` or `PGMCP_CONFIG_PATH` to overwrite these properties.
*   **Schema Resolution**: Schemas need to be resolvable within the folder-contained structure. This avoids Python imports entirely if schemas are defined directly within the `artifacts.yaml` or as JSON schemas inside the template root.

---

## Approved Strategy

The compatibility and migration policy is to transition to a pure "single-root" template resolution engine. Instead of complex fallback chains or merging logic, the server relies exclusively on the configured `resolved_template_root` and `resolved_config_root` properties from the `ServerSettings`.

The physical template folder (whether it resides in the workspace or in a shared organizational repo) will contain the complete scaffolding trinity (Jinja2 templates, `artifacts.yaml`, and schema definitions). 

- **Jinja2**: Loaded via a standard `FileSystemLoader` initialized with the single `resolved_template_root`.
- **Metadata**: The `artifacts.yaml` file located in `resolved_config_root` is loaded as the absolute SSOT. No merging.
- **Schemas**: Schemas are resolved dynamically from the template pack environment, decoupling them from internal module imports.

---

## Expected Results

Jinja templates and schemas load from the single configured `resolved_template_root`. The `artifacts.yaml` file loads strictly from `resolved_config_root`. Scaffolding logic operates entirely independently of core bundling, achieving true "folder-contained" simplicity and predictability.

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-14 | Agent | Initial draft |