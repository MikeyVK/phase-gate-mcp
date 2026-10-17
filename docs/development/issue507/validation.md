<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Issue 507 — Validation

**Status:** PASS — independent Validation review requested  
**Version:** 0.2  
**Last Updated:** 2026-10-17

## Purpose

Record the completed native validation of the owner-approved harness, schema, resource and typing maintenance, including the failed first attempt and its bounded repair.

## Scope

Validated implementation snapshot: `9cb4e6394cf107d3bd7a703c35bc278717b798dd`, following the earlier implementation at `e805b108`. The normal Validation transition is the only subsequent workflow-state change. No production or native configuration changed during the test repair.

Included: restart task ownership, collection diagnostics, removal of an empty manual placeholder, stale XPASS repair, `schema_document`, Python 3.13, MCP SDK 1.30 resource returns and the approved per-rule PEP 695 changes. Excluded: SDK 2 migration, a higher Python baseline, compatibility bridges, new diagnostic test suites and gate waivers.

## Prerequisites

- Independent QA approved Implementation → Validation on `e805b108`.
- The owner approved returning to Implementation for the two stale configuration tests (reply: “Prima”); the force-transition audit records the reason and approval.
- Independent QA approved the bounded repair on `9cb4e639` before the final full run. QA turn: `01a14870-6016-7923-a2ad-9b10aac6c27b`.
- Test/client budgets remained 1200/1800 seconds; the complete native suite was not split or narrowed.

## Validation Status

PASS for the executed verification. Independent QA owns the phase-progression decision.

## Evidence

| Invocation and scope | Observed result | Supplemental receipt |
| --- | --- | --- |
| `run_tests(scope="configured", timeout_seconds=1200)`; selected `python_tests`, no caller targets or arguments | **2913 passed in 416.58 seconds**, 8 workers, native exit 0; no warnings, skips or XPASS reported. Complete, no termination problem, capture not truncated. | `0cb248439a914d9a867ece916ebf103f` |
| `run_checks(scope="branch", timeout_seconds=600)`; default `python_review`, native per-check branch selection | Formatting: 43 Python files; lint passed; Mypy: 29 production files; Pyright: 29 production files, 0 errors/0 warnings. All native exits 0. | `617082d635da440b85a4d5ee3648dfbf` |
| `run_checks(scope="configured", checks=["python_types"], timeout_seconds=600)` | 191 production source files passed. Reused unchanged production/config evidence; the subsequent repair modified only tests and the report. | `0852896198dd41709de6a5d323757e43` |
| `run_tests(scope="targets", targets=["tests/mcp_server/integration/adapters/test_pyright.py", "tests/mcp_server/integration/test_rollout_configuration.py"], tests=["python_tests"], args={"python_tests":["-r","sxX"]}, timeout_seconds=240)` | 55 passed in 53.63 seconds, native exit 0. | `c636eab80048463e808d2bede1f0a655` |
| `run_checks(scope="targets", targets=[the same two test files], checks=["python_format","python_lint","python_pyright"], timeout_seconds=180)` | All passed; Pyright analyzed 2 files with 0 errors/0 warnings. | `112102770c7b4b79813a2a077a8b2b39` |
| `run_checks(scope="targets", targets=["README.md","docs/setup/README.md","docs/setup/dev-isolation.md","docs/development/issue507/research.md"], checks=["markdown_links"], timeout_seconds=180)` | 71 occurrences, 58 unique; 32 successful, 39 excluded, 0 errors. Existing offline policy excludes external URLs; no online verification claim. The edited report is separately checked by safe-edit validation. | `adb2ced9d9974e64956e38330c05abf5` |

The final suite used the unchanged native [pytest settings](../../../pyproject.toml). The runtime was Python 3.13.7 with pytest 9.0.2. Gates used Ruff 0.15.6, Mypy 1.19.1 and Pyright 1.1.408. The broad capture size was inspected before reading its opening and final summary; the 824,211-character result was not downloaded blindly.

## First Attempt and Bounded Repair

The first completed `run_tests(scope="configured", timeout_seconds=1200)` on `e805b108` produced **2912 passed, 2 failed in 458.00 seconds**, native exit 1, with no timeout or truncated capture (supplemental `b646aae98e4e4a6991cd73b107634e46`). Its FAIL remains historical evidence and was not waived.

