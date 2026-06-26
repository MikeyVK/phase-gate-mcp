# Resolve Decorator Pipeline Technical Debt — Research Document

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-25  

---

## 1. Problem Statement

The decorator pipeline refactoring left behind technical debt in the form of hardcoded config-like registries, duplicated cache key normalizations, circular import bypasses via inline imports, and retired files. This document maps these issues, defines their architectural boundaries, and assesses their refactoring blast radius.

---

## 2. Research Goals

- Map all OCP/Config-First violations (hardcoded classifications and schemas).
- Define clean architectural boundaries for cache key normalization.
- Analyze circular dependencies in bootstrapping.
- Outline the cleanup of obsolete files.
- Document the deferred scope in detail for follow-up implementation.

---

## 3. Findings

### Item 1: Hardcoded Configuration & OCP Violations

A total of 8 hardcoded configuration and OCP violations were mapped across the codebase:

1. **Tool Classifications in `TextPresenter`**
   - *Location:* [text_presenter.py:110-141](file:///c:/temp/pgmcp/mcp_server/presenters/text_presenter.py#L110-L141)
   - *Problem:* Mappings of tool names to presentation categories (`mutation`, `bootstrap`) are hardcoded.
   - *Boundary:* Presentation Layer.
   - *Refactor Implications & Blast Radius:* Low. Move to `presentation.yaml` and load via `PresentationConfig`.

2. **Hardcoded V2-Artifact Context Registry**
   - *Location:* [artifact_manager.py:43-67](file:///c:/temp/pgmcp/mcp_server/managers/artifact_manager.py#L43-L67) (`_v2_context_registry`)
   - *Problem:* Static dictionary mapping artifact types to Context schema classes.
   - *Boundary:* Scaffolding Layer.
   - *Refactor Implications & Blast Radius:* Medium. Move to `artifacts.yaml` by adding `context_class` to `ArtifactDefinition`.

3. **Hardcoded Action Types for Tool Exemptions**
   - *Location:* [enforcement_config.py:20](file:///c:/temp/pgmcp/mcp_server/config/schemas/enforcement_config.py#L20) (`_EXEMPT_TOOLS_ALLOWED_TYPES`)
   - *Problem:* Hardcoded `frozenset` limits tool exemptions to `"check_context_loaded"`.
   - *Boundary:* Policy Enforcement Config.
   - *Refactor Implications & Blast Radius:* Low. Make exemption capability validation dynamic or property-based.

4. **Hardcoded Known Enforcement Categories**
   - *Location:* [enforcement_runner.py:34](file:///c:/temp/pgmcp/mcp_server/managers/enforcement_runner.py#L34) (`KNOWN_TOOL_CATEGORIES`)
   - *Problem:* Hardcoded `frozenset({"branch_mutating"})` restricts valid categories.
   - *Boundary:* Policy Enforcement Runner.
   - *Refactor Implications & Blast Radius:* Low. Validate category names dynamically against config rules.

5. **Static Tool Category Attributes on Tool Classes**
   - *Location:* Class variables `tool_category` and `presentation_category` declared statically in tool subclasses across [mcp_server/tools/](file:///c:/temp/pgmcp/mcp_server/tools/).
   - *Problem:* Categorization is statically defined on tools, distributing classification metadata.
   - *Boundary:* Tool Execution Layer vs. Configuration.
   - *Refactor Implications & Blast Radius:* Medium/High. Remove class variables from tools and map them dynamically in `enforcement.yaml` and `presentation.yaml`.

6. **Hardcoded Label Category Regex Pattern**
   - *Location:* [label_config.py:99](file:///c:/temp/pgmcp/mcp_server/config/schemas/label_config.py#L99) (`pattern_str`)
   - *Problem:* Hardcoded label category prefixes.
   - *Boundary:* Label Config.
   - *Refactor Implications & Blast Radius:* Low. Generate validation patterns dynamically from categories defined in `labels.yaml`.

7. **Hardcoded Phase Keys in `project_tools.py`**
   - *Location:* [project_tools.py:515-524](file:///c:/temp/pgmcp/mcp_server/tools/project_tools.py#L515-L524) and [project_tools.py:657-666](file:///c:/temp/pgmcp/mcp_server/tools/project_tools.py#L657-L666)
   - *Problem:* Hardcoded phase name lists used to count deliverables.
   - *Boundary:* Project/Planning Tool Layer.
   - *Refactor Implications & Blast Radius:* Low. Query phase keys dynamically from `WorkphasesConfig`.

8. **Obsolete `_known_phase_keys` Set**
   - *Location:* [project_manager.py:40-42](file:///c:/temp/pgmcp/mcp_server/managers/project_manager.py#L40-L42) (`_known_phase_keys`)
   - *Problem:* Unused hardcoded set (dead code).
   - *Boundary:* Project Manager.
   - *Refactor Implications & Blast Radius:* Zero. Safe to delete.

---

### Item 2: Cache Normalization Boundaries

To resolve the duplicate cache normalization logic, we establish a strict boundary separation:

1. **State Layer (`ResponseCache`):**
   - Agnostic to URI schemes and transport protocols.
   - Only processes and stores outputs using raw `run_id` strings (UUID hex format).
   - Remove all manual URI parsing or checks (e.g., `pgmcp://cache/runs/`).

2. **API/Resource Boundary (`CachedResponseResource`):**
   - Translates between external URI representations (`pgmcp://cache/runs/{run_id}`) and internal raw `run_id` strings.
   - Performs key normalizations (handling hyphenated vs. non-hyphenated UUIDs) at the point of entry before querying the cache.

3. **Presentation Layer (`TextPresenter`):**
   - Converts raw `run_id` to its URI representation for user-facing markdown output.

---

### Item 3: Bootstrapping and Process-Startpoint Dependencies (Circular Dependencies)

- *Problem Analysis:* There is a circular dependency in the dependency graph between the initialization layer (`bootstrap.py`) and the runtime layer (`server.py`). This circular dependency is caused by mixing the **Process-Startpoint Responsibility** (the entrypoint) with the **Server Runtime Responsibility** (`MCPServer`) within the same module. Inline imports were introduced to bypass circular dependency errors.
- *Architectural Boundary & Constraints:*
  1. **Server Runtime Boundary:** The definition of `MCPServer` must be completely independent of the bootstrapping process. This layer must have zero imports or knowledge of the initialization layer.
  2. **Bootstrapping Boundary:** The bootstrapper acts as the *assembler*. This layer may statically depend on the Server Runtime layer to construct the server instance.
  3. **Process Entrypoint Boundary:** The process startup trigger (the runner) must reside in a dedicated, isolated *leaf-node* module (a module never imported by any other module in the codebase).
- *Refactor Implications & Blast Radius:* Low. Physical separation of the process startup logic from runtime definitions allows all inline imports in `bootstrap.py` to be converted to module-level static imports.

---

### Item 4: Retired Files Cleanup

- *Problem Analysis:* The file [base.py](file:///c:/temp/pgmcp/mcp_server/tools/base.py) is empty and retired but remains in the repository.
- *Boundary:* Tool execution layer files.
- *Refactor Implications & Blast Radius:* Very Low (Metadata only). 
  1. Physically delete `mcp_server/tools/base.py`.
  2. Remove references to `mcp_server.tools.base` in the `@dependencies` header comments of [test_pr_status_lockdown.py:15](file:///c:/temp/pgmcp/tests/mcp_server/integration/test_pr_status_lockdown.py#L15) and [test_submit_pr_tool.py:5](file:///c:/temp/pgmcp/tests/mcp_server/unit/tools/test_submit_pr_tool.py#L5).

---

## 4. Expected Results & Accepted Strategy

### Accepted Strategy per Boundary
- **Preserve Compatibility (External API/Protocols):** 100% backward compatibility of the MCP JSON-RPC protocol and the URI structure (`pgmcp://cache/runs/{run_id}`). External clients must observe no differences in resource retrieval or presented outputs.
- **Clean Break (Internal Python Structure):** 
  - Migrate internal hardcoded schemas and classifications to configuration-driven files (`presentation.yaml`, `artifacts.yaml`, `enforcement.yaml`, `labels.yaml`).
  - Move the process entrypoint `main()` from `server.py` to a dedicated `__main__.py` leaf-node module, allowing static imports in `bootstrap.py`.
  - Strip the `ResponseCache` of URI-parsing logic and enforce raw key storage.
  - Delete retired `tools/base.py` and clean dependency comments in tests.

### Expected Results per Boundary
- **Config-First & OCP (Item 1):** Adding new tools, categories, artifact types, or label categories requires no code modifications in Python. All 8 mapped config violations are resolved.
- **Cache Normalization (Item 2):** URI-to-ID conversion is fully isolated to the `CachedResponseResource` boundary. The cache remains completely agnostic of the URI scheme.
- **Circular Imports (Item 3):** No inline imports in `bootstrap.py`. Circular dependencies are completely eliminated.
- **Retired Files (Item 4):** `tools/base.py` is removed, and test suites build and execute without errors.

---

## 5. Deferred Work Scope (Out of Scope for #411)

To limit regression risk and narrow the blast radius of issue #411, the following items are deferred to a dedicated follow-up issue:

1. **Redesign of Error DTOs & Removal of `error_message` from `BaseToolOutput`**
   - *Problem:* `BaseToolOutput` contains an optional `error_message` field, which mixes success and failure concerns in a single model.
   - *Future Action:* 
     - Separate success and failure concerns: successful outputs inherit from `BaseToolOutput` (which will no longer contain `error_message`), and failed outputs inherit from a new `BaseErrorOutput` (without a `success` field).
     - Update routing in `server.py` and `text_presenter.py` to dispatch based on `isinstance(result, BaseErrorOutput)`.
     - Update return types of all tool execution methods to allow either successful outputs or error DTOs.
   - *Blast Radius:* High. Affects almost all tool subclasses and presenter templates.

2. **Validation Resource Schema Generation Refactoring**
   - *Problem:* The validation resource schema generation (`schema://validation`) is generated inside `server.py` instead of being handled by a presenter.
   - *Future Action:* Move the generation of `schema://validation` out of `server.py` and delegate it to `IPresenter`.
   - *Blast Radius:* Low/Medium. Affects `server.py` and the presentation interface.

3. **Fallback Warnings & Warnings Refactoring**
   - *Problem:* Tool warnings (such as fallback warnings in `discovery_tools.py`) are hardcoded in the tool classes rather than being templates in `presentation.yaml`.
   - *Future Action:* Move fallback warnings and warnings presentation to `TextPresenter` and configure warning templates dynamically in `presentation.yaml`.
   - *Blast Radius:* Low. Affects discovery tools and `TextPresenter`.

---

## 6. References

- [ARCHITECTURE_PRINCIPLES.md](file:///c:/temp/pgmcp/docs/coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [presentation.yaml](file:///c:/temp/pgmcp/.phase-gate/config/presentation.yaml)
- [artifacts.yaml](file:///c:/temp/pgmcp/.phase-gate/config/artifacts.yaml)
