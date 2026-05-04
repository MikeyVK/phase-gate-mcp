<!-- docs\development\issue300\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-03T14:04Z updated= -->
# Issue #300: run_tests — Expose Actionable Failure Details in Tool Response

**Status:** DRAFT  
**Version:** 1.3  
**Last Updated:** 2026-05-03

---

## Purpose

Identify all failure modes where `run_tests` produces insufficient output, trace each gap to its root cause in the current implementation, and define expected outputs per scenario as input for the design and planning phases.

## Scope

**In Scope:**
`mcp_server/managers/pytest_runner.py`, `mcp_server/tools/test_tools.py`, `mcp_server/core/operation_notes.py`, `mcp_server/tools/tool_result.py`, `mcp_server/tools/base.py`, `mcp_server/server.py` — limited to the run_tests tool response pipeline

**Out of Scope:**
Design decisions, TDD cycle breakdown, implementation code or pseudocode, other MCP tools, pytest plugin internals, coverage support (issue #253 Gap 3 — separate concern), changes to the MCP protocol layer

---

## Problem Statement

The `run_tests` tool does not surface enough information for the caller to diagnose failures without falling back to a direct terminal pytest invocation. Exit codes 2, 3, and 4 silently collapse all structured diagnostics into a single-line text error. Stderr is always discarded. Non-standard failure patterns (collection errors, INTERNALERROR) are not captured in the `failures[]` payload. The result is that `run_tests` cannot replace the terminal for anything beyond a simple passing run.

## Research Goals

- Map which exit codes produce useful output vs. diagnostic voids
- Identify where stderr is lost and why
- Identify which pytest failure patterns are not captured in failures[]
- Understand the three existing communication paths and confirm no new paths are needed
- Document the exact sequence from ExecutionError → tool_error_handler → ToolResult.error() that loses structured data
- Define expected results per scenario as a baseline for design and planning

---

## Background

Issue #253 (resolved) established the current architecture: a thin `RunTestsTool` adapter delegating to a `PytestRunner` domain manager, with typed `PytestResult` / `FailureDetail` contracts. The raw stdout dump was deliberately removed in commit `cc98d61` ('remove raw_output from run_tests response, structured failures sufficient'). The intent was correct: structured typed data is better than a raw dump. The implementation, however, left the structured data undersurfaced on the happy path and entirely absent on error paths.

The current MCP server has exactly three communication paths from tool internals to the caller: (1) **ToolResult** — the primary response object returned by `execute()`; (2) **NoteContext** — typed secondary notes (RecoveryNote, SuggestionNote, InfoNote, etc.) attached during execution and rendered as a text block appended after the primary content by `note_context.render_to_response(raw_result)` in `server.py`; (3) **exceptions** — caught by the auto-wrapped `tool_error_handler` in `BaseTool.__init_subclass__`, which converts any `ExecutionError` to `ToolResult.error(message=str)`. No new communication paths should be created.

---

## Findings

### Finding 1 — Exit code 1 (test failures) already produces structured output but surfaces only summary_line as text

When pytest exits with code 1 (tests ran and some failed), `_EXIT_CODE_POLICY` maps it to `outcome='return'`, so `run()` returns a `PytestResult` and `_to_tool_result()` is called. The result has `content[0]` = text(summary_line) and `content[1]` = json(payload with `failures[]`). This is correct in structure. However, `content[0]` shows only the one-line summary ('1 failed in 2.1s'), while the `failures[]` with full tracebacks lives in `content[1]` as a JSON block that is serialised to text by `_convert_tool_result_to_content()` before reaching the caller. The failure details are present but buried in JSON text — they are not surfaced in the human-readable primary content block.

### Finding 2 — Exit codes 2, 3, and 4 collapse all diagnostics via the exception path

Exit code 2 (interrupted / INTERNALERROR), code 3 (internal pytest error), and code 4 (usage error / bad invocation) all map to `outcome='raise'` in `_EXIT_CODE_POLICY`. In `test_tools.py` `execute()`, this triggers `raise ExecutionError(f'pytest exited with returncode {result.exit_code}')`. At that point the typed `PytestResult` — including any `failures[]` that were parsed — is abandoned. The `tool_error_handler` decorator (auto-applied by `BaseTool.__init_subclass__`) catches `ExecutionError` and returns `ToolResult.error(message=exc.message)`, which is a text-only, `is_error=True` result. All structured data is irrecoverably lost. The caller receives a single line: 'pytest exited with returncode N'.

Live verification: `run_tests(markers='(')` (malformed marker → exit 3) returns only 'pytest exited with returncode 3' plus a RecoveryNote. Terminal pytest for the same input returns the full INTERNALERROR traceback including the crash test-id and xdist stack.

### Finding 3 — Stderr is captured in _PytestExecution but never passed to _parse_output — always lost

`PytestRunner._execute()` returns a `_PytestExecution` namedtuple containing both `stdout` and `stderr`. In `run()`, only `stdout` is passed to `_parse_output(stdout)`. Stderr is discarded unconditionally. For exit codes 2 and 3 (INTERNALERROR, internal error), pytest writes the most diagnostic content — the full INTERNALERROR traceback, crash test-id, and plugin stack — to stderr, not stdout. Because stderr is dropped, this information cannot appear in any output, regardless of how the exit-code path is handled.

### Finding 4 — _FAILED_LINE_RE only matches standard 'FAILED test - reason' lines

`_FAILED_LINE_RE = re.compile(r'^FAILED (.+?) - (.+)$', re.MULTILINE)` matches only the standard FAILED summary lines that appear at the end of a test run with exit code 1. Collection errors (`ERROR collecting tests/...`) and INTERNALERROR sections have a different format and are not matched. Even when stdout is available and contains these patterns, `_parse_output()` produces an empty `failures[]` for them. Any caller logic that relies on `failures[]` being populated for non-code-1 failures will receive an empty list.

### Finding 5 — _extract_traceback() may return empty string when xdist worker prefixes alter the FAILURES section header

`_extract_traceback(stdout, test_id)` extracts `test_name` via `test_id.rpartition('::')` then searches for the FAILURES section header pattern `_{3,}\s+{test_name}\s+_{3,}` using `re.escape()`. The `re.escape()` call correctly handles brackets in parametrized test names (`test_foo[a-b]` → `test_foo\[a\-b\]`), so brackets are **not** the issue.

The actual failure mode is the xdist worker prefix. When pytest-xdist is active, the FAILURES section header is emitted as `[gw0] ______ test_name ______` rather than `______ test_name ______`. The regex anchors on `_{3,}\s+` and does not account for the leading `[gw0] ` token, so the match returns `None` and `FailureDetail.traceback` is set to `''` even when a full traceback exists in stdout. This manifests on every run in this project because xdist is the default configuration (see `pyproject.toml` `addopts`).

### Finding 6 — NoteContext is appropriate for secondary signals; it is not a substitute for primary diagnostic transport

The note bus (`NoteContext`) emits RecoveryNote and SuggestionNote as secondary, machine-readable operator hints appended after the primary result. The established usage pattern (enforcement_runner.py, discovery_tools.py, git_manager.py) is: notes supplement a primary result that already contains the core diagnostic content. For exit codes 2/3/4, the problem is that the primary ToolResult carries no structured data at all — only a one-line error string. Emitting a note that references information the primary result has already dropped does not resolve the diagnostic void. Notes are the right mechanism for secondary signals (LF-cache empty, no tests collected, plugin missing). They are not the right mechanism for primary failure diagnostics.

### Finding 7 — Three existing communication paths are sufficient; no new paths should be created

The current architecture has exactly three paths from tool internals to the caller: ToolResult (primary), NoteContext (secondary), and exceptions (infrastructure). The pattern is well-established and documented. Adding a fourth path would add protocol complexity without necessity. The diagnostic void in Finding 2 can be resolved by routing structured data through the existing ToolResult path with `is_error=True` instead of relying on the exception path.

### Finding 8 — The decision to remove raw_output (cc98d61) was architecturally correct but incompletely implemented

Commit `cc98d61` removed the raw pytest stdout dump from the response. The stated rationale — 'structured failures sufficient' — is valid in principle: typed data is more useful than raw text. The gap is that the implementation did not complete the contract: (a) for exit code 1, `failures[]` exists but is not surfaced in the primary text block where the caller can see it without parsing JSON; (b) for exit codes 2/3/4, structured data is available after `_parse_output()` but is abandoned before `_to_tool_result()` is reached; (c) stderr diagnostics were never included in the structured output. The removal of raw_output created a regression for error paths that the structured output did not yet cover.

---

## Expected Results

This section documents what the tool *should* produce per scenario. It is written as a verifiable contract for design and planning, not as implementation instructions.

| Exit code | Scenario | Expected primary content | Expected notes |
|-----------|----------|--------------------------|----------------|
| 0 | All tests pass | Summary line ('N passed in Xs') | None |
| 1 | Some tests failed | Summary line + at least one human-readable failure line per FailureDetail | None |
| 2 | Interrupted / INTERNALERROR | Structured error result with summary line and stderr snippet | RecoveryNote with guidance |
| 3 | Internal pytest error | Structured error result with summary line and stderr snippet | RecoveryNote with guidance |
| 4 | Usage error / bad path | Structured error result identifying the bad invocation | RecoveryNote with guidance |
| 5 | No tests collected | Summary line ('no tests ran') | SuggestionNote to check markers/path |

**Constraints that must hold after the change:**
- `is_error=True` results for exit codes 2/3/4 must still be distinguishable from `is_error=False` failure results (exit code 1)
- `content[0]` must remain a human-readable text block (not raw JSON)
- The two-element content structure (text + JSON) established in issue #253 must be preserved for exit code 1
- No new communication paths (beyond ToolResult, NoteContext, exceptions) may be introduced
- NoteContext is still the correct channel for secondary signals (LF-cache empty, plugin missing, no-tests)

**Implementation approach — clean break (no backward compat for exit 2/3/4):**

The three tests in `test_test_tools.py` that currently assert `pytest.raises(ExecutionError)` for exit codes 2, 3, and 4 test an implementation detail (raising an exception) rather than the desired behavioral contract (structured error output). These tests will be **rewritten** in the implementation phase. Preserving them would lock in the diagnostic void that this issue is designed to fix. This is a clean break, not a migration.

**Test blast radius:**

| File | Tests affected | Change type |
|------|---------------|-------------|
| `tests/mcp_server/unit/tools/test_test_tools.py` | `test_c4_run_tests_interrupted_raises_execution_error` (r.124), `test_c4_run_tests_internal_error_raises_execution_error` (r.145), `test_c4_run_tests_usage_error_raises_execution_error` (r.168) | Rewritten: `pytest.raises(ExecutionError)` → assert `is_error=True` result with structured content |
| `tests/mcp_server/unit/tools/test_test_tools.py` | `test_c4_run_tests_unknown_exit_code_raises_execution_error` (r.213) | Unchanged — unknown exit codes have no pytest specification; structured handling for undefined behavior violates YAGNI (§9). The exception path is the correct signal for genuinely unexpected conditions. |
| `tests/mcp_server/unit/tools/test_test_tools.py` | `test_c4_run_tests_timeout_raises_execution_error` (r.307), `test_c4_run_tests_oserror_raises_execution_error` (r.320) | Unchanged — OSError and timeout are infrastructure failures, not pytest exit conditions; no PytestResult is available to surface. |
| `tests/mcp_server/unit/tools/test_test_tools.py` | New tests | Assert structured content shape for exit codes 2, 3, 4; assert stderr snippet present in payload |
| `tests/mcp_server/unit/managers/test_pytest_runner.py` | `test_errors_during_collection` (r.195) | Extended: add assertion that stderr is carried in result when returncode is 2 |
| `tests/mcp_server/unit/managers/test_pytest_runner.py` | New tests | INTERNALERROR stdout+stderr scenario; xdist-prefix FAILURES header for `_extract_traceback` |

## Open Questions

**OQ 1 — RESOLVED: exit codes 2/3/4 return `is_error=True` ToolResult with structured content.**

The `is_error` field already encodes the semantic distinction between "pytest ran and found failures" (exit code 1, `is_error=False`) and "pytest could not run normally" (exit codes 2/3/4, `is_error=True`). Routing exit codes 2/3/4 through a structured `ToolResult` with `is_error=True` and a JSON payload preserves this contract and eliminates the diagnostic void from Finding 2. The three tests that currently assert `pytest.raises(ExecutionError)` for these exit codes will be rewritten (see blast radius above).

**OQ 2 — DEFERRED to design:** How to surface failure details in `content[0]` for exit code 1 — whether and how to include `test_id` / `short_reason` lines alongside the summary line.

**OQ 3 — DEFERRED to design:** What stderr content to include for exit codes 2/3/4 — how much, in which field, and whether trimming is needed.

**OQ 4 — DEFERRED to design:** Whether to fix `_extract_traceback()` for the xdist worker-prefix pattern or replace it with an alternative approach.


## Related Documentation
- **[mcp_server/tools/test_tools.py][related-1]**
- **[mcp_server/managers/pytest_runner.py][related-2]**
- **[mcp_server/core/operation_notes.py][related-3]**
- **[mcp_server/tools/base.py][related-4]**
- **[mcp_server/server.py][related-5]**
- **[tests/mcp_server/unit/tools/test_test_tools.py][related-6]**
- **[tests/mcp_server/unit/managers/test_pytest_runner.py][related-7]**
- **[docs/development/issue253/design.md][related-8]**
- **[docs/development/issue253/research.md][related-9]**

<!-- Link definitions -->

[related-1]: mcp_server/tools/test_tools.py
[related-2]: mcp_server/managers/pytest_runner.py
[related-3]: mcp_server/core/operation_notes.py
[related-4]: mcp_server/tools/base.py
[related-5]: mcp_server/server.py
[related-6]: tests/mcp_server/unit/tools/test_test_tools.py
[related-7]: tests/mcp_server/unit/managers/test_pytest_runner.py
[related-8]: docs/development/issue253/design.md
[related-9]: docs/development/issue253/research.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-03 | Agent | Initial draft |
| 1.1 | 2026-05-03 | Agent | QA v1.0 feedback: sharpen F5 (xdist prefix, not brackets); C-1 resolved (clean break + blast radius table); C-2 resolved (blast radius table added); OQ1 + OQ3 answered; OQ2 + OQ4 deferred to design |
| 1.2 | 2026-05-03 | Agent | QA v1.1 feedback: separate r.213 rationale (YAGNI for unknown exit codes); OQ2 resolved (expand content[0] with failure lines); OQ4 resolved (regex fix with optional xdist prefix group) |
| 1.3 | 2026-05-03 | Agent | Revert OQ2/OQ3/OQ4 to design-deferred — format/implementation specifics cross the research boundary |