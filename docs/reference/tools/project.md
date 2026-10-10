<!-- docs/reference/mcp/tools/project.md -->
<!-- template=reference version=064954ea created=2026-02-08T12:00:00+01:00 updated=2026-05-24 -->
# Project & Phase Management Tools

**Status:** DEFINITIVE  
**Version:** 3.3  
**Last Updated:** 2026-10-10  

**Source:** [mcp_server/tools/project_tools.py](../../../mcp_server/tools/project_tools.py), [phase_tools.py](../../../mcp_server/tools/phase_tools.py)  
**Tests:** [tests/mcp_server/unit/tools/test_project_tools.py](../../../tests/mcp_server/unit/tools/test_project_tools.py), [tests/mcp_server/unit/tools/test_transition_phase_tool.py](../../../tests/mcp_server/unit/tools/test_transition_phase_tool.py), [tests/mcp_server/unit/tools/test_force_phase_transition_tool.py](../../../tests/mcp_server/unit/tools/test_force_phase_transition_tool.py)  

---

## Purpose

Complete reference documentation for project lifecycle and phase management tools. The tools provide workflow initialization, complete planning queries and mutations, and phase/cycle transitions with configured admission and gates.

Phase state persists in [.pgmcp/state.json](../../../.pgmcp/state.json) and workflow definitions / planning deliverables persist in [.pgmcp/deliverables.json](../../../.pgmcp/deliverables.json). Both files are branch-local artifacts synchronized with git branch operations and neutralized before PR submission.

---

## Overview

The core project/phase tools are:

| Tool | Purpose | Key Feature |
|------|---------|-------------|
| `initialize_project` | Initialize project with workflow selection | Human selects workflow type |
| `get_project_plan` | Inspect project phase plan | Read-only complete planning query |
| `save_planning_deliverables` | Save the initial complete plan | Server-derived references |
| `update_planning_deliverables` | Mutate complete planning blocks | Explicit operations and Git protection |
| `transition_phase` | Sequential phase transition | Strict validation |
| `force_phase_transition` | Skip phases (emergency) | Requires reason + human approval |

All tools interact with:
- **PhaseStateEngine:** Phase state tracking and validation
- **[.pgmcp/config/workflows.yaml](../../../.pgmcp/config/workflows.yaml):** Workflow definitions (feature, bug, docs, refactor, hotfix, chore, epic)
- **[.pgmcp/state.json](../../../.pgmcp/state.json):** Current branch state (branch-local artifact, committed with branch history; neutralized by `submit_pr`)
- **[.pgmcp/deliverables.json](../../../.pgmcp/deliverables.json):** Workflow definition and planning deliverables (branch-local artifact)

---

## API Reference

### initialize_project

**MCP Name:** `initialize_project`  
**Class:** `InitializeProjectTool`  
**File:** [mcp_server/tools/project_tools.py](../../../mcp_server/tools/project_tools.py)

Initialize project with phase plan selection. The configured `workflow_name` selects the project-specific phase plan.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issue_number` | `int` | **Yes** | GitHub issue number |
| `issue_title` | `str` | **Yes** | Issue title |
| `workflow_name` | `str` | **Yes** | Workflow name. Valid values are populated at runtime from `contracts.yaml` via enum injection (C3 A4 override). Examples: `"feature"`, `"bug"`, `"docs"`, `"refactor"`, `"hotfix"`, `"chore"`, `"epic"`. |
| `parent_branch` | `str` | No | Parent branch this feature/bug branches from (auto-detected from git reflog if not provided) |
| `custom_phases` | `list[str]` | No | Optional required-phase override stored in the selected configured project plan. It does not register a workflow or change strict contract transition order. |
| `skip_reason` | `str` | **Conditional** | Required audit justification when `custom_phases` is provided |

#### Workflow Types

| Workflow | Phases | Use Case |
|----------|--------|----------|
| `feature` | research → design → planning → implementation → validation → documentation → ready | New feature development |
| `bug` | research → design → planning → implementation → validation → documentation → ready | Bug fixes |
| `docs` | planning → documentation → ready | Documentation-only changes |
| `refactor` | research → design → planning → implementation → validation → documentation → ready | Code refactoring |
| `hotfix` | implementation → validation → documentation → ready | Emergency fixes |
| `chore` | research → implementation → validation → documentation → ready | Lightweight maintenance and housekeeping |
| `epic` | See `contracts.yaml` for the configured phase order | Multi-issue coordination |

#### Returns (via MCP Resource Cache)

`initialize_project` presents the realized issue, workflow, branch, initial phase, parent,
execution mode, and bounded `required_phases` and `files_created` collections. The
complete `InitializeProjectOutput` remains available through the resource link.

The DTO is stored in the MCP Resource cache at `pgmcp://cache/runs/{run_id}` and contains the following fields:
- `success`: `bool`
- `error_message`: `string | null`
- `post_tool_instruction`: `string | null`
- `issue_number`: `int`
- `workflow_name`: `string`
- `branch`: `string`
- `initial_phase`: `string`
- `parent_branch`: `string | null`
- `required_phases`: `list[string]`
- `execution_mode`: `string`
- `files_created`: `list[string]`

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

