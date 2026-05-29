<!-- docs\development\issue346\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-29T13:59Z updated= -->
# Remove validate_architecture stub tool from MCP server

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-29

---

## Purpose

Establish the full evidence base for a clean stub removal with zero production risk.

## Scope

**In Scope:**
ValidationTool + ValidationInput classes; server.py import/registration; stub test in test_validation_tools.py; make_validation_tool in test_all_tools.py; qa.agent.md allowed tool entry; active docs (quality.md, README.md, 03_tool_layer.md, 08_naming_landscape.md, TOOLS.md); archive docs with active references (VSCODE_AGENT_ORCHESTRATION.md, PHASE_WORKFLOWS.md, GAP_ANALYSIS_IMPLEMENTATION_PLAN.md)

**Out of Scope:**
ValidateDTOTool and ValidateDTOInput (no changes); QAManager itself; backend/ modules; docs/development/archive/ issue135, issue99, issue19, issue273 (historical only)

---

## Problem Statement

ValidationTool (validate_architecture) is a stub that unconditionally returns success without performing any validation. It is registered in server.py and agent-visible, producing false-positive signals. Stubs do not belong in a production tool inventory.

## Research Goals

- Identify all code, test, and documentation surfaces that reference validate_architecture or ValidationTool
- Determine exact removal scope without breaking ValidateDTOTool or other quality tools
- Confirm blast radius and establish approved deletion strategy

---

## Findings

1. ValidationTool.execute() (validation_tools.py L42-44) always returns ToolResult.text('Architecture validation passed for scope: {scope}') with a # Stub implementation comment — no real checks are performed.
2. ValidationInput model (L14-23) has a scope field with a pattern constraint but is functionally unused.
3. QAManager is imported (L9) and injected in ValidationTool.__init__ (L33) but never called in execute(). ValidateDTOTool does not use QAManager — the import can be removed entirely.
4. server.py imports ValidationTool at line 129 and registers it at line 355 under # Quality tools.
5. test_validation_tools.py contains 1 stub test (test_validation_tool, L19-22) AND 2 real ValidateDTOTool tests (L28-55) — the file cannot be deleted; only the stub test + its ValidationTool/ValidationInput imports must be removed.
6. test_all_tools.py imports ValidationTool (L54) and defines make_validation_tool factory (L172-173).
7. qa.agent.md L25 lists phase-gate-mcp/validate_architecture as an allowed tool for the QA agent.
8. Active docs referencing the tool: quality.md, README.md (tool counts 50->49, Quality 4->3), 03_tool_layer.md (validation_tools.py: 2 tools -> 1 tool), 08_naming_landscape.md (ValidationTool row), TOOLS.md (tool count).
9. Archive docs with live references: VSCODE_AGENT_ORCHESTRATION.md (6 occurrences), PHASE_WORKFLOWS.md, GAP_ANALYSIS_IMPLEMENTATION_PLAN.md.
10. No references in backend/ modules or __init__.py exports — no hidden consumers.

## Open Questions

None. The tool count assertion question was resolved during research: `test_all_tools.py` contains no assertions on total tool count. No open questions remain for planning.

---

## Approved Strategy

**Boundary:** `validate_architecture` MCP tool — agent-visible tool surface, test surface, documentation surface.

**Selected strategy:** Clean break — complete removal with no compatibility bridge or deprecation period.

**Rationale:** The tool has no real implementation and no legitimate consumers. It is not referenced in AGENTS.md, the Tool Priority Matrix, or any documented workflow. No external caller can depend on a stub that always returns success. A clean break eliminates the false-positive signal immediately and leaves no dead code.

**Constraints for later phases:**
- `ValidateDTOTool` and its tests must remain fully intact.
- `QAManager` itself is not in scope; only its import in `validation_tools.py` is removed.
- Archive docs under `docs/development/archive/` are out of scope; only active and currently referenced docs require updates.
- `test_validation_tools.py` must not be deleted; only the stub test and its stub-specific imports are removed.
- Tool count references in active docs must be updated: 50 → 49 total; Quality 4 → 3.


## Related Documentation
- **[mcp_server/tools/validation_tools.py][related-1]**
- **[mcp_server/server.py lines 129 and 355][related-2]**
- **[tests/mcp_server/unit/tools/test_validation_tools.py][related-3]**
- **[tests/mcp_server/unit/integration/test_all_tools.py lines 54 and 172-173][related-4]**
- **[.github/agents/qa.agent.md line 25][related-5]**
- **[docs/reference/mcp/tools/quality.md][related-6]**
- **[docs/reference/mcp/tools/README.md][related-7]**
- **[docs/mcp_server/architectural_diagrams/03_tool_layer.md line 81][related-8]**
- **[docs/mcp_server/architectural_diagrams/08_naming_landscape.md line 85][related-9]**
- **[docs/mcp_server/TOOLS.md][related-10]**
- **[docs/architecture/VSCODE_AGENT_ORCHESTRATION.md][related-11]**
- **[docs/mcp_server/PHASE_WORKFLOWS.md][related-12]**
- **[docs/mcp_server/GAP_ANALYSIS_IMPLEMENTATION_PLAN.md][related-13]**

<!-- Link definitions -->

[related-1]: mcp_server/tools/validation_tools.py
[related-2]: mcp_server/server.py lines 129 and 355
[related-3]: tests/mcp_server/unit/tools/test_validation_tools.py
[related-4]: tests/mcp_server/unit/integration/test_all_tools.py lines 54 and 172-173
[related-5]: .github/agents/qa.agent.md line 25
[related-6]: docs/reference/mcp/tools/quality.md
[related-7]: docs/reference/mcp/tools/README.md
[related-8]: docs/mcp_server/architectural_diagrams/03_tool_layer.md line 81
[related-9]: docs/mcp_server/architectural_diagrams/08_naming_landscape.md line 85
[related-10]: docs/mcp_server/TOOLS.md
[related-11]: docs/architecture/VSCODE_AGENT_ORCHESTRATION.md
[related-12]: docs/mcp_server/PHASE_WORKFLOWS.md
[related-13]: docs/mcp_server/GAP_ANALYSIS_IMPLEMENTATION_PLAN.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |