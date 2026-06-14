# DTO Contracts & Presentation Templates — Issue #402

This document serves as the Single Source of Truth (SSOT) for the Pydantic DTO contracts and their corresponding presentation templates defined in `presentation.yaml`.

---

## Centralized Presentation Configuration (`presentation.yaml`)

To enforce DRY and prevent presentation leakage into the codebase, emojis, default error handlers, advisories, and the structured JSON payload reference are declared centrally:

```yaml
global:
  emojis:
    success: "✅"
    failure: "❌"
    warning: "⚠️"
    query: "📋"
    bootstrap: "🚀"
  json_reference: "*(Full details available in the structured JSON payload)*"
  default_failure_template: "Failed: {error_message}"
  advisories:
    context_reset: "\n\n🚀 REQUIRED NEXT STEP: Call get_work_context now before any other tool call to load the current phase context for this branch."
    server_restart: "\n\n⏳ WAIT 3 SECONDS before continuing - server needs time to reload. Service will be unavailable briefly during restart."
    branch_lockdown: "\n\n⚠️ Warning: Branch is now locked down. Branch-mutating tools are blocked until the PR is merged."
    todo_discipline: "\n\n📋 TODO discipline: create or refresh your TODO list now; keep exactly one item in progress and update it after each material step."
```

### Presentation Rules:
1. **Status Emoji Prefixes**: Emojis are prepended automatically by the `TextPresenter` based on the status and metadata of the tool execution (`success` is True -> prepend `emoji_success`; `success` is False -> prepend `emoji_failure`; query tools -> prepend `emoji_query`; initialization tools -> prepend `emoji_bootstrap`).
2. **Default Failure Text**: If a tool fails and does not define a custom `template_failure`, the presenter falls back to the `default_failure_template` (`Failed: {error_message}`), prefixed by the failure emoji.
3. **Dynamic JSON Reference Appending**: The reference `*(Full details available in the structured JSON payload)*` is appended dynamically by the presenter only when rich structured data (like `diff`, `failures`, `validation_schema`, or lists of items) is present in the DTO, keeping simple messages clean and uncluttered.
4. **Advisories**: Advisories are resolved from the global lookup table and appended automatically.

---

## Shared Base Schemas

Every DTO schema inherits from `BaseToolOutput` to enforce immutability, disallow extra fields, and guarantee a unified structure for error handling and agent instruction propagation.

```python
from enum import Enum
from pydantic import BaseModel, ConfigDict


class BaseToolOutput(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    success: bool = True
    error_message: str | None = None
    post_tool_instruction: str | None = None

class GitHubObjectOutput(BaseToolOutput):
    """Base class for GitHub resources that have a number and title."""
    number: int
    title: str

class GateTransitionOutput(BaseToolOutput):
    """Base class for workflows verifying gates during phase or cycle transitions."""
    branch: str
    passing_gates: list[str] = []
    skipped_gates: list[str] = []
    passing_gates_count: int = 0
    skipped_gates_count: int = 0

class GitFetchPullOutput(BaseToolOutput):
    """Base class for Git remote operations returning output."""
    remote: str
    raw_output: str

class BranchPairOutput(BaseToolOutput):
    """Base class for Git operations comparing or merging two branches."""
    source_branch: str
    target_branch: str
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
      **Server Health Status**
      - Status: {status}
      - Version: {version}
      - Process ID: {pid}
      - Platform: {platform}
      - Uptime: {uptime_seconds} seconds
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
    template_success: "Server restart initiated successfully (Reason: {reason})."
    advisory: "server_restart"
  ```

### 3. TransitionCycleTool & ForceCycleTransitionTool

* **DTOs (`CycleTransitionOutput`, `ForceCycleTransitionOutput`):**
  ```python
  class CycleTransitionOutput(GateTransitionOutput):
      from_cycle: int | None = None
      to_cycle: int
      total_cycles: int
      cycle_name: str

  class ForceCycleTransitionOutput(CycleTransitionOutput):
      skip_reason: str
      human_approval: str
  ```
* **YAML Config:**
  ```yaml
  transition_cycle:
    template_success: &cycle_transition_template "Transitioned to Cycle {to_cycle}/{total_cycles} ({cycle_name}) on branch '{branch}' (Passed gates: {passing_gates_count}, Skipped gates: {skipped_gates_count})."
    advisory: "context_reset"

  force_cycle_transition:
    template_success: *cycle_transition_template
    advisory: "context_reset"
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
    template_success: "Found {results_count} documentation matches for query '{query}' in scope '{scope}'."
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
      Phase: {phase} (confidence={phase_confidence})
      Role: {sub_role_hint}
      Parent: {parent_branch}
    advisory: "todo_discipline"
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
    template_success: "Initialized project for issue #{issue_number} on branch '{branch}' (Initial Phase: '{initial_phase}')."
    advisory: "context_reset"
  ```

### 4. GetProjectPlanTool

