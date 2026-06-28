<!-- docs\development\issue289\design.md -->
<!-- template=design version=5827e841 created=2026-06-27T11:36Z updated= -->
# Error Taxonomy Refactoring & DTO Segregation Design

**Status:** DRAFT  
**Version:** 1.0.0  
**Last Updated:** 2026-06-27

---

## 1. Context & Requirements

### 1.1. Problem Statement

The current error representation on the MCP platform violates the Single Responsibility Principle (SRP) and the Presentation Boundary principle. Success DTOs (BaseToolOutput) contain error fields, error DTOs carry success fields, and presentation formatting is hardcoded in Python exceptions and decorator logic.

### 1.2. Requirements

**Functional:**
- [ ] Remove success and error_message fields from BaseToolOutput success DTOs.
- [ ] Introduce passed: bool = True on BaseToolOutput to indicate visual/logical domain outcomes.
- [ ] Remove success and error_message fields from BaseErrorOutput and subclasses ValidationErrorOutput, EnforcementErrorOutput, ConfigErrorOutput.
- [ ] Isolate traceback and error_message fields exclusively on ExecutionErrorOutput DTO.
- [ ] Remove redundant CacheErrorOutput DTO and handle caching errors cleanly via CachePublication.
- [ ] Ensure server.py and TextPresenter perform type-based error checks using isinstance(..., BaseErrorOutput).
- [ ] Separate presentation templates into a dedicated errors block in presentation.yaml and dynamically format messages using DTO structured parameters in TextPresenter.
- [ ] Add boot-time validation in validate_presentation_alignment to verify all subclasses of BaseErrorOutput have matching presentation templates.
- [ ] Convert core tools to return only success DTOs and bubble up structured exceptions instead of returning error DTOs.
- [ ] Explicitly define the EnforcementError exception in exceptions.py and raise it in EnforcementRunner for policy failures, separating validation from enforcement.
- [ ] Design reusable test assertion helpers assert_success_output and assert_error_output to clean up the test suite and reduce test bloat.
**Non-Functional:**
- [ ] Ensure strict type checking passes with mypy and pyright.
- [ ] Avoid hardcoded error presentation templates in Python logic (maintain strict Presentation Boundary).
- [ ] Ensure backward compatibility with existing tests by refactoring test assertions cleanly.

### 1.3. Constraints

*   **MCP Protocol Constraint**: The `isError` protocol attribute must be set to `True` if and only if the returned DTO is an instance of `BaseErrorOutput` (logical failures do not trigger protocol errors).
*   **Context Size Protection**: JSON-RPC error payload size must remain bounded. High-volume tracebacks and unhandled debug logs are isolated to `ExecutionErrorOutput` and cached in the operations cache rather than returned inline in transport.
*   **Presentation Boundary Constraint**: No core code may construct user-facing messages or embed emojis; formatting is inverted to the TextPresenter.
*   **Backward Compatibility of Success DTOs**: Tools returning logical checks (failing tests, linter failures) continue to return success DTOs with `passed: bool = False` to prevent triggering transport-level protocol errors.
---

## 2. Design Options

### 2.1. Option A: Clean Break with Custom Test Assertion Helpers (Preferred)

Remove success and error_message from DTOs. Core tools bubble up exceptions. Server uses isinstance. Refactor test assertions using centralized helpers.

**Pros:**
- 100% compliance with SRP/SOLID and Presentation Boundary.
- Completely eliminates legacy debt.
- Custom test helpers clean up test suite bloat and reduce fragility.

**Cons:**
- Requires significant initial effort to refactor assertions across 250+ tests.

### 2.2. Option B: Partial Clean Break (Keep success/error_message properties with deprecation warnings)

Keep success and error_message properties on DTOs as deprecated properties. Avoid refactoring the test suite immediately.

**Pros:**
- Reduces initial test refactoring effort.

**Cons:**
- Directly violates YAGNI.
- Keeps deprecated, SRP-violating attributes alive, inviting future coupling.

## 3. Chosen Design

