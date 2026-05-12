# path: docs/development/issue333/research.md
# template=research version=2 created=2026-05-12 updated=2026-05-12

# Agent File Inventory & VS Code Authoritative Chain Analysis

## Purpose

Complete inventory of all agent orchestration files in the S1mpleTrader V3 workspace,
with their current content summarised, verified against official VS Code/GitHub Copilot
documentation (fetched 2026-05-12), and assessed for correctness, role clarity, and
injection behaviour.

---

## Problem Statement

The project has accumulated multiple agent orchestration files over time (`.github/agents/`,
`.github/prompts/`, `.github/.copilot-instructions.md`, `agent.md`, `co_agent.md`,
`imp_agent.md`, `qa_agent.md`). The authoritative chain between them must be verified
against official VS Code documentation to eliminate contradictions, reduce friction, and
ensure correct auto-injection behaviour so that agents operate with a single source of
truth per concern, without repetition or conflicting directives.

---

## Goals

1. Inventory all agent orchestration files and document their current content summary.
2. Verify the project's described authoritative chain against official VS Code docs.
3. Identify discrepancies between intended purpose and actual VS Code behaviour per file.
4. Define the correct minimal chain per Microsoft documentation.
5. Produce a concrete, actionable change plan for issue #333.

---

## Source Documentation

Official VS Code documentation fetched on 2026-05-12:

- https://code.visualstudio.com/docs/copilot/customization/custom-instructions
- https://code.visualstudio.com/docs/copilot/customization/custom-agents
- https://code.visualstudio.com/docs/copilot/customization/prompt-files

All quotes below are verbatim from these pages.

---

## Part 1 — Official VS Code File Types and Their Purpose

### 1.1 `copilot-instructions.md`

**Official location:** `.github/copilot-instructions.md`  
**Auto-detect:** Yes — VS Code auto-detects the file at exactly `.github/copilot-instructions.md`.  
**Injection:** Always-on. Included in every chat request in the workspace.  
**Purpose per docs:** "Coding style and naming conventions that apply across the project /
Technology stack declarations and preferred libraries / Architectural patterns to follow or
avoid / Security requirements and error handling approaches / Documentation standards."  
**NOT for:** Role definition, persona, tool restrictions, agent-to-agent handoffs.  
**Priority:** Repository level — below personal (user-level) instructions.

### 1.2 `*.agent.md` (custom agents)

**Official location:** `.github/agents/` folder (configurable via `chat.agentFilesLocations`).  
**Auto-detect:** Yes — VS Code detects any `.md` file in `.github/agents/`.  
**Injection:** Conditional — body is "prepended to the user chat prompt" only when the user
selects that agent in the Chat view.  
**Purpose per docs:** "Configure the AI to adopt different personas tailored to specific
development roles and tasks. Each persona can have its own behaviour, available tools, and
instructions."  
**Key fields:** `name`, `description`, `argument-hint`, `tools`, `agents`, `model`,
`handoffs`, `target`.  
**Authority:** THE authoritative place for role definition, tool restrictions, and handoffs.
Not "generic" — workspace-specific and fully authoritative for that agent's behaviour.

### 1.3 `*.instructions.md` (file-based instructions)

**Official location:** `.github/instructions/` folder.  
**Auto-detect:** Conditional — applied when files match `applyTo` glob pattern.  
**Purpose per docs:** "Different conventions for frontend vs. backend code / Language-specific
guidelines in a monorepo / Framework-specific patterns for specific modules / Specialized
rules for test files or documentation."  
**Currently:** NOT used in this project. The gap is documented here for completeness.

### 1.4 `*.prompt.md` (prompt files / slash commands)

**Official location:** `.github/prompts/` folder.  
**Auto-detect:** No — manually invoked via `/name` in the Chat view.  
**Purpose per docs:** "Simplify prompting for common tasks, such as scaffolding a new
component, running and fixing tests, or preparing a pull request."  
**Key fields:** `name`, `description`, `agent`, `tools`, `model`, `argument-hint`.  
**Tool priority:** Prompt file tools > referenced agent tools > default agent tools.

### 1.5 `AGENTS.md`

