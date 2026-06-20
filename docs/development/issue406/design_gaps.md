<!-- docs\development\issue406\design_gaps.md -->
<!-- template=design version=5827e841 created=2026-06-20T17:54Z updated= -->
# Design: Decorator Pipeline, Caching & Presentation Gaps Solution

**Status:** APPROVED  
**Version:** 1.0.0  
**Last Updated:** 2026-06-20

---

## Purpose

Design solutions to presentation, caching status, and interface packaging gaps in Issue 406.

---

## 1. Context & Requirements

### 1.1. Problem Statement

The presentation formatting and caching failure logic are leaked into the transport layer of server.py, and interfaces/__init__.py contains concrete implementations instead of purely facade exports.

### 1.2. Requirements

**Functional:**
- [ ] Move visual markdown formatting and fallback warnings from server.py to TextPresenter.
- [ ] Introduce CachePublication DTO to communicate caching results explicitly.
- [ ] Resolve Pydantic validation schemas dynamically from ValidationErrorOutput DTO.
- [ ] Refactor interfaces/__init__.py to serve as a pure facade by exporting separate interface files.

**Non-Functional:**
- [ ] Ensure 100% Pyright type safety with 0 ignores.
- [ ] Provide robust unit and integration test coverage for the refactored subsystems.

### 1.3. Constraints

- Must pass strict Pyright type checking.
- Must preserve JSON-RPC backward compatibility.
---

## 2. Design Options

### 2.1. Option A: Keep current inline validation schema fetching
* **Pros:**
  * Less files to touch.
* **Cons:**
  * Violates DIP and keeps `server.py` coupled to internal validation schema generation.

### 2.2. Option B: Dynamic ValidationErrorOutput.input_schema extraction (Selected)
* **Pros:**
  * Encapsulates schema generation in decorators, server only reads the clean DTO.
* **Cons:**
  * Requires updating validator decorator to expose input_schema.
---
## 3. Chosen Design

**Decision:** Refactor MCPServer to only orchestrate using clean DTO boundary classes, move formatting entirely to TextPresenter using template-driven fallbacks, and move concrete classes out of the interfaces init module.

**Rationale:** Maintains SRP, ISP, DIP, and Presentation Boundary, eliminating technical debt and hardcoded strings in code.

### 3.1. Detailed Specifications

#### 3.1.1. CachePublication DTO
* **Location:** `mcp_server/schemas/cache_publication.py` [NEW]
* **Definition:**
  ```python
  from pydantic import BaseModel, ConfigDict
  
  class CachePublication(BaseModel):
      model_config = ConfigDict(frozen=True)
      run_id: str | None = None
      success: bool = True
      error_code: str | None = None
  ```
* **Creator:** `IToolResponsePublisher.put()` signature is updated to return `CachePublication` instead of `str | None`. If a write failure occurs, it catches the exception and returns `CachePublication(run_id=None, success=False, error_code="write_failed")`.
* **Presenter Integration:** Both `IPresenter.present()` and `TextPresenter.present()` are updated in lock-step to accept `cache_pub: CachePublication | None = None` instead of `run_id: str | None`.

#### 3.1.2. Agnostic Transport Layer & URI Link Formatting
* **Orchestration:** `server.py` performs zero rendering or string formatting. All templates, SafeNoneFormatter imports, and URI link formatting (formerly L183–201) are moved completely to `TextPresenter.present()`.
* **Config Warning:** The fallback warning note is configured under `global.next_instruction_texts.cache_publication_failed` in `presentation.yaml`.

#### 3.1.3. Validation Schema Presentation
* **Schema Source:** The transport layer reads the schema directly from `result_dto.input_schema` (where `isinstance(result_dto, ValidationErrorOutput)`).
* **Protocol Formatting:** The transport layer appends the resource block (`schema://validation`) containing this schema directly to the MCP `CallToolResult` blocks.

#### 3.1.4. Interface Package Separation
* **Facading:** All concrete interfaces/classes (e.g. `PRStatus`, `IPRStatusReader`, `GateReport`, etc.) are moved out of `interfaces/__init__.py` to individual files under `mcp_server/core/interfaces/`.
* **Facade re-exports:** `interfaces/__init__.py` remains a pure facade that only re-exports these definitions, causing zero breaking changes to 66+ consumer files.

#### 3.1.5. Test Coupling Migration
* **Target:** `tests/mcp_server/unit/test_server.py` is in scope for Cycle 10.
* **Orchestration:** References accessing `server.enforcement_runner` or `server._workspace_root` are refactored to construct `ToolFactory` and mock dependencies independently of the `MCPServer` instance.
## Related Documentation
- **[docs/development/issue406/research_gaps.md][related-1]**

<!-- Link definitions -->

[related-1]: docs/development/issue406/research_gaps.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-20 | Agent | Initial draft |