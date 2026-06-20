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

**Goal:** Extract concrete class and protocol definitions from `mcp_server/core/interfaces/__init__.py` into separate files, converting it into a pure re-export facade. Fix the TypeVar variance in `icore_tool.py` and add `@runtime_checkable` to `IPresenter`.

**In-Scope Files:**
* `mcp_server/core/interfaces/__init__.py`
* `mcp_server/core/interfaces/icore_tool.py`
* `mcp_server/core/interfaces/ipresenter.py`
* `mcp_server/core/interfaces/gate.py` [NEW]
* `mcp_server/core/interfaces/state.py` [NEW]
* `mcp_server/core/interfaces/ipr_status.py` [NEW]
* `mcp_server/core/interfaces/ipytest_runner.py` [NEW]
* `mcp_server/core/interfaces/git.py` [NEW]
* `mcp_server/core/interfaces/quality.py` [NEW]
* `mcp_server/core/interfaces/workflow.py` [NEW]
* `mcp_server/core/interfaces/context.py` [NEW]

**Migration Strategy (Strategy A: Move + Re-export):**
1. Extract classes to their dedicated sub-modules:
   * `gate.py`: `GateReport`, `GateViolation`, `IWorkflowGateRunner`
   * `state.py`: `IStateReader`, `IStateRepository`, `IStateReconstructor`
   * `ipr_status.py`: `PRStatus` (enum), `IPRStatusReader`, `IPRStatusWriter`
   * `ipytest_runner.py`: `IPytestRunner`
   * `git.py`: `IGitContextReader`, `IBranchParentReader`
   * `quality.py`: `IQualityStateRepository`
   * `workflow.py`: `IWorkflowStateMutator`
   * `context.py`: `IContextLoadedReader`, `IContextLoadedWriter`
2. Update `mcp_server/core/interfaces/__init__.py` to act as a pure facade containing only re-exports (e.g., `from mcp_server.core.interfaces.gate import GateReport as GateReport`). This ensures zero changes or breakage for the 66+ consumer files importing from `core.interfaces`.

**TDD RED Test:**
* Add a test in `tests/mcp_server/unit/core/interfaces/test_interface_imports.py` (new test file) that attempts to import `GateReport` directly from `mcp_server.core.interfaces.gate`. Verify it fails with `ImportError` before the file is created.

**Success Criteria & Incremental Gate:**
* TypeVar variance (`contravariant=True`/`covariant=True`) is removed from `icore_tool.py` (invariant TypeVars).
* `@runtime_checkable` is added to `ipresenter.py`.
* **Incremental Verification Gate:** The full unit test suite (`tests/mcp_server/unit/`) must be executed and pass after each individual class is moved and re-exported, before proceeding to move the next class, ensuring immediate isolation of any export regression.
* `interfaces/__init__.py` contains zero concrete class definitions.

### Cycle 9: Decoupled Visual Presentation & Config Fallbacks

**Goal:** Implement the frozen `CachePublication` DTO, update `IPresenter.present` and `TextPresenter.present` in lock-step, move fallback warnings to YAML, and move visual URI link formatting completely to `TextPresenter`.

**In-Scope Files:**
* `mcp_server/schemas/cache_publication.py` [NEW]
* `mcp_server/core/interfaces/ipresenter.py`
* `mcp_server/presenters/text_presenter.py`
* `mcp_server/core/interfaces/itool_response_cache.py`
* `mcp_server/state/response_cache.py`
* `tests/mcp_server/unit/core/interfaces/test_itool_response_cache_segregation.py`
* `mcp_server/server.py`
* `presentation.yaml`

**CachePublication DTO Specification (Pydantic BaseModel):**
```python
from pydantic import BaseModel, ConfigDict

class CachePublication(BaseModel):
    model_config = ConfigDict(frozen=True)
    run_id: str | None = None
    success: bool = True
    error_code: str | None = None
```
It is returned by `IToolResponsePublisher.put()` and passed to `presenter.present()`.
* **Breaking API Change Risk:** Updating the return type of `IToolResponsePublisher.put()` to `CachePublication` is a breaking API change that cascades to the concrete implementation `ResponseCacheManager.put()` and the unit test `test_itool_response_cache_segregation.py`. Both are marked in-scope for Cycle 9 to ensure concurrent refactoring and prevent regressions.

**TDD RED Test:**
* Write a test in `tests/mcp_server/unit/test_presenter.py` that calls `TextPresenter.present` with `cache_pub=CachePublication(success=False, error_code="write_failed")` and verify it formats the fallback JSON dump without tracebacks. This test should raise `TypeError` initially due to signature mismatch.

**Success Criteria:**
* `IPresenter.present()` and `TextPresenter.present()` signatures are updated in lock-step to accept `cache_pub: CachePublication | None = None`.
* Redundant try-except block around `put()` in `server.py` is removed.
* Falling back to JSON dump uses the `global.next_instruction_texts.cache_publication_failed` key in `presentation.yaml`.
* The visual URI link formatting logic (formerly L183–201 in `server.py`) is moved entirely to `TextPresenter.present()`.

### Cycle 10: Validation Schema Integration & Orchestration Clean-up

**Goal:** Clean up the `MCPServer` constructor by removing unused manager dependencies, refactor `handle_call_tool` to be linear, and read validation schemas dynamically from `ValidationErrorOutput.input_schema`.

**In-Scope Files:**
* `mcp_server/server.py`
* `mcp_server/bootstrap.py`
* `tests/mcp_server/unit/test_server.py`
* `tests/mcp_server/integration/test_pipeline_e2e.py`

**TDD RED Test:**
* Update `test_server.py` to instantiate `MCPServer` without `configs` and `managers` graphs. The test should raise `TypeError` or fail on constructor instantiation initially.

**Success Criteria:**
* `MCPServer.__init__` accepts only used parameters (`settings`, `tools`, `resources`, `presenter`, `publisher`).
* All `test_server.py` mock assertions accessing `server.enforcement_runner` or `server._workspace_root` are refactored to construct `ToolFactory` and mock dependencies independently of the `MCPServer` instance.
* `handle_call_tool` contains zero rendering, string formatting, or template lookups (100% linear flow).
* Validation schemas are read dynamically from `ValidationErrorOutput.input_schema` and appended as resources.
## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-20 | Agent | Initial draft |