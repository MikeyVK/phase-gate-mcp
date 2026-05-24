---
name: close-issue
description: Execute lifecycle exit under the approved ownership model.
agent: co
argument-hint: Issue number + PR number when merge is required. Example: "issue 341 pr 412"
---

# Close Issue

Complete explicit lifecycle exit. This prompt models owned-branch exit, not background coordination around work already in progress.

## Required Input

Extract from the invocation argument:
- `ISSUE_NUMBER` — the GitHub issue number
- `PR_NUMBER` — the pull request to merge when lifecycle exit requires a merge

If `ISSUE_NUMBER` is missing, derive it from `get_work_context()` when possible.
If `PR_NUMBER` is required for merge and missing, stop and ask for it. Do not guess it with unapproved tools.

## Startup Context

1. **Load branch context**
   `get_work_context()` → record branch, workflow, issue number, and parent branch.

2. **Read the issue when needed**
   `get_issue(ISSUE_NUMBER)` → confirm the current issue state and any relevant close-out notes.

## Non-Epic Path

Use this path when the active workflow is not `epic`.

3. **Preserve the inherited issue268 baseline**
   Wait for explicit human instruction before merge or close actions.

4. **Merge**
   `merge_pr(pr_number=PR_NUMBER)`

5. **Close the issue when the inherited baseline requires it**
   `close_issue(issue_number=ISSUE_NUMBER)`

6. **Optional cleanup**
   Verify or report branch-cleanup follow-up only within the inherited non-epic baseline.
   Do not add the epic-specific merge-verify-cleanup override to non-epic flows from this prompt.

## Epic-Owned Path

Use this override only when the active workflow is `epic`.

3. **Confirm lifecycle exit authority**
   Ensure explicit human approval is present and QA or documented hand-over conditions are satisfied.
   If `parent_branch` is missing from `get_work_context()`, stop and report the blocker before merge.

4. **Merge the PR**
   `merge_pr(pr_number=PR_NUMBER)`
   `close_issue` is not the normative next step on this epic-owned path.

5. **Return to the parent branch**
   `git_checkout(branch="<parent_branch from get_work_context>")`

6. **Verify landed work**
   `git_diff_stat(target_branch="<parent_branch>", source_branch="<closing branch>")`
   → expect no remaining diff that suggests the merge did not land cleanly.
   → if the result is inconsistent, stop and report the blocker.

7. **Verify cleanup outcomes**
   `git_list_branches(remote=true)`
   → confirm the closing branch is absent remotely when host-side auto-delete is enabled.
   → if local or remote cleanup did not happen automatically, report explicit follow-up instead of assuming an unapproved cleanup tool.

8. **Update epic coordination state when relevant**
   Use `get_project_plan(issue_number=ISSUE_NUMBER)` when you need to identify the next planned issue from the epic plan.
   Use `update_issue(issue_number=ISSUE_NUMBER, body=...)` when the epic issue body needs merged status, the next planned issue, or a factual follow-up note.

9. **Recovery-only closure**
   If post-merge verification shows the linked issue is still open and the human wants explicit closure, call:
   `close_issue(issue_number=ISSUE_NUMBER, comment="<optional recovery note>")`
   Use this only as recovery on the epic-owned path.

## Guardrails

- This prompt models lifecycle exit only; for ongoing coordination use a normal `@co` session.
- Do not silently widen `@co` tool use beyond the approved allowlist.
- Treat remote cleanup as an outcome to verify, not a guaranteed tool capability.
- Do not rewrite the inherited non-epic baseline inside this prompt.

## Output

After completing or stopping the flow, report:
- branch and workflow
- merge result
- parent branch used for verification when applicable
- landed-work verification result
- cleanup verification result, including whether explicit follow-up remains
- whether the epic issue state was updated
- the next planned or logically following issue when relevant
- blockers
