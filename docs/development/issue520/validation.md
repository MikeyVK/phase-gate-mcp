<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue \#520 — Startup admission validation

**Status:** REVIEW REQUESTED  
**Version:** 1.0  
**Last Updated:** 2026-10-18

## Purpose

Verify GREEN commit 7f783100291c5db79fb44a6db2016921383e67b2 against the approved startup policy and preservation boundaries.

## Scope Out

Shared services, activation retries, compatibility bridges, release/builder changes, host activation and a new coverage gate.

## Issue Number

#520

## Cycle

C_1

## Validation Status

PASS

## Scope

Selected Python 3.15.0 / MCP SDK 2.3.0. One implementation cycle; no production or test edits during Validation.

## Obligations

### D\_1.1 — Existing ConfigLoader composes required immutable startup policy.

**Evidence:**

- [Public loader cases](<../../../tests/mcp_server/unit/config/test_loader.py>)
- [ServerConfig](<../../../mcp_server/config/schemas/server_config.py>)

**Outcome:** Basis/override, independent early read, required basis, strict numeric bounds and deadline relationship pass.

### D\_1.2 — Native exclusion and bounded contention retain truthful causes.

**Evidence:**

- [Native lock behavior](<../../../tests/mcp_server/integration/test_template_activation.py>)

**Outcome:** Release-before-deadline, exhaustion, owned-instance misuse, same-errno open failure, invalid native descriptor, failed-stream cleanup and fresh-empty-file cross-process exclusion pass. Activation remains single-attempt.

### D\_1.3 — Entry points use one policy without disabling setup/renewal.

**Evidence:**

- [Proxy entrypoint cases](<../../../tests/mcp_server/core/test_proxy.py>)
- [Installed and recovery behavior](<../../../tests/mcp_server/integration/test_target_startup.py>)
- [Renewal CLI](<../../../tests/mcp_server/integration/test_renewal_cli.py>)

**Outcome:** Configured proxy construction and fail-before-launch on missing basis pass. Existing CLI/renewal cases and the installed fresh-init/migration case pass; the latter exercises bootstrap consuming the packaged new basis.

### D\_1.4 — Public MCP behavior and complete acceptance.

**Evidence:**

- [Concurrent startup and health diagnostics](<../../../tests/mcp_server/integration/test_target_startup.py>)

**Outcome:** Three clients become healthy with equal normal catalogs. Exhaustion exposes only health/restart and the timeout/path/attempts plus original native cause. The complete configured suite passes.

## Evidence

### Full native-configured suite

Final complete run: 2979 passed, zero failures/skips, 436.14s, native exit 0. Python 3.15.0 / pytest 9.1.1, configured testpaths tests/mcp_server, eight workers; no coverage opt-in. Initial complete run: 2976 passed, 3 failed, 371.65s, native exit 1. All three package tests stopped at 'No module named build'; this environment prerequisite was restored before the successful targeted and complete reruns.

**Sources:**

- [Native test policy](<../../../pyproject.toml>)
- [Offline installed-package fixture](<../../../tests/mcp_server/fixtures/installed_distribution.py>)

**Invocation:** run_tests(scope="configured", tests=["python_tests"], args={"python_tests":["-q","--junitxml=.pgmcp/temp/issue520/validation.xml"]}, timeout_seconds=1800)

### Package test prerequisites restored without source changes

3 passed, 152.26s, exit 0. Provisioned build==1.6.1, setuptools==84.0.0 and wheel==0.48.0 in .venv315, matching the earlier #517 evidence environment; pip also installed pyproject_hooks==1.3.3. No runtime dependency declaration or source changed.

**Sources:**

- [Installed distribution behavior](<../../../tests/mcp_server/integration/test_installed_distribution_v3.py>)
- [Fresh installed initialization](<../../../tests/mcp_server/integration/test_v3_cutover.py>)

**Invocation:** run_tests(scope="targets", targets=["tests/mcp_server/integration/test_target_startup.py","tests/mcp_server/integration/test_v3_cutover.py","tests/mcp_server/integration/test_installed_distribution_v3.py"], tests=["python_tests"], args={"python_tests":["-q","-k","installed_candidate or fresh_installed_init_and_startup or complete_wheel"]}, timeout_seconds=900)

### Focused corrected behavior and causal RED

