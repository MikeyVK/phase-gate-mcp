<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=3zJkRylM4sIT4HzD sf=9PfER5JkyAoFQLRi -->

# Issue 469 — Native Adapter Validation

**Status:** Blocked — independent review requested
**Version:** 1.0
**Last Updated:** 2026-10-02


## Purpose

Record factual Validation evidence for the directly corrected unreleased adapter contract, including the installed-consumer gap and the incomplete full-suite proof.

## Scope In

Issue 469 implementation through 9bc12fe; separate E469/E474/E475 obligations; native adapter, invocation ownership, wire and public projections.

## Scope Out

Host-account sandboxing, external migration, legacy bridges, and approval to close or merge linked issues.

## Prerequisites

- Research 1.5, Design 1.3 and Planning 1.2; owner-approved B1–B6 including the bounded Pyright filename channel.
- Implementation independently reviewed on 9bc12fe; latest root-causes remain subject to full Validation.
- Python 3.13.7, Pytest 9.0.2 and installed package-local declared native prerequisites.




## Issue Number

#469




## Validation Status

FAIL



## Scope

Production HEAD 9bc12fe67479093e4a50fc4d3955db74ba02fe9b on bug/469-native-adapter-robustness. No production/test/configuration patch has been made in Validation.



## Obligations


### V\_NATIVE — full configured suite

**Evidence:**

- [Native Pytest adapter](<../../../mcp_server/bundled_adapters/pytest/test.py>)
- [Configured suite](<../../../pyproject.toml>)


**Outcome:** Incomplete. The required unmodified configured call reached the 300 s client limit; bounded repeats returned unavailable/timeout. No alternate worker count, collect-only or reduced selection is counted as full-suite success.



### V\_GATES — complete changed surface

**Evidence:**

