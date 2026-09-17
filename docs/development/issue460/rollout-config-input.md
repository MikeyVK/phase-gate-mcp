<!-- docs\development\issue460\rollout-config-input.md -->
<!-- template=generic_doc version=43c84181 created=2026-09-17T15:05Z updated=2026-09-17 -->
# Issue 460 Rollout Config Input: Placement and Rollout Configuration

**Status:** PRELIMINARY  
**Version:** 1.0  
**Last Updated:** 2026-09-17

---

## Purpose

Record reviewed configuration source mappings, replacement `artifacts.yaml` placement policy, `[tool.pyright]` removal hunk, and prospective V3 diffs for CY072 cutover.

## Scope

**In Scope:**
Artifacts location policy, presentation and quality configuration compatibility, `pyproject.toml` Pyright cleanup, and prospective configuration diffs.

**Out of Scope:**
Direct mutation of live configuration files prior to CY072; modification of server proxy or transport logic.

## Prerequisites

Read these first:
1. [design-mutation-validation.md](design-mutation-validation.md)
2. [planning-rollout.md](planning-rollout.md#cy070)
3. [rollout-workflow-input.md](rollout-workflow-input.md)
4. [rollout-host-input.md](rollout-host-input.md)

---

## Summary

Implementation evidence for Cycle 70 (Prepared placement and rollout configuration) under Issue #460. Documents V3 configuration migration models, records the exact `[tool.pyright]` removal hunk, proves loader acceptance and rejection on isolated copies, and stages prospective diffs without premature live modification.

---

## Key Changes

- Prepare exact replacement `artifacts.yaml` location policy and schema validation.
- Prepare `presentation.yaml`, `quality.yaml`, and `.version` compatibility changes.
- Record `[tool.pyright]`-only deletion hunk and verify preserved Pyright values in `pyrightconfig.json`.
- Provide executable integration test evidence in `test_rollout_configuration.py`.

---

## Migration Steps

1. CY070: Record configuration delta baseline and prospective diffs in `rollout-config-input.md`.
2. CY070: Verify target loaders accept prospective configs and reject obsolete inputs in `test_rollout_configuration.py`.
3. CY071: Rehearse prospective configuration changes against isolated candidate installation.
4. CY072: Atomically apply prospective configuration diffs to live workspace files alongside cutover.

---

## Validation Checklist

- [x] DOCFLOW-E04: Prospective configuration diffs agree with registered V3 configuration schemas.
- [x] DOCFLOW-E04: Isolated target loaders accept prospective configs and reject obsolete structures.
- [x] `[tool.pyright]` deletion preserves effective Pyright settings via `pyrightconfig.json`.
- [x] No live configuration mutated prior to CY072 cutover.

---

## 1. Configuration Review and Preservation Register (DOCFLOW-E04)

Under DI-04 §3.3, DI-05 §7.20, and Planning Path Ownership, CY070 reviews eight catalogued configuration sources:

| Source ID | Repository Path | Role / Content Authority | CY070 Disposition | Cutover Cycle |
|---|---|---|---|---|
| C004 | `.pgmcp/config/artifacts.yaml` | Workspace artifact location policy | Reviewed; prepare V2.0.0 placement schema; live file untouched | CY072 |
| C005 | `.pgmcp/config/quality.yaml` | Legacy quality gates configuration | Reviewed; superseded by modular V3 checks/tests/fixes; live file untouched | CY072 |
| C006 | `pyproject.toml` | Project configuration | Reviewed; prepare `[tool.pyright]` deletion hunk; live file untouched | CY072 |
| C063 | `mcp_server/config/settings.py` | Central server settings authority | Reviewed; target wiring proven; live file untouched | CY072 |
| C106 | `.pgmcp/config/presentation.yaml` | Output and presentation configuration | Reviewed; target tool hints aligned; live file untouched | CY072 |
| S008 | `pyrightconfig.json` | Native Pyright compiler configuration | Reviewed; confirmed canonical source for Pyright flags; untouched | CY022 / CY072 |
| S017 | `.pgmcp/config/project_structure.yaml` | Legacy project structure | Reviewed; no active dependency in EnforcementRunner; untouched | CY082 |
| S051 | `.pgmcp/.version` | Version marker scalar | Reviewed; compatibility value retained; live file untouched | CY072 |

---

## 2. Replacement `artifacts.yaml` Location Policy

Under DI-02 and DI-04 §3.2, `.pgmcp/config/artifacts.yaml` is repurposed from an empty template-registry shell into the workspace authority for produced-artifact placement.

### 2.1 Target V3 Schema Model
The target configuration schema is defined by `mcp_server.config.schemas.artifact_locations.ArtifactLocationsConfig`:

```yaml
version: "2.0.0"
artifacts:
  dto:
    default_root: "mcp_server/dtos"
    additional_roots:
      - "mcp_server/models"
  worker:
    default_root: "mcp_server/workers"
  generic_doc:
    default_root: "docs/development"
```

### 2.2 Semantic Invariants and Validation Rules
1. **Canonical Key Reference:** The mapping key (`<template_id>`) is authored once as `manifest.yaml:template_id`.
2. **One-Way Reference:** Every configured template ID must resolve to a loaded template package. `ConfigValidator.validate_artifact_locations` rejects unknown or stale template IDs at startup. Loaded packages without entries default to the central temporary root `.pgmcp/temp/artifacts`.
3. **Root Normalization & Distinctness:** `default_root` and entries in `additional_roots` must be distinct workspace-relative paths. Duplicate roots within an entry are rejected with `duplicate_artifact_location_root`.
4. **Target Resolution:** Explicit targets at or below admitted roots require no force; targets outside admitted roots require `force_target`.

---

## 3. `pyproject.toml` `[tool.pyright]` Deletion Hunk

Under CY022 and Planning Path Ownership, `pyproject.toml` contains a duplicate `[tool.pyright]` block that is redundant with `pyrightconfig.json`. CY070 records the exact deletion hunk for CY071 rehearsal and CY072 atomic application.

### 3.1 Prospective Unified Diff

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -123,4 +123,0 @@
-[tool.pyright]
-# Pydantic v2 integration - prevents FieldInfo type inference issues
-reportFunctionMemberAccess = false
-
```

### 3.2 Native Setting Preservation (CY022 Alignment)
Removing `[tool.pyright]` from `pyproject.toml` introduces zero configuration drift because `pyrightconfig.json` is already authoritative for the compiler settings:
- `reportFunctionMemberAccess: false` (line 79)
- `pythonVersion: "3.11"` (line 15)
- `pythonPlatform: "Windows"` (line 16)
- `typeCheckingMode: "strict"` (line 17)
- `include: ["mcp_server"]` (line 3)

All other TOML sections in `pyproject.toml` (`[project]`, `[build-system]`, `[tool.ruff]`, `[tool.coverage]`, `[tool.mypy]`, `[tool.pytest]`) remain untouched.

---

## 4. Compatibility and Retirement of Legacy Configs

### 4.1 `.pgmcp/config/quality.yaml` (C005)
In V2, `quality.yaml` configured legacy quality gate thresholds. In V3, quality checking is partitioned into modular, declarative configs:
- `checks.yaml` (check bindings, tool wrappers, profiles)
- `tests.yaml` (test adapter execution)
- `fixes.yaml` (automated fixer bindings)
`ConfigLoader` in V3 no longer requires `quality.yaml`. In CY072, `quality.yaml` is retired from active configuration.

### 4.2 `.pgmcp/config/presentation.yaml` (C106)
`presentation.yaml` retains full presentation templating and bounded response budgets. In CY072, presentation hints referencing `run_quality_gates` will be cleanly updated to `run_checks`.

### 4.3 `.pgmcp/config/project_structure.yaml` (S017)
As established in DI-04 §3.3, `project_structure.yaml` has no active dependency in `EnforcementRunner`. It remains untouched in CY070 and will be retired through a systematic field/consumer migration in CY082.

---

## 5. Executable Evidence (DOCFLOW-E04)

Durable verification for CY070 is provided by the dedicated integration test suite:
[`tests/mcp_server/integration/test_rollout_configuration.py`](../../../tests/mcp_server/integration/test_rollout_configuration.py)

The test suite validates:
1. `test_artifacts_location_config_validates_prospective_v3`: `ConfigLoader` and `ConfigValidator` successfully load and cross-validate prospective V3 `artifacts.yaml`.
2. `test_artifacts_location_config_rejects_obsolete_and_invalid`: Confirms that legacy V1 `artifacts.yaml` (`artifact_types: []`), duplicate roots, and unknown template IDs are strictly rejected.
3. `test_pyproject_pyright_removal_preserves_pyrightconfig_values`: Verifies that prospective deletion of `[tool.pyright]` preserves all TOML sections and that `pyrightconfig.json` contains the identical setting.
4. `test_live_configuration_remains_unmutated_in_cy070`: Verifies that live `.pgmcp/config/artifacts.yaml` and `pyproject.toml` remain unmodified on disk during CY070.

---

## 6. Rollback (R-CY070)

In case of rollback:
- **Pre-cycle Git Commit SHA:** `f9ac26eac0ae2ce526c62af49c00464e4a4bcd2a`
1. Remove `docs/development/issue460/rollout-config-input.md`.
2. Remove `tests/mcp_server/integration/test_rollout_configuration.py`.
3. Live repository configuration files remain unmutated and require no rollback.

---

## Related Documentation
- [design-mutation-validation.md](design-mutation-validation.md)
- [planning-rollout.md](planning-rollout.md)
- [rollout-workflow-input.md](rollout-workflow-input.md)
- [rollout-host-input.md](rollout-host-input.md)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-17 | @imp implementer | Initial release: configuration source register, artifacts location policy, pyproject deletion hunk, and test verification. |
