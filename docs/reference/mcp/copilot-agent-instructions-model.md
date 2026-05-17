<!-- docs/reference/mcp/copilot-agent-instructions-model.md -->
<!-- template=generic_doc version=43c84181 created=2026-05-17 updated=2026-05-17 -->
# Copilot Agent Instructions Model

**Status:** DEFINITIVE
**Version:** 1.0
**Last Updated:** 2026-05-17

---

## Purpose

This document explains in one place how the GitHub Copilot instruction files and the
`phase-gate-mcp` server cooperate to enforce workflow discipline in VS Code. It is intended
for developers, integrators, and any AI agent starting fresh on this project.

After reading this document you will understand:
- which instruction files exist and what each one does
- how VS Code decides what to inject into a chat session
- where the `phase-gate-mcp` server fits into that flow
- how `phase_instructions` and `sub_role_hint` from `get_work_context` override static
  instructions at runtime
- what the three-agent model looks like and why the tools are restricted the way they are

## Scope

**In Scope:**
- VS Code instruction primitive hierarchy and loading mechanics
- Project-specific file roles (`copilot-instructions.md`, `AGENTS.md`, `.agent.md` files)
- Three-agent model (`@co`, `@imp`, `@qa`) and tool restrictions
- `get_work_context` integration: `phase_instructions` and `sub_role_hint`
- Context loading order per session type
- Design decisions and known deviations from Microsoft guidance

**Out of Scope:**
- MCP tool API details — see [tools/README.md][tools-ref]
- Phase-gate enforcement internals (EnforcementRunner, contracts.yaml) — see [mcp_vision_reference.md][vision-ref]
- Git workflow mechanics — see [GIT_WORKFLOW.md][git-workflow]

## Prerequisites

Read these first:
1. [mcp_vision_reference.md][vision-ref] — what the MCP server is and why it exists
2. [AGENTS.md][agents-md] — three-agent model quick reference

---

## 1. VS Code Instruction Primitive Hierarchy

GitHub Copilot in VS Code supports several instruction primitives. They differ in when they
are loaded and what they are for.

| Primitive | File pattern | When loaded | Purpose |
|-----------|-------------|-------------|---------|
| **Agent instructions** | `copilot-instructions.md` or `AGENTS.md` | **Always** — every chat interaction | Workspace-wide standards |
| **Custom agent** | `.github/agents/*.agent.md` | On demand — when that `@agent` is invoked | Role-specific persona, tools, startup |
| **File instructions** | `.github/instructions/*.instructions.md` | When file matches `applyTo:` glob | File-type or folder-specific guidelines |
| **Prompts** | `.github/prompts/*.prompt.md` | On demand — when invoked as `/command` | Single focused task with parameters |

### 1.1 Agent Instructions (Always-On)

Microsoft documents two file choices — use exactly one:

| File | Location | Format |
|------|----------|--------|
| `copilot-instructions.md` | `.github/` | Recommended; cross-editor |
| `AGENTS.md` | repo root or subfolders | Open standard; monorepo support |

**Microsoft's design intent:** minimal, concise, actionable. Only what is relevant to every
interaction. Link to detailed docs rather than embedding them.

**Core principles (from Microsoft reference docs):**
1. Minimal by default — only what matters for *every* task
2. Concise and actionable — every line should guide behavior
3. Link, don't embed — reference docs instead of copying content
4. Keep current — update when practices change

### 1.2 Custom Agents (`.agent.md`)

An `.agent.md` file defines a named agent available in the VS Code agent picker (`@name`).
It is loaded **only** when that agent is explicitly invoked in a chat session.

Key frontmatter fields:
```yaml
description: "..."          # Discovery surface — how parent agents find this agent
tools: [...]                # Tool allowlist — enforced by VS Code at runtime
argument-hint: "..."        # Guidance shown to the user in the picker
handoffs: [...]             # Transitions to other agents
```

The `tools:` list is the primary enforcement mechanism. VS Code silently blocks any tool
call not in the list. This is how `@qa`'s read-only constraint is enforced — not by
text instruction, but by omitting mutation tools from the frontmatter.

---

## 2. This Project's Instruction File Architecture

This project uses **both** `copilot-instructions.md` and `AGENTS.md`. This is a deliberate
deviation from Microsoft's "use only one" guidance. The roles are explicitly split:

