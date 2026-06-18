<!-- docs\development\issue404\decorator_pipeline_design.md -->
<!-- template=design version=5827e841 created=2026-06-16T15:17Z updated=2026-06-17T18:30Z -->
# Decorator Pipeline Design (Phase 2 Blueprint)

**Status:** DRAFT  
**Version:** 1.4  
**Last Updated:** 2026-06-17

---

## Purpose

To document the long-term target architecture for Phase 2 (Decorator Pipeline refactoring), focusing on the reusable decorator chain and double fault prevention.

## Prerequisites

1. Understanding of the ITool and DTO migration (Issue #402)
2. Phase 1 Design: [design.md](design.md)
3. [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)

---

## 1. Pipeline Architecture & Ordering

In Phase 2, the hardcoded try/except logic, input validation, and enforcement checks will be completely removed from `server.py` and refactored into modular `ITool` decorators.

The decorators are assembled by `ToolFactory` in `bootstrap.py` like a Russian doll, from the outside in:

```text
Server -> CacheErrorHandler -> ResourcePublisher -> ToolErrorHandler -> Validator -> Enforcer -> ITool
```

### 1.1. Decorator Roles

- **`CacheErrorHandlerDecorator` (Outermost):** Catches publishing/cache errors (e.g., disk full, write permissions issue) raised by the `ResourcePublisherDecorator`. Returns `CacheErrorOutput` DTO directly.
- **`ResourcePublisherDecorator` (Middle):** Caches returning DTOs and wraps them in a `ToolExecutionEnvelope` with a generated `run_id`.
- **`ToolErrorHandlerDecorator` (Inner):** Catches unexpected tool execution exceptions (e.g., third-party crashes) and maps them to `ExecutionErrorOutput` DTO.
- **`InputValidationDecorator`:** Validates incoming arguments against the tool's Pydantic `args_model`. If validation fails, returns `ValidationErrorOutput`.
- **`EnforcementDecorator`:** Runs pre/post phase guards and business rule checks. If blocked, returns `EnforcementErrorOutput`.
- **`ITool` (Core):** Executes core domain logic.

---

## 2. Double Fault Prevention

By separating the outermost `CacheErrorHandler` and the inner `ToolErrorHandler` with the `ResourcePublisher` in between, we achieve robust double-fault prevention:

1. If the tool execution crashes, the exception bubbles to `ToolErrorHandlerDecorator` which wraps it in an `ExecutionErrorOutput` DTO.
2. The `ResourcePublisherDecorator` receives this DTO, caches it, and returns the envelope.
3. If caching itself throws a filesystem exception, the outer `CacheErrorHandlerDecorator` intercepts it and returns a `CacheErrorOutput` directly to the server, preventing a server crash.

### 2.1. Conceptual Decorator Schema

```python
class CacheErrorHandlerDecorator(ITool):
    def __init__(self, tool: ITool):
        self._tool = tool

    async def execute(self, params: Any, context: NoteContext) -> Any:
        try:
            return await self._tool.execute(params, context)
        except Exception as e:
            # Catch failures in ResourcePublisher (e.g. disk full, read-only cache)
            log_error(f"Cache/Publisher failed: {str(e)}")
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
            log_error(f"Tool execution failed: {str(e)}")
            return ExecutionErrorOutput(
                message=str(e), 
                traceback=get_traceback(e)
            )
```

---

## 3. Logging, Stdio, and Stderr Hygiene

To preserve JSON-RPC communication integrity over `sys.stdout` and ensure clear diagnostics, the decorator pipeline enforces strict hygiene:

### 3.1. Standard Output (`sys.stdout`) Protection
- **No Direct Writes:** No decorator or tool may write directly to `sys.stdout` (e.g. via `print()`), as this corrupts JSON-RPC framing and drops the client connection.
- **Subprocess Capture:** All subprocess invocations (e.g., calling `git` or `pytest` processes) must capture stdout/stderr programmatically (`capture_output=True` or `stdout=subprocess.PIPE`) instead of inheriting parent streams. The captured text is packaged into the DTO and returned.

### 3.2. Standard Error (`sys.stderr`) and Auditing
- **Logger Access:** All decorators and managers access the structured logging system via `mcp_server.core.logging.get_logger(__name__)`.
- **Diagnostics:** System warnings and diagnostic logs are written exclusively to `sys.stderr` or the audit log file (`mcp_server/logs/mcp_audit.log`).
- **Traceback Interception:** Unhandled exceptions are logged as `ERROR` with their full tracebacks via the logger to `sys.stderr` before being packaged into the DTO's `traceback` field.

---

## 4. Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.4 | 2026-06-17 | Agent | Restored as Phase 2 blueprint draft, covering decorator structure and stdio hygiene |
