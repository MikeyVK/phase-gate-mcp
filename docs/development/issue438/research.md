<!-- c:\temp\pgmcp\docs\development\issue438\research.md -->
<!-- template=research version=8b7bb3ab created=2026-07-20T20:17Z updated= -->
# Dynamic State File Versioning Research

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-07-20

---

## Purpose

Define the error boundaries and versioning strategy for dynamic state files.

## Scope

**In Scope:**
Refactoring exception structures of state files, updating the decorator-level error mapping, removing silent reconstructs in PhaseStateEngine, implementing file backup-on-mismatch actors, and refactoring bootstrapper version checking logic.

**Out of Scope:**
Implementing python-level data schema migration functions (e.g. mapping JSON fields between versions dynamically).

## Prerequisites

Read these first:
1. Familiarity with the Russian Doll Decorator Pipeline (Issue #406 / #410)
2. Understanding of state repositories (state_repository.py, quality_state_repository.py, project_manager.py)
---

## Problem Statement

Dynamic state files (state.json, deliverables.json, quality_state.json) lack schema versioning and consistent boundary-level exception mapping, causing inconsistent behavior (e.g. silent reconstruction fallbacks, raw JSONDecodeError crashes, and [BUG] tracebacks in error logs).

## Research Goals

- Analyze the actual tool-level boundary consequences of missing or corrupt state files.
- Establish a clean exception-mapping model using the existing Russian Doll Decorator Pipeline.
- Evaluate version detection timing and dynamic state migration versus defensive backup-and-reset policies.
- Decouple workspace version validation logic from the ServerBootstrapper composition root.

---

## Background

During Issue #289 and #406, core tools were refactored to bubble up exceptions to decorators. However, state repository error boundaries were not fully aligned, causing domain errors to bubble as raw exceptions that trigger unhandled traceback logging.

---

## Findings

We mapped tool behaviors when state files go missing or are corrupt. We found that state.json lacks SSOT enforcement due to a silent reconstruction fallback. We verified that the ToolErrorHandlerDecorator handles ConfigError cleanly, mapping it to ConfigErrorOutput, while raw Exceptions trigger [BUG] tracebacks. We also confirmed that ConfigLoader validates static configurations during bootstrap, while dynamic files are loaded lazy at runtime.

---

## Approved Strategy

1. Sequence error-handling uniformization before version checking and backup logic.
2. Remove the silent reconstruction fallback in PhaseStateEngine, enforcing state.json as SSOT.
3. Subclass StateNotFoundError and other state failures from ConfigError so they are cleanly mapped by the decorator pipeline without traceback noise.
4. Implement version checking at load-time (runtime) in repositories using a central validator service, triggering a backup-and-reset on mismatch.

---

## Expected Results

Missing or corrupted state files will cleanly return presented failure markdown text to the agent instead of generating raw crashes or tracebacks. Mismatched schemas will result in backup files (.bak) and guide the agent/user to re-initialize the state using initialize_project or save_planning_deliverables.

## Related Documentation
- **[mcp_server/core/decorators/tool_error_handler_decorator.py][related-1]**
- **[mcp_server/core/error_handling.py][related-2]**
- **[mcp_server/managers/state_repository.py][related-3]**
- **[docs/development/archive/issue289/tools_error_mapping_research.md][related-4]**

<!-- Link definitions -->

[related-1]: mcp_server/core/decorators/tool_error_handler_decorator.py
[related-2]: mcp_server/core/error_handling.py
[related-3]: mcp_server/managers/state_repository.py
[related-4]: docs/development/archive/issue289/tools_error_mapping_research.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-20 | Agent | Initial draft |