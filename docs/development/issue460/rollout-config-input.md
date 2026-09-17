<!-- docs\development\issue460\rollout-config-input.md -->
<!-- template=generic_doc version=43c84181 created=2026-09-17T15:05Z updated=2026-09-17 -->
# Issue 460 Rollout Config Input: Placement and Rollout Configuration

**Status:** APPROVED  
**Version:** 2.0  
**Last Updated:** 2026-09-17

---

## Purpose

Record reviewed configuration source mappings, replacement `artifacts.yaml` placement policy for the complete 19-package template suite, `[tool.pyright]` removal hunk, and prospective V3 diffs, preimages, postimages, and drift protection for CY072 cutover.

## Scope

**In Scope:**
Artifacts location policy for all 19 real template suite packages, presentation and quality configuration compatibility, `pyproject.toml` Pyright cleanup, prospective configuration diffs, SHA-256 pre/postimages, and drift protection against preimage mismatch.

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

Implementation evidence for Cycle 70 (Prepared placement and rollout configuration) under Issue #460. Documents V3 configuration migration models, records the exact prospective diffs and SHA-256 pre/postimages for all four affected configurations (`artifacts.yaml`, `pyproject.toml`, `presentation.yaml`, `.version`), proves loader acceptance and rejection of stale aliases on isolated copies against the real 19-package catalog, establishes drift protection / mismatch refusal, and stages prospective diffs without premature live modification.

---

## Key Changes

- Prepare exact replacement `artifacts.yaml` location policy and schema validation for all 19 real template packages.
- Explicitly reject informal aliases (`dto`, `worker`) and unknown packages in accordance with Design contract DI-04 §3.2.
- Record prospective unified diffs and SHA-256 pre/postimages for all 4 affected configurations.
- Record `[tool.pyright]` deletion hunk and verify preserved Pyright values in `pyrightconfig.json`.
- Establish and verify drift protection / mismatch refusal protocol across all prospective patches.
- Provide executable integration test evidence in `test_rollout_configuration.py`.

---

## Migration Steps

1. CY070: Record configuration delta baseline, prospective diffs, and pre/post SHA-256 hashes in `rollout-config-input.md`.
2. CY070: Verify target loaders accept prospective configs, cross-validate against the real 19 template packages, and reject obsolete/stale inputs in `test_rollout_configuration.py`.
3. CY071: Rehearse prospective configuration changes and drift protection against an isolated candidate installation.
4. CY072: Atomically apply prospective configuration diffs to live workspace files alongside cutover.

---

## Validation Checklist

- [x] DOCFLOW-E04: Prospective configuration diffs agree with registered V3 configuration schemas.
- [x] DOCFLOW-E04: All 19 real template packages (`.pgmcp/template_suite/*/manifest.yaml`) are explicitly configured with canonical `template_id`s; informal aliases are rejected.
- [x] DOCFLOW-E04: Isolated target loaders accept prospective configs and reject obsolete structures and unknown template IDs.
- [x] DOCFLOW-E04: Exact prospective diffs and SHA-256 pre/postimages recorded for `artifacts.yaml`, `pyproject.toml`, `presentation.yaml`, and `.version`.
- [x] DOCFLOW-E04: Drift protection / mismatch refusal verified: patches refuse to apply if preimages do not match expected hashes/content.
- [x] `[tool.pyright]` deletion preserves effective Pyright settings via `pyrightconfig.json`.
- [x] No live configuration mutated prior to CY072 cutover.

---

## 1. Configuration Review and Preservation Register (DOCFLOW-E04)

Under DI-04 §3.3, DI-05 §7.20, and Planning Path Ownership, CY070 reviews eight catalogued configuration sources:

