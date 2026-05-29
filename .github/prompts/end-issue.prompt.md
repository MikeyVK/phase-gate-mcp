---
name: end-issue
description: Execute lifecycle exit under the approved ownership model.
agent: co
argument-hint: PR number. Optional issue number for recovery-only cases. Example: "pr 412" or "issue 345 pr 412"
---

# End Issue

Complete explicit lifecycle exit. Human invocation of this prompt is the required
merge-approval signal. Do not invoke this prompt autonomously or as part of an
automated pipeline.

This prompt models owned-branch lifecycle exit only. For ongoing coordination around
work in progress use a normal `@co` session instead.

## Required Input

Extract from the invocation argument:
- `PR_NUMBER` — required GitHub pull request number to merge
- `ISSUE_NUMBER` — optional GitHub issue number; use only when recovery or epic coordination needs an explicit issue target

If `PR_NUMBER` is missing, stop and ask for it. Do not guess.
If `ISSUE_NUMBER` is missing, do not derive it up front. Read the merged PR body first
and only derive or request an issue number if a later recovery step actually needs one.

## Common Sequence

Execute in this exact order. Do not skip steps.

1. **Load PR context**
   `get_pr(pr_number=PR_NUMBER)`
   → record `head_branch`, `base_branch`, `body`, `state`, and `title`.
   → treat the PR as the authoritative source for closeout metadata.
   → if `head_branch` or `base_branch` is missing, stop and report the blocker before merge.

2. **Merge**
   `merge_pr(pr_number=PR_NUMBER)`
   → this is the authoritative proof that the host-side merge was accepted.
   → do not use `git_diff_stat` as a substitute for merge proof.

3. **Refresh merged PR**
   `get_pr(pr_number=PR_NUMBER)`
   → record refreshed `body`, `merged_at`, and `merge_sha`.
   → if `merged_at` is null or `merge_sha` is null, stop and report the blocker; do not proceed with checkout or cleanup.

4. **Return to parent branch**
   `git_checkout(branch=<base_branch from step 3>)`
   → required before local branch cleanup is legal.

5. **Pull parent branch**
   `git_pull()`
   → updates the local parent branch so the merged content is present locally.
   → do not proceed to branch cleanup until pull completes without error.

6. **Verify merged content is present on the current branch**
   `check_merge(merge_sha=<merge_sha from step 3>)`
   → this thin wrapper is the destructive-cleanup gate for post-merge reachability.
   → if the tool is unavailable on this branch, stop and report the blocker; do not substitute raw terminal git commands.
   → if the result says the merge SHA is not reachable from `HEAD`, stop and report the blocker; do not delete the branch.

7. **Load parent-branch context (best-effort)**
   `get_work_context()`
   → call this only after checkout to the parent branch.
   → if the checked-out parent branch is a tracked workflow branch, record `workflow`, `issue_number`, and `parent_branch` for coordination that depends on parent state.
   → if the checked-out parent branch is `main` or another stateless non-epic branch and phase or workflow context does not load cleanly, treat that as expected and continue.
   → do not use `get_work_context()` as the source of child-branch merge metadata.

8. **Clean up the branch**
   `git_delete_branch(branch=<head_branch from step 3>, mode="both")`
   → removes both local and remote refs in one step.
   → if the remote ref is already absent, `mode="both"` returns `absent` for that side rather than an error; no manual retry is needed.

9. **Read the PR body**
   Read the merged PR body as the durable `@imp` → `@co` transfer artifact.
   The PR body carries delivered scope, `Closes #N` claims, deferred items, and tracking state.
   Use this as the authoritative record of what landed and what was intentionally deferred.

10. **Epic-parent update (conditional)**
   Perform this step only when step 7 confirms that the checked-out parent branch is a tracked epic branch.
   `update_issue(issue_number=<issue_number from step 7>, body=<updated coordination state>)`
   → if step 7 returned no meaningful workflow context on `main` or another stateless non-epic branch, skip this step.
   → if epic coordination is required but the checked-out parent branch still has no issue number in step 7, stop and report the blocker instead of guessing.
   → record merged status and the next planned or logically following issue.

11. **Next-issue recommendation (advisory)**
   Based on the PR body durable facts and current epic or backlog state,
   recommend the next logically following issue.
   This recommendation is advisory. It is not an automatic priority mutation and
   does not trigger any tool calls without explicit human confirmation.

## Recovery: Issue Still Open After Merge

Use this block only when the merged PR body carried a `Closes #N` claim for a specific issue,
the merge is confirmed complete, and that issue is still open.

If `ISSUE_NUMBER` was not supplied as input, derive the recovery target from the merged PR body before calling `close_issue(...)`.

```
close_issue(issue_number=ISSUE_NUMBER, comment="<recovery note>")
```

`close_issue()` is not part of the normative lifecycle-exit path. It is a recovery
action only.

## Guardrails

- Human invocation of this prompt is the required merge-approval signal. Do not merge autonomously or interpret any other event as implicit approval.
- `merge_pr(pr_number=PR_NUMBER)` is the authoritative merge signal. Do not rely on `git_diff_stat` or stale local branch state as merge proof.
- `check_merge(...)` is the delete gate for merged-content reachability on the checked-out parent branch. Do not substitute raw terminal git commands in this prompt.
- `get_work_context()` is parent-branch coordination context after checkout, not the source of child-branch merge metadata.
- `close_issue()` is absent from the normative path. Use it only in the recovery block above when explicitly needed.
- Do not widen `@co` tool use beyond the approved allowlist for this prompt.
- Remote branch cleanup is an outcome of `git_delete_branch(mode="both")`, not a separate tool call or manual verification step.

## Output

After completing or stopping the flow, report:
- PR number and merge result
- closing branch and parent branch used for checkout
- merged-content reachability result
- branch cleanup result (local and remote status from `git_delete_branch`)
- next-issue recommendation when relevant
- epic-parent update result when applicable
