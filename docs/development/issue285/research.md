<!-- docs\development\issue285\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-07T20:39Z updated= -->
# Research: Separate MCPServer composition root from runtime dispatch (Issue #285)

**Status:** APPROVED  
**Version:** 0.1  
**Last Updated:** 2026-06-07

---

## Purpose

Produce a research nucleus suitable for drafting the formal research document following DOCUMENTATION_STANDARD.md

## Scope

**In Scope:**
Repository-local analysis limited to files under the workspace (mcp_server, tests, docs).

**Out of Scope:**
External consumer behavior outside repository, web searches, or third-party integrations beyond code inspections.

## Prerequisites

Read these first:
1. Read docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
2. Read docs/coding_standards/DOCUMENTATION_STANDARD.md
3. Familiarity with Python packaging and DI patterns
---

## Problem Statement

MCPServer mixes composition (config loading, manager and tool instantiation) with runtime dispatch. This research identifies the blast radius, preservation goals, candidate seams, and constraints for extracting a composition root (ServerBootstrapper) while preserving runtime behavior.

## Research Goals

- Map current responsibilities and coupling in `mcp_server/server.py`
- Identify risky boundaries and affected tests/fixtures
- Propose candidate seams for extraction without committing to a migration strategy
- Collect repo-only evidence to support planning

---

## Background

Observed SRP violation in MCPServer during QA review of issue #283. The server `__init__` contains large composition logic and tool registration.

---

## Findings (evidence-backed)

Summary:
- `MCPServer` is the active composition root: it constructs the config loader, loads ~14 config objects, instantiates state repositories and ~13 managers, registers ~30 tools and resources, then installs the runtime handlers. The bulk of composition lives inside `MCPServer.__init__`.
- Test suites instantiate `MCPServer()` directly in many unit and integration tests; they therefore depend on the composition side-effect of `__init__`.
- There are no `backend` imports inside `mcp_server/` (the server is isolated from the old ST3 backend). Backend tests and baselines still import `backend.*` but are separate test groups.

Concrete evidence (file → snippet):

