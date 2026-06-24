<!-- docs/reference/mcp/tools/quality.md -->
<!-- template=reference version=064954ea created=2026-02-08T12:00:00+01:00 updated=2026-03-01 -->
# Quality & Validation Tools

**Status:** DEFINITIVE  
**Version:** 4.0  
**Last Updated:** 2026-06-15

**Source:** [mcp_server/tools/quality_tools.py](../../../../mcp_server/tools/quality_tools.py), [mcp_server/managers/qa_manager.py](../../../../mcp_server/managers/qa_manager.py), [mcp_server/tools/test_tools.py](../../../../mcp_server/tools/test_tools.py), [mcp_server/tools/template_validation_tool.py](../../../../mcp_server/tools/template_validation_tool.py)

---

## Purpose

Contract-first reference for quality and validation tool usage.

This page is optimized for agents: exact input contracts, copy/paste call patterns, and failure-safe execution order.

---

## Tool Set

| Tool | Purpose | Contract Anchor |
| `run_quality_gates` | Config-driven quality gates over explicit scope | `RunQualityGatesInput` in `quality_tools.py` |
| `run_tests` | Pytest execution and failure reporting | `RunTestsInput` in `test_tools.py` |
| `validate_template` | Template conformance checks | `TemplateValidationInput` in `template_validation_tool.py` |
| `auto_fix` | Execute configured fixer commands on matching files | `AutoFixInput` in `quality_tools.py` |

---

## run_quality_gates (authoritative contract)

| Field | Type | Required | Allowed values | Rule |
|------|------|----------|----------------|------|
| `scope` | `string` | No | `auto`, `branch`, `project`, `files` | Default is `auto` |
| `files` | `list[string] \| null` | Conditional | Any workspace-relative paths | Required and non-empty **only** when `scope="files"`; must be omitted otherwise |
| `verbose` | `bool` | No | `true`, `false` | Default is `false`. When `true`, captures stdout/stderr of failing gates in cached DTO. |
### Validation rules

- `scope="files"` and `files` is missing or `[]` → validation error.
- `scope!="files"` and `files` is provided → validation error.
- If a quality gate fails and `verbose=false` is set, a `recovery` note is produced suggesting to rerun with `verbose=true`.
### Scope semantics

| Scope | Target resolution |
|------|--------------------|
| `auto` | `git diff baseline_sha..HEAD` union persisted `failed_files`; if no baseline → project scope fallback |
| `branch` | `git diff parent_branch..HEAD` (`parent_branch` from `.phase-gate/state.json`, fallback `main`) |
| `project` | `.phase-gate/quality.yaml` `project_scope.include_globs` |
| `files` | Explicit user list; directories expanded to `.py` files |

### Output contract

`run_quality_gates` returns a single `TextContent` block containing a human-readable summary of the gate checks and the resource cache link pointing to the cached `RunQualityGatesOutput` DTO.

The DTO is stored in the MCP Resource cache at `pgmcp://cache/runs/{run_id}` and conforms to the following schema:
- `success`: `bool`
- `error_message`: `string`
- `overall_pass`: `bool`
- `scope`: `string`
- `file_count`: `int`
- `gates`: list of gate result objects, each containing:
  - `name`: `string`
  - `passed`: `bool`
  - `status`: `string`
  - `score`: `string | null`
  - `details`: `string` (contains full process stdout/stderr when `verbose=true`; empty `""` when `verbose=false`)
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
| `collect_only` | `bool` | No | `false` | Only collect tests, do not run them (pytest `--collect-only`) |
| `verbose` | `bool` | No | `false` | Enable verbose mode to capture tracebacks and stdout/stderr. Only allowed in path-based execution targeting specific files |
### Validation rules

- `path` and `scope` are mutually exclusive. Providing both → validation error.
- Providing neither `path` nor `scope` → validation error.
- `verbose=true` is only allowed when executing with `path` targeting specific test files. Rerunning folders or the entire suite with `verbose=true` is forbidden.
- `coverage=true` requires `pytest-cov` installed; otherwise pytest exits with an error (exit code 3).

