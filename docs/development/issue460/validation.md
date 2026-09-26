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

- F-VAL-01: Required branch checks could not launch native tools with the current branch target selection on Windows. Repair is explicitly deferred outside #460 as D-VAL-01 below, including an audit of all shipped adapters. This remains an observed evidence limitation, not an issue-460 implementation task; no blanket batching workaround or equivalent coverage is assumed.
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


### D-VAL-01 — Audit native execution robustness across all shipped adapters

**Disposition:** Deferred outside issue #460 by explicit owner decision on 2026-09-24. Coordination owns creation and triage of a separate issue; no follow-up issue has been created here.

**Suggested issue title:** Audit and harden shipped adapters for large selections and native invocation limits.

**Confirmed trigger:** F-VAL-01: the branch selection becomes one oversized native command line in Ruff, Mypy and Pyright, producing WinError 206 / ENAMETOOLONG. See the cached branch operation and the command-length diagnosis below.

**Follow-up scope:** Inventory every shipped adapter package and each implemented check/test/fix role. Review selection-to-native invocation, platform command/argument limits, quoting and path handling, large selections, native discovery semantics, and actionable failure evidence. Establish applicability per adapter instead of assuming every adapter has the same defect. Where internal batching or alternative transport is considered, prove preserved cross-file semantics, complete coverage, aggregate outcomes and diagnostics, lifecycle limits, and fix-role mutation/failure behavior. Exercise representative boundary cases on supported platforms.

**Contract boundary:** Preserve the existing generic role request/response contracts as the starting constraint. Keep native-tool execution knowledge inside adapters; do not make agents or generic orchestration calculate tool-specific command limits. No contract expansion or universal batching design is approved by this deferral.

**Issue-460 consequence:** No adapter repair or additional implementation cycle for D-VAL-01 belongs to this issue. The observed unavailable branch checks remain recorded validation evidence; deferring the repair does not convert them into passing checks or by itself close V460.4. Missing full-suite completion evidence remains a separate finding, not part of this deferral.

**Coordination hand-off:** Create the separate issue from this notice and link it back here. Future Research must distinguish confirmed defects, equivalent risks in other adapters, and tool-specific non-applicability; define acceptance evidence before choosing remedies.





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

D-VAL-01 length-safe native execution and the all-adapter robustness audit are deferred outside issue #460 for coordination to create a separate issue. Other findings remain under discussion: misleading Ruff failure classification, the intended full-suite native discovery boundary, client/adapter timeout budgets and native environments. No remediation of those other findings is selected by the D-VAL-01 deferral. No production files, ACLs, scratch directories, dependencies or client configuration were changed.

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

D-VAL-01 / F-VAL-01: adapter launch robustness is explicitly deferred outside #460; coordination must create a separate issue covering all shipped adapters and link it to this notice. The unavailable branch-check evidence remains visible. F-VAL-02 missing full execution completion and the separately diagnosed root-scope collection failures, plus F-VAL-04 misleading Ruff classification, remain under discussion. F-VAL-03 is withdrawn by the investigation addendum. Full V460.1–V460.5 closure and independent review remain open. Native Ruff version discrepancy and historical Mypy failures remain recorded above.

### Review Request

Review requested. Resume an independently invoked `pgmcp-qa` validator review before deciding the bounded remediation and resumption route.


## Owner-approved validation configuration correction — 2026-09-24

The owner explicitly authorized fixing point 2 inside issue #460: validation workflow instructions must use run_tests(scope='configured') for the complete native-configured suite, while explicit directories/files remain scope='targets'. The five prescribed test invocations in contracts.yaml now use configured; full-suite wording is aligned. Explicit workspace root selection remains available for deliberate native discovery from the root. No adapter contract or selection implementation changes.

Pytest norecursedirs replaces its defaults rather than extending them. Restore all native default exclusions, retain repository-specific exclusions, and exclude temp/tmp scratch directories. The restored .* excludes hidden cache, temporary and template-backup trees. testpaths remains tests/mcp_server; no marker filters or narrower testpaths were introduced. This addresses traversal selection, not the underlying Windows ACLs.

YAML/TOML edits use safe_edit_file(validation='report') because no artifact validation profile is selected for these files (enforce returned validation_blocked with selected_source=none and selection_reason=absent). Verification uses existing contract/config tests and native collection. This bounded owner-authorized configuration correction does not reopen the deferred D-VAL-01 adapter robustness implementation scope.

### Verification of the approved scope/configuration correction

- run_tests(scope='targets', targets=['tests/mcp_server/unit/config/test_contracts_loader.py', 'tests/mcp_server/unit/config/test_contracts_config.py', 'tests/mcp_server/unit/test_pytest_config.py'], args={'python_tests': ['-q', '-n', '0']}, timeout_seconds=90): 58 passed, 1 failed. Both contract test modules passed. The failure is test_qa_tests_relocated_to_integration_directory, asserting that the absent tests/mcp_server/integration/test_qa.py exists; it is unrelated to discovery exclusions or scope instruction changes and remains open. Cache: pgmcp://cache/runs/a7351c2facea434b91e706eae790d5ca.
- run_tests(scope='configured', args={'python_tests': ['--collect-only', '-q', '-n', '0']}, timeout_seconds=90): 2,601 tests collected, exit 0, 2.57 seconds. Cache: pgmcp://cache/runs/e84ab6dbd3ec4386ad0e2160d51e436d.
- Identical collection options with scope='workspace': 2,601 tests collected, exit 0, 2.25 seconds; the five former access-denied collection errors are absent. Cache: pgmcp://cache/runs/01900aa049184f14949034cddfeec15c.
- Both collection resources were read completely in contiguous windows. Successful collection does not establish full-suite execution or passing tests. The configured collection count is unchanged from the pre-edit 2,601 baseline; root collection previously found 2,602 plus five errors.

