---
name: end-issue
description: Execute lifecycle exit under the approved ownership model.
agent: co
argument-hint: Issue number + PR number. Example: "issue 345 pr 412"
---

# End Issue

Complete explicit lifecycle exit. Human invocation of this prompt is the required
merge-approval signal. Do not invoke this prompt autonomously or as part of an
automated pipeline.

This prompt models owned-branch lifecycle exit only. For ongoing coordination around
work in progress use a normal `@co` session instead.

## Required Input

Extract from the invocation argument:
- `ISSUE_NUMBER` — the GitHub issue number
- `PR_NUMBER` — the pull request number to merge

If `ISSUE_NUMBER` is missing, derive it from `get_work_context()` when possible.
If `PR_NUMBER` is missing, stop and ask for it. Do not guess.

## Common Sequence

Execute in this exact order. Do not skip steps.

1. **Load branch context**
   `get_work_context()`
   → record `branch`, `workflow`, `issue_number`, and `parent_branch`.
   → if `parent_branch` is missing or the phase context does not load cleanly,
     stop and report the blocker before merge.

2. **Merge**
   `merge_pr(pr_number=PR_NUMBER)`
   → this is the authoritative proof that the host-side merge was accepted.
   → do not use `git_diff_stat` as a substitute for merge proof.

3. **Verify merged PR**
   `get_pr(pr_number=PR_NUMBER)`
   → record `head_branch` and `base_branch` from the result.
   → verify that `head_branch` matches the `branch` recorded in step 1.
     If they differ, stop and report the mismatch; do not proceed with checkout or cleanup.

4. **Return to parent branch**
   `git_checkout(branch=<base_branch from step 3>)`
   → required before local branch cleanup is legal.

5. **Pull parent branch**
   `git_pull()`
   → updates the local parent branch so the merged content is present locally.
   → do not proceed to branch cleanup until pull completes without error.

6. **Verify merge SHA is reachable**
   Record `merge_commit_sha` from the `get_pr` result in step 3.
   Run: `git merge-base --is-ancestor <merge_commit_sha> HEAD && echo reachable || echo BLOCKED`
   → if the output is `BLOCKED`, the merged commit is not yet in the local parent branch.
     Stop and report the blocker; do not delete the branch.
   → proceed only when output is `reachable`.

7. **Clean up the branch**
   `git_delete_branch(branch=<closing branch>, mode="both")`
   → removes both local and remote refs in one step.
   → if the remote ref is already absent, `mode="both"` returns `absent` for that
     side rather than an error; no manual retry is needed.

8. **Read the PR body**
   Read the merged PR body as the durable `@imp` → `@co` transfer artifact.
   The PR body carries: delivered scope, `Closes #N` claims, deferred items, and
   tracking state. Use this as the authoritative record of what landed and what
   was intentionally deferred.

9. **Epic-parent update (conditional)**
   Perform this step only when the active workflow is `epic` or when the merged
   branch is a child of a tracked epic.
   `get_project_plan(issue_number=ISSUE_NUMBER)`
   `update_issue(issue_number=<epic_issue_number>, body=<updated coordination state>)`
   → record merged status and the next planned or logically following issue.

10. **Next-issue recommendation (advisory)**
   Based on the PR body durable facts and current epic or backlog state,
   recommend the next logically following issue.
   This recommendation is advisory. It is not an automatic priority mutation and
   does not trigger any tool calls without explicit human confirmation.

## Recovery: Issue Still Open After Merge

Use this block only when the merged PR body carried a `Closes #N` claim for
`ISSUE_NUMBER`, the merge is confirmed complete, and the issue is still open.

```
close_issue(issue_number=ISSUE_NUMBER, comment="<recovery note>")
```

`close_issue()` is not part of the normative lifecycle-exit path. It is a recovery
action only.

## Guardrails

- Human invocation of this prompt is the required merge-approval signal. Do not
  merge autonomously or interpret any other event as implicit approval.
- `merge_pr(pr_number=PR_NUMBER)` is the authoritative merge signal. Do not rely
  on `git_diff_stat` or stale local branch state as merge proof.
- `close_issue()` is absent from the normative path. Use it only in the recovery
  block above when explicitly needed.
- Do not widen `@co` tool use beyond the approved allowlist for this prompt.
- Remote branch cleanup is an outcome of `git_delete_branch(mode="both")`, not a
  separate tool call or manual verification step.

## Output

After completing or stopping the flow, report:
- branch and workflow
- merge result
- parent branch used for checkout
- branch cleanup result (local and remote status from `git_delete_branch`)
- next-issue recommendation when relevant
- epic-parent update result when applicable
- blockers encountered, if any
