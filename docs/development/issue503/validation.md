<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=KoFPQ3-cAAWFeesb -->

# Issue 503 — Validation observations and remaining failures

**Status:** VALIDATION — FAIL, REPAIR DECISION PENDING  
**Version:** 0.1  
**Last Updated:** 2026-10-15

## Purpose

Record observed outcomes against the approved clean break and preserve the repair boundary. This report grants no independent QA approval.

## Scope In

C_1 registration/state/PR changes, source-preserving validation, bounded consumer cleanup, active runtime cutover and the planned native configured verification.

## Scope Out

Compatibility, migration frameworks, broad warning cleanup, releases and implementation patches during Validation.

## Prerequisites

- Independent Implementation → Validation GO on b8f72b099f759113499b9b716d4ce2ac83ec6d49 after tracked instruction-source repair.
- Authoritative Planning v0.2, Design v0.1 and owner-approved Research strategy.
- Full verification ran on that production/test snapshot; only the normal Validation phase audit changed afterward.

## Issue Number

#503

## Cycle

C_1

## Validation Status

FAIL

## Scope

One complete configured suite; current branch review; separate configured production Mypy. Native arguments, workers and selection retained.

## Obligations

### D\_1.1 — Complete explicit registration, validated state mutation and repository parity

**Evidence:**

- [State repositories](<../../../mcp_server/managers/state_repository.py>)
- [Mutator behavior](<../../../tests/mcp_server/unit/managers/test_workflow_state_mutator.py>)
- [Handover/parent evidence](<../../../tests/mcp_server/unit/managers/test_phase_state_engine_parent_branch.py>)

**Outcome:** Focused public behavior evidence supports the contract. One broader resolver test still assumes branch-keyed in-memory absence; consumer completion is not certified.

### D\_1.2 — State-authorized PR targets before effects

**Evidence:**

- [PR behavior](<../../../tests/mcp_server/unit/tools/test_submit_pr_tool.py>)
- [Atomic submission flow](<../../../tests/mcp_server/integration/test_submit_pr_atomic_flow.py>)

**Outcome:** Focused success/authorization/rollback evidence passed. Two broader input/description tests still refer to removed PR fields; cleanup remains incomplete.

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

**Outcome:** Runtime and tracked instruction-source repair verified; three test consumers remain unresolved. File/key presence descriptors are not treated as semantic completion.

## Evidence

### Complete configured native suite

Pytest 9.0.2 completed with native configured testpaths tests/mcp_server and eight workers; no caller arguments, partitioning or timeout. Capture was not truncated.

**Sources:**

- [Native test configuration](<../../../pyproject.toml>)
- [Test binding](<../../../.pgmcp/config/tests.yaml>)

**Invocation:** run_tests(scope="configured", timeout_seconds=1200)

**Observed Result:** Native exit 1: 3 failed, 2927 passed, 1 skipped, 1 xpassed, 261 warnings in 310.73 seconds.

### Branch-wide gates

Check-specific branch preselection used the registered main parent. Passing branch Mypy does not certify unchanged production files.

**Sources:**

- [Configured check selection](<../../../.pgmcp/config/checks.yaml>)

**Invocation:** run_checks(scope="branch", timeout_seconds=600)

**Observed Result:** Passed python_review: python_format, python_lint, python_types and python_pyright; args_source=configured.

### Configured production Mypy

Both combined catches read e.error_code from PhaseEntryError | PlanningMutationError. The latter is an MCPError with code, not error_code. GitHub main was read directly during Validation and contains the same catch and domain-error definition; this is an existing main defect, not attributed to #503.

**Sources:**

