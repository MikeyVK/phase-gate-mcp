# Resolve Decorator Pipeline Technical Debt — Design Document

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-25  

---

## 1. Context & Requirements

### 1.1. Problem Statement

The decorator pipeline refactoring left behind technical debt in the form of hardcoded config-like registries, duplicated cache key normalizations, circular import bypasses via inline imports, and retired files. To adhere to clean architecture principles, we must decouple these dependencies and make metadata configurations fully dynamic.

### 1.2. Requirements

**Functional:**
- [ ] Decouple tool classes from categories.
- [ ] Unify cache key parsing and normalization.
- [ ] Resolve circular bootstrapping imports.
- [ ] Remove `base.py`.

**Non-Functional:**
- [ ] OCP / Config-First compliance.
- [ ] Zero change to external JSON-RPC interface.
- [ ] No inline import workarounds.

### 1.3. Constraints

None.

---

## 2. Design Options

### 2.1. Option A: Status quo

Keep static attributes in Python tools and hardcoded categories in runner/presenter.

**Pros:**
- ✅ Simple to read locally inside a single tool file.

**Cons:**
- ❌ Violates OCP.
- ❌ Violates Config-First.
- ❌ High coupling between layers.

### 2.2. Option B: Config-first dynamic registries (Chosen)

Move all categorizations, context registries, and phase keys to YAML files, parsing them dynamically at runtime.

**Pros:**
- ✅ Adheres to OCP.
- ✅ Enables adding categories without changing Python code.
- ✅ Decouples tools from presentation/enforcement.

**Cons:**
- ❌ Requires parsing configs at startup.

---

## 3. Chosen Design

**Decision:** Transition categories to `presentation.yaml` and `enforcement.yaml`, parse cache URIs at `CachedResponseResource`, separate entrypoint to `__main__.py`.

**Rationale:** Adheres to SOLID principles, keeps core tools stateless and decoupled from transport/presentation layers.

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Tool categories in YAML | Allows tools to remain completely stateless regarding presentation and policy enforcement. |
| Execution entrypoint separation | Moving `main()` to `__main__.py` isolates the bootstrapping orchestration from the `MCPServer` definition, breaking the import loop. |

### 3.2. Detailed Component Design

