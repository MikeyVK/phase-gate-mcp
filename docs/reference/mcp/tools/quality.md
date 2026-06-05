<!-- docs/reference/mcp/tools/quality.md -->
<!-- template=reference version=064954ea created=2026-02-08T12:00:00+01:00 updated=2026-03-01 -->
# Quality & Validation Tools

**Status:** DEFINITIVE  
**Version:** 3.0  
**Last Updated:** 2026-03-01

**Source:** [mcp_server/tools/quality_tools.py](../../../../mcp_server/tools/quality_tools.py), [mcp_server/managers/qa_manager.py](../../../../mcp_server/managers/qa_manager.py), [mcp_server/tools/test_tools.py](../../../../mcp_server/tools/test_tools.py), [mcp_server/tools/template_validation_tool.py](../../../../mcp_server/tools/template_validation_tool.py)

---

## Purpose

Contract-first reference for quality and validation tool usage.

This page is optimized for agents: exact input contracts, copy/paste call patterns, and failure-safe execution order.

---

## Tool Set

| Tool | Purpose | Contract Anchor |
|------|---------|-----------------|
| `run_quality_gates` | Config-driven quality gates over explicit scope | `RunQualityGatesInput` in `quality_tools.py` |
| `run_tests` | Pytest execution and failure reporting | `RunTestsInput` in `test_tools.py` |
| `validate_template` | Template conformance checks | `TemplateValidationInput` in `template_validation_tool.py` |

---

## run_quality_gates (authoritative contract)

### Input

| Field | Type | Required | Allowed values | Rule |
|------|------|----------|----------------|------|
| `scope` | `string` | No | `auto`, `branch`, `project`, `files` | Default is `auto` |
| `files` | `list[string] \| null` | Conditional | Any workspace-relative paths | Required and non-empty **only** when `scope="files"`; must be omitted otherwise |

### Validation rules

- `scope="files"` and `files` is missing or `[]` → validation error.
- `scope!="files"` and `files` is provided → validation error.

### Scope semantics

| Scope | Target resolution |
|------|--------------------|
| `auto` | `git diff baseline_sha..HEAD` union persisted `failed_files`; if no baseline → project scope fallback |
| `branch` | `git diff parent_branch..HEAD` (`parent_branch` from `.st3/state.json`, fallback `main`) |
| `project` | `.st3/quality.yaml` `project_scope.include_globs` |
| `files` | Explicit user list; directories expanded to `.py` files |

### Output contract

`run_quality_gates` returns `ToolResult.content` with exactly two items:

1. `content[0]`: `{"type":"text","text":"...summary line..."}`
2. `content[1]`: `{"type":"json","json": {"overall_pass": bool, "gates": [...]}}`

Compact JSON root keys are:
- `overall_pass`
- `gates`

### Baseline lifecycle behavior

Baseline mutation is allowed only for effective `scope="auto"` runs.

- Auto all-pass: advance `baseline_sha` to `HEAD`, clear `failed_files`.
- Auto fail: update `failed_files` to failing subset.
- Non-auto (`files`, `branch`, `project`): do not mutate auto lifecycle fields.

---

---

## run_tests (authoritative contract)

### Input

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `path` | `string \| null` | No | `null` | Space-separated pytest paths/files. **Mutually exclusive with `scope`** |
| `scope` | `"full" \| null` | No | `null` | Pass `"full"` to run the full test suite. Mutually exclusive with `path` |
| `markers` | `string \| null` | No | `null` | Pytest `-m` expression (e.g. `"unit and not slow"`) |
| `last_failed_only` | `bool` | No | `false` | Re-run only last-failed tests (`--lf`). Skipped if lf-cache is empty |
| `timeout` | `int` | No | `300` | Hard kill timeout in seconds |
| `coverage` | `bool` | No | `false` | Enable pytest-cov coverage reporting (`--cov`) |

### Validation rules

- `path` and `scope` are mutually exclusive. Providing both → validation error.
- Providing neither `path` nor `scope` → validation error.
- `coverage=true` requires `pytest-cov` installed; otherwise pytest exits with an error (exit code 3).

### Output contract

`run_tests` returns `ToolResult.content` with exactly two items:

1. `content[0]`: `{"type":"text","text":"..."}` — human-readable summary
2. `content[1]`: `{"type":"json","json": {...}}` — structured payload

#### content[0] text semantics by exit code