| Source ID | Repository Path | Role / Content Authority | CY070 Disposition | Cutover Cycle |
|---|---|---|---|---|
| C004 | `.pgmcp/config/artifacts.yaml` | Workspace artifact location policy | Reviewed; prepare V2.0.0 placement schema for 19 packages; live file untouched | CY072 |
| C005 | `.pgmcp/config/quality.yaml` | Legacy quality gates configuration | Reviewed; superseded by modular V3 checks/tests/fixes; live file untouched | CY072 |
| C006 | `pyproject.toml` | Project configuration | Reviewed; prepare `[tool.pyright]` deletion hunk; live file untouched | CY072 |
| C063 | `mcp_server/config/settings.py` | Central server settings authority | Reviewed; target wiring proven; live file untouched | CY072 |
| C106 | `.pgmcp/config/presentation.yaml` | Output and presentation configuration | Reviewed; target tool hints aligned; live file untouched | CY072 |
| S008 | `pyrightconfig.json` | Native Pyright compiler configuration | Reviewed; confirmed canonical source for Pyright flags; untouched | CY022 / CY072 |
| S017 | `.pgmcp/config/project_structure.yaml` | Legacy project structure | Reviewed; no active dependency in EnforcementRunner; untouched | CY082 |
| S051 | `.pgmcp/.version` | Version marker scalar | Reviewed; compatibility value retained (`2.0.0\n`); live file untouched | CY072 |

---

## 2. Replacement `artifacts.yaml` Location Policy

