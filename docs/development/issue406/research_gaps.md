<!-- docs\development\issue406\research_gaps.md -->
<!-- template=research version=8b7bb3ab created=2026-06-20T17:54Z updated= -->
# Research: Decorator Pipeline, Caching & Presentation Gaps

**Status:** APPROVED  
**Version:** 1.0.0  
**Last Updated:** 2026-06-20

---

## Problem Statement

The initial design and planning for Issue 406 left critical visual presentation, caching failure fallbacks, and interface packaging gaps unresolved, causing violations of SRP, ISP, and the Presentation Boundary.

## Research Goals

- Identify gaps between original design.md and codebase reality.
- Detail the missing validation schema presentation under the MCP protocol.
- Address the interface packaging issues in mcp_server/interfaces/__init__.py.

---

## Background

During the initial implementation of Issue 406, we identified several violations of ARCHITECTURE_PRINCIPLES.md, including formatting logic leaked into server.py, implicit caching status checks, and hardcoded fallback warning strings in Python. Additionally, the interface package __init__.py still contains concrete classes.

---

1. Presentation Leak: server.py directly formats cache links (L183–201), importing SafeNoneFormatter.
2. Caching Implicit Status: run_id is None is used by the presenter to check for cache failure.
3. Hardcoded warnings: fallback warning is in text_presenter.py instead of presentation.yaml.
4. Validation Resource Gap: the target design missed returning validation schemas via schema://validation.
5. Interface Packaging: concrete classes are still in interfaces/__init__.py.
---

Use clean Russian Doll decorators for execution. Introduce a frozen CachePublication DTO (encapsulating run_id, success, and error_code) returned by the publisher and passed explicitly to the presenter. Configure all user-facing fallback warnings in presentation.yaml. Move all URI-link formatting and SafeNoneFormatter calls out of server.py to TextPresenter. Extract concrete interface implementations from __init__.py into separate files.

---

## Expected Results

Clean transport layer in server.py, fully config-driven presenter, explicit cache publication status DTOs, and clean interfaces/__init__.py serving as a pure facade.

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-20 | Agent | Initial draft |