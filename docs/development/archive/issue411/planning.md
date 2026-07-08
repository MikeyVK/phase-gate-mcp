# Resolve Decorator Pipeline Technical Debt - Planning Document

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-25

---

## Summary

Plan to resolve technical debt and configuration violations remaining from the decorator pipeline refactoring without test bloat.

---

## Preservation Goals

- **External Protocol Compatibility:** Preserve 100% backward compatibility of the MCP JSON-RPC protocol. External clients must observe no change in behavior or output format.
- **Cache URI Scheme:** Preserve the external cache URI scheme (`pgmcp://cache/runs/{run_id}`).
- **Zero Redesign:** No new dynamic classifications, custom action types, or additional features are to be introduced.

---

## Constraints & Quality Expectations

- **Test-Suite Impact:** Avoid any test bloat. Unit/integration tests must check behavior/interfaces and must NOT read internal configuration files (e.g. YAML files) directly. Mocks/fixtures that use cache/run IDs must be updated to use valid hex run_ids rather than reading configs.
- **Typing Obligations:** Compliance with the [Type Checking Playbook](file:///c:/temp/pgmcp/docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md) is mandatory. Introduce a Pydantic-enforced custom type `HexUUID` using `Annotated[str, StringConstraints(pattern=r"^[a-f0-9]{32}$")]`.
- **Quality-Gate Expectations:** Run `run_quality_gates` before phase transitions and before PR creation. Code must achieve a Pylint score of 10.00/10 and type checking must pass without errors.
- **Cleanup Expectations:** Clean up all static variables (`tool_category`, `presentation_category`), unused imports, and retired files.
- **Approved Strategy Execution Constraints:** Adhere strictly to the Approved Strategy defined in the research phase.

---

## TDD Cycles

### Cycle 1: C_BOOTSTRAP.1

**Goal:** Isolate the bootstrapping process entrypoint to __main__.py to eliminate circular imports. Ensure all imports in bootstrap.py are static.

**Deliverables:**
- **[D1.1]** Create [__main__.py](file:///c:/temp/pgmcp/mcp_server/__main__.py) with process startup `main()`.
- **[D1.2]** Clean up inline imports in [bootstrap.py](file:///c:/temp/pgmcp/mcp_server/bootstrap.py) and convert to module-level static imports.

**Tests:**
- Verify all existing test suites run without circular import warnings or bypass inline imports. No new tests are added.

**Success Criteria:**
- MCPServer startup and initialization runs without using inline imports in bootstrap.py.

---

### Cycle 2: C_CACHE.2

**Goal:** Unify cache key normalization at the CachedResponseResource API boundary and enforce strict HexUUID keys in ResponseCache.

**Deliverables:**
- **[D2.1]** Define custom Pydantic `HexUUID` validation type and apply to `CachePublication` `run_id`.
- **[D2.2]** Remove URI parsing/normalizing logic from `ResponseCache` and enforce `HexUUID` keys.
- **[D2.3]** Implement URI validation and extraction at `CachedResponseResource` API boundary.
- **[D2.4]** Update tests to use valid hex run_ids rather than reading configs.

**Tests:**
- Verify `ResponseCache` unit tests enforce 32-char hex UUID `run_id`. Update test mocks/fixtures to use valid hex values.
- Verify `CachedResponseResource` unit tests validate and normalize cache keys correctly.

**Success Criteria:**
- `ResponseCache` is completely agnostic of URI schemes.
- `CachedResponseResource` handles and normalizes URI schemes and rejects invalid key formats.

---

### Cycle 3: C_PRESENTER.3

**Goal:** Make TextPresenter classifications and emojis fully dynamic via presentation.yaml. Remove static category class attributes.

**Deliverables:**
- **[D3.1]** Add category and emojis properties to presentation config schema and configure [presentation.yaml](file:///c:/temp/pgmcp/.phase-gate/config/presentation.yaml).
- **[D3.2]** Refactor [text_presenter.py](file:///c:/temp/pgmcp/mcp_server/presenters/text_presenter.py) to look up category emojis dynamically from config.
- **[D3.3]** Remove static category class variables from tool classes.

**Tests:**
- Verify presenters tests render correctly using configured category emojis without hardcoded class attributes or text_presenter.py classifications.

**Success Criteria:**
- Presentation categories map to emojis dynamically based on configuration.
- Static presentation_category and tool_category attributes are removed from tool classes.

---

### Cycle 4: C_ENFORCEMENT.4

**Goal:** Refactor policy enforcement to read categories dynamically from enforcement.yaml. Remove hardcoded allowed types.

**Deliverables:**
- **[D4.1]** Add categories property to `EnforcementConfig` and configure [enforcement.yaml](file:///c:/temp/pgmcp/.phase-gate/config/enforcement.yaml).
- **[D4.2]** Update `EnforcementRunner` to check category rules dynamically.
- **[D4.3]** Remove hardcoded exempt tool action types from `enforcement_config.py`.

**Tests:**
- Verify enforcement tests function correctly using dynamic categories from enforcement.yaml.
- Verify tool exemption validation works dynamically without hardcoded allowed types.

**Success Criteria:**
- Tool categories for policy enforcement are mapped in enforcement.yaml.
- Tool subclass files contain zero static enforcement category variables.

---

### Cycle 5: C_SCAFFOLD.5

**Goal:** De-duplicate and externalize context schemas in artifact manager using context_class in artifacts.yaml. Rename v2 occurrences.

**Deliverables:**
- **[D5.1]** Add `context_class` to `ArtifactDefinition` and configure [artifacts.yaml](file:///c:/temp/pgmcp/.phase-gate/config/artifacts.yaml).
- **[D5.2]** Refactor `ArtifactManager` to resolve context classes dynamically and remove v2 registry.
- **[D5.3]** Clean up and rename legacy v2 variables and strings to neutral terminology.

**Tests:**
- Verify scaffolding tests run successfully using context_class configuration.

**Success Criteria:**
- All occurrences of `_v2_context_registry` are replaced with dynamic artifacts.yaml configuration.
- All 'v2' naming is replaced with neutral schema-based naming.

---

### Cycle 6: C_LABELS_PHASES.6

**Goal:** Clean up label validation loophole and query workphase keys dynamically. Remove obsolete phase keys set.

**Deliverables:**
- **[D6.1]** Remove legacy 4th fallback validation step from `label_config.py`.
- **[D6.2]** Update `project_tools.py` to query phase keys dynamically from `WorkphasesConfig`.
- **[D6.3]** Delete obsolete `_known_phase_keys` set from `project_manager.py`.

**Tests:**
- Verify label validator tests function correctly relying only on configuration-based rules.
- Verify project_tools tests count deliverables dynamically from WorkphasesConfig.

**Success Criteria:**
- Legacy 4th step regex pattern check is removed from label validation.
- Phase name lists are dynamically queried from WorkphasesConfig.

---

### Cycle 7: C_CLEANUP.7

**Goal:** Delete empty base.py tool and clean up comments/references. Clean up obsolete test remnants.

**Deliverables:**
- **[D7.1]** Delete obsolete [base.py](file:///c:/temp/pgmcp/mcp_server/tools/base.py).
- **[D7.2]** Remove references to `mcp_server.tools.base` in code and test comments.

**Tests:**
- Run full quality gates and verify no references to base.py or dead test code remain.

**Success Criteria:**
- mcp_server/tools/base.py is deleted.
- All references/comments to it are removed. Obsolete tests cleaned up.

---

## Related Documentation

- [RESEARCH_DOCUMENT](file:///c:/temp/pgmcp/docs/development/issue411/research.md)
- [DESIGN_DOCUMENT](file:///c:/temp/pgmcp/docs/development/issue411/design.md)
- [ARCHITECTURE_PRINCIPLES](file:///c:/temp/pgmcp/docs/coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [TYPE_CHECKING_PLAYBOOK](file:///c:/temp/pgmcp/docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-25 | Agent | Initial draft containing preservation goals, constraints, dynamic cycles, and synced deliverables |
