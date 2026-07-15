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

- **Decoupled Template Architecture**: Templates are no longer strictly bundled. The server operates as an engine that resolves scaffolding from a configured list of template directory paths (e.g., `template_paths`).
- **Folder-Contained Scaffolding**: The "scaffolding trinity" (Jinja2 templates, `artifacts.yaml` metadata, and schema logic) is fully resolved from these configured paths, making them external to the core engine.
- **Path-Based Resolution & Merging**: `artifacts.yaml` merges across all configured paths in priority order. Jinja2 templates are loaded via `FileSystemLoader(searchpath=template_paths)`.
- Enable agentic orchestration of project-specific templates reusable across projects.

## Background

*   **Current State of Templating**: The Jinja2 templates are bundled in the MCP server wheel, loaded directly via `FileSystemLoader` pointing to a single bundled directory. Schema validation uses Python imports dynamically loaded from the internal `mcp_server.schemas` package. `artifacts.yaml` configuration is loaded strictly from the `server_root/config/artifacts.yaml` path.
*   **Prior Art in Other Tools**: External tools like Copier use Git to track and merge changes from a template repository, whereas Cookiecutter behaves as a single-pass generator. Neither inherently supports a path-based composition of multiple template directories out of the box. However, Jinja2's native `FileSystemLoader` accepts a list of directories (`searchpath=[workspace_dir, shared_dir, bundled_dir]`), making it trivial to compose templates from multiple generic paths.
*   **Reusability across Projects**: The user wishes to establish a template workspace initiative where specific templates designed for one project via agentic orchestration can be shared and reused in other projects.

## Findings

*   **Blast Radius**: Implementing these changes impacts `JinjaRenderer` and `TemplateEngine` initialization. `ArtifactManager._enrich_schema_context` must be refactored to discover schemas from the configured template paths rather than internal `sys.modules`. `ConfigLoader` requires deep-merge functionality for `artifacts.yaml` reading across all configured paths. Tests such as `test_concrete_templates.py`, `test_template_scaffolder.py`, and `test_artifact_registry_config.py` will also need significant updates.
*   **Architectural Constraints**:
    *   **SSOT (Single Source of Truth)**: The merged `artifacts.yaml` definition (from all paths) must become the SSOT. Downstream services and validation logic should not handle merging; they should consume a unified `ArtifactRegistryConfig`.
    *   **Law of Demeter**: `ArtifactManager` should be injected with a `SchemaRegistry` rather than using `getattr(sys.modules, ...)` directly.
*   **Configuration**: The server must support a configuration option (e.g., in `.pgmcp/config.yaml`) that specifies `template_paths`. If none is specified, it might default to `[.pgmcp/templates, <internal_defaults>]`, but the engine itself treats all paths equally.
*   **Schema Resolution**: Schemas need to be resolvable within these "folder-contained" packs. This could mean reading a `schemas.py` in the template path, or defining schemas entirely within the `artifacts.yaml` as JSON schemas, avoiding Python imports altogether.

---

## Approved Strategy

The compatibility and migration policy is to transition to a pure "path-based" template resolution engine. Instead of a hardcoded "wheel vs workspace" fallback or complex python `entry_points`, the server will rely on a configured list of `template_paths`. 

The physical template folders (whether they reside in the workspace, in a shared organizational repo, or in the package installation directory) will contain the complete scaffolding trinity (Jinja2 templates, `artifacts.yaml`, and schema definitions). 

- **Jinja2**: Loaded via a standard `FileSystemLoader` initialized with the configured list of paths.
- **Metadata**: `artifacts.yaml` files discovered across the search paths are deep-merged, with earlier paths taking precedence.
- **Schemas**: Schemas are resolved from the template packs directly, decoupling them from internal module imports.

---

## Expected Results

Jinja templates load via a search path spanning the configured directories. `artifacts.yaml` is deep-merged across all valid paths in order of precedence. Scaffolding logic operates entirely independently of where the physical files are stored, allowing true "folder-contained" agentic orchestration.

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-14 | Agent | Initial draft |