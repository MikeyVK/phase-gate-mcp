# DTO Contracts & Presentation Templates — Issue #402

This document serves as the Single Source of Truth (SSOT) for the Pydantic DTO contracts and their corresponding presentation templates defined in `presentation.yaml`.

---

## Shared Base Schema

Every DTO schema inherits from `BaseToolOutput` to enforce immutability, disallow extra fields, and guarantee a unified structure for error handling and agent instruction propagation.

```python
from enum import Enum
from pydantic import BaseModel, ConfigDict

class BaseToolOutput(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    success: bool = True
    error_message: str | None = None
    post_tool_instruction: str | None = None
```

---

## Batch 1: Admin, Health & Cycle Tools

### 1. HealthCheckTool

* **DTO (`HealthCheckOutput`):**
  ```python
  class HealthStatus(str, Enum):
      HEALTHY = "healthy"
      UNHEALTHY = "unhealthy"

  class HealthCheckOutput(BaseToolOutput):
      status: HealthStatus = HealthStatus.HEALTHY
      version: str
      pid: int
      platform: str
      uptime_seconds: float
  ```
* **YAML Config:**
  ```yaml
  health_check:
    template_success: |
      {emoji_success} **Server Health Status**
      - Status: {status}
      - Version: {version}
      - Process ID: {pid}
      - Platform: {platform}
      - Uptime: {uptime_seconds} seconds
      *(Full details available in the structured JSON payload)*
    template_failure: "{emoji_failure} Health check failed: {error_message}"
  ```

### 2. RestartServerTool

* **DTO (`RestartServerOutput`):**
  ```python
  class RestartServerOutput(BaseToolOutput):
      reason: str
      pid: int
      timestamp: float
      iso_time: str
  ```
* **YAML Config:**
  ```yaml
  restart_server:
    template_success: "{emoji_success} Server restart initiated successfully (Reason: {reason})."
    template_failure: "{emoji_failure} Restart failed: {error_message}"
    post_tool_instruction: "WAIT 3 SECONDS before calling any other tool. The server needs time to reload."
  ```

### 3. TransitionCycleTool

* **DTO (`CycleTransitionOutput`):**
  ```python
  class CycleTransitionOutput(BaseToolOutput):
      branch: str
      from_cycle: int | None = None
      to_cycle: int
      total_cycles: int
      cycle_name: str
      passed_gates: list[str] = []
      passed_gates_count: int = 0
  ```
* **YAML Config:**
  ```yaml
  transition_cycle:
    template_success: "{emoji_success} Transitioned to TDD Cycle {to_cycle}/{total_cycles}: {cycle_name} on branch '{branch}' (Passed gates: {passed_gates_count})."
    template_failure: "{emoji_failure} Cycle transition failed: {error_message}"
    post_tool_instruction: "Call get_work_context immediately to load the new context for this phase."
  ```

### 4. ForceCycleTransitionTool

* **DTO (`ForceCycleTransitionOutput`):**
  ```python
  class ForceCycleTransitionOutput(BaseToolOutput):
      branch: str
      from_cycle: int
      to_cycle: int
      total_cycles: int
      cycle_name: str
      skip_reason: str
      human_approval: str
      skipped_gates: list[str] = []
      passing_gates: list[str] = []
      skipped_gates_count: int = 0
      passing_gates_count: int = 0
  ```
* **YAML Config:**
  ```yaml
  force_cycle_transition:
    template_success: "{emoji_warning} Forced transition to Cycle {to_cycle}/{total_cycles} ({cycle_name}) on branch '{branch}' (Passed gates: {passing_gates_count}, Skipped gates: {skipped_gates_count}).\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Forced transition failed: {error_message}"
    post_tool_instruction: "Present the skipped gates (found in structuredContent.skipped_gates) to the human moderator for verification before proceeding, then call get_work_context immediately."
  ```
---

## Batch 2: Discovery, Search & Project Tools

### 1. SearchDocumentationTool

* **DTO (`SearchDocumentationOutput`):**
  ```python
  class SearchResultDTO(BaseModel):
      title: str
      path: str
      score: float
      snippet: str
      start_line: int
      end_line: int

  class SearchDocumentationOutput(BaseToolOutput):
      query: str
      scope: str
      results_count: int
      results: list[SearchResultDTO] = []
  ```
* **YAML Config:**
  ```yaml
  search_documentation:
    template_success: "{emoji_query} Found {results_count} documentation matches for query '{query}' in scope '{scope}'.\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Documentation search failed: {error_message}"
  ```

### 2. GetWorkContextTool

* **DTO (`GetWorkContextOutput`):**
  ```python
  class GetWorkContextOutput(BaseToolOutput):
      current_branch: str
      workflow_name: str
      phase: str
      issue_number: int | None = None
      parent_branch: str | None = None
      current_cycle: int | None = None
      sub_phase: str | None = None
      phase_source: str
      phase_confidence: str
      sub_role_hint: str
      phase_instructions: str
      handover_template: str | None = None
      invalid_phase_warning: str | None = None
  ```
* **YAML Config:**
  ```yaml
  get_work_context:
    template_success: |
      Branch: `{current_branch}` | Workflow: {workflow_name} | Issue: #{issue_number}
      Phase: {emoji_phase} {phase} (confidence={phase_confidence})
      Role: {sub_role_hint}
      Parent: {parent_branch}
      *(Full details available in the structured JSON payload)*
    template_failure: "{emoji_failure} Failed to retrieve work context: {error_message}"
    post_tool_instruction: "TODO discipline: create or refresh your TODO list now; keep exactly one item in progress and update it after each material step."
  ```

### 3. InitializeProjectTool

* **DTO (`InitializeProjectOutput`):**
  ```python
  class InitializeProjectOutput(BaseToolOutput):
      issue_number: int
      workflow_name: str
      branch: str
      initial_phase: str
      parent_branch: str | None = None
      required_phases: list[str] = []
      execution_mode: str
      files_created: list[str] = []
  ```
* **YAML Config:**
  ```yaml
  initialize_project:
    template_success: "{emoji_bootstrap} Initialized project for issue #{issue_number} on branch '{branch}' (Initial Phase: '{initial_phase}').\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Project initialization failed: {error_message}"
    post_tool_instruction: "Call get_work_context immediately to load the new context for this phase."
  ```

### 4. GetProjectPlanTool

* **DTO (`ProjectPlanOutput`):**
  ```python
  class ProjectPlanOutput(BaseToolOutput):
      issue_number: int
      workflow_name: str
      phases: list[dict[str, Any]] = []
  ```
* **YAML Config:**
  ```yaml
  get_project_plan:
    template_success: "{emoji_query} **Project Plan for Issue #{issue_number}** (Workflow: {workflow_name}).\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Failed to retrieve project plan: {error_message}"
  ```

### 5. SavePlanningDeliverablesTool & UpdatePlanningDeliverablesTool

* **Shared DTO (`PlanningDeliverablesOutput`):**
  ```python
  class PlannedCycleSummary(BaseModel):
      cycle_number: int
      deliverables_count: int

  class PlanningDeliverablesOutput(BaseToolOutput):
      issue_number: int
      total_cycles: int
      total_deliverables: int
      cycles: list[PlannedCycleSummary] = []
  ```
* **YAML Config:**
  ```yaml
  save_planning_deliverables:
    template_success: "{emoji_success} Planning deliverables saved for issue #{issue_number} ({total_cycles} cycles, {total_deliverables} deliverables).\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Failed to save planning deliverables: {error_message}"

  update_planning_deliverables:
    template_success: "{emoji_success} Planning deliverables updated for issue #{issue_number} ({total_cycles} cycles, {total_deliverables} deliverables).\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Failed to update planning deliverables: {error_message}"
  ```

---

## Batch 3: Git Analysis & Mutation Tools

### 1. GitListBranchesTool

* **DTO (`GitListBranchesOutput`):**
  ```python
  class BranchDetailDTO(BaseModel):
      name: str
      is_current: bool
      commit_hash: str | None = None
      upstream: str | None = None

  class GitListBranchesOutput(BaseToolOutput):
      current_branch: str
      branches: list[BranchDetailDTO] = []
      branches_count: int = 0
  ```
* **YAML Config:**
  ```yaml
  git_list_branches:
    template_success: "{emoji_query} Found {branches_count} branches. Current branch is '{current_branch}'.\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Failed to list branches: {error_message}"

### 2. GitDiffTool

* **DTO (`GitDiffOutput`):**
  ```python
  class GitDiffOutput(BaseToolOutput):
      target_branch: str
      source_branch: str
      stats: str
      files_changed: int | None = None
      insertions: int | None = None
      deletions: int | None = None
  ```
* **YAML Config:**
  ```yaml
  git_diff_stat:
    template_success: |
      {emoji_query} **Git Diff Summary** (Comparing {source_branch} -> {target_branch})
      - Files changed: {files_changed}
      - Insertions: +{insertions}
      - Deletions: -{deletions}
      *(Full details available in the structured JSON payload)*
    template_failure: "{emoji_failure} Failed to compare branches: {error_message}"
  ```

### 3. GetParentBranchTool

* **DTO (`GetParentBranchOutput`):**
  ```python
  class GetParentBranchOutput(BaseToolOutput):
      branch: str
      parent_branch: str | None = None
  ```
* **YAML Config:**
  ```yaml
  get_parent_branch:
    template_success: "{emoji_query} Branch '{branch}' has parent branch: '{parent_branch}'."
    template_failure: "{emoji_failure} Failed to get parent branch: {error_message}"
  ```

### 4. CheckMergeTool

* **DTO (`CheckMergeOutput`):**
  ```python
  class CheckMergeOutput(BaseToolOutput):
      merge_sha: str
      is_ancestor: bool
  ```
* **YAML Config:**
  ```yaml
  check_merge:
    template_success: "{emoji_success} Merge verification confirmed: SHA {merge_sha} is reachable from HEAD."
    template_failure: "{emoji_failure} Merge verification failed: SHA {merge_sha} is NOT reachable from HEAD."
  ```

### 5. CreateBranchTool
*Note: Now dynamically generates branch name from issue_number and slug to prevent human naming errors.*

* **DTO (`CreateBranchOutput`):**
  ```python
  class CreateBranchOutput(BaseToolOutput):
      branch_name: str
      branch_type: str
      base_branch: str
  ```
* **YAML Config:**
  ```yaml
  create_branch:
    template_success: "{emoji_success} Created branch '{branch_name}' of type '{branch_type}' from '{base_branch}'."
    template_failure: "{emoji_failure} Failed to create branch: {error_message}"
    post_tool_instruction: "Call get_work_context immediately to load the new context for this branch."
  ```

### 6. GitStatusTool

* **DTO (`GitStatusOutput`):**
  ```python
  class GitStatusOutput(BaseToolOutput):
      branch: str
      is_clean: bool
      modified_files: list[str] = []
      untracked_files: list[str] = []
      modified_count: int
      untracked_count: int
  ```
* **YAML Config:**
  ```yaml
  git_status:
    template_success: |
      {emoji_query} **Git Status Summary**
      - Branch: {branch}
      - Clean: {is_clean}
      - Modified: {modified_count} files
      - Untracked: {untracked_count} files
      *(Full details available in the structured JSON payload)*
    template_failure: "{emoji_failure} Git status failed: {error_message}"
  ```

### 7. GitCommitTool

* **DTO (`GitCommitOutput`):**
  ```python
  class GitCommitOutput(BaseToolOutput):
      commit_hash: str
      branch: str
      workflow_phase: str
      sub_phase: str | None = None
      cycle_number: int | None = None
      commit_type: str
      files: list[str] = []
  ```
* **YAML Config:**
  ```yaml
  git_add_or_commit:
    template_success: "{emoji_success} Committed changes to '{branch}' with hash {commit_hash} (Phase: {workflow_phase}, Type: {commit_type}).\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Commit failed: {error_message}"
  ```

### 8. GitRestoreTool

* **DTO (`GitRestoreOutput`):**
  ```python
  class GitRestoreOutput(BaseToolOutput):
      files: list[str] = []
      source: str
      files_count: int = 0
  ```
* **YAML Config:**
  ```yaml
  git_restore:
    template_success: "{emoji_success} Restored {files_count} file(s) from {source}.\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Restore failed: {error_message}"

