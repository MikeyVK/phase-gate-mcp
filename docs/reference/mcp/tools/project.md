<!-- docs/reference/mcp/tools/project.md -->
<!-- template=reference version=064954ea created=2026-02-08T12:00:00+01:00 updated=2026-05-24 -->
# Project & Phase Management Tools

**Status:** DEFINITIVE  
**Version:** 2.1  
**Last Updated:** 2026-05-24  

**Source:** [mcp_server/tools/project_tools.py](../../../../mcp_server/tools/project_tools.py), [phase_tools.py](../../../../mcp_server/tools/phase_tools.py)  
**Tests:** [tests/mcp_server/unit/tools/test_project_tools.py](../../../../tests/mcp_server/unit/tools/test_project_tools.py), [tests/mcp_server/unit/tools/test_transition_phase_tool.py](../../../../tests/mcp_server/unit/tools/test_transition_phase_tool.py), [tests/mcp_server/unit/tools/test_force_phase_transition_tool.py](../../../../tests/mcp_server/unit/tools/test_force_phase_transition_tool.py)  

---

## Purpose

Complete reference documentation for project lifecycle and phase management tools. These 4 tools provide workflow initialization, phase plan inspection, sequential phase transitions, and emergency phase skipping with human approval.

Phase state persists in [.phase-gate/state.json](../../../../.phase-gate/state.json) and workflow definitions / planning deliverables persist in [.phase-gate/deliverables.json](../../../../.phase-gate/deliverables.json). Both files are branch-local artifacts synchronized with git branch operations and neutralized before PR submission.

---

## Overview

The MCP server provides **4 project/phase tools**:

| Tool | Purpose | Key Feature |
|------|---------|-------------|
| `initialize_project` | Initialize project with workflow selection | Human selects workflow type |
| `get_project_plan` | Inspect project phase plan | Read-only phase inspection |
| `transition_phase` | Sequential phase transition | Strict validation |
| `force_phase_transition` | Skip phases (emergency) | Requires reason + human approval |

All tools interact with:
- **PhaseStateEngine:** Phase state tracking and validation
- **[.phase-gate/config/workflows.yaml](../../../../.phase-gate/config/workflows.yaml):** Workflow definitions (feature, bug, docs, refactor, hotfix, epic, custom)
- **[.phase-gate/state.json](../../../../.phase-gate/state.json):** Current branch state (branch-local artifact, committed with branch history; neutralized by `submit_pr`)
- **[.phase-gate/deliverables.json](../../../../.phase-gate/deliverables.json):** Workflow definition and planning deliverables (branch-local artifact)

---

## API Reference

### initialize_project

**MCP Name:** `initialize_project`  
**Class:** `InitializeProjectTool`  
**File:** [mcp_server/tools/project_tools.py](../../../../mcp_server/tools/project_tools.py)

