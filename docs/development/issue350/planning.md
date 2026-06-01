<!-- docs\development\issue350\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-01T06:54Z updated= -->
# scaffold_artifact: proactive schema exposure and v1 doc-type coverage

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-01

---

## Scope

**In Scope:**
ArtifactManager.get_context_schema(); ScaffoldSchemaTool; TemplateSchema removal; error_handling.py schema format; start-issue.prompt.md step 2

**Out of Scope:**
generic_doc V2 migration (deferred to #286); ScaffoldArtifactTool changes beyond error path wiring; other prompt files

## Prerequisites

Read these first:
1. Design approved (issue #350)
2. Phase: planning
---

## Summary

Three-cycle plan: (C1) ArtifactManager.get_context_schema() + TemplateSchema removal + error path fix; (C2) ScaffoldSchemaTool + server registration; (C3) start-issue.prompt.md base_branch correction.

---

## Dependencies

- C2 depends on C1 (get_context_schema must exist before ScaffoldSchemaTool can delegate)

---

## TDD Cycles


### Cycle 1: C1: get_context_schema + TemplateSchema removal + error path

**Goal:** Implement ArtifactManager.get_context_schema(), remove TemplateSchema, and update error_handling.py to use dict directly.

**Tests:**
- tests/mcp_server/unit/managers/test_artifact_manager.py
- tests/mcp_server/unit/core/test_validation_error_enhancement.py
- tests/mcp_server/integration/test_scaffold_validation_e2e.py
- tests/mcp_server/unit/tools/test_scaffold_artifact.py

**Success Criteria:**
get_context_schema returns valid JSON Schema for V2 types; ConfigError for generic_doc; TemplateSchema removed; error path returns dict; all tests green; gates 10.00 + type-check pass

**Architecture obligations:**
- `get_context_schema` must be a pure method (no I/O, no async, no side effects)
- No config loading inside any Context class (A3)
- `ValidationError.schema: Any` type annotation unchanged — value changes from `TemplateSchema` to `dict[str, Any]`
- No `TemplateSchema` import may remain outside its own deleted file

**Typing obligations:**
- `get_context_schema(artifact_type: str) -> dict[str, Any]` — explicit return type
- mypy must pass without new `# type: ignore` directives


### Cycle 2: C2: ScaffoldSchemaTool + server registration

**Goal:** Implement ScaffoldSchemaTool (read-only, A4 pattern) and register it in server.py.

**Tests:**
- tests/mcp_server/unit/tools/test_scaffold_schema_tool.py
- tests/mcp_server/unit/integration/test_all_tools.py

**Success Criteria:**
scaffold_schema in tool manifest; execute() delegates to manager; input_schema.artifact_type.enum populated; all tests green; gates pass

**Architecture obligations:**
- `ScaffoldSchemaTool` inherits `BaseTool`, NOT `BranchMutatingTool` (read-only)
- A4 pattern: `input_schema` override on tool class only; `ScaffoldSchemaInput` Pydantic model stays pure
- `execute()` must contain no extraction logic — delegates entirely to `self.manager.get_context_schema()`
- `model_config = ConfigDict(extra="forbid")` on `ScaffoldSchemaInput`

**Typing obligations:**
- `ScaffoldSchemaTool.execute()` return type: `ToolResult`
- `input_schema` property return type: `dict[str, Any]`
- mypy must pass without new `# type: ignore` directives

**Dependencies:** C1


### Cycle 3: C3: start-issue.prompt.md base_branch correction

**Goal:** Replace hardcoded base_branch='main' with 4-step git_list_branches derivation algorithm.

**Tests:**

**Success Criteria:**
No hardcoded main in branch-creation step; step numbering consistent; prompt coherent

**Scope note:** Prompt file only — no Python production code affected. No automated tests; manual review in QA validates correctness.

**Architecture obligations:** N/A (no Python code)


---

## Risks & Mitigation

- **Risk:** C1 test blast radius: 4 test files with format-breaking assertions (TemplateSchema → JSON Schema dict)
  - **Mitigation:** Update all 4 in same RED cycle; run full suite before GREEN commit
- **Risk:** A4 pattern compliance for ScaffoldSchemaTool.input_schema override
  - **Mitigation:** Mirror ScaffoldArtifactTool pattern exactly; QA verifier checks A4 compliance

## Related Documentation
- **[docs/development/issue350/research.md][related-1]**
- **[docs/development/issue350/design.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/development/issue350/research.md
[related-2]: docs/development/issue350/design.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |