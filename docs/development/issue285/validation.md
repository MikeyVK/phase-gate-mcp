<!-- docs\development\issue285\validation.md -->
<!-- template=validation_report version=fe38a66d created=2026-06-09T15:10Z updated= -->
# Validation Report: Separate MCPServer composition root from runtime dispatch (Issue #285)


**Status:** DRAFT  
**Version:** 0.1  
**Last Updated:** 2026-06-09  
**Validation Outcome:** PASS  
**Issue:** #285  
**Cycle:** Branch-wide (Cycles 1-5)  

---

## Validation Scope & Prerequisites

Branch-wide validation after completion of 5 TDD refactor cycles on branch `refactor/285-separate-mcpserver-composition-root`.

**Prerequisites verified:**
- Research artifact (`docs/development/issue285/research.md`) — APPROVED status
- Planning artifact (`docs/development/issue285/planning.md`) — v0.3, addresses §14 QA finding
- Approved Strategy: **Clean Break** (no shims, no fallbacks)
- Architecture contract: `ARCHITECTURE_PRINCIPLES.md` consulted throughout

---

## Summary Verdict

**PASS** ✅

All 5 TDD cycles completed successfully. The MCPServer composition root has been fully separated from runtime dispatch. All planned deliverables are satisfied, all quality gates pass, and zero legacy instantiations remain.

---

## Full-Suite Test Result

```
run_tests(scope='full')
→ 2877 passed, 11 skipped, 6 xfailed, 23 warnings in 42.27s
→ exit_code: 0, failures: 0, errors: 0
```

---

## Branch Quality-Gate Result

```
run_quality_gates(scope='branch') → 13 files
→ overall_pass: true
→ Gate 0: Ruff Format       — passed
→ Gate 1: Ruff Strict Lint  — passed
→ Gate 2: Imports           — passed
→ Gate 3: Line Length       — passed
→ Gate 4b: Pyright          — passed
```

---

## Deliverable Mapping

| Deliverable | Description | Evidence | Status |
|---|---|---|---|
| D1.1 | ConfigLayer `@dataclass(frozen=True)` with 14 config fields | `bootstrap.py:144-161` | ✅ |
| D1.2 | ManagerGraph `@dataclass(frozen=True)` with 17 manager fields | `bootstrap.py:164-184` | ✅ |
| D1.3 | Unit tests for immutability and type-checking | `TestBootstrap` in `test_bootstrap.py:55-115` | ✅ |
| D2.1 | ServerBootstrapper composition of ConfigLayer | `_build_config_layer()` at `bootstrap.py:239-287` | ✅ |
| D2.2 | ServerBootstrapper composition of ManagerGraph | `_build_manager_graph()` at `bootstrap.py:289-412` | ✅ |
| D2.3 | Bootstrap side-effects (logging, audit, template registry) | `ServerBootstrapper.bootstrap()` at `bootstrap.py:198-216` | ✅ |
| D3.1 | ServerBootstrapper composition of tools list | `_build_tools()` at `bootstrap.py:414-615` | ✅ |
| D3.2 | ServerBootstrapper composition of resources list | `_build_resources()` at `bootstrap.py:617-631` | ✅ |
| D4.1 | MCPServer.__init__ constructor injection cutover | `server.py:59-66` — requires `settings`, `configs`, `managers`, `tools`, `resources` | ✅ |
| D4.2 | `make_test_server` in `tests/mcp_server/test_support.py` | Factory at `test_support.py:560-567` | ✅ |
| D4.3 | conftest.py server fixture update | `conftest.py:35` uses `make_test_server` | ✅ |
| D4.4 | Constructor rejection test | `test_mcp_server_requires_injected_dependencies` at `test_bootstrap.py:329-335` | ✅ |
| D5.1 | Migration of remaining 26+ test instantiations | `grep MCPServer()` returns 0 results in tests and production | ✅ |
| D5.2 | Update `mcp_server/server.py:main()` | `main()` at `server.py:388-395` uses `ServerBootstrapper(settings).bootstrap()` | ✅ |
| D5.3 | All quality gates pass | Branch quality gates: 5/5 active passed | ✅ |

---

## Research & Approved Strategy Alignment

### Approved Strategy: Clean Break

| Constraint | Satisfied | Evidence |
|---|---|---|
| No compatibility shims or fallback code | ✅ | No fallback instantiation logic in `MCPServer.__init__` |
| Constructor requires injection, no self-bootstrapping | ✅ | All 5 params are required positional, no defaults |
| All 27 test instantiations updated | ✅ | `grep MCPServer()` returns 0 results; only 2 intentional `MCPServer(` calls in `test_bootstrap.py` for constructor validation |
| No regression tests left behind | ✅ | All tests migrated or updated |
| Circular import avoidance | ✅ | `bootstrap.py` uses `TYPE_CHECKING` guard (L30-31) and local import (L229); `server.py:main()` uses local import (L390) |

