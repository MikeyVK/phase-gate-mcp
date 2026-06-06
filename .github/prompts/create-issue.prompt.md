---
name: create-issue
description: Scaffold and submit a new GitHub issue of a specified type.
agent: co
argument-hint: Issue type + short description. Examples: "bug: login fails on timeout", "feature: add dark mode toggle", "refactor: split CreateIssueTool"
---

# Create Issue

Guide through scaffolding a GitHub issue body and submitting it as a real GitHub issue.

## Required Input

Extract from the invocation argument:

- `ISSUE_TYPE` — one of: `feature`, `bug`, `hotfix`, `chore`, `docs`, `epic`
- `DESCRIPTION` — short description (optional; used as a starting point for the title)

If `ISSUE_TYPE` is absent, ask the user before proceeding. Do not guess.

---

## Step 1: Select fields for this issue type

Based on `ISSUE_TYPE`, determine which optional context fields to populate when calling `scaffold_artifact`.

| ISSUE_TYPE | Recommended optional fields |
| ---------- | --------------------------- |
| `bug`      | `actual`, `steps_to_reproduce`, `expected` |
| `feature`  | `expected`, `context`, `summary` |
| `refactor` | `context`, `expected` |
| `chore`    | `context` |
| `docs`     | `context` |
| `hotfix`   | `actual`, `steps_to_reproduce`, `expected` |
| `epic`     | `summary`, `context`, `expected` |

Do not ask about fields outside the recommended set unless the user volunteers them.

---

## Step 2: Collect content

Use conversation context or ask the user for:

- `title` — concise issue title (required)
- `problem` — what is wrong or needed (required)
- Recommended optional fields from Step 1

---

## Step 3: Collect metadata

Ask the user for:

- `priority` — one of the values injected at runtime from config (typically `critical`, `high`, `medium`, `low`, `triage`). Default to `medium` if the user does not specify.
- `scope` — one of the values injected at runtime from config (typically `architecture`, `mcp-server`, `platform`, `tooling`, `workflow`, `documentation`). Ask if unclear.
- `is_epic` — `true` only when `ISSUE_TYPE` is `epic`. Default `false`.
- `parent_issue` — parent issue number (optional, positive integer).
- `milestone` — milestone title (optional).
- `assignees` — list of GitHub logins (optional).

Do not invent values for `priority` or `scope`. If uncertain, ask.

---

## Step 4: Scaffold the issue body

Call `scaffold_artifact` with the collected context. Include only fields with actual values — omit empty optional fields entirely.

```
scaffold_artifact(
  artifact_type="issue",
  name="<slug-from-title>",
  context={
    "title": "<title>",
    "problem": "<problem>",
    # include only when filled in:
    "summary": "<summary>",
    "expected": "<expected behavior>",
    "actual": "<actual behavior>",
    "context": "<additional context>",
    "steps_to_reproduce": "<reproduction steps>",
    "labels": [],           # leave empty — assembled by create_issue
    "milestone": "<milestone>",
    "assignees": ["<login>"]
  }
)
```

Read the scaffolded file path returned by `scaffold_artifact` and show its content to the user. Offer to adjust before submitting.

> **Important:** Pass the exact file content as the `body` in Step 5. Do NOT retype or reconstruct the body — retyping produces literal `\n` escape sequences instead of real newlines, which breaks formatting on GitHub.

---

## Step 5: Create the issue

After user confirmation, submit with:

```
create_issue(
  issue_type="<ISSUE_TYPE>",
  title="<title>",
  priority="<priority>",
  scope="<scope>",
  body="<rendered markdown from Step 4>",
  is_epic=<true|false>,
  parent_issue=<number>,   # omit if not set
  milestone="<milestone>", # omit if not set
  assignees=["<login>"]    # omit if not set
)
```

Report the created issue number and URL to the user.
