<!-- docs\development\issue413\tools_error_mapping_research.md -->
<!-- template=research version=8b7bb3ab created=2026-06-27T20:04Z updated= -->
# Tools Error Mapping and Exception Segregation Research

**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-06-27

---

## Problem Statement

Expected tool execution failures (such as invalid parameter values or lock timeouts) are currently treated as unhandled exceptions and transformed into generic system-level ExecutionErrorOutput DTOs with tracebacks, violating SRP, SOLID, and the Presentation Boundary.

## Research Goals

- Analyze all 20 MCP tool implementations for error handling and try-except blocks
- Classify all tool failure cases into the 5 target architecture error categories
- Define the approved exception-to-DTO translation strategy for decorators and core tools

---

## Background

During the refactoring of Issue #413, local try-except blocks were removed from core tools to let exceptions bubble up. However, this caused predictable value errors (e.g. invalid regex patterns, line numbers out of bounds) and lock timeouts to bubble up as unhandled exceptions, resulting in system-level ExecutionErrorOutput with tracebacks rather than structured ValidationErrorOutput or EnforcementErrorOutput.

---

## Findings

All 20 MCP tool implementations have been analyzed. A key gap was identified: `InputValidationDecorator` only catches `pydantic.ValidationError`, meaning custom `ValidationError` exceptions raised during execution bubble past it and get mapped to `ExecutionErrorOutput` (with traceback). We must update `InputValidationDecorator` to catch project-level `ValidationError` exceptions.

### 🔧 Comprehensive Tools Mapping

#### 1. `admin_tools.py`
Contains administrative tools for server lifecycle events.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **RestartServerTool** (`restart_server`) | Invalid or extra parameters. | Pydantic validation error. | **1. Schema Validation** $\rightarrow$ `ValidationErrorOutput` |
| **verify_server_restarted** *(Helper)* | Missing `server_root` and `MCP_CONFIG_ROOT` env var. | Raises `ValueError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **verify_server_restarted** *(Helper)* | Marker file not found or corrupted JSON/read error. | Returns dictionary with `restarted=False` and error details. | **5. Logical Failure** $\rightarrow$ success DTO with `passed=False` |

#### 2. `cycle_tools.py`
Contains developmental cycle transition tools.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **TransitionCycleTool** (`transition_cycle`) | Missing/invalid fields in input. | Pydantic validation error. | **1. Schema Validation** $\rightarrow$ `ValidationErrorOutput` |
| **TransitionCycleTool** (`transition_cycle`) | Cannot detect issue number from branch name. | Returns `ValidationErrorOutput`. | **2. Semantic Validation** $\rightarrow$ `ValidationErrorOutput` |
| **TransitionCycleTool** (`transition_cycle`) | Concurrency/state conflict during transition (`StateMutationConflictError`). | Catches error; returns `ExecutionErrorOutput`. | **2. Semantic Validation** $\rightarrow$ `ValidationErrorOutput` |
| **TransitionCycleTool** (`transition_cycle`) | Quality gate violation (`GateViolation`). | Catches error; returns `ExecutionErrorOutput`. | **3. Policy/Preflight Failure** $\rightarrow$ `EnforcementErrorOutput` |
| **TransitionCycleTool** (`transition_cycle`) | Standard exceptions (`ValueError`, `OSError`, `RuntimeError`, `KeyError`). | Catches error; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **ForceCycleTransitionTool** (`force_cycle_transition`) | Missing/invalid fields in input. | Pydantic validation error. | **1. Schema Validation** $\rightarrow$ `ValidationErrorOutput` |
| **ForceCycleTransitionTool** (`force_cycle_transition`) | Cannot detect issue number from branch name. | Returns `ValidationErrorOutput`. | **2. Semantic Validation** $\rightarrow$ `ValidationErrorOutput` |
| **ForceCycleTransitionTool** (`force_cycle_transition`) | Concurrency/state conflict during transition (`StateMutationConflictError`). | Catches error; returns `ExecutionErrorOutput`. | **2. Semantic Validation** $\rightarrow$ `ValidationErrorOutput` |
| **ForceCycleTransitionTool** (`force_cycle_transition`) | Quality gate violation (`GateViolation`). | Catches error; returns `ExecutionErrorOutput`. | **3. Policy/Preflight Failure** $\rightarrow$ `EnforcementErrorOutput` |
| **ForceCycleTransitionTool** (`force_cycle_transition`) | Standard exceptions (`ValueError`, `OSError`, `RuntimeError`, `KeyError`). | Catches error; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |

#### 3. `discovery_tools.py`
Contains documentation indexing and AI self-orientation tools.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **SearchDocumentationTool** (`search_documentation`) | Invalid search scope pattern. | Pydantic validation error. | **1. Schema Validation** $\rightarrow$ `ValidationErrorOutput` |
| **SearchDocumentationTool** (`search_documentation`) | Docs directory does not exist. | Produces Recovery Notes and raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` |
| **GetWorkContextTool** (`get_work_context`) | Git / state read failures during execution. | Let exceptions bubble. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` |
| **GetWorkContextTool** (`get_work_context`) | Active branch moved to an invalid phase. | Returns successfully with `invalid_phase_warning` text. | **5. Logical Failure** $\rightarrow$ success DTO with `passed=False` (as a warning field) |

#### 4. `git_analysis_tools.py`
Contains tools for inspecting repository branch structure and diffs.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **GitListBranchesTool** (`git_list_branches`) | Git executable unavailable or system error. | Let exceptions bubble. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` |
| **GitDiffTool** (`git_diff_stat`) | Comparison branch doesn't exist or git command fails. | Let exceptions bubble. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` |

