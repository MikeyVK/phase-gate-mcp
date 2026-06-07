<!-- docs/reference/mcp/README.md -->
<!-- template=reference version=064954ea created=2026-06-04T00:00Z updated= -->
# MCP Template/Scaffolding Reference

**Status:** DEFINITIVE
**Version:** 1.0
**Last Updated:** 2026-06-04

---

## Purpose

Navigation index for the template/scaffolding documentation cluster. Start here to find the right document for your task.

---

## Document Map

| Document | Audience | Use when you want to… |
|---|---|---|
| [docs/architecture/TEMPLATE_LIBRARY.md](../../architecture/TEMPLATE_LIBRARY.md) | Architecture, contributors | Understand the three-layer pipeline model; learn how to add a new artifact type; understand Layer 3 tier hierarchy |
| [TEMPLATE_LIBRARY_USAGE.md](TEMPLATE_LIBRARY_USAGE.md) | Agent users, contributors | Use `scaffold_artifact` and `scaffold_schema`; understand what context to provide; add a new artifact type step by step |
| [TEMPLATE_LIBRARY_QUICK_REFERENCE.md](TEMPLATE_LIBRARY_QUICK_REFERENCE.md) | Agent users | Quick lookup: which artifact types exist, minimum required context, template paths |
| [template_metadata_format.md](template_metadata_format.md) | Template editors | Understand the `TEMPLATE_METADATA` block format; write validation rules for new templates; understand enforcement levels |
| [validation_api.md](validation_api.md) | Developers | `TemplateAnalyzer` and `LayeredTemplateValidator` API; programmatic template validation |
| [tools/scaffolding.md](tools/scaffolding.md) | Agent users | Complete reference for `scaffold_artifact` and `scaffold_schema` MCP tool parameters, returns, errors, and examples |

---

## Three-Layer Architecture (quick summary)

The scaffolding pipeline has three layers:

| Layer | Location | Role |
|---|---|---|
| 1 — Context schema | `mcp_server/schemas/contexts/` | User-facing. Pydantic validation. You provide this. |
| 2 — RenderContext schema | `mcp_server/schemas/render_contexts/` | System-internal. Adds lifecycle fields. |
| 3 — Jinja2 template | `mcp_server/scaffolding/templates/concrete/` | Output rendering. `TEMPLATE_METADATA` is the variable contract SSOT. |

**To add a new artifact type, all six steps are required:**

1. Create Context schema in `mcp_server/schemas/contexts/<type>.py`
2. Create RenderContext schema in `mcp_server/schemas/render_contexts/<type>.py`
3. Export both from `mcp_server/schemas/__init__.py`
4. Add the new type to the artifact-to-Context registry in `mcp_server/managers/artifact_manager.py`
5. Enable the type in `.phase-gate/config/artifacts.yaml`
6. Create the Jinja2 template in `mcp_server/scaffolding/templates/concrete/<type>.<ext>.jinja2`

> Steps 1–4 require Python source code changes.

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-04 | Agent | Initial navigation surface for template/scaffolding cluster (#286) |