#### 3.2.1. Presenter Tool Categories
- **Configuration:** 
  - Add `category: str | None = None` to [ToolPresentationConfig](file:///c:/temp/pgmcp/mcp_server/config/schemas/presentation_config.py#L62) in [presentation_config.py](file:///c:/temp/pgmcp/mcp_server/config/schemas/presentation_config.py).
  - Change the `emojis` property in [GlobalPresentationConfig](file:///c:/temp/pgmcp/mcp_server/config/schemas/presentation_config.py#L49) from a static `EmojisConfig` model to a dynamic `dict[str, str]` to allow arbitrary custom categories to map to emoji prefixes.
- **Declaration:** 
  - Define custom category emoji mappings under `global: emojis:` in [presentation.yaml](file:///c:/temp/pgmcp/.phase-gate/config/presentation.yaml) (e.g. `testing: "🧪"`, `quality: "🔍"`, `scaffold: "🏗️"`).
  - Add `category` values for all tools under `tools:` in [presentation.yaml](file:///c:/temp/pgmcp/.phase-gate/config/presentation.yaml). E.g., `create_branch` will have `category: mutation`, `run_tests` will have `category: testing`, and `initialize_project` will have `category: bootstrap`.
- **Parsing:** In [text_presenter.py](file:///c:/temp/pgmcp/mcp_server/presenters/text_presenter.py#L110), retrieve the category via `tool_cfg.category` and fall back to `"query"` if not specified. Retrieve the emoji dynamically via `emojis.get(resolved_cat, emojis.get("success", "✅"))`. Remove the hardcoded classification `if-elif` chain.


#### 3.2.2. Enforcement Tool Categories
- **Configuration:** Add `categories: dict[str, list[str]] = Field(default_factory=dict)` to [EnforcementConfig](file:///c:/temp/pgmcp/mcp_server/config/schemas/enforcement_config.py#L74) in [enforcement_config.py](file:///c:/temp/pgmcp/mcp_server/config/schemas/enforcement_config.py).
- **Declaration:** In [enforcement.yaml](file:///c:/temp/pgmcp/.phase-gate/config/enforcement.yaml), define a `categories:` mapping block:
  ```yaml
  categories:
    branch_mutating:
      - create_branch
      - git_add_or_commit
      ...
  ```
- **Parsing & Validation:**
  - Remove `KNOWN_TOOL_CATEGORIES` from [enforcement_runner.py](file:///c:/temp/pgmcp/mcp_server/managers/enforcement_runner.py#L34).
  - Inside [EnforcementRunner](file:///c:/temp/pgmcp/mcp_server/managers/enforcement_runner.py), check if a tool matches a category rule by looking up the tool name inside the loaded `self._config.categories` dictionary.
  - Dynamically validate category rule target names against the keys defined in `self._config.categories`.

#### 3.2.3. Scaffolding Context Registry (Legacy V2 Naming Cleanup)
- **Configuration:** Add `context_class: str | None = None` to [ArtifactDefinition](file:///c:/temp/pgmcp/mcp_server/config/schemas/artifact_registry_config.py#L66) in [artifact_registry_config.py](file:///c:/temp/pgmcp/mcp_server/config/schemas/artifact_registry_config.py).
- **Declaration:** In [artifacts.yaml](file:///c:/temp/pgmcp/.phase-gate/config/artifacts.yaml), define the `context_class` property for all artifact types (e.g. `context_class: DTOContext` for `dto`).
- **Parsing:** Retrieve the context class name dynamically from `artifact_definition.context_class` inside [artifact_manager.py](file:///c:/temp/pgmcp/mcp_server/managers/artifact_manager.py). Delete the module-level dictionary `_v2_context_registry`.
- **Legacy Cleanup:** Rename all occurrences of `"v2"` in variable names, error messages, and logs inside [artifact_manager.py](file:///c:/temp/pgmcp/mcp_server/managers/artifact_manager.py) to use neutral terminology (e.g., rename `v2_supported_artifacts` to `schema_supported_artifacts`, rename `v2_template_exists` to `schema_template_exists`, and update error message texts accordingly).

#### 3.2.4. Label Validation Categories
- **Parsing:** In [label_config.py](file:///c:/temp/pgmcp/mcp_server/config/schemas/label_config.py#L99), remove the legacy 4th fallback validation step (`pattern_str` regex check) completely. Validation will rely strictly on the first three steps: `freeform_exceptions`, pre-declared `labels`, and `label_patterns` loaded from configuration. This closes the loophole allowing unconfigured categories to bypass validation.

#### 3.2.5. Planning Phase Keys
- **Parsing:** In [project_tools.py](file:///c:/temp/pgmcp/mcp_server/tools/project_tools.py#L515), load the phase keys dynamically from `self.workphases_config.phases.keys()` instead of using a hardcoded list of phase names.

#### 3.2.6. Process Entrypoint Separation
- **Relocation:** Create [__main__.py](file:///c:/temp/pgmcp/mcp_server/__main__.py) as a package entrypoint. Move `main()` and the `if __name__ == "__main__":` block from [server.py](file:///c:/temp/pgmcp/mcp_server/server.py#L250) to `__main__.py`.
- **Parsing:** Statically import `ServerBootstrapper` in `__main__.py`. Statically import `MCPServer` in [bootstrap.py](file:///c:/temp/pgmcp/mcp_server/bootstrap.py#L250) at the module level.

#### 3.2.7. Action Types for Tool Exemptions
- **Parsing:** In [enforcement_config.py](file:///c:/temp/pgmcp/mcp_server/config/schemas/enforcement_config.py), remove the hardcoded `_EXEMPT_TOOLS_ALLOWED_TYPES` set and the validation checks restricting `exempt_tools` to specific action types.

#### 3.2.8. Obsolete Phase Keys Set
- **Cleanup:** In [project_manager.py](file:///c:/temp/pgmcp/mcp_server/managers/project_manager.py#L40-L42), delete the unused `_known_phase_keys` set completely.

#### 3.2.9. Cache Normalization and Key Types
- **Typing:** Introduce a Pydantic-enforced custom type `HexUUID` using `Annotated[str, StringConstraints(pattern=r"^[a-f0-9]{32}$")]`. Update [CachePublication](file:///c:/temp/pgmcp/mcp_server/schemas/cache_publication.py)'s `run_id` to use this hard validation type constraint.
- **Cache Storage:** Ensure `ResponseCache` only accepts and stores keys matching this `HexUUID` type. Remove all legacy URI-splitting or string fallback parsing from `ResponseCache.put`, `get`, and `exists`.
- **API Boundary:** In `CachedResponseResource.read()`, extract the ID from the URI. If it doesn't match the `HexUUID` pattern, reject it. This puts a "hard lock" on the cache key schema, ensuring invalid key formats are blocked at the boundary.
- **Testing:** Update unit/integration tests that mock `run_id` (e.g. `test_presenter.py`, `test_autofix_tool.py`) to use valid 32-character hex UUID values (e.g. `"a" * 32` or `uuid.uuid4().hex`) to comply with this validation schema.

## 4. References

- [ARCHITECTURE_PRINCIPLES.md](file:///c:/temp/pgmcp/docs/coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [research.md](file:///c:/temp/pgmcp/docs/development/issue411/research.md)
