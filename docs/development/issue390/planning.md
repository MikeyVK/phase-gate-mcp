<!-- docs/development/issue390/planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-11T06:35:05Z updated=2026-06-11T08:38Z -->
# Planning — Issue #390: Improve validation logic of save/update deliverables tools

**Status:** APPROVED  
**Version:** 1.1  
**Last Updated:** 2026-06-11

---

## Purpose

Plan sequential integration cycles for introducing StructuredTool, SRP conversion, strict Pydantic deliverables validation, and cycles renaming.

---

## Prerequisites

Before implementation begins, the following must be in place:
1. Approved design document (`docs/development/issue390/design.md`) and migration guide (`docs/development/issue390/migration.md`).
2. Clean working tree on branch `bug/390-improve-validation-logic-of-save-update-deliverables`.
3. All quality gates passing on the base branch.

---

## Scope

**In Scope:**
* Implementation of the abstract `StructuredTool` base class.
* Implementation of `mcp_converters.py` containing pure response-to-content functions.
* Definition of strict frozen Pydantic schemas for deliverables validation.
* Refactoring of `ProjectManager` and deliverables tools to use injected `ContractsConfig` and validation models.
* Complete renaming of the `tdd_cycles` database key to `cycles` across production and test files.
* Migration of all 8 JSON-producing/deliverables tools.
* Central test helper `assert_structured_result` implementation.

**Out of Scope:**
* Migration of non-JSON tools.
* Altering the core execution logic of `EnforcementRunner` or unrelated managers.

---

## Cycle Strategy

The implementation is broken down into 8 sequential cycles to allow for step-by-step TDD verification and minimal regression risk:

| Cycle | Focus | Why this boundary exists | Main affected surfaces | Primary proof |
| :--- | :--- | :--- | :--- | :--- |
| **Cycle 1** | StructuredTool & Converters | Core base infrastructure. | `base.py`, `mcp_converters.py` | Unit tests for converters |
| **Cycle 2** | GetIssueTool Migratie | First tool migration, validates base. | `issue_tools.py`, `test_support.py` | GetIssueTool unit tests |
| **Cycle 3** | GetPRTool Migratie | Second tool migration. | `pr_tools.py` | GetPRTool unit tests |
| **Cycle 4** | GetProjectPlanTool Migratie | Third tool migration. | `project_tools.py` | GetProjectPlanTool unit tests |
| **Cycle 5** | InitializeProjectTool Migratie | Validates multiple inheritance. | `project_tools.py` | InitializeProjectTool unit tests |
| **Cycle 6** | Scaffold Tools Migratie | Scaffold tools (schema & artifact). | `scaffold_schema_tool.py`, `scaffold_artifact.py` | Scaffolder tool tests |
| **Cycle 7** | Schema Validation & Rename | Pydantic validation & cycles renaming. | `project_manager.py`, schemas, templates | Deliverables validation tests |
| **Cycle 8** | Cleanup & QA | Cleanup of tests & gates tools. | `test_tools.py`, `quality_tools.py` | Entire pytest suite |

---

## TDD Cycles

### Cycle 1: StructuredTool Base & Server Transport

**Goal:** Implement the StructuredTool class and extract response conversion logic.

| ID | Deliverable | File |
| :--- | :--- | :--- |
| **D1.1** | StructuredTool base class in base.py | `mcp_server/tools/base.py` |
| **D1.2** | MCP converter functions in mcp_converters.py | `mcp_server/utils/mcp_converters.py` |

* **Exit Criteria:** Unit tests in `test_tool_result_conversion.py` succeed.
* **Regression Obligations:** Ensure non-json tools still execute and serialize normally via base.py.

### Cycle 2: GetIssueTool Migratie

**Goal:** Migrate GetIssueTool to StructuredTool and add a central test helper.

| ID | Deliverable | File |
| :--- | :--- | :--- |
| **D2.1** | Migrated GetIssueTool in issue_tools.py | `mcp_server/tools/issue_tools.py` |

* **Exit Criteria:** `GetIssueTool` tests succeed using `assert_structured_result` helper.
* **Regression Obligations:** Verify no text format regressions occur during JSON pop.

### Cycle 3: GetPRTool Migratie

**Goal:** Migrate GetPRTool to StructuredTool.

| ID | Deliverable | File |
| :--- | :--- | :--- |
| **D3.1** | Migrated GetPRTool in pr_tools.py | `mcp_server/tools/pr_tools.py` |

* **Exit Criteria:** `GetPRTool` unit tests pass.
* **Regression Obligations:** Protect PR information output formatting.

### Cycle 4: GetProjectPlanTool Migratie

**Goal:** Migrate GetProjectPlanTool to StructuredTool.