| Exit code | Meaning | content[0] text shape |
|-----------|---------|----------------------|
| 0 | All tests passed | `summary_line` only |
| 1 | Test failures | `summary_line` + `\nFAILED test_id — short_reason` per failure |
| 5 | No tests collected | `summary_line` only |
| 2 / 3 / 4 | Pytest interrupted / internal error / usage error | `summary_line` + optional `\nstderr: {first_nonempty_line[:120]}` |

For exits 2/3/4 the `ToolResult` has `is_error=True`. For exits 0/1/5 it has `is_error=False`.

Exits 99 (timeout), OSError, and unrecoverable errors raise `ExecutionError` (never returned as a result).

#### content[1] JSON payload (always present)

```json
{
  "exit_code": 1,
  "summary": {"passed": 10, "failed": 2, "skipped": 0, "errors": 0},
  "summary_line": "2 failed, 10 passed in 1.23s",
  "failures": [
    {
      "test_id": "tests/unit/test_foo.py::TestFoo::test_bar",
      "location": "tests/unit/test_foo.py",
      "short_reason": "AssertionError: assert 1 == 2",
      "traceback": "..."
    }
  ],
  "coverage_pct": 87.4,
  "lf_cache_was_empty": false,
  "stderr": ""
}
```

Payload keys:
- `exit_code`: raw pytest exit code
- `summary`: counts `{passed, failed, skipped, errors}`
- `summary_line`: human-readable one-liner from pytest output
- `failures`: list of failure objects (empty `[]` when no failures)
- `coverage_pct`: `float` when `coverage=true` and coverage data available; `null` otherwise
- `lf_cache_was_empty`: `true` when `last_failed_only=true` but no lf-cache existed (full run was performed)
- `stderr`: full pytest stderr (last 50 lines). Always present; empty string `""` when no stderr

---

## Agent Call Patterns (copy/paste)


### Minimal changed-files check during TDD refactor

```json
{"scope": "files", "files": ["mcp_server/managers/qa_manager.py", "tests/mcp_server/unit/managers/test_baseline_advance.py"]}
```

### Branch-wide quality gate check

```json
{"scope": "branch"}
```

### Baseline-aware rerun behavior

```json
{"scope": "auto"}
```

### Project-wide sweep

```json
{"scope": "project"}
```

### run_tests — targeted file/folder

```json
{"path": "tests/mcp_server/unit/managers/test_pytest_runner.py"}
```

### run_tests — full suite with coverage

```json
{"scope": "full", "coverage": true}
```

### run_tests — last-failed only

```json
{"path": "tests/", "last_failed_only": true}
```

---

## Execution order for reliable agent runs

1. Run targeted tests via `run_tests(path=...)`.
2. Run `run_quality_gates(scope="files", files=[...changed files...])`.
3. Before acceptance closure, run switch-path checks (`auto↔files`, `branch↔files`, `project→auto`).
4. Use `restart_server`, then wait 3 seconds, before live behavior validation after server/tool code changes.

---

## Common mistakes to avoid

- Do **not** call `run_quality_gates(files=[...])` without `scope="files"`.
- Do **not** use `scope="project"` with a `files` payload.
- Do **not** treat `run_quality_gates` as test runner replacement; use `run_tests` for pytest execution.
- Do **not** infer compact payload from legacy `json_data` examples; use `content[0]/content[1]` contract.
- Do **not** use `path` and `scope` together in `run_tests`; they are mutually exclusive.
- Do **not** assume `is_error=False` means all tests passed; exits 0 and 5 both produce `is_error=False`.
- Do **not** parse `content[0]` text for structured data; use `content[1]` JSON payload instead.
- Do **not** omit checking `lf_cache_was_empty` when using `last_failed_only`; if `true`, a full run was performed.

---

## Quick checks for documentation consumers

Use this checklist when writing prompts/instructions for agents:

- [ ] `run_quality_gates` examples include explicit `scope`
- [ ] `files` appears only with `scope="files"`
- [ ] No references to Gate 5/6 test/coverage under quality gates
- [ ] Output examples show `content[0]=text` and `content[1]=json`
- [ ] Lifecycle notes mention auto-only state mutation

---

## Related

- [docs/reference/mcp/tools/README.md](README.md)
- [docs/reference/mcp/MCP_TOOLS.md](../MCP_TOOLS.md)
- [docs/development/issue251/live-validation-plan-v2.md](../../development/issue251/live-validation-plan-v2.md)
- [docs/development/issue251/live-validation-blocked-scenarios-20260301.md](../../development/issue251/live-validation-blocked-scenarios-20260301.md)