Initialize project with phase plan selection. Human selects workflow_name (feature/bug/docs/refactor/hotfix/epic/custom) to generate project-specific phase plan.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issue_number` | `int` | **Yes** | GitHub issue number |
| `issue_title` | `str` | **Yes** | Issue title |
| `workflow_name` | `str` | **Yes** | Workflow name. Valid values are populated at runtime from `contracts.yaml` via enum injection (C3 A4 override). Examples: `"feature"`, `"bug"`, `"docs"`, `"refactor"`, `"hotfix"`, `"epic"`, `"custom"`. |
| `parent_branch` | `str` | No | Parent branch this feature/bug branches from (auto-detected from git reflog if not provided) |
| `custom_phases` | `list[str]` | **Conditional** | Custom phase list (REQUIRED if `workflow_name="custom"`) |
| `skip_reason` | `str` | No | Reason for custom phases (audit trail) |

#### Workflow Types

| Workflow | Phases | Use Case |
|----------|--------|----------|
| `feature` | 7 phases | New features (planning → research → red → green → refactor → documentation → merge-prep) |
| `bug` | 6 phases | Bug fixes (investigation → red → green → refactor → documentation → merge-prep) |
| `docs` | 2 phases | Documentation only (planning → documentation) |
| `refactor` | 5 phases | Code refactoring (planning → research → refactor → documentation → merge-prep) |
| `hotfix` | 3 phases | Critical fixes (red → green → merge-prep) |
| `epic` | 2 phases | Epic coordination (planning → tracking) |
| `custom` | User-defined | Custom workflows (requires `custom_phases` and `skip_reason`) |

#### Returns

```json
{
  "success": true,
  "message": "Project initialized with feature workflow",
  "project": {
    "issue_number": 123,
    "issue_title": "Add OAuth2 authentication",
    "workflow_name": "feature",
    "phases": [
      "planning",
      "research",
      "red",
      "green",
      "refactor",
      "documentation",
      "merge-prep"
    ],
    "current_phase": "planning",
    "parent_branch": "main"
  }
}
```

#### Example Usage

**Feature workflow:**
```json
{
  "issue_number": 123,
  "issue_title": "Add OAuth2 authentication",
  "workflow_name": "feature",
  "parent_branch": "main"
}
```

**Custom workflow:**
```json
{
  "issue_number": 456,
  "issue_title": "Experimental ML feature",
  "workflow_name": "custom",
  "custom_phases": ["research", "prototype", "evaluation", "implementation"],
  "skip_reason": "ML workflow requires prototype/evaluation phases"
}
```

#### Behavior Notes

- **State Persistence:** Creates `.phase-gate/deliverables.json` (workflow definition) and `.phase-gate/state.json` (branch state) atomically
- **Parent Branch Auto-Detection:** If `parent_branch` not provided, attempts detection via `git reflog`
- **Branch Validation:** Current branch must match pattern `<type>/<issue_number>-*`
- **Idempotency:** Re-running on same branch returns error (project already initialized)

#### Workflow Responsibility

`initialize_project` **must be called by `@co` (coordination role)** as part of the start-issue lifecycle, always after `create_branch` and `git_checkout`.

`@imp` (implementation role) always inherits a branch where `initialize_project` has already completed. If `@imp` reaches a branch without `.phase-gate/state.json`, this is a process violation — `@imp` must **not** call `initialize_project` as recovery; it must stop and report the blocker so `@co` can correct the lifecycle.


---

### get_project_plan

**MCP Name:** `get_project_plan`  
**Class:** `GetProjectPlanTool`  
**File:** [mcp_server/tools/project_tools.py](../../../../mcp_server/tools/project_tools.py)

Get project phase plan for issue number.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issue_number` | `int` | **Yes** | GitHub issue number |

#### Returns

```json
{
  "issue_title": "Add OAuth2 authentication",
  "workflow_name": "feature",
  "execution_mode": "interactive",
  "required_phases": [
    "research",
    "design",
    "planning",
    "implementation",
    "validation",
    "documentation",
    "ready"
  ],
  "skip_reason": null,
  "parent_branch": "main",
  "created_at": "2026-02-08T10:00:00Z",
  "current_phase": "implementation",
  "phase_source": "state.json",
  "phase_detection_error": null
}
```

#### Example Usage

```json
{
  "issue_number": 123
}
```

#### Behavior Notes

- **Read-Only:** Does not modify state
- **Plan Access:** Reads workflow definition from `.phase-gate/deliverables.json`; current phase is read from `.phase-gate/state.json` via `WorkflowStatusResolver`. Returns plan without phase fields when state is absent or branch-mismatched.
- **Not Found:** Returns error if project not initialized

---

### transition_phase

**MCP Name:** `transition_phase`  
**Class:** `TransitionPhaseTool`  
**File:** [mcp_server/tools/phase_tools.py](../../../../mcp_server/tools/phase_tools.py)

