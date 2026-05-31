<!-- docs\development\issue358\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-31T14:00Z updated= -->
# MCP Tool Schema Audit: Surface Constraints to Prevent First-Use Errors

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-31

---

## Approved Strategy Constraints

The following strategy decisions from research are binding for all implementation cycles. No cycle may deviate from these without reopening the human decision.

| Boundary | Strategy | Implementation constraint |
|----------|----------|--------------------------|
| Grens A — config-driven enum/maxLength | **A4** (tool `input_schema` override) | Pydantic model stays pure; override is on tool class only; always call `super().input_schema`, mutate the returned dict, return it |
| Grens B — static constraints | **A2** (direct Pydantic `Field`) | Only for values that are not config-driven; no drift risk |
| Grens C — stateful constraints | **A1** (description only) | Cannot be schema constraints; no Pydantic enforcement attempted |
| `CreateBranchInput` / `GitCommitInput` ClassVar | **A4 atomically** (Q8) | ClassVar removal and A4 override must land in the same commit — no split |
| `to_phase` enrichment | **A4 enum-only + A1 compact pointer** | Enum from `workphases.yaml` phases; compact `get_work_context()` pointer; no workflow×phase matrix |
| Reference docs | **In scope** | `docs/reference/mcp/tools/` updated for all 14 modified tools in C4 |
| `ValidateDTOTool` | **A1 only** | Description fix only; no structural validation added |
| A4 per-tool pattern | **No mixin** | Each tool independently overrides `input_schema`; shared convention is `schema = super().input_schema`, mutate, return |

**A2 is architecturally forbidden for config-driven values** (Architecture Principles §3 Config-First; §2 DRY/SSOT). Any field whose valid values come from a config file must use A4, not A2.

---

## Config Access Map

Resolved config access paths for all A4 tools. Implementation must follow these paths exactly. No tool may read config from a path not listed here.

| Tool | Field(s) enriched | Config access path | Constructor gap |
|------|-------------------|-------------------|-----------------|
| `CreateBranchTool` | `branch_type.enum`, `name.pattern` | `self.manager.git_config.branch_types`, `self.manager.git_config.branch_name_pattern` | None — clean |
| `GitCommitTool` | `commit_type.enum` | `self.manager.git_config.commit_types` | None — clean |
| `ScaffoldArtifactTool` | `artifact_type.enum` | `self.manager.registry.list_type_ids()` | None — clean |
| `TransitionPhaseTool` | `to_phase.enum` | `self._workphases_config.phases.keys()` | New param `workphases_config: WorkphasesConfig` in `_BaseTransitionTool.__init__` |
| `ForcePhaseTransitionTool` | `to_phase.enum` | Same | Same |
| `InitializeProjectTool` | `workflow_name.enum` | `self._contracts_config.workflows.keys()` | New param `contracts_config: ContractsConfig` in `__init__` |
| `CreateIssueTool` | `issue_type.enum` | `[e.name for e in self._issue_config.issue_types]` | None — `issue_config` already injected |
| `CreateIssueTool` | `priority.enum` | `[l.name.split(":")[-1] for l in self._label_config.get_labels_by_category("priority")]` | New param `label_config: LabelConfig` |
| `CreateIssueTool` | `scope.enum` | `self._scope_config.scopes` | New param `scope_config: ScopeConfig` |
| `CreateIssueTool` | `title.maxLength` | `self._git_config.issue_title_max_length` | New param `git_config: GitConfig` |

`server.py` already loads all config objects at startup. No new config loading is required — only new param forwarding in tool constructors.

---

## Blast Radius Per Cycle

### C1 — ClassVar removal + A4 git_tools.py

