<!-- docs\development\issue365\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-05T20:26Z updated= -->
# Remove validate_dto and create_file tools from MCP server

**Status:** DRAFT  
**Version:** 0.1  
**Last Updated:** 2026-06-05

---

## Scope

**In Scope:**
mcp_server/tools/validation_tools.py, mcp_server/tools/code_tools.py, mcp_server/server.py, all test files referencing ValidateDTOTool or CreateFileTool

**Out of Scope:**
TemplateValidationTool, backend/, archive docs, documentation files (handled in documentation phase)

## Prerequisites

Read these first:
1. Research phase complete (docs/development/issue365/research.md)
2. Approved Strategy: clean break for both tools — no shim, no opt-out
---

## Summary

Single implementation cycle: delete ValidateDTOTool and CreateFileTool (and their Input classes) from production, unregister from server.py, and clean up all affected test files. No TDD red phase — correctness is verified by a fully green test suite after deletion. Documentation cleanup is deferred to the documentation phase.

---

## TDD Cycles


### Cycle 1: C1 — Delete tools and clean up tests

**Goal:** Remove ValidateDTOTool, ValidateDTOInput, CreateFileTool, CreateFileInput from production and server registration. Clean up all affected test files. Verify correctness via green test suite.

**Tests:**
- Delete mcp_server/tools/validation_tools.py (entire file)
- Delete mcp_server/tools/code_tools.py (entire file)
- mcp_server/server.py: remove CreateFileTool import (L68) and registration (L367); remove ValidateDTOTool import (L130) and registration (L360)
- Delete tests/mcp_server/unit/tools/test_validation_tools.py (entire file — includes test_validation_tool_class_removed, which is intentionally removed per planning decision)
- Delete tests/mcp_server/unit/tools/test_code_tools.py (entire file)
- tests/mcp_server/unit/tools/test_dev_tools.py: remove test_create_file_tool (L54-65) and test_create_file_security_check (L68-77)
- tests/mcp_server/unit/tools/test_extra_forbid.py: remove CreateFileInput import (L7) + parametrize entry (L67); remove ValidateDTOInput import (L55) + parametrize entry (L145)
- tests/mcp_server/unit/integration/test_all_tools.py: remove both tool imports, factory wiring, test_validation_tool_flow, test_create_file_tool_flow, and parametrize entries in test_all_quality_tools_have_schemas
- tests/mcp_server/tools/test_c4_description_invariants.py: remove ValidateDTOTool import (L26) and test_validate_dto_tool_description_states_scope (L78-82)
- tests/mcp_server/integration/test_pr_status_lockdown.py: remove CreateFileTool import (L52) and parametrize entry (L94)

**Success Criteria:**
Full test suite passes (pytest). Quality gates pass on all modified files (run_quality_gates scope=branch). No import of ValidateDTOTool, ValidateDTOInput, CreateFileTool, or CreateFileInput remains in any non-archive file. SafeEditTool remains in test_pr_status_lockdown.py parametrize list.


---

## Risks & Mitigation

- **Risk:** test_all_tools.py has multiple scattered references to both tools — a missed deletion would cause an ImportError at collect-time rather than a test failure
  - **Mitigation:** After editing, run pytest collection-only before full suite to catch ImportErrors early
- **Risk:** test_extra_forbid.py parametrize list: removing entries may shift indices and break unrelated parametrized cases if the list has inline dependencies
  - **Mitigation:** Verify parametrize structure before and after edit; run the narrowest possible test slice on that file

## Related Documentation
- **[docs/development/issue365/research.md][related-1]**

<!-- Link definitions -->

[related-1]: docs/development/issue365/research.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-06-05 | Agent | Initial draft |