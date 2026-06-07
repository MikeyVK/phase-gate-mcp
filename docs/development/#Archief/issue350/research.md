<!-- docs\development\issue350\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-31T20:22Z updated= -->
# scaffold_artifact: proactive schema exposure and v1 doc-type coverage

**Status:** DRAFT
**Version:** 1.0
**Last Updated:** 2026-05-31

---

## Problem Statement

`scaffold_artifact` has three gaps that force agents into multi-round-trip failure loops:

- **Gap A** — `context` is opaque at tool-discovery time: no per-type schema is visible in the MCP manifest
- **Gap B** — the validation error schema response lists field names only, omitting types and descriptions, so retries fail on the same type mismatch
- **Gap C** — there is no proactive schema-discovery path: schema is only exposed reactively after a failed call

## Research Goals

- Determine the correct scope of each gap against the current codebase state post-#358
- Identify the ArtifactManager method that should be promoted to a reusable schema-extraction helper
- Establish the JSON Schema compliant output format for context schema exposure (matching `BaseTool.input_schema` conventions)
- Determine blast radius for `TemplateSchema` format change and `ScaffoldSchemaTool` addition
- Capture the `generic_doc` V2 coverage gap (no `GenericDocContext`) as an out-of-scope finding — tracked in issue #286
- Capture the `start-issue` prompt `base_branch="main"` hardcoding as an in-scope finding: the prompt must be corrected as part of #350

## Related Documentation

- `docs/development/issue260/findings.md` — prior config centralization context
- `mcp_server/tools/scaffold_artifact.py` — `ScaffoldArtifactTool`, `ScaffoldArtifactInput`
- `mcp_server/managers/artifact_manager.py` — V1/V2 pipeline, schema-extraction inline
- `mcp_server/scaffolding/template_introspector.py` — `TemplateSchema` dataclass
- `mcp_server/core/error_handling.py` — `tool_error_handler`, schema attachment
- `mcp_server/schemas/contexts/` — all `XxxContext` Pydantic models
- `.phase-gate/config/artifacts.yaml` — artifact registry (17 types)
- `.github/prompts/start-issue.prompt.md` — in scope for #350 (step 2 hardcodes `base_branch="main"`)

---

## Background

### V1 / V2 Pipeline Architecture

The `ArtifactManager` routes each scaffold call through one of two pipelines, controlled by the feature flag `PYDANTIC_SCAFFOLDING_ENABLED` (default: `true`):

| Aspect | V1 (dict-based) | V2 (schema-typed) |
|--------|-----------------|-------------------|
| Validation timing | After rendering starts (introspection) | Before rendering (Pydantic) |
| Context input | `**kwargs` dict | Validated `XxxContext` Pydantic model |
| Schema on error | None | `TemplateSchema(required, optional)` — names only |
| Schema format | N/A | `{required: [str, ...], optional: [str, ...]}` |
| Covered types | Fallback only | 16 of 17 registered types (`generic_doc` unmapped) |

Pipeline decision point: `artifact_manager.py:648` — `if use_v2_pipeline and artifact_type in v2_supported_artifacts`.

### Artifact Registry (17 types)

| Category | Types | V2 Context class |
|----------|-------|-----------------|
| Code (8) | `dto`, `worker`, `tool`, `schema`, `service`, `generic`, `unit_test`, `integration_test` | `DTOContext`, `WorkerContext`, `ToolContext`, `SchemaContext`, `ServiceContext`, `GenericContext`, `UnitTestContext`, `IntegrationTestContext` |
| Document (6) | `research`, `planning`, `design`, `architecture`, `reference`, `generic_doc` | `ResearchContext`, `PlanningContext`, `DesignContext`, `ArchitectureContext`, `ReferenceContext`, **none** |
| Tracking (3) | `commit`, `pr`, `issue` | `CommitContext`, `PRContext`, `IssueContext` |

`generic_doc` is the only type in the V2 registry's `_v2_context_registry` dict that is absent — it falls through to the V1 pipeline.

### Context Schema Infrastructure (V2)

