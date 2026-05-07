# Error Taxonomy & Strict Input Validation — Planning

**Status:** DRAFT
**Version:** 1.0
**Last Updated:** 2026-05-07
**Issues:** #136 + #147 (bundled)
**Branch:** `refactor/136-error-taxonomy-and-strict-input-validation`
**References:** [research.md](research.md) · [design.md](design.md)

---

## Overview

Three independent TDD cycles implement the design decisions D1–D8 from `design.md`.

- **Cycle 1 (Change B):** Extract `_resolve_schema_refs` to shared utility, apply to `BaseTool.input_schema`, delete redundant overrides, add `extra="forbid"` to all 50 input models.
- **Cycle 2 (Change A):** Fix `_validate_tool_arguments` to return `ToolResult` on failure with `schema://validation` EmbeddedResource.
- **Cycle 3 (Change C):** Wire `NoteContext` through the full scaffold chain: `ScaffoldArtifactTool` → `ArtifactManager` → `TemplateScaffolder`.

Cycles are independent but Cycle 2 depends on Cycle 1 (the `schema://validation` resource in `_validate_tool_arguments` uses `tool.input_schema`, which must be normalized first).

---

## Scope

**In scope:**
- `mcp_server/utils/schema_utils.py` (new file — shared `_resolve_schema_refs` utility)
- `mcp_server/tools/base.py` (`BaseTool.input_schema` default normalization)
- `mcp_server/tools/issue_tools.py` (delete module-local `_resolve_schema_refs`, update import)
- `mcp_server/tools/scaffold_artifact.py` (delete redundant `input_schema` override, remove `del context`, wire `NoteContext`)
- All 50 input models in `mcp_server/tools/*.py` (`extra="forbid"`)
- `mcp_server/server.py` (`_validate_tool_arguments` return type + `handle_call_tool` guard)
- `mcp_server/managers/artifact_manager.py` (`note_context` parameter, typed notes at raise-sites)
- `mcp_server/scaffolders/template_scaffolder.py` (`note_context` parameter in `validate()` and `scaffold()`)
- Related tests in `tests/mcp_server/`

