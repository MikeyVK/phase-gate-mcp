---
name: implement-cycle
description: >
  Execute a single TDD cycle for an active issue. Loads focused implementation
  context via Explore sub-agent, runs RED → GREEN → REFACTOR, then invokes a QA
  sub-agent gate before handing off.
agent: imp
argument-hint: >
  Sub-role + issue number + cycle ID + impl model.
  Example: "implementer: issue #302 cycle C_302.1 (impl: claude-sonnet-4.6)"
  Sub-roles: researcher, planner, designer, implementer (default), validator, documenter
---

# Implementation Cycle Protocol

> **Cold-start rule:** You have no prior knowledge of this project, its workflow, or its
> pre-implementation documents. Execute every phase below in order.

---

## Phase 0: Boot

Activate all MCP tool categories before any other call (VS Code lazy-loads these):

```
activate_file_editing_tools
activate_git_workflow_management_tools
activate_branch_phase_management_tools
activate_issue_management_tools
activate_label_management_tools
activate_milestone_and_pr_management_tools
activate_project_initialization_tools
activate_code_validation_tools
```

Synchronize state:

1. Read [agent.md](../../agent.md) — full document.
2. Read [docs/coding_standards/ARCHITECTURE_PRINCIPLES.md](../../docs/coding_standards/ARCHITECTURE_PRINCIPLES.md) — binding contract.
3. `st3://rules/coding_standards`
4. `st3://status/phase` → record `active_branch`
5. `get_work_context` → record `active_issue_number`

<!-- FUTURE HOOK: get_work_context will become a mandatory per-cycle gate checkpoint.
     Branch-mutating tools will be blocked until confirmed called. See agent.md. -->

Extract from the invocation argument:
- `ISSUE_NUMBER` — the active issue number
- `CYCLE_ID` — the cycle to execute (e.g. `C_302.1`)
- Active sub-role (default: `implementer`)

---

## Phase 1: Context Load

Delegate all document reading to the Explore sub-agent.
Do not read pre-implementation docs yourself.

```
runSubagent(
  agent="Explore",
  description="Load cycle context: issue {ISSUE_NUMBER}, cycle {CYCLE_ID}",
  prompt="""
Read ALL files that exist in docs/development/issue{ISSUE_NUMBER}/:
research.md, design.md, planning.md, and any other files present.
Read every file completely.

Return a document with these sections:

## ORIENTATION
Brief summary of the full problem (2–3 sentences per sub-problem A/B/C/...).
State which sub-problem(s) the requested cycle addresses.
State any pre-conditions: which earlier cycles (if any) must be complete before
this cycle can start, and why.

## DESIGN CONTEXT FOR CYCLE {CYCLE_ID}
From the design doc, extract all decisions that are relevant to cycle {CYCLE_ID}.
For each relevant decision:
- Decision ID and title
- The exact before-code verbatim (copy it)
- The exact after-code verbatim (copy it)
- Any constraints, notes, or known limitations stated in the design that affect
  this cycle (import paths, forbidden patterns, architectural principles cited)

## CYCLE {CYCLE_ID} — FULL IMPLEMENTATION CHECKLIST

### RED phase
The exact test code to write, verbatim from the design or planning doc.
Include: test file path, class name, method name(s), full test body.
State the RED condition: exactly why this test fails before any fix is applied.
If multiple test methods are part of this cycle's RED phase, include all of them.

### GREEN phase
Every change needed to make the RED tests pass, in execution order:

For each file that must change:
- File path
- What changes (new function, modified method, deleted override, new import, etc.)
- Exact code to add or replace, verbatim from the design
- Approximate line numbers where stated in the docs

Also list explicitly:
- New imports required in each file
- New fixtures required (name, which conftest.py, exact fixture code)
- All existing call sites that must be updated because of a signature change
  (file path, approximate line, before → after)
- All existing test assertions that must be updated in this cycle
  (file path, line, old assertion string, new assertion string)
- Any runtime operations that are part of GREEN but are not code changes
  (e.g. MCP tool calls for data migration, label creation/deletion)

### REFACTOR phase
Only if the design or planning doc explicitly specifies refactor content for this
cycle. If none: state "No refactor specified."
List: files, quality gate command to run.

## EXIT CRITERIA FOR CYCLE {CYCLE_ID}
List the deliverables and validation items from the planning doc for this cycle.
These are what the QA gate will verify.

## OUT OF SCOPE FOR THIS CYCLE
Items the design explicitly defers or excludes from cycle {CYCLE_ID}.

Thoroughness: thorough.
Copy all code verbatim — do not paraphrase. Implementation depends on exact strings.
  """
)
```

