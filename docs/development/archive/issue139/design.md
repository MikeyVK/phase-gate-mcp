<!-- docs\development\issue139\design.md -->
<!-- template=design version=5827e841 created=2026-05-16T09:00Z updated= -->
# Design: Fix stale project.md reference for get_project_plan

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-16

---

## 1. Context & Requirements

### 1.1. Problem Statement

docs/reference/mcp/tools/project.md shows a stale, incorrect output format for get_project_plan. The documented format wraps the response under a 'project' key, uses 'phases' instead of 'required_phases', and omits current_phase, phase_source, phase_detection_error. The code fix is already complete and tested.

### 1.2. Requirements

**Functional:**
- [ ] Replace stale response JSON example with the actual flat-dict format
- [ ] Show current_phase, phase_source, phase_detection_error fields in the example
- [ ] Remove non-existent fields: success wrapper, project wrapper, phases, completed_phases, updated_at
- [ ] Fix Behavior Notes: state.json is the only source (not 'commit scope with fallback')

**Non-Functional:**
- [ ] Documentation-only change — zero production code modifications
- [ ] No test changes required

### 1.3. Constraints

None
---

## 2. Design Options

### 2.1. Option A — Documentation-only fix (Chosen)

Update `docs/reference/mcp/tools/project.md` §`get_project_plan` only.

**Changes:**
- Replace the `Returns` block with the actual flat-dict format
- Remove non-existent keys (`success`, `project` wrapper, `phases`, `completed_phases`, `updated_at`)
- Add `current_phase`, `phase_source`, `phase_detection_error` to the example
- Fix Behavior Notes text: replace "commit scope with fallback to state.json" with "state.json only"

**Risk:** Zero — documentation only. No production code or test changes.

### 2.2. Option B — Documentation + tool description

Same as A, plus update `GetProjectPlanTool.description` in `project_tools.py`.

**Risk:** Very low — one-line change. Out of scope for this bug fix.

---

## 3. Chosen Design

**Decision:** Option A: update `docs/reference/mcp/tools/project.md` §`get_project_plan` only — no code changes.

**Rationale:** The implementation via WorkflowStatusResolver is complete and all 63 relevant tests
pass. The only outstanding success criterion is accurate reference documentation. A
documentation-only fix is the smallest complete change that closes the issue.

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Documentation-only | Code is already complete; no new logic needed |
| Single file change | Only `project.md` is stale; `README.md` tool list is not affected |
| state.json SSOT in Behavior Notes | Reflects WorkflowStatusResolver contract: state.json is authoritative |

### 3.2. Exact Changes to `docs/reference/mcp/tools/project.md`

The `get_project_plan` section (lines ~131–173) must be updated.

**Replace the `Returns` code block** with:

```json
{
  "issue_title": "My Feature",
  "workflow_name": "feature",
  "execution_mode": "interactive",
  "required_phases": ["research", "design", "planning", "implementation", "validation", "documentation", "ready"],
  "skip_reason": null,
  "parent_branch": "main",
  "created_at": "2026-02-08T10:00:00Z",
  "current_phase": "implementation",
  "phase_source": "state.json",
  "phase_detection_error": null
}
```

**Replace Behavior Notes bullet** for Plan Access:

- Before: `"Reads workflow definition from .st3/deliverables.json; live phase is detected from commit scope with fallback to .st3/state.json"`
- After: `"Reads workflow definition from .st3/deliverables.json; current phase is read from .st3/state.json via WorkflowStatusResolver. Returns plan without phase fields when state is absent or branch-mismatched."`

### 3.3. Test Strategy

No new tests required. The existing 63 tests cover all code paths. This is a docs-only change.

---

## Related Documentation

- `docs/reference/mcp/tools/project.md` — file to update
- `docs/development/issue139/research.md` — research findings
- Issue #231 — WorkflowStatusResolver adoption (where code fix landed)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-16 | imp-designer | Initial design: Option A documentation-only fix |