#### Behavior Notes

- **State Persistence:** Writes project metadata and branch state separately. Each file uses its existing persistence path; there is no transaction spanning both files.
- **Parent Branch Auto-Detection:** If `parent_branch` not provided, attempts detection via `git reflog`
- **Branch Validation:** Current branch must match pattern `<type>/<issue_number>-*`
- **Same-Branch Guard:** Existing same-branch state is rejected before project metadata can be overwritten. The direct branch initializer uses the same guard. Absent/other-branch state and the existing recovery route after PR closure remain supported; initialization does not unlock an open PR.
- **Configured workflow required:** `custom_phases` does not create an arbitrary workflow; `workflow_name` must exist in `contracts.yaml`, and strict transitions use that configured contract

#### Workflow Responsibility

`initialize_project` **must be called by `@co` (coordination role)** as part of the start-issue lifecycle, always after `create_branch` and `git_checkout`.

`@imp` (implementation role) always inherits a branch where `initialize_project` has already completed. If `@imp` reaches a branch without `.pgmcp/state.json`, this is a process violation — `@imp` must **not** call `initialize_project` as recovery; it must stop and report the blocker so `@co` can correct the lifecycle.


---

### get_project_plan

**MCP Name:** `get_project_plan`  
**Class:** `GetProjectPlanTool`  
**File:** [mcp_server/tools/project_tools.py](../../../mcp_server/tools/project_tools.py)

Get project phases and complete stored planning deliverables for an issue.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issue_number` | `int` | **Yes** | GitHub issue number |

#### Returns (via MCP Resource Cache)

`get_project_plan` presents the issue and workflow followed by bounded phase records.
Each phase shows its name and status; configured child collections show task ID, title,
and status. Phase and task order is preserved from the DTO.

The DTO is stored in the MCP Resource cache at `pgmcp://cache/runs/{run_id}` and contains the following fields:
- `success`: `bool`
- `error_message`: `string | null`
- `post_tool_instruction`: `string | null`
- `issue_number`: `int`
- `workflow_name`: `string`
- `phases`: `list[PhaseDTO]`, where each phase contains:
  - `name`: `string`
  - `status`: `string`
  - `tasks`: `list[PhaseTaskDTO]` with `id`, `title`, and `status`
- `planning_deliverables`: optional `StoredPlanningModel`, containing ordered cycles with server-derived references, names, complete deliverables and exit criteria, plus configured non-cycle phase blocks keyed by phase name. It is absent from the compact cache JSON when planning has not yet been saved. Invalid stored planning returns a failed result; it is never silently omitted from a successful partial plan.

#### Reading large cached plans

The response includes the run-specific `pgmcp://cache/runs/{run_id}` URI. If the
complete result exceeds the configured cache-read budget, the presentation also points
to `pgmcp://docs/cache-reading`. That packaged guide defines the bounded window,
integrity, truncation, and retry protocol. It is available without a repository checkout.
If this read-only plan query's cached result has expired, repeat `get_project_plan` and
start again from the new run URI; never combine windows from separate runs.

#### Example Usage

```json
{
  "issue_number": 123
}
```

#### Behavior Notes

- **Planning Read:** Does not rewrite or back up the deliverables source during queries, including invalid-envelope failures. Current-phase enrichment retains the existing workflow-state resolver behavior.
- **Plan Access:** Reads the configured project plan and returns phases plus the complete stored planning payload; existing phase/task presentation remains unchanged.
- **Not Found:** Returns error if project not initialized

---

### transition_phase

**MCP Name:** `transition_phase`  
**Class:** `TransitionPhaseTool`  
**File:** [mcp_server/tools/phase_tools.py](../../../mcp_server/tools/phase_tools.py)

