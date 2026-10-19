<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue \#522 — Selected-workspace Git validation

**Status:** REVIEW REQUESTED  
**Version:** 1.1  
**Last Updated:** 2026-10-19

## Purpose

Validate final source/test snapshot acd7c6bc (production correction e97833d7) against Research1.1, Design1.2 and Planning1.1. This authored report does not grant independent QA approval.

## Scope In

C_1 D_1.1–D_1.4: explicit canonical Git composition; lazy exact/native worktree admission; existing history-unavailable contract; proportional consumer preparation; source and externally installed isolation.

## Scope Out

No repository discovery/router, compatibility path, host activation, release, configuration policy change, or issues523/524.

## Issue Number

#522

## Cycle

C_1

## Validation Status

PASS

## Obligations

### D\_1.1: all existing Git consumers share the selected canonical workspace.

**Evidence:**

- [Bootstrap](<../../../mcp_server/bootstrap.py>)
- [Public startup/installed behavior](<../../../tests/mcp_server/integration/test_target_startup.py>)

**Outcome:** Public status and workflow context agree on A from foreign/neutral launch directories; non-Git A stays healthy and refuses Git use.

### D\_1.2: no ancestor/child/native fallback; selected writes remain bound.

**Evidence:**

- [Adapter](<../../../mcp_server/adapters/git_adapter.py>)
- [Native worktree behavior](<../../../tests/mcp_server/unit/adapters/test_git_adapter.py>)

**Outcome:** Distinct A/B snapshot proof covers real commits, native identity and later core.worktree drift. Eight inherited selector cases refuse both first and cached writes; unsupported roots refuse; nested/linked roots work; failed initial admission can retry after explicit repair.

### D\_1.3: history failure and valuable consumer behavior remain intact.

**Evidence:**

- [History evidence](<../../../tests/mcp_server/integration/test_git_cycle_evidence.py>)
- [Explicit shared test composition](<../../../tests/mcp_server/test_support.py>)
- [Opt-in Git preparation](<../../../tests/mcp_server/fixtures/suite_roots.py>)

**Outcome:** MCPSystemError cause survives CommitHistoryUnavailableError; actual manager returns unavailable with no invented branch/head/protected cycles. Nineteen affected test modules select their own Git fixture without replacing assertions; obsolete shallow default-constructor case removed.

### D\_1.4: installed package operates on another target without package installation inside it.

**Evidence:**

- [One-wheel installed scenario](<../../../tests/mcp_server/integration/test_target_startup.py>)

**Outcome:** Public git_status/get_work_context and create_branch operate on A from neutral and foreign B CWD; B HEAD/index/file/refs remain identical.

## Evidence

### Causal RED and focused GREEN

RED commit2b10b93b: three intended failures (wrong foreign branch; foreign success for non-Git A; missing selector/history refusal). Same cases pass after correction. Final five-file core run adds unit/adapters/test_git_adapter.py, unit/managers/test_git_manager.py and unit/server/test_bootstrap.py with -q:162 passed in194.92s, exit0.

**Sources:**

- [Tests](<../../../tests/mcp_server/integration/test_target_startup.py>)

**Invocation:** run_tests(scope="targets", targets=["tests/mcp_server/integration/test_target_startup.py","tests/mcp_server/integration/test_git_cycle_evidence.py"], tests=["python_tests"], args={"python_tests":["-q","-k","selected_workspace_git or admission_conflict"]}, timeout_seconds=900)

### Direct Git and helper consumer preservation

43 passed43.52s: unit/adapters/test_git_adapter_neutralize_to_base.py, test_git_adapter_skip_paths.py; unit/execution/test_check_selection.py; integration/test_model1_branch_tip_neutralization.py, test_workflow_cycle_e2e.py. 66 passed30.67s: unit/tools/test_project_tools.py, test_initialize_project_tool.py, test_cycle_tools.py, test_cycle_tools_business_logic.py (-q --tb=short). 158 passed41.28s: unit/managers/test_project_manager.py, test_phase_state_engine.py, test_phase_state_engine_parent_branch.py, test_phase_state_engine_persistence.py, test_phase_state_engine_workflow.py, test_state_repository.py (-q --tb=short). Paths are relative to tests/mcp_server/.

**Sources:**

- [Test families](<../../../tests/mcp_server>)

**Invocation:** run_tests(scope="targets", tests=["python_tests"], args={"python_tests":["-q"]}, timeout_seconds=900), using the file groups below.

### Consumer recovery after the first full run

The first configured run on the e97833d7 source/test tree returned 2996 cases: 2959 passed, 27 failed, 10 setup errors, zero skips, native exit1 in572.38s. All37 negative cases contain the missing target-Git diagnosis; twelve surface through planning_readback_failed. This negative outcome was committed in98c67942 before the audited return to existing C_1 (zero skipped gates).

Commit acd7c6bc adds explicit git_workspace selection in nine further modules and gives the shared fixture a real local baselinecommit with explicit identity. Production code and existing assertions remain unchanged. Independent QA authorized Implementation→Validation again on this snapshot; the complete configured run is repeated, not waived.