### Output contract

`run_tests` returns a single `TextContent` block containing a human-readable summary of test execution and the resource cache link pointing to the cached `RunTestsOutput` DTO.

The DTO is stored in the MCP Resource cache at `pgmcp://cache/runs/{run_id}` and contains:
- `exit_code`: `int` (raw pytest exit code)
- `summary`: counts `{passed, failed, skipped, errors}`
- `summary_line`: human-readable one-liner from pytest output
- `failures`: list of failure objects (empty `[]` when no failures). Each failure object contains `test_id`, `location`, `short_reason`, and `traceback` (which includes captured stdout/stderr). The `traceback` field is only populated when `verbose=true` is set and is capped to the first 3 failing tests; otherwise it is empty (`""`).
- `coverage_pct`: `float | null` (when `coverage=true` and coverage data available; `null` otherwise)
- `lf_cache_was_empty`: `bool` (when `last_failed_only=true` but no lf-cache existed)
- `stderr`: full pytest stderr (last 50 lines)
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

- `stderr`: full pytest stderr (last 50 lines)

---

## auto_fix (authoritative contract)

### Input

| Field | Type | Required | Allowed values | Rule |
|------|------|----------|----------------|------|
| `scope` | `string` | No | `auto`, `branch`, `project`, `files` | Default is `auto` |
| `files` | `list[string] \| null` | Conditional | Any workspace-relative paths | Required and non-empty **only** when `scope="files"`; must be omitted otherwise |

### Validation rules

- `scope="files"` and `files` is missing or `[]` → validation error.
- `scope!="files"` and `files` is provided → validation error.

### Output contract

`auto_fix` returns a single `TextContent` block containing a human-readable summary of the auto-fix operations and the resource cache link pointing to the cached `AutoFixOutput` DTO.

The DTO is stored in the MCP Resource cache at `pgmcp://cache/runs/{run_id}` and conforms to the following schema:
- `success`: `bool`
- `error_message`: `string | None`
- `post_tool_instruction`: `string | None`
- `modified_files`: `list[string]`
- `modified_files_count`: `int`
- `formatted_modified_files`: `string`
- `gates_executed`: `list[string]`
- `gates_executed_count`: `int`

### Example Usage

```json
{"scope": "auto"}
```

---
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
- Do **not** expect `structuredContent` or multiple content blocks; look for the resource cache link `pgmcp://cache/runs/{run_id}`.
- Do **not** use `path` and `scope` together in `run_tests`; they are mutually exclusive.
- Do **not** use `verbose=true` with `scope="full"` or when targeting directories in `run_tests`; it is only allowed when targeting specific test files.
- Do **not** assume `is_error=False` means all tests passed; exits 0 and 5 both produce `is_error=False`.
- Do **not** parse the text output for structured data; read the cached DTO from the resource cache at `pgmcp://cache/runs/{run_id}` instead.
- Do **not** omit checking `lf_cache_was_empty` when using `last_failed_only`; if `true`, a full run was performed.

---

## Quick checks for documentation consumers

Use this checklist when writing prompts/instructions for agents:

- [ ] `run_quality_gates` examples include explicit `scope`
- [ ] `files` appears only with `scope="files"`
- [ ] No references to Gate 5/6 test/coverage under quality gates
- [ ] Output contract specifies single text block with resource cache link
- [ ] Lifecycle notes mention auto-only state mutation

---

## Related

- [docs/reference/mcp/tools/README.md](README.md)
- [docs/reference/mcp/MCP_TOOLS.md](../MCP_TOOLS.md)
- [docs/development/issue251/live-validation-plan-v2.md](../../development/issue251/live-validation-plan-v2.md)
- [docs/development/issue251/live-validation-blocked-scenarios-20260301.md](../../development/issue251/live-validation-blocked-scenarios-20260301.md)
