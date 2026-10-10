<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=CT9NV5LmQjKHFGqX sf=zJbLuUrs_I33kpX4 -->

# Issue \#491 — Planning mutation and workflow validation

**Status:** Independent Validation review requested  
**Version:** 1.1  
**Last Updated:** 2026-10-10

## Purpose

Record observed behavior and structural completion against the approved clean-break strategy. PASS describes the native verification outcomes; independent QA owns phase approval.

## Scope In

All seven execution deliverables across C_1–C_3, their consumer/configuration cleanup and the live gate-wiring repair on b72922a673a26dc6612835defd08df89c9f5e4b4. The final test-only suppression correction is d16ebd8dc96fdddc90080399b3901c1c997be80e; it changes three existing negative-test invocation forms, retaining all assertions and production/configuration behavior. Validation adds this report and the phase audit only.

## Scope Out

Compatibility/migration tooling, completion tracking, broad test rewrites, unrelated warning repairs, historical commit rewriting and a new cross-process transaction architecture.

## Prerequisites

- Research Approved Strategy, Design v1.1 and the three-cycle Planning are authoritative.
- Independent Implementation → Validation GO from ‘Beoordeel designplan’ on b72922a673a26dc6612835defd08df89c9f5e4b4; both P2 test-boundary findings were corrected and independently rechecked.

## Issue Number

#491

## Validation Status

PASS

## Obligations

### D\_1.1 — Shared lossless scope contract

**Evidence:**

- [Shared grammar](<../../../mcp_server/core/scope_contract.py>)
- [Codec round-trip behavior](<../../../tests/mcp_server/core/test_phase_detection.py>)

**Outcome:** One injected configured vocabulary preserves independent phase/cycle/subphase and returns immutable unknown results without guessing. Encoder/decoder and retained wrapper use the same contract; no query-time configuration loading.

### D\_1.2 — Captured-HEAD cycle evidence

**Evidence:**

- [Local Git traversal](<../../../mcp_server/adapters/git_adapter.py>)
- [Native ancestry/qualification behavior](<../../../tests/mcp_server/integration/test_git_cycle_evidence.py>)

**Outcome:** Traversal starts at captured active-branch HEAD, follows all reachable parents and has no count cutoff/network fetch. Deep and merged-parent execution evidence qualifies; other issues/phases/body-only markers do not. Unavailable evidence retains known positives. Title normalization preserves different issue references and the body.

### D\_2.1 — Complete-block planning commands

**Evidence:**

- [Planning command owner](<../../../mcp_server/managers/project_manager.py>)
- [Mutation/protection behavior](<../../../tests/mcp_server/unit/managers/test_project_manager.py>)

**Outcome:** Write-once save, five explicit whole-block operations and original-snapshot targeting produce a commonly validated complete plan. Server derives total/C_n/D_n.m/local D_n. Missing/duplicate/invalid targets preserve bytes. Every update retries evidence, including force; known positive deletion/renumbering protection remains binding and accepted uncertainty override is reported only after persistence.

### D\_2.2 — Planning consumers and admission

**Evidence:**

- [Public planning tools](<../../../mcp_server/tools/project_tools.py>)
- [Public tool/admission behavior](<../../../tests/mcp_server/unit/tools/test_project_tools.py>)
- [Live gate demonstration](<../../../tests/mcp_server/integration/test_project_plan_readback.py>)

**Outcome:** Tools return complete stored planning; existing configured enforcement admits planning-content writes only in Planning. Split dir/pattern reaches the unchanged checker through real bootstrap. Resolver reads the current issue plan on every gate evaluation; all four enforce/inspect phase/cycle routes receive issue identity.

### D\_2.3 — Fixture and workspace format cutover

**Evidence:**

- [Shared explicit construction](<../../../tests/mcp_server/test_support.py>)
- [Planning template behavior](<../../../tests/mcp_server/integration/templates/test_planning_artifact.py>)
- [Stored plan](<../../../.pgmcp/deliverables.json>)

**Outcome:** Affected constructors/readers and operational template projection use the new stored shape; obsolete partial-merge/static-plan expectations are removed. Native get_project_plan(491) returns the planned C_1–C_3, seven execution deliverables and two phase deliverables. Direct file remained 7,182 bytes with UTC mtime 2026-10-10T05:56:34.1350286Z before, during and after broad verification.

### D\_3.1 — Explicit cycle entry and initialization guard

**Evidence:**