After the supported server restart, get_work_context returned the updated configured-scope validation instruction (pgmcp://cache/runs/b4e49d3d05cc4526b77de42a93bdad91), proving the active server loaded the revised contract. Independent review remains requested; full-suite completion, deferred adapter launch robustness and other unresolved findings remain separate.

## Timeout provenance and authorization investigation — owner scope refinement, 2026-09-26

**Owner-provided historical evidence:** Before issue #460, run_tests calls could run longer than 120 seconds. This is an explicit regression baseline to investigate; it is not yet independently reconstructed from old run receipts. The owner does not recall authorizing introduction of the observed 120-second client limit. Do not infer unauthorized implementation or an author solely from this discrepancy.

**Required investigation:**
- Reconstruct the earlier successful long-running call path: host/client, configuration, native execution budget, elapsed time and returned evidence. Distinguish the prior run_tests timeout parameter from a whole MCP-call deadline.
- Trace the introduction of .codex/config.toml tool_timeout_sec=120 through available local configuration/session history and setup scripts. Git ignores this file; timestamps and first observed reads are not proof of writer, approval or introduction time.
- Map each budget independently: native tool, PGMCP adapter invocation, bounded termination, complete multi-adapter tool operation and MCP client/transport. Identify owners, defaults, overrides and aggregate overhead.
- Trace Research/Approved Strategy, Design, Planning, implementation commits and user authorization for each changed boundary. A document labelled human-approved is a claim to trace, not independent proof that a separate client limit was approved.
- Establish actual client timeout/cancellation behavior, process-tree termination, late result handling, cache publication/discoverability, and what the agent/user can know before retrying. Do not infer the fate of the original interrupted run from code inspection alone.
- Extend the provenance audit to adjacent issue-460 execution/client settings and materially changed defaults to identify other unapproved decisions, distinguishing approved changes, missing provenance, implementation departures and host-only configuration.

**Owner requirement:** Tool deadlines are acceptable when intentionally designed with clear PGMCP behavior and correct failure/result handling. Merely increasing a client value does not close the finding or authorize a new asynchronous execution design. No timeout setting or execution code is changed by this investigation refinement.

### Bounded timeout follow-up — 2026-09-26

The owner requested a focused follow-up rather than a separate broad investigation. Read-only local session search found tool_timeout_sec=120 already present in the S1mpleTrader PGMCP v2 Codex workspace configuration on 2026-08-17 at 14:55:30 UTC (session 01a01037-51bb-7802-b314-022c6d29681d, explicit read of C:/1Voudig/99_Programming/ST/.codex/config.toml). This is a different workspace: it proves the value was used before the current adapter rollout, not that today's pgmcp file was copied from it or who chose it. In the inspected available history, the current pgmcp file is first observed on 2026-09-23 at 17:59:57 UTC; no attributable write or specific approval was found. No unauthorized issue-460 introduction is established.

The legacy RunTestsInput at c8f46c6a^ already exposed timeout=300; PytestRunner passed that value to subprocess.run. The current python_tests binding also uses 300 seconds. The 120-second client boundary is distinct from either server-side default. A client/workspace configuration difference is a plausible explanation for earlier long calls, not a demonstrated reconstruction of those calls.

Current source inspection: the proxy forwards ordinary JSON-RPC traffic and has no 120-second per-call timer; the shared adapter runtime types deadline expiry, attempts bounded process-tree stopping, and returns cancellation observations. Existing real-process tests cover timeout and cancellation stopping, including a Pytest xdist descendant test. These tests were inspected, not rerun. The server publishes the operation cache only after tool.execute returns; no early recoverable job handle is supplied. Therefore proper server-side timeout handling does not guarantee receipt of a final result after an earlier client deadline. No observed cancellation delivery or final fate of the original 120-second run is established by this source review.

Disposition: treat this as an unaligned host/client deadline and unresolved end-to-end completion evidence, not a proven missing generic timeout implementation. A bounded remedy should align the host deadline with the selected PGMCP execution budget plus termination/response overhead (and cumulative work when multiple bindings run), then verify a representative call beyond 120 seconds with an observable final result. Do not infer support for arbitrary long calls or cancellation delivery from configuration alone. No settings changed, no long run started, and no unrelated scope/authorization audit was performed.

### Owner decision — client timeout, 2026-09-26

The owner ended the historical provenance investigation and explicitly selected tool_timeout_sec=300 for the local Codex phase_gate_mcp connection. The setting was changed from 120 to 300 in the Git-ignored .codex/config.toml using safe_edit_file(validation='report'). Runs expected to exceed 300 seconds should be split into bounded selections with recorded coverage rather than extending the deadline again. This session refinement permits partitioned validation evidence without dropping suite coverage; prior instructions demanding one indivisible full-suite invocation do not override this owner decision.

The native test binding remains at 300 seconds; equal client and adapter budgets do not guarantee delivery of an adapter timeout result after cleanup. Keep actual planned calls comfortably within the client limit. The new client configuration value is verified on disk; activation in the already-running Codex connection is not established by editing it or by restarting only the PGMCP server. No long test run or end-to-end timeout certification is claimed. Earlier missing execution evidence remains unknown, not retroactively passing.