**Out of scope:**
- NoteContext wiring for `project_manager`, `enforcement_runner`, label/issue/pr/git/code/milestone tools (→ issue #321)
- `config/loader.py` and adapter-layer raises (startup/infrastructure, NoteContext architecturally unavailable)
- Granular error codes (C4: not agent-visible)
- NoteContext extension with resource rendering (C2: SRP, DRY)

---

## Cycle 1 — Change B: `_resolve_schema_refs` shared + `extra="forbid"`

**Goal:** All tools expose normalized `input_schema` (no `$defs`/`$ref`); all 50 input models are strict.

### RED — tests to write first

1. `tests/mcp_server/unit/utils/test_schema_utils.py`
   - `test_resolve_schema_refs_inlines_defs`: schema with `$defs` + `$ref` → all refs inlined
   - `test_resolve_schema_refs_preserves_descriptions`: field descriptions must survive inlining
   - `test_resolve_schema_refs_noop_on_flat_schema`: flat schema unchanged

2. `tests/mcp_server/unit/tools/test_base_tool_input_schema.py`
   - `test_base_tool_input_schema_no_defs`: any `BaseTool` subclass with nested model must not expose `$defs` in `input_schema`
   - `test_base_tool_input_schema_preserves_descriptions`

3. `tests/mcp_server/unit/tools/test_extra_forbid.py`
   - Parametrized over all 50 `*Input` models: extra field raises `ValidationError`
   - `test_safe_edit_nested_extra_forbid`: extra field inside `LineEdit` / `InsertLine` also raises

### GREEN — changes to make

1. Create `mcp_server/utils/schema_utils.py` with `_resolve_schema_refs()` (moved from `issue_tools.py`)
2. Update `mcp_server/tools/base.py`: `input_schema` imports and calls `_resolve_schema_refs`
3. Update `mcp_server/tools/issue_tools.py`: remove module-local `_resolve_schema_refs`, import from `schema_utils`; delete `CreateIssueTool.input_schema` override
4. Update `mcp_server/tools/scaffold_artifact.py`: delete `input_schema` override
5. Add `model_config = ConfigDict(extra="forbid")` to all 50 input models (and `LineEdit`, `InsertLine` nested models)

### REFACTOR — quality gates

- `run_quality_gates(scope="files", files=["mcp_server/utils/schema_utils.py", "mcp_server/tools/base.py", "mcp_server/tools/issue_tools.py"])` 
- Verify existing C9 test (`test_create_issue_schema.py`) still passes

---

## Cycle 2 — Change A: `_validate_tool_arguments` returns `ToolResult`

**Goal:** Argument validation failures return `isError=True` + `schema://validation` resource.

**Depends on:** Cycle 1 (normalized `tool.input_schema` used in failure path).

### RED — tests to write first

1. `tests/mcp_server/unit/server/test_validate_tool_arguments.py`
   - `test_returns_tool_result_on_validation_error`: extra field → `ToolResult.is_error == True`
   - `test_failure_includes_schema_resource`: response content contains `schema://validation` resource with valid JSON
   - `test_failure_includes_diagnostic_text`: text content describes the invalid field
   - `test_success_returns_model_instance`: valid input → `BaseModel` instance returned

2. `tests/mcp_server/integration/test_strict_input_validation_response.py`
   - End-to-end via `handle_call_tool`: extra field → `CallToolResult(isError=True)` + schema resource

### GREEN — changes to make

1. Update `mcp_server/server.py`:
   - `_validate_tool_arguments` return type: `BaseModel | dict[str, Any] | ToolResult`
   - Failure path: return `ToolResult` with text content + `schema://validation` EmbeddedResource from `tool.input_schema`
   - `handle_call_tool`: guard changes from `isinstance(validated, list)` to `isinstance(validated, ToolResult)`

### REFACTOR — quality gates

- `run_quality_gates(scope="files", files=["mcp_server/server.py"])`
- Confirm `_convert_tool_result_to_mcp_result` handles the new failure shape correctly (no new code path needed)

---

## Cycle 3 — Change C: NoteContext through scaffold chain

**Goal:** `ScaffoldArtifactTool` wires `NoteContext` to `ArtifactManager` and `TemplateScaffolder`; typed notes produced at all actionable raise-sites.

### RED — tests to write first

1. `tests/mcp_server/unit/tools/test_scaffold_artifact_note_context.py`
   - `test_del_context_removed`: `ScaffoldArtifactTool.execute()` must not discard `context`
   - `test_blocker_note_on_missing_template`: unknown `artifact_type` → `BlockerNote` in context
   - `test_blocker_note_on_missing_output_path`: missing output_path → `BlockerNote` in context

2. `tests/mcp_server/unit/managers/test_artifact_manager_notes.py`
   - `test_blocker_note_produced_before_config_error`: `ConfigError` for null template → note in context
   - `test_blocker_note_produced_before_validation_error`: missing output_path for file artifact → note
   - `test_recovery_note_on_write_failure`: filesystem write raises → `RecoveryNote` in context

3. `tests/mcp_server/unit/scaffolders/test_template_scaffolder_notes.py`
   - `test_blocker_note_on_no_template_configured`
   - `test_suggestion_note_on_missing_required_fields`
   - `test_blocker_note_on_template_not_found` (JinjaRenderer raises, caller note)

### GREEN — changes to make

1. `mcp_server/tools/scaffold_artifact.py`:
   - Remove `del context`
   - Pass `note_context=context` to `self.manager.scaffold_artifact(...)`

2. `mcp_server/managers/artifact_manager.py`:
   - Add `note_context: NoteContext | None = None` to `scaffold_artifact()` signature
   - Add `if note_context:` guards with `BlockerNote` before `ConfigError` (null template)
   - Add `if note_context:` guard with `BlockerNote` before `ValidationError` (missing output_path)
   - Wrap `fs_adapter.write_file()` call with `try/except MCPSystemError`; produce `RecoveryNote` if `note_context`
   - Pass `note_context` to `self.scaffolder.scaffold()`

3. `mcp_server/scaffolders/template_scaffolder.py`:
   - Add `note_context: NoteContext | None = None` to `validate()` and `scaffold()` signatures
   - `validate()`: produce `BlockerNote` before no-template `ValidationError`; produce `SuggestionNote` before missing-fields `ValidationError`
   - `scaffold()`: wrap `self._renderer.get_template()` call; produce `BlockerNote` if `note_context` before re-raising `ExecutionError`

### REFACTOR — quality gates

- `run_quality_gates(scope="files", files=["mcp_server/tools/scaffold_artifact.py", "mcp_server/managers/artifact_manager.py", "mcp_server/scaffolders/template_scaffolder.py"])`
- Run existing scaffold integration tests: `run_tests(path="tests/mcp_server/integration/test_scaffold_validation_e2e.py")`

---

## End-of-Phase Quality Gate

After all three cycles:

```
run_tests(path="tests/mcp_server/")
run_quality_gates(scope="branch")
```

All existing tests (especially C9 `test_create_issue_schema.py` and `test_blocker_recovery_note_dispatch.py`) must remain green.

---

## Related Documentation

- [docs/development/issue136/research.md](research.md)
- [docs/development/issue136/design.md](design.md)
- [docs/development/issue300/research.md](../issue300/research.md)
- [docs/development/issue295/research.md](../issue295/research.md)
- `tests/mcp_server/unit/tools/test_create_issue_schema.py` (C9 contract, must stay green)
- `tests/mcp_server/integration/test_blocker_recovery_note_dispatch.py` (NoteContext contract)