**Official location:** Workspace root (or subfolders in experimental mode).  
**Auto-detect:** Always-on (like `copilot-instructions.md`), if `chat.useAgentsMdFile` is
enabled.  
**Purpose:** Alternative to `copilot-instructions.md`, useful when multiple AI agents must
share a single instruction set.  
**Currently:** NOT used in this project.

### 1.6 Instruction priority (official)

When multiple instruction types conflict, priority is:

1. Personal / user-level instructions (highest)
2. Repository instructions (`.github/copilot-instructions.md` or `AGENTS.md`)
3. Organization-level instructions (lowest)

`.agent.md` body content is injected in addition to, not instead of, instructions.
Referenced files via Markdown links are only included when `chat.includeReferencedInstructions`
is enabled (default state varies by installation).

---

## Part 2 — Complete File Inventory

### FILE 1: `.github/.copilot-instructions.md`

**VS Code type:** Intended as always-on instructions file.  
**Filename issue:** The file is named `.copilot-instructions.md` (with a leading dot), stored
in `.github/`. The VS Code auto-detect path is `.github/copilot-instructions.md` (no leading
dot). This means VS Code does NOT auto-detect this file via the standard mechanism. It is
instead injected by the extension via `modeInstructions` in the YAML frontmatter of the
`.agent.md` files, or via a configured `chat.instructionsFilesLocations` entry. This is a
**de facto non-standard setup** — it works, but only through project-specific tooling, not
the VS Code native mechanism.

**Current content summary:**
- Architecture contract reference to `ARCHITECTURE_PRINCIPLES.md`
- Tool Priority Matrix (git, GitHub, file ops, quality/testing, project management)
- `run_in_terminal` restriction rules
- TDD cycle protocol — uses **stale parameter names**: `phase="red"` instead of
  `workflow_phase=... sub_phase=...`
- Prime Directives (7 laws + 8th type-checking law)
- Workflow Types table — uses **stale phase names**: `tdd`, `integration` instead of
  `implementation`, `validation` (as in current `workflows.yaml`)
- Scaffolding table
- Key Documentation links
- Agent Cooperation section (content to be read below)

**Agent Cooperation section content:**
Describes a three-agent model (@co, @imp, @qa) briefly — but this section is at the very
end of the file and is **incomplete**: it does not describe the role boundaries, hand-over
contracts, or startup protocols.

**Assessment:**
- ✅ Correct VS Code intent (always-on coding standards)
- ❌ Wrong filename — not auto-detected by VS Code natively
- ❌ TDD commit parameter names stale (`phase=` → should be `workflow_phase=`/`sub_phase=`)
- ❌ Workflow phase names stale (`tdd`/`integration` → `implementation`/`validation`)
- ❌ Agent Cooperation section is thin — real role detail belongs in `.agent.md` bodies
- ℹ️ Role description content is partially duplicated across this file and `agent.md`

---

### FILE 2: `agent.md` (workspace root)

**VS Code type:** Plain Markdown — NOT a recognized VS Code customization file.  
**Injection:** Not auto-injected by VS Code. Referenced via Markdown links from `.agent.md`
body files and `copilot-instructions.md`. Injected into this session via extension
`modeInstructions` YAML key.  
**Intended purpose:** Full project reference — workflow, tool matrix, TDD cycle, phase
management, all MCP tools.

**Current content summary:**
- Phase 1: Orientation Protocol (tool activation, state sync)
- Phase 2: Issue-First Development Workflow (create_issue, branch, phases, TDD cycles)
- Phase 3: Execution Protocols (Implement Component, Create Documentation, Labels)
- Phase 4: Critical Directives (Prime Directives)
- Phase 5: Tool Priority Matrix (comprehensive — git, GitHub, labels, milestones, PRs,
  scaffolding, quality, discovery, MCP server management, file editing)
- Ready-Phase Enforcement details (PR blocking rules)
- `run_in_terminal` restrictions

**Assessment:**
- ✅ Comprehensive and accurate tool matrix
- ✅ Correct workflow types and phase names
- ❌ Does NOT mention the three-agent model (@co/@imp/@qa) anywhere
- ❌ Workflow types table in Phase 2 section is missing `ready` as final phase (present in
  `workflows.yaml` but not documented here)
- ❌ Large overlap with `copilot-instructions.md` (tool matrix duplicated in both)
- ℹ️ Primary value: full authoritative reference that agents actively read on startup

---

### FILE 3: `.github/agents/co.agent.md`

