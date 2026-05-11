<!-- .st3\temp\pr_render.md -->
<!-- template=pr version=93bb9b4e created=2026-03-01T19:21Z updated= -->
# Issue #251 closure: stabilize run_quality_gates and align documentation

Completes issue251 stabilization and updates agent/reference docs to the refactored scope-based run_quality_gates contract.
## Changes
- Finalized scope-safe lifecycle behavior for `run_quality_gates` (auto-only baseline mutation semantics).
- Closed blocked live-validation scenarios (`A1-pass`, `B1-pass`, `P1-pass`, `X3c`, `X5`) with reversible setup and evidence capture.
- Added blocked-scenarios validation addendum for issue251.
- Updated root and MCP reference docs to the current input/output contract (`scope` + conditional `files`, compact `content[0]/content[1]` behavior).
- Marked issue251 planning/research/live-validation artifacts as completed historical records.
- Refreshed metadata headers (version/last-updated) where content changed.

## Testing
- Targeted unit suites for quality manager/tool behavior passed during TDD cycles.
- Focused quality gate runs passed on touched files.
- Live acceptance and blocked-scenario re-runs executed with server restarts and state restoration checks.
- Final branch state verified clean before PR creation.
## Checklist

- [ ] Quality gates pass for touched files
- [ ] Issue251 blocked scenarios are documented as closed
- [ ] Reference docs reflect current `run_quality_gates` contract
- [ ] No temporary validation state/config artifacts remain
- [ ] Branch is clean and pushed

## Related Documentation
- **[docs/development/issue251/live-validation-plan-v2.md][related-1]**
- **[docs/development/issue251/live-validation-blocked-scenarios-20260301.md][related-2]**
- **[docs/reference/mcp/tools/quality.md][related-3]**
- **[docs/reference/mcp/MCP_TOOLS.md][related-4]**
- **[agent.md][related-5]**

---

Closes: #251