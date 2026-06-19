<!-- docs\development\issue406\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-19T21:16Z updated= -->
# Planning: Russian Doll Decorator Pipeline for Exception Mapping

**Status:** DRAFT  
**Version:** 1.0.0  
**Last Updated:** 2026-06-19

---

## Summary

Refactor the monolithic exception mapping and validation bridge in server.py into a decoupled Russian Doll decorator pipeline with CQRS cache segregation, linear transport orchestration, and graceful presentation fallbacks.

---

## TDD Cycles


### Cycle 1: Interfaces & Type Foundation (Cycle 1)

**Goal:** Introduce new ITool/ICoreTool interfaces under mcp_server/core/interfaces/, rename old ITool to ILegacyTool in tools/base.py, and update ToolErrorOutput signatures

**Tests:**
- tests/mcp_server/unit/test_presenter.py
- tests/mcp_server/unit/test_server.py

**Success Criteria:**
New interfaces compile, legacy imports resolved using ILegacyTool, DTO constructors updated in tests



### Cycle 2: Decorator Pipeline (Cycle 2)

**Goal:** Implement ToolErrorHandlerDecorator, InputValidationDecorator, and EnforcementDecorator under mcp_server/core/decorators/

**Tests:**
- tests/mcp_server/unit/decorators/test_pipeline_decorators.py

**Success Criteria:**
Decorators handle raw validation, enforcement pre/post checks, and catch-all exception logging



### Cycle 3: CQRS Cache Segregation (Cycle 3)

**Goal:** Segregate cache interfaces to publisher/reader and implement concrete ResponseCacheManager put/get updates for run_id

**Tests:**
- tests/mcp_server/unit/core/interfaces/test_itool_response_cache_segregation.py
- tests/mcp_server/unit/tools/test_autofix_tool.py

**Success Criteria:**
ResponseCacheManager put returns run_id instead of URI, and get deserializes to target DTO class



### Cycle 4: Presenter Engine & Fallback Unit Tests (Cycle 4)

**Goal:** Implement IPresenter interface and TextPresenter fallback with Option A traceback stripping

**Tests:**
- tests/mcp_server/unit/test_presenter.py

**Success Criteria:**
TextPresenter strips traceback and appends warning/JSON block when run_id is None in unit tests



### Cycle 5: ToolFactory & Bootstrap Prep (Cycle 5)

**Goal:** Implement ToolFactory composition root under mcp_server/core/tool_factory.py and configure Ruff T20 linting

**Tests:**
- tests/mcp_server/unit/core/test_tool_factory.py

**Success Criteria:**
ToolFactory correctly wraps core tools, pyproject.toml and quality.yaml enforce T20 print checks



### Cycle 6: Tool-laag Migratie (Cycle 6a)

**Goal:** Migrate all tool endpoints to ICoreTool and retire ILegacyTool and ToolExecutionEnvelope

**Tests:**
- tests/mcp_server/unit/tools/test_cycle_tools.py
- tests/mcp_server/unit/tools/test_project_tools.py

**Success Criteria:**
All ~50 tool endpoints migrated to use typed inputs/outputs; legacy base tool files removed



### Cycle 7: Transport Orchestratie & E2E (Cycle 6b)

**Goal:** Refactor server.py handle_call_tool, retire ResourcePublishingDecorator, and add E2E integration test

**Tests:**
- tests/mcp_server/integration/test_pipeline_e2e.py

**Success Criteria:**
Clean linear flow coordinates pipeline execution, cache publishing, and markdown presentation on success and failure paths


## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-19 | Agent | Initial draft |