Transition branch to next phase (strict sequential validation).

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `branch` | `str` | **Yes** | Branch name (e.g., `"feature/123-oauth"`) |
| `to_phase` | `str` | **Yes** | Target phase to transition to. Run `get_work_context()` to see valid phases for the current branch; enum is injected at runtime from `workphases.yaml`. |
| `human_approval` | `str` | No | Optional human approval message (audit trail) |

#### Returns

```json
{
  "success": true,
  "message": "Transitioned from 'red' to 'green'",
  "transition": {
    "branch": "feature/123-oauth",
    "from_phase": "red",
    "to_phase": "green",
    "timestamp": "2026-02-08T12:00:00Z"
  }
}
```

#### Example Usage

**Sequential transition:**
```json
{
  "branch": "feature/123-oauth",
  "to_phase": "green"
}
```

**With human approval:**
```json
{
  "branch": "feature/123-oauth",
  "to_phase": "documentation",
  "human_approval": "Tests passing, code reviewed, ready for docs"
}
```

#### Behavior Notes

- **Sequential Validation:** Target phase must be the **next** phase in workflow (no skipping)
- **State Update:** Updates `.phase-gate/state.json` atomically
- **Branch-Local State:** Updates `.phase-gate/state.json` for the active branch only
- **Required Next Step:** On success, the response appends `🚀 REQUIRED NEXT STEP: Call get_work_context now before any other tool call to load the current phase context for this branch.`
- **Not Initialized:** Returns error if project not initialized

#### Example Error (Attempting to Skip)

**Request:**
```json
{
  "branch": "feature/123-oauth",
  "to_phase": "merge-prep"  // Trying to skip from "red" to "merge-prep"
}
```

**Response:**
```json
{
  "success": false,
  "error": "Invalid phase transition: cannot skip from 'red' to 'merge-prep'. Next phase is 'green'. Use force_phase_transition if intentional."
}
```

---

### force_phase_transition

**MCP Name:** `force_phase_transition`  
**Class:** `ForcePhaseTransitionTool`  
**File:** [mcp_server/tools/phase_tools.py](../../../../mcp_server/tools/phase_tools.py)

Force non-sequential phase transition (skip/jump with reason and human approval).

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `branch` | `str` | **Yes** | Branch name (e.g., `"feature/123-oauth"`) |
| `to_phase` | `str` | **Yes** | Target phase to transition to (can skip phases). Run `get_work_context()` to see valid phases for the current branch; enum is injected at runtime from `workphases.yaml`. |
| `skip_reason` | `str` | **Yes** | Reason for skipping validation (audit trail) — must be non-empty (min_length=1) |
| `human_approval` | `str` | **Yes** | Human approval message (REQUIRED for forced transitions) — must be non-empty (min_length=1) |

#### Returns

```json
{
  "success": true,
  "message": "Forced transition from 'red' to 'merge-prep' (skipped: green, refactor, documentation)",
  "transition": {
    "branch": "feature/123-oauth",
    "from_phase": "red",
    "to_phase": "merge-prep",
    "skipped_phases": ["green", "refactor", "documentation"],
    "skip_reason": "Emergency hotfix approved by team lead",
    "human_approval": "Team lead approval: critical security fix",
    "timestamp": "2026-02-08T12:00:00Z"
  }
}
```

#### Example Usage

```json
{
  "branch": "feature/123-oauth",
  "to_phase": "merge-prep",
  "skip_reason": "Emergency hotfix: critical security vulnerability discovered",
  "human_approval": "Approved by Tech Lead (John Doe) - immediate merge required"
}
```

#### Behavior Notes

- **No Validation:** Bypasses sequential phase validation
- **Branch-Local State:** Updates `.phase-gate/state.json` for the active branch; forced-transition metadata stays in that branch-local state
- **Required Next Step:** On success, the response appends `🚀 REQUIRED NEXT STEP: Call get_work_context now before any other tool call to load the current phase context for this branch.`
- **Use Sparingly:** Intended for emergency situations only
- **Required Fields:** Both `skip_reason` and `human_approval` are REQUIRED (not optional)

