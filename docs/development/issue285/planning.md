<!-- docs\development\issue285\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-09T06:40Z updated= -->
# Separate MCPServer composition root from runtime dispatch

**Status:** DRAFT  
**Version:** 0.1  
**Last Updated:** 2026-06-09

---

## Purpose

To separate the build phase (parsing environment, loading configurations, instantiating managers, and registering tools) from the dispatch phase (stdio communication, request handling, pre/post execution hooks) of MCPServer, complying with SRP and DIP.

## Scope

**In Scope:**
- Creation of `mcp_server/bootstrap.py`.
- Modification of `mcp_server/server.py`.
- Introduction of `make_test_server` in `tests/mcp_server/test_support.py` to prevent DRY violations.
- Migration of `conftest.py` and all 26 other test instantiations.

**Out of Scope:**
- Any changes to external consumer APIs (clean break approved).
- Changes to third-party library integrations.

---

## Invariants & Preservation Goals

- **Independent Test Support Factories:** Existing independent test support factories (`make_project_manager`, `make_phase_state_engine`, `make_qa_manager`, etc.) in `tests/mcp_server/test_support.py` must be preserved as-is. They must not be forced to use the new bootstrapper, maintaining isolation and fast unit testing.
- **Bootstrap Side-Effects:** Logging setup (`setup_logging`), audit log file initialization, and template registry bootstrapping must be fully preserved and owned by `ServerBootstrapper.bootstrap()`.
- **Observable Behavior:** The observable behavior of request dispatching, tool execution, and pre/post enforcement must remain unchanged.

---

## Assumptions

- No external consumers exist for the internal `MCPServer` constructor API, making a **Clean Break** strategy safe and optimal.
- The `Settings` object provided by the environment remains the SSOT for configuration paths.

---

## Open Questions

- None. (The strategy, scope, and TDD steps are fully defined).

---

## Approved Strategy & Constraints

- **Selected Strategy:** **Clean Break**.
- **Execution Constraints:**
  - Do not write or retain any compatibility shims or fallback parallel instantiation code in production.
  - The constructor of `MCPServer` must require constructor injection and must not fall back to self-bootstrapping.
  - The cutover must be atomic: once the constructor changes, all tests must use the new bootstrapper or mock injection immediately.

---

## Typing & Quality Gate Obligations

- **Typing Standards:** All code must conform to `docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md`. Dataclasses must be strictly typed, imports resolved using `TYPE_CHECKING` guards where necessary to prevent circular imports, and global disables are prohibited.
- **Per-Cycle Quality Gates:** At the end of **every cycle**, `run_quality_gates` must be executed on all changed production and test files. Each cycle must pass quality gates before proceeding.
- **Final Validation:** The final codebase must achieve 10.0/10 linting and pass all static type checking.

---

## Dependencies

- Cycle 2 depends on Cycle 1.
- Cycle 3 depends on Cycle 2.
- Cycle 4 depends on Cycle 3.
- Cycle 5 depends on Cycle 4.

---

## TDD Cycles

### Cycle 1: Define Immutable Dependency Containers (ConfigLayer & ManagerGraph)

**Goal:** Define ConfigLayer and ManagerGraph as frozen dataclasses in mcp_server/bootstrap.py to hold configuration models and manager classes.

**Tests:**
- tests/mcp_server/unit/server/test_bootstrap.py:TestImmutableContainers

**Success Criteria:**
- ConfigLayer and ManagerGraph are immutable.
- Mypy and pyright pass type validation for the dataclass structures.
- `run_quality_gates` executed and passes on changed files.

### Cycle 2: Extract Configuration and Manager Building Logic

**Goal:** Extract config loading, validation, logging setup, template registry bootstrapping, and manager instantiation from MCPServer.__init__ to ServerBootstrapper.

**Tests:**
- tests/mcp_server/unit/server/test_bootstrap.py:TestServerBootstrapperConfigsAndManagers

**Success Criteria:**
- `ServerBootstrapper(settings).bootstrap()` returns a valid `MCPServer` instance with configured managers wired and accessible via public attributes (e.g., `server.git_manager`).
- Side effects like logging setup, audit logs, and template registry bootstrapping are correctly triggered and observed.
- `run_quality_gates` executed and passes on changed files.

