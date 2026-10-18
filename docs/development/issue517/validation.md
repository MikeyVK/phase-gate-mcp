<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue 517 — Selected Stack Validation

**Status:** Actual90% and checks pass; one lifecycle test setup race remains
**Version:** 0.10  
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

No new permanent test module, SDK1 bridge, version-matrix suite, skip, reduced coverage or gate exception was added. One existing missing-file case gained JSON input coverage and the obsolete requirements-content test was removed. The neutral-CWD GitManager composition finding remains separately deferred. At C_3 closure, complete Validation was still pending; its executed result is recorded below.

## Post-C_3 Complete Validation

**Outcome: FAIL under the current #517 Planning acceptance.** The exact tested snapshot was `94cc5638be0493f2d6d9ebb27652d8c2892724ce`, with all three cycles retained, Validation active and a clean real issue branch in the isolated verification worktree. No source/workflow files changed during verification; the final native git_status was clean and the primary checkout was restored afterward.

The actual installed candidate ran:

```text
run_tests(scope="configured", tests=["python_tests"],
  args={"python_tests":["--cov=mcp_server","--cov-branch","-q",
    "--junitxml=.pgmcp/temp/issue517/full-suite-retry.xml",
    "--cov-report=term","--cov-report=xml:.pgmcp/temp/issue517/coverage-retry.xml"]},
  timeout_seconds=1800)
```

| Required selection | Native result |
| --- | --- |
| Complete suite, native eight workers |2911 passed,1 failed,0 errors,0 skips in483.07s; native exit1. JUnit contains2912 cases. |
| Opt-in combined line/branch coverage |87.93%, below the configured90%. XML:13100/14456 lines,3019/3876 branches; line-rate0.9062, branch-rate0.7789. No threshold, source selection or exclusion was changed. |
| run_checks(scope="branch", checks=["python_format","python_lint","python_pyright"], timeout_seconds=600) |All passed:61 Python formatting/lint targets; Pyright24 production files, zero diagnostics. |
| run_checks(scope="configured", checks=["python_types","python_format","python_lint","python_pyright"], timeout_seconds=600) |All passed: Mypy191 production files; formatting474 files; lint passed; Pyright191 files, zero diagnostics. The native unused tests.* override note stays visible. |

The sole failing case is `tests/mcp_server/integration/test_target_startup.py::TestTargetStartup::test_installed_candidate_init_migration_and_mcp_handshake`. Its fresh-installed client still uses the helper's30s default at the `run_server_process(launch, cwd=fresh, env=fresh_env)` call; a second installed route has the same default. The failure captured proxy_started, server_spawned and server-starting diagnostics before the client deadline. The already repaired source-startup route has an explicit45s client window. A directed repair must cover the remaining installed callers and retain the unchanged production initialization deadline.

### Coverage acceptance decision reopened

The native test binding has default_args=[]; pyproject's addopts does not request coverage and explicitly documents coverage as opt-in. [Issue507's complete Validation](../issue507/validation.md) records2913 passing cases with the normal configured invocation and no caller coverage arguments. Thus there is no measured pre-upgrade coverage baseline in that acceptance evidence. The present87.93% is an observed shortfall, not proof that this migration reduced coverage.

The producer added --cov/--cov-branch as mandatory #517 Planning acceptance without first establishing that baseline. Owner choice has been requested: either restore normal complete configured-suite acceptance while recording the coverage shortfall for explicit follow-up, or retain the added coverage gate and investigate/remediate it within #517. The owner explicitly chose to retain the extra90% gate and investigate/restore coverage within #517. This closes the policy question without relaxing acceptance; the current plan still fails and no next-phase approval is claimed. Investigate measurement completeness and actual behavioral gaps. Do not lower90%, add exclusions or create a broad collection of metric-only tests.

The remaining startup repair requires an earlier-phase recovery; the owner's standing force-backtransition approval is recorded in AGENTS.md. No production/test patch has been made in this Validation phase and no gate exception has been applied.

## C_4 Recovery Evidence

The owner retained the extra90% combined line/branch gate. Independent QA approved Planning at cc79277e4b1c8cea0abaade180d56ef37d744989; C_4 re-entry is recorded in8d94c26f. C_1–C_3 and both negative complete runs remain unchanged. No production source has changed in C_4.

