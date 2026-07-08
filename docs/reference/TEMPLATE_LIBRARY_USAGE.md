<!-- docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md -->
<!-- template=reference version=064954ea created=2026-02-07T00:00Z updated=2026-06-04 -->
# Template Library Usage Guide

**Status:** DEFINITIVE
**Version:** 2.0
**Last Updated:** 2026-06-04

**Source:** [mcp_server/tools/scaffold_artifact.py][source]
**Tests:** [tests/mcp_server/integration/test_smoke_all_types.py][tests]

---

## Purpose

Practical guide for using the scaffolding pipeline: how to scaffold an artifact, how to inspect context requirements before scaffolding, and how to register a new artifact type.

## Scope

**In Scope:**
- Using `scaffold_artifact` and `scaffold_schema` tools
- Understanding the three-layer pipeline from a caller perspective
- How artifact types map to Context schemas and Jinja2 templates
- How to add a new artifact type (all six required steps)
- Context schema conventions

**Out of Scope:**
- Full TEMPLATE_METADATA format → See docs/reference/mcp/template_metadata_format.md
- Architecture rationale → See docs/architecture/TEMPLATE_LIBRARY.md
- Artifact type inventory → See docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md

---

---

## The Three-Layer Pipeline (Caller View)

When you call `scaffold_artifact(artifact_type, name, context)`, your call passes through three layers:

1. **Layer 1 — Context schema** (`mcp_server/schemas/contexts/`): your `context` dict is validated against a Pydantic schema. Required fields are enforced; unknown fields are rejected. This is the only layer you interact with directly.
2. **Layer 2 — RenderContext schema** (`mcp_server/schemas/render_contexts/`): the system adds lifecycle fields (`output_path`, `template_id`, `scaffold_created`, `version_hash`). These are never user-facing.
3. **Layer 3 — Jinja2 template** (`mcp_server/scaffolding/templates/concrete/`): the enriched context is rendered into the output artifact. The `TEMPLATE_METADATA` block is the Layer 3 variable contract SSOT.

**Practical implication:** always use `scaffold_schema` to discover required and optional context fields before calling `scaffold_artifact`.

---

## API Reference

### scaffold_schema (use before scaffold_artifact)

Return the JSON Schema for the `context` parameter of an artifact type. Use this before every first call to discover which fields are required and optional.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `artifact_type` | `str` | Yes | Artifact type ID (e.g. `"design"`, `"worker"`, `"dto"`) |

**Returns:** A JSON Schema object describing the `context` parameter for the type.

**Error:** Returns an error if the type has no registered Context schema.

**Example:**
```
scaffold_schema(artifact_type="design")
→ { "properties": { "title": {...}, "summary": {...}, ... }, "required": ["title", "summary", "cycles"], ... }
```

---

### scaffold_artifact

Generate any registered artifact type from a context dict.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `artifact_type` | `str` | Yes | Artifact type ID from registry |
| `name` | `str` | Yes | PascalCase for code artifacts, kebab-case for document artifacts |
| `context` | `dict` | No | Template rendering context — validated against the type's Context schema |
| `output_path` | `str` | No | Explicit output path; auto-resolved from `project_structure.yaml` when omitted |

---

## Recommended Workflow

```
1. scaffold_schema(artifact_type="worker")       → inspect required + optional fields
2. build context dict from the schema
3. scaffold_artifact(artifact_type="worker", name="OrderProcessor", context={...})
```

This eliminates trial-and-error context validation failures.

---

## Usage Examples

### Scaffold a DTO

```json
{
  "artifact_type": "dto",
  "name": "OrderDTO",
  "context": {
    "dto_name": "OrderDTO",
    "fields": ["id: int", "user_id: int", "total: Decimal"]
  }
}
```

### Scaffold a Worker

```json
{
  "artifact_type": "worker",
  "name": "EmailNotificationWorker",
  "context": {
    "name": "EmailNotificationWorker",
    "description": "Send email notifications asynchronously"
  }
}
```

### Scaffold a Design Document

```json
{
  "artifact_type": "design",
  "name": "payment-gateway-design",
  "context": {
    "title": "Payment Gateway Integration Design",
    "summary": "Design for integrating Stripe and PayPal payment providers",
    "cycles": []
  }
}
```

### Scaffold a Generic Document (generic_doc)

```json
{
  "artifact_type": "generic_doc",
  "name": "migration-guide",
  "context": {
    "title": "Migration Guide: Commit Scope Update"
  }
}
```

---


## How to Add a New Artifact Type

All six steps are required. Steps 1–4 require Python source code changes.

| Step | File | Action |
|---|---|---|
| 1 | `mcp_server/schemas/contexts/<type>.py` | Create Context schema: user-facing Pydantic `BaseModel`; required fields from `TEMPLATE_METADATA.introspection.variables.required`; optional fields with sensible defaults |
| 2 | `mcp_server/schemas/render_contexts/<type>.py` | Create RenderContext schema: extends appropriate render base; adds lifecycle fields |
| 3 | `mcp_server/schemas/__init__.py` | Export `TypeContext` and `TypeRenderContext` |
| 4 | `mcp_server/managers/artifact_manager.py` | Add the new type to the artifact-to-Context registry |
| 5 | `.pgmcp/config/artifacts.yaml` | Enable the artifact type entry |
| 6 | `mcp_server/scaffolding/templates/concrete/<type>.<ext>.jinja2` | Create Jinja2 template with `TEMPLATE_METADATA` block including `introspection.variables` |

### Context schema conventions

- Only truly required fields are required (minimalism: callers need the minimum input to get a working scaffold)
- Code artifact types: `name: str` as only mandatory field unless template requires more
- Document artifact types: `title: str` as only mandatory field unless template requires more
- All other fields are optional with sensible defaults
- Shared value objects must be `frozen=True`

---

## Naming Conventions

| Artifact category | Name format | Example |
|---|---|---|
| Code (dto, worker, tool, service, ...) | PascalCase | `OrderDTO`, `ProcessOrderWorker` |
| Document (design, architecture, research, ...) | kebab-case | `oauth-design`, `worker-pattern-architecture` |

---

## Related Documentation
- **[docs/architecture/TEMPLATE_LIBRARY.md][related-1]**
- **[docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md][related-2]**
- **[docs/reference/mcp/template_metadata_format.md][related-3]**
- **[docs/reference/mcp/tools/scaffolding.md][related-4]**

<!-- Link definitions -->
[source]: ../../mcp_server/tools/scaffold_artifact.py
[tests]: ../../tests/mcp_server/integration/test_smoke_all_types.py
[related-1]: ../../docs/architecture/TEMPLATE_LIBRARY.md
[related-2]: TEMPLATE_LIBRARY_QUICK_REFERENCE.md
[related-3]: template_metadata_format.md
[related-4]: tools/scaffolding.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.0 | 2026-06-04 | Agent | Full rewrite: three-layer model; real API and context examples; 6-step contributor guide; removed legacy paths and branding (#286) |
| 1.0 | 2026-02-07 | Agent | Initial draft |
