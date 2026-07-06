<!-- docs\development\issue420\research.md -->
<!-- template=research version=8b7bb3ab created=2026-07-06T05:52Z updated= -->
# Research: Deferred Release Assets and Template Bootstrap

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-07-06

## Prerequisites

Read these first:
1. Issue #420
2. docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
3. docs/coding_standards/DOCUMENTATION_STANDARD.md
4. docs/reference/mcp/release-assets-procedure.md
---

## Problem Statement

Clean repository checkouts contain the tracked .pgmcp/config folder but miss the untracked .pgmcp/templates directory. The current workspace initialization (pgmcp --init) crashes if .pgmcp exists, preventing template bootstrap. Additionally, the release packaging automation and manifest synchronization specified in release-assets-procedure.md are deferred, requiring automated sync from the docs/agents/ Single Source of Truth to mcp_server/assets/ during wheel compilation.

## Research Goals

- Support template initialization via pgmcp --init when .pgmcp exists but .pgmcp/templates is missing.
- Eliminate templates directory triplication by removing mcp_server/scaffolding/templates and updating the test suite to use resolved settings.
- Implement automated build-time copy/sync of release-bound assets to mcp_server/assets/ on release builds using release_manifest.yaml.
- Establish a secure development isolation setup where the active running server instance operates from a packaged wheel, separated from the active development codebase.

---

## Approved Strategy

Boundary: Default Configuration Root & Workspace Initialization.
Policy: Adapt pgmcp --init to check for missing .pgmcp/templates instead of aborting when the .pgmcp directory exists. Use shutil.copytree(..., dirs_exist_ok=True) to populate missing assets.

Boundary: Templates Source of Truth.
Policy: Remove the duplicate mcp_server/scaffolding/templates directory. All unit and integration tests must load templates from Settings-resolved paths or test-isolated temporary paths, keeping .pgmcp/templates as the active dev environment SSOT.

Boundary: Release Packaging & Automation.
Policy: Implement a build script/pre-build step that parses release_manifest.yaml and copies the specified assets to mcp_server/assets/ prior to wheel building. Exclude dev-specific sync mechanisms from production runtime code.

---

## Expected Results

1. Clean checkouts of the repository can be initialized via pgmcp --init to restore templates under .pgmcp/templates.
2. mcp_server/scaffolding/templates is deleted and all tests pass using the settings-based template paths.
3. Bundled package assets (mcp_server/assets/) are populated automatically during package packaging by a build-time pre-build sync script.
4. The running instance of the MCP server can be installed and run from a packaged wheel independently of the active development repository.

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-06 | Agent | Initial draft |