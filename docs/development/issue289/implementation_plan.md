<!-- docs\development\issue289\implementation_plan.md -->
<!-- template=planning version=130ac5ea created=2026-06-28T06:01Z updated= -->
# Implementation Plan - Redesign Error DTOs & Exception Segregation

**Status:** APPROVED  
**Version:** 1.0.0  
**Last Updated:** 2026-06-28

## Prerequisites

Read these first:
1. [Approved research document](file:///c:/temp/pgmcp/docs/development/issue289/tools_error_mapping_research.md)
2. [Approved design document](file:///c:/temp/pgmcp/docs/development/issue289/presentation_error_codes_design.md)

---

## Review & Approval Doctrine (MANDATORY)

To ensure the user is fully in the loop for every change, we will follow a strict **Go/No-go** protocol for each step:

1. **Step Proposal (Before Edit)**:
   - The agent will explain in the chat exactly what is going to change, which files are affected, how the logic changes, and why.
   - The agent will **stop** and wait for the user's explicit approval ("Go") before touching any files.
2. **Step Execution**:
   - Once approved, the agent will perform the file edits or test commands.
3. **Step Presentation (After Edit)**:
   - The agent will present the resulting code diffs, files, or verification outcomes.
   - The agent will wait for confirmation before moving to the next step.

---

## MANDATORY Architectural & Testing Safeguards (Primacy of ARCHITECTURE_PRINCIPLES.md)

To prevent regression into defensive compatibility coding, the following rules are strictly enforced and binding:

1. **Explicit Architectural Mapping on Proposals**:
   - Every Step Proposal (Step 1 of the Doctrine) must explicitly state which section of `docs/coding_standards/ARCHITECTURE_PRINCIPLES.md` justifies the proposed design change.
2. **Behavioral Testing ONLY (No Exception Message Checks)**:
   - Any test checking the string value of Category 1 exceptions (e.g. via `pytest.raises(..., match=...)` or checking `str(exc)`) is architecturally invalid.
   - When a test file is touched, all such checks must be immediately refactored to test *behavior* (verifying `exc.code`, `exc.error_code`, or `exc.params`).
   - No compatibility wrappers, fallback string formatting, or ad-hoc custom properties are allowed in production code to keep legacy string assertions happy. The test must be updated, not the code.
3. **Decorator DTO Ignorance**:
   - Tools and inner decorators (`InputValidationDecorator`, `EnforcementDecorator`) must have zero dependencies on and zero imports of error DTO classes. All domain failures bubble up as exceptions. Centralized translation occurs exclusively at the outer `ToolErrorHandlerDecorator` boundary.

---

## Summary

Refactor decorators, exceptions, managers, and all 51 core tools to strictly segregate success and error outputs, routing all user-facing templates to presentation.yaml.

We will eliminate the side-channel `NoteContext` class entirely. Instead, notes will be represented as first-class DTOs (`NoteDTO`) on `BaseToolOutput`. For exceptions (failures), recovery and suggestion notes will be defined directly in `presentation.yaml` under `failures` (Option B) for visual uniformity without Python boilerplate.

---

## TDD Cycles

### Cycle 6: Base Infrastructure

**Goal:** Align exceptions.py, decorators, and text_presenter.py to support `passed` bool, `NoteDTO`, and block message arguments, while fully eliminating the `NoteContext` sidecar.

**Detail of Changes:**
1. **tool_outputs.py**:
   - Define `NoteType` enum (`exclusions`, `suggestions`, `recoveries`, `info`).
   - Define `NoteDTO` with `type`, `code`, and `params`.
   - Update `BaseToolOutput` with `passed: bool = True` and `notes: list[NoteDTO] = Field(default_factory=list)`.
2. **exceptions.py**:
   - Remove `message: str` argument from `ValidationError`, `PreflightError`, and `EnforcementError` constructors. Pass `""` internally to `super().__init__()`.
   - `ValidationError` and `PreflightError` will use static base codes (`ERR_VALIDATION` and `ERR_PREFLIGHT`) and store fine-grained codes in `self.error_code`. No `__str__` overrides formatting human-readable messages.
3. **decorators**:
   - **`ToolErrorHandlerDecorator`**: Central outermost boundary. Catch `ValidationError`, `EnforcementError`, and `PreflightError` and map them to their corresponding DTOs (`ValidationErrorOutput`, `EnforcementErrorOutput`, `PreflightErrorOutput`).
   - **`InputValidationDecorator`**: Raise custom `ValidationError` on Pydantic validation failure. Has zero DTO imports/knowledge.
   - **`EnforcementDecorator`**: Let pre- and postflight exceptions bubble up. Has zero DTO imports/knowledge.
4. **text_presenter.py**: Update `is_error` and `resolved_success` to check `getattr(data, "passed", True) is False` instead of `getattr(data, "success", True)`. Update `validate_presentation_alignment` to allow `"passed"`.
5. **Delete operation_notes.py**: Delete `mcp_server/core/operation_notes.py`. Remove `context` parameter from decorators and core execute signatures.

**Tests:**
- `tests/mcp_server/unit/schemas/test_tool_outputs.py`
- `tests/mcp_server/unit/core/test_exceptions.py`
- `tests/mcp_server/unit/presenters/test_text_presenter.py`
- `tests/mcp_server/integration/test_exception_propagation.py`
- `tests/mcp_server/integration/test_metadata_e2e.py`
- `tests/mcp_server/integration/test_validation_policy_e2e.py`
- `tests/mcp_server/integration/test_context_loaded_enforcement.py`
- `tests/mcp_server/integration/test_pr_status_lockdown.py`
- `tests/mcp_server/managers/test_git_manager_config.py`

**Success Criteria:**
- All tests pass (testing strictly on behavior - exception class, base code, error code, params - never regex matching messages)
- Zero compile/type errors

### Cycle 7: Managers Refactoring

**Goal:** Remove hardcoded error messages from git_manager, enforcement_runner, artifact_manager, and phase_state_engine, updating signatures to remove `note_context`.

**Detail of Changes:**
1. **git_manager.py**: Remove hardcoded strings from `ValidationError` and `PreflightError` raise calls. Remove `note_context` argument.
2. **enforcement_runner.py**: Remove hardcoded strings from `EnforcementError` raise calls. Remove `note_context` argument.
3. **artifact_manager.py**: Remove hardcoded strings from `ValidationError` raise calls. Remove `note_context` argument.
4. **phase_state_engine.py**: Replace standard `ValueError` and `StateAlreadyExistsError` raised in `initialize_branch` with custom `ValidationError` throwing structured error codes. Remove `note_context` argument.

**Tests:**
- `tests/mcp_server/unit/managers/...`

**Success Criteria:**
- All manager tests pass

### Cycle 8: Tools Refactoring (Batch 1-5)

**Goal:** Refactor all 51 core tools in 5 batches with step-by-step user review, removing `context` argument and mapping to DTO-bound `NoteDTO`s.

**Batches:**
- **Batch 1: File & Transition Control Tools** (SafeEditTool, InitializeProjectTool, GetProjectPlanTool, transition tools)
- **Batch 2: Git Mutation & Query Tools** (GitCommit, GitRestore, GitCheckout, GitPush, etc.)
- **Batch 3: GitHub Issue, Label, and PR Tools**
- **Batch 4: Quality & Test Tools**
- **Batch 5: Scaffolding, Schemas, & Search Tools**

**Tests:**
- `tests/mcp_server/integration/...`

**Success Criteria:**
- All integration and E2E tests pass

---

## Related Documentation
- **[docs/development/issue289/tools_error_mapping_research.md][related-1]**
- **[docs/development/issue289/presentation_error_codes_design.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/development/issue289/tools_error_mapping_research.md
[related-2]: docs/development/issue289/presentation_error_codes_design.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-28 | Agent | Initial draft with strict Review Doctrine and Base Infrastructure Phase details |
| 1.1.0 | 2026-06-28 | Agent | Update plan to use NoteDTOs, remove NoteContext, and use Option B for failure template structures |
