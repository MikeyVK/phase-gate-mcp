<!-- docs\development\issue333\planning.md -->
<!-- template=planning version=130ac5ea created=2026-05-12T09:47Z updated=2026-05-12 -->
# Agent Orchestration Files Cleanup (#333)

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-12

---

## Summary

Migrate all agent orchestration files to the VS Code-native model: `AGENTS.md` (workspace
root) as the always-on multi-agent protocol file; self-contained `.agent.md` bodies absorbing
`*_agent.md` root files; renamed `copilot-instructions.md` (leading dot removed) with stale
params fixed; 7 legacy prompt files archived; 3 additional entry points updated or deleted.

**Research basis:** `docs/development/issue333/research.md` (commits b143d22e, e3ee4a8f, c04eaec1)

---

## Purpose

The current setup has three structural problems that reduce reliability and portability:

1. `agent.md` is injected via `github.copilot.chat.codeGeneration.instructions.file` in
   `.vscode/settings.json` (gitignored). On a fresh clone this layer is absent.
2. `.github/.copilot-instructions.md` is not natively always-on (leading dot breaks
   VS Code auto-detect). It is only reachable via Markdown links — conditional on
   `chat.includeReferencedInstructions`.
3. Critical role content (`*_agent.md` root files) is only included when Markdown links
   are followed — not guaranteed.

Migration to `AGENTS.md` + self-contained `.agent.md` bodies eliminates all three issues.

---

## Scope In

1. Create `AGENTS.md` (workspace root) — multi-agent protocol from `agent.md`
2. Rename `.github/.copilot-instructions.md` → `.github/copilot-instructions.md` — fix
   leading dot, repair stale TDD params, repair stale workflow phase names
3. Rewrite `.github/agents/co.agent.md` — add `tools` + `handoffs` frontmatter; absorb
   `co_agent.md` into body
4. Rewrite `.github/agents/imp.agent.md` — add `tools` + `handoffs` frontmatter; absorb
   `imp_agent.md` into body
5. Rewrite `.github/agents/qa.agent.md` — add `tools` + `handoffs` frontmatter; absorb
   `qa_agent.md` into body
6. Delete `agent.md`, `co_agent.md`, `imp_agent.md`, `qa_agent.md`, `AGENT_PROMPT.md`
7. Archive 7 legacy prompt files to `.github/prompts/archive/`
8. Fix dead `session-state.json` reference in `resume-work.prompt.md`
9. Update `role_reset_snippets.md` — replace `*_agent.md` filename references with
   "select @qa / @imp and run startup protocol"
10. Update `.agent/reboot.md` — change `agent.md` → `AGENTS.md` in authority line

## Scope Out

- No changes to MCP server, backend, or test files
- No changes to prompt file content beyond the described fixes
- `implement-cycle.prompt.md` Phase 0 `activate_*` calls are not in scope (working correctly)

---

## Prerequisites

- Research phase completed (commit `c04eaec1`)
- **Post-merge manual setup (per developer — not committable):**
  - Update `.vscode/settings.json`:
    - Remove `github.copilot.chat.codeGeneration.instructions` entry for `agent.md`
    - Add `"chat.useAgentsMdFile": true`

---

## Implementation Steps

This is a documentation issue — no TDD cycles. Steps are sequential file operations.

### Step 1 — Create AGENTS.md
Content from `agent.md`: Phase 1 (Orientation), Phase 2 (Issue-First Workflow), Phase 3
(Execution Protocols), Phase 4 (Critical Directives), Phase 5 (Tool Priority Matrix),
ready-phase enforcement, `run_in_terminal` restrictions.  
Add three-agent model section (@co/@imp/@qa, two-chat model, hand-over contract).  
Fix: workflow types table missing `ready` as final phase.

### Step 2 — Rename + repair copilot-instructions.md
- Git-rename: `.github/.copilot-instructions.md` → `.github/copilot-instructions.md`
- Fix TDD commit params: `phase="red"` → `workflow_phase=... sub_phase=...`
- Fix workflow phase names: `tdd` → `implementation`, `integration` → `validation`

