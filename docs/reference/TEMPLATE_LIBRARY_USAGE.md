# Template Library Usage

**Status:** DEFINITIVE  
**Last Updated:** 2026-10-04

Use the active template suite to discover a suitable artifact package, inspect its caller schema, create a valid starting point, and refine the result for its intended use. The runtime catalog and resolved package schema own exact IDs, purposes, fields, and package identity; this guide intentionally contains no copied inventory.

## Discover and scaffold

Use the current tool schema to see the admitted package IDs. Call `scaffold_schema` for a selected ID to confirm the package purpose and inspect its complete resolved JSON Schema. This schema describes the caller's `context`; it does not prescribe an artifact's full content.

Build the caller context from the resolved schema, then call `scaffold_artifact` with the selected `artifact_type`, exact output `file_name`, and context. Use `target_path` only when the file needs a specific workspace-relative directory. The server validates the caller context and uses the selected package's resolved render graph and output profile.

A successful scaffold gives you a valid basis. Read the result and refine the file with your editor or `safe_edit_file` to meet the task's actual requirements. First-call validity is not a substitute for review or completion. For safe-edit validation, choose `enforce` when a failed required check must block the write, or `report` when the findings should be returned while continuing. Independent safety and operational checks still apply.

The public [scaffolding tool reference](tools/scaffolding.md) documents the current operation and schema behavior. The [editing reference](tools/editing.md) explains refinement and validation policy.

The [context migration and output responsibilities](tools/scaffolding.md#context-migration-and-output-responsibilities) explain mandatory authored document metadata, revision history, preserved caller content and clean input migration. These requirements are separate from technical package provenance; use the selected schema for exact admitted fields.

## Extend or maintain a package

Use the runtime catalog to find the package purpose and `scaffold_schema` to read its resolved input contract; do not copy package IDs or field tables into another guide. A concrete package owns its manifest identity and purpose, caller schema, release version, policy, and root template. The resolved template graph may use shared bases, patterns, and definitions. Follow [Scaffold Schema and Template Maintenance](../development/schema-template-maintenance.md) for maintenance decisions.

First adapt an admitted package's schema and template graph when they can express the required behavior. A requirement for a generic engine capability, such as a new schema dialect, graph rule, rendering feature, or output-profile behavior, needs a generic implementation change. Package-specific facts belong to the package and must not become hardcoded server branches.

The server resolves the complete suite from its configured `template_suite/` root at startup. In a workspace-managed installation this is commonly `.pgmcp/template_suite/`. Suite changes are visible after the server restarts and resolves the suite again. Official package content is maintained and delivered with PGMCP; a workspace owner controls the installed workspace state and its explicit upgrade/recovery choices. See [Discovery and Admin Tools](tools/discovery.md) for restart guidance.

## Package identity and artifact provenance

Newly scaffolded artifacts record the selected package identity, its authored package version, the resolved package fingerprint, and the source suite fingerprint. These are generation-source facts. They do not promise that historical source files are available and do not authorize renewal or overwrite. Non-artifact schema results carry package identity only where the public result contract defines it.

See [Template Package Identity and Artifact Provenance](template_metadata_format.md) for the compact record and the distinction between package and suite identity.

## Related guidance

- [Scaffolding Tools](tools/scaffolding.md) — current public scaffold and schema behavior.
- [Editing Tools](tools/editing.md) — safe refinement and validation policy.
- [Discovery and Admin Tools](tools/discovery.md) — restart behavior.
- [Scaffold Schema and Template Maintenance](../development/schema-template-maintenance.md) — package extension and maintenance.
- [Template Package Identity and Artifact Provenance](template_metadata_format.md) — persisted artifact provenance.