All 16 V2-covered types have a typed Pydantic `XxxContext` model in `mcp_server/schemas/contexts/`. Each field carries a `Field(description="...")` and a Python type annotation (`str`, `list[str]`, `str | None`, etc.). Pydantic exposes this via `model_fields: dict[str, FieldInfo]`, where `FieldInfo` carries:

- `.annotation` — Python type (e.g. `list[str]`)
- `.description` — the Field description string
- `.is_required()` — whether the field has a default

### Current Schema-Extraction Logic (inline, artifact_manager.py:694–701)

When V2 validation fails, the manager builds a `TemplateSchema` inline:

```python
_required = [f for f, fi in context_class.model_fields.items() if fi.is_required()]
_optional = [f for f, fi in context_class.model_fields.items() if not fi.is_required()]
raise ValidationError(..., schema=TemplateSchema(required=_required, optional=_optional))
```

This produces **field names only**. The `FieldInfo.annotation` and `FieldInfo.description` are available but not used. A consumer receiving `goals` in `required[]` cannot determine that `goals` expects `list[str]` rather than `str`.

### MCP Schema Format Baseline (all other tools)

`BaseTool.input_schema` (`base.py:55`) calls `model_json_schema()` + `resolve_schema_refs()`. This produces a JSON Schema Draft 7 object: `{type: "object", properties: {field: {type, description}}, required: [...]}`. MCP clients and agents parse this format natively.

### Schema Output Format Selection

Four candidate formats were evaluated for `get_context_schema()` output:

| Format | Example | Verdict |
|--------|---------|---------|
| Current names-only | `{"required": ["goals"], "optional": ["purpose"]}` | Rejected — no types, no descriptions; agents cannot distinguish `str` from `list[str]`; the retry loop is not broken |
| Custom list | `{"fields": [{"name": "goals", "type": "list[str]", "required": true, "description": "..."}]}` | Rejected — new dialect; agents and MCP clients require custom parsing; no precedent anywhere in the codebase |
| **JSON Schema Draft 7** | `{"type": "object", "properties": {"goals": {"type": "array", "items": {"type": "string"}, "description": "..."}}, "required": ["goals"]}` | **Selected** — identical contract to `BaseTool.input_schema`; MCP clients parse it natively; `model_json_schema()` already produces it from the existing Pydantic context models |
| OpenAPI Schema Object | Superset of JSON Schema Draft 7 | Rejected — not used elsewhere in the codebase; extra complexity with no benefit for this use case |

Decisive factors for JSON Schema Draft 7:
1. **Internal consistency** — every tool input schema already uses this format via `BaseTool.input_schema`; context schema must be no different
2. **Zero new parsing** — an agent that handles `input_schema` can handle `get_context_schema()` output without any new logic
3. **Pydantic native** — `context_class.model_json_schema()` already produces JSON Schema; `get_context_schema()` calls the same machinery with minimal new code

---

## Findings

### Finding 1 — Gap A is partially resolved by #358

Issue #358 (C3) added `artifact_type.enum` to `ScaffoldArtifactTool.input_schema` via A4 override. Agents can now enumerate valid artifact types at discovery time. However, the `context` parameter remains `dict[str, Any] | None` with description "Template rendering context (varies by artifact type)" — no per-type schema is exposed in the manifest.

**Residual gap:** An agent calling `scaffold_artifact` for the first time with a correct `artifact_type` still has no signal about which context fields are required, their types, or their semantics.

### Finding 2 — Gap B: TemplateSchema format is too thin

`TemplateSchema.to_dict()` (`template_introspector.py:44`) returns:

```json
{"required": ["problem_statement", "goals"], "optional": ["purpose", "scope_in", ...]}
```

`ResearchContext.goals` is annotated `list[str]` with `Field(description="Research goals / questions to answer")`. An agent supplying `"goals": "understand the problem"` (a string) fails Pydantic validation, receives the schema, sees `"goals"` in `required[]`, and has no basis to infer the list type — the retry will fail identically unless the agent guesses.

The fix is to enrich `TemplateSchema` and its `to_dict()` to expose type and description per field. The existing `FieldInfo` already carries this data.

### Finding 3 — Gap C: No proactive discovery path exists

`context=null` on `ScaffoldArtifactInput` currently passes an empty dict to the manager, which attempts scaffolding and may raise a `ConfigError` or partial error. No schema is returned on success of a null-context call.

