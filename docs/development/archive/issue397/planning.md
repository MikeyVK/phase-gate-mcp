<!-- C:\temp\pgmcp\docs\development\issue397\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-11T15:30Z updated= -->
# Add verbose traceback and stdout capture to run_tests tool

**Status:** DRAFT  
**Version:** 1.0.0  
**Last Updated:** 2026-06-11

---

## Purpose

To specify the test execution cycles and deliverables for Issue #397.

## Scope

**In Scope:**
RunTestsInput, RunTestsTool, PytestRunner, RunQualityGatesTool dead code cleanup, and related unit tests.

**Out of Scope:**
Changing settings structure and modifying third-party test execution engines.

## Prerequisites

Read these first:
1. docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
2. docs/coding_standards/DOCUMENTATION_STANDARD.md
3. docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md
---

## Summary

This planning document outlines the sequential TDD implementation cycles to add verbose traceback and stdout capture support to the run_tests tool, and to perform dead code cleanup in quality_tools.py. Explicit typing obligations (pyright) and quality gates (ruff) apply to changed files at the end of every cycle.

---

## TDD Cycles


### Cycle 1: IPytestRunner Protocol & FakePytestRunner alignment

**Goal:** Update the IPytestRunner protocol signature, FakePytestRunner, and concrete PytestRunner to accept the verbose keyword argument, preserving backward compatibility and avoiding intermediate LSP compiler violations.

**Tests:**
- tests/mcp_server/unit/tools/test_test_tools.py
- tests/mcp_server/fixtures/fake_pytest_runner.py

**Success Criteria:**
- [D1.1] IPytestRunner.run and PytestRunner.run signatures include *, verbose: bool = False, preserving backward compatibility with existing callers.
- [D1.2] FakePytestRunner signature updated and all existing unit tests compile and pass.
- Run quality gates (run_quality_gates) on changed files. Achieve 10.00/10 linting score and pass type checking cleanly (no global ignores, per TYPE_CHECKING_PLAYBOOK.md).



### Cycle 2: RunTestsInput Schema & Path-based Validation

**Goal:** Implement Pydantic validation rules and parameter description for verbose in RunTestsInput.

**Tests:**
- tests/mcp_server/unit/tools/test_test_tools.py

**Success Criteria:**
- [D2.1] RunTestsInput schema includes verbose parameter with detailed agent description.
- [D2.2] ValueError raised if verbose=True is set when path is None or contains directories. Validator uses os.path.isdir combined with ends-with-py/contains-py-double-colon string check fallback for isolated unit testing.
- Run quality gates (run_quality_gates) on changed files. Achieve 10.00/10 linting score and pass type checking cleanly (no global ignores, per TYPE_CHECKING_PLAYBOOK.md).



### Cycle 3: PytestRunner Verbose Execution & Capping

**Goal:** Update PytestRunner execution to run with --tb=long when verbose=True, and cap failures at MAX_FAILURES_DETAILED = 3.

**Tests:**
- tests/mcp_server/unit/managers/test_pytest_runner.py

**Success Criteria:**
- [D3.1] RunTestsTool._build_cmd command execution builds --tb=long when verbose=True, and --tb=short when verbose=False. PytestRunner execution itself does not modify command-line arguments.
- [D3.2] Traceback extraction in PytestRunner._parse_failures caps detailed tracebacks at MAX_FAILURES_DETAILED = 3 (module-level constant in pytest_runner.py) when verbose=True, leaving others empty.
- [D3.3] All traceback strings are empty in PytestRunner._parse_failures when verbose=False.
- Run quality gates (run_quality_gates) on changed files. Achieve 10.00/10 linting score and pass type checking cleanly (no global ignores, per TYPE_CHECKING_PLAYBOOK.md).



### Cycle 4: RunTestsTool Execution & RecoveryNote

**Goal:** Update RunTestsTool.execute to propagate verbose flag and generate a conditional RecoveryNote on failure.

**Tests:**
- tests/mcp_server/unit/tools/test_test_tools.py

**Success Criteria:**
- [D4.1] ToolResult JSON contains empty tracebacks when verbose=False.
- [D4.2] RecoveryNote suggesting failing test files is generated when verbose=False and tests fail. Note format is exactly: 'Some tests failed. To see detailed tracebacks and stdout/stderr, rerun with verbose=True. Suggested command: run_tests(path=\'<failing_test_files>\', verbose=True)'.
- Run quality gates (run_quality_gates) on changed files. Achieve 10.00/10 linting score and pass type checking cleanly (no global ignores, per TYPE_CHECKING_PLAYBOOK.md).



### Cycle 5: RunQualityGatesTool Dead Code Cleanup

**Goal:** Remove the unused _render_text_output static method from quality_tools.py.

**Tests:**
- tests/mcp_server/unit/tools/test_quality_tools.py

**Success Criteria:**
- [D5.1] _render_text_output is completely removed from quality_tools.py.
- [D5.2] All existing unit tests and quality gates pass cleanly.
- Run quality gates (run_quality_gates) on changed files. Achieve 10.00/10 linting score and pass type checking cleanly (no global ignores, per TYPE_CHECKING_PLAYBOOK.md).


## Related Documentation
- **[[docs/development/issue397/research.md](file:///c:/temp/pgmcp/docs/development/issue397/research.md)][related-1]**
- **[[docs/development/issue397/design.md](file:///c:/temp/pgmcp/docs/development/issue397/design.md)][related-2]**

<!-- Link definitions -->

[related-1]: [docs/development/issue397/research.md](file:///c:/temp/pgmcp/docs/development/issue397/research.md)
[related-2]: [docs/development/issue397/design.md](file:///c:/temp/pgmcp/docs/development/issue397/design.md)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-11 | Agent | Initial draft |