**Decision:** Adopt a Clean Break strategy for DTO schemas, server-side type-based dispatch, presenter-level template mapping, core tool execution logic, and test assertions. Introduce central test assertion helpers under tests/mcp_server/assertion_helpers.py to abstract DTO structures and reduce test suite fragility.

**Rationale:** A Clean Break ensures that legacy, deprecated success/error fields are completely eliminated, preventing future coupling and domain leakage. Centralized test assertion helpers mitigate the blast radius of test suite updates, making tests more readable, robust, and DRY.

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| DTO Class Segregation | Isolate success and error DTO models to respect SRP. BaseToolOutput has passed: bool = True. BaseErrorOutput does not inherit from BaseToolOutput and has no success/error_message fields. |
| Presenter-Driven Formatting | Align with Presentation Boundary (§15). TextPresenter formats error messages from presentation.yaml templates based on BaseErrorOutput subclasses and their structured params. |
| Core Tool Exception Bubbling | Decouple core tools from error DTO generation. Core tools only return success DTOs; decorators handle exception mapping. |
| EnforcementError Exception | Define EnforcementError explicitly in exceptions.py to segregate policy gate check failures from input ValidationError, caught by EnforcementDecorator and mapped to EnforcementErrorOutput. |
| Centralized Test Assertion Helpers | Place assertions in tests/mcp_server/assertion_helpers.py to centralize DTO structure assertions, reducing test bloat and future fragility. |

### 3.2. Detailed Exception & DTO Mapping Contracts

This section defines the precise mappings between exceptions bubbled by core tools and the resulting error DTOs generated by the decorator pipeline, maintaining a strict separation between domain logic and presentation.

#### 3.2.1. Exceptions Taxonomy (`mcp_server/core/exceptions.py`)

All exceptions raised within core tools or managers inherit from `MCPError`:
*   `ValidationError`: Raised when input format/type validation or basic tool parameter checks fail. Code: `"ERR_VALIDATION"`.
*   `EnforcementError` [NEW]: Raised exclusively by the `EnforcementRunner` when policy gates or pre/post checks fail. Code: `"ERR_ENFORCEMENT"`.
*   `ConfigError`: Raised when loading or parsing configuration files fails. Code: `"ERR_CONFIG"`.
*   `PreflightError`: Raised when external system/environment checks fail. Code: `"ERR_PREFLIGHT"`.
*   `ExecutionError`: Raised for explicit tool execution errors that do not violate policies or inputs. Code: `"ERR_EXECUTION"`.

#### 3.2.2. DTO Schemas Contract (`mcp_server/schemas/error_outputs.py` and `tool_outputs.py`)

*   **`BaseToolOutput`** (Success DTOs):
    ```python
    class BaseToolOutput(BaseModel):
        model_config = ConfigDict(frozen=True, extra="forbid")
        passed: bool = True
        post_tool_instruction: str | None = None
    ```
*   **`BaseErrorOutput`** (Error DTOs base; does NOT inherit from `BaseToolOutput`):
    ```python
    class BaseErrorOutput(BaseModel):
        model_config = ConfigDict(frozen=True, extra="forbid")
        error_type: str
        params: dict[str, Any] = Field(default_factory=dict)
    ```
*   **`ValidationErrorOutput`**:
    ```python
    class ValidationErrorOutput(BaseErrorOutput):
        error_type: str = "ValidationError"
        validation_errors: list[dict[str, Any]] | str
        input_schema: dict[str, Any] = Field(default_factory=dict)
    ```
*   **`EnforcementErrorOutput`**:
    ```python
    class EnforcementErrorOutput(BaseErrorOutput):
        error_type: str = "EnforcementError"
        error_code: str
    ```
*   **`ConfigErrorOutput`**:
    ```python
    class ConfigErrorOutput(BaseErrorOutput):
        error_type: str = "ConfigError"
        file_path: str | None = None
    ```
*   **`ExecutionErrorOutput`**:
    ```python
    class ExecutionErrorOutput(BaseErrorOutput):
        error_type: str = "ExecutionError"
        error_message: str | None = None
        traceback: str | None = None
    ```

