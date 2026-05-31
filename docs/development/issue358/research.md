<!-- docs\development\issue358\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-30T11:24Z updated=2026-05-30T12:00Z -->
# MCP Tool Schema Audit: Surface Constraints to Prevent First-Use Errors

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-30

---

## Problem Statement

MCP tool input schemas contain significant drift from the constraints and behaviors enforced at runtime. Agents discover limits only via round-trip errors. This wastes tokens, causes incorrect assumptions, and creates systematic friction across every issue lifecycle.

Concretely: the MCP protocol exposes `inputSchema` during tool discovery (`list_tools`). That schema is derived from the Pydantic model via `model_json_schema()`. If a constraint only lives in execute-time manager code, it is invisible during discovery. An agent submitting a 90-character issue title, an invalid `branch_type`, or an unknown `workflow_name` finds out only after a full round trip — with a stack trace instead of a clear early rejection.

---

## Research Goals

1. Audit all 52 MCP tool input models for schema-to-runtime constraint drift
2. Classify each gap by fix category: static Pydantic (A2), config-driven schema mutation (A4), or description-only (A1)
3. Identify strategy-sensitive boundaries and present policy options per boundary type
4. Document the correct architectural approach for config-driven constraints without violating SRP/DIP
5. Produce an Approved Strategy per boundary for use as planning input

---

## Scope

**In scope:**
- All 52 MCP tool input Pydantic models in `mcp_server/tools/`
- Constraints enforced at runtime in `execute()` or managers but not surfaced in input schemas
- Field description gaps where behavior is underdocumented
- Architectural fit of each fix strategy

**Out of scope:**
- Internal manager logic and business rule changes
- New tool functionality
- Changes to output schemas or ToolResult structure
- Reference documentation updates (tracked separately — confirm with user)

---

## Background: How Tool Schemas Are Exposed

In `mcp_server/server.py:658`:
```python
Tool(name=t.name, description=t.description, inputSchema=t.input_schema)
```

`input_schema` is a property on `BaseTool` (`mcp_server/tools/base.py:51`):
```python
@property
def input_schema(self) -> dict[str, Any]:
    if self.args_model:
        return resolve_schema_refs(self.args_model.model_json_schema())
    return {"type": "object", "properties": {}}
```

This means:
- **What agents see at discovery**: the dict returned by `model_json_schema()` — purely what is defined in the Pydantic model class, nothing more
- **What validates at call time**: the Pydantic model validates the incoming arguments; if the model has no constraint, validation passes; the constraint then fires in `execute()` or inside a manager
- **The gap**: any constraint that is only in `execute()` or a manager is invisible to agents at discovery time

---

## Strategy Taxonomy

Four strategies are available. Only A1, A2, and A4 are architecturally valid.

### A1 — Description-Only

Enrich the field `description` string to document the constraint. No Pydantic enforcement added.

**Appropriate when:** The constraint is stateful (depends on state.json, git HEAD, or network), cross-field in a way JSON Schema cannot express, or behavioral rather than a simple value domain.

**Limitations:** Agents still discover the constraint only when they violate it; the schema does not expose a machine-readable constraint. The improvement is documentation quality.

### A2 — Hardcoded Pydantic Field Constraint

Add a static constraint directly to the Pydantic `Field()` definition: `max_length=72`, `pattern="^[a-z0-9-]+$"`, `Literal[...]`, `ge=1`, etc.

**Appropriate when:** The constraint value is static and not driven by any external config file. The value does not need to change between deployments.

**Advantages:** True early rejection — Pydantic validates before `execute()` runs, before any manager is involved. Schema `maxLength`/`pattern`/`enum` is machine-readable by the MCP client. No additional plumbing needed.

**Limitation:** If the constraint value comes from a config file (e.g., `git.yaml:issue_title_max_length = 72`), hardcoding creates config drift: changing the config file has no effect on the schema or Pydantic validation. Two sources of truth.

### A3 — Config Loading Inside the Pydantic Model ⛔ FORBIDDEN

Add a validator inside the Pydantic model that reads config (e.g., `GitConfig`, `WorkflowConfig`) to apply a constraint.

**Why forbidden by ARCHITECTURE_PRINCIPLES.md:**

The Pydantic input model is a **value object** (a pure data container). Its role is to define field structure and simple static invariants. It must not know about configuration files, config loaders, or the filesystem.

Specifically, A3 violates the binding architecture rule:

> "Schema or value-object changes that add file-path knowledge, config-root knowledge, cross-config orchestration state, or loader responsibilities to pure config models" → **REJECTED**

And the anti-pattern rule:

> "Module-level `Config.load()`" → **REJECTED**

Even if config is injected via a `ClassVar` (as `CreateBranchInput` does for `branch_type` validation), the model class still carries config state at the class level — shared across all instances. This creates hidden coupling: the model's validation behavior depends on an external configuration call that must have been made before the model is instantiated. This is an SRP violation (the model is responsible for both field structure and enforcing business constraints from config) and a DIP violation (the value object depends on a concrete infrastructure class).

**Note:** The existing `CreateBranchInput._git_config: ClassVar[GitConfig | None]` pattern for `branch_type` validation is itself a latent architectural violation of this rule. It is flagged here as pre-existing technical debt. This audit does not recommend extending that pattern.

### A4 — Post-Pydantic Schema Mutation in the Transport Layer

Override the `input_schema` property on the **tool class** (not the model class) to mutate the dict returned by `model_json_schema()` with runtime config values before it is presented to the MCP SDK.

Concretely:
```python
class CreateIssueTool(BranchMutatingTool):

    def __init__(self, ..., github_manager: GitHubManager) -> None:
        self._github_manager = github_manager  # already has git_config access

    @property
    def input_schema(self) -> dict[str, Any]:
        schema = super().input_schema            # pure Pydantic dict — model untouched
        max_len = self._github_manager.git_config.issue_title_max_length
        schema["properties"]["title"]["maxLength"] = max_len
        schema["properties"]["title"]["description"] += f" (max {max_len} chars)"
        return schema
```

**Why NOT forbidden:**
- `CreateIssueInput` remains a pure static value object — it does not know about `git.yaml`, config loaders, or file paths
- `CreateIssueTool` already receives infrastructure objects via constructor injection (`GitHubManager`). This is expected — tools ARE allowed to have infrastructure dependencies. The tool is the MCP adapter layer.
- `input_schema` is a **protocol-adaptation concern**: it describes the tool's interface to the MCP SDK. It is appropriate for this layer to enrich the schema with runtime config values.
- The mutation is on a plain Python dict (the return value of `model_json_schema()`), not on the model class itself. The model class definition is unchanged.
- No ClassVar shared state is added to any model class.

**Honest limitation of A4:** Pydantic still validates the input against the un-mutated model at call time. A 90-char title passes Pydantic validation; the manager then rejects it. The schema advertises `maxLength: 72` (for agent guidance), but Pydantic does not enforce it. The manager remains the actual enforcement layer. This creates a **discovery gap but not a correctness gap** — the agent sees the constraint before calling, and if it violates it, the manager's error message is still clear.

If true early Pydantic-level rejection is wanted in addition to schema accuracy, A4 must be paired with adding the constraint to the Pydantic model also — but that adds the drift risk of A2. The recommended approach is A4 for schema accuracy, keeping manager enforcement as the single source of truth.

---

## Complete Tool Audit (52 tools)

Tools are grouped by file. Each entry shows the input model, the gap found (if any), and the recommended fix strategy.

### Classification key

| Symbol | Meaning |
|--------|---------|
| ✅ | No schema gap — schema and runtime constraints are aligned |
| ⚠️ | Description fix only — behavior is correct, description is incomplete or misleading |
| 🔴 B | Schema change, static (Grens B) — add Pydantic constraint (A2), no config dependency |
| 🔴 A | Schema change, config-driven (Grens A) — requires A4 post-Pydantic schema mutation |
| 🔴 C | Behavioral gap — stateful constraint; A1 description improvement only |

---

### `git_tools.py` — 11 tools

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `CreateBranchTool` (`create_branch`) | `name` field: no pattern constraint in Pydantic model. Runtime enforces `^[a-z0-9-]+$` in `GitManager`. `branch_type` validator uses ClassVar-injected `GitConfig` (latent A3 pattern). | 🔴 B (name) + latent A3 (branch_type) | `CreateBranchInput.name` has only `description="Branch name (kebab-case)"` | A2: add `pattern="^[a-z0-9-]+$"` to `name` field. Do NOT extend ClassVar pattern to other fields. |
| `GitStatusTool` (`git_status`) | — | ✅ | Empty model | — |
| `GitCommitTool` (`git_add_or_commit`) | `cycle_number`: required when `workflow_phase="implementation"` — enforced only in `execute()`, not in model_validator. | 🔴 B | `git_tools.py:388-390`: `if workflow_phase == "implementation" and params.cycle_number is None: raise ValueError(...)` | A2: add `@model_validator(mode="after")` enforcing `cycle_number is not None` when `workflow_phase == "implementation"`. Also add A1: describe constraint in field description. |
| `GitRestoreTool` (`git_restore`) | — | ✅ | `files: list[str]` has `min_length=1` in Field | — |
| `GitCheckoutTool` (`git_checkout`) | — | ✅ | — | — |
| `GitPushTool` (`git_push`) | — | ✅ | — | — |
| `GitMergeTool` (`git_merge`) | — | ✅ | — | — |
| `GitDeleteBranchTool` (`git_delete_branch`) | — | ✅ | `mode` has `Literal["local", "remote", "both"]` | — |
| `GitStashTool` (`git_stash`) | — | ✅ | `action` has `pattern="^(push|pop|list)$"` | — |
| `GetParentBranchTool` (`get_parent_branch`) | — | ✅ | — | — |
| `CheckMergeTool` (`check_merge`) | — | ✅ | — | — |