Under DI-02, DI-04 §3.2, and Design contract [design-mutation-validation.md](design-mutation-validation.md#L1096), `.pgmcp/config/artifacts.yaml` is repurposed from an empty template-registry shell (`version: 1.0.0`, `artifact_types: []`) into the workspace authority for produced-artifact placement.

### 2.1 Canonical Key Reference & Package Catalog

The 19 canonical template packages present in `.pgmcp/template_suite/*/manifest.yaml` (excluding `shared`) define the authoritative catalog:
1. `architecture`
2. `commit`
3. `design`
4. `generic_doc`
5. `issue`
6. `planning`
7. `pr`
8. `pytest_integration_test`
9. `pytest_unit_test`
10. `python_adapter`
11. `python_class`
12. `python_protocol`
13. `python_pydantic_config`
14. `python_pydantic_dto`
15. `python_worker`
16. `reference`
17. `research`
18. `typescript_dto`
19. `validation_report`

**No informal aliases:** Location keys are exact `manifest.yaml:template_id` references. Aliases such as `dto` or `worker` are invalid and strictly rejected by `ConfigValidator.validate_artifact_locations` with `artifact_location_template_unknown`.

### 2.2 Target V3 Schema Model
The target configuration schema is defined by `mcp_server.config.schemas.artifact_locations.ArtifactLocationsConfig`:

```yaml
version: "2.0.0"
artifacts:
  architecture:
    default_root: "docs/architecture"
  commit:
    default_root: ".pgmcp/commits"
  design:
    default_root: "docs/design"
  generic_doc:
    default_root: "docs/development"
  issue:
    default_root: ".pgmcp/issues"
  planning:
    default_root: "docs/planning"
  pr:
    default_root: ".pgmcp/prs"
  pytest_integration_test:
    default_root: "tests/mcp_server/integration"
  pytest_unit_test:
    default_root: "tests/mcp_server/unit"
  python_adapter:
    default_root: "mcp_server/adapters"
  python_class:
    default_root: "mcp_server/classes"
  python_protocol:
    default_root: "mcp_server/protocols"
  python_pydantic_config:
    default_root: "mcp_server/config/schemas"
  python_pydantic_dto:
    default_root: "mcp_server/dtos"
    additional_roots:
      - "mcp_server/models"
  python_worker:
    default_root: "mcp_server/workers"
  reference:
    default_root: "docs/reference"
  research:
    default_root: "docs/research"
  typescript_dto:
    default_root: "frontend/src/dtos"
  validation_report:
    default_root: "docs/development"
```

### 2.3 Semantic Invariants and Validation Rules
1. **Canonical Key Reference:** The mapping key (`<template_id>`) must match `manifest.yaml:template_id` exactly.
2. **One-Way Reference:** Every configured template ID must resolve to a loaded template package. `ConfigValidator.validate_artifact_locations` rejects unknown or stale template IDs at startup. Loaded packages without entries default to the central temporary root `.pgmcp/temp/artifacts`.
3. **Root Normalization & Distinctness:** `default_root` and entries in `additional_roots` must be distinct workspace-relative paths. Duplicate roots within an entry are rejected with `duplicate_artifact_location_root`.
4. **Target Resolution:** Explicit targets at or below admitted roots require no force; targets outside admitted roots require `force_target`.

---

## 3. Prospective Configuration Diffs, Hashes, and Drift Protection

Under Planning §4.1 / §4.3 (DOCFLOW-E04) and Rollout CY070, all planned configuration deltas for CY072 are recorded with their prospective unified diffs, SHA-256 preimages, and SHA-256 postimages.

### 3.1 Drift Protection / Mismatch Refusal Protocol

To protect against configuration drift and race conditions during rollout:
1. Every patch or configuration rewrite verifies that the live file on disk exactly matches the expected **Preimage SHA-256** hash before performing any modification.
2. If the hash or expected hunk does not match, the application procedure immediately **refuses** with `preimage_mismatch` without altering the target file.
3. Upon application, the resulting file is verified against the **Postimage SHA-256** hash.

### 3.2 C004: `.pgmcp/config/artifacts.yaml`
- **Role:** Workspace artifact location policy.
- **Preimage SHA-256:** `e17c98ebd7bc03771ea0b7faab55b05b9b02b16d0b5c34cada21443c962f5157`
- **Postimage SHA-256:** `f5a9870c1f3d140a04f6efdf3a46285e5bcd8549d22eec72bf5c976cb08506bb`

**Prospective Unified Diff:**
```diff
--- a/.pgmcp/config/artifacts.yaml
+++ b/.pgmcp/config/artifacts.yaml
@@ -1,2 +1,42 @@
-version: 1.0.0
-artifact_types: []
+version: "2.0.0"
+artifacts:
+  architecture:
+    default_root: "docs/architecture"
+  commit:
+    default_root: ".pgmcp/commits"
+  design:
+    default_root: "docs/design"
+  generic_doc:
+    default_root: "docs/development"
+  issue:
+    default_root: ".pgmcp/issues"
+  planning:
+    default_root: "docs/planning"
+  pr:
+    default_root: ".pgmcp/prs"
+  pytest_integration_test:
+    default_root: "tests/mcp_server/integration"
+  pytest_unit_test:
+    default_root: "tests/mcp_server/unit"
+  python_adapter:
+    default_root: "mcp_server/adapters"
+  python_class:
+    default_root: "mcp_server/classes"
+  python_protocol:
+    default_root: "mcp_server/protocols"
+  python_pydantic_config:
+    default_root: "mcp_server/config/schemas"
+  python_pydantic_dto:
+    default_root: "mcp_server/dtos"
+    additional_roots:
+      - "mcp_server/models"
+  python_worker:
+    default_root: "mcp_server/workers"
+  reference:
+    default_root: "docs/reference"
+  research:
+    default_root: "docs/research"
+  typescript_dto:
+    default_root: "frontend/src/dtos"
+  validation_report:
+    default_root: "docs/development"
```

### 3.3 C006: `pyproject.toml`
- **Role:** Project configuration.
- **Preimage SHA-256:** `e91b9079e91c2c7ea4c43433c0e635053533696016dfb16160624c994e3cd66f`
- **Postimage SHA-256:** `957d76949f2f1f7bf7da4cbcfa91ed706e0f79f7be495753f9eddd27f9eecfca`

**Prospective Unified Diff:**
```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -123,4 +123,0 @@
-[tool.pyright]
-# Pydantic v2 integration - prevents FieldInfo type inference issues
-reportFunctionMemberAccess = false
-
```

**Native Setting Preservation (CY022 Alignment):**  
Removing `[tool.pyright]` from `pyproject.toml` introduces zero configuration drift because `pyrightconfig.json` is already authoritative for the compiler settings:
- `reportFunctionMemberAccess: false` (line 79)
- `pythonVersion: "3.11"` (line 15)
- `pythonPlatform: "Windows"` (line 16)
- `typeCheckingMode: "strict"` (line 17)
- `include: ["mcp_server"]` (line 3)

### 3.4 C106: `.pgmcp/config/presentation.yaml`
- **Role:** Tool output and instruction presentation configuration.
- **Preimage SHA-256:** `2a51cbf0d6a62cb92b6ba2d302477410de299104185da4170aa64dfa67f70217`
- **Postimage SHA-256:** `1e0a4f5b03dd38a64279aa9c13ad5f9b1e47cc475521aa2b4efe3c8362e75895`

**Prospective Unified Diff:**
```diff
--- a/.pgmcp/config/presentation.yaml
+++ b/.pgmcp/config/presentation.yaml
@@ -60,1 +60,1 @@
-    recheck_quality: "📋 REQUIRED NEXT STEP: Run run_quality_gates(scope='files', files={modified_files}) to verify that the auto-fixed files now pass all quality checks."
+    recheck_quality: "📋 REQUIRED NEXT STEP: Run run_checks(scope='files', files={modified_files}) to verify that the auto-fixed files now pass all quality checks."
```

### 3.5 S051: `.pgmcp/.version`
- **Role:** Compatibility version scalar.
- **Preimage SHA-256:** `efdfae9d0dc9b09f9524df6c401bf7143a882469c6243bfbcb0bbeaefe9aa3c1`
- **Postimage SHA-256:** `efdfae9d0dc9b09f9524df6c401bf7143a882469c6243bfbcb0bbeaefe9aa3c1`
- **Disposition:** Unchanged. The file contains `2.0.0\n` (7 bytes) and remains byte-identical throughout CY070 and CY071 until retirement in CY072.

---

## 4. Compatibility and Retirement of Legacy Configs

### 4.1 `.pgmcp/config/quality.yaml` (C005)
In V2, `quality.yaml` configured legacy quality gate thresholds. In V3, quality checking is partitioned into modular, declarative configs:
- `checks.yaml` (check bindings, tool wrappers, profiles)
- `tests.yaml` (test adapter execution)
- `fixes.yaml` (automated fixer bindings)
`ConfigLoader` in V3 no longer requires `quality.yaml`. In CY072, `quality.yaml` is retired from active configuration.

### 4.2 `.pgmcp/config/project_structure.yaml` (S017)
As established in DI-04 §3.3, `project_structure.yaml` has no active dependency in `EnforcementRunner`. It remains untouched in CY070 and will be retired through a systematic field/consumer migration in CY082.

---

## 5. Executable Evidence (DOCFLOW-E04)

Durable verification for CY070 is provided by the dedicated integration test suite:  
[`tests/mcp_server/integration/test_rollout_configuration.py`](../../../tests/mcp_server/integration/test_rollout_configuration.py)

The test suite validates:
1. `test_real_template_package_catalog_discovery`: Discovers and confirms the 19 real canonical template packages from `.pgmcp/template_suite/*/manifest.yaml`.
2. `test_artifacts_location_config_validates_prospective_v3`: `ConfigLoader` and `ConfigValidator` successfully load and cross-validate prospective V3 `artifacts.yaml` against real packages.
3. `test_stale_or_unknown_template_id_rejection`: Confirms that informal aliases (`dto`, `worker`) and unknown package IDs are strictly rejected with `ConfigError("artifact_location_template_unknown")`.
4. `test_artifacts_location_config_rejects_obsolete_and_duplicate_roots`: Confirms that legacy V1 `artifacts.yaml` (`artifact_types: []`) and duplicate roots within a single entry are strictly rejected.
5. `test_pyproject_pyright_exact_hunk_and_mismatch_refusal`: Verifies prospective deletion of `[tool.pyright]`, TOML parseability, and mismatch refusal.
6. `test_pyrightconfig_native_settings_preservation`: Confirms that `pyrightconfig.json` natively declares all compiler flags (`reportFunctionMemberAccess: false`, `3.11`, `Windows`, `strict`).
7. `test_presentation_yaml_patch_and_mismatch_refusal`: Verifies `presentation.yaml` patch application, `ConfigLoader` acceptance, and mismatch refusal.
8. `test_live_configuration_remains_unmutated_in_cy070`: Verifies that live `.pgmcp/config/artifacts.yaml`, `pyproject.toml`, `presentation.yaml`, and `.version` remain unmodified on disk during CY070.
9. `test_prospective_configuration_hashes_and_drift_protection`: Asserts exact SHA-256 pre/postimages for all 4 configs and verifies drift refusal when preimage hashes deviate.

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
| 2.0 | 2026-09-17 | @imp implementer | Remediation: update artifacts.yaml to all 19 real template suite packages, reject informal aliases, add prospective diffs and SHA-256 pre/postimages for all 4 configs, and document drift protection / mismatch refusal. |
