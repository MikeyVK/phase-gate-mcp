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

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Agnostic Transport Layer | server.py delegates all rendering and fallback warnings to TextPresenter. |
| Explicit CachePublication status | Conveys write results explicitly to the presenter to avoid magic note scanning. |
| Interface package separation | Move all concrete classes from interfaces/__init__.py to individual modules to keep the facade clean. |

## Related Documentation
- **[docs/development/issue406/research_gaps.md][related-1]**

<!-- Link definitions -->

[related-1]: docs/development/issue406/research_gaps.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-20 | Agent | Initial draft |