### Native measurement

pytest-cov7 removed automatic subprocess measurement. The existing14 proxy/activation cases passed before and after coverage.py patch=["subprocess"]: native reports23.36% and23.70% for that limited selection, with47 additional covered lines and15 branches (42 lines in template activation). These small selections intentionally do not satisfy the workspace-wide90% gate; native exit1 is retained rather than reported as a gate pass.

Directory-based source selection becomes absolute when native coverage configuration is serialized into children. To measure the same package in source and installed launches, native source_pkgs=["mcp_server"] and --cov without a value preserve package identity. Standard coverage.paths maps the checkout, */installed/mcp_server and */site-packages/mcp_server; no source exclusions or threshold changes are introduced. All191 source Python files matched the isolated installed package as text; two files differed only in line endings. Native package-entrypoint reporting completed without missing-source errors or duplicate installed paths. Windows forcible termination still cannot guarantee a child flush; no production shutdown change or private instrumentation was added.

### Focused behavior

| Selection through actual candidate run_tests | Outcome |
| --- | --- |
| Proxy and template activation,14 existing cases, native parallelism |14 passed before/after measurement change (87.54s/67.13s native summaries). |
| Target startup and v3 cutover, eight cases, explicit45s installed client windows |8 passed in148.97s. |
| Package source/installed entrypoints, two existing cases with package-based measurement |2 passed in54.45s; native no-data warnings from idle workers remain visible. |
| Four changed component families: proxy, target startup, Git adapter and typed presentation |84 passed in135.13s. Seven subsequently identified duplicate projection scenarios were removed; retained scenarios reuse this evidence until their surface changes. |
| Existing real-process cleanup/serialization cases, strengthened result-provenance checks |First six selected cases passed in10.85s. Whole-family retry:34 passed,2 new assertions failed because interrupted test/fix messages are legitimately optional. Corrected those new test assumptions without changing production policy. A subsequent38-case diagnostic had37 passed and one further over-strict test success-flag assertion; that assertion was also corrected. Final scoped closure is recorded below. |

The catalog test now observes actual initialized listing, valid published schemas where present and structured health data validated as HealthCheckOutput. It does not invent a requirement that every tool advertises outputSchema: the existing normal decorator stack does not forward that metadata. This is a separate finding for coordination, not a new production change or a claim that structured DTO delivery failed.

New public proxy scenarios prove recovery after malformed frames and child cleanup on EOF, interruption and IO failure. One temporary-local-remote Git scenario proves actual GitPython tracking/fetch/pull, stash content preservation and commit/merge ancestry. Typed-projection admission adds only previously uncovered cases; public result tests reject fabricated native facts, missing invocation identity, duplicate rows and contradictory operation/refusal claims. No test asserts dependency versions or source text; no compatibility scenario or new permanent test module was added.

### C_4 focused closure

run_tests(scope="targets", targets=the ten changed Python test files, tests=["python_tests"], args={"python_tests":["-q","--junitxml=.pgmcp/temp/issue517/c4-final-focused.xml"]}, timeout_seconds=1200) completed with223 passed, zero failures/errors/skips, native exit0 in125.54s. This is a focused family selection, not full Validation.

The final native format/lint/Pyright checks on those ten files all passed; Pyright1.1.414 reported ten files and zero diagnostics. An initial fixture inherited and narrowed a mutable field; it was corrected to an independent frozen model without an ignore or production change. Its17-case presentation family then passed again in7.53s with native exit0 (c4-projection-typed-final.xml); unchanged family evidence is reused.

Additional bounded diagnostics retained native XML evidence:74 Git/proposal cases passed in16.34s (c4-preservation.xml);98 check/edit/runtime cases passed in13.94s (c4-contract-final.xml);18 IO cases passed in9.61s (c4-file-io-final.xml). Their opt-in coverage calls correctly returned native exit1 because these limited families do not cover the full package; no --cov-fail-under override was used.