---

## State Management

### save_planning_deliverables

**MCP Name:** `save_planning_deliverables`  
**Class:** `SavePlanningDeliverablesTool`  
**File:** [mcp_server/tools/project_tools.py](../../../../mcp_server/tools/project_tools.py)

Save TDD cycle planning deliverables for an issue to deliverables.json. Validates each `validates` entry schema before persisting.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issue_number` | `int` | **Yes** | GitHub issue number |
| `planning_deliverables` | `dict` | **Yes** | Planning deliverables dict with `tdd_cycles.total` + `cycles[]`. Each deliverable entry may include a `validates` spec with `type` + required fields (Layer 2 runtime validation). |

#### Behavior Notes

- **Write-Once:** Raises an error if deliverables already exist for the issue (use `update_planning_deliverables` to extend)
- **Layer 2 Validation:** Every `validates` entry is validated before writing

---

### update_planning_deliverables

**MCP Name:** `update_planning_deliverables`  
**Class:** `UpdatePlanningDeliverablesTool`  
**File:** [mcp_server/tools/project_tools.py](../../../../mcp_server/tools/project_tools.py)

Merge-update TDD cycle planning deliverables for an issue in deliverables.json. Must be preceded by `save_planning_deliverables`. New cycles are appended; deliverables within existing cycles are merged by id.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issue_number` | `int` | **Yes** | GitHub issue number |
| `planning_deliverables` | `dict` | **Yes** | Partial or full planning deliverables to merge. New cycles are appended; existing cycles have deliverables merged by id. Deliverable entries may include a `validates` spec with `type` + required fields (Layer 2 validation). |

#### Behavior Notes

- **Requires Prior Save:** Returns error if `save_planning_deliverables` was not called first (write-once guard)
- **Merge Strategy:** New cycle → append; existing cycle + new id → append; existing id → overwrite
- **Layer 2 Validation:** Every `validates` entry is validated before writing

---


### .phase-gate/state.json

Current branch state (runtime, branch-local, neutralized before PR submission):

```json
{
  "branch": "feature/123-oauth",
  "issue_number": 123,
  "workflow_name": "feature",
  "current_phase": "documentation",
  "current_cycle": null,
  "last_cycle": 3,
  "cycle_history": [],
  "required_phases": [
    "research",
    "design",
    "planning",
    "implementation",
    "validation",
    "documentation"
  ],
  "execution_mode": "normal",
  "skip_reason": null,
  "issue_title": "Add OAuth2 authentication",
  "parent_branch": "main",
  "created_at": "2026-02-08T10:00:00Z",
  "transitions": [],
  "reconstructed": false
}
```

**Behavior:**
- Updated by `initialize_project`, `transition_phase`, and `force_phase_transition`
- Synchronized by `git_checkout` (loads state when switching branches)
- Treated as a branch-local artifact and neutralized before `submit_pr`

---

### .phase-gate/deliverables.json

Workflow definition and planning deliverables (branch-local artifact):

```json
{
  "123": {
    "issue_title": "Add OAuth2 authentication",
    "workflow_name": "feature",
    "execution_mode": "normal",
    "required_phases": [
      "research",
      "design",
      "planning",
      "implementation",
      "validation",
      "documentation"
    ],
    "skip_reason": null,
    "parent_branch": "main",
    "created_at": "2026-02-08T10:00:00Z",
    "planning_deliverables": {
      "tdd_cycles": {
        "total": 3,
        "cycles": []
      }
    }
  }
}
```

**Behavior:**
- Initialized by `initialize_project`
- Extended by `save_planning_deliverables` and `update_planning_deliverables`
- Treated as a branch-local artifact and neutralized before `submit_pr`

---
---

## Workflow Definitions

### .phase-gate/workflows.yaml

