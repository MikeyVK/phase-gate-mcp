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

### 1. Subsystem-by-Subsystem Gap Analysis

#### 1.1. Transport Layer (`server.py`)
* **Presentation Boundary Violation (§15):**
  * **Gap:** The transport controller (`MCPServer.handle_call_tool`) directly constructs a user-facing visual payload (URI, mimeType, and JSON formatting) when returning validation errors:
    ```python
    if getattr(result_dto, "error_type", None) == "ValidationError":
        raw_result.content.append({
            "type": "resource",
            "resource": {
                "uri": "schema://validation",
                "mimeType": "application/json",
                "text": json.dumps(getattr(result_dto, "input_schema", {})),
            },
        })
    ```
  * **Correction:** The transport layer must remain completely agnostic of display resources and URIs. The formatting of this resource block should be delegated to `IPresenter`.
* **Open/Closed Principle (OCP - §1.2) Violation:**
  * **Gap:** The validation resource injection is hardcoded for the `"ValidationError"` error type. If a new type of error requires a similar schema injection, `server.py` must be modified.

#### 1.2. Presentation Layer (`text_presenter.py`)
* **Open/Closed Principle (OCP - §1.2) & Config-First (§3) Violation:**
  * **Gap:** The presenter contains a hardcoded mapping of tool names to their categories (`mutation`, `query`, `bootstrap`):
    ```python
    if tool_name in ("create_branch", "git_add_or_commit", ...):
        resolved_cat = "mutation"
    ```
  * **Correction:** Tool classifications and metadata (like display categories or emojis) must be defined in the tool schemas, decorators, or `presentation.yaml` configuration, never as string literals in Python.
* **Fail-Fast Violation (§4):**
  * **Gap:** String templates in `presentation.yaml` are formatted at runtime. If a template contains a syntax error or a mismatch with a DTO field, it triggers a formatting exception during execution, returning a raw fallback text block.
  * **Correction:** All configuration presentation templates should be validated against their corresponding DTO classes at **startup** inside `ConfigValidator`.

#### 1.3. State & Resource Cache Layer (`response_cache.py` & `cache.py`)
* **Single Responsibility Principle (SRP - §1.1) Gaps:**
  * **ResponseCacheManager:** Responsible for caching, FIFO eviction logic, generating new UUIDs, and parsing run-ids from URIs.
  * **CachedResponseResource:** Exposes the MCP resource API AND performs UUID format normalization (replacing/re-adding hyphens to match cache keys).
* **DRY & SSOT Violation (§2):**
  * **Gap:** Key parsing and UUID normalization logic (e.g., stripping hyphens from UUIDs to lookup cache entries) is duplicated in both `CachedResponseResource` and `ResponseCacheManager`. There is no single utility class or value object that canonicalizes `run_id` references.

#### 1.4. Bootstrapping & Composition Layer (`bootstrap.py` & `tool_factory.py`)
* **Dependency Inversion Violation (DIP - §1.5 / §11):**
  * **Gap:** `MCPServer` couples directly to the concrete class `TextPresenter` instead of the `IPresenter` abstraction.
  * **Gap:** `TextPresenter` parses raw `dict` structures in its constructor instead of relying on a pre-validated configuration object injected from the loader.
* **Tight Coupling (Circular Dependency Smells - §12):**
  * **Gap:** `bootstrap.py` uses extensive inline imports (`from mcp_server.presenters.text_presenter import ...` inside functions) to bypass circular import errors. This indicates architectural coupling between the bootstrap sequence, presenters, and server entry points.

#### 1.5. Enforcement Subsystem (`enforcement_runner.py`)
* **Single Responsibility Principle (SRP - §1.1) Violation:**
  * **Gap:** `EnforcementRunner` orchestrates the policy dispatch execution AND implements all concrete check logic (e.g., `_handle_check_branch_policy`, `_handle_check_pr_status`, etc.) inside the same class. If a specific validation rule changes, the runner class itself must be modified.
* **Open/Closed Principle (OCP - §1.2) Violation:**
  * **Gap:** The standard action-registry mapping (`_build_default_registry`) hardcodes action types to handler methods:
    ```python
    registry.register("check_branch_policy", self._handle_check_branch_policy)
    ```
    Supporting a new action type requires adding a new method and registering it directly in Python code. Handlers should be separate strategy classes or functions registered dynamically.
* **Config-First Violation (§3):**
  * **Gap:** The set of allowed tool categories is hardcoded in Python:
    ```python
    KNOWN_TOOL_CATEGORIES: frozenset[str] = frozenset({"branch_mutating"})
    ```
    Adding new categories requires Python changes.

#### 1.6. Config Loading (`loader.py`)
* **Single Responsibility Principle (SRP - §1.1) Violation:**
  * **Gap:** `ConfigLoader` contains cross-validation logic (such as checking parent references and validating artifact types in `load_project_structure_config`). 
  * **Correction:** The config loader should only read and deserialize files into Pydantic models. All validation of relationships between config objects must be delegated to `ConfigValidator` to keep responsibilities clean.
* **Explicit over Implicit Violation (§8):**
  * **Gap:** `resolve_config_root` contains heuristic probing (`_probe_candidates`) using parent directories and CWD to locate the configuration directory if no explicit path is passed. This creates implicit behaviors that can cause silent errors in testing or production.

#### 1.7. Config Validation (`validator.py`)
* **Open/Closed Principle (OCP - §1.2) Violation:**
  * **Gap:** `ConfigValidator.validate_startup()` explicitly dispatches to hardcoded private validators (e.g., `_validate_phase_contracts`, `_validate_project_structure`). Introducing a new configuration file (like `presentation.yaml`) requires modifying the validator class.
