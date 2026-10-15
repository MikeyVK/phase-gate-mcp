<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=KoFPQ3-cAAWFeesb -->

# Issue 503 — Validation outcomes and bounded repair

**Status:** VALIDATION — NATIVE VERIFICATION PASSED, INDEPENDENT REVIEW PENDING  
**Version:** 0.2  
**Last Updated:** 2026-10-15

## Purpose

Record observed outcomes against the approved clean break and preserve the repair boundary. This report grants no independent QA approval.

## Scope In

C_1 registration/state/PR changes, source-preserving validation, bounded consumer cleanup and active runtime cutover; the owner-approved C_2 test-consumer/diagnostic repair and renewed native configured verification.

## Scope Out

Compatibility, migration frameworks, broad warning cleanup, releases and implementation patches during Validation.

## Prerequisites

- Independent Implementation → Validation GO on b8f72b099f759113499b9b716d4ce2ac83ec6d49 after tracked instruction-source repair.
- The first attempt used Planning v0.2 and Design v0.1. Its failed outcomes remain below.
- The owner approved a bounded return to Planning, preserving C_1 and appending C_2. Research v1.1, Design v0.2 and Planning v0.3 record that amendment.
- Independent Planning GO on 60afe250ace33577f487fd7fc011bb62bffff403; independent C_2 Implementation → Validation GO on 5e4ee891e8f6d30d899d2c6e3f75343ee7852678.
- Renewed full verification ran on that latter production/test snapshot. Only the normal Validation phase audit changed before this report update.

## Issue Number

#503

## Cycle

C_1 and C_2

## Validation Status

Required native suite and gates passed on the repaired snapshot. Independent Validation review is pending; the initial attempt remains a recorded FAIL.

## Scope

One complete configured suite; current branch review; separate configured production Mypy. Native arguments, workers and selection retained.

## Obligations

### D\_1.1 — Complete explicit registration, validated state mutation and repository parity

**Evidence:**

- [State repositories](<../../../mcp_server/managers/state_repository.py>)
- [Mutator behavior](<../../../tests/mcp_server/unit/managers/test_workflow_state_mutator.py>)
- [Handover/parent evidence](<../../../tests/mcp_server/unit/managers/test_phase_state_engine_parent_branch.py>)

**Outcome:** Focused public behavior evidence and the renewed complete suite support the contract. C_2 retired the duplicate branch-keyed absence expectation while retaining the existing exact-branch wrapper mismatch test.

### D\_1.2 — State-authorized PR targets before effects

**Evidence:**

- [PR behavior](<../../../tests/mcp_server/unit/tools/test_submit_pr_tool.py>)
- [Atomic submission flow](<../../../tests/mcp_server/integration/test_submit_pr_atomic_flow.py>)

**Outcome:** Focused success/authorization/rollback evidence and the renewed suite passed. C_2 corrected the valid SubmitPR input fixture and retired the obsolete base-cascade content assertion.

### D\_1.3 — Failed-source preservation and exhausted backup cleanup

**Evidence:**

- [Repository behavior](<../../../tests/mcp_server/unit/managers/test_state_repository.py>)
- [Planning behavior](<../../../tests/mcp_server/unit/managers/test_project_manager.py>)
- [Query validator](<../../../mcp_server/managers/state_version_validator.py>)

**Outcome:** Existing corrupt/version planning-command matrix, repeated state reads, unreadable cause preservation and indirect plan/status reads support source/prior-backup preservation. Successful writes and persisted=True readback facts retained. No production backup_file caller remains; unrelated activation/upgrade backups retained.

### D\_1.4 — Bounded consumers, instruction parity and live activation

**Evidence:**

- [Explicit preparation helper](<../../../tests/mcp_server/test_support.py>)
- [Tracked Codex instructions](<../../agents/codex/AGENTS.md>)
- [Branch state](<../../../.pgmcp/state.json>)

**Outcome:** Runtime and tracked instruction-source repair verified. C_2 closed the three missed test consumers; full configured verification now passes. File/key presence descriptors are not treated as semantic completion.

### D\_2.1 — Complete remaining test consumer migration

**Evidence:** [Generic input behavior](../../../tests/mcp_server/unit/tools/test_extra_forbid.py), [retained exact-branch mismatch behavior](../../../tests/mcp_server/unit/managers/test_workflow_status_resolver.py) and [description-test cleanup](../../../tests/mcp_server/tools/test_c4_description_invariants.py).

**Outcome:** One valid fixture corrected and two obsolete methods removed; no replacement content or legacy-rejection test. The focused five-file family and renewed full suite passed.

### D\_2.2 — Preserve planning-domain diagnosis through existing wrappers

**Evidence:** [Phase tools](../../../mcp_server/tools/phase_tools.py) and [normal/forced public wrapped behavior](../../../tests/mcp_server/unit/tools/test_transition_phase_tool.py).

**Outcome:** PlanningMutationError is absent from the two PhaseEntryError catches and its unused import is removed. Both routes use the existing input/error wrappers to retain the original domain code, parameters, exception type and traceback. The one two-variant matrix was unchanged between intended RED and GREEN. No new production helper, error DTO, extractor, suppression or compatibility path was introduced.