#### 3.2.3. Decorator Exception-to-DTO Translation Mapping

The Russian Doll decorator stack maps bubbled exceptions at the outer boundaries:

| Caught Exception | Decorator | Resulting Error DTO | Note / Design Choice |
| :--- | :--- | :--- | :--- |
| `pydantic.ValidationError` | `InputValidationDecorator` | `ValidationErrorOutput` | Translates raw input Pydantic violations. |
| `ValidationError` (Project) | `InputValidationDecorator` | `ValidationErrorOutput` | Custom input or scaffold schema validation failures. |
| `EnforcementError` | `EnforcementDecorator` | `EnforcementErrorOutput` | Raised when policy checks or gates fail. |
| `PreflightError` | `EnforcementDecorator` | `EnforcementErrorOutput` | Pre-flight git/env checks are mapped as policy failures (Option A). |
| `ConfigError` | `ToolErrorHandlerDecorator` | `ConfigErrorOutput` | Caught at outermost boundary for config loading failures. |
| `MCPSystemError` | `ToolErrorHandlerDecorator` | `ExecutionErrorOutput` | Infrastructure/adapter crashes mapped as system failures. |
| Unhandled `Exception` | `ToolErrorHandlerDecorator` | `ExecutionErrorOutput` | Fallback for unexpected bugs, capturing traceback and error message. |
#### 3.2.4. Core Tool Refactoring Specifications

Every core tool in `mcp_server/tools/` is refactored as follows:
*   Remove all `success=...` and `error_message=...` parameters from returned DTOs.
*   Remove all try-except blocks that catch exceptions only to return error DTOs. Instead, allow exceptions (`EnforcementError`, `ValidationError`, `ConfigError`, etc.) to bubble up freely.
*   Signatures of `execute` are typed as `async def execute(self, params: TInput, context: NoteContext) -> TOutput` where `TOutput` is strictly a subclass of `BaseToolOutput` representing a successful run.

#### 3.2.5. Presenter & Boot-Time Validation

*   **`presentation.yaml`**: Contains a root-level `errors` section:
    ```yaml
    errors:
      ValidationErrorOutput: "Validation failed: {validation_errors}"
      EnforcementErrorOutput: "Policy check failed: {error_code}"
      ConfigErrorOutput: "Configuration error in file: {file_path}"
      ExecutionErrorOutput: "An unexpected error occurred. (Details: {error_message})"
    ```
*   **`TextPresenter`**:
    *   **Lookup Hierarchy**: To prevent loss of specific user-facing feedback, templates are resolved in the following strict order:
        1.  **`error_code` template**: If the DTO contains an `error_code` (as an attribute or key in `params`), look up a specific template under `global.failures` in `presentation.yaml`.
        2.  **DTO class template**: Fall back to the class-level template mapped under the `errors` section in `presentation.yaml`.
        3.  **Default failure**: Fall back to the `default_failure_template`.
    *   This ensures that all rich, context-specific messages (e.g. branch creation mismatches, dirty directory blocks) are fully preserved and formatted using DTO parameters, without requiring a separate DTO class for every error type.
    *   **`default_failure_template` Update**: The `default_failure_template` in `presentation.yaml` is updated to `"Failed: {error_type}"` or a safe fallback parameter that does not reference `error_message`, since `error_message` is removed from non-execution DTOs.
*   **`validate_presentation_alignment`**:
    *   Reflected dynamically using `BaseErrorOutput.__subclasses__()`.
    *   Asserts that a template exists for every subclass in `errors`.
    *   Validates that all formatting placeholders in the template match fields defined on the DTO model class.
    *   Ensures all `error_code` values raised in exceptions have a corresponding template registered under `global.failures` in `presentation.yaml`, raising a fail-fast `ConfigError` at boot time if any drift is detected.

#### 3.2.6. Inventory of Tools Affected by `success=False` Refactoring

