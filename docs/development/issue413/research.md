<!-- docs/development/issue413/research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-26T08:48:Z updated=2026-06-26T11:15Z -->
# Error Taxonomy Refactoring & DTO Segregation Research

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-06-26

---

## 1. Problem Statement

The current error representation on the MCP platform violates the Single Responsibility Principle (SRP). Specifically:
1. `BaseToolOutput` contains both success-related and error-related concerns (`success` and `error_message` fields), enabling invalid error payloads in success states.
2. Error DTOs (inheriting from `ToolErrorOutput`) carry a redundant `success` boolean field (`success = False`), violating separation of concerns.
3. The platform's transport and presentation layers (`server.py` and `TextPresenter`) determine execution status by checking the value of the `success` attribute rather than using type-safe checks.
4. Internal exceptions and decorators hardcode human-readable `error_message` or `message` strings in Python, bypassing the declarative presentation boundary defined in `presentation.yaml`.

---

## 2. Research Goals

- Map the current Exception and DTO Taxonomy to understand exact coupling and dependencies.
- Define the absolute boundaries, constraints, and kaders of the target architecture.
- Identify the blast radius of removing `error_message` from success DTOs and `success` from error DTOs.
- Formulate a strategy for handling legacy test assertions that couple tests to deprecated attributes.
- Evaluate the feasibility of isolating error DTO generation entirely to the decorator pipeline.
- Identify and eliminate redundant/obsolete error DTOs.

---

## 3. Findings

### Item 1: Current Exception & DTO Taxonomies

The codebase maintains two distinct taxonomies for error representation:

#### 1. Runtime Exceptions (`mcp_server/core/exceptions.py`)
These are raised in core modules during runtime and caught by decorators:
- `MCPError`: Base exception (erfts from `Exception`) containing `message`, `code` (defaults to `"ERR_INTERNAL"`), and `params: dict`.
  - `ConfigError`: Configuration parsing/loading errors, carrying `file_path`. Hardcoded code: `"ERR_CONFIG"`.
  - `ValidationError`: Input or validation failures, carrying `schema`, `missing`, and `provided`. Default code: `"ERR_VALIDATION"`.
    - `MetadataParseError`: Specific metadata-validative failures, carrying `file_path`.
  - `PreflightError`: Fails checked before tool execution. Default code: `"ERR_PREFLIGHT"`.
  - `ExecutionError`: Execution failures in tools. Hardcoded code: `"ERR_EXECUTION"`.
  - `MCPSystemError`: System/platform-level failures, carrying `fallback`. Hardcoded code: `"ERR_SYSTEM"`.

#### 2. Tool Output DTOs (`mcp_server/schemas/`)
These are Pydantic models returned by tool execution and decorators:
- **Success DTOs** (`[tool_outputs.py](file:///c:/temp/pgmcp/mcp_server/schemas/tool_outputs.py)`): All inherit from `BaseToolOutput`.
  - `BaseToolOutput`: Contains `success: bool = True`, `error_message: str | None = None`, and `post_tool_instruction: str | None = None`.
- **Error DTOs** (`[error_outputs.py](file:///c:/temp/pgmcp/mcp_server/schemas/error_outputs.py)`): All inherit from `ToolErrorOutput`.
  - `ToolErrorOutput`: Contains `success: bool = False`, `error_type: str`, `error_message: str | None = None`, `traceback: str | None = None`, and `params: dict`.
  - Subclasses: `ValidationErrorOutput`, `ExecutionErrorOutput`, `CacheErrorOutput`, `EnforcementErrorOutput`, `ConfigErrorOutput`.

### Item 2: Boundary Analysis & Mapping Points

Exceptions are mapped to DTOs in the **Decorator Pipeline** at specific boundary points:

