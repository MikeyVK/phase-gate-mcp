<!-- docs\development\issue413\presentation_error_codes_design.md -->
<!-- template=design version=5827e841 created=2026-06-27T20:16s updated= -->
# Presentation Error Codes and Templates Contract

**Status:** APPROVED  
**Version:** 1.0.0  
**Last Updated:** 2026-06-27

---

## Purpose

Define the presentation error codes and templates contract for Issue #413.

---

## 1. Context & Requirements

### 1.1. Problem Statement

To prevent error messages from becoming generic, we must define the exact mapping of error codes and templates in presentation.yaml for all core tool exceptions before implementation starts.

### 1.2. Requirements

**Functional:**
- [ ] Define exact error_code and template string for every failure case across all tools.
- [ ] Register all new templates under global.failures in presentation.yaml.

**Non-Functional:**
- [ ] Maintain strict Presentation Boundary compliance.
- [ ] Ensure no hardcoded strings leak into exception classes.

### 1.3. Constraints

- Presentation templates must reside exclusively in presentation.yaml under failures.
- Exception constructors must not accept user-facing text strings.

---

## 2. Design Options

### 2.1. Option A: Centralized presentation.yaml Registry (Preferred)

Register all failure templates inside the `failures` block in `presentation.yaml`. Exceptions raised inside core tools only pass an `error_code` and parameters.

*   **Pros:**
    *   Guarantees strict separation of presentation and logic.
    *   All user-facing templates are in one central, easy-to-manage location.
    *   Enables compile-time and boot-time validation of error templates.
*   **Cons:**
    *   Requires upfront mapping of all failure paths.

### 2.2. Option B: Ad-hoc Inline Error Strings in Tools

Allow tools to raise exceptions containing hardcoded string messages.

*   **Pros:**
    *   Saves upfront mapping time.
*   **Cons:**
    *   Leaks user-facing text into core code; violates the Presentation Boundary architecture.
    *   Makes error messages fragile and hard to maintain or localize.

---

## 3. Chosen Design

**Decision:** Establish a structured catalog of 18 specific error codes and templates in presentation.yaml, refactoring exceptions to only accept error_code and params.

**Rationale:** Defining the contract upfront ensures consistency and prevents implementation-time ad-hoc deviations.

### 3.1. Key Design Decisions

| Decision | Rationale | Impact |
| :--- | :--- | :--- |
| Remove the message parameter from ValidationError, PreflightError, and EnforcementError constructors | Design-enforces the Presentation Boundary at compile-time. | Core tools cannot raise exceptions with hardcoded user-facing strings. |
| Pre-map all predictable failures to specific error codes in presentation.yaml | Avoids generic fallbacks and ensures high-quality user-facing errors. | The presentation layer handles all error rendering. |

### 3.2. Presentation Error Codes & Templates Contract

| Error Code | Template String | Expected Parameters | Raising Tool(s) | Exception Class |
| :--- | :--- | :--- | :--- | :--- |
| `invalid_regex` | `"Invalid regex pattern '{pattern}': {error}"` | `pattern`, `error` | `SafeEditTool` | `ValidationError` |
| `line_out_of_bounds` | `"Line {line} is out of bounds (file has {total} lines)."` | `line`, `total` | `SafeEditTool` | `ValidationError` |
| `overlapping_edits` | `"Overlapping line edits detected in range {start}-{end}."` | `start`, `end` | `SafeEditTool` | `ValidationError` |
| `file_locked` | `"File '{path}' is already being edited. Please wait or bundle multiple edits."` | `path` | `SafeEditTool` | `PreflightError` |
| `missing_cycle_number` | `"Committing in cycle-based phase '{phase}' requires a valid 'cycle_number'."` | `phase` | `GitCommitTool` | `ValidationError` |
| `state_mutation_conflict` | `"State mutation conflict: {error_details}"` | `error_details` | `TransitionCycleTool`, `TransitionPhaseTool`, `RunQualityGatesTool` | `ValidationError` |
| `git_error` | `"Git command failed: {error_details}"` | `error_details` | `CheckMergeTool`, `GitStatusTool` | `ExecutionError` |
| `no_project_plan` | `"No project plan found for issue #{issue_number}."` | `issue_number` | `GetProjectPlanTool` | `ValidationError` |
| `missing_planning_deliverables` | `"Planning deliverables file '{path}' was not found or is empty after writing."` | `path` | `SavePlanningDeliverablesTool`, `UpdatePlanningDeliverablesTool` | `ValidationError` |
| `label_validation_failed` | `"Label validation failed: {error_details}"` | `error_details` | `CreateIssueTool` | `ValidationError` |
| `invalid_label_name` | `"Label name '{name}' does not match the required naming convention."` | `name` | `CreateLabelTool` | `ValidationError` |
| `invalid_phase_label` | `"Label phase value '{phase}' is not a recognized workphase."` | `phase` | `CreateLabelTool`, `AddLabelsTool` | `ValidationError` |
| `invalid_color_code` | `"Color code '{color}' is invalid. Must be a 6-character hex string without '#' prefix."` | `color` | `CreateLabelTool` | `ValidationError` |
| `invalid_labels_registry` | `"Label operation failed: labels '{labels}' are not configured in labels.yaml."` | `labels` | `AddLabelsTool` | `ValidationError` |
| `invalid_workflow_config` | `"Workflow '{workflow}' requires custom phases to be configured."` | `workflow` | `InitializeProjectTool` | `ValidationError` |
| `pytest_timeout` | `"Tests timed out after {timeout} seconds."` | `timeout` | `RunTestsTool` | `ExecutionError` |
| `pytest_execution_failed` | `"Failed to run tests: {error_details}"` | `error_details` | `RunTestsTool` | `ExecutionError` |
| `docs_dir_missing` | `"Documentation directory '{docs_dir}' not found."` | `docs_dir` | `SearchDocumentationTool` | `ValidationError` |

