<!-- docs\development\issue402\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-12T19:45Z updated= -->
# Planning — Issue #402: Expose JSON data in MCP tools

**Status:** DRAFT  
**Version:** 1.3
**Last Updated:** 2026-06-12

---

## Purpose

Slice the implementation of Issue #402 into 9 manageable cycles for TDD execution.

## Scope

**In Scope:**
All active registered tools in mcp_server/tools/, schemas/tool_outputs.py, presenters/text_presenter.py, and presentation.yaml.

**Out of Scope:**
Unregistered or legacy tools (specifically DetectLabelDriftTool).

## Prerequisites

Read these first:
1. Approved Research Document
2. Approved Design Document
---

## Summary

Plan for migrating all active MCP tools to return Pydantic DTOs alongside declarative text fallbacks, resolving DRY and presentation concerns.

---

## Dependencies

- All cycles are sequential, dependencies follow cycle ordering.

---

## TDD Cycles

### Cycle 1: Core Presenter & Infrastructure

**Goal:** Build the base DTO schemas, global presentation.yaml config, TextPresenter logic, fail-fast template validation, and pytest helper.

**Deliverables:**
- **[D1.1]** Base output schemas in `tool_outputs.py` and global `presentation.yaml` config (File: `mcp_server/schemas/tool_outputs.py`)
- **[D1.2]** `TextPresenter` implementation and `validate_presentation_alignment` drift validator, verifying that YAML anchors and aliases are parsed and resolved safely (File: `mcp_server/presenters/text_presenter.py`)
- **[D1.3]** `assert_structured_tool_result` pytest helper (File: `tests/mcp_server/test_support.py`)
- **[D1.4]** Update `StructuredTool.execute()` dispatcher and signature to support `BaseModel | tuple` return types (File: `mcp_server/tools/base.py`)
- **[D1.5]** Add `presentation_config: PresentationConfig` to `ConfigLayer` in `bootstrap.py` and implement parsing in `ConfigLoader` (Files: `mcp_server/config/loader.py`, `mcp_server/bootstrap.py`)
- **[D1.6]** Extend `MCPServer.__init__` and `ServerBootstrapper` to inject `TextPresenter` (Files: `mcp_server/server.py`, `mcp_server/bootstrap.py`)
- **[D1.7]** Infrastructure test suite refactor: update all test instantiations of `MCPServer` and mock configs to support `PresentationConfig` and `TextPresenter` constructor-injection (Files: `tests/**/*.py`)

**Tests:**
- `tests/mcp_server/unit/test_presenter.py`

**Success/Exit Criteria:**
TextPresenter, server injection, config loader, and startup validator pass all unit tests.
### Cycle 2: Batch 1 (Admin, Health & Cycle Tools)

**Goal:** Migrate HealthCheckTool, RestartServerTool, TransitionCycleTool, and ForceCycleTransitionTool to StructuredTool with DTOs and configs.

**Deliverables:**
- **[D2.1]** Migration of HealthCheckTool, RestartServerTool, TransitionCycleTool, and ForceCycleTransitionTool.

**Tests:**
- `tests/mcp_server/unit/tools/test_cycle_tools.py`
- `tests/mcp_server/unit/tools/test_health_tools.py`

**Success/Exit Criteria:**
All Batch 1 tools return Pydantic DTOs and compact text fallbacks, verified by assert_structured_tool_result.


### Cycle 3: Batch 2 (Discovery & Project Tools)

**Goal:** Migrate all search, project, and context tools to StructuredTool with flattened DTOs.

**Deliverables:**
- **[D3.1]** Migration of Discovery, Search, and Project tools (Batch 2).

**Tests:**
- `tests/mcp_server/unit/tools/test_discovery_tools.py`

**Success/Exit Criteria:**
All Discovery & Project tools return Pydantic DTOs and match templates in presentation.yaml.


### Cycle 4: Batch 3a (Git Analysis & Info Tools)

**Goal:** Migrate Git list, diff, parent, merge check, and status tools.

**Deliverables:**
- **[D4.1]** Migration of Git status, list, diff, parent, and merge check tools.

**Tests:**
- `tests/mcp_server/unit/tools/test_git_tools.py`

**Success/Exit Criteria:**
Git status, list, diff, parent, and merge check tools migrated and return DTOs.


### Cycle 5: Batch 3b (Git Mutation & Action Tools)

**Goal:** Migrate Git branch creation, commit, restore, checkout, push, merge, delete, stash, fetch, and pull tools.

**Deliverables:**
- **[D5.1]** Migration of Git branch creation, commit, restore, checkout, push, merge, delete, stash, fetch, and pull tools.

**Tests:**
- `tests/mcp_server/unit/tools/test_git_tools.py`

**Success/Exit Criteria:**
Git branch creation, commit, restore, checkout, push, merge, delete, stash, fetch, and pull tools migrated.


### Cycle 6: Batch 4a (GitHub Issues & PRs)

**Goal:** Move read models to github_models.py and migrate Issue and PR tools.

- **[D6.1]** Move read models to `github_models.py` and migrate Issue and PR tools (File: `mcp_server/schemas/github_models.py`).
- **[D6.2]** Check that nested read models validation in `IssueOutput` and `PROutput` does not trigger extra fields errors or serialization mismatch under `frozen=True` (Files: `tests/mcp_server/unit/tools/test_issue_tools.py`, `tests/mcp_server/unit/tools/test_pr_tools.py`).
**Tests:**
- `tests/mcp_server/unit/tools/test_issue_tools.py`
- `tests/mcp_server/unit/tools/test_pr_tools.py`

