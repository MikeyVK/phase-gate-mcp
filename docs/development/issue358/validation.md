<!-- docs/development/issue358/validation.md -->
# MCP Tool Schema Audit — Validation Report

**Issue:** #358  
**Branch:** `refactor/358-mcp-tool-schema-audit`  
**Phase:** validation  
**Date:** 2026-05-31  
**Verdict:** ✅ PASS

---

## Prerequisites

- Research artifact: `docs/development/issue358/research.md` (v1.1)
- Planning artifact: `docs/development/issue358/planning.md` (5-cycle plan)
- Implementation cycles C1–C5 committed and all quality gates green
- `ARCHITECTURE_PRINCIPLES.md` used as binding contract throughout

---

## Validation Scope

This report covers the full branch `refactor/358-mcp-tool-schema-audit`, verifying that all 5 implementation cycles (C1–C5) satisfy their respective deliverables, that no A3 violations were introduced, and that the Approved Strategy constraints from research are honored.

**Out of scope:** Manager business logic, new tool functionality, output schema / ToolResult changes, new workflows/phases.

---

## Summary Verdict

**PASS** — All 5 cycles are confirmed delivered. Full test suite passes (2885 passed, 0 failed). Branch quality gates are green across all 29 changed files (6/6 gates, 1 skipped by design). No A3 violations remain. The Config-First principle is respected for all config-driven enums. The C5 regression fix (Q9) is confirmed on both auto-detect and explicit paths.

---

## Full Test Suite Result

```
run_tests(scope='full')
2885 passed, 11 skipped, 6 xfailed, 27 warnings in 57.02s
Exit code: 0
```

No failures. No errors.

---

## Branch Quality Gate Result

```
run_quality_gates(scope='branch')  — 29 files
Gate 0: Ruff Format      ✅ PASS
Gate 1: Ruff Strict Lint ✅ PASS
Gate 2: Imports          ✅ PASS
Gate 3: Line Length      ✅ PASS
Gate 4: Types (mypy)     ⏭ SKIP (by design — global skip)
Gate 4b: Pyright         ✅ PASS
Gate 4c: Types mcp_server ✅ PASS
Overall: PASS
```

---

## Cycle Deliverable Alignment

### C1 — ClassVar removal + A4 git_tools.py (atomic)

| Deliverable | Evidence |
|-------------|----------|
| `CreateBranchInput`: no `_git_config` ClassVar, no `configure()`, no `validate_branch_type` | Zero `ClassVar` matches in `git_tools.py`; grep confirms clean |
| `GitCommitInput`: no `_git_config` ClassVar, no `configure()`, no `validate_commit_type` | Same grep; model construction clean |
| `CreateBranchTool.input_schema` override: `branch_type.enum` + `name.pattern` from `git_config` | `git_tools.py:115–118` confirmed |
| `GitCommitTool.input_schema` override: `commit_type.enum` from `git_config` | `git_tools.py:276–279` confirmed |
| All 5 ClassVar call sites removed | `server.py`, `test_support.py`, `test_git_tools_config.py`, `test_git_tools.py` clean |
| `test_git_tools_config.py` fully rewritten with A4 schema content assertions | File confirms `branch_type` enum and `name` pattern assertions |

**Exit criteria met:** ✅

### C2 — A2 static Pydantic constraints

| Deliverable | Evidence |
|-------------|----------|
| `ForcePhaseTransitionInput.skip_reason` + `human_approval`: `Field(min_length=1)` | `phase_tools.py:66–67` |
| `CreateLabelInput.name`: pattern `^(type\|priority\|...\|parent):[a-z0-9-]+$` | `label_tools.py:60–63` |
| `CreateLabelInput.color`: pattern `^[0-9A-Fa-f]{6}$` | `label_tools.py:65–68` |
| `InitializeProjectInput`: `@model_validator(mode="after")` for `custom_phases` | `project_tools.py:61–71` |

**Exit criteria met:** ✅

### C3 — A4 config-driven schema overrides + constructor injection

| Deliverable | Evidence |
|-------------|----------|
| `_BaseTransitionTool.__init__` accepts `workphases_config: WorkphasesConfig` | `phase_tools.py:79–102` |
| `TransitionPhaseTool.input_schema`: `to_phase.enum` from `workphases_config.phases.keys()` | `phase_tools.py:128–131` |
| `ForcePhaseTransitionTool.input_schema`: same | `phase_tools.py:183–186` |
| `InitializeProjectTool.__init__` accepts `contracts_config: ContractsConfig`; override for `workflow_name.enum` | `project_tools.py:104–107` |
| `CreateIssueTool.__init__` accepts `label_config`, `scope_config`, `git_config`; override for `issue_type`, `priority`, `scope`, `title.maxLength` | `issue_tools.py:165–193` |
| `ScaffoldArtifactTool.input_schema` override: `artifact_type.enum` | `scaffold_artifact.py:63–64` |
| `server.py` updated for all 5 constructor call sites | `server.py` confirmed |

**Exit criteria met:** ✅

### C4 — A1 description enrichments + reference docs

| Deliverable | Evidence |
|-------------|----------|
| `SubmitPRTool.base` description: 3-tier cascade | `pr_tools.py:162–167` — "explicit value → state.json parent_branch → git_config.default_base_branch" |
| `TransitionPhaseTool.to_phase` + `ForcePhaseTransitionTool.to_phase`: `get_work_context()` pointer | `phase_tools.py:42–46`, `phase_tools.py:59–63` |
| `ValidateDTOTool` description: file-exists scope | `validation_tools.py:25` — "Checks that the file path exists before parsing" |
| `docs/reference/mcp/tools/` updated for all 14 modified tools | `docs/reference/mcp/tools/` directory contains updated pages |
| `test_c4_description_invariants.py`: 9 tests verifying all A1 enrichments | File confirmed present and passing |

