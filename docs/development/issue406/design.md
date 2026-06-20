<!-- docs\development\issue406\design.md -->
<!-- template=design version=5827e841 created=2026-06-20T17:53Z updated= -->
# Design: Russian Doll Decorator Pipeline, Caching & Interface Refactor

**Status:** APPROVED  
**Version:** 1.1.0  
**Last Updated:** 2026-06-20

---

## Purpose

Design the Russian Doll Decorator Pipeline, Caching & Interface Refactor for Issue 406.

---

## 1. Context & Requirements

### 1.1. Problem Statement

The initial design for Issue 406 failed to cleanly separate transport orchestration from visual presentation and cache status monitoring, leading to God-like dependencies in server.py, hardcoded warnings in presenters, and concrete classes in interfaces/__init__.py.

### 1.2. Requirements

**Functional:**
- [ ] Move all visual rendering, formatting, and markdown generation to TextPresenter.
- [ ] Construct a clean, linear, exception-free transport flow in MCPServer.handle_call_tool.
- [ ] Incorporate an explicit CachePublication DTO for cache status.
- [ ] Append validation schemas dynamically from the DTO rather than inspecting tools.
- [ ] Remove all concrete class definitions from mcp_server/interfaces/__init__.py, turning it into a pure re-export facade.

**Non-Functional:**
- [ ] Pass Pyright type-checking with zero ignores.
- [ ] Maintain 100% backward compatibility with standard JSON-RPC and MCP protocols.
- [ ] Verify correctness using clean unit and E2E integration tests.

### 1.3. Constraints

- Must preserve standard JSON-RPC and MCP tool-call protocols.
- Must pass strict Pyright type checks with zero ignores.
---

## 2. Design Options

### 2.1. Option A: 



**Pros:**
- ✅ F
- ✅ i
- ✅ t
- ✅ s
- ✅  
- ✅ o
- ✅ l
- ✅ d
- ✅  
- ✅ s
- ✅ t
- ✅ r
- ✅ u
- ✅ c
- ✅ t
- ✅ u
- ✅ r
- ✅ e
- ✅ ,
- ✅  
- ✅ r
- ✅ e
- ✅ q
- ✅ u
- ✅ i
- ✅ r
- ✅ e
- ✅ s
- ✅  
- ✅ l
- ✅ e
- ✅ s
- ✅ s
- ✅  
- ✅ r
- ✅ e
- ✅ f
- ✅ a
- ✅ c
- ✅ t
- ✅ o
- ✅ r
- ✅ i
- ✅ n
- ✅ g
- ✅ .

**Cons:**
- ❌ V
- ❌ i
- ❌ o
- ❌ l
- ❌ a
- ❌ t
- ❌ e
- ❌ s
- ❌  
- ❌ S
- ❌ R
- ❌ P
- ❌  
- ❌ a
- ❌ n
- ❌ d
- ❌  
- ❌ P
- ❌ r
- ❌ e
- ❌ s
- ❌ e
- ❌ n
- ❌ t
- ❌ a
- ❌ t
- ❌ i
- ❌ o
- ❌ n
- ❌  
- ❌ B
- ❌ o
- ❌ u
- ❌ n
- ❌ d
- ❌ a
- ❌ r
- ❌ y
- ❌ ,
- ❌  
- ❌ l
- ❌ e
- ❌ a
- ❌ v
- ❌ e
- ❌ s
- ❌  
- ❌ h
- ❌ a
- ❌ r
- ❌ d
- ❌ c
- ❌ o
- ❌ d
- ❌ e
- ❌ d
- ❌  
- ❌ u
- ❌ s
- ❌ e
- ❌ r
- ❌ -
- ❌ f
- ❌ a
- ❌ c
- ❌ i
- ❌ n
- ❌ g
- ❌  
- ❌ s
- ❌ t
- ❌ r
- ❌ i
- ❌ n
- ❌ g
- ❌ s
- ❌  
- ❌ i
- ❌ n
- ❌  
- ❌ P
- ❌ y
- ❌ t
- ❌ h
- ❌ o
- ❌ n
- ❌ .

### 2.2. Option B: 



**Pros:**
- ✅ P
- ✅ u
- ✅ r
- ✅ e
- ✅  
- ✅ s
- ✅ e
- ✅ p
- ✅ a
- ✅ r
- ✅ a
- ✅ t
- ✅ i
- ✅ o
- ✅ n
- ✅  
- ✅ o
- ✅ f
- ✅  
- ✅ c
- ✅ o
- ✅ n
- ✅ c
- ✅ e
- ✅ r
- ✅ n
- ✅ s
- ✅ ,
- ✅  
- ✅ 1
- ✅ 0
- ✅ 0
- ✅ %
- ✅  
- ✅ c
- ✅ o
- ✅ n
- ✅ f
- ✅ i
- ✅ g
- ✅ -
- ✅ d
- ✅ r
- ✅ i
- ✅ v
- ✅ e
- ✅ n
- ✅  
- ✅ u
- ✅ s
- ✅ e
- ✅ r
- ✅ -
- ✅ f
- ✅ a
- ✅ c
- ✅ i
- ✅ n
- ✅ g
- ✅  
- ✅ t
- ✅ e
- ✅ x
- ✅ t
- ✅ ,
- ✅  
- ✅ c
- ✅ l
- ✅ e
- ✅ a
- ✅ n
- ✅  
- ✅ f
- ✅ a
- ✅ c
- ✅ a
- ✅ d
- ✅ e
- ✅  
- ✅ p
- ✅ a
- ✅ c
- ✅ k
- ✅ a
- ✅ g
- ✅ i
- ✅ n
- ✅ g
- ✅ .

**Cons:**
- ❌ R
- ❌ e
- ❌ q
- ❌ u
- ❌ i
- ❌ r
- ❌ e
- ❌ s
- ❌  
- ❌ r
- ❌ e
- ❌ f
- ❌ a
- ❌ c
- ❌ t
- ❌ o
- ❌ r
- ❌ i
- ❌ n
- ❌ g
- ❌  
- ❌ s
- ❌ e
- ❌ v
- ❌ e
- ❌ r
- ❌ a
- ❌ l
- ❌  
- ❌ f
- ❌ i
- ❌ l
- ❌ e
- ❌ s
- ❌  
- ❌ a
- ❌ n
- ❌ d
- ❌  
- ❌ t
- ❌ e
- ❌ s
- ❌ t
- ❌  
- ❌ s
- ❌ u
- ❌ i
- ❌ t
- ❌ e
- ❌ s
- ❌ .
---

## 3. Chosen Design

**Decision:** Implement a completely decoupled transport orchestrator in server.py, a config-driven presentation fallback system in TextPresenter, explicit CachePublication DTOs, and a pure facade interfaces package.

**Rationale:** Enforces SRP, ISP, DIP, and the Presentation Boundary (§15 of ARCHITECTURE_PRINCIPLES.md), removing code leaks and ensuring clean separation of concerns.

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Agnostic Transport Layer | server.py is a pure coordinator, delegating all formatting and visual layout to TextPresenter. |
| Explicit CachePublication DTO | Conveys caching outcomes explicitly to the presenter to avoid magic note scanning and implicit checks. |
| Config-Driven Warnings | Moves user-facing warning texts to presentation.yaml under next_instruction_texts (Config-First). |
| Facade Interfaces Package | Moves concrete implementations out of interfaces/__init__.py to individual files to keep the package clean and facade-only. |

## Related Documentation
- **[docs/development/issue406/research.md][related-1]**

<!-- Link definitions -->

[related-1]: docs/development/issue406/research.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.1.0 | 2026-06-20 | Agent | Initial draft |