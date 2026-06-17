<!-- docs/development/issue404/research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-15T19:45:50Z updated=2026-06-17T14:15:00Z -->
# Research: Resolving TextPresenter Formatting Gaps & Error Propagation

**Status:** APPROVED  
**Version:** 1.1.0  
**Last Updated:** 2026-06-17  

---

## 1. Context & Purpose

This document details the historical evolution of error propagation in the MCP server, performs a gap analysis on the text presentation layer (TextPresenter), and designs a clean, Config-First strategy to route all user-facing texts—including validation, enforcement, and runtime errors—through the presentation layer.

---

## 2. Scope

### 2.1. In Scope (Phase 1: Presentation & DTO Contracts)
* **Define DTO Contracts:** Create a new schema file `mcp_server/schemas/error_outputs.py` to house the `ToolErrorOutput` hierarchy (`ValidationErrorOutput`, `EnforcementErrorOutput`, `ExecutionErrorOutput`, `CacheErrorOutput`).
* **Configure Failure Templates:** Add global error formatting templates in `presentation.yaml` under `global.failures` and support tool-specific failure templates under `tools.<tool_name>.templates_failure`.
* **Config-First Translation:** Map raw error metadata (Pydantic error types, enforcement error codes, tool-specific error codes) to YAML templates, eliminating hardcoded user-facing strings in Python.
* **Temporary Server Bridge:** Modify `server.py` (`handle_call_tool`) to intercept validation, enforcement, and execution exceptions, convert them to error DTOs, cache them manually, and present them via `TextPresenter`.
* **Drift Validation:** Extend `validate_presentation_alignment` to verify failure templates.
* **Unit and Integration Testing:** Test error presenter rendering (unit) and end-to-end MCP-level error formats (integration).

### 2.2. Out of Scope (Phase 2: Pipeline Refactoring / Decorators)
* **Decorator Implementation:** Developing the `InputValidationDecorator`, `EnforcementDecorator`, `ToolErrorHandlerDecorator`, and `CacheErrorHandlerDecorator` classes in `decorators.py`.
* **Tool Factory Composition:** Modifying `ToolFactory` in `bootstrap.py` to wire the decorator execution chain.
* **Server Cleanup:** Removing validation/enforcement methods and direct exception-handling blocks from `server.py`.

---

## 3. Background & Findings

### 3.1. Historical Milestones of Error Propagation
1. **Issue #77:** Introduced a global `@tool_error_handler` to catch exceptions and return `ToolResult.error()` to keep tools enabled in VS Code.
2. **Issue #120:** Appended inline schema details to `ValidationError` responses.
3. **Issue #283:** Decoupled presentation formatting by introducing `NoteContext` to make the decorator context-agnostic.
4. **Issue #300:** Restored `stderr`/`stdout` details for pytest execution failures instead of masking them.
5. **Issue #327:** Added early-return validation failures from the server.

### 3.2. Critical Gaps in Current Error Handling
* **BaseTool Removal Impact:** Following the Issue #402 refactor and removal of `BaseTool`, the `@tool_error_handler` is no longer applied in production. Uncaught exceptions can bubble up directly and cause VS Code to disable the tools.
* **Double Fault Vulnerability:** Cache/publishing failures (e.g. disk full) when attempting to cache an execution error or normal result must not crash the server. This requires an outer `CacheErrorHandler` separate from the inner `ToolErrorHandler`.
* **Violations of Config-First:** Validators, enforcers, and tools generate hardcoded user-facing strings (e.g., `"Phase mismatch detected"`, `"Pattern not found"`) directly in Python, violating the principle that the presentation layer is the sole author of user-facing text.

### 3.3. The 6 Error Categories
1. **Server Startup Errors:** Handled during bootstrap, logged, never reaches the LLM.
2. **Tool Input Schema Validation:** Pydantic validation failures. Currently pollutes context with raw schema JSON.
3. **Tool-related Platform Errors:** Unexpected infrastructural errors (e.g., I/O error, network timeout) bubbling out of tools.
4. **Tool-specific Domain Errors:** Expected business logic failures (e.g., tests failing, no search hits). Already handled via `success=False` in domain DTOs.
5. **MCP Server / Cache Errors:** Failures within the MCP pipeline itself (e.g., cache disk full). Must not crash the server.
6. **Enforcement Errors:** Phase-guard blocks. Currently evaluated inside the server orchestrator.

---

## 4. Gaps in Presenter & Hardcoded Texts

A systematic scan identified the following visual and architectural gaps:
1. **Hardcoded URI Reference:** `server.py` manually appends the resource cache notice, bypassing `presentation.yaml`.
2. **Bypassing Presenter via Notes:** Note classes implement a hardcoded `to_message()` method in Python.
3. **Hardcoded Emojis in Notes:** Note classes hardcode emojis like `🩹` and `❌`, leading to double emojis when formatted.
4. **Duplicate Instructions:** Transition tools emit both an `InfoNote` and `next_instructions: ["context_reset"]`, double-printing advice.
5. **None Value Formatting:** If a DTO field is `None`, the presenter formats it as the literal string `"None"`.
6. **ToolResult Success Fallback:** If a tool returns an error `ToolResult`, the presenter falls back to `success=True` because it lacks a `success` attribute.

---

## 5. Approved Strategy

### Boundary 1: Note Visuals and Emojis
* **Selected Strategy:** Clean Break. All note formatting templates, emojis, and group headers are moved to `presentation.yaml` under `global.notes` and `tools`. Note classes in Python are simplified to a single dataclass `Note(key, params)` containing only raw metadata.

### Boundary 2: TextPresenter Exception & None Handling
* **Selected Strategy:** Clean Break. The presenter checks for `ToolResult` error state, formats `None` values as `"-"` globally via `global.formatting.none_value`, and checks `global.failures` for error formatting.

### Boundary 3: Config-First Error Translation
* **ValidationError:** Pydantic errors (e.g., `missing`, `type_error`) are mapped to sub-templates in `presentation.yaml` under `global.failures.validation.types` to format each field failure dynamically.
* **EnforcementError:** Enforcement blocks return an `error_code` and a `metadata` dict, which are formatted using `global.failures.enforcement.[error_code]`.
* **Tool-Specific Domain Errors:** Tools return `success=False`, an `error_code`, and context fields on their DTO. The presenter resolves these using a failure dictionary in `presentation.yaml` under `tools.<tool_name>.templates_failure.[error_code]`.
* **Platform/Cache Errors:** OS/interpreter exceptions are caught and formatted using global templates under `global.failures.execution_error` and `global.failures.cache_error`.

---

## 6. Open Questions

1. **Drift Validation Scope:** Should the startup drift validator also verify the structure of global failures and enforcement templates against the DTO definitions and error codes? (Decision: Yes. The validator will check global failure schemas to prevent template key drift).

---

## Related Documentation
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)**
- **[docs/development/issue404/decorator_pipeline_design.md](decorator_pipeline_design.md)**
- **[docs/development/issue404/user_facing_text_inventory.md](user_facing_text_inventory.md)**

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-15 | Agent | Initial research draft approved |
| 1.1.0 | 2026-06-17 | Agent | Updated with error propagation gaps, Config-First error translation design, and implementation phasing. |
