<!-- docs\development\issue404\decorator_pipeline_design.md -->
<!-- template=design version=5827e841 created=2026-06-16T15:17Z updated=2026-06-17T13:15Z -->
# Error Handling & Decorator Pipeline (Issue #404)

**Status:** APPROVED  
**Version:** 1.2  
**Last Updated:** 2026-06-17  

---

## 1. Context & Requirements

### 1.1. Problem Statement

MCP tool errors, validation failures, and enforcement checks are currently evaluated using hardcoded blocks inside the `MCPServer`. This violates SRP, pollutes the LLM context with raw JSON schemas during validation errors, and lacks a unified error schema.

#### 1.1.1. The Error Taxonomy
To design a comprehensive solution, we identified 6 distinct categories of errors in the system:
1. **Server Startup Errors:** (e.g., config validation). Handled during bootstrap, logged, never reaches LLM.
2. **Tool Input Schema Validation:** Pydantic failures before execution. Currently pollutes context with raw schema JSON.
3. **Tool-related Platform Errors:** Unexpected infrastructural errors (e.g., Network timeout, Disk I/O) bubbling out of tools.
4. **Tool-specific Domain Errors:** Business logic failures (e.g., tests failing, no search hits). Already handled via `success=False` in domain DTOs.
5. **MCP Server / Cache Errors:** Failures within the MCP pipeline itself (e.g., Resource Cache disk full, write permissions). Must not crash the server.
6. **Enforcement Errors:** Phase-guard blocks. Currently evaluated inside the server orchestrator.

### 1.2. Requirements

**Functional:**
- [x] Define explicit DTOs for all error types (`ExecutionErrorOutput`, `CacheErrorOutput`, `ValidationErrorOutput`, `EnforcementErrorOutput`).
- [x] Ensure validation errors expose the full JSON schema via the resource cache.
- [x] Remove `_validate_tool_arguments` and `_run_tool_enforcement` from `server.py`.
- [x] Assemble the pipeline via `ToolFactory` in `bootstrap.py`.
- [x] Ensure that the `MCPServer` remains a pure protocol orchestrator and does not generate run IDs or write to the cache.

**Non-Functional:**
- [x] Strict adherence to SOLID and SRP (Architecture Principles).
- [x] Fail-safe execution (cache failures must not crash the orchestrator).
- [x] Zero context pollution (large tracebacks and schemas go to cache, not the LLM chat window).

### 1.3. Constraints

None

---

## 2. Design Options

### 2.1. Option A: Protocol Boundary Handling

Catch all errors directly in the `MCPServer.handle_call_tool()` method. The server remains responsible for validating inputs, enforcing rules, catching exceptions, and returning `isError=True` strings.

**Pros:**
- Simple, straightforward execution path.
- No deep abstraction layers to trace.

**Cons:**
- **Violates SRP:** The server is responsible for protocol translation AND validation AND enforcement AND error handling.
- **Context Pollution:** Validation errors return the schema as an embedded resource directly to the LLM, bypassing the resource cache.
- **Fragile:** If the cache crashes, the server handles it poorly.

### 2.2. Option B: Abstract Base Class (`AbstractTool`)

Reintroduce a base class that all tools inherit from. The base class's `execute()` method contains the `try/except` and validation logic.

**Pros:**
- Centralized error handling.

**Cons:**
- **Violates Architecture Principles:** We explicitly removed `BaseTool` in Issue #402 to favor Composition over Inheritance. 
- **God Class Anti-pattern:** The base class quickly accumulates unrelated responsibilities (caching, validation, enforcement), tightly coupling all tools.

### 2.3. Option C: Full Decorator Pipeline

Extract all pre/post processing into a Russian Doll decorator pipeline. Tools remain pure. Validation, Enforcement, Caching, and Error Handling are separate decorators wrapping the `ITool`.

**Pros:**
- **Perfect SRP:** Each cross-cutting concern is isolated in its own class.
- **Natural Caching:** Placing the Validator inside the Cache publisher means validation errors are automatically cached without custom logic.
- **Fail-safe:** Placing the ErrorHandler at the outermost edge protects the server even if the Cache publisher itself crashes.

**Cons:**
- **Complex Assembly:** Requires careful wiring in the `ToolFactory` composition root.

---

## 3. Chosen Design

**Decision:** Implement the "Full Decorator Pipeline" architecture where Validation, Enforcement, Caching, and Error Catching are isolated into dedicated decorators. The MCPServer becomes a pure JSON-RPC orchestrator.