## Evidence

### Complete configured native suite

Pytest 9.0.2 completed with native configured testpaths tests/mcp_server and eight workers; no caller arguments, partitioning or timeout. Capture was not truncated.

**Sources:**

- [Native test configuration](<../../../pyproject.toml>)
- [Test binding](<../../../.pgmcp/config/tests.yaml>)

**Invocation:** run_tests(scope="configured", timeout_seconds=1200)

**Initial Attempt:** Native exit 1: 3 failed, 2927 passed, 1 skipped, 1 xpassed, 261 warnings in 310.73 seconds.

**Renewed Result:** The same invocation after C_2 completed with native exit 0: **2930 passed, 1 skipped, 1 xpassed, 261 warnings in 394.35 seconds**. Pytest 9.0.2, eight workers, no caller arguments, no partitioning, no truncation, termination problem or request rejection. The two removed methods and two added behavior variants leave the collected case count unchanged.

### Branch-wide gates

Check-specific branch preselection used the registered main parent. Passing branch Mypy does not certify unchanged production files.

**Sources:**

- [Configured check selection](<../../../.pgmcp/config/checks.yaml>)

**Invocation:** run_checks(scope="branch", timeout_seconds=600)

**Observed Result:** Passed in both attempts. The renewed python_review run passed python_format, python_lint, python_types and python_pyright; args_source=configured.

### Configured production Mypy

In the initial attempt, both combined catches read e.error_code from PhaseEntryError | PlanningMutationError. The latter is an MCPError with code, not error_code. GitHub main was read directly during that attempt and contained the same catch and domain-error definition; the defect was not introduced by #503. The owner-approved C_2 repair now lets the planning-domain error reach the existing exception wrapper and leaves PhaseEntryError handling intact.

**Sources:**