### 9. GitCheckoutTool

* **DTO (`GitCheckoutOutput`):**
  ```python
  class GitCheckoutOutput(BaseToolOutput):
      branch: str
      previous_branch: str | None = None
      current_phase: str
      parent_branch: str | None = None
  ```
* **YAML Config:**
  ```yaml
  git_checkout:
    template_success: "{emoji_success} Switched branch '{previous_branch}' -> '{branch}' (Current Phase: '{current_phase}')."
    template_failure: "{emoji_failure} Checkout failed: {error_message}"
    post_tool_instruction: "Call get_work_context immediately to load the context for this branch."
  ```

### 10. GitPushTool

* **DTO (`GitPushOutput`):**
  ```python
  class GitPushOutput(BaseToolOutput):
      branch: str
      set_upstream: bool
      new_upstream_created: bool = False
  ```
* **YAML Config:**
  ```yaml
  git_push:
    template_success: "{emoji_success} Pushed branch '{branch}' to origin (Upstream branch created: {new_upstream_created})."
    template_failure: "{emoji_failure} Push failed: {error_message}"
  ```

### 11. GitMergeTool

* **DTO (`GitMergeOutput`):**
  ```python
  class GitMergeOutput(BaseToolOutput):
      source_branch: str
      target_branch: str
  ```
* **YAML Config:**
  ```yaml
  git_merge:
    template_success: "{emoji_success} Merged branch '{source_branch}' into '{target_branch}' successfully."
    template_failure: "{emoji_failure} Merge failed: {error_message}"
  ```

### 12. GitDeleteBranchTool

* **DTO (`GitDeleteBranchOutput`):**
  ```python
  class GitDeleteBranchOutput(BaseToolOutput):
      branch: str
      local_status: str
      remote_status: str
  ```
* **YAML Config:**
  ```yaml
  git_delete_branch:
    template_success: "{emoji_success} Deleted branch '{branch}' (Local: {local_status}, Remote: {remote_status}).\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Failed to delete branch: {error_message}"
  ```

### 13. GitStashTool

* **DTO (`GitStashOutput`):**
  ```python
  class GitStashOutput(BaseToolOutput):
      action: str
      message: str | None = None
      stashes: list[str] = []
  ```
* **YAML Config:**
  ```yaml
  git_stash:
    template_success: "{emoji_success} Stash action '{action}' executed successfully.\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Stash action failed: {error_message}"
  ```

### 14. GitFetchTool

* **DTO (`GitFetchOutput`):**
  ```python
  class GitFetchOutput(BaseToolOutput):
      remote: str
      prune: bool
      raw_output: str
  ```
* **YAML Config:**
  ```yaml
  git_fetch:
    template_success: "{emoji_success} Fetched updates from remote '{remote}'.\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Fetch failed: {error_message}"
  ```

### 15. GitPullTool

* **DTO (`GitPullOutput`):**
  ```python
  class GitPullOutput(BaseToolOutput):
      remote: str
      rebase: bool
      raw_output: str
  ```
* **YAML Config:**
  ```yaml
  git_pull:
    template_success: "{emoji_success} Pulled updates from remote '{remote}'.\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Pull failed: {error_message}"
  ```

---

## Batch 4: Issue, PR, Label & Milestone Tools

### 1. CreateIssueTool, GetIssueTool & UpdateIssueTool
*Note: Shared structure reusing the domain `IssueReadModel`.*

* **Shared DTO (`IssueOutput`):**
  ```python
  from mcp_server.state.github_read_models import IssueReadModel

  class IssueOutput(BaseToolOutput):
      issue: IssueReadModel
      # Flattened presentation-friendly fields
      number: int
      title: str
      state: str
      milestone_title: str = "None"
      assignees_summary: str = "Unassigned"
      html_url: str
  ```
