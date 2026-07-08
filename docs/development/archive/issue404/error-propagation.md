<!-- c:\temp\pgmcp\docs\development\issue404\error-propagation.md -->
<!-- template=research version=8b7bb3ab created=2026-06-15T20:04Z updated= -->
# Error Propagation and Presentation Architecture

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-15

---

## Purpose

To document how error propagation has evolved and to design a clean integration path between error handling and configurable text presentation.

## Scope

**In Scope:**
mcp_server/server.py, mcp_server/core/error_handling.py, mcp_server/presentation/presenter.py, presentation.yaml, and all related tool exception paths.

**Out of Scope:**
Changes to the Pydantic models themselves or external client implementations.

## Prerequisites

Read these first:
1. Understanding of the NoteContext protocol (Issue #283)
2. Understanding of the ITool and DTO migration (Issue #402)
3. Understanding of the TextPresenter template configuration (Issue #404)
---

## Problem Statement

Uncaught exceptions and validation errors are mapped to ToolResult objects but bypass the configurable presentation layer, causing formatting failures or generic error representations.

## Research Goals

- Trace the historical development of error propagation in the MCP server.
- Analyze the current gap between error handling and the TextPresenter presentation layer.
- Propose a structured mechanism for configurable error presentation in presentation.yaml.

---

## Background

The project historically introduced a global @tool_error_handler in Issue #77 to prevent VS Code from disabling tools on exceptions. Over time, validation schemas (Issue #120), NoteContext (Issue #283), and pytest stderr details (Issue #300) were integrated. However, the presentation layer (Issue #404) still assumes that all return values are successful tool DTOs, causing key errors and bypasses during exception rendering.

---

## Findings

Historically, error propagation evolved across five key milestones:
1. Issue #77: Added @tool_error_handler to catch exceptions and return ToolResult.error() so VS Code keeps tools enabled.
2. Issue #120: Added inline schema details to ValidationError responses.
3. Issue #283: Decoupled presentation formatting by introducing NoteContext and making the decorator context-agnostic.
4. Issue #300: Restored stderr/stdout details for pytest failures instead of losing them in ExecutionError.
5. Issue #327: Added early-return validation failures from the server.

The Current Presentation Gap:
In server.py, the server calls getattr(data_dto, "success", True) to determine if the run was successful. When a tool raises an exception, the @tool_error_handler catches it and returns a ToolResult representing an error. Because ToolResult does not have a success attribute, getattr returns True. The presenter then attempts to format the ToolResult using the tool's template_success. This causes a KeyError or AttributeError (e.g., ToolResult lacks tool-specific fields like name or path), which is caught in a broad try-except block in server.py and returned as a generic server processing error.

Proposed Resolution Strategy:
1. In server.py, explicitly check if data_dto is an instance of ToolResult and data_dto.is_error is True. If so, set success = False.
2. Build a standard error formatting context in the presenter containing error_message, error_code, and file_path.
3. Fallback to global.default_failure_template if the tool does not define template_failure in presentation.yaml.

## Open Questions

- ❓ Should the presenter support custom validation error templates distinct from execution failures?
- ❓ How should multi-content ToolResults (e.g. text + schema JSON) be formatted when passing through the presenter?


## Related Documentation
- **[docs/development/issue404/research.md][related-1]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/development/issue404/research.md
[related-2]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-15 | Agent | Initial draft |