| Source Exception / Error | Decorator | Resulting DTO | Presenter Template Mapping |
| :--- | :--- | :--- | :--- |
| `pydantic.ValidationError` | `[InputValidationDecorator](file:///c:/temp/pgmcp/mcp_server/core/decorators/input_validation_decorator.py)` | `ValidationErrorOutput` | Resolved via `failures.validation` or `failures.ERR_VALIDATION` |
| `mcp_server.core.exceptions.ValidationError` | `[EnforcementDecorator](file:///c:/temp/pgmcp/mcp_server/core/decorators/enforcement_decorator.py)` | `EnforcementErrorOutput` | Resolved via `failures` mapping in `presentation.yaml` using `error_code` |
| `ConfigError` | `[ToolErrorHandlerDecorator](file:///c:/temp/pgmcp/mcp_server/core/decorators/tool_error_handler_decorator.py)` | `ConfigErrorOutput` | Resolved via `failures.config` or `failures.ERR_CONFIG` |
| Uncaught Python `Exception` | `[ToolErrorHandlerDecorator](file:///c:/temp/pgmcp/mcp_server/core/decorators/tool_error_handler_decorator.py)` | `ExecutionErrorOutput` | Falls back to `default_failure_template` |

### Item 3: Redundant DTOs and Resilient Subsystems

- **`CacheErrorOutput` Redundancy:** 
  Analysis of `[response_cache.py](file:///c:/temp/pgmcp/mcp_server/state/response_cache.py)` shows that cache writing is completely resilient. The `put` method catches any internal exceptions and returns a `CachePublication` object containing `success=False` and `error_code="write_failed"`. It never raises an exception and never generates a `CacheErrorOutput` DTO. Thus, `CacheErrorOutput` is completely redundant and can be deleted.
- **Presenter Error Handling:**
  The `TextPresenter` catches formatting errors internally at runtime (`Format error: {exc}`), preventing presenter exceptions from crashing tool execution. Furthermore, template-schema alignment is verified at boot time via `validate_presentation_alignment`. Thus, no dedicated presenter error DTO is required.

---

## 4. Target Architecture Boundaries & Framework (Kaders)

To resolve the identified violations while preserving system stability, we define the following architectural boundaries and kaders:

### Kader 1: Status Checking via Type Evaluation
- **Current Behavior:** `server.py` and `TextPresenter` evaluate whether an execution failed using boolean queries: `success = getattr(result, "success", True)`.
- **Target Kader:** The platform must treat types as the single source of truth for execution status. `server.py` and `TextPresenter` must check if `isinstance(result, BaseErrorOutput)`. 
- **Protocol Vlag:** `is_error` at the MCP protocol level must be set to `True` if and only if the result is an instance of `BaseErrorOutput`. Domain-level outcomes (such as failed test suites or linting warnings) returned in successful tool outputs must not trigger `is_error=True`.

### Kader 2: Elimination of Python-Hardcoded Error Messages
- **Current Behavior:** Internal exception handlers pass hardcoded strings in Python (e.g. `error_message=f"Invalid input for {self.name}"`).
- **Target Kader:** 
  1. `BaseErrorOutput` and all internal DTOs (`ValidationErrorOutput`, `EnforcementErrorOutput`, `ConfigErrorOutput`, `CacheErrorOutput`) must **not** contain any form of `error_message`, `message`, or `msg` fields.
  2. All internal exceptions must only pass structured keys and parameters (such as `error_code`, `file_path`, `params`) to their corresponding DTOs.
  3. The `TextPresenter` is solely responsible for looking up and formatting user-facing messages from `presentation.yaml` using these parameters.
  4. Only external exceptions wrapped in `ExecutionErrorOutput` are allowed to carry a fallback `error_message` containing the raw external traceback/exception message.

