<!-- pgmcp:v1 id=planning pv=1.0.0 pf=K72uxa-fhywx1wo8 sf=zJbLuUrs_I33kpX4 -->

# Issue 470 — LF cutover planning

**Status:** Planning complete; independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-11

## Purpose

Execute one bounded cycle and reuse focused evidence.

## Scope In

The seven production sources below, three existing test sources for adaptation/cutover, active editing reference and issue phase artifacts.

## Scope Out

Writer/check/adapter redesign, scaffold policy, Git/editor settings, bulk normalization, old-policy regression coverage.

## Prerequisites

- Research v1.0 and Design v1.0; Design→Planning GO on 84867c15.

## Summary

One C_1 cycle with D_1.1–D_1.3; no compatibility period or new test files. Stored plan readback confirms one cycle, three execution deliverables and two phase deliverables.

## Dependencies

- Execution: focused baseline → existing case adaptation/current-policy failure observation → production/consumer cutover and obsolete-structure deletion → focused tests/file gates → independent Implementation→Validation QA.
- A temporary failing behavior expectation may be observed locally; no separate regression file or old-policy rejection test remains. Existing adequate safety coverage needs no artificial RED.
- Rollback before publication: restore only the cycle's source/test paths from 84867c15 via git_restore; return to Planning for any changed strategy. No runtime migration.

## Milestones

- Validation alone: run_tests(scope='configured', tests=['python_tests'], timeout_seconds=1800), native args/selection/workers retained. One full run; rerun only for material invalidation or failure.
- Validation: run_checks(scope='branch', checks=['python_format','python_lint','python_types','python_pyright','markdown_links'], timeout_seconds=600); per-binding configured branch filters apply.
- Validation: run_checks(scope='configured', checks=['python_format','python_lint','python_types','python_pyright'], timeout_seconds=600). Record exact native counts/outcomes and existing caveats compactly.
- Documentation: update docs/reference/tools/editing.md with safe_edit enforce; run only invalidated document links. No broad suite repetition for docs/state.
- One independent phase GO/NOGO at each transition; QA reuses producer evidence and runs narrow reproduction only when a material gap justifies it.

## Work Units

### C\_1 — LF safe-edit cutover

**Goal:** Complete the Design clean break in one coherent cutover.

**Cycle Number:** 1

#### Scope In

Production: mcp_server/services/edit_construction.py, mcp_server/services/edit_operation.py, mcp_server/core/interfaces/file_writer.py, mcp_server/utils/atomic_file_writer.py, mcp_server/bootstrap.py, mcp_server/schemas/mutation_outputs.py, mcp_server/tools/edit_tool.py. Test edits: tests/mcp_server/unit/services/test_edit_construction.py, tests/mcp_server/integration/test_edit_operation_v3.py, tests/mcp_server/integration/test_markdown_mutations.py.

#### Scope Out

No adapter/writer persistence changes or new test files.

#### Deliverables

##### D\_1.1

One pure LF construction route; remove preservation-only source/proposal structure.

**Owner:** @imp implementer

##### D\_1.2

Cut over service/bootstrap/integration consumers; same checked/written text and original-byte guard; factual byte-change output.

**Owner:** @imp implementer

##### D\_1.3

Adapt existing tests and reduce preservation matrix to eight behavior cases; focused checks pass without new test files.

**Owner:** @imp implementer

#### Exit Criteria

Design v1.0 implemented; focused behavior and appropriately scoped Python gates pass; old preservation consumers absent; no test-count growth.

#### Dependencies

- No preceding implementation cycle. Research/Design approvals are prerequisites.

#### Obligations

- Same final checked/written string and exact-original-byte race guard.
- No remaining dual proposal/source-only consumer or preservation algorithm.
- Adapt current behavior coverage; remove preservation-only cases; keep focused count non-growing.

#### Verification

##### Baseline and final behavior

**Method:** run_tests(scope='targets', targets=["tests/mcp_server/unit/services/test_edit_construction.py","tests/mcp_server/integration/test_edit_operation_v3.py","tests/mcp_server/integration/test_edit_public_v3.py","tests/mcp_server/integration/test_markdown_mutations.py"], tests=['python_tests'], timeout_seconds=600), native args omitted.

**Expected Result:** Focused green baseline; final LF/byte-change/safety behavior passes with fewer parameterized integration items.

##### Appropriate file gates

**Method:** run_checks(scope='targets', targets=["mcp_server/services/edit_construction.py","mcp_server/services/edit_operation.py","mcp_server/core/interfaces/file_writer.py","mcp_server/utils/atomic_file_writer.py","mcp_server/bootstrap.py","mcp_server/schemas/mutation_outputs.py","mcp_server/tools/edit_tool.py"], checks=['python_format','python_lint','python_types','python_pyright'], timeout_seconds=600). Changed test paths separately receive only python_format/python_lint.

**Expected Result:** All pass; no Markdown/JSON/test files sent to production type gates.

#### Risks

##### Whole-file LF conversion on a successful no-match proposal is intentional.

Assert persisted bytes and changed=true; document the policy.

#### Stop Conditions

- Unexpected consumer, required compatibility or safety/regex behavior outside Design.
- Failing required checks, increased retained test count or incomplete cleanup.

## Phase Deliverables

### Validation

#### D\_1

One configured full native suite, branch gates, configured Python gates and compact durable outcomes.

**Validates:**

**Type:** file_exists

**File:** "docs/development/issue470/validation.md"

### Documentation

#### D\_1

Document LF text policy, native regex matching and byte-change/no-op semantics in the active editing reference.

**Validates:**

**Type:** file_exists

**File:** "docs/reference/tools/editing.md"

## Related Documents

- [Research](<research.md>)
- [Design](<design.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-11 | @imp planner | Save and verify one cycle; assign targeted gates and one Validation full suite. |
