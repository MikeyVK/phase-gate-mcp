<!-- docs\development\issue406\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-18T11:15s updated= -->
# Research: Russian Doll Decorator Pipeline for Exception Mapping

**Status:** APPROVED  
**Version:** 1.0.0  
**Last Updated:** 2026-06-18

## Prerequisites

Read these first:
1. [docs/development/issue404/design.md](../issue404/design.md)
2. [docs/development/issue404/validation.md](../issue404/validation.md)
3. [docs/development/issue404/decorator_pipeline_design.md](../issue404/decorator_pipeline_design.md)
---

## Problem Statement

Exception interception is currently implemented as a temporary bridge directly in server.py (handle_call_tool). This violates the Single Responsibility Principle (SRP) by coupling transport/control logic with validation, enforcement, caching, and exception mapping. To scale the architecture and clean up server.py, we need a modular middleware/decorator pipeline to wrap tool execution.

## Research Goals

- Map the 6 system error categories to specific decorators in a Russian Doll chain.
- Ensure robust double fault prevention by separating CacheErrorHandler and ToolErrorHandler.
- Decouple server.py from direct try-except, validation, and enforcement blocks.
- Maintain 100% backward compatibility of JSON-RPC response boundaries and error DTO formats.

---

## 1. Scope

### 1.1. In Scope
- Refactoring the temporary integration bridge in `server.py` (`handle_call_tool`) into modular `ITool` decorators.
- Defining decorators for cache error handling, resource publishing, tool error handling, argument validation, and lifecycle/phase enforcement.
- Updating `ToolFactory` in `bootstrap.py` to assemble the decorator chain.
- Refactoring `tests/mcp_server/unit/test_server.py` to target the decorated tools instead of raw server methods.

### 1.2. Out of Scope
- Changing the public JSON-RPC API contracts or response structures.
- Changing the Pydantic schemas of the error DTOs established in Issue #404.
- Adding new tool actions or modifying core execution logic within managers/adapters.

---

## 2. Background & Prior Art

In Issue #404, we resolved the formatting gaps and established the taxonomical error DTO models (`ValidationErrorOutput`, `EnforcementErrorOutput`, `ExecutionErrorOutput`, `CacheErrorOutput`). 
To keep the test suite protected and stable, we built a temporary integration bridge directly in `server.py` inside `handle_call_tool`.
This temporary bridge intercepts:
1. `ValidationError` (from argument checking) -> `ValidationErrorOutput`
2. `MCPError` (from pre-enforcement guards) -> `EnforcementErrorOutput`
3. Generic `Exception` (from tool execution) -> `ExecutionErrorOutput`
4. Caching failures (double fault validation) -> `CacheErrorOutput`
5. `MCPError` (from post-enforcement guards) -> `EnforcementErrorOutput`

While this bridge successfully achieved 100% of functional goals, it resulted in high coupling inside `server.py` and mixed protocol transportation logic with domain execution concerns. The blueprint in `decorator_pipeline_design.md` outlines the decorator pipeline pattern as the target solution.

---

## 3. Findings & Analysis

### 3.1. Responsibility & Coupling Analysis
Currently, `MCPServer.handle_call_tool` is responsible for:
- Orchestrating JSON-RPC request decoding.
- Creating a unique `call_id` and tracking duration.
- Validating tool schemas and wrapping arguments.
- Running pre-execution lifecycle enforcement rules.
- Invoking the core tool execute command.
- Writing success/error DTOs to the response cache.
- Running post-execution lifecycle enforcement rules.
- Resolving templates and rendering note groups using `TextPresenter`.
- Handling double fault protection on cache/publishing exceptions.
- Translating the final payload into MCP-compliant protocol structures.

This constitutes a clear violation of the Single Responsibility Principle (SRP). A change in lifecycle rules, error formatting, caching, or transport protocol all target `server.py`, increasing maintenance risk.

### 3.2. Error Taxonomy Coverage Validation
We checked the coverage of the 6 system error categories identified in `issue404/design.md` against our decorator pipeline design:

| Category | Description | Coverage in Decorator Pipeline |
| :--- | :--- | :--- |
| **1. Server Startup** | Configuration or bootstrap failures | Handled by `ServerBootstrapper` (outside decorators). |
| **2. Tool Input Schema Validation** | Pydantic validation failures of LLM arguments | `InputValidationDecorator` catches `ValidationError` and returns `ValidationErrorOutput`. |
| **3. Tool Platform Errors** | Unexpected infrastructural errors bubbling from tools | `ToolErrorHandlerDecorator` catches generic exceptions and returns `ExecutionErrorOutput`. |
| **4. Tool Domain Errors** | Expected business logic failures | Core tool execution returns `success=False` domain DTOs (normal flow, passes through). |
| **5. MCP Server / Cache Errors** | Failures within the caching pipeline itself | `CacheErrorHandlerDecorator` catches cache write issues and returns `CacheErrorOutput`. |
| **6. Enforcement Errors** | Phase-guard or lifecycle rule blocks | `EnforcementDecorator` catches `MCPError` and returns `EnforcementErrorOutput`. |

This confirms that the decorator pipeline provides 100% functional coverage for all error types.

### 3.3. Double Fault Prevention Flow
Robust double fault protection requires that a crash in the publisher/cache layer (such as a full disk or permissions failure) does not crash the client connection:
- In the sequence `Server -> CacheErrorHandler -> ResourcePublisher -> ToolErrorHandler`, the `CacheErrorHandler` sits outside the `ResourcePublisher`.
- If `ToolErrorHandler` or core execution raises an error, it is returned to `ResourcePublisher` as a DTO.
- `ResourcePublisher` attempts to write it to cache. If this write fails (raising a caching exception), `CacheErrorHandler` intercepts it and formats a safe `CacheErrorOutput` plaintext fallback.
- This ensures the JSON-RPC channel remains stable.

### 3.4. Blast Radius & Test Suite Coupling
- **`mcp_server/tools/decorators.py`**: Will host all new decorator classes. Currently only hosts `ResourcePublishingDecorator` (which will be renamed/extended).
- **`mcp_server/bootstrap.py`**: `ToolFactory.build_tool` will assemble the decorators. `ServerBootstrapper` must pass the required dependencies (`response_cache`, `enforcement_runner`).
- **`mcp_server/server.py`**: The bridge in `handle_call_tool` will be replaced with a single `tool.execute()` call and NoteContext rendering.
- **`tests/mcp_server/unit/test_server.py`**: Currently asserts exceptions directly on `server.py` mock targets. These tests will be refactored to verify decorator behavior.

---

## 4. Open Questions

1. **Decorator Construction Dependency Injection**: Should `ToolFactory` be injected with the full configuration settings, or should it receive individual manager/caching interfaces? (Recommendation: pass narrow interfaces like `IToolResponseCache` and `EnforcementRunner` to maintain loose coupling).
2. **NoteContext Routing**: Should note-context formatting remain in `server.py` after execution, or should a decorator handle notes presentation? (Recommendation: leave notes presentation to the outer execution boundary to keep decorators focused on execution flow).

---

## 5. Approved Strategy

Preserve compatibility across all external JSON-RPC boundaries and error DTO shapes. The temporary integration bridge in server.py will be completely replaced by the modular decorator pipeline, keeping the public contracts identical. No special migration policy is required for clients.

---

## 6. Expected Results

Complete decoupling of server.py from validation, enforcement, and exception handling blocks. Clean, modular decorators in decorators.py that implement the ITool interface. 100% test success across all 2873 unit and integration tests.

---

## 7. Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-18 | Agent | Initial validation and decorator analysis report |