Native coverage precision is now2, with fail_under=90 unchanged: whole-percent rounding must not make89.6% satisfy the retained90% requirement. Both direct and proxy entrypoints are observed in the existing source/installed scenarios. The ten edited families contain223 cases versus177 before C_4, a net46 additional behavior cases; no permanent test module was added. Seven duplicate new projection scenarios, one old protocol-instance assertion and obsolete negative V2 tool/config assertions in touched startup tests were removed.

The pre-migration active installed server also uses optional output_model metadata to publish outputSchema, and its normal decorators do not forward that metadata. Thus the catalog observation predates this SDK cutover. Preserve it as a coordination finding; structured DTO delivery and conditional schema preservation are proven separately, without silently changing the wrapper contract.

Full90% acceptance remains unproven and is owned by renewed complete Validation. C_4 made no production-source edit, threshold reduction, exclusion/skip, suppression, private measurement hook, new dependency or active-host switch. The existing coherent installed wheel remains valid for target RPC because production code is unchanged. Required complete suite/coverage and branch/configured gates follow only after independent Implementation → Validation GO.



## Post-C_4 Complete Validation

**Outcome: FAIL.** Independent QA approved Implementation to Validation on `59878795a40905c6d3092d75fdfab54e977a1e91`. The exact tested snapshot was `3ab7be16e9778b0f8c572ffd4e258321f0ca5af6`, with Validation active, all four planning cycles intact and a clean issue branch. The final native git_status remained clean.

```text
run_tests(scope="configured", tests=["python_tests"],
  args={"python_tests":["--cov","--cov-branch","-q",
    "--junitxml=.pgmcp/temp/issue517/full-suite-c4.xml",
    "--cov-report=term","--cov-report=xml:.pgmcp/temp/issue517/coverage-c4.xml"]},
  timeout_seconds=1800)
```

| Required selection | Native result |
| --- | --- |
| Complete suite, native eight workers |2956 passed,2 failed,0 errors,0 skips;2958 cases, native exit1 in586.50s. |
| Combined line/branch coverage, precision2 |89.94%, below90%;13348/14456 lines and3139/3876 branches. Threshold/source/branch scope unchanged. |
| Branch format/lint/Pyright, timeout600 |All passed:66 formatting/lint targets;24 production Pyright files, zero diagnostics. |
| Configured Mypy/format/lint/Pyright, timeout600 |All passed: Mypy191 production files, formatting474 files, lint passed and Pyright191 files with zero diagnostics. The native unused tests.* override note remains visible. |

The first failure is the installed initialization/migration/planning-readback test at `test_target_startup.py:406`. Its45s client received the real proxy `ERR_SERVER_UNAVAILABLE` with reason `initialize_timeout`; extending the client again would not repair this. Retained native audit events show child PID47628 spawned at13:04:18.388UTC, reached bootstrap's starting message at13:04:36.360 and exceeded the unchanged30s proxy initialization deadline at13:04:48.429. No ready event preceded the deadline. Other source and installed startup controls in the same run became ready in approximately21s and17s. These observations establish a load/instrumentation-sensitive initialization failure, not a proven production deadlock or authorization to change production timing.

The second failure is `integration/adapters/test_pytest.py::test_native_coverage_is_opt_in_and_owns_threshold_rejection`: a literal assertion against the repository's old coverage.run dictionary fails before the valuable native behavior assertions. Remove that content coupling while retaining the direct/adapter opt-in and native threshold rejection proof. Do not replace it with a new exact config-content assertion.

The89.94% result remains negative. The failed installed test did not execute its planning/cache/migration body; repair the failures and inspect fresh native coverage before adding any further behavior cases. No gate exception, reduced threshold, skip, source exclusion, production patch or additional test case was applied in Validation. Native XML under .pgmcp/temp/issue517 is supplemental; the snapshot, invocations, observations and counts here are the durable evidence.

## C_5 Focused Recovery

Independent QA approved C_5 Planning on `0104cd720d3a07f1cb3b2cc3101ce0a1eb987bf9`. Only two existing test files changed. The installed functional migration/readback probe uses the existing public MCPProxy constructor with90s initialization and120s client windows; production default30, default module-entrypoint tests and explicit silent-child rejection remain unchanged. This probe establishes functional behavior under instrumentation, not a30s startup guarantee.

