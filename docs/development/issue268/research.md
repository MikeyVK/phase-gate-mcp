<!-- docs/development/issue268/research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-12T14:35Z updated=2026-05-12 -->
# MCP-Tool-First Orchestration: get_work_context Extension and context_loaded Gate

**Status:** FINAL DRAFT
**Version:** 2.0
**Last Updated:** 2026-05-12

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
| `handover_template` | SubRoleSpec required fields from YAML | Required fields for crosschat handover block |

The response delivers everything an agent needs to begin work without reading any static
document. It is the machine-driven equivalent of the AGENTS.md §1.2 startup protocol.

### F_268.7 — context_loaded enforcement gate

On entry to every phase and every cycle, the `context_loaded` flag in `state.json` is
reset to `false` by the state engine as part of writing the new phase/cycle state record.
This is an invariant of the state engine, not a responsibility of the transition tools —
an implementation agent must not land the reset on a transition tool call. All tools
except `get_work_context` and the two force transition tools check this flag as a
pre-condition. When `false`, execution is blocked. Calling `get_work_context` sets the
flag to `true` as a side effect.

**Excluded from the gate:**
- `get_work_context` — the tool that unblocks; must always be callable
- `force_phase_transition` and `force_cycle_transition` — exception paths that must not
  require a context-load acknowledgment mid-correction (see scenario analysis below)

**Phase-skip scenarios with the gate active:**

| Scenario | Steps | Notes |
|----------|-------|-------|
| 1 | `force_phase_transition` directly to target | Cleanest; rationale is required by the tool |
| 2 | Normal transition → `force_phase_transition` | Valid but indirect |
| 3 | Normal transition → `get_work_context` → normal transition | Only if no blocking exit gates |
| 4 | Normal transition → `get_work_context` → `force_phase_transition` | Bypasses exit gates |

**Configuration:** enabled by default. A single config flag allows developers to disable the
gate. No `strict`/`warn` split — warn mode produces ruis without changing behavior and has
no practical value. An explicit opt-out preserves the intent; a degraded mode does not.

**Implementation pattern:** follows the existing `enforcement_event` + `EnforcementRunner`
pattern. A new `check_context_loaded` action type is registered in `enforcement.yaml`. The
`context_loaded` flag is a new field in `state.json` managed by the state engine.

### F_268.8 — Reusable code from feature/263

Cherry-pick targets (hooks/ package excluded — confirmed dead):

| File | Purpose |
|------|---------|
| `src/copilot_orchestration/config/requirements_loader.py` | SubRoleSpec loading backend |
| `src/copilot_orchestration/contracts/interfaces.py` | SubRoleSpec datatype |
| `src/copilot_orchestration/utils/_paths.py` | State file path resolver |
| `.copilot/sub-role-requirements.yaml` | Sub-role config + handover fields |
| `.copilot/_default_requirements.yaml` | Default sub-role config |

Config root question (for design phase): move `.copilot/` files to `.phase-gate/config/` to
match current project convention?

---

## Blast Radius Analysis

### Production code

**`mcp_server/tools/base.py`**
`BaseTool` gains `enforcement_event` support for `check_context_loaded`. No change to the
class structure — the event is registered in `enforcement.yaml`, not hardcoded. The
`BranchMutatingTool` pattern (class variable sets category → enforcement picks it up) is
the model to follow.

**`mcp_server/tools/discovery_tools.py` — `GetWorkContextTool`**
Extended response schema (new fields). Must also set `context_loaded = true` in state as a
side effect of execution. This is a CQS tension point (query that also writes state) — see
Architecture Principles section below.

**`mcp_server/tools/phase_tools.py` — `TransitionPhaseTool`**
No direct change for the `context_loaded` flag. The state engine resets it automatically
on writing new phase state. `ForcePhaseTool` is exempt from the blocking check; the state
engine still resets the flag when it writes new state, so agents must call
`get_work_context` after a forced phase transition before resuming other tool calls.

**`mcp_server/tools/cycle_tools.py` — `TransitionCycleTool`**
No direct change for the `context_loaded` flag. Same state-engine ownership as above.
`ForceCycleTool` exempt from blocking check; flag still reset by state engine on entry.

**`mcp_server/managers/phase_state_engine.py`**
New field `context_loaded: bool` in state model. The engine resets the flag to `false`
on any new phase or cycle state write. A separate method sets it to `true`, called by
`GetWorkContextTool` after delivering context.

**`mcp_server/managers/enforcement_runner.py`**
New action type `check_context_loaded`. Reads the flag from state, returns blocking error
when `false` (and gate is enabled in config). Follows existing `check_pr_status` pattern.

**`.phase-gate/config/enforcement.yaml`**
New entry: event `tool_category: all` (or a new category), timing `pre`,
action `check_context_loaded`. Excludes force tools and `get_work_context` by tool name or
by a new `exempt` list.

**`.phase-gate/config/contracts.yaml`**
New `instructions` section per workflow+phase entry. Read by `get_work_context`, ignored
by transition tools.

