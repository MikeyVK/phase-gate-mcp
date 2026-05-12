<!-- docs\development\issue268\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-12T14:35Z updated=2026-05-12 -->
# MCP-Tool-First Orchestration: get_work_context + create_handover

**Status:** DRAFT
**Version:** 1.0
**Last Updated:** 2026-05-12

---

## Problem Statement

Hooks-based model context injection is empirically dead (#263 Findings 7/8: all three
injection paths — UPS systemMessage, PreCompact systemMessage, Stop reason — do not reach
the model). The only reliable context injection path is via MCP tool-call responses. Agent
startup currently relies on reading static markdown files and manual phase detection, with no
machine-enforced handover validation. Two tools are needed: an extended `get_work_context`
that delivers role/sub-role/phase expectations in one call, and a new `create_handover` that
validates handover fields against a YAML-defined SubRoleSpec.

---

## Goals

1. Define `get_work_context` extension schema (`sub_role_hint`, `phase_expectations`, `handover_template`)
2. Define `create_handover` input schema and validation contract
3. Map canonical 7-step startup sequence to a machine-triggerable orchestration step
4. Identify reusable code from `feature/263` branch

---

## Scope

**In scope:**
- `get_work_context` response schema extension
- `create_handover` tool design
- SubRoleSpec YAML config structure
- Startup sequence orchestration (7-step sequence)
- Connection to #333 AGENTS.md startup protocol

**Out of scope:**
- Hooks infrastructure (confirmed dead in #263)
- `content_contract` gate from #258 (superseded, see #258 closing comment)
- VS Code extension internals

---

## Background

Issue #263 (`feature/263-vscode-implementation-orchestration`) empirically confirmed that
all three hook injection paths cannot reach the model. Finding 8 confirmed that agent files
(`.agent.md`) do work reliably. Issue #333 built on this by establishing AGENTS.md as the
three-agent model authority with a human startup protocol:

> "Read AGENTS.md → `get_work_context` → `get_project_plan` → read planning doc"

This human protocol is the authoritative specification that #268 must make instrument-driven.

---

## Findings

### F_268.1 — Canonical startup sequence (7 steps)

The canonical sequence for starting work on a new issue:

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `get_issue(issue_number)` | Understand scope and context |
| 2 | `create_branch(name, base_branch, branch_type)` | Create + auto-checkout |
| 3 | `initialize_project(issue_number, issue_title, workflow_name, parent_branch)` | Initialize phase state |
| 4 | `get_project_plan(issue_number)` | Verify phases and exit criteria |
| 5 | `get_work_context()` | Confirm active phase, issue, blockers |
| 6 | `git_add_or_commit(message, workflow_phase)` | Commit state files |
| 7 | `git_push(set_upstream=True)` | Push branch to remote |

Steps 4 and 5 are currently absent from `open-issue.prompt.md` and from any tool response.
This is the core gap that #268 must close.

### F_268.2 — open-issue.prompt.md is the correct landing target (Optie A)

The `.github/prompts/open-issue.prompt.md` slash command created in #333 already covers
steps 1–3 + 6–7. It is missing `get_project_plan` (step 4) and `get_work_context` (step 5).
These two calls must be added between `initialize_project` and the first commit, so the agent
context is fully loaded before work begins.

**Action:** Add steps 4–5 to `open-issue.prompt.md` in the planning or implementation phase.

### F_268.3 — get_work_context extension: sub_role_hint + phase_expectations

The current `get_work_context` response returns: branch, linked issue, phase, recent commits.
Required extensions:

| New field | Source | Content |
|-----------|--------|---------|
| `sub_role_hint` | phase → sub-role map in SubRoleSpec YAML | e.g. `phase=research → sub_role=researcher` |
| `phase_expectations` | SubRoleSpec YAML for active sub-role | What the agent must produce this phase |
| `handover_template` | SubRoleSpec.required_fields | The required fields for the crosschat handover block |

Source YAML: `.copilot/sub-role-requirements.yaml` from `feature/263` (cherry-pick candidate).
Config root question: move to `.phase-gate/config/` to match current convention?

### F_268.4 — create_handover: YAML-driven field validation

`create_handover` validates a handover dict against SubRoleSpec.required_fields. Contract:

- **Input:** `sub_role: str`, `fields: dict[str, str]`
- **Validation:** missing fields → `HandoverValidationError` with list of missing keys
- **On success:** format handover block as Markdown, optionally write to `.phase-gate/temp/`
- **Schema:** dynamic per sub-role, driven by YAML config
- **Reusable from #263:** `requirements_loader.py`, `interfaces.py` (SubRoleSpec), `_default_requirements.yaml`

### F_268.5 — #333 AGENTS.md startup protocol is the authoritative human specification

AGENTS.md §1.2 State Synchronization defines the human startup protocol. The `get_work_context`
extension makes this protocol instrument-driven: instead of reading static docs, the tool
response delivers the same information as structured data. The agent reads one tool response
and has everything: phase, sub-role hint, what to produce, handover template.

### F_268.6 — Reusable code from feature/263 (cherry-pick targets)

Cherry-pick targets (DO NOT take `hooks/` package — confirmed dead):

| File | Purpose |
|------|---------|
| `src/copilot_orchestration/config/requirements_loader.py` | Backend for SubRoleSpec loading |
| `src/copilot_orchestration/contracts/interfaces.py` | SubRoleSpec datatype |
| `src/copilot_orchestration/utils/_paths.py` | State file path resolver |
| `.copilot/sub-role-requirements.yaml` | Sub-role config + handover fields |
| `.copilot/_default_requirements.yaml` | Default sub-role config |

---

## Open Questions

1. Does the SubRoleSpec YAML from feature/263 already cover all sub-roles in the
   three-agent model (`@co` triager/backlog-reviewer/tracker/issue-author,
   `@imp` researcher/planner/designer/implementer/validator/documenter,
   `@qa` design-reviewer/plan-verifier/verifier/validation-reviewer/doc-reviewer)?

2. Should `create_handover` write to `.phase-gate/temp/` (persistent) or return
   content-only (ephemeral)?

3. Should the `get_work_context` extension be backward-compatible (new fields
   optional/additive) or a versioned breaking change?

4. Where does the YAML config live: `.copilot/` (as in #263) or `.phase-gate/config/`
   (current project convention)?

---

## References

- Issue #268 (this issue)
- `feature/263-vscode-implementation-orchestration` branch (cherry-pick source; not merged to main)
- Issue #333 results: `AGENTS.md` §1.2 Startup Protocol, `.github/prompts/open-issue.prompt.md`
- Issue #258 (closed): content_contract gate — superseded by #268 approach
- Issue #290 (parent epic): Workflow Intelligence / Agent UX
- `docs/reference/mcp/tools/README.md` — `get_work_context` current spec (Discovery & Admin section)