- [Read-only plan/state orchestration](<../../../mcp_server/managers/phase_state_engine.py>)
- [Entry/re-entry behavior](<../../../tests/mcp_server/unit/managers/test_phase_state_engine.py>)
- [Initialization rejection before writes](<../../../tests/mcp_server/unit/tools/test_project_tools.py>)

**Outcome:** First entry selects C_1; re-entry selects an explicit current-plan C_n and clears last_cycle/subphase while preserving factual history. Normal and forced invalid entry leave state bytes/history/context unchanged. Same-branch initialization rejects before project persistence. Existing mutator performs the composed state change.

### D\_3.2 — Configured cycle policy and dependency cleanup

**Evidence:**

- [Configuration admission](<../../../mcp_server/config/schemas/contracts_config.py>)
- [Alternative phase/config behavior](<../../../tests/mcp_server/unit/config/test_contracts_config.py>)
- [Compact workflow behavior](<../../../tests/mcp_server/unit/tools/test_transition_phase_tool.py>)
- [Composition root](<../../../mcp_server/bootstrap.py>)

**Outcome:** Zero or one cycle-based phase is configured; Hotfix/Chore stay compact. State consumes IProjectPlanReader; passive decoder/detector state/status injections and independent entry/exit write hooks are removed. The subphase docstring describes pre-commit registration/rollback. Surgical instructions no longer require duplicate issue markers. No execute-time dependency construction or compatibility bridge was introduced.

## Evidence

### Complete native-configured suite

Native pytest configuration and eight xdist workers retained. 2,858 items; no selection partition or native argument override. This full run covers the b72922a6 production/test tree before the final test-only correction; it is not presented as a second full run on d16ebd8. The unchanged suite surfaces retain this evidence, while all three corrected test files have fresh independent evidence below.

**Sources:**

- [Configured tests](<../../../.pgmcp/config/tests.yaml>)
- [Native configuration](<../../../pyproject.toml>)

**Invocation:** run_tests(scope="configured", tests=["python_tests"], timeout_seconds=1800); args omitted.

**Observed Result:** 2856 passed, 1 skipped, 1 xpassed, 261 warnings; native exit 0; 533.00 seconds. Receipt 7b628326f3204ace9ef67ad81f4479fb.

### Required branch gates

Existing per-check configured_targets performs branch preselection. Native format: 64 files; production Mypy/Pyright: 21 files. Initial Markdown run before this report: 184 successful, 1 excluded, 0 errors (185 occurrences).

**Sources:**

- [Check configuration](<../../../.pgmcp/config/checks.yaml>)

**Invocation:** run_checks(scope="branch", checks=["python_format","python_lint","python_types","python_pyright","markdown_links"], timeout_seconds=600); args omitted.

**Observed Result:** All five checks passed, every native exit 0. Pyright: zero errors/warnings. Receipt a56428935c1a452280d2c9a8210566dc. Post-scaffold run_checks(scope="targets", targets=["docs/development/issue491/validation.md"], checks=["markdown_links"], timeout_seconds=600) also passed; no argument override.

### Final configured Python gates

Native format: 469 files already formatted; production Mypy/Pyright: 189 files.

**Sources:**

- [Gate selection and scope](<../../coding_standards/QUALITY_GATES.md>)

**Invocation:** run_checks(scope="configured", checks=["python_format","python_lint","python_types","python_pyright"], timeout_seconds=600); args omitted.

**Observed Result:** All four checks passed, every native exit 0; lint clean and Pyright zero errors/warnings. Receipt cf4378642c3648879029814177afe34d.

### Independent targeted closure of Implementation blockers

QA independently reran both complete files on b72922a6: 19 passed, 51 warnings, exit 0 in 37.31 seconds; all three checks passed. Private bootstrap access is removed, and both boolean approvals remain rejected through public model_validate without suppressions.

**Sources:**

- [Public-bootstrap demonstration](<../../../tests/mcp_server/integration/test_project_plan_readback.py>)
- [Approval admission behavior](<../../../tests/mcp_server/unit/tools/test_force_phase_transition_tool.py>)

**Invocation:** run_tests(scope="targets", targets=["tests/mcp_server/integration/test_project_plan_readback.py","tests/mcp_server/unit/tools/test_force_phase_transition_tool.py"], tests=["python_tests"], timeout_seconds=600); format/lint/Pyright on the same files.

**Observed Result:** Independent Implementation → Validation GO; receipts 2183e79be1c549c998ece1b6a15ac540 and 0271323192134b6d955e86e5bda96cb4. This verdict does not substitute for Validation approval.

### Final test-only correction and fresh affected-file evidence