| ID | Deliverable | File |
| :--- | :--- | :--- |
| **D4.1** | Migrated GetProjectPlanTool in project_tools.py | `mcp_server/tools/project_tools.py` |

* **Exit Criteria:** `GetProjectPlanTool` unit tests pass.
* **Regression Obligations:** Verify phase plan dictionaries are not mutated.

### Cycle 5: InitializeProjectTool Migratie

**Goal:** Migrate InitializeProjectTool with multiple inheritance.

| ID | Deliverable | File |
| :--- | :--- | :--- |
| **D5.1** | Migrated InitializeProjectTool in project_tools.py | `mcp_server/tools/project_tools.py` |

* **Exit Criteria:** `InitializeProjectTool` tests pass and `tool_category` is preserved.
* **Regression Obligations:** Ensure PRStatus check enforcement still runs before execution.

### Cycle 6: Scaffold Tools Migratie

**Goal:** Migrate ScaffoldSchemaTool and ScaffoldArtifactTool to StructuredTool.

| ID | Deliverable | File |
| :--- | :--- | :--- |
| **D6.1** | Migrated ScaffoldSchemaTool in scaffold_schema_tool.py | `mcp_server/tools/scaffold_schema_tool.py` |
| **D6.2** | Migrated ScaffoldArtifactTool in scaffold_artifact.py | `mcp_server/tools/scaffold_artifact.py` |

* **Exit Criteria:** Both tools pass their unit tests.
* **Regression Obligations:** Ensure file scaffolding still writes artifacts correctly.

### Cycle 7: Deliverables Schema's & Cycles Validatie

**Goal:** Implement Pydantic validation for deliverables and rename `tdd_cycles` to `cycles`.

| ID | Deliverable | File |
| :--- | :--- | :--- |
| **D7.1** | Pydantic schemas in deliverables.py | `mcp_server/schemas/deliverables.py` |
| **D7.2** | Updated ProjectManager with conditional cycles validation and rename | `mcp_server/managers/project_manager.py` |

* **Exit Criteria:** All validation tests pass; all files, templates, and schemas are renamed.
* **Regression Obligations:** Scan all references to ensure no legacy `"tdd_cycles"` keys remain in production.

### Cycle 8: RunTestsTool & RunQualityGatesTool Cleanup

**Goal:** Clean up RunTestsTool and RunQualityGatesTool and verify full test suite.

| ID | Deliverable | File |
| :--- | :--- | :--- |
| **D8.1** | Cleaned up RunTestsTool and RunQualityGatesTool | `mcp_server/tools/test_tools.py`, `mcp_server/tools/quality_tools.py` |

* **Exit Criteria:** All unit/integration tests (2800+) succeed and run_quality_gates passes 10.00/10.
* **Regression Obligations:** Fully verify that client output truncation is resolved for all tools.

---

## Cross-Cycle Obligations

### Approved Strategy Constraints
* **Native structuredContent**: JSON payloads must be extracted from the content block at the server layer to populate the `structuredContent` field of `CallToolResult`.
* **ToolResult Compatibility**: The `ToolResult.json_data` signature must remain backward compatible during the migration (`text: str | None = None`) to prevent test breakage mid-refactor.

### Architecture Obligations
* **SOLID Principles**: Decouple tool response formatting from execution (SRP). Use constructor injection for configs (DIP).
* **Law of Demeter**: Limit tool dependency chain to at most 2 layers from the tool.

### Typing & Gates Obligations
* **Frozen Schemas**: Deliverables schemas must be frozen value objects (`ConfigDict(frozen=True, extra="forbid")`) in compliance with CQS.
* **Quality Gates**: Run `run_quality_gates` and verify ruff/pyright compliance after every green step.

---

## Dependencies

* Cycle 2 depends on Cycle 1 (requires StructuredTool infrastructure).
* Cycles 3, 4, 5, 6 depend on Cycle 2 (for the test helper pattern).
* Cycle 7 depends on Cycles 1-6 (requires complete codebase readiness before rename cutover).
* Cycle 8 depends on Cycle 7.

---

## Risks and Unknowns

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| MRO conflicts on InitializeProjectTool | Tool execution fails or enforcement bypassed. | Explicitly define `tool_category` on the class and write structural tests. |
| Existing branch deliverables break | Agents on other branches fail to initialize. | Deliver the manual migration guide (`migration.md`) to guide manual updates. |
| Large test regression | 88+ test suites fail during renaming. | Use the central `assert_structured_result` helper to quickly align assertions. |

---

## Related Documentation
- **[docs/development/issue390/design.md][related-1]**
- **[docs/development/issue390/migration.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/development/issue390/design.md
[related-2]: docs/development/issue390/migration.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-11 | Agent | Initial draft. |
| 1.1 | 2026-06-11 | Agent | Restructured to include detailed deliverables tables, cross-cycle obligations, dependencies, and risks matrix. |
