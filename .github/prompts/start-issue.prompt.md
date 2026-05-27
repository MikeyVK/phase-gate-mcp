---
name: start-issue
description: Bootstrap issue lifecycle entry under the approved ownership model.
agent: co
argument-hint: Issue number + workflow type. Example: "issue 341 epic"
---

# Start Issue

Bootstrap explicit lifecycle entry. This prompt models branch entry, not background coordination around work already in progress.

## Required Input

Extract from the invocation argument:
- `ISSUE_NUMBER` — the GitHub issue number
- `WORKFLOW_TYPE` — one of: feature, bug, refactor, docs, hotfix, epic

If `WORKFLOW_TYPE` is missing, call `get_issue(ISSUE_NUMBER)` and derive it from authoritative issue context.
If `ISSUE_NUMBER` is missing, stop and ask for it. Do not guess from branch names or free-form text.

## Common Sequence

Execute in this exact order. Do not skip steps.

1. **Read the issue**
   `get_issue(ISSUE_NUMBER)` → read the result as flat JSON; record the `title` and `labels` fields, plus the stated scope.

2. **Create the branch**
   `create_branch(branch_type=WORKFLOW_TYPE, name="<short-slug-from-title>", base_branch="main")`
   → branch name format: `{type}/{ISSUE_NUMBER}-{slug}`

3. **Switch to the branch**
   `git_checkout(branch="{type}/{ISSUE_NUMBER}-{slug}")`

4. **Initialize the project**
   `initialize_project(issue_number=ISSUE_NUMBER, issue_title="{title}", workflow_name=WORKFLOW_TYPE)`

## Epic-Owned Path

Use this path only when `WORKFLOW_TYPE` is `epic`.

5. **Load startup context**
   `get_work_context()`
   → record branch, workflow, and first phase.
   → if startup context does not load cleanly, stop before the first commit or push and report the blocker.

6. **Verify project plan and workflow contract**
   `get_project_plan(issue_number=ISSUE_NUMBER)`
   → if the workflow or phase contract is missing or inconsistent, stop before the first commit or push and report the blocker.

7. **First commit**
   `git_add_or_commit(workflow_phase="<first phase from get_work_context>", message="Start issue #ISSUE_NUMBER: {title}")`
   → use the initialized workflow phase returned by `get_work_context`; do not guess or hardcode the phase name.

8. **Push**
   `git_push(set_upstream=true)`

## Non-Epic Path

Use this path for `feature`, `bug`, `refactor`, `docs`, and `hotfix` workflows.

5. **Verify project plan and hand-off boundary**
   `get_project_plan(issue_number=ISSUE_NUMBER)`
   → if the initialized plan is missing or inconsistent, stop and report the blocker.

6. **Hand off at the issue268 boundary**
   `@co` owns lifecycle entry through `get_project_plan`, then stops.
   `@imp` becomes the first agent to call `get_work_context` before the first commit or any further write action on the new branch.
   Do not make the first commit or push on the non-epic path from `@co`.

## Guardrails

- If `@co` is merely coordinating around ongoing `@imp` work, use a normal `@co` session instead of this prompt.
- Do not skip the `get_work_context` or `get_project_plan` stop-go checks where this prompt requires them.
- Do not silently widen the non-epic flow into full owned-branch execution.

## Output

After completing or stopping the flow, report:
- branch name
- workflow
- first phase when available
- whether the flow stopped at the `@co` hand-off or completed full owned-branch bootstrap
- push result when applicable
- blockers