- [Phase tool catches](<../../../mcp_server/tools/phase_tools.py>)
- [Domain error](<../../../mcp_server/schemas/deliverables.py>)
- [Observed main catch](<https://github.com/MikeyVK/phase-gate-mcp/blob/main/mcp_server/tools/phase_tools.py>)
- [Observed main domain error](<https://github.com/MikeyVK/phase-gate-mcp/blob/main/mcp_server/schemas/deliverables.py>)

**Invocation:** run_checks(scope="configured", checks=["python_types"], timeout_seconds=600)

**Observed Result:** Native exit 1: two union-attr errors in phase_tools.py at lines 239 and 336; 190 source files checked with Mypy 1.19.1.

### Focused implementation and cleanup evidence

Initial preservation RED selected seven cases and failed because source files moved. The six-file core group subsequently passed 143 tests. The phase/PR group had 85 passed and one fixture failure, followed by a passing targeted repair. The consumer group had 175 passed and four setup/caller failures; affected server/GitHub files then passed. Later repository/mutator/init/helper and repository/parent groups passed. Changed Python format/lint/Pyright, production Mypy and YAML checks passed. Workspace-root instruction copies passed native offline/cache/fragment link policy with an explicit workspace-root base; location-relative preflight failures were not called passes.

**Sources:**

- [Exact focused groups and gate policy](<planning.md>)
- [Primary behavior tests](<../../../tests/mcp_server/unit/managers/test_state_repository.py>)

**Invocation:** run_tests(scope='targets', tests=['python_tests'], timeout_seconds=600) on the Planning groups and affected repair files; changed Python file checks, production-only Mypy, YAML checks and instruction-link checks.

**Observed Result:** Focused implementation outcomes passed after local consumer repairs; this narrower evidence did not discover all three remaining test consumers.

## Demonstration

Controlled activation followed Planning: coherent code195f383 under old healthy PID36144/state1; final generic schema-only safe-edit reported written=True with validation not_executed; immediate restart. New healthy PID55532 accepted state2. Before any new-runtime state-writing commit, parsed comparison reported otherFieldsEqual=true and backupEqual=true: identity, progress and audit were unchanged, and no backup was created/changed. get_work_context and get_project_plan(503) succeeded. The client initially retained old public schemas, so activation commit waited for the owner's client restart. After refresh, healthy PID6712 and fresh metadata showed required parent_branch and submit_pr title/body/draft only. Complete plan names/descriptions/descriptors/literal exit criteria matched Planning before activation commit11cf166. Final instruction repair b8f72b0 changed only tracked signatures/audit.

## Preservation

Existing read-only interfaces, one injected lock/mutator, normal configured phases/cycles, exact-branch wrapper versus general handover reader, Ready admission, PR preparation/rollback/status, successful planning persistence and original diagnostic causes remain the intended boundaries. Source inspection found no production default_base_branch, reflog-parent inference, ignored reconstructor, placeholder bootstrap or automatic backup call. A producer-delegated findings-only source review found no concrete production issue; independent QA remains separate.

## Containment

No production/test patch was made in Validation. Post-suite git_status showed only .pgmcp/state.json's normal phase audit; get_project_plan(503) still read the complete project. Scope was not widened to repair warning categories or the pre-existing phase-tool error path.

## Failures

- test_workflow_status_resolver.py::TestWorkflowStatusResolver::test_resolve_raises_state_not_found_on_branch_mismatch: DID NOT RAISE StateNotFoundError. The test injects the general single-slot in-memory repository while expecting the retired branch-keyed absence behavior. Use the existing exact-branch wrapper and meaningful mismatch behavior, or remove duplicate obsolete coverage after comparing the existing mismatch case.
- test_extra_forbid.py::TestExtraForbidOnAllInputModels::test_extra_field_raises_validation_error[SubmitPRInput-valid_kwargs33]: its supposedly valid payload still contains removed head, so validation fails before the intended generic extra-field check. Correct the existing valid fixture.
- test_c4_description_invariants.py::TestC4DescriptionInvariants::test_submit_pr_base_documents_cascade: KeyError base. This content assertion describes the removed fallback cascade; retire the directly obsolete method without a replacement content test.
- Configured Mypy: phase_tools.py:239 and :336 read an unavailable error_code from PlanningMutationError. The same defect is present on main. It can also obscure an actual planning-domain diagnosis at runtime; owner scope/exception-routing decision is still pending.

## Caveats

- Validation is FAIL; passing branch gates and focused tests do not override failed full-suite/configured evidence.
- 261 warning occurrences include Pydantic schema-field shadowing, collection warnings, deprecated pathlib/read_resource APIs and restart-test asynchronous/SystemExit diagnostics. They were not all reclassified or repaired. One skip and one non-strict xpass are reported as observed, not converted to passes.
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
