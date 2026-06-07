<!-- docs\development\issue359\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-06T20:05Z updated= -->
# Planning: Fix ServerSettings.version configurability (#359)

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-06-06

---

## Purpose

Define the single implementation cycle required to fix issue #359 within the constraints of the Approved Strategy.

## Scope

**In Scope:**
mcp_server/config/settings.py (ServerSettings class), mcp_config.yaml (operator file), docs/mcp_server/ARCHITECTURE.md (documented YAML example), tests/mcp_server/unit/config/test_settings.py, tests/mcp_server/unit/test_cli.py

**Out of Scope:**
LogSettings, GitHubSettings, Settings — no version-equivalent violation. extra='forbid' on other settings classes. Any refactor beyond the version field.

## Prerequisites

Read these first:
1. Research artifact approved (docs/development/issue359/research.md)
2. Approved Strategy: @computed_field + ConfigDict(extra='forbid') + operator config cleanup
---

## Summary

One TDD cycle: replace ServerSettings.version with @computed_field, add ConfigDict(extra='forbid'), remove version: from mcp_config.yaml and the documented ARCHITECTURE.md example. Fix is isolated to one production class and one test file verification. Corrects two env-dependent test failures.

---

## Dependencies

- Research v1.1 (docs/development/issue359/research.md) — Approved Strategy is the binding input

---

## TDD Cycles


### Cycle 1: C1: @computed_field + extra='forbid' on ServerSettings

**Goal:** Make version a read-only computed property that always returns the installed package version, and make ServerSettings reject any extra fields (including a stale version: key) at construction time.

**Tests:**
- RED — add test_server_settings_rejects_version_kwarg: assert that ServerSettings(version='injected') raises ValidationError (characterizes the defect before fix)
- RED — confirm test_load_from_env and test_cli_version fail when MCP_CONFIG_PATH points to a config file with version: '1.0.0' (regression characterization)
- GREEN — test_server_settings_rejects_version_kwarg now passes (ValidationError raised)
- GREEN — test_load_from_env passes: mock controls version regardless of MCP_CONFIG_PATH
- GREEN — test_cli_version passes: output contains mocked version
- GREEN — test_load_from_yaml: verify no version: key in fixture; update if present
- REFACTOR — run_quality_gates on mcp_server/config/settings.py and affected test files

**Success Criteria:**
- D1: ServerSettings.version is a @computed_field — passing version= to the constructor raises Pydantic ValidationError
- D2: ServerSettings has model_config = ConfigDict(extra='forbid') — any unknown key in constructor raises ValidationError
- D3: _default_server_version() is called via the computed property; importlib.metadata mock in test_settings.py controls the returned value
- D4: test_load_from_env passes via MCP run_tests (no longer affected by MCP_CONFIG_PATH loading mcp_config.yaml)
- D5: test_cli_version passes via MCP run_tests
- D6: test_load_from_yaml fixture verified — version: key absent or removed if present
- D7: version: key removed from docs/mcp_server/ARCHITECTURE.md documented YAML example
- D8: mcp_config.yaml version: key removal documented (operator responsibility; file is in .gitignore)
- D9: All tests in tests/mcp_server/unit/config/test_settings.py and tests/mcp_server/unit/test_cli.py green
- D10: Quality gates pass on changed files (Ruff format, Ruff lint, Pyright, line length)


---

## Risks & Mitigation

- **Risk:** test_load_from_yaml fixture may contain version: key that will raise ValidationError after extra='forbid' is added
  - **Mitigation:** RED phase verifies current fixture contents; fix included in GREEN if needed
- **Risk:** Operator mcp_config.yaml may not be tracked (in .gitignore) — no automated removal possible
  - **Mitigation:** Documented in planning; operator must manually remove version: key; startup ValidationError will surface the issue immediately

---

## Milestones

- C1 GREEN: two previously-failing tests pass via MCP run_tests
- C1 REFACTOR: branch quality gates pass

## Related Documentation
- **[docs/development/issue359/research.md][related-1]**
- **[docs/mcp_server/ARCHITECTURE.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/development/issue359/research.md
[related-2]: docs/mcp_server/ARCHITECTURE.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-06 | Agent | Initial draft |