* **YAML Config:**
  ```yaml
  create_issue:
    template_success: "{emoji_success} Created issue #{number}: {title}.\nURL: {html_url}"
    template_failure: "{emoji_failure} Issue creation failed: {error_message}"

  update_issue:
    template_success: "{emoji_success} Updated issue #{number} successfully.\nURL: {html_url}"
    template_failure: "{emoji_failure} Issue update failed: {error_message}"

  get_issue:
    template_success: |
      {emoji_query} **Issue #{number}: {title}**
      - State: {state}
      - Milestone: {milestone_title}
      - Assignees: {assignees_summary}
      *(Full details available in the structured JSON payload)*
    template_failure: "{emoji_failure} Failed to retrieve issue: {error_message}"

### 2. CloseIssueTool

* **DTO (`CloseIssueOutput`):**
  ```python
  class CloseIssueOutput(BaseToolOutput):
      issue_number: int
  ```
* **YAML Config:**
  ```yaml
  close_issue:
    template_success: "{emoji_success} Closed issue #{issue_number} successfully."
    template_failure: "{emoji_failure} Failed to close issue: {error_message}"
  ```

### 3. ListIssuesTool

* **DTO (`ListIssuesOutput`):**
  ```python
  class ListIssuesOutput(BaseToolOutput):
      issues_count: int
      issues: list[IssueReadModel] = []
  ```
* **YAML Config:**
  ```yaml
  list_issues:
    template_success: "{emoji_query} Found {issues_count} issues matching criteria.\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Failed to list issues: {error_message}"
  ```

### 4. SubmitPRTool & GetPRTool
*Note: Aligned fallback layout and shared structure reusing the domain `PRReadModel`.*

* **Shared DTO (`PROutput`):**
  ```python
  from mcp_server.state.github_read_models import PRReadModel

  class PROutput(BaseToolOutput):
      pull_request: PRReadModel
      # Flattened presentation fields
      number: int
      title: str
      html_url: str
      base_ref: str
      head_ref: str
  ```
* **YAML Config:**
  ```yaml
  submit_pr:
    template_success: |
      {emoji_success} Submitted PR #{number}: {title}.
      URL: {html_url}
      - Target: {base_ref}
      - Source: {head_ref}
      *(Full details available in the structured JSON payload)*
    template_failure: "{emoji_failure} PR submission failed: {error_message}"
    post_tool_instruction: "Warning: Branch is now locked down. Branch-mutating tools are blocked until the PR is merged."

  get_pr:
    template_success: |
      {emoji_query} Retrieved PR #{number}: {title}.
      URL: {html_url}
      - Target: {base_ref}
      - Source: {head_ref}
      *(Full details available in the structured JSON payload)*
    template_failure: "{emoji_failure} Failed to retrieve PR: {error_message}"

### 5. MergePRTool

* **DTO (`MergePROutput`):**
  ```python
  class MergePROutput(BaseToolOutput):
      pr_number: int
      merge_sha: str
      merge_method: str
  ```
* **YAML Config:**
  ```yaml
  merge_pr:
    template_success: "{emoji_success} Merged PR #{pr_number} using strategy '{merge_method}' (SHA: {merge_sha})."
    template_failure: "{emoji_failure} Merge failed: {error_message}"
  ```

### 6. ListPRsTool

* **DTO (`ListPRsOutput`):**
  ```python
  class ListPRsOutput(BaseToolOutput):
      prs_count: int
      pull_requests: list[PRReadModel] = []
  ```
* **YAML Config:**
  ```yaml
  list_prs:
    template_success: "{emoji_query} Found {prs_count} pull requests matching criteria.\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Failed to list PRs: {error_message}"
  ```

### 7. ListLabelsTool

* **DTO (`ListLabelsOutput`):**
  ```python
  class LabelOutputModel(BaseModel):
      name: str
      color: str
      description: str | None = None

  class ListLabelsOutput(BaseToolOutput):
      total_labels: int
      labels: list[LabelOutputModel] = []
  ```