- [Phase tool catches](<../../../mcp_server/tools/phase_tools.py>)
- [Domain error](<../../../mcp_server/schemas/deliverables.py>)
- [Observed main catch](<https://github.com/MikeyVK/phase-gate-mcp/blob/main/mcp_server/tools/phase_tools.py>)
- [Observed main domain error](<https://github.com/MikeyVK/phase-gate-mcp/blob/main/mcp_server/schemas/deliverables.py>)

**Invocation:** run_checks(scope="configured", checks=["python_types"], timeout_seconds=600)

**Initial Attempt:** Native exit 1: two union-attr errors in phase_tools.py at lines 239 and 336; 190 source files checked with Mypy 1.19.1.

**Renewed Result:** The same configured invocation passed: **Success: no issues found in 190 source files**, Mypy 1.19.1, native exit 0, args_source=configured, no truncation or termination problem.

### Focused implementation and cleanup evidence

Initial preservation RED selected seven cases and failed because source files moved. The six-file core group subsequently passed 143 tests. The phase/PR group had 85 passed and one fixture failure, followed by a passing targeted repair. The consumer group had 175 passed and four setup/caller failures; affected server/GitHub files then passed. Later repository/mutator/init/helper and repository/parent groups passed. Changed Python format/lint/Pyright, production Mypy and YAML checks passed. Workspace-root instruction copies passed native offline/cache/fragment link policy with an explicit workspace-root base; location-relative preflight failures were not called passes.

**Sources:**

- [Exact focused groups and gate policy](<planning.md>)
- [Primary behavior tests](<../../../tests/mcp_server/unit/managers/test_state_repository.py>)

**Invocation:** run_tests(scope='targets', tests=['python_tests'], timeout_seconds=600) on the Planning groups and affected repair files; changed Python file checks, production-only Mypy, YAML checks and instruction-link checks.

**Observed Result:** C_1 focused outcomes passed but did not discover the three remaining test consumers. C_2 then used exactly the following bounded route:

- RED: run_tests(scope="targets", targets=["tests/mcp_server/unit/tools/test_transition_phase_tool.py"], tests=["python_tests"], args={"python_tests": ["-k", "test_wrapped_transition_preserves_planning_domain_diagnosis"]}, timeout_seconds=300). Both normal/forced cases reached the tool and failed on the expected missing original error code after the faulty e.error_code access; no setup or collection failure.
- GREEN: run_tests(scope="targets", targets=["tests/mcp_server/unit/managers/test_workflow_status_resolver.py", "tests/mcp_server/unit/tools/test_extra_forbid.py", "tests/mcp_server/tools/test_c4_description_invariants.py", "tests/mcp_server/unit/tools/test_transition_phase_tool.py", "tests/mcp_server/unit/tools/test_force_phase_transition_tool.py"], tests=["python_tests"], timeout_seconds=600): **92 passed, 9 SchemaAttachment warnings, native exit 0 in 6.49 seconds**.
- run_checks(scope="targets", targets=[the five changed Python files listed under D_2.1/D_2.2], checks=["python_format", "python_lint", "python_pyright"], timeout_seconds=600): all passed. run_checks(scope="targets", targets=["mcp_server/tools/phase_tools.py"], checks=["python_types"], timeout_seconds=600): passed.
- RED commit 76a0c7df672ae63de32a736be158ae9ea703efbd; coherent GREEN commit 5e4ee891e8f6d30d899d2c6e3f75343ee7852678. No new test file or test helper.

## Demonstration

Controlled activation followed Planning: coherent code195f383 under old healthy PID36144/state1; final generic schema-only safe-edit reported written=True with validation not_executed; immediate restart. New healthy PID55532 accepted state2. Before any new-runtime state-writing commit, parsed comparison reported otherFieldsEqual=true and backupEqual=true: identity, progress and audit were unchanged, and no backup was created/changed. get_work_context and get_project_plan(503) succeeded. The client initially retained old public schemas, so activation commit waited for the owner's client restart. After refresh, healthy PID6712 and fresh metadata showed required parent_branch and submit_pr title/body/draft only. Complete plan names/descriptions/descriptors/literal exit criteria matched Planning before activation commit11cf166. Final instruction repair b8f72b0 changed only tracked signatures/audit.

C_2 used an ordinary source-runtime restart after the coherent GREEN commit. get_work_context was the first subsequent call and returned Implementation/C_2/green; health was healthy under PID56364, state schema2 remained active, and full get_project_plan(503) readback retained both cycles and phase blocks. No package build, state-envelope edit or client-schema refresh was required.

## Preservation

Existing read-only interfaces, one injected lock/mutator, normal configured phases/cycles, exact-branch wrapper versus general handover reader, Ready admission, PR preparation/rollback/status, successful planning persistence and original diagnostic causes remain the intended boundaries. Source inspection found no production default_base_branch, reflog-parent inference, ignored reconstructor, placeholder bootstrap or automatic backup call. A producer-delegated findings-only source review found no concrete production issue; independent QA remains separate.

## Containment

No production/test patch was made in either Validation attempt. The explicit owner-approved repair returned to Planning, added C_2, obtained independent Planning and Implementation GO decisions, then re-entered Validation. C_1 and phase blocks remained unchanged. After the renewed suite, git_status showed only .pgmcp/state.json's normal phase audit and get_project_plan(503) still read the complete project. Warning repair and unrelated presentation behavior were not added to C_2.

## Initial failures and C_2 resolution

| Initial observation | Bounded disposition | Renewed evidence |
| --- | --- | --- |
| Resolver branch-mismatch test expected StateNotFoundError from the general single-slot repository. | Removed that obsolete duplicate; existing BranchValidatedStateReader mismatch behavior remains. | Focused family and complete suite passed. |
| Generic SubmitPR valid fixture still contained removed head and failed before its intended extra-field check. | Removed head from the valid fixture. | Generic input behavior and complete suite passed. |
| SubmitPR base-cascade content assertion raised KeyError because base no longer exists. | Removed the obsolete method, import and coverage-list entry. | Remaining file and complete suite passed. |
| Configured Mypy reported two union-attr errors; the same catches could replace PlanningMutationError diagnosis with AttributeError. | Removed only PlanningMutationError from both catches and its import; retained PhaseEntryError. Existing outer wrapper owns diagnosis. | Intended RED, unchanged normal/forced GREEN matrix, focused gates, complete suite and configured production Mypy passed. |

No required test/check failure remains on the repaired snapshot. This statement records observed native outcomes, not independent QA approval.

## Caveats

- The initial attempt was FAIL. The renewed required suite and gates passed after the approved repair; independent Validation review remains pending.
- The renewed run reports 261 warning occurrences: Pydantic SchemaAttachment field shadowing, TestCapability/TestsConfig collection warnings, deprecated pathlib.is_reserved/read_resource APIs and an unawaited delayed_exit coroutine diagnostic. The earlier attempt also showed restart-related SystemExit diagnostics. These categories were not broadly reclassified or repaired. One skip and one non-strict xpass remain observed outcomes, not passes.
- Appending C_2 produced an unrelated informational presentation note about flat scalar sequence formatting policy/max_items. The operation and complete public readback confirmed the saved plan. This presentation note is a separate @co triage candidate, not repaired or treated as mutation uncertainty.
- Transient process-local caches are supplementary navigation only. Exact invocations, native outcomes, concrete failures and source/reproduction paths in this report are the durable evidence; no routine SHA requirement is imposed.
- Other workspaces need deliberate handling of the clean-break state envelope; no automatic migration or package release is introduced.

## Related Documents

- [Approved Research](<research.md>)
- [Approved Design](<design.md>)
- [Approved Planning](<planning.md>)
- [Quality evidence policy](<../../coding_standards/QUALITY_GATES.md>)
- [Architecture contract](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-15 | @imp validator | Record the complete configured suite, branch/configured gates, preservation/cutover evidence and concrete remaining failures without modifying implementation during Validation. |
| 0.2 | 2026-10-15 | @imp validator | Preserve the initial FAIL, record owner-approved C_2 and independent entry reviews, then report renewed complete configured suite and gates with all five failures resolved and warnings explicit. |