* **DTO (`ProjectPlanOutput`):**
  ```python
  class PhaseTaskDTO(BaseModel):
      id: str
      title: str
      status: str

  class PhaseDTO(BaseModel):
      name: str
      status: str
      tasks: list[PhaseTaskDTO] = []

  class ProjectPlanOutput(BaseToolOutput):
      issue_number: int
      workflow_name: str
      phases: list[PhaseDTO] = []
  ```
* **YAML Config:**
  ```yaml
  get_project_plan:
    template_success: "**Project Plan for Issue #{issue_number}** (Workflow: {workflow_name})."
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
    template_success: &planning_success_template "Planning deliverables for issue #{issue_number} ({total_cycles} cycles, {total_deliverables} deliverables)."

  update_planning_deliverables:
    template_success: *planning_success_template
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
    template_success: "Found {branches_count} branches. Current branch is '{current_branch}'."
  ```

### 2. GitDiffTool

* **DTO (`GitDiffOutput`):**
  ```python
  class GitDiffOutput(BranchPairOutput):
      stats: str
      files_changed: int | None = None
      insertions: int | None = None
      deletions: int | None = None
  ```
* **YAML Config:**
  ```yaml
  git_diff_stat:
    template_success: |
      **Git Diff Summary** (Comparing {source_branch} -> {target_branch})
      - Files changed: {files_changed}
      - Insertions: +{insertions}
      - Deletions: -{deletions}
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
    template_success: "Branch '{branch}' has parent branch: '{parent_branch}'."
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
    template_success: "Merge verification confirmed: SHA {merge_sha} is reachable from HEAD."
    template_failure: "Merge verification failed: SHA {merge_sha} is NOT reachable from HEAD."
  ```

### 5. CreateBranchTool

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
    template_success: "Created branch '{branch_name}' of type '{branch_type}' from '{base_branch}'."
    advisory: "context_reset"
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
      **Git Status Summary**
      - Branch: {branch}
      - Clean: {is_clean}
      - Modified: {modified_count} files
      - Untracked: {untracked_count} files
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
    template_success: "Committed changes to '{branch}' with hash {commit_hash} (Phase: {workflow_phase}, Type: {commit_type})."
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
    template_success: "Restored {files_count} file(s) from {source}."
  ```

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
    template_success: "Switched branch '{previous_branch}' -> '{branch}' (Current Phase: '{current_phase}')."
    advisory: "context_reset"
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
    template_success: "Pushed branch '{branch}' to origin (Upstream branch created: {new_upstream_created})."
  ```

### 11. GitMergeTool

* **DTO (`GitMergeOutput`):**
  ```python
  class GitMergeOutput(BranchPairOutput):
      pass
  ```
* **YAML Config:**
  ```yaml
  git_merge:
    template_success: "Merged branch '{source_branch}' into '{target_branch}' successfully."
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
    template_success: "Deleted branch '{branch}' (Local: {local_status}, Remote: {remote_status})."
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
    template_success: "Stash action '{action}' executed successfully."
  ```

### 14. GitFetchTool & GitPullTool

* **DTOs (`GitFetchOutput`, `GitPullOutput`):**
  ```python
  class GitFetchOutput(GitFetchPullOutput):
      prune: bool

  class GitPullOutput(GitFetchPullOutput):
      rebase: bool
  ```
* **YAML Config:**
  ```yaml
  git_fetch:
    template_success: "Fetched updates from remote '{remote}'."

  git_pull:
    template_success: "Pulled updates from remote '{remote}'."
    advisory: "context_reset"
  ```

---

## Batch 4: Issue, PR, Label & Milestone Tools

### 1. CreateIssueTool, GetIssueTool & UpdateIssueTool

* **Shared DTO (`IssueOutput`):**
  ```python
  class IssueOutput(GitHubObjectOutput):
      # Flattened presentation-friendly fields
      state: str
      milestone_title: str = "None"
      assignees_summary: str = "Unassigned"
      html_url: str
      body: str = ""
      labels: list[str] = []
      created_at: str
      updated_at: str
      closed_at: str | None = None
      author: str
  ```
* **YAML Config:**
  ```yaml
  create_issue:
    template_success: &issue_success_template "Issue #{number}: {title}.\nURL: {html_url}"

  update_issue:
    template_success: *issue_success_template

  get_issue:
    template_success: |
      **Issue #{number}: {title}**
      - State: {state}
      - Milestone: {milestone_title}
      - Assignees: {assignees_summary}
  ```

### 2. CloseIssueTool

* **DTO (`CloseIssueOutput`):**
  ```python
  class CloseIssueOutput(BaseToolOutput):
      issue_number: int
  ```
* **YAML Config:**
  ```yaml
  close_issue:
    template_success: "Closed issue #{issue_number} successfully."
  ```

### 3. ListIssuesTool

* **DTO (`ListIssuesOutput`):**
  ```python
  class IssueSummaryDTO(BaseModel):
      number: int
      title: str
      state: str
      html_url: str
      labels: list[str] = []
      assignees_summary: str = "Unassigned"
      created_at: str

  class ListIssuesOutput(BaseToolOutput):
      issues_count: int
      issues: list[IssueSummaryDTO] = []
  ```
* **YAML Config:**
  ```yaml
  list_issues:
    template_success: "Found {issues_count} issues matching criteria."
  ```