* **YAML Config:**
  ```yaml
  list_labels:
    template_success: "{emoji_query} Found {total_labels} labels.\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Failed to list labels: {error_message}"
  ```

### 8. CreateLabelTool & DeleteLabelTool

* **DTOs (`CreateLabelOutput`, `DeleteLabelOutput`):**
  ```python
  class CreateLabelOutput(BaseToolOutput):
      label_name: str
      color: str

  class DeleteLabelOutput(BaseToolOutput):
      label_name: str
  ```
* **YAML Config:**
  ```yaml
  create_label:
    template_success: "{emoji_success} Created label '{label_name}' (Color: #{color})."
    template_failure: "{emoji_failure} Failed to create label: {error_message}"

  delete_label:
    template_success: "{emoji_success} Deleted label '{label_name}' successfully."
    template_failure: "{emoji_failure} Failed to delete label: {error_message}"
  ```

### 9. AddLabelsTool & RemoveLabelsTool

* **Shared DTO (`LabelOperationOutput`):**
  ```python
  class LabelOperationOutput(BaseToolOutput):
      issue_number: int
      labels: list[str] = []
      formatted_labels: str = ""
  ```
* **YAML Config:**
  ```yaml
  add_labels:
    template_success: "{emoji_success} Added labels {formatted_labels} to issue #{issue_number}."
    template_failure: "{emoji_failure} Failed to add labels: {error_message}"

  remove_labels:
    template_success: "{emoji_success} Removed labels {formatted_labels} from issue #{issue_number}."
    template_failure: "{emoji_failure} Failed to remove labels: {error_message}"

### 10. ListMilestonesTool

* **DTO (`ListMilestonesOutput`):**
  ```python
  from mcp_server.state.github_read_models import MilestoneReadModel

  class ListMilestonesOutput(BaseToolOutput):
      total_milestones: int
      milestones: list[MilestoneReadModel] = []
  ```
* **YAML Config:**
  ```yaml
  list_milestones:
    template_success: "{emoji_query} Found {total_milestones} milestones.\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Failed to list milestones: {error_message}"
  ```

### 11. CreateMilestoneTool & CloseMilestoneTool

* **Shared DTO (`MilestoneOutput`):**
  ```python
  class MilestoneOutput(BaseToolOutput):
      milestone: MilestoneReadModel
      # Flattened presentation fields
      title: str
      number: int
  ```
* **YAML Config:**
  ```yaml
  create_milestone:
    template_success: "{emoji_success} Created milestone '{title}' (Number: #{number})."
    template_failure: "{emoji_failure} Failed to create milestone: {error_message}"

  close_milestone:
    template_success: "{emoji_success} Closed milestone '{title}' (Number: #{number}) successfully."
    template_failure: "{emoji_failure} Failed to close milestone: {error_message}"

---

## Batch 5: Phase, Scaffold, Quality & Testing Tools

### 1. TransitionPhaseTool & ForcePhaseTransitionTool

* **Shared DTO (`PhaseTransitionOutput`):**
  ```python
  class PhaseTransitionOutput(BaseToolOutput):
      branch: str
      from_phase: str
      to_phase: str
      skipped_gates: list[str] = []
      passing_gates: list[str] = []
      skipped_gates_count: int = 0
      passing_gates_count: int = 0
  ```
* **YAML Config:**
  ```yaml
  transition_phase:
    template_success: "{emoji_success} Transitioned phase successfully on branch '{branch}' from '{from_phase}' to '{to_phase}' (Passed gates: {passing_gates_count})."
    template_failure: "{emoji_failure} Phase transition failed: {error_message}"
    post_tool_instruction: "Call get_work_context immediately to load the new context for this phase."

  force_phase_transition:
    template_success: "{emoji_warning} Forced phase transition on branch '{branch}' from '{from_phase}' to '{to_phase}' (Passed gates: {passing_gates_count}, Skipped gates: {skipped_gates_count}).\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Forced phase transition failed: {error_message}"
    post_tool_instruction: "Call get_work_context immediately to load the new context for this phase."
  ```