| File | Type | Change |
|------|------|--------|
| `mcp_server/tools/git_tools.py` | Production | Remove `_git_config` ClassVar + `configure()` from `CreateBranchInput` and `GitCommitInput`; remove `validate_branch_type` and `validate_commit_type` field_validators; add `input_schema` overrides to `CreateBranchTool` and `GitCommitTool`; add `model_validator` on `GitCommitInput` for `cycle_number` |
| `mcp_server/server.py` | Production | Remove `CreateBranchInput.configure(...)` call (line 140) and `GitCommitInput.configure(...)` call (line 312) |
| `tests/mcp_server/tools/test_git_tools_config.py` | Test | **Full rewrite** — tests ClassVar pattern that disappears; replace with A4 schema content assertions |
| `tests/mcp_server/test_support.py` | Test | Remove `CreateBranchInput.configure(git_config)` call at line 222 |
| `tests/mcp_server/unit/tools/test_git_tools.py` | Test | Rewrite 2 tests (`test_git_commit_tool_with_invalid_commit_type`, `test_git_commit_tool_commit_type_case_insensitive`); remove configure() call at line 351; add A4 `commit_type.enum` test |

### C2 — A2 static Pydantic constraints

| File | Type | Change |
|------|------|--------|
| `mcp_server/tools/phase_tools.py` | Production | `ForcePhaseTransitionInput`: add `Field(..., min_length=1)` to `skip_reason` and `human_approval` |
| `mcp_server/tools/label_tools.py` | Production | `CreateLabelInput`: add `pattern` to `name` field; add `pattern="^[0-9A-Fa-f]{6}$"` to `color` field |
| `mcp_server/tools/project_tools.py` | Production | `InitializeProjectInput`: add `@model_validator(mode="after")` for `custom_phases` conditional |
| Tests | Test | New tests for `CreateLabelInput` pattern rejection; new test for `InitializeProjectInput` `custom_phases` conditional |

### C3 — A4 config-driven overrides + constructor injection

| File | Type | Change |
|------|------|--------|
| `mcp_server/tools/phase_tools.py` | Production | `_BaseTransitionTool.__init__`: new `workphases_config: WorkphasesConfig` param; both tools: `input_schema` override injecting `to_phase.enum` |
| `mcp_server/tools/project_tools.py` | Production | `InitializeProjectTool.__init__`: new `contracts_config: ContractsConfig` param; `input_schema` override for `workflow_name.enum`; existing manual schema property refactored |
| `mcp_server/tools/issue_tools.py` | Production | `CreateIssueTool.__init__`: new `label_config`, `scope_config`, `git_config` params; `input_schema` override for `issue_type`, `priority`, `scope`, `title.maxLength` |
| `mcp_server/tools/scaffold_artifact.py` | Production | `ScaffoldArtifactTool.input_schema` override for `artifact_type.enum` |
| `mcp_server/server.py` | Production | Update 5 tool constructor call sites (CreateIssueTool ×2, `_BaseTransitionTool` descendants ×2, `InitializeProjectTool` ×1) |
| Tests | Test | New tests for each `input_schema` override; stable: `test_all_tools.py`, `test_create_issue_schema.py` |

### C4 — A1 descriptions + reference docs

| File | Type | Change |
|------|------|--------|
| `mcp_server/tools/pr_tools.py` | Production | `SubmitPRTool.base` description (3-tier cascade) |
| `mcp_server/tools/project_tools.py` | Production | `SavePlanningDeliverablesTool`, `UpdatePlanningDeliverablesTool` descriptions |
| `mcp_server/tools/label_tools.py` | Production | `AddLabelsTool.labels` description |
| `mcp_server/tools/milestone_tools.py` | Production | `CreateMilestoneTool.due_on` description |
| `mcp_server/tools/validation_tools.py` | Production | `ValidateDTOTool` tool description |
| `mcp_server/tools/phase_tools.py` | Production | `TransitionPhaseTool.to_phase`, `ForcePhaseTransitionTool.to_phase` A1 pointer descriptions |
| `docs/reference/mcp/tools/` | Docs | Reference pages for all 14 modified tools |

**Stable test files (confirmed no changes needed in any cycle):**

| File | Reason stable |
|------|--------------|
| `tests/mcp_server/unit/tools/test_extra_forbid.py` | Does not include modified models |
| `tests/mcp_server/unit/tools/test_base_tool_input_schema.py` | Tests `BaseTool` base class only |
| `tests/mcp_server/unit/integration/test_all_tools.py` | Asserts `schema is dict`; A4 overrides return valid dicts |
| `tests/mcp_server/unit/tools/test_force_phase_transition_tool.py` | Tests execute; non-empty strings pass `min_length=1` |

**C3-affected test files (requires changes in C3):**