Transition branch to next phase (strict sequential validation).

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `branch` | `str` | **Yes** | Branch name (e.g., `"feature/123-oauth"`) |
| `to_phase` | `str` | **Yes** | Target phase to transition to. Run `get_work_context()` to see valid phases for the current branch; enum is injected at runtime from `workphases.yaml`. |
| `human_approval_message` | `str` | No | Optional human approval message (audit trail) |
| `resume_cycle` | `str` | Conditional | Existing current-plan `cycle_id` (`"C_2"`, for example), required on re-entry to a cycle-based phase; see cycle entry below. |

#### Returns

The bounded text confirms `from_phase`, `to_phase`, `branch`, and passing/skipped gate
counts. When gates were skipped, up to 20 skipped-gate identifiers are listed inline;
the complete `passing_gates` and `skipped_gates` sequences remain in the cached
`PhaseTransitionOutput` DTO.

#### Example Usage

**Sequential transition:**
```json
{
  "branch": "feature/123-oauth",
  "to_phase": "design"
}
```

Use the next phase allowed by the branch's configured workflow and current state. A
sequential transition cannot skip intervening phases; use the separately documented
force-transition operation when its explicit approval contract applies.

#### Behavior Notes

- **Sequential Validation:** Target phase must be the **next** phase in workflow (no skipping)
- **State Update:** Updates `.pgmcp/state.json` atomically
- **Branch-Local State:** Updates `.pgmcp/state.json` for the active branch only
- **Required Next Step:** On success, the response appends `🚀 REQUIRED NEXT STEP: Call get_work_context now before any other tool call to load the current phase context for this branch.`
- **Not Initialized:** Returns error if project not initialized

---

### force_phase_transition

**MCP Name:** `force_phase_transition`  
**Class:** `ForcePhaseTransitionTool`  
**File:** [mcp_server/tools/phase_tools.py](../../../mcp_server/tools/phase_tools.py)

Force non-sequential phase transition (skip/jump with reason and human approval).

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `branch` | `str` | **Yes** | Branch name (e.g., `"feature/123-oauth"`) |
| `to_phase` | `str` | **Yes** | Target phase to transition to (can skip phases). Run `get_work_context()` to see valid phases for the current branch; enum is injected at runtime from `workphases.yaml`. |
| `skip_reason` | `str` | **Yes** | Reason for skipping validation (audit trail) — must be non-empty (min_length=1) |
| `human_approval_message` | `str` | **Yes** | Human approval message (REQUIRED for forced transitions) — must be non-empty (min_length=1) |
| `resume_cycle` | `str` | Conditional | Existing current-plan `cycle_id` (`"C_2"`, for example), required on re-entry to a cycle-based phase; see cycle entry below. |

#### Returns

The bounded text contains the normal transition fields and gate evidence plus
`skip_reason` and `human_approval_message`. The complete structured
`ForcePhaseTransitionOutput` is stored in the resource cache.

#### Example Usage

```json
{
  "branch": "feature/123-oauth",
  "to_phase": "implementation",
  "skip_reason": "Urgent fix requires an approved skip of intermediate phases",
  "human_approval_message": "Approved by the project owner for this specific phase skip"
}
```

#### Behavior Notes

- **Forced Transition:** Bypasses normal exit gates and sequential ordering. Required approval and cycle-entry validity still apply; an invalid or missing resumption target is rejected before any state write.
- **Branch-Local State:** Updates `.pgmcp/state.json` for the active branch; forced-transition metadata stays in that branch-local state
- **Required Next Step:** On success, the response appends `🚀 REQUIRED NEXT STEP: Call get_work_context now before any other tool call to load the current phase context for this branch.`
- **Use Sparingly:** Intended for emergency situations only
- **Required Fields:** Both `skip_reason` and `human_approval_message` are REQUIRED (not optional)

---

### Entering or resuming a cycle-based phase

Both phase-transition tools validate the complete current plan and cycle selection
before changing state, transition history, or sub-phase context. First entry without
prior cycle state/history selects `C_1`; an explicitly supplied first-entry target must
also be `C_1`. Re-entry requires an explicit existing `resume_cycle` from the current
plan. Non-cycle targets do not admit this field.

For example, after an approved return to Planning and a complete-block mutation:

```json
{
  "branch": "feature/123-oauth",
  "to_phase": "implementation",
  "resume_cycle": "C_2"
}
```