The existing Pytest coverage-conformance case retains actual native and adapter opt-in/threshold proof. Its obsolete repository-config equality and unused tomllib import were removed. Instrumented evidence then exposed its synthetic package's mcp_server name in production coverage (four sample lines/two branches); rename only that isolated fixture to coverage_example. The production coverage selection was not changed.

| Actual candidate MCP selection | Result |
| --- | --- |
| run_tests(scope="targets"), target_startup.py, integration/adapters/test_pytest.py, core/test_proxy.py; -q --junitxml=.pgmcp/temp/issue517/c5-focused.xml; timeout900, native eight workers |38 passed,1 failed in161.90s. The repaired startup/coverage cases and all proxy controls passed. One unchanged native xdist subprocess exceeded its45s helper budget. |
| Same two affected files, -k "installed_candidate_init_migration_and_mcp_handshake or native_coverage_is_opt_in_and_owns_threshold_rejection or (native_outcomes_and_options and xdist)", --cov --cov-branch -q, c5-instrumented.xml and c5-instrumented-coverage.xml; timeout900, native eight workers |All3 cases passed in138.64s; the previously timed-out xdist case completed in12.44s. Native exit1 correctly reflects narrow42.71% coverage, not a test failure. No xdist timeout was changed and the prior failure stays visible. |
| Pytest-adapter file only, -k native_coverage_is_opt_in_and_owns_threshold_rejection, --cov --cov-branch -q, c5-coverage-isolation.xml and c5-coverage-isolation-coverage.xml; timeout300 |1 passed in23.00s after fixture rename; native exit1 for narrow17.43% coverage. XML contains no temporary synthetic mcp_server package. |
| run_checks(scope="targets"), both edited test files, python_format/python_lint/python_pyright; timeout600 |All passed; Pyright two files, zero diagnostics. An initial ISC004 in the new launch string was repaired with explicit parentheses. |

Paths above are relative to tests/mcp_server except native evidence outputs under .pgmcp/temp/issue517. Earlier passing cases are reused only where the subsequent parentheses/isolated-fixture edits cannot change their behavior. No new permanent case/module or production code was added in C_5.

Comparison of the instrumented startup probe with the failed full run found no additional covered production lines/branches. The89.94% shortfall therefore remains substantively unresolved; no further full run is justified solely by these two repaired failures. Plan a minimal additional public proxy behavior gap: malformed replacement initialization and changed negotiated protocol. Preserve default deadline, actual child termination and factual error output; no metric-only assertions or new architecture.

## C_6 Focused Closure

Independent QA approved Planning on `1f1d36fb06f9ac79fdc98c87aaad41d307e09100`. Exactly two parameter cases were added to the existing proxy failed-replacement test: malformed JSON initialization output and a structurally valid result changing the negotiated protocol. The existing public process factory supplies real controlled children. Assertions observe restart_failed reason/original diagnosis, no restart_completed, subsequent ERR_SERVER_UNAVAILABLE/unavailable and bounded cleanup of every real child. No production/config/default-deadline change, private calls or new permanent module.

Actual candidate invocation:

```text
run_tests(scope="targets", targets=["tests/mcp_server/core/test_proxy.py"],
  tests=["python_tests"],
  args={"python_tests":["-q","--cov","--cov-branch",
    "--junitxml=.pgmcp/temp/issue517/c6-proxy.xml",
    "--cov-report=term","--cov-report=xml:.pgmcp/temp/issue517/c6-proxy-coverage.xml"]},
  timeout_seconds=300)
```

All10 cases passed, zero failures/errors/skips in50.25s. Native exit1 is the correct global threshold rejection for this narrow16.11% selection; no coverage-gate override was passed. Native XML shows the intended previously unmeasured protocol-change rejection and initialize-stdout parse-failure paths executed. A diagnostic comparison with the last full run finds ten additional production lines and three additional branch destinations; that comparison is not a combined acceptance result or a guarantee of final90%.

run_checks(scope="targets", targets=["tests/mcp_server/core/test_proxy.py"], checks=["python_format","python_lint","python_pyright"], timeout_seconds=600) passed all three; Pyright one file, zero diagnostics. Document edits pass their native link checks. C_5's unchanged family/control evidence is reused with its recorded negative xdist timeout and later passing targeted recheck; complete parallel stability and total coverage remain obligations of full Validation.

