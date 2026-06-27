<!-- docs\development\issue413\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-27T12:20Z updated= -->
# Error Taxonomy Refactoring & DTO Segregation Planning

**Status:** DRAFT  
**Version:** 1.0.0  
**Last Updated:** 2026-06-27

---

## Summary

This plan decomposes the Clean Break refactoring of the error DTO taxonomy and exception handling into 5 sequential implementation cycles. Each cycle uses strict TDD (RED -> GREEN -> REFACTOR) and has explicit validation obligations to prevent system-wide regressions.

---

## TDD Cycles


### Cycle 1: Cycle 1: Test Suite Preparation & Assertion Helpers

**Goal:** Abstract DTO success/failure assertions in tests to minimize blast radius and clean up test suite bloat.

**Tests:**
- tests/mcp_server/unit/test_assertion_helpers.py (new)

**Success Criteria:**
- Custom assertion helpers `assert_success_output` and `assert_error_output` created in `tests/mcp_server/assertion_helpers.py`.
- All 250+ assertions on `result.success` or `result.error_message` in the test suite refactored to use the new helpers.
- The test suite remains green.



### Cycle 2: Cycle 2: Exceptions Taxonomy Expansion

**Goal:** Define and integrate the new `EnforcementError` exception to segregate input validation from policy gates.

**Tests:**
- tests/mcp_server/unit/core/test_exceptions.py
- tests/mcp_server/unit/decorators/test_pipeline_decorators.py

**Success Criteria:**
- `EnforcementError` exception defined in `mcp_server/core/exceptions.py`.
- `EnforcementRunner` raises `EnforcementError` instead of `ValidationError` for policy gate checks.
- `EnforcementDecorator` catches `EnforcementError` and `PreflightError` and maps them to `EnforcementErrorOutput`.
- All unit tests pass.

**Dependencies:** Cycle 1


### Cycle 3: Cycle 3: DTO Schemas Segregation

**Goal:** Restructure success and error DTO models to adhere to Single Responsibility Principle (SRP) and delete redundant schemas.

**Tests:**
- tests/mcp_server/unit/test_presenter.py
- tests/mcp_server/assertion_helpers.py

**Success Criteria:**
- `BaseToolOutput` has `passed: bool = True` and no `success`/`error_message` fields.
- `BaseErrorOutput` has no `success`/`error_message` fields.
- `ValidationErrorOutput`, `EnforcementErrorOutput`, and `ConfigErrorOutput` inherit from `BaseErrorOutput` without message fields.
- `ExecutionErrorOutput` is the sole error DTO containing `error_message` and `traceback`.
- `CacheErrorOutput` is deleted.
- `ConfigErrorOutput` registered in schemas/`__init__.py`.

**Dependencies:** Cycle 2


### Cycle 4: Cycle 4: Dispatch & Presentation Alignment

**Goal:** Align server dispatch, presenter formatting lookup order, and boot-time template checks with the new DTO hierarchy.

**Tests:**
- tests/mcp_server/unit/test_server.py
- tests/mcp_server/unit/test_presenter.py
- tests/mcp_server/integration/test_pipeline_e2e.py

**Success Criteria:**
- `server.py` uses `isinstance(result_dto, BaseErrorOutput)` to flag `is_error=True` on `ToolResult`.
- `TextPresenter.present` uses the 3-level lookup hierarchy (error_code -> class template -> default failure).
- `validate_presentation_alignment` uses reflection over subclasses of `BaseErrorOutput` and checks error codes.
- The `default_failure_template` in `presentation.yaml` is updated to `'Failed: {error_type}'`.

**Dependencies:** Cycle 3


### Cycle 5: Cycle 5: Core Tools Refactoring

**Goal:** Convert all core tools to only return success DTOs and bubble up structured exceptions.

**Tests:**
- Individual unit tests for all 15+ refactored tools in `tests/mcp_server/unit/tools/`

**Success Criteria:**
- All 15+ tool classes in `mcp_server/tools/` refactored to bubble exceptions and remove try-except faal-DTO blocks.
- Logical tool failures (fixers, tests) return success DTOs with `passed=False`.
- Legacy compatibility attributes in `assertion_helpers.py` are cleaned up.
- Mypy and pyright type-checking pass 100% without global ignores.
- All tests pass.

**Dependencies:** Cycle 4

---

## Risks & Mitigation

- **Risk:** Blast radius of Cycle 1 test refactoring is large (250+ assertions).
  - **Mitigation:** Cycle 1 assertion helpers support a legacy compatibility layer to allow incremental test migration and testing.
- **Risk:** MCP JSON-RPC response compatibility with external clients.
  - **Mitigation:** Strictly adhere to the MCP protocol `isError` flag on the transport envelope, while separating visual outcomes via the `passed` field.
- **Risk:** Dynamic reflection fails if error subclasses are not imported at startup.
  - **Mitigation:** Import all subclasses of `BaseErrorOutput` in `mcp_server/schemas/__init__.py` to guarantee registration in the Python runtime.

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-27 | Agent | Initial draft |