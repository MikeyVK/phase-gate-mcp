<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue 507 — Test-harness diagnostic classification

**Status:** RESEARCH — OWNER STRATEGY PENDING  
**Version:** 0.1  
**Last Updated:** 2026-10-16

## Purpose

Bound maintenance to demonstrated harness defects and honest expectations; distinguish production API warnings and intentional contracts.

## Scope In

Fresh targeted diagnostic baseline; restart coroutine/task ownership in existing tests; collection-name collisions; stale XPASS; assessment of the current manual skip; explicit disposition of production warning families.

## Scope Out

No zero-warning quota, global filters, replacement test framework, coverage campaign, broad helper/isolation refactor (#250/#140), general process/runtime timeout stabilization, release/dependency-floor change or automatic deployment.

## Problem Statement

Earlier full suites pass while reporting warnings, a non-strict XPASS, a manual skip and restart-task stderr. Warning counts do not identify causes. Research must distinguish actual test defects from intentional contracts and production API maintenance before repair.

## Goals

- Repair genuine harness coroutine/task lifecycle defects in existing valuable tests.
- Remove false test-collection candidates and stale expectations without production pytest metadata.
- Retain a manual skip only when it protects real executable behavior.
- Obtain a boundary-specific owner strategy for residual warnings and any production expansion.

## Background

Main includes merged #506 at961d1edf1f17dd3ed1b570827c3da1a058365472. Its full confirmation2915passed/1skip/1xpass/253warnings is history, not #507 evidence. #319 DF-319.4 deferred this classification. #250 owns broader isolation/maintenance and #140 broader coverage debt; neither historical count/threshold is imported here.

## Findings

### Fresh classification

| Signal | Observed cause / responsibility | Proposed disposition |
| --- | --- | --- |
| Unawaited delayed_exit coroutine | unit/tools/test_health_tools.py patches create_task with a plain Mock, which never schedules or closes the supplied coroutine. GC can report it during a later unrelated test. | Fix test ownership at that boundary: consume/close the intentionally unexecuted coroutine. Preserve DTO assertions; no production change. |
| Task exception never retrieved / SystemExit42 | Three tools/test_admin_tools.py tests deliberately raise SystemExit42 from mocked sys.exit inside the real scheduled background task; asyncio.run propagates it but task outcome is not retrieved. | Test-only repair using owned/awaited scheduled tasks and a controlled exit boundary. Preserve marker, response-before-exit, restart marker/exit42 and meaningful audit evidence. Remove obsolete os.execv absence/duplicate test ballast rather than new regression cases. |
| Collection warnings | Imported TestCapability in integration/adapters/test_pytest.py and TestsConfig in unit/resources/test_standards.py look like pytest test classes. | Alias imports/usages locally. Do not put __test__ metadata into production models. |
| Non-strict XPASS | test_enforcement_runner_unit.py's note-rendering test is marked xfail for unrelated old neutralize_to_base behavior and has duplicate asyncio markers. It currently exercises NoteContext.render_to_response and passes. | Remove stale xfail/duplicate mark; describe the actual public rendering contract. No expectation for obsolete commit behavior. |
| Manual skip | core/test_proxy.py's TestProxyIntegration checks RUN_MANUAL_TESTS then contains comments only. With the flag enabled it would pass without execution/assertions. | Owner choice: remove this empty test placeholder; do not claim manual restart coverage or build a new integration scenario. Retain other proxy tests. |
| Historical stale asyncio marks | Recent full output does not contain this warning; current module-wide marks inspected in create_issue_e2e and create_issue_label_assembly apply to async tests. | No demonstrated current defect; no general marker sweep. |
| SchemaAttachment.schema shadow warning | core/tool_execution.py intentionally replaces BaseModel's deprecated schema() method; the field is explicit in #460 shared contracts and used by attachment producers/presenter. | Recommend retain contract and disclose warning; no rename/alias or filter merely to reduce count. |
| PureWindowsPath.is_reserved deprecation | Real production path safety in utils/path_resolver.py; package supports Python>=3.11. Replacement os.path.isreserved is Windows-only and added in3.13; old method is scheduled for removal in3.15. | Recommend retain pending an explicit Python-support/path-safety decision; no compatibility bridge, version-floor increase or weaker guard in this Chore. |
| SDK read_resource deprecation | Real production server.py handler returns str. Installed SDK1.25.0 accepts Iterable[ReadResourceContents] and warns for str/bytes. This is not caused by test assertions. | Owner scope choice: preserve/disclose for a bounded test-only Chore, or first investigate a minimal production boundary update. Minimum declared mcp>=1.0,<2 support has not been proven for the replacement; no dependency-floor change or inferred compatibility claim. |

Repeated worker warnings are multiple occurrences of a family, not independent bugs.
The selected94warnings comprise9schema-shadow,45SDKresource,39Windowsreserved-path and1unawaited-coroutine occurrences. Their count is scoped evidence, not a workspace acceptance target.

### Consumer and verification boundary

Recommended implementation touches only existing tests: tools/test_admin_tools.py,
unit/tools/test_health_tools.py, unit/managers/test_enforcement_runner_unit.py,
core/test_proxy.py, integration/adapters/test_pytest.py and unit/resources/test_standards.py.
No new fixture module, global reset/filter, production restart/exit behavior or schema/path
contract change. Adapt useful existing tests, remove only demonstrated empty/obsolete
test material. Collection-only proof must not be represented as executed behavior tests.

Resource reads in project-plan/cache/presentation integration tests expose the production
SDK warning through the real MCP handler. Merely changing those tests would hide the
source. A production SDK repair, if selected, needs explicit output/URI/MIME/error behavior,
supported-version and consumer evidence first.

The previous #506 process-lifecycle PID readiness failure is outside this boundary.
It did not recur in that issue's unchanged full confirmation; its exact cause remains
unproven. Do not add a runtime/timeout fix by assumption. If it recurs during required
Validation, preserve diagnostics and investigate before a new scope decision.

Implementation uses narrow tests and file gates. Validation owns the required full native
configured suite and filtered branch/configured-production gates, preserving native args,
coverage and the1200-second execution budget within the1800-second client window.

### Execution checkpoint

- Issue/branch/parent: #507; chore/507-test-harness-restart-diagnostics; main.
- Phase/baseline: Research;961d1edf1f17dd3ed1b570827c3da1a058365472.
- Artifacts: this Research; #506 Validation is historical input only.
- Owner decisions: queue execution authorized; boundary-specific strategy pending.
- Code/tests: unchanged. Only targeted existing diagnostic calls performed.
- QA boundary/verdict: Research→Implementation, not yet requested.
- Blockers/next: settle empty manual placeholder and residual production warning/SDK scope,
  record Approved Strategy, then independent QA. No implementation before that decision.

## Questions

- Approve removing the empty manual integration placeholder instead of retaining a skip that guards no executable test?
- Approve the recommended test-only scope with explicit residual production warnings, or first investigate the minimal production SDK handler route?

## Approved Strategy

PENDING HUMAN DECISION. Proposed: test-only clean maintenance with existing task ownership/mocks, local collection aliases and truthful XPASS/manual expectations; no old-behavior regression tests. Preserve production restart/exit semantics, schema field and path guard; disclose their residual warnings without filters. SDK handler migration is excluded unless the owner first authorizes that bounded production investigation. No global fixtures/framework, Python/MCP version-floor change, automatic workaround or broad cleanup.

## Expected Results

Targeted collection no longer misidentifies imported production classes; restart tests own/consume all created coroutine/tasks and preserve observable restart protocol/audit facts; stale XPASS becomes an ordinary meaningful pass. A justified real manual skip is preserved, but an empty enabled-pass placeholder is not presented as coverage. Any accepted production warning remains visible with exact source/rationale; no warning-count target.

## Evidence

### Both collection-name collisions reproduce.

27 tests collected, zero tests executed, exit0 in0.21s. Warnings: SchemaAttachment.schema shadow, TestCapability and TestsConfig collection. Supplemental d1972a95fb474f88955ccd75e08178d7.

**Invocation:** run_tests(scope='targets',targets=['tests/mcp_server/integration/adapters/test_pytest.py','tests/mcp_server/unit/resources/test_standards.py'],tests=['python_tests'],args={'python_tests':['--collect-only','-q']},timeout_seconds=180).

### Fresh focused baseline separates test outcomes from diagnostics.

37passed,1skipped,1xpassed,94warnings,39items,33.25s,nativeexit0. Skip source is empty manual placeholder; XPASS reason is stale; unawaited coroutine reported later during unrelated test due to GC. Supplemental32186dd47f29453e83407c72f6c9e164.

- [Unowned restart coroutine](<../../../tests/mcp_server/unit/tools/test_health_tools.py>)
- [Stale expectation](<../../../tests/mcp_server/unit/managers/test_enforcement_runner_unit.py>)
- [Manual placeholder](<../../../tests/mcp_server/core/test_proxy.py>)

**Invocation:** run_tests(scope='targets',targets=["tests/mcp_server/tools/test_admin_tools.py","tests/mcp_server/unit/tools/test_health_tools.py","tests/mcp_server/unit/managers/test_enforcement_runner_unit.py","tests/mcp_server/core/test_proxy.py","tests/mcp_server/integration/test_project_plan_readback.py","tests/mcp_server/integration/test_cache_fidelity_v3.py","tests/mcp_server/integration/test_execution_presentation_v3.py","tests/mcp_server/unit/services/test_artifact_target_resolver.py"],tests=['python_tests'],args={'python_tests':['-r','sxX']},timeout_seconds=300).

### Restart stderr is caused by explicit test exit doubles.

6passed,9schema warnings,12.83s,nativeexit0. Native stderr section contains three restart markers and three task-not-retrieved traces, each ending at test mock_exit raising SystemExit42. This is not an established production restart incident. Supplemental b5b2b6e543334f1e84786facc55600a6.

- [Existing restart tests](<../../../tests/mcp_server/tools/test_admin_tools.py>)
- [Production restart boundary](<../../../mcp_server/tools/admin_tools.py>)

**Invocation:** run_tests(scope='targets',targets=['tests/mcp_server/tools/test_admin_tools.py'],tests=['python_tests'],args={'python_tests':['-s','--log-cli-level=ERROR']},timeout_seconds=180).

### Production deprecations require real contract choices.

Installed SDK1.25.0 read_resource wrapper accepts str/bytes or Iterable[ReadResourceContents]; its deprecated string path creates text/plain. A replacement must not silently change MIME or resource/error behavior. Python docs place isreserved in3.13 and is_reserved removal in3.15; project still declares Python>=3.11. Early SDK1.0 historical raw-source URL probes did not retrieve the source, so replacement support at that floor is unverified.

- [Current declared support](<../../../pyproject.toml>)
- [SDK handler consumer](<../../../mcp_server/server.py>)
- [Windows path safety](<../../../mcp_server/utils/path_resolver.py>)
- [Python pathlib deprecation](<https://docs.python.org/3.13/library/pathlib.html#pathlib.PurePath.is_reserved>)
- [Python replacement availability](<https://docs.python.org/3.13/library/os.path.html#os.path.isreserved>)

## Related Documents

- [Issue507](<https://github.com/MikeyVK/phase-gate-mcp/issues/507>)
- [Broader maintenance250](<https://github.com/MikeyVK/phase-gate-mcp/issues/250>)
- [Coverage140](<https://github.com/MikeyVK/phase-gate-mcp/issues/140>)
- [Prior506evidence](<../issue506/validation.md>)
- [Approved attachment contract460](<../archive/issue460/design-shared-contracts.md>)
- [Architecture](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-16 | @imp researcher | Record targeted native baseline, causal harness findings, production warning limits and two owner choices. |
