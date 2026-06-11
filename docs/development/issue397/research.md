<!-- c:\temp\pgmcp\docs\development\issue397\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-11T13:57Z updated= -->
# Add verbose traceback and stdout capture to run_tests tool

**Status:** DRAFT  
**Version:** 1.0.0  
**Last Updated:** 2026-06-11

---

## Purpose

To research the constraints, blast radius, and strategy options for adding verbose traceback and captured stdout/stderr support to the run_tests tool.

## Scope

**In Scope:**
- Injected IPytestRunner and PytestRunner implementation
- RunTestsTool adapter and RunTestsInput schema
- Test suites for test_tools.py and pytest_runner.py

**Out of Scope:**
- Modifying general settings.py or settings configuration schema
- Adding external dependencies or CLI tools
- Changing quality gate rules outside pytest testing

## Prerequisites

Read these first:
1. docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
2. docs/coding_standards/DOCUMENTATION_STANDARD.md
---

## Problem Statement

The run_tests tool executes tests but lacks support for detailed tracebacks and captured stdout/stderr, which hampers developer experience and forces agents to run tests manually in the terminal.

## Research Goals

- Determine command-line arguments and configuration settings for verbose test execution
- Establish a robust mechanism to prevent context and response payload size explosion
- Verify the blast radius and test suites affected by the verbose parameter integration

---

## Background

The RunTestsTool relies on an injected IPytestRunner implementation (concrete PytestRunner) to invoke pytest and capture test results. Currently, it runs pytest with --tb=short and returns a summary line along with parsed failures. However, it does not capture complete tracebacks or stdout/stderr. To improve debugging, we need to support a verbose mode, while strictly guarding against context length explosion in the MCP tool response.

---

## Findings

1. PytestRunner execution uses subprocess.run with capture_output=True, yielding stdout and stderr.
2. When --tb=short is active, pytest's stdout contains minimal traceback details. If --tb=long is used, pytest output includes verbose traceback details and captured stdout/stderr for failed tests.
3. The current _extract_traceback method in PytestRunner parses failure blocks from stdout based on test names.
4. Exposing max failures detailed as a Python constant avoids config pollution and satisfies the YAGNI principle. A constant value of 3 is optimal for preventing token/context window explosion.
5. If verbose=False, the traceback fields in the JSON payload must remain empty (no placeholder strings). A RecoveryNote will guide the user/agent to run with verbose=True on the specific failing files.
6. Restricting verbose=True to only be allowed when running specific test files (no directories or full suite) provides maximum protection against token payload explosion.

## Open Questions

- *None* (All questions resolved during research alignment).

## Related Documentation
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-1]**
- **[docs/coding_standards/DOCUMENTATION_STANDARD.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-2]: docs/coding_standards/DOCUMENTATION_STANDARD.md

---

## Approved Strategy

- **Boundary / consumer scope:** RunTestsTool / IPytestRunner boundaries.
- **Selected strategy:** Clean break / Extension. We are extending the API by adding `verbose: bool = False` to `RunTestsInput`. Since it is an optional parameter with a default value, it is backward-compatible.
- **Rationale:** Extension is clean and preserves existing contracts.
- **Constraints for later phases:**
  - The `RunTestsInput` model must validate that `verbose=True` is only permitted when running specific test files (i.e. `scope` is not "full" and `path` does not contain directories).
  - The description of the `verbose` property in the input schema must explicitly document these constraints to guide agents.
  - Python constant `MAX_FAILURES_DETAILED = 3` in the code will limit traceback extraction when `verbose=True` is used.
  - When `verbose=False`, traceback strings in JSON must be empty. A conditional `RecoveryNote` suggesting the failing files will be generated on test failure.

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-11 | Agent | Initial draft |