To guarantee complete scoping, we classify every tool currently returning `success=False` in `mcp_server/tools/` into one of two patterns:
1.  **Logical Failure (`passed=False` on success DTO)**: The tool completes execution successfully and returns its success DTO, but the domain-level logical check failed.
2.  **Execution Exception (Raise structured exception)**: The tool cannot complete execution due to input validation, policy gate, git conflict, environment, or configuration failures.

| Tool Component | Current `success=False` Pattern | Target Design Action | Affected DTO / Exception |
| :--- | :--- | :--- | :--- |
| `quality_tools.py` (`AutoFixTool`) | Returns `AutoFixOutput(success=False, error_message=...)` on fixer failures. | Convert to logical failure. Sets `passed=False` and adds `failed_gate`/`exit_code` to DTO. | `AutoFixOutput` |
| `quality_tools.py` (`RunQualityGatesTool`) | Returns `RunQualityGatesOutput(success=False, ...)` on linter/checker failures. | Convert to logical failure. Sets `passed=False` on output. | `RunQualityGatesOutput` |
| `test_tools.py` (`RunTestsTool`) | Returns `RunTestsOutput` with logical fail status. | Convert to logical failure. Sets `passed=False` on output when failures > 0. | `RunTestsOutput` |
| `safe_edit_tool.py` (`SafeEditTool`) | Returns `SafeEditOutput(success=False, ...)` on validation/dry-run failures. | Convert to logical failure. Sets `passed=False` on output. | `SafeEditOutput` |
| `template_validation_tool.py` | Returns `TemplateValidationOutput(success=False, ...)` on syntax failures. | Convert to logical failure. Sets `passed=False` on output. | `TemplateValidationOutput` |
| `cycle_tools.py` (`TransitionCycleTool`) | Returns `CycleTransitionOutput(success=False, ...)` on issue detection or SSE errors. | Raise `ValidationError` (for missing issue) or `EnforcementError` (for conflict/gate failures). | `ValidationError`, `EnforcementError` |
| `phase_tools.py` (`TransitionPhaseTool`) | Returns `PhaseTransitionOutput(success=False, ...)` on gate violations. | Raise `EnforcementError` on gate violations. | `EnforcementError` |
| `git_tools.py` (All git mutation tools) | Catch `ValidationError`, `PreflightError`, or `OSError` and return `success=False` DTOs. | Remove try-except blocks. Let `ValidationError`, `PreflightError`, and `EnforcementError` bubble up. | `ValidationError`, `PreflightError`, `EnforcementError` |
| `git_fetch_tool.py` (`GitFetchTool`) | Catches exceptions and returns `success=False` DTO. | Let exceptions bubble up as `PreflightError` or `ExecutionError`. | `PreflightError`, `ExecutionError` |
| `git_pull_tool.py` (`GitPullTool`) | Catches exceptions and returns `success=False` DTO. | Let exceptions bubble up as `PreflightError` or `ExecutionError`. | `PreflightError`, `ExecutionError` |
| `git_analysis_tools.py` | Catch exceptions during git status/diff and return `success=False` DTOs. | Let exceptions bubble up as `PreflightError` or `ExecutionError`. | `PreflightError`, `ExecutionError` |
| `pr_tools.py` (`SubmitPRTool`) | Returns `PROutput(success=False, ...)` on dirty workdir or API crashes. | Let exceptions bubble up as `PreflightError` or `ExecutionError`. | `PreflightError`, `ExecutionError` |
| `project_tools.py` | Returns `InitializeProjectOutput(success=False, ...)` on directory policy errors. | Let exceptions bubble up as `ValidationError` or `PreflightError`. | `ValidationError`, `PreflightError` |
| `scaffold_artifact.py` | Catches exceptions and returns `success=False` DTO. | Let exceptions bubble up as `ValidationError` or `ConfigError`. | `ValidationError`, `ConfigError` |
| `scaffold_schema_tool.py` | Catches exceptions and returns `success=False` DTO. | Let exceptions bubble up as `ValidationError` or `ConfigError`. | `ValidationError`, `ConfigError` |

## Related Documentation
- docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
- docs/coding_standards/DOCUMENTATION_STANDARD.md
- docs/development/issue289/research.md
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-27 | Agent | Initial draft |