**VS Code type:** Custom agent — `.github/agents/` folder. Auto-detected. ✅  
**Injection:** When `@co` is selected by user.

**Current frontmatter:**
```yaml
name: co
description: Coordination role wrapper for VS Code orchestration on this repository.
argument-hint: "Sub-role + task. Sub-roles: triager (default), backlog-reviewer, tracker, issue-author. Example: ..."
target: vscode
```

**Current body summary:**
- Declares role: coordination authority, no production code.
- Orchestration section: sub-role declaration, context entry (get_work_context + list_issues),
  hand-over contract.
- Role boundary: read-only for code; allowed to create/update issues, labels, milestones.
- Norms: points to `agent.md` and `co_agent.md` via Markdown links.
- Two-chat model statement.

**Assessment:**
- ✅ Correct VS Code agent format
- ✅ Concise and role-focused
- ⚠️ Body defers to `co_agent.md` via Markdown link — this content is only guaranteed to
  be included if `chat.includeReferencedInstructions` is enabled. If disabled, agents operate
  on a weaker basis.
- ❌ Missing `tools` field in frontmatter — no tool restriction specified. Currently any
  tool available in chat is accessible from @co, which contradicts the role boundary
  (read-only for code, no commits).
- ❌ Missing `handoffs` — no structured hand-over to @imp defined at the VS Code level.

---

### FILE 4: `.github/agents/imp.agent.md`

**VS Code type:** Custom agent — `.github/agents/` folder. Auto-detected. ✅  
**Injection:** When `@imp` is selected by user.

**Current frontmatter:**
```yaml
name: imp
description: Implementation role wrapper for VS Code orchestration on this repository.
argument-hint: "Sub-role + task. Sub-roles: researcher (default), planner, designer, implementer, validator, documenter. Example: ..."
target: vscode
```

**Current body summary:**
- Declares role: execution agent.
- Orchestration section: sub-role declaration, `get_work_context` on startup, sub_role_hint
  handling, hand-over production.
- Norms: points to `agent.md` and `imp_agent.md` via Markdown links.
- Two-chat model statement.

**Assessment:**
- ✅ Correct VS Code agent format
- ✅ Correct startup protocol reference
- ⚠️ Same dependency on `chat.includeReferencedInstructions` for linked files.
- ❌ Missing `tools` field — no tool restriction. The implementer should have a specific
  tool set (all MCP tools + file editing) defined explicitly.
- ❌ Missing `handoffs` — no structured hand-over to @qa defined at VS Code level.

---

### FILE 5: `.github/agents/qa.agent.md`

**VS Code type:** Custom agent — `.github/agents/` folder. Auto-detected. ✅  
**Injection:** When `@qa` is selected by user.

**Current frontmatter:**
```yaml
name: qa
description: QA role wrapper for VS Code orchestration on this repository.
argument-hint: "Sub-role + review target. Sub-roles: design-reviewer (default), plan-verifier, verifier, validation-reviewer, doc-reviewer. Example: ..."
target: vscode
```

**Current body summary:**
- Declares role: read-only QA authority.
- Orchestration section: sub-role declaration, `get_work_context` on startup,
  hand-over anchoring.
- Role boundary: read-only by default; allowed to run tests and quality gates.
- Norms: points to `agent.md` and `qa_agent.md` via Markdown links.
- Two-chat model statement.

**Assessment:**
- ✅ Correct VS Code agent format
- ✅ Read-only role boundary correctly stated
- ⚠️ Same `chat.includeReferencedInstructions` dependency.
- ❌ Missing `tools` field — QA should be restricted to read-only tools (no `editFiles`,
  no `git_*` mutations, no `submit_pr`).
- ❌ Missing `handoffs` — no structured return to @imp after NOGO verdict.

---

### FILE 6: `co_agent.md` (workspace root)

**VS Code type:** Plain Markdown — NOT a recognized VS Code customization file.  
**Injection:** Only when `chat.includeReferencedInstructions` is enabled and the model follows
the Markdown link in `co.agent.md`.

**Current content summary:**
- Mission statement: coordination authority, triage/review/track/author.
- Precedence order: runtime > agent.md > copilot-instructions.md > this file > user request.
- Sub-roles with detailed scope: triager, backlog-reviewer, tracker, issue-author.
- Startup Protocol After Context Compaction: what to read + what to call.
- QA Boundary: coordination does not adjudicate implementation quality.
- Output Contracts: structured table format for backlog-reviewer/tracker + issue body
  format for issue-author + hand-over block format for @imp.

