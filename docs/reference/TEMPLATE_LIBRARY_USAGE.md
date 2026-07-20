<!-- docs/reference/TEMPLATE_LIBRARY_USAGE.md -->
<!-- template=reference version=349a0002 created=2026-02-07T00:00Z updated=2026-07-16 -->
# Template Library Usage Guide

**Status:** DEFINITIVE
**Version:** 3.0
**Last Updated:** 2026-07-16

**Source:** [mcp_server/tools/scaffold_artifact.py](file:///C:/temp/pgmcp/mcp_server/tools/scaffold_artifact.py)
**Tests:** [tests/mcp_server/unit/config/test_modular_loader.py](file:///C:/temp/pgmcp/tests/mcp_server/unit/config/test_modular_loader.py) | [tests/mcp_server/unit/managers/test_artifact_manager.py](file:///C:/temp/pgmcp/tests/mcp_server/unit/managers/test_artifact_manager.py)

---

## Purpose

Practical guide for using the scaffolding pipeline: how to scaffold an artifact, how to inspect context requirements before scaffolding, and how to register a new artifact type.

## Scope

**In Scope:**
- Using `scaffold_artifact` and `scaffold_schema` tools
- Understanding the V3 dynamic template validation pipeline
- How artifact types map to declarative YAML schemas and Jinja2 templates
- How to add a new artifact type (no Python edits required)
- Context schema conventions

**Out of Scope:**
- Full TEMPLATE_METADATA format → See docs/reference/template_metadata_format.md
- Architecture rationale → See docs/development/schema-template-maintenance.md
- Artifact type inventory → See docs/reference/TEMPLATE_LIBRARY_QUICK_REFERENCE.md
---

## The Dynamic Validation Pipeline (Caller View)

When you call `scaffold_artifact(artifact_type, name, context)`, your call passes through three layers:

1. **Layer 1 — Declarative Schema**: Your `context` dict is validated against a dynamic Pydantic model constructed at runtime from the `context_schema` configured under `.pgmcp/templates/config/<artifact_type>.yaml`. Required fields are enforced; unknown fields are rejected.
2. **Layer 2 — RenderContext enrichment**: The system dynamically enriches the model with lifecycle fields (`output_path`, `template_id`, `scaffold_created`, `version_hash`).
3. **Layer 3 — Jinja2 template** (`.pgmcp/templates/concrete/`): The enriched context is rendered into the output artifact.

**Practical implication:** Always use `scaffold_schema` to discover required and optional context fields before calling `scaffold_artifact`.

---

## API Reference

### scaffold_schema (use before scaffold_artifact)

Return the JSON Schema for the `context` parameter of an artifact type. Use this before every first call to discover which fields are required and optional.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `artifact_type` | `str` | Yes | Artifact type ID (e.g. `"design"`, `"worker"`, `"dto"`, `"typescript_dto"`) |

**Returns:** A JSON Schema object describing the `context` parameter for the type.

**Error:** Returns an error if the type has no registered configuration file.

**Example:**
```
scaffold_schema(artifact_type="design")
→ { "properties": { "title": {...}, "summary": {...}, ... }, "required": ["title"], ... }
```

---

### scaffold_artifact

Generate any registered artifact type from a context dict.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `artifact_type` | `str` | Yes | Artifact type ID from registry (e.g., `dto`, `typescript_dto`) |
| `name` | `str` | Yes | PascalCase for code artifacts, kebab-case for document artifacts |
| `context` | `dict` | No | Template rendering context — validated against the type's dynamic schema |
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

### Scaffold a TypeScript DTO

```json
{
  "artifact_type": "typescript_dto",
  "name": "OrderDTO",
  "context": {
    "fields": ["id: number", "readonly userId: number", "total: number"],
    "implements": "IOrder"
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

Adding a new artifact type is fully declarative. **No Python source code changes are required.**

| Step | File | Action |
|---|---|---|
| 1 | `.pgmcp/templates/config/<new_type>.yaml` | Create modular configuration file defining metadata, template path, file extension, strict validation policies, and the `context_schema` (defining required/optional fields). |
| 2 | `.pgmcp/templates/concrete/<new_type>.<ext>.jinja2` | Create Jinja2 template extending the appropriate language base (e.g. `tier2_base_python.jinja2`, `tier2_base_typescript.jinja2`). |

### Context schema conventions

- Only truly required fields are marked `required: true` (minimalism: callers need the minimum input to get a working scaffold).
- Code artifact types: `name` or `dto_name` as only mandatory field unless template requires more.
- Document artifact types: `title` as only mandatory field unless template requires more.
- All other fields are optional with sensible defaults.

---

## Naming Conventions

| Artifact category | Name format | Example |
|---|---|---|
| Code (dto, worker, tool, service, typescript_dto, ...) | PascalCase | `OrderDTO`, `ProcessOrderWorker` |
| Document (design, architecture, research, ...) | kebab-case | `oauth-design`, `worker-pattern-architecture` |

## Strict Version Pairing
Templates and their configurations are strictly paired using Semantic Versioning. Every Jinja2 template MUST include a header like `{#- Version: X.Y.Z -#}` that exactly matches the `template_version` specified in its corresponding YAML configuration. A mismatch in the major version will cause a strict configuration error at startup.

---

## Related Documentation
- **[docs/development/schema-template-maintenance.md][related-1]** — Scaffolding Architecture Guide
- **[docs/reference/TEMPLATE_LIBRARY_QUICK_REFERENCE.md][related-2]**
- **[docs/reference/template_metadata_format.md][related-3]**
- **[docs/reference/tools/scaffolding.md][related-4]**

<!-- Link definitions -->
[related-1]: ../development/schema-template-maintenance.md
[related-2]: TEMPLATE_LIBRARY_QUICK_REFERENCE.md
[related-3]: template_metadata_format.md
[related-4]: tools/scaffolding.md
[source]: ../../mcp_server/tools/scaffold_artifact.py
[tests]: ../../tests/mcp_server/unit/config/test_modular_loader.py


## Version History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 3.1 | 2026-07-20 | Agent | Fix stale reference/mcp/ paths in link references |
| 3.0 | 2026-07-16 | Agent | Updated for modular YAML configuration loading, dynamic validation model, and added TypeScript DTO examples. Removed Python context class dependencies. |
| 2.1 | 2026-07-08 | Agent | Update template locations to Git-tracked `.pgmcp/templates` and correct broken architecture link (#420) |
| 2.0 | 2026-06-04 | Agent | Full rewrite: three-layer model; real API and context examples; 6-step contributor guide; removed legacy paths and branding (#286) |
| 1.0 | 2026-02-07 | Agent | Initial draft |