**Rationale:** The decorator pipeline achieves perfect Single Responsibility. By placing the Validator inside the Publisher, validation errors are cached automatically. By splitting error handling into two distinct decorators—an inner `ToolErrorHandler` and an outer `CacheErrorHandler`—we ensure that unhandled tool exceptions are cleanly mapped to DTOs and cached by the publisher, while cache failures themselves are caught and handled gracefully at the outermost boundary.

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **ToolErrorOutput Hierarchy** | Defines a strict error contract with distinct DTOs for execution (`ExecutionErrorOutput`), validation (`ValidationErrorOutput`), enforcement (`EnforcementErrorOutput`), and cache failures (`CacheErrorOutput`). |
| **Two-Tier Error Handling** | Splitting error handling into `CacheErrorHandler` (outermost) and `ToolErrorHandler` (inner) solves the ordering problem. Tool errors are mapped to DTOs and cached by the publisher. Cache/publishing errors are caught by the outer handler. |
| **ResourcePublishingDecorator wraps ToolErrorHandlerDecorator** | Ensures that unexpected tool crashes caught by the inner error handler are returned as `ExecutionErrorOutput` DTOs, allowing the publisher to cache them exactly like successful results. |
| **Double Fault Prevention** | If the publisher/cache throws a `CacheError` (e.g. disk full) when attempting to cache an execution error or a normal result, the outer `CacheErrorHandler` catches it and returns a `CacheErrorOutput` directly to the server without attempting to write to the broken cache. |

---

## 4. Detailed Implementation Architecture (V5)

This is the definitive, clean architectural design that reduces the MCPServer to a pure protocol orchestrator. Every distinct responsibility (Validation, Enforcement, Caching, Error Handling) receives its own dedicated layer (Decorator) wrapping the original tool.

### 4.1. The Error Contract
We establish a strict taxonomy of errors modeled as DTOs in `mcp_server/schemas/tool_outputs.py`.

```python
class ToolErrorOutput(BaseToolOutput):
    """Base DTO for all decorator pipeline errors."""
    success: bool = False
    error_type: str
    message: str
    traceback: str | None = None

class ExecutionErrorOutput(ToolErrorOutput):
    """Fails during actual tool execution (e.g., third-party API timeout, subprocess crash)."""
    error_type: str = "ExecutionError"

class CacheErrorOutput(ToolErrorOutput):
    """Fails during resource caching (e.g., cache disk full, write permissions issue)."""
    error_type: str = "CacheError"

class ValidationErrorOutput(ToolErrorOutput):
    """Input validation errors. Contains the complete expected input_schema."""
    error_type: str = "ValidationError"
    validation_errors: list[dict[str, Any]] | str
    input_schema: dict[str, Any]

class EnforcementErrorOutput(ToolErrorOutput):
    """Phase-guards or business rules blocking the tool execution."""
    error_type: str = "EnforcementError"
    error_code: str
```

### 4.2. Error-to-Producer Mapping
To ensure clarity, each error type is produced by exactly one layer in the pipeline.

| Error DTO / State | Producer (Layer) | Condition |
|-------------------|------------------|-----------|
| **Server Logs (No DTO)** | `bootstrap.py` | Server fails to boot or read configuration. |
| **`ValidationErrorOutput`** | `InputValidationDecorator` | Pydantic validation of LLM arguments fails. |
| **`EnforcementErrorOutput`**| `EnforcementDecorator` | Phase guard or lifecycle rule blocks execution. |
| **Domain DTO (success=False)**| `ITool` (Domain Logic) | Expected domain failures (e.g., tests fail, no search hits). |
| **`ExecutionErrorOutput`** | `ToolErrorHandlerDecorator` | Caught unhandled exception bubbling from `ITool`, `EnforcementDecorator`, or `InputValidationDecorator`. |
| **`CacheErrorOutput`** | `CacheErrorHandlerDecorator` | Caught unhandled exception bubbling from `ResourcePublishingDecorator` (e.g., disk full, write permissions). |

### 4.3. Pipeline Assembly (`mcp_server/bootstrap.py`)
The `ToolFactory` builds the execution chain like a Russian doll, from the outside in:
`Server -> CacheErrorHandler -> ResourcePublisher -> ToolErrorHandler -> Validator -> Enforcer -> ITool`

**Execution Flow (Outside-in):**
1. **Server:** Receives the argument `dict` from the LLM and blindly passes it to the outermost decorator.
2. **CacheErrorHandler:** Begins a `try/except Exception` block to catch cache/filesystem write failures bubbling from the `ResourcePublisher`.
3. **ResourcePublisher:** Attempts to cache all returning DTOs (success DTOs, `ValidationErrorOutput`, `EnforcementErrorOutput`, `ExecutionErrorOutput`) and wraps them in a `ToolExecutionEnvelope` containing a generated `run_id`.
4. **ToolErrorHandler:** Begins a `try/except Exception` block to catch unhandled crashes from the tool execution and wraps them in an `ExecutionErrorOutput` DTO.
5. **Validator:** Attempts to parse the `dict` into the Pydantic `args_model`. If it fails, execution halts and it returns a `ValidationErrorOutput` (including the `input_schema`) back to the publisher.
6. **Enforcer:** Checks business rules (e.g., "Wrong Phase"). If blocked, it returns an `EnforcementErrorOutput`.
7. **ITool:** Executes pure domain logic.