**Assessment:**
- ✅ Detailed and well-structured sub-role definitions
- ✅ Correct precedence order
- ⚠️ Only reliably included if referenced-instructions is enabled
- ℹ️ The sub-role definitions, output contracts, and startup protocol here are exactly the
  kind of content that should be in `co.agent.md` body directly — not in a separate file.

---

### FILE 7: `imp_agent.md` (workspace root)

**VS Code type:** Plain Markdown — NOT a recognized VS Code customization file.  
**Injection:** Only when `chat.includeReferencedInstructions` is enabled.

**Current content summary:**
- Mission: execute current cycle exactly, follow architecture, produce verifiable hand-over.
- QA Boundary: does not declare GO; no self-reinterpretation of planning.
- Precedence order.
- Startup Protocol After Context Compaction: what to read + what to call.
- Scope Lock: scope defined by intersection of user request + current cycle + deliverables.
- Architecture Contract: binding reference to ARCHITECTURE_PRINCIPLES.md.
- Architectural Purity During Refactors: config schemas as pure value objects, no
  cross-config orchestration state in schemas.
- Test Refactor Within Cycle: blast-radius test updates required in same cycle.
- Working Style: smallest coherent change set.
- Interaction With QA: concrete falsifiable hand-overs, no overclaiming.
- Planning and Deliverables Discipline: may not self-edit planning.
- Temporary Compatibility Layers: allowed only when plan explicitly stages removal.
- Test and Verification Discipline: run targeted tests before hand-over.

**Assessment:**
- ✅ Extremely detailed and precise — highest information density of all agent files
- ✅ Strong architecture enforcement guidance
- ⚠️ Only reliably included if referenced-instructions is enabled
- ℹ️ Key sections (Scope Lock, QA Boundary, Architecture Contract) are critical enough
  to warrant guaranteed injection, not link-dependent inclusion.

---

### FILE 8: `qa_agent.md` (workspace root)

**VS Code type:** Plain Markdown — NOT a recognized VS Code customization file.  
**Injection:** Only when `chat.includeReferencedInstructions` is enabled.

**Current content summary:**
- Mission: skeptical, precise, fair QA authority.
- Role Boundaries: read-only by default; no code/test/commit edits.
- Precedence order.
- Startup Protocol After Context Compaction.
- How To Determine Scope: intersection of user request + hand-over + cycle + deliverables.
- Core QA Questions: 8 ordered questions for every review.
- Architectural Purity Checks: schema purity, cross-config contamination patterns.
- Suppression Audit: ruff noqa header detection rules, permitted vs forbidden suppressions.
- Review Standard: priority order for findings (GO/NOGO/CONDITIONAL GO).
- New Production Code vs Temporary Compatibility Layers: judgment criteria.

**Assessment:**
- ✅ Detailed, operationally precise review standard
- ✅ Suppression Audit section is particularly critical (prevents silent quality degradation)
- ⚠️ Only reliably included if referenced-instructions is enabled
- ℹ️ Suppression Audit and Core QA Questions are too critical for link-dependent injection.

---

### FILE 9 — 17: `.github/prompts/*.prompt.md` (9 files)

All prompt files are in `.github/prompts/` — correct location per VS Code docs. ✅  
All use `.prompt.md` extension. ✅  
All are manually invoked via `/name`. ✅

| File | `name` | `agent` | Purpose summary |
|------|--------|---------|-----------------|
| `open-issue.prompt.md` | `open-issue` | `co` | Bootstrap new issue branch end-to-end |
| `start-work.prompt.md` | `start-work` | `imp` | Start fresh impl session before coding |
| `resume-work.prompt.md` | `resume-work` | `imp` | Rebuild impl context after compaction |
| `implement-cycle.prompt.md` | `implement-cycle` | `imp` | Full TDD cycle with Explore sub-agent |
| `prepare-handover.prompt.md` | `prepare-handover` | `imp` | Structured hand-over for QA chat |
| `prepare-qa-brief.prompt.md` | `prepare-qa-brief` | `imp` | Deep copy-paste QA prompt block |
| `request-review.prompt.md` | `request-review` | `qa` | Start separate QA review chat |
| `prepare-implementation-brief.prompt.md` | `prepare-implementation-brief` | `qa` | Deep copy-paste impl prompt from QA |
| `plan-executionDirectiveBatchCoordination.prompt.md` | *(no name field)* | *(none)* | Old design discussion doc — NOT a real slash command |