- [Cached cb1c52e3dfe04e4b8c0a4d63ca149f38](<pgmcp://cache/runs/cb1c52e3dfe04e4b8c0a4d63ca149f38>)
- [Cached 31f9dc508924469f8c68cf6783e8c177](<pgmcp://cache/runs/31f9dc508924469f8c68cf6783e8c177>)
- [Cached 7d7c79dfc7e747e5951746fb053ae084](<pgmcp://cache/runs/7d7c79dfc7e747e5951746fb053ae084>)


**Outcome:** All 42 changed Python files pass format, lint and Pyright; configured production Mypy passes 186 files. Four changed Markdown files pass offline links. Actual CJS entrypoints, JSON role contracts and bundled manifests are exercised by the 383-test target run.



### E469-1/E469-3 — complete native selection and preservation

**Evidence:**

- [Ruff checks](<../../../tests/mcp_server/integration/adapters/test_ruff_checks.py>)
- [Mypy](<../../../tests/mcp_server/integration/adapters/test_mypy.py>)
- [Pyright](<../../../tests/mcp_server/integration/adapters/test_pyright.py>)
- [Pytest](<../../../tests/mcp_server/integration/adapters/test_pytest.py>)
- [Lychee](<../../../tests/mcp_server/integration/adapters/test_lychee.py>)


**Outcome:** Focused actual-native regressions pass: late findings in oversized selections, small controls, discovery/exclusions and input-channel refusal. Pinned native grammar bounds remain explicit; selections are not silently truncated or batched.



### E469-2/E469-4/E475-1 — truthful completion, cause and prerequisite

**Evidence:**

- [Ruff checks/failure classification](<../../../tests/mcp_server/integration/adapters/test_ruff_checks.py>)
- [Ruff fixes](<../../../tests/mcp_server/integration/adapters/test_ruff_fixes.py>)
- [Commitlint](<../../../tests/mcp_server/integration/adapters/test_commitlint.py>)
- [Python syntax](<../../../tests/mcp_server/integration/adapters/test_python_syntax.py>)
- [TypeScript syntax](<../../../tests/mcp_server/integration/adapters/test_typescript_syntax.py>)


**Outcome:** Targeted regressions pass for causal diagnostics independent of filenames/quoted input, metadata refusal and actual native version admission. Intentional Ruff exit-zero and Pytest collect-only/exit5 remain native policies.



### E474-1/E-CROSS — invocation ownership, resources and public evidence

**Evidence:**

- [Runtime](<../../../tests/mcp_server/integration/execution/test_process_runtime.py>)
- [Process termination](<../../../tests/mcp_server/integration/execution/test_process_stopping.py>)
- [Content preparation](<../../../tests/mcp_server/integration/execution/test_content_input.py>)
- [Installed consumer](<../../../tests/mcp_server/integration/test_installed_distribution_v3.py>)


**Outcome:** Owned-resource and public result preservation regressions pass, including cleanup failure and modified fix sources. However, the installed distribution smoke still constructs a request without required execution_context and fails; D1_PROTOCOL/D1_FIXTURES migration is incomplete.





## Evidence


### Required complete-suite run and bounded factual retry

run_tests(scope='configured',tests=['python_tests']) with configured args[] and unchanged Pytest addopts [-v,--strict-markers,--tb=short,-n,auto] reached the client300 s timeout without a cache receipt. The same selection/arguments with timeout_seconds240 returned unavailable/timeout, message adapter_deadline_expired, zero captured output and confirmed termination. No conclusion about native pass/fail can be derived from withheld subprocess output.

**Sources:**

- [Cached 90cb8b6314aa4418ae592748bc48bc1d](<pgmcp://cache/runs/90cb8b6314aa4418ae592748bc48bc1d>)
- [Test binding](<../../../.pgmcp/config/tests.yaml>)
- [MCP launcher](<../../../.codex/config.toml>)


**Invocation:** run_tests({scope:'configured',tests:['python_tests']}); repeat with timeout_seconds:240



**Observed Result:** No completed full-suite proof.




### Diagnostic collection and execution traces

Collection-only with -n0 collected 2777 tests in 2.46 s. Full-selection -x at 180 s and -x -n2 at 240 s timed out with confirmed termination. A120 s native --debug run showed ongoing passing tests and an installed-consumer failure; --debug also triggers Pluggy UnicodeEncodeError on surrogate parametrization during collection, so the trace is diagnostic and its counts/timing are not acceptance evidence. QA trace overlap further prevents clean timing attribution.

**Sources:**

- [Cached 6990540fa70f48bf9da1642acd6668cf](<pgmcp://cache/runs/6990540fa70f48bf9da1642acd6668cf>)
- [Cached 03388e77d68648f2b451e69f8dd75fdc](<pgmcp://cache/runs/03388e77d68648f2b451e69f8dd75fdc>)
- [Cached 2221699fae3e40abb11699bba6ec2d0c](<pgmcp://cache/runs/2221699fae3e40abb11699bba6ec2d0c>)
- [Cached 124c346f69cf4763b75edaab19f6f194](<pgmcp://cache/runs/124c346f69cf4763b75edaab19f6f194>)



**Observed Result:** Execution duration, not ordinary collection, is the full-run barrier; precise sole cause remains unproven.




### Installed entrypoint reproduction

The existing wheel/catalog/entrypoint smoke fails at its installed commitlint invocation: returncode2, invalid_request, location[execution_context], code missing_field. The direct request includes operation, target_path, content and args but omits the newly mandatory context. The installed adapter rejection is correct; the consumer fixture was missed by the contract migration.

**Sources:**

- [Installed distribution smoke](<../../../tests/mcp_server/integration/test_installed_distribution_v3.py>)
- [Cached 38aa9812d9454f50ad622b400e32040a](<pgmcp://cache/runs/38aa9812d9454f50ad622b400e32040a>)


**Invocation:** run_tests({scope:'targets',targets:['tests/mcp_server/integration/test_installed_distribution_v3.py'],tests:['python_tests'],timeout_seconds:240})



**Observed Result:** 1 failed,9 warnings in 28.57 s; configured args[].




### Actual native adapter and invocation regressions

All 383 tests passed with 17 existing warnings in 104.49 s using configured args[] and normal native worker defaults. Target scope contains every changed adapter integration file, all four changed execution integration files, and test_catalog.py. Tests launch native programs, validate role JSON schemas, compare native effects/results and exercise both changed CJS entrypoints.

**Sources:**

- [Cached 55478afa6ad440d6987f5d5e2ae5cec3](<pgmcp://cache/runs/55478afa6ad440d6987f5d5e2ae5cec3>)
- [Native adapters](<../../../tests/mcp_server/integration/adapters>)
- [Runtime regressions](<../../../tests/mcp_server/integration/execution>)
- [Catalog/role schemas](<../../../tests/mcp_server/unit/execution/test_catalog.py>)


**Invocation:** run_tests(scope='targets',targets=<15 files below>,tests=['python_tests'],timeout_seconds=240)

```text
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
tests/mcp_server/unit/execution/test_catalog.py
```



**Observed Result:** 383 passed; focused proof only, not a replacement for V_NATIVE.




### Broad Python gate inventory

The main-to-branch diff resolves53 changed files and42 Python files. Every stat abbreviation was resolved to a unique tracked path; the explicit list below is the complete Python target vector. Format:42 already formatted; lint:all passed; Pyright1.1.408:42 analyzed,0 errors/0 warnings. Configured Mypy1.19.1 passes 186 production files.

**Sources:**

- [Cached 8b8791a19deb41898bdc4c80fd817461](<pgmcp://cache/runs/8b8791a19deb41898bdc4c80fd817461>)
- [Cached cb1c52e3dfe04e4b8c0a4d63ca149f38](<pgmcp://cache/runs/cb1c52e3dfe04e4b8c0a4d63ca149f38>)
- [Cached 31f9dc508924469f8c68cf6783e8c177](<pgmcp://cache/runs/31f9dc508924469f8c68cf6783e8c177>)


**Invocation:** run_checks(scope='targets',targets=<42 .py paths>,checks=['python_format','python_lint','python_pyright']); run_checks(scope='configured',checks=['python_types'])

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
tests/mcp_server/unit/execution/test_catalog.py
tests/mcp_server/unit/execution/test_check_selection.py
tests/mcp_server/unit/execution/test_check_service.py
tests/mcp_server/unit/execution/test_fix_service.py
tests/mcp_server/unit/execution/test_test_service.py
```



**Observed Result:** All selected gates passed. No mixed branch-scope Python extension filtering.




### Markdown and server health

Offline Lychee links on Research, Design, Planning and effect-probe pass:131 links,103 successful,28 exclusions,0 errors. Server2.0.0 remains healthy on win32, PID41964, after confirmed process termination.

**Sources:**

- [Cached 7d7c79dfc7e747e5951746fb053ae084](<pgmcp://cache/runs/7d7c79dfc7e747e5951746fb053ae084>)
- [Cached e7c3f28836de443d8cf7f2b8be4de100](<pgmcp://cache/runs/e7c3f28836de443d8cf7f2b8be4de100>)



**Observed Result:** Passed links and healthy server.






## Demonstration

Reproduce the installed consumer gap with the one existing test file and configured arguments. Review actual causal Ruff regressions and public cleanup projections in the 383-test receipt. Full-suite execution remains required; diagnostics are the closest factual fallback while it is unavailable.



## Preservation

B1–B6 are unchanged: direct unreleased identity1 correction; mandatory JSON scratch context; one complete native operation; truthful outcomes/versions/diagnostics; ordinary native cache/report effects under trusted host-account execution. Existing CLI/config precedence, configured discovery, operation order, fix evidence and intentional native success policies remain covered by useful regressions.



## Containment

No OS sandbox or filesystem/network/credential isolation is claimed. PGMCP owns exclusively created invocation directories and cleans after confirmed termination; unconfirmed termination preserves resources. Compatible native caches/reports outside selected sources remain allowed.



## Failures

- D1_PROTOCOL/D1_FIXTURES: installed distribution consumer omitted required execution_context; existing smoke fails with missing_field. Must be corrected in Implementation and independently reviewed.
- V_NATIVE: full configured suite lacks a completed verdict within existing native/client time limits. Do not treat383 targeted passes, collection-only or alternate workers as full-suite success.



## Caveats

- Cached receipts are transient; the factual outcomes, exact vectors and source regressions are recorded here for durable review.
- Native --debug changes tracing behavior, including surrogate collection errors, and overlapped another diagnostic trace; neither trace establishes a clean full-suite verdict or sole timeout cause.
- Pyright1.1.408 explicit filenames with spaces/line separators/native trimming or invalidUTF8 are refused as unsupported_input under the owner's approved bounded stdin convention.
- Lychee positional fallback remains bounded when files_from already occupies the native filename channel.



## Risks


### Incomplete broad-suite proof

Retain FAIL, correct the installed-consumer fixture via the implementation workflow, and obtain a completed full configured run without reduced selection or alternate success criteria.


**Consequence:** No Validation→Documentation authorization is asserted.





## Deferred Work


### Issue 474 wording alignment before acceptance/closure

@co owns reconciliation of the superseded strict destination-policy wording with approved trusted-host/native-cache/report strategy. Separate469/474/475 disposition is retained; no issue is implicitly closed here.


**References:**

- [Approved strategy](<research.md>)
- [Disposition requirement](<planning.md>)





## Related Documents

- [Research 1.5](<research.md>)
- [Design 1.3](<design.md>)
- [Planning 1.2](<planning.md>)


