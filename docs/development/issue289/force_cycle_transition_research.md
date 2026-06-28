<!-- docs\development\issue289\force_cycle_transition_research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-28T07:10Z updated= -->
# Research: Relaxing Force Cycle Transition Validation

**Status:** APPROVED  
**Version:** 1.0.0  
**Last Updated:** 2026-06-28

---

## Problem Statement

The `force_cycle_transition` tool currently rejects target cycles outside the planned `[1..total]` range, throwing a `ValueError`. This violates the core design principle that forced commands should act as an escape hatch for operators/humans to bypass constraints during emergencies or custom cycles.

---

## Research Goals

- Analyze impact of removing range check in `force_cycle_transition`.
- Design warning-based note emission for out-of-range cycle numbers.
- Outline necessary code, test, and presentation changes.

---

## Findings

1. **PhaseStateEngine.force_cycle_transition**:
   - Currently calls `self._validate_cycle_number_range(to_cycle, issue_number)`, which throws a `ValueError` if the cycle is out of bounds.
   - Bypassing this validation for forced transitions is safe because:
     - `_get_cycle_name` returns `"Unknown"` gracefully if the cycle details are missing.
     - `skipped_cycles` range calculation (`range(min(from, to) + 1, max(from, to))`) functions correctly with any integer bounds.
     - `matching_cycle` resolves to `None`, returning an empty list of deliverables (`[]`). No crashes or unhandled exceptions occur.
2. **Warning Emission**:
   - To alert the operator that they have transitioned to an out-of-bounds cycle, the tool can attach a `cycle_out_of_range_warning` warning Note.
   - This note will be registered in `presentation.yaml` under `notes.templates.info`.

---

## Approved Strategy

- **Retain Range Checking for Normal Transitions**:
  - `transition_cycle` will continue to call `_validate_cycle_number_range` to prevent accidental out-of-bounds transitions during standard cycles.
- **Relax Range Checking for Forced Transitions**:
  - `force_cycle_transition` will skip the strict range check.
  - If the target cycle is out of range, the engine will write a warning log and append a `cycle_out_of_range_warning` note.
- **Testing**:
  - Add a unit test in `tests/mcp_server/unit/managers/test_phase_state_engine_parent_branch.py` that verifies forcing an out-of-range transition succeeds and produces the expected warning note.

---

## Expected Results

- Calling `force_cycle_transition` with `to_cycle=5` on a project planned with only 4 cycles succeeds.
- The `state.json` updates `current_cycle` to `5`.
- A warning message is presented to the user: `⚠️ Warning: Cycle 5 is outside the planned range [1..4].`

---

## Related Documentation
- **[docs/development/issue289/implementation_plan.md](file:///c:/temp/pgmcp/docs/development/issue289/implementation_plan.md)**
- **[docs/development/issue289/presentation_error_codes_design.md](file:///c:/temp/pgmcp/docs/development/issue289/presentation_error_codes_design.md)**

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-28 | Agent | Initial draft and analysis of relaxing force cycle transitions |