45 passed, 77.90s, exit 0 on final source. RED commit 0ec82c4406fb55aaaa37ab8ba5d9dbd0e3271eb7 recorded 11 expected failures for missing new configuration/wait interfaces before GREEN. Corrected tests prove public behavior, not source/document strings.

**Sources:**

- [Loader behavior](<../../../tests/mcp_server/unit/config/test_loader.py>)
- [Startup behavior](<../../../tests/mcp_server/integration/test_target_startup.py>)

**Invocation:** run_tests(scope="targets", targets=["tests/mcp_server/unit/config/test_loader.py","tests/mcp_server/core/test_proxy.py","tests/mcp_server/integration/test_template_activation.py","tests/mcp_server/integration/test_target_startup.py"], tests=["python_tests"], args={"python_tests":["-q","-k","not installed_candidate"]}, timeout_seconds=900)

### Required branch and configured quality gates

Both passed. Ruff 0.17.1: 475 configured files formatted, lint clean. Mypy 2.4.0: 192 production files clean, with existing unused tests.* section note. Pyright 1.1.414: 192 configured production files, zero errors/warnings. New YAML basis passed targeted yaml_configuration. No new suppressions or coverage opt-in.

**Sources:**

- [Native checker policy](<../../../pyproject.toml>)
- [Startup basis](<../../../.pgmcp/config/defaults/server.yaml>)

**Invocation:** run_checks(scope="branch", checks=["python_format","python_lint","python_pyright"], timeout_seconds=900); run_checks(scope="configured", checks=["python_format","python_lint","python_types","python_pyright"], timeout_seconds=1200)

### Actual 30/.25/60 policy succeeds for three concurrent starts

Normal source proxy entrypoint, no wrappers, artificial holds or coverage instrumentation: healthy after 10.462 / 15.968 / 21.406 seconds, with 49 tools each, equal catalogs, separate process identities and no startup diagnosis. Initialize completed after 10.415 / 15.918 / 21.358 seconds. Functional suite fixture deliberately uses 90s lock / 180s proxy / 210s client budgets for instrumented/load execution; it does not establish default latency.

**Sources:**

- [Normal composition entrypoint](<../../../mcp_server/core/proxy.py>)
- [Source admission](<../../../mcp_server/bootstrap.py>)

## Demonstration

Reproduce the uninstrumented observation with the selected Python 3.15 / MCP 2.3 environment in a valid workspace: load ConfigLoader(config_root).load_server_config() and confirm 30 / 0.25 / 60; create three concurrent MCP SDK clients using StdioServerParameters(command=sys.executable, args=["-m","mcp_server.core.proxy"], cwd=workspace, env=the selected workspace/root environment), with read_timeout_seconds=75 and cache=None. For each client record monotonic elapsed time through initialize, tools/list and tools/call health_check; compare complete tool-name sets and assert status="healthy" and startup_diagnostic=null. Use the current source on PYTHONPATH for source acceptance, or a reviewed installed candidate for package acceptance. Do not patch UpgradeLock/MCPProxy or author a timing override for this observation. On Windows, the proxy's launcher PID can differ from the public health PID.

## Preservation

Original admission window, unresolved-recovery refusal, activation exclusion, proxy generation/restart behavior and complete causal diagnostics remain covered. The full suite retains native testpaths tests/mcp_server and eight workers. Production remains at the independently reviewed GREEN snapshot.

## Containment

No gate exception, new test framework, permanent diagnostic module or extra dependency/version-matrix tests. Transient cache receipts are supplemental; this report records exact native routes and observations.

## Failures

- Initial full run failed for missing build prerequisites; the three affected cases and final complete suite pass after provisioning. No outstanding validation failures.

## Caveats

- Observed startup durations are measurements, not general latency guarantees.
- Coverage remains opt-in; #517's issue-specific extra90% gate is not a #520 acceptance requirement.
- Installing the new required basis in existing workspaces is explicit; --upgrade remains template-only. Changing coordinated startup policy requires full proxy/child relaunch; restart_server alone retains the existing proxy deadline.
- No active host config or installed production server was switched by this issue.

## Related Documents

- [Approved Research](<research.md>)
- [Design](<design.md>)
- [Planning](<planning.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-18 | @imp validator | Record complete native acceptance, focused behavior, restored build prerequisites and measured three-client startup. |
