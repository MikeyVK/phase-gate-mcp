<!-- c:\temp\pgmcp\docs\development\issue404\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-17T20:02Z updated= -->
# Planning: Resolving TextPresenter Formatting Gaps & Error Propagation

**Status:** DRAFT  
**Version:** 1.1.0  
**Last Updated:** 2026-06-17

---

## Purpose

Define the implementation cycles, sequencing, test coverage, and validation obligations for resolving presenter formatting gaps and error propagation.

## Scope

**In Scope:**
Pydantic schemas in presentation_config.py, schemas/error_outputs.py, text_presenter.py rendering loop and custom Formatter, server.py exception bridge, validate_presentation_alignment blacklist, operation_notes.py generic Note class and NoteContext, note and exception migrations across managers and adapters, and clean break test refactoring.

**Out of Scope:**
Phase 2 Decorator Pipeline refactoring, modifications to external client tools, or changes to tool registration schemas.

## Prerequisites

Read these first:
1. Approved design in docs/development/issue404/design.md
2. Clean Git state on feature/404-resolve-textpresenter-formatting-gaps
---

## Summary

Sequential planning breakdown for notes redesign (generic Note class, fallback config templates, rendering loop) and exception propagation bridge (Pydantic schemas, Error DTOs, formatter subclass, and drift validator parameter blacklists) including explicit dead code cleanup in Cycle 6.

---

## Dependencies

- Approved design document (design.md) approval

---

## 4. TDD Cycles

