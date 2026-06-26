<!-- docs\reference\schema-template-maintenance.md -->
<!-- template=reference version=064954ea created=2026-02-18T22:17Z updated=2026-06-26 -->
# Schema & Template Scaffolding Maintenance Reference

**Status:** DEFINITIVE  
**Version:** 2.0  
**Last Updated:** 2026-06-26  

**Source:** [mcp_server/schemas/][source]  
**Tests:** [tests/mcp_server/unit/managers/test_feature_flag.py][tests]

---

## API Reference

### Architecture: Two-Schema Pattern

Every artifact type has exactly two Pydantic classes: a user-facing **Context** and a system-enriched **RenderContext**.

```mermaid
classDiagram
    class LifecycleMixin {
        +output_path Path
        +scaffold_created datetime
        +template_id str
        +version_hash str
    }
    class BaseContext {
        <<abstract>>
        extra=forbid
    }
    class BaseRenderContext {
        <<abstract>>
    }
    class TitledArtifactContext {
        +title str
    }
    class DocArtifactContext

    BaseRenderContext --|> LifecycleMixin
    BaseRenderContext --|> BaseContext
    TitledArtifactContext --|> BaseContext
    DocArtifactContext --|> TitledArtifactContext

    class DTOContext {
        +dto_name str
        +fields list~str~
    }
    class DTORenderContext
    DTOContext --|> BaseContext
    DTORenderContext --|> BaseRenderContext
    DTORenderContext --|> DTOContext

    class DesignContext {
        +title str
        +status str
        +problem_statement str
    }
    class DesignRenderContext
    DesignContext --|> DocArtifactContext
    DesignRenderContext --|> BaseRenderContext
    DesignRenderContext --|> DesignContext
```

**Rule:** `XxxContext` = what the caller provides. `XxxRenderContext` = what the template receives. The `ArtifactManager` is the only code that crosses this boundary.

### LifecycleMixin: System-Managed Fields

Located: `mcp_server/schemas/mixins/lifecycle.py`

The mixin defines 4 fields that are **never user-provided**. They are injected by `_enrich_context()` inside `ArtifactManager`:

| Field | Type | Description |
|---|---|---|
| `output_path` | `Path` | Absolute path where artifact was written |
| `scaffold_created` | `datetime` | UTC timestamp at moment of scaffolding |
| `template_id` | `str` | Template identifier e.g. `"dto"`, `"design"` |
| `version_hash` | `str` | 8-char lowercase hex from tier-chain hash |

The `version_hash` validator enforces `len == 8` and `[0-9a-f]` only. It connects to `.phase-gate/template_registry.yaml` for provenance tracking.

`BaseRenderContext` inherits both `LifecycleMixin` and `BaseContext`, so every `XxxRenderContext` automatically has all 4 lifecycle fields plus the artifact-specific fields.

### Scaffolding Pipeline: Full Data Flow

Triggered when `PYDANTIC_SCAFFOLDING_ENABLED=true` (default) and `context_class` is configured in `artifacts.yaml`.

```mermaid
sequenceDiagram
    participant Tool as ScaffoldArtifactTool
    participant AM as ArtifactManager
    participant Ctx as XxxContext
    participant RC as XxxRenderContext
    participant Scaf as TemplateScaffolder
    participant FS as FilesystemAdapter

    Tool->>AM: scaffold_artifact(type, name=X, **user_context)
    AM->>AM: Strip routing params {name, output_path}
    AM->>Ctx: XxxContext.model_validate(user_context)
    Note over Ctx: extra=forbid catches unknown fields
    Ctx-->>AM: validated XxxContext
    AM->>RC: _enrich_context(context, type)
    Note over RC: Naming Convention lookup<br/>XxxContext → XxxRenderContext<br/>via mcp_server.schemas globals()
    RC-->>AM: XxxRenderContext with lifecycle fields
    AM->>AM: Inject computed version_hash
    AM->>Scaf: scaffold(type, **render_ctx.model_dump())
    Note over Scaf: Resolved template via artifacts.yaml<br/>(e.g. dto_v2.py.jinja2)
    Scaf-->>AM: TemplateResult(content=...)
    AM->>FS: write_file(path, content)
    FS-->>Tool: absolute file path
```

**Fallback:** If `PYDANTIC_SCAFFOLDING_ENABLED=false` or no schema registry is configured in `artifacts.yaml`, a raw dict-based pipeline runs unchanged. Tests use `monkeypatch.setenv('PYDANTIC_SCAFFOLDING_ENABLED', 'false')` to opt out explicitly.

### Artifacts Configuration: Type Mapping

Located: `.phase-gate/config/artifacts.yaml`

This YAML file drives scaffolding routing. Every entry maps an `artifact_type` string to a `context_class` name resolved from `mcp_server.schemas`.

| artifact_type | Context class | Template file |
|---|---|---|
| `dto` | `DTOContext` | `concrete/dto.py.jinja2` |
| `worker` | `WorkerContext` | `concrete/worker.py.jinja2` |
| `tool` | `ToolContext` | `concrete/tool.py.jinja2` |
| `schema` | `SchemaContext` | `concrete/config_schema.py.jinja2` |
| `service` | `ServiceContext` | `concrete/service_command.py.jinja2` |
| `generic` | `GenericContext` | `concrete/generic.py.jinja2` |
| `unit_test` | `UnitTestContext` | `concrete/test_unit.py.jinja2` |
| `integration_test` | `IntegrationTestContext` | `concrete/test_integration.py.jinja2` |
| `research` | `ResearchContext` | `concrete/research.md.jinja2` |
| `planning` | `PlanningContext` | `concrete/planning.md.jinja2` |
| `design` | `DesignContext` | `concrete/design.md.jinja2` |
| `architecture` | `ArchitectureContext` | `concrete/architecture.md.jinja2` |
| `reference` | `ReferenceContext` | `concrete/reference.md.jinja2` |
| `commit` | `CommitContext` | `concrete/commit.txt.jinja2` |
| `pr` | `PRContext` | `concrete/pr.md.jinja2` |
| `issue` | `IssueContext` | `concrete/issue.md.jinja2` |
| `validation_report` | `ValidationReportContext` | `concrete/validation_report.md.jinja2` |