Implementation recovery is complete within C_5/C_6. Both earlier C_4 full failures and the negative89.94% remain visible. Independent Implementation → Validation review is required before the next full run. No release, active-host switch, compatibility/version matrix, skip, new suppression, threshold/source/parallelism reduction or gate exception is included.

## Post-C_6 Complete Validation

**Tests and checks pass; strict90% acceptance remains FAIL.** Exact clean tested snapshot: `077c922092f9b603ccfb080bd5dc4a03c513710f`, after independent Implementation GO on d2c1d8b. All six cycles remained intact and post-run git_status was clean.

The same complete configured invocation used --cov --cov-branch -q, timeout1800 and native eight workers, with JUnit .pgmcp/temp/issue517/full-suite-c6.xml and coverage .pgmcp/temp/issue517/coverage-c6.xml.

| Required evidence | Observed result |
| --- | --- |
| Full configured tests |2960 passed, zero failures/errors/skips in513.20s; native exit0 and adapter status passed. |
| Actual combined line/branch coverage |13357/14456 lines and3141/3876 branches:16498/18332 =89.9956360462579%, below90%. No synthetic paths appear in XML. |
| Native reporting discrepancy |Terminal displays90.00% plus FAIL Required test coverage not reached; pytest-cov's exit decision rounds to configured precision2, so native exit0 disagrees with the raw comparison in its terminal summary. This is native rounding, not evidence that the adapter invented an exit code. |
| Required branch format/lint/Pyright |All passed;66 format/lint targets,24 production Pyright files, zero diagnostics. |
| Configured format/lint/Pyright |All passed;474 format files and191 Pyright files, zero diagnostics. |
| Configured production Mypy |Reuse post-C_4 passing191-file result; production source/Mypy configuration unchanged in C_5/C_6. Native unused tests.* note remains visible. |

Installed migration, native opt-in coverage, xdist and proxy replacement cases all passed in this complete run. The earlier xdist timeout remains historical evidence, not a current failure. Native tool status/exit alone is insufficient here: the owner's actual90% requirement is not reached by the raw counts, so no forward phase request was made.

The installed pytest-cov plugin at its runtest-loop calls coverage.results.should_fail_under(total,fail_under,precision), whereas its terminal summary uses total < fail_under before formatting to two decimals. Precision2 can therefore round this one-hit shortfall into a zero exit while printing FAIL. Tighten report precision to6 without changing the threshold, measured package, branch scope or exclusions. One additional genuine public proxy obligation remains unproved: an explicit JSON-RPC initialize error from a replacement must be rejected with its original response diagnosis. Plan that single scenario in the existing parameterization, not a percentage/version assertion.

## C_7 Focused Closure

Independent QA approved Planning on4bb4592939591fb681a7cc0f51c9eeee6fb07a15. Only native coverage.report.precision changed2→6, and one existing failed-replacement parameter was added. fail_under=90, source/branch/subprocess/path configuration, exclusions, production defaults and all production source remain unchanged.

The explicit JSON-RPC initialize-error case asserts initialize_response_failed/invalid_initialize_response, exact original error code/message/data in the failure response, no restart_completed, subsequent unavailable and real-child cleanup. It uses existing public process/event/sink seams; no new module, private call, version or percentage assertion.

Actual candidate run_tests(scope="targets", targets=["tests/mcp_server/core/test_proxy.py"], tests=["python_tests"], args={"python_tests":["-q","--cov","--cov-branch","--junitxml=.pgmcp/temp/issue517/c7-proxy.xml","--cov-report=term","--cov-report=xml:.pgmcp/temp/issue517/c7-proxy-coverage.xml"]}, timeout_seconds=300) ran11 passing cases, zero failures/errors/skips. Native terminal reports99.91s; JUnit suite time is52.275s, so this evidence is not used for latency claims. Native exit1 correctly rejects this narrow16.123387% coverage selection; no threshold override. The actual report uses six-decimal precision and XML confirms the explicit-refusal rejection path executed.