### Preservation Goals

| Goal | Satisfied | Evidence |
|---|---|---|
| Independent test factories preserved | ✅ | `make_project_manager`, `make_phase_state_engine`, etc. untouched in `test_support.py:242-543` |
| Logging/audit setup preserved | ✅ | `setup_logging()` called in `ServerBootstrapper.bootstrap()` at `bootstrap.py:198-216` |
| Template registry bootstrapping preserved | ✅ | `TemplateRegistry` bootstrapped in `ServerBootstrapper.bootstrap()` |
| Observable dispatch behavior unchanged | ✅ | 2877 tests pass, including integration tests for tool dispatch |
| Public attribute surface preserved | ✅ | `MCPServer.__init__` unpacks `ManagerGraph` onto public attributes at `server.py:74-93` |

### Architecture Principles Compliance

| Principle | Satisfied | Evidence |
|---|---|---|
| §14 — Test via public API only | ✅ | All tests call `bootstrap()` or public constructors, never `_build_*` private methods |
| SRP — Single Responsibility | ✅ | Build phase in `bootstrap.py`, dispatch in `server.py` |
| DIP — Dependency Inversion | ✅ | `MCPServer` receives all dependencies via constructor |
| Frozen dataclasses for value objects | ✅ | `ConfigLayer` and `ManagerGraph` are `@dataclass(frozen=True)` |

---

## Live Demonstration Proposal

### Why No Meaningful Live Demo Exists

This refactoring is a **structural separation** of the composition root from runtime dispatch. The observable runtime behavior of the MCP server (tool execution, resource listing, stdio protocol) is **intentionally identical** before and after the refactor. There is no new user-facing feature to demonstrate.

### Closest Observable Fallback Evidence

1. **Full test suite** (2877 tests): Proves all existing behavior is preserved.
2. **Constructor rejection test**: `test_mcp_server_requires_injected_dependencies` at `test_bootstrap.py:329-335` proves the old `MCPServer(settings=only)` constructor is now rejected with `TypeError`, confirming the clean break.
3. **Grep verification**: `MCPServer()` zero-argument calls return 0 results across the entire codebase.
4. **Entry point verification**: `main()` in `server.py` uses `ServerBootstrapper(settings).bootstrap()` as the sole composition path.

---

## Branch Diff Statistics

```
28 files changed, 2682 insertions(+), 611 deletions(-)
```

**Key production changes:**
- `mcp_server/bootstrap.py` — +631 lines (NEW)
- `mcp_server/server.py` — net ~-79 lines (composition logic removed)

**Key test changes:**
- `tests/mcp_server/unit/server/test_bootstrap.py` — +363 lines (NEW, 4 test classes, 11 tests)
- 8 test files migrated to `make_test_server()`

---

## Residual Risks, Caveats & Follow-up Items

| # | Item | Severity | Details |
|---|---|---|---|
| 1 | **`pytest_output.txt` stale file** | Low | Appears in branch diff (+30 lines). Should be cleaned up or `.gitignore`d before merge. |
| 2 | **`_build_resources` unused params** | Low | `configs` and `managers` params in `_build_resources()` are suppressed with `ARG002`. They exist for API symmetry with `_build_tools()` but are currently unused. Intentional design choice. |
| 3 | **Duplicate `BranchValidatedStateReader` instantiation** | Low | `_build_manager_graph` creates one (L302), `_build_tools` creates another (L418). Not a bug (stateless wrappers), but minor DRY concern. |
| 4 | **`pyright: ignore[reportPrivateUsage]` in test** | Low | `test_bootstrap.py:352` accesses `server._settings` with rationale comment. Compliant with §14 for unavoidable test infrastructure. |
| 5 | **`pyright: reportMissingImports=false` in server.py** | Low | Line 1 global suppress pre-dates the refactor. Should be verified as still necessary after import cleanup. |
| 6 | **No explicit unit test for `main()` wiring** | Medium | `main()` at `server.py:388-395` has no dedicated unit test. Integration tests exercise the full path, but a targeted test would strengthen proof. |
| 7 | **`make_test_server()` performance** | Low | Every test now goes through the full bootstrapper (14 configs, 17 managers). May increase unit test execution time. Not a correctness issue. |

---

## Related Documentation

- [Research artifact](research.md)
- [Planning artifact](planning.md)
- [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [Type Checking Playbook](../../coding_standards/TYPE_CHECKING_PLAYBOOK.md)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-06-09 | Agent | Initial draft with full validation evidence |
