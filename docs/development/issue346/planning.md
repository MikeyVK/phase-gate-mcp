<!-- docs/development/issue346/planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-30T06:14Z updated=2026-05-30T06:30Z -->
# Remove validate_architecture stub tool (#346)

**Status:** DRAFT  
**Version:** 1.1  
**Last Updated:** 2026-05-30

---

## Scope

**In Scope:**
ValidationTool + ValidationInput classes; QAManager import in validation_tools.py; server.py import/registration; stub test + stub imports in test_validation_tools.py; ValidationTool references in test_all_tools.py and test_extra_forbid.py; qa.agent.md allowlist entry; tool counts and rows in 8 active doc files.

**Out of Scope:**
ValidateDTOTool and ValidateDTOInput (no changes); QAManager itself; backend/ modules; archive docs (VSCODE_AGENT_ORCHESTRATION.md, PHASE_WORKFLOWS.md, GAP_ANALYSIS_IMPLEMENTATION_PLAN.md, docs/development/archive/).

---

## Summary

Clean break removal of ValidationTool + ValidationInput and all exclusive references from the MCP server. ValidateDTOTool and all real quality tools remain intact. One TDD cycle covers production code + all test files. Active documentation updates are documentation-phase obligations, separated from the TDD cycle.

---

## TDD Cycles

> **Approved Strategy:** Clean break — complete removal, no compatibility bridge. ValidateDTOTool is fully independent and untouched. Archive docs explicitly excluded.

### Cycle 1: Delete ValidationTool stub and all exclusive references

**Goal:** Remove ValidationTool and ValidationInput from the production tool surface and the full test suite in one coherent RED → GREEN → REFACTOR slice, leaving no dangling imports anywhere.

---

#### RED

**Action:** Add `test_validation_tool_class_removed()` to `test_validation_tools.py` after the existing imports:

```python
def test_validation_tool_class_removed() -> None:
    """RED: fails while ValidationTool exists; passes after stub deletion."""
    import mcp_server.tools.validation_tools as vt
    assert not hasattr(vt, "ValidationTool"), (
        "ValidationTool stub must be removed — it always returns success without performing validation"
    )
```

**Falsifiable failure:** This assertion fails immediately (`hasattr` returns `True` while the class still exists). Running the test suite confirms RED before any production code is touched.

**Commit sub-phase:** `red`

---

#### GREEN

All of the following changes must land in a single atomic pass so the suite turns green without intermediate ImportErrors.

| File | Change |
|------|--------|
| `mcp_server/tools/validation_tools.py` | Remove `QAManager` import (L9); remove `ValidationInput` class (L14-24); remove `ValidationTool` class (L26-44) |
| `mcp_server/server.py` | L129: remove `ValidationTool,` from joint import, leaving `ValidateDTOTool` only; remove L355 `ValidationTool(manager=self.qa_manager),` registration line |
| `tests/.../test_all_tools.py` | Remove `ValidationInput, ValidationTool` imports (L53-54); remove `make_validation_tool` factory (L172-173); remove `make_validation_tool()` call (L220); remove `test_validation_tool_flow` test method (L421-425) |
| `tests/.../test_validation_tools.py` | Remove `ValidationInput, ValidationTool` imports (L15-16); remove `test_validation_tool` stub test (L21-25); keep `test_validation_tool_class_removed` (now passes) and all ValidateDTOTool tests |
| `tests/.../test_extra_forbid.py` | Remove `(ValidationInput, {}),` parametrize entry (L118) |

**Why all files in one pass:** After `ValidationTool` and `ValidationInput` are deleted from `validation_tools.py`, any test file that still imports them raises `ImportError`. GREEN must be clean across the full import graph before the commit.

**Preservation obligation:** `ValidateDTOTool`, `ValidateDTOInput`, and both their tests in `test_validation_tools.py` (L28-58) are untouched. `test_validation_tools.py` is not deleted.

**Commit sub-phase:** `green`

---

#### REFACTOR

| File | Change |
|------|--------|
| `.github/agents/qa.agent.md` | Remove `- phase-gate-mcp/validate_architecture` entry (L25) |

**Quality gates:** Run `run_quality_gates` on all changed files (production + tests + agent config) before committing. Pylint 10.00/10 and mypy must pass. No `# type: ignore` additions permitted.

**Commit sub-phase:** `refactor`

---

#### Exit Criteria