---

## 4. Note Contexts vs. Presenter Failure Templates

To keep the codebase lean and prevent repetitive boilerplate, we refine the roles of `NoteContext` and `failures` presenter templates:

1. **Exception-Based Failures (No Notes Needed)**:
   - When a tool or manager raises a Category 1 exception (e.g., `ValidationError`, `PreflightError`, `EnforcementError`), execution halts immediately.
   - We **do not** need to produce separate `Note` objects in Python code.
   - Instead, the corresponding template under `failures` in `presentation.yaml` bundles **both** the diagnostic description and the recovery/suggestion text.
   - *Example*: For `line_out_of_bounds`, the template in `failures` becomes:
     `"Line {line} is out of bounds (file has {total} lines). Suggestion: Inspect the file using view_file or git diff to verify the correct range."`

2. **Logical Failures and Info on Success (Notes Required)**:
   - When a tool executes successfully but has logical failures (e.g. `passed=False` on `RunTestsOutput` or `RunQualityGatesOutput`) or needs to provide metadata (like the created commit hash), no exception is raised.
   - Here, `NoteContext` is still required to attach suggestions, recoveries, or information (e.g. `pytest_failed_verbose_suggestion`).

### 4.1. Refined failures Template Registry (with recovery text included)

We update the failures registry in `presentation.yaml` to include actionable recoveries and suggestions directly:

| Error Code | Template String (with Diagnostic + Recovery) | Raising Layer / Component |
| :--- | :--- | :--- |
| `invalid_regex` | `"Invalid regex pattern '{pattern}': {error}. Suggestion: Verify the regex pattern syntax or test it locally before running the tool."` | Tool (`SafeEditTool`) |
| `line_out_of_bounds` | `"Line {line} is out of bounds (file has {total} lines). Suggestion: Inspect the file using view_file or git diff to verify the correct range."` | Tool (`SafeEditTool`) |
| `overlapping_edits` | `"Overlapping line edits detected in range {start}-{end}. Suggestion: Make sure each ReplacementChunk targets a unique and non-overlapping line range."` | Tool (`SafeEditTool`) |
| `file_locked` | `"File '{path}' is already being edited. Recovery: Wait for the concurrent process to release the file lock, or bundle multiple edits."` | Tool / Manager |
| `missing_cycle_number` | `"Committing in cycle-based phase '{phase}' requires a valid 'cycle_number'. Suggestion: Retrieve the current cycle number using get_work_context, then provide it in the arguments."` | Tool / Manager |
| `state_mutation_conflict` | `"State mutation conflict: {error_details}. Recovery: Wait for concurrent state updates to finish and retry."` | Manager |
| `git_error` | `"Git command failed: {error_details}. Recovery: Verify the local branch state, remote configuration, and network connection."` | Manager |
| `no_project_plan` | `"No project plan found for issue #{issue_number}. Suggestion: Run initialize_project to bootstrap the project plan for this issue."` | Tool / Manager |
| `missing_planning_deliverables` | `"Planning deliverables file '{path}' was not found or is empty. Suggestion: Verify the path is correct and ensure the file is saved before calling the tool."` | Tool / Manager |
| `label_validation_failed` | `"Label validation failed: {error_details}. Suggestion: Verify the labels exist on GitHub and conform to the project guidelines."` | Tool / Manager |
| `invalid_label_name` | `"Label name '{name}' does not match the required naming convention. Suggestion: Conform to naming conventions (e.g. prefix with 'phase:', 'type:', or 'priority:')."` | Tool / Manager |
| `invalid_phase_label` | `"Label phase value '{phase}' is not a recognized workphase. Suggestion: Ensure the phase value matches a valid workflow phase name."` | Tool / Manager |
| `invalid_color_code` | `"Color code '{color}' is invalid. Suggestion: Provide a 6-character hex code, e.g. 'ff0000' (omit the '#' prefix)."` | Tool / Manager |
| `invalid_labels_registry` | `"Label operation failed: labels '{labels}' are not configured in labels.yaml. Suggestion: Add the label to labels.yaml or use an already registered label."` | Tool / Manager |
| `invalid_workflow_config` | `"Workflow '{workflow}' requires custom phases to be configured. Suggestion: Ensure the workflow is defined in contracts.yaml and contains valid phases."` | Tool / Manager |
| `pytest_timeout` | `"Tests timed out after {timeout} seconds. Recovery: Run a smaller subset of tests or raise the timeout."` | Manager |
| `pytest_execution_failed` | `"Failed to run tests: {error_details}. Recovery: Check the test output and tracebacks for syntax errors or import issues."` | Manager |
| `docs_dir_missing` | `"Documentation directory '{docs_dir}' not found. Suggestion: Create a 'docs/' directory in the workspace root and populate it with markdown files."` | Tool / Manager |

---

## Related Documentation
- **[docs/development/issue413/tools_error_mapping_research.md](file:///C:/temp/pgmcp/docs/development/issue413/tools_error_mapping_research.md)**

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-27 | Agent | Initial draft with full error templates contract |