Successful entry sets `current_cycle` to the selected number, clears `last_cycle`
and the sub-phase context, and preserves factual cycle history. Planning mutations
do not change workflow position. Git evidence protects cycle numbering, not completion;
a previously active cycle alone is not protected against planning changes.

---

### transition_cycle and force_cycle_transition

`transition_cycle(to_cycle, issue_number?)` advances sequentially to the next planned
implementation cycle. `force_cycle_transition(to_cycle, skip_reason,
human_approval_message, issue_number?)` permits a skip or backward transition with an
explicit audit trail.

Both responses present the source and target cycle, total cycle count, cycle name,
branch, and passing/skipped gate counts. Up to 20 skipped-gate identifiers are rendered
when present. The force response additionally shows the reason and approval. Complete
gate sequences remain in the cached `CycleTransitionOutput` or
`ForceCycleTransitionOutput` DTO. A successful transition instructs the caller to reload
`get_work_context` before another governed operation.

---

## State Management

### save_planning_deliverables

**MCP Name:** `save_planning_deliverables`  
**Class:** `SavePlanningDeliverablesTool`  
**File:** [mcp_server/tools/project_tools.py](../../../mcp_server/tools/project_tools.py)

Save the complete initial plan once. The bundled [enforcement policy](../../../.pgmcp/config/enforcement.yaml)
admits both planning mutation tools only in Planning; admission uses the existing
configured mechanism rather than a hardcoded phase check.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issue_number` | positive `int` | **Yes** | Initialized issue to plan |
| `planning_deliverables` | `SavePlanningModel` | **Yes** | Complete named blocks, using the input shape below |

Supply ordered named cycles and/or configured non-cycle phase blocks:

```json
{
  "issue_number": 123,
  "planning_deliverables": {
    "cycles": {
      "cycles": [
        {
          "cycle_name": "Authentication",
          "deliverables": [
            {
              "deliverable_name": "Authentication service",
              "description": "Implement the configured authentication boundary",
              "validates": {"type": "file_exists", "file": "backend/services/auth_service.py"}
            }
          ],
          "exit_criteria": "Authentication behavior is verified"
        }
      ]
    },
    "phases": {
      "validation": {
        "deliverables": [
          {
            "deliverable_name": "Validation report",
            "description": "Record observed validation outcomes"
          }
        ]
      }
    }
  }
}
```

- Each cycle requires `cycle_name`, a nonempty complete `deliverables` list and
  `exit_criteria`. Each deliverable requires `deliverable_name` and `description`;
  `validates` is optional.
- Each phase block contains its complete nonempty `deliverables` list. Phase names
  must belong to the selected workflow, and its cycle-based phase uses `cycles`.
- A workflow may contain zero or one cycle-based phase. Supply `cycles` when it has
  one; omit the key when it has none. Explicit `null` is rejected. At least one
  planning block must remain.
- Callers do not supply totals, numeric cycle positions, or stored identifiers.
  The server derives and persists contiguous `C_1`, `C_2`, … cycle references,
  `D_1.1`, `D_1.2`, … within a cycle and `D_1`, `D_2`, … within each phase.
  Deliverable references are local to their enclosing block; names describe content
  and are not global lookup keys.

#### Validation rules

The [planning values](../../../mcp_server/schemas/deliverables.py) admit exactly the
fields required for each `validates.type`:

| Type | Required fields besides `type` |
|------|---------------------------------|
| `file_exists` | `file` |
| `file_glob` | `dir`, `pattern` |
| `contains_text`, `absent_text` | `file`, `text` |
| `key_path` | `file`, `path` |

For example: `{"type":"file_glob","dir":"mcp_server","pattern":"**/*.py"}`.
The common final-plan validation runs before persistence for both save and update.
The live deliverable-gate resolver reads the current plan and passes these rules to
the existing checker. The planning document's scaffold context is a separate authoring
schema: discover it with `scaffold_schema(artifact_type="planning")`, and use returned
planning references in the document rather than inventing command identifiers.

#### Returns (via MCP Resource Cache)

Successful save and update responses use `PlanningDeliverablesOutput`:

- `success`, `error_message`, `post_tool_instruction`, `issue_number`;
- `error_code` for structured failures;
- `total_cycles`, `total_deliverables`;
- `cycles`: summaries with `cycle_id`, `cycle_number`, `cycle_name` and `deliverables_count`;
- `planning_deliverables`: the complete persisted `StoredPlanningModel`.

Successful counts and references come from persisted readback, using the same complete
representation as `get_project_plan` and direct file reads. A rejected command does
not persist its candidate plan. A failed post-write readback reports
`planning_readback_failed`; it does not claim that persistence was rolled back.
Failure counts do not describe an existing plan; query it explicitly if needed.

### update_planning_deliverables

**MCP Name:** `update_planning_deliverables`  
**Class:** `UpdatePlanningDeliverablesTool`  
**File:** [mcp_server/tools/project_tools.py](../../../mcp_server/tools/project_tools.py)

Apply explicit operations to an existing saved plan. Each replacement supplies the
whole cycle or phase block; omitted blocks stay unchanged.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issue_number` | positive `int` | **Yes** | Initialized issue with a saved plan |
| `operations` | nonempty list | **Yes** | Discriminated operations below |
| `force` | `bool` | No | Default `false`; retry evidence and accept continued uncertainty only |