- MCPServer composition root
  - [mcp_server/server.py](mcp_server/server.py#L136)

  ```py
  class MCPServer:
      def __init__(self, settings: Settings | None = None) -> None:
          settings = settings or Settings.from_env()
          # setup logging, template registry
          config_loader = ConfigLoader(config_root=config_root)
          git_config = config_loader.load_git_config()
          workflow_config = config_loader.load_workflow_config()
          # ... loads ~14 configs

          # managers
          self.git_manager = GitManager(git_config=git_config, workphases_config=workphases_config)
          self._state_repository = FileStateRepository(state_file=server_root / "state.json")
          self.project_manager = ProjectManager(...)
          self.phase_state_engine = PhaseStateEngine(...)

          # tools (core + conditional GitHub tools)
          self.tools = [CreateBranchTool(manager=self.git_manager), GitStatusTool(...), ...]
          if github_token:
              self.tools.extend([CreateIssueTool(...), SubmitPRTool(...), MergePRTool(...), ...])

          self.setup_handlers()
  ```

- Tests that instantiate MCPServer (representative list)
  - [tests/mcp_server/unit/test_server.py](tests/mcp_server/unit/test_server.py) — multiple `server = MCPServer()` uses and tests validating tool registration, call dispatch and logging. See test helpers that patch `Settings`.
  - [tests/mcp_server/unit/tools/test_cycle_tools.py](tests/mcp_server/unit/tools/test_cycle_tools.py) — unit tests create `MCPServer()` to test cycle tool wrappers.
  - [tests/mcp_server/unit/server/test_validate_tool_arguments.py](tests/mcp_server/unit/server/test_validate_tool_arguments.py) — fixture returns `MCPServer()` for validation path tests.
  - [tests/mcp_server/integration/mcp_server/conftest.py](tests/mcp_server/integration/mcp_server/conftest.py) — integration fixture yields `MCPServer(settings=settings)` with GitHub adapter patched.

  Example snippet (integration fixture):
  ```py
  @pytest.fixture
  def server() -> Generator[MCPServer, None, None]:
      with patch("mcp_server.managers.github_manager.GitHubAdapter") as mock_adapter_class:
          settings = Settings(server=ServerSettings())
          yield MCPServer(settings=settings)
  ```

- Test support and factories (used by many unit tests), centralizing composition helpers
  - [tests/mcp_server/test_support.py](tests/mcp_server/test_support.py)
    - contains `make_config_loader`, `make_git_manager`, `make_project_manager`, `make_phase_state_engine` helper factories.
    - These factories duplicate some composition logic and are tightly coupled to the ConfigLoader and manager constructors.

- Packaging / test discovery
  - [pyproject.toml](pyproject.toml)

  ```toml
  [tool.setuptools.packages.find]
  where = ["."]
  include = ["backend*", "tests*", "mcp_server*"]

  [tool.setuptools.package-data]
  mcp_server = ["scaffolding/templates/**/*"]

  [tool.pytest.ini_options]
  pythonpath = ["."]
  testpaths = ["tests/mcp_server"]
  ```

- No module-level import-time side-effects found in `mcp_server/` (ConfigLoader and Settings expose constructors / `from_env()` classmethod used at runtime instead of module import-time loading). Example: `ConfigLoader` is instantiated inside `MCPServer.__init__`, not at module import.

- Backend imports (sanity check)
  - Repository grep confirms backend tests and baselines import `backend.*` (e.g. `tests/baselines/baseline_worker.py`), but `mcp_server/` contains no `backend` imports. This means server extraction is not blocked by direct coupling to backend.

---

## Candidate Seams (nucleus — options, not decisions)

The goal of a candidate seam is to separate composition from dispatch without changing external behavior. The following seams are viable and low-risk when implemented incrementally.

1. ServerBootstrapper (recommended primary seam)
   - New class `mcp_server.bootstrap.ServerBootstrapper` that encapsulates the composition logic currently in `MCPServer.__init__` with four explicit methods:
     - `build_config_layer()` → loads the 14 config objects and returns an immutable `ConfigLayer` dataclass
     - `build_manager_graph(config_layer)` → instantiates managers and state repositories, returns `ManagerGraph` dataclass
     - `build_tool_registry(graph, config_layer)` → creates the tools list (conditional GitHub tools included)
     - `build_resource_registry(settings)` → returns resource instances
   - Rationale: isolates DI, makes composition testable, and keeps `MCPServer` focused on handlers/dispatch.

2. ConfigLayer dataclass
   - Make an explicit `ConfigLayer` value object that holds the loaded config snapshots. Pass this object between bootstrap methods and into tests.

3. ManagerGraph dataclass
   - A sealed container for instantiated managers to prevent ad-hoc late instantiation.

4. Minimal runtime adapter in `MCPServer`
   - `MCPServer` becomes the runtime dispatcher that accepts a `ManagerGraph` + `tools` + `resources` and calls `setup_handlers()`; its `__init__` becomes a short adapter.

---

## Risky Boundaries & Blast Radius

### Blast radius by layer

| Layer | Likely impact | Evidence | Risk |
|---|---|---|---|
| Composition root | `mcp_server/server.py` constructor, handler setup, tool/resource registration | `MCPServer.__init__` currently loads config, builds managers, registers tools, then calls `setup_handlers()` | High |
| Direct server tests | Unit tests that create `MCPServer()` to inspect tool registration or dispatch hooks | [tests/mcp_server/unit/test_server.py](tests/mcp_server/unit/test_server.py), [tests/mcp_server/unit/server/test_validate_tool_arguments.py](tests/mcp_server/unit/server/test_validate_tool_arguments.py), [tests/mcp_server/unit/tools/test_cycle_tools.py](tests/mcp_server/unit/tools/test_cycle_tools.py) | High |
| Integration fixtures | Shared fixtures that yield a real `MCPServer(settings=...)` | [tests/mcp_server/integration/mcp_server/conftest.py](tests/mcp_server/integration/mcp_server/conftest.py) | High |
| Shared helpers | Factory helpers that duplicate composition decisions | [tests/mcp_server/test_support.py](tests/mcp_server/test_support.py) | Medium |
| Config and packaging | package discovery and test discovery assumptions | [pyproject.toml](pyproject.toml) | Medium |

### Specific behaviors at risk

- Tests that assert tool registration order or tool presence/absence based on GitHub token.
- Tests that rely on a single shared `FileStateRepository` instance being reused across resolver, mutator, engine, and enforcement flows.
- Any code paths that patch manager classes at import points to prevent real network or filesystem access.
- Constructor ordering between `ProjectManager`, `PhaseStateEngine`, `WorkflowStatusResolver`, `WorkflowGateRunner`, and `EnforcementRunner`.

### Why the test blast radius is bounded

- The repo's `mcp_server/` package does not import `backend`, so there is no cross-era ST3 dependency to unwind in this refactor.
- The biggest pressure point is not the total number of tests but the shared fixtures/helpers they call. That means a small number of helper changes can unlock a large number of suites.
- The refactor can stay localized if the extraction preserves the current public `MCPServer` surface until implementation chooses to move the call sites.

---

## Approved Strategy

- **Boundary / preservation scope:** Server composition boundary inside `mcp_server/server.py` and repo-local test consumers of `MCPServer`.
- **Selected strategy:** clean break.
- **Rationale:** The project has not released the phase-gate MCP server yet, so there are no external users to preserve compatibility for. The desired outcome is to remove composition responsibility from `MCPServer` rather than maintain a bridge layer.
- **Constraints for later phases:** Do not add compatibility shims, deprecation layers, or temporary parallel composition paths. Preserve observable behavior only where repo tests assert it; treat constructor and helper restructuring as fair game.

## Open Questions (prioritized)

1. Which test helpers should move with the composition extraction versus remain as thin test-only factories?
2. Do any server tests rely on construction side-effects that should be recast as explicit bootstrap assertions in design?
3. Is there any additional repo-local behavior that should be treated as stable despite the clean break policy?

---

## Design Readiness

- No compat blocker remains for design.
- The remaining questions are implementation-shaping, not policy-shaping.
- Design can now focus on how to split the composition root, not whether a compatibility bridge is needed.

---

## Related Documentation
- docs/development/issue283/design-ready-phase-enforcement.md
- docs/architecture/03_tool_layer.md
- docs/reference/mcp/config-loading-architecture.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-06-07 | Agent | Initial draft with evidence nucleus |
