<!-- docs\development\issue404\design.md -->
<!-- template=design version=5827e841 created=2026-06-17T15:59Z updated=2026-06-17T18:35Z -->
# Design: Resolving TextPresenter Formatting Gaps & Error Propagation

**Status:** DRAFT  
**Version:** 1.3.0  
**Last Updated:** 2026-06-17

---

## Purpose

To define the technical architecture for resolving TextPresenter formatting gaps and error propagation.

## Prerequisites

Read these first:
1. Understanding of the ITool and DTO migration (Issue #402)
2. Understanding of the TextPresenter template configuration (Issue #404)
3. [Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md)
4. [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)

---

## 1. Context & Requirements

### 1.1. Problem Statement

Uncaught exceptions, validation errors, and enforcement checks are currently evaluated using hardcoded blocks inside the `MCPServer`. This violates SRP, pollutes the LLM context with raw JSON schemas during validation errors, and lacks a unified error schema. Additionally, None values are rendered literally as `'None'` in text templates, and transition advisory notes are duplicated.

### 1.2. Requirements

**Functional:**
- Define explicit DTOs for all error types (`ValidationErrorOutput`, `EnforcementErrorOutput`, `ExecutionErrorOutput`, `CacheErrorOutput`) in a dedicated schemas file [error_outputs.py](file:///c:/temp/pgmcp/mcp_server/schemas/error_outputs.py).
- Ensure validation errors expose the full JSON schema via the resource cache.
- Catch validation, enforcement, and execution exceptions inside [server.py](file:///c:/temp/pgmcp/mcp_server/server.py) and map them to error DTOs formatted via `TextPresenter` using global failure templates in `presentation.yaml`.
- Format `None` values as `"-"` in the `TextPresenter`, configured via `global.formatting.none_value`.
- Remove redundant python transition advisory notes from tools and rely solely on `presentation.yaml` `next_instructions`.
- Complete migration of all operation notes to the presenter-driven model. Note classes in [operation_notes.py](file:///c:/temp/pgmcp/mcp_server/core/operation_notes.py) must be simplified to pure metadata dataclasses, with templates moved to `presentation.yaml` under a `notes` configuration section.
- Completely remove all legacy `to_message()` Python methods before closing Issue #404 (Clean Break).

**Non-Functional:**
- SOLID / Single Responsibility Principle compliance.
- Zero context pollution (large tracebacks/schemas in cache).
- Double Fault Prevention (Cache/Publisher failures caught by outer handler and returned as plain text).

### 1.3. Constraints

- The MCP server uses `sys.stdout` for JSON-RPC transport; no direct print to stdout is allowed.
- All DTOs must be frozen (`frozen=True`, `extra='forbid'`).
- The Approved Strategy must be explicitly defined per boundary (Topic 1: Notes Redesign, Topic 2: Error Presentation).

---

## 2. Design Options

| Option | Pros | Cons |
|:---|:---|:---|
| **Option A: Protocol Boundary Handling** | - Simple and straightforward implementation path.<br>- No deep abstraction layers to trace. | - Violates Single Responsibility Principle (SRP) by combining protocol handling, validation, enforcement, and error presentation.<br>- Validation errors bypass cache and are sent as raw JSON schemas to LLM.<br>- Poor cache/publisher fault tolerance (cache failures crash the connection). |
| **Option B: Abstract Base Class (AbstractTool)** | - Centralized error handling and validation logic in a single base class. | - Violates composition over inheritance established in Issue #402.<br>- God class anti-pattern where the base class accumulates unrelated pipeline duties. |
| **Option C: Full Decorator Pipeline (Phased)** | - Isolates each cross-cutting concern to a single decorator class.<br>- Allows automatic caching of validation/enforcement DTOs.<br>- Double Fault Prevention (outer `CacheErrorHandler` catches publisher disk failures and returns text directly).<br>- Phased rollout protects the test suite by keeping the public JSON-RPC boundaries identical between phases. | - Requires maintaining a temporary integration bridge in `server.py` during Phase 1 (Issue #404). |

---

## 3. Chosen Design

**Decision:** Implement the Phased Migration Strategy: Phase 1 (Issue #404) focuses on defining DTOs in `error_outputs.py`, configuring `presentation.yaml`, and building a temporary integration bridge in `server.py`. Phase 2 (Deferred) will refactor the backend into a Russian Doll decorator pipeline wrapped by the Tool Factory.

**Rationale:** Allows us to isolate visual presentation formatting fixes and error propagation contract establishment in Issue #404 without a massive backend rewrite, keeping the test suite protected. Placing error DTOs in their own file avoids contaminating `tool_outputs.py` and keeps error types isolated.

### 3.1. Error DTOs mapping per Category

The 6 system error categories are mapped to their producers and output formats:

| Error Category | Description | Producer (Phase 1) | Producer (Phase 2) | Error DTO / Format |
|:---|:---|:---|:---|:---|
| **1. Server Startup** | Configuration or bootstrap failures | `bootstrap.py` | `bootstrap.py` | None (Logged only) |
| **2. Tool Input Schema Validation** | Pydantic validation failures of LLM arguments | `_validate_tool_arguments` in `server.py` | `InputValidationDecorator` | `ValidationErrorOutput` |
| **3. Tool Platform Errors** | Unexpected infrastructural errors bubbling from tools | `tool.execute()` in `server.py` | `ToolErrorHandlerDecorator` | `ExecutionErrorOutput` |
| **4. Tool Domain Errors** | Expected business logic failures | `ITool` (Domain logic) | `ITool` (Domain logic) | Domain DTO (success=False) |
| **5. MCP Server / Cache Errors** | Failures within the caching pipeline itself | `server.py` bridge | `CacheErrorHandlerDecorator` | `CacheErrorOutput` |
| **6. Enforcement Errors** | Phase-guard or lifecycle rule blocks | `_run_tool_enforcement` in `server.py` | `EnforcementDecorator` | `EnforcementErrorOutput` |

### 3.2. Phase 1 Integration Bridge (Flow Diagram)

The temporary bridge inside `server.py` intercepts errors, writes them to the cache, and formats them:

```mermaid
graph TD
    A[Start: handle_call_tool] --> B{Args Validation}
    B -->|Failed: ValidationError| C[ValidationErrorOutput DTO]
    B -->|Success| D{Pre-Enforcement}
    D -->|Failed: MCPError| E[EnforcementErrorOutput DTO]
    D -->|Success| F[Execute tool.execute]
    F -->|Raw Exception| G[ExecutionErrorOutput DTO]
    F -->|Success: DTO / Envelope| H[Extract DTO & run_id]
    C & E & G --> I{Write to Cache}
    I -->|Success| J[Wrap in ToolExecutionEnvelope & present]
    I -->|Failed: CacheError| K[CacheErrorOutput DTO]
    H --> J
    J --> L[Run Post-Enforcement]
    L --> M[Render Notes via note_context]
    M --> N[Return CallToolResult]
    K --> O[Present directly as plain text]
    O --> N
```

### 3.3. Phase 2 Decorator Pipeline (Flow Diagram)

The long-term decorator architecture for backend execution:

```mermaid
graph TD
    Server[MCPServer] --> CacheHandler[CacheErrorHandlerDecorator]
    CacheHandler --> Publisher[ResourcePublisherDecorator]
    Publisher --> ToolHandler[ToolErrorHandlerDecorator]
    ToolHandler --> Validator[InputValidationDecorator]
    Validator --> Enforcer[EnforcementDecorator]
    Enforcer --> CoreTool[ITool core]
```

### 3.4. Detailed Implementation Contracts

#### 3.4.1. The Error Contract DTOs
We establish a strict taxonomy of errors modeled as DTOs in `mcp_server/schemas/error_outputs.py`:

```python
from typing import Any
from pydantic import BaseModel, ConfigDict, Field

class ToolErrorOutput(BaseModel):
    """Base DTO for all decorator pipeline errors."""
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    success: bool = False
    error_type: str
    message: str
    traceback: str | None = None

class ExecutionErrorOutput(ToolErrorOutput):
    """Fails during actual tool execution."""
    error_type: str = "ExecutionError"

class CacheErrorOutput(ToolErrorOutput):
    """Fails during resource caching."""
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

#### 3.4.2. Notes Redesign (Topic 1)
Operation notes in `operation_notes.py` are simplified to pure metadata dataclasses:

```python
@dataclass(frozen=True)
class OperationNote:
    pass

@dataclass(frozen=True)
class ExclusionNote(OperationNote):
    file: str

@dataclass(frozen=True)
class BlockerNote(OperationNote):
    message: str

@dataclass(frozen=True)
class RecoveryNote(OperationNote):
    message: str

@dataclass(frozen=True)
class InfoNote(OperationNote):
    message: str
```

All `to_message()` methods are deprecated and will be removed at the end of the issue. The notes templates are configured in `presentation.yaml`:

```yaml
global:
  formatting:
    none_value: "-"
  notes:
    exclusion: "Excluded from commit index: {file}"
    blocker: "Blocker: {message}"
    recovery: "Recovery: {message}"
    info: "{message}"
```

#### 3.4.3. None-Value filter in TextPresenter
`TextPresenter` will substitute `None` values with `global.formatting.none_value` (default: `"-"`) for all placeholders in templates.

---

## 4. Test & Verification Plan

### 4.1. Affected Test Suites

| Test File | Verification Goal |
|:---|:---|
| `tests/mcp_server/unit/test_presenter.py` | Verify that `None` values are formatted as `"-"`. Verify Note template rendering. |
| `tests/mcp_server/unit/test_server.py` | Verify that validation, enforcement, and execution exception handling map to the correct error DTOs and present them using global failure templates. |
| `tests/mcp_server/integration/` | Verify E2E protocol-level JSON-RPC error responses wrap presenter outputs. |

### 4.2. Verification Commands

```powershell
# Run presenter unit tests
run_tests(path="tests/mcp_server/unit/test_presenter.py")

# Run server unit tests
run_tests(path="tests/mcp_server/unit/test_server.py")

# Run full test suite
run_tests(scope="full")

# Run quality gates
run_quality_gates(scope="branch")
```

---

## 5. Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.3.0 | 2026-06-17 | Agent | Cleaned design focusing strictly on Phase 1, added error mapping and Mermaid flowcharts |