| `op` | Additional fields | Effect |
|--------|-------------------|--------|
| `append_cycle` | `cycle` | Append one complete named cycle |
| `replace_cycle` | `cycle_id`, `cycle` | Replace an existing complete cycle |
| `remove_cycle` | `cycle_id` | Explicitly delete an existing cycle |
| `set_phase` | `phase`, `block` | Create or replace a complete configured non-cycle phase block |
| `remove_phase` | `phase` | Explicitly delete an existing phase block |

Here `cycle` and `block` use the save authoring shapes. All targets resolve against
the original plan snapshot before renumbering; missing or duplicate targets reject
the whole request. Surviving cycles retain their order; appended cycles follow them
in request order. The server regenerates identifiers and totals for the final plan.
Null values are not deletion requests, and there is no per-deliverable merge.
The following example assumes the saved plan contains an unprotected `C_2` whose
removal does not renumber a protected survivor.

```json
{
  "issue_number": 123,
  "operations": [
    {
      "op": "set_phase",
      "phase": "documentation",
      "block": {
        "deliverables": [
          {
            "deliverable_name": "API reference",
            "description": "Reconcile the active authentication reference"
          }
        ]
      }
    },
    {"op": "remove_cycle", "cycle_id": "C_2"}
  ]
}
```

#### Git protection and force

Every update attempts fresh local Git evidence, including phase-only updates and
`force=true` calls. Traversal starts at the captured active-branch HEAD and examines
its reachable history without a fixed commit-count limit, network fetch, other refs
or merge-base cutoff. Exact issue subjects and the shared configured scope decoder
identify committed cycles in the workflow's cycle-based execution phase. Other phases,
other issues and body-only markers do not protect cycles.

A commit-evidenced cycle cannot be deleted or renumbered. Its complete content may
be replaced if its identifier/number remains fixed. For example, removing `C_2`
would renumber `C_3` and is rejected if `C_3` has qualifying commits.

Unavailable or incomplete evidence (for example, a shallow checkout, detached HEAD,
a traversal error or an undecodable exact-issue scope) blocks an ordinary update.
Investigate first. `force=true` retries the evidence query and permits writing only
if uncertainty persists; it never overrides known committed cycles, invalid final
planning or snapshot/issue identity checks. Operation notes report the evidence
status, captured HEAD, known protected cycles and any accepted uncertainty override.

The [ProjectManager](../../../mcp_server/managers/project_manager.py) receives a narrow
read-only evidence dependency; [GitManager](../../../mcp_server/managers/git_manager.py)
owns configured interpretation and the Git adapter owns traversal. Planning value
models perform no Git or state IO. Writes use the existing snapshot check and atomic
file persistence, without a cross-process or cross-file transaction promise.

The response contract is the same as save. Existing workspaces must explicitly adopt
the new input and stored formats; no compatibility merge or automatic migration is supplied.

---

### .pgmcp/state.json

Current branch state (runtime, branch-local, neutralized before PR submission):

```json
{
  "schema_version": "1.0.0",
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
  "transitions": []
}
```

**Behavior:**
- Validated at load-time by `StateVersionValidator` against expected SemVer `1.0.0`.
- Updated by `initialize_project`, `transition_phase`, and `force_phase_transition`.
- On schema version mismatch or file corruption, `StateVersionValidator` performs a Clean Break: backs up the file to `state.json.bak` and raises a `ConfigError` without fallback git-log reconstruction.
- Synchronized by `git_checkout` (loads state when switching branches).
- Treated as a branch-local artifact and neutralized before `submit_pr`.
---

### .pgmcp/deliverables.json