### Kader 3: Tool-level Return Segregation (No Error DTOs in Core Tools)
- **Current Behavior:** Tool classes (like `TransitionCycleTool`) catch their own internal exceptions (e.g. `GateViolation`) and return DTOs with `success=False` and `error_message`.
- **Target Kader:** 
  1. Core tool classes must **only** generate and return their specific success DTOs (e.g., `CycleTransitionOutput` representing a successful run). They must **never** return error DTOs.
  2. For any execution, validation, pre-flight, or configuration failure, the core tool must raise a structured exception (e.g., `ValidationError`, `PreflightError`, `ConfigError`).
  3. The decorator pipeline wraps the core tool and is exclusively responsible for catching these exceptions and mapping them to `BaseErrorOutput` subclasses.
  4. The generic `ICoreTool` interface defines `execute` as returning `TOutput`. Under this kader, the core tool's type signature remains `TOutput` (only success DTO). Only the outer decorated `ITool` interface returns `Union[BaseToolOutput, BaseErrorOutput]`.

---

## 5. Approved Strategy

To establish a clean, non-compromised target state and clear the accumulated technical debt, we adopt a **Clean Break** strategy across all boundaries:

### Boundary Strategies

1. **DTO Schemas:**
   - *Clean Break:* We will remove `error_message` from `BaseToolOutput` and remove `success` and `error_message` from all internal DTOs (`ValidationErrorOutput`, `EnforcementErrorOutput`, `ConfigErrorOutput`, `CacheErrorOutput`) in a single step. We will completely delete the redundant `CacheErrorOutput`.
   - *Rationale:* Keeping deprecated attributes would invite future coupling and violate the clean Separation of Concerns contract.

2. **Core Tools Execution Returns:**
   - *Clean Break:* Refactor all tool execute methods to bubble exceptions rather than catching and returning error DTOs. Core tools return only their successful DTO.

3. **Server & Presenter:**
   - *Clean Break:* Transition immediately to `isinstance(result, BaseErrorOutput)` checks. All code path branching in `server.py` and `text_presenter.py` will rely on type evaluations.

4. **Test Suite refactoring:**
   - *Clean Break:* We will refactor all assertions in the test suite that assert on legacy properties (such as `.success` or `.error_message` on error DTOs) to check DTO type (`isinstance(result, BaseErrorOutput)`) or check presence of structured parameters.
   - *Rationale:* Tests that verify legacy behavior are themselves technical debt. They must be cleaned up to align with the new schema contracts.

---

## 6. Expected Results & Verification Baseline

1. **Static Analysis & Type Checks:**
   - Standard strict static analysis (`mypy` and `pyright`) passes 100% on the entire codebase.
   - Tool `execute` signatures match `SuccessDTO`, and decorators return type-compatible `BaseErrorOutput` DTOs.
2. **Quality Gates:**
   - `run_quality_gates` passes 10.00/10 with no warnings or violations of Presentation Boundary (§15) or SOLID.
3. **Execution Correctness:**
   - System/pipeline/validation errors correctly set `isError=True` in the MCP protocol.
   - Domain failures (e.g. failing tests, git status differences) do not trigger protocol errors and are returned cleanly as markdown content.
   - All tests in the test suite pass 100%.

---

## 7. Related Documentation

- [ARCHITECTURE_PRINCIPLES.md](file:///c:/temp/pgmcp/docs/coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [DOCUMENTATION_STANDARD.md](file:///c:/temp/pgmcp/docs/coding_standards/DOCUMENTATION_STANDARD.md)
- [presentation.yaml](file:///c:/temp/pgmcp/.phase-gate/config/presentation.yaml)
- [exceptions.py](file:///c:/temp/pgmcp/mcp_server/core/exceptions.py)
- [error_outputs.py](file:///c:/temp/pgmcp/mcp_server/schemas/error_outputs.py)

---

## 8. Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-26 | Agent | Initial draft |
| 1.1 | 2026-06-26 | Agent | Approved target kaders, clean break strategy, and test cleanup focus |
| 1.2 | 2026-06-26 | Agent | Refined target architecture with tool-level return segregation, deletion of redundant CacheErrorOutput, and presenter analysis |