### Cycle 1: Configuration Schemas & Error DTOs
- **Goal:** Define the error DTO structures in [error_outputs.py](file:///c:/temp/pgmcp/mcp_server/schemas/error_outputs.py) and extend [presentation_config.py](file:///c:/temp/pgmcp/mcp_server/config/schemas/presentation_config.py) to prevent Pydantic validation crashes.
- **Tests:** `tests/mcp_server/unit/test_presenter.py`
- **Deliverables:**
  - `D1.1`: Extend [presentation_config.py](file:///c:/temp/pgmcp/mcp_server/config/schemas/presentation_config.py) with Pydantic configuration schemas (`FormattingConfig`, `NoteGroupConfig`, `GlobalNotesConfig`, `failures`, and `formatting` fields).
  - `D1.2`: Define base `ToolErrorOutput` (with `params: dict[str, Any]`) and error DTO subclasses in [error_outputs.py](file:///c:/temp/pgmcp/mcp_server/schemas/error_outputs.py).
- **Exit Criteria:** Pydantic presentation configuration model correctly loads formatting, global templates, and failures. Custom error DTO models compile and enforce `extra='forbid'` and `frozen=True`.

### Cycle 2: Note Presentation Engine & Loop
- **Goal:** Implement the generic `Note` class, the custom `string.Formatter` subclass, and the `present_notes` loop in [text_presenter.py](file:///c:/temp/pgmcp/mcp_server/presenters/text_presenter.py).
- **Tests:** `tests/mcp_server/unit/test_presenter.py`, `tests/mcp_server/unit/core/test_note_context_unit.py`
- **Deliverables:**
  - `D2.1`: Implement `Note(key, params)` dataclass and deprecate legacy note classes in [operation_notes.py](file:///c:/temp/pgmcp/mcp_server/core/operation_notes.py).
  - `D2.2`: Implement `SafeNoneFormatter` subclass of `string.Formatter` to safely format `None` values, bypassing specifiers.
  - `D2.3`: Implement `TextPresenter.present_notes(tool_name, notes)` with note grouping and markdown formatting.
- **Exit Criteria:** Unit tests verify note rendering loop and safe formatter.

### Cycle 3: server.py Integration Bridge & Error Interception
- **Goal:** Catch exceptions in `handle_call_tool`, map them to error DTOs, cache them, and render notes via `TextPresenter` in [server.py](file:///c:/temp/pgmcp/mcp_server/server.py).
- **Tests:** `tests/mcp_server/unit/test_server.py`
- **Deliverables:**
  - `D3.1`: Intercept validation, enforcement, and execution exceptions in `handle_call_tool` in [server.py](file:///c:/temp/pgmcp/mcp_server/server.py), mapping to error DTOs and caching/formatting them.
  - `D3.2`: Decouple `NoteContext` from direct rendering and route collected notes to `TextPresenter.present_notes` in [server.py](file:///c:/temp/pgmcp/mcp_server/server.py).
- **Exit Criteria:** Validation, enforcement, and execution exceptions are caught, DTO-wrapped, cached, and formatted using templates.

### Cycle 4: Drift Validator Extension & Blacklist
- **Goal:** Extend `validate_presentation_alignment` to validate failure templates and note placeholders while blacklisting backdoor parameters.
- **Tests:** `tests/mcp_server/unit/test_presenter.py`
- **Deliverables:**
  - `D4.1`: Extend `validate_presentation_alignment` in [text_presenter.py](file:///c:/temp/pgmcp/mcp_server/presenters/text_presenter.py) to validate failure templates and note placeholders.
  - `D4.2`: Enforce generic parameter name blacklist (`message`, `msg`, `text`, `txt`, `error_message`, `error`, `err`) in templates.
- **Exit Criteria:** Server fails to boot with `ConfigError` if templates violate backdoor or blacklist rules.

### Cycle 5: Code & Note Production Migration
- **Goal:** Migrate note production and exceptions in managers and adapters (including [git_manager.py](file:///c:/temp/pgmcp/mcp_server/managers/git_manager.py), [enforcement_runner.py](file:///c:/temp/pgmcp/mcp_server/managers/enforcement_runner.py), [qa_manager.py](file:///c:/temp/pgmcp/mcp_server/managers/qa_manager.py), [artifact_manager.py](file:///c:/temp/pgmcp/mcp_server/managers/artifact_manager.py), [deliverable_checker.py](file:///c:/temp/pgmcp/mcp_server/managers/deliverable_checker.py), [phase_state_engine.py](file:///c:/temp/pgmcp/mcp_server/managers/phase_state_engine.py) and adapters) and tools to use generic `Note` events and exception codes.
- **Tests:** `tests/mcp_server/unit/test_server.py`, `tests/mcp_server/integration/`
- **Deliverables:**
  - `D5.1`: Migrate note production and exceptions in managers and adapters to the new format.
  - `D5.2`: Remove Python transition advisory notes in [cycle_tools.py](file:///c:/temp/pgmcp/mcp_server/tools/cycle_tools.py) and tools.
- **Exit Criteria:** All managers/adapters migrated. Server compiles and E2E integration tests pass using the compatibility mapper.

### Cycle 6: Test Suite Refactoring, Clean Break & Dead Code Cleanup
- **Goal:** Remove the compatibility mapper and legacy note subclasses from [operation_notes.py](file:///c:/temp/pgmcp/mcp_server/core/operation_notes.py), refactor tests, and delete dead code in production and tests.
- **Tests:** `tests/mcp_server/unit/core/test_note_context_unit.py`, `tests/mcp_server/unit/test_server.py`, `tests/mcp_server/integration/`
- **Deliverables:**
  - `D6.1`: Remove compatibility mapper and legacy note subclasses from [operation_notes.py](file:///c:/temp/pgmcp/mcp_server/core/operation_notes.py).
  - `D6.2`: Refactor all unit and integration test suites to assert presenter-formatted markdown blocks.
  - `D6.3`: Identify and delete all dead/obsolete code in both production and test suites (including legacy `to_message()` methods and unused note fixtures/helpers/assertions).
- **Exit Criteria:** All legacy note subclasses and `to_message()` methods are deleted. All unit and integration test assertions are updated to verify presenter output. All dead/obsolete code in both production and test suites is completely removed. Full test suite passes.

---

## 5. Execution Obligations & Constraints

### 5.1. Typing Obligations
- **Playbook Compliance:** All new and modified production and test code must conform to the strict type safety rules defined in [Type Checking Playbook](../../coding_standards/TYPE_CHECKING_PLAYBOOK.md).
- **No Global Disables:** Mass diagnostics disabling in `pyrightconfig.json` or `mypy` global overrides is forbidden. Line-level specific ignores with rationales only.
- **Strict DTO Verification:** Newly defined DTOs in `error_outputs.py` and `presentation_config.py` must compile under Pyright with zero typing issues.

### 5.2. Quality Gate Expectations
- **Strict Quality Rules:** All code must conform to [Quality Gates](../../coding_standards/QUALITY_GATES.md).
- **Formatting & Style:** Code must maintain a 10.00/10 pylint score, conform to Ruff strict formatting and import sorting, and enforce a maximum line length of 100 characters.
- **Coverage baseline:** Maintain branch test coverage >= 90% for all modified or newly introduced production modules.

### 5.3. Approved Strategy Execution Constraints
- **Topic 1 (Notes Redesign): Clean Break Requirement:** In Cycle 6, we enforce an absolute Clean Break. All legacy subclassed note types and `to_message()` methods must be deleted, leaving `Note(key, params)` as the single source of truth.
- **Topic 2 (Error Presentation): Temporary Integration Bridge:** The bridge inside `server.py` (`handle_call_tool`) is a temporary architectural bridge. It catches exceptions and formats DTOs directly, but it must keep public JSON-RPC E2E boundaries stable so that Phase 2 decorators can seamlessly replace it.

---

## 6. Risks & Mitigation

- **Risk:** Duplicating or mismatched parameters between note events and yaml templates.
  - **Mitigation:** Cycle 4 drift validator will catch mismatched fields at boot time, preventing runtime errors.
- **Risk:** Unexpected crashes on None formatting values.
  - **Mitigation:** Cycle 2 custom Formatter class explicitly catches None and bypasses specifiers.

---

## 7. Milestones

- **Milestone 1:** Cycle 1-4 core presenter and server bridge changes pass quality gates and unit tests.
- **Milestone 2:** Cycle 5 full codebase notes and exception migration completed.
- **Milestone 3:** Cycle 6 clean break and full test suite passes with zero dead code or legacy note classes remaining.

---

## 8. Related Documentation
- **[Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md)**
- **[Architectural Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)**
- **[Quality Gates](../../coding_standards/QUALITY_GATES.md)**
- **[Type Checking Playbook](../../coding_standards/TYPE_CHECKING_PLAYBOOK.md)**
- **[Design Document](design.md)**
- **[Research Document](research.md)**

---

## 9. Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-17 | Agent | Initial draft |
| 1.1.0 | 2026-06-17 | Agent | Integrated QA plan-verifier audit feedback: fixed double-numbered headers, explicitly defined typing and quality gate expectations, added Approved Strategy constraints, and resolved deliverable details |