> **Note (Issue #271):** Phase membership and ordering are no longer defined in `workflows.yaml`. The file now contains only workflow metadata (name, description, execution mode). Phase sequences are exclusively defined in `.phase-gate/config/contracts.yaml`.

```yaml
# .phase-gate/config/workflows.yaml
version: "1.0"
phase_source: ".phase-gate/config/workphases.yaml"

workflows:
  feature:
    name: feature
    description: "Full development workflow (research → design → planning → implementation → validation → docs)"
    default_execution_mode: interactive

  bug:
    name: bug
    description: "Bug fix workflow (research → design → planning → implementation → validation → docs)"
    default_execution_mode: interactive

  hotfix:
    name: hotfix
    description: "Emergency fix workflow (implementation → validation → docs only)"
    default_execution_mode: autonomous

  refactor:
    name: refactor
    description: "Code refactoring workflow (research → planning → implementation → validation → docs)"
    default_execution_mode: interactive

  docs:
    name: docs
    description: "Documentation-only workflow (planning → docs)"
    default_execution_mode: interactive

  epic:
    name: epic
    description: "Epic workflow for large initiatives (research → planning → design → coordination → documentation)"
    default_execution_mode: interactive

```


For the phase sequences per workflow, see `.phase-gate/config/contracts.yaml`.

---

## Integration with Git Tools

Phase state is **synchronized** with git branch operations:

| Git Operation | Phase State Behavior |
|---------------|---------------------|
| `git_checkout` | Loads phase state from `.phase-gate/state.json` after switching branches |
| `create_branch` | No phase state (must run `initialize_project` after) |
| `git_delete_branch` | Removes phase state from `.phase-gate/state.json` |

---

## Common Workflows

### Starting a New Feature

```
1. create_branch(name="feature/123-oauth", base_branch="main")
2. git_checkout(branch="feature/123-oauth")
3. initialize_project(issue_number=123, issue_title="Add OAuth2", workflow_name="feature")
```

### TDD Cycle with Phase Transitions

```
1. transition_phase(branch="feature/123-oauth", to_phase="red")
2. scaffold_artifact(artifact_type="dto", name="OAuthToken")
3. git_add_or_commit(workflow_phase="implementation", sub_phase="red", cycle_number=1, message="Add failing test for OAuthToken")
4. transition_phase(branch="feature/123-oauth", to_phase="green")
5. safe_edit_file(...)  # Implement
6. run_tests(path="tests/test_oauth.py")
7. git_add_or_commit(workflow_phase="implementation", sub_phase="green", cycle_number=1, message="Implement OAuthToken")
```

### Emergency Phase Skip (Hotfix)

```
1. force_phase_transition(
     branch="bugfix/456-security",
     to_phase="merge-prep",
     skip_reason="Critical security vulnerability - zero-day exploit",
     human_approval="CTO approval (Jane Smith) - immediate production deployment"
   )
2. git_push(set_upstream=True)
3. submit_pr(title="HOTFIX: Security patch", body="...", head="bugfix/456-security")
4. merge_pr(pr_number=78, merge_method="merge")
```

---

## Related Documentation

- [README.md](README.md) — MCP Tools navigation index
- [git.md](git.md) — Git workflow tools (branch, checkout, commit)
- [.phase-gate/config/workflows.yaml](../../../../.phase-gate/config/workflows.yaml) — Workflow definitions
- [.phase-gate/state.json](../../../../.phase-gate/state.json) — Current branch state
- [.phase-gate/deliverables.json](../../../../.phase-gate/deliverables.json) — Workflow definition and planning deliverables
- [docs/development/issue268/validation.md](../../../development/issue268/validation.md) — Validation evidence for the delivered phase-state and `get_work_context` contract

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.1 | 2026-05-24 | Agent | Document the required `get_work_context` follow-up note on successful phase transitions |
| 2.0 | 2026-02-08 | Agent | Complete reference for 4 project/phase tools: initialize, inspect, transition, force-transition |
| 2.0 | 2026-02-08 | Agent | Complete reference for 4 project/phase tools: initialize, inspect, transition, force-transition |
