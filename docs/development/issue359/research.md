<!-- docs\development\issue359\research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-06T19:58Z updated=2026-06-06T20:30Z -->
# Research: ServerSettings.version is not configurable (#359)

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-06-06

---

## Purpose

Establish root cause, affected surface, Approved Strategy, and corrected behavior for issue #359 to serve as binding input for design and planning.

## Scope

**In Scope:**
mcp_server/config/settings.py (ServerSettings, _default_server_version, from_env), mcp_config.yaml, mcp_server/cli.py (version consumer), tests/mcp_server/unit/config/test_settings.py, tests/mcp_server/unit/test_cli.py

**Out of Scope:**
LogSettings, GitHubSettings, Settings — no version-equivalent violation found in those classes. extra='forbid' on classes other than ServerSettings is out of scope for this fix.

## Prerequisites

Read these first:
1. Pydantic v2 computed_field semantics
2. importlib.metadata.version() behavior
3. MCP_CONFIG_PATH environment variable propagation in VS Code subprocess model
---

## Problem Statement

ServerSettings.version is a regular Pydantic field with a default_factory. When MCP_CONFIG_PATH is set in the VS Code environment, Settings.from_env() loads mcp_config.yaml which contains version: '1.0.0'. This YAML value overrides the default_factory, making any importlib.metadata mock in tests irrelevant. Two tests fail consistently when run via MCP run_tests because pytest inherits MCP_CONFIG_PATH from the VS Code process.

## Research Goals

- Establish the exact code path that allows version to be overridden from config
- Identify all consumers of settings.server.version
- Identify all other ServerSettings fields and determine whether any are also incorrectly configurable
- Determine the correct fix strategy and obtain approval
- Establish corrected behavior as design input

---

## Background

Discovered during validation of issue #355. The bug is environment-dependent: tests pass from a plain terminal (no MCP_CONFIG_PATH) but fail via MCP run_tests (pytest subprocess inherits MCP_CONFIG_PATH from VS Code). mcp_config.yaml is in .gitignore; the documented example in docs/mcp_server/ARCHITECTURE.md includes version: '1.0.0' as a hardcoded value.

---

## Findings

## Root Cause

`ServerSettings.version` is declared as a regular Pydantic field:

```python
version: str = Field(default_factory=_default_server_version)
```

Pydantic treats this as a settable input field. `from_env()` loads `mcp_config.yaml` via `yaml.safe_load()` and passes the full server dict (including `version: '1.0.0'`) directly to `ServerSettings(**server_data)`. There is no code path that strips or ignores the version key before construction. The `importlib.metadata` mock patches the `default_factory` callable, but when an explicit value is provided via the constructor, the factory is never called.

## Affected Code

| File | Symbol | Role |
|------|--------|------|
| `mcp_server/config/settings.py` | `ServerSettings.version` | Defective field — must become computed |
| `mcp_server/config/settings.py` | `_default_server_version()` | Must become the body of the computed_field |
| `mcp_server/config/settings.py` | `Settings.from_env()` | No change needed — hardening at ServerSettings level is sufficient |
| `mcp_server/cli.py:21` | `_settings.server.version` | Only consumer — unaffected by fix |
| `mcp_config.yaml` (operator file) | `server.version` key | Must be removed |
| `docs/mcp_server/ARCHITECTURE.md` | documented example with `version:` | Must be updated |

## Other ServerSettings Fields

| Field | Should be configurable? | Reasoning |
|-------|------------------------|----------|
| `name` | Yes | User-facing server identifier |
| `version` | **No** | Package invariant — runtime-derived from importlib.metadata |
| `workspace_root` | Yes | Deployment-specific path |
| `config_root` | Yes | Deployment-specific path |
| `server_root_dir` | Yes | Project-specific state directory |
| `logs_dir` | Yes | Operator-controlled output directory |

`version` is the **only** field in `ServerSettings` that violates the configurable/read-only boundary.

## Pydantic v2 `computed_field` Behavior