### 2. ScaffoldArtifactTool

* **DTO (`ScaffoldArtifactOutput`):**
  ```python
  class ScaffoldArtifactOutput(BaseToolOutput):
      artifact_type: str
      name: str
      files_created: list[str] = []
      formatted_files_created: str = ""
      schema_info: str = ""
      validation_schema: dict[str, Any] | None = None
      missing_fields: list[str] = []
      provided_fields: list[str] = []
  ```
* **YAML Config:**
  ```yaml
  scaffold_artifact:
    template_success: "{emoji_success} Scaffolded artifact '{name}' of type '{artifact_type}' successfully (Created: {formatted_files_created})."
    template_failure: |
      {emoji_failure} Scaffolding failed: {error_message}
      {schema_info}

### 3. ScaffoldSchemaTool

* **DTO (`ScaffoldSchemaOutput`):**
  ```python
  class ScaffoldSchemaOutput(BaseToolOutput):
      artifact_type: str
      schema_data: dict[str, Any]
  ```
* **YAML Config:**
  ```yaml
  scaffold_schema:
    template_success: "{emoji_query} Retrieved schema for artifact type '{artifact_type}'.\n*(Full details available in the structured JSON payload)*"
    template_failure: "{emoji_failure} Failed to retrieve schema: {error_message}"
  ```

### 4. RunQualityGatesTool

* **DTO (`RunQualityGatesOutput`):**
  ```python
  class GateResultDTO(BaseModel):
      name: str
      passed: bool
      status: str
      score: str | None = None

  class RunQualityGatesOutput(BaseToolOutput):
      overall_pass: bool
      scope: str
      file_count: int
      gates: list[GateResultDTO] = []
  ```
* **YAML Config:**
  ```yaml
  run_quality_gates:
    template_success: "{emoji_success} All quality gates passed successfully for scope '{scope}' ({file_count} files checked)."
    template_failure: "{emoji_failure} Quality gates failed for scope '{scope}' ({file_count} files checked).\n*(Full details available in the structured JSON payload)*"
  ```

### 5. RunTestsTool

* **DTO (`RunTestsOutput`):**
  ```python
  class TestFailureDTO(BaseModel):
      test_id: str
      short_reason: str

  class RunTestsOutput(BaseToolOutput):
      exit_code: int
      passed_count: int
      failed_count: int
      skipped_count: int
      errors_count: int
      summary_line: str
      coverage_pct: float | None = None
      failures: list[TestFailureDTO] = []
      verbose_output: str = ""
  ```
* **YAML Config:**
  ```yaml
  run_tests:
    template_success: "{emoji_success} Test suite passed: {summary_line}."
    template_failure: |
      {emoji_failure} Test suite failed (exit code {exit_code}): {summary_line}.
      {verbose_output}
      *(Full details available in the structured JSON payload)*
  ```

### 6. SafeEditTool

* **DTO (`SafeEditOutput`):**
  ```python
  class SafeEditOutput(BaseToolOutput):
      path: str
      passed: bool
      issues: str | None = None
      mode: str
      written: bool
      diff: str | None = None
      has_diff: bool = False
  ```
* **YAML Config:**
  ```yaml
  safe_edit_file:
    template_success: "{emoji_success} Safely modified file '{path}' (Mode: {mode})."
    template_failure: "{emoji_failure} Safe edit rejected for '{path}' due to validation errors (Mode: {mode}): {issues}.\n*(Full details available in the structured JSON payload)*"
  ```

### 7. TemplateValidationTool

* **DTO (`TemplateValidationOutput`):**
  ```python
  class TemplateValidationErrorDTO(BaseModel):
      severity: str
      message: str

  class TemplateValidationOutput(BaseToolOutput):
      passed: bool
      errors_count: int
      errors: list[TemplateValidationErrorDTO] = []
  ```
* **YAML Config:**
  ```yaml
  validate_template:
    template_success: "{emoji_success} Template validation passed successfully."
    template_failure: "{emoji_failure} Template validation failed with {errors_count} issues.\n*(Full details available in the structured JSON payload)*"
