<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue \#522 — Selected-workspace Git validation

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-10-19

## Purpose

Validate GREEN e97833d7 against Research1.1, Design1.2 and Planning1.1. This authored report does not grant independent QA approval.

## Scope In

C_1 D_1.1–D_1.4: explicit canonical Git composition; lazy exact/native worktree admission; existing history-unavailable contract; proportional consumer preparation; source and externally installed isolation.

## Scope Out

No repository discovery/router, compatibility path, host activation, release, configuration policy change, or issues523/524.

## Issue Number

#522

## Cycle

C_1

## Validation Status

FAIL

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

**Outcome:** MCPSystemError cause survives CommitHistoryUnavailableError; actual manager returns unavailable with no invented branch/head/protected cycles. Ten affected test modules select their own Git fixture without replacing assertions; obsolete shallow default-constructor case removed.

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

### Focused file gates

Ruff0.17.1 format/lint passed for19 changed Pythonfiles, with final four import-block corrections rechecked. Mypy2.4.0 and Pyright1.1.414 passed for bootstrap.py, adapters/git_adapter.py and managers/git_manager.py; zero Pyright errors/warnings. Mypy notes an existing unused tests.* configuration section in production-only selection.

**Sources:**

- [Production entry point](<../../../mcp_server/bootstrap.py>)

**Invocation:** run_checks(scope="targets", targets=[changed Python files], checks=["python_format","python_lint"], timeout_seconds=900); production-only targets for ["python_types","python_pyright"].

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

- First configured run: 2996 cases, 2959 passed, 27 failed and10 setup errors in572.38s, native exit1. Invocation: run_tests(scope='configured', tests=['python_tests'], args={'python_tests':['-q','--junitxml=.pgmcp/temp/issue522/validation.xml']}, timeout_seconds=1200). Additional direct/shared Git test preparation remains incomplete; Validation is blocked. Branch format/lint/Pyright passed; configured format/lint/Mypy/Pyright passed (475 format targets;192 source type targets). Return to existing C_1 for scoped consumer repair, then obtain independent Implementation→Validation review and repeat full native proof; no gate exception.
- No atomic guarantee against arbitrary concurrent filesystem/config replacement is added. Linked worktrees retain normal shared native repository metadata.

## Related Documents

- [Research](<research.md>)
- [Design](<design.md>)
- [Planning and exact gate routes](<planning.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-19 | @imp validator | Record causal correction, focused evidence and full Validation outcomes. |