Schema validation guarantees presence and catches missing/extra fields before rendering templates.

### Template ↔ Schema Contract

Templates access context fields directly by name. Unvalidated templates use defensive `{{ field | default('') }}` patterns. Schema-validated templates omit defenses because the schema guarantees presence.

**Validated template pattern** (`dto.py.jinja2`):
```jinja
# Schema-guaranteed: dto_name and fields always present
class {{ dto_name }}(BaseModel):
    {% for field_def in fields %}
    {{ field_def }} = Field(description="{{ field_def.split(':')[0].strip() }} field")
    {% endfor %}
```

**Contract rule:** The template variable names must match the Pydantic field names on the `XxxRenderContext`. Change a field name in the schema → must change it in the template. The reverse is also true.

### Routing Parameters: name and output_path

Two kwargs are **routing params**, not user context. They are stripped before `model_validate()` and handled separately:

| Param | Injected by | Purpose | Where restored |
|---|---|---|---|
| `name` | `ScaffoldArtifactTool` (always) | `get_artifact_path(type, name)` for path resolution | `enriched_context["name"]` after `model_dump()` |
| `output_path` | Caller (optional) | Explicit output override | `provided_output_path` param of `_enrich_context()` |

The strip set is `_strip_keys = {"output_path", "name"}` in `ArtifactManager`. Any future routing param added to `scaffold_artifact()` must also be added to this set.

**Why this matters:** `XxxContext` schemas declare `extra='forbid'`. Any unknown key (including routing params) causes `ValidationError`. This is enforced by Pydantic, not by application code — which means mistakes surface immediately as `extra_forbidden` errors rather than silently corrupting context.

### Adding a New Artifact Type: Step-by-Step

Follow these steps exactly in order. Each step is mandatory unless marked optional.

**1. Create the Context schema** (`mcp_server/schemas/contexts/new_type.py`)
```python
from mcp_server.schemas.base import BaseContext  # or DocArtifactContext for docs
from pydantic import Field

class NewTypeContext(BaseContext):
    """User-facing context for new_type artifacts."""
    # Required fields (all user must provide)
    my_required_field: str = Field(description="...")
    # Optional fields with defaults
    my_optional: list[str] = Field(default_factory=list, description="...")
```
Rules: `extra='forbid'` is inherited. Field names must match the template variables exactly.

**2. Create the RenderContext** (`mcp_server/schemas/render_contexts/new_type.py`)
```python
from mcp_server.schemas.base import BaseRenderContext
from mcp_server.schemas.contexts.new_type import NewTypeContext

class NewTypeRenderContext(BaseRenderContext, NewTypeContext):
    """System-enriched context for new_type template rendering."""
    pass  # Inherits all fields via multiple inheritance
```
This class body is always `pass`. All logic lives in the base classes.

**3. Export from `mcp_server/schemas/__init__.py`**
```python
from mcp_server.schemas.contexts.new_type import NewTypeContext
from mcp_server.schemas.render_contexts.new_type import NewTypeRenderContext
```
Mandatory: `_enrich_context()` discovers `NewTypeRenderContext` via `getattr(schemas_module, 'NewTypeRenderContext')`. If not exported, the schema pipeline falls back to dict-based logic.

**4. Register in `.phase-gate/artifacts.yaml`**
Add the new `type_id` and map the Pydantic context class using the `context_class` attribute:
```yaml
artifacts:
  - type_id: new_type
    context_class: NewTypeContext
    template_path: concrete/new_type.py.jinja2
    type: code
```

**5. Create the template** (`mcp_server/scaffolding/templates/concrete/new_type.py.jinja2`)
Use template variables that match the `NewTypeContext` field names exactly. No `| default()` guards needed — schema validation guarantees field presence.

**6. Write a smoke test** (see `tests/mcp_server/integration/test_smoke_all_types.py` for the pattern):
```python
@pytest.mark.parametrize("artifact_type,context", [
    ("new_type", {"my_required_field": "value"}),
])
def test_smoke_new_type(v2_manager, artifact_type, context):
    result = asyncio.run(v2_manager.scaffold_artifact(artifact_type, **context))
    assert result is not None
```

### Base Class Selection Guide

Choose the right base class for the Context schema:

| Base class | Use for | Inherits |
|---|---|---|
| `BaseContext` | Code artifacts: dto, worker, tool, service, unit_test, integration_test, generic, schema | `extra=forbid` |
| `TitledArtifactContext` | Tracking artifacts that need a `title` field: commit, pr, issue | `BaseContext` + `title: str` + non-empty validator |
| `DocArtifactContext` | Document artifacts: design, research, planning, architecture, reference, validation_report | `TitledArtifactContext` |

**Never** inherit directly from `BaseRenderContext` in a Context class. The only classes that may inherit from `BaseRenderContext` are `XxxRenderContext` classes.

## Related Documentation
None

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.0 | 2026-06-26 | Agent | Refactored V2 scaffolding pipeline terminology to neutral schema-based naming, and moved registry mapping description to artifacts.yaml |
| 1.0 | 2026-02-18 | Agent | Initial draft |

<!-- Link definitions -->
[source]: ../../mcp_server/schemas/
[tests]: ../../tests/mcp_server/unit/managers/test_feature_flag.py