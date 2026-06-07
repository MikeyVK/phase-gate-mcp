<!-- docs\development\issue139\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-16T09:00Z updated= -->
# Planning: Fix stale project.md reference for get_project_plan

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-16

---

## Summary

Single-cycle documentation fix: update the get_project_plan section in docs/reference/mcp/tools/project.md to reflect the actual output format including current_phase, phase_source, phase_detection_error. No code changes required.

---

## TDD Cycles


### Cycle 1: C1: Update project.md reference documentation

**Goal:** Replace stale get_project_plan output example and behavior notes with accurate content

**Tests:**
- No automated tests — documentation change only; verify by reading the updated file

**Success Criteria:**
docs/reference/mcp/tools/project.md get_project_plan Returns block shows flat dict with current_phase, phase_source, phase_detection_error; Behavior Notes describes state.json as sole source


## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |