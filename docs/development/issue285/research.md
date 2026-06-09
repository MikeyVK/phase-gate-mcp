<!-- docs\development\issue285\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-07T20:39Z updated= -->
# Research: Separate MCPServer composition root from runtime dispatch (Issue #285)

**Status:** APPROVED  
**Version:** 0.1  
**Last Updated:** 2026-06-07

---

## Purpose

Produce a definitive research document mapping the SRP refactoring of `MCPServer`, identifying the precise blast radius in production and test layers, and establishing the strategy parameters for planning.

## Scope

**In Scope:**
* Repository-local analysis of `mcp_server/` composition logic.
* Meticulous mapping of the blast radius across production files and test suites.
* Design of the bootstrapper and dependency schemas.

**Out of Scope:**
* External consumer compatibility (clean break path approved).
* Third-party library integrations or web/framework research.

## Prerequisites

1. Read [docs/coding_standards/ARCHITECTURE_PRINCIPLES.md](file:///c:/temp/pgmcp/docs/coding_standards/ARCHITECTURE_PRINCIPLES.md) (binding contract).
2. Read [docs/coding_standards/DOCUMENTATION_STANDARD.md](file:///c:/temp/pgmcp/docs/coding_standards/DOCUMENTATION_STANDARD.md).
3. Verify test coverage is stable before making changes.

---

## Problem Statement

The class `MCPServer` in [mcp_server/server.py](file:///c:/temp/pgmcp/mcp_server/server.py) currently violates the Single Responsibility Principle (SRP) and is a God Class. It mixes:
1. **Composition Root Concerns**: Parsing environment settings, constructing `ConfigLoader`, loading 14 config files, validating startup state, instantiating 13 managers, and registering over 30 tools and resources.
2. **Runtime Protocol Dispatch Concerns**: Initializing the stdio server, setting up request handlers, validating arguments, and running pre/post-execution tool enforcement.

To resolve this Technical Debt, we must separate the **Build** phase from the **Dispatch** phase by extracting a dedicated `ServerBootstrapper` class and value objects for the dependencies, while maintaining a clear and clean architecture.

---

## Findings & Meticulous Blast Radius Analysis

### 1. Affected Production Code (Blast Radius)

| File | Target / Symbol | Proposed Change / Impact | Risk |
|---|---|---|---|
| [mcp_server/server.py](file:///c:/temp/pgmcp/mcp_server/server.py) | `MCPServer` | Strip all config loading, manager instantiation, tool/resource registration, and template registry bootstrapping from `__init__`. The constructor will now accept fully constructed dependencies via constructor injection. | High |
| [mcp_server/server.py](file:///c:/temp/pgmcp/mcp_server/server.py) | `main()` | Modify to instantiate `ServerBootstrapper` and call its `bootstrap()` method to obtain a fully composed `MCPServer` instance before executing `run()`. | Medium |
| [mcp_server/bootstrap.py](file:///c:/temp/pgmcp/mcp_server/bootstrap.py) | [NEW] `ServerBootstrapper` | Implements the composition root. Responsible for loading configs, validating startup, configuring logging, bootstrapping the template registry, creating managers, registering tools, and returning a configured `MCPServer`. | High |
| [mcp_server/bootstrap.py](file:///c:/temp/pgmcp/mcp_server/bootstrap.py) | [NEW] `ConfigLayer`, `ManagerGraph` | Immutable dataclasses (`frozen=True`) to bundle configuration models and managers respectively, facilitating clean injection and type safety. | Low |

### 2. Affected Test Code (Blast Radius)

The search for imports of `MCPServer` shows that the server is instantiated exactly **27 times** across integration and unit tests. Every single one of these instantiations represents a point in the blast radius that must be updated.

| File | Symbol / Context | Change / Impact |
|---|---|---|
| [tests/mcp_server/integration/mcp_server/conftest.py](file:///c:/temp/pgmcp/tests/mcp_server/integration/mcp_server/conftest.py) | `server` fixture (lines 17-34) | Change `MCPServer(settings=settings)` to `ServerBootstrapper(settings=settings).bootstrap()`. |
| [tests/mcp_server/unit/test_server.py](file:///c:/temp/pgmcp/tests/mcp_server/unit/test_server.py) | `server` instantiations (10 occurrences) | Replace direct `MCPServer()` instantiation with `ServerBootstrapper(settings).bootstrap()` or pass explicit mock dependencies for isolated unit tests. |
| [tests/mcp_server/unit/tools/test_cycle_tools.py](file:///c:/temp/pgmcp/tests/mcp_server/unit/tools/test_cycle_tools.py) | `server` instantiations (4 occurrences) | Replace direct `MCPServer()` with `ServerBootstrapper(settings).bootstrap()`. |
| [tests/mcp_server/unit/server/test_validate_tool_arguments.py](file:///c:/temp/pgmcp/tests/mcp_server/unit/server/test_validate_tool_arguments.py) | `server` fixture (lines 80-84) | Replace `MCPServer()` with `ServerBootstrapper().bootstrap()`. |
| [tests/mcp_server/integration/test_strict_input_validation_response.py](file:///c:/temp/pgmcp/tests/mcp_server/integration/test_strict_input_validation_response.py) | `server` fixture (lines 53-56) | Replace `MCPServer()` with `ServerBootstrapper().bootstrap()`. |
| [tests/mcp_server/integration/mcp_server/test_server_tool_registration.py](file:///c:/temp/pgmcp/tests/mcp_server/integration/mcp_server/test_server_tool_registration.py) | 7 tool registration assertions | Replace `MCPServer()` with `ServerBootstrapper().bootstrap()`. |
| [tests/mcp_server/integration/mcp_server/test_server_lifecycle.py](file:///c:/temp/pgmcp/tests/mcp_server/integration/mcp_server/test_server_lifecycle.py) | `server` instantiations (2 occurrences) | Replace `MCPServer(settings=...)` with `ServerBootstrapper(settings=...).bootstrap()`. |

### 3. Affected Test Helpers (Blast Radius)

* **[tests/mcp_server/test_support.py](file:///c:/temp/pgmcp/tests/mcp_server/test_support.py)**: Contains independent factory helpers (`make_project_manager`, `make_phase_state_engine`, etc.) which duplicate part of the composition. 
  * *Refactoring Policy*: To keep unit tests fast and isolated, we will **preserve** these helpers as independent, test-only factories. We will not force them to use the bootstrapper, avoiding heavy DI setup where simple mocks are preferred.

---

## Candidate Seams

1. **ServerBootstrapper (Primary Seam)**
   * Extracted to `mcp_server/bootstrap.py`. Encapsulates composition via explicit private/public pipeline methods:
     * `_build_config_layer() -> ConfigLayer`
     * `_build_manager_graph(configs, template_registry) -> ManagerGraph`
     * `_build_tools(configs, graph) -> list[BaseTool]`
     * `_build_resources(configs, graph) -> list[Resource]`
     * `bootstrap() -> MCPServer`
2. **Immutable Dependency Containers**
   * `@dataclass(frozen=True)` value objects to pass loaded components type-safely.
3. **Clean Injection in MCPServer**
   * `MCPServer` receives dependencies cleanly through constructor:
     ```python
     def __init__(
         self,
         settings: Settings,
         tools: list[BaseTool],
         resources: list[Resource],
         enforcement_runner: EnforcementRunner,
         managers: ManagerGraph,
     ) -> None:
     ```
     This keeps `MCPServer` public attributes (like `self.git_manager`) intact for test assertions, but isolates the construction.

---

## Approved Strategy

* **Boundary / preservation scope**: Server composition boundary inside `mcp_server/server.py` and repo-local test consumers of `MCPServer`.
* **Selected strategy**: **Clean Break**.
* **Rationale**: The project has not released the phase-gate MCP server yet, so there are no external users. A clean break avoids compatibility shims, deprecation layers, or temporary parallel composition paths. It ensures zero legacy debt is retained.
* **Constraints for later phases**: Do not add compatibility shims or fallback parallel instantiation code. Preserve observable behavior only where repo tests assert it. Update all 27 server-level test instantiations to use the bootstrapper directly. No regression tests may be left over after implementation.

---

## Resolved & Open Questions

1. **Which test helpers should move with composition?**
   * *Resolution*: Test factories in [test_support.py](file:///c:/temp/pgmcp/tests/mcp_server/test_support.py) remain as thin test-only fixtures to keep unit tests isolated and fast.
2. **Do server tests rely on construction side-effects?**
   * *Resolution*: Yes, mainly for setting up logging, audit files, and template registries. These side effects are now owned by `ServerBootstrapper.bootstrap()`.
3. **Should we include external framework or language-level research?**
   * *Resolution*: No. Locally defined architecture principles in [docs/coding_standards/ARCHITECTURE_PRINCIPLES.md](file:///c:/temp/pgmcp/docs/coding_standards/ARCHITECTURE_PRINCIPLES.md) are fully sufficient.

---

## Design & Planning Readiness

* No compatibility blockers remain.
* The blast radius has been meticulously mapped to 4 production symbols/files and 27 test code locations.
* The research phase is ready to be closed.

---

## Related Documentation

* [docs/coding_standards/ARCHITECTURE_PRINCIPLES.md](file:///c:/temp/pgmcp/docs/coding_standards/ARCHITECTURE_PRINCIPLES.md)
* [docs/coding_standards/DOCUMENTATION_STANDARD.md](file:///c:/temp/pgmcp/docs/coding_standards/DOCUMENTATION_STANDARD.md)
* [docs/reference/mcp/config-loading-architecture.md](file:///c:/temp/pgmcp/docs/reference/mcp/config-loading-architecture.md)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-06-07 | Agent | Initial draft with evidence nucleus |
| 0.2 | 2026-06-09 | Agent | Meticulous blast radius mapping, resolved strategy constraints, and finalized research details. |