- `ValidationTool` and `ValidationInput` are absent from `mcp_server/tools/validation_tools.py`
- `server.py` no longer imports or registers `ValidationTool`
- `test_all_tools.py` has no `ValidationTool` imports, factory, call, or test method
- `test_validation_tools.py` has no stub test and no stub imports; `test_validation_tool_class_removed` passes; ValidateDTOTool tests pass
- `test_extra_forbid.py` has no `ValidationInput` parametrize entry
- `qa.agent.md` does not list `phase-gate-mcp/validate_architecture`
- `grep -r "ValidationTool\|ValidationInput" mcp_server/ tests/` returns zero hits
- Full test suite green; pylint 10.00/10 + mypy pass on all changed files

#### Deliverables

| ID | Artifact | Phase |
|----|----------|-------|
| C1.D1 | RED test `test_validation_tool_class_removed` added to `test_validation_tools.py`; confirmed FAIL | RED |
| C1.D2 | `ValidationTool`, `ValidationInput`, `QAManager` import removed from `validation_tools.py` | GREEN |
| C1.D3 | `server.py` import fixed; `ValidationTool` registration removed | GREEN |
| C1.D4 | `test_all_tools.py` imports, factory, call, test removed | GREEN |
| C1.D5 | `test_validation_tools.py` stub test + stub imports removed; RED test passes; ValidateDTOTool tests intact | GREEN |
| C1.D6 | `test_extra_forbid.py` `ValidationInput` parametrize entry removed | GREEN |
| C1.D7 | `qa.agent.md` `validate_architecture` allowlist entry removed | REFACTOR |
| C1.D8 | Full test suite green; pylint 10.00/10 + mypy pass on changed files | REFACTOR |

---

## Documentation Phase Obligations

> Documentation phase is separate from the TDD cycle. These are not C1 deliverables.

The following 8 active doc files require semantic changes — row/entry removals and count corrections:

| File | Required change |
|------|----------------|
| `docs/reference/mcp/tools/quality.md` | Remove `validate_architecture` / `ValidationTool` row from tools table; update Quality tool count 4→3 |
| `docs/reference/mcp/MCP_TOOLS.md` | Remove `ValidationTool` entry; update total tool count 50→49 |
| `docs/mcp_server/README.md` | Update total tool count 50→49; update Quality group count 4→3 |
| `docs/mcp_server/TOOLS.md` | Remove `ValidationTool` row; update total count |
| `docs/mcp_server/ARCHITECTURE.md` | Remove `ValidationTool` reference where it appears in tool inventory |
| `docs/mcp_server/architectural_diagrams/03_tool_layer.md` | Update `validation_tools.py` entry from 2 tools to 1; remove ValidationTool sub-entry |
| `docs/mcp_server/architectural_diagrams/08_naming_landscape.md` | Remove `ValidationTool` row from naming table |
| `docs/reference/mcp/mcp_vision_reference.md` | Remove `ValidationTool` / `validate_architecture` reference |

**Constraint:** Archive docs (`VSCODE_AGENT_ORCHESTRATION.md`, `PHASE_WORKFLOWS.md`, `GAP_ANALYSIS_IMPLEMENTATION_PLAN.md`, `docs/development/archive/`) are explicitly excluded — do not update.

---

## Risky Seams

| File | Risk | Guard |
|------|------|-------|
| `server.py` L129 | Joint import — must keep `ValidateDTOTool` | After edit: `from mcp_server.tools.validation_tools import ValidateDTOTool` only |
| `test_validation_tools.py` | Partial deletion — stub test at L21-25 removed; ValidateDTOTool tests at L28-58 stay | Run tests after GREEN; confirm both ValidateDTOTool tests pass |
| GREEN atomicity | Any file that still imports a deleted symbol raises `ImportError` | All 5 file changes must land before running the suite |

---

## Related Documentation

- [mcp_server/tools/validation_tools.py](../../../mcp_server/tools/validation_tools.py)
- [mcp_server/server.py](../../../mcp_server/server.py)
- [tests/mcp_server/unit/tools/test_validation_tools.py](../../../tests/mcp_server/unit/tools/test_validation_tools.py)
- [tests/mcp_server/unit/integration/test_all_tools.py](../../../tests/mcp_server/unit/integration/test_all_tools.py)
- [tests/mcp_server/unit/tools/test_extra_forbid.py](../../../tests/mcp_server/unit/tools/test_extra_forbid.py)
- [.github/agents/qa.agent.md](../../../.github/agents/qa.agent.md)
- [docs/development/issue346/research.md](research.md)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.1 | 2026-05-30 | Agent | Revised per QA: falsifiable RED test; GREEN atomicity; docs moved to documentation phase |
| 1.0 | 2026-05-30 | Agent | Initial draft — 1 cycle, clean break, full constraints |
