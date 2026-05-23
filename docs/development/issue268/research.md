<!-- docs/development/issue268/research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-12T14:35Z updated=2026-05-12 -->
# MCP-Tool-First Orchestration: get_work_context Extension and context_loaded Gate

**Status:** FINAL DRAFT
**Version:** 2.1
**Last Updated:** 2026-05-23


---

## Problem Statement

Hooks-based model context injection is empirically dead (issue #263, Findings 7 and 8: all
three injection paths — UPS systemMessage, PreCompact systemMessage, Stop reason — do not
reach the model). The only reliable context injection path is via MCP tool-call responses.

Agent startup currently relies on reading static markdown files and manual phase detection,
with no machine-enforced context acknowledgment. This creates two failure modes: an agent
that skips static documentation misses its work instructions entirely, and there is no
mechanism to verify that context was loaded before work begins.

Three changes are needed:

1. `get_work_context` extended to deliver phase-specific work instructions in its response
2. An `instructions` section added to `contracts.yaml` per workflow+phase, serving as the
   SSOT for those work instructions
3. A `context_loaded` enforcement gate that blocks tool execution until `get_work_context`
   has been called after each phase or cycle entry

---

## Goals

1. Define the SSOT and structure for workflow+phase work instructions
2. Define the `get_work_context` response extension
3. ~~Define `create_handover` input schema and validation contract~~ *(deferred — see Open Questions #6)*
4. Establish the symmetric lifecycle model (open/close slash commands vs. in-phase tools)
5. Define the `context_loaded` enforcement mechanism
6. Determine blast radius in production and test code

---

## Scope

**In scope:**
- `contracts.yaml` `instructions` section design (conceptual)
- `get_work_context` response extension
- ~~`create_handover` tool contract~~ *(deferred)*
- Branch lifecycle symmetry model
- `context_loaded` enforcement gate design
- Reusable code from `feature/263`
- Blast radius in production and test code

**Out of scope:**
- Hooks infrastructure (confirmed dead in #263)
- `content_contract` gate from #258 (superseded)
- VS Code extension internals
- YAML schema syntax and field naming (design phase)
- Python implementation patterns (design phase)

---

## Background

Issue #263 empirically confirmed that all hook injection paths fail to reach the model.
Agent files (`.agent.md`) were confirmed to work. Issue #333 built on this by establishing
`AGENTS.md` as the three-agent model authority with a human startup protocol:

> "Read AGENTS.md → `get_work_context` → `get_project_plan` → read planning doc"

This human protocol is the authoritative specification that #268 must make instrument-driven.
The `get_work_context` tool already exists and is the mandatory first action for `@imp`.
Extending it is the minimal, correct path — no new mandatory tool, no new protocol.

The existing enforcement infrastructure (enforcement.yaml, `enforcement_event` class
variable on tools, `EnforcementRunner`) provides the pattern for the new gate. A new
`check_context_loaded` action type follows the same registration model as `check_pr_status`
and `check_phase_readiness`.

---

## Findings

### F_268.1 — The only reliable context injection path is tool-call responses

Hooks are dead. Agent files work but are static — they cannot reflect dynamic state (active
phase, current cycle, pending deliverables). The tool-response path is the only mechanism
that is both reliable and dynamic. `get_work_context` is already the established entry
point for this path.

### F_268.2 — contracts.yaml is the correct SSOT for work instructions

`workphases.yaml` defines phase identity independently of workflow type (subphases,
commit-type hints). It is workflow-agnostic by design and the wrong abstraction level for
instructions.

Work instructions are inherently workflow+phase specific. A `research` phase in a `feature`
workflow has different expectations than in a `refactor` workflow. A `hotfix` has no
research phase at all.

`contracts.yaml` already defines behavior per workflow+phase combination via `exit_requires`.
It is the existing authority for what a phase means within a given workflow. An `instructions`
section alongside `exit_requires` is structurally consistent and preserves SSOT:

- Transition tools read `exit_requires` only
- `get_work_context` reads `instructions` only
- Consumer separation enforces SRP without splitting the file

Change-rate asymmetry (gate criteria are stable; instructions evolve with tooling) is managed
by this consumer separation, not by splitting into separate files.

### F_268.3 — The branch lifecycle has exactly two human-triggered boundaries

The branch lifecycle has two moments where no machine state exists to query:

1. **Branch start**: no `state.json`, no linked issue, no active phase. No tool can deliver
   instructions — there is nothing to query. This is bootstrap, not in-phase work.

2. **Post-merge cleanup**: PR approved by human. The branch is no longer the active context.
   Machine state is not authoritative for what happens next.

Both moments require a human-triggered slash command. Everything between these two moments
is covered by `get_work_context`.

### F_268.4 — The lifecycle symmetry model

| Moment | Mechanism | Agent |
|--------|-----------|-------|
| Branch start | `open-issue` slash command | `@co` |
| Every phase/cycle entry | `get_work_context` response | `@imp` |
| PR submission | `submit_pr` (via ready-phase instructions) | `@imp` |
| Post-merge cleanup | `close-issue` slash command | human-triggered |

`open-issue.prompt.md` exists (#333). It currently covers steps 1–3 and 6–7 of the
startup sequence. Steps 4 (`get_project_plan`) and 5 (`get_work_context`) must be added
between `initialize_project` and the first commit.

`close-issue.prompt.md` does not yet exist and must be created as the symmetric counterpart.

### F_268.5 — The ready phase needs no special machine structure

The ready phase instruction is singular: submit the PR and hand over to the human. It fits
the same `instructions` structure as every other phase. Post-approval work lives in
`close-issue`, not in config. No `pre_approval`/`post_approval` split is needed.

### F_268.6 — get_work_context response extension

The current response returns: branch, linked issue, phase, recent commits. Required additions:

| New field | Source | Content |
|-----------|--------|---------|
| `sub_role_hint` | phase → sub-role mapping in instructions config | e.g. `phase=research → researcher` |
| `phase_instructions` | `instructions` section in contracts.yaml for active workflow+phase | What to produce, which tools to use |
| `handover_template` | Static format from AGENTS.md (or contracts.yaml instructions field) | Required fields for crosschat handover block |

The response delivers everything an agent needs to begin work without reading any static

Cherry-pick targets (hooks/ package excluded — confirmed dead):

| File | Purpose |
|------|---------|
| `src/copilot_orchestration/config/requirements_loader.py` | SubRoleSpec YAML loading backend |
| `src/copilot_orchestration/contracts/interfaces.py` | SubRoleSpec datatype |
| `src/copilot_orchestration/utils/_paths.py` | State file path resolver |
| `.copilot/sub-role-requirements.yaml` | Sub-role config + handover required fields |
| `.copilot/_default_requirements.yaml` | Default sub-role config |

**SubRoleSpec is orthogonal to `contracts.yaml instructions`:**

- `contracts.yaml instructions` (F_268.2) = what the agent must produce in this phase.
  Per workflow+phase combination. Delivered by `get_work_context` as `phase_instructions`.
- `SubRoleSpec` = which fields a crosschat handover must contain. Per sub-role
  (e.g. `@imp implementer` must supply `scope`, `files`, `deliverables`, `stop_go_proof`).
  This is the validation schema consumed by the future `create_handover` tool (OQ 6,
  deferred).

**Scope concern for #268:** `create_handover` is deferred (OQ 6). Without that consumer,
the SubRoleSpec YAML loader has no active use in #268. The only remaining use would be
populating the `handover_template` field in `get_work_context`, but the handover format
is already defined statically in AGENTS.md. The cherry-pick of the full YAML+loader stack
may be premature scope. For #268, `handover_template` can be a static format string from
`contracts.yaml instructions` (or hardcoded), deferring SubRoleSpec YAML until
`create_handover` is picked up. **This is an open scope question for design.**

**Config root (OQ 3 resolved):** any SubRoleSpec YAML that does ship in #268 belongs in
`.phase-gate/config/`, not `.copilot/`. Rationale: this project introduces a custom
orchestration model that goes beyond standard VS Code agent orchestration. Forcing
orchestration config into the VS Code-standard `.copilot/` structure would misrepresent
the ownership and scope of the config. `.phase-gate/config/` is the existing convention
for all project orchestration config and is the correct home.

### F_268.7 — context_loaded enforcement gate

On entry to every phase and every cycle, the `context_loaded` flag is reset to `false`
by the state engine as part of writing the new phase/cycle state record. This is an
invariant of the state engine, not a responsibility of the transition tools — an
implementation agent must not land the reset on a transition tool call.

All write-tools check this flag as a pre-condition before execution. Read-only tools are
never gated — reads may always proceed regardless of flag state. When the flag is `false`,
write-tool execution is blocked. Calling `get_work_context` sets the flag to `true` as a
command side-effect (see F_268.9 and Architecture Principles section).

**Gate scope — write vs read distinction:**

The gate applies only to tools that mutate branch state or workspace state. Read-only
tools (`get_project_plan`, `git_status`, `health_check`, `search_documentation`, etc.) are
never gated. This mirrors the existing `branch_mutating` category model: `check_pr_status`
also gates only `branch_mutating` tools, not reads.

This distinction resolves the open-issue edge case: after `initialize_project` (which
creates `state.json`), `@co` can still call `get_project_plan` because it is read-only.
Only write-tools are blocked until `@imp` calls `get_work_context`.

**Excluded from the gate (write-tools that must never be blocked):**
- `get_work_context` — the tool that unblocks; must always be callable
- `force_phase_transition` and `force_cycle_transition` — correction paths that must not
  require a context-load acknowledgment mid-correction
- `initialize_project` — pre-state bootstrap; gate fires only when `state.json` already
  exists for the current branch (see F_268.11 for related bug)
- `git_checkout` and `git_pull` — these are reset-triggers themselves; blocking them
  would be circular

**`git_pull` reset is conditional:** the flag is reset only when the pull is non-noop
(commits were received). An "Already up to date" pull does not invalidate context.

**`git_checkout` always resets:** switching branch always invalidates context, regardless
of whether the target branch has a different phase.

**Phase-skip scenarios with the gate active:**

| Scenario | Steps | Notes |
|----------|-------|-------|
| 1 | `force_phase_transition` directly to target | Cleanest; rationale required by tool |
| 2 | Normal transition → `force_phase_transition` | Valid but indirect |
| 3 | Normal transition → `get_work_context` → normal transition | Only if no blocking exit gates |
| 4 | Normal transition → `get_work_context` → `force_phase_transition` | Bypasses exit gates |

**Configuration:** enabled by default. A single boolean flag allows developers to disable
the gate. No `strict`/`warn` split — warn mode produces noise without behavioral change
and has no practical value (YAGNI, §9).

**Implementation pattern:** new `check_context_loaded` action type registered in
`enforcement.yaml`, following the existing `check_pr_status` handler pattern in
`EnforcementRunner`. A new `IContextLoadedReader` interface is injected into
`EnforcementRunner` alongside the existing `IPRStatusReader` — the blocking infrastructure
(registry, dispatch, `ValidationError`) is reused unchanged.

### F_268.8 — context_loaded is session-scope, not persistent

`context_loaded` is an in-memory flag, not a field in `state.json`. The rationale follows
the same logic as `PRStatusCache` (issue #283): there is no external source of truth to
fall back to, but `false` is the correct default on any cold start.

If the MCP server restarts, or work is picked up in an existing session on another machine
after a `git pull` and `git checkout`, the flag is `false` — the agent must call
`get_work_context` again. This is semantically correct: the agent's context has been lost
and must be reloaded.

**Contrast with `PRStatusCache`:** PR status has an external ground truth (GitHub API) to
fall back to on cold start. `context_loaded` has no external source — `false` as the
default is both the safe and the correct behavior.

**No shared implementation with `PRStatusCache`:** the status-tracking mechanisms are
fundamentally different. The blocking infrastructure (enforcement handler pattern) is
shared via the existing registry — no new infrastructure needed.

### F_268.9 — Reusable code from feature/263

Cherry-pick targets (hooks/ package excluded — confirmed dead):

| File | Purpose |
|------|---------|
| `src/copilot_orchestration/config/requirements_loader.py` | SubRoleSpec loading backend |
| `src/copilot_orchestration/contracts/interfaces.py` | SubRoleSpec datatype |
| `src/copilot_orchestration/utils/_paths.py` | State file path resolver |
| `.copilot/sub-role-requirements.yaml` | Sub-role config + handover fields |
| `.copilot/_default_requirements.yaml` | Default sub-role config |

Config root resolved: `.phase-gate/config/` (see OQ 3 — closed).

### F_268.10 — initialize_project has no guard on existing state (bug)

`InitializeProjectTool.execute()` calls `state_engine.initialize_branch()` unconditionally.
`initialize_branch()` constructs a fresh `BranchState` and overwrites `state.json` via
`_apply_state()` with no check for an existing state record. If `state.json` already exists
for the current branch, all transition history, cycle history, and current phase are silently
destroyed.

This is a bug independent of #268, but it intersects with the gate design:
- When `state.json` exists, `initialize_project` must be blocked — both by the
  `context_loaded` gate (it is a write-tool) and by an explicit guard in the tool itself.
- An agent must not be able to reset the `context_loaded` gate by calling
  `initialize_project` on an already-initialized branch.
- Fix scope: `initialize_branch()` should raise `ValidationError` when a `BranchState`
  already exists for the branch. This fix belongs in a separate issue but must be
  accounted for in the blast radius of #268.

### F_268.11 — MVP approach: validate delivery mechanism before full implementation

The full #268 implementation is substantial (new cache, new enforcement handler, new
interfaces, new YAML sections, extended test suite). Previous orchestration attempts
(hooks in #263) invested similar effort and produced no measurable behavioral change.
Before committing to the full implementation, the core hypothesis must be validated:

**Hypothesis:** if `get_work_context` returns `phase_instructions` in its response, an
agent in a fresh session will follow those instructions without reading static AGENTS.md.

**MVP scope — F_268.6 + F_268.13 (response restructuring), everything else deferred:**

| Component | MVP | Full |
|-----------|-----|------|
| `phase_instructions` field in response | ✅ hardcoded static string | from contracts.yaml |
| `sub_role_hint` field in response | ✅ hardcoded | from contracts.yaml |
| `handover_template` field in response | ✅ hardcoded | from contracts.yaml |
| F_268.13 noise-field removal (`tdd_cycle_info`, `active_issue`, `recent_commits`, `recently_closed`) | ✅ MVP — prerequisite for signal clarity | — |
| F_268.13 BranchState fields added (`workflow_name`, `issue_number`, `parent_branch`) | ✅ MVP — zero cost, already in state | — |
| F_268.13 `include_closed_recent` param removed | ✅ MVP — breaking change with no consumers | — |
| F_268.13 `phase_instructions` promoted to top, conditional `phase_source` | ✅ MVP — structural | — |
| `contracts.yaml instructions` section | ❌ not yet | all workflows × phases |
| `ContextLoadedCache` + interfaces | ❌ not yet | full implementation |
| `check_context_loaded` enforcement gate | ❌ not yet | full implementation |
| `enforce.yaml` new rule | ❌ not yet | full implementation |

**All F_268.13 field changes are MVP-scope and belong in the same implementation cycle as
`phase_instructions`.** The MVP hypothesis — that an agent follows `phase_instructions` in
a fresh session — cannot be validated if the response is still cluttered with noise fields
that bury the signal. The restructuring and the new fields are not optional convenience;
they are preconditions for the validation to be meaningful.



**MVP validation harness — the initialize_project guard bug:**

The MVP is validated using real work, not a synthetic test scenario. After building the
MVP, a new issue is created for the `initialize_project` guard bug (F_268.10). A fresh
`@imp` session on that bug-fix branch becomes the test subject:

1. Build MVP: hardcoded `phase_instructions`, `sub_role_hint`, `handover_template` in
   `get_work_context` response (this issue, implementation cycle 1)
2. Create new issue: `initialize_project` guard — `initialize_branch()` must raise
   `ValidationError` when `state.json` already exists
3. Start fresh `@imp` session on the bug-fix branch
4. Observe: does the agent call `get_work_context`? Does it reference content from
   `phase_instructions` in its first response? Does it follow the prescribed tool order?
   Does the handover match `handover_template` format without reading AGENTS.md?

The bug-fix itself (~5 production lines + 1 test) is real deliverable work. If the agent
executes it correctly while following `phase_instructions`, the delivery mechanism is
validated. If the agent ignores `phase_instructions` but still produces correct work,
the mechanism fails the hypothesis regardless of the output quality.

**Failure modes to distinguish:**
- Field present in response but ignored → formatting problem (field too buried in JSON)
- Field followed in first response but reverted later → context-window pressure problem
- Field followed consistently → mechanism validated; proceed with full #268

**Consequence if MVP fails:** scope reduction — drop the enforcement gate (F_268.7/F_268.8)
and focus only on the response extension as a convenience feature. The enforcement gate
only has value if instructions are actually followed.

**Implementation order:** MVP is the first deliverable of the implementation phase.
Full infrastructure (ContextLoadedCache, enforcement gate) is blocked on MVP validation.
Full infrastructure (ContextLoadedCache, enforcement gate) is blocked on MVP validation.

### F_268.12 — Role model: @co as lifecycle coordinator

The current role definitions are inconsistent in one place: `open-issue` already grants
`@co` write access to branch state (`initialize_project`), but the stated role definition
calls `@co` read-only for git operations. The inconsistency should be resolved by
formalizing the correct definition rather than reverting the `open-issue` behavior.

**Revised role model:**

| Dimension | `@co` | `@imp` | `@qa` |
|-----------|-------|--------|-------|
| Purpose | Lifecycle coordination | Technical execution | Quality judgment |
| Write access | Lifecycle-administrative (branch open/close) | Technical (commits, transitions, files) | Never |
| Decision authority | Priority, scope, go/no-go to implementation | How it is built | Approve or reject |
| Team analogy | Project lead | Developer | QA engineer |

**Lifecycle-boundary writes belong to `@co`:**

- **Lifecycle entry (open-issue):** `create_issue`, `create_branch`, `git_checkout`,
  `initialize_project`, `get_project_plan`
- **Lifecycle exit (close-issue):** `merge_pr`, `close_issue`, optional branch cleanup
- **Never:** commits, file edits, phase transitions, `submit_pr` — those remain `@imp`

**`merge_pr` is a lifecycle-exit write, symmetric with `initialize_project`:**
Both are administrative writes at a lifecycle boundary. The symmetry is structural:

```
open-issue  (@co):  ... → initialize_project  [lifecycle entry]
close-issue (@co):  merge_pr → close_issue      [lifecycle exit]
```

**Why not `@imp`:** `@imp`'s scope closes at `submit_pr`. Starting a new `@imp` session
solely to call `merge_pr` is a session-waste for one administrative tool-call. `@imp`
executes within the branch; merging the branch is a boundary event, not within-branch work.

**Why not `@qa`:** `@qa` must remain unconditionally write-free. The QA verdict is verbal
("GO / NO-GO" in chat), not a mechanical action. If `@qa` can call `merge_pr`, the
role loses its absolute read-only guarantee. `@qa`'s approval is input to `@co`, who
decides to merge.

**Human-in-the-loop protocol with this model:**
```
@qa:   "GO — all gates pass"
         ↓
Human: reads verdict, instructs @co to proceed
         ↓
@co:   merge_pr → close_issue
```

The merge is never automatic. The human triggers it by instructing `@co`. `@co` executes
it. This satisfies the AGENTS.md "PR merge ALWAYS requires human approval" requirement
without requiring a human to manually click GitHub.

**Consequence for `close-issue.prompt.md`:** the slash command for lifecycle exit belongs
to `@co`. It encodes: wait for human instruction (not just `@qa` verdict), call `merge_pr`,
call `close_issue`, optionally clean up branch. This is the symmetric counterpart to
`open-issue.prompt.md`.

**Consequence for `AGENTS.md`:** the `@co` role definition must be updated to explicitly
call out lifecycle-boundary write permissions (`initialize_project`, `merge_pr`,
`close_issue`). The current wording "Read all; create/update issues, labels, milestones"
understates the role.


### F_268.13 — get_work_context response: minimal-orientation contract and field decisions

The current `GetWorkContextTool` response mixes three categories of information:

1. **Orientation** — where the agent is now (branch, phase, role)
2. **Work instructions** — what the agent must do now (`phase_instructions`)
3. **Ancillary data** — recent commits, issue body, TDD cycle details, recently closed issues

The tool contract must be reduced to categories 1 and 2 only. Category 3 belongs in
dedicated read-only tools (`get_project_plan`, `get_issue`, git tooling) that `phase_instructions`
explicitly instructs the agent to call when actually needed. Every category-3 field that
remains in the response is noise that dilutes the `phase_instructions` signal.

**Non-overlap boundary with `get_project_plan`:**
`get_project_plan` owns the planning content: cycle names, deliverables, exit criteria.
`get_work_context` owns the position: which cycle is active, which phase. This boundary
is absolute — the same information must not appear in both tools.

**Fields removed:**

| Field | Reason |
|---|---|
| `tdd_cycle_info` block (name, deliverables, exit_criteria) | Direct overlap with `get_project_plan`; user-confirmed removal |
| `active_issue` (title, body, labels, acceptance_criteria) | Noise during work phases; research phase calls `get_issue(N)` via `phase_instructions` |
| `recent_commits` | Low orientation value; agent has full git tooling |
| `recently_closed` | Co-agent information; no value to `@imp` during work |
| `phase_source` / `phase_confidence` when confidence is high | Debug metadata; invisible during normal operation |

**Fields added (all already in `BranchState`, not currently rendered):**

| Field | Source | Rationale |
|---|---|---|
| `workflow_name` | `BranchState.workflow_name` | Fundamental orientation; agent must know which workflow type is active |
| `issue_number` | `BranchState.issue_number` | Renamed from `linked_issue_number`; sourced from state, not regex on branch name |
| `parent_branch` | `BranchState.parent_branch` | Needed for `submit_pr(base=...)` in ready phase; already read by `get_parent_branch` from the same state field — adding it here eliminates a redundant tool call with zero additional cost |

**Fields changed:**

| Field | Change |
|---|---|
| `current_cycle` | Retain as position indicator only in the phase header line; the full `tdd_cycle_info` block (name, deliverables, exit criteria) is removed. Format: `Phase: 🧪 implementation (cycle 2) → 🔴 red`. The cycle number is positional (`BranchState.current_cycle`), not planning content. Without it the agent cannot supply `cycle_number=N` to `git_add_or_commit`. The total cycle count (`/M`) is **not** shown: it is planning content owned by `get_project_plan` and its inclusion would violate the non-overlap boundary stated in this finding. |
| `phase_source` / `phase_confidence` | Conditional: rendered only when `confidence != 'high'` or source is not `state_json`. Mirrors the existing `phase_error_message` conditional pattern. |
| `phase_instructions` | Promoted to dominant block; rendered first after the orientation header, not last. |
| `linked_issue_number` | Renamed `issue_number` in rendered output and sourced from `BranchState.issue_number` (eliminates fragile regex on branch name). |

**`include_closed_recent` input parameter:** removed. With `recently_closed` removed from
output, the parameter becomes vestigial. No external API consumers exist in this project;
a clean break is preferable to a dead parameter. This is a breaking change to the tool
input schema (`GetWorkContextInput`).

**Resulting minimal output structure:**

```
## Work Context

Branch: `feature/268-...` | Workflow: feature | Issue: #268
Phase: 🔍 research | Role: researcher
[Phase: 🧪 implementation (cycle 2) → 🔴 red | Role: implementer]   ← implementation only
Parent: main
[⚠️ Phase detection: source=reflog, confidence=medium]              ← only when non-high

---

### 🎯 Phase Instructions

[phase_instructions content — operative block]
```

All other content — issue details, commit history, cycle deliverables — is available on
demand via `get_issue`, `get_project_plan`, and git tools. The `phase_instructions` block
should instruct the agent to call those tools when appropriate; `get_work_context` itself
should not duplicate their output.

### F_268.14 — TODO-list discipline is phase-local today and lacks an always-on reinforcement layer

The current issue-268 delivery makes TODO-list usage visible inside per-phase `phase_instructions`, but it does not yet enforce the same discipline through the two global channels that shape `@imp` behavior before or alongside those instructions:

1. **Static implementation-role instructions** in `.github/agents/imp.agent.md`
2. **The fixed orientation header** rendered by `GetWorkContextTool._format_context()`

Repo evidence is consistent:

| Surface | Current behavior | Gap |
|---|---|---|
| `.phase-gate/config/contracts.yaml` | Every governed phase already starts with `Create a TODO list and work through it step by step` or equivalent wording | Strong phase-local discipline exists once the agent is already following the phase script |
| `.github/agents/imp.agent.md` | Startup protocol requires `get_work_context`, architecture review, plan lookup, and worktree inspection | No always-on instruction says TODO-list creation or refresh is mandatory before execution, that only one item may be in progress, or that the list must be updated after each material step |
| `mcp_server/tools/discovery_tools.py` | `get_work_context` renders a compact orientation header, then the first H3 block `### 🎯 Phase Instructions` | No fixed header reminder reinforces TODO-list discipline before the phase script begins |
| `tests/mcp_server/unit/tools/test_discovery_tools.py` | The current contract requires `### 🎯 Phase Instructions` to remain the first H3 block | Any reminder added as a new H3 section would create unnecessary contract churn and break current expectations |

This makes the current gap behavioral rather than structural. The missing piece is not another phase instruction. The missing piece is a persistent reinforcement layer that survives across phases and is visible even before the phase-specific checklist is read in detail.

**Blast radius for the follow-up:**

| Surface | Expected change scope |
|---|---|
| `.github/agents/imp.agent.md` | Small wording-only tightening of always-on TODO-list discipline |
| `mcp_server/tools/discovery_tools.py` | Small formatting change in the orientation/header area of `get_work_context` |
| `tests/mcp_server/unit/tools/test_discovery_tools.py` | Narrow assertion updates or one new regression test for the fixed reminder line |
| Documentation follow-up | Update reference docs after validation so the documented work-context contract matches the new reminder |

**Viable policy options for later phases:**

| Option | Description | Trade-off |
|---|---|---|
| A | Strengthen only `.github/agents/imp.agent.md` | Improves static discipline, but `get_work_context` still misses a live reminder at execution time |
| B | Strengthen only `get_work_context` header | Improves live orientation, but leaves the always-on role contract underspecified |
| C | Reinforce both channels while preserving the current output structure | Smallest complete correction; adds discipline without expanding the work-context payload or phase schema |

Research recommendation: later phases should treat **Option C** as the preferred direction, but preserve the current `get_work_context` shape where `### 🎯 Phase Instructions` remains the first H3 block and the TODO reminder lives in the non-H3 header layer.

## Blast Radius Analysis

### Production code

**`mcp_server/tools/base.py`**
No structural change. The `BranchMutatingTool` ABC pattern is the model for the new
`ContextGatedTool` category (or equivalent enforcement.yaml `tool_category` value).

**`mcp_server/tools/discovery_tools.py` — `GetWorkContextTool`**
Response restructured per F_268.13: noise fields removed (`tdd_cycle_info` block,
`active_issue`, `recent_commits`, `recently_closed`); new fields rendered from existing
`BranchState` data (`workflow_name`, `issue_number`, `parent_branch`); `current_cycle`
retained as compact position indicator in phase header (format: `cycle N`, no total);
`phase_source`/`phase_confidence` made conditional on non-high confidence;
`phase_instructions` promoted to dominant first block; `linked_issue_number` renamed
`issue_number` with state-sourced extraction (eliminates fragile branch-name regex).
`GetWorkContextInput.include_closed_recent` parameter removed (breaking change — no
external consumers). Sets `context_loaded = true` in the in-memory `ContextLoadedCache`
as a command side-effect after delivering context.
**C7 (`TODO(C7)` in discovery_tools.py):** the existing TODO anticipates extending
`WorkflowStatusDTO` to expose `workflow_name`. F_268.13 resolves this differently:
`workflow_name` is already in the `BranchState` object that `get_state()` returns;
render it directly. No DTO extension required.

**`mcp_server/tools/phase_tools.py` — `TransitionPhaseTool`**
No direct change for the `context_loaded` flag. The state engine resets it automatically
on writing new phase state. `ForcePhaseTool` is exempt from the blocking check; the state
engine still resets the flag when it writes new state, so `get_work_context` must be
called before resuming write-tool calls after a forced transition.

**`mcp_server/tools/cycle_tools.py` — `TransitionCycleTool`**
No direct change. Same state-engine ownership as above. `ForceCycleTool` exempt from
blocking check; flag reset by state engine on cycle entry.

**`mcp_server/tools/git_pull_tool.py` — `GitPullTool`**
Conditional reset: if the pull result indicates new commits were received, the
`ContextLoadedCache` flag is reset to `false`. Noop pulls ("Already up to date") do not
reset the flag.

**`mcp_server/tools/git_tools.py` — `GitCheckoutTool`**
Unconditional reset: every branch switch invalidates context. `ContextLoadedCache` flag
reset to `false` on successful checkout, regardless of target branch state.

**`mcp_server/managers/phase_state_engine.py`**
No new field in `BranchState` / `state.json` — `context_loaded` is session-scope.
The state engine signals phase/cycle entry to the `ContextLoadedCache` (injected),
which performs the in-memory reset.

**`mcp_server/state/context_loaded_cache.py`** (new file)
In-memory flag store implementing `IContextLoadedReader` and `IContextLoadedWriter`.
Default state: `false`. Analogous to `PRStatusCache` in structure, without API fallback.

**`mcp_server/core/interfaces/__init__.py`**
New `IContextLoadedReader` and `IContextLoadedWriter` Protocol definitions, alongside
existing `IPRStatusReader` / `IPRStatusWriter`.

**`mcp_server/managers/enforcement_runner.py`**
New `_handle_check_context_loaded` handler registered in `_build_default_registry()`.
New optional constructor parameter `context_loaded_reader: IContextLoadedReader | None`.
Follows existing `pr_status_reader` injection pattern exactly.

**`.phase-gate/config/enforcement.yaml`**
New entry: `tool_category: branch_mutating`, timing `pre`, action `check_context_loaded`,
`exempt_tools: [force_phase_transition, force_cycle_transition]`. Force tools remain
`BranchMutatingTool`; `get_work_context` and `git_checkout` are `BaseTool`
(not `branch_mutating`) and are unaffected by the gate. `git_pull` is `BranchMutatingTool`
(gated) but is listed in `exempt_tools` to prevent circular blocking — it must be able to
pull updates before `get_work_context` has been called. `initialize_project` is `branch_mutating`
but the handler returns early when `state.json` does not exist.

**`.phase-gate/config/contracts.yaml`**
New `instructions` section per workflow+phase entry.

**`mcp_server/schemas/` (config schema)**
New schema fields for `instructions` in the contracts YAML loader.

**`mcp_server/config/schemas/enforcement_config.py`**
`EnforcementAction` has `model_config = ConfigDict(extra="forbid")`. New optional field
`exempt_tools: list[str] = []` required. A `model_validator` must validate that
`exempt_tools` is only present on action types that support exemption (e.g.
`check_context_loaded`). Without this schema change, adding `exempt_tools:` to
`enforcement.yaml` triggers a `ConfigError` at startup — correct Fail-Fast behavior,
but the field must exist in the schema first.

### Test code

**`tests/mcp_server/integration/test_pr_status_lockdown.py`**
This test asserts `len(BRANCH_MUTATING_TOOLS) == 18`. Count unchanged — no new
`BranchMutatingTool` subclasses are added. Force tools must be verified to STILL
inherit `BranchMutatingTool` — they are exempt only from `check_context_loaded` via
`exempt_tools`, not from `check_pr_status`.

**`tests/mcp_server/unit/state/test_context_loaded_cache.py`** (new file)
Analogous to `test_pr_status_cache.py`. Tests: default `false`, set `true`, reset to
`false`, independence per session.

**`tests/mcp_server/unit/tools/test_discovery_tools.py`**
`TestGetWorkContextTool` extended: new response fields, `context_loaded` side-effect
verification via observable `IContextLoadedReader` state (not private attribute access).

**`tests/mcp_server/unit/tools/test_git_pull_tool.py`**
New test: flag reset on non-noop pull; flag unchanged on noop pull.

**`tests/mcp_server/unit/tools/test_git_tools.py` (GitCheckoutTool section)**
New test: flag reset on successful checkout.

**`tests/mcp_server/unit/managers/test_phase_state_engine.py`**
New tests: state engine signals `ContextLoadedCache` on phase entry; on cycle entry;
force transitions also signal reset (state-write side effect).

**`tests/mcp_server/integration/test_context_loaded_enforcement.py`** (new file)
Modelled on `test_ready_phase_enforcement.py`: gate blocks write-tools when flag is
`false`; unblocks after `get_work_context`; force tools are never blocked; read-only
tools are never blocked regardless of flag state.

**No backward compatibility with legacy code**: no prior `context_loaded` implementation
exists. `feature/263` cherry-pick targets contain `SubRoleSpec` logic never merged —
no migration layer needed.

## Architecture Principles Analysis

### CQS tension in GetWorkContextTool — resolved

`get_work_context` sets `context_loaded = true` as a side effect, which is a CQS tension
(§5: methods return a value OR mutate state, not both). Resolution: every MCP tool
`execute()` always returns a `ToolResult` — there are no pure query tools at the tool
layer. `submit_pr` writes `PRStatus.OPEN` and returns a result; `merge_pr` writes
`PRStatus.ABSENT` and returns a result. The `execute()` method is by convention a
command-with-result. §5 governs domain methods (e.g., preventing `get_state()` from
calling `save()`), not the tool execution layer. No CQS violation, no design-phase
decision needed. **OQ 1 closed.**

### Config-First and OCP for the new enforcement action

`check_context_loaded` must be registered in `enforcement.yaml`, not hardcoded in Python
(ARCHITECTURE_PRINCIPLES.md §3, §13). The exemption mechanism — which tools are outside
the gated category — belongs in config as a `tool_category` value, not as an
`if tool_name == ...` chain in the runner. **OQ 2 resolved — Optie B:** `exempt_tools`
list at the action level in `enforcement.yaml`. The exempt list is action-type-specific:
it applies only to `check_context_loaded`, not to `check_pr_status`. Force tools remain
`BranchMutatingTool` and are still blocked by `check_pr_status` after `submit_pr` —
the exemption is chirurgical. `initialize_project` is handled by an early return in the
handler when `state.json` does not exist (not via the exempt list).

### ISP for the flag read

The enforcement runner reads `context_loaded` via `IContextLoadedReader`. It should not
receive a write interface (ARCHITECTURE_PRINCIPLES.md §1.4). Analogous to `IPRStatusReader`
vs `IPRStatusWriter` split already present in the codebase.


### YAGNI on warn mode

A `strict`/`warn` configuration split was considered and rejected. One boolean flag
(enabled/disabled) is the correct scope (ARCHITECTURE_PRINCIPLES.md §9).



All remaining open questions are design or planning questions, not research questions.

1. ~~**CQS resolution for GetWorkContextTool**~~ — resolved in Architecture Principles
   section: `execute()` is a command-with-result at the tool layer; no CQS violation.
   *(closed)*

2. ~~**Exemption mechanism for force tools**~~ — resolved: Optie B — `exempt_tools`
   list in `enforcement.yaml` at the action level, scoped to `check_context_loaded` only.
   Does not affect `check_pr_status`; force tools remain blocked after `submit_pr`.
   `initialize_project` pre-state exemption: early return in handler when `state.json`
   absent, not via exempt list. *(closed)*

3. ~~**Config root for SubRoleSpec YAML**~~ — deferred with `create_handover` (OQ 6).
   SubRoleSpec YAML has no consumer in #268 without that tool; the cherry-pick scope is
   premature. If any SubRoleSpec YAML does ship in #268, it belongs in `.phase-gate/config/`
   (custom orchestration model must not be forced into VS Code-standard `.copilot/`
   structure). *(deferred with OQ 6)*

4. ~~**`instructions` section optional vs mandatory**~~ — resolved: mandatory (Optie B).
   Phases without instructions require an explicit empty declaration; the ConfigLoader raises
   at startup on missing sections (Fail-Fast §4). However: the `instructions` section is
   NOT populated in this issue's MVP. The MVP hardcodes field values in the tool response
   for one workflow+phase. Full `contracts.yaml instructions` authorship is gated on MVP
   validation (see F_268.11). *(closed — implementation deferred past MVP)*

5. ~~**`close-issue` invoker**~~ — resolved: `@co` (lifecycle coordinator role).
   `merge_pr` and `close_issue` are lifecycle-exit writes, symmetric with
   `initialize_project` on entry. `@imp` scope closes at `submit_pr`. `@qa` must
   remain unconditionally write-free. Human-in-the-loop: human instructs `@co` after
   reading `@qa` verdict; `@co` calls `merge_pr` → `close_issue`. See F_268.12.
   Blast radius: `AGENTS.md` `@co` role definition and new `close-issue.prompt.md`.
   *(closed)*

6. **`create_handover` tool** — deferred. A dedicated tool that validates handover
   fields against the SubRoleSpec before cross-chat handover is a candidate feature,
   but is not required for #268. The `handover_template` delivered by `get_work_context`
   may be sufficient as a protocol-discipline mechanism. Pick up as a separate issue.
   *(deferred)*

7. ~~**`initialize_project` guard bug**~~ — resolved scope: separate issue, fixed as
   part of the MVP validation harness. After the MVP is built, a new issue is opened for
   the guard fix (~5 production lines + 1 test). The bug-fix work session is the MVP
   test subject: an agent on that branch calls `get_work_context`, receives
   `phase_instructions`, and executes the fix. Correct execution while following
   instructions validates the delivery mechanism. *(separate issue — MVP validation
   harness)*


## Approved Strategy

| Boundary / consumer scope | Selected strategy | Rationale | Constraints for later phases |
|---|---|---|---|
| `@imp` startup discipline plus `get_work_context` orientation output | Preserve compatibility for the current work-context structure while adding a small, always-on TODO-discipline reinforcement | The gap is behavioral, not architectural. Existing phase instructions already carry TODO discipline, and current tests already protect `### 🎯 Phase Instructions` as the first H3 block. The safest correction strengthens behavior without reopening the response contract or widening scope. | Later phases may tighten `.github/agents/imp.agent.md` and add a non-H3 TODO reminder in the `get_work_context` header. They must not add a new top-level H3 block before `### 🎯 Phase Instructions`, must not reintroduce old work-queue payload fields, and must keep the change limited to the small blast radius identified in F_268.14. |

## References
- Issue #268 (this issue)
- Issue #263 `feature/263-vscode-implementation-orchestration` (cherry-pick source; not on main)
- Issue #333 results: `AGENTS.md` §1.2, `.github/prompts/open-issue.prompt.md`
- Issue #258 (closed): content_contract gate superseded by #268
- Issue #290 (parent epic): Workflow Intelligence / Agent UX
- `.github/agents/imp.agent.md` — current static implementation-role instructions
- `mcp_server/tools/base.py` — `BaseTool`, `BranchMutatingTool`
- `mcp_server/tools/discovery_tools.py` — current work-context header and phase-instructions renderer
- `mcp_server/managers/enforcement_runner.py` — `KNOWN_TOOL_CATEGORIES`
- `.phase-gate/config/enforcement.yaml` — existing gate registrations
- `.phase-gate/config/contracts.yaml` — existing workflow+phase gate structure
- `.phase-gate/config/workphases.yaml` — workflow-agnostic phase definitions
- `tests/mcp_server/unit/tools/test_discovery_tools.py` — current output-contract guardrails
- `tests/mcp_server/integration/test_pr_status_lockdown.py` — blast radius reference