Independent Validation QA on a30ac083 confirmed all nine broad checks and the full-suite outcome, but returned NOGO for seven existing uncoded type suppressions. Implementation C_3 was explicitly resumed for that correction only. The final diff replaces boolean constructor calls with public model_validate and offers the unsupported keyword through explicit dynamic dict[str, Any] input. All existing negative assertions remain; no production/configuration/helper change or new test was added. A Git-selected audit of every modified Python test file finds zero uncoded type ignores and zero file-level Ruff disable headers.

**Invocation:** run_tests(scope="targets", targets=["tests/mcp_server/unit/tools/test_transition_phase_tool.py","tests/mcp_server/unit/tools/test_cycle_tools.py","tests/mcp_server/unit/managers/test_phase_state_engine.py"], tests=["python_tests"], timeout_seconds=600); args omitted. Format/lint/Pyright use the same three targets.

**Observed Result:** Producer: 72 passed, 9 warnings, exit 0, 10.81 seconds; all three checks passed. Independent QA on d16ebd8: 72 passed, 9 warnings, exit 0, 10.75 seconds; all three checks passed; Pyright zero errors/warnings. QA closed the P2 and issued Implementation → Validation GO. Receipts fb0f6e3944024b2bac0cb0969d3963b5 and 38d4d24fce5f45a5b63ad45a4930c076 supplement these facts. This does not grant Validation approval.

**Reuse boundary:** The complete native suite was already executed and independently confirmed. Only the three negative-test invocation forms changed afterward; their complete files were rerun independently. No shared fixture, helper, import or production/configuration change invalidates the remaining suite surfaces. The broad check rows above keep their original snapshot/counts. After this revision, the same five branch checks and four configured Python checks were rerun with timeout_seconds=600 and no argument override: all nine passed. Receipts 4554fcbeae844a4d9bde59d060b71cfa and b408d42473474e56b426695852d3b0d4. Markdown validation of the final prose update also passed.

## Demonstration

Reproduce with run_tests(scope="targets", targets=["tests/mcp_server/integration/test_project_plan_readback.py"], tests=["python_tests"], timeout_seconds=600). The normal bootstrap precedes plan save. Four parameterized phase/cycle × normal/force cases use registered MCP handlers of the same server. Missing reader.py blocks the correct deliverable and preserves state. Create reader.py, replace the saved rule with revised.py and retry: the refreshed rule still blocks without restart. Create revised.py for normal success, or force with approval/reason and observe the current deliverable in skipped_gates. Outcomes are read from actual cached DTOs through the registered resource handler, not reconstructed from summaries.

## Preservation

Write-once initial creation and supported command/query ownership remain. The owner-approved input/storage/codec changes are a clean break; no old-format guarantees are claimed. The default full suite proves the integrated result beyond the focused demonstrations.

## Containment

All behavior fixtures use isolated temporary workspaces. No live planning mutation or forced workflow bypass was used for Validation. The earlier planning-loss incident was restored and investigated; no writer was proven. The owner directed one closed-pane full run and to stop investigating if planning stayed intact. That condition was met; no new incident repair or persistent diagnostic test was added.

## Failures

- The earlier full configured run had two failures: an obsolete Hotfix cycle-content assertion and a forced-history fixture entering Implementation without planning. Their existing tests were corrected in 5266982e; the full run above now has zero failures. The earlier failed run is not relabelled as passing.

## Caveats

- The suite retains one native skip, one non-strict XPASS and 261 warnings. QA reproduced the skip/XPASS in a separate diagnostic selection: the skip is the RUN_MANUAL_TESTS-gated proxy restart sketch in tests/mcp_server/core/test_proxy.py (no actual restart proof), and XPASS is the successful exclusion-note assertion with an older non-strict xfail marker in tests/mcp_server/unit/managers/test_enforcement_runner_unit.py. Neither proves an additional #491 obligation or blocks its selected behavior. No marker/assertion was weakened or repaired; native suite exit is 0.
- Git evidence protects attributable execution cycle identities, not completion. Unknown evidence rejects by default; force can override continued uncertainty only after retry, never known positive protection.
- Snapshot checks and existing atomic file writers do not guarantee transactions across processes/files. This issue adds no such guarantee.
- Other workspaces require deliberate direct format adjustment; no compatibility/migration tool is supplied. Active reference reconciliation belongs to Documentation.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-10 | @imp validator | Record full configured verification, structural mapping and public gate demonstration. |
| 1.1 | 2026-10-10 | @imp validator | Record final suppression correction, independent affected-file evidence and explicit full-suite reuse boundary. |