**Dependencies:** Cycle 1

### Cycle 3: Extract Tool and Resource Building Logic

**Goal:** Extract tool list composition and resource lists from MCPServer.__init__ into ServerBootstrapper.

**Tests:**
- tests/mcp_server/unit/server/test_bootstrap.py:TestServerBootstrapperToolsAndResources

**Success Criteria:**
- `ServerBootstrapper(settings).bootstrap()` returns an `MCPServer` containing the expected list of tools in `server.tools`.
- `ServerBootstrapper(settings).bootstrap()` returns an `MCPServer` containing the expected list of resources in `server.resources`.
- GitHub tools are conditionally registered based on token presence.
- `run_quality_gates` executed and passes on changed files.

**Dependencies:** Cycle 2

### Cycle 4: MCPServer DI Cutover, conftest Fixture Update, and Test Helper

**Goal:** Refactor MCPServer to accept constructor-injected dependencies, define make_test_server in tests/mcp_server/test_support.py to centralize test-server creation, and update the server conftest.py fixture.

**Tests:**
- tests/mcp_server/unit/server/test_bootstrap.py:TestMCPServerBootstrap
- tests/mcp_server/integration/mcp_server/test_server_startup.py

**Success Criteria:**
- MCPServer requires injected dependencies and no longer performs self-bootstrapping.
- make_test_server correctly builds and returns MCPServer.
- The server conftest fixture successfully uses make_test_server, and core integration tests pass.
- `run_quality_gates` executed and passes on changed files.

**Dependencies:** Cycle 3

### Cycle 5: Complete Test Blast Radius Migration & Validation

**Goal:** Migrate all remaining 26 test instantiations to use make_test_server() and update mcp_server/server.py:main() to use ServerBootstrapper. Run all quality gates.

**Tests:**
- tests/mcp_server/unit/test_server.py
- tests/mcp_server/unit/tools/test_cycle_tools.py
- tests/mcp_server/integration/mcp_server/test_server_tool_registration.py

**Success Criteria:**
- All 27 test locations are successfully migrated.
- No direct MCPServer() calls without arguments remain in test code.
- Grep verification (`grep_search` for `MCPServer()`) confirms zero legacy/parameterless instantiations.
- Quality gates run_quality_gates(files=[...]) return 10.0/10 and type checking passes.

**Dependencies:** Cycle 4

---

## Risks & Mitigation

- **Risk:** Circular imports between server.py and bootstrap.py.
  - **Mitigation:** Import ServerBootstrapper locally within server.py:main() and use from __future__ import annotations / TYPE_CHECKING guards in server.py.
- **Risk:** DRY violation in tests by repeating bootstrap setup 27 times.
  - **Mitigation:** Introduce make_test_server in test_support.py to centralize server creation in tests.
- **Risk:** GitHub adapter class mocking in integration tests fails when instantiations move to bootstrapper.
  - **Mitigation:** Ensure class-level patches in integration tests (e.g. conftest.py) successfully intercept the adapter instantiation.

---

## Milestones

- Milestone 1: ServerBootstrapper unit tests pass (Cycles 1-3)
- Milestone 2: MCPServer cutover and conftest integration green (Cycle 4)
- Milestone 3: Entire test suite migrated and quality gates pass (Cycle 5)

---

## Cleanup Expectations

- Grep search to verify zero parameterless/legacy `MCPServer()` calls.
- Verification that all unused imports in `mcp_server/server.py` are removed.

---

## Related Documentation
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-1]**
- **[docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md][related-2]**
- **[docs/development/issue285/research.md][related-3]**

<!-- Link definitions -->

[related-1]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-2]: docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md
[related-3]: docs/development/issue285/research.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-06-09 | Agent | Initial draft |
| 0.2 | 2026-06-09 | Agent | Addressed plan-verifier review feedback: added Invariants, Assumptions, Open Questions, typing obligations, per-cycle quality gates, and cleanup expectations. |
| 0.3 | 2026-06-09 | Agent | Fixed ARCHITECTURE_PRINCIPLES.md §14 violation: changed Cycles 2 and 3 success criteria to test through the public API bootstrap() instead of calling private _build_* methods. |