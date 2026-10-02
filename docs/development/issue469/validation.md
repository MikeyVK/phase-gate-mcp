<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=3zJkRylM4sIT4HzD sf=9PfER5JkyAoFQLRi -->

# Issue 469 — Native Adapter Validation

**Status:** Completed — refreshed independent Validation review requested
**Version:** 1.2
**Last Updated:** 2026-10-02
**Validation Status:** PASS — refreshed producer suite and gates; independent review pending

## Purpose and scope

Validate the direct unreleased check/test/fix contract correction on branch `bug/469-native-adapter-robustness` through `01c7887aaa036542282239484d1ace7ad659f703`. Production code is unchanged since `9bc12fe67479093e4a50fc4d3955db74ba02fe9b`; later commits repair direct test consumers, existing test support and the finite rendered-template native comparison budget. Validation made no production or test patches. Every correction returned through Implementation and independent review.

Authoritative inputs are [Research 1.5](research.md), [Design 1.3](design.md) and [Planning 1.2](planning.md). B1–B6 remain binding: internal identity 1, required JSON context, one complete native operation, truthful outcomes/versions/diagnostics, and ordinary native effects under trusted host-account execution. External migration, legacy adapter bridges, OS confinement and linked-issue closure are excluded.

## Prerequisites and complete-suite proof

An official MCP SDK client launched the same configured PGMCP command, arguments, working directory and environment from .codex/config.toml on Windows. The actual SDK client and MCP server processes, as well as the primary server, were independently observed under the original operator account 1Voudig. It ran the complete configured selection:

```json
{"scope":"configured","tests":["python_tests"],"timeout_seconds":600}
```

The SDK receive budget was 900 seconds and the public invocation deadline was 600 seconds. Only these budgets changed to permit a complete receipt beyond the primary client's 300-second ceiling. No caller native argument, worker, collection, debug or selection override was supplied. Independent QA reviewed this route; passing criteria and native prerequisites were unchanged. Native Pytest 9.0.2 ran on Python 3.13.7 with the existing configured addopts and eight workers; `args_source=configured` and `effective_args=[]`.

