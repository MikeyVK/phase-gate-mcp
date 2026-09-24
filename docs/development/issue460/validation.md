<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=3zJkRylM4sIT4HzD sf=9PfER5JkyAoFQLRi -->

# Issue 460 Refactor Validation

**Status:** Blocked — required execution evidence unavailable; independent review requested
**Version:** 1.1
**Last Updated:** 2026-09-24


## Purpose

Record observed validation evidence and blocking gaps without declaring independent QA approval.

## Scope In

Authoritative plan/strategy review, bounded structural and test-source inspection, one workspace-wide test attempt, one branch-wide python_review check run, and observed failure reporting.

## Scope Out

Production/test fixes, changed native settings, dependency installation, repeated full-suite execution after an uncertain timeout, external-workspace migration, release, merge and phase progression.

## Prerequisites

- Research Approved Strategy, Design package contracts, Planning and the stored 105-cycle plan remain binding.
- Implementation evidence is indexed by the cycle cards; CY105 records focused tests and a pre-existing failed Mypy gate. Those historical claims are not a fresh full-suite result.




## Issue Number

#460




## Validation Status

FAIL



## Scope

Refactor issue #460, branch refactor/460-audit-scaffolding-schema-template-contracts. V460.1–V460.5 remain the binding completion obligations. The phase is validation; no production repair or strategy change is authorized by this report.



## Obligations


### V460.1 — exact source closure and architecture review

**Evidence:**

- [Exact path ledger](<planning-path-ownership.md>)
- [Retirement and CY105 evidence](<planning-rollout.md>)
- [Test architecture](<design-test-architecture.md>)


**Outcome:** PARTIAL. Read-only closure inspection confirms all 79 A001–A079 legacy template paths absent, plus 47 C-register paths with retirement dispositions absent. C084 survives only as an empty package docstring, consistent with lifecycle-export removal. The 126/151/79/57 ledger and 279 proposed paths are not thereby fully behaviorally certified. Full retained-assertion and architecture closure remains open.



### V460.2 — native, consumer and real public evidence

**Evidence:**

- [Native Ruff conformance](<../../../tests/mcp_server/integration/adapters/test_ruff_checks.py>)
- [Native Pytest conformance](<../../../tests/mcp_server/integration/adapters/test_pytest.py>)
- [Public scaffold](<../../../tests/mcp_server/integration/test_scaffold_public_v3.py>)
- [Public edit](<../../../tests/mcp_server/integration/test_edit_public_v3.py>)
- [Cache fidelity](<../../../tests/mcp_server/integration/test_cache_fidelity_v3.py>)


**Outcome:** PARTIAL. Source inspection confirms direct native subprocess comparisons, isolated workspaces and public persistence/cache assertions, rather than only a mocked executor. No fresh aggregate native/public passing result was returned in this session. Live schema discovery succeeded; that is not certification of every artifact contract.



### V460.3 — fresh installed distribution, migration, recovery and client rediscovery

**Evidence:**

- [Installed distribution test](<../../../tests/mcp_server/integration/test_installed_distribution_v3.py>)
- [Installed startup and handshake](<../../../tests/mcp_server/integration/test_target_startup.py>)
- [Activation recovery](<../../../tests/mcp_server/integration/test_template_activation.py>)
- [Renewal](<../../../tests/mcp_server/integration/test_renewal_cli.py>)
- [Historical rehearsal](<rollout-rehearsal.md>)


**Outcome:** UNPROVEN for the current validation run. Existing tests build an offline wheel, separately install it, compare packaged bytes and assert import origins, real MCP handshakes and recovery. Their presence and historical rehearsal do not establish a fresh successful execution after all later edits.



### V460.4 — one full suite and branch gates

**Evidence:**