Targeted run_checks for the same file with python_format/python_lint/python_pyright, timeout600 all passed; Pyright one file, zero diagnostics. Native Markdown checks on edited evidence also passed. The full2960 passing tests and actual89.995636% shortfall above remain the latest complete result, not a green coverage claim. Independent Implementation → Validation review precedes the final complete configured run and required branch/configured gates, with raw combined coverage at least90% and no native threshold-failure text.

## Post-C_7 Complete Validation

**Coverage and checks pass; complete acceptance FAILS on one test-harness race.** Exact clean snapshot46292376e199cafbba59bd99d70b84bf33bece30, after independent Implementation GO686fc435. All seven cycles remain intact; final native git_status is clean.

Same full configured native eight-worker invocation with --cov --cov-branch -q, timeout1800, output .pgmcp/temp/issue517/full-suite-c7.xml and coverage-c7.xml:2960 passed,1 failed, zero errors/skips,2961 cases in628.26s, native exit1. Combined coverage is13363/14456 lines plus3141/3876 branches =16504/18332 (90.028366%); native output explicitly says90% reached. Branch format/lint/Pyright and configured format/lint/Pyright all pass (66 formatting/lint targets,24 branch production types;474 configured format targets and191 configured production types, zero diagnostics). Reuse unchanged191-file production Mypy evidence.

The sole failure is integration/execution/test_process_stopping.py::test_member_spawned_during_stop_cannot_be_confirmed_from_old_snapshot. Its caller timeout1s starts stopping before the test has armed the original Node children. The synchronous observe-members injection then waits2s for a late child while blocking the event loop needed to arm the originals. The retained fixture establishes this ordering: parent/first PID at16:16:55, second PID and spawn-late.request at16:16:56, first.armed/second.armed only at16:16:58; no late.pid was published. The failure is the fixture AssertionError before a typed termination result, not demonstrated acceptance of an unsafe production stop.

Repair only this existing race test: let the Node parent acknowledge that original children are armed; await that factual marker with a bounded async readiness wait; then explicitly cancel the invocation. Preserve the member-created-after-snapshot injection, UNCONFIRMED result, retained scratch and absent late.done; existing timeout/cause/shared-five-second-stop-budget tests stay unchanged. No new cases/modules, production timing change or gate exception. Another complete native Validation remains mandatory after independent phase review.

## Related Documents

- [Approved Research](<research.md>)
- [Design](<design.md>)
- [Planning](<planning.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-18 | @imp validator | Record complete negative suite/configured gate evidence, clean checkout restoration and concrete missed consumer/provisioning boundaries. |
| 0.2 | 2026-10-18 | @imp implementer | Preserve failed full Validation and record owner-approved C_3 recovery, exact focused outcomes, native/process causes and pending complete revalidation. |
| 0.3 | 2026-10-18 | @imp validator | Record complete C_3 retry:2911/2912 tests pass, all required checks pass,87.93% opt-in coverage fails and one installed-startup client window remains; reopen the unbaselined extra coverage acceptance with the owner. |
| 0.4 | 2026-10-18 | @imp implementer | Record bounded C_4 measurement and focused behavior evidence; preserve negative full runs and owner-required90% acceptance as pending. |
| 0.5 | 2026-10-18 | @imp validator | Record post-C_4 full run:2956 pass,2 failures,89.94% coverage; preserve green checks and native startup timeline without weakening acceptance. |
| 0.6 | 2026-10-18 | @imp implementer | Record C_5 focused/instrumented outcomes, retained xdist timeout evidence and synthetic-package isolation; preserve unresolved90% gate. |
| 0.7 | 2026-10-18 | @imp implementer | Record10 passing public proxy cases and targeted checks after C_6; reserve full90% acceptance for independent re-entry to Validation. |
| 0.8 | 2026-10-18 | @imp validator | Record2960 passing full cases/checks but89.995636% actual coverage; expose native rounding/terminal discrepancy and retain strict90% obligation. |
| 0.9 | 2026-10-18 | @imp implementer | Record11 passing proxy cases, original initialize-error diagnosis and precision6; exact90% full acceptance remains pending. |
| 0.10 | 2026-10-18 | @imp validator | Record actual90.028366% and green checks but one confirmed test setup deadlock; preserve negative complete outcome. |
