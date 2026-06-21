<!-- docs\development\issue406\research_arch_gap.md -->
<!-- template=research version=8b7bb3ab created=2026-06-21T06:39Z updated= -->
# Architectural Gap Analysis

**Status:** APPROVED  
**Version:** 1.0.0  
**Last Updated:** 2026-06-21

---

## Problem Statement

Evaluate the pgmcp server codebase and test suite against the ARCHITECTURE_PRINCIPLES.md guidelines to identify violations, legacy dependencies, dead code, and test redundancy.

## Research Goals

- Identify architectural gaps in transport, presentation, cache, bootstrapping, enforcement, and config validation layers.
- Analyze the root causes of test suite bloat and redundancy (~3000 tests).
- Document dead code and legacy files remaining in the repository.

---

## Background

During Issue #406 implementation, multiple architectural principles were found to be violated across existing components such as EnforcementRunner, ConfigLoader, and ConfigValidator, in addition to the newly refactored presenter and server layers.

---

## Findings

### 1. Transport Layer (server.py)
- **Presentation Boundary Violation (§15):** The transport controller directly constructs user-facing visual payload resources (`schema://validation`) and JSON formatting for validation errors.
- **OCP Violation (§1.2):** Error payload formatting is hardcoded for `ValidationError`.

### 2. Presentation Layer (text_presenter.py)
- **OCP & Config-First Violation (§1.2 / §3):** Hardcoded tool-to-category mapping (e.g. `create_branch` mapped to `mutation`) in Python instead of configuration.
- **Fail-Fast Violation (§4):** String templates are parsed at runtime; template syntax errors are not validated at startup.

### 3. State & Cache Layer (response_cache.py & cache.py)
- **SRP Violation (§1.1):** Cache manager handles UUID generation and URI parsing. Cache resource handles UUID format normalization.
- **DRY & SSOT Violation (§2):** Parsing and UUID canonicalization is duplicated between resource and cache manager layers.

### 4. Bootstrapping Layer (bootstrap.py & tool_factory.py)
- **DIP Violation (§1.5 / §11):** MCPServer couples to concrete `TextPresenter` instead of `IPresenter`. Presenter constructor parses raw dicts.
- **Coupling (§12):** Circular dependency bypasses using extensive inline imports.

### 5. Enforcement Subsystem (enforcement_runner.py)
- **SRP Violation (§1.1):** EnforcementRunner dispatch orchestrator also implements concrete check logic (e.g. branch policy, PR status checks).
- **OCP Violation (§1.2):** Handlers are hardcoded and registered using local methods.
- **Config-First Violation (§3):** Hardcoded set of allowed tool categories (`KNOWN_TOOL_CATEGORIES`).

### 6. Config Loading & Validation (loader.py & validator.py)
- **SRP Violation (§1.1):** `ConfigLoader` contains cross-validation logic for project structure.
- **OCP Violation (§1.2):** `ConfigValidator` dispatches to hardcoded private validators.
- **Fail-Fast Violation (§4):** Validator ignores `presentation.yaml` templates at startup.

### 7. Dead Code & Test Bloat
- **Dead Files:** Empty production files (`tools/base.py`, `tools/decorators.py`) and retired test files exist in the repository.
- **Test Bloat (~3000 tests):** Caused by trivial metadata assertions, massive setup mock duplication (DRY violation), and unit/E2E overlap.

---

## Approved Strategy

Implement an architectural clean-up phase and refactor violated boundaries incrementally.

---

## Expected Results

100% compliance with ARCHITECTURE_PRINCIPLES.md, deletion of all dead code, and reduction of test suite bloat via shared fixtures.

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-21 | Agent | Initial draft |