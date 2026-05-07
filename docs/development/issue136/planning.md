# Error Taxonomy & Strict Input Validation — Planning

**Status:** DRAFT
**Version:** 2.0
**Last Updated:** 2026-05-07
**Issues:** #136 + #147 (bundled)
**Branch:** `refactor/136-error-taxonomy-and-strict-input-validation`
**References:** [research.md](research.md) · [design.md](design.md)

---

## Overview

Three TDD cycles implement design decisions D1–D8 from `design.md`. Cycle 2 depends on Cycle 1 (normalized `tool.input_schema` must exist before the failure path can use it); Cycle 3 is fully independent.

---

## Scope Rationale

**Why these three changes are bundled (not separate issues):**

`extra="forbid"` (Change B) is the trigger for the entire issue: without it, argument validation failures are rare edge cases. Once applied to all 50 input models, every agent typo routes through `_validate_tool_arguments` — making Change A's fix a pre-condition for safe rollout of Change B, not an optional improvement. Splitting them across issues would leave a broken window between merges.

Change C (scaffold chain) is bundled because it applies the same NoteContext taxonomy established in this issue to the most prominent un-wired domain layer. The `del context` marker was explicitly left as a non-architectural placeholder (research §8), and the sweep (issue #321 research task) confirmed the scaffold chain is the only actionable subset in this issue's blast radius. Moving it to a separate issue would delay the taxonomy to a second implementation phase without architectural benefit.

**Why Cycle 1 (B) runs before Cycle 2 (A):**

The `schema://validation` EmbeddedResource in `_validate_tool_arguments`' failure path is built from `tool.input_schema`. If `tool.input_schema` still contains `$defs`/`$ref` at that point, the schema resource will be client-breaking for tools with nested models (confirmed defect, issue #99 C9). Cycle 1 normalizes all schemas first; Cycle 2 then relies on that guarantee.

**Why Cycle 3 (C) is last:**

Cycle 3 is independent but placed last because: (1) it has the largest surface area (four files, 14+ raise-sites) and benefits from having the rest of the suite green as a baseline; (2) the `NoteContext` pattern it applies is validated end-to-end by Cycle 1 and 2 tests, giving the implementer higher confidence before touching the scaffold chain.

---

## Scope

**In scope:**
- `mcp_server/utils/schema_utils.py` (new file — shared `_resolve_schema_refs` utility)
- `mcp_server/tools/base.py` (`BaseTool.input_schema` default normalization)
- `mcp_server/tools/issue_tools.py` (delete module-local `_resolve_schema_refs`, update import)
- `mcp_server/tools/scaffold_artifact.py` (delete redundant `input_schema` override, remove `del context`, wire `NoteContext`)
- All 50 input models in `mcp_server/tools/*.py` (`extra="forbid"`, incl. nested `LineEdit` and `InsertLine`)
- `mcp_server/server.py` (`_validate_tool_arguments` return type + `handle_call_tool` guard)
- `mcp_server/managers/artifact_manager.py` (`note_context` parameter, typed notes at raise-sites)
- `mcp_server/scaffolders/template_scaffolder.py` (`note_context` parameter in `validate()` and `scaffold()`)
- Related tests in `tests/mcp_server/`

**Out of scope:**
- NoteContext wiring for `project_manager`, `enforcement_runner`, label/issue/pr/git/code/milestone tools (→ issue #321)
- `config/loader.py` and adapter-layer raises (startup/infrastructure, NoteContext architecturally unavailable)
- Granular error codes (C4 decision: not agent-visible)
- NoteContext extension with resource rendering (C2 decision: SRP, DRY)

---

## Cycle Deliverables Overview

### Cycle 1 — Change B: `_resolve_schema_refs` shared + `extra="forbid"`

**Goal:** All tools expose normalized `input_schema` (no `$defs`/`$ref`); all 50 input models are strict.

| ID | Deliverable | Gate |
|----|-------------|------|
| D1.1 | `mcp_server/utils/schema_utils.py` created with `_resolve_schema_refs()` | `file_exists` |
| D1.2 | `BaseTool.input_schema` calls `_resolve_schema_refs` | `contains_text` in `tools/base.py` |
| D1.3 | Module-local `_resolve_schema_refs` removed from `issue_tools.py` | `absent_text` in `issue_tools.py` |
| D1.4 | `CreateIssueTool.input_schema` override removed | `absent_text`: `def input_schema` absent in `CreateIssueTool` block |
| D1.5 | `extra="forbid"` present in all tool input model files (spot-check: `safe_edit_tool.py`) | `contains_text` in `safe_edit_tool.py` |
| D1.6 | `extra="forbid"` on `LineEdit` nested model | `contains_text` in `safe_edit_tool.py` |
| D1.7 | `extra="forbid"` on `InsertLine` nested model | `contains_text` in `safe_edit_tool.py` |
| D1.8 | `ScaffoldArtifactTool.input_schema` override removed | `absent_text`: `def input_schema` absent in `scaffold_artifact.py` |

**Exit criteria:** All D1.x gates pass; C9 test (`test_create_issue_schema.py`) remains green; full test suite green.

---

### Cycle 2 — Change A: `_validate_tool_arguments` returns `ToolResult`

**Goal:** Argument validation failures return `isError=True` + `schema://validation` resource.
**Pre-condition:** Cycle 1 complete (normalized `tool.input_schema`).

| ID | Deliverable | Gate |
|----|-------------|------|
| D2.1 | `_validate_tool_arguments` return type includes `ToolResult` | `contains_text` in `server.py`: `ToolResult` in return annotation |
| D2.2 | Failure path returns `ToolResult` with `is_error=True` | `contains_text` in `server.py`: `is_error=True` |
| D2.3 | `schema://validation` resource in failure path | `contains_text` in `server.py`: `schema://validation` |
| D2.4 | Early-return guard uses `isinstance(validated, ToolResult)` | `contains_text` in `server.py`: `isinstance(validated, ToolResult)` |
| D2.5 | Old `isinstance(validated, list)` guard absent | `absent_text` in `server.py`: `isinstance(validated, list)` |

**Exit criteria:** All D2.x gates pass; integration test (`test_strict_input_validation_response.py`) green; full test suite green.

---

### Cycle 3 — Change C: NoteContext through scaffold chain

**Goal:** Typed notes produced at all actionable scaffold raise-sites.

| ID | Deliverable | Gate |
|----|-------------|------|
| D3.1 | `del context` absent from `ScaffoldArtifactTool.execute()` | `absent_text` in `scaffold_artifact.py`: `del context` |
| D3.2 | `ArtifactManager.scaffold_artifact` accepts `note_context` parameter | `contains_text` in `artifact_manager.py`: `note_context` |
| D3.3 | `TemplateScaffolder.validate` accepts `note_context` parameter | `contains_text` in `template_scaffolder.py`: `note_context` |
| D3.4 | `TemplateScaffolder.scaffold` accepts `note_context` parameter | `contains_text` in `template_scaffolder.py`: `note_context` |
| D3.5 | `BlockerNote` imported and used in `artifact_manager.py` | `contains_text` in `artifact_manager.py`: `BlockerNote` |
| D3.6 | `RecoveryNote` imported and used in `artifact_manager.py` | `contains_text` in `artifact_manager.py`: `RecoveryNote` |
| D3.7 | `SuggestionNote` imported and used in `template_scaffolder.py` | `contains_text` in `template_scaffolder.py`: `SuggestionNote` |

**Exit criteria:** All D3.x gates pass; existing scaffold integration test (`test_scaffold_validation_e2e.py`) remains green; full test suite green.

---

## Cycle 1 — TDD Plan

### RED — tests to write first

1. `tests/mcp_server/unit/utils/test_schema_utils.py`
   - `test_resolve_schema_refs_inlines_defs`: schema with `$defs` + `$ref` → all refs inlined
   - `test_resolve_schema_refs_preserves_descriptions`: field descriptions survive inlining
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
5. Add `model_config = ConfigDict(extra="forbid")` to all 50 input models and to `LineEdit`, `InsertLine`

### REFACTOR — quality gates

- `run_quality_gates(scope="files", files=["mcp_server/utils/schema_utils.py", "mcp_server/tools/base.py", "mcp_server/tools/issue_tools.py"])`
- Verify existing C9 test (`test_create_issue_schema.py`) still passes

---

## Cycle 2 — TDD Plan

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

## Cycle 3 — TDD Plan

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

1. `mcp_server/tools/scaffold_artifact.py`: Remove `del context`; pass `note_context=context` to `self.manager.scaffold_artifact(...)`
2. `mcp_server/managers/artifact_manager.py`: Add `note_context: NoteContext | None = None`; add `if note_context:` guards with typed notes at all actionable raise-sites; wrap `fs_adapter.write_file()` in try/except with `RecoveryNote`; pass `note_context` to `self.scaffolder.scaffold()`
3. `mcp_server/scaffolders/template_scaffolder.py`: Add `note_context: NoteContext | None = None` to `validate()` and `scaffold()`; produce `BlockerNote` before no-template `ValidationError`; produce `SuggestionNote` before missing-fields `ValidationError`; wrap `self._renderer.get_template()` and produce `BlockerNote` before re-raising `ExecutionError`

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

All existing tests (especially `test_create_issue_schema.py` C9 and `test_blocker_recovery_note_dispatch.py`) must remain green.

---

## Related Documentation

- [docs/development/issue136/research.md](research.md)
- [docs/development/issue136/design.md](design.md)
- [docs/development/issue300/research.md](../issue300/research.md)
- [docs/development/issue295/research.md](../issue295/research.md)
- `tests/mcp_server/unit/tools/test_create_issue_schema.py` (C9 contract, must stay green)
- `tests/mcp_server/integration/test_blocker_recovery_note_dispatch.py` (NoteContext contract)
