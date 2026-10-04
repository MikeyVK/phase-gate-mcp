# Scaffold Schema and Template Maintenance

**Status:** DEFINITIVE  
**Last Updated:** 2026-10-04

This guide explains how to discover, extend, and maintain the active template suite. The runtime catalog and resolved package schema are authoritative for available packages and caller fields. This page describes durable workflow only; it does not duplicate a package inventory or schema.

## Discover and use a package

1. Choose a package by its declared purpose in the active runtime catalog.
2. Once you know its template ID, call `scaffold_schema` when the resolved schema is not already available. Inspect the complete returned JSON Schema rather than inferring fields from an old example.
3. Use `scaffold_artifact` to produce a valid starting point from the selected package and the caller context.
4. Review the generated artifact and refine it with the normal editor or `safe_edit_file`. Schema-valid output is a starting point; it does not establish that the artifact is complete or correct for its task.

Use `validation=enforce` when the configured pre-mutation checks must prevent a write on failure. Use `validation=report` when the caller wants findings while continuing, subject to independent safety and operational checks. See the [scaffolding tool reference](../reference/tools/scaffolding.md) and [editing guidance](../reference/tools/editing.md) for current public behavior.

## Extend the suite

A concrete package is the unit that owns one artifact purpose and its generation contract. Its manifest supplies the stable template ID and purpose; its context schema describes caller inputs; its policy and resolved template graph supply validation and rendering behavior. The active suite also owns shared bases, patterns, and definitions that packages explicitly reach through the graph.

Start by checking whether an existing package and the admitted schema and template capabilities can express the requirement. Add or adapt package-owned content when they can. A new JSON Schema dialect, graph behavior, renderer feature, or output-profile capability needs a generic engine change; do not describe every extension as code-free. Keep package-specific facts in that package rather than adding artifact IDs or fields to generic server code.

Every Jinja environment that admits or renders shared suite templates must receive the real generic filters before compilation. Direct environment consumers use the public register_template_filters(environment) from [template_engine.py](../../mcp_server/services/template_engine.py); engine construction uses the same routine. Register before admission analysis as well as rendering. A local stand-in filter or a validation bypass does not implement that contract.

The complete suite is loaded from the configured `template_suite/` root. A workspace-managed installation commonly keeps that root at `.pgmcp/template_suite/`; the installed PGMCP distribution supplies its official suite assets. The selected package's logical identity comes from its manifest, not its storage-directory name or an absolute host path. Keep local suite changes within the workspace owner's upgrade and recovery process. Changes to suite sources or configuration become available after the server restarts and resolves the suite again.

## Provenance and ownership

Newly scaffolded artifacts carry compact source provenance derived from the selected package and the supplied suite generation. It records package identity, its authored release version, the resolved package fingerprint, and the source suite fingerprint. These values describe generation inputs. They do not locate historical files, prove authenticity, authorize overwrite, or replace the separate installation checkpoint used for suite renewal.

See [Template Package Identity and Artifact Provenance](../reference/template_metadata_format.md) for the compact persisted record. Technical source provenance needs no additional per-file template-version header or manually maintained registry. Authored full-document metadata is a separate obligation: its visible header and Version History remain mandatory under the [Documentation Standard](../coding_standards/DOCUMENTATION_STANDARD.md#scaffolded-document-metadata-and-whitespace).

## Related guidance

- [Template Library Usage](../reference/TEMPLATE_LIBRARY_USAGE.md) — discovery, scaffold basis, refinement, and extension.
- [Scaffolding Tools](../reference/tools/scaffolding.md) — public schema and scaffold behavior.
- [Editing Tools](../reference/tools/editing.md) — safe refinement and validation policy.
- [Discovery and Admin Tools](../reference/tools/discovery.md) — restart behavior.