Store the full returned document as `CYCLE_CONTEXT`.
Read it completely. Resolve any ambiguities by reasoning over the design content before touching code.

---

## Phase 2: Execute Cycle

### 2.1 RED

- Write the failing test(s) exactly as specified in `CYCLE_CONTEXT › RED phase`.
- Apply any collateral changes to existing tests listed under GREEN (assertion updates that break because of a message/signature change belong in RED — they must fail together).
- Run: `run_tests(path="<TEST_FILE>::<CLASS>::<METHOD>")` for each new test.
- Confirm: every new test fails for the stated RED condition — not an import error or unrelated failure.
- Commit: `git_add_or_commit(sub_phase="red", cycle_number=<N>, message="...")`

### 2.2 GREEN

Work through the GREEN checklist in `CYCLE_CONTEXT` in order:
- Apply each file change as specified.
- Add all required imports.
- Create all required fixtures.
- Update all existing call sites.
- Execute any runtime operations.
- Run: `run_tests(path="<TEST_FILE>")` after each meaningful unit of change to maintain visibility.
- Final run: `run_tests(path="<TEST_FILE>")` → all tests in scope must be GREEN.
- Commit: `git_add_or_commit(sub_phase="green", cycle_number=<N>, message="...")`

### 2.3 REFACTOR

- Apply only if `CYCLE_CONTEXT › REFACTOR phase` specifies content.
- Run: `run_quality_gates(scope="files", files=[<all files touched this cycle>])`
- Commit if changes were made: `git_add_or_commit(sub_phase="refactor", cycle_number=<N>, message="...")`

---

## Phase 3: QA Gate

Invoke the QA sub-agent. Pass the full `CYCLE_CONTEXT` and a summary of what you did.

```
runSubagent(
  agent="qa",
  description="Post-cycle gate {CYCLE_ID} issue #{ISSUE_NUMBER}",
  prompt="""
Sub-role: validation-reviewer

Verify the completed TDD cycle {CYCLE_ID} for issue #{ISSUE_NUMBER} on branch {ACTIVE_BRANCH}.

## Pre-implementation context (from Explore sub-agent)

{paste full CYCLE_CONTEXT verbatim here}

## What the implementation agent reports

{brief summary: which tests were written, which files were changed, final test run result}

## Your verification task

Using the EXIT CRITERIA in the context above as your primary checklist:

1. Verify each new test exists in the stated file with the stated class and method name.
   Confirm the test body matches the design's intent (not necessarily verbatim — reason
   about whether it correctly tests the stated RED condition).

2. Verify each implementation change matches the design's after-code. Flag any deviation,
   including additions that go beyond what the design specifies (scope creep).

3. Verify all collateral changes (assertion updates, call site updates, fixture additions)
   are applied.

4. Run: run_tests(path="<TEST_FILE>") → confirm GREEN.

5. Verify no files outside the DESIGN CONTEXT's listed files were modified.

6. Assess: does the implementation comply with the architectural constraints cited in
   the design? (Quote the principle and state your assessment.)

Return: PASS or FAIL.
If FAIL: state exact file, exact line, what was found, what was expected.
Be specific — the implementation agent will fix based on your output.
  """
)
```

**If QA returns FAIL:** fix the finding, re-run the affected sub-phase, re-invoke QA.
Do not proceed while there is an open FAIL.

---

## Phase 4: Cycle Completion

Report to the user:
- Cycle `{CYCLE_ID}` complete — QA: PASS
- Tests added: `<list>`
- Files changed: `<list>`
- Next cycle (if stated in planning doc): `<NEXT_CYCLE_ID>`
- Or: all cycles complete — ready for `transition_phase(to_phase="validation")`

Do not call `transition_phase` autonomously. Present it as a suggested next step and wait.

---

## Guardrails

- **MCP tools only** — see agent.md §5 Tool Priority Matrix. No `run_in_terminal` for git / file / test operations.
- **Scope is the files listed in DESIGN CONTEXT** — any other file requires explicit user approval.
- **No unrequested refactoring** — only what the design specifies.
- **Architecture contract is binding** — ARCHITECTURE_PRINCIPLES.md violations are rejected even if all tests pass.
- **Language** — English for code, commits, doc edits. Dutch for user-facing chat.
- **PR merge requires explicit human instruction.**