---

### `issue_tools.py` — 5 tools

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `CreateIssueTool` (`create_issue`) | `title`: no `max_length` in model; enforced by manager. `issue_type`, `priority`, `scope`: no enum/Literal/pattern; valid values from IssueConfig/scopes.yaml/labels.yaml. | 🔴 A (title, issue_type, priority, scope) | `issue_tools.py:193-197`: `GitHubManager.validate_issue_params()` enforces at runtime | A4: override `input_schema` in `CreateIssueTool` to inject `maxLength` for `title` and `enum` arrays for `issue_type`, `priority`, `scope` from injected config objects. |
| `GetIssueTool` (`get_issue`) | — | ✅ | — | — |
| `ListIssuesTool` (`list_issues`) | — | ✅ | `state`: `Literal["open","closed","all"]` | — |
| `UpdateIssueTool` (`update_issue`) | — | ✅ | — | — |
| `CloseIssueTool` (`close_issue`) | — | ✅ | — | — |

---

### `project_tools.py` — 4 tools

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `InitializeProjectTool` (`initialize_project`) | `workflow_name`: no enum/Literal in model. Valid values from `workflows.yaml`. `custom_phases`: required when `workflow_name="custom"` — not enforced in model. | 🔴 A (workflow_name) + 🔴 B (custom_phases conditional) | Runtime enforces in `ProjectManager.initialize_project()` | A4: override `input_schema` to inject `enum` from `WorkflowConfig.workflow_names`. A2: add `@model_validator` for `custom_phases` conditioned on `workflow_name="custom"`. |
| `GetProjectPlanTool` (`get_project_plan`) | — | ✅ | — | — |
| `SavePlanningDeliverablesTool` (`save_planning_deliverables`) | `planning_deliverables` field description does not mention that a Layer 2 validator checks the `validates` entry schema structure after Pydantic. | ⚠️ | Execute logic calls secondary validator invisible to schema | A1: enrich field description to reference the validates-spec structure. |
| `UpdatePlanningDeliverablesTool` (`update_planning_deliverables`) | Same as Save. | ⚠️ | Same | A1: same as Save. |

---

### `phase_tools.py` — 2 tools

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `TransitionPhaseTool` (`transition_phase`) | `to_phase`: no enum/Literal/pattern. Valid phases depend on the current workflow (from `state.json`). Cannot be fully constrained without runtime state. | 🔴 C | `PhaseStateEngine.transition()` enforces at runtime | A1: update description to list all known phases across all workflows. Cannot enumerate per-workflow options at discovery time without state. |
| `ForcePhaseTransitionTool` (`force_phase_transition`) | `to_phase`: same as above. `skip_reason` and `human_approval`: validators exist but `Field(min_length=...)` is absent — agents may pass empty strings that pass Pydantic but fail execute. | 🔴 C (to_phase) + 🔴 B (skip_reason/human_approval min_length) | `phase_tools.py`: validators call `.strip()` and check empty | A1: enrich `to_phase` description. A2: add `min_length=1` to `skip_reason` and `human_approval` fields. |

---

### `cycle_tools.py` — 2 tools

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `TransitionCycleTool` (`transition_cycle`) | — | ✅ | — | — |
| `ForceCycleTransitionTool` (`force_cycle_transition`) | — | ✅ | Validators exist | — |

---

### `pr_tools.py` — 4 tools

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `ListPRsTool` (`list_prs`) | — | ✅ | `state` has pattern | — |
| `MergePRTool` (`merge_pr`) | — | ✅ | `merge_method` has pattern | — |
| `GetPRTool` (`get_pr`) | — | ✅ | — | — |
| `SubmitPRTool` (`submit_pr`) | `base` description says "defaults to main" — actual behavior is 3-tier cascade: provided value → `IBranchParentReader.get_parent_branch()` (from state.json) → `git_config.default_base_branch`. | ⚠️ | `submit_pr.py` execute logic | A1: rewrite field description to document the 3-tier cascade precisely. |

