# Bug Workflow Phase Instructions — Hardcoded MVP Content (issue #268)

**Status:** MVP hardcoded content — will migrate to contracts.yaml in C6
**Scope:** `bug` workflow, all 7 phases
**Source of truth for:** `_PHASE_INSTRUCTIONS_MAP` entries in `discovery_tools.py`

---

## How to read this document

Each section below describes one phase of the `bug` workflow.
The instruction text is what `get_work_context` renders as `phase_instructions`.
`sub_role_hint` is rendered as a separate field — it is NOT repeated in the instructions.

---

## Phase 1 — research

**sub_role_hint:** `researcher`

**phase_instructions:**

```
Create a TODO list now and work through it step by step:

[ ] Call get_issue(issue_number=N) — read problem, expected behavior,
    and all linked code locations.
[ ] Locate root cause: grep_search + read_file on affected files and methods.
[ ] Identify all callers: vscode_listCodeUsages or grep_search.
[ ] scaffold_artifact(artifact_type='research', name='issueN-research').
    Required sections: Problem, Root Cause, Affected Files, Impact,
    Solution Options A and B, Recommended Option + Rationale.
[ ] Exit gate: docs/development/issueN/research*.md must exist.
[ ] git_add_or_commit(workflow_phase='research', message='Add research: ...')
[ ] transition_phase(branch='...', to_phase='design')
[ ] get_work_context (mandatory after every transition)

Produce this hand-over before ending the session:
### Research → Design hand-over
**Root cause:** <one sentence>
**Affected method(s):** <file:method>
**Recommended option:** <A or B> — <rationale>
**Key constraint:** <architectural rule that applies>
**Scope for designer:** elaborate chosen option only; do not implement yet.
```

---

## Phase 2 — design

**sub_role_hint:** `designer`

**phase_instructions:**

```
Create a TODO list now and work through it step by step:

[ ] Read: docs/development/issueN/research.md (or Research → Design hand-over).
[ ] Elaborate chosen option:
    - exact method signature changes (parameters, return types)
    - new error type(s) to introduce (name, base class, message format)
    - edge cases: state absent, branch mismatch, concurrent writes
    - callers that need updating
[ ] Define test strategy: which tests (unit/integration), mock boundaries,
    coverage targets.
[ ] scaffold_artifact(artifact_type='design', name='issueN-design').
    Required sections: Chosen Solution, Implementation Details,
    Affected Interfaces, Edge Cases, Test Strategy.
[ ] Exit gate: docs/development/issueN/design*.md must exist.
[ ] git_add_or_commit(workflow_phase='design', message='Add design: ...')
[ ] transition_phase(branch='...', to_phase='planning')
[ ] get_work_context (mandatory after every transition)

Produce this hand-over before ending the session:
### Design → Planning hand-over
**Changed methods:** <file:method — before/after signature>
**New error type:** <ClassName(BaseClass) — message format>
**Edge cases covered:** <N edge cases listed>
**Estimated TDD cycles:** <1–3>
**Test file:** <path>
**Implementation file:** <path>
**Scope for planner:** split into cycles; do not write code yet.
```

---

## Phase 3 — planning

**sub_role_hint:** `planner`

**phase_instructions:**

```
Create a TODO list now and work through it step by step:

[ ] Read: research + design documents (or summaries from hand-overs).
[ ] Decide cycle count (bugs: 1–2 cycles, max 3).
[ ] Per cycle: define name, deliverables (concrete output items),
    exit_criteria (one sentence per cycle).
[ ] scaffold_artifact(artifact_type='planning', name='issueN-planning').
[ ] save_planning_deliverables(issue_number=N, planning_deliverables={
      'tdd_cycles': {'total': N, 'cycles': [
        {'cycle_number': 1, 'name': '...', 'deliverables': ['...'],
         'exit_criteria': '...'}
      ]}
    })
[ ] Exit gate: docs/development/issueN/planning*.md must exist.
[ ] git_add_or_commit(workflow_phase='planning', message='Add planning: ...')
[ ] transition_phase(branch='...', to_phase='implementation')
[ ] get_work_context (mandatory after every transition)

Produce this hand-over before ending the session:
### Planning → Implementation hand-over
**Total cycles:** N
**Cycle 1:** <name>
  - Deliverables: <list>
  - Exit criteria: <sentence>
**Test file:** <path>
**Implementation file:** <path>
**Scope for implementer:** execute cycles in strict RED→GREEN→REFACTOR order only.
```

---

## Phase 4 — implementation

**sub_role_hint:** `implementer`

**phase_instructions:**

