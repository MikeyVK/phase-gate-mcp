<!-- .st3\temp\pr_render.md -->
<!-- template=pr version=93bb9b4e created=2026-04-10T15:05Z updated= -->
# Fix ready-phase PR enforcement and prevent branch-local artifact contamination

Implements the ready-phase enforcement flow for PR creation, hardens the enforcement request path, and adds server-level regression coverage for blocked create_pr calls.
## Changes
- Added ready-phase enforcement configuration and phase-contract wiring for merge readiness and branch-local artifact exclusion.
- Implemented merge-readiness checks in the enforcement runner, including non-interactive git subprocess safeguards for request-path commands.
- Updated the MCP server tool dispatch path so pre/post enforcement failures return proper tool errors instead of falling through toward the GitHub create_pr call.
- Added integration and server-level regression tests for wrong-phase and tracked-artifact create_pr blocking behavior.
- Updated issue #283 research, planning, design, and QA handover documentation plus related reference docs for the final workflow behavior.

## Testing
- pytest tests/mcp_server/unit/test_server.py tests/mcp_server/integration/test_ready_phase_enforcement.py
- Focused quality gates passed for mcp_server/server.py, mcp_server/managers/enforcement_runner.py, tests/mcp_server/unit/test_server.py, and tests/mcp_server/integration/test_ready_phase_enforcement.py
- Live runtime verification: create_pr returned ERR_VALIDATION immediately while .st3/state.json and .st3/deliverables.json were still tracked, without hanging
## Checklist

- [ ] Code follows project standards
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Quality gates passing
## Related Documentation
- **[docs/development/issue283/research-ready-phase-enforcement.md][related-1]**
- **[docs/development/issue283/planning-ready-phase-enforcement.md][related-2]**
- **[docs/development/issue283/design-ready-phase-enforcement.md][related-3]**
- **[docs/development/issue283/qa-handover-design-v2.md][related-4]**

---

Closes: #283