- [Branch check operation](<pgmcp://cache/runs/48b56dd627ed49249c13f71bd00aa777>)


**Outcome:** BLOCKED. The workspace test call timed out at the MCP client boundary after 120 seconds without a result URI. Its completion and pass/fail counts are unknown. All four branch checks report unavailable/execution_error, with run_status=incomplete. Operation success=true means the operation returned facts, not that checks passed.



### V460.5 — nineteen workflow carriers and host source/copy consistency

**Evidence:**

- [Workflow design](<design-workflow-documentation.md>)
- [Host mapping](<rollout-host-input.md>)
- [Carrier tests](<../../../tests/mcp_server/unit/config/test_contracts_loader.py>)


**Outcome:** PARTIAL. Bounded read-only review found all eight direct source/consumer pairs byte-identical. Existing tests address nineteen carrier meanings and render four phase artifacts, with separate family integration coverage. Fresh passing execution and full semantic closure remain unproven.





## Evidence


### Branch-wide required checks

Configured python_review selected python_format, python_lint, python_types and python_pyright. All four returned status=unavailable, reason=execution_error, adapter exit code=3, evidence=null. Removed-target inventory contains 266 entries.

**Sources:**

- [Complete cached check operation](<pgmcp://cache/runs/48b56dd627ed49249c13f71bd00aa777>)


**Invocation:** run_checks(scope="branch", timeout_seconds=300)



**Observed Result:** incomplete




### Exact native launch failures

python_format/python_lint: Ruff launch failed: [WinError 206] De bestandsnaam of -extensie is te lang. python_types: Mypy launch failed: [WinError 206] De bestandsnaam of -extensie is te lang. python_pyright: Pyright execution failed: spawnSync C:\Program Files\nodejs\node.exe ENAMETOOLONG. Observed native identities: Ruff 0.14.13, Mypy 1.19.1, Pyright 1.1.408. All adapter package versions 1.0.0; fingerprints Ruff Ny0reoegAdrc-QS5, Mypy Qz4DehR5ukmWj2cr, Pyright UC15y_s27GyMRNMP.

**Sources:**

- [Cached native failure facts](<pgmcp://cache/runs/48b56dd627ed49249c13f71bd00aa777>)
- [Ruff process construction](<../../../mcp_server/bundled_adapters/ruff/check.py>)
- [Mypy process construction](<../../../mcp_server/bundled_adapters/mypy/check.py>)





### One workspace-wide test attempt

The tool returned: timed out awaiting tools/call after 120s. No run ID/cache URI, test counts or completion acknowledgement were returned. The requested adapter timeout does not override the observed client transport limit. No second full run was started; native process completion/termination is not inferred.

**Sources:**




**Invocation:** run_tests(scope="workspace", timeout_seconds=1200)



**Observed Result:** UNKNOWN — missing completion evidence




### Structural removal and retained helpers

A001–A079 absence counts by CY094–CY104: 9/11/8/6/6/6/7/6/6/5/9. T004 artifact_test_harness and T106 fake_pytest_runner are absent. Hidden-aware search of active server/tests/template-suite/config/root project configuration found no retired dotted-module imports, get_template_root or old tier/pattern references. tests/conftest.py retains workflow_fixtures and suite_roots and selects template_suite. make_project_manager remains used by project tools/manager/readback tests. This bounded delegated review was findings-only and did not run tests.

**Sources:**

- [Retirement ledger](<planning-path-ownership.md>)
- [Conftest](<../../../tests/conftest.py>)
- [Retained test support](<../../../tests/mcp_server/test_support.py>)





### Live public discovery and server availability

scaffold_schema(validation_report) returned the current closed content schema and its schema attachment. A subsequent health_check reported healthy, process 21540, win32, version 2.0.0. Server health is not a test-job status query or validation verdict.

**Sources:**

- [Schema result](<pgmcp://cache/runs/25647f89bbbd4bd88ae197b061d8866f>)
- [Health result](<pgmcp://cache/runs/02d14e2ef1c74944802f47acaffc4ef2>)







## Demonstration

Observed end-to-end fallback: live schema discovery and the real branch check operation returned structured facts. Full behavioral demonstration remains unavailable. Existing installed-distribution/startup/activation tests are the intended current-source demonstration entry points; no fresh success is inferred from inspecting them.



## Preservation

The Approved Strategy retains the explicit V3 clean break, separate check/test/fix roles, generation fingerprints distinct from renewal checkpoints, enforce/report persistence and independent native evidence. No compatibility bridge, weakened assertion or changed check configuration was introduced. Structural absence supports planned cleanup only; all 19 invariants and 23 expected results remain subject to complete behavioral and architecture evidence.



## Containment

Only this validation report and the existing phase-transition state are intended for the validation commit. Startup status contained .pgmcp/installation.json, .pgmcp/template_upgrade.lock and a retained template backup tree among 136 untracked files; these operational artifacts are excluded from the commit.



## Failures

- F-VAL-01: Required branch checks cannot launch native tools with the current branch target selection on Windows. Current source appends the target list to native argv; this is consistent with the observed command-length failures. Large explicit selections need a supported length-safe execution route; bounded target batches can provide useful evidence without first changing production code. Equivalent complete coverage must be documented.
- F-VAL-02: Full-suite completion evidence is unavailable after the MCP client timeout. Determine the existing run's fate or a supported durable-result route before authorizing/repeating a replacement run.



## Caveats

- This FAIL is a producer validation outcome because required proof is missing, not an independent QA GO/NOGO.
- CY105 previously recorded 14 Mypy errors in unchanged lines; that historic failure was not resolved or freshly re-established by the unavailable branch run.
- Native Ruff source conformance asserts 0.15.6 while the live check adapter reports 0.14.13. This is an observed environment-version discrepancy, not a claimed test failure.
- The all-cycle hand-over is represented by distributed cycle evidence. No separate final implementation QA verdict was found in the inspected issue-local files.
- Full architecture/retained-test auditing stopped short of certification after the execution blockers; no additional temporary tests or implementation changes were added.



## Risks


### Treating operation success or structural absence as behavioral completion would hide unavailable checks and missing tests.

Keep V460.1–V460.5 explicitly incomplete until required evidence is available; independent QA reviews exact results.


**Consequence:** Validation cannot be closed or progressed on this evidence.





## Deferred Work


### Resolve native branch launch limits and missing full-suite completion evidence through a bounded implementation/tooling follow-up.

The validation contract requires reporting failures without redesigning or patching the implementation.





## Related Documents

- [Planning](<planning.md>)
- [Research strategy and invariants](<research.md>)
- [Design](<design.md>)
- [Architecture principles](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)


## Investigation addendum — 2026-09-24

### F-VAL-03 withdrawn: documented intentional refinement

The prior classification missed [CY011.D1/D2](planning-execution.md#cy011): it explicitly records the **session-approved refinement of 2026-09-17**, with a short budget-triggered guide reference and the packaged resource owning unchanged window/integrity/safe-retry instructions. [Host preparation](rollout-host-input.md#22-contractual-separation-and-lazy-cache-discovery) deliberately implements lazy discovery. The owner has also explicitly reconfirmed that this is intentional. This is not an implementation blocker. Stale generalized CY069/hub wording and unavailable historical fresh-agent proof are documentation/provenance reconciliation, not a reason to replay cutover.

### Scope and command-length diagnosis

The read-only current branch selection at HEAD 625b29a4 contains 593 existing paths, including 136 nonignored untracked files, with 266 deleted paths recorded separately. Only 217 selected paths have a .py extension. The longest individual absolute path is 128 characters. Reconstruction with the local interpreter and Python Windows list2cmdline yields 41,939/41,946/41,917 UTF-16 units including terminating NUL for Ruff format/lint and Mypy. These are reconstructed argv measurements, not an intercepted native process command; the live adapter's PATH-selected interpreter can differ. All exceed CreateProcessW's 32,767-unit command-line limit. With untracked paths excluded analytically, the reconstructed Ruff lint command is 28,351 units. No files were removed or ignored to obtain this comparison.

GitAdapter.get_branch_changes includes tracked merge-base/index/worktree changes and nonignored untracked paths. ScopeResolver converts existing paths to absolute paths; adapters append all targets to one native argv. Therefore ignored-by-native extensions still consume command-line space before the native process can filter them. This is native-child launch failure, not a long individual filename, MCP payload limit, or test timeout. The measured backup/untracked contribution materially pushes the current selection past the Windows limit. There is no automatic native argv batching or response-file route in the inspected implementation.

### Workspace traversal and Windows access failures

Workspace passes one root path; configured passes no explicit native targets. Consequently workspace Pytest bypasses testpaths selection and recursively discovers from the root under native recursion rules. Pytest does not inherit Git ignores. Current norecursedirs does not exclude all local scratch locations.

A diagnostic-only collection run with scope=workspace, args python_tests=[--collect-only,-q,-n,0], timeout_seconds=90 returned native exit 2: **2,602 tests collected, five collection errors in 13.52 seconds**. Full cached tracebacks name:
- .pytest_cache_ci
- .tmp/pytest-of-1Voudig
- temp/cy086-ruff
- temp/cy087-ruff-after
- temp/cy087-ruff-baseline

Each raises PermissionError/WinError 5 while os.scandir enumerates a directory. This identifies denied filesystem reads, not a generic timeout. Resource: pgmcp://cache/runs/e6c5f7f5e27b42bdbb830ac813601599.

With the same collection options but scope=configured, native discovery used testpaths=tests/mcp_server: **2,601 tests collected, exit 0, in 2.13 seconds**. Resource: pgmcp://cache/runs/eb1ed8a32dd749e09e94dc42f86c2a10. This proves successful collection only, not passing test execution; it does not retroactively determine the earlier timed-out run.

Ruff format also reproduces access errors when targeting .pytest_cache_ci, .tmp and temp separately (resources 2161c16436354c689bb93c36a48e7ade, 81d6da3976014585b4ca6971a1adbf40, 3ba7e8d9532a472a9284662c00c20c3f). The native Ruff diagnostic omits the exact denied child path. Targeting mcp_server/docs/scripts instead returns 184/6/1 already-formatted files. Targeting tests reports two actual formatting differences and 276 already-formatted files, without access errors. The two differences are test_contracts_loader.py and test_artifact_identity.py. Disabling Ruff caching does not remove the workspace access failure (9a35c9cbb205441284079c6cfd4311a7).

### F-VAL-04 — Ruff diagnostic classification changes under verbose output

The same workspace formatting failure without verbose yields execution_error and the access-denied message. With --verbose it yields invalid_configuration and a benign first debug line about using pyproject.toml, although the native evidence still ends in the access-denied error. Source: mcp_server/bundled_adapters/ruff/check.py _message and _classify_native_failure. The latter scans all output for broad markers including configuration; the former can select the first debug line. This is a concrete error-classification/message defect, distinct from cache loss. Resource: pgmcp://cache/runs/b43a3af617c74b62ba0f0d5ea13859b9 (complete operation 177,822 characters, fully read through windows).

### Cache contract and actual retention

[DI-05 diagnostic capture](design-execution-adapters.md) and [Shared presentation boundary](design-shared-contracts.md) require native evidence, typed error details and ProcessCapture in the complete operation cache, not inline dumps. Formal adapter stdout is limited to 8 MiB; supplemental adapter stderr retains at most 256 KiB with explicit head/tail truncation. Accepted JSON stdout intentionally has null capture fragments: the decoded role response is stored instead. Native stdout/stderr belongs in evidence.data.

For WinError 206 the native child never started, so no native stdout/stderr exists: the OS exception is retained in message and evidence is null. For actual native failures, the inspected cache contains diffs, complete available native error text and Pytest tracebacks. The verbose Ruff operation and workspace collection operation were reconstructed through all cache windows. No confirmed cache-retention contract violation was found. The producer's earlier summary failed to explain available evidence sufficiently.

The adapter uses subprocess capture_output for its native child and emits its formal response only after completion. Thus native progress is buffered inside the adapter, not streamed as cache entries; the server publishes the final DTO after tool execution. A client timeout before receipt may leave no delivered resource URI. No background-job handle or timeout-recovery lookup is exposed by the current run_tests tool.

### Timeout history and runtime identity

.codex/config.toml is Git-ignored. Its local creation and last-write timestamps are both 2026-09-23 08:00:24 UTC. Available session history first confirms this exact workspace configuration with tool_timeout_sec=120 at 2026-09-23 17:59:57 UTC. These facts establish it predates this validation; they do not prove the exact original edit or author. The producer made no timeout-config change.

The original full-suite request already specified timeout_seconds=1200, while the MCP client failed after 120 seconds. Those are separate budgets. Raising the adapter budget alone cannot address the client deadline; nor can either timeout repair the now-confirmed root-scope collection failures.

Adapter manifests request executable=python; bootstrap resolves it through shutil.which, not automatically the server's sys.executable. The observed live Ruff version is 0.14.13 and Pytest is 9.0.2; cache traces use the system Python313 installation. The server launcher being a venv Python does not itself establish native adapter environment parity.

### Remaining work

Resolve length-safe selection execution with explicit preservation of native semantics; fix misleading Ruff failure classification; select and document the intended full-suite native discovery boundary; reconcile the client/adapter timeout budgets and native environments. These are findings and candidate remediation boundaries, not an implementation patch or a changed Approved Strategy. No production files, ACLs, scratch directories, dependencies or client configuration were changed.

## Refactor / Validation Hand-over

### Scope

Partial validation of V460.1–V460.5. Production repair, native environment changes and phase progression excluded.

### Deliverables

- [Validation report](validation.md)
- [Planning and validation obligations](planning.md#validation-and-documentation-deliverables)
- [Structural ownership ledger](planning-path-ownership.md)
- [Native check failure evidence](pgmcp://cache/runs/48b56dd627ed49249c13f71bd00aa777)

### Evidence

One workspace test attempt returned only a 120-second MCP timeout. One branch check run returned four unavailable execution errors. All 79 legacy template paths were absent in the bounded structural review; eight mapped host source/copy pairs matched. No complete behavioral or architecture verdict is claimed.

### Open Work

F-VAL-01 native launch length; F-VAL-02 missing full execution completion plus diagnosed root-scope collection failures; F-VAL-04 misleading Ruff classification. F-VAL-03 is withdrawn by the investigation addendum. Full V460.1–V460.5 closure and independent review remain open. Native Ruff version discrepancy and historical Mypy failures remain recorded above.

### Review Request

Review requested. Resume an independently invoked `pgmcp-qa` validator review before deciding the bounded remediation and resumption route.

