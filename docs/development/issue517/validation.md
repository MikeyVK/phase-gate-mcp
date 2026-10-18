<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue 517 — Selected Stack Validation

**Status:** Initial Validation failed; C_3 focused recovery complete; renewed full Validation pending  
**Version:** 0.2  
**Last Updated:** 2026-10-18

## Purpose

Record the first complete selected-stack Validation and the bounded recovery required before progression.

## Scope Out

No release, active host upgrade, SDK1 compatibility matrix, broad suppression-policy repair or gate exception.

## Issue Number

#517

## Validation Status

FAIL

## Scope

Python3.15/SDK2.3 migration at commit32083d48206fc085fcc8b89681a229d3ab6ada6d on refactor/517-migrate-python315-mcp-sdk23. Research v0.4, Design v0.3, both planned cycles and independent Implementation-entry GO on b9910773.

## Obligations

### C\_1 — coherent SDK/prerequisite/consumer cutover

**Evidence:**

- [Server](<../../../mcp_server/server.py>)
- [Shared native client](<../../../tests/mcp_server/test_support.py>)
- [Dependency authority](<../../../pyproject.toml>)

**Outcome:** Focused SDK evidence and branch checks pass. Full-suite native-adapter and private-launcher consumers were missed by the earlier direct-SDK inventory; C_1 is not sufficient for final acceptance.

### C\_2 — proxy lifecycle and clean installed acceptance

**Evidence:**

- [Proxy behavior tests](<../../../tests/mcp_server/core/test_proxy.py>)

**Outcome:** Four focused lifecycle cases pass and real installed proxy acceptance passes. Three proxy cases fail in the full parallel run; parallel robustness remains unproven.

### Validation — complete native suite and branch/configured gates

**Evidence:**

- [Planning](<planning.md>)

**Outcome:** FAIL. Full suite and configured format/lint/Pyright are negative; no waiver or reduced threshold.

## Evidence

### Focused implementation preservation

Initial narrow old-host baseline11passed. Selected stack148SDKcases:143passed5failed; those5 consumers corrected and6targeted cases passed, including one new processing-diagnosis case. QA's missed isError fallback was corrected and1targeted success test passed. This is reused focused evidence, not a green full-suite claim.

**Sources:**

