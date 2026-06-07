<!-- docs\development\issue353\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-25T19:29Z updated=2026-05-25 -->
# create_branch: remove implicit auto-checkout (#353)

**Status:** DRAFT
**Version:** 1.1
**Last Updated:** 2026-05-25

---

## Scope

**In Scope:**
- `mcp_server/adapters/git_adapter.py` — root cause (1 line + 1 log message)
- `mcp_server/tools/git_tools.py` — return text correction (1 line)
- 4 tests in 2 files:
  - `tests/mcp_server/unit/adapters/test_git_adapter.py` (3 tests)
  - `tests/mcp_server/unit/tools/test_git_tools.py` (1 test)

**Out of Scope:**
- `.github/prompts/start-issue.prompt.md` — already structurally correct; no content change needed
- `IGitAdapter` protocol — does not exist in the codebase

---

## Summary

Remove the implicit auto-checkout from `GitAdapter.create_branch()` (single line),
correct the tool return text and adapter log message, and update 4 tests in 2 files that
assert the defect behavior. One TDD cycle. Clean break, no migration shim.

---

## Approved Strategy Constraints

The following constraints from research are **binding** for implementation:

| Constraint | Rationale |
|---|---|
| No optional `checkout: bool` flag | Would preserve the defect path as an opt-in; forbidden by Approved Strategy |
| No backward-compat shim | No production caller depends on auto-checkout as a supported contract |
| No bridge or cutover | Clean break only; `start-issue.prompt.md` step 3 already has the correct explicit `git_checkout` call |
| Prompt left unchanged | `.github/prompts/start-issue.prompt.md` is already correct for the post-fix world |

---

## TDD Cycles

### Cycle 1: C1 — Remove auto-checkout

**Goal:** Remove `new_branch.checkout()` from `GitAdapter.create_branch()`, correct tool
return text and adapter log message, update 4 tests to assert checkout is NOT called.

**Tests (RED phase — write/update these first):**

| Test | File | Change |
|---|---|---|
| `test_create_branch_with_head` | `tests/mcp_server/unit/adapters/test_git_adapter.py` | `checkout.assert_called_once()` → `checkout.assert_not_called()` |
| `test_create_branch_with_branch_name` | idem | `checkout.assert_called_once()` → `checkout.assert_not_called()` |
| `test_create_branch_with_commit_hash` | idem | `checkout.assert_called_once()` → `checkout.assert_not_called()` |
| `test_create_branch_tool_calls_manager_with_explicit_base` | `tests/mcp_server/unit/tools/test_git_tools.py` | `"Created and switched to branch"` → `"Created branch"` |

**Deliverables:**

| ID | Deliverable |
|---|---|
| C1.D1 | `new_branch.checkout()` removed from `GitAdapter.create_branch()` |
| C1.D2 | Tool return text: `"✅ Created branch: {name}"` (no "switched") |
| C1.D3 | Adapter log message: `"Created branch"` (not `"Created and checked out branch"`) |
| C1.D4 | 4 tests updated: `checkout.assert_not_called()` + corrected return text assertion |

**Exit Criteria:**

- C1.D1: `new_branch.checkout()` does not appear in `GitAdapter.create_branch()`
- C1.D2: Tool return text contains `"Created branch"` and not `"switched"`
- C1.D3: Adapter log message is `"Created branch"`
- C1.D4: All 4 updated tests pass
- Full test suite passes with zero regressions (`run_tests` scope full)
- Validation obligations satisfied (see below)

---

## Validation Obligations

Run `run_quality_gates(scope='files')` on all changed files before committing REFACTOR.
Active gates for `mcp_server/` and `tests/mcp_server/`:

| Gate | Tool | Scope |
|---|---|---|
| Gate 0: Ruff Format | `ruff format --check --isolated` | changed `.py` files |
| Gate 1: Ruff Strict Lint | `ruff check --isolated` (E,W,F,I,N,UP,ANN,B,C4,DTZ,T10,ISC,RET,SIM,ARG,PLC) | changed `.py` files |
| Gate 2: Import Placement | `ruff check --isolated --select=PLC0415` | changed `.py` files |
| Gate 3: Line Length | `ruff check --isolated --select=E501` | changed `.py` files |
| Gate 4b: Pyright | `pyright` strict | broad scope incl. `mcp_server/` |
| Gate 4c: mypy mcp_server | `mypy` targeted strict flags | `mcp_server/**/*.py` |
| Tests | `run_tests(scope='full')` | full suite |

Gate 4 (mypy strict for DTOs) is not applicable — no DTO changes.

---

## Risks

| Risk | Mitigation |
|---|---|
| Silent wrong-branch operation after fix | No such production path found in `mcp_server/`; confirmed by code inspection |
| Defect re-introduced | Updated tests assert `checkout.assert_not_called()` — will catch any reintroduction |

---

## Related Documentation
- **[docs/development/issue353/research.md][related-1]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-2]**
- **[docs/coding_standards/QUALITY_GATES.md][related-3]**

<!-- Link definitions -->

[related-1]: docs/development/issue353/research.md
[related-2]: ../../coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-3]: ../../coding_standards/QUALITY_GATES.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-25 | Agent | Initial draft |
| 1.1 | 2026-05-25 | Agent | QA NOGO fixes: forbidden constraints, deliverable IDs, gate list, test blast radius |