### 4. SubmitPRTool & GetPRTool

* **Shared DTO (`PROutput`):**
  ```python
  class PROutput(GitHubObjectOutput):
      # Flattened presentation fields
      html_url: str
      state: str
      base_ref: str
      head_ref: str
      merged_at: str | None = None
      merge_sha: str | None = None
      body: str = ""
  ```
* **YAML Config:**
  ```yaml
  get_pr:
    template_success: &pr_detail_template |
      PR #{number}: {title}
      URL: {html_url}
      - Target: {base_ref}
      - Source: {head_ref}

  submit_pr:
    template_success: *pr_detail_template
    advisory: "branch_lockdown"
  ```

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
    template_success: "Merged PR #{pr_number} using strategy '{merge_method}' (SHA: {merge_sha})."
  ```

### 6. ListPRsTool

* **DTO (`ListPRsOutput`):**
  ```python
  class PRSummaryDTO(BaseModel):
      number: int
      title: str
      state: str
      html_url: str
      base_ref: str
      head_ref: str

  class ListPRsOutput(BaseToolOutput):
      prs_count: int
      pull_requests: list[PRSummaryDTO] = []
  ```
* **YAML Config:**
  ```yaml
  list_prs:
    template_success: "Found {prs_count} pull requests matching criteria."
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
    template_success: "Found {total_labels} labels."
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
    template_success: "Created label '{label_name}' (Color: #{color})."

  delete_label:
    template_success: "Deleted label '{label_name}' successfully."
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
    template_success: "Added labels {formatted_labels} to issue #{issue_number}."

  remove_labels:
    template_success: "Removed labels {formatted_labels} from issue #{issue_number}."
  ```

### 10. ListMilestonesTool

* **DTO (`ListMilestonesOutput`):**
  ```python
  class MilestoneSummaryDTO(BaseModel):
      number: int
      title: str
      state: str

  class ListMilestonesOutput(BaseToolOutput):
      total_milestones: int
      milestones: list[MilestoneSummaryDTO] = []
  ```
* **YAML Config:**
  ```yaml
  list_milestones:
    template_success: "Found {total_milestones} milestones."
  ```

### 11. CreateMilestoneTool & CloseMilestoneTool

* **Shared DTO (`MilestoneOutput`):**
  ```python
  class MilestoneOutput(GitHubObjectOutput):
      state: str
  ```
* **YAML Config:**
  ```yaml
  create_milestone:
    template_success: &milestone_success_template "Milestone '{title}' (Number: #{number})."

  close_milestone:
    template_success: *milestone_success_template
  ```

---

## Batch 5: Phase, Scaffold, Quality & Testing Tools

### 1. TransitionPhaseTool & ForcePhaseTransitionTool

* **DTOs (`PhaseTransitionOutput`, `ForcePhaseTransitionOutput`):**
  ```python
  class PhaseTransitionOutput(GateTransitionOutput):
      from_phase: str
      to_phase: str

  class ForcePhaseTransitionOutput(PhaseTransitionOutput):
      skip_reason: str
      human_approval: str
  ```
* **YAML Config:**
  ```yaml
  transition_phase:
    template_success: &phase_transition_template "Phase transition on branch '{branch}' from '{from_phase}' to '{to_phase}' (Passed gates: {passing_gates_count}, Skipped gates: {skipped_gates_count})."
    advisory: "context_reset"

  force_phase_transition:
    template_success: *phase_transition_template
    advisory: "context_reset"
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
    template_success: "Scaffolded artifact '{name}' of type '{artifact_type}' successfully (Created: {formatted_files_created})."
    template_failure: "Scaffolding failed: {error_message}.\n{schema_info}"
  ```

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
    template_success: "Retrieved schema for artifact type '{artifact_type}'."
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
    template_success: "All quality gates passed successfully for scope '{scope}' ({file_count} files checked)."
    template_failure: "Quality gates failed for scope '{scope}' ({file_count} files checked)."
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
    template_success: "Test suite passed: {summary_line}."
    template_failure: "Test suite failed (exit code {exit_code}): {summary_line}."
  ```
  *(Note: If tests fail and verbose=False, the tool populates `post_tool_instruction` with advice to rerun with verbose=True).*

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
    template_success: "Safely modified file '{path}' (Mode: {mode})."
    template_failure: "Safe edit rejected for '{path}' due to validation errors (Mode: {mode}): {issues}."
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
    template_success: "Template validation passed successfully."
    template_failure: "Template validation failed with {errors_count} issues."
  ```

### 8. AutoFixTool

* **DTO (`AutoFixOutput`):**
  ```python
  class AutoFixOutput(BaseToolOutput):
      file_path: str
      fixes_applied: int
      fixes_failed: int
      has_diff: bool = False
      diff: str | None = None
  ```
* **YAML Config:**
  ```yaml
  auto_fix:
    template_success: "Applied {fixes_applied} automatic fixes to '{file_path}' ({fixes_failed} failed)."
    template_failure: "Failed to apply automatic fixes to '{file_path}': {error_message}."
  ```
