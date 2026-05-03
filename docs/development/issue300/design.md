<!-- docs\development\issue300\design.md -->
<!-- template=design version=5827e841 created=2026-05-03T16:08Z updated= -->
# run_tests: Expose Actionable Failure Details in Tool Response

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-03

---

## Purpose

Define the concrete implementation shape for surfacing actionable failure details in run_tests responses, answering the three deferred open questions from research.md (OQ2, OQ3, OQ4) and specifying the blast radius of required test changes.

## Scope

**In Scope:**
mcp_server/managers/pytest_runner.py, mcp_server/tools/test_tools.py, tests/mcp_server/unit/tools/test_test_tools.py, tests/mcp_server/unit/managers/test_pytest_runner.py

**Out of Scope:**
Coverage support (issue #253 Gap 3), other MCP tools, pytest plugin internals, MCP protocol layer, OSError/timeout/unknown-exit-code paths

## Prerequisites

Read these first:
1. research.md v1.3 for issue #300 (all 8 findings documented, OQ1 resolved)
2. issue #253 design.md (PytestResult / FailureDetail contract established)
---

## 1. Context & Requirements

### 1.1. Problem Statement

The run_tests tool does not surface enough information for the caller to diagnose failures without falling back to direct terminal invocation. Exit codes 2/3/4 collapse all structured diagnostics into a single-line error string. Stderr is always discarded. Non-standard failure patterns (collection errors, INTERNALERROR) are absent from failures[]. The failure traceback extraction silently returns empty string when xdist worker prefixes alter FAILURES section headers.

### 1.2. Requirements

**Functional:**
- [ ] RF-1: Exit codes 2, 3, and 4 must return is_error=True ToolResult with structured content[0] (human-readable) and content[1] (JSON payload) instead of raising ExecutionError
- [ ] RF-2: content[0] for exit code 1 must include at least one human-readable failure line per FailureDetail (test_id + short_reason), not only the summary line
- [ ] RF-3: Stderr must be captured and included in the JSON payload for exit codes 2/3/4 (trimmed to last N lines, max 50)
- [ ] RF-4: _extract_traceback() must match FAILURES section headers with optional leading xdist worker prefix [gwN]
- [ ] RF-5: The is_error distinction between exit code 1 (tests ran, some failed) and exit codes 2/3/4 (pytest could not run normally) must be preserved

**Non-Functional:**
- [ ] RNF-1: No new communication paths beyond ToolResult, NoteContext, exceptions may be introduced
- [ ] RNF-2: content[0] must remain a human-readable text block — not raw JSON, not raw stderr
- [ ] RNF-3: The two-element content structure (text + json) established in issue #253 must be preserved for exit code 1
- [ ] RNF-4: Stderr trimming must not silently discard the most diagnostic lines — trim from the top, preserve the tail
- [ ] RNF-5: Changes must not affect the OSError, TimeoutExpired, and unknown-exit-code paths (those raise ExecutionError correctly)

### 1.3. Constraints

- `is_error=True` results for exit codes 2/3/4 must remain distinguishable from `is_error=False` failure results (exit code 1)
- No new communication paths beyond ToolResult, NoteContext, exceptions
- OSError, TimeoutExpired, and unknown-exit-code paths must continue to raise `ExecutionError`
- Backward compatibility for exit code 1 callers: `content[0]` gains lines but stays plain text; `content[1]` schema gains `stderr` field (additive, callers that ignore unknown keys are unaffected)
---

## 2. Design Options

### OQ2 — How to surface failure details in `content[0]` for exit code 1

**Options considered:**

| Option | Description | Verdict |
|--------|-------------|---------|
| A | Keep `content[0]` = summary_line only; leave details in `content[1]` JSON | Rejected — callers see only '1 failed in 2.1s'; details require JSON parsing |
| B | Replace `content[0]` with full traceback dump | Rejected — verbose, not machine-friendly, inconsistent with structured approach |
| **C** | Append one line per `FailureDetail` (`FAILED test_id — short_reason`) below summary_line | **Chosen** — preserves summary as first line, adds scannable per-failure context without raw dump |

**Decision (OQ2):** `content[0]` for exit code 1 becomes a multi-line text block:
```
{summary_line}
FAILED {test_id} — {short_reason}
FAILED {test_id} — {short_reason}
...
```
If `failures` is empty (e.g., only errors), `content[0]` remains the summary line only.

---

### OQ3 — Stderr content for exit codes 2/3/4

**Options considered:**

| Option | Description | Verdict |
|--------|-------------|---------|
| A | Include full stderr in `content[0]` text block | Rejected — raw stderr can be very long and contains ANSI codes; violates RNF-2 |
| B | Omit stderr entirely; only include stdout-parsed data | Rejected — for exit 2/3, the most diagnostic content (INTERNALERROR traceback) is on stderr |
| **C** | Include stderr tail (last 50 lines) in `content[1]` JSON as `stderr` field; include one-line hint in `content[0]` | **Chosen** — keeps `content[0]` human-readable, makes stderr accessible in structured payload |

**Decision (OQ3):** For exit codes 2/3/4:
- `content[0]` (text) = `"{summary_line}\nstderr: {first_line_of_stderr_if_nonempty}"`  
  Where `first_line_of_stderr_if_nonempty` is the first non-empty stderr line, truncated to 120 chars. Omitted if stderr is empty.
- `content[1]` (JSON payload) gains a `stderr` field: last 50 lines of stderr joined with `\n`. Empty string if stderr is empty.
- Trim strategy: tail-trim (preserve the most recent lines — these are the most diagnostic for pytest errors).
- The `_PytestExecution.stderr` field already exists; `PytestRunner.run()` must pass it through to `_parse_output()`.

---

### OQ4 — Fix `_extract_traceback()` for xdist worker-prefix pattern

**Options considered:**

| Option | Description | Verdict |
|--------|-------------|---------|
| A | Strip xdist prefix from stdout before regex search | Rejected — destructive preprocessing; may corrupt test output that legitimately contains `[gwN]` |
| B | Replace regex approach with line-range scan (find header line index, slice until next `___` or `===`) | Viable but over-engineered for a one-character pattern fix |
| **C** | Add optional `(?:\[gw\d+\]\s+)?` group to existing regex pattern | **Chosen** — minimal, targeted, fully backward-compatible with non-xdist runs |

**Decision (OQ4):** Replace the `_extract_traceback` pattern with:
```python
pattern = re.compile(
    r"(?:\[gw\d+\]\s+)?_{3,}\s+" + re.escape(test_name) + r"\s+_{3,}\n(.*?)(?=\n_{3,}|\n={3,}|\Z)",
    re.DOTALL,
)
```
The `(?:\[gw\d+\]\s+)?` group is non-capturing and optional — matches `[gw0]`, `[gw12]`, etc., with trailing whitespace, or matches nothing when xdist is not active.

---

## 3. Chosen Design

**Decision:** Extend PytestRunner._parse_output to accept stderr and carry it in PytestResult; route exit codes 2/3/4 through _to_tool_result with is_error=True instead of raising ExecutionError; expand content[0] for exit code 1 to include per-failure lines; fix _extract_traceback regex with optional xdist prefix group.

**Rationale:** All four changes are minimal and self-contained within the existing architecture. They use only the two established primary communication channels (ToolResult content[0] text + content[1] JSON) without introducing new paths. The is_error flag already encodes the semantic distinction between failure types. Carrying stderr in PytestResult is a pure additive field change with no blast radius beyond the two classes that use it. The xdist regex fix is a one-line change to the pattern string. Routing exit 2/3/4 through _to_tool_result eliminates the ExecutionError throw that abandons all structured data — this is the minimum change that closes the diagnostic void described in F2 and F3.

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Pass `stderr` through `PytestRunner.run()` → `_parse_output()` → `PytestResult` | `_PytestExecution.stderr` already exists but is silently dropped at the `run()` call boundary. Adding a `stderr: str` field to `PytestResult` is the minimum change to make stderr available in `_to_tool_result()`. No interface changes; `IPytestRunner` only exposes `run()`. |
| Route exit codes 2/3/4 through `_to_tool_result()` with `is_error=True` instead of `raise ExecutionError` | Eliminates the diagnostic void (F2). The `ToolResult(is_error=True, content=[...])` shape already exists and is the canonical way to return a structured error result. Removes the three `pytest.raises(ExecutionError)` tests that test an implementation detail, not the behavioral contract. |
| `content[0]` for exit code 1: summary_line + per-FailureDetail lines | Brings the human-readable text block into parity with the JSON payload. First line stays summary_line for all callers that parse position 0; additional lines are purely additive. |
| `content[0]` for exit codes 2/3/4: summary_line + first non-empty stderr line (120 char cap) | Signals the nature of the failure in the primary text block without dumping raw stderr. The full stderr tail lives in `content[1].stderr` for callers that need it. |
| Stderr tail-trim: last 50 lines, joined as single string in `content[1].stderr` | Pytest error messages (INTERNALERROR, usage errors) concentrate at the end of stderr output. Top-trimming preserves the most diagnostic content. 50 lines is sufficient for all observed INTERNALERROR patterns while keeping payload size bounded. |
| xdist regex fix: add `(?:\[gw\d+\]\s+)?` prefix to `_extract_traceback` pattern | One-line change; non-breaking for non-xdist runs (group is optional). Fixes the silent empty-traceback regression on every project run (xdist is default in `pyproject.toml`). |

## Related Documentation
- **[docs/development/issue300/research.md][related-1]**
- **[docs/development/issue253/design.md][related-2]**
- **[mcp_server/managers/pytest_runner.py][related-3]**
- **[mcp_server/tools/test_tools.py][related-4]**

<!-- Link definitions -->

[related-1]: docs/development/issue300/research.md
[related-2]: docs/development/issue253/design.md
[related-3]: mcp_server/managers/pytest_runner.py
[related-4]: mcp_server/tools/test_tools.py

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-03 | Agent | Initial draft |