| File | Impact |
|------|--------|
| `tests/mcp_server/unit/tools/test_create_issue_schema.py` | Uses `__new__` bypass — breaks when `input_schema` reads instance attrs; must construct tool fully or mock attributes |
| `tests/mcp_server/unit/tools/test_initialize_project_tool.py` | Fixture missing new `contracts_config` param → `TypeError`; fixture update required |
| `tests/mcp_server/unit/tools/test_scaffold_artifact.py` | Additive new tests for `artifact_type.enum` schema content |

---

## Architecture and Typing Obligations

- **A3 is forbidden in all cycles.** No Pydantic model may import or call config loaders, `ClassVar`, or any infrastructure object. Violations are rejected regardless of green tests.
- **A4 pattern**: always `schema = super().input_schema` → mutate the returned dict → return it. Never call `model_json_schema()` directly in overrides.
- **Type annotations**: all new constructor params must be fully typed. New `input_schema` overrides must have return type `dict[str, Any]`.
- **Quality gates**: run `run_quality_gates` on all changed files before each phase commit. Target: pylint 10.00/10, mypy pass.
- **`test_extra_forbid.py` invariant**: any new `Field` constraints must not break the extra-forbid test for affected models.

---

## Scope

**In Scope:**
A4 input_schema overrides; A2 static Pydantic constraints; A1 description enrichments; ClassVar removal from git_tools.py; constructor injection of missing config params in server.py; reference docs in docs/reference/mcp/tools/

**Out of Scope:**
Manager business logic changes; new tool functionality; output schema or ToolResult changes; new workflows or phases

## Prerequisites

Read these first:
1. Research artifact complete and Approved Strategy captured (docs/development/issue358/research.md @ c137c505)
2. Config access map established in planning — no design phase required
---

## Summary

4-cycle plan to implement A1/A2/A4 schema fixes for 14 gaps across 52 MCP tool input models, eliminating first-use errors where agents discover constraints only via round-trip failures.

---

## Dependencies

- C2 must follow C1 (git_tools ClassVar removal precondition)
- C3 must follow C2 (constructor injection depends on stable A2 validators)
- C4 has no code dependencies and may be done in any order after C3

---

## TDD Cycles


### Cycle 1: C1 — ClassVar removal + A4 git_tools.py (atomic)

**Goal:** Atomically remove ClassVar pattern from CreateBranchInput and GitCommitInput and replace with per-tool input_schema overrides; add A2 model_validator for cycle_number conditional on GitCommitInput.

**Tests:**
- test_git_tools_config.py: full rewrite — A4 branch_type.enum and name.pattern schema content tests
- test_git_tools.py: rewrite 2 ClassVar-dependent tests; add A4 commit_type.enum test
- test_support.py:222: remove configure() call

**Success Criteria:**
- CreateBranchInput and GitCommitInput have no ClassVar _git_config field or configure() classmethod
- All 5 ClassVar call sites removed (git_tools.py:140, git_tools.py:312, test_support.py:222, test_git_tools_config.py:66, test_git_tools.py:351)
- CreateBranchTool.input_schema returns branch_type.enum from git_config.branch_types and name.pattern from git_config.branch_name_pattern
- GitCommitTool.input_schema returns commit_type.enum from git_config.commit_types
- GitCommitInput model_validator enforces cycle_number is not None when workflow_phase==implementation
- All existing tests pass; new A4 schema content tests pass; quality gates green



### Cycle 2: C2 — A2 static Pydantic constraints

**Goal:** Add static min_length, pattern, and model_validator constraints to ForcePhaseTransitionInput, CreateLabelInput, and InitializeProjectInput.

**Tests:**
- test_force_phase_transition_tool.py: stable (existing tests pass non-empty strings)
- New or updated tests for CreateLabelInput pattern rejection (name and color)
- New test for InitializeProjectInput custom_phases conditional model_validator

**Success Criteria:**
- ForcePhaseTransitionInput.skip_reason and human_approval have Field(min_length=1) in addition to existing field_validator
- CreateLabelInput.name has pattern matching LabelConfig.validate_label_name() structural regex
- CreateLabelInput.color has pattern ^[0-9A-Fa-f]{6}$
- InitializeProjectInput has model_validator(mode=after) requiring custom_phases when workflow_name==custom
- Pydantic rejects empty skip_reason/human_approval before execute(); label name and color pattern violations rejected at model level
- All tests pass; quality gates green