| Failure | Cause and repair |
| --- | --- |
| [test_native_configuration_preservation_and_editor_target](../../../tests/mcp_server/integration/adapters/test_pyright.py) | Read the repository's Python version and demanded 3.11 after the approved move to 3.13. The existing native-versus-adapter diagnostics, configured-rule behavior and version-override comparison now use an explicit isolated test configuration. The 3.11 analyzer target is scenario input, not server compatibility support. The isolated TOML is checked for preservation. |
| Removed `TestRolloutConfiguration.test_pyrightconfig_native_settings_preservation` in [rollout tests](../../../tests/mcp_server/integration/test_rollout_configuration.py) | Only asserted fixed repository config values, including 3.11; it executed no product behavior. Removed that method and its unused import. No replacement content snapshot or new case was added. |

The suite changed from 2914 to 2913 items because one content-only test was removed. The real Pyright behavior test remains and passes. The repair added no production changes, native checker exceptions or test cases.

## Live Server and Resource Demonstration

After Implementation review, `health_check()` reported healthy PID 66008. `restart_server(reason="Issue #507 Validation: load approved Python 3.13/SDK 1.30 resource and typing changes from e805b108 after independent QA GO.")` succeeded. After 3.5 seconds, `health_check()` reported healthy PID 31008 with uptime 9.97 seconds.

`read_mcp_resource(server="phase_gate_mcp", uri="pgmcp://cache/runs/bbbcf149f57f4d8698d1e38d5d1d017d?offset=0&limit=2000")` returned that exact requested URI and `text/plain` content with the healthy PID. Work-context, Git/issue, check and test calls remained usable through the current client. Installed/test metadata: Python 3.13.7, MCP 1.30.0, Pydantic 2.11.7. Product version 3.0.0 in health output is a separate fact.

See the [central resource boundary](../../../mcp_server/server.py), [schema transport](../../../mcp_server/core/tool_execution.py) and [restart behavior tests](../../../tests/mcp_server/tools/test_admin_tools.py). The later repair changed only tests, so this live demonstration remains fresh.

## Preservation and Containment

The [approved strategy and implementation record](research.md) retains explicit covariance, seven declaration-local UP046 exceptions, the strict Pydantic Mypy plugin (`init_typed=true`, `init_forbid_extra=true`) and one field-local Mypy `misc` exception. No global Ruff exclusions or Pyright weakening were introduced.

The focused 191-test Implementation evidence complements the final complete suite. Temporary positive/negative typing probes are diagnostic evidence, not permanent suite additions. Final test execution left production, native configuration and planning data unchanged; Git status showed only the expected phase transition before this report update.

## Failures

None remain in the final executed verification. The two first-attempt failures and their repairs are retained above.

## Caveats

- Native coverage was not requested; configured addopts contain no `--cov`. No numeric coverage claim.
- Tool receipts supplement the durable invocations and outcomes above; cache persistence is not assumed.
- Passing checks do not replace independent architecture/phase review or claim SDK 2 compatibility.

## Deferred Work

[MCP SDK 2/higher Python and suppression reassessment — #513](https://github.com/MikeyVK/phase-gate-mcp/issues/513) owns the next-major options, version-specific evidence and owner strategy. Its scope includes substantive review of global, per-file and local checker suppressions. Current exceptions are neither automatically permanent nor removed without contract evidence. Coordination has recorded the follow-up. No other deferred work was identified within this bounded repair.

## Related Documents

- [Approved strategy and implementation evidence](research.md)
- [Issue 507](https://github.com/MikeyVK/phase-gate-mcp/issues/507)
- [Native check bindings](../../../.pgmcp/config/checks.yaml)
- [Setup requirements](../../setup/README.md)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-16 | @imp validator | Record completed native full suite, two stale configuration-test failures, passing gates and live server refresh. |
| 0.2 | 2026-10-17 | @imp validator | Preserve the first-attempt failures, record the owner-approved bounded repair and independent re-entry GO, and capture the complete passing rerun and fresh branch gates. |