- [Consumer inventory](<research.md#source-and-test-impact>)

**Invocation:** Candidate run_tests(scope='targets', targets=the17 affected SDK files inventoried in Research, tests=['python_tests'], args={'python_tests':['-n','0']}, timeout_seconds=300); narrow6case repair recheck; later1case QA assert recheck.

### Proxy and installed-package controls

4focused cases passed14.93s. Wheel+sdist build and clean installation succeeded; pip check: no broken requirements. Neutral-CWD module path was installed-py315/Lib/site-packages/mcp_server. Actual initialized2025-11-25 route:49tools5resources; schema-compatible structured DTO, schema attachment and cache semantic roundtrip; unknown tool error, unknown resource code0; restart reached healthy with a different childPID. Both health childPIDs were absent after teardown. Invalid temporary config yielded exactly health_check/restart_server and original ERR_CONFIG/cause diagnosis; restored via safe_edit.

**Sources:**

- [Lifecycle tests](<../../../tests/mcp_server/core/test_proxy.py>)
- [Builder](<../../../scripts/build_package.py>)

**Invocation:** Candidate run_tests(scope='targets',targets=['tests/mcp_server/core/test_proxy.py'],tests=['python_tests'],args={'python_tests':['-n','0']},timeout_seconds=120); existing builder; clean wheel[dev]+check_jsonschema prerequisites install; pip check; isolated native Client against actual installed proxy/server.

### Single full configured suite

2912cases on8native workers, native exit1:2760passed82failed70errors, no skips,315.56s. Native combined coverage88% is below fail-under90; XML line-rate0.905 and branch-rate0.7768. Supplemental receipt55f309108a6842d49a88ddc0c783eeab; this report and native XML preserve the substantive evidence without depending on cache persistence.

**Sources:**

- [Native pytest configuration](<../../../pyproject.toml>)

**Invocation:** run_tests(scope='configured',tests=['python_tests'],args={'python_tests':['--cov=mcp_server','--cov-branch','-q','--junitxml=.pgmcp/temp/issue517/full-suite.xml','--cov-report=term','--cov-report=xml:.pgmcp/temp/issue517/coverage.xml']},timeout_seconds=1800); native client read window2100s.

### Required branch gates

All passed: Ruff0.17.1 formatting23Pythonfiles, lint, and Pyright1.1.414 on4selected productionfiles. Native configured branch preselection retained.

**Sources:**

- [Branch selection](<../../../mcp_server/execution/check_selection.py>)

**Invocation:** run_checks(scope='branch',checks=['python_format','python_lint','python_pyright'],timeout_seconds=600) on the real issuebranch/registered parentmain.

### Final configured Python gates

Mypy2.4 passed191productionfiles, retaining the native unused tests.* configuration note. Format failed:24files would change,603alreadyformatted. Lint failed:25diagnostics (ISC004,UP037,UP043,UP040). Pyright failed:one contextmanager Iterator-return deprecation in services/template_activation.py. Branch success does not supersede these workspace failures.

**Sources:**

- [Native config](<../../../pyproject.toml>)
- [Pyright config](<../../../pyrightconfig.json>)

**Invocation:** run_checks(scope='configured',checks=['python_types','python_format','python_lint','python_pyright'],timeout_seconds=600).

## Preservation

SDK knowledge remains in exactly server.py, core/proxy.py and utils/mcp_converters.py. No request_handlers consumers remain in tests. Structured content is the real operation DTO; text/resources/cache, error diagnosis, initialized protocol and explicit covariance retain their approved owners.

## Containment

Native checks/tests were invoked through the clean installed candidate MCP, using Python -I with the verification workspace as cwd. The exact real issuebranch, Validation state and clean commit were verified before the run. A temporary parking branch freed the branch for that managed worktree; the original checkout was restored cleanly and the parking branch deleted. Post-run candidate git_status confirmed no tracked/untracked source or workflow mutations. The verification worktree and ignored native XML evidence remain available for recovery. The active host/runtime was not upgraded.

## Failures

- 70setup errors:47Pyright cases require the removed Python-Pyright distribution for fixture provisioning;23commitlint/template/distribution cases cannot find worktree-local native Node prerequisites and fall back to an absent historical scratch path.
- 68native-adapter failures across Ruff checks28, Ruff fixes5, Pytest10 and Mypy25. They include hardcoded old version assertions (0.15.6/9.0.2/1.19.1) and Mypy2.4's additional native configuration note. Preserve meaningful native diagnostic/guard behavior; do not simply change or delete failing assertions without checking their purpose.
- 3startup/cutover failures require private .codex/config.toml from the author's active host. That dependency also risks choosing the old active interpreter instead of the selected target.
- 9parallel process failures:3new proxy cases plus6existing template-activation cases. Focused proxy controls passed, but full-load failures involve readiness/short5s or8s waits; reproduce and repair the test lifecycle/import/deadline boundary before claiming robustness.
- 1TypeScript dependency-absence case is affected by the temporary orchestration NODE_PATH leaking globally provisioned packages into a negative fixture.
- 1static requirements-dev content assertion rejects the approved metadata/extras authority despite native xdist running. Remove/adapt based on behavioral value, without adding a replacement version/content assertion suite.
- Configured format/lint/Pyright failures listed above require a bounded target-induced repair. New Ruff discovery also includes Markdown code blocks; the selection policy must be explicit before altering unrelated documentation.

## Caveats

- The direct SDK impact inventory was incomplete for upgraded native-tool/test provisioning consumers. Focused green evidence did not establish complete configured-environment readiness.
- Native XML is under .pgmcp/temp/issue517 in the managed verification worktree. It is supplemental local evidence; committed invocations, counts and causes above are the durable record.
- Neutral-CWD GitManager composition still uses its pre-existing cwd fallback: _build_manager_graph does not inject its workspace-root GitAdapter. Read-only check selection separately injects the workspace root correctly. Verification used Python-isolated installed imports with cwd at the workspace; no production fallback was changed.

## Deferred Work

### \#518 global/local suppression and type-policy repair

Remains blocked until #517 is completed, accepted and merged; this failure does not authorize broad suppression or covariance changes.

**References:**

- [Follow-up issue](<https://github.com/MikeyVK/phase-gate-mcp/issues/518>)

### Triage neutral-CWD GitManager composition separately

Existing root-injection defect observed during installed verification; outside the SDK-boundary strategy. Preserve the diagnostic and ask Coordinatie to triage instead of silently fixing it in this migration.

## Bounded Recovery Proposal

Return to Planning with explicit owner approval for force_phase_transition, retaining C_1/C_2 and their committed history. Add one repair cycle, reviewed independently before implementation:

1. Provision only the isolated validation environment with the required native Node packages/build prerequisites. Use ordinary workspace-native package resolution and remove the diagnostic driver's global NODE_PATH override so negative dependency controls remain isolated.
2. Adapt native-adapter evidence assertions to actual native results instead of old hardcoded version literals; preserve meaningful exact-version rejection and diagnostic-fidelity behavior. Replace the Pyright fixture's Python-wrapper lookup with native Node provisioning. Do not add a version-matrix/assertion suite.
3. Preserve startup/installed-catalog behavior tests while removing dependency on private active Codex configuration or its old interpreter. Use the selected interpreter and existing installed-distribution/public-process fixtures. Remove the obsolete requirements-dev text assertion rather than recreating it elsewhere.
4. Keep Client loading local to the protocol-test helper where that reduces unrelated subprocess startup cost. Reproduce parallel lifecycle failures and use readiness/termination observations with bounded budgets appropriate to the existing contract; no arbitrary sleeps as success proof.
5. Repair the concrete configured format/lint/contextmanager findings, reviewing unsafe suggestions for semantic equivalence. Preserve explicit covariance and existing suppression policy. Obtain an owner choice on newly discovered native Markdown formatting before modifying unrelated documents or narrowing discovery.
6. Run only affected test families and file gates during repair, request independent Implementation-to-Validation review, then rerun complete required Validation because the original full run failed and repairs invalidate it. Do not skip cases, lower coverage, disable new diagnostics or accept a gate exception.

No production behavior repair, neutral-CWD Git composition change or new architecture is presumed. A reproduced product defect or type-contract change reopens its exact decision.

## C_3 Recovery Evidence

The owner authorized the forced return to Planning for this and future sessions, explicitly chose Python-only native Ruff automatic discovery without force-exclude, and authorized targeted repairs at every existing adapter owner required by the selected upgrade. Independent QA approved C_3 at e801d5998f368e01b33c112086bd1e16a347ad00. C_1/C_2 and the failed full Validation above remain intact.

| Focused invocation / surface | Observed result |
| --- | --- |
| run_tests, targets: core/test_proxy.py and integration/test_template_activation.py; native eight workers, -q --tb=long; timeout600 | Baseline: 14 passed in49.95s. This alone did not reproduce the parallel failures. |
| run_tests, targets: affected native adapter, startup/install, proxy/activation and direct syntax-consumer families; native eight workers, -q --tb=long; timeout1200 | 333 passed,13 failed in401.09s. Native JUnit: .pgmcp/temp/issue517/c3-focused.xml. Preserved as diagnostic evidence. |
| run_tests, targets: integration/adapters/test_mypy.py, integration/adapters/test_pytest.py, integration/test_template_activation.py, core/test_proxy.py, integration/test_target_startup.py, integration/test_v3_cutover.py; native eight workers, -q --tb=long; timeout1200 | 99 passed,2 failed in196.81s; only Mypy report-cause stream assumptions remained. All process/startup/cancellation cases passed. Native JUnit: .pgmcp/temp/issue517/c3-recheck.xml. |
| run_tests, targets: integration/adapters/test_mypy.py; native eight workers, -q --tb=long; timeout600 | After cause extraction repair: all54 passed in40.11s. Native JUnit: .pgmcp/temp/issue517/c3-mypy-final.xml. |
| run_tests, targets: integration/execution/test_process_stopping.py and unit/test_c260_c2_state_root_injection.py; native eight workers, -q; timeout600 | 32 passed in24.61s. |
| run_checks, scope=targets, the40 changed Python files; checks=python_format,python_lint,python_pyright; timeout600 | All passed; Pyright1.1.414 reported40 analyzed files, zero errors/warnings/information. |
| run_checks, scope=configured, checks=python_types; timeout600 | Mypy2.4.0 passed191 production files. The native unused tests.* override note remains visible. |
| Existing scripts/build_package.py, selected Python3.15 | Real wheel and sdist built successfully; isolated --no-index --no-deps reinstall succeeded and pip check reported no broken requirements. No publication or active-host upgrade. |
| Rebuilt installed proxy, neutral CWD and initialized2025-11-25 |49 tools,5 resources; structured health/schema attachment, same-session cache fidelity and explicit tool/resource errors passed. Restart changed actual health PID67944 to20752 and remained healthy. Both modules resolved under the isolated site-packages; all5 observed proxy/child-wrapper/actual-server PIDs were absent after exit. |

Test paths in the table are relative to tests/mcp_server. Evidence is reused only where later edits did not change the tested surface; the forthcoming complete Validation remains mandatory.

### Reproduced causes and repairs

- Native prerequisite/fixture repair: provision worktree-local Node Pyright, TypeScript and commitlint plus build prerequisites; remove diagnostic NODE_PATH contamination. Native guards and deliberate missing-dependency controls stay effective. Pyright uses the declared native Node package instead of the removed Python wrapper.
- Native evidence assertions use the actual invoked native version/output. Remove the obsolete requirements-dev text assertion; retain meaningful native rejection, read-only/fix and complete-output behavior cases.
- Mypy2.4 reports a missing target as `absent.py: error: Cannot read file: No such file or directory`; the existing adapter now preserves execution_error/unavailable for both text and JSON diagnostics. Report-write traceback causes are extracted from the stream actually containing the traceback instead of accidentally selecting another stream's final hint. Complete stdout/stderr remain in evidence. Existing report cases explicitly request --show-traceback to prove cause retention.
- Shared test_support had eagerly imported the SDK Client for non-protocol consumers. Eight parallel activation-test module imports measured8.33s before and6.03s after localizing that import; all eight later imports omitted the SDK client. This proves avoidable coupling, not a claim that it alone explained every failure.
- The combined native run reproduced initialize_timeout in the proxy probes, whose test-only deadline was5s versus the existing production default30s. Tests now use the actual default; the silent-child deadline/rejection case and child cleanup remain required. Activation waits observe errors/exits immediately within30s; client windows include launcher startup before the unchanged production deadline. Nested cancellation observes worker/descendant readiness before cancellation, preserving the actual termination assertions. No arbitrary sleep is accepted as readiness and no production deadline changed.
- Startup/installed tests use the selected interpreter, initialized2025 protocol and existing public process/build seams, independent of private .codex/config.toml.
- Concrete Python3.15 format/lint/contextmanager findings were repaired at their existing owners. Implicit string concatenations remain single values via explicit parentheses; test-only type aliases are used only as annotations. Explicit covariance, diagnostic policy and existing suppressions remain intact.

No new permanent test module, SDK1 bridge, version-matrix suite, skip, reduced coverage or gate exception was added. One existing missing-file case gained JSON input coverage and the obsolete requirements-content test was removed. The neutral-CWD GitManager composition finding remains separately deferred. Full-suite/coverage and final configured gates are still pending renewed Validation.

## Related Documents

- [Approved Research](<research.md>)
- [Design](<design.md>)
- [Planning](<planning.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-18 | @imp validator | Record complete negative suite/configured gate evidence, clean checkout restoration and concrete missed consumer/provisioning boundaries. |
| 0.2 | 2026-10-18 | @imp implementer | Preserve failed full Validation and record owner-approved C_3 recovery, exact focused outcomes, native/process causes and pending complete revalidation. |