There is no companion introspection tool or dedicated endpoint. The only schema exposure is reactive (post-error).

### Finding 4 — Promoting inline extraction to ArtifactManager method

The inline extraction at `artifact_manager.py:694–701` is the natural seed for a promoted method:

```python
def get_context_schema(self, artifact_type: str) -> dict[str, Any]:
    """Return JSON Schema for the given artifact type's context."""
```

This method can:
1. Look up `context_class` via `_v2_context_registry`
2. Iterate `context_class.model_fields` using existing `FieldInfo` access
3. Return a JSON Schema compliant dict (matching `BaseTool.input_schema` format)

Both the error-raise path (`artifact_manager.py:694–701`) and the new `ScaffoldSchemaTool` would call this method. `TemplateSchema` as an intermediate dataclass may become redundant or can be retained as an internal representation with a richer `to_json_schema()` method.

### Finding 5 — ScaffoldSchemaTool: thin wrapper approach

A new `ScaffoldSchemaTool(artifact_type: str)` wraps `ArtifactManager.get_context_schema(artifact_type)` and returns the JSON Schema as a `ToolResult`. This:

- Satisfies the SRP: schema discovery is separated from scaffold execution
- Reuses the same extraction logic as the error path — no duplication
- Exposes a dedicated MCP tool that agents can call proactively
- Keeps `ScaffoldArtifactTool.execute()` unchanged

### Finding 6 — generic_doc has no V2 Context class (out of scope — tracked in #286)

`generic_doc` is the only type without a `GenericDocContext` in `mcp_server/schemas/contexts/`. It is absent from `_v2_context_registry` in `artifact_manager.py:44` and falls through to the V1 pipeline (dict-based, no schema on error, no schema discovery). Issue #286 tracks missing templates including `generic_doc`; creating `GenericDocContext` is deferred to that issue. **This finding is out of scope for #350.**

### Finding 7 — start-issue prompt hardcodes `base_branch="main"` (in scope for #350)

`start-issue.prompt.md` step 2 reads:

```
create_branch(branch_type=WORKFLOW_TYPE, name="<short-slug-from-title>", base_branch="main")
```

The base branch is not always `main`. For child issues under an epic, the correct base branch is the epic branch (e.g. `epic/320-production-readiness-tracker`). `@co` determines the correct base branch from parent-branch context, but the prompt does not instruct this — it hardcodes `"main"`. This causes child branches to be cut from `main` instead of from the parent epic branch, silently corrupting the branch hierarchy.

**This finding is in scope for #350.** The prompt must be corrected to derive `base_branch` from parent-branch context rather than hardcoding `"main"`. The fix is a targeted correction to step 2 of `.github/prompts/start-issue.prompt.md`; no production code is affected.

---

## Blast Radius

### Production files

| File | Change | Rationale |
|------|--------|-----------|
| `mcp_server/scaffolding/template_introspector.py` | Extend `TemplateSchema` + `to_dict()` or add `to_json_schema()` | Gap B — richer format |
| `mcp_server/managers/artifact_manager.py` | Promote inline extraction to `get_context_schema(artifact_type)` method | Gap B + C + Finding 4 |
| `mcp_server/core/error_handling.py` | Update `schema.to_dict()` call site if format changes | Gap B — format migration |
| `mcp_server/tools/scaffold_artifact.py` | No changes to execute(); `input_schema` context description may be updated | Gap A residual |
| `mcp_server/tools/scaffold_schema_tool.py` | New file — `ScaffoldSchemaTool` + `ScaffoldSchemaInput` | Gap C |
| `mcp_server/server.py` | Register `ScaffoldSchemaTool` | Gap C |
| `.github/prompts/start-issue.prompt.md` | Correct step 2: derive `base_branch` from parent-branch context, remove `"main"` hardcode | Finding 7 |

### Test files at risk

| File | Risk |
|------|------|
| `tests/mcp_server/unit/core/test_validation_error_enhancement.py` | Asserts exact `{required, optional}` format — breaks on format change |
| `tests/mcp_server/unit/tools/test_scaffold_artifact.py` | Error-structure assertions |
| `tests/mcp_server/integration/test_scaffold_validation_e2e.py` | Full pipeline error response |
| `tests/mcp_server/unit/integration/test_all_tools.py` | Tool enumeration — needs `ScaffoldSchemaTool` added |

