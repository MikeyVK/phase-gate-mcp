<!-- docs\development\issue413\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-26T18:20Z updated= -->
# Redesign Error DTOs & Segregate BaseToolOutput

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-26

---

## Summary

Refactor the error handling schema on the MCP server to separate success and error concerns. Remove success and error_message from BaseToolOutput, establish BaseErrorOutput, clean up redundant DTOs, refactor tools to raise exceptions instead of returning error DTOs, update the decorator pipeline to handle exception mapping, and update the test suite to use type-safe assertions.

---

## TDD Cycles


### Cycle 1: C_SCHEMA.1

**Goal:** Refactor error and tool output schemas in mcp_server/schemas/

**Tests:**
- tests/schemas/test_error_outputs.py

**Success Criteria:**
- BaseToolOutput does not have success or error_message fields
- BaseErrorOutput is defined with a read-only is_error property returning True
- ValidationErrorOutput, EnforcementErrorOutput, ConfigErrorOutput, and ExecutionErrorOutput inherit from BaseErrorOutput and lack success/error_message fields
- CacheErrorOutput is deleted entirely
- Pydantic validation and static typing pass on the new schema definition



### Cycle 2: C_SERVER.2

**Goal:** Update server and presenter layers to use type-safe status checking

**Tests:**
- tests/test_server.py
- tests/test_text_presenter.py

**Success Criteria:**
- server.py checks isinstance(result, BaseErrorOutput) instead of getattr(..., 'success')
- TextPresenter uses isinstance(result, BaseErrorOutput) for conditional rendering logic
- MCP is_error flag is set correctly based on BaseErrorOutput instance status



### Cycle 3: C_TOOLS.3

**Goal:** Refactor core tools to raise exceptions instead of returning error DTOs

**Tests:**
- tests/tools/test_test_tools.py
- tests/tools/test_workflow_tools.py

**Success Criteria:**
- Core tools only return their success DTO type in signatures and execution paths
- Any tool failures raise custom exceptions (ValidationError, PreflightError, ConfigError, etc.) instead of returning error DTOs



### Cycle 4: C_DECORATORS.4

**Goal:** Refactor the decorator pipeline to map exceptions to error DTOs

**Tests:**
- tests/decorators/test_tool_error_handler_decorator.py
- tests/decorators/test_input_validation_decorator.py
- tests/decorators/test_enforcement_decorator.py

**Success Criteria:**
- ToolErrorHandlerDecorator, InputValidationDecorator, and EnforcementDecorator catch core exceptions and return the mapped BaseErrorOutput subclass DTOs



### Cycle 5: C_TESTS.5

**Goal:** Refactor all test assertions in the test suite asserting on legacy fields

**Tests:**
- All pytest tests in tests/

**Success Criteria:**
- Legacy assertions checking .success or .error_message on error outputs are removed or refactored to check type / structured properties
- All tests pass successfully


## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-26 | Agent | Initial draft |