| File | Role | Content |
|------|------|---------|
| `.github/copilot-instructions.md` | **Operational reference** | Tool priority matrix, TDD protocol, quality gates, architecture contract quick ref, prime directives |
| `AGENTS.md` (root) | **Coordination manifest** | Three-agent model, sub-roles, hand-over formats, links to agent files |
| `.github/agents/co.agent.md` | **@co role** | Coordination startup, sub-roles, tool allowlist (GitHub + read-only) |
| `.github/agents/imp.agent.md` | **@imp role** | Implementation startup, scope lock, architecture contract, hand-over format |
| `.github/agents/qa.agent.md` | **@qa role** | Review startup, suppression audit, verification workflow, tool allowlist (read-only) |

### Why two always-on files?

`copilot-instructions.md` concentrates the *how* (procedures, tool matrix, TDD steps). It is
loaded for every interaction including default Copilot chat, so it keeps the operational
protocols always visible.

`AGENTS.md` concentrates the *who and coordination* (agent boundaries, hand-over formats,
two-chat model). Keeping them in a separate file avoids one massive file and aligns with
the multi-agent use case that `AGENTS.md` was designed for.

### What should NOT be in the always-on files

Per Microsoft's "minimal by default" principle, the always-on files must not contain:
- Detailed startup protocols for specific agent roles (belongs in `.agent.md`)
- Phase-specific workflow instructions (served dynamically by `get_work_context`)
- Content duplicated from the other always-on file

---

## 3. The Three-Agent Model

### Agent Roles

| Agent | Invocation | Mission | File |
|-------|-----------|---------|------|
| `@co` | `@co <sub-role>: <task>` | Coordination authority — assess, prioritize, author issues | [co.agent.md][co-agent] |
| `@imp` | `@imp <sub-role>: <task>` | Implementation executor — code, tests, commits, phase transitions | [imp.agent.md][imp-agent] |
| `@qa` | `@qa <sub-role>: <task>` | QA authority — read-only review, test runs, verdicts | [qa.agent.md][qa-agent] |

### Sub-Roles

Each agent has sub-roles that bind to a phase of the workflow:

**`@co`:** `triager` (default), `backlog-reviewer`, `tracker`, `issue-author`

**`@imp`:** `researcher` (default), `planner`, `designer`, `implementer`, `validator`, `documenter`

**`@qa`:** `design-reviewer` (default), `plan-verifier`, `verifier`, `validation-reviewer`, `doc-reviewer`

### Tool Restrictions by Agent

Tool restrictions are enforced by VS Code at the frontmatter level, not by text instruction.

| Capability | `@co` | `@imp` | `@qa` |
|------------|-------|--------|-------|
| Read files, search | ✅ | ✅ | ✅ |
| Run tests / quality gates | ❌ | ✅ | ✅ |
| Edit files (`safe_edit_file`) | ❌ | ✅ (via MCP) | ❌ |
| Git operations | ❌ read-only | ✅ (via MCP) | ❌ read-only |
| GitHub issue/label/milestone | ✅ | ✅ (via MCP) | ❌ read-only |
| Phase transitions | ❌ | ✅ (via MCP) | ❌ |
| All `phase-gate-mcp/*` tools | ❌ (explicit allowlist) | ✅ (wildcard) | ❌ (explicit allowlist) |

`@imp` uses `tools: ["phase-gate-mcp/*"]` — all MCP tools. `@co` and `@qa` use explicit
per-tool allowlists that exclude mutation operations.

### Two-Chat Model

Use separate VS Code chat sessions for each role. This prevents role contamination:

```
User → @co triager: assess incoming issue → Co→Imp hand-over
User → @imp implementer: execute cycle X  → Imp→QA hand-over
User → @qa verifier: review C_LOADER.5   → GO/NOGO verdict
```

Never mix roles in one session. Fresh context prevents authority confusion and scope drift.

---

## 4. Phase-Gate MCP Integration

### 4.1 `get_work_context` — the runtime context bridge

The `get_work_context` MCP tool is the bridge between the static instruction files and the
dynamic workflow state. It reads the active branch's `.phase-gate/state.json`, queries the
GitHub issue, and returns a context block that agents can act on immediately.

**Key fields returned:**

| Field | Type | Purpose |
|-------|------|---------|
| `current_phase` | string | Active workflow phase |
| `current_branch` | string | Active git branch |
| `workflow_name` | string | Active workflow type (feature/bug/etc.) |
| `active_issue` | object | GitHub issue title, number, labels |
| `sub_role_hint` | string | Suggested `@imp` sub-role for the current phase |
| `phase_instructions` | string | **Operational TODO list for the current phase** |

### 4.2 `phase_instructions` — dynamic operational script