### Cycle 3: C3 — A4 config-driven schema overrides + constructor injection

**Goal:** Add input_schema property overrides to TransitionPhaseTool, ForcePhaseTransitionTool, InitializeProjectTool, CreateIssueTool, and ScaffoldArtifactTool; inject missing config params via constructors and update server.py call sites.

**Tests:**
- New tests for each new input_schema override: to_phase.enum, workflow_name.enum, issue_type/priority/scope.enum, title.maxLength, artifact_type.enum
- test_all_tools.py: stable (asserts schema is dict — additive overrides remain valid dicts)
- test_create_issue_schema.py: **requires update** — uses `CreateIssueTool.__new__(CreateIssueTool)` which bypasses `__init__`; after C3 installs `input_schema` override reading instance attrs (`self._label_config` etc.) this will raise `AttributeError`; test must construct tool fully or mock missing attributes
- test_initialize_project_tool.py: **requires update** — fixture instantiates `InitializeProjectTool` without the new `contracts_config` param; will fail with `TypeError` after C3 adds that required param; fixture must pass a `ContractsConfig` instance
- tests/mcp_server/unit/tools/test_scaffold_artifact.py: additive new tests for `artifact_type.enum` schema content
**Success Criteria:**
- _BaseTransitionTool.__init__ accepts workphases_config: WorkphasesConfig; to_phase.enum injected in both TransitionPhaseTool and ForcePhaseTransitionTool from workphases_config.phases.keys()
- InitializeProjectTool.__init__ accepts contracts_config: ContractsConfig; workflow_name.enum injected from contracts_config.workflows.keys(); existing manual schema property refactored to super().input_schema pattern
- CreateIssueTool.__init__ accepts label_config: LabelConfig, scope_config: ScopeConfig, git_config: GitConfig; issue_type.enum from issue_config, priority.enum from label_config, scope.enum from scope_config, title.maxLength from git_config
- ScaffoldArtifactTool.input_schema returns artifact_type.enum from self.manager.registry.list_type_ids()
- server.py updated: CreateIssueTool x2 call sites, _BaseTransitionTool x2, InitializeProjectTool x1 all pass new params
- All existing and new tests pass; quality gates green



### Cycle 4: C4 — A1 description enrichments + reference docs

**Goal:** Enrich field and tool descriptions for 8 A1 gaps across 6 tool files; update docs/reference/mcp/tools/ reference pages for all 14 modified tools.

**Tests:**
- No test changes required (A1 description strings have no test assertions in current suite)
- Quality gates verify changed tool files

**Success Criteria:**
- SubmitPRTool.base description documents 3-tier cascade (explicit value → state.json parent_branch → git_config.default_base_branch)
- SavePlanningDeliverablesTool and UpdatePlanningDeliverablesTool descriptions reference the validates-spec Layer 2 validation structure
- AddLabelsTool.labels description mentions label naming constraints
- CreateMilestoneTool.due_on description specifies accepted ISO 8601 datetime format (YYYY-MM-DDTHH:MM:SSZ)
- ValidateDTOTool description accurately states what it validates (file-exists check, not structural DTO validation)
- TransitionPhaseTool.to_phase and ForcePhaseTransitionTool.to_phase A1 descriptions include compact get_work_context() pointer
- docs/reference/mcp/tools/ updated for all 14 modified tools
- All tests pass; quality gates green on all changed files


---

## Risks & Mitigation

- **Risk:** ClassVar removal (C1) creates a no-validation window if split across commits
  - **Mitigation:** Q8 atomicity: ClassVar removal and A4 input_schema override land in same commit
- **Risk:** A4 does not add Pydantic early rejection — manager remains enforcement authority
  - **Mitigation:** Accepted per Q1 Approved Strategy: schema is for discovery, manager enforces. Not a regression.
- **Risk:** test_git_tools_config.py full rewrite may miss edge cases
  - **Mitigation:** Exit criteria require all A4 schema content paths covered by new tests

## Related Documentation
- **[docs/development/issue358/research.md][related-1]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/development/issue358/research.md
[related-2]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |