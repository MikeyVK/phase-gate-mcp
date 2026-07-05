<!-- docs\development\issue385\documentation.md -->
<!-- template=generic_doc version=43c84181 created=2026-07-05T13:53Z updated= -->
# Documentation Report: Package Identity Rename and Init Bootstrap

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-07-05

---

## Purpose

Document the documentation scan results, active repository updates, and reviewed pages for Issue #385.

## Prerequisites

Read these first:
1. docs/development/issue385/validation.md
---

## Summary

Renamed the default package configuration and state directory from .phase-gate to .pgmcp, implemented pgmcp --init bootstrap command, removed legacy transition bridges, and comprehensively synchronized agent and developer documentation.

---

## Key Changes

- Rename default configuration path from .phase-gate to .pgmcp
- Remove transitional compatibility fallbacks in Settings, proxy, and test_support
- Add pgmcp --init CLI command to initialize workspace-local assets
- Standardize workspace-local config setup as standard Antigravity practice
- Fix stale links to TDD_WORKFLOW.md and GIT_WORKFLOW.md in quality and style guides




## Related Documentation
- **[docs/setup/README.md][related-1]**
- **[docs/mcp_server/README.md][related-2]**
- **[docs/mcp_server/USER_GUIDE.md][related-3]**
- **[docs/mcp_server/ARCHITECTURE.md][related-4]**
- **[docs/reference/mcp/server-configuration.md][related-5]**
- **[docs/reference/mcp/config-loading-architecture.md][related-6]**
- **[docs/reference/mcp/mcp_vision_reference.md][related-7]**
- **[docs/reference/mcp/copilot-agent-instructions-model.md][related-8]**
- **[docs/coding_standards/README.md][related-9]**
- **[docs/coding_standards/QUALITY_GATES.md][related-10]**
- **[docs/reference/mcp/release-assets-procedure.md][related-11]**

<!-- Link definitions -->

[related-1]: docs/setup/README.md
[related-2]: docs/mcp_server/README.md
[related-3]: docs/mcp_server/USER_GUIDE.md
[related-4]: docs/mcp_server/ARCHITECTURE.md
[related-5]: docs/reference/mcp/server-configuration.md
[related-6]: docs/reference/mcp/config-loading-architecture.md
[related-7]: docs/reference/mcp/mcp_vision_reference.md
[related-8]: docs/reference/mcp/copilot-agent-instructions-model.md
[related-9]: docs/coding_standards/README.md
[related-10]: docs/coding_standards/QUALITY_GATES.md
[related-11]: docs/reference/mcp/release-assets-procedure.md
<!-- Link definitions -->

[related-1]: docs/setup/README.md
[related-2]: docs/mcp_server/README.md
[related-3]: docs/mcp_server/USER_GUIDE.md
[related-4]: docs/mcp_server/ARCHITECTURE.md
[related-5]: docs/reference/mcp/server-configuration.md
[related-6]: docs/reference/mcp/config-loading-architecture.md
[related-7]: docs/reference/mcp/mcp_vision_reference.md
[related-8]: docs/reference/mcp/copilot-agent-instructions-model.md
[related-9]: docs/coding_standards/README.md
[related-10]: docs/coding_standards/QUALITY_GATES.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-05 | Agent | Initial draft |