### Step 3 — Rewrite co.agent.md
Frontmatter additions:
```yaml
tools:
  - mcp_st3-workflow_get_work_context
  - mcp_st3-workflow_list_issues
  - mcp_st3-workflow_get_issue
  - mcp_st3-workflow_create_issue
  - mcp_st3-workflow_update_issue
  - mcp_st3-workflow_close_issue
  - mcp_st3-workflow_list_labels
  - mcp_st3-workflow_create_label
  - mcp_st3-workflow_list_milestones
  - mcp_st3-workflow_git_status
  - mcp_st3-workflow_git_list_branches
  - mcp_st3-workflow_search_documentation
  - mcp_st3-workflow_health_check
handoffs:
  - agent: imp
    condition: When coordination produces actionable implementation directive
```
Body: absorb full `co_agent.md` content (sub-roles, startup protocol, output contracts,
QA boundary). Remove Markdown link to `co_agent.md`.

### Step 4 — Rewrite imp.agent.md
Frontmatter additions:
```yaml
tools:
  - mcp_st3-workflow_*
handoffs:
  - agent: qa
    condition: When implementation cycle is complete and hand-over is produced
```
Body: absorb full `imp_agent.md` content (scope lock, architectural purity rules, test
refactor discipline, hand-over format, QA boundary). Remove Markdown links to `agent.md`
and `imp_agent.md`.

### Step 5 — Rewrite qa.agent.md
Frontmatter additions:
```yaml
tools:
  - mcp_st3-workflow_get_work_context
  - mcp_st3-workflow_run_tests
  - mcp_st3-workflow_run_quality_gates
  - mcp_st3-workflow_git_status
  - mcp_st3-workflow_git_diff_stat
  - mcp_st3-workflow_git_list_branches
  - mcp_st3-workflow_search_documentation
  - mcp_st3-workflow_get_issue
  - mcp_st3-workflow_list_issues
  - mcp_st3-workflow_health_check
handoffs:
  - agent: imp
    condition: NOGO verdict — implementation corrections required
  - agent: co
    condition: Scope or planning issue requiring coordination
```
Body: absorb full `qa_agent.md` content (suppression audit — CRITICAL, 8 core QA questions,
review standard, scope determination). Remove Markdown links to `agent.md` and `qa_agent.md`.

### Step 6 — Delete legacy root files
Delete: `agent.md`, `co_agent.md`, `imp_agent.md`, `qa_agent.md`, `AGENT_PROMPT.md`

### Step 7 — Archive legacy prompts
Move to `.github/prompts/archive/`:
- `start-work.prompt.md`
- `resume-work.prompt.md`
- `prepare-handover.prompt.md`
- `prepare-qa-brief.prompt.md`
- `prepare-implementation-brief.prompt.md`
- `request-review.prompt.md`
- `plan-executionDirectiveBatchCoordination.prompt.md`

Verify post-archive: only `open-issue.prompt.md` and `implement-cycle.prompt.md` remain
in `.github/prompts/` root.

### Step 8 — Fix resume-work.prompt.md
Remove line 17: `4. Read .copilot/session-state.json if it exists — ...`  
(File will be in archive by this step — fix before moving, or fix in archive.)

### Step 9 — Update role_reset_snippets.md
Replace snippet text that references `qa_agent.md` → `"Select @qa in the Chat view and
run the startup protocol (get_work_context, list_issues)."`  
Replace snippet text that references `imp_agent.md` → `"Select @imp in the Chat view and
run the startup protocol (get_work_context)."`

### Step 10 — Update .agent/reboot.md
Change `Authority: Read \`agent.md\` for full context.`  
→ `Authority: Read \`AGENTS.md\` for full context.`

---

## Risks

| Risk | Mitigation |
|------|-----------|
| `AGENTS.md` file size: full `agent.md` content may make always-on context very large | Keep AGENTS.md to multi-agent protocol only; omit detailed tool matrix; cross-reference to docs/ for deep reference |
| `.vscode/settings.json` is gitignored: post-merge settings update not enforceable | Document in PR description as mandatory manual step |
| VS Code may not scan `.github/prompts/archive/` subdirectory for slash commands | Verify in VS Code after archiving; if archive files still appear, rename to `_archived-*.prompt.md` pattern as fallback |
| `chat.useAgentsMdFile` not yet enabled: `AGENTS.md` will be committed but inactive | Document as prerequisite; current `agent.md` injection continues to work until the developer updates their settings |

---

## Related Documentation

- [docs/development/issue333/research.md](research.md)
- [docs/architecture/VSCODE_AGENT_ORCHESTRATION.md](../../architecture/VSCODE_AGENT_ORCHESTRATION.md)
- VS Code custom agents: https://code.visualstudio.com/docs/copilot/customization/custom-agents
- VS Code custom instructions: https://code.visualstudio.com/docs/copilot/customization/custom-instructions

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-12 | Agent | Initial planning |