`phase_instructions` is a multi-line string that contains the complete TODO list for the
current (workflow, phase) combination. It is generated by `GetWorkContextTool` from a
lookup table (`_PHASE_INSTRUCTIONS_MAP`) keyed on `(workflow_name, phase_name)`.

**Example output for `(bug, implementation)` phase:**

```
Create a TODO list now and work through it step by step:

[ ] Call get_project_plan to load TDD cycle deliverables
[ ] Identify the active TDD cycle from the planning document
[ ] Write the failing test (RED sub-phase) ...
[ ] Commit with sub_phase="red", cycle_number=N
...
[ ] Produce the Imp→QA hand-over block
```

**Why this matters:** `@imp` agents can autonomously execute all phases because
`transition_phase` has no built-in human-approval gate. `phase_instructions` is the
mechanism that scopes the agent to the current phase's expected behavior. It is returned
at invocation time, not embedded in a static file, so it can evolve without changing the
`.agent.md` file.

### 4.3 `sub_role_hint` — sub-role guidance

`sub_role_hint` maps the current phase to the correct `@imp` sub-role:

| Phase | Sub-role hint |
|-------|--------------|
| research | researcher |
| design | designer |
| planning | planner |
| implementation | implementer |
| validation | validator |
| documentation | documenter |
| ready | documenter |

This ensures the agent declares the correct sub-role without guessing from the phase name.

### 4.4 How `@imp` uses these fields

The `imp.agent.md` precedence chain is:

```
1. Runtime-injected system instructions
2. phase_instructions from get_work_context  ← overrides 3–6 when present
3. AGENTS.md
4. copilot-instructions.md
5. imp.agent.md (this file)
6. Latest user request
```

`phase_instructions` sits at precedence #2. When present, it is the authoritative
operational script for the session. The agent reads all lower-priority documents only
when `phase_instructions` is absent or explicitly directs it to do so.

---

## 5. Context Loading Order Per Session Type

### Default Copilot chat (no `@agent` invoked)

```
Always loaded:
  copilot-instructions.md        ← operational reference
  AGENTS.md                      ← coordination manifest
```

### `@co` session

```
Always loaded:
  copilot-instructions.md
  AGENTS.md

On @co invocation:
  .github/agents/co.agent.md     ← role persona, tool allowlist, sub-roles

Startup sequence (per co.agent.md):
  1. get_work_context
  2. list_issues(state="open")
  3. [tracker only] get_issue(320)
```

### `@imp` session

```
Always loaded:
  copilot-instructions.md
  AGENTS.md

On @imp invocation:
  .github/agents/imp.agent.md    ← role persona, full MCP tool access

Startup sequence (per imp.agent.md):
  1. get_work_context
     └─ if phase_instructions present → follow it as operational script
     └─ if absent → read AGENTS.md, copilot-instructions.md, then proceed
  2. ARCHITECTURE_PRINCIPLES.md  ← always binding
  3. [conditional] get_project_plan
  4. Inspect worktree for existing changes
  5. Inspect latest QA verdict
```

### `@qa` session

```
Always loaded:
  copilot-instructions.md
  AGENTS.md

On @qa invocation:
  .github/agents/qa.agent.md     ← role persona, read-only tool allowlist

Startup sequence (per qa.agent.md):
  1. AGENTS.md + copilot-instructions.md  ← always read first
  2. ARCHITECTURE_PRINCIPLES.md
  3. get_work_context
  4. get_project_plan for active issue
  5. Read active planning document
  6. Read changed files in worktree
  7. Read latest implementation hand-over
```

---

## 6. Instruction File Interaction Map

```
                            ┌─────────────────────────────────────┐
                            │         VS Code Chat Session         │
                            └──────────────┬──────────────────────┘
                                           │ always injected
                         ┌─────────────────┼──────────────────┐
                         │                 │                  │
               ┌─────────▼─────────┐  ┌───▼──────────────┐   │
               │ copilot-           │  │    AGENTS.md     │   │
               │ instructions.md   │  │                  │   │
               │                   │  │  • 3-agent model │   │
               │  • Tool matrix    │  │  • Hand-overs    │   │
               │  • TDD protocol   │  │  • Sub-roles     │   │
               │  • Quality gates  │  │  • 2-chat model  │   │
               │  • Architecture   │  └──────────────────┘   │
               │    contract       │                          │
               └───────────────────┘           when @agent invoked
                                               ┌─────────────▼──────┐
                                               │   *.agent.md       │
                                               │  co / imp / qa     │
                                               │                    │
                                               │  • tools: [...]    │
                                               │  • startup proto   │
                                               │  • role boundary   │
                                               └────────┬───────────┘
                                                        │ @imp calls
                                              ┌─────────▼───────────┐
                                              │  get_work_context   │
                                              │  (MCP tool)         │
                                              │                     │
                                              │  → sub_role_hint    │
                                              │  → phase_instruc-   │
                                              │    tions  [#2 prec] │
                                              └─────────────────────┘
```