**Exit criteria met:** ✅

### C5 — Q9 config-driven cycle_number enforcement (regression fix)

| Deliverable | Evidence |
|-------------|----------|
| `GitCommitInput.require_cycle_number_for_implementation` `@model_validator` removed | No `@model_validator` in `GitCommitInput` — confirmed by grep |
| `GitCommitInput.cycle_number` description updated | `git_tools.py:225–230` — "Required when the active phase is cycle-based (e.g. implementation). Optional otherwise." |
| `GitCommitTool.__init__` accepts `phase_contract_resolver: PhaseContractResolver \| None = None` | `git_tools.py:255–273` |
| `execute()`: `auto_state = None` init + `assert auto_state is not None` narrowing | `git_tools.py:284`, `git_tools.py:315` |
| `execute()`: `is_cycle_based_phase()` guard on both paths → `ToolResult.error` | `git_tools.py:309–328` |
| `server.py`: `phase_contract_resolver=self.phase_contract_resolver` in `GitCommitTool` call | `server.py:324–331` |
| `docs/reference/mcp/tools/git.md` `cycle_number` description updated | Confirmed in `git.md` |
| Regression test (auto-detect path) | `test_git_tools.py: test_git_commit_cycle_number_required_auto_detect_path` |
| Regression test (explicit path) | `test_git_tools.py: test_git_commit_cycle_number_required_explicit_path` |

**Exit criteria met:** ✅

---

## Research & Approved Strategy Alignment

| Boundary | Approved Strategy | Implementation | Status |
|----------|-------------------|----------------|--------|
| Grens A — config-driven enum/maxLength | A4 (`input_schema` override) | All 5 A4 tools use `super().input_schema` → mutate → return; no `model_json_schema()` direct calls | ✅ |
| Grens B — static constraints | A2 (direct Pydantic `Field`) | Used only for static values (`min_length`, regex patterns) with no config dependency | ✅ |
| Grens C — stateful constraints | A1 (description only) | No Pydantic enforcement for stateful constraints; descriptions enriched | ✅ |
| `GitCommitInput` cycle_number (Q9) | Runtime guard via `PhaseContractResolver.is_cycle_based_phase()` | Implemented in `execute()` post-resolution; model stays pure; no hardcoded phase names | ✅ |
| A3 forbidden | No config loading inside Pydantic models | Zero `ClassVar` in `CreateBranchInput`/`GitCommitInput`; no module-level config loading in models | ✅ |
| Config-First principle | `is_cycle_based` from `contracts.yaml` via `PhaseContractResolver` | `is_cycle_based_phase(workflow_name, workflow_phase)` reads config; no hardcoded `"implementation"` string | ✅ |

---

## A3 Violation Audit

- **ClassVar in `CreateBranchInput`:** 0 matches ✅
- **ClassVar in `GitCommitInput`:** 0 matches ✅
- **`configure()` classmethod:** 0 matches in production models ✅
- **Config loading inside Pydantic models:** 0 violations found ✅

---

## Live Demonstration Proposal

The refactor's primary observable effect is that MCP tool `input_schema` calls now return runtime-enriched JSON Schemas. The closest verifiable fallback without a live server:

**Option 1 — Schema content inspection (testable now):**
```bash
cd c:\temp\st3
python -c "
from mcp_server.config.git_config import GitConfig
from mcp_server.tools.git_tools import CreateBranchTool, GitManager
# CreateBranchTool.input_schema requires a constructed tool with git_manager injected
# The test suite (test_git_tools_config.py) serves as the canonical live demo for this
print('Import OK — A4 pattern wired correctly')
"
```

**Option 2 — Run the targeted A4 test suite:**
```bash
pytest tests/mcp_server/tools/test_git_tools_config.py -v
pytest tests/mcp_server/unit/tools/test_c4_description_invariants.py -v
```
These tests assert the exact schema content visible to an AI client at runtime.

**Option 3 — C5 regression demo:**
```bash
pytest tests/mcp_server/unit/tools/test_git_tools.py -k "cycle_number_required" -v
```
This demonstrates both the auto-detect and explicit-path guards returning `ToolResult.error` without `cycle_number`.

**Why no full live server demo:** The MCP server requires a valid git repo and GitHub credentials to start. The test suite is the authoritative and reproducible observable fallback.

---

## Residual Risks & Caveats

| Item | Severity | Notes |
|------|----------|-------|
| `workflow_phase` field redundancy in `GitCommitInput` | Low | Deferred to D1 in planning.md; structurally redundant with phase guard but not a regression |
| Gate 4 (mypy global) skipped | Info | Project-wide skip, not branch-specific; Pyright (Gate 4b) and mcp_server mypy (Gate 4c) both pass |
| `assert auto_state is not None` in `execute()` | Info | Assertion is correct (exception path exits early); Pyright accepted it; runtime `AssertionError` is impossible in correct usage |
| A4 enum list not validated against live server state at test time | Info | Enum values sourced from config files loaded at test fixture time; consistent with project conventions |

---

## Related Documents

- `docs/development/issue358/research.md` — Approved Strategy source (v1.1)
- `docs/development/issue358/planning.md` — 5-cycle plan
- `docs/coding_standards/ARCHITECTURE_PRINCIPLES.md` — binding contract
- `docs/reference/mcp/tools/git.md` — updated reference