---

### `label_tools.py` — 6 tools

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `ListLabelsTool` (`list_labels`) | — | ✅ | — | — |
| `CreateLabelTool` (`create_label`) | `name`: label name format validated in execute via `LabelConfig.validate_label_name()`, not in model. `color`: 6-char hex validated in execute, not in model. | 🔴 B (both) | `label_tools.py:58-60` | A2: add `pattern="^[a-z0-9:._-]+$"` to `name`, `pattern="^[0-9A-Fa-f]{6}$"` to `color`. Confirm exact pattern from `LabelConfig.validate_label_name()`. |
| `DeleteLabelTool` (`delete_label`) | — | ✅ | — | — |
| `RemoveLabelsTool` (`remove_labels`) | — | ✅ | — | — |
| `AddLabelsTool` (`add_labels`) | `labels` field: format constraint only in execute via `LabelConfig.validate_label_name()`. | ⚠️ | `label_tools.py:177-180` | A1: enrich field description to mention label naming constraints. Or A2: add `min_length=1` per item (but item-level pattern on list[str] requires custom validator). |
| `DetectLabelDriftTool` (`detect_label_drift`) | — | ✅ | — | — |

---

### `milestone_tools.py` — 3 tools

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `ListMilestonesTool` (`list_milestones`) | — | ✅ | `state` has pattern | — |
| `CreateMilestoneTool` (`create_milestone`) | `due_on` description says "ISO 8601 string" without specifying the format. GitHub accepts `YYYY-MM-DDTHH:MM:SSZ` (datetime). | ⚠️ | No model validator | A1: clarify description. Optionally A2: add `pattern="^\\d{4}-\\d{2}-\\d{2}(T\\d{2}:\\d{2}:\\d{2}Z)?$"`. |
| `CloseMilestoneTool` (`close_milestone`) | — | ✅ | — | — |

---

### `admin_tools.py` — 1 tool

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `RestartServerTool` (`restart_server`) | — | ✅ | — | — |

---

### `code_tools.py` — 1 tool

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `CreateFileTool` (`create_file`) | — | ✅ | Deprecated | — |

---

### `discovery_tools.py` — 2 tools

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `SearchDocumentationTool` (`search_documentation`) | — | ✅ | `scope` has pattern | — |
| `GetWorkContextTool` (`get_work_context`) | — | ✅ | Empty model | — |

---

### `git_analysis_tools.py` — 2 tools

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `GitListBranchesTool` (`git_list_branches`) | — | ✅ | — | — |
| `GitDiffTool` (`git_diff_stat`) | — | ✅ | — | — |

---

### `git_fetch_tool.py` — 1 tool

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `GitFetchTool` (`git_fetch`) | — | ✅ | — | — |

---

### `git_pull_tool.py` — 1 tool

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `GitPullTool` (`git_pull`) | — | ✅ | Always pulls current branch's upstream; this is a behavioral design decision, not a schema constraint | — |

---

### `health_tools.py` — 1 tool

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `HealthCheckTool` (`health_check`) | — | ✅ | — | — |

---

### `quality_tools.py` — 1 tool

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `RunQualityGatesTool` (`run_quality_gates`) | — | ✅ | `scope` Literal + `@model_validator` for files/scope contract | — |

---

### `safe_edit_tool.py` — 1 tool

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `SafeEditTool` (`safe_edit_file`) | — | ✅ | `mode` has pattern; `@model_validator` enforces exactly-one edit mode | — |

---

### `scaffold_artifact.py` — 1 tool

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `ScaffoldArtifactTool` (`scaffold_artifact`) | `artifact_type`: no enum constraint. Valid types come from the artifact registry (`artifacts.yaml`). Runtime rejects unknown types. | 🔴 A | `ArtifactManager.scaffold_artifact()` enforces at runtime | A4: override `input_schema` to inject `enum` from `TemplateRegistry.list_artifact_types()`. |

---

### `template_validation_tool.py` — 1 tool

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `TemplateValidationTool` (`validate_template`) | — | ✅ | `template_type` has `pattern="^(worker|tool|dto|adapter|base)$"` | — |

---

### `test_tools.py` — 1 tool

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `RunTestsTool` (`run_tests`) | — | ✅ | `scope: Literal["full"]`; `@model_validator` enforces path/scope mutex | — |

---

### `validation_tools.py` — 1 tool

