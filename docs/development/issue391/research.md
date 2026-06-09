<!-- C:\temp\pgmcp\docs\development\issue391\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-09T17:15Z updated=2026-06-09T20:33Z -->
# Research: System Scan for Legacy Naming References

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-06-09

---

## Purpose

Document all legacy terms in the active codebase and documentation to prepare the standalone phase-gate-mcp server for release.

## Scope

**In Scope:**
Active documentation files and directories, mcp_server source files, and test files.

**Out of Scope:**
docs/development/ directory (treated as historical archive).

## Prerequisites

Read these first:
1. Issue #391 branch initialized
---

## Problem Statement

Identify all occurrences of legacy naming conventions (st3, simpletrader, s1mpletraderv3, and variants) across active documentation and the codebase to ensure the pgmcp server is ready for its first release.

## Research Goals

- Scan active documentation directories: docs/mcp_server/, docs/reference/, docs/coding_standards/, docs/setup/.
- Scan codebase directories: mcp_server/, tests/, .phase-gate/.
- Identify affected boundaries and formulate policy options for renaming, cleanup, and archival.

---

## Background

The repository was recently split from the SimpleTraderV3 backend into a standalone phase-gate-mcp server. The configuration directory was renamed from .st3/ to .phase-gate/, but legacy references remain in documentation and tests.

---

## Findings

1. **Codebase (mcp_server/)**: 0 occurrences of 'st3' or 'simpletrader'. The production codebase is completely clean.
2. **Configuration (.phase-gate/)**: 0 occurrences of legacy terms.
3. **Tests (tests/)**: ~40 occurrences of 'st3' or 'simpletrader' in fixtures, variables, and comments (e.g., test_workflow_cycle_e2e.py). These are functional test utilities that mock old paths or use variable names like _ST3_CONFIG.
4. **Active Documentation (docs/)**:
   - docs/mcp_server/ARCHITECTURE.md: Multiple references to 'ST3 Workflow MCP Server' and 'st3://' resource URIs.
   - docs/mcp_server/RESOURCES.md: Defines st3:// URIs (should be pgmcp://).
   - docs/mcp_server/TOOLS.md: References .st3/ state files.
   - docs/mcp_server/USER_GUIDE.md: References /path/to/SimpleTraderV3.
   - docs/reference/mcp/mcp_vision_reference.md: Vision doc containing 'ST3 Workflow MCP Server' and .st3/ configuration paths.
   - docs/coding_standards/README.md: References .st3/quality.yaml and .st3/artifacts.yaml.

---

## Strategy Options & Policy Analysis

### Boundary 1: Test Code Naming (tests/)
- **Option A: Full Refactor of Legacy Names**: Rename all variables (e.g., `_ST3_CONFIG` -> `_PGMCP_CONFIG`), test function names, and mock directories (e.g., `.st3` -> `.phase-gate` in e2e tests).
  - *Pros*: Completely clean codebase, no legacy terms left, uniform developer experience.
  - *Cons*: Risk of breaking e2e tests that rely on hardcoded paths.
  - *Risk Mitigation*: Run full `pytest` suite locally after refactoring.
- **Option B: Preserve Legacy Names in Tests**: Keep test code variables and comments as they are, only updating paths necessary for functional operation.
  - *Pros*: Minimizes risk of test suite regression.
  - *Cons*: Contaminates test codebase with outdated terminology.

**Recommendation**: Option A (Full Refactor of Legacy Names).

### Boundary 2: Deprecated Design Documents (docs/archive/)
- **Option A: Delete Deprecated Documents**: Remove `docs/archive/` entirely.
  - *Pros*: Keeps the repository clean and prevents developer confusion.
  - *Cons*: Loss of historical context on deprecated design iterations.
- **Option B: Retain and Mark as Deprecated**: Retain the files but update headers to indicate deprecation.
  - *Pros*: Historical context remains accessible in the tree.
  - *Cons*: Increases clutter in the repository.

**Recommendation**: Option A (Delete Deprecated Documents).

### Boundary 3: Historical Issue Artifacts (docs/development/ and development/archive/)
- **Option A: Move to a Dedicated Archive Branch**: Move historical issue directories to a separate Git branch (e.g., `archive/historical-issues`) and delete them from the `main` branch.
  - *Pros*: Retains all historical issue artifacts in the repository's history, but completely declutters the `main` branch.
  - *Cons*: Ontwikkelaars must switch branches to view past issue artifacts.
- **Option B: Retain on main Branch**: Keep all historical directories on `main`.
  - *Pros*: Immediate access to past issue artifacts.
  - *Cons*: Bloats the codebase with hundreds of historical markdown files.

**Recommendation**: Option A (Move to a Dedicated Archive Branch).

---

## Approved Strategy

### Boundary: Active Documentation Naming (`docs/`)
- **Selected Strategy**: Clean Break
- **Rationale**: Ensures all active documents reflect the current name `pgmcp` / `phase-gate` and standard `pgmcp://` URIs for the first release.
- **Constraints**: Excludes historical archive directories (`docs/development/` and `docs/archive/`).

### Boundary: Test Code Naming (`tests/`)
- **Selected Strategy**: Clean Break
- **Rationale**: Removes all legacy naming references (e.g., `_ST3_CONFIG` -> `_PGMCP_CONFIG`, `.st3` -> `.phase-gate` mock paths) to ensure codebase consistency.
- **Constraints**: Test suite must remain green; validation required.

### Boundary: Deprecated Design Documents (`docs/archive/`)
- **Selected Strategy**: Clean Break
- **Rationale**: Completely delete `docs/archive/` from the active codebase for the first release to avoid developer confusion.
- **Constraints**: Deletion is permanent on the `main` branch, but preserved in Git history.

### Boundary: Historical Issue Artifacts (`docs/development/` and `development/archive/`)
- **Selected Strategy**: Temporary Bridge / Migration
- **Rationale**: Keep historical issue artifacts archived on a dedicated branch (`archive/historical-issues`) and remove them from the `main` branch before the final release.
- **Constraints**: Defer actual removal from `main` to the final cleanup/release issue, keeping them on the active branch during development of this issue.

---

## Related Documentation
- **[docs/coding_standards/DOCUMENTATION_STANDARD.md][related-1]**

<!-- Link definitions -->

[related-1]: docs/coding_standards/DOCUMENTATION_STANDARD.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-09 | Agent | Initial draft with strategy analysis and approved strategy |
