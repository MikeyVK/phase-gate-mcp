<!-- docs\development\issue406\planning_gaps.md -->
<!-- template=planning version=130ac5ea created=2026-06-20T17:54Z updated= -->
# Planning: Decorator Pipeline, Caching & Presentation Gaps Cycles

**Status:** APPROVED  
**Version:** 1.0.0  
**Last Updated:** 2026-06-20

---

## Summary

This planning document outlines the additional TDD cycles (Cycles 8, 9, and 10) to address presentation, caching status, and interface packaging gaps for Issue 406.

---

## TDD Cycles


### Cycle 8: Interface Packaging Refactor (Facade init)

**Goal:** Extract concrete classes from mcp_server/interfaces/__init__.py into separate files, converting it into a pure re-export facade.

**Tests:**
- Verify that quality gates and imports check pass on all interface files.

**Success Criteria:**
- All concrete classes moved to individual files in core/interfaces/.
- interfaces/__init__.py has 0 lines of implementation logic and acts purely as a facade.



### Cycle 9: Decoupled Visual Presentation & Config Fallbacks

**Goal:** Implement CachePublication DTO, update TextPresenter to accept it, and load fallback warnings from presentation.yaml.

**Tests:**
- tests/mcp_server/unit/test_presenter.py

**Success Criteria:**
- CachePublication DTO is introduced.
- TextPresenter.present uses CachePublication instead of run_id is None.
- Fallback warnings are fully config-driven via presentation.yaml.



### Cycle 10: Validation Schema Integration & Orchestration Clean-up

**Goal:** Clean up MCPServer constructor parameters and refactor handle_call_tool to a linear 5-step orchestrator that dynamically reads the validation schema from the DTO.

**Tests:**
- tests/mcp_server/unit/test_server.py
- tests/mcp_server/integration/test_pipeline_e2e.py

**Success Criteria:**
- MCPServer constructor is stripped of unused manager dependencies.
- handle_call_tool is linear with 0 rendering/formatting code.
- Validation schemas are dynamically returned from ValidationErrorOutput.input_schema.


## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-20 | Agent | Initial draft |