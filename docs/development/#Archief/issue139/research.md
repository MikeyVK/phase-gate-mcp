<!-- docs\development\issue139\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-16T08:58Z updated=2026-05-16 -->
# Bug: get_project_plan does not return current_phase from state.json

**Status:** COMPLETE
**Version:** 1.0
**Last Updated:** 2026-05-16

---

## Problem Statement

`GetProjectPlanTool` only returned workflow definition from `deliverables.json`
(workflow_name, required_phases, execution_mode), but did NOT return the current phase
from `state.json`. Agents had to separately read `state.json` to determine where a project was.

## Research Goals

- Confirm root cause
- Assess implementation status
- Identify remaining documentation gaps
- Define minimal fix scope

---

## Findings

### 1. Root Cause (confirmed)

`ProjectManager.get_project_plan()` read only from `deliverables.json`. There was no call to
`state.json` or any phase-state component. `GetProjectPlanTool.execute()` called this method
directly and returned the result verbatim.

**Original path:**
```
GetProjectPlanTool.execute()
  → manager.get_project_plan(issue_number)
    → reads deliverables.json only
    → returns dict without current_phase
```

### 2. Fix Already Implemented

The fix was implemented as part of issue #231 (C4: WorkflowStatusResolver adoption). As of
the current codebase on `main`:

- `ProjectManager.__init__` accepts `workflow_status_resolver: WorkflowStatusResolver`
- `ProjectManager.get_project_plan()` calls `self._workflow_status_resolver.resolve_current()`
- On success: enriches the plan dict with `current_phase`, `phase_source`, `phase_detection_error`
- On `StateNotFoundError` or `StateBranchMismatchError`: returns plan without phase fields (graceful degradation)

**Current path:**
```
GetProjectPlanTool.execute()
  → manager.get_project_plan(issue_number)
    → reads deliverables.json (base plan)
    → calls WorkflowStatusResolver.resolve_current()
      → reads state.json via BranchValidatedStateReader
      → returns WorkflowStatusDTO(current_phase, phase_source="state.json", ...)
    → enriches plan with current_phase, phase_source, phase_detection_error
    → returns enriched dict
```

**Live verification (2026-05-16):**
```json
{
  "issue_title": "Bug: get_project_plan does not return current_phase from state.json",
  "workflow_name": "bug",
  "current_phase": "research",
  "phase_source": "state.json",
  "phase_detection_error": null,
  ...
}
```

### 3. Test Coverage

63 tests pass for `test_project_manager.py` + `test_project_tools.py`.

Tests cover all success criteria scenarios:
- `test_get_project_plan_uses_resolver_phase` — current_phase returned from resolver
- `test_get_project_plan_formats_phase_colon_sub_phase` — sub_phase formatting
- `test_get_project_plan_passes_resolver_error_to_plan` — phase_detection_error propagation
- `test_get_project_plan_returns_plan_without_phase_fields_when_state_absent` — StateNotFoundError → graceful
- `test_get_project_plan_returns_plan_without_phase_fields_on_mismatch` — StateBranchMismatchError → graceful

### 4. Remaining Gap: Documentation

`docs/reference/mcp/tools/project.md` §`get_project_plan` is stale and incorrect:

| Issue | Documented (stale) | Actual |
|---|---|---|
| Response structure | Nested `"project": {...}` | Flat dict |
| Field name | `"phases"` | `"required_phases"` |
| Missing fields | — | `current_phase`, `phase_source`, `phase_detection_error` |
| Extra fields | `"completed_phases"`, `"updated_at"`, `"success"` | Not present |
| Behavior Note | "commit scope with fallback to state.json" | state.json only |

The issue success criterion "✅ agent.md updated with expected output format" is NOT yet met.

---

## Affected Files

| File | Status | Action |
|------|--------|--------|
| `mcp_server/tools/project_tools.py` | ✅ OK | No change needed |
| `mcp_server/managers/project_manager.py` | ✅ Fixed | No change needed |
| `mcp_server/managers/workflow_status_resolver.py` | ✅ OK | No change needed |
| `tests/mcp_server/unit/managers/test_project_manager.py` | ✅ Tests pass | No change needed |
| `tests/mcp_server/unit/tools/test_project_tools.py` | ✅ Tests pass | No change needed |
| `docs/reference/mcp/tools/project.md` | ❌ Stale | **Must update** |

---

## Impact Assessment

- **Severity:** Low — code already works correctly; only documentation is wrong
- **Blast radius:** Agents reading `project.md` reference docs get incorrect output format
- **User-visible risk:** Agents may expect `"project"` wrapper or `"phases"` field — wrong

---

## Solution Options

### Option A: Documentation-only fix (Recommended)

Update `docs/reference/mcp/tools/project.md` §`get_project_plan`:
- Replace the stale response example with the actual format
- Remove `"success"`, `"project"` wrapper, `"phases"`, `"completed_phases"`, `"updated_at"`
- Add `current_phase`, `phase_source`, `phase_detection_error` to the example
- Fix the Behavior Notes (state.json is the only source, not commit scope)

**Risk:** Zero — documentation only. No code change.

### Option B: Documentation + tool description (Optional enhancement)

Same as A, plus update `GetProjectPlanTool.description` to mention `current_phase` in output.

**Risk:** Very low — docstring change only.

---

## Recommended Option

**Option A** — minimal documentation fix satisfies the remaining success criterion.
The code is complete and tested. Only the reference doc needs updating.

**Key constraint:** Architecture principle §3 Config-First: the documentation must accurately
reflect the actual behavior from state.json (not invent a "commit scope" priority that no longer exists).

---

## Scope for Designer

Elaborate Option A only: exact line-by-line changes to `docs/reference/mcp/tools/project.md`
for the `get_project_plan` section. No implementation changes.

---

## Related Documentation

- `mcp_server/managers/project_manager.py` — get_project_plan() implementation
- `mcp_server/managers/workflow_status_resolver.py` — WorkflowStatusResolver
- `docs/reference/mcp/tools/project.md` — reference doc to fix
- Issue #231 — WorkflowStatusResolver adoption (where the code fix landed)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-16 | imp-researcher | Initial research: confirmed fix in place, identified doc gap |