- Nine repaired families: integration/templates/test_planning_artifact.py; integration/test_context_loaded_enforcement.py; integration/test_project_plan_readback.py; unit/managers/test_phase_state_engine_c2.py, test_phase_state_engine_c3.py, test_phase_state_engine_c4_issue257.py; unit/test_server.py; unit/tools/test_force_phase_transition_tool.py, test_transition_phase_tool.py. Paths are under tests/mcp_server/.
- Reproduction: run_tests(scope="targets", targets=[these nine files], tests=["python_tests"], args={"python_tests":["-q","--tb=short"]}, timeout_seconds=900):75 passed in86.61s, exit0.
- The ten earlier fixture consumers listed above were rerun with the same -q --tb=short route:224 passed in69.93s, exit0. Focused format/lint on the ten changed recovery Pythonfiles passed.

### Focused file gates

Ruff0.17.1 format/lint passed for19 changed Pythonfiles, with final four import-block corrections rechecked. Mypy2.4.0 and Pyright1.1.414 passed for bootstrap.py, adapters/git_adapter.py and managers/git_manager.py; zero Pyright errors/warnings. Mypy notes an existing unused tests.* configuration section in production-only selection.

**Sources:**

- [Production entry point](<../../../mcp_server/bootstrap.py>)

**Invocation:** run_checks(scope="targets", targets=[changed Python files], checks=["python_format","python_lint"], timeout_seconds=900); production-only targets for ["python_types","python_pyright"].

### Full configured acceptance after recovery

```python
run_tests(
    scope="configured",
    tests=["python_tests"],
    args={"python_tests": ["-q", "--junitxml=.pgmcp/temp/issue522/validation.xml"]},
    timeout_seconds=1200,
)
```

On acd7c6bc: **2996 passed in535.40s (8m55s), native exit0**. The JUnit readback confirms2996 tests, zero failures, zero errors and zero skips. Native selection remains tests/mcp_server, Python3.15.0, pytest9.1.1, eight xdist workers, without coverage opt-in or extra exclusions. Captured stderr includes the informational child_exited line; native pytest completed successfully.

The complete suite includes the public source/installed isolation and native/history controls above, so another demonstration run would duplicate fresh proof. The previous failed run and scoped repair remain recorded; final acceptance uses the repaired snapshot.

### Final branch and configured gates

On the acd7c6bc source/test snapshot:

| Invocation | Native outcome |
| --- | --- |
| run_checks(scope="branch", checks=["python_format","python_lint","python_pyright"], timeout_seconds=900) | All passed; production Pyright has zero errors/warnings. |
| run_checks(scope="configured", checks=["python_format","python_lint","python_types","python_pyright"], timeout_seconds=1200) | All passed:475 format targets, lint clean, Mypy192 source files, Pyright192 source files with zero errors/warnings. |

Native tools: Ruff0.17.1, Mypy2.4.0 and Pyright1.1.414. The existing Mypy unused tests.* section is an informational note, not a new failure. Native quality policies, coverage opt-in and thresholds were not changed.

## Demonstration

Reproduce the installed case in integration/test_target_startup.py with run_tests(scope='targets', targets=[that file], tests=['python_tests'], args={'python_tests':['-q','-k','installed_candidate']}, timeout_seconds=900). It builds one isolated wheel and launches the selected interpreter against a separate workspace; it never mutates the owner's nonselected repository.

## Preservation

Public tool DTOs, state/config/scope contracts, native identity/credentials/user/system policy, proxy/CLI/install modes and the #520 startup admission remain unchanged. GitManager and GitAdapter construction make a clean break; no aliases or legacy routes.

## Containment

All scenario repositories/configs/builds live under pytest tmp_path. Installed local-Git proof explicitly deletes only the online PR-status rule in its disposable config using the existing $delete mechanism; other admission rules remain. Production enforcement/config are unchanged and no live GitHub request is needed.

## Failures

- Before causal RED, a setup assumed a wholly external server-data folder. ArtifactTargetResolver correctly rejected it before Git; audited Research1.1/Design1.2/Planning1.1 constrain server data to the workspace. This is not counted as Git RED.
- Initial disposable foreign-repository setup read a nonexistent empty index; an initial tracked file corrected that preparation before causal RED.
- An added commit-content assertion assumed LF bytes on Windows. It now verifies the semantic committed text independently of native line-ending policy.
- Initial installed mutation reached the native online PR-status check without a token. The disposable local-Git scenario now explicitly removes that external-service rule; no product/config policy was weakened.
- Affected project/state/cycle fixtures had no target Git repository and had implicitly used launch Git. Explicit opt-in target repositories repair their preparation; existing behavior assertions remain.

## Caveats

- Final native full-suite and branch/configured acceptance pass. No new release or active host installation was performed.
- No atomic guarantee against arbitrary concurrent filesystem/config replacement is added. Linked worktrees retain normal shared native repository metadata.

## Related Documents

- [Research](<research.md>)
- [Design](<design.md>)
- [Planning and exact gate routes](<planning.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-19 | @imp validator | Record causal correction, focused evidence and first full-suite FAIL. |
| 1.1 | 2026-10-19 | @imp validator | Preserve the scoped consumer recovery and record final 2996-case configured acceptance and broad gates. |