---

## Architectural Constraints

| Constraint | Source | Binding rule |
|------------|--------|-------------|
| A4 pattern | `ARCHITECTURE_PRINCIPLES.md` | Schema overrides on tool class only; Pydantic model stays pure |
| A3 forbidden | `ARCHITECTURE_PRINCIPLES.md` | No config loading inside Pydantic context models |
| SRP | `ARCHITECTURE_PRINCIPLES.md` | `ScaffoldSchemaTool` may not absorb scaffold execution; schema extraction belongs in `ArtifactManager`, not the tool |
| JSON Schema format baseline | `BaseTool.input_schema` / `schema_utils.py` | `get_context_schema()` output must match `model_json_schema()` + `resolve_schema_refs()` format |
| No duplication | Research Finding 4 | `ScaffoldSchemaTool` must call `ArtifactManager.get_context_schema()`; it must not reimplement extraction |

---

## Open Questions

1. Should `TemplateSchema` be retained as an internal intermediate, or removed in favour of passing the JSON Schema dict directly through the error path?
2. Should the error response format change be backward-incompatible (replace `{required, optional}`) or additive (extend with a `schema` key alongside the existing keys)? The single consumer is `error_handling.py` — no external API contract exists.
3. Should `ScaffoldSchemaTool` return a graceful error (or V1 introspection fallback) for `generic_doc` which currently has no V2 Context class and falls through to V1?

---

## Expected Results (Design and Planning Input)

- `ArtifactManager.get_context_schema(artifact_type)` exists as a reusable method returning JSON Schema compliant `dict[str, Any]`
- `ScaffoldSchemaTool` wraps it with no business logic of its own
- The validation error path calls the same method (or returns the same format) — schema on error is rich, not names-only
- `generic_doc` V2 coverage is deferred to issue #286 — `ScaffoldSchemaTool` must handle a graceful fallback for this type
- `.github/prompts/start-issue.prompt.md` step 2 is corrected to derive `base_branch` from parent-branch context instead of hardcoding `"main"`

---

## Approved Strategy

**Boundary: Context schema extraction**
Selected strategy: **Promote + reuse** — extract the inline schema-extraction logic from `artifact_manager.py:694–701` into a dedicated `ArtifactManager.get_context_schema(artifact_type)` method. Both the error path and `ScaffoldSchemaTool` call this method. No duplication.

**Boundary: ScaffoldSchemaTool (proactive discovery)**
Selected strategy: **Dedicated tool (Approach B)** — a new `ScaffoldSchemaTool` is the discovery surface. `scaffold_artifact` is not dual-moded. SRP is preserved.

**Boundary: Schema format (Gap B)**
Selected strategy: **JSON Schema compliant, backward-incompatible replacement** — `TemplateSchema.to_dict()` (or a new `to_json_schema()` method) returns `{type: "object", properties: {field: {type, description}}, required: [...]}`. The current `{required: [], optional: []}` format is replaced. The only consumer (`error_handling.py`) is updated in the same cycle. No external API contract exists on this format.

**Boundary: generic_doc V2 coverage**
Selected strategy: **Out of scope for #350** — deferred to issue #286. `ScaffoldSchemaTool` must return a clear error or fallback message when called for `generic_doc` (V1-only type with no Context class).

**Boundary: start-issue prompt base_branch hardcoding**
Selected strategy: **In scope for #350** — correct step 2 of `.github/prompts/start-issue.prompt.md` to derive `base_branch` from parent-branch context (the correct base is the parent epic branch, not `"main"`). The change is a targeted prompt correction; no production code is affected.

**Constraints for later phases:**
- Design must not put schema extraction logic in `ScaffoldArtifactInput` or any Pydantic model (A3/A4 boundary)
- Planning must ensure the error-format change and `ScaffoldSchemaTool` registration land in the same or closely sequenced cycles
- `GenericDocContext` must follow the `DocArtifactContext` inheritance pattern used by the other 5 doc context classes

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-31 | Agent | Initial research — gaps A/B/C, blast radius, Approved Strategy |
