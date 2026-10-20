<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue \#530 — normal note policy validation

**Status:** Validation complete — independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-20

## Purpose

Verify readable normal planning notes while preserving complete stored planning and genuine diagnostics.

## Scope In

C_1/D_1.1–D_1.2 on implementation d9400f1b0adb986ad66ed9fa37ce33dfdc77f794; existing formatter policy, normal public note/SDK surface and independent planning readback.

## Scope Out

No producer, persistence, protection, public DTO/schema/channel/cache/config/default or lifecycle-test changes.

## Issue Number

#530

## Cycle

C_1

## Validation Status

PASS

## Obligations

### Supported planning evidence is readable after a successful mutation

**Evidence:**

- [SDK append/readback case](<../../../tests/mcp_server/integration/test_execution_presentation_v3.py>)

**Outcome:** The test performs a real isolated append, then calls get_project_plan separately. Complete C_1 matches its snapshot; appended C_2/D_2.1, description and criteria match inputs before the visible-note assertion. Controlled evidence/admission is not claimed as real Git/enforcement coverage.

### Existing policy and honest diagnostics

**Evidence:**

- [Public note cases](<../../../tests/mcp_server/unit/test_presenter.py>)
- [Unchanged formatter](<../../../mcp_server/presenters/collection_text_renderer.py>)

**Outcome:** Global/local list/tuple ordering, configured bound/separator/omission/empty value, local priority and unchanged source values are exercised. Missing limit/nested-value cases preserve native ConfigError/trace/text while the operation and another note remain visible.

### Minimal boundary change

**Evidence:**

- [Presentation owner](<../../../mcp_server/presenters/text_presenter.py>)
- [Design](<design.md>)

**Outcome:** Only note formatter inputs and reuse of selected tool config changed in production. No numeric fallback or new public contract; existing scalar/syntax/composition evidence reused.

## Evidence

### Meaningful RED and focused GREEN

RED commit 01f155bd87e7aee1b0e08f3d81a0212b4bffb951:1 failed,31 deselected in2.75s after successful update/readback, solely at absent supplied HEAD value (9938495886fe40cfa5ca0f43f84fbe92). Focused GREEN:89 passed in11.73s, native defaults/eight workers (0a468198392944ad8c8a6b8c4650e6e2). Six new behavior cases across two existing files; no research-probe copy or prose snapshots.

**Sources:**

- [Public SDK case](<../../../tests/mcp_server/integration/test_execution_presentation_v3.py>)
- [Presenter cases](<../../../tests/mcp_server/unit/test_presenter.py>)

**Invocation:** RED: run_tests(scope='targets',targets=['tests/mcp_server/integration/test_execution_presentation_v3.py'],tests=['python_tests'],args={'python_tests':['-n','0','-k','planning_update_note']},timeout_seconds=300). GREEN: run_tests(scope='targets',targets=['tests/mcp_server/integration/test_execution_presentation_v3.py','tests/mcp_server/unit/test_presenter.py','tests/mcp_server/unit/presenters/test_collection_text_renderer.py','tests/mcp_server/unit/presenters/test_text_presenter_composition.py'],tests=['python_tests'],timeout_seconds=600), no args.

### Changed-file gates

Formatting, lint and Pyright all passed before GREEN commit (53e36b5b8a3f47eeb3ad72fba690a97e). Native format/lint fixes2be609e22fc5418996bd498eeb91565c were reviewed before tests; no suppressions or settings relaxation.

**Sources:**

- [Changed presentation owner](<../../../mcp_server/presenters/text_presenter.py>)

**Invocation:** run_checks(scope='targets',targets=['mcp_server/presenters/text_presenter.py','tests/mcp_server/integration/test_execution_presentation_v3.py','tests/mcp_server/unit/test_presenter.py'],checks=['python_format','python_lint','python_pyright'],timeout_seconds=300)

### Branch and configured gates

All four branch checks passed (97f00244b4244f01a7fba59a8bd30f28). All four configured Python checks passed (d0da57d2daf145669ce38a120124a786), preserving production-only Mypy and per-check branch filtering. No YAML/schema targets changed.

**Sources:**

- [Required selections](<planning.md>)
- [Quality standards](<../../coding_standards/QUALITY_GATES.md>)

**Invocation:** run_checks(scope='branch',checks=['python_format','python_lint','python_pyright','markdown_links'],timeout_seconds=600); run_checks(scope='configured',checks=['python_format','python_lint','python_types','python_pyright'],timeout_seconds=600)

### Complete native suite

3104 passed in 594.48s (9m54s), native exit 0, no termination problem, no args override and no repeat. Receipt: 04db774d8fcf4617b42cedc10a5236c2. The full native selection includes the six added behavior cases; the successful SDK case establishes independent storage/readback before its readable-note assertion.

**Sources:**

- [Native settings](<../../../pyproject.toml>)

**Invocation:** run_tests(scope='configured',tests=['python_tests'],timeout_seconds=1800), no args override

### Active source and no live mutation replay

Existing restart activated final source; fresh work context and health showed healthy PID10980 (a464cb121e784cd2b5041b63310f2c70). No real issue-planning mutation was used for demonstration. Independent chat instances need their own refresh; no universal refresh claim.

**Sources:**

- [Research isolation and control](<research.md>)

**Invocation:** restart_server(reason='Activate #530 normal note formatting after focused GREEN and all target gates passed; public tool contracts unchanged.'), fresh get_work_context(), health_check()

## Demonstration

Safe repeatable corrected-behavior demonstration is the SDK RED invocation above on current source. It mutates only configured_workspace in pytest temp storage and independently queries readback. It uses current real tools/presenters/SDK without counterfactual patches.

## Preservation

Source notes remain native values; domain models, IDs, descriptions, criteria, Git protections and command/readback APIs are unchanged. Existing 21 tools without max_items are not assigned a default. No public output/schema/channel/cache or #528 compact-recovery change.

## Failures

- The intentional behavioral RED above is retained as defect evidence. Research initially failed before mutation because its temporary workspace lacked contracts config; isolated setup was corrected and two characterization/control cases passed in2.98s. See Research for exact invocation/outcomes; no production change was claimed from that probe.

## Caveats

- Post-suite get_project_plan(530) retained exactly C_1 with D_1.1–D_1.2 and the same phase deliverables. git_status() showed only the expected Validation transition audit and this new report; source, tests and planning deliverables were not mutated by the suite.
- The pre-existing Windows lifecycle readiness risk recorded under #528 is not repaired by this issue; current required verification must still complete and report its actual result.

## Related Documents

- [Research](<research.md>)
- [Design](<design.md>)
- [Plan](<planning.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-20 | @imp validator | Record exact note/persistence evidence and required native verification; complete native suite and post-suite preservation confirmed. |

