<!-- c:\temp\pgmcp\docs\development\issue402\response_cache_design.md -->
<!-- template=design version=5827e841 created=2026-06-13T18:36Z updated= -->
# Design — Response Cache & Resource Management

**Status:** DRAFT  
**Version:** 1.1  
**Last Updated:** 2026-06-14

---

## Purpose

Establish the architectural and data-flow design for the in-memory Response Cache and dynamic Resource Management in the MCP server, ensuring alignment with CQS, SRP, and DIP.

## Scope

**In Scope:**
Design of IToolResponseCache, ResponseCacheManager, resource URI conventions, Pydantic DTO cache contracts, and token minimization strategy.

**Out of Scope:**
Changing the client-side MCP client execution or UI, and caching of non-DTO state or persistent data.

## Prerequisites

Read these first:
1. docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
2. docs/development/issue402/research_autofix.md
---

## 1. Context & Requirements

### 1.1. Problem Statement

To expose rich structured JSON output from MCP tools to the model without bloating the standard text fallback or violating client-side content constraints, we need a reliable, generic in-memory cache on the server that stores tool execution outputs and exposes them dynamically as read-only MCP resources.

### 1.2. Requirements

**Functional:**
- [ ] Provide a centralized in-memory cache service (ResponseCacheManager)
- [ ] Support caching of any StructuredTool output DTO keyed by its Resource URI
- [ ] Support dynamic resource lookup via the server read_resource handler
- [ ] Implement LRU or FIFO eviction logic to prevent memory leaks

**Non-Functional:**
- [ ] Comply with SOLID (SRP, DIP, OCP) and CQS
- [ ] Ensure cached data is immutable (frozen Pydantic DTOs)
- [ ] Minimize LLM token consumption by returning compact, white-space stripped JSON on resource reads

### 1.3. Constraints

- Must conform to Command-Query Separation (CQS) by treating resource lookup as a read-only query.
- Must conform to DIP: dependency injected via constructor at composition root.
---

## 2. Design Options

### 2.1. Option A: Option A: Ad-hoc tool/manager caching

Each tool class or tool manager (e.g. QAManager, GitManager) handles its own caching dictionary inside the class.

**Pros:**
- ✅ Simple to implement for a single tool

**Cons:**
- ❌ Violates SRP (managers mix logic and caching)
- ❌ Violates OCP (adding caching to a new tool requires code changes to the tool/manager)
- ❌ Hard to enforce global memory limits or consistent eviction rules

### 2.2. Option B: Option B: Gecentraliseerde ResponseCacheManager (Recommended)

A single cache manager class injected at composition root that provides a generic read-write interface for all tool execution caches.

**Pros:**
- ✅ Respects SRP, DIP, and OCP
- ✅ Enforces consistent eviction policies (LRU/FIFO)
- ✅ Keeps tool logic clean

**Cons:**
- ❌ Requires declaring a new interface and registering it at startup
---

## 3. Chosen Design

**Decision:** Implement a centralized `ResponseCacheManager` that implements a narrow `IToolResponseCache` interface, alongside a single, uniform `CachedResponseResource` provider matching the URI scheme `pgmcp://cache/runs/{run_id}`. The cache manager stores frozen Pydantic DTO instances keyed by the dynamic resource URI of each tool execution run, evicting the oldest entries when the cache exceeds a max_size limit using `OrderedDict`.

**Rationale:** A centralized cache manager separates caching logic from tool logic (SRP) and the server interface (DIP). Storing frozen DTOs maintains type-safety and contract consistency (CQS). Introducing a uniform `CachedResponseResource` ensures that any future tool can cache its output without requiring new resource classes (OCP/DRY), and serializing to compact JSON with `exclude_none=True` minimizes token consumption.

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Use Uniform URI `pgmcp://cache/runs/{run_id}` | Provides a consistent and generic naming convention for all cached tool outputs, avoiding tool-specific resource classes. |
| Use Resource URI as the cache key | It naturally maps the tool execution output to the endpoint requested by the model during a `read_resource` call, avoiding custom key mapping logic. |
| Store frozen Pydantic DTOs directly | It guarantees that the cached content is validated at the boundary and cannot be mutated afterwards (CQS compliance). |
| Apply FIFO/LRU eviction inside ResponseCacheManager using OrderedDict | Keeps the eviction policy encapsulated (SRP) and ensures memory consumption remains bounded. |
| Serialize to compact, whitespace-stripped JSON with exclude_none=True during read | Minimizes token counts for LLM consumption while preserving structure. |

### 3.2. Uniform Resource Provider Implementation

The `CachedResponseResource` class will inherit from `BaseResource` and be registered in `self.resources` at startup:

```python
class CachedResponseResource(BaseResource):
    """Uniform resource provider for cached tool outputs."""

    uri_pattern = "pgmcp://cache/runs/.*"
    description = "Cached tool execution outputs"
    mime_type = "application/json"

    def __init__(self, cache: IToolResponseCache) -> None:
        self._cache = cache

    def matches(self, uri: str) -> bool:
        return bool(re.match(r"^pgmcp://cache/runs/[\w-]+$", uri))

    async def read(self, uri: str) -> str:
        dto = self._cache.get(uri)
        if not dto:
            raise ValueError(f"No cached data found for URI: {uri}")
        return dto.model_dump_json(exclude_none=True)
```

---
## 4. Open Questions

| Question | Options | Status |
|----------|---------|--------|
| What is the optimal default max_size for the in-memory cache? (Proposed: 50 runs) |  |  |
## Related Documentation
- **[docs/development/issue402/design.md][related-1]**
- **[docs/development/issue402/auto_fix_design.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/development/issue402/design.md
[related-2]: docs/development/issue402/auto_fix_design.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-13 | Agent | Initial draft |
| 1.1 | 2026-06-14 | Agent | Updated to reflect the removal of json_reference entity and the transition to list-based next_instructions in the presentation layer. |
