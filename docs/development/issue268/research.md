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

Config root question (for design phase): move `.copilot/` files to `.phase-gate/config/`
to match current project convention?

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

| `.copilot/sub-role-requirements.yaml` | Sub-role config + handover fields |
| `.copilot/_default_requirements.yaml` | Default sub-role config |

Config root question (for design phase): move `.copilot/` files to `.phase-gate/config/` to
match current project convention?

---

## Blast Radius Analysis

### Production code

**`mcp_server/tools/base.py`**
`BaseTool` gains `enforcement_event` support for `check_context_loaded`. No change to the
**`mcp_server/tools/base.py`**
No structural change. The `BranchMutatingTool` ABC pattern is the model for the new
`ContextGatedTool` category (or equivalent enforcement.yaml `tool_category` value).

**`mcp_server/tools/discovery_tools.py` — `GetWorkContextTool`**
Extended response schema (new fields: `sub_role_hint`, `phase_instructions`,
`handover_template`). Sets `context_loaded = true` in the in-memory
`ContextLoadedCache` as a command side-effect after delivering context.

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
New entry: `tool_category: context_gated` (or equivalent), timing `pre`,
action `check_context_loaded`. Force tools, `get_work_context`, `git_checkout`,
`git_pull`, and `initialize_project` (pre-state) are outside this category.

**`.phase-gate/config/contracts.yaml`**
New `instructions` section per workflow+phase entry.

**`mcp_server/schemas/` (config schema)**
New schema fields for `instructions` in the contracts YAML loader.


**`mcp_server/schemas/` (config schema)**
**`tests/mcp_server/integration/test_pr_status_lockdown.py`**
This test asserts `len(BRANCH_MUTATING_TOOLS) == 18`. Count unchanged — no new
`BranchMutatingTool` subclasses are added. Force tools must be verified to NOT inherit
`BranchMutatingTool`.

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
`if tool_name == ...` chain in the runner. **OQ 2 partially resolved:** gate scope is
defined by category membership (write-tools carry the category; read-tools and exempt
write-tools do not). The exact category name and exemption representation is a design
question.

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

2. ~~**Exemption mechanism for force tools**~~ — partially resolved: gate scope is
   category-based (write-tools carry the gated category; read-tools and exempt write-tools
   do not). Exact category name and config representation is a design question.
   **Remaining:** category name choice and how `initialize_project` exemption is expressed
   when `state.json` does not yet exist. *(design)*

3. ~~**Config root for SubRoleSpec YAML**~~ — resolved: `.phase-gate/config/` (Optie A).
   Rationale: this project introduces a custom orchestration model beyond VS Code standard
   orchestration; forcing config into `.copilot/` misrepresents ownership. Additionally:
   SubRoleSpec YAML cherry-pick may be out of scope for #268 (no consumer until
   `create_handover` is picked up). If any SubRoleSpec YAML ships in #268, it belongs in
   `.phase-gate/config/`. *(closed)*

4. **`instructions` section optional vs mandatory** — should phases without instructions
   silently omit the field or require an explicit empty declaration to force conscious
   authorship?
   *(design)*

5. **`close-issue` invoker** — is this a `@co` or `@imp` responsibility after human
   PR approval?
   *(planning)*

6. **`create_handover` tool** — deferred. A dedicated tool that validates handover
   fields against the SubRoleSpec before cross-chat handover is a candidate feature,
   but is not required for #268. The `handover_template` delivered by `get_work_context`
   may be sufficient as a protocol-discipline mechanism. Pick up as a separate issue.
   *(deferred)*

7. **`initialize_project` guard bug** — when `state.json` already exists for the current
   branch, `initialize_project` silently overwrites all state. Fix: `initialize_branch()`
   must raise `ValidationError` on existing state. Separate issue required; blast radius
   of #268 must account for the guard being in place before the gate can rely on it.
   *(separate issue, design blocker for gate)*


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