**Assessment:**
- ✅ 8 of 9 are correct VS Code prompt files
- ❌ `plan-executionDirectiveBatchCoordination.prompt.md` has no frontmatter `name` field
  and is not a prompt — it's a stale design discussion document that accidentally has a
  `.prompt.md` extension. It will appear in the `/` command list with its full filename.
- ⚠️ `start-work.prompt.md` and `resume-work.prompt.md` reference a `.copilot/session-state.json`
  file that does not exist in the repo. This is dead reference.
- ⚠️ `implement-cycle.prompt.md` uses `activate_*` tool calls (Phase 0) that are specific
  to the MCP lazy-loading model. These work correctly but should be reviewed when MCP
  activation model changes.

---

## Part 3 — Chain Assessment

### 3.1 What the user described vs official reality

| User's described layer | Official reality | Verdict |
|---|---|---|
| `agent.md` = project-specific working method | Plain markdown, not VS Code-recognized. Injected via extension `modeInstructions` or Markdown links only. | ✅ Purpose correct — but injection is non-standard |
| `copilot-instructions.md` = "what is the role? auto-injected every prompt?" | Always-on ✅, but purpose = **coding standards/conventions**, NOT role definition. Role is in `.agent.md`. | ❌ Purpose mislabelled |
| `*.agent.md` = generic role descriptions | These ARE the authoritative role/persona definitions. Body prepended to user prompt when selected. Not "generic" — workspace-specific and fully authoritative. | ❌ Understated — they are THE authority |
| `*_agent.md` = further elaboration, workspace-specific | NOT a VS Code concept. Included only if `chat.includeReferencedInstructions` enabled. | ✅ Purpose correct — but injection not guaranteed |
| Slash commands = prompts | Correct. `.prompt.md` in `.github/prompts/`. | ✅ Correct |

### 3.2 Authoritative chain per official VS Code docs

```
Always-on (every request):
  .github/copilot-instructions.md   → coding standards, conventions, tool rules

Conditional (agent selected):
  .github/agents/co.agent.md        → @co persona, tools, role boundary, handoffs
  .github/agents/imp.agent.md       → @imp persona, tools, role boundary, handoffs
  .github/agents/qa.agent.md        → @qa persona, tools, role boundary, handoffs

Referenced (if chat.includeReferencedInstructions enabled):
  co_agent.md                       → detailed sub-role elaboration
  imp_agent.md                      → detailed scope, architecture, test discipline
  qa_agent.md                       → detailed review standard, suppression audit
  agent.md                          → full project reference

Manual invocation (slash commands):
  .github/prompts/*.prompt.md       → task-specific workflows
```

### 3.3 Critical gaps identified

| Gap | Severity | Location |
|---|---|---|
| `.agent.md` bodies missing `tools` field — no tool restriction enforced at VS Code level | High | All 3 `.agent.md` files |
| `.agent.md` bodies missing `handoffs` — no structured agent transitions at VS Code level | Medium | All 3 `.agent.md` files |
| `copilot-instructions.md` filename has leading dot — not auto-detected by VS Code natively | High | `.github/.copilot-instructions.md` |
| TDD commit params stale in `copilot-instructions.md` (`phase=` → `workflow_phase=`/`sub_phase=`) | High | `.github/.copilot-instructions.md` |
| Workflow phase names stale in `copilot-instructions.md` (`tdd`/`integration` → `implementation`/`validation`) | High | `.github/.copilot-instructions.md` |
| `agent.md` does not mention three-agent model (@co/@imp/@qa) | Medium | `agent.md` |
| `agent.md` workflow types table missing `ready` as final phase | Low | `agent.md` |
| Tool matrix duplicated between `agent.md` and `copilot-instructions.md` | Low | Both |
| `plan-executionDirectiveBatch...prompt.md` is a stale doc with `.prompt.md` extension | Medium | `.github/prompts/` |
| `start-work` and `resume-work` reference non-existent `.copilot/session-state.json` | Low | 2 prompt files |
| `*_agent.md` files are critical (suppression audit, scope lock, etc.) but inclusion not guaranteed | High | `co_agent.md`, `imp_agent.md`, `qa_agent.md` |

