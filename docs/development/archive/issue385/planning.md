<!-- docs\development\issue385\planning.md -->
<!-- template=planning version=130ac5ea created=2026-07-03T19:44Z updated= -->
# Planning: Package Identity and Init Bootstrap

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-07-03

---

## Summary

Planning the implementation for Issue #385. The goal is to rename the config root to .pgmcp, introduce Settings properties for path coherence, eliminate template_config.py and legacy loader.py fallbacks, and implement the pgmcp --init flat-copy initialization, while migrating 50+ hardcoded test paths cleanly.

### Core Obligations
- **Approved Strategy:** `Settings` must become the single source of truth for all paths. Fallback probes in loaders/scaffolders must be eliminated (Explicit over Implicit).
- **Quality Gates:** Every cycle must pass `run_quality_gates` (Ruff 10.00/10 + Mypy pass) before being marked complete.
- **Typing:** Strict static typing is required for the new properties in `Settings`. No generic `Any` types allowed.

---

## TDD Cycles


### Cycle 1: C_TEST_DECOUPLE

**Goal:** Prepare the test suite for the directory name change without altering any production behavior.

**Tests:**
- tests/mcp_server/test_support.py
- 50+ test files containing .phase-gate

**Success Criteria:**
- Test files use get_default_server_root() instead of hardcoded strings.
- All tests remain green.
- Static analysis passes.



### Cycle 2: C_ARCH_FOUNDATION

**Goal:** Implement new path resolutions in Settings, package the defaults as assets, and eliminate template_config.py.

**Tests:**
- tests/mcp_server/unit/config/test_template_config.py (deleted)

**Success Criteria:**
- mcp_server/assets/ is populated with config and templates.
- server_root_dir defaults to .pgmcp in Settings.
- resolved_server_root, resolved_config_root, resolved_template_root are added to Settings.
- template_config.py is deleted and consumers use Settings DI.
- get_default_server_root() is updated to .pgmcp.



### Cycle 3: C_LOADER_PROBES

**Goal:** Rip out legacy fallback magic from loader.py and force strict DI.

**Tests:**
- test_loader.py

**Success Criteria:**
- _probe_candidates is removed from loader.py.
- Test helpers point to mcp_server/assets/config as fallback.



### Cycle 4: C_CLI_INIT

**Goal:** Expose the initialization feature and properly bundle the package.

**Tests:**
- test_cli.py

**Success Criteria:**
- pgmcp --init command flat-copies assets to workspace_root / .pgmcp.
- CLI gracefully aborts if .pgmcp already exists.
- CLI fails-fast with an explicit error asking the user to run --init if .pgmcp is missing and --init is not provided.
- pyproject.toml registers assets package data and pgmcp script.



### Cycle 5: C_WORKSPACE_MIGRATION

**Goal:** Migrate the project's own configuration folder to the new standard.

**Tests:**
- None

**Success Criteria:**
- The repository's .phase-gate/ directory is renamed to .pgmcp/.
- The MCP server is restarted to pick up the new state directory.
- CI/CD and local VS Code configurations are updated if they contain hardcoded references.



### Cycle 6: C_DEBT_ELIMINATION

**Goal:** Eliminate all transitional compatibility debt, settings fallbacks, and proxy/test support migration bridges.

**Tests:**
- tests/mcp_server/unit/config/test_settings.py
- tests/mcp_server/test_support.py

**Success Criteria:**
- The implicit disk-probing fallback to package assets is removed from `resolved_config_root` and `resolved_template_root` properties in `settings.py`.
- The transitional fallback bridge in `settings.py` and `proxy.py` (auto-redirecting `.phase-gate` to `.pgmcp`) is removed.
- The legacy fallback logic in `test_support.py` (`get_default_server_root()`) is removed; it strictly returns `.pgmcp` (or environment overrides).
- All 2,870+ tests remain green.
## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-03 | Agent | Initial draft |
| 1.1 | 2026-07-05 | Agent | Add Cycle 6 for debt elimination |