#### 5. `git_fetch_tool.py`
Contains tools for fetching remote updates.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **GitFetchTool** (`git_fetch`) | Network timeout or git command error. | Let exceptions bubble. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` |

#### 6. `git_pull_tool.py`
Contains tools for pulling remote updates.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **GitPullTool** (`git_pull`) | Merge conflicts or pull timeout. | Let exceptions bubble. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` |
| **GitPullTool** (`git_pull`) | Phase state sync fails after pulling. | Catches `(MCPError, ValueError, OSError, StateBranchMismatchError)`, logs warning, and continues. | *Suppressed internally* |

#### 7. `git_tools.py`
Contains core git workflow tools.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **CreateBranchTool** (`create_branch`) | Invalid base branch or git command fails. | Catches `Exception`; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **GitStatusTool** (`git_status`) | Git command fails. | Catches `Exception`; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **GitCommitTool** (`git_add_or_commit`) | State file missing or mismatched during phase auto-detection. | Catches `(FileNotFoundError, StateBranchMismatchError)`; returns `ExecutionErrorOutput`. | **2. Semantic Validation** / **3. Policy Failure** $\rightarrow$ `ValidationErrorOutput` / `EnforcementErrorOutput` |
| **GitCommitTool** (`git_add_or_commit`) | Committing in cycle-based phase without a cycle number. | Returns `ExecutionErrorOutput`. | **2. Semantic Validation** $\rightarrow$ `ValidationErrorOutput` |
| **GitCommitTool** (`git_add_or_commit`) | Phase or cycle mismatch guard violation. | Catches guard exception; returns `ExecutionErrorOutput`. | **3. Policy/Preflight Failure** $\rightarrow$ `EnforcementErrorOutput` |
| **GitCommitTool** (`git_add_or_commit`) | Commit execution fails (e.g. git lock, invalid file path). | Catches `Exception`; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **GitRestoreTool** (`git_restore`) | Invalid file list or git command fails. | Catches `Exception`; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **GitCheckoutTool** (`git_checkout`) | Checkout fails (e.g. dirty working directory). | Catches `Exception`; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **GitCheckoutTool** (`git_checkout`) | Phase state sync fails after checkout. | Catches `(MCPError, ValueError, OSError, StateBranchMismatchError)`, logs warning, and continues. | *Suppressed internally* |
| **GitPushTool** (`git_push`) | Push command fails. | Catches `Exception`; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **GitMergeTool** (`git_merge`) | Merge conflicts or failed merge command. | Catches `Exception`; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **GitDeleteBranchTool** (`git_delete_branch`) | Cannot delete protected/current branch or git fails. | Catches `Exception`; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **GitStashTool** (`git_stash`) | Stash command fails. | Catches `Exception`; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **GetParentBranchTool** (`parent_branch`) | `PhaseStateEngine` not injected. | Returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` |
| **GetParentBranchTool** (`parent_branch`) | Branch state not found. | Catches `Exception`; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **CheckMergeTool** (`check_merge`) | Git command fails or invalid SHA. | Catches `Exception`; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |

#### 8. `health_tools.py`
Contains health check tools.

* There are no failure cases or exceptions in `HealthCheckTool` (`health_check`).

#### 9. `issue_tools.py`
Contains GitHub Issue management tools.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **CreateIssueTool** (`create_issue`) | Issue validation parameters fail (e.g. invalid type, title length). | Catches `ValueError` from validator; raises `ExecutionError`. | **2. Semantic Validation** $\rightarrow$ `ValidationErrorOutput` |
| **CreateIssueTool** (`create_issue`) | Label assembly fails. | Catches `ValueError` from label manager; raises `ExecutionError`. | **2. Semantic Validation** $\rightarrow$ `ValidationErrorOutput` |
| **CreateIssueTool** (`create_issue`) | GitHub API call fails. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **GetIssueTool** (`get_issue`) | GitHub API call fails or issue not found. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **ListIssuesTool** (`list_issues`) | GitHub API call fails. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **UpdateIssueTool** (`update_issue`) | GitHub API call fails or invalid issue number. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **CloseIssueTool** (`close_issue`) | GitHub API call fails. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |

#### 10. `label_tools.py`
Contains GitHub Label management tools.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **ListLabelsTool** (`list_labels`) | GitHub API call fails. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **CreateLabelTool** (`create_label`) | Invalid label name naming pattern. | Raises `ExecutionError`. | **2. Semantic Validation** $\rightarrow$ `ValidationErrorOutput` |
| **CreateLabelTool** (`create_label`) | Phase label value not in known workphases. | Raises `ExecutionError`. | **2. Semantic Validation** $\rightarrow$ `ValidationErrorOutput` |
| **CreateLabelTool** (`create_label`) | Color code includes `#` prefix. | Raises `ExecutionError`. | **1. Schema Validation** $\rightarrow$ `ValidationErrorOutput` |
| **CreateLabelTool** (`create_label`) | Color code regex hex pattern fails. | Raises `ExecutionError`. | **1. Schema Validation** $\rightarrow$ `ValidationErrorOutput` |
| **CreateLabelTool** (`create_label`) | GitHub API call fails. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **DeleteLabelTool** (`delete_label`) | Label doesn't exist or GitHub API fails. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **RemoveLabelsTool** (`remove_labels`) | GitHub API call fails. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **AddLabelsTool** (`add_labels`) | Target labels are invalid per registry configuration. | Raises `ExecutionError`. | **2. Semantic Validation** $\rightarrow$ `ValidationErrorOutput` |
| **AddLabelsTool** (`add_labels`) | Phase label value not in known workphases. | Raises `ExecutionError`. | **2. Semantic Validation** $\rightarrow$ `ValidationErrorOutput` |
| **AddLabelsTool** (`add_labels`) | GitHub API call fails. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |

#### 11. `milestone_tools.py`
Contains GitHub Milestone management tools.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **ListMilestonesTool** (`list_milestones`) | GitHub API call fails. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **CreateMilestoneTool** (`create_milestone`) | GitHub API call fails. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **CloseMilestoneTool** (`close_milestone`) | Milestone doesn't exist or GitHub API fails. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |

#### 12. `phase_tools.py`
Contains workflow phase transition tools.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **TransitionPhaseTool** (`transition_phase`) | Concurrency/state conflict during transition (`StateMutationConflictError`). | Catches error; returns `ExecutionErrorOutput`. | **2. Semantic Validation** $\rightarrow$ `ValidationErrorOutput` |
| **TransitionPhaseTool** (`transition_phase`) | Standard exceptions (`ValueError`, `OSError`, `RuntimeError`, `KeyError`). | Catches error; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **ForcePhaseTransitionTool** (`force_phase_transition`) | `skip_reason` or `human_approval` field is empty. | Pydantic `@field_validator` raises `ValueError`. | **1. Schema Validation** $\rightarrow$ `ValidationErrorOutput` |
| **ForcePhaseTransitionTool** (`force_phase_transition`) | Concurrency/state conflict during transition (`StateMutationConflictError`). | Catches error; returns `ExecutionErrorOutput`. | **2. Semantic Validation** $\rightarrow$ `ValidationErrorOutput` |
| **ForcePhaseTransitionTool** (`force_phase_transition`) | Standard exceptions (`ValueError`, `OSError`, `RuntimeError`, `KeyError`). | Catches error; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |

#### 13. `pr_tools.py`
Contains GitHub Pull Request management tools.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **ListPRsTool** (`list_prs`) | GitHub API call fails. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **MergePRTool** (`merge_pr`) | Pull request cannot be merged or GitHub API fails. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **GetPRTool** (`get_pr`) | Pull request doesn't exist or GitHub API fails. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **SubmitPRTool** (`submit_pr`) | Git preflight check or commit preparation fails. | Catches `(PreflightError, ExecutionError)`; raises `ExecutionError`. | **3. Policy Failure** / **4. System Failure** $\rightarrow$ `EnforcementErrorOutput` / `ExecutionErrorOutput` |
| **SubmitPRTool** (`submit_pr`) | PR creation fails (causes local git rollback). | Catches `ExecutionError`; attempts rollback and raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **SubmitPRTool** (`submit_pr`) | Retrieval / mapping of created PR fails. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |

#### 14. `project_tools.py`
Contains project planning and initialization tools.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **InitializeProjectTool** (`initialize_project`) | Workflow name is 'custom' but no custom phases are defined. | Pydantic `@model_validator` raises `ValueError`. | **1. Schema Validation** $\rightarrow$ `ValidationErrorOutput` |
| **InitializeProjectTool** (`initialize_project`) | State or deliverables file writing fails. | Catches `Exception`; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **GetProjectPlanTool** (`get_project_plan`) | No project plan found for the issue. | Returns `ExecutionErrorOutput`. | **5. Logical Failure** $\rightarrow$ success DTO with `passed=False` |
| **GetProjectPlanTool** (`get_project_plan`) | File read error or standard exception. | Catches `(ValueError, OSError)`; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **SavePlanningDeliverablesTool** (`save_planning_deliverables`) | Planning deliverables structure fails schema check. | Pydantic validation error. | **1. Schema Validation** $\rightarrow$ `ValidationErrorOutput` |
| **SavePlanningDeliverablesTool** (`save_planning_deliverables`) | Planning deliverables missing after writing. | Returns `ExecutionErrorOutput`. | **5. Logical Failure** $\rightarrow$ success DTO with `passed=False` |
| **SavePlanningDeliverablesTool** (`save_planning_deliverables`) | File write error or standard exception. | Catches `Exception`; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **UpdatePlanningDeliverablesTool** (`update_planning_deliverables`) | Update model schema check fails. | Pydantic validation error. | **1. Schema Validation** $\rightarrow$ `ValidationErrorOutput` |
| **UpdatePlanningDeliverablesTool** (`update_planning_deliverables`) | Planning deliverables missing after merging. | Returns `ExecutionErrorOutput`. | **5. Logical Failure** $\rightarrow$ success DTO with `passed=False` |
| **UpdatePlanningDeliverablesTool** (`update_planning_deliverables`) | File merge error or standard exception. | Catches `Exception`; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |

#### 15. `quality_tools.py`
Contains quality gate checking and code formatting tools.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **RunQualityGatesTool** (`run_quality_gates`) | Invalid scope/files combination. | Pydantic `@model_validator` raises `ValueError`. | **1. Schema Validation** $\rightarrow$ `ValidationErrorOutput` |
| **RunQualityGatesTool** (`run_quality_gates`) | Concurrency/state mutation conflict (`QualityStateMutationConflictError`). | Catches error; returns `ExecutionErrorOutput`. | **2. Semantic Validation** $\rightarrow$ `ValidationErrorOutput` |
| **RunQualityGatesTool** (`run_quality_gates`) | Quality state save file write fails. | Catches `OSError`; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **RunQualityGatesTool** (`run_quality_gates`) | One or more quality gates fail. | Returns successfully with `overall_pass=False` in DTO. | **5. Logical Failure** $\rightarrow$ success DTO with `passed=False` |
| **AutoFixTool** (`auto_fix`) | Invalid scope/files combination. | Pydantic `@model_validator` raises `ValueError`. | **1. Schema Validation** $\rightarrow$ `ValidationErrorOutput` |
| **AutoFixTool** (`auto_fix`) | Subprocess execution error or file format failure. | Let exceptions bubble. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |

#### 16. `safe_edit_tool.py`
Contains safe file writing and editing tools.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **SafeEditTool** (`safe_edit_file`) | Line range validation fails in LineEdit or InsertLine. | Pydantic `@model_validator` raises `ValueError`. | **1. Schema Validation** $\rightarrow$ `ValidationErrorOutput` |
| **SafeEditTool** (`safe_edit_file`) | Mutually exclusive edit modes violated or incomplete search/replace params. | Pydantic `@model_validator` raises `ValueError`. | **1. Schema Validation** $\rightarrow$ `ValidationErrorOutput` |
| **SafeEditTool** (`safe_edit_file`) | Aggressive mutex lock acquisition timeout (10ms). | Raises `asyncio.TimeoutError` which bubbles up. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` |
| **SafeEditTool** (`safe_edit_file`) | Trying to apply edits/replacements to non-existent file. | Catches `FileNotFoundError`; returns `SafeEditOutput(passed=False)`. | **5. Logical Failure** $\rightarrow$ success DTO with `passed=False` |
| **SafeEditTool** (`safe_edit_file`) | Surgical edit line numbers out-of-bounds or overlapping edits. | Raises `ValueError` inside helper (bubbles up). | **2. Semantic Validation** $\rightarrow$ `ValidationErrorOutput` |
| **SafeEditTool** (`safe_edit_file`) | Search pattern not found (in strict mode). | Returns `SafeEditOutput(passed=False)` with preview. | **5. Logical Failure** $\rightarrow$ success DTO with `passed=False` |
| **SafeEditTool** (`safe_edit_file`) | Invalid regex pattern used for search/replace. | Raises `ValueError` inside regex compiler (bubbles up). | **2. Semantic Validation** $\rightarrow$ `ValidationErrorOutput` |
| **SafeEditTool** (`safe_edit_file`) | Target file content edit validation fails (in strict mode). | Returns `SafeEditOutput(passed=False)` with issue text. | **5. Logical Failure** $\rightarrow$ success DTO with `passed=False` |

#### 17. `scaffold_artifact.py`
Contains unified artifact scaffolding tools.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **ScaffoldArtifactTool** (`scaffold_artifact`) | Template context lacks required schema fields. | Catches `ValidationError`; returns `ValidationErrorOutput`. | **2. Semantic Validation** $\rightarrow$ `ValidationErrorOutput` |
| **ScaffoldArtifactTool** (`scaffold_artifact`) | Configuration registry error or file generation error. | Catches `ConfigError`, `OSError`, `ValueError`, `RuntimeError`, `MCPError`; returns error output DTOs. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |

#### 18. `scaffold_schema_tool.py`
Contains tools for retrieving artifact context schemas.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **ScaffoldSchemaTool** (`scaffold_schema`) | Unknown artifact type registry lookup fails. | Catches `ConfigError`, `ValueError`, `RuntimeError`; returns error output DTOs. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |

#### 19. `template_validation_tool.py`
Contains template structural validation tools.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **TemplateValidationTool** (`validate_template`) | Template structure check fails. | Returns successfully with DTO containing `passed=False`. | **5. Logical Failure** $\rightarrow$ success DTO with `passed=False` |
| **TemplateValidationTool** (`validate_template`) | File read error or invalid template type. | Catches `(ValueError, OSError)`; returns `ExecutionErrorOutput`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |

#### 20. `test_tools.py`
Contains test suite execution tools.

| Tool Name / Helper | Failure Case | Current Behavior | Target Architecture Classification |
| :--- | :--- | :--- | :--- |
| **RunTestsTool** (`run_tests`) | Missing execution parameters or invalid verbose configuration. | Pydantic `@model_validator` raises `ValueError`. | **1. Schema Validation** $\rightarrow$ `ValidationErrorOutput` |
| **RunTestsTool** (`run_tests`) | Pytest subprocess timeout expired. | Catches `Exception`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` |
| **RunTestsTool** (`run_tests`) | Failed to execute test suite runner (e.g. runner executable error). | Catches `OSError`; raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` (let bubble) |
| **RunTestsTool** (`run_tests`) | Pytest exited with critical failure code (`result.should_raise`). | Raises `ExecutionError`. | **4. System/Execution Failure** $\rightarrow$ `ExecutionErrorOutput` |

## Violation Categories & Target Recipes

To streamline the transition from research to implementation, we classify all violations across the 51 tools into five distinct **Violation Categories**. Each category has a unified "Target Recipe" that dictates the exact code modification pattern.

---

### Category A: Internal Python Exceptions raised for Parameter Validation
*   **The Violation**: The tool raises standard Python exceptions (`ValueError`, `KeyError`, `IndexError`) during execution to signal that user arguments are invalid (e.g. invalid regex patterns, line numbers out of bounds, missing required state attributes). Because these bubble up uncaught, the decorator pipeline treats them as unexpected system crashes (`ExecutionErrorOutput`) with tracebacks.
*   **Target Recipe**: Replace the internal `ValueError` or standard exception with a structured project-level `ValidationError` containing **only** an `error_code` and `params`. Under the approved strategy, the `message: str` parameter is removed from the exception constructor to prevent passing hardcoded strings.
*   **Example Code**:
    ```python
    # ❌ WRONG
    raise ValueError(f"Invalid regex pattern: {e}")

    # ✅ CORRECT (Constructor takes no message parameter!)
    from mcp_server.core.exceptions import ValidationError
    raise ValidationError(
        error_code="invalid_regex",
        params={"pattern": params.search, "error": str(e)}
    )
    ```
*   **Affected Tools**: `SafeEditTool`, `GitCommitTool`, `CreateIssueTool`, `CreateLabelTool`, `AddLabelsTool`, `ScaffoldArtifactTool`.

---

### Category B: Redundant Local Wrapping to `ExecutionError`
*   **The Violation**: The tool catches predictable third-party/external API errors (e.g. GitHub client crashes, subprocess file/permission failures) and manually wraps them to raise `ExecutionError` (e.g. `raise ExecutionError(str(e)) from e`). This creates repetitive, un-DRY error handling blocks inside core tools.
*   **Target Recipe**: Delete the local try-except block and let the standard Python exception (or client/API exception) bubble up naturally. The `ToolErrorHandlerDecorator` is exclusively responsible for catching these and formatting them as `ExecutionErrorOutput`.
*   **Example Code**:
    ```python
    # ❌ WRONG
    try:
        issue = self.github_client.get_issue(number)
    except Exception as e:
        raise ExecutionError(str(e)) from e

    # ✅ CORRECT
    issue = self.github_client.get_issue(number)
    ```
*   **Affected Tools**: `CreateIssueTool`, `GetIssueTool`, `ListIssuesTool`, `UpdateIssueTool`, `CloseIssueTool`, `ListLabelsTool`, `CreateLabelTool`, `DeleteLabelTool`, `RemoveLabelsTool`, `AddLabelsTool`, `ListMilestonesTool`, `CreateMilestoneTool`, `CloseMilestoneTool`, `ListPRsTool`, `MergePRTool`, `GetPRTool`, `SubmitPRTool`, `RunTestsTool`.

---

### Category C: Return of Error DTOs from Core Tools
*   **The Violation**: The tool catches exceptions inside `execute` and explicitly instantiates and returns `ExecutionErrorOutput` or `ValidationErrorOutput` DTOs (violating Constraint 3, which states that core tools must only return success DTOs).
*   **Target Recipe**: Remove the try-except block and let the structured project exception (`ValidationError`, `PreflightError`, `EnforcementError`) or standard Python exception bubble up to the decorator pipeline.
*   **Example Code**:
    ```python
    # ❌ WRONG
    try:
        reachable = self.manager.is_ancestor(params.merge_sha)
    except Exception as e:
        return ExecutionErrorOutput(error_message=str(e), params={"merge_sha": params.merge_sha})

    # ✅ CORRECT
    reachable = self.manager.is_ancestor(params.merge_sha)
    ```
*   **Affected Tools**: `CheckMergeTool`, `TransitionCycleTool`, `ForceCycleTransitionTool`, `TransitionPhaseTool`, `ForcePhaseTransitionTool`, `InitializeProjectTool`, `GetProjectPlanTool`, `SavePlanningDeliverablesTool`, `UpdatePlanningDeliverablesTool`, `RunQualityGatesTool`, `ScaffoldSchemaTool`, `TemplateValidationTool`.

---

### Category D: Parameter Validation in Code instead of Pydantic Schema
*   **The Violation**: The tool performs format or type checks on parameters (such as checking regex patterns, color codes, or conflicting modes) during tool execution, which could be validated statically at the presentation boundary before execution starts.
*   **Target Recipe**: Move these validations to a `@field_validator` or `@model_validator` inside the tool's Pydantic Input DTO. This leverages Pydantic's built-in validation pipeline and naturally returns a schema-based `ValidationErrorOutput` before execution.
*   **Example Code**:
    ```python
    # ✅ Move to Input DTO:
    class CreateLabelInput(BaseModel):
        color: str

        @field_validator("color")
        @classmethod
        def validate_hex_color(cls, v: str) -> str:
            if v.startswith("#") or not re.match(r"^[0-9a-fA-F]{6}$", v):
                raise ValueError("Color must be a 6-character hex string without prefix.")
            return v
    ```
*   **Affected Tools**: `CreateLabelTool`, `RunQualityGatesTool`, `AutoFixTool`, `SafeEditTool`, `RunTestsTool`.

---

### Category E: Concurrency Lock and Preflight Failures
*   **The Violation**: The tool catches concurrency state conflicts or mutex acquisition timeouts and returns error DTOs or lets them bubble as standard python exceptions (e.g. `TimeoutError`), producing tracebacks instead of a policy enforcement warning.
*   **Target Recipe**: Catch the concurrency conflict or lock timeout and raise a structured `PreflightError` or `EnforcementError` containing strictly `error_code` and `params` (no message argument).
*   **Example Code**:
    ```python
    # ✅ Catch timeout and raise PreflightError (strictly no message parameter!):
    try:
        async with asyncio.timeout(0.01):
            async with file_lock:
                # ...
    except TimeoutError as e:
        raise PreflightError(
            error_code="file_locked",
            params={"path": params.path}
        ) from e
    ```
*   **Affected Tools**: `SafeEditTool` (lock timeout), `TransitionCycleTool` (state conflict), `ForceCycleTransitionTool` (state conflict), `TransitionPhaseTool` (state conflict), `ForcePhaseTransitionTool` (state conflict), `RunQualityGatesTool` (quality state conflict).

---

## Approved Strategy

1. **Refactor Core Exception Constructors**: 
   Modify the signature of custom structured exceptions in `mcp_server/core/exceptions.py` (specifically `ValidationError`, `PreflightError`, and `EnforcementError`) to **completely remove the `message: str` argument** from their `__init__` methods.
   * Internally, they will call `super().__init__("")` to satisfy the base `MCPError`/`Exception` class, but callers raising these exceptions will strictly only supply `error_code` (or `code`) and `params`.
   * This design-enforces the Presentation Boundary: developers literally cannot write a hardcoded, user-facing error message string when raising validation or policy errors.

2. **Decorator catch-and-translate mapping**:
   * Refactor `InputValidationDecorator` to catch `mcp_server.core.exceptions.ValidationError` (project exception) and map it to `ValidationErrorOutput(validation_errors=exc.code, input_schema=..., params={"error_code": exc.code, **exc.params})`.
   * Refactor decorators to ensure `PreflightError` and `EnforcementError` are translated to `EnforcementErrorOutput` without message fields, relying entirely on `error_code` parameter lookup in `presentation.yaml`.

3. **Core Tool Rollout**:
   * Refactor the 51 core tools by applying the target recipes (A, B, C, D, E) corresponding to their failure cases.
   * Standard Python system exceptions (like `OSError` or `PermissionError`) will bubble up natively to be caught by `ToolErrorHandlerDecorator` as generic `ExecutionErrorOutput`. (These are the only error types allowed to carry raw error messages and tracebacks).

---

## Expected Results

All tools execute without leaking tracebacks for expected parameter or resource lock failures. Parameter validations yield ValidationErrorOutput formatted via presentation.yaml templates. Concurrency timeouts yield EnforcementErrorOutput. Unhandled OS crashes yield ExecutionErrorOutput.

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-27 | Agent | Initial draft |