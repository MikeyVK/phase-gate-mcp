<!-- docs\development\issue348\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-05T18:50Z updated=2026-06-05 -->
# Issue #348 Planning

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-05

---

## Scope

**In Scope:**
Localized contract change for the agent-facing `safe_edit_file` input/output behavior plus the directly affected tests that must prove the compact-response contract.

**Out of Scope:**
Reference and historical documentation updates; broader MCP response model changes; validation-engine redesign; any new response modes or compatibility bridge.

## Prerequisites

Read these first:
1. The research artifact for issue #348, which records the Approved Strategy.
2. `ARCHITECTURE_PRINCIPLES.md`.
3. `TYPE_CHECKING_PLAYBOOK.md`.

---

## Summary

Compact planning for the clean-break `safe_edit_file` response contract change. One implementation cycle is sufficient because the production blast radius is local to the tool contract, the Approved Strategy is already settled in research, and documentation updates are intentionally deferred to the documentation phase.

---

## Design Alignment

A separate substantive design phase was intentionally skipped by audited force transition. Planning must preserve the research conclusion that the change is a localized contract simplification rather than a broader response-model redesign.

## Approved Strategy Alignment

Implementation must preserve the Approved Strategy from [research.md][related-1]:
- clean break on the agent-facing `safe_edit_file` contract
- remove the public `show_diff` exposure
- remove diff preview from default responses
- preserve useful status and validation feedback
- keep internal diff functionality private if it remains useful for future non-agent contexts

---

## Dependencies

- Implementation depends on the clean-break strategy recorded in [research.md][related-1].
- Documentation reconciliation is intentionally postponed to the documentation phase.
- The implementation cycle must begin with a narrow audit to confirm that `show_diff`, `SafeEditInput`, and `_generate_diff()` are not used in ways that widen the local blast radius.

---

## TDD Cycles

### Cycle 1: C_348.1 — Remove diff from agent-facing `safe_edit_file` contract

**Why this boundary exists:**
The entire approved change is a single localized contract simplification. Splitting production code and directly affected tests into separate cycles would create artificial sequencing without reducing risk.

**Goal:**
Implement the clean-break contract change in `safe_edit_file`, preserve useful status and validation feedback, and align directly affected tests to the compact response contract.

**Production and test impact:**
- Production surface: `mcp_server/tools/safe_edit_tool.py`
- Test surface: directly affected `safe_edit_file` unit tests and any narrow response-text assertions discovered during the pre-implementation audit
- Documentation: explicitly deferred to documentation phase; not part of this implementation cycle

**Deliverables:**
- D_348.1.1: narrow pre-implementation audit recorded in code/test work, confirming whether `SafeEditInput`, `_generate_diff()`, and `show_diff` references widen the blast radius
- D_348.1.2: agent-facing `safe_edit_file` contract updated so `show_diff` is no longer publicly exposed
- D_348.1.3: diff preview removed from default `safe_edit_file` response builders while preserving status and validation messaging
- D_348.1.4: directly affected tests updated to assert the compact response contract

**Validation obligations:**
- run the narrowest directly affected test slice first
- keep validation focused on compact-response behavior, preserved `response.issues` semantics, and unchanged success/warning/error status text behavior
- confirm no unexpected contract widening from hidden references discovered during the pre-implementation audit

**Typing obligations:**
- remove the exposed field cleanly from the input schema without introducing broad ignores or casts
- keep type changes local to the affected tool/test surfaces
- follow the type-checking playbook if schema or test assertions expose typing fallout

**Quality-gate obligations:**
- targeted quality gates must pass for all touched production and test files before the cycle closes
- no cycle close if status or validation messaging regresses while diff is removed

**Exit Criteria:**
- the agent-facing `safe_edit_file` contract no longer exposes `show_diff`
- default `safe_edit_file` responses no longer include diff preview
- useful status and validation feedback remains intact
- directly affected `safe_edit_file` unit tests pass against the compact response contract
- targeted quality gates pass for all touched files

**Dependencies:**
- Approved Strategy from research: clean break on the agent-facing `safe_edit_file` contract
- documentation updates are deferred to the documentation phase and are not part of this implementation cycle

---

## Risks & Mitigation

- **Risk:** Unexpected reflective or example usage of `show_diff` outside the local `safe_edit_file` surface could widen the blast radius.
  - **Mitigation:** Perform a narrow pre-implementation audit of `SafeEditInput`, `_generate_diff()`, and `show_diff` references before editing.
- **Risk:** Removing diff output could accidentally strip useful validation text if response builders are edited too broadly.
  - **Mitigation:** Keep the change local to diff prepend logic and explicitly preserve `response.issues` and status text behavior in tests.

## Test / Validation Strategy

Implementation should prove only what this localized cycle changes:
- compact response contract now excludes diff preview
- status, warning, and validation text remain actionable
- no unexpected reference to the removed public field blocks the cycle
- changed production and test files pass targeted quality gates

## Highest-Risk Dependencies

- The narrow audit on `show_diff`, `SafeEditInput`, and `_generate_diff()` is the only meaningful sequencing checkpoint before editing.
- The main failure mode is not architectural complexity but accidental removal of useful status or validation feedback while stripping diff output.

## Open Questions

None blocking for planning. Remaining audit points are execution checks inside Cycle 1, not unresolved planning or design questions.

## Related Documentation
- **[docs/development/issue348/research.md][related-1]**
- **[docs/reference/mcp/tools/editing.md][related-2]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-3]**
- **[docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md][related-4]**

<!-- Link definitions -->

[related-1]: docs/development/issue348/research.md
[related-2]: docs/reference/mcp/tools/editing.md
[related-3]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-4]: docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-05 | Agent | Initial draft |