| Tool | Gap | Category | Evidence | Recommended Fix |
|------|-----|----------|---------|-----------------|
| `ValidateDTOTool` (`validate_dto`) | Tool description says "Validate DTO definition". `execute()` only checks: file exists and is not empty. No structural DTO validation is performed. Description is misleading. | ⚠️ | `validation_tools.py` execute body | A1: update tool `description` to accurately state what it validates. |

---

## Summary Statistics

| Category | Count | Tools |
|----------|-------|-------|
| ✅ No gap | 38 | (see table above) |
| ⚠️ Description fix | 7 | SubmitPRTool, SavePlanningDeliverablesTool, UpdatePlanningDeliverablesTool, AddLabelsTool, CreateMilestoneTool, ValidateDTOTool, (GitPullTool — design decision) |
| 🔴 B Static schema (A2) | 4 | CreateBranchTool (name), GitCommitTool (cycle_number conditional), ForcePhaseTransitionTool (skip_reason/human_approval), CreateLabelTool (name+color) |
| 🔴 A Config-driven schema (A4) | 4 | CreateIssueTool (title/issue_type/priority/scope), InitializeProjectTool (workflow_name), ScaffoldArtifactTool (artifact_type), + InitializeProjectTool (custom_phases: A2 conditional validator) |
| 🔴 C Behavioral (A1 only) | 2 | TransitionPhaseTool (to_phase), ForcePhaseTransitionTool (to_phase) |

**Total gaps: 14** (across 52 tools, 38 need no changes)

---

## Boundary Classification: Architectural Decision Points

### Grens A — Config-Driven Enum/Constraint Values

These fields have valid values that live in a config file, not in Python source. The constraint value must be read from config at server startup.

| Field | Config Source | Values |
|-------|-------------|--------|
| `create_issue.title` max_length | `git.yaml:issue_title_max_length` | 72 (default) |
| `create_issue.issue_type` | `IssueConfig` / labels.yaml | e.g., `feature, bug, hotfix, chore, docs, epic` |
| `create_issue.priority` | `LabelConfig` / labels.yaml | e.g., `critical, high, medium, low` |
| `create_issue.scope` | `scopes.yaml` | e.g., `architecture, mcp-server, platform, tooling, workflow, documentation` |
| `initialize_project.workflow_name` | `workflows.yaml` | e.g., `feature, bug, docs, refactor, hotfix, custom` |
| `scaffold_artifact.artifact_type` | `artifacts.yaml` / TemplateRegistry | e.g., `dto, worker, tool, research, design, reference` |

**Why A3 is forbidden for all of these:**
The input models (`CreateIssueInput`, `InitializeProjectInput`, `ScaffoldArtifactInput`) are value objects. They may not import or instantiate config loaders. Adding a class-level or validator-level reference to `GitConfig.load()`, `WorkflowConfig()`, or `ArtifactRegistry()` inside the model class:
- Violates SRP: the value object acquires a loader responsibility
- Violates DIP: the model class depends on concrete infrastructure
- Violates the explicit Architecture Principles rule against "loader responsibilities to pure config models"
- Creates hidden coupling: validation behavior depends on external state having been loaded