`@computed_field` in Pydantic v2 produces a property-like field that:
- Is excluded from model `__init__` (cannot be set via constructor kwargs)
- Is included in model serialization (`.model_dump()`, `.model_fields_set`)
- Is compatible with both mutable and frozen models
- When `extra='forbid'` is active, passing `version` as a constructor kwarg raises `ValidationError` immediately

This makes `@computed_field` the correct mechanism for package-derived values.

## Test Impact

The `autouse` fixture `mock_server_version()` in `test_settings.py` patches `mcp_server.config.settings.metadata.version`. After the fix, `@computed_field` calls `_default_server_version()` at property-access time, not at construction time. The mock remains effective because `metadata.version()` is called on each access.

The `test_load_from_yaml` test must be verified: its YAML fixture must not contain `version:` under `server:`, or it will raise `ValidationError` after `extra='forbid'` is added.

## Corrected Behavior

- `settings.server.version` always returns the value from `importlib.metadata.version()`
- Any `mcp_config.yaml` containing `version:` under `server:` raises a Pydantic `ValidationError` at startup
- `importlib.metadata` mocks in tests work correctly regardless of `MCP_CONFIG_PATH`

## Approved Strategy

**Boundary**: `ServerSettings.version`
**Selected strategy**: Clean break (A+)
**Policy**: Hard-fail on stale config

**Implementation constraints for design/planning**:
1. `version: str = Field(default_factory=_default_server_version)` → `@computed_field` calling `_default_server_version()`
2. `ServerSettings` gains `model_config = ConfigDict(extra='forbid')`
3. `version:` key removed from `mcp_config.yaml` (operator file)
4. `version:` key removed from documented YAML example in `docs/mcp_server/ARCHITECTURE.md`

**Supported contract vs defect dependence**: No legitimate caller passes `version` to `ServerSettings` — all existing usages read the field, they never set it. This is a clean break with zero supported-contract impact.

**Operator impact**: Operators with `version:` in their `mcp_config.yaml` will get a startup `ValidationError`. This is the intended behavior, selected explicitly by the project owner.

## Blast Radius

### Production files changed

| File | Change | Risk |
|------|--------|------|
| `mcp_server/config/settings.py` | `version` field → `@computed_field`; add `ConfigDict(extra='forbid')`; add `computed_field` import | Low — isolated to ServerSettings class |
| `mcp_config.yaml` (operator file, .gitignore) | Remove `version:` key | Operator must update before restart |
| `docs/mcp_server/ARCHITECTURE.md` | Remove `version:` from documented YAML example | Documentation only |

### Test files affected

| File | Change required | Reason |
|------|----------------|--------|
| `tests/mcp_server/unit/config/test_settings.py` | Verify/remove `version:` from any YAML fixture passed to `from_env()` or `ServerSettings()` | `extra='forbid'` will raise `ValidationError` if version key is present |
| `tests/mcp_server/unit/test_cli.py` | No change expected | Mock patches `metadata.version()` at call time; `@computed_field` calls it on access — same behavior |

### Files confirmed unaffected

9 additional test files import `Settings` or `ServerSettings` but do not interact with the `version` field. `LogSettings`, `GitHubSettings`, and `Settings` itself require no changes. `from_env()` requires no changes — hardening at `ServerSettings` level is sufficient.

### Total scope

3 production files (1 code, 1 operator config, 1 doc) + 1 test file verification. No API surface changes, no new dependencies, no cross-module blast.

## Design Phase

**Design phase is skipped.** The Approved Strategy fully specifies the implementation:

- The fix mechanism is unambiguous (`@computed_field` + `extra='forbid'`)
- There are no strategy-sensitive boundaries requiring design input
- There are no interface or compatibility decisions outstanding
- There are no open questions for design to resolve

All constraints needed by planning and implementation are captured in this research document. Planning may proceed directly from this artifact.

## Related Documentation
- **[Pydantic v2 computed_field: https://docs.pydantic.dev/latest/concepts/fields/#computed-fields][related-1]**

<!-- Link definitions -->

[related-1]: Pydantic v2 computed_field: https://docs.pydantic.dev/latest/concepts/fields/#computed-fields

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-06 | Agent | Initial draft |
| 1.1 | 2026-06-06 | Agent | Added blast radius; confirmed design phase skipped |