<!-- docs\development\issue397\validation.md -->
<!-- template=validation_report version=fe38a66d created=2026-06-11T19:02Z updated=2026-06-11 -->
# Validation Report - Add verbose traceback and stdout capture to run_tests tool

**Status:** APPROVED  
**Version:** 1.0.0  
**Last Updated:** 2026-06-11  
**Validation Outcome:** PASS  
**Issue:** #397  
**Cycle:** 5  

---

## Scope

`RunTestsInput`, `RunTestsTool`, `PytestRunner`, `RunQualityGatesTool` dead code cleanup, and related unit and integration tests.

---

## Prerequisites

- Base workspace verified and clean.
- Python environment activated and all package dependencies installed.
- Authoritative reference documents: `design.md`, `planning.md`, `ARCHITECTURE_PRINCIPLES.md`.

---

## Summary Verdict

**PASS**. All implementation cycles are complete, all 2884 tests pass cleanly, and branch-wide quality gates report 0 violations.

---

## Test & Quality Gate Evidence

### Full-Suite Test Result
- Command: `run_tests(scope='full')`
- Output: `2884 passed, 5 skipped, 2 xfailed, 1 xpassed, 22 warnings in 41.42s`

### Branch Quality-Gate Result
- Command: `run_quality_gates(scope='branch')`
- Output: `6/6 active (1 skipped) [branch · 11 files] - Success`

---

## Deliverables Mapping

| Deliverable ID | Description | Observed Evidence | Status |
|---|---|---|---|
| **D1.1** | `IPytestRunner.run` / `PytestRunner.run` accept `verbose` keyword argument | Signatures updated and verified backwards-compatible. | **PASS** |
| **D1.2** | `FakePytestRunner` signature alignment | Updated signature in `fake_pytest_runner.py`; tests compile/pass. | **PASS** |
| **D2.1** | `RunTestsInput` schema includes `verbose` parameter | Detailed description added to `verbose` field in `RunTestsInput`. | **PASS** |
| **D2.2** | Path-based validation for `verbose=True` | `RunTestsInput` validator raises `ValueError` if `verbose=True` without specific test file path. | **PASS** |
| **D3.1** | `RunTestsTool` builds correct command line | Generates `--tb=long` when `verbose=True`, and `--tb=short` when `verbose=False`. | **PASS** |
| **D3.2** | Traceback extraction capped at `MAX_FAILURES_DETAILED` | Capped at 3 detailed tracebacks when `verbose=True`. | **PASS** |
| **D3.3** | Tracebacks empty when `verbose=False` | PytestRunner extraction returns empty traceback strings. | **PASS** |
| **D4.1** | ToolResult JSON empty tracebacks when `verbose=False` | Verified in JSON data payload. | **PASS** |
| **D4.2** | `RecoveryNote` formatting and suggestion note | Appends `\n🩹 Recovery: Some tests failed. To see detailed tracebacks and stdout/stderr, rerun with verbose=True. Suggested command: run_tests(...)` on failure. | **PASS** |
| **D5.1** | Unused `_render_text_output` removed | Static method removed from `quality_tools.py`. | **PASS** |
| **D5.2** | Gate verification | Changed files pass linting and type checking gates. | **PASS** |

---

## Design and Approved Strategy Alignment

- **Verbose Constraints**: Verbose mode is strictly limited to path-based runs targeting specific python test files. It is forbidden for directories or full suite runs, preventing response size explosion.
- **Wrench/Plaster Styling**: The `RecoveryNote` formats with a leading newline and the `🩹` emoji to stand out clearly from the diagnostic exit code error message.

---

## Live Demonstration Proposal

To demonstrate the new `RecoveryNote` and verbose execution:

1. **Preconditions**:
   - Branch is clean.
   
2. **Steps**:
   - Temporarily introduce an intentional test runner bug (e.g. modify `mcp_server/managers/pytest_runner.py` to return `0, 999, 0, 0` from `_parse_counts`).
   - Run `run_tests(scope='full')`.
   - **Observation**: Observe the formatted `RecoveryNote` in the error response:
     ```text
     pytest exited with code 1
     ...
     🩹 Recovery: Some tests failed. To see detailed tracebacks and stdout/stderr, rerun with verbose=True. Suggested command: run_tests(path='tests/mcp_server/unit/managers/test_pytest_runner.py', verbose=True)
     ```
   - Copy the suggested command and run it:
     ```python
     run_tests(path='tests/mcp_server/unit/managers/test_pytest_runner.py', verbose=True)
     ```
   - **Observation**: The command runs without raising a recovery note, showing detailed failures and tracebacks (up to 3) for `test_pytest_runner.py`.

---

## Residual Risks & Caveats

- **None**. All systems, signatures, and schemas behave as specified in design and planning.

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-11 | Agent | Initial draft |