**Why A4 is the correct approach:**
The tool class (e.g., `CreateIssueTool`) already receives infrastructure objects via constructor injection. The `input_schema` property is a protocol-adaptation concern (it translates the model's structure into the MCP transport format). Overriding this property to enrich the dict with config values at the transport layer is architecturally identical to any other protocol adaptation — the model stays pure, the tool's MCP representation is accurate.

A4 implementation pattern:
```python
# In CreateIssueTool
@property
def input_schema(self) -> dict[str, Any]:
    schema = super().input_schema  # model_json_schema() dict — model unchanged
    cfg = self._github_manager.git_config  # already injected
    schema["properties"]["title"]["maxLength"] = cfg.issue_title_max_length
    # Enrich enum for issue_type (example — confirm field path from model):
    schema["properties"]["issue_type"]["enum"] = list(cfg.issue_types)
    return schema
```

**A4's limitation (honest):** Pydantic validates against the un-mutated model at call time. A 90-char title passes Pydantic, hits the manager, and is rejected there with a clear error. A4 improves discovery (agents see the constraint) but does not add Pydantic early rejection. This is acceptable: the schema is informational for agent guidance; the manager remains the enforcement authority.

**Alternative (A2 + config duplication):** Hardcoding `max_length=72` in the Pydantic model gives true early Pydantic rejection but creates drift if `git.yaml` changes. This is an acceptable tradeoff only if the constraint value is stable and considered a code-level constant rather than a deployment-level configuration. **Recommendation: prefer A4 to avoid drift.**

---

### Grens B — Static Pydantic Constraints

These constraints have a fixed value known at code-write time, independent of any config file.

| Field | Constraint | Current State | Fix |
|-------|-----------|--------------|-----|
| `create_branch.name` | `^[a-z0-9-]+$` | Description only ("kebab-case") | A2: `pattern="^[a-z0-9-]+$"` in Field |
| `git_add_or_commit.cycle_number` | Required when `workflow_phase="implementation"` | Execute-time check only | A2: `@model_validator(mode="after")` |
| `force_phase_transition.skip_reason` | Non-empty string | Validator strips and checks, but no `min_length` in Field | A2: `Field(..., min_length=1)` |
| `force_phase_transition.human_approval` | Non-empty string | Same | A2: `Field(..., min_length=1)` |
| `create_label.name` | Validated by `LabelConfig.validate_label_name()` | No model constraint | A2: add `pattern` matching LabelConfig logic |
| `create_label.color` | 6-char hex, no `#` prefix | Execute-time check | A2: `pattern="^[0-9A-Fa-f]{6}$"` |

All of these are appropriate for A2 because the constraint value is not configurable — it is a code-level invariant. Adding a Pydantic constraint does not create any drift risk.

---

### Grens C — Stateful/Behavioral Constraints

These constraints depend on runtime state (state.json, current branch, git HEAD, GitHub API) and cannot be expressed as Pydantic constraints at discovery time.

| Field | Why It Is Stateful | Fix |
|-------|--------------------|-----|
| `transition_phase.to_phase` | Valid phases depend on current workflow in state.json (workflow-specific phase list) | A1: description lists all known phases across all workflows |
| `force_phase_transition.to_phase` | Same | A1: same |
| `submit_pr.base` | 3-tier cascade: explicit value → state.json parent_branch → git_config.default_base_branch | A1: rewrite description to document cascade precisely |

---

## Open Questions for Strategy Approval

These questions require human decision before planning can begin:

**Q1: Grens A — Preferred strategy for config-driven constraints?**

**✅ APPROVED: A4** — Override `input_schema` on affected tools to inject enum/maxLength from injected config. Schema accurate; Pydantic model stays pure; manager remains enforcement authority.

**Note — A2 is architecturally forbidden for config-driven values:** §2 DRY/SSOT: "Any config file defining a list of valid values is the SSOT. Duplicating that list as a regex alternation or hardcoded set elsewhere is a violation." §3 Config-First: "workflow names, branch types: always in config, never as string literals in Python." Hardcoding `Literal["feature","bug",...]` in Python is a Config-First violation.

**Design requirement:** The A4 implementation pattern must be established during the design phase, aligned with existing composition patterns in the codebase. No ad-hoc per-tool `input_schema` overrides without a shared, coherent abstraction.

**Q2: `CreateBranchInput.branch_type` ClassVar pattern — address or defer?**
The existing ClassVar injection pattern for `branch_type` validation in `CreateBranchInput` is architecturally inconsistent with the A3=forbidden ruling (it is a pre-C_LOADER legacy pattern). Options: (a) refactor to A4 within this issue, or (b) defer to a separate issue.

**Q3: `to_phase` — A4 two-part approach**

**✅ APPROVED: A4 two-part** — Strategy is twofold:
1. **Enum injection (machine-readable):** Override `input_schema` to inject the union of all known phases from `workphases.yaml` as a JSON Schema `enum`. This gives the MCP client a machine-readable constraint on the universe of possible phases, while the engine still enforces the workflow-specific valid subset at runtime.
2. **Description enrichment (context):** Enrich the field description with the exact workflow→phase combinations from `contracts.yaml`, so an agent understands which phases are valid for which workflow without a round-trip.

**Open design constraint — description token budget:**
The description enrichment approach raises a cross-cutting design question: if multiple tools carry enriched descriptions (workflow×phase matrices, enum lists, constraint prose), the cumulative token cost of `list_tools` grows with every tool. The MCP client sends the full tool schema in every context window. There is a practical ceiling beyond which description enrichment causes more harm (context overload) than it prevents (round-trip errors).

**This must be quantified in the design phase before any descriptions are written:**
- Measure current total token cost of all 52 tool descriptions (baseline)
- Establish a per-field description budget (e.g., max N tokens per enriched field)
- Apply the budget as a design constraint on all A1 and A4 description changes in this issue
- The workflow×phase matrix for `to_phase` should be the test case for this budget

**Q4: Reference documentation scope — in this branch or separate issue?**
`docs/reference/mcp/tools/` contains per-tool reference pages. Should constraint documentation updates be in scope for this branch, or tracked as a follow-up issue?

**Q5: `ValidateDTOTool` — description fix only, or implement real validation?**

**✅ APPROVED: A1** — Correct the description only. Tool is nominated for removal; no further investment warranted.


---

## Approved Strategy

| Boundary | Strategy | Notes |
|----------|----------|---------|
| Grens A: config-driven enums/maxLength | **A4** (A4 per architecture; A2 forbidden) | Q1 ✅ |
| Grens B: static constraints | A2 (direct Pydantic) | No config dependency |
| Grens C: stateful constraints | A1 (description only) | Cannot be schema constraints |
| CreateBranchInput.branch_type ClassVar | **A4** (refactor ClassVar away; in scope) | Q2 ✅ |
| to_phase descriptions | **A4 two-part** (enum from workphases.yaml + description from contracts.yaml; design-phase token budget required) | Q3 ✅ |
| Reference doc updates | **In scope** (docs/reference/mcp/tools/ updated alongside schema changes) | Q4 ✅ |
| ValidateDTOTool | **A1** (description fix only; nominated for removal) | Q5 ✅ |

---

## Blast Radius

### Production Files With Code Changes (10 files)

| File | Tools Affected | Change Type | Notes |
|------|---------------|-------------|-------|
| `mcp_server/tools/git_tools.py` | `CreateBranchTool`, `GitCommitTool` | A2 + A4 (ClassVar removal × 2) | `CreateBranchInput` ClassVar removed + A4 `input_schema` override for `branch_type`; `GitCommitInput` ClassVar removed, `commit_type` field_validator removed, A4 enriches schema |
| `mcp_server/tools/issue_tools.py` | `CreateIssueTool` | A4 | Override `input_schema` to inject `maxLength` for `title`; `enum` for `issue_type`, `priority`, `scope` |
| `mcp_server/tools/project_tools.py` | `InitializeProjectTool`, `SavePlanningDeliverablesTool`, `UpdatePlanningDeliverablesTool` | A4 + A2 + A1 | A4 `input_schema` for `workflow_name` enum; A2 `@model_validator` for `custom_phases` conditional; A1 description for planning deliverables fields |
| `mcp_server/tools/phase_tools.py` | `TransitionPhaseTool`, `ForcePhaseTransitionTool` | A4 + A2 + A1 | A4 `input_schema` for `to_phase` (two-part: enum + description); A2 `min_length=1` on `skip_reason`/`human_approval` |
| `mcp_server/tools/label_tools.py` | `CreateLabelTool`, `AddLabelsTool` | A2 + A1 | A2 `pattern` on `name` and `color` in `CreateLabelInput`; A1 description for `AddLabelsTool.labels` |
| `mcp_server/tools/milestone_tools.py` | `CreateMilestoneTool` | A1 | Clarify `due_on` description |
| `mcp_server/tools/pr_tools.py` | `SubmitPRTool` | A1 | Rewrite `base` field description (3-tier cascade) |
| `mcp_server/tools/scaffold_artifact.py` | `ScaffoldArtifactTool` | A4 | Override `input_schema` to inject `enum` from TemplateRegistry |
| `mcp_server/tools/validation_tools.py` | `ValidateDTOTool` | A1 | Correct tool description |
| `mcp_server/server.py` | — | Cleanup | Remove `CreateBranchInput.configure(...)` call (line 140 in `CreateBranchTool.__init__`) and `GitCommitInput.configure(...)` call (line 312 in `GitCommitTool.__init__`) |

**Total: 10 production files changed.** 38 of 52 tools are confirmed clean (no changes needed).

### Test Files With Changes (4 files)

| File | Impact | Type |
|------|--------|------|
| `tests/mcp_server/tools/test_git_tools_config.py` | **Full rewrite** | Tests the ClassVar pattern for `CreateBranchInput.configure()` — entire test file tests behavior that disappears. Must be replaced with A4 `input_schema` tests that verify branch_type enum is injected from config |
| `tests/mcp_server/test_support.py` (line 222) | Remove `CreateBranchInput.configure(git_config)` call in `configure_create_branch_input()` helper | Cleanup |
| `tests/mcp_server/unit/tools/test_git_tools.py` (line 351) | Remove `GitCommitInput.configure(mock_git_manager.git_config)` call; update `test_git_commit_tool_with_invalid_commit_type` (tests Pydantic-level rejection that disappears when ClassVar is removed); update `test_git_commit_tool_commit_type_case_insensitive` (tests `.lower()` normalization in the field_validator that disappears) | Rewrite 2 tests |
| `tests/mcp_server/unit/tools/test_scaffold_artifact.py` | Currently tests `ScaffoldArtifactInput(artifact_type="dto")` which remains valid; A4 adds a new `input_schema` property that may need new test coverage for schema content | Additive (new tests, no breaks) |

**Total: 4 test files changed.** Of these, 1 is a full rewrite (`test_git_tools_config.py`), 2 are cleanup/minor updates, and 1 is additive.

### Test Files Confirmed Stable (no changes needed)

| File | Why Stable |
|------|-----------|
| `tests/mcp_server/unit/tools/test_extra_forbid.py` | Parametrized over many Input models; does NOT include `CreateBranchInput`, `GitCommitInput`, or `InitializeProjectInput`. Adding A2 constraints to these models does not affect the test — the valid kwargs still pass, and extra-field rejection is already present |
| `tests/mcp_server/unit/tools/test_base_tool_input_schema.py` | Tests `BaseTool` base class behavior only; unaffected by per-tool overrides |
| `tests/mcp_server/unit/tools/test_create_issue_schema.py` | Tests `CreateIssueTool.input_schema` for `$ref`/`$defs` absence (already fixed). A4 additions are additive; existing assertions on `$ref` absence remain valid |
| `tests/mcp_server/unit/tools/test_initialize_project_tool.py` | Tests execute behavior; `workflow_name` validation moves to schema (A4 enum) not Pydantic. Existing tests pass valid `workflow_name` values — stable |
| `tests/mcp_server/unit/integration/test_all_tools.py` | Asserts only `schema is not None` and `isinstance(schema, dict)`; A4 overrides return valid dicts. Stable |
| `tests/mcp_server/unit/tools/test_force_phase_transition_tool.py` | Tests execute behavior; A2 additions to `skip_reason`/`human_approval` min_length are additive (current tests pass non-empty strings) |

### ClassVar Removal — Call Site Inventory

Both ClassVar patterns in `git_tools.py` have call sites that must be cleaned up:

**`CreateBranchInput.configure(git_config)` — 3 call sites:**
1. `mcp_server/tools/git_tools.py:140` — production, in `CreateBranchTool.__init__`
2. `tests/mcp_server/test_support.py:222` — test helper `configure_create_branch_input()`
3. `tests/mcp_server/tools/test_git_tools_config.py:66` — integration test (full rewrite)

**`GitCommitInput.configure(git_config)` — 2 call sites:**
1. `mcp_server/tools/git_tools.py:312` — production, in `GitCommitTool.__init__`
2. `tests/mcp_server/unit/tools/test_git_tools.py:351` — test, in `test_git_commit_tool_with_invalid_commit_type`

### A1-Only Changes — Zero Test Impact

Description-only changes (A1) in `SubmitPRTool`, `SavePlanningDeliverablesTool`, `UpdatePlanningDeliverablesTool`, `AddLabelsTool`, `CreateMilestoneTool`, and `ValidateDTOTool` require no test changes: string values in tool descriptions have no test assertions in the current suite.

### Blast Radius Summary

| Dimension | Count |
|-----------|-------|
| Production files changed | 10 |
| Test files requiring changes | 4 |
| Test files requiring full rewrite | 1 (`test_git_tools_config.py`) |
| ClassVar call sites to remove | 5 (2 production + 3 test) |
| New tests to write (A4 schema content) | To be specified in planning |
| Tools with changes | 14 of 52 |
| Tools confirmed clean | 38 of 52 |

---

## Related Documentation

- `docs/coding_standards/ARCHITECTURE_PRINCIPLES.md` — binding contract; §2 DRY/SSOT and §3 Config-First prohibit A2 for config-driven values; A3 forbidden
- `docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md`
- `mcp_server/tools/base.py` — `input_schema` property (override point for A4)
- `mcp_server/server.py:655-660` — `handle_list_tools()` registers `t.input_schema`
- `mcp_server/tools/git_tools.py` — `CreateBranchInput` with ClassVar pattern (Q2)
- `mcp_server/tools/issue_tools.py` — `CreateIssueInput` (Grens A primary candidate)
- `mcp_server/tools/project_tools.py` — `InitializeProjectInput` (Grens A)
- `mcp_server/tools/scaffold_artifact.py` — `ScaffoldArtifactInput` (Grens A)
- `mcp_server/tools/phase_tools.py` — `TransitionPhaseInput`, `ForcePhaseTransitionInput` (Grens B+C)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-30 | Agent | Initial research — exhaustive 52-tool audit; strategy taxonomy; boundary classification; open questions for Approved Strategy |
