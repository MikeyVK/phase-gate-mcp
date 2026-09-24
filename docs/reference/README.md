<!-- docs/reference/README.md -->
<!-- template=reference version=064954ea created=2026-06-04T00:00Z updated= -->
# MCP Template/Scaffolding Reference

**Status:** DEFINITIVE
**Version:** 1.0
**Last Updated:** 2026-09-24

---

## Purpose

Navigation index for the template/scaffolding documentation cluster. Start here to find the right document for your task.

---

## Document Map

| Document | Audience | Use when you want to… |
|---|---|---|
| [docs/manuals/architecture.md](../manuals/architecture.md) | Architecture, contributors | Understand the current server composition and responsibilities |
| [architectural diagrams](../manuals/architectural_diagrams/09_scaffolding_subsystem.md) | Contributors | Follow the startup-resolved suite and generic scaffolding flow |
| [TEMPLATE_LIBRARY_USAGE.md](TEMPLATE_LIBRARY_USAGE.md) | Agent users, contributors | Use `scaffold_artifact` and `scaffold_schema`; understand what context to provide; add a new artifact type step by step |
| [template_metadata_format.md](template_metadata_format.md) | Template editors | Understand package identity and the `pgmcp:v1` provenance record in scaffolded artifacts |
| [tools/scaffolding.md](tools/scaffolding.md) | Agent users | Complete reference for `scaffold_artifact` and `scaffold_schema` MCP tool parameters, returns, errors, and examples |

---

## Start here

- Use [TEMPLATE_LIBRARY_USAGE.md](TEMPLATE_LIBRARY_USAGE.md) to discover packages,
  inspect their caller schemas, scaffold valid input, and follow the extension procedure.
- Use [tools/scaffolding.md](tools/scaffolding.md) for current `scaffold_schema` and
  `scaffold_artifact` tool schemas, results, and examples.
- Use [template_metadata_format.md](template_metadata_format.md) for the compact
  provenance record written to generated artifacts.
- Use the [architecture manual](../manuals/architecture.md) and
  [scaffolding subsystem diagram](../manuals/architectural_diagrams/09_scaffolding_subsystem.md)
  for current responsibility boundaries.

The template suite owns package manifests, JSON Schemas, templates, and shared
components. Startup resolves the configured suite into one immutable catalog. The
physical package directory is a storage location; `manifest.yaml:template_id` is the
package identity. This index does not duplicate the catalog, package IDs, fields, or
paths.

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.2 | 2026-09-24 | Agent | Replace obsolete three-layer registry recipe with current suite-discovery navigation |
| 1.1 | 2026-07-20 | Agent | Fix stale reference/mcp/ path in header |
| 1.0 | 2026-06-04 | Agent | Initial navigation surface for template/scaffolding cluster (#286) |