**`mcp_server/schemas/` (config schema)**
New schema fields for `instructions` in the contracts YAML loader.

### Test code

**`tests/mcp_server/integration/test_pr_status_lockdown.py`**
This test asserts `len(BRANCH_MUTATING_TOOLS) == 18`. No new branch-mutating tools are
added by this issue — count unchanged. Force tools must be explicitly verified to NOT
inherit `BranchMutatingTool`.

**`tests/mcp_server/unit/tools/test_discovery_tools.py`**
`TestGetWorkContextTool` must be extended: new response fields, `context_loaded` side
effect verification via observable state (not private attribute inspection).

**`tests/mcp_server/unit/managers/test_phase_state_engine.py`**
New tests for `context_loaded` flag: reset by the engine on phase entry, reset on cycle
entry, set by the engine when `get_work_context` marks context loaded. Force transitions
verify that the engine resets the flag (as a state-write side effect) but are not blocked
by the gate pre-check.

**`tests/mcp_server/integration/test_ready_phase_enforcement.py`**
Model for new integration test `test_context_loaded_enforcement.py`: verifies the gate
blocks tools when `context_loaded = false`, unblocks after `get_work_context`, and that
force tools are exempt.

**No backward compatibility with legacy code**: there is no prior `context_loaded`
implementation to be compatible with. The `feature/263` cherry-pick targets contain
`SubRoleSpec` logic that was never merged — no migration layer needed.

---

## Architecture Principles Analysis

### CQS tension in GetWorkContextTool

`get_work_context` is a query (returns context) that must also set `context_loaded = true`
(a state mutation). This is a CQS violation by the strict definition in
ARCHITECTURE_PRINCIPLES.md §5.

**Resolution:** the mutation is a logging/acknowledgment side effect, not a business state
change that affects query results. The architectural precedent for this type of side effect
exists in the codebase (`git_checkout` syncs phase state as a side effect). The correct
framing: `get_work_context` is primarily a command (acknowledge context load) that also
returns the loaded context as its result. The naming is user-facing and cannot change, but
the internal design should treat the state write as the primary action.

This is a design-phase decision.

### Config-First and OCP for the new enforcement action

`check_context_loaded` must be registered in `enforcement.yaml`, not hardcoded in Python
(ARCHITECTURE_PRINCIPLES.md §3, §13). The exemption list for force tools and
`get_work_context` must live in config, not as an `if tool_name == "force_phase_transition"`
chain in the runner.

### ISP for the flag read

The enforcement runner reads `context_loaded` from state. It should receive a narrow
read-only interface (`IStateReader`), not the full `IStateRepository` with write methods
(ARCHITECTURE_PRINCIPLES.md §1.4).

### YAGNI on warn mode

A `strict`/`warn` configuration split was considered and rejected. Warn mode produces
behavioral ruis without changing outcomes and has no practical value. One boolean flag
(enabled/disabled) is the correct scope (ARCHITECTURE_PRINCIPLES.md §9).

---

## Open Questions

All remaining open questions are design or planning questions, not research questions.

1. **CQS resolution for GetWorkContextTool** — should the tool be renamed or restructured
   to make the command nature primary, or is the side-effect framing sufficient?
   *(design)*

2. **Exemption mechanism for force tools** — should exemptions be a named list in
   `enforcement.yaml`, a new tool class variable (`context_gate_exempt: bool = False`),
   or something else?
   *(design)*

3. **Config root for SubRoleSpec YAML** — `.copilot/` (as in feature/263) or
   `.phase-gate/config/` (current convention)?
   *(design)*

4. **`instructions` section optional vs mandatory** — should phases without instructions
   silently omit the field or require an explicit empty declaration to force conscious
   authorship?
   *(design)*

5. **`close-issue` invoker** — is this a `@co` or `@imp` responsibility after human
   PR approval?
6. **`create_handover` tool** — deferred. A dedicated tool that validates handover
   fields against the SubRoleSpec before cross-chat handover is a candidate feature,
   but is not required for #268. The `handover_template` delivered by `get_work_context`
   may be sufficient as a protocol-discipline mechanism. Pick up as a separate issue.
   *(deferred)*

---

## References

- Issue #268 (this issue)
- Issue #263 `feature/263-vscode-implementation-orchestration` (cherry-pick source; not on main)
- Issue #333 results: `AGENTS.md` §1.2, `.github/prompts/open-issue.prompt.md`
- Issue #258 (closed): content_contract gate superseded by #268
- Issue #290 (parent epic): Workflow Intelligence / Agent UX
- `mcp_server/tools/base.py` — `BaseTool`, `BranchMutatingTool`
- `mcp_server/managers/enforcement_runner.py` — `KNOWN_TOOL_CATEGORIES`
- `.phase-gate/config/enforcement.yaml` — existing gate registrations
- `.phase-gate/config/contracts.yaml` — existing workflow+phase gate structure
- `.phase-gate/config/workphases.yaml` — workflow-agnostic phase definitions
- `tests/mcp_server/integration/test_pr_status_lockdown.py` — blast radius reference
