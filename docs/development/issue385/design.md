<!-- docs\development\issue385\design.md -->
<!-- template=design version=5827e841 created=2026-07-03T18:56Z updated= -->
# Design: Path Coherence and Pgmcp Init Bootstrap

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-07-03

---

## 1. Context & Requirements

### 1.1. Problem Statement

The current configuration paths (config_root, template_root) are disconnected from the settings layer and fall back to hardcoded .phase-gate paths. We need to bundle default assets into a flat folder inside the pip package and copy them cleanly into .pgmcp using pgmcp --init, while enforcing coherent Dependency Injection across the codebase for test stability.

### 1.2. Requirements

**Functional:**
- [ ] Add pgmcp entry point to pyproject.toml.
- [ ] Implement pgmcp --init in mcp_server/cli.py to copy a flat assets/ folder to Settings().server.resolved_server_root.
- [ ] Bundle mcp_server/assets in the pip package via pyproject.toml package-data.
- [ ] Resolve all path settings strictly through Settings without relying on magic TEMPLATE_ROOT env vars or probe fallbacks in loaders.

**Non-Functional:**
- [ ] Explicit over implicit: Server crashes gracefully before bootstrap if .pgmcp is missing and --init is absent.
- [ ] Backward compatibility for Settings: Must still allow environment overrides for specific paths.
- [ ] Test suite integrity: 50+ test files must use dynamic injection of the root directory instead of .phase-gate string replacement.

### 1.3. Constraints

None
---

## 2. Design Options

### 2.1. Option A: DI Refactor with Settings as Source of Truth

Add resolved path properties to Settings and inject them downstream.

**Pros:**
- ✅ Architecturally pure
- ✅ Solves test tech-debt
- ✅ Eliminates hardcoding

**Cons:**
- ❌ Requires invasive changes in constructor signatures

### 2.2. Option B: Patch legacy probes and replace test strings

Keep `template_config.py` and `loader.py` fallbacks, patch them to check `.pgmcp`, and use a massive string replacement in the tests for `.phase-gate` -> `.pgmcp`.

**Pros:**
- ✅ Faster to implement
- ✅ No constructor signature changes

**Cons:**
- ❌ Violates ARCHITECTURE_PRINCIPLES.md (Implicit over Explicit)
- ❌ Does not resolve the test tech-debt (strings are just renamed)
---

## 3. Chosen Design

**Decision:** Consolidate all path resolution inside Settings via properties (resolved_config_root, resolved_template_root). Remove legacy fallback probes in loaders and scaffolders. Inject paths down the stack. Implement flat-folder copy logic in cli.py.

**Rationale:** This completely eliminates the need for string hardcoding across the codebase, ensuring that changing the config root via environment variable cleanly affects the entire application tree, including templates and config files, while making the --init logic trivial.

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Remove template_config.py and loader fallbacks; enforce Settings DI. | Eliminates implicit/hardcoded path probing, adhering strictly to Explicit over Implicit principles. |

### 3.2. Concrete Interface Contracts

**Settings Path Properties (`mcp_server/config/settings.py`):**
```python
class ServerSettings(BaseModel):
    # existing fields...
    @computed_field
    @property
    def resolved_server_root(self) -> Path:
        return Path(self.workspace_root) / self.server_root_dir

    @computed_field
    @property
    def resolved_config_root(self) -> Path:
        return Path(self.config_root) if self.config_root else self.resolved_server_root / "config"

    @computed_field
    @property
    def resolved_template_root(self) -> Path:
        return self.resolved_server_root / "templates"
```

**CLI Initialization (`mcp_server/cli.py`):**
```python
def main(settings: Settings | None = None) -> None:
    # After arg parsing:
    # if args.init:
    #     copy mcp_server/assets/* to _settings.server.resolved_server_root
    #     sys.exit(0)
    # if not _settings.server.resolved_server_root.exists():
    #     print("Run pgmcp --init")
    #     sys.exit(1)
```

### 3.3. Test Suite Dependency Injection Strategy

To resolve the 50+ files hardcoding `.phase-gate`, we will expose the default setting in test support and update fixtures:
```python
# tests/mcp_server/test_support.py
from mcp_server.config.settings import Settings
SERVER_ROOT_DIR = Settings().server.server_root_dir

# tests/mcp_server/fixtures/workflow_fixtures.py
def _make_loader() -> ConfigLoader:
    return ConfigLoader(Path(Settings().server.server_root_dir) / "config")
```
This strategy removes string replacements entirely; the test suite dynamically adopts whatever default `server_root_dir` is configured in `Settings` (which will become `.pgmcp`).

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-03 | Agent | Initial draft |