**Success/Exit Criteria:**
GitHub Issues and PR tools successfully migrated and return flattened DTO presentation fields.


### Cycle 7: Batch 4b (GitHub Labels & Milestones)

**Goal:** Migrate GitHub Label and Milestone tools.

**Deliverables:**
- **[D7.1]** Migration of GitHub Label and Milestone tools.

**Tests:**
- `tests/mcp_server/unit/tools/test_label_tools.py`
- `tests/mcp_server/unit/tools/test_milestone_tools.py`

**Success/Exit Criteria:**
GitHub Labels and Milestones tools successfully migrated and return flattened DTO presentation fields.


### Cycle 8: Batch 5 (Phase, Scaffold, Quality & Testing Tools)

**Goal:** Migrate transition, scaffold, quality, pytest, and safe edit tools, ensuring strict separation of details (verbose/diffs/schemas only in JSON).

**Deliverables:**
- **[D8.1]** Migration of transition, scaffold, quality, pytest, and safe edit tools, ensuring strict separation of details (verbose/diffs/schemas only in JSON).
- **[D8.2]** Remove transition constants (`TRANSITION_ADVISORY_NOTE`, `TRANSITION_ADVISORY_TOOL_NAMES`) and discard logic from `phase_tools.py` and `server.py`, resolving the double-SSOT advisory issue (Files: `mcp_server/tools/phase_tools.py`, `mcp_server/server.py`).

**Tests:**
- `tests/mcp_server/unit/tools/test_test_tools.py`
- `tests/mcp_server/unit/tools/test_safe_edit_tool.py`
## Test Suite Strategy & Refactoring

Transitioning to dual JSON+text outputs and Pydantic DTOs requires modifications to the test suite to prevent breaking changes and ensure tests remain DRY:

### 1. Introduction of `assert_structured_tool_result`
We will add a shared helper in `tests/mcp_server/test_support.py` to validate the dual-payload structure. All modified tests will transition from asserting directly on `result.content` to using this helper:
- Verifies that `len(result.content) == 2`.
- Verifies that `content[0]["type"] == "json"` and `content[1]["type"] == "text"`.
- Validates the JSON content against the expected DTO key-values.
- Verifies that the text fallback contains the expected substring.

### 2. Pytest Fixture Consolidation
Many test files (such as `test_git_tools.py` and `test_pr_tools.py`) currently duplicate mock setup code for managers and tool instances. We will refactor these to use reusable fixtures:
- Introduce module- and class-level fixtures for instantiating tools with mocked managers.
- Centralize default mock behavior (such as returning a clean git status or the active branch) in fixtures to minimize boilerplate.

### 3. Incremental Test Adaptation
The compatibility bridge in `StructuredTool` allows us to migrate tests incrementally:
- In each cycle, we migrate a batch of tools and simultaneously update their corresponding test cases to the new DTO structure.
- Unmigrated tools continue to use their existing tests and succeed via the legacy-tuple fallback route.
- This ensures the test suite remains 100% green at every commit.

---
**Success/Exit Criteria:**
Batch 8 tools migrated; pytest tracebacks and safe edit diffs are only returned in the JSON payload, and JSON reference is appended conditionally. If tests fail and verbose=False, post_tool_instruction recommends running with verbose=True.


### Cycle 9: Validation, Quality Gates, and Cleanup

**Goal:** Perform full test suite run and ruff quality gate checks on the entire changed codebase, and remove the temporary compatibility layer.

**Deliverables:**
- **[D9.1]** Green full test suite run and clean quality gates check.
- **[D9.2]** Remove the compatibility bridge in `StructuredTool` so it only supports `BaseModel` DTOs, satisfying YAGNI §9 (File: `mcp_server/tools/base.py`).

**Tests:**
- Run full test suite: `pytest`
- Run quality gates: `ruff check` and type checks

**Success/Exit Criteria:**
All 2880+ tests pass, and quality gates pass with zero lint or typing violations. Compatibility bridge removed cleanly.

---

## Risks & Mitigation

- **Risk:** Broken tests due to output structure change
  - **Mitigation:** Implement assert_structured_tool_result helper in Cycle 1 and apply to all migrated test files.
- **Risk:** Startup failures due to template-DTO drift
  - **Mitigation:** Implement validate_presentation_alignment and ensure it runs during server startup and test-time.

---

## Milestones

- Cycle 1 Complete: present presenter architecture to user.
- Cycle 5 Complete: check Git tools.
- Cycle 8 Complete: check Batch 5 tools.
- Cycle 9 Complete: ready for QA PR.

## Related Documentation
- **[docs/development/issue402/research.md][related-1]**
- **[docs/development/issue402/design.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/development/issue402/research.md
[related-2]: docs/development/issue402/design.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-12 | Agent | Initial draft |
| 1.1 | 2026-06-12 | Agent | Refined cycles and deliverables to 9 sequential TDD cycles |
| 1.2 | 2026-06-12 | Agent | Resolved QA blockers, warnings, and added YAML anchor parsing verification |
| 1.3 | 2026-06-12 | Agent | Resolved QA NOGO feedback (flattened DTOs, server-level routing, presentation_category, test suite impact) |
