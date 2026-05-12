---
name: open-issue
description: Create a branch for a specific issue, switch to it, initialize the project, and make the first commit and push.
agent: co
argument-hint: Issue number + workflow type. Example: "issue 302 feature"
---

# Open Issue

Bootstrap a new issue branch end-to-end: branch → checkout → initialize → first commit → push.

## Required Input

Extract from the invocation argument:
- `ISSUE_NUMBER` — the GitHub issue number
- `WORKFLOW_TYPE` — one of: feature, bug, refactor, docs, hotfix, epic

If either is missing, call `get_issue(ISSUE_NUMBER)` to derive the workflow type from the issue labels before proceeding.

## Execution Sequence

Execute in this exact order. Do not skip steps.

1. **Read the issue**
   `get_issue(ISSUE_NUMBER)` → note the title, labels, and any stated scope.

2. **Create the branch**
   `create_branch(branch_type=WORKFLOW_TYPE, name="<short-slug-from-title>", base_branch="main")`
   → branch name format: `{type}/{ISSUE_NUMBER}-{slug}`

3. **Switch to the branch**
   `git_checkout(branch="{type}/{ISSUE_NUMBER}-{slug}")`

4. **Initialize the project**
   `initialize_project(issue_number=ISSUE_NUMBER, workflow_name=WORKFLOW_TYPE)`
   → verifies workflow phases loaded.

5. **First commit**
   `git_add_or_commit(message="chore: open issue #{ISSUE_NUMBER} — {title}")`
   → commits any state file changes produced by initialize_project.

6. **Push**
   `git_push(set_upstream=true)`

## Output

After completing all steps, report:
- Branch name created
- Active workflow and first phase
- Remote push confirmed (yes/no)
- Any blockers encountered