Workflow definition and planning deliverables (branch-local artifact):

```json
{
  "schema_version": "1.0.0",
  "projects": {
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
        "cycles": {
          "total": 1,
          "cycles": [
            {
              "cycle_id": "C_1",
              "cycle_number": 1,
              "cycle_name": "Authentication",
              "deliverables": [
                {
                  "deliverable_id": "D_1.1",
                  "deliverable_name": "Authentication service",
                  "description": "Implement the configured authentication boundary"
                }
              ],
              "exit_criteria": "Authentication behavior is verified"
            }
          ]
        },
        "phases": {
          "validation": {
            "deliverables": [
              {
                "deliverable_id": "D_1",
                "deliverable_name": "Validation report",
                "description": "Record observed validation outcomes"
              }
            ]
          }
        }
      }
    }
  }
}
```

**Behavior:**
- Wrapped in a top-level `"schema_version": "1.0.0"` envelope and validated by `StateVersionValidator` on load.
- Initialized by `initialize_project`.
- Initial planning is saved once; updates replace or explicitly remove complete blocks and derive references/totals before persistence.
- On schema version mismatch or corruption, `StateVersionValidator` backs up to `deliverables.json.bak` and raises `ConfigError`.
- Treated as a branch-local artifact and neutralized before `submit_pr`.
---
---

## Workflow Definitions

### .pgmcp/config/workflows.yaml

> **Note (Issue #271):** Phase membership and ordering are no longer defined in `workflows.yaml`. The file now contains only workflow metadata (name, description, execution mode). Phase sequences are exclusively defined in `.pgmcp/config/contracts.yaml`.

```yaml
# .pgmcp/config/workflows.yaml
version: "1.0"
phase_source: ".pgmcp/config/workphases.yaml"

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
    description: "Code refactoring workflow (research → design → planning → implementation → validation → docs)"
    default_execution_mode: interactive

  docs:
    name: docs
    description: "Documentation-only workflow (planning → docs)"
    default_execution_mode: interactive

  chore:
    name: chore
    description: "Lightweight maintenance workflow"
    default_execution_mode: interactive

  epic:
    name: epic
    description: "Epic workflow for large initiatives (research → planning → design → coordination → documentation)"
    default_execution_mode: interactive

```


For the phase sequences per workflow, see `.pgmcp/config/contracts.yaml`. For the complete extension procedure, see [Adding a First-Class Workflow](../workflow-extension-guide.md).

---

## Integration with Git Tools

Phase state is **synchronized** with git branch operations:

| Git Operation | Phase State Behavior |
|---------------|---------------------|
| `git_checkout` | Loads phase state from `.pgmcp/state.json` after switching branches |
| `create_branch` | No phase state (must run `initialize_project` after) |
| `git_delete_branch` | Removes phase state from `.pgmcp/state.json` |

---

## Workflow examples

Use `get_work_context` and the current project, phase, and cycle tool schemas for the active branch. The workflow order and required evidence come from `.pgmcp/config/contracts.yaml` and the stored project plan; avoid copying a fixed sequence of tool calls into this reference.

## Related Documentation

- [README.md](README.md) — MCP Tools navigation index
- [git.md](git.md) — Git workflow tools (branch, checkout, commit)
- [.pgmcp/config/workflows.yaml](../../../.pgmcp/config/workflows.yaml) — Workflow definitions
- [.pgmcp/state.json](../../../.pgmcp/state.json) — Current branch state
- [.pgmcp/deliverables.json](../../../.pgmcp/deliverables.json) — Workflow definition and planning deliverables
- [docs/development/issue268/validation.md](../../development/archive/issue268/validation.md) — Validation evidence for the delivered phase-state and `get_work_context` contract

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 3.3 | 2026-10-10 | @imp documenter | Reconcile complete-block planning, persisted references, Git protection, explicit cycle resumption and initialization guard (#491) |
| 3.1 | 2026-08-22 | Agent | Align project, transition, and planning output projections with structured DTOs |
| 3.0 | 2026-07-21 | Agent | Update state management sections with dynamic state file version validation and Clean Break strategy (#438) |
| 2.2 | 2026-06-11 | Agent | Rename tdd_cycles to cycles in project planning deliverables schema |
| 2.1 | 2026-05-24 | Agent | Document the required `get_work_context` follow-up note on successful phase transitions |
| 2.0 | 2026-02-08 | Agent | Complete reference for 4 project/phase tools: initialize, inspect, transition, force-transition |

