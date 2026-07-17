<!-- docs\development\issue429\planning.md -->
<!-- template=planning version=130ac5ea created=2026-07-17T15:44Z updated= -->
# Implementation Plan: Issue #429 - Template Package Bundling

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-07-17

---

## Purpose

Define the slices, dependencies, and constraints for implementing Template Packages.

## Scope

**In Scope:**
- Strict Version Pairing in ArtifactDefinition\n- Refactoring test harness for centralized pathing (`templates/config/`)\n- ConfigLoader DI integration of `template_root`\n- Emptying the `assets/` directory

**Out of Scope:**
- Proactive rewrites of the entire test suite purely to clean up historical paths\n- Feature changes to existing templates\n- Backward compatibility for `config/artifacts/`

---

## Summary

This document outlines the sequential cycles required to bundle Jinja2 templates and artifact configuration YAMLs into cohesive Template Packages within the `templates/config/` directory. It incorporates a Strict Refactor TDD rule to prevent extraneous tests.

---

## TDD Cycles


### Cycle 1: C_SEMVER.1: Centralized Version Validation

**Goal:** Implement a centralized Semantic Versioning (SemVer) utility (`mcp_server/utils/versioning.py`) that strictly enforces version alignment (MAJOR=crash, MINOR=warn/accept, PATCH=accept) to ensure DRY and SRP compliance across all version checks.

**Tests:**
- test_versioning.py (new)

**Success Criteria:**
The `validate_compatibility` function correctly identifies and raises/warns on Major/Minor/Patch mismatches according to the defined SemVer rules.

### Cycle 2: C_VERSION.2: Version-Pairing Foundation

**Goal:** Update ArtifactDefinition and loader logic to strictly pair template versions with configuration files by extracting the `{#- Version: X.Y.Z -#}` header from the Jinja2 file and comparing it to `template_version` in the YAML.

**Tests:**
- test_artifact_registry_config.py
- test_artifacts_yaml_type_field.py

**Success Criteria:**
ConfigLoader raises ConfigError if `template_version` is missing in the YAML, or if it fails to match the version embedded in the Jinja2 template header.



### Cycle 3: C_HARNESS.3: Test Harness & Path Centralization

**Goal:** Centralize path resolution for the test suite to use `templates/config/`.

**Tests:**
- artifact_test_harness.py
- test_smoke_all_types.py
- test_template_missing_e2e.py
- test_concrete_templates.py

**Success Criteria:**
The test infrastructure correctly provisions and intercepts `templates/config/` without hardcoded legacy paths.



### Cycle 4: C_LOADER.4: The Loader Migration (Clean Break)

**Goal:** Point ConfigLoader to `template_root / 'config'` and remove legacy loading fallbacks.

**Tests:**
- test_modular_loader.py

**Success Criteria:**
ConfigLoader successfully loads modular configs from `templates/config/` and fails if legacy `config/artifacts/` is used.



### Cycle 5: C_ASSETS.5: Assets Package Container Cleanup

**Goal:** Empty the dev-time `assets/` directory to solidify its role as a build-time package container.

**Tests:**
- N/A

**Success Criteria:**
The `assets/` directory is completely empty in the source tree.


---

## Typing & Static Analysis Obligations

- Strict adherence to `TYPE_CHECKING_PLAYBOOK.md` is mandatory.
- Proper Dependency Injection types must be defined for `ConfigLoader` when receiving `template_root`.
- Strict typing must be applied for the new `template_version` fields.
- **No global disables** or file-level suppressions are permitted for type checking.

## Quality Gate Expectations

- All implementations and tests must pass `run_quality_gates` before phase completion or cycle progression.
- Expected standard: Linting 10.00/10 and Type checking Pass.
- Code changes must adhere to the `ARCHITECTURE_PRINCIPLES.md` (e.g., Principle 11: Dependency Injection, Principle 16: Template Packages co-location).

---

## Risks & Mitigation

- **Risk:** C_LOADER.3 breaks the entire server if `bootstrap.py` incorrectly injects `template_root`.
  - **Mitigation:** C_HARNESS.2 guarantees the test infrastructure handles the new paths correctly before the loader is switched.
- **Risk:** TDD leads to over-testing or regression testing existing behavior.
  - **Mitigation:** Strict Refactor TDD constraint enforced: NO new test files for existing behavior; strictly modify existing tests.

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-17 | Agent | Initial draft |