* **Fail-Fast Violation (§4):**
  * **Gap:** The startup validator completely ignores the presentation configuration (`presentation.yaml`). Presentation syntax errors or missing keys are not validated at startup, deferring errors to runtime presentation formatting.

### 2. Dead Code in Production & Test Suites

#### 2.1. Production Code Dead Files
* **[base.py](file:///c:/temp/pgmcp/mcp_server/tools/base.py):**
  * **Gap:** Since the tool migration to `ICoreTool` completed, this file is empty and only contains a retired module docstring. It represents dead code in the repository.
* **[decorators.py](file:///c:/temp/pgmcp/mcp_server/tools/decorators.py):**
  * **Gap:** An empty file containing a single comment. All decorators have been moved to `mcp_server/core/decorators/`.

#### 2.2. Test Suite Dead Files
* **[test_base.py](file:///c:/temp/pgmcp/tests/mcp_server/unit/tools/test_base.py):**
  * **Gap:** Empty file marked as "Retired base tools unit tests".
* **[test_base_tool_error_handling.py](file:///c:/temp/pgmcp/tests/mcp_server/unit/tools/test_base_tool_error_handling.py):**
  * **Gap:** Empty file marked as "Deprecated - BaseTool error handling is deleted".
* **[test_base_tool_input_schema.py](file:///c:/temp/pgmcp/tests/mcp_server/unit/tools/test_base_tool_input_schema.py):**
  * **Gap:** Empty deprecated file.
* **[test_branch_mutating_tool.py](file:///c:/temp/pgmcp/tests/mcp_server/unit/tools/test_branch_mutating_tool.py):**
  * **Gap:** Empty deprecated file.

### 3. Test Suite Bloat, Legacy Tests & Redundancy

The `pgmcp` codebase contains nearly **3000 tests** for ~50 tools, which is disproportionately large for a clean, decoupled architecture. This bloat is caused by the following structural issues:

#### 3.1. Trivial and Redundant Metadata Tests
* **Gap:** Every concrete tool test file contains copy-pasted tests verifying static attributes (name, description, args model):
  ```python
  def test_tool_name(self, tool: SearchDocumentationTool) -> None:
      assert tool.name == "search_documentation"
  ```
  These tests verify constants and do not test business logic or behavior, adding maintenance overhead with zero functional coverage.

#### 3.2. Massive Setup Duplication (DRY Violation - §2)
* **Gap:** The test suite lacks a centralized set of reusable fakes or fixtures for the core managers. Nearly every tool test class manually constructs its own complex mocks (e.g. `MockGitManager`, `MockEnforcementRunner`) using monkeypatches or unittest.mock, leading to thousands of lines of redundant setup code.
* **Correction:** Centralize common manager fakes (e.g., `InMemoryGitManager`, `FakeEnforcementRunner`) under `tests/mcp_server/fixtures/`.

#### 3.3. Unit and Integration Test Overlap
* **Gap:** Many unit tests in `tests/mcp_server/unit/tools/` perform extensive mocking of multiple layers to verify E2E behavior. This creates huge overlap with E2E tests in `tests/mcp_server/integration/`. 
* **Correction:** Pure unit tests should only assert inputs/outputs of the concrete `ICoreTool.execute` method in isolation, while decorators and server orchestration should be verified in dedicated, flat integration tests.

#### 3.4. Direct Private Method Access in Tests (API Boundary Violation - §14)
* **Gap:** Several tests inspect internal properties or call private helper methods to assert state:
  * **Example:** Accessing private properties like `_workspace_root` or mocking private handlers.
  * **Correction:** Tests must be written purely against the public interfaces.

### 4. Comprehensive Gap Action Items

| Subsystem / Area | Identified Gap | Required Architectural Correction |
| :--- | :--- | :--- |
| **Transport (`server.py`)** | Inline validation resource formatting. | Move validation schema resource construction to `IPresenter`. |
| **Presenter (`text_presenter.py`)** | Hardcoded tool classification. | Define tool categories/emojis in configuration (`presentation.yaml`). |
| **Presenter (`text_presenter.py`)** | Runtime template format errors. | Validate format placeholders in `ConfigValidator` at startup. |
| **Cache (`cache.py`)** | Normalization in presentation resource. | Move ID normalization out of resource layer to cache manager. |
| **Cache (`response_cache.py`)** | Duplicate ID canonicalization. | Implement a unified `RunId` value object or helper to ensure SSOT. |
| **Imports (`bootstrap.py`)** | Inline imports to bypass circular dependency. | Refactor class boundaries to resolve circular references statically. |
| **Enforcement (`enforcement_runner.py`)** | Class implements both dispatching and checks. | Split specific handler logic into separate strategy classes/functions. |
| **Enforcement (`enforcement_runner.py`)** | Hardcoded tool categories. | Load valid tool categories from schema configs. |
| **Config Loader (`loader.py`)** | Class performs project structure validation. | Delegate cross-config checks (such as directory/parent paths) to `ConfigValidator`. |
| **Config Loader (`loader.py`)** | Heuristic probing to guess config root. | Require explicit config path passing; fail fast if missing. |
| **Validation (`validator.py`)** | Startup check ignores presentation config. | Add cross-validation checks for presentation config placeholders. |
| **Clean-up (Codebase)** | Empty/retired production & test files. | Physically delete `tools/base.py`, `tools/decorators.py`, and empty test files. |
| **Test Suite** | High test count due to redundant metadata assertions. | Delete trivial name/description assertions; rely on interface schema checks. |
| **Test Suite** | Setup duplication. | Create reusable shared fakes/fixtures for managers in `tests/fixtures/`. |
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