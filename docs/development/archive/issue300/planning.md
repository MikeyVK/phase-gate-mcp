<!-- docs\development\issue300\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-03T17:27Z updated= -->
# run_tests: Expose Actionable Failure Details — TDD Cycle Plan

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-03

---

## Purpose

Break down the design.md v1.2 implementation into four sequenced TDD cycles with explicit, binary success criteria and JSON deliverables that gate cycle transitions during implementation.

## Scope

**In Scope:**
mcp_server/managers/pytest_runner.py, mcp_server/tools/test_tools.py, tests/mcp_server/unit/managers/test_pytest_runner.py, tests/mcp_server/unit/tools/test_test_tools.py

**Out of Scope:**
OSError / TimeoutExpired paths (RNF-5 — unchanged), coverage support (issue #253 Gap 3), MCP protocol layer, other MCP tools

## Prerequisites

Read these first:
1. design.md v1.2 QA LGTM (commit f372b11)
2. research.md v1.3 — all 8 findings documented
3. Python 3.13.7, Pydantic v2, anyio MCP server
4. pytest-xdist default in pyproject.toml
---

## Summary

Four TDD cycles implement design.md v1.2 in dependency order: contract types first, then the stderr pipeline, then tool-result routing, then the xdist regex fix. Each cycle is self-contained and can be quality-gated independently. The order is enforced by field-import dependencies — later cycles consume fields introduced in earlier ones.

---

## TDD Cycles


### Cycle 1: ExitCodePolicy + PytestResult contract

**Goal:** Expand ExitCodePolicy.outcome Literal to three values (ok|error|raise); add is_error: bool and stderr: str = '' fields to PytestResult; update _parse_output() assignment. No behavior change for exit 0/1/5/99 paths — all existing tests must remain green.

**Tests:**
- test_c1_parse_output_exit2_sets_is_error_true — exit 2 → result.is_error == True, result.should_raise == False
- test_c1_parse_output_exit3_sets_is_error_true — exit 3 → result.is_error == True
- test_c1_parse_output_exit4_sets_is_error_true — exit 4 → result.is_error == True
- test_c1_parse_output_exit0_sets_is_error_false — exit 0 → result.is_error == False
- test_c1_parse_output_exit99_should_raise_unchanged — exit 99 → result.should_raise == True, result.is_error == False
- test_c1_pytest_result_default_stderr_is_empty_string — PytestResult() with no stderr kwarg → result.stderr == ''

**Success Criteria:**
- All 6 new tests pass (RED→GREEN confirmed)
- All pre-existing test_pytest_runner.py tests still pass
- run_quality_gates(scope='files', files=['mcp_server/managers/pytest_runner.py']) clean — mypy sees outcome as Literal['ok','error','raise']
- result.should_raise still True for exit 99 (RNF-5 guard not broken)



### Cycle 2: Stderr pipeline: run() → _parse_output() → PytestResult

**Goal:** Add stderr parameter to _parse_output(stdout, stderr, returncode); pass execution.stderr from PytestRunner.run() through to PytestResult.stderr.

**Tests:**
- test_c2_run_populates_result_stderr — monkeypatch _execute returning stderr='INTERNALERROR\nfoo' → result.stderr == 'INTERNALERROR\nfoo'
- test_c2_run_empty_stderr_yields_empty_string — monkeypatch _execute returning stderr='' → result.stderr == ''
- test_c2_stderr_not_mixed_into_stdout_parse — _parse_output does not receive stderr content in stdout arg

**Success Criteria:**
- All 3 new tests pass
- Existing tests pass (_run() helper extended to _PytestExecution(stdout, stderr, returncode) with stderr='' default)
- run_quality_gates(scope='files', files=['mcp_server/managers/pytest_runner.py']) clean — _parse_output signature matches all call sites

**Dependencies:** Cycle 1 — PytestResult.stderr field must exist


### Cycle 3: _to_tool_result() routing + test_test_tools rewrites

**Goal:** Implement _to_tool_result() routing split on result.is_error (§3.2 pseudo-code); expand content[0] for exit 1 with per-FailureDetail lines; rewrite exit 2/3/4 tests from pytest.raises(ExecutionError) to ToolResult(is_error=True) assertions; update _make_pytest_result() helper with is_error and stderr kwargs. execute() raise-branch for exit 99 RETAINED.

**Tests:**
- test_c3_to_tool_result_exit1_content0_includes_failure_lines — failures non-empty → content[0] has 'FAILED test_id — reason'
- test_c3_to_tool_result_exit1_no_failures_content0_is_summary_only — empty failures → content[0] == summary_line
- test_c3_to_tool_result_exit2_returns_tool_result_is_error_true — is_error=True → ToolResult(is_error=True)
- test_c3_to_tool_result_exit2_content0_includes_stderr_hint — nonempty stderr → content[0] has 'stderr: <first line[:120]>'
- test_c3_to_tool_result_exit2_content0_no_hint_when_stderr_empty — empty stderr → content[0] == summary_line only
- test_c3_to_tool_result_exit2_content1_has_stderr_tail_50_lines — 60-line stderr → content[1]['stderr'] has last 50 lines
- REWRITE test_c4_run_tests_interrupted (r.124) → ToolResult(is_error=True)
- REWRITE test_c4_run_tests_internal_error (r.145) → ToolResult(is_error=True)
- REWRITE test_c4_run_tests_usage_error (r.168) → ToolResult(is_error=True)
- test_c3_execute_exit99_still_raises_execution_error — UNCHANGED (r.213 guard)

**Success Criteria:**
- All new and rewritten tests pass
- test for exit 99 (r.213) still raises ExecutionError — UNCHANGED
- run_quality_gates(scope='files', files=['mcp_server/tools/test_tools.py']) clean
- run_tests(path='tests/mcp_server/unit/tools/test_test_tools.py') all green

**Dependencies:** Cycle 1 — PytestResult.is_error and PytestResult.stderr must exist, Cycle 2 — result.stderr available in _to_tool_result() for content[1] payload


### Cycle 4: xdist _extract_traceback() regex fix

**Goal:** Add optional (?:[gw\d+]\s+)? prefix to _extract_traceback() FAILURES section pattern. Tests go via run() + monkeypatch on _execute with crafted stdout — no direct call to _extract_traceback (§14).

**Tests:**
- test_c4_extract_traceback_with_xdist_prefix_gw0 — crafted stdout with '[gw0] ___ test_foo ___' header → failure.traceback non-empty
- test_c4_extract_traceback_with_xdist_prefix_gw12 — double-digit worker [gw12] → traceback extracted correctly
- test_c4_extract_traceback_without_prefix_unchanged — standard FAILURES header (no prefix) → traceback still extracted (regression guard)

**Success Criteria:**
- All 3 new tests pass via run() + monkeypatch on _execute
- Existing traceback extraction tests still pass (no regression)
- run_quality_gates(scope='files', files=['mcp_server/managers/pytest_runner.py']) clean
- run_tests(path='tests/mcp_server/unit/managers/test_pytest_runner.py') all green

**Dependencies:** Cycle 2 — _run() helper extended to _PytestExecution(stdout, stderr, returncode)

---

## Risks & Mitigation

- **Risk:** PytestResult is a frozen dataclass — field order matters for any positional construction sites
  - **Mitigation:** All construction sites use keyword arguments; verify with mypy after C1 before proceeding
- **Risk:** _run() helper in test_pytest_runner.py is shared by many tests — extending it risks silent breakage
  - **Mitigation:** Add stderr='' default to mock; all existing callers pass stdout + returncode by keyword and are unaffected
- **Risk:** xdist regex change could over-match if test names contain [gwN] substrings
  - **Mitigation:** Pattern anchors on _{3,} blocks; [gwN] must precede the underscores; false-positive risk negligible

## Related Documentation
- **[docs/development/issue300/design.md (v1.2)][related-1]**
- **[docs/development/issue300/research.md (v1.3)][related-2]**
- **[mcp_server/managers/pytest_runner.py][related-3]**
- **[mcp_server/tools/test_tools.py][related-4]**

<!-- Link definitions -->

[related-1]: docs/development/issue300/design.md (v1.2)
[related-2]: docs/development/issue300/research.md (v1.3)
[related-3]: mcp_server/managers/pytest_runner.py
[related-4]: mcp_server/tools/test_tools.py

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |