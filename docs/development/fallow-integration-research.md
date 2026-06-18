<!-- docs\development\fallow-integration-research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-18T06:33:31Z updated=2026-06-18T08:32:00Z -->
# Research: Integrating Fallow as a Quality Gate & Auto-Fix Tool

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-06-18

---

## Purpose

Provide a clear architectural analysis of Fallow integration possibilities under the constraint of zero code changes.

## Scope

**In Scope:**
- Mapping Fallow's CLI command, JSON output, and auto-fix capabilities to the existing configuration schema of `phase-gate-mcp`.
- Identifying configuration changes in `.phase-gate/config/quality.yaml`.
- Formulating a configuration template for Fallow integration.

**Out of Scope:**
- Modifying Python code in `mcp_server/` or `tests/`.

## Prerequisites

Read these first:
1. [docs/coding_standards/QUALITY_GATES.md](file:///c:/temp/pgmcp/docs/coding_standards/QUALITY_GATES.md)
2. [mcp_server/config/schemas/quality_config.py](file:///c:/temp/pgmcp/mcp_server/config/schemas/quality_config.py)

---

## Problem Statement

Investigate the integration of Fallow (https://fallow.tools/) as a quality gate and auto-fix tool within the `phase-gate-mcp` framework, uitsluitend via configuration changes and without code modifications.

## Research Goals

- Understand Fallow output formatting and capability mapping to `phase-gate-mcp`.
- Identify necessary configuration changes in `.phase-gate/config/quality.yaml`.
- Evaluate the applicability of Fallow to the current Python-based project compared to a TypeScript/JavaScript context.
- Formulate a concrete configuration template for Fallow integration.

---

## Background

Fallow is a Rust-based, zero-configuration codebase intelligence tool designed specifically for JavaScript and TypeScript projects. It identifies unused code (dead code), code duplication, complexity hotspots, and architectural boundary violations. 

While the current `phase-gate-mcp` codebase is written in Python, it serves as a platform-agnostic orchestrator. In a hybrid or multi-language repository, or when using this platform to orchestrate a TypeScript/JavaScript codebase, Fallow can be integrated directly as a Quality Gate and Auto-Fix tool.

---

## Findings

Through an analysis of the `phase-gate-mcp` QA configuration loader (`mcp_server/config/schemas/quality_config.py`) and execution runner (`mcp_server/managers/qa_manager.py`), we have verified that the platform natively supports external tools using JSON diagnostics without code changes.

### 1. Fallow Output Formatting & Mapping

Fallow emits machine-readable JSON reports when run with `--format json`. A typical Fallow check/audit output is structured as follows:

```json
{
  "verdict": "fail",
  "total_issues": 3,
  "elapsed_ms": 142,
  "workspace_diagnostics": [
    {
      "type": "unused_export",
      "path": "src/utils/helpers.ts",
      "line": 12,
      "message": "Export 'calculateTotal' is never imported.",
      "severity": "warn",
      "auto_fixable": true,
      "actions": [
        {
          "type": "remove_export",
          "command": "fallow fix --path src/utils/helpers.ts --line 12"
        }
      ]
    }
  ]
}
```

This maps perfectly to the `JsonViolationsParsing` schema of `phase-gate-mcp`:

| ViolationDTO Field | Fallow JSON Field | Mapping Path |
|---|---|---|
| `violations_path` | Target list container | `workspace_diagnostics` |
| `file` | Relative file path | `path` |
| `line` | Start line number | `line` |
| `rule` | Check/issue type | `type` |
| `message` | Explanatory message | `message` |
| `severity` | Issue severity | `severity` |
| `fixable` | Auto-fixability flag | `auto_fixable` (specified via `fixable_when`) |

### 2. Auto-Fix Integration

The `QAManager.run_auto_fix` method resolves the files for a gate and executes the configured `execution.fix_command` command with resolved files appended:
```python
cmd = self._resolve_command(gate.execution.fix_command or [], gate_files)
```
Fallow provides the `fallow fix` command to automatically resolve dead code and unused exports. By configuring the `fix_command` as `["npx", "fallow", "fix", "--yes"]` (or a global `fallow` binary), the execution runner will run:
```bash
npx fallow fix --yes <file_1> <file_2> ...
```
This is fully supported by Fallow and satisfies the auto-fix requirements without code changes.

---

## Proposed Configuration Template

To integrate Fallow as a quality gate (e.g. `gate1_fallow`) and enable auto-fixing, the following block can be added to the `.phase-gate/config/quality.yaml` file:

```yaml
active_gates:
  - gate1_fallow
  # ... other active gates

gates:
  gate1_fallow:
    name: "Fallow Codebase Intelligence"
    description: "Detect dead code, unused exports, duplication and complexity hotspots (JS/TS)"
    execution:
      command: ["npx", "fallow", "audit", "--format", "json"]
      fix_command: ["npx", "fallow", "fix", "--yes"]
      timeout_seconds: 120
      working_dir: null
    success:
      exit_codes_ok: [0]
      require_no_issues: true
    capabilities:
      file_types: [".js", ".jsx", ".ts", ".tsx"]
      supports_autofix: true
      parsing_strategy: "json_violations"
      json_violations:
        violations_path: "workspace_diagnostics"
        field_map:
          file: "path"
          line: "line"
          rule: "type"
          message: "message"
          severity: "severity"
        fixable_when: "auto_fixable"
    scope:
      exclude_globs:
        - "**/node_modules/**"
        - "**/dist/**"
```

### Explanation of Configuration Parameters:
- `execution.command`: Runs `fallow audit` returning machine-readable JSON output.
- `execution.fix_command`: Runs `fallow fix --yes` to automate resolving fixable issues.
- `capabilities.file_types`: Filters execution so that Fallow is only run when JavaScript or TypeScript files have changed (ignoring Python, YAML, and Markdown files).
- `capabilities.parsing_strategy`: Set to `json_violations`.
- `json_violations.violations_path`: Directs the `ViolationParser` to extract violations from the `"workspace_diagnostics"` array.
- `json_violations.field_map`: Maps Fallow keys directly to `ViolationDTO` attributes.
- `json_violations.fixable_when`: Tells the manager to treat a violation as auto-fixable if Fallow's JSON includes `"auto_fixable": true`.

---

## Open Questions & Risks

> [!NOTE]
> **Execution Environment Dependencies:**
> Since Fallow is executed via `npx` (Node Package Executor), the target environment must have Node.js and npm installed. If Node is missing, the gate will fail with a `Tool not found` error.

> [!WARNING]
> **Scope Filtering & Positional Arguments:**
> Fallow's CLI accepts positional arguments to limit analysis to specific files. However, some rules (like unused exports or unresolved imports) require workspace-wide visibility. Passing a subset of changed files to `fallow audit` might yield false negatives (or false positives) if Fallow cannot analyze the relationships with other files. For project-level verification, using `fallow` without positional file targets is safer.

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-18 | Antigravity | Initial draft and final research findings |
