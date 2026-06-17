<!-- docs\development\issue404\design.md -->
<!-- template=design version=5827e841 created=2026-06-17T15:59Z updated=2026-06-17T16:05Z -->
# Design: Resolving TextPresenter Formatting Gaps & Error Propagation

**Status:** APPROVED  
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

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Fout-DTOs in error_outputs.py** | Keeps error schemas separated from successful tool outputs, avoiding circular dependencies and schema pollution. |
| **None formatting to '-'** | Approved in chat to present a cleaner, professional representation in structured tables. Configured via `global.formatting.none_value: "-"`. |
| **Phased Decorator Rollout** | Phase 1 implements error DTO contracts and a temporary bridge in `server.py`; Phase 2 migrates to decorators. Protects API boundaries. |
| **Dataclass-only Notes** | Decouples notes formatting from Python logic. Note templates are moved to `presentation.yaml` under `global.notes` templates, and Python classes in `operation_notes.py` become pure metadata containers. |

### 3.2. Detailed Implementation Architecture

#### 3.2.1. The Error Contract DTOs
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

#### 3.2.2. Notes Redesign (Topic 1)
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

#### 3.2.3. None-Value filter in TextPresenter
Modify `TextPresenter.present` and next instructions rendering to substitute `None` values with `global.formatting.none_value` (default: `"-"`):

```python
none_val = self.global_config.get("formatting", {}).get("none_value", "-") if isinstance(self.global_config, dict) else getattr(getattr(self.global_config, "formatting", {}), "none_value", "-")

format_dict = {}
for key in placeholders:
    val = data_dict.get(key, "")
    format_dict[key] = none_val if val is None else val
```

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
| 1.3.0 | 2026-06-17 | Agent | Consolidated design incorporating error_outputs.py and '-' None formatting decisions |