### 4.4. Two-Tier Error Handling & Double Fault Prevention
By splitting the error handling logic, we avoid duplicating cache operations in the error handlers and enforce a strict hierarchy:

1. **Tool Crashes:** When the `ITool` throws an exception, it bubbles past the Enforcer and Validator into the `ToolErrorHandlerDecorator`. The handler maps it to an `ExecutionErrorOutput` DTO and returns it.
2. **Normal Caching Flow:** The `ResourcePublisherDecorator` receives this DTO, generates a `run_id`, caches the `ExecutionErrorOutput` DTO, and returns a `ToolExecutionEnvelope` containing the `run_id` and DTO.
3. **Cache Failure (Double Fault / Disk Full):** If the `ResourcePublisherDecorator` fails to write to the cache (either for a successful tool result or an execution error), it raises a cache write exception. This exception is caught by the outermost `CacheErrorHandlerDecorator`. The handler logs the issue and returns a `CacheErrorOutput` DTO directly to the server (unwrapped, without a `run_id`).
4. **Server Presentation:** Because the server receives the `CacheErrorOutput` directly (unwrapped), it formats and returns the traceback/warning to the LLM directly as plain text, preventing a server crash.

#### Conceptual Implementation of the Decoupled Handlers

```python
class CacheErrorHandlerDecorator(ITool):
    def __init__(self, tool: ITool):
        self._tool = tool

    async def execute(self, params: Any, context: NoteContext) -> Any:
        try:
            return await self._tool.execute(params, context)
        except Exception as e:
            # Catch failures in ResourcePublisher (e.g. disk full, read-only cache)
            log_error(f"Cache/Publisher failed: {str(e)}", traceback=get_traceback(e))
            return CacheErrorOutput(
                message=f"Cache failed: {str(e)}", 
                traceback=get_traceback(e)
            )

class ToolErrorHandlerDecorator(ITool):
    def __init__(self, tool: ITool):
        self._tool = tool

    async def execute(self, params: Any, context: NoteContext) -> Any:
        try:
            return await self._tool.execute(params, context)
        except Exception as e:
            # Catch failures in ITool, Enforcement, or Validator
            log_error(f"Tool execution failed: {str(e)}", traceback=get_traceback(e))
            return ExecutionErrorOutput(
                message=str(e), 
                traceback=get_traceback(e)
            )
```

### 4.5. Cleaning the Server (`mcp_server/server.py`)
The methods `_validate_tool_arguments` and `_run_tool_enforcement` will be completely removed from `server.py` and rebuilt as isolated classes (`InputValidationDecorator` and `EnforcementDecorator`) in `mcp_server/tools/decorators.py`.

The `handle_call_tool` method inside the Server will:
1. Invoke `tool.execute()`.
2. Pass the resulting DTO to the `TextPresenter`.
3. Check if the DTO inherits from `ToolErrorOutput` (setting `isError=True` in the MCP protocol response if so).
4. Return the formatted text to the LLM.

---

## 5. Phased Implementation & Migration Strategy

To minimize scope creep and ensure stable delivery, the decorator pipeline refactoring is divided into two distinct phases:

### Phase 1: Presentation & DTO Contracts (Current Issue #404)
The focus of this phase is to align the presentation layer and close visual formatting gaps.
1. **Define DTO Contracts:** Add `ToolErrorOutput`, `ExecutionErrorOutput`, `CacheErrorOutput`, `ValidationErrorOutput`, and `EnforcementErrorOutput` in `mcp_server/schemas/tool_outputs.py`.
2. **Configure Presenter Templates:** Add formatting templates in `presentation.yaml` under `global.failures` for all error types so `TextPresenter` renders them correctly.
3. **Temporary Integration:** Modify the existing hardcoded execution path in `server.py` to instantiate and return these new error DTOs. This validates the presenter formatting flow and mapping without altering the overall server-tool architecture yet.

### Phase 2: Pipeline Refactoring (Subsequent Issue)
The focus of this phase is backend server refactoring.
1. **Build Decorator Classes:** Implement `CacheErrorHandlerDecorator`, `ResourcePublisherDecorator`, `ToolErrorHandlerDecorator`, `InputValidationDecorator`, and `EnforcementDecorator` in `mcp_server/tools/decorators.py`.
2. **Update Tool Composition:** Modify `ToolFactory` in `bootstrap.py` to wire the decorators.
3. **Clean Server:** Delete `_validate_tool_arguments` and `_run_tool_enforcement` from `server.py`.

---

## Related Documentation
- **[docs/development/issue404/error-propagation.md](error-propagation.md)**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)**

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-16 | Agent | Initial draft |
| 1.1 | 2026-06-17 | Agent | Restored Execution/CacheErrorOutput split, added Double Fault Prevention details, and defined the Phased Migration Strategy. |
| 1.2 | 2026-06-17 | Agent | Decoupled outer CacheErrorHandler and inner ToolErrorHandler to resolve decorator ordering and eliminate duplicated cache logic. |