**Observed result:** 2775 passed, 1 skipped, 1 xpassed, 229 warnings in 286.09 seconds on commit 01c7887a. Native exit 0, no invocation rejection or unconfirmed termination. The complete [full-suite receipt](pgmcp://cache/runs/f7964e6eca254e54a6b275c86e6e8fe0) was read in contiguous pages and verified against its Unicode length and UTF-8 SHA256 before parsing. Receipt integrity: 796120 Unicode characters; UTF-8 SHA256 `a355bfdfd1fad40eff53763848aab89432b8fcf5f2f6a0b5b47766fea5713dcf`. All 2777 native items were selected; 2775 PASSED item records and zero FAILED item records were observed, with no native error lines. SDK server PID32264 and client PID41076 were verified under the same operator account 1Voudig as primary PID41964. The existing rendered-template native execution is included in this complete passing selection. The native summary, rather than operation-level success or the bounded projection, establishes the outcome. Existing skip and XPASS policies remain unchanged.

## Obligation mapping

| Obligation | Useful evidence and observable result |
|---|---|
| V_NATIVE | The complete configured suite above finished successfully; previous partial runs and timeouts are not substituted for it. |
| V_GATES | All 48 changed Python paths below pass format, lint and Pyright; configured production Mypy passes 186 files. Actual CJS entrypoints, role JSON schemas and bundled manifests are exercised by native adapter, catalog and installed-distribution tests. Changed Markdown gets its offline link checks. |
| E469-1/E469-3 | [Ruff](../../../tests/mcp_server/integration/adapters/test_ruff_checks.py), [Mypy](../../../tests/mcp_server/integration/adapters/test_mypy.py), [Pyright](../../../tests/mcp_server/integration/adapters/test_pyright.py), [Pytest](../../../tests/mcp_server/integration/adapters/test_pytest.py) and [Lychee](../../../tests/mcp_server/integration/adapters/test_lychee.py) exercise oversized selections with late findings, small controls, discovery/exclusions and faithful whole-input refusal. |
| E469-2/E469-4/E475-1 | Native adapter tests exercise truthful completion, metadata refusal, actual prerequisite versions and retained diagnostic verbosity. Ruff usage/configuration/access classification follows causal native records independent of quoted arguments and filenames. |
| E474-1/E-CROSS | [Runtime](../../../tests/mcp_server/integration/execution/test_process_runtime.py), [process stopping](../../../tests/mcp_server/integration/execution/test_process_stopping.py), [content](../../../tests/mcp_server/integration/execution/test_content_input.py), service projections and [installed distribution](../../../tests/mcp_server/integration/test_installed_distribution_v3.py) prove required context, pure ownership descriptions, exclusive allocation, termination-sensitive cleanup and public evidence preservation. |
| D1_PROTOCOL/direct consumers | Installed entrypoint request now supplies a caller-owned directory. The held runtime test wrapper explicitly accepts/forwards the typed request contract and cannot indefinitely hide early task failure. |
| V_ACCEPTANCE | This report separates actual outcomes, prior failures, scoped guarantees and remaining limits; independent QA alone determines phase progression. |

The focused actual-native run of all 15 adapter/execution/catalog files also passed **383 tests, 17 warnings in 104.49 seconds**, configured arguments and ordinary workers, [receipt](pgmcp://cache/runs/55478afa6ad440d6987f5d5e2ae5cec3). That useful regression evidence supplements the full suite. It is not its replacement.

## Complete changed Python inventory and gates

The main-to-HEAD [branch inventory](pgmcp://cache/runs/c92cbf5016304315bdf3fa8e10512caa) contains 60 changed files and 48 Python files. Every abbreviated stat path was uniquely resolved against repository paths; the complete sorted Python vector is:

```text
mcp_server/bootstrap.py
mcp_server/bundled_adapters/commitlint/check.py
mcp_server/bundled_adapters/lychee/check.py
mcp_server/bundled_adapters/markdown_preflight/check.py
mcp_server/bundled_adapters/mypy/check.py
mcp_server/bundled_adapters/pytest/test.py
mcp_server/bundled_adapters/python_syntax/check.py
mcp_server/bundled_adapters/ruff/check.py
mcp_server/bundled_adapters/ruff/fix.py
mcp_server/core/interfaces/execution.py
mcp_server/execution/check_service.py
mcp_server/execution/fix_service.py
mcp_server/execution/invocation_scratch.py
mcp_server/execution/models.py
mcp_server/execution/process_runtime.py
mcp_server/execution/protocol.py
mcp_server/execution/test_service.py
mcp_server/schemas/execution_outputs.py
mcp_server/schemas/mutation_outputs.py
mcp_server/services/check_operation.py
mcp_server/services/scaffold_operation.py
tests/mcp_server/fixtures/adapter_process.py
tests/mcp_server/fixtures/suite_roots.py
tests/mcp_server/fixtures/test_role_double.py
tests/mcp_server/integration/adapters/test_commitlint.py
tests/mcp_server/integration/adapters/test_lychee.py
tests/mcp_server/integration/adapters/test_markdown_preflight.py
tests/mcp_server/integration/adapters/test_mypy.py
tests/mcp_server/integration/adapters/test_pyright.py
tests/mcp_server/integration/adapters/test_pytest.py
tests/mcp_server/integration/adapters/test_python_syntax.py
tests/mcp_server/integration/adapters/test_ruff_checks.py
tests/mcp_server/integration/adapters/test_ruff_fixes.py
tests/mcp_server/integration/adapters/test_typescript_syntax.py
tests/mcp_server/integration/execution/test_check_profiles.py
tests/mcp_server/integration/execution/test_content_input.py
tests/mcp_server/integration/execution/test_process_runtime.py
tests/mcp_server/integration/execution/test_process_stopping.py
tests/mcp_server/integration/templates/test_pytest_integration_test.py
tests/mcp_server/integration/test_edit_operation_v3.py
tests/mcp_server/integration/test_installed_distribution_v3.py
tests/mcp_server/integration/test_target_startup.py
tests/mcp_server/unit/execution/test_catalog.py
tests/mcp_server/unit/execution/test_check_selection.py
tests/mcp_server/unit/execution/test_check_service.py
tests/mcp_server/unit/execution/test_fix_service.py
tests/mcp_server/unit/execution/test_test_service.py
tests/mcp_server/unit/fixtures/test_suite_roots.py
```

Exact calls:

```text
run_checks(scope='targets', targets=<all 48 paths above>,
           checks=['python_format','python_lint','python_pyright'])
run_checks(scope='configured', checks=['python_types'])
```

The refreshed [48-file gate receipt](pgmcp://cache/runs/ad2ab6596bd34d6985a62c79fc419de1) records all files already formatted, lint passed and Pyright 1.1.408 with zero errors or warnings across 48 files. Refreshed configured Mypy 1.19.1 passed 186 production files, [receipt](pgmcp://cache/runs/a63056e2d2fd4ddabc188fd326d381aa). Test Mypy is not the configured production gate.

Research, Design, Planning and the historical effect probe passed offline links: 131 total, 103 successful, 28 excluded, zero errors, [receipt](pgmcp://cache/runs/7d7c79dfc7e747e5951746fb053ae084). Report link verification is recorded with its final review hand-over. MCP cache URIs are intentionally excluded from native link fetching.

## Closed findings and prior failure ledger

| Observation | Correction and relevant evidence |
|---|---|
| Cleanup errors lost accepted responses and secondary causes | Commit 06bf112b preserves complete preceding JSON response and outcome; public check/test/fix/content projections retain the additional cause without replacing cancellation or request rejection. Regression evidence observes serialized results, large tail diagnostics and actual modified fix bytes. Independent QA closed the cleanup P2. |
| Ruff classified quoted input and filename words as causes | Commit 9bc12fe uses causal usage/configuration/access diagnostics; check and fix share the corrected classifier. Invalid config under a directory containing “unknown option” remains invalid_configuration. Independent QA closed both Ruff reproductions. |
| Installed entrypoint smoke omitted execution_context | Actual native rejection was correct: missing_field, protocol exit 2; [receipt](pgmcp://cache/runs/38aa9812d9454f50ad622b400e32040a) recorded one failed test. Commit 43e071a6 corrects the consumer. Existing test passed with configured settings, [receipt](pgmcp://cache/runs/74455cd1426e4bd892ac31dd4e4c5c63); independent QA repeated it. |
| Held runtime wrapper omitted request_contract | Existing selected test timed out after 60 seconds with confirmed termination, [receipt](pgmcp://cache/runs/c8f106591bf94db39a8d59646f821785); QA independently reproduced the same cause. Commit f960dde5 fixes explicit typed forwarding and bounds event/task synchronization. Full affected file: 42 passed, 53 warnings in 4.91 seconds, [receipt](pgmcp://cache/runs/69865adbfd3b433c926d9ca5609bc45f); independent QA repeated it and gave Implementation→Validation GO. |
| Full suite exposed retired repository template sources | On f960dde5 the exact configured suite completed: 1 failed, 2704 passed, 1 skipped, 1 xpassed, 207 warnings, 70 errors in 213.61 seconds, [receipt](pgmcp://cache/runs/c2c95e5292314d249c362ed630ea6c03). Every failure/error causal line was the absent .pgmcp/templates path. The two locations were unchanged from main; independent QA reproduced the shared fixture error and checked the startup condition. |
| Existing test support required the retired tree | Commit 8697f92 copies the current delivered template_suite into isolated fixture roots and explicitly authors the startup rehearsal's legacy directory. It preserves all assertions, changes no production/legacy route and restores no retired assets. Six complete affected test files: 101 passed, 31 warnings in 90.99 seconds, [receipt](pgmcp://cache/runs/146a67242d0b48579da40b5ca8b0b5b1). Three-file format/lint/Pyright passed, [receipt](pgmcp://cache/runs/d05bceec2720487988e4a79979852ed9). Independent Implementation review preceded the final full Validation run. |

Earlier diagnostics remain non-acceptance evidence:

- The subsequent exact default full call on 8697f921 again reached the primary client's 300-second ceiling without a receipt. No Pytest processes were present at the later process check; that observation establishes no native pass/fail outcome.

- The first complete configured call exceeded the client's 300-second limit and yielded no receipt. A 240-second repeat returned unavailable/timeout with confirmed termination, [receipt](pgmcp://cache/runs/90cb8b6314aa4418ae592748bc48bc1d).
- Full-selection `-x`/180-second and `-x -n2`/240-second diagnostics also timed out; receipts 03388e77d68648f2b451e69f8dd75fdc and 2221699fae3e40abb11699bba6ec2d0c. These alternative arguments were never counted as required-suite success.
- Collection-only selected 2777 tests in 2.46 seconds, receipt 6990540fa70f48bf9da1642acd6668cf. Collection is not execution proof.
- A 120-second native debug trace introduced Pluggy surrogate-encoding errors and overlapped QA tracing; receipt 124c346f69cf4763b75edaab19f6f194. Its counts/timing are not a clean full-run verdict.
- SDK diagnostics with 600- and 1800-second budgets timed out with confirmed termination under a different local account. They do not prove equivalent Validation prerequisites. Those sessions were closed normally.
- The producer's mistaken lock selector selected zero tests, receipt af7b9aaa1583433faafff3e60fa85cce. It supplies no passing regression evidence.
- Earlier FAIL reports and audited backward transitions remain in commit history. No forward gate was waived, and no failed outcome was reclassified as passing.

## Demonstration and preservation

The full suite contains the actual-native late-target, causal Ruff and resource-result regressions. A focused reproduction can use the existing Ruff checks/fixes and process_runtime test files through run_tests with configured arguments. Direct consumers can follow the installed distribution smoke for the explicit owned-context contract.

CLI/config precedence, configured discovery, native operation order, ordered fix effects and deliberate Ruff exit-zero/Pytest collect-only/exit-5 policies remain exercised. Fixes do not promise rollback. If cleanup fails after a fix, its preserved preceding result and actual source bytes remain inspectable.

The server remains healthy after completion: PGMCP 2.0.0 on win32; the SDK server was healthy before and after its run and its client session closed normally, [health receipt](pgmcp://cache/runs/958f623dec9f4d4f842a835dd912553d).

## Caveats, scoped guarantees and deferred work

| Boundary | Accepted limit or remaining responsibility |
|---|---|
| Pyright 1.1.408 explicit filename stdin | Ordinary spaces, CR/LF, native leading/trailing trimming and invalid UTF-8 cannot be represented faithfully and cause whole-selection unsupported_input. No quoting, normalization, batching or argv fallback. Empty selection preserves configured discovery, which may discover paths containing spaces. |
| Lychee occupied files_from channel | Caller/config channel ownership retains the positional route and native argv-size limit. No override or merge is implied. |
| Native effects and trusted account | Operational caches/state and compatible reports may be outside selected sources. Role/selection/result guards supply no OS, filesystem, network or credential sandbox. |
| Invocation ownership | Only exclusively created invocation resources are cleaned after confirmed termination. Unconfirmed termination retains them. Native caches are not invocation cleanup targets. |
| Evidence and versions | Caches are process-local/transient. Every inspected DTO was fully read and hash-verified; durable outcomes and exact vectors are recorded here. Package-local declared prerequisites and actual observed versions remain authoritative. |
| Separate acceptance | E469, E474 and E475 remain distinct. @co must align issue 474's superseded strict destination wording with the approved trusted-host/native-cache/report strategy before acceptance or closure. No linked issue is implicitly closed by this report. |

The original adapter/runtime findings remain closed. The additional native failure and its narrowly scoped harness correction are recorded below; independent QA accepted the correction for Implementation → Validation. Its Validation disposition and phase progression await the refreshed independent review.

## Related documents

- [Research](research.md)
- [Design](design.md)
- [Planning](planning.md)
- [Quality and evidence standards](../../coding_standards/QUALITY_GATES.md)


## Prior independent Validation NOGO and failure evidence

Independent QA returned NOGO on commit `87b7ce70` after observing conflicting complete native runs with no source changes. Both runs selected all 2777 items through the official SDK with 900-second receive and 600-second invocation budgets, unchanged native arguments/prerequisites/eight workers and verified client/server account `1Voudig`.

| Independent evidence | Actual outcome |
|---|---|
| First full run, receipt `b2f17289e1244d88ac9d93eef97c67de` | 1 failed, 2774 passed, 1 skipped, 1 xpassed, 229 warnings in 271.49 seconds |
| Isolated existing failing test | 1 passed, 9 warnings in 28.07 seconds |
| Second full run, receipt `ccaa458071f645db810a98bd1be4cdf6` | 2775 passed, 1 skipped, 1 xpassed, 229 warnings in 267.55 seconds |
| All 47 Python gates, receipt `6625481907c04248ba4846563747a7cf` | Format, lint and Pyright passed |
| Configured Mypy, receipt `507c28c33b2844b5b89b19adfc6dbd82` | 186 production files passed |
| Offline links, receipt `ab6df409f72c4eee92a472071da59af6` | 119 successful, 43 excluded, zero errors |

The sole failure was `test_explicit_json_and_filesystem_components_execute_with_native_pytest` in `tests/mcp_server/integration/templates/test_pytest_integration_test.py`. The test is unchanged relative to main and calls the direct native Pytest comparison helper, not the adapter. At that review, no product regression, baseline defect or timeout cause was established. The first SDK session closed without durable retention of its full failure traceback; its factual failure, item counts and receipt integrity were retained. A later pass does not erase that failure.

The skip is an existing manual proxy-restart test requiring RUN_MANUAL_TESTS. The XPASS is an existing xfail(strict=False) test. Neither marking was introduced by this work. All QA DTOs were fully paged and hash-verified; these facts are attributed to the independent review, not a producer replay of its server-local caches.

The review opened a P2 requiring causal investigation and an evidence-backed disposition. A new traceback was subsequently retained before cache closure and the required correction returned through Implementation, as recorded below. No Validation-to-Documentation approval is implied by later producer evidence.

## Causal reproduction and bounded test-harness maintenance

A new unchanged full configured run on 8bbd9dbc reproduced the same failing test and retained its complete failure section before the SDK session closed. Receipt `e611b3cd45574ed99795a959255ac689`: 798021 Unicode characters; UTF-8 SHA256 `a3993899184ebc675b3426a2cb80763e932fe8d2875704c3be45ce66f1b26d97`; 1 failed, 2774 passed, 1 skipped, 1 xpassed, 229 warnings in 283.45 seconds. Configured arguments, all 2777 items, native prerequisites and eight workers were unchanged. Post-run health receipt `46e28948dfa648c9afac61fd9b36f8c3` was healthy and the session closed normally.

The causally retained traceback is:

```text
test_pytest_integration_test.py:193
  result = native(native_case, [str(native_case.source)], [])
adapters/test_pytest.py:81
  subprocess.run(..., capture_output=True, timeout=45)
subprocess.py:556 -> communicate(timeout=timeout)
subprocess.py:1646 -> raise TimeoutExpired(self.args, orig_timeout)
subprocess.TimeoutExpired: [Python313/python.exe, -m, pytest,
  .../pytest-7036/popen-gw5/test_explicit_json_and_filesys0/
  native workspace/selected/test_native.py] timed out after 45 seconds
```

This proves exhaustion of the direct native comparison helper's finite 45-second budget during the complete concurrent suite; the test invokes no adapter. It does not retrospectively recover the first QA run's lost traceback or prove its unobserved exact cause. A representative concurrency probe of template/Pytest/Mypy/Pyright files passed 224 tests with 17 warnings in 93.56 seconds, receipt `27943c9538cd4ff0b48a9949c5525dc4`; that pass is supplementary and does not erase either full failure.

The audited return to Implementation, receipt `1b88beb9a1284fac8cfbb446e7cb0109`, skipped zero gates. Mechanical test maintenance preserves the native comparison helper's default 45-second deadline and adds a keyword-only `timeout_seconds` argument. Only the existing rendered-template native execution requests 120 seconds. All native arguments, fixture contents, result/three-test assertions, plugins, outer workers and selection remain unchanged. The run remains finitely bounded; no retry, skip, serialized suite or altered success policy is introduced. Production code and Approved Strategy are unchanged.

Two complete affected files passed 30 tests with 17 warnings in 39.29 seconds, receipt `4c9e109f58d0489289877bc72fde2d67`. Format, lint and Pyright passed both files, receipt `5c5150569d32403aa8558741bd4f6b0d`. An initial malformed check request combining profile and explicit checks was rejected before execution, receipt `036c08b26c7c454784fb398df37d4569`; the corrected explicit request supplies the actual gate evidence. No duplicate regression was added for this mechanical budget adjustment.

Independent QA accepted commit `01c7887a` for Implementation → Validation. QA repeated both full affected files: 30 passed, 17 warnings in 17.82 seconds, receipt `481da30589914df2814592d4397be925`; both-file format/lint/Pyright passed, receipt `e9fb91dbdc894b8bb7ccf6267eaa4191`. QA confirmed finite scope and preserved assertions, while explicitly reserving Validation closure for complete evidence and a new review. The refreshed complete Validation evidence below is offered for that decision; the producer does not declare independent approval.


## Refreshed Validation disposition for independent review

The complete configured run above includes the previously failing rendered-template native operation with its bounded 120-second comparison budget. All 2777 items ran under the existing native arguments, prerequisites and eight workers; no retry, selection reduction, skip or worker override was introduced. The actual result is 2775 passed, 1 skipped, 1 xpassed, 229 warnings in 286.09 seconds. The complete 48-path format/lint/Pyright gate and configured 186-source Mypy gate were rerun after the correction.

The earlier producer full pass remains historical evidence: receipt `f8a67efb6e1c42d0bf6f385843a4cd90`, 2775 passed/1 skipped/1 xpassed/229 warnings in 269.33 seconds, 796069 Unicode characters, UTF-8 SHA256 `311d1426dd41e2ff1ed29a8117439444baa7b1a74e23b835c0763403d37d9609`. It did not erase the subsequent independent failure. The later full causal reproduction establishes a concrete harness-budget defect and the reviewed correction addresses that defect. The first QA traceback remains unavailable; no unobserved exact cause is manufactured. Independent QA determines whether this retained history, direct causal reproduction, reviewed correction and refreshed complete evidence satisfy the outstanding Validation disposition.

The SDK server was healthy after the new run, receipt `958f623dec9f4d4f842a835dd912553d`, and the session closed normally. Its request was run_tests(scope='configured', tests=['python_tests'], timeout_seconds=600), with 900-second client receive budget and no native argument override. These budgets allow the full MCP receipt; the internal template comparison remains independently bounded at 120 seconds. Documentation work and phase progression await independent Validation review.
