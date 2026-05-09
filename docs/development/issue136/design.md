<!-- docs\development\issue136\design.md -->
<!-- template=design version=5827e841 created=2026-05-07T19:35Z updated= -->
# Error Taxonomy & Strict Input Validation

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-07

---

## Purpose

Define the architecture for predictable MCP error handling: a fixed argument-validation response path, schema://validation resources on input failures, NoteContext propagation through the scaffold chain, and $defs/$ref normalization for all tool input schemas.

## Scope

**In Scope:**
mcp_server/server.py (_validate_tool_arguments); mcp_server/tools/base.py (input_schema); mcp_server/tools/issue_tools.py (_resolve_schema_refs extraction); all 50 tool input models (extra=forbid); mcp_server/tools/scaffold_artifact.py (remove del context); mcp_server/managers/artifact_manager.py; mcp_server/scaffolders/template_scaffolder.py; mcp_server/scaffolding/renderer.py; mcp_server/adapters/filesystem.py (NoteContext wiring); related tests

**Out of Scope:**
NoteContext extension with structured resource rendering (C2 decision); granular error codes (C4 decision); NoteContext wiring in project_manager, enforcement_runner, label/issue/pr/git/code/milestone tools (tracked in issue #321); config/loader.py and adapter-layer raises (startup/infrastructure, NoteContext architecturally unavailable); $defs/$ref deep normalization beyond inline inlining (YAGNI until client issue confirmed for specific tools beyond SafeEditInput)

## Prerequisites

Read these first:
1. Research v5.0 complete (docs/development/issue136/research.md)
2. Constraint decisions C1-C5 documented in research §13
3. issue #321 created for NoteContext structural debt sweep
---

## 1. Context & Requirements

### 1.1. Problem Statement

Two connected gaps prevent predictable, agent-actionable MCP failures. (1) All 50 tool input models currently accept unknown fields silently. Applying extra='forbid' routes failures through _validate_tool_arguments() before NoteContext exists, returning a bare list[TextContent] without isError=True, no schema, and no note. (2) ScaffoldArtifactTool discards NoteContext (del context) and ArtifactManager has no NoteContext parameter, so 14+ scaffold raise-sites produce no typed notes. Additionally, SafeEditInput still exposes $defs/$ref in its input_schema (confirmed client-breaking defect from issue #99 C9), and the _resolve_schema_refs() fix exists only in issue_tools.py.

### 1.2. Requirements

**Functional:**
- [ ] When _validate_tool_arguments fails (Pydantic ValidationError), the response must have isError=True, diagnostic text, and a schema://validation EmbeddedResource from tool.input_schema
- [ ] The schema://validation resource must contain the fully normalized input schema (no $defs/$ref) for the failed tool
- [ ] _resolve_schema_refs() must be available as a shared utility and applied to all tools via BaseTool.input_schema
- [ ] ScaffoldArtifactTool must propagate NoteContext to ArtifactManager, TemplateScaffolder, JinjaRenderer, and FilesystemAdapter
- [ ] ArtifactManager and the full scaffold chain must accept NoteContext and produce typed notes (BlockerNote, SuggestionNote, RecoveryNote) at their raise-sites
- [ ] All 50 tool input models must have model_config = ConfigDict(extra='forbid')

**Non-Functional:**
- [ ] NoteContext lifecycle must not change: it is created after argument validation in handle_call_tool, not before
- [ ] tool_error_handler must remain context-agnostic (issue #283 contract)
- [ ] NoteContext/NoteEntry rendering must remain text-only (to_message() -> str); no resource-type notes
- [ ] Existing error codes (ERR_CONFIG, ERR_VALIDATION, etc.) must not change
- [ ] GitManager is the reference pattern for NoteContext propagation in the domain layer; all scaffold chain changes must follow it
- [ ] Schema normalization must not break existing CreateIssueTool behavior (C9 test must remain green)

### 1.3. Constraints

- NoteContext must not be created before argument validation (C1: SRP, Law of Demeter)
- NoteContext rendering stays text-only; no resource-type NoteEntry variants (C2: SRP, DRY)
- tool_error_handler stays context-agnostic; no operation_notes import in error_handling.py (issue #283 contract)
- Schema normalization must preserve field descriptions (issue #236: descriptions are the primary agent guidance channel)
- SafeEditInput $defs/$ref defect is confirmed breaking for VS Code/Copilot Chat (issue #99 C9)
- GitManager is the binding reference pattern for NoteContext in domain managers
---

## 2. Design Options

Three independent changes that must all be implemented; they share no runtime coupling but must be coordinated in tests.

---

### 2.A — `_validate_tool_arguments` returns `ToolResult` on failure

**Current call flow (`mcp_server/server.py`):**

```
handle_call_tool(name, arguments)
  ├─ _validate_tool_arguments(tool, arguments, call_id, name)
  │   → success: BaseModel | dict
  │   → failure: list[TextContent]        ← no isError, no schema resource, bypasses MCP pipeline
  ├─ if isinstance(validated, list):
  │       return validated                 ← raw list, not CallToolResult
  └─ ...
```

**Proposed call flow:**

```
handle_call_tool(name, arguments)
  ├─ _validate_tool_arguments(tool, arguments, call_id, name)
  │   → success: BaseModel | dict
  │   → failure: ToolResult(is_error=True) ← diagnostic text + schema://validation EmbeddedResource
  ├─ if isinstance(validated, ToolResult):
  │       return _convert_tool_result_to_mcp_result(validated)  ← same MCP conversion path
  └─ ...
```

**Interface change — `_validate_tool_arguments` failure path:**

```python
# New return type annotation
def _validate_tool_arguments(
    self, tool: BaseTool, arguments: dict[str, Any] | None, call_id: str, name: str
) -> BaseModel | dict[str, Any] | ToolResult:
    ...
    except ValidationError as validation_error:
        schema = tool.input_schema  # already normalized via BaseTool (Change B)
        return ToolResult(
            content=[
                {"type": "text", "text": f"Invalid input for {name}: {validation_error!s}"},
                {
                    "type": "resource",
                    "resource": {
                        "uri": "schema://validation",
                        "mimeType": "application/json",
                        "text": json.dumps(schema, indent=2),
                    },
                },
            ],
            is_error=True,
        )
```

**Caller change — early-return guard (`handle_call_tool`):**

```python
validated = self._validate_tool_arguments(tool, arguments, call_id, name)
if isinstance(validated, ToolResult):          # was: isinstance(validated, list)
    return self._convert_tool_result_to_mcp_result(validated)
```

**Invariants preserved:**
- `NoteContext` created after argument validation, as today.
- `tool_error_handler` not involved (remains context-agnostic, issue #283 contract).
- Response shape identical to `_convert_tool_result_to_mcp_result(ToolResult.error(...))`.

---

### 2.B — `_resolve_schema_refs` shared utility + `BaseTool.input_schema`

**Current state:**
- `_resolve_schema_refs()` defined in `mcp_server/tools/issue_tools.py` (module-local, lines 43–64).
- `BaseTool.input_schema` returns raw `self.args_model.model_json_schema()`.
- `CreateIssueTool` overrides `input_schema` to call `_resolve_schema_refs()`.
- `ScaffoldArtifactTool` overrides `input_schema` with a redundant copy (same raw call).
- `SafeEditInput` still exposes `$defs`/`$ref` (confirmed client-breaking, issue #99 C9).

**Proposed state:**

1. Move `_resolve_schema_refs()` to `mcp_server/utils/schema_utils.py` (new file, single export).
2. `BaseTool.input_schema` applies normalization by default:

```python
# mcp_server/tools/base.py — after change
from mcp_server.utils.schema_utils import _resolve_schema_refs

@property
def input_schema(self) -> dict[str, Any]:
    if self.args_model:
        return _resolve_schema_refs(self.args_model.model_json_schema())
    return {"type": "object", "properties": {}}
```

3. Delete `CreateIssueTool.input_schema` override (lines 194–195 of `issue_tools.py`) — now redundant.
4. Delete `ScaffoldArtifactTool.input_schema` override — now redundant.
5. `_resolve_schema_refs` import in `issue_tools.py` → replaced with import from `schema_utils`.
6. Existing C9 test (`test_create_issue_schema.py`) stays green without code change — it validates the `input_schema` property, which is now satisfied by the base class.

**`extra="forbid"` application:** All 50 input models listed in research §9 receive:

```python
model_config = ConfigDict(extra="forbid")
```

For nested models in `SafeEditInput` (`LineEdit`, `InsertLine`): `extra="forbid"` must also be set on each nested model; otherwise extra fields inside nested objects bypass the guard.

---

### 2.C — NoteContext propagation through scaffold chain

**Current state:**
- `ScaffoldArtifactTool.execute()` does `del context` (line 79, non-architectural marker).
- `ArtifactManager.scaffold_artifact()` has no `note_context` parameter.
- 14+ raise-sites across the scaffold chain produce no typed notes.

**Propagation strategy: parameter-per-method (GitManager reference pattern):**
- `NoteContext` is never stored as instance state on any manager or scaffolder.
- Each method that can produce notes receives `note_context` as an explicit parameter.
- Layers below `TemplateScaffolder` (JinjaRenderer, FilesystemAdapter) remain context-agnostic; their callers produce notes before re-raising.

**Call flow after change:**

```
ScaffoldArtifactTool.execute(params, context: NoteContext)
  └─ manager.scaffold_artifact(artifact_type, note_context=context, **kwargs)
       └─ ArtifactManager.scaffold_artifact(artifact_type, ..., note_context: NoteContext)
            ├─ note_context.produce(BlockerNote) before ConfigError (no template)
            ├─ note_context.produce(BlockerNote) before ValidationError (missing output_path)
            └─ self.scaffolder.scaffold(artifact_type, note_context=note_context, ...)
                 └─ TemplateScaffolder.validate(artifact_type, note_context, **kwargs)
                 │     ├─ note_context.produce(BlockerNote) before ValidationError (no template configured)
                 │     └─ note_context.produce(SuggestionNote) before ValidationError (missing required fields)
                 └─ TemplateScaffolder.scaffold(artifact_type, note_context, **kwargs)
                       ├─ try: self._renderer.get_template(path)
                       │   except ExecutionError:
                       │     note_context.produce(BlockerNote)  ← JinjaRenderer stays context-agnostic
                       │     raise
                       └─ [content validated and written by ArtifactManager]
```

**ArtifactManager filesystem error wrapping (FilesystemAdapter stays context-agnostic):**

```python
try:
    self.fs_adapter.write_file(str(output_path), result.content)
except MCPSystemError as exc:
    note_context.produce(RecoveryNote(
        message=f"Scaffold write failed at {output_path}: check path access and disk space"
    ))
    raise
```

**Interface changes:**

```python
# ScaffoldArtifactTool.execute() — del context removed
artifact_path = await self.manager.scaffold_artifact(
    params.artifact_type, note_context=context, **kwargs
)

# ArtifactManager.scaffold_artifact() — new parameter
async def scaffold_artifact(
    self,
    artifact_type: str,
    output_path: str | None = None,
    note_context: NoteContext | None = None,
    **context: Any,
) -> str:

# TemplateScaffolder.validate() — new parameter
def validate(self, artifact_type: str, note_context: NoteContext | None, **kwargs: Any) -> bool:

# TemplateScaffolder.scaffold() — new parameter
def scaffold(self, artifact_type: str, skip_validation: bool = False,
             note_context: NoteContext | None = None, **kwargs: Any) -> ScaffoldResult:
```

`NoteContext | None = None` is used (not required) for `ArtifactManager` and `TemplateScaffolder` to maintain backward compatibility with unit tests that call these layers directly. Note-producing `if note_context:` guards are added at each raise-site.

---

## 3. Chosen Design

**Decision:** Three parallel changes: (A) _validate_tool_arguments returns ToolResult on failure (not list[TextContent]); (B) _resolve_schema_refs moved to shared utility applied via BaseTool.input_schema; (C) NoteContext propagated through full scaffold chain following GitManager pattern.

**Rationale:** A keeps NoteContext lifecycle unchanged (SRP, Law of Demeter). B fixes a confirmed client-breaking defect (issue #99 C9) as a DRY refactor of existing code. C applies the established NoteContext contract (issue #283, #300) to the scaffold chain, which is the largest un-wired domain layer. All three changes use existing patterns with no new abstractions.

### 3.1. Key Design Decisions

| # | Decision | Selected option | Rationale |
|---|----------|-----------------|-----------|
| D1 | `_validate_tool_arguments` failure return type | `ToolResult(is_error=True)` with `schema://validation` EmbeddedResource | Keeps `NoteContext` lifecycle unchanged (SRP §1.1, Law of Demeter §7). Schema in `ToolResult.content` is consistent with `tool_error_handler` schema-resource precedent (DRY §2). |
| D2 | Early-return guard in `handle_call_tool` | `isinstance(validated, ToolResult)` | `ToolResult` is the established failure carrier for all other paths; using it here routes validation failures through the same `_convert_tool_result_to_mcp_result` pipeline (DRY §2). |
| D3 | Shared location for `_resolve_schema_refs` | `mcp_server/utils/schema_utils.py` (new file) | Keeps `base.py` import-clean; utility has no tool-specific dependencies; `utils/` is the established location for cross-cutting helpers in this codebase (Cohesion §10). |
| D4 | `BaseTool.input_schema` normalization | Default implementation in `BaseTool` applies `_resolve_schema_refs` | All 50+ tools inherit the fix without individual overrides (DRY §2). `CreateIssueTool` and `ScaffoldArtifactTool` override becomes redundant and must be deleted. |
| D5 | `extra="forbid"` on nested `SafeEditInput` models | `extra="forbid"` on `LineEdit` and `InsertLine` in addition to `SafeEditInput` | Extra fields in nested objects bypass the outer guard; nested strictness is required for complete enforcement (Explicit §8). |
| D6 | NoteContext propagation boundary in scaffold chain | `ArtifactManager` + `TemplateScaffolder` receive `NoteContext`; `JinjaRenderer` and `FilesystemAdapter` remain context-agnostic | Consistent with GitManager pattern: managers produce notes before raising, adapters stay I/O-only (Law of Demeter §7, Cohesion §10). Callers wrap adapter calls in try/except and produce notes there. |
| D7 | `note_context` parameter optionality in `ArtifactManager` and `TemplateScaffolder` | `NoteContext \| None = None` (optional, not required) | Backward compatibility with existing unit tests that call these layers directly without a note context. Required at `ScaffoldArtifactTool` call site where context is always available. |
| D8 | FilesystemAdapter in-scope review conclusion | Not modified; `ArtifactManager` wraps `fs_adapter.write_file()` call | Adding NoteContext to FilesystemAdapter would violate the adapter's I/O-only responsibility and create a cross-cutting dependency at the wrong layer (SRP §1.1). Design.md scope entry for `filesystem.py` resolves as: review confirmed, no change needed. |

## Related Documentation
- **[docs/development/issue136/research.md][related-1]**
- **[docs/development/issue300/research.md][related-2]**
- **[docs/development/issue300/design.md][related-3]**
- **[docs/development/issue295/research.md][related-4]**
- **[docs/development/archive/issue120/SESSIE_OVERDRACHT_IMP_20260122.md][related-5]**
- **[docs/development/archive/issue99/research.md][related-6]**
- **[mcp_server/managers/git_manager.py][related-7]**
- **[mcp_server/core/operation_notes.py][related-8]**
- **[mcp_server/core/error_handling.py][related-9]**
- **[mcp_server/server.py][related-10]**
- **[mcp_server/tools/base.py][related-11]**
- **[mcp_server/tools/issue_tools.py][related-12]**
- **[tests/mcp_server/unit/tools/test_create_issue_schema.py][related-13]**

<!-- Link definitions -->

[related-1]: docs/development/issue136/research.md
[related-2]: docs/development/issue300/research.md
[related-3]: docs/development/issue300/design.md
[related-4]: docs/development/issue295/research.md
[related-5]: docs/development/archive/issue120/SESSIE_OVERDRACHT_IMP_20260122.md
[related-6]: docs/development/archive/issue99/research.md
[related-7]: mcp_server/managers/git_manager.py
[related-8]: mcp_server/core/operation_notes.py
[related-9]: mcp_server/core/error_handling.py
[related-10]: mcp_server/server.py
[related-11]: mcp_server/tools/base.py
[related-12]: mcp_server/tools/issue_tools.py
[related-13]: tests/mcp_server/unit/tools/test_create_issue_schema.py

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |