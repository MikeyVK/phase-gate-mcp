<!-- docs/development/issue346/validation.md -->
# Validation: Remove validate_architecture stub tool (#346)

**Status:** PASS  
**Version:** 1.0  
**Last Updated:** 2026-05-30

---

## Scope

**Branch:** `refactor/346-remove-validate-architecture-stub`  
**Validation focus:** Branch-wide verification after C1 (clean-break deletion of `ValidationTool` stub)  
**Approved Strategy:** Clean break — complete removal, no compatibility bridge

**In Scope:** `ValidationTool`, `ValidationInput`, their imports and registrations, stub test, agent config entry  
**Out of Scope:** `ValidateDTOTool`, `ValidateDTOInput`, `QAManager` itself, archive docs, documentation-phase updates (active doc tool-count changes)

---

## Verdict

**PASS** — All C1 exit criteria satisfied. Full suite green. Branch quality gates pass.

---

## Test Results

| Suite | Result | Detail |
|-------|--------|--------|
| Full test suite | ✅ PASS | 2848 passed, 11 skipped, 6 xfailed, 0 failed |
| Targeted scope (3 changed test files) | ✅ PASS | 74 passed, 0 failed |

---

## Quality Gates (branch scope — 5 changed files)

| Gate | Result |
|------|--------|
| Gate 0: Ruff Format | ✅ Pass |
| Gate 1: Ruff Strict Lint | ✅ Pass |
| Gate 2: Imports | ✅ Pass |
| Gate 3: Line Length | ✅ Pass |
| Gate 4: Types (mypy) | ⚠️ Skipped (not applicable) |
| Gate 4b: Pyright | ✅ Pass |
| Gate 4c: Types (mcp_server) | ✅ Pass |

**Overall: 6/6 active gates pass (1 inapplicable skipped)**

---

## Deliverable Evidence

| ID | Deliverable | Evidence |
|----|-------------|---------|
| C1.D1 | RED test `test_validation_tool_class_removed` added; FAIL confirmed | Test FAIL on `hasattr(vt, 'ValidationTool') == True`; commit `3df076b` |
| C1.D2 | `ValidationTool`, `ValidationInput`, `QAManager` import removed from `validation_tools.py` | File contains only `ValidateDTOInput` + `ValidateDTOTool`; no stub classes |
| C1.D3 | `server.py` import fixed; registration removed | L129: `import ValidateDTOTool` only; L355 `ValidationTool(...)` line absent |
| C1.D4 | `test_all_tools.py` — all ValidationTool references removed (5 locations) | Imports, factory `make_validation_tool`, call in `make_core_tools`, `test_validation_tool_flow`, call in `test_all_quality_tools_have_schemas` — all absent |
| C1.D5 | `test_validation_tools.py` — stub test + stub imports removed; invariant test passes | `test_validation_tool_class_removed` → PASS; ValidateDTOTool tests (2) → PASS |
| C1.D6 | `test_extra_forbid.py` — `ValidationInput` parametrize entry + import removed | `ValidationInput` not present in imports or parametrize list |
| C1.D7 | `qa.agent.md` — `validate_architecture` allowlist entry removed | `phase-gate-mcp/validate_architecture` absent from tools list |
| C1.D8 | Full suite green; quality gates pass | 2848 passed; branch gates 6/6 pass |

---

## Preservation Verification

| Preservation goal | Status | Evidence |
|-------------------|--------|---------|
| `ValidateDTOTool` intact | ✅ | `validation_tools.py` — class present; `test_dto_validation_tool` and `test_dto_validation_tool_missing_file` both pass |
| `ValidateDTOInput` intact | ✅ | Class present; `test_extra_forbid.py` `ValidateDTOInput` entry unchanged and passing |
| `QAManager` itself untouched | ✅ | Only `validation_tools.py` import of `QAManager` removed; `QAManager` class and all other consumers unaffected |
| `test_validation_tools.py` file kept | ✅ | File exists with 3 tests (1 invariant + 2 ValidateDTOTool tests) |

---

## Approved Strategy Alignment

| Constraint | Status |
|-----------|--------|
| Clean break — no compatibility bridge | ✅ Stub fully deleted; no deprecation path |
| Archive docs out of scope | ✅ Not touched |
| Active doc updates deferred to documentation phase | ✅ Not in C1; documentation-phase obligations documented in planning.md |

---

## Grep Confirmation

`grep -r "ValidationTool\|ValidationInput" mcp_server/ tests/` — results:

- `mcp_server/`: zero hits on `ValidationTool` or `ValidationInput` as class names (only `TemplateValidationTool` and `TemplateValidationInput` — unrelated tool)
- `tests/`: only the invariant test string `"ValidationTool"` in the assertion message, and `TemplateValidationTool` in its own test file

**No dangling references in production code or tests.**

---

## Live Demonstration

No meaningful live server demo is applicable — the change is a pure deletion. The closest observable fallback:

1. Start the MCP server and inspect the tool registry: `validate_architecture` is absent from the tool list
2. Run `pytest tests/mcp_server/unit/tools/test_validation_tools.py -v` — `test_validation_tool_class_removed` passes; both ValidateDTOTool tests pass
3. Check `qa.agent.md` — `validate_architecture` is no longer in the allowlist

---

## Residual Items

- **Documentation phase (not yet done):** 8 active doc files require row/count updates (`quality.md`, `MCP_TOOLS.md`, `README.md`, `TOOLS.md`, `ARCHITECTURE.md`, `03_tool_layer.md`, `08_naming_landscape.md`, `mcp_vision_reference.md`). These are explicitly deferred to the documentation phase per planning.

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-30 | Agent | Initial validation report — PASS |