```
Create a TODO list now and work through it step by step:

[ ] Call get_project_plan(issue_number=N) — read ALL cycle deliverables
    before writing any code.

Per cycle (repeat until all cycles complete):
[ ] RED: write failing test first — no implementation code yet.
    run_tests(path='<test file>') — verify it FAILS.
    git_add_or_commit(workflow_phase='implementation', sub_phase='red',
      cycle_number=N, message='...')
[ ] GREEN: write minimal code to pass the test — no cleanup yet.
    run_tests(path='<test file>') — verify it PASSES.
    git_add_or_commit(workflow_phase='implementation', sub_phase='green',
      cycle_number=N, message='...')
[ ] REFACTOR: clean up while keeping tests green.
    run_quality_gates(scope='files', files=['<changed files>'])
    git_add_or_commit(workflow_phase='implementation', sub_phase='refactor',
      cycle_number=N, message='...')
[ ] If more cycles: transition_cycle(to_cycle=N+1), then get_work_context.

Hard rules — never violate:
- RED is mandatory. Never write implementation before a failing test.
- Never skip REFACTOR. Quality gates are enforced here.
- Never self-declare GO. QA decides after reviewing the hand-over.
- Never call merge_pr. Human approval is required.

Produce this hand-over when all cycles are complete:
### Imp → QA hand-over
#### Scope
- Cycles executed: <list>
- Out of scope: <list>
#### Files
**Tests:** <path> (new/modified)
**Implementation:** <path> (new/modified)
#### Deliverables
- C1.D1: <name> — ✅ satisfied | ❌ not satisfied
#### Stop-Go Proof
- Tests: run_tests(path='...') → <N passed, 0 failed>
- Gates: run_quality_gates(scope='files') → <N/N green>
```

---

## Phase 5 — validation

**sub_role_hint:** `validator`

**phase_instructions:**

```
Create a TODO list now and work through it step by step:

[ ] Read the Imp→QA hand-over from the implementation session.
[ ] get_project_plan(issue_number=N) — verify all deliverables satisfied.
[ ] run_tests(scope='full') — full suite, zero failures required.
[ ] run_quality_gates(scope='branch') — all branch-changed files.
[ ] Gate 7 — Architectural review (ARCHITECTURE_PRINCIPLES.md):
    [ ] SRP: each new/changed class has one responsibility.
    [ ] OCP: no new if-chain on phase/workflow/action names.
    [ ] DIP: no direct instantiation inside execute().
    [ ] CQS: no query method calls save() or mutates state.
    [ ] Config-First: no hardcoded phase/workflow names in production.
    [ ] No import-time side effects.
    [ ] ISP: read-only consumers use narrow read-only interface.
[ ] If any check fails: produce STOP verdict, list findings, stop here.
[ ] If all green: git_add_or_commit + transition_phase(to_phase='documentation')
[ ] get_work_context (mandatory after every transition)

Produce this hand-over before ending the session:
### Validation hand-over
**Verdict:** STOP | GO
**Tests:** run_tests(scope='full') → <N passed, 0 failed>
**Gates:** run_quality_gates(scope='branch') → <N/N green>
**Architecture:** GO: no violations | STOP: <file>:<line> — <principle>
**For documenter:** PR bullets: <2–3 key changes in plain English>
```

---

## Phase 6 — documentation

**sub_role_hint:** `documenter`

**phase_instructions:**

```
Create a TODO list now and work through it step by step:

[ ] Confirm validation verdict is GO before proceeding. STOP if verdict is STOP.
[ ] Read validation hand-over for PR description bullets.
[ ] Check for affected reference documentation:
    docs/reference/ — if a tool signature or behavior changed.
    docs/coding_standards/ — if an architectural pattern was applied newly.
    AGENTS.md — if agent workflow was affected.
[ ] Update affected reference docs using safe_edit_file.
[ ] git_add_or_commit(workflow_phase='documentation', message='Document: ...')
[ ] transition_phase(branch='...', to_phase='ready')
[ ] get_work_context (mandatory after every transition)

Produce this hand-over before ending the session:
### Documentation hand-over
**Updated docs:** <path — what changed> (or: none required)
**PR body:**
## Summary
<2–3 sentences: what was fixed and why>
## Changes
- <bullet per meaningful change>
## Test coverage
- <N new tests> covering: <what>
```

---

## Phase 7 — ready

**sub_role_hint:** `documenter`

**phase_instructions:**

```
Create a TODO list now and work through it step by step:

[ ] Confirm phase=ready via get_work_context output.
[ ] submit_pr(
      head='<current branch>',
      base='<parent branch from get_work_context>',
      title='fix: <description> (#N)',
      body='<PR body from documentation hand-over>'
    )
    Note: submit_pr is atomic — it neutralizes branch-local artifacts,
    commits, pushes, and creates the GitHub PR in one call.
    Do NOT push manually before calling submit_pr.
[ ] Report the PR URL to the user.
[ ] STOP. Do not call merge_pr. Human approval is required.
```

---

## Refinement notes

_Use this section to capture feedback from validation runs before content migrates to contracts.yaml._

| Date | Phase | Finding | Action |
|------|-------|---------|--------|
| 2026-05-13 | research/design | get_work_context response was empty — map had only (feature, implementation) | Added all 7 bug phases |
