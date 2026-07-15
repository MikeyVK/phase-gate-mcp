<!-- docs\development\issue349\design.md -->
<!-- template=design version=5827e841 created=2026-07-15T17:38Z updated=2026-07-15T18:00Z -->
# Dynamic YAML Schema Validation

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-07-15

---

## Purpose

Define the technical schema and architecture required to transition to pure declarative template resolution and absorb Issue #326 (Remove V1 pipeline and feature flag).

## Scope

**In Scope:**
- Refactoring ArtifactManager, ArtifactRegistryConfig, get_schema tool, scaffold_artifact tool.
- Deletion of V1 dict-based fallback and `PYDANTIC_SCAFFOLDING_ENABLED` feature flag (Closes #326).
- Deletion of legacy python `contexts` and `render_contexts`.

**Out of Scope:**
- Template registry versioning (deferred to another issue).

---

## 1. Context & Requirements

### 1.1. Problem Statement

The scaffolding trinity (Jinja2 templates, artifacts.yaml, Pydantic context schemas) is currently bundled, requiring Python source code modifications for any template overrides. The Python dependency introduces security risks and blocks dynamic workspace-local overrides. Furthermore, the legacy V1 fallback pipeline and feature flag add dead weight and maintenance overhead.

### 1.2. Requirements

**Functional:**
- [ ] Artifact templates must be resolved purely via the configured template_root
- [ ] Artifact schemas must be dynamically validated directly against configurations defined in artifacts.yaml at config_root
- [ ] No Python context classes or plugin registries may be required or loaded
- [ ] The generic lifecycle fields (output_path, etc.) must still be injected seamlessly
- [ ] The V1 dict-based fallback pipeline and `PYDANTIC_SCAFFOLDING_ENABLED` feature flag must be entirely removed.

**Non-Functional:**
- [ ] Validation must fail-fast matching the existing pydantic validation behavior
- [ ] The get_schema() tool must return a valid JSON Schema compliant with MCP specs
- [ ] No server restarts required to change a template or schema field constraint

### 1.3. Constraints

- Must preserve the exact same user-facing CLI/MCP tool arguments so the LLM experience is not broken

---

## 2. Design Options

| Option | Pros | Cons |
|--------|------|------|
| **A: Pydantic create_model (Chosen)** | ✅ Preserves CQS via frozen=True<br>✅ `model_json_schema()` works natively<br>✅ Consistent with Config-First architecture | ❌ Requires a dynamic builder to map YAML to Pydantic types |
| **B: Pure jsonschema package** | ✅ Direct 1-to-1 mapping with YAML definitions | ❌ Violates CQS (returns mutable dicts)<br>❌ Requires custom JSON schema generation for MCP endpoint |

---

## 3. Chosen Design

**Decision:** Implement Option A (Pydantic create_model). We will completely drop python module lookup for context schemas, eliminate the V1 fallback pipeline, and replace it with an in-memory builder in ArtifactManager.

**Rationale:** Option A strictly adheres to ARCHITECTURE_PRINCIPLES.md (CQS / Frozen query results, Config-First fail fast validation). Retaining Pydantic models keeps blast radius low for downstream consumers and get_schema(), while fulfilling the Clean Break strategy. Removing the V1 pipeline removes technical debt.

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| artifacts.yaml defines purely declarative schema constraints (e.g. min_length, pattern, type) instead of a 'context_class' string. | SSOT constraint - single source of truth for template validation. |
| Remove explicit *RenderContext classes. Use a generic RenderContext builder that injects lifecycle fields into the dynamically built Pydantic model. | Reduces boilerplate; dynamic schema can inherit base fields automatically. |

### 3.2. Concrete Interface Contracts

**1. Configuration Schema (artifacts.yaml changes):**
The `ArtifactRegistryConfig` will drop `context_class` and use a declarative schema definition:
```python
class SchemaFieldDef(BaseModel):
    model_config = ConfigDict(frozen=True)
    type: str  # "string", "array", "boolean", "integer"
    title: str
    description: str
    default: Any | None = None
    required: bool = True
    # Validation constraints
    min_length: int | None = None
    pattern: str | None = None
    items: dict[str, str] | None = None  # for arrays e.g. {"type": "string"}

class ArtifactDef(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    description: str
    template_name: str | None = None
    # REPLACES context_class:
    context_schema: dict[str, SchemaFieldDef] | None = None
```

**2. Generic Render Context Model:**
A dynamic builder generates Pydantic models at runtime that inherit from a base context.
```python
class BaseRenderContext(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    # Base lifecycle fields injected by ArtifactManager (aligned with LifecycleMixin)
    scaffold_created: str | None = None
    template_id: str | None = None
    output_path: str | None = None
    version_hash: str | None = None
```

**3. ArtifactManager Method Signatures:**
```python
class ArtifactManager:
    # No changes to public signatures, only internal resolution changes:
    def get_schema(self, artifact_type: str) -> dict[str, Any]:
        # Returns model_json_schema() from dynamically generated model
        ...

    def scaffold_artifact(self, artifact_type: str, name: str, context: dict[str, Any]) -> ScaffoldResult:
        # Validates context against dynamic Pydantic model instead of getattr(schemas_module)
        # Drops ALL V1 pipeline fallback dict logic.
        ...
```

### 3.3. Testing Strategy & Constraints

**Test Relevance & Pruning:**
- Tests must validate the new dynamic YAML-driven behavior and the clean break from Python bundled dependencies.
- Avoid writing dedicated regression tests simply to assert that old legacy behavior is removed. The old components will be deleted entirely, which implicitly breaks and cleans up legacy tests.
- Explicitly delete the 17 parity tests from Issue #326.

**Test Hygiene & Architectural Purity:**
- **Single Source of Truth (SSOT):** Test fixtures and helpers must use central path resolution.
- **DRY (Don't Repeat Yourself):** Reusable logic for scaffolding mock templates and configuration must be extracted to unified helpers.
- All testing must strictly follow the `ARCHITECTURE_PRINCIPLES.md`, including isolation and clean data flow.

## Related Documentation
- **[docs/development/issue349/research.md][related-1]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/development/issue349/research.md
[related-2]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-15 | Agent | Initial draft |
| 1.1 | 2026-07-15 | Agent | Add concrete interface contracts, options table |
| 1.2 | 2026-07-15 | Agent | Broadened scope with Issue #326, reconciled lifecycle fields |