---

## Part 4 — What a Correct Setup Looks Like

Per Microsoft documentation and the project's three-agent model, the minimal correct setup is:

### `.github/copilot-instructions.md` (rename: remove leading dot)
**Content:** coding standards, tool priority matrix, architecture contract reference, prime
directives, `run_in_terminal` restrictions, TDD cycle (with correct parameter names),
workflow types (with correct phase names), scaffolding reference.  
**NOT in here:** role descriptions, persona, tool restrictions per agent.

### `.github/agents/co.agent.md`
**Content:**  
- Frontmatter: `tools` list (read-only: get_*, list_*, search_*, create_issue,
  update_issue, close_issue, create_label, etc. — NO file editing, NO commits, NO git push)
- Frontmatter: `handoffs` to @imp and optionally @qa
- Body: role, sub-roles, startup protocol, output contracts, QA boundary
**Goal:** Body should be self-sufficient. Link to `co_agent.md` for deep sub-role detail
(depends on `chat.includeReferencedInstructions`), but critical constraints must be in the body.

### `.github/agents/imp.agent.md`
**Content:**  
- Frontmatter: `tools` list (all MCP tools + file editing)
- Frontmatter: `handoffs` to @qa
- Body: role, sub-roles, startup, scope lock, architecture contract ref, hand-over format
**Goal:** Body self-sufficient for the core protocol.

### `.github/agents/qa.agent.md`
**Content:**  
- Frontmatter: `tools` list (read-only: run_tests, run_quality_gates, read-only git/file)
- Frontmatter: `handoffs` back to @imp (NOGO path)
- Body: role, sub-roles, startup, suppression audit rule (critical — must be in body),
  core QA questions, review standard

### `agent.md` (workspace root)
**Content:** Full reference document. Add three-agent model section. Fix workflow types
table. Reduce tool matrix duplication with `copilot-instructions.md` by keeping the
complete matrix here and a minimal summary there.

### `*_agent.md` files (workspace root)
**Status:** Remain as detailed elaboration. Their inclusion depends on
`chat.includeReferencedInstructions`. The most critical content from each (suppression
audit, scope lock, QA boundary) should be mirrored in the `.agent.md` body to guarantee
injection.

---

## Findings Summary

1. The filename `.github/.copilot-instructions.md` (with leading dot) breaks VS Code
   native auto-detect. The file is injected through non-standard means only.
2. The `.agent.md` files are structurally correct but incomplete — missing `tools` and
   `handoffs` frontmatter fields that VS Code uses to enforce role boundaries.
3. The most critical operational rules (suppression audit, scope lock, QA questions) are
   only in `*_agent.md` files whose inclusion is not guaranteed.
4. `copilot-instructions.md` contains stale TDD commit parameters and stale workflow
   phase names that actively mislead agents.
5. `agent.md` is accurate and comprehensive on the tool matrix but does not describe the
   three-agent model — a gap for onboarding.
6. One prompt file (`plan-executionDirectiveBatch...`) is a stale document masquerading
   as a slash command.
7. Two prompt files reference a non-existent session state file.

---

## Questions

1. Should `tools` in `.agent.md` frontmatter enumerate all st3-workflow MCP tools
   individually, or is the `st3-workflow/*` wildcard format sufficient for MCP tools?
   *(Official docs: "To include all tools of an MCP server, use the `<server name>/*` format.")*
2. Should `handoffs` be added now or in a separate issue?
3. Should `chat.includeReferencedInstructions` be documented as a project prerequisite,
   or should the critical content be fully migrated into `.agent.md` bodies?

---

## References

- VS Code custom instructions: https://code.visualstudio.com/docs/copilot/customization/custom-instructions
- VS Code custom agents: https://code.visualstudio.com/docs/copilot/customization/custom-agents
- VS Code prompt files: https://code.visualstudio.com/docs/copilot/customization/prompt-files
- `chat.includeReferencedInstructions` setting: controls whether Markdown-linked instruction files are included
- `chat.agentFilesLocations` setting: configures additional agent file locations