---

## 7. Design Decisions and Rationale

### Why two always-on files instead of one?

Both `copilot-instructions.md` and `AGENTS.md` are always injected. Microsoft recommends
only one. The project deliberately keeps both for a split-responsibility design:
- `copilot-instructions.md` is understood by all editors and tools
- `AGENTS.md` carries the multi-agent protocol in the format VS Code 1.108+ prefers for
  its `chat.useAgentsMdFile` feature

The result is that both files are injected every session. This wastes context tokens but
gives maximum visibility of both the operational rules and the coordination model to all
agents, including default chat sessions with no specific agent invoked.

### Why `phase_instructions` via MCP and not in the `.agent.md` file?

Three reasons:
1. **Dynamic**: phase instructions change as the project evolves without requiring agent
   file changes. The lookup table in `GetWorkContextTool` is the single source of truth.
2. **Per-workflow**: different workflows (feature/bug/docs/refactor) have different phase
   instructions for the same phase name. A static file cannot express this without complex
   conditionals.
3. **Precedence position**: by returning `phase_instructions` at runtime, `@imp` can place
   it at precedence #2 (above all static files), making it the highest-authority script.
   This is not achievable with static embedded text.

### Why is `@qa` read-only enforced at the tool level, not by text?

Text instructions can be overridden by an autonomous agent under task pressure.
Tool restrictions in `tools:` frontmatter are enforced by VS Code before the model runs.
An `@qa` session physically cannot call `safe_edit_file` or `git_add_or_commit` because
those tools are not in its allowlist. This is hard enforcement, not soft guidance.

### Why does `@imp` use `tools: ["phase-gate-mcp/*"]` (wildcard)?

`@imp` is the implementation executor. It needs the full MCP surface. Maintaining an
explicit per-tool allowlist would require updating the agent file every time a new MCP
tool is added. The wildcard future-proofs the agent. The `@imp` role boundary is enforced
by the `.agent.md` body instructions and by QA review — not by tool restriction.

---

## 8. Adding a New Workflow Phase

If a new workflow is added to `workflows.yaml` and a new phase is added, the instruction
layer must be updated:

1. Add entries to `_PHASE_INSTRUCTIONS_MAP` in `mcp_server/tools/discovery_tools.py`
   for every `(workflow_name, phase_name)` tuple that should have instructions.
2. Add an entry to `_SUB_ROLE_MAP` if the phase needs a specific `@imp` sub-role hint.
3. Test with `get_work_context` on a branch in that workflow+phase to verify the output.

No changes to `.agent.md` files, `AGENTS.md`, or `copilot-instructions.md` are required
for new phases — those files are static infrastructure.

---

## Related Documentation

- **[tools/README.md][tools-ref]** — all 49 MCP tools with parameters and examples
- **[mcp_vision_reference.md][vision-ref]** — MCP server architecture and vision
- **[AGENTS.md][agents-md]** — three-agent coordination manifest
- **[.github/agents/imp.agent.md][imp-agent]** — implementation agent full spec
- **[.github/agents/qa.agent.md][qa-agent]** — QA agent full spec
- **[.github/agents/co.agent.md][co-agent]** — coordination agent full spec
- **[ARCHITECTURE_PRINCIPLES.md][arch-principles]** — binding architecture contract
- **[GIT_WORKFLOW.md][git-workflow]** — branch and commit conventions

<!-- Link definitions -->
[tools-ref]: tools/README.md
[vision-ref]: mcp_vision_reference.md
[agents-md]: ../../../AGENTS.md
[imp-agent]: ../../../.github/agents/imp.agent.md
[qa-agent]: ../../../.github/agents/qa.agent.md
[co-agent]: ../../../.github/agents/co.agent.md
[arch-principles]: ../../coding_standards/ARCHITECTURE_PRINCIPLES.md
[git-workflow]: ../../coding_standards/GIT_WORKFLOW.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-17 | Agent | Initial document — covers instruction hierarchy, three-agent model, MCP integration, context loading order |
