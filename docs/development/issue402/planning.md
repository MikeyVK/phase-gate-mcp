<!-- docs/development/issue402/planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-15T00:20Z updated= -->
# Planning — Issue #402: Quality Gates Verbose Option

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-06-15

---

## Purpose

Slice the implementation of the `verbose` option for the `run_quality_gates` tool (Issue #402) into a safe, sequential TDD cycle.

## Scope

**In Scope:**
- Add `verbose: bool` option to `RunQualityGatesInput`.
- Add `details: str` field to `GateResultDTO`.
- Capture stdout/stderr of subprocesses in `QAManager` when `verbose=True`.
- Generate `RecoveryNote` when checks fail and `verbose=False`.

**Out of Scope:**
- Any changes to other quality tools or caching managers.

## Prerequisites

Read these first:
1. [Quality Gates Verbose Output Design](file:///c:/temp/pgmcp/docs/development/issue402/quality_gates_verbose_design.md)

---

## Summary

The planning follows the Approved Strategy: we will implement the verbose option for the quality gates tool and verify it using unit tests and quality gates checks.

---

## TDD Cycles

### Cycle 1: Quality Gates Verbose Option

**Goal:** Extend the `run_quality_gates` tool with a `verbose` option to expose stdout/stderr details for failing checks without cluttering the presenter output.

**Deliverables:**
- **[D1.1]** Add `verbose: bool = Field(default=False, ...)` to `RunQualityGatesInput` in `mcp_server/tools/quality_tools.py`.
- **[D1.2]** Add `details: str = ""` field to `GateResultDTO` in `mcp_server/schemas/tool_outputs.py`.
- **[D1.3]** Update `QAManager.run_quality_gates` and `_execute_gate` to accept `verbose: bool` and populate `GateResultDTO.details` with process stdout/stderr when verbose is enabled.
- **[D1.4]** Update `RunQualityGatesTool.execute` to propagate `verbose` to the manager, and to generate a `RecoveryNote` on failures when `verbose=False`.
- **[D1.5]** Update `tests/mcp_server/unit/tools/test_quality_tools.py` and `tests/mcp_server/unit/managers/test_qa_manager.py` to cover the new verbose options and RecoveryNotes.

**Tests:**
- `tests/mcp_server/unit/tools/test_quality_tools.py`
- `tests/mcp_server/unit/managers/test_qa_manager.py`

**Success/Exit Criteria:**
`run_quality_gates` with `verbose=True` populates the `details` field with stdout/stderr upon failure, and caching of this DTO is verified. Running with `verbose=False` leaves `details` empty but generates a `RecoveryNote` on failure.
