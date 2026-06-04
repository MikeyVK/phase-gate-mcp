<!-- docs/architecture/TEMPLATE_LIBRARY.md -->
<!-- template=architecture version=8b924f78 created=2026-02-07T00:00Z updated=2026-06-04 -->
# Template Library Architecture

**Status:** DEFINITIVE
**Version:** 2.0
**Last Updated:** 2026-06-04

---

## Purpose

Define the architecture of the scaffolding pipeline: the three-layer model that governs how artifact types are registered, validated, and rendered; how the Jinja2 template tier hierarchy works within Layer 3; and how to register a new artifact type.

## Scope

**In Scope:**
- Three-layer pipeline architecture (Context schema → RenderContext schema → Jinja2 template)
- Layer responsibilities and separation of concerns
- Layer 3 internal tier hierarchy and composition
- How to add a new artifact type (all six required steps)
- Template provenance tracking via SCAFFOLD header

**Out of Scope:**
- Tool API usage → See docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md
- TEMPLATE_METADATA format specification → See docs/reference/mcp/template_metadata_format.md
- Artifact type inventory → See docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md

## Prerequisites

Read these first:
1. docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
2. docs/reference/mcp/README.md (cluster navigation)
---

## 1. Three-Layer Pipeline Architecture

The scaffolding pipeline has three layers with distinct responsibilities. Callers interact only with Layer 1; the rest is system-internal.

| Layer | Location | Responsible for | Must NOT contain |
|---|---|---|---|
| 1 — Context schema | `mcp_server/schemas/contexts/` | User-facing API contract; field types; Pydantic fail-fast validation | Lifecycle fields; render logic |
| 2 — RenderContext schema | `mcp_server/schemas/render_contexts/` | Lifecycle enrichment: `template_id`, `scaffold_created`, `version_hash`, `output_path` | User input fields; business validation |
| 3 — Jinja2 template | `mcp_server/scaffolding/templates/concrete/` | Output rendering; `TEMPLATE_METADATA` block is variable contract SSOT | Input validation; lifecycle computation |

**Flow:** caller provides a `context` dict → Layer 1 validates it → `ArtifactManager._enrich_context_v2()` adds lifecycle fields in Layer 2 → `TemplateScaffolder.render()` passes enriched context to Layer 3 → output file.

**Why three layers?** Each layer holds information the other two cannot:
- Layer 1 = user intention (what the caller specifies)
- Layer 2 = system state at render time (timestamps, paths, hashes)
- Layer 3 = structural output contract (how the artifact is formatted)

Three different concerns, three separate surfaces, zero accidental overlap when the contract is intact.

---

## 2. Layer 3 Internal Structure: Tier Hierarchy

Within Layer 3, concrete templates compose behavior from reusable tier templates. This is an internal Layer 3 concern — callers interact only with Layer 1.

### Tier Model

Templates root: `mcp_server/scaffolding/templates/`

| Tier | Purpose | Location |
|---|---|---|
| 0 | Universal lifecycle metadata (SCAFFOLD header) | `tier0_base_artifact.jinja2` |
| 1 | Format structure (CODE / DOCUMENT / TRACKING / CONFIG) | `tier1_base_*.jinja2` |
| 2 | Language/syntax framing (Python, Markdown, YAML) | `tier2_base_*.jinja2` |
| 3 | Composable pattern macro libraries | `tier3_pattern_*.jinja2` |
| Concrete | Artifact-specific output | `concrete/<type>.<ext>.jinja2` |

### Composition Rules

- Stable bases use `{% extends %}` — concrete templates extend the appropriate tier 2 base
- Optional patterns use `{% import %}` — concrete templates import tier 3 macro libraries at merge points
- Enforcement intent is expressed via `TEMPLATE_METADATA.enforcement`: tiers 0–2 are STRICT foundations, tier 3 patterns are ARCHITECTURAL, concrete templates are GUIDELINE

### TEMPLATE_METADATA: Layer 3 Variable Contract SSOT

Every concrete template contains a `TEMPLATE_METADATA` block in a `{# ... #}` comment. This block is the single source of truth for which variables are `required` vs `optional` (via `introspection.variables`), the enforcement level, and agent hints.

**Layer 1 Context schemas are derived from these variable contracts.** Required variables in `TEMPLATE_METADATA` become required fields in the Context schema; optional variables become optional fields with sensible defaults.

---

## 3. Adding a New Artifact Type

To introduce a new artifact type into the pipeline, all six steps are required.

| Step | File | What to create |
|---|---|---|
| 1 | `mcp_server/schemas/contexts/<type>.py` | Context schema: user-facing Pydantic `BaseModel`; required and optional fields matching the `TEMPLATE_METADATA` variable contract |
| 2 | `mcp_server/schemas/render_contexts/<type>.py` | RenderContext schema: extends the appropriate render base; adds lifecycle fields |
| 3 | `mcp_server/schemas/__init__.py` | Export `TypeContext` and `TypeRenderContext` |
| 4 | `mcp_server/managers/artifact_manager.py` | Add `"type_id": "TypeContext"` to `_v2_context_registry` |
| 5 | `.phase-gate/config/artifacts.yaml` | Enable the artifact type entry |
| 6 | `mcp_server/scaffolding/templates/concrete/<type>.<ext>.jinja2` | Jinja2 template with `TEMPLATE_METADATA` block including `introspection.variables` |

> **Note:** Steps 1–4 require Python source code changes. Adding a new artifact type without repository access is not currently possible.

### Context schema conventions

- Only truly required fields are required (minimalism: agent callers need minimal viable input to scaffold)
- Code artifact types: `name: str` is the only mandatory field unless the template requires more
- Document artifact types: `title: str` is the only mandatory field unless the template requires more
- All other fields are optional with sensible defaults
- Shared value objects (e.g. `MethodSpec`) must be `frozen=True`

---

## 4. Provenance Tracking

Every scaffolded artifact receives a SCAFFOLD header:

```python
# template=generic version=abc12345 created=2026-06-04T10:00Z updated=
```

```markdown
<!-- template=design version=def67890 created=2026-06-04T10:00Z updated= -->
```

| Field | Description |
|---|---|
| `template` | Artifact type (matches `type_id` in `artifacts.yaml`) |
| `version` | 8-char hash of the template content at scaffold time |
| `created` | ISO 8601 timestamp when the artifact was first scaffolded |
| `updated` | ISO 8601 timestamp of last edit (empty when first created) |

---

## Related Documentation
- **[docs/reference/mcp/README.md][related-1]**
- **[docs/reference/mcp/TEMPLATE_LIBRARY_USAGE.md][related-2]**
- **[docs/reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md][related-3]**
- **[docs/reference/mcp/template_metadata_format.md][related-4]**
- **[docs/reference/mcp/validation_api.md][related-5]**

<!-- Link definitions -->
[related-1]: ../reference/mcp/README.md
[related-2]: ../reference/mcp/TEMPLATE_LIBRARY_USAGE.md
[related-3]: ../reference/mcp/TEMPLATE_LIBRARY_QUICK_REFERENCE.md
[related-4]: ../reference/mcp/template_metadata_format.md
[related-5]: ../reference/mcp/validation_api.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.0 | 2026-06-04 | Agent | Full revision: three-layer pipeline as primary architecture; tier model repositioned as Layer 3 internal structure; 6-step new-type guide; removed legacy content (#286) |
| 1.0 | 2026-02-07 | Agent | Initial draft: